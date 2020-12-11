#!/usr/bin/env python3
from Crypto.Cipher import PKCS1_OAEP
from deom import *

class LFSR64:
    def __init__(self, state, taps):
        self.mask = (1 << 64) - 1
        self.state = state
        self.taps = taps
    def encrypt(self, m: bytes) -> bytes:
        r = bytearray()
        for b in m:
            r.append(b ^ self._gene(8) ^ 0x69)
        return bytes(r)
    def _gene(self, n: int) -> int:
        s = 0
        for _ in range(n):
            s ^= self._tick()
            s <<= 1
        s >>= 1
        return s
    def _tick(self) -> int:
        r = self.state
        self.state = (r << 1) & self.mask
        i = (r & self.taps) & self.mask
        s = 0
        while i:
            s ^= (i & 1)
            i >>= 1
        self.state ^= s
        return s

out = open('../peserta/output.txt').read().strip().split()
c1 = bytes.fromhex(out[0])
c2 = bytes.fromhex(out[1])
c3 = bytes.fromhex(out[2])

randbs = xor(c3, b'-----BEGIN RSA PRIVATE KEY-----', b'\x69')
output = bin(int.from_bytes(randbs, 'big'))[2:]
output = list(map(int, list(output)))[:64]

length = len(output)
state = 0
taps = 0xC936000000000000

for i in range(length):
    state |= output[i] << (length - 1 - i)

for _ in range(length + (len(c1) * 8)):
    bit = state & 1
    tmp = taps & (state >> 1)
    while tmp:
        bit ^= (tmp & 1) 
        tmp = tmp >> 1
    state = (state >> 1) | (bit << (length-1))

lfsr = LFSR64(state, taps)
m1 = lfsr.encrypt(c1)
m3 = lfsr.encrypt(c3)
print(m3.decode())

rsa = RSA.import_key(m3)
oaep = PKCS1_OAEP.new(rsa)
m2 = oaep.decrypt(c2)
print('[*] Flag: redmask{%s}' % (m1+m2).decode())
