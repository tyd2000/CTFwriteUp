from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import *
from randcrack import RandCrack

io = remote('pwn.challenge.ctf.show', 28105)
def woohoo():
    a = rc.predict_getrandbits(32)
    b = rc.predict_getrandbits(32)
    c = rc.predict_getrandbits(32)
    d = rc.predict_getrandbits(32)
    return (a<<96)+(b<<64)+(c<<32)+(d)

def split1(m):
    temp = bin(m)[2:].rjust(128,'0')
    for i in range(4):
        rc.submit(int(temp[32*i:32*(i+1)],2))

rc = RandCrack()
pay = b'hashhashhashhas'
pay1 = bytes_to_long(b'hashhashhashhas\x01')
for i in range(78):
    io.sendline(b'e')
    io.recvuntil(b'> ')
    io.sendline(pay)
    io.recvuntil(b'Ciphertext (hex): ')
    c = int(io.recvline()[:-1],16)
    io.recvuntil(b'Key (hex): ')
    key = int(io.recvline()[:-1],16)
    key1 = long_to_bytes(key).rjust(AES.block_size, b"\x00")
    aes = AES.new(key1,AES.MODE_ECB)
    iv = bytes_to_long(aes.decrypt(long_to_bytes(c)))^pay1
    split1(key)
    split1(iv)

io.sendline(b't')
io.recvuntil(b'Ciphertext (hex): ')
c = int(io.recvline()[:-1],16)
io.recvuntil(b'IV (hex): ')
ivv = int(io.recvline()[:-1],16)
print(bin(ivv))
key = woohoo()
iv = woohoo()
print(bin(iv))
key = long_to_bytes(key)
iv = long_to_bytes(iv)
c = long_to_bytes(c)
aes = AES.new(key,AES.MODE_CBC,iv)
print(aes.decrypt(c))