from Crypto.PublicKey import RSA
import libnum
import gmpy2
#导入公钥
with open("public.key","rb") as f:
    key = RSA.import_key(f.read())
    n =key.n
    e =key.e
 
with open("encrypted.message1","rb") as f:
    c1=libnum.s2n(f.read())
with open("encrypted.message2","rb") as f:
    c2=libnum.s2n(f.read())
with open("encrypted.message3","rb") as f:
    c3=libnum.s2n(f.read())
 
p=302825536744096741518546212761194311477
q=325045504186436346209877301320131277983
d=libnum.invmod(e,(p-1)*(q-1))
c=[c1,c2,c3]
flag=''
for i in c:
    m=pow(i,d,n)
    m1=str(libnum.n2s(int(m)))
    flag+=(m1.split("x00")[1])[:-3]  
print(flag)
# flag{3b6d3806-4b2b-11e7-95a0-000c29d7e93d}