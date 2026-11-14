from PIL import Image
import struct

def read_png_chunks(path):
    with open(path,"rb") as f:
        raw = f.read()
    pos = 8
    comment_data = b""
    while pos < len(raw):
        length = struct.unpack(">I", raw[pos:pos+4])[0]
        ctype = raw[pos+4:pos+8]
        content = raw[pos+8:pos+8+length]
        if ctype == b"tEXt":
            idx = content.find(b"\x00")
            key = content[:idx]
            val = content[idx+1:]
            if key == b"Comment":
                comment_data = val
        pos = pos + 12 + length
    return comment_data

# 读取TLS数据包
tls_packet = read_png_chunks("bleeding_ghost.png")
_, _, rec_len = struct.unpack(">BHH", tls_packet[:5])
heartbeat_msg = tls_packet[5:5+rec_len]

# 标准3字节心跳头解析（本题关键）
hb_type = heartbeat_msg[0]
hb_payload_len = struct.unpack(">H", heartbeat_msg[1:3])[0]
hb_cipher = heartbeat_msg[3:3+hb_payload_len]

# 出题人隐藏密钥生成算法
im = Image.open("bleeding_ghost.png")
w, h = im.size
digits = [2,0,1,4,0,1,6,0]
key40 = []

for i in range(40):
    d_idx = i % 8
    y = (digits[d_idx]*100 + digits[(d_idx+1)%8]*10 + digits[(d_idx+2)%8] + i*113) % 941
    x = (digits[(d_idx+3)%8]*200 + digits[d_idx]*70 + i*211) % 1672
    x = max(0, min(x, w-1))
    y = max(0, min(y, h-1))
    r,g,b = im.getpixel((x,y))
    ch = i % 3
    if ch == 0:
        key40.append(r)
    elif ch == 1:
        key40.append(g)
    else:
        key40.append(b)

key40 = bytes(key40)

# 流式XOR解密
def xor_stream(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

res = xor_stream(hb_cipher, key40)
flag = res[:36].decode()
print(flag)
# flag{h34rtbl33d_kb_0v3rr34d_m3m0ry}