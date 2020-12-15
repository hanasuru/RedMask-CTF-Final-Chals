from textwrap import wrap
from PIL import Image
from zlib import crc32

import struct

class Chunk:
    def __init__(self, data, pos):
        self.size = self.get_size(data)
        self.type = self.get_type(data)
        self.data = self.get_data(data)
        self.crc  = self.get_crc(data)

    def get_size(self, data):
        return data[:4]

    def get_type(self, data):
        return data[4:8]

    def get_data(self, data):
        return data[8:-4]

    def get_crc(self, data):
        return data[-4:]

    @property
    def chunks(self):
        return [self.size, self.type, self.data + self.crc]

    @property
    def raw(self):
        return ''.join(self.chunks)

def calc_crc32(data):
    checksum = crc32(data) % (1<<32)
    return struct.pack('>I', checksum)

def parse_chunk(pos, length, content):
    begin, end = (pos, pos+length)
    content = content[begin: end]
    pos = len(content)

    return Chunk(content, pos), pos

def bytes_to_long(data):
    return struct.unpack('!I', data)[0]

def long_to_bytes(data):
    return struct.pack('!I', data)

def iterate_chunk(content):
    chunks = []
    pos = 8

    while pos < len(content):
        try:
            begin, end = (pos, pos+4)
            length = struct.unpack('!I', content[begin: end])[0]
            res = parse_chunk(pos, length + 12, content)

            chunks.append(res[0])
            pos += res[1]
        except struct.error:
            break

    return chunks

def resort(chunks, base):
    data = dict()

    for e,chunk in chunks:
        seq = bytes_to_long(chunk.data[:4])
        data[seq] = (e, chunk)
        
    offset = min(data.values())[0]
    for e,chunk in data.values():
        base[offset] = chunk
        offset += 2
    return base

with open('fixed.png') as img:
    image = img.read()
    chunks = iterate_chunk(image)
    head = image[:8]

fctl = [(e,i) for e,i in enumerate(chunks) if i.type == 'fcTL']
fdat = [(e,i) for e,i in enumerate(chunks) if i.type == 'fdAT']

chunks = resort(fctl, chunks)
chunks = resort(fdat, chunks)

# Write 881 Frame on acTL
chunks[1].data = long_to_bytes(len(fctl)) + '\x00' * 4
chunks[1].crc = calc_crc32(chunks[1].type + chunks[1].data)

with open('fixed.png','wb') as f:
    f.write(head)
    for chunk in chunks:
        f.write(chunk.raw)
