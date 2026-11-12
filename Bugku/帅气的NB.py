#!/usr/bin/env python3
import base64
from itertools import cycle
from sympy import discrete_log, n_order, sqrt_mod


p = 264939537474946022184387148430768313346646329012994880624541045888711787653231
a = 172758858410161032222325336695971283308452620208332306681758664416752295370991

G = (
    137420494633265081853520303631701429441392730524428977912483910109442079887667,
    136590225176889456337403539826679828679637705963081988883359461639544522481417,
)

C = (
    3322719648942820303660920116849927911747359606160907256835130390304318706650,
    204524730679882164003064278501342862761246901119278949376421891596385644502844,
)

blob = b"4h;_j2mxFW3P1t~ECyaW8&NSVGXV(}SPWem"


def phi(point: tuple[int, int], s: int) -> int:
    """将奇异曲线上的非奇异点映射到 F_p^*。"""
    x, y = point
    t = y * pow(x, -1, p) % p
    return (t + s) * pow((t - s) % p, -1, p) % p


# sympy 可能返回两个平方根中的任意一个。
# 选择另一根只会把映射整体取逆，不影响离散对数 d。
s = int(sqrt_mod(a, p))
g = phi(G, s)
c = phi(C, s)

order = n_order(g, p)
d = int(discrete_log(p, c, g))

assert pow(g, d, p) == c
assert 0 <= d < order

key = d.to_bytes(8, "big")
ciphertext = base64.b85decode(blob)
plaintext = bytes(x ^ k for x, k in zip(ciphertext, cycle(key)))

# 回编码验证，排除 Base85 变体、字节序或异或方向错误。
rebuilt = bytes(x ^ k for x, k in zip(plaintext, cycle(key)))
assert base64.b85encode(rebuilt) == blob
assert plaintext.startswith(b"flag{") and plaintext.endswith(b"}")

print(f"d     = {d}")
print(f"key   = {key!r}")
print(f"flag  = {plaintext.decode()}")
# flag{n1ub!ll_i3_s0_H@nds0m3}