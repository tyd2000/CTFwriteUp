import gmpy2
n = 8870619487339789349033932217513908953609539651949986489986889710933094577873155191810742828503059670650154455297603719
c = 6940158573485767169443582872275118843545217792197971962103010557916847970940437712181778807436191892307187137338300231
# from sage.all import euler_phi
# d = gmpy2.invert(3, euler_phi(n))
# 如果没有sagemath 可以用totient平替euler_phi
from sympy import totient
d = gmpy2.invert(3, int(totient(n)))
m = pow(c, d, n)
flag = bytes.fromhex(hex(m)[2:]).decode('utf-8')
print(flag)
# ctfshow{W4r_Dull_Eeeee_LLL3333_A_n0_F14sH_@w@}