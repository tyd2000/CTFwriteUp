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

token = 'eyJBRyI6Ijk0YzUxMTExMzZmZDMyY30iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJGTCI6ImN0Zmh1YntkN2Q2YTdlNTAifQ.R1vt_3OMolyUUIHw-RWDxF-9R8Z_63kWxcCXrFKT_pw'
(h, p, s) = jwt_decode(token)
print("Header:", h)
# Header: {'AG': '94c5111136fd32c}', 'typ': 'JWT', 'alg': 'HS256'}
print("Payload:", p)
# Payload: {'username': 'admin', 'password': '123', 'FL': 'ctfhub{d7d6a7e50'}
flag = p['FL']+h['AG']
print(flag)
# ctfhub{d7d6a7e5094c5111136fd32c}