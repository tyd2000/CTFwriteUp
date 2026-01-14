## Docker安装

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install containerd
sudo apt-get install docker.io
sudo service docker start
docker version
```
当然，也可以选择用官方脚本安装：
```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```
切换中科大镜像源：
```bash
cat > /etc/docker/daemon.json << EOF 
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
} 
EOF
```
#### Docker 相关指令
```bash
sudo docker info  # 查看docker的基本信息
sudo docker images  # 查看本机上的所有镜像
sudo docker build  # 容器构建
sudo docker run  # 运行容器
sudo docker stop  # 停止容器
sudo docker kill  # 强制停止容器
sudo docker rm  # 删除容器
sudo netstat -antp | grep docker  # 查看端口连接
sudo lsof -i:[端口号]  # 查看端口所在进程
sudo kill [PID]  # 断开连接
```
------
## 下载并使用ctf_xinetd
GitHub开源项目：[ctf_xinetd](https://github.com/Eadom/ctf_xinetd)。
```bash
git clone https://github.com/Eadom/ctf_xinetd.git
# 把flag和二进制程序放入bin目录中，并且按照readme修改ctf_xinetd
cd ~/ctf_xinetd
sudo docker build -t "pwn" .  # 在ctf_xinetd目录下构建容器
sudo docker run -d -p "0.0.0.0:port:9999" -h "pwn" --name="pwn" pwn # 运行并部署该镜像 port端口号
```
接着`nc`进去测试发现可以打通了。
```bash
nc [ip] [port]
cat flag
```
然而[ctf_xinetd](https://github.com/Eadom/ctf_xinetd)存在一些缺点，比如：需要自己配置`flag`，一次只能部署一道题目等等。

------
## 下载并使用pwn_deploy_chroot
针对[ctf_xinetd](https://github.com/Eadom/ctf_xinetd)的缺点改进后，有了GitHub开源项目：[pwn_deploy_chroot](https://github.com/giantbranch/pwn_deploy_chroot)，`flag`会由`initialize.py`生成并写入。原版用的是`python2`来写，我`fork`之后改进成了`python3`版本：[pwn_deploy](https://github.com/Don2025/pwn_deploy)。
```bash
sudo apt-get install docker-compose  # docker-compose
git clone https://github.com/Don2025/pwn_deploy.git
# 将所有pwn题目的二进制程序放到bin目录中，注意文件名中不要含有特殊字符，后续会用这个文件名创建用户名
python initialize.py
sudo docker-compose up --build -d
```
出题时编译的相关参数：
```bash
# NX保护机制：
-z execstack / -z noexecstack  # (关闭 / 开启) 堆栈不可执行

# Canary：(关闭 / 开启 / 全开启) 栈里插入cookie信息
# !开canary好像会造成栈中局部变量的顺序有所改变
-fno-stack-protector / -fstack-protector / -fstack-protector-all 

# ASLR和PIE：
-no-pie / -pie   # (关闭 / 开启) 地址随机化，另外打开后会有get_pc_thunk

# RELRO：
-Wl -z norelro / -z lazy / -z now   # (关闭 / 部分开启 / 完全开启) 对GOT表具有写权限

-s   # 去除符号表
```
要编译并开启 NX 保护、Canary、Full RELRO 和 PIE enabled，可以使用以下编译命令：
```bash
gcc -fstack-protector-all -pie -Wl,-z,relro,-z,now -o calculate calculate.c -pthread
```
这条编译命令中的选项说明如下：
- `-fstack-protector-all`：开启栈保护，即 Canary 机制。
- `-fPIE`：生成可执行文件的位置无关代码（Position Independent Executable）。
- `-pie`：生成可执行文件为位置无关可执行文件。
- `-Wl,-z,relro,-z,now`：启用 RELRO（RELocation Read-Only）和 NOW（No Execute）保护机制。
编译并开启 NX 保护、Partial RELRO，可以使用以下编译命令：
```bash
gcc -fno-stack-protector -z noexecstack -no-pie -z lazy -o babystack babystack.c
```
