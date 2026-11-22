#!/usr/bin/env python3
# Confidence-only oracle attack: RBF classifier inversion + membership residual test.
import socket, ssl, re, math, sys, time

HOST = sys.argv[1] if len(sys.argv) > 1 else "20f9e130d933dd539977d617.tcp-ctf2.dasctf.com"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

CAND = {
    1: [110, 52, 101, 49, 97, 110],   # n4e1an
    2: [116, 48, 100, 51, 92, 111],   # t0d3\o
    3: [104, 54, 102, 45, 98, 112],   # h6f-bp
    4: [113, 55, 104, 53, 101, 114],   # q7h5er
    5: [107, 45, 104, 50, 99, 107],   # k-h2ck
    6: [112, 53, 95, 47, 101, 110],   # p5_/en
}

LINE_RE = re.compile(
    r"ALLOW\s+(-?\d+(?:\.\d+)?)\s+REVIEW\s+(-?\d+(?:\.\d+)?)\s+VAULT\s+(-?\d+(?:\.\d+)?)",
    re.I,
)


class Oracle:
    def __init__(self, host, port, timeout=20):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        raw = socket.create_connection((host, port), timeout=timeout)
        self.s = ctx.wrap_socket(raw, server_hostname=host)  # SNI is mandatory
        self.s.settimeout(timeout)
        self.f = self.s.makefile("rwb", buffering=0)
        self.cache = {}
        self.n = 0
        self.banner = []

    def _readline(self):
        line = self.f.readline()
        if not line:
            raise EOFError("server closed connection")
        return line.decode("utf-8", "replace").strip()

    def query(self, feats):
        key = tuple(int(v) for v in feats)
        if key in self.cache:
            return self.cache[key]
        self.f.write(("QUERY " + " ".join(map(str, key)) + "\n").encode())
        for _ in range(25):
            try:
                line = self._readline()
            except socket.timeout:
                raise RuntimeError("timeout waiting for QUERY reply")
            if not line:
                continue
            m = LINE_RE.search(line)
            if m:
                self.n += 1
                val = tuple(float(g) for g in m.groups())
                self.cache[key] = val
                return val
            # keep non-matching lines (banner/prompt) for diagnostics
            self.banner.append(line)
        raise RuntimeError("no confidence line in reply")

    def submit(self, token, cid):
        self.f.write(("SUBMIT %s %d\n" % (token, cid)).encode())
        out = []
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                line = self._readline()
            except socket.timeout:
                break
            except EOFError:
                out.append("<EOF>")
                break
            out.append(line)
            if "FLAG" in line.upper() or "CTF" in line.upper():
                # drain a little more
                try:
                    while True:
                        self.s.settimeout(2)
                        line = self._readline()
                        out.append(line)
                except Exception:
                    pass
                break
        return out


def main():
    o = Oracle(HOST, PORT)
    print("[*] connected to %s:%d" % (HOST, PORT))

    # 0) baseline + candidates
    base = CAND[1]
    print("[*] base VAULT =", o.query(base)[2])
    print("[*] candidate direct reads:")
    for cid, x in CAND.items():
        a, r, v = o.query(x)
        print("    #%d %-12s ALLOW=%8.3f REVIEW=%8.3f VAULT=%8.3f" %
              (cid, "".join(chr(c) for c in x), a, r, v))

    if o.banner:
        print("[*] server extra lines:", o.banner[:10])

    # 1) locate prototype by per-dimension argmax scan (kernel is localized)
    #    start point = candidate whose VAULT response is largest (non-zero => inside a kernel)
    start = max(CAND.values(), key=lambda x: o.query(x)[2])

    def scan_dim(start_pt, dim, ch):
        best_v, best_x = -1.0, start_pt[dim]
        for v in range(127):
            p = list(start_pt)
            p[dim] = v
            val = o.query(p)[ch]
            if val > best_v:
                best_v, best_x = val, v
        return best_x, best_v

    center = list(start)
    for d in range(6):
        center[d], _ = scan_dim(center, d, 2)
        print("[*] VAULT dim %d -> %d (%r)" % (d, center[d], chr(center[d]) if 32 <= center[d] < 127 else "?"))

    # hill climb to exact peak (argmax scan may be off when coords interact)
    best = o.query(center)[2]
    moved = True
    while moved:
        moved = False
        for d in range(6):
            for step in (-1, 1):
                y = list(center)
                y[d] += step
                if not 0 <= y[d] <= 126:
                    continue
                val = o.query(y)[2]
                if val > best + 1e-9:
                    center, best, moved = y, val, True
    V = tuple(center)
    token = "".join(chr(c) for c in V)
    print("[+] VAULT prototype =", V, "peak =", best, "token =", repr(token))

    # 2) kernel shape check: 100*exp(-d^2/72) on single-axis offsets
    print("[*] kernel checks (offset -> observed vs model):")
    for off in (1, 2, 3, 4):
        p = list(V)
        p[0] += off
        if p[0] > 126:
            p[0] = V[0] - off
        obs = o.query(p)[2]
        model = 100.0 * math.exp(-(off ** 2) / 72.0)
        print("    off=%d obs=%.4f model=%.4f" % (off, obs, model))

    # 3) membership by residual against the analytic VAULT class kernel
    def gauss(x, c):
        return 100.0 * math.exp(-sum((a - b) ** 2 for a, b in zip(x, c)) / 72.0)

    print("[*] residuals (VAULT observed - pure class kernel):")
    residuals = {}
    for cid, x in CAND.items():
        got = o.query(x)
        resid = got[2] - gauss(x, V)
        residuals[cid] = resid
        print("    #%d %-12s got=%8.4f pure=%8.4f resid=%+9.4f" %
              (cid, "".join(chr(c) for c in x), got[2], gauss(x, V), resid))

    member = max(residuals, key=lambda k: residuals[k])
    print("[+] member candidate =", member, "resid = %+0.4f" % residuals[member])

    # sanity: uniqueness must be clear
    others = [r for k, r in residuals.items() if k != member]
    if residuals[member] < 1.0:
        print("[-] no clear member residual; aborting submit")
        return
    if max(others) > residuals[member] * 0.05:
        print("[!] warning: residual not unique:", residuals)

    # 4) submit
    print("[*] SUBMIT %s %d" % (token, member))
    out = o.submit(token, member)
    for line in out:
        print("    " + line)

    m = re.search(r"CTF2?\{[^}]+\}", "\n".join(out))
    if m:
        print("[FLAG]", m.group(0))
    # CTF2{108b8203-4a89-47b9-997a-6d1014b580c1}

if __name__ == "__main__":
    main()
