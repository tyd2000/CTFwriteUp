import requests
import json

url = "http://6d2fd070-5666-4ee3-93ec-7c6785a6f590.challenge.ctf.show/sx.php"
cookies = {'PHPSESSID':'5kou9mmciqef9dbtrpb6otq976'}
for i in range(1000):
    r = requests.get(url, cookies=cookies)
    # print(r.text)
    data = json.loads(r.text)
    if "j0ke" in r.text: # "ctfsh0w-f1ag-n0t-h3r3-th1s-msg-just-a-j0ke-}{"
        print(f"num值是: {data['num']}")
    else:  # ctfshow in r.text
        print(f"flag值是：{data['flag']}")
        break