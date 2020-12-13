typedef unsigned long uint64_t;

__attribute__((naked)) void helper() {
    asm("pop rdi; ret;");
    asm("pop rsi; ret;");
    asm("pop rdx; ret;");
    asm("pop rax; ret;");
}
__attribute__((naked)) int sys_read(int fd, char* buf, uint64_t n) {
    asm("xor rax, rax");
    asm("syscall");
    asm("ret");
}

__attribute__((naked)) int sys_write(int fd, char* buf) {
    asm("xor rax, rax; inc rax;");
    asm("syscall");
    asm("ret");
}

int main() {
    char buf[32];
    sys_write(1, "welcome to sandbox\n");
    sys_read(0, buf, 0x200);
    sys_write(1, buf);
    return 0;
}

__attribute__((naked)) void _start () {
    main();
    asm("hlt");
}