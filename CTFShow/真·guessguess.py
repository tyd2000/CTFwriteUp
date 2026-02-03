C='85677bc8302bb20f3be728f99be0002ee88bc8fdc045'
M=b'The secret message is:'.hex()
lines=[]
for i in range(1,len(M)): 
     l=[int(M[i],16),int(C[i],16),int(M[i-1],16)] 
     l.sort()
     a,b,c=l 
     lines.append(f"g[{a}]^g[{b}]^g[{c}]==0")

lines=set(lines)

from z3 import *
g=[BitVec(f"g{i}",4) for i in range(16)]
s=Solver()

for i in lines:
    s.add(eval(i))

for i in range(16):
    for j in range(i+1,16):
        s.add(g[i]!=g[j])

s.add(g[4]==0)
s.add(g[5]^g[8]==7)

ans_key=[]
while(s.check()==sat):
    m=s.model()
    cond=[]
    key=[0]*16
    for d in m.decls():
        #exec(f"key[{int(d.name()[1:])}]={m[d]}")
        exec(f"key[{m[d]}]={int(d.name()[1:])}")

        cond.append(eval(f"g[{int(d.name()[1:])}]!={m[g[int(d.name()[1:])]]}"))
    ans_key.append("".join([hex(i)[2:] for i in key]))    
    s.add(Or(cond))

print(len(ans_key))    
print(ans_key[0])



from random import shuffle
#from secret import secret_msg

ALPHABET = '0123456789abcdef'

class Cipher:
    def __init__(self, key):
        self.key = key
        self.n = len(self.key)
        self.s = 7

    def add(self, num1, num2):
        res = 0
        for i in range(4):
            res += (((num1 & 1) + (num2 & 1)) % 2) << i
            num1 >>= 1
            num2 >>= 1
        return res

    def encrypt(self, msg):
        key = self.key
        s = self.s
        ciphertext = ''
        for m_i in msg:
            c_i = key[self.add(key.index(m_i), s)]
            ciphertext += c_i
            s = key.index(m_i)
        return ciphertext

    def decrypt(self, c):
        key = self.key
        s = self.s
        msg = ''
        for c_i in c:
            m_i = key[self.add(key.index(c_i), s)]
            msg += m_i
            s = key.index(m_i)
        return msg


plaintext = b'The secret message is:'.hex() #+ secret_msg.hex()

from Crypto.Util.number import *
C1="85677bc8302bb20f3be728f99be0002ee88bc8fdc045b80e1dd22bc8fcc0034dd809e8f77023fbc83cd02ec8fbb11cc02cdbb62837677bc8f2277eeaaaabb1188bc998087bef3bcf40683cd02eef48f44aaee805b8045453a546815639e6592c173e4994e044a9084ea4000049e1e7e9873fc90ab9e1d4437fc9836aa80423cc2198882a"
i=1
for key in ans_key:
    cipher = Cipher(key)
    ciphertext = cipher.encrypt(plaintext)
    if ciphertext == C:
        print(key)
        print(ciphertext)
        print(C)
        print(i)
        i+=1
    flag = long_to_bytes(int(cipher.decrypt(C1),16)).decode()
    print(flag)
# DUCTF{d1d_y0u_Us3_gu3ss1nG_0r_l1n34r_4lg3bRA??}