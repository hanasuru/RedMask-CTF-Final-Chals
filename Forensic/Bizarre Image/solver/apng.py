from base64 import b32encode as base32
from collections import OrderedDict
from struct import unpack, pack
from random import shuffle
from textwrap import wrap
from zlib import crc32
from PIL import Image

class PNGReader(object):
	def __init__(self, path):
		self.path = path
		self.info = OrderedDict()

	def getInfo(self):
		if not self.info:
			with open(self.path, 'rb') as img:
				buf = img.read()
				pos = 8; i = 0

				while True:
					try:
						data  = self.iterate(buf, pos)
						exist = self.info.get(data['type'], list())						
						if not exist:
							self.info[data['type']] = exist
						exist.append(data)
						# print data['type']
						pos += data['pos'] + 12
						i+=1
					except:
						break
		return self.info

	def calcCRC(self, text):
		crc  = crc32(text) % (1<<32)
		return pack('>I', crc)

	def iterate(self, buf, pos):
		data = OrderedDict()
		size = unpack('!I', buf[pos:pos+4])[0]
		data['pos']  = size
		data['size'] = buf[pos:pos+4]
		data['type'] = buf[pos+4:pos+8]
		data['data'] = buf[pos+8:pos+8+size]
		data['crc']  = buf [pos+8+size: pos+size+12]
		return data

	def editChunk(self, count, _type, _sect, data):
		self.info[_type][count][_sect] = data
		raw = self.info[_type][count]['type'] +\
				  self.info[_type][count]['data'] 
		self.info[_type][count]['crc'] = self.calcCRC(raw)

	def calcCRC(self, text):
		crc  = crc32(text) % (1<<32)
		return pack('>I', crc)

	def save(self, path):
		result = '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
		for _ in self.info.values():
			for __ in _:
				result += ''.join(__.values()[1:])
		open(path,'wb').write(result)

def reSort(data, offset):
	chunk = dict()
	for _ in data[offset:]:
		seq_num = unpack('!I', _['data'][:4])[0]
		chunk[seq_num] = _
	return chunk.values()

png  = PNGReader('flag.png')
png.getInfo()

fctl = reSort(png.info['fcTL'], 1)
fdat = reSort(png.info['fdAT'], 0)

data = [__ for _ in zip(fctl, fdat) for __ in _]
png.info['fcTL'][1:] = []
png.info['fdAT'] = data
png.editChunk(0, 'acTL', 'data', '\x00\x00\x01\x61\x00\x00\x00\x00')
png.save('recovered.png')
