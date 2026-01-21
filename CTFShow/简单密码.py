def encrypt_string(s):
    """将输入的字符串进行加密，逐个字节递增加"""
    encrypted_bytes = bytearray(s, 'utf-8')
    for i in range(len(encrypted_bytes)):
        encrypted_bytes[i] += (i + 1)
    return encrypted_bytes.hex()

def decrypt_string(hex_string):
    """将加密后的16进制字符串解密"""
    encrypted_bytes = bytearray.fromhex(hex_string)
    for i in range(len(encrypted_bytes)):
        encrypted_bytes[i] -= (i + 1)
    return encrypted_bytes.decode('utf-8')

def main():
    print("选择功能：")
    print("1. 加密字符串")
    print("2. 解密字符串")
    choice = input("输入你的选择（1 或 2）：")

    if choice == '1':
        plaintext = input("输入要加密的字符串：")
        encrypted_string = encrypt_string(plaintext)
        print(f"加密后的字符串：{encrypted_string}")
    elif choice == '2':
        hex_string = input("输入加密后的16进制字符串：")
        decrypted_string = decrypt_string(hex_string)
        print(f"解密后的字符串：{decrypted_string}")
    else:
        print("无效的选择，请输入1或2。")

if __name__ == "__main__":
    main()
