#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/fetch_images.py — 从 Bing 图片搜索下载候选图片到本地缓存目录。

用途：为巡防百科各页面搜索"参考学习图片"的网络真实图素材。
用法：
    python tools/fetch_images.py "关键词1|关键词2|关键词3" <输出目录> [--count N]

行为：
  - 依次用各组关键词调 Bing images async 接口，每组取前 N 条候选
  - 下载为合法图片（JPEG/PNG）的文件，跳过失败/非图片/过小文件
  - 候选命名 candidate-000.jpg / candidate-001.png ...，避免同名覆盖
  - 结束后打印各候选的文件大小，供人工挑选
注意：本脚本不保证图片内容与主题匹配，需人工（图片查看）挑选。
"""
import os
import re
import sys
import argparse
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def search_urls(keyword, count):
    """返回 Bing 图片搜索结果中真实的图片 URL 列表（URL 已解码）。"""
    q = urllib.parse.quote(keyword)
    url = (f"https://cn.bing.com/images/async?q={q}&first=0&count={count}"
           f"&mkt=zh-CN")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=25).read().decode(
        "utf-8", errors="ignore")
    raw = re.findall(r'murl&quot;:&quot;(.*?)&quot;', html)
    urls = []
    seen = set()
    for u in raw:
        u = u.replace("&amp;", "&")
        try:
            dec = urllib.parse.unquote(u)
        except Exception:
            dec = u
        if dec in seen:
            continue
        seen.add(dec)
        urls.append(dec)
    return urls


def image_size(path):
    """解析图片宽高（标准库，无需 PIL）。返回 (w,h) 或 None。"""
    with open(path, "rb") as f:
        head = f.read(32)
    if head[:2] == b"\xff\xd8":  # JPEG
        with open(path, "rb") as f:
            f.seek(2)
            b = f.read(65536)
        i = 0
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1
                continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h = int.from_bytes(b[i + 5:i + 7], "big")
                w = int.from_bytes(b[i + 7:i + 9], "big")
                return w, h
            i += 2
        return None
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
    return None


def is_image_file(path):
    """用文件头判断是否为合法 JPEG/PNG，并返回 (是否图片, 大小KB)。"""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(8)
    if size < 30 * 1024:  # 过小，多为缩略图/图标/截断
        return False, size // 1024
    if head[:2] == b"\xff\xd8" or head[:8] == b"\x89PNG\r\n\x1a\n":
        return True, size // 1024
    return False, size // 1024


def download(url, dest):
    """下载 URL 到 dest，返回是否成功。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", help="关键词，用 | 分隔多组")
    ap.add_argument("outdir", help="输出目录")
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--min-edge", type=int, default=0,
                    help="过滤：长边小于该像素的候选丢弃（默认不过滤）")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    keywords = [k for k in args.keywords.split("|") if k.strip()]

    seen_names = set()
    total_ok = 0
    for kw in keywords:
        print(f"== 搜索「{kw}」==")
        try:
            urls = search_urls(kw, args.count)
        except Exception as e:
            print(f"   搜索失败: {e}")
            continue
        print(f"   候选 {len(urls)} 个，尝试下载...")
        for i, u in enumerate(urls):
            if total_ok >= args.count:
                break
            n = total_ok
            name = f"candidate-{n:03d}.img"
            dest = os.path.join(args.outdir, name)
            if not download(u, dest):
                continue
            ok, kb = is_image_file(dest)
            if not ok:
                os.remove(dest)
                continue
            if args.min_edge:
                wh = image_size(dest)
                if wh and max(wh) < args.min_edge:
                    os.remove(dest)
                    print(f"   丢弃（长边<{args.min_edge}）{os.path.basename(dest)}")
                    continue
            # 按真实格式改名
            ext = ".png" if kb > 0 and open(dest, "rb").read(8)[:8] == b"\x89PNG\r\n\x1a\n" else ".jpg"
            final = os.path.join(args.outdir, f"candidate-{n:03d}{ext}")
            if final != dest:
                os.rename(dest, final)
            print(f"   [OK] {os.path.basename(final)}  {kb}KB  <- {u[:100]}")
            total_ok += 1
        if total_ok >= args.count:
            break

    print(f"\n共下载 {total_ok} 个合法候选到 {args.outdir}")


if __name__ == "__main__":
    main()
