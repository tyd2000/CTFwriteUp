import random
import tqdm
from pwn import *
from Crypto.Util.number import *

context(arch='amd64', os='linux', log_level='debug')
io = remote('pwn.challenge.ctf.show', 28258)
io.recvuntil(b'p = ')
p = int(io.recvline().decode()[:-1])
if p % 4 != 3:
    io.close()
    exit()
io.recvuntil(b'len(flag) = ')
flag_len = int(io.recvline().decode()[:-1])
log.info(p, flag_len)
flag = [-1 for i in range(flag_len)]
INDEX = []
SEED = []
seed = 0
while len(SEED) != flag_len:
    random.seed(seed)
    randlist = list(range(flag_len))
    random.shuffle(randlist)
    indexx = list(range(flag_len)).index(randlist[0])
    if indexx not in INDEX:
        INDEX.append(indexx)
        SEED.append(seed)
    seed += 1
assert len(SEED) == flag_len
for i in tqdm.tqdm(range(len(SEED))):
    io.recvuntil(b'> ')
    io.sendline(str(SEED[i]).encode())
    io.recvuntil(b'newbie(sometimes_naive, p) = ')
    c = int(io.recvline().decode()[:-1])
    check = pow(c, (p - 1) // 2, p)
    flag[INDEX[i]] = 0 if check == 1 else 1
flag = [str(i) for i in flag]
log.success(long_to_bytes(int(''.join(flag), 2)))
io.close()