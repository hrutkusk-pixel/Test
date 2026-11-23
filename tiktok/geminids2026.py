#!/usr/bin/env python3
"""宇宙ミステリー #2「ふたご座流星群の"親"は彗星じゃない」+ 2026年の見頃

  python3 tiktok/geminids2026.py voice | preview | render
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, font
from wow1977 import glow

SCENES = [
    dict(d=3.6, visual="hook", size=88, text=["ふたご座流星群の", "\"親\"は", "[彗星じゃない]らしい"]),
    dict(d=3.0, visual="teaser", size=76, text=["最後に", "[2026年の見頃]も紹介"]),
    dict(d=4.5, visual="dust", size=70, text=["流れ星の正体は", "宇宙の[チリ]", "ふつうは彗星がまいたもの"]),
    dict(d=4.0, visual="phaethon", size=74, text=["でも親は", "小惑星[ファエトン]"]),
    dict(d=4.5, visual="sun", size=70, text=["太陽に[水星よりずっと]近づき", "表面は[約750℃]とも"]),
    dict(d=4.5, visual="rockcomet", size=72, text=["太陽の熱でチリを出す", "[岩石彗星]とも呼ばれる"]),
    dict(d=4.5, visual="notenough", size=72, text=["でも今出ているチリでは", "流星群の量に", "[全然足りない]"]),
    dict(d=5.0, visual="breakup", size=70, text=["昔はもっと活発だった？", "[何かが崩れた]？", "答えはまだ出ていない"]),
    dict(d=5.0, visual="destiny", size=66, text=["JAXAの探査機", "[DESTINY+]が調べに行く計画", "打ち上げは2028年度目標"]),
    dict(d=4.5, visual="calendar", size=76, text=["＜2026年の見頃＞", "[12月14日の夜]", "極大は23時ごろ"]),
    dict(d=4.0, visual="moon", size=74, text=["月は21時ごろに沈む", "[好条件]の年"]),
    dict(d=4.5, visual="count", size=72, text=["空が暗ければ", "15日0〜2時ごろ", "[1時間に約60個]"]),
    dict(d=4.5, visual="tips", size=72, text=["コツは空を[広く]見る", "目が慣れるまで[15分]"]),
    dict(d=5.5, visual="question", size=76, text=["あなたは見に行く？", "[見に行く]？[寝る]？", "コメントで教えて"]),
]

LINES = [
    [(Z, "ふたご座流星群の親って、彗星じゃないらしいのだ！")],
    [(M, "最後に、2026年の見頃も、わたくしが教えてあげるわ。")],
    [(M, "流れ星の正体は、宇宙のチリが大気に飛び込んで光ったもの。流星群のチリは、ふつう彗星がまき散らしたものなの。")],
    [(M, "でも、ふたご座流星群の親は、ファエトンという小惑星なのよ。"), (Z, "岩なのに、チリを出すのだ？")],
    [(M, "ファエトンは、太陽に水星よりもずっと近づくの。表面は750度くらいになるとも言われているわ。")],
    [(M, "太陽に焼かれて表面からチリが飛び出すから、岩石彗星とも呼ばれているのよ。")],
    [(M, "ところが、今ファエトンが出しているチリだけでは、流星群の量に全然足りないの。"), (Z, "じゃあ、どこから来たのだ！？")],
    [(M, "昔はもっと活発だった説や、数千年以内に何かが崩れて一気にチリをまいた説があるけど、答えはまだ出ていないわ。")],
    [(M, "そこで日本のJAXAが、探査機デスティニープラスで調べに行く計画を進めているの。打ち上げは2028年度が目標よ。"), (Z, "謎を解きに行くのだ！")],
    [(M, "さあ、約束の見頃よ。2026年は12月14日の夜。極大は23時ごろと予想されているわ。")],
    [(M, "しかも月が21時ごろに沈むから、そのあとは月明かりがなくて好条件なの。"), (Z, "ラッキーなのだ！")],
    [(M, "空の暗い場所なら、15日の0時から2時ごろに、1時間に60個くらい見えると予想されているわ。")],
    [(M, "コツは、空を広く見わたすこと。目が暗さに慣れるまで、15分は見続けなさい。"), (Z, "防寒もしっかりなのだ！")],
    [(Z, "みんなは、見に行くのだ？"), (M, "見に行く？寝る？アンタたちの予定、コメントで聞かせなさい。")],
]

RADIANT = (760, 560)


# ---------------------------------------------------------------- 部品
def meteors(c, t, n=10, seed=1, radiant=RADIANT, rate=1.0):
    """放射点から四方へ流れる流れ星。"""
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rng = random.Random(seed)
    for k in range(n):
        period = rng.uniform(1.2, 2.6) / rate
        ph = rng.random() * period
        life = (t + ph) % period / period
        if life > 0.45:
            continue
        q = life / 0.45
        ang = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(120, 500)
        L = rng.uniform(160, 320)
        sx, sy = radiant[0] + r0 * math.cos(ang), radiant[1] + r0 * math.sin(ang)
        hx, hy = sx + L * q * math.cos(ang), sy + L * q * math.sin(ang)
        tx, ty = hx - 0.6 * L * math.cos(ang), hy - 0.6 * L * math.sin(ang)
        a = int(255 * (1 - abs(q - 0.5) * 1.6))
        for w, al in ((9, 0.25), (4, 0.6), (2, 1.0)):
            d.line([tx, ty, hx, hy], fill=(255, 250, 230, int(max(0, a) * al)), width=w)
    c.alpha_composite(lay)


def asteroid(c, cx, cy, r, t=0.0, hot=0.0, seed=3):
    """ゴツゴツした小惑星(イメージ)。hot: 0..1 で赤熱。"""
    rng = random.Random(seed)
    pts = []
    for k in range(18):
        a = k / 18 * 2 * math.pi + t * 0.2
        rr = r * rng.uniform(0.78, 1.08)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.9))
    d = ImageDraw.Draw(c)
    base = (int(110 + 120 * hot), int(100 + 20 * hot), int(95 - 40 * hot))
    if hot > 0:
        glow(c, (cx, cy), r * 1.2, (255, 140, 60), int(160 * hot))
    d.polygon(pts, fill=base + (255,), outline=(50, 45, 40, 255))
    for k in range(6):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, r * 0.6)
        cr = rng.uniform(r * 0.08, r * 0.18)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        d.ellipse([x - cr, y - cr, x + cr, y + cr], fill=(int(base[0] * 0.7), int(base[1] * 0.7), int(base[2] * 0.7), 255))


def dust_spray(c, cx, cy, t, direction=0.0, spread=0.5, n=60, color=(230, 210, 180)):
    d = ImageDraw.Draw(c)
    rng = random.Random(11)
    for k in range(n):
        ph = rng.random()
        life = (t * 0.6 + ph) % 1.0
        a = direction + rng.uniform(-spread, spread)
        dist = 40 + life * 420
        x, y = cx + dist * math.cos(a), cy + dist * math.sin(a)
        s = 3 + rng.random() * 4
        d.ellipse([x - s, y - s, x + s, y + s], fill=color + (int(230 * (1 - life)),))


def box_text(c, x, y, text, size=48, col=WHITE, pad=18):
    d = ImageDraw.Draw(c)
    f = font(size)
    w = d.textlength(text, font=f)
    d.rounded_rectangle([x - pad, y - pad / 2, x + w + pad, y + size * 1.2 + pad / 2], radius=18, fill=(0, 0, 0, 170))
    d.text((x, y), text, font=f, fill=col + (255,))


# ---------------------------------------------------------------- シーン
def v_hook(c, t, p, gt, sc):
    meteors(c, t, n=16, rate=1.4)
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    d = ImageDraw.Draw(c)
    f = font(300)
    d.text((W / 2 - 110, 1150), "？", font=f, fill=(255, 214, 64, 220), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return c, 760, RED


def v_teaser(c, t, p, gt, sc):
    meteors(c, t, n=10)
    return c, 780, YELLOW


def v_dust(c, t, p, gt, sc):
    E.paste_comet(c, (900, 1180), 200, scale=0.55, alpha=0.9)
    dust_spray(c, 900, 1180, t, direction=math.pi * 0.95, spread=0.25, n=50)
    c.alpha_composite(E.EARTH_SMALL, (140, 1450))
    meteors(c, t, n=5, radiant=(270, 1580), seed=4)
    return c, 690, YELLOW


def v_phaethon(c, t, p, gt, sc):
    k = E.ease_out(min(1, t / 0.6))
    asteroid(c, W / 2, 1300, 230 * k, t)
    E.mark_image(c, "※ファエトンのイメージ", (60, 1680))
    return c, 720, YELLOW


def v_sun(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    sx, sy = 170, 1300
    glow(c, (sx, sy), 170, (255, 180, 60), 255)
    d.ellipse([sx - 110, sy - 110, sx + 110, sy + 110], fill=(255, 220, 120, 255))
    # 水星の軌道(比較)
    d.ellipse([sx - 330, sy - 330, sx + 330, sy + 330], outline=(180, 180, 200, 160), width=4)
    d.text((sx + 240, sy - 360), "水星の軌道", font=font(34), fill=(200, 200, 220, 255))
    # ファエトンの細長い軌道(近日点が太陽のすぐそば)
    a, b = 560, 260
    cx = sx + 150 + a  # 近日点は太陽と水星軌道の間
    d.ellipse([cx - a, sy - b, cx + a, sy + b], outline=(255, 160, 120, 200), width=4)
    ang = math.pi + 0.9 * math.sin(t * 0.9)
    px, py = cx + a * math.cos(ang), sy + b * math.sin(ang)
    hot = max(0, 1 - abs(px - (sx + 150)) / 300)
    asteroid(c, px, py, 46, t, hot=hot)
    d.text((px - 60, py + 60), "ファエトン", font=font(34), fill=(255, 200, 170, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※イメージ（大きさ・距離は実際と異なる）", (60, 1700))
    return c, 690, YELLOW


def v_rockcomet(c, t, p, gt, sc):
    glow(c, (60, 1300), 200, (255, 180, 60), 220)
    asteroid(c, 470, 1300, 150, t, hot=0.6)
    dust_spray(c, 470, 1300, t, direction=0.0, spread=0.45, n=70)
    E.mark_image(c, "※イメージ", (W - 230, 1680))
    return c, 700, YELLOW


def v_notenough(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    k = E.ease_out(min(1, t / 1.0))
    base = 1600
    bars = [("今出している\nチリ", 0.02, (255, 170, 90)), ("流星群の\nチリ", 1.0, (120, 200, 255))]
    for i, (name, v, col) in enumerate(bars):
        x = 220 + i * 400
        h = 520 * v * k
        d.rectangle([x, base - max(8, h), x + 240, base], fill=col + (255,))
        for j, ln in enumerate(name.split("\n")):
            f = font(40)
            d.text((x + (240 - d.textlength(ln, font=f)) / 2, base + 20 + j * 50), ln, font=f, fill=WHITE + (255,),
                   stroke_width=3, stroke_fill=(0, 0, 0, 255))
    if t > 1.2:
        d.text((220, base - 140), "ほんの\nわずか", font=font(48), fill=RED + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※割合はイメージ", (60, 1740))
    return c, 700, RED


def v_breakup(c, t, p, gt, sc):
    sep = min(1, max(0, (t - 1.0) / 1.5))
    rng = random.Random(5)
    for k in range(6):
        a = k / 6 * 2 * math.pi + 0.3
        ox, oy = math.cos(a) * 160 * sep, math.sin(a) * 120 * sep
        asteroid(c, W / 2 + ox, 1300 + oy, 95 if k else 120, t, seed=10 + k)
    if sep > 0:
        dust_spray(c, W / 2, 1300, t, direction=0, spread=math.pi, n=int(80 * sep))
    del rng
    E.mark_image(c, "※イメージ", (W - 230, 1680))
    return c, 680, YELLOW


def v_destiny(c, t, p, gt, sc):
    asteroid(c, 830, 1250, 110, t)
    d = ImageDraw.Draw(c)
    x, y = 250 + 120 * p, 1400 - 60 * p
    d.rectangle([x - 50, y - 40, x + 50, y + 40], fill=(220, 190, 90, 255), outline=(80, 70, 30, 255), width=4)
    for s in (-1, 1):
        xa, xb = sorted((x + s * 60, x + s * 230))
        d.rectangle([xa, y - 18, xb, y + 18], fill=(60, 90, 170, 255), outline=(30, 40, 80, 255), width=3)
        for k in range(1, 4):
            xx = x + s * (60 + k * 42)
            d.line([xx, y - 18, xx, y + 18], fill=(30, 40, 80, 255), width=2)
    glow(c, (x - 70, y), 24, (120, 200, 255), 200)
    E.mark_image(c, "※探査機・小惑星はイメージ", (60, 1680))
    return c, 660, YELLOW


def v_calendar(c, t, p, gt, sc):
    meteors(c, t, n=6, seed=8)
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1310
    s = 1 + 0.03 * math.sin(t * 4)
    w, h = 280 * s, 300 * s
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=30, fill=(250, 248, 240, 255))
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy - h + 140], radius=30, fill=(40, 80, 180, 255))
    d.rectangle([cx - w, cy - h + 100, cx + w, cy - h + 140], fill=(40, 80, 180, 255))
    for txt, f, y, col in [("2026年12月", font(64), cy - h + 30, WHITE), ("14", font(280), cy - h + 130, (30, 30, 30))]:
        d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col + (255,))
    return c, 650, YELLOW


def v_moon(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    hy = 1560
    mx, my = 300, 1180 + 300 * p
    glow(c, (mx, my), 70, (255, 240, 200), 150)
    d.ellipse([mx - 70, my - 70, mx + 70, my + 70], fill=(255, 245, 210, 255))
    d.ellipse([mx - 30, my - 80, mx + 110, my + 80], fill=(14, 18, 45, 255))
    d.rectangle([0, hy, W, 1920], fill=(8, 10, 20, 255))
    d.polygon([(0, hy), (200, hy - 60), (420, hy - 10), (650, hy - 80), (880, hy - 20), (W, hy - 50), (W, hy)], fill=(8, 10, 20, 255))
    box_text(c, 640, 1200, "21:00ごろ", 56, YELLOW)
    if p > 0.5:
        meteors(c, t, n=6, seed=9, radiant=(760, 900))
    return c, 720, YELLOW


def v_count(c, t, p, gt, sc):
    meteors(c, t, n=18, rate=1.6, radiant=(W / 2, 1300))
    d = ImageDraw.Draw(c)
    n = int(60 * min(1, t / 2.5))
    f = font(170)
    s = f"{n}個"
    d.text(((W - d.textlength(s, font=f)) / 2, 1180), s, font=f, fill=YELLOW + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    f2 = font(48)
    s2 = "1時間あたり（予想）"
    d.text(((W - d.textlength(s2, font=f2)) / 2, 1410), s2, font=f2, fill=WHITE + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return c, 700, YELLOW


def v_tips(c, t, p, gt, sc):
    meteors(c, t, n=8, seed=12, radiant=(W / 2, 900))
    d = ImageDraw.Draw(c)
    hy = 1600
    d.rectangle([0, hy, W, 1920], fill=(10, 14, 22, 255))
    # 寝転んで空を見る人(シルエット)
    d.ellipse([340, hy - 70, 410, hy - 10], fill=(30, 36, 50, 255))
    d.rounded_rectangle([400, hy - 60, 700, hy - 15], radius=20, fill=(30, 36, 50, 255))
    # 視野の扇形
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).pieslice([375 - 700, hy - 40 - 700, 375 + 700, hy - 40 + 700], 200, 340, fill=(120, 200, 255, 40))
    c.alpha_composite(lay)
    sec = int(15 * min(1, t / 3.0))
    box_text(c, 720, 1430, f"{sec:02d}分", 60, YELLOW)
    return c, 700, YELLOW


def v_question(c, t, p, gt, sc):
    meteors(c, t, n=8, seed=13)
    d = ImageDraw.Draw(c)
    for i, (txt, col) in enumerate([("見に行く", (255, 214, 64)), ("寝る", (150, 200, 255))]):
        x0 = 120 + i * 440
        bob = math.sin(t * 3 + i * 1.5) * 8
        d.rounded_rectangle([x0, 1360 + bob, x0 + 400, 1500 + bob], radius=30, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(60)
        d.text((x0 + (400 - d.textlength(txt, font=f)) / 2, 1388 + bob), txt, font=f, fill=col + (255,))
    return c, 720, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, dust=v_dust, phaethon=v_phaethon, sun=v_sun, rockcomet=v_rockcomet,
               notenough=v_notenough, breakup=v_breakup, destiny=v_destiny, calendar=v_calendar, moon=v_moon,
               count=v_count, tips=v_tips, question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (3, 6, 9):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("text-impact3", 0.7), S[3] + 0.05)      # 親は小惑星
    add(se("tin1", 0.5), S[6] + 0.05)              # 全然足りない
    add(se("correct2", 0.6), S[9] + 0.05)          # 見頃
    add(se("kira1", 0.5), S[11] + 0.3)             # 60個
    add(se("pa1", 0.6), S[12] + 0.1)               # コツ
    add(se("kira1", 0.5), S[13] + 0.05)            # 質問


def make_episode():
    return E.Episode("geminids2026", "宇宙ミステリー #2", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.22)


if __name__ == "__main__":
    E.main(make_episode)
