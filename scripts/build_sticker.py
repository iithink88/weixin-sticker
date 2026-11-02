#!/usr/bin/env python
"""绿幕表情源图 → 240×240 透明 PNG，并叠加中文文字（图+文字形式）。
用法: python build_sticker.py 源.png 输出.png "文字"
处理: 去水印 → 绿幕抠图去绿边 → 裁主体 → 底部对齐缩放 → 顶部居中排版中文（白字+深棕描边）
"""
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFont

SIZE = 240
TEXT_BAND = 62           # 顶部预留文字高度
ART_H = SIZE - TEXT_BAND  # 角色可用高度
WM = (0.80, 0.90, 1.0, 1.0)
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_INDEX = 2  # W6 加粗

def erase_watermark(im):
    w, h = im.size
    x0, y0, x1, y1 = int(WM[0]*w), int(WM[1]*h), int(WM[2]*w), int(WM[3]*h)
    region = im.crop((x0, y0, x1, y1)).convert("RGB")
    raw = region.tobytes()
    px = list(zip(raw[0::3], raw[1::3], raw[2::3]))
    greenish = sum(1 for r, g, b in px if g > 150 and r < 120 and b < 120) / max(1, len(px))
    if greenish > 0.5:
        ImageDraw.Draw(im).rectangle([x0, y0, x1, y1], fill=(0, 255, 0))
    return im

def key_green(im):
    im = im.convert("RGB")
    r, g, b = im.getchannel("R"), im.getchannel("G"), im.getchannel("B")
    maxrb = ImageChops.lighter(r, b)
    greenness = ImageChops.subtract(g, maxrb)          # 绿色超出量
    # 60 以上判定背景全透明；30~60 羽化；30 以下不透明
    alpha = greenness.point(lambda v: 0 if v >= 60 else 255 if v <= 30 else int((60 - v) / 30 * 255))
    # 去绿边：边缘处 G 压到 max(R,B)
    g_fixed = ImageChops.darker(g, maxrb)
    g_out = Image.composite(g_fixed, g, alpha.point(lambda v: 255 if v < 255 else 0))
    rgb = Image.merge("RGB", (r, g_out, b))
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out

def fit_art(im):
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop(bbox)
    im.thumbnail((SIZE, ART_H), Image.LANCZOS)
    return im

def draw_text(base, text):
    if not text:
        return base
    draw = ImageDraw.Draw(base)
    size = 46
    while size > 16:
        font = ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)
        # 逐字测量，支持多字符
        w = draw.textlength(text, font=font)
        if w <= SIZE - 16:
            break
        size -= 2
    font = ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)
    w = draw.textlength(text, font=font)
    x = (SIZE - w) / 2
    # 文字在顶部区域垂直居中
    asc, desc = font.getmetrics()
    y = (TEXT_BAND - (asc + desc)) / 2
    stroke = max(3, size // 12)
    draw.text((x, y), text, font=font, fill=(255, 255, 255), stroke_width=stroke, stroke_fill=(58, 42, 34))
    return base

def main(src, dst, text=""):
    im = erase_watermark(Image.open(src))
    art = fit_art(key_green(im))
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(art, ((SIZE - art.width) // 2, SIZE - art.height), art)
    draw_text(canvas, text)
    canvas.save(dst)
    a = canvas.getchannel("A")
    print(f"OK {dst} art={art.size} alpha_bbox={a.getbbox()}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="绿幕表情源图 → 240×240 透明 PNG，并按需在顶部排版中文文字。")
    p.add_argument("src", help="绿幕源图路径（纯 #00FF00 背景）")
    p.add_argument("dst", help="输出 PNG 路径")
    p.add_argument("text", nargs="?", default="", help="顶部文字，留空则输出纯图形表情")
    p.add_argument("--font", default=FONT_PATH, help="中文字体路径")
    p.add_argument("--font-index", type=int, default=FONT_INDEX, help="ttc 字体索引")
    args = p.parse_args()
    if args.font != FONT_PATH:
        FONT_PATH = args.font
    if args.font_index != FONT_INDEX:
        FONT_INDEX = args.font_index
    main(args.src, args.dst, args.text)
