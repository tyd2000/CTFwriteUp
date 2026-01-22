import re

x='2559659965656A9A65656996696965A6695669A9695A699569666A5A6A6569666A59695A69AA696569666AA6'
strr=bin(int(x,16))[2:]
print(strr)
step = 2
str2 = [strr[i:i+step] for i in range(0,len(strr),step)]
print(str2)
flag = []
final = ""
for i in str2:
    flag.append(i)
for i in flag:
    if(i=="10"):
        final += "1"
    if(i=="01"):
        final += "0"
print(hex(int(final,2)))
#424a447b4469664d616e63686573746572636f64657d
flag = ''
for i in re.findall(r".{2}","424a447b4469664d616e63686573746572636f64657d"):
    flag += chr(int(i,16))
print(flag)
# BJD{DifManchestercode}