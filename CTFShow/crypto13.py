import base64

filename = r"base.txt"
with open(filename) as f:
    s = f.read()
while True:
    try:
        s = base64.b16decode(s)
        continue
    except:
        pass
    try:
        s = base64.b32decode(s)
        continue
    except:
        pass
    try:
        s = base64.b64decode(s)
        continue
    except:
        pass
    break
flag = s.decode('utf-8')
print(flag)
# flag{b4Se_Fami1y_Is_FUn}