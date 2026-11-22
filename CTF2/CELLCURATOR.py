import json
import urllib.request

URL = "http://d71d56cb336ba4ff026f3695.http-ctf2.dasctf.com/"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def post(path, payload):
    req = urllib.request.Request(
        URL + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with opener.open(req, timeout=25) as r:
        return json.loads(r.read())

# 1. 拉一条足够长的演化序列（seed 传什么都无所谓，服务端固定从全 0 起演）
rows = [list(map(int, r)) for r in post("/evolve", {"seed": [0] * 31, "steps": 14})["rows"]]
W = len(rows[0])

# 2. 相邻行差分，只用内部位置，避开边界策略
table = {}
for a, b in zip(rows, rows[1:]):
    for i in range(1, W - 1):
        key = (a[i - 1], a[i], a[i + 1])
        val = b[i]
        assert key not in table or table[key] == val, f"冲突 {key}"
        table[key] = val

assert len(table) == 8, f"邻域未覆盖全: {sorted(table)}"

# 3. 组规则号：111 为最高位，000 为最低位
rule = 0
for (l, c, r), out in table.items():
    rule |= out << ((l << 2) | (c << 1) | r)

print("rule =", rule, format(rule, "08b"))   # -> 45 00101101

# 4. 交叉校验：用该规则重放整条序列
for idx in range(len(rows) - 1):
    a, b = rows[idx], rows[idx + 1]
    for i in range(1, W - 1):
        assert table[(a[i - 1], a[i], a[i + 1])] == b[i]

# 5. 提交
res = post("/submit", {"rule": rule})
print(res)
flag = res['flag']
print(flag)
# CTF2{a51ca73a-8dfa-489d-966b-8178aa8aecd0}