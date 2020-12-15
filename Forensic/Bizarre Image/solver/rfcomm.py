data = open('data').read().split('\n')[:-1]
lengths = open('length').read().split('\n')[:-1]

extras = []
current = lengths[0]
for e,i in enumerate(lengths):
    length = i

    dat = data[e]
    if current != length:
        try:
            byte = data[e+1][:12]
            extras.append(byte)
        except:
            pass
            
result = ''.join(data)[64:]
for i in extras:
    result = result.replace(i, '')

with open('fixed.png', 'wb') as f:
    f.write(result.decode('hex'))
