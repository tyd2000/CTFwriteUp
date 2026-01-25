from pwn import *

io = remote('pwn.challenge.ctf.show', 28172)
def exp():
    z = io.recvuntil(']\n')
    a = str(io.recvline())
    b = a.find('= (')
    c = a.find(',',9)
    d = int(a[b+3:c])#x
    e = int(a[c+2:-4])#y
    if(d>=e):
        io.sendline(str(d+e))
    else:
        f = e%d
        g = (e-f)//d
        h = g*d+f//2
        io.sendline(str(h))

for i in range(233):
    exp()
    print('进行了',i,'轮爆破')
io.interactive()
"""
进行了 232 轮爆破
[*] Switching to interactive mode
给出正整数n的值：
n = 春哥纯爷们，铁血真汉子！
--------------------------------
=== [第一届“快乐爷们”颁奖典礼] ===
助力春哥成功，春哥最后成为了整个宇宙最纯的纯爷们！
这是春哥的礼物：ctfshow{d0d6c212-de04-41eb-a07c-53e2ef03b437}
"""