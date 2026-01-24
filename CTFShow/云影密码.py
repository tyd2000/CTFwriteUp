s = "44414440122401244401404424404421440414"
s = s.split('0')
l = []
# print(s)
for i in s:
    sum=0
    for j in i:
        sum+=eval(j)
    l.append(chr(sum+64))
print(l)
# ['Y', 'I', 'O', 'E', 'R', 'S', 'I']
flag = ''.join(l).lower()
flag = f'flag{{{flag}}}'
print(flag)
# flag{yioersi}