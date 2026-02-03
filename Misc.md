# Misc

## BUUCTF

### [签到](https://buuoj.cn/challenges#%E7%AD%BE%E5%88%B0)

提交`flag{buu_ctf}`即可。

------

### [金三胖](https://buuoj.cn/challenges#%E9%87%91%E4%B8%89%E8%83%96)

这题的附件是`.gif`文件，查看`gif`的时候发现有一帧出现了`flag`，编写`Python`代码将`gif`动态图按帧分解为多张静态图片。

```python
from PIL import Image, ImageSequence

src = 'aaa.gif'
suffix='png'
with Image.open(src) as img:
    i = 0
    for frame in ImageSequence.Iterator(img):
        i += 1
        frame.save(f"{i}.{suffix}")
```

程序运行结束后，可以在`21.png`看到`flag{`，`51.png`看到`he11o`，`79.png`看到`hongke}`，提交`flag{he11ohongke}`即可。

------

### [二维码](https://buuoj.cn/challenges#%E4%BA%8C%E7%BB%B4%E7%A0%81)

这题的附件是一个二维码，扫描后显示`secret is here`，并没有什么信息。用`WinHex`打开发现`4number.txt`，盲猜文件里含有`.txt`文件，使用命令行`foremost -i QR_code.png`或者`binwalk -e QR_code.png`可以分离出图片和压缩包，压缩包被加密啦。

使用`fcrackzip`对压缩包进行爆破，根据`4number.txt`这一提示可知密码是4位数字。`fcrackzip`的一些参数如下：

> -b 表示使用暴力破解的方式
>
> -c 'aA1'表示使用大小写字母和数字混合破解的方式
>
> -l 1-16 表示需要破解的密码长度为1~10位
>
> -u 表示只显示破解出来的密码，尝试错误的密码不被显示

我们采用4位数字的暴力破解的方式可以得出压缩包密码是`7639`。

```bash
┌──(tyd㉿kali-linux)-[~/ctf/misc/buuctf]
└─$ fcrackzip -b -c '1' -l 4 -u 1D7.zip

PASSWORD FOUND!!!!: pw == 7639
```

解压缩后打开新的`4number.txt`文件得到`CTF{vjpw_wnoei}`，提交`flag{vjpw_wnoei}`即可。

------

### [你竟然赶我走](https://buuoj.cn/challenges#%E4%BD%A0%E7%AB%9F%E7%84%B6%E8%B5%B6%E6%88%91%E8%B5%B0)

这题附件是一个`.jpg`图片，使用`WinHex`打开文件后，在末尾可以看到相应的`ASCII`码信息`flag IS flag{stego_is_s0_bor1ing}`，提交`flag{stego_is_s0_bor1ing}`即可。也可以用`stegSolve`打开，然后`Analyse`→`File Format`在`Ascii`中发现`flag`。

------

### [N种方法解决](https://buuoj.cn/challenges#N%E7%A7%8D%E6%96%B9%E6%B3%95%E8%A7%A3%E5%86%B3)

这题附件是`KEY.exe`，使用`WinHex`打开文件后，发现`ASCII`码信息如下：

```
data:image/jpg;base64,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
```

直接将以上信息复制到`Google Chrome`的网址输入栏中，按下回车键后可以看到一张二维码图片，使用`QR Research`扫描后可以得到`KEY{dca57f966e4e4e31fd5b15417da63269}`，提交`flag{dca57f966e4e4e31fd5b15417da63269}`即可。

------

### [大白](https://buuoj.cn/challenges#%E5%A4%A7%E7%99%BD)

这题附件是`dabai.png`，用`tweakpng`打开图片会弹出提示框`Incorrect crc for IHDR chunk (is 6d7c7135, should be 8e14dfcf)`，双击`IHDR`的`CRC`，把图片的`Height`设置为和`Width`一样的`679`后保存，重新打开图片可以看到`flag{He1l0_d4_ba1}`。

------

### [基础破解](https://buuoj.cn/challenges#%E5%9F%BA%E7%A1%80%E7%A0%B4%E8%A7%A3)

这题附件是`.rar`压缩包，根据题目描述可知密码是四位数字，暴力破解后发现解压密码是`2563`，解压缩后打开`flag.txt`得到`base64`加密后的字符串，编写`Python`代码进行`base64`解码：

```python
from base64 import *

flag = b64decode('ZmxhZ3s3MDM1NDMwMGE1MTAwYmE3ODA2ODgwNTY2MWI5M2E1Y30=').decode('utf-8')
print(flag) # flag{70354300a5100ba78068805661b93a5c}
```

提交`flag{70354300a5100ba78068805661b93a5c}`即可。

------

### [乌镇峰会种图](https://buuoj.cn/challenges#%E4%B9%8C%E9%95%87%E5%B3%B0%E4%BC%9A%E7%A7%8D%E5%9B%BE)

这题附件是一个`.jpg`图片，使用`WinHex`打开文件后，在末尾可以看到相应的`ASCII`码信息`flag IS flag{stego_is_s0_bor1ing}`，提交`flag{97314e7864a8f62627b26f3f998c37f1}`即可。也可以用`stegSolve`打开，然后`Analyse`→`File Format`在`Ascii`中发现`flag`。

------

### [文件中的秘密](https://buuoj.cn/challenges#%E6%96%87%E4%BB%B6%E4%B8%AD%E7%9A%84%E7%A7%98%E5%AF%86)

这题附件是一个`.jpeg`图片，右键→属性→详细信息，可以在备注看到`flag{870c5a72806115cb5439345d8b014396}`。

------

### [wireshark](https://buuoj.cn/challenges#wireshark)

这题的附件是`.pcap`文件，用`wireshark`打开后，根据题目提示输入`http.request.method==POST`直接过滤出`POST`流量包，可以看到`password`，题目描述说管理员的密码就是答案，因此提交`flag{ffb7567a1d4f4abdffdb54e022f8facd}`即可。

------

### [LSB](https://buuoj.cn/challenges#LSB)

这题的附件是`.png`，根据题目名称，用`StegSolve`打开图片，进行`Data Extract`，`Bit Order`设置`LSB first`，`Bit Planes`勾选`Red 0`，`Green 0`，`Blue 0`，点击`Save Bin`保存覆盖原文件，可以得到一张二维码，使用`QR Research`扫描二维码得到`cumtctf{1sb_i4_s0_Ea4y}`，提交`flag{1sb_i4_s0_Ea4y}`即可。

------

### [rar](https://buuoj.cn/challenges#rar)

这题的附件是`.rar`，根据题目提示可知该`.rar`文件的密码是`4`位纯数字，使用`ARCHPR`对压缩包进行4位纯数字密码爆破可得解压密码为`8795`，解压缩后在`.txt`文件中可以看到`flag{1773c5da790bd3caff38e3decd180eb7}`，提交即可。

------

### Yesec no drumsticks

题目描述：

> Yesec是个老涩逼（lsb），所以要给他扣鸡腿

附件是`.png`，根据题目描述的提示，用`StegSolve`打开图片，进行`Data Extract`，`Bit Order`设置`LSB first`，`Bit Planes`勾选`Red 0`，`Green 0`，`Blue 0`，点击`Preview`预览，可以看到`flag{Yesec_1s_lsb}`，提交即可。

------

### qsdz's girlfriend

题目描述：

> 我失忆了，这是我在我桌面上发现的压缩包，可是我忘记了压缩包密码了...请问你能帮助我找到我女朋友的名字吗？flag格式为：flag{女朋友名字_女朋友生日}

根据题目描述，压缩包的密码很可能是女朋友生日，生日作为密码，可能是`6`位，可能是`8`位，但一定是纯数字，设置好范围后，使用`Advanced Archive Password Recovery`暴力破解，得到密码`20031201`，解压缩后得到一张图片。

![](https://paper.tanyaodan.com/BUUCTF/qsdz's_girlfriend/girlfriend.png)

这是音乐游戏**Arcaea**里的光，`WinHex`打开图片可以在文件末尾看见隐藏信息：

```
TXkgZ2lybGZyaWVuZCdzIG5hbWUgaGFzIHNpeCBsZXR0ZXJzIGFuZCB0aGUgZmlyc3QgbGV0dGVyIGlzIGNhcGl0YWxpemVk
```

`base64`解码得到：

```
My girlfriend's name has six letters and the first letter is capitalized
```

他女朋友名字有六个字母且首字母大写。重新回到韵律源点这款音乐游戏，姓名为“光”的日文“ひかり”所对应的罗马音为“Hikari”。最终构造出`flag`为`flag{Hikari_20031201}`。

------

### EzSnake

题目描述：达到114分即可获得一个一个一个一个flag。题目附件给出一个`EzSnake.jar`文件，直接用[**jd-gui**](https://github.com/java-decompiler/jd-gui)或[**Luyten**](https://github.com/deathmarine/Luyten)这种`jar`包反编译工具打开`jar`包进行解码后，全部保存在文件夹`decompiled-EzSnake`中。用`IDEA`对`decompiled-EzSnake\top\woodwhale\snake\GamePanel.java`文件进行修改，把`114`改成一个很小的数字，比如`1`。重新编译运行项目，如果报错`java: 对Timer的引用不明确`的话，在`GamePanel`中添加以下代码即可：

```java
import javax.swing.Timer;
```

编译运行项目，只要得到一分就能弹出来提示框：

![](https://paper.tanyaodan.com/BUUCTF/EzSnake/1.png)

很明显，这是一张少了三个锚点的二维码，用Photoshop把锚点加上即可识别。

![](https://paper.tanyaodan.com/BUUCTF/EzSnake/2.png)

扫描二维码的结果如下：

```
ZmxhZ3tZMHVfNHJlXzBuZV9vTmVfMG5FX3N0NFJ9=
```

这是一个`base64`字符串，编写`Python`代码进行解码可得`flag{Y0u_4re_0ne_oNe_0nE_st4R}`。

```python
from base64 import *

flag = b64decode('ZmxhZ3tZMHVfNHJlXzBuZV9vTmVfMG5FX3N0NFJ9=').decode()
print(flag) # flag{Y0u_4re_0ne_oNe_0nE_st4R}
```

------



## PwnTheBox

### [迟来的签到题](https://ce.pwnthebox.com/challenges?tag=29&id=962)

题目描述给出的信息如下：

> easy xor???
>
> AAoHAR1XICciX1IlXiBUVFFUIyRRJFRQVyUnVVMnUFcgIiNXXhs=

编写`Python`代码遍历`[0, 256)`进行异或操作，得到`flag{1FAD94C8F2272EB7B261CA35A61FDE18}`。

```python
from base64 import *

s = b64decode('AAoHAR1XICciX1IlXiBUVFFUIyRRJFRQVyUnVVMnUFcgIiNXXhs=')
for i in range(0, 256):
    ans = ''
    for x in s:
        ans += chr(x^i)
    if "flag" in ans:
        print(ans)
```

------

### [对象](https://ce.pwnthebox.com/challenges?type=1&id=497)

打开数据流量包，发现里面有`TCP`和`HTTP`两种协议，直接搜索`flag`没有发现任何信息。挨个观察数据流传输信息，发现大部分数据流都是在传输图片和`gif`，第`188`个数据流是`http`协议数据流，传输的是`text/html`，进行流追踪可以看到 `Hey this is a flag FLAG-GehFMsqCeNvof5szVpB2Dmjx`，提交`FLAG-GehFMsqCeNvof5szVpB2Dmjx`即可。

------

### [文件](https://ce.pwnthebox.com/challenges?type=1&id=149)

这题附件是`key.pcapng`，用`Wireshark`打开数据流量包，发现里面有`TCP`和`HTTP`两种协议，直接输入`http contains "flag"`筛选协议。进行`HTTP`流追踪可以看到`flag{This_is_a_f10g}`，提交即可。

------

### [据说有些数据可以进行多重编码](https://ce.pwnthebox.com/challenges?id=1077)

这题的附件是`.txt`文件，其中内容如下：

```
486d65656d727720516372697a716e7a72707a687271207262205a6278656d7163206e767a612072626b206e65727468706d7863615b32362c34352c31362c35362c31375d2c20686d6b7a657420707a7872706b7a6b2072712061637a2078707a72617a71612068706d617a70206d622061637a205a6278656d716320657262787372787a2072626b2061637a20687670656b2771206e707a2d7a776d627a6261206b70727772616d71612e437a206d71207675617a62206a7265657a6b205a62786572626b2771206272616d76627265206e767a612072626b2061637a20224472706b2076752052677662225b382c32302c33382c31322c37322c34322c332c365d2e436d7120717370676d676d62782068767069712c206d626a65736b6d6278207176777a206a7665657264767072616d7662712c206a7662716d7161207675207264767361203338206e657274712c717662627a61712c206168762065766278206272707072616d677a206e767a77712c2072626b20717a677a707265207661637a70206e767a77712e20436d71206e65727471206372677a20647a7a622061707262716572617a6b206d626176207a677a70742077726c767020656d676d627820657262787372787a2072626b2072707a206e7a70757670777a6b207776707a207675617a62206163726220616376717a20767520726274207661637a70206e65727468706d7863615b31302c36322c31322c35392c332c33382c35312c34352c342c31342c34312c31335d2e0a516372697a716e7a72707a2068727120647670622072626b2070726d717a6b206d622051617072617576706b2d736e76622d526776622e2041637a20697a74206d712076622061636d7120716172787a2e2052612061637a2072787a2076752031382c20637a20777270706d7a6b205262627a2043726163726872742c20686d6163206863767720637a2063726b206163707a7a206a636d656b707a623a20517371726262722c2072626b2061686d627120437277627a612072626b204c736b6d61632e20447a61687a7a6220313538352072626b20313539322c20637a20647a78726220722071736a6a7a7171757365206a72707a7a705b34312c34332c32322c35342c31322c34322c33332c35312c385d206d62204576626b766220727120726220726a6176702c2068706d617a702c2072626b206e727061207668627a702076752072206e6572746d6278206a76776e726274206a7265657a6b2061637a204576706b204a637277647a7065726d62277120577a622c206572617a702069627668622072712061637a20496d6278277120577a622e2041637a20756572782074767320627a7a6b206d7120637a707a3a615474486c545369587a4961677a7351596970684d446467635566616d765a554a444c634d7441427672553d3d2e20437a20726e6e7a727071206176206372677a20707a616d707a6b2061762051617072617576706b2072707673626b20313631332c2068637a707a20637a206b6d7a6b206163707a7a20747a727071206572617a702e20557a6820707a6a76706b7120767520516372697a716e7a72707a2771206e706d6772617a20656d757a20717370676d677a2c2072626b2061637a707a2063727120647a7a62206a7662716d6b7a707264657a20716e7a6a736572616d76622072647673612071736a6320777261617a707120727120636d71206e6374716d6a726520726e6e7a727072626a7a2c20717a667372656d61742c20707a656d786d76737120647a656d7a75712c2072626b2068637a61637a702061637a20687670697120726161706d6473617a6b20617620636d7720687a707a2068706d61617a62206474207661637a70715b31362c34332c33312c332c35342c31322c33332c31352c35395d2e
```

使用`s=bytes.fromhex()`进行`16`进制解码后得到：

```
Hmeemrw Qcrizqnzrpzhrq rb Zbxemqc nvza rbk nerthpmxca[26,45,16,56,17], hmkzet pzxrpkzk rq acz xpzrazqa hpmazp mb acz Zbxemqc erbxsrxz rbk acz hvpek\'q npz-zwmbzba kprwramqa.Cz mq vuazb jreezk Zbxerbk\'q bramvbre nvza rbk acz "Drpk vu Rgvb"[8,20,38,12,72,42,3,6].Cmq qspgmgmbx hvpiq, mbjeskmbx qvwz jveerdvpramvbq, jvbqmqa vu rdvsa 38 nertq,qvbbzaq, ahv evbx brppramgz nvzwq, rbk qzgzpre vaczp nvzwq. Cmq nertq crgz dzzb aprbqerazk mbav zgzpt wrlvp emgmbx erbxsrxz rbk rpz nzpuvpwzk wvpz vuazb acrb acvqz vu rbt vaczp nerthpmxca[10,62,12,59,3,38,51,45,4,14,41,13].\nQcrizqnzrpz hrq dvpb rbk prmqzk mb Qaprauvpk-snvb-Rgvb. Acz izt mq vb acmq qarxz. Ra acz rxz vu 18, cz wrppmzk Rbbz Cracrhrt, hmac hcvw cz crk acpzz jcmekpzb: Qsqrbbr, rbk ahmbq Crwbza rbk Lskmac. Dzahzzb 1585 rbk 1592, cz dzxrb r qsjjzqquse jrpzzp[41,43,22,54,12,42,33,51,8] mb Evbkvb rq rb rjavp, hpmazp, rbk nrpa vhbzp vu r nertmbx jvwnrbt jreezk acz Evpk Jcrwdzpermb\'q Wzb, erazp ibvhb rq acz Imbx\'q Wzb. Acz uerx tvs bzzk mq czpz:aTtHlTSiXzIagzsQYiphMDdgcUfamvZUJDLcMtABvrU==. Cz rnnzrpq av crgz pzampzk av Qaprauvpk rpvsbk 1613, hczpz cz kmzk acpzz tzrpq erazp. Uzh pzjvpkq vu Qcrizqnzrpz\'q npmgraz emuz qspgmgz, rbk aczpz crq dzzb jvbqmkzprdez qnzjseramvb rdvsa qsjc wraazpq rq cmq nctqmjre rnnzrprbjz, qzfsremat, pzemxmvsq dzemzuq, rbk hczaczp acz hvpiq raapmdsazk av cmw hzpz hpmaazb dt vaczpq[16,43,31,3,54,12,33,15,59].
```

接着用 http://www.quipqiup.com/ 进行`quipqiup`解码，得到：

```
William Shakespearewas an English poet and playwright[26,45,16,56,17], widely regarded as the greatest writer in the English language and the world\'s pre-eminent dramatist.He is often called England\'s national poet and the "Bard of Avon"[8,20,38,12,72,42,3,6].His surviving works, including some collaborations, consist of about 38 plays,sonnets, two long narrative poems, and several other poems. His plays have been translated into every major living language and are performed more often than those of any other playwright[10,62,12,59,3,38,51,45,4,14,41,13].\pShakespeare was born and raised in Stratford-upon-Avon. The key is on this stage. At the age of 18, he married Anne Hathaway, with whom he had three children: Susanna, and twins Hamnet and Judith. Between 1585 and 1592, he began a successful career[41,43,22,54,12,42,33,51,8] in London as an actor, writer, and part owner of a playing company called the Lord Chamberlain\'s Men, later known as the King\'s Men. The flag you need is here:tYyWjYUkGeKtveuSZkrwIBbvhFxtioEFCBJhIyTNoaF==. He appears to have retired to Stratford around 1613, where he died three years later. Few records of Shakespeare\'s private life survive, and there has been considerable speculation about such matters as his physical appearance, sexuality, religious beliefs, and whether the works attributed to him were written by others[16,43,31,3,54,12,33,15,59]
```

编写`Python`代码进行异或操作得到`ntio{QAMK-awpoK_ahTDdFl_eoSb_cogpJZCVzbBNn}`。

```python
s = 'tYyWjYUkGeKtveuSZkrwIBbvhFxtioEFCBJhIyTNoaF'
weight = [[26,45,16,56,17],
[8,20,38,12,72,42,3,6],
[10,62,12,59,3,38,51,45,4,14,41,13],
[41,43,22,54,12,42,33,51,8],
[16,43,31,3,54,12,33,15,59]]
weight = sum(weight, [])
flag = [ord(x) ^ y for x, y in zip(s, weight)]
print(bytes(flag)) # ntio{QAMK-awpoK_ahTDdFl_eoSb_cogpJZCVzbBNn}
```

接着进行凯撒密码解密可以得到`flag{ISEC-sohgC_szLVvXd_wgKt_ugyhBRUNrtTFf}`，提交即可。

```python
text = 'ntio{QAMK-awpoK_ahTDdFl_eoSb_cogpJZCVzbBNn}'
flag = ''
for i in range(1, 27):
    s = ''
    for x in text:
        if x.isupper():
            s += chr(ord('A')+(ord(x)-ord('A')+i)%26)
        elif x.islower():
            s += chr(ord('a')+(ord(x)-ord('a')+i)%26)
        else:
            s += x
    if 'flag' in s:
        flag = s
    # print('{}的移位是{}'.format(s, (ord(text[0])-ord(s[0]))%26))

print(flag) # flag{ISEC-sohgC_szLVvXd_wgKt_ugyhBRUNrtTFf}
```

------

## Bugku

### 好多压缩包

下载附件，解压得到 68 个压缩包，并且每个压缩文件里都有一个 4 个字节大小的名为 `data.txt` 的 `txt` 文件，于是尝试用 `CRC32` 碰撞还原出所有压缩包中的文件内容。

循环冗余校验（Cyclic Redundancy Check， CRC）是一种根据网络数据包或计算机文件等数据产生简短固定位数校验码的一种信道编码技术，主要用来检测或校验数据传输或者保存后可能出现的错误。它是利用除法及余数的原理来作错误侦测的。

每个文件都有唯一的 `CRC32` 值，即使文件中有个一个 bit 发生了变化，`CRC32` 值也会不同。`CRC32` 爆破：知道文件中一段数据的长度和文件的 `CRC32` 值，编写脚本程序，利用穷举法与其 `CRC32` 对照，从而达到猜解数据的目的（通常只适用于较小的文本文件，文件太大穷举难度太大）。

```python
import zipfile
import string
import binascii

def CrackCrc(crc):
    for i in dic:
        for j in dic:
            for p in dic:
                for q in dic:
                    s = i + j + p + q
                    if crc == (binascii.crc32(s.encode('utf-8')) & 0xffffffff):
                        # print(s)
                        f.write(s)
                        return

def CrackZip():
    for I in range(68):
        file = 'out' + str(I) + '.zip'
        f = zipfile.ZipFile(file, 'r')
        GetCrc = f.getinfo('data.txt')
        crc = GetCrc.CRC
        #以上3行为获取压缩包CRC32值的步骤
        #print(hex(crc))
        CrackCrc(crc)

dic = string.ascii_letters + string.digits + '+/='

f = open('out.txt', 'w')
CrackZip()
f.close()
```

得到如下内容：

```
z5BzAAANAAAAAAAAAKo+egCAIwBJAAAAVAAAAAKGNKv+a2MdSR0zAwABAAAAQ01UCRUUy91BT5UkSNPoj5hFEVFBRvefHSBCfG0ruGnKnygsMyj8SBaZHxsYHY84LEZ24cXtZ01y3k1K1YJ0vpK9HwqUzb6u9z8igEr3dCCQLQAdAAAAHQAAAAJi0efVT2MdSR0wCAAgAAAAZmxhZy50eHQAsDRpZmZpeCB0aGUgZmlsZSBhbmQgZ2V0IHRoZSBmbGFnxD17AEAHAA==
```

base64 decode 得到：

![](https://paper.tanyaodan.com/Bugku/%E5%A5%BD%E5%A4%9A%E5%8E%8B%E7%BC%A9%E5%8C%85.png)

解码出来的字符串提示包含关键字 `flag.txt`，及字符串 “fix the file and get the flag” 提示修复文件，这里猜测应该是某种文件，但是头尾不完整需要补充

注意到结尾处存在 `rar` 的文件尾 `C43D7B00400700`，但缺少文件头，于是补上 rar 的文件头` 526172211A0700`，保存为新文件得到 `flag`：`flag{nev3r_enc0de_t00_sm4ll_fil3_w1th_zip}`。

------

### 404号

> 一个被时间抹空的 Git 仓库，flag 藏在“看不见的历史”里

下载附件后解压缩得到文件夹`404_timecapsule`，内含`.no_file_here`、`README.md`和`.git`文件夹。

用`git fsck --full`检查`.git`目录中的对象完整性。

用`git reset --hard`回滚到之前提交的历史版本。

用`git log --all`显示仓库中所有分支提交历史。‌

```bash
C:\Users\tyd\Downloads\404_timecapsule>git fsck --full
Checking ref database: 100% (1/1), done.
error in commit ed102331474a5b036d29be77938be8ac8edc6bc5: badDate: invalid author/committer line - bad date
Checking object directories: 100% (256/256), done.
notice: HEAD points to an unborn branch (master)
notice: No default references
dangling commit 47a3f4237ab26d53778bd943a0fa06e7cd6d253a

C:\Users\tyd\Downloads\404_timecapsule>git reset --hard 47a3f4237ab26d53778bd943a0fa06e7cd6d253a
HEAD is now at 47a3f42 你终于来了。时间不是我走的方向。 flag{you_traveled_beyond_time_itself}

C:\Users\tyd\Downloads\404_timecapsule\404_timecapsule>git log --all
commit 47a3f4237ab26d53778bd943a0fa06e7cd6d253a (HEAD -> master)
Author: 404 <404@localhost>
Date:   Tue Jan 19 03:14:07 2038 +0000

    你终于来了。时间不是我走的方向。
    flag{you_traveled_beyond_time_itself}

commit ed102331474a5b036d29be77938be8ac8edc6bc5
Author: 404 <404@localhost>
Date:   Thu Jan 1 00:00:00 1970 +0000

    Initial commit
```

提交`flag{you_traveled_beyond_time_itself}`即可。

------

## CTFSHOW

### 单身杯misc签到

> **重要提示：**
>
> 1. 压缩包密码是5位字符
> 2. lsb有内容
> 3. flag包含5个空格、2个逗号，均替换为下划线，连续只留1个下划线

这道题考点太多了，求解步骤很繁琐，涉及到压缩包密码爆破，lsb隐写，缺失定位块的二维码修复。

下载附件`xxxtentacion.zip`，用`ARCHPR`爆破所有可打印字符，位数为5，得到压缩包密码`61f@X`。

输入密码解压缩后得到图片`xxxtentacion.jpg`，用`010editor`打开图片可以找到`base64`字符串。

在浏览器中输入`data:image/png,base64,`粘贴`base64`字符串可以将其转换为图片，右键保存。

```
data:image/png;base64,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
```

打开图片后，发现这是一张缺少三个定位块的二维码。用`zsteg -a broken_qr.png`检查隐写内容，发现关键内容`ctfshow{Your potential,va`，这是`flag`的前一部分，还需要找另一部分。

```bash
┌──(t0ur1st㉿kali)-[~/problems]
└─$ zsteg -a broken_qr.png
b6,abgr,msb,xy      .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6p,abgr,msb,xy     .. text: ["?" repeated 14 times]
b8,rgb,msb,xy       .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b8,rgba,msb,xy      .. file: RDI Acoustic Doppler Current Profiler (ADCP)
b1,r,lsb,xy,prime   .. file: MPEG ADTS, layer II, v1, 112 kbps, Stereo
b1,r,lsb,yx         .. text: "ctfshow{Your potential,va"
b1,r,msb,yx         .. file: OpenPGP Public Key
b6,abgr,msb,yx      .. file: MPEG ADTS, layer I, v2, 112 kbps, Monaural
b6p,abgr,msb,yx     .. text: ["?" repeated 14 times]
```

补全二维码定位点这里有一个坑，因为我尝试直接修补定位块后扫描二维码但一直解码内容失败。仔细观察后发现这张二维码图片的黑白区域正好相反，用`Stegsolve`打开图片，黑白颠倒转换一下，保存为`turn_black_into_white.png`。编写`Python`代码补全黑白颠倒转换后的二维码的三个定位点并解码。

```python
import numpy as np
from PIL import Image, ImageDraw
import cv2

def detect_qr_structure(image_path):
    """检测QR码结构"""
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    # 转换为灰度图
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    # 使用自适应阈值
    binary = cv2.adaptiveThreshold(gray, 255, 
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 找到最大的轮廓（假设是QR码）
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        # 确保有合理的边界
        x = max(0, x-5)
        y = max(0, y-5)
        w = min(width-x, w+10)
        h = min(height-y, h+10)
        # 裁剪QR码区域
        qr_region = img_array[y:y+h, x:x+w]
        return qr_region, (x, y, w, h)
    return img_array, (0, 0, width, height)

def estimate_module_size(qr_region):
    """估计模块大小"""
    height, width = qr_region.shape[:2]
    # 转换为灰度
    gray = cv2.cvtColor(qr_region, cv2.COLOR_RGB2GRAY)
    # 取中间几行进行采样
    sample_row = gray[height//2, :]
    # 计算黑白转换
    is_black = sample_row < 128
    changes = np.where(is_black[:-1] != is_black[1:])[0]
    if len(changes) > 5:
        # 计算相邻变化之间的距离
        distances = np.diff(changes)
        # 去除异常值（太大或太小的距离）
        median_dist = np.median(distances)
        distances = distances[(distances > median_dist*0.5) & (distances < median_dist*2)]
        module_size = np.median(distances) if len(distances) > 0 else max(1, width // 40)
    else:
        module_size = max(1, width // 40)
    return int(round(module_size))

def create_finder_pattern(module_size):
    """创建定位块图案"""
    # 确保模块大小至少为1
    module_size = max(1, module_size)
    size = 7 * module_size
    # 创建图案
    pattern = np.ones((size, size, 3), dtype=np.uint8) * 255  # 白色背景
    # 绘制黑色边框
    pattern[:module_size, :] = [0, 0, 0]  # 上边框
    pattern[-module_size:, :] = [0, 0, 0]  # 下边框
    pattern[:, :module_size] = [0, 0, 0]  # 左边框
    pattern[:, -module_size:] = [0, 0, 0]  # 右边框
    # 绘制白色边框内的区域
    pattern[module_size:-module_size, module_size:-module_size] = [255, 255, 255]
    # 绘制中心黑色方块 (3x3)
    center_start = 2 * module_size
    center_end = 5 * module_size
    pattern[center_start:center_end, center_start:center_end] = [0, 0, 0]
    # 绘制中心白色点
    white_start = 3 * module_size
    white_end = 4 * module_size
    pattern[white_start:white_end, white_start:white_end] = [255, 255, 255]
    return pattern

def find_qr_corners(qr_region, module_size):
    """查找QR码的角点"""
    height, width = qr_region.shape[:2]
    # 假设标准QR码结构
    # 尝试不同版本 (1-40)
    for version in range(1, 41):
        total_modules = 17 + 4 * version
        estimated_width = total_modules * module_size
        # 如果估计的宽度接近实际宽度，则采用此版本
        if abs(estimated_width - width) <= module_size * 2:
            # 计算角点位置
            finder_size = 7 * module_size
            corners = {
                'top_left': (0, 0),
                'top_right': (0, width - finder_size),
                'bottom_left': (height - finder_size, 0)
            }
            return corners, version
    # 如果无法确定版本，使用默认位置
    finder_size = 7 * module_size
    corners = {
        'top_left': (0, 0),
        'top_right': (0, width - finder_size),
        'bottom_left': (height - finder_size, 0)
    }
    return corners, 1

def repair_qr_code(image_path, output_path='repaired_qr.png'):
    """二维码修复函数"""
    try:
        # 1. 检测并裁剪QR码区域
        qr_region, bbox = detect_qr_structure(image_path)
        print(f"QR码区域: 位置={bbox[0:2]}, 尺寸={bbox[2:4]}")
        # 2. 估计模块大小
        module_size = estimate_module_size(qr_region)
        print(f"估计模块大小: {module_size} 像素")
        # 确保模块大小合理
        if module_size <= 0:
            module_size = max(1, bbox[2] // 40)
            print(f"调整模块大小为: {module_size} 像素")
        # 3. 创建定位块图案
        finder_pattern = create_finder_pattern(module_size)
        pattern_size = finder_pattern.shape[0]
        print(f"定位块尺寸: {pattern_size}x{pattern_size} 像素")
        # 4. 查找角点位置
        corners, version = find_qr_corners(qr_region, module_size)
        print(f"估计QR码版本: {version}")
        print(f"角点位置: {corners}")
        # 5. 复制原始图像
        repaired = qr_region.copy()
        # 6. 在三个角点绘制定位块
        for corner_name, (y, x) in corners.items():
            # 确保坐标有效
            if x >= 0 and y >= 0 and x + pattern_size <= repaired.shape[1] and y + pattern_size <= repaired.shape[0]:
                repaired[y:y+pattern_size, x:x+pattern_size] = finder_pattern
                print(f"在 {corner_name} ({y}, {x}) 绘制定位块")
            else:
                print(f"警告: {corner_name} 位置无效，跳过")
        # 7. 保存修复后的图像
        repaired_img = Image.fromarray(repaired)
        repaired_img.save(output_path)
        print(f"修复完成，图像已保存到: {output_path}")
        # 8. 显示修复后的图像
        repaired_img.show()
        return repaired_img
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        print("尝试备用方法...")
        return repair_qr_code_simple(image_path, output_path)

def decode_qr(image_path: str)->str:
    """ 读取扫描二维码图片解码出QR内容 """
    img = Image.open(image_path)
    from pyzbar import pyzbar
    barcodes = pyzbar.decode(img)
    data = ''.join(barcode.data.decode('utf-8') for barcode in barcodes)
    return data

# 主程序
if __name__ == "__main__":    
    input_image = "turn_black_into_white.png"
    print("开始修复QR码...")
    output_file = "repaired_qr.png"
    repaired = repair_qr_code(input_image, output_file)
    print("\n修复完成！请查看生成的图像文件。")
    try:
        msg = decode_qr(output_file)
        if msg:
            print("解码成功:", msg)
        else:
            print("未检测到有效二维码")
    except Exception as e:
        print("解码失败:", e)
    # ctfshow单身杯misc签到题
    flag = bytes.fromhex(msg).decode()
    # lue, far exceeds your belief}
    flag = 'ctfshow{Your potential,va'+flag
    print(flag)
    # ctfshow{Your potential,value, far exceeds your belief}
    flag = flag.replace(" ", "_").replace(",", "_")
    print(f'🎉Final Flag is found!\n{flag}')
    # ctfshow{Your_potential_value__far_exceeds_your_belief}
```

拿到另一半`flag`后直接拼接提交报错，还需要将`,`和空格全部替换为`_`，这部分代码补充在脚本尾部。`Python`代码的运行结果如下：

```
开始修复QR码...
QR码区域: 位置=(0, 0), 尺寸=(280, 280)
估计模块大小: 7 像素
定位块尺寸: 49x49 像素
估计QR码版本: 6
角点位置: {'top_left': (0, 0), 'top_right': (0, 231), 'bottom_left': (231, 0)}
在 top_left (0, 0) 绘制定位块
在 top_right (0, 231) 绘制定位块
在 bottom_left (231, 0) 绘制定位块
修复完成，图像已保存到: repaired_qr.png

修复完成！请查看生成的图像文件。
解码成功: 6C75652C20666172206578636565647320796F75722062656C6965667D
ctfshow{Your potential,value, far exceeds your belief}
🎉Final Flag is found!
ctfshow{Your_potential_value__far_exceeds_your_belief}
```

提交`ctfshow{Your_potential_value__far_exceeds_your_belief}`即可。

------

### project Tao-1

进入靶机后，首先看到的是`/W4lc0me`。

> 你可以通过访问特定地址来跳转下一关，如/Letsstart，此页面为第0关，请注意关卡。

根据提示访问第一关`/Letsstart`，可以看到以下信息。

```
开始你的CTF秀之旅
要不动动鼠标看看你要干啥？

/some_informations

35903762.log
```

`35903762.log`文件是一段聊天记录，继续访问第二关`/some_informations`。

> 题目在哪呢?
>
> 这个页面会不会有什么错误
>
> 我的意思是，来到这个奇怪名字的页面本身就是一个错误

根据提示可知名字错了，`information`是不可数名词，正确的应该是`some_information`。

访问第三关暨真正的第二关`/some_information`，可以看到一些“可爱的色块”。

```html
<div class="not-here">
    <p>可爱的色块</p>
    <div>
        <div class="color-block" style="background-color: rgb(71,48,111)"></div>
        <div class="color-block" style="background-color: rgb(100,33,32)"></div>
        <div class="color-block" style="background-color: rgb(78,101,120)"></div>
        <div class="color-block" style="background-color: rgb(116,32,105)"></div>
        <div class="color-block" style="background-color: rgb(115,32,47)"></div>
        <div class="color-block" style="background-color: rgb(67,84,70)"></div>
        <div class="color-block" style="background-color: rgb(71,48,100)"></div>
    </div>
    <p class="Log">77665160.log</p>
</div>
```

`77665160.log`是一段聊天记录（hint），我们将颜色的`R`、`G`、`B`值按`ASCII`转为字符串得到下一关。

```python
import re

html_content = """
<div class="not-here">
    <p>可爱的色块</p>
    <div>
        <div class="color-block" style="background-color: rgb(71,48,111)"></div>
        <div class="color-block" style="background-color: rgb(100,33,32)"></div>
        <div class="color-block" style="background-color: rgb(78,101,120)"></div>
        <div class="color-block" style="background-color: rgb(116,32,105)"></div>
        <div class="color-block" style="background-color: rgb(115,32,47)"></div>
        <div class="color-block" style="background-color: rgb(67,84,70)"></div>
        <div class="color-block" style="background-color: rgb(71,48,100)"></div>
    </div>
    <p class="Log">77665160.log</p>
</div>
"""
# Extract RGB values using regex
rgb_values = re.findall(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', html_content)
# Convert RGB values to ASCII
ascii_string = ""
for r, g, b in rgb_values:
    ascii_string += chr(int(r)) + chr(int(g)) + chr(int(b))

print(ascii_string)
# 'G0od! Next is /CTFG0d'
```

 访问第四关`/CTFG0d`，`ctrl+A`选中所有页面可以看到与背景色融为一体的文字。

```
你已经正式通过了考验，来帮套一起逃离这里吧

NTQ1NjVhNTM1NjMwNGQ3YTUyNDY0NjUwNTU2YTUyNDU1MzU2NTI1MzU1NDEzZDNk

这里貌似有几层被子，要不要盖盖？

62399474.log
```

`62399474.log`是一段聊天记录（hint），经过一系列`base64—>base16—>base64—>base32—>reverse`处理，我们可以得到下一关`/N4xtplace`。

```python
from base64 import *
import binascii

s = 'NTQ1NjVhNTM1NjMwNGQ3YTUyNDY0NjUwNTU2YTUyNDU1MzU2NTI1MzU1NDEzZDNk'
# base64解码
b64_decoded = b64decode(s)
# b'54565a5356304d7a52464650556a52455356525355413d3d'
# base16解码
b16_decoded = binascii.unhexlify(b64_decoded)
# b'TVZSV0MzRFFPUjRESVRSUA=='
# base64解码
b64_after_b16 = b64decode(b16_decoded)
# b'MVRWC3DQOR4DITRP'
# base32解码
b32_decoded = b32decode(b64_after_b16)
# b'ecalptx4N/'
# 翻转字符串
s = b32_decoded[::-1].decode()
print(s)
# '/N4xtplace'
```

 访问第五关`/N4xtplace`，`F12`检查可以看到以下内容：

```
<div class="what-happend">
<p>可恶（｀Δ´）ゞ 这到底是什么地方(;｀O´)o</p>
<p>怎么回事(•'╻'• )꒳ᵒ꒳ᵎᵎᵎ 每句话都多了奇怪的东西"(º Д º*)</p>
<p class="n0-look">69766277.log</p>
</div>
<script data-description="magic">
ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); (ﾟДﾟ) =(ﾟΘﾟ)= (o^_^o)/ (o^_^o);(ﾟДﾟ)={ﾟΘﾟ: '_' ,ﾟωﾟﾉ : ((ﾟωﾟﾉ==3) +'_') [ﾟΘﾟ] ,ﾟｰﾟﾉ :(ﾟωﾟﾉ+ '_')[o^_^o -(ﾟΘﾟ)] ,ﾟДﾟﾉ:((ﾟｰﾟ==3) +'_')[ﾟｰﾟ] }; (ﾟДﾟ) [ﾟΘﾟ] =((ﾟωﾟﾉ==3) +'_') [c^_^o];(ﾟДﾟ) ['c'] = ((ﾟДﾟ)+'_') [ (ﾟｰﾟ)+(ﾟｰﾟ)-(ﾟΘﾟ) ];(ﾟДﾟ) ['o'] = ((ﾟДﾟ)+'_') [ﾟΘﾟ];(ﾟoﾟ)=(ﾟДﾟ) ['c']+(ﾟДﾟ) ['o']+(ﾟωﾟﾉ +'_')[ﾟΘﾟ]+ ((ﾟωﾟﾉ==3) +'_') [ﾟｰﾟ] + ((ﾟДﾟ) +'_') [(ﾟｰﾟ)+(ﾟｰﾟ)]+ ((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+((ﾟｰﾟ==3) +'_') [(ﾟｰﾟ) - (ﾟΘﾟ)]+(ﾟДﾟ) ['c']+((ﾟДﾟ)+'_') [(ﾟｰﾟ)+(ﾟｰﾟ)]+ (ﾟДﾟ) ['o']+((ﾟｰﾟ==3) +'_') [ﾟΘﾟ];(ﾟДﾟ) ['_'] =(o^_^o) [ﾟoﾟ] [ﾟoﾟ];(ﾟεﾟ)=((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+ (ﾟДﾟ) .ﾟДﾟﾉ+((ﾟДﾟ)+'_') [(ﾟｰﾟ) + (ﾟｰﾟ)]+((ﾟｰﾟ==3) +'_') [o^_^o -ﾟΘﾟ]+((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+ (ﾟωﾟﾉ +'_') [ﾟΘﾟ]; (ﾟｰﾟ)+=(ﾟΘﾟ); (ﾟДﾟ)[ﾟεﾟ]='\\'; (ﾟДﾟ).ﾟΘﾟﾉ=(ﾟДﾟ+ ﾟｰﾟ)[o^_^o -(ﾟΘﾟ)];(oﾟｰﾟo)=(ﾟωﾟﾉ +'_')[c^_^o];(ﾟДﾟ) [ﾟoﾟ]='\"';(ﾟДﾟ) ['_'] ( (ﾟДﾟ) ['_'] (ﾟεﾟ+(ﾟДﾟ)[ﾟoﾟ]+ (ﾟДﾟ)[ﾟεﾟ]+((ﾟｰﾟ) + (ﾟΘﾟ))+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (o^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ ((o^_^o) +(o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+((o^_^o) +(o^_^o))+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ (o^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (c^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+((o^_^o) +(o^_^o))+ (c^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');
</script>
```

`69766277.log`是一段聊天记录（hint），使用`AAencode`解码得到`/cftla5gsh0w`。

访问第六关`/cftla5gsh0w`，进入一个标题为`no flag here!!!`的页面，可以看到以下信息：

```
题目已经写在页面上了

要不你仔细找找？

找不到咱就放弃吧，套娃题狗都不做

06958446.log
```

访问`06958446.log`查看聊天记录获取`hint`。

```
MuziLog --- Mar 22 2021

套:给我出的考题呢？存心不让我走吗？ 17:02:06

神:已经写在屏幕上了啊... 17:03:18

套:我看我把屏幕抠坏都找不到。 17:06:44

神:已经写在屏幕上了啊！ 17:06:52

套:所以在哪啊？？？ 17:07:39

神:已经写在屏幕上了啊！！！ 17:07:50

CJ:既然他说已经写了那就已经写了吧。 17:15:31

[获得碎片信息]

[获得碎片提示 1]
nn]ch\aXe\WcgR``OUMYKLIP

[获得碎片提示 2]
加减
```

编写`python`代码对其求解，得到`no_flag_means_no_f_l_a_g`。

```python
s = r'nn]ch\aXe\WcgR``OUMYKLIP'
for i in range(len(s)):
    print(chr(ord(s[i])+i),end='')
    
# no_flag_means_no_f_l_a_g
```

意思是把`/cftla5gsh0w`中的`f`、`l`、`a`、`g`这四个字母去掉，去掉后为`/ct5sh0w`。

访问第七关`/ct5sh0w`，看到以下信息：

> 好像什么也没有
>
> 那就当做无事发生
>
> 10654572.log

滚动条可以往下滑啦，右键查看源码发现有一张图片。

```html
<div class="mask"></div>
<img class="hidden flag" src="data:image/png;base64,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">
	<div class="text light" style="top: 5%; transform: translateY(-50%);">
	<p>好像什么也没有</p>
	<p>那就当做无事发生</p>
	<p class="bujiangwude">10654572.log</p>
  </div>
</body>
<!--怎么又看源码,太不讲武德了-->
<!--话说这是缩小版的码吗？-->
```

将图片直接放在浏览器中访问，得到一个打乱的二维码图片，手动修复一下即可用`QR_Research`扫码，得到`/t308g0d`。

继续访问第八关`/t308g0d`，弹出一个提示框`挑战过半!`，点击确定又弹出提示框`送你一个过半的flag吧，仔细找找，格式ctfshow{}`。这还用你说？！累了，右键查看源码。

```html
<div class="not-here">
    <p>看起来他遗忘一张照片</p>
    <p>照片里有什么秘密呢？</p>
    <div>
    <p><a href="./secret_of_name.zip" target="_blank">[photo File]</a></p>
    </div>
    <p class="have-flag">03190886.log</p>
</div>
<script>
    if(!localStorage.getItem("_has_visited")) {
        alert("挑战过半!");
        alert("送你一个过半的flag吧，仔细找找，格式ctfshow{}");
        localStorage.setItem("_has_visited", "true");
    }
</script>
```

附件`/secret_of_name.zip`下载后解压缩，得到图片`secret_of_name.png`。

在[010 Editor官方模板](https://sweetscape.com/010editor/repository/templates/)下载`PNG.bt`后放入`\Documents\SweetScape\010 Templates\Repository`中。

用`010 Editor`打开图片，并运行`PNG.bt`，修改图片高度与宽度`942`一致，保存文件后打开图片，可以看到你想要的，提交`ctfshow{easy_half_and_Ez_flag}`即可。

------

### project Tao-2

这道题的靶机环境跟上一道题是一样的。根据hint可知，“Tao-2的log貌似有点重要”。

上一道题的最后一个`log`文件`03190886.log`的内容如下：

```
MuziLog --- Jun 10 2021

套:这是?

神:这不是你最喜欢的吗?

套:别别别，我可讨厌这玩意了。

神:真搞不懂你。

套:那东西在哪啊？

神:寸头男子是看不到图片上不上写了吗？

套:你再骂？

神:别想太多。

[获得碎片信息]

[获得碎片提示]
注意大小写
```

打开图片`secret_of_name.png`，看到最大的文字是DEADSOUL，尝试访问`/DEADSOUL`，来到第九关。右键查看网页源码如下：

```html
<div class="not-here">
    <p>看起来你有点累了，要不这样吧</p>
    <p>我模仿田一名给你唱首歌吧</p>
    <p>我晒干了沉默🎵,悔得很冲动🎵，就算这是做错也只是怕错过🎵</p>
    <div>
    </div>
    <p class="a-log">38450011.log</p>
    <p class="a-log">你知道知乎在后台日志埋藏了一个彩蛋吗？(注意大小写)</p>
</div>
```

知乎在后台日志的彩蛋就是招聘——`HIRE`。

访问第十关`/HIRE`，右键查看网页源码如下：

```html
<div class="not-here">
    <p>给你看一张图</p>
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAACGklEQVR4nO3TMRGAMADAwFIBlYF/1GCnBnpZYfhXkCXXep97AEfz6wD4M4NAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIBINAMAgEg0AwCASDQDAIhA0E6ANMJb3uMQAAAABJRU5ErkJggm5vbm9ub25vbm9oaW50LHRyeSB5b3VyIGJlc3Qh">
    <div>
    </div>
    <p class="a-log">46082046.log</p>
</div>
```

将图片保存为`a.png`，读取任意像素得到`(14, 215, 177, 38)`，将其转为IP格式`14.215.177.38`，会跳转到百度的首页（现在的IP已经换了），最下方有个About Baidu，所以下一关是`/About_Baidu`。

```
>>> from PIL import Image
>>> pic = Image.open('a.png')
>>> print(pic.getpixel((5,5)))
(14, 215, 177, 38)
```

访问第十一关`/About_Baidu`，查看网页源码如下：

```html
<div class="not-here">
    <p>我来给你吟一首</p>
    <p>巴山夜雨涨秋池，长安大道连狭邪。自笑平生无所着，此地空余黄鹤楼。</p>
    <p>上头了，再来一首</p>
    <p>前不见古人，黄河入海流。灵山多秀色，西北是融州。</p>
    <p class="a-log">99563810.log</p>
</div>
```

“巴山夜雨涨秋池，长安大道连狭邪。自笑平生无所着，此地空余黄鹤楼。”分别对应地名：川渝—西安—郑州—武汉。“前不见古人，黄河入海流。灵山多秀色，西北是融州。”分别对应地名：北京—山西拥挤—庐山—柳川。从百度地图上看，这些地名连线后分别是`n`和`s`的形状，所以下一关是`/ns`。

访问第十二关`/ns`，查看网页源码如下：

```html
<div class="not-here">
<p class="a-log">78716321.log</p>
<p>这次就不磨磨唧唧了</p>
<p>直接告诉你该干什么吧</p>
<p>SAYL7UNIT</p> 
</div>
```

直接访问`/SAYL7UNIT`是不对的，看`log`文件知道与摩斯电码有关，盲猜是摩斯的点和划反过来了，先用摩斯电码加密`SAYL7UNIT`，然后将点和划调换一下即可得到正确的下一关`ONLY2GAME`。

```python
MORSE_CODE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',     'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    
    '0': '-----',  '1': '.----',  '2': '..---',  '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',  '9': '----.',
    
    # 标点符号
    '.': '.-.-.-',   # 句号
    ',': '--..--',   # 逗号
    '?': '..--..',   # 问号
    "'": '.----.',   # 单引号
    '!': '-.-.--',   # 感叹号
    '/': '-..-.',    # 斜杠
    '(': '-.--.',    # 左括号
    ')': '-.--.-',   # 右括号
    '&': '.-...',    # and 符号
    ':': '---...',   # 冒号
    ';': '-.-.-.',   # 分号
    '=': '-...-',    # 等号
    '+': '.-.-.',    # 加号
    '-': '-....-',   # 减号/连字符
    '_': '..--.-',   # 下划线
    '"': '.-..-.',   # 双引号
}

def morse_encrypt(message):
    """将英文文本转换为摩斯电码,默认用点.和划-"""
    cipher = []
    for char in message.upper():
        if char == ' ':
            cipher.append('/')
        elif char in MORSE_CODE_DICT:
            cipher.append(MORSE_CODE_DICT[char])
        # 忽略不支持的字符（如中文、特殊符号等）
    return ' '.join(cipher)

MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()} # Reverse key and value 

def morse_decrypt(ciphertext:str, dot='.', dash='-', sign=' ') -> str:
    '''
    ciphertext => 密文
    dot => 点
    dash => 划
    sign => 分割符
    plaintext => 明文
    '''
    plaintext = ''
    for code in ciphertext.replace(dot,'.').replace(dash,'-').split(sign):
        plaintext += MORSE_DICT[code]
    return plaintext

s = morse_encrypt('SAYL7UNIT')
# '... .- -.-- .-.. --... ..- -. .. -'
# morse_decrypt(s)
# 'SAYL7UNIT'
# 如果直接调换会报错 因为出现重复替换 需要借助中间变量 先将-换成t .换成d 再令t为. d为-
s = s.replace('-', 't').replace('.', 'd')
print(morse_decrypt(s,'t','d',' '))
# 'ONLY2GAME'
```

访问第十三关`/ONLY2GAME`，网页标题是`11011 11001`，右键查看网页源码：

```
<div class="not-here">
<p class="a-log">78716321.log</p>
<p>梅开二度？</p>
<p>-..../...--/--.../.--.-/..--./.--../...--/-..-.</p>
</div>
```

尝试用摩斯电码解密失败，这并非摩斯电码而是博多码Baudot Code，网页标题用博多码解密后是个`?`。

将`-`换成`1`，`.`换成`0`，`/`换成空格，得到`10000 00011 11000 01101 00110 01100 00011 10010`。

```python
>>> '-..../...--/--.../.--.-/..--./.--../...--/-..-.'.replace('-','1').replace('.','0').replace('/', ' ')
'10000 00011 11000 01101 00110 01100 00011 10010'
```

用[Baudot Code](https://www.boxentriq.com/code-breaking/baudot-code)解密，得到`TAOFINAL`。

访问第十四关`/TAOFINAL`，查看网页源码如下：

```html
<body>
    <div class="mail" onclick="mail.open();">
        <div class="icon">✉</div>
    </div>
    <div id="here-is">
        <p><small>TaoFinal</small></p>
        <div class="subject">Email</div>
        <p><small>From: <a href="@77602440">套</a></small></p>
        <hr>
        <p>我喜欢夏天的风，秋天的太阳。</p>
        <p>有时候一张张风景照也能让我陷入一段段可爱的回忆。</p>
        <p>你说走这一遭还有什么可遗憾的。</p>
		<p>还有，那就是打CTF。/doge</p>
        <p><a href="./ctfShow.png" target="_blank">[FLAG FILE]</a></p>
        <p class="hint">根据群主要求，题目不难，你都找到这了，该相信我了吧</p>
        <p class="hint">哦对了，你发现彩蛋了吗？提示一下：libnum</p>
        <p class="what-is-this">28430703.log</p>
    </div>
    <script data-cfasync="false" src=""></script><script>mail=[];mail.open=()=>{document.getElementById('here-is').className="that"}</script>
</body>
```

访问`/libnum`只见`Not Found`，点击`FLAG FILE`下载图片`/ctfShow.png`。用`010 Editor`打开图片后，可以在文件尾看到`ctfshow{this_is_a_ez_try_cuz_no_time}`，提交即可。

------

### 

