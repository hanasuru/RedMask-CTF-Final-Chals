import re
import os
import base64

os.popen("tshark -r log.pcap -d 'tcp.port==57000,http' -d 'tcp.port==44322,http' -d 'tcp.port==44818,http' -Y 'data-text-lines' -Tfields -e http.file_data > request")

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

requ = open('request').readlines()[:]
result = dict()

for x in requ:
    clean = x.strip('\n')
    clean = re.sub(r'\\n', '', clean)
    clean = base64.b64decode(clean)
    clean = evals(clean.split('=')[1])

    if 'index' in clean:
        index, name, pos, char = extract(clean)
        key = result.get(name, dict())
        index = int(index)
        pos = int(pos)

        if not key:
            result[name] = key

        lastIndexed = result[name].get(index, dict())
        if not lastIndexed:
            result[name][index] = lastIndexed

        lastOccurence = result[name][index].get(pos, [''])
        if not lastOccurence[0]:
            result[name][index][pos] = lastOccurence
    
        lastOccurence[0] = (index, pos, char)

for k,v in result.iteritems():
    print '[+] Saving', k

    temp = ''
    for kk in sorted(v):
        vv = result[k][kk]

        for kkk in sorted(vv):
            vvv = result[k][kk][kkk]

            char = vvv[0][-1]
            if char != '\\n':
                temp += vvv[0][-1]

    with open(k, 'wb') as f:
        content = temp.decode('hex')
        f.write(content)