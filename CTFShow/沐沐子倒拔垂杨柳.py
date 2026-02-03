from pwn import *

BLOCK_SIZE = 16
port = 28132

context.log_level = 'debug'
sh = remote('pwn.challenge.ctf.show', port)

plaintext = b'\x00' * 32

def attack(tip):
    sh.recvuntil(b'>')
    sh.sendline(tip)
    sh.recvuntil(b'>')
    sh.sendline(b'1')
    sh.recvuntil(b'>')
    sh.sendline(plaintext.hex())
    sh.recvline()
    cipher = bytes.fromhex(sh.recvline()[:-1].decode())
    c3, c4 = cipher[:16], cipher[16:32]
    sh.recvuntil(b'>')
    sh.sendline(b'2')
    sh.recvuntil(b'>')
    sh.sendline(c4.hex())
    sh.recvline()
    res = bytes.fromhex(sh.recvline()[:-1].decode())
    key = xor(res, c3)
    sh.recvuntil(b'>')
    sh.sendline(b'3')
    return key


flag = ''
for i in range(3):
    flag += attack(str(i).encode()).decode()
print(flag)