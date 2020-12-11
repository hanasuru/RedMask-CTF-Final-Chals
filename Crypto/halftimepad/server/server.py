#!/usr/bin/python
from binascii import hexlify
from re import findall
from os import urandom
import sys

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
madpad = lambda a, b: ''.join([chr(ord(i) ^ ord(j) ^ 0x69) for i, j in zip(a, b)])
genkey = lambda n: hexlify(urandom(n / 2))

if __name__ == '__main__':
    flag = open('flag.txt').read().strip()
    m = findall(r'^redmask{(\w+)}$', flag)[0]
    print hexlify(madpad(m, genkey(len(m))))
