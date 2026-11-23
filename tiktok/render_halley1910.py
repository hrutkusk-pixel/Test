#!/usr/bin/env python3
"""外れた人類滅亡説 #1「1910年 ハレー彗星騒動」縦型動画(1080x1920 / 30fps / H.264)を書き出す。

使い方:  python3 tiktok/render_halley1910.py  [--preview]
  --preview : 各シーン中央のフレームをPNGで書き出すだけ(確認用)
出力:     tiktok/output/halley1910.mp4
  先に voice_halley1910.py を実行しておくと、ずんだもん・四国めたんの音声と効果音入りになり、
  シーン尺も音声に合わせて伸びる。BGMはTikTokアプリで付ける。
"""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FONT_BLACK = os.path.join(HERE, "fonts", "NotoSansJP_900Black.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "NotoSansJP_700Bold.ttf")
OUT = os.path.join(HERE, "output", "halley1910.mp4")

YELLOW = (255, 214, 64)
RED = (255, 70, 70)
WHITE = (255, 255, 255)
CYAN = (120, 230, 255)

# ---------------------------------------------------------------- 台本
# text: 1行ずつ。[ ] で囲んだ部分を強調色にする。
# visual: 背景の種類 / size: 文字サイズ
SCENES = [
    dict(d=3.6, visual="hook", size=92, text=["1910年、人類は", "[彗星のガス]で", "死ぬと本気で信じた"]),
    dict(d=3.0, visual="comet", size=76, text=["最後に、この彗星が", "[次に来る年]も教えます"]),
    dict(d=4.0, visual="comet", size=76, text=["主役は[ハレー彗星]", "約76年ごとに", "地球に近づく彗星"]),
    dict(d=4.4, visual="spectrum", size=70, text=["1910年2月", "アメリカの天文台が", "彗星の尾から", "有毒な[シアン系のガス]を検出"]),
    dict(d=4.0, visual="pass", size=76, text=["しかもこの年、地球は", "[彗星の尾の中]を", "通過する"]),
    dict(d=5.0, visual="news", size=68, text=["「ガスが大気に広がれば", "生命が絶えるかも」", "天文学者の説を", "[新聞が報道]"]),
    dict(d=3.0, visual="panic", size=96, text=["世界中が", "[パニック]に"]),
    dict(d=3.5, visual="keyhole", size=76, text=["家の隙間や鍵穴を", "[目張り]して閉じこもる"]),
    dict(d=3.5, visual="mask", size=80, text=["[ガスマスク]を", "買い込む人も"]),
    dict(d=4.0, visual="pills", size=78, text=["露店では", "[彗星よけの薬]が", "売られた"]),
    dict(d=3.5, visual="umbrella", size=80, text=["[彗星よけの傘]まで", "登場"]),
    dict(d=3.5, visual="candle", size=80, text=["教会に集まって", "[祈る人]も"]),
    dict(d=4.0, visual="calendar", size=80, text=["そして運命の日", "[1910年5月19日]ごろ"]),
    dict(d=4.0, visual="calm", size=96, text=["……", "[何も起きなかった]"]),
    dict(d=5.5, visual="answer", size=72, text=["＜答え合わせ＞", "尾のガスは", "[とてつもなく薄かった]", "地球の大気のほうが", "何千倍も濃い"]),
    dict(d=4.5, visual="2061", size=74, text=["約束の答え", "ハレー彗星の次の接近は"]),
    dict(d=5.5, visual="question", size=76, text=["あなたは2061年", "この彗星を見られる？", "[見られる]？[見られない]？", "コメントで教えて"]),
]
SERIES_LABEL = "外れた人類滅亡説 #1"

# ---------------------------------------------------------------- 共通素材
_font_cache = {}


def font(size, black=True):
    key = (size, black)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_BLACK if black else FONT_BOLD, size)
    return _font_cache[key]


def make_starfield(seed=7):
    """少し大きめの星空(パララックス用)。"""
    rng = random.Random(seed)
    bw, bh = W + 200, H + 200
    y = np.linspace(0, 1, bh)[:, None]
    base = np.zeros((bh, bw, 3), np.float32)
    base[..., 0] = 6 + 10 * y
    base[..., 1] = 8 + 12 * y
    base[..., 2] = 22 + 30 * y
    img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    # 天の川っぽいもや
    neb = Image.new("RGB", (bw, bh), (0, 0, 0))
    nd = ImageDraw.Draw(neb)
    for _ in range(60):
        cx, cy = rng.randint(0, bw), rng.randint(0, bh)
        r = rng.randint(80, 260)
        col = rng.choice([(40, 30, 80), (20, 40, 90), (60, 25, 70)])
        nd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    neb = neb.filter(ImageFilter.GaussianBlur(120))
    img = Image.fromarray(np.minimum(255, np.asarray(img, np.int16) + np.asarray(neb, np.int16) // 2).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(1400):
        x, yy = rng.randint(0, bw), rng.randint(0, bh)
        b = rng.randint(90, 255)
        s = rng.random()
        if s > 0.985:
            d.ellipse([x - 3, yy - 3, x + 3, yy + 3], fill=(b, b, 255))
        elif s > 0.9:
            d.ellipse([x - 1.5, yy - 1.5, x + 1.5, yy + 1.5], fill=(b, b, b))
        else:
            d.point((x, yy), fill=(b, b, b))
    return img


def make_comet_sprite(length=1500, head=46):
    """右向きに頭、左に尾がのびる彗星(RGBA)。"""
    sw, sh = length + 700, 1200
    arr = np.zeros((sh, sw), np.float32)
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    hx, hy = sw - 500, sh / 2
    dx = hx - xx  # 頭からの距離(尾側が正)
    t = np.clip(dx / length, 0, 1)
    width = 18 + t * 230
    tail = np.exp(-((yy - hy - t * t * 90) / width) ** 2) * (1 - t) ** 1.4 * (dx > 0)
    tail2 = np.exp(-((yy - hy + t * 40) / (10 + t * 90)) ** 2) * (1 - t) ** 2.2 * (dx > 0) * 0.8
    r2 = (xx - hx) ** 2 + (yy - hy) ** 2
    coma = np.exp(-r2 / (2 * head ** 2)) * 1.6 + np.exp(-r2 / (2 * (head * 3) ** 2)) * 0.5
    arr = tail * 0.9 + tail2 + coma
    a = np.clip(arr, 0, 1)
    rgb = np.zeros((sh, sw, 4), np.uint8)
    rgb[..., 0] = np.clip(170 + 85 * a, 0, 255)
    rgb[..., 1] = np.clip(215 + 40 * a, 0, 255)
    rgb[..., 2] = 255
    rgb[..., 3] = (a * 255).astype(np.uint8)
    img = Image.fromarray(rgb, "RGBA")
    return img, (hx, hy)


def make_earth(r=260):
    size = r * 2 + 80
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = size / 2
    nx, ny = (xx - c) / r, (yy - c) / r
    rr = nx ** 2 + ny ** 2
    inside = rr <= 1
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    light = np.clip(0.25 + 0.85 * (-0.55 * nx - 0.45 * ny + 0.7 * nz), 0.05, 1.2)
    # 大陸っぽいノイズ
    rng = np.random.default_rng(3)
    noise = np.zeros_like(nx)
    for k, amp in [(3, 1.0), (6, 0.5), (12, 0.25)]:
        ph = rng.random(4) * 6.28
        noise += amp * np.sin(nx * k * 2.1 + ph[0]) * np.cos(ny * k * 1.7 + ph[1]) + amp * np.sin((nx + ny) * k + ph[2])
    land = noise > 0.55
    col = np.zeros((size, size, 3), np.float32)
    col[...] = (30, 90, 200)
    col[land] = (60, 150, 80)
    cloud = noise < -1.1
    col[cloud] = (230, 235, 245)
    col *= light[..., None]
    alpha = np.where(inside, 255, 0).astype(np.float32)
    # 大気のふち
    rim = np.exp(-((np.sqrt(rr) - 1) * r / 14) ** 2) * 200
    alpha = np.maximum(alpha, rim * (np.sqrt(rr) > 1))
    col = np.where(inside[..., None], col, np.array([110, 180, 255], np.float32))
    out = np.dstack([np.clip(col, 0, 255), alpha]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


STARS = make_starfield()
COMET, COMET_HEAD = make_comet_sprite()
EARTH = make_earth()
EARTH_SMALL = EARTH.resize((260, 260), Image.LANCZOS)


# ---------------------------------------------------------------- テキスト描画
def parse(line):
    """'[強調]普通' -> [(text, highlight)]"""
    segs, buf, hl = [], "", False
    for ch in line:
        if ch == "[":
            if buf:
                segs.append((buf, hl))
            buf, hl = "", True
        elif ch == "]":
            if buf:
                segs.append((buf, hl))
            buf, hl = "", False
        else:
            buf += ch
    if buf:
        segs.append((buf, hl))
    return segs


def draw_text_block(canvas, lines, size, center_y, appear, hl_color=YELLOW, max_w=880):
    """画面中央寄りに字幕を描く。appear: 0..1 のポップイン進行度。"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rows = []
    for ln in lines:
        segs = parse(ln)
        s = size
        while True:
            f = font(s)
            wsum = sum(d.textlength(t, font=f) for t, _ in segs)
            if wsum <= max_w or s < 30:
                break
            s -= 2
        rows.append((segs, f, wsum, s))
    gap = 0.32
    total = sum(r[3] * (1 + gap) for r in rows) - rows[-1][3] * gap
    y = center_y - total / 2
    for i, (segs, f, wsum, s) in enumerate(rows):
        # 行ごとに少しずつ遅れて出す
        p = max(0.0, min(1.0, appear * 1.6 - i * 0.18))
        if p <= 0:
            y += s * (1 + gap)
            continue
        dy = (1 - ease_out(p)) * 40
        x = (W - wsum) / 2
        for t, hl in segs:
            col = hl_color if hl else WHITE
            # 影
            d.text((x + 5, y + 7 + dy), t, font=f, fill=(0, 0, 0, int(160 * p)))
            d.text((x, y + dy), t, font=f, fill=col + (int(255 * p),),
                   stroke_width=max(4, s // 12), stroke_fill=(0, 0, 0, int(255 * p)))
            x += d.textlength(t, font=f)
        y += s * (1 + gap)
    canvas.alpha_composite(layer)


def ease_out(p):
    return 1 - (1 - p) ** 3


def label(canvas, text, y=300, color=(255, 255, 255)):
    d = ImageDraw.Draw(canvas)
    f = font(40, black=False)
    w = d.textlength(text, font=f)
    x = (W - w) / 2
    d.rounded_rectangle([x - 28, y - 12, x + w + 28, y + 58], radius=34, fill=(0, 0, 0, 150), outline=color + (180,), width=3)
    d.text((x, y - 2), text, font=f, fill=color)


# ---------------------------------------------------------------- 背景・イラスト
def bg_stars(t, drift=(12, 6)):
    ox = int(100 + math.sin(t * 0.2) * 60 + t * drift[0]) % 200
    oy = int(100 + t * drift[1]) % 200
    return STARS.crop((ox, oy, ox + W, oy + H)).convert("RGBA")


def paste_comet(canvas, head_xy, angle, scale=1.0, alpha=1.0):
    spr = COMET
    if scale != 1.0:
        spr = spr.resize((int(spr.width * scale), int(spr.height * scale)), Image.BILINEAR)
    if alpha < 1.0:
        a = spr.getchannel("A").point(lambda v: int(v * alpha))
        spr = spr.copy()
        spr.putalpha(a)
    hx, hy = COMET_HEAD[0] * scale, COMET_HEAD[1] * scale
    # 頭を中心に回転させるため、頭が中心に来る大きなキャンバスへ
    big = max(spr.width, spr.height) * 2
    tmp = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    tmp.paste(spr, (int(big / 2 - hx), int(big / 2 - hy)))
    tmp = tmp.rotate(angle, resample=Image.BILINEAR)
    canvas.alpha_composite(tmp, (int(head_xy[0] - big / 2), int(head_xy[1] - big / 2)))


def vignette(canvas, strength=0.6, color=(0, 0, 0)):
    v = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(v)
    d.ellipse([-300, -200, W + 300, H + 200], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(200))
    inv = Image.eval(v, lambda x: int((255 - x) * strength))
    over = Image.new("RGBA", (W, H), color + (0,))
    over.putalpha(inv)
    canvas.alpha_composite(over)


VIGNETTE = None


def icon_canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def draw_keyhole(c, t):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1300
    d.rounded_rectangle([cx - 210, cy - 250, cx + 210, cy + 250], radius=40, fill=(120, 85, 50, 255), outline=(60, 40, 20, 255), width=10)
    d.ellipse([cx - 45, cy - 90, cx + 45, cy], fill=(15, 10, 5, 255))
    d.polygon([(cx - 30, cy - 20), (cx + 30, cy - 20), (cx + 50, cy + 110), (cx - 50, cy + 110)], fill=(15, 10, 5, 255))
    # テープで×(時間で貼られていく)
    p = min(1, t / 0.8)
    for sgn in (1, -1):
        L = 300 * p
        tape = Image.new("RGBA", (int(L) + 2, 70), (235, 225, 190, 240))
        tape = tape.rotate(35 * sgn, expand=True)
        c.alpha_composite(tape, (int(cx - tape.width / 2), int(cy - 40 - tape.height / 2)))


def draw_mask(c, t):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1300 + math.sin(t * 6) * 8
    d.ellipse([cx - 230, cy - 240, cx + 230, cy + 200], fill=(70, 75, 70, 255), outline=(30, 30, 30, 255), width=10)
    for sx in (-1, 1):
        ex = cx + sx * 100
        d.ellipse([ex - 75, cy - 130, ex + 75, cy + 10], fill=(170, 220, 230, 255), outline=(25, 25, 25, 255), width=14)
        d.ellipse([ex - 40, cy - 105, ex - 5, cy - 70], fill=(255, 255, 255, 200))
    d.rounded_rectangle([cx - 70, cy + 60, cx + 70, cy + 250], radius=30, fill=(110, 110, 100, 255), outline=(25, 25, 25, 255), width=10)
    for k in range(4):
        yk = cy + 100 + k * 35
        d.line([cx - 50, yk, cx + 50, yk], fill=(40, 40, 40, 255), width=8)


def draw_pills(c, t):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1310
    d.rounded_rectangle([cx - 150, cy - 230, cx + 150, cy + 230], radius=30, fill=(150, 90, 40, 230), outline=(60, 30, 10, 255), width=8)
    d.rectangle([cx - 110, cy - 290, cx + 110, cy - 230], fill=(40, 40, 40, 255))
    d.rectangle([cx - 130, cy - 120, cx + 130, cy + 90], fill=(245, 235, 205, 255))
    f = font(46)
    for i, s in enumerate(["彗星よけ", "の薬"]):
        w = d.textlength(s, font=f)
        d.text((cx - w / 2, cy - 105 + i * 62), s, font=f, fill=(120, 20, 20, 255))
    rng = random.Random(1)
    for i in range(7):
        ang = i * 0.9 + t * 1.5
        px = cx + 290 * math.cos(ang) + rng.randint(-20, 20)
        py = cy + 260 * math.sin(ang) * 0.7
        d.ellipse([px - 36, py - 20, px + 36, py + 20], fill=(250, 250, 250, 255), outline=(150, 150, 150, 255), width=4)
        d.line([px, py - 20, px, py + 20], fill=(180, 180, 180, 255), width=4)


def draw_umbrella(c, t):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1180 + math.sin(t * 3) * 10
    d.pieslice([cx - 330, cy - 230, cx + 330, cy + 230], 180, 360, fill=(200, 40, 60, 255), outline=(60, 10, 20, 255), width=10)
    for k in range(-2, 3):
        x = cx + k * 132
        d.arc([x - 66, cy - 40, x + 66, cy + 40], 180, 360, fill=(60, 10, 20, 255), width=10)
    d.line([cx, cy - 230, cx, cy + 340], fill=(60, 50, 40, 255), width=16)
    d.arc([cx - 90, cy + 270, cx, cy + 380], 0, 180, fill=(60, 50, 40, 255), width=16)
    # 降ってくる星くず
    rng = random.Random(5)
    for i in range(14):
        x = rng.randint(80, W - 80)
        y = (rng.randint(0, 900) + t * 400) % 900 + 600
        if abs(x - cx) < 330 and y > cy - 240:
            continue
        d.line([x, y, x - 14, y - 40], fill=(150, 230, 255, 200), width=5)


def draw_candle(c, t):
    d = ImageDraw.Draw(c)
    for i, cx in enumerate([W / 2 - 220, W / 2, W / 2 + 220]):
        cy = 1420 - (i == 1) * 60
        d.rectangle([cx - 45, cy - 160, cx + 45, cy + 180], fill=(240, 230, 200, 255))
        fl = 1 + 0.12 * math.sin(t * 13 + i * 2)
        glow = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([80, 80, 320, 320], fill=(255, 170, 60, 110))
        glow = glow.filter(ImageFilter.GaussianBlur(50))
        c.alpha_composite(glow, (int(cx - 200), int(cy - 250 - 200 + 40)))
        d.ellipse([cx - 22 * fl, cy - 250 * fl + (fl - 1) * 160, cx + 22 * fl, cy - 175], fill=(255, 200, 80, 255))
        d.ellipse([cx - 10, cy - 215, cx + 10, cy - 180], fill=(255, 250, 220, 255))
        d.line([cx, cy - 175, cx, cy - 160], fill=(40, 40, 40, 255), width=5)


def draw_calendar(c, t):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1300
    s = 1 + 0.03 * math.sin(t * 4)
    w, h = 300 * s, 330 * s
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=30, fill=(250, 248, 240, 255))
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy - h + 150], radius=30, fill=(200, 40, 50, 255))
    d.rectangle([cx - w, cy - h + 100, cx + w, cy - h + 150], fill=(200, 40, 50, 255))
    f1, f2 = font(70), font(300)
    for txt, f, y, col in [("1910年5月", f1, cy - h + 30, WHITE), ("19", f2, cy - h + 140, (30, 30, 30))]:
        tw = d.textlength(txt, font=f)
        d.text((cx - tw / 2, y), txt, font=f, fill=col + (255,))


def draw_news(c, t):
    d = ImageDraw.Draw(c)
    paper = Image.new("RGBA", (760, 620), (238, 230, 205, 255))
    pd = ImageDraw.Draw(paper)
    pd.rectangle([0, 0, 759, 619], outline=(80, 70, 50, 255), width=6)
    pd.line([30, 110, 730, 110], fill=(40, 30, 20, 255), width=5)
    f = font(56)
    title = "彗星の尾に毒ガス？"
    pd.text(((760 - pd.textlength(title, font=f)) / 2, 22), title, font=f, fill=(25, 20, 15, 255))
    rng = random.Random(2)
    for row in range(12):
        y = 140 + row * 36
        for col in range(3):
            x0 = 30 + col * 240
            pd.line([x0, y, x0 + rng.randint(140, 215), y], fill=(110, 100, 80, 255), width=12)
    pd.text((30, 572), "※イメージ", font=font(30, black=False), fill=(90, 80, 60, 255))
    paper = paper.rotate(-4 + math.sin(t * 2) * 1.2, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(paper, (int(W / 2 - paper.width / 2), 1010))


def draw_spectrum(c, t):
    d = ImageDraw.Draw(c)
    x0, y0, w, h = 140, 1150, 800, 110
    for i in range(w):
        hue = i / w
        r = int(255 * max(0, min(1, 1.5 - abs(hue - 0.9) * 4)))
        g = int(255 * max(0, min(1, 1.5 - abs(hue - 0.5) * 4)))
        b = int(255 * max(0, min(1, 1.5 - abs(hue - 0.1) * 4)))
        d.line([x0 + i, y0, x0 + i, y0 + h], fill=(r, g, b, 230))
    for lx in (0.18, 0.21, 0.47, 0.7):
        X = x0 + lx * w
        d.line([X, y0, X, y0 + h], fill=(0, 0, 0, 255), width=6)
    p = min(1, t / 1.0)
    X = x0 + 0.18 * w
    d.rounded_rectangle([X - 120, y0 + h + 30, X + 220, y0 + h + 120], radius=20, fill=(255, 70, 70, int(230 * p)))
    d.text((X - 95, y0 + h + 40), "有毒ガス成分", font=font(52), fill=(255, 255, 255, int(255 * p)))
    d.text((x0, y0 - 70), "彗星の光を分析（スペクトル）", font=font(40, black=False), fill=(220, 230, 255, 255))


def draw_density(c, t):
    """左: 地球の大気(粒がぎっしり) / 右: 彗星の尾(粒がスカスカ)"""
    d = ImageDraw.Draw(c)
    rng = random.Random(9)
    boxes = [(110, "地球の大気", 900, (120, 190, 255)), (590, "彗星の尾", 9, (200, 240, 255))]
    for x0, name, n, col in boxes:
        y0, bw, bh = 1130, 380, 380
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=24, fill=(0, 0, 0, 140), outline=col + (255,), width=5)
        for _ in range(n):
            px = x0 + 15 + rng.random() * (bw - 30) + math.sin(t * 3 + _) * 3
            py = y0 + 15 + rng.random() * (bh - 30) + math.cos(t * 3 + _) * 3
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=col + (255,))
        f = font(46)
        w = d.textlength(name, font=f)
        d.text((x0 + (bw - w) / 2, y0 + bh + 20), name, font=f, fill=WHITE + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    d.text((150, 1600), "※粒の数はイメージ", font=font(34, black=False), fill=(200, 200, 210, 255))


# ---------------------------------------------------------------- フレーム生成
def render_frame(si, sc, t, gt):
    """si: シーン番号 / t: シーン内秒 / gt: 全体秒"""
    v = sc["visual"]
    p = t / sc["d"]
    canvas = bg_stars(gt)
    text_y = 760
    hl = YELLOW

    if v == "hook":
        # 画面いっぱいに迫る彗星 + 下に地球
        canvas.alpha_composite(EARTH, (int(W / 2 - EARTH.width / 2), int(1450 - p * 30)))
        hx = 1000 - p * 260
        hy = 1250 + p * 80
        paste_comet(canvas, (hx, hy), -28, scale=1.25 + p * 0.25)
        if t < 0.25:
            flash = Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (1 - t / 0.25))))
            canvas.alpha_composite(flash)
        hl = RED
    elif v in ("comet", "2061", "question"):
        hx = 900 - (gt % 20) * 18
        paste_comet(canvas, (hx, 1350), -20, scale=0.95)
        if v == "2061":
            pop = ease_out(min(1, max(0, (t - 0.8) / 0.5)))
            if pop > 0:
                f = font(int(250 * (0.6 + 0.4 * pop)))
                d = ImageDraw.Draw(canvas)
                s = "2061年"
                w = d.textlength(s, font=f)
                d.text(((W - w) / 2, 980), s, font=f, fill=YELLOW + (int(255 * pop),), stroke_width=12, stroke_fill=(0, 0, 0, 255))
            text_y = 680
    elif v == "spectrum":
        paste_comet(canvas, (980, 1650), -15, scale=0.7)
        draw_spectrum(canvas, t)
        text_y = 650
    elif v == "pass":
        ex, ey = W / 2 - EARTH.width / 2, 1050
        canvas.alpha_composite(EARTH, (int(ex), int(ey)))
        # 尾が地球を横切る
        paste_comet(canvas, (1250 + 200 - p * 300, 1000 + p * 100), -12, scale=1.6, alpha=0.75)
        text_y = 700
    elif v == "news":
        canvas.alpha_composite(EARTH_SMALL, (int(W / 2 - 130), 1650))
        draw_news(canvas, t)
        text_y = 650
    elif v == "panic":
        shake = 18 * math.sin(t * 50) * (1 - p * 0.5)
        canvas = canvas.transform(canvas.size, Image.AFFINE, (1, 0, shake, 0, 1, shake * 0.6))
        canvas.alpha_composite(EARTH, (int(W / 2 - EARTH.width / 2 + shake), 1300))
        red = Image.new("RGBA", (W, H), (200, 0, 0, int(70 + 50 * abs(math.sin(t * 8)))))
        canvas.alpha_composite(red)
        hl = RED
        text_y = 820
    elif v in ("keyhole", "mask", "pills", "umbrella", "candle", "calendar"):
        dark = Image.new("RGBA", (W, H), (10, 5, 20, 120))
        canvas.alpha_composite(dark)
        {"keyhole": draw_keyhole, "mask": draw_mask, "pills": draw_pills, "umbrella": draw_umbrella,
         "candle": draw_candle, "calendar": draw_calendar}[v](canvas, t)
        text_y = 640
    elif v == "calm":
        canvas.alpha_composite(EARTH, (int(W / 2 - EARTH.width / 2), 1200))
        paste_comet(canvas, (300 - p * 200, 600), 160, scale=0.6, alpha=0.6)
        text_y = 760
        hl = CYAN
    elif v == "answer":
        # 地球の大気(濃い) と 尾(薄い) の比較バー
        draw_density(canvas, t)
        text_y = 700
        hl = CYAN

    global VIGNETTE
    if VIGNETTE is None:
        VIGNETTE = icon_canvas()
        vignette(VIGNETTE, 0.55)
    canvas.alpha_composite(VIGNETTE)

    label(canvas, SERIES_LABEL)
    credit(canvas, si, t)
    appear = min(1.0, t / 0.45)
    lines = sc["text"]
    if v == "calm":
        # 「……」を先に、少し間をおいてオチ
        lines = lines if t > 1.5 else lines[:1]
    draw_text_block(canvas, lines, sc["size"], text_y, appear if v != "calm" else 1.0, hl_color=hl)
    speaker_badge(canvas, sc, t)
    # 進行バー(上部、UIと被らないよう細く)
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, int(W * gt / TOTAL), 10], fill=YELLOW + (255,))
    return canvas.convert("RGB")


SPEAKER_COLOR = {"ずんだもん": (120, 205, 80), "四国めたん": (240, 110, 170)}


def credit(canvas, si, t):
    """VOICEVOX のクレジット。最後のシーンだけエンドクレジット風に出す。"""
    if not VOICED or si != len(SCENES) - 1:
        return
    a = min(1.0, t / 0.5)
    d = ImageDraw.Draw(canvas)
    f = font(36, black=False)
    rows = ["VOICEVOX:ずんだもん", "VOICEVOX:四国めたん"]
    y = 1200
    for s in rows:
        w = d.textlength(s, font=f)
        d.text(((W - w) / 2, y), s, font=f, fill=(235, 235, 245, int(235 * a)),
               stroke_width=3, stroke_fill=(0, 0, 0, int(220 * a)))
        y += 52


def speaker_badge(canvas, sc, t):
    """いま話している人の名前札(字幕の上)。"""
    for ln in sc.get("lines", []):
        if ln["start"] - 0.05 <= t <= ln["start"] + ln["dur"] + 0.1:
            name = ln["speaker"]
            col = SPEAKER_COLOR[name]
            d = ImageDraw.Draw(canvas)
            f = font(44)
            w = d.textlength(name, font=f)
            x, y = (W - w) / 2, 450
            d.rounded_rectangle([x - 34, y - 8, x + w + 34, y + 62], radius=36, fill=col + (235,))
            d.text((x, y - 4), name, font=f, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(30, 30, 30, 255))
            return


# 音声タイミング表があれば、シーン尺を音声に合わせる
TIMING = os.path.join(HERE, "output", "halley1910_timing.json")
AUDIO = os.path.join(HERE, "output", "halley1910_audio.wav")
VOICED = os.path.exists(TIMING) and os.path.exists(AUDIO)
if VOICED:
    import json
    _tm = json.load(open(TIMING))
    assert len(_tm["scenes"]) == len(SCENES)
    for _s, _t in zip(SCENES, _tm["scenes"]):
        _s["d"] = _t["d"]
        _s["lines"] = _t["lines"]
TOTAL = sum(s["d"] for s in SCENES)
N_FRAMES = int(round(TOTAL * FPS))


def timeline():
    t0 = 0.0
    for i, s in enumerate(SCENES):
        yield i, s, t0
        t0 += s["d"]


def scene_at(gt):
    last = None
    for i, s, t0 in timeline():
        last = (i, s, t0)
        if gt < t0 + s["d"]:
            return last
    return last


def render_range(args):
    """フレーム [a, b) を動画ファイル path に書き出す(並列処理用)。"""
    a, b, path = args
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-profile:v", "high", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        gt = fi / FPS
        i, s, t0 = scene_at(gt)
        proc.stdin.write(render_frame(i, s, gt - t0, gt).tobytes())
    proc.stdin.close()
    proc.wait()
    return path


def main():
    preview = "--preview" in sys.argv
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if preview:
        pdir = os.path.join(HERE, "output", "preview")
        os.makedirs(pdir, exist_ok=True)
        for i, s, t0 in timeline():
            t = s["lines"][0]["start"] + 0.3 if s.get("lines") else s["d"] * 0.7
            t = max(t, s["d"] * 0.5) if s["visual"] == "calm" else t
            render_frame(i, s, t, t0 + t).save(os.path.join(pdir, f"scene{i + 1:02d}.png"))
        print("preview written:", pdir)
        return
    import multiprocessing as mp
    import tempfile
    workers = max(1, os.cpu_count() or 1)
    tmp = tempfile.mkdtemp(prefix="render_", dir=os.path.join(HERE, "output"))
    step = -(-N_FRAMES // workers)
    jobs = [(k, min(k + step, N_FRAMES), os.path.join(tmp, f"part{j:02d}.mp4"))
            for j, k in enumerate(range(0, N_FRAMES, step))]
    print(f"{N_FRAMES} frames ({TOTAL:.1f}s) / {len(jobs)} workers", flush=True)
    with mp.Pool(len(jobs)) as pool:
        parts = pool.map(render_range, jobs)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    audio_in = ["-i", AUDIO] if VOICED else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, *audio_in,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ac", "2",
                    "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", OUT], check=True)
    for p in parts + [lst]:
        os.remove(p)
    os.rmdir(tmp)
    print("done:", OUT, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
