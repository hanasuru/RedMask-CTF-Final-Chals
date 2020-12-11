#!/usr/bin/env python3
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import getRandomNBitInteger
import re

from flag import flag

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

def main():
    ptx = re.findall(r'^redmask{(\w+)}$', flag)[0].encode()
    rsa = RSA.generate(1024)
    oaep = PKCS1_OAEP.new(rsa)
    lfsr = LFSR64(getRandomNBitInteger(64), 0xC936000000000000)
    with open('output.txt', 'w') as f:
        f.write(f"{lfsr.encrypt(ptx[:len(ptx)//2]).hex()}\n")
        f.write(f"{oaep.encrypt(ptx[len(ptx)//2:]).hex()}\n")
        f.write(f"{lfsr.encrypt(rsa.export_key('PEM')).hex()}\n")
        f.close()

if __name__ == '__main__':
    main()
