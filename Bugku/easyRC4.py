def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key):
    S = KSA(key)
    return PRGA(S)

# 核心解密函数
def decrypt(enc_list, key_str):
    # 将密钥字符串转为 ASCII 列表
    key_ascii = [ord(c) for c in key_str]
    # 生成密钥流
    keystream = RC4(key_ascii)
    
    flag = ""
    for num in enc_list:
        # 密文数字 ^ 密钥流字节 = 明文字符的 ASCII 码
        flag += chr(num ^ next(keystream))
    return flag

if __name__ == "__main__":
    Key = "WhereIsTheFLAG"
    enc = [195, 9, 221, 178, 213, 181, 65, 218, 40, 240, 50, 46, 100, 185, 192, 60, 123, 5, 131, 46, 171, 112, 91, 101, 100, 20, 11]
    
    # 调用解密函数
    flag = decrypt(enc, Key)
    print("解密结果:", flag)
    # flag{wOw!Y0u_F1nd_th3_Flag}