"""看得见的两层 - 解题脚本
思路: IHDR 声明 800x600, 但 IDAT 解压后含 1400 行原始扫描行(每行 1+800*4 字节),
      第 0~599 行为可见壁纸, 第 600~1399 行为隐藏的 800x800 黑白二维码。
"""
import struct, zlib, base64
import numpy as np
import cv2
from PIL import Image

PNG = r"E:/AI/tmp/look.png"
W, H = 800, 600
STRIDE = 1 + W * 4

# 1) 取 IHDR 与 tEXt 注释
data = open(PNG, "rb").read()
p, idat = 8, b""
while p < len(data):
    ln = struct.unpack(">I", data[p:p + 4])[0]
    typ = data[p + 4:p + 8]
    if typ == b"tEXt":
        print("[第一层] 注释:", data[p + 8:p + 8 + ln].split(b"\x00")[1].decode())
    if typ == b"IDAT":
        idat += data[p + 8:p + 8 + ln]
    p += 12 + ln

# 2) 解压后按行重新切分, 超出 IHDR 高度的部分即第二层
raw = zlib.decompress(idat)
rows = len(raw) // STRIDE
print(f"声明高度 {H}, 实际扫描行 {rows}, 多出 {rows - H} 行")
assert len(raw) % STRIDE == 0
img = np.frombuffer(raw, np.uint8).reshape(rows, STRIDE)[:, 1:].reshape(rows, W, 4)

Image.fromarray(img[:H]).save("layer1_visible.png")
Image.fromarray(img[H:]).save("layer2_hidden.png")

# 3) 解码第二层二维码
qr = cv2.imread("layer2_hidden.png")
content, _, _ = cv2.QRCodeDetector().detectAndDecode(qr)
print("[第二层] 二维码内容:", content)
flag = base64.b64decode(content).decode()
print("[FLAG]", flag)
# flag{tw0_l4y3rs_1n_0n3_png}