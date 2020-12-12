#!/usr/bin/python
from base64 import b64decode
from libnum import n2s, rev_grey_code, s2n
from pwn import xor

def revSus(s):
    v0 = s[len(s) / 2:][::-1]
    v1 = s[:len(s) / 2][::-1]
    return ''.join([i + j for i, j in zip(v0, v1)])

def rotateRight64(num, k):
    b = bin(num)[2:].zfill(64)
    return int(b[-(k % 64):] + b[:-(k % 64)], 2)

out = open('output.txt').read().strip()
out = xor(b64decode(out), '\x69')
out = [out[i:i + 8][::-1] for i in range(0, len(out), 8)]
out = [rotateRight64(s2n(i), 13) for i in out]
out = [n2s(rev_grey_code(i)) for i in out]
out = revSus(''.join(out))
print out
