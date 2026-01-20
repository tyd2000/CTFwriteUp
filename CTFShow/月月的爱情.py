import hashlib
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int):
    """
    OpenSSL EVP_BytesToKey 实现（MD5, 1 次迭代）
    """
    d = d_i = b''
    while len(d) < key_len + iv_len:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]

def openssl_decrypt(encrypted_data_b64: str, password: str) -> bytes:
    encrypted_data = b64decode(encrypted_data_b64)
    # 检查是否以 "Salted__" 开头
    if encrypted_data[:8] != b'Salted__':
        raise ValueError("Not a valid OpenSSL salted format")
    salt = encrypted_data[8:16]
    ciphertext = encrypted_data[16:] 
    # 使用 EVP_BytesToKey 生成 key 和 iv（AES-256 需要 32 字节 key，16 字节 IV）
    key, iv = evp_bytes_to_key(password.encode(), salt, 32, 16)
    # 创建 AES 解密器（CBC 模式）
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

def morse_decode(ciphertext:str) -> str:
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z',
        '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
        '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'
    }
    plaintext = ''.join(morse_dict.get(code, '?') for code in ciphertext.split())
    return plaintext

s = 'VTJGc2RHVmtYMS9iVkY0NXp5dGxrZUVoZWZBcWtwSFFkTXF0VUxrMk9pYkxxNzlOSEpNbTlyUDNDdGtLckU0MQpDYUJKbU1JVmNVVlNiM0l6cEhldVd3PT0='
ciphertext_b64 = b64decode(s).decode('utf-8')
# U2FsdGVkX1/bVF45zytlkeEhefAqkpHQdMqtULk2OibLq79NHJMm9rP3CtkKrE41\nCaBJmMIVcUVSb3IzpHeuWw==
hint = ".--. .- ... ... .-- --- .-. -.. .. ... -.-- ..- . -.-- ..- . -.... -.... -...."
password = morse_decode(hint)[10:]  # PASSWORDISYUEYUE666
# print(password) # YUEYUE666
decrypted = openssl_decrypt(ciphertext_b64, password)
flag = decrypted.decode('utf-8')
print(flag)
# ctfshow{W0w_th3_st0ry_s0_w0nderfu1!}