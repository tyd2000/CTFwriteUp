#!/usr/bin/env python3
# solve.py — 依赖: pip install msoffcrypto-tool numpy
import io, struct, wave, re, base64, zipfile
import numpy as np, msoffcrypto

raw = open('此地无银三百两.docx','rb').read()

# 1) FAT 扫描空闲扇区,找非零空闲区里的 RIFF（本题动态定位到偏移 20480）
ss = 512; fat = []
for i in range(3):
    fs = struct.unpack('<I', raw[0x4c+4*i:0x50+4*i])[0]   # DIFAT: FAT 扇区号
    fat += list(struct.unpack('<128I', raw[(fs+1)*ss:(fs+2)*ss]))
used = {s for s in fat if s < 0xFFFFFFFA}
off = next(((s+1)*ss for s in range(len(raw)//ss)
            if s not in used and raw[(s+1)*ss:(s+1)*ss+4] == b'RIFF'))

# 2) 提取 WAV 并 DTMF 解码
w = wave.open(io.BytesIO(raw[off:])); fs = w.getframerate()
pcm = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)
win = 512
env = np.array([np.abs(pcm[i:i+win]).mean() for i in range(0, len(pcm)-win, win)])
on = env > env.max()*0.15
segs, s = [], None
for i, v in enumerate(on):
    if v and s is None: s = i
    if not v and s is not None: segs.append((s*win, i*win)); s = None
DTMF = {(697,1209):'1',(697,1336):'2',(697,1477):'3',(770,1209):'4',(770,1336):'5',
        (770,1477):'6',(852,1209):'7',(852,1336):'8',(852,1477):'9',
        (941,1209):'*',(941,1336):'0',(941,1477):'#'}
rows, cols = [697,770,852,941], [1209,1336,1477,1633]
near = lambda f, t: min(t, key=lambda x: abs(x-f))
pwd = ''
for a, b in [x for x in segs if x[1]-x[0] > 1000]:
    sp = np.abs(np.fft.rfft(pcm[a:b]*np.hanning(b-a)))
    fr = np.fft.rfftfreq(b-a, 1/fs)
    pk = lambda lo, hi: fr[(fr>lo)&(fr<hi)][np.argmax(sp[(fr>lo)&(fr<hi)])]
    pwd += DTMF[(near(pk(600,1000), rows), near(pk(1100,1800), cols))]
print('[+] password:', pwd)

# 3) 解密 docx → 解包 word/document.xml → 取 Base64 → flag
f = msoffcrypto.OfficeFile(io.BytesIO(raw)); f.load_key(password=pwd)
out = io.BytesIO(); f.decrypt(out)
xml = zipfile.ZipFile(out).read('word/document.xml').decode('utf-8')
text = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml))
b64 = re.search(r'[A-Za-z0-9+/]{20,}={0,2}', text).group()
print('[+] flag:', base64.b64decode(b64).decode())
# bugku{c0NGr4tul4ti0n5_Fr0m_d0cx_st39}