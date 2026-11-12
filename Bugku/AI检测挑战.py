import requests, json, time, random, re

BASE = "http://160.202.254.160:19309"

c4 = '''n = int(input())
d_p = [1] + [0] * n
for coin in range(1, n):  
    for s in range(coin, n + 1):
        d_p[s] += d_p[s - coin]
print(d_p[n])
'''

s = requests.Session()
r = s.get(BASE + "/")
m = re.search(r'id="csrfToken" value="([^"]+)"', r.text)
csrf = m.group(1)


payload = {"code": c4, "lang": "python3", "keystroke_log": [], "csrf_token": csrf}
r = s.post(BASE + "/submit", json=payload ,verify=False)
d = r.json()
print(json.dumps(d, ensure_ascii=False, indent=2))