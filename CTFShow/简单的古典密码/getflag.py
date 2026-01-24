import base64,base58,base91,base92
from tqdm import trange
import gmpy2

dec=[base64.b32decode,base58.b58decode,base64.b64decode,base64.a85decode,base64.b85decode,base91.decode]

flagc = open('ctfshow.txt','r').read()

def dcas(s='', key=1):
    cf = ''
    for ch in s:
        if 'a' <= ch <= 'z':
            cf += chr((ord(ch) - ord('a') - key) % 26 + ord('a'))
        elif 'A' <= ch <= 'Z':
            cf += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        else:
            cf += ch
    return cf

def dbase(s=''):
    for i in dec:
        for j in range(1,26):
            cs = dcas(s,j)
            try:
                f = i(cs).decode()
                if f.isprintable():
                    return f
            except:
                pass
    return s

for x in trange(10):
    flagc=dbase(flagc)
    print('\nLength:%s'%len(flagc))

d={chr(i):0 for i in range(128)}
for i in flagc:
    d[i]+=1
flag = ''
for i in range(2,20):
    fib=gmpy2.fib(i)
    for j in d:
        if d[j]==fib:
            flag += j
flag = f'ctfshow{{{flag}}}'
print(flag)
# ctfshow{MAlaTUtou_HO}