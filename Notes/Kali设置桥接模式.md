在`VMWare`中修改虚拟机设置，将网络适配器从NAT模式修改为桥接模式并勾选复制物理网络连接状态。

在Windows主机的虚拟网络编辑器中，点击更改设置，将VMnet0的桥接模式中的外部连接修改为Inter(R) Wi-Fi 6 AX201 160MHz。

在Windows主机中`ipconfig`，查看WLAN的IPv4地址为`192.168.31.22`。

```
ipconfig
...
无线局域网适配器 WLAN:

   连接特定的 DNS 后缀 . . . . . . . :
   本地链接 IPv6 地址. . . . . . . . : fe80::a0a0:8526:53c3:827%10
   IPv4 地址 . . . . . . . . . . . . : 192.168.31.22
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.31.1
```

在虚拟机中测试网络连通性，并设置HTTP代理。

在主机的防火墙设置中放行7890和7891端口。

```bash
┌──(t0ur1st㉿kali)-[~]
└─$ ping 192.168.31.22
PING 192.168.31.22 (192.168.31.22) 56(84) bytes of data.
64 bytes from 192.168.31.22: icmp_seq=1 ttl=64 time=1.73 ms
64 bytes from 192.168.31.22: icmp_seq=2 ttl=64 time=1.61 ms
^C
--- 192.168.31.22 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.609/1.671/1.733/0.062 ms
                                                                   
┌──(t0ur1st㉿kali)-[~]
└─$ telnet 192.168.31.22 7890
Trying 192.168.31.22...
Connected to 192.168.31.22.
Escape character is '^]'.
# 在当前shell临时设置代理
┌──(t0ur1st㉿kali)-[~]
└─$ export http_proxy="http://192.168.31.22:7890"  
                                                                   
┌──(t0ur1st㉿kali)-[~]
└─$ export https_proxy="http://192.168.31.22:7890"
# 或者写入shell配置文件~/.zshrc
┌──(t0ur1st㉿kali)-[~/pwndbg]
└─$ echo 'export http_proxy="http://192.168.31.22:7890"' >> ~/.zshrc

┌──(t0ur1st㉿kali)-[~/pwndbg]
└─$ echo 'export https_proxy="http://192.168.31.22:7890"' >> ~/.zshrc

┌──(t0ur1st㉿kali)-[~/pwndbg]
└─$ source ~/.zshrc
                           
┌──(t0ur1st㉿kali)-[~]
└─$ curl -I https://httpbin.org/ip                 
HTTP/1.1 200 Connection established

HTTP/2 200 
date: Thu, 15 Jan 2026 15:14:06 GMT
content-type: application/json
content-length: 32
server: gunicorn/19.9.0
access-control-allow-origin: *
access-control-allow-credentials: true
```

`sudo vim /etc/proxychains4.conf`修改配置。

```
dynamic_chain
#strict_chain
[ProxyList]
http 192.168.31.22 7890
```

分别用`curl`和`proxychains`测试网络连通性

```bash
┌──(t0ur1st㉿kali)-[~]
└─$ curl -x http://192.168.31.22:7890 -I https://github.com
HTTP/1.1 200 Connection established

HTTP/2 200 
......

┌──(t0ur1st㉿kali)-[~]
└─$ proxychains4 curl -I https://github.com
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Dynamic chain  ...  192.168.31.22:7890  ...  192.168.31.22:7890  ...  OK
HTTP/1.1 200 Connection established

HTTP/2 200 
...
```

亲测，后续变更WiFi环境，需要重新配置。

```
ipconfig
...
无线局域网适配器 WLAN:

   连接特定的 DNS 后缀 . . . . . . . :
   本地链接 IPv6 地址. . . . . . . . : fe80::a0a0:8526:53c3:827%10
   IPv4 地址 . . . . . . . . . . . . : 192.168.1.9
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : 192.168.1.1
```

修改`~/.zshrc`即可。

```bash
┌──(t0ur1st㉿kali)-[~]
└─$ vim ~/.zshrc
                                                                   
┌──(t0ur1st㉿kali)-[~]
└─$ source ~/.zshrc 

┌──(t0ur1st㉿kali)-[~]
└─$ tail -n4 ~/.zshrc
#export http_proxy="http://192.168.31.22:7890"
#export https_proxy="http://192.168.31.22:7890"
export http_proxy="http://192.168.1.9:7890"
export https_proxy="http://192.168.1.9:7890"

$ curl -x http://192.168.1.9:7890 -I https://httpbin.org/ip
HTTP/1.1 200 Connection established

HTTP/2 200 
date: Sat, 17 Jan 2026 09:48:49 GMT
content-type: application/json
content-length: 33
server: gunicorn/19.9.0
access-control-allow-origin: *
access-control-allow-credentials: true
```

