#!/usr/bin/python
from pwn import *

LEN = 20
boxes = [[] for _ in range(LEN)]

ctr = 0

while not all(len(box) == 16 for box in boxes):
    # p = process('./server.py', level='warn')
    p = remote('localhost', 30001, level='warn')
    pantun = p.recvline(0).decode('hex')
    assert len(pantun) == LEN
    for i in range(LEN):
        if pantun[i] not in boxes[i]:
            boxes[i].append(pantun[i])
    p.close()
    ctr += 1

print ctr

flag = ''

for i in range(LEN):
    box = sorted(boxes[i])
    for j in range(256):
        baru = []
        for k in '0123456789abcdef':
            baru.append(chr(j ^ ord(k)))
        baru = sorted(baru)
        if baru == box:
            flag += chr(j ^ 0x69)
            print flag
            break

assert len(flag) == LEN
print 'Flag: redmask{%s}' % (flag)
