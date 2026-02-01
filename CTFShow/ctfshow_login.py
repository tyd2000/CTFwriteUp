from Crypto.Util.number import *
from random import randint
from pwn import *

context(log_level='debug', os='linux', arch='amd64')
io = remote('pwn.challenge.ctf.show', 28218)
io.recvuntil(b'Here is the public key: (')
l = io.recvline()[:-2].decode()
log.info('l: %s'%l)
y, p = map(int, l.split(','))
g = 7

while (True):
    i, j = randint(2, p-2), randint(2, p-2)
    if GCD(j, p-1) != 1:
        continue
    r = pow(g, i, p) * pow(y, j, p) % p
    s = -r * inverse(j, p-1) % (p-1)
    m = s * i % (p-1)
    m_hex = b'Daniu@CTFshow'.hex() + f'{m:0260x}'
    io.sendlineafter(b'username (in hex): ', m_hex.encode())
    io.sendlineafter(b'r (in hex): ', f'{r:x}'.encode())
    io.sendlineafter(b's (in hex): ', f'{s:x}'.encode())
    msg = io.recvline()
    if b'[Error]: Token verification failure!\n' not in msg:
        log.success(msg)
    break
    ''' 不能这样无脑梭哈
    CTFSHOW_MEMBERS = [
        'Joker',
        'h1xa',
        'Daniu',
        'FW_Mumuzi',
        'cheyenne',
        'striving',
        'ThTsOd',
        'bit',
        'Lazzaro',
        'Y4tacker',
        'ISHAO',
        'aliga',
        'whwhwzwz',
        'XunYing',
        'cs',
        'Ricky',
        'FW_Suica',
        'duck0123',
        'yuchouxuan',
        'MiGooli',
        'owod',
        'yu22x',
        'ZM.J',
        'Yasso',
        'daliangba',
        '7herightp4th',
        'zealot',
        '0x7e',
        'i_kei',
        'V3geD4g',
        'paidx0',
        'lorlike',
        'saulgoodman',
        'Asofia',
        'ENJOEY',
        'g4_simon',
        'werewolfcjj',
        'lewiserii',
    ]

    CTFSHOW_MEMBERS = [f'{mem}@CTFshow'.encode() for mem in CTFSHOW_MEMBERS]
    for username in CTFSHOW_MEMBERS:
        m_hex = username.hex() + f'{m:0260x}'
        io = remote('pwn.challenge.ctf.show', 28218)
        io.sendlineafter(b'username (in hex): ', m_hex.encode())
        io.sendlineafter(b'r (in hex): ', f'{r:x}'.encode())
        io.sendlineafter(b's (in hex): ', f'{s:x}'.encode())
        msg = io.recvline()
        if b'[Error]: Token verification failure!\n' not in msg:
            log.success(msg)
        io.close()
    break
    '''
