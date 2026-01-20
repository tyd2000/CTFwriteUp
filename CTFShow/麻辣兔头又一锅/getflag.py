from gmpy2 import fib

with open('flag.txt','r') as f:
    txt = f.readlines()
    c = eval(f'[{txt[0]}],[{txt[1]}]')
flag = ''
for i in range(len(c[1])):
    flag += chr((fib(c[0][i])^fib(c[1][i]))&0xff)
print(flag)
# ctfshow{6d83b2f1-1241-4b25-9c1c-0a4c218f6c5f}