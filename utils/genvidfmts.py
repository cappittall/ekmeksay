lines= open('./device.txt', 'r' ).read().splitlines()
lines = [i.replace('\t', '').strip() for i in lines if ('30/1' in i and ('video/x-raw' in i or 'image/jpeg') and 'caps' not in i) ]
liss = []
for l in lines:
    l = l.replace('format=', '')
    l = l.replace('width=', '')
    l = l.replace('height=', '')
    l = l.replace('framerate={ (fraction)', '')
    l = l.replace('(fraction)', '')
    l = l.replace('framerate=', '')
    l = l.replace('}', '')
    l = l.split(',')
    print(l)  # 11.satır
    if l[0] == 'video/x-raw':
        print(l[0], len(l))
        ll0 = '/dev/video1:YUY2' + l[2].strip() + 'x' + l[3].strip()
        for r in l[4:0]:
            liss.append(ll0 + ':' + r.strip())
    else:
        ll0 = '/dev/video1:image/jpeg:' + l[1].strip() + 'x' + l[2].strip()
        for r in l[3:]:
            liss.append(ll0 + ':' + r.strip())
with open('videofmts.txt', 'w') as f:
    f.writelines([i+'\n' for i in list(set(liss)) if '30/1' in i or '60/1' in i ])
    f.writelines()
    