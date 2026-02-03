from pwn import *
from Crypto.Util.number import *

# context(log_level='debug', os='linux', arch='amd64')
while True:
    io = remote('pwn.challenge.ctf.show', 28122)
    io.recvuntil(b'Here is the public key: (')
    l = io.recvline()[:-2].decode()
    log.info('p, y = %s'%l)
    p, y = map(int, l.split(','))
    # 等价于 import re
    # content = io.recvuntil(b'username (in hex):').decode()
    # p, y = findall(r"\d+", content)
    # p, y = int(p), int(y)
    u = bytes_to_long(b'ZM.J@CTFshow') << 1024
    u, r, s = long_to_bytes(u + (p - 1) // 2), (p - 1) // 2, (p - 1) // 2
    io.sendline(u.hex().encode())
    io.recvuntil(b'r (in hex):')
    io.sendline(hex(r).encode())
    io.recvuntil(b's (in hex):')
    io.sendline(hex(s).encode())
    flag = io.recvline()
    if b'ctfshow' in flag:
        log.success(flag.decode())
        break
# ctfshow{66bf44d9-ae38-4d5c-9e5c-20dc649340fa}