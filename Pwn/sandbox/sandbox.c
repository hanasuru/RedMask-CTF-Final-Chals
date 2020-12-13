#include <elf.h>
#include <err.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unicorn/unicorn.h>
#include <unistd.h>

#define USER_ADDRESS 0x4000000
#define USER_STACK 0x7ffffffff000
#define MAPPING_SIZE 0x100000

char *USER_STACK_MEM[MAPPING_SIZE] = {0};
const char flag[] = "redmask{ez_pz__lem0n_squeezY_fix3fix3fix3fix7}";
char *cache[6] = {0};

void handler() {
  puts("too long");
  exit(0);
}

void setup() {
  signal(SIGALRM, handler);
  alarm(180);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

struct Mapped {
  size_t start;
  size_t len;
  size_t flags;
  void *mem;
} Mapped;

struct Mapped sections[0x100];
size_t num_sections = 0;

void *load_file(const char *path, size_t *size) {
  int fd = open(path, O_RDONLY);
  if (fd <= 0) {
    err(1, "cannot open file");
  }

  size_t len = lseek(fd, 0, SEEK_END);
  void *p = mmap(NULL, len, PROT_READ, MAP_PRIVATE, fd, 0);
  if (p <= 0) {
    err(1, "cannot mmap file");
  }
  close(fd);
  *size = len;
  return p;
}

size_t map_elf(uc_engine *uc, const char *path) {
  size_t len = 0;
  void *p = load_file(path, &len);

  Elf64_Ehdr *ehdr = (Elf64_Ehdr *)p;
  Elf64_Shdr *shdrs = (void *)ehdr + ehdr->e_shoff;

  if (ehdr->e_shoff > len) {
    errx(1, "corrupt file");
  }

  for (int i = 0; i < ehdr->e_shnum; i++) {
    if (shdrs[i].sh_addr) {
      size_t flags = 0;
      if (shdrs[i].sh_flags & SHF_WRITE) {
        flags |= UC_PROT_WRITE | UC_PROT_READ;
      }
      if (shdrs[i].sh_flags & SHF_EXECINSTR) {
        flags |= UC_PROT_EXEC | UC_PROT_READ;
      }

      size_t len = ((shdrs[i].sh_size + 0x1000 - 1) / 0x1000) * 0x1000;
      size_t start = (shdrs[i].sh_addr / 0x1000) * 0x1000;
      size_t end = start + len;

      size_t last_i = num_sections - 1;

      if (num_sections == 0 ||
          start >= sections[last_i].start + sections[last_i].len) {
        sections[num_sections].start = start;
        sections[num_sections].len = len;
        sections[num_sections].flags = flags;
        sections[num_sections].mem = malloc(len);
        memset(sections[num_sections].mem, 0, len);
        num_sections++;
      } else if (num_sections != 0 &&
                 end > sections[last_i].start + sections[last_i].len) {
        size_t new_len = end - sections[last_i].start;
        sections[last_i].len = new_len;
        sections[last_i].mem = realloc(sections[last_i].mem, new_len);
        memset(sections[last_i].mem, 0, new_len);
      }

      if (num_sections != 0 && flags != sections[last_i].flags) {
        sections[last_i].flags |= flags;
      }
    }
  }

  for (int i = 0; i < num_sections; i++) {
    uc_err e = uc_mem_map_ptr(uc, sections[i].start, sections[i].len,
                              sections[i].flags, sections[i].mem);
    if (e) {
      err(1, "Failed on uc_mem_map_ptr() with error returned: %u\n", e);
    }
  }

  for (int i = 0; i < ehdr->e_shnum; i++) {
    if (shdrs[i].sh_addr) {
      if (shdrs[i].sh_type == SHT_PROGBITS ||
          shdrs[i].sh_type == SHT_INIT_ARRAY ||
          shdrs[i].sh_type == SHT_FINI_ARRAY) {
        uc_mem_write(uc, shdrs[i].sh_addr, p + shdrs[i].sh_offset,
                     shdrs[i].sh_size);
      }
    }
  }

  return ehdr->e_entry;
}

static bool handle_userland_invalid(uc_engine *uc, uc_mem_type type,
                                    uint64_t address, int size, int64_t value,
                                    void *user_data) {
  fprintf(stderr, "invalid addr [0x%016lx]\n", address);
  exit(1);
  return false;
}

void handle_syscall(uc_engine *engine, void *user_data) {
  uint64_t rax, rdi, rsi, rdx, tmp;
  char buf[0x400];

  memset(buf, 0, sizeof(buf));
  uc_reg_read(engine, UC_X86_REG_RAX, &rax);

  switch (rax) {
    case 0:
      uc_reg_read(engine, UC_X86_REG_RDI, &rdi);
      uc_reg_read(engine, UC_X86_REG_RSI, &rsi);
      uc_reg_read(engine, UC_X86_REG_RDX, &rdx);
      tmp = read(rdi, buf, rdx);
      uc_mem_write(engine, rsi, buf, tmp);
      uc_reg_write(engine, UC_X86_REG_RAX, &tmp);
    case 1:
      uc_reg_read(engine, UC_X86_REG_RDI, &rdi);
      uc_reg_read(engine, UC_X86_REG_RSI, &rsi);
      uc_mem_read(engine, rsi++, buf, 1);
      while (buf[0]) {
        tmp = write(rdi, buf, 1);
        uc_mem_read(engine, rsi++, buf, 1);
      }
      break;
    case 59:
      puts("# id\nuid=0(root) gid=0(root) groups=0(root)\n# exit");
      break;
    case 1337:
      uc_reg_read(engine, UC_X86_REG_RDI, &rdi);
      uc_reg_read(engine, UC_X86_REG_RSI, &rsi);
      uc_reg_read(engine, UC_X86_REG_RDX, &rdx);
      if (rdi == 0x1337 && rdx) {
        uc_mem_write(engine, rsi, flag, sizeof(flag));
      }
      break;
    default:
      puts("unimplemented");
      exit(255);
      break;
  }
}

static void trace(uc_engine *engine, uint64_t address, uint32_t size,
                  void *user_data) {
  uint64_t rsp;
  uc_reg_read(engine, UC_X86_REG_RSP, &rsp);
  fprintf(stderr, "trace: 0x%lx (0x%x) %lx\n", address, size, rsp);
}

void run(const char *path) {
  uc_engine *engine;
  uc_err e;
  uc_hook hh, hhh;

  e = uc_open(UC_ARCH_X86, UC_MODE_64, &engine);
  if (e) {
    puts("failed to initialize unicorn");
    exit(1);
  }

  size_t entry = map_elf(engine, path);

  uc_mem_map_ptr(engine, USER_STACK - MAPPING_SIZE, MAPPING_SIZE,
                 UC_PROT_READ | UC_PROT_WRITE, USER_STACK_MEM);
  uc_hook_add(engine, &hh, UC_HOOK_INSN, handle_syscall, NULL, 1, 0,
              UC_X86_INS_SYSCALL);
  uc_hook_add(engine, &hhh,
              UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED |
                  UC_HOOK_MEM_FETCH_UNMAPPED,
              handle_userland_invalid, NULL, 1, 0);

  size_t min = -1;
  size_t max = 0;
  for (int i = 0; i < num_sections; i++) {
    if (sections[i].flags & UC_PROT_EXEC && sections[i].start < min)
      min = sections[i].start;
    if (sections[i].flags & UC_PROT_EXEC &&
        sections[i].start + sections[i].len > max)
      max = sections[i].start + sections[i].len;
  }

  // uc_hook debug;
  // uc_hook_add(engine, &debug, UC_HOOK_CODE, trace, NULL, min, max);

  uint64_t rsp = USER_STACK - 0x1000;
  uint64_t rip = entry;

  uc_reg_write(engine, UC_X86_REG_RSP, &rsp);
  uc_reg_write(engine, UC_X86_REG_RIP, &rip);
  uc_emu_start(engine, entry, max, 0, 0);
}

int main(int argc, const char **argv) {
  setup();
  run(argv[1]);
}
