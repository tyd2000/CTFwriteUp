#!/opt/sage/venv/bin/ python3
# -*- coding: utf-8 -*-
"""
CTF RSA Parity Oracle Attack (Adaptive Chosen Ciphertext)
Target: Recover plaintext from ciphertext using a signing oracle that leaks parity info.
Server: pwn.challenge.ctf.show:28144 (or 28276)

Based on the "Never gonna..." challenge with custom hash and Jacobi symbol leakage.
"""
import sys
import socket
import hashlib
from sage.all import kronecker
from Crypto.Util.number import bytes_to_long, long_to_bytes
N = 18546721845979927569500143751660105533561486316231224465080625317376238264944740878457193385226698959802719372533690834284860737851929107163579187879895388120942312652954549671398264315985738386063687826049340153475764762320419809887400141782272319772175613926330746384510813184415900331770119033044622690940477810277396517358312757248120240055407842257982535105406966617903737782220404404644459553334905091694987679788339901767262741660223359618116200505397580036748964773373441655648565481823043475551779287949673519191553190302422175246969165641890331993628578551062334369824625164536808726394693221961254696074691
e = 65537
p = 24074624372939710957902553829568388349796810585932597965247721110129830468800036256026076982213498961372616008101708874099574700088150475222639563817914865052788850184089778132465415340980378135746900061263517304153485433985299953682148733981366808528082636204740025363446729188464380931250501761664305346381138286856186476986484913576109916879190154878781616175599052154216615394032414499234529973797040464698872321982946683153298157064531262284470661150270186224788419122959403896437988552792877168892664837002108590144855389176310488655364026719942320436915792611600545729690463037233338070404315644982404557646573
g = 2
# nc pwn.challenge.ctf.show 28276
HOST = 'pwn.challenge.ctf.show'
PORT = 28276
def H(x: bytes) -> int:
    """Domain-separated 1024-bit hash as integer."""
    return bytes_to_long(
        hashlib.sha512(b"Never gonna make you cry" + x).digest() +
        hashlib.sha512(b"Never gonna say goodbye" + x).digest()
    )

def HH(r: int) -> int:
    """Hash used in signature verification: H(r || fixed string)."""
    return H(str(r).encode() + b"Never gonna tell a lie and hurt you")


def get_parity(r: int, s: int) -> tuple[bool, int]:
    """
    Determine if we can extract message parity.
    Returns (valid, parity_bit), where parity_bit = m % 2.
    Uses Jacobi symbol (kronecker) to infer k's parity.
    """
    e_val = HH(r)
    if e_val % 2 == 0:
        # Cannot determine parity if e is even
        return False, 0

    # k_parity = 1 iff kronecker(r, p) == -1 (i.e., r is non-residue mod p)
    k_parity = 1 if kronecker(r, p) == -1 else 0
    s_parity = s % 2

    # From signature equation: s ≡ k - x·e (mod q) → mod 2: s ≡ k - x·e ⇒ x ≡ k - s (mod 2) since e odd
    # But here oracle gives us s for input x = c' (ciphertext), so m = x, thus m_parity = (k_parity - s_parity) % 2
    m_parity = (k_parity - s_parity) % 2
    return True, m_parity


def recv_line(sock):
    """Receive until newline."""
    buf = b''
    while b'\n' not in buf:
        chunk = sock.recv(1)
        if not chunk:
            break
        buf += chunk
    return buf.strip()

if __name__ == '__main__':
    # Connect and get encrypted flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    banner = sock.recv(4096).decode()
    print("Banner:", repr(banner))
    # Extract encflag: "We're no strangers to love: <encflag>"
    lines = banner.strip().split('\n')
    encflag = None
    for line in lines:
        if "We're no strangers to love:" in line:
            encflag = int(line.split(':', 1)[1].strip())
            break
    else:
        raise RuntimeError("Failed to extract encrypted flag from server response!")
    print("Encrypted flag:", encflag)
    # Initial bounds for binary search
    low, high = 0, N
    current_ct = (pow(2, e, N) * encflag) % N  # Start with 2^e * c mod N
    call_count = 0
    valid_count = 0
    while high - low > 1:
        try:
            # Send current ciphertext
            sock.sendall(f"{current_ct}\n".encode())
            call_count += 1
            # Receive response
            line1 = recv_line(sock).decode()
            line2 = recv_line(sock).decode()
            print("Response lines:", repr(line1), repr(line2))
            # Parse r and s
            if "Never gonna give you up:" in line1:
                r = int(line1.split(': ')[1])
            else:
                raise ValueError("Unexpected format")
            if "Never gonna let you down:" in line2:
                s = int(line2.split(': ')[1])
            else:
                # Sometimes s spans two lines? Handle carefully.
                extra = recv_line(sock).decode()
                s_str = line2.split(': ')[1] + extra
                s = int(s_str)        
            print(f"r = {r}, s = {s}")
            valid, parity = get_parity(r, s)
            if valid:
                valid_count += 1
                mid = (low + high) // 2
                if parity == 1:
                    low = mid
                else:
                    high = mid
                print(f"[{call_count}] Valid! Parity={parity}, Range size: {high - low}")
            else:
                print(f"[{call_count}] Skipped (e(r) even)")
            # Update ciphertext: multiply by 2^e mod N (i.e., shift m left by 1 bit)
            current_ct = (current_ct * pow(2, e, N)) % N
            print(f"[{call_count}] Range: [{low}, {high})")
            if high - low < 10000:
                print("Narrow range! Trying brute-force...")
                break
        except Exception as ex:
            print("Error:", ex)
            # Reconnect on failure (server may close connection)
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            # Skip re-fetching flag; assume same session or reconnect logic handled externally
            continue
    # Brute-force
    for x in range(low, min(high, low + 20000)):
        if pow(x, e, N) == encflag:
            print("🎉 FLAG FOUND:", long_to_bytes(x))
            break
    else:
        print("Failed to recover flag.❌Flag not found in range.")
    sock.close()