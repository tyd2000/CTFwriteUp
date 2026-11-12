import random

outs = [
    502000127,
    401997630,
    180303717,
    474190135,
    138669659,
    178962539,
    254230901,
]

# 1. 确定每行长度（flag 长度）
L = max(len(bin(x)[2:]) for x in outs)
print('flag length =', L)

# 2. 每行左补 0 到 L 位
shuffled = [bin(x)[2:].zfill(L) for x in outs]
for i, s in enumerate(shuffled):
    print(f'row {i}: {s}')

def unshuffle(shuffled_row, seed):
    """把打乱后的行还原成原始顺序"""
    idx = list(range(L))
    random.seed(seed)
    random.shuffle(idx)          # idx[after] = before
    orig = [''] * L
    for after, before in enumerate(idx):
        orig[before] = shuffled_row[after]
    return ''.join(orig)

def try_seed(seed):
    rows = [unshuffle(shuffled[i], seed) for i in range(7)]
    chars = []
    for j in range(L):
        b = ''.join(rows[i][j] for i in range(7))
        chars.append(chr(int(b, 2)))
    return ''.join(chars)

# 3. 暴力 seed
for seed in range(114514, 1919811):
    s = try_seed(seed)
    if s.startswith('flag{') and s.endswith('}'):
        print('seed =', seed)
        print('flag =', s)
        break
    # s = try_seed(668598)
    # flag{34sy_81n@ry_With_R4nd0m}