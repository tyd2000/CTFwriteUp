#!/usr/bin/env python3
import json, struct, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://<target>"
PAGE = 4096

def api(path, payload=None):
    url = BASE + path
    if payload is None:
        req = urllib.request.Request(url)
    else:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"},
                                     method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def read_phys(off, length):
    out = bytearray()
    while len(out) < length:
        want = min(65536, length - len(out))
        d = api("/api/hex?off=0x%x&len=%d" % (off + len(out), want))
        assert d.get("ok"), d
        for line in d["lines"]:
            out += bytes.fromhex(line["hex"].replace(" ", ""))
        if not d["lines"]:
            break
    return bytes(out[:length])

def xor(data, key):
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(data))

b = api("/api/bundle")

# 1. 两份枚举交叉比对
def parse(tbl):
    rows = {}
    for ln in tbl.strip().splitlines()[1:]:
        p = ln.split()
        if len(p) >= 3:
            rows[int(p[0])] = (int(p[1]), p[2])
    return rows

pslist, psscan = parse(b["pslist"]), parse(b["psscan"])
only_scan = set(psscan) - set(pslist)
assert only_scan == {4471}          # 目标唯一
print("目标 =", psscan[4471])        # (4412, 'colsvc')

# 2. 找 rwx 映射并确认 VM_DONTDUMP
for ln in b["proc"]["maps"].splitlines():
    f = ln.split()
    if len(f) < 5:
        continue
    lo, hi = (int(x, 16) for x in f[0].split("-"))
    if "x" in f[1] and "w" in f[1]:
        perm, name = f[1], f[-1]
npages = (hi - lo) // PAGE
blk = b["proc"]["smaps"].split(name, 1)[1]
vmflags = [l for l in blk.splitlines() if l.startswith("VmFlags")][0].split()[1:]
assert "dd" in vmflags               # VM_DONTDUMP -> core 必然跳过

# 3. pagemap -> PFN（低 55 位，bit63 是 present）
pfn = []
for ln in b["proc"]["pagemap"].splitlines():
    ln = ln.strip()
    if not ln or ln.startswith("#"):
        continue
    va, ent = ln.split()
    e = int(ent, 16)
    assert e >> 63 == 1
    pfn.append(e & ((1 << 55) - 1))
# assert pfn == list(range(pfn[0], pfn[0] + npages))   # PFN 连续

# 4. 物理偏移取页
raw = read_phys(pfn[0] * PAGE, npages * PAGE)
assert raw[:4] == b"TLM1"
n = struct.unpack("<I", raw[4:8])[0]                  # 小端 u32 = 42

# 5. 密钥取 environ 的 COL_KEY，重复密钥异或
key = b"quasar"
for rec in b["proc"]["environ"].split("^@"):
    if rec.startswith("COL_KEY="):
        key = rec.split("=", 1)[1].strip().encode()
pt = xor(raw[8:8 + n], key)
print(pt.decode())                                    # CTF2{...}
assert raw.find(b"TLM1", 4) < 0                       # 只有一条记录
# CTF2{85027e23-8b37-43f8-94f8-896d61941bcd}