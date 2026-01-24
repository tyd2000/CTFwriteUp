# Kali编译Sage

没有使用`apt install`直接安装`sage`也没有使用`docker`，而是选择了自己重新编译`Sagemath`。

从https://mirrors.aliyun.com/sagemath/src/index.html下载最新版本的`sage-10.8.tar.gz`。

```
tar -xzf sage-10.8-kali-x86_64.tar.gz -C /opt/sage
```

进入`/opt/sage`后，`sudo apt install`安装好相关依赖，确认无误后再编译。

```bash
$ ./configure
$ make build
$ make -j6 sagelib
```

需要过好几个小时才安装好。

```
Sage build/upgrade complete!
real 40m37.502s user 141m46.973s sys 8m1.493s
```

尝试运行底层组件，验证`make build`是否成功。如果都能正常输出结果，说明底层依赖100% 可用。

```bash
┌──(t0ur1st㉿kali)-[/opt/sage]
└─$ ./local/bin/gp -q <<< "factor(2^67-1)"
[   193707721 1]
[761838257287 1]
# 数论核心PARI库和GP前端工作正常

┌──(t0ur1st㉿kali)-[/opt/sage]
└─$ echo "Size(SymmetricGroup(5));; quit;" | ./local/bin/gap -q
# 测试群论库GAP

┌──(t0ur1st㉿kali)-[/opt/sage]
└─$ echo "ring r=0,(x,y),dp; ideal I=x2-y3; std(I);" | ./local/bin/Singular 
                     SINGULAR                                 /
 A Computer Algebra System for Polynomial Computations       /   version 4.4.1
                                                           0<
 by: W. Decker, G.-M. Greuel, G. Pfister, H. Schoenemann     \   Jan 2025
FB Mathematik der Universitaet, D-67653 Kaiserslautern        \
_[1]=y3-x2
Auf Wiedersehen.
# 测试代数几何引擎Singular
```

尝试运行`sage`，验证`sage`是否安装成功，不能直接用`python`运行`import sage.all`是正常的，完全符合`SageMath`的设计逻辑。如果我们写的`.py`文件中使用了 `from sage.all import *` 或任何Sage特有的功能（如 `factor`, `EllipticCurve`, `matrix`, `plot` 等），都必须用`Sage`的`Python`环境来运行它。

```bash
┌──(t0ur1st㉿kali)-[/opt/sage]
└─$ sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 10.8, Release Date: 2025-12-18                    │
│ Using Python 3.13.11. Type "help()" for help.                      │
└────────────────────────────────────────────────────────────────────┘
sage: sage.version.version
'10.8'
sage: exit

┌──(t0ur1st㉿kali)-[/opt/sage]
└─$ cd ~

┌──(t0ur1st㉿kali)-[~]
└─$ python -c "import sage.all; print('Sage version:', sage.version.version)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sage.all; print('Sage version:', sage.version.version)
    ^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'sage'
                                                                           
┌──(t0ur1st㉿kali)-[~]
└─$ /opt/sage/venv/bin/python -c "import sage.all; print('OK')"
OK
                                                                           
┌──(t0ur1st㉿kali)-[~]
└─$ which sage
/usr/local/bin/sage
                                                                           
┌──(t0ur1st㉿kali)-[~]
└─$ sage -c "import sage.all; print('OK')"
OK
```

在编译成功的机器上打包整个`sage`目录（保留权限和符号链接）

```bash
sudo tar --owner=root --group=root -czvf sage-10.8-Kali-x86_64-precompile.tar.gz -C /opt sage
```

打包完成后验证内容：

```bash
$ tar -tzf sage-10.8-Kali-x86_64-precompile.tar.gz | head -n 5
sage/
sage/=1.1.0
sage/CODE_OF_CONDUCT_COMMITTEE.md
sage/build/
sage/build/tox.ini
```

通过网盘分享的文件：sage-10.8-Kali-x86_64-precompile.tar.gz 链接: https://pan.baidu.com/s/1g0GYw0tOf8WXlJJ8y3Hicg?pwd=nd6i 提取码: nd6i --来自百度网盘超级会员v9的分享

在同样的Kali系统和Python3.13环节的目标机器上验证是否可移植，如果不能请`apt`安装相关环境依赖。

```bash
# 在目标机解压到 /opt
sudo tar -xzf /tmp/sage-10.8-kali-x86_64.tar.gz -C /

# 检查 Sage 是否识别新路径
$ sage -c "import sage.all; print('OK')"
OK

# 检查关键组件
$ sage -c "print(gap('2+2'))"
4

$ sage -c "print(pari('factor(100)'))"
[2, 2; 5, 2]
```

如果需要部署到多台其他机器，可以考虑制作`deb`包，用 `checkinstall` 打包成 `.deb`：

```
sudo apt install checkinstall
cd /opt/sage
sudo checkinstall --pkgname=sagemath --pkgversion=10.8 --backup=no --deldoc=yes --fstrans=yes --default
```

生成的 `sagemath_10.8_amd64.deb` 可直接 `dpkg -i` 安装。

我们安装的`Sage`依赖系统软连接的`Python 3.13`，最可靠的分发方式是`Docker`：

```
FROM kalilinux/kali-rolling
RUN apt update && apt install -y python3 python3-pip
COPY sage /opt/sage
ENV PATH="/opt/sage: $ PATH"
CMD ["/opt/sage/sage"]
```

但是这样又本末倒置了，何不直接用官方的`docker`安装呢。
