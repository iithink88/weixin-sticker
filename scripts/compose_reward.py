#!/usr/bin/env python
"""赞赏图后期：裁切到目标比例 → 抹水印 → 排版文字。
用法: python compose_reward.py 源.png 输出.png W H "文字"
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def patch_watermark(im, region_ratio=(0.80, 0.90, 1.0, 1.0)):
    """右下角水印区：用周围背景色均值填充（背景为纯色奶油色时安全）"""
    w, h = im.size
    x0, y0, x1, y1 = (int(region_ratio[0]*w), int(region_ratio[1]*h),
                      int(region_ratio[2]*w), int(region_ratio[3]*h))
    # 在左上角纯背景区取样（避开角色与装饰元素）
    sample_box = im.crop((int(0.03*w), int(0.03*h), int(0.20*w), int(0.10*h)))
    px = list(sample_box.convert("RGB").tobytes())
    rs, gs, bs = px[0::3], px[1::3], px[2::3]
    avg = (sum(rs)//len(rs), sum(gs)//len(gs), sum(bs)//len(bs))
    draw = ImageDraw.Draw(im)
    draw.rectangle([x0, y0, x1, y1], fill=avg)
    return im

def main(src, dst, W, H, text):
    im = Image.open(src).convert("RGB")
    im = ImageOps.fit(im, (W, H), Image.LANCZOS)  # 居中裁切不拉伸
    im = patch_watermark(im)
    draw = ImageDraw.Draw(im)
    size = 64
    font = ImageFont.truetype(FONT_PATH, size, index=2)
    while draw.textlength(text, font=font) > W - 80 and size > 24:
        size -= 2
        font = ImageFont.truetype(FONT_PATH, size, index=2)
    w = draw.textlength(text, font=font)
    asc, desc = font.getmetrics()
    y = 28
    draw.text(((W - w) / 2, y), text, font=font, fill=(58, 42, 34),
              stroke_width=6, stroke_fill=(255, 250, 240))
    im.save(dst)
    print(f"OK {dst} {im.size}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
