cipher = b'FK?DWzCLwPEJFFqN'

flag = bytes(((c + i) ^ 0x20) & 0xff for i, c in enumerate(cipher))
print(flag.decode())   # flag{_is_yours_}

# 自验算:按程序逻辑重新加密
enc = bytes((((c ^ 0x20) - i) & 0xff) for i, c in enumerate(flag))
print(enc == cipher)   # True