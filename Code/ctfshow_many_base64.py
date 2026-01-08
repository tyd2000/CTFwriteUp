import re
import requests
import itertools
from base64 import b64decode
from bs4 import BeautifulSoup

correct = "SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU="
# Layer 5: btoa(L4) = correct → L4 = base64.b64decode(correct)
L4 = b64decode(correct).decode()  
print("L4:", L4)  # IpUFQxM1UzRmtSRk0wU2xSU05qRXduVVVk9cVc5
# Layer 4: L4 = b64encode('aB3' + L3 + 'qW9')[2:]
# So full_b64 = ?? + L4, and len(full_b64) % 4 == 0
s = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
for combo in itertools.product(s, s):
    passwd_4 = ''.join(combo) + L4
    if str(b64decode(passwd_4)).find("aB3") > 0:
        # print(passwd_4)
        try:
            passwd_3 = b64decode(passwd_4).decode()
            if passwd_3.startswith('aB3') and passwd_3.endswith('qW9'):
                L3 = passwd_3[3:-3]
                print("L3:", L3)  # PT13U3FkRFM0SlRSNjEwTUY=
        except:
            continue
# Layer 3: L3 = b64encode(reverse(L2))
# So reverse(L2) = base64.b64decode(L3)
rev_L2 = b64decode(L3).decode()
L2 = rev_L2[::-1]
print("L2:", L2)  # FM016RTJ4SDdqSw==
# Layer 2: L2 = b64encode(L1 + 'xH7jK')[3:]
# Again, need to recover full b64

url = 'https://e858b1f7-9a9b-4bce-b913-25323b065280.challenge.ctf.show/check.php'
# 配置HTTP协议的代理，监听本地8080端口
proxies = {'http': "http://127.0.0.1:8080"}
heads = {'User-Agent': "ctf-show-brower"}

for combo in itertools.product(s,s,s):
    passwd_1=''.join(combo) + L2
    passwd_0=str(b64decode(passwd_1))[slice(0,-6)]   # 解码后去掉最后5个字符
    passwd=passwd_0[slice(2, None)]  # 去掉前2个字符
    if re.match(r'^[A-Za-z0-9]{3}', passwd):
        filtered = [s for s in str(b64decode(passwd)) if '\\' not in s]
        passwd="".join(filtered)[slice(2,None)][0:-1]
        # print(passwd)
        if passwd == 'T17316':
            response = requests.post(
                url=url,
                data={"username": "admin", "password":passwd},
                proxies=proxies,
                headers=heads,
                verify=False)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            match = re.search(r'CTF\{[^}]+\}', text)
            if match:
                print("Flag:", match.group(0))
                # Flag: CTF{base64_brute_force_success}