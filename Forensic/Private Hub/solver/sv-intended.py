from Crypto.PublicKey import RSA
from Crypto.Util.number import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512

import re
import os
import base64

os.popen("tshark -r log.pcap -d 'tcp.port==57000,http' -d 'tcp.port==44322,http' -d 'tcp.port==44818,http' -Y 'data-text-lines' -Tfields -e http.file_data > request")
os.popen("tshark -r log.pcap -Y 'dns.txt' -Tjsonraw | jq '.[]._source.layers.dns_raw[0][128:]' json | tr -d '\"' | while read i; do echo $i | xxd -r -p; echo; done > response")

keyPriv = RSA.importKey(open("key").read())
oaep = PKCS1_OAEP.new(keyPriv)

def evals(text):
    template = "{}\['__doc__'\]\[\d+\]"
    keys = map(str, range(10))
    keys += ['\[\]','\(\)',"''"]
    
    rule = '|'.join(template.format(_) for _ in keys)
    regex = re.compile(rule + "|'[\w|\d]'")

    for i in regex.findall(text):
        r = i.replace("['__doc__']", ".__doc__")
        r = re.sub('^\d', 'int', r)
        r = re.sub('^\(\)', 'tuple', r)
        text = text.replace(i, eval(r))
    
    text = text.replace('\n', '\\n')
    return text.replace('~','')

def extract(text):
    regex = re.compile(r'-s (\d+) -l \d+ ([\w\.]+)\).*\[(\d+)\].*\((\w|\d|\\n)\)')
    return regex.findall(text)[0]

def decrypt(text):
    text = text[12:-4]
    rsa = PKCS1_OAEP.new(keyPriv, hashAlgo=SHA512, randfunc=os.urandom(0))
    return rsa.decrypt(text)

resp = open('response').readlines()[:]
requ = open('request').readlines()[:]

result = dict()
for x,y in zip(requ, resp):
    x, y = map(lambda _: _.strip('\n'), (x,y))
    x, y = map(lambda _: re.sub(r'\\n', '', _), (x,y))
    x, y = map(lambda _: base64.b64decode(_), (x,y))

    x = evals(x.split('=')[1])
    y = decrypt(y)

    if 'int' in y and  'xxd' in x:
        index, name, pos, char = extract(x)
        key = result.get(name, list())

        if not key:
            result[name] = key
        key.append((int(index), int(pos), char))

for k,v in result.iteritems():
    print '[+] Saving', k
    vals = sorted(v)
    val = [_[2] for _ in vals]

    with open(k, 'wb') as f:
        content = ''.join(val).decode('hex')
        f.write(content)