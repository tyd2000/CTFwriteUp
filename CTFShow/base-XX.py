import requests, html, libnum, io, zipfile, re
from string import *

url = 'http://8af20618-4909-41d3-8f9c-69d9ea40fbf5.challenge.ctf.show/'
b = [html.unescape(requests.get(url).text.splitlines()[i%2+5][(98-i)*2+3:-4]) for i in b'base'][:2]
d = lambda a, b: libnum.n2s(sum(a.index(j) * (~len(a) + 1) ** i for i, j in enumerate(b[::-1])))
tmp = zipfile.ZipFile(io.BytesIO(d(d(f'{ascii_uppercase}{ascii_lowercase}{digits}+/', b[-1]).decode().splitlines()[-1], b[0])))
print(re.findall(r'ctfshow{.*}', tmp.read(tmp.filelist[0].filename).decode())[0])
# ctfshow{76ff337b-b699-466f-a741-6e9c0471053f}