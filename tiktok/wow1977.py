#!/usr/bin/env python3
"""宇宙ミステリー #1「Wow!シグナル(1977年)」

  python3 tiktok/wow1977.py voice    # セリフ・BGM・効果音(VOICEVOX ENGINE が必要)
  python3 tiktok/wow1977.py preview  # 各シーンの静止画
  python3 tiktok/wow1977.py render   # MP4 書き出し
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

import engine as E
from engine import CYAN, RED, W, YELLOW, M, Z, font

# ---------------------------------------------------------------- 台本
# text の [ ] は強調色。d は最低尺(秒)。reveal=(n, 秒) は指定秒まで先頭 n 行だけ出す
SCENES = [
    dict(d=3.6, visual="hook", size=92, text=["宇宙から届いた", "[72秒の信号]", "いまだに正体不明"]),
    dict(d=3.0, visual="teaser", size=76, text=["最後に", "[最新研究の説]も紹介"]),
    dict(d=4.0, visual="telescope", size=74, text=["1977年8月15日", "アメリカの電波望遠鏡", "[ビッグイヤー]がキャッチ"]),
    dict(d=4.0, visual="graph", size=76, text=["いて座の方向から", "宇宙の雑音の[約30倍]", "強い電波"]),
    dict(d=3.5, visual="printout", size=80, text=["記録用紙には", "[6EQUJ5]"]),
    dict(d=4.0, visual="scale", size=74, text=["暗号ではなく", "[電波の強さ]を表す記号"]),  # U が最大(雑音の約30倍)
    dict(d=4.0, visual="printout_wow", size=72, text=["発見した天文学者が", "思わず[「Wow!」]と書き込んだ"]),
    dict(d=4.0, visual="rotation", size=72, text=["なぜ72秒？", "地球の自転で", "同じ空を見られるのが[72秒]"]),
    dict(d=4.0, visual="hydrogen", size=74, text=["周波数は約1420MHz", "宇宙で一番多い", "[水素]が出す電波"]),
    dict(d=4.0, visual="alien", size=72, text=["宇宙人が通信するなら", "[この周波数]を使うかも", "と考えられていた"]),
    dict(d=3.5, visual="nodetect", size=80, text=["でも", "[二度と観測されなかった]"]),
    dict(d=4.0, visual="comet", size=72, text=["2017年 [彗星]が原因説", "→ 発見者らが否定"]),
    dict(d=5.0, visual="magnetar", size=68, text=["＜最新の説（2024年）＞", "強烈なフレアが", "[冷たい水素の雲]を", "一瞬光らせた？"]),
    dict(d=4.0, visual="unresolved", size=74, text=["ただし[まだ仮説]", "正体は今も", "確定していない"]),
    dict(d=5.5, visual="question", size=76, text=["あなたはどっち？", "[宇宙人]？[自然現象]？", "コメントで教えて"]),
]

# 口調: ずんだもん=「ボク」「〜のだ」 / 四国めたん=「わたくし」お嬢様風タメ口・二人称「アンタ(たち)」
LINES = [
    [(Z, "宇宙から、72秒だけ届いた謎の信号。いまだに、正体不明なのだ！")],
    [(M, "最後に、最新の研究で出てきた説も、わたくしが教えてあげるわ。")],
    [(M, "1977年8月15日。アメリカの電波望遠鏡ビッグイヤーが、謎の信号をとらえたの。")],
    [(M, "いて座の方向から、宇宙の雑音の約30倍という、強い電波が届いたのよ。"), (Z, "30倍！？")],
    [(M, "記録用紙には、6、E、Q、U、J、5。"), (Z, "暗号なのだ！？")],
    [(M, "残念、暗号じゃないわ。電波の強さを、数字と文字で表しただけよ。")],
    [(M, "見つけた天文学者のジェリー・エーマンは、思わず赤ペンで、ワオ！と書き込んだの。"), (Z, "だから、ワオ！シグナルなのだ！")],
    [(M, "72秒なのは、地球の自転で、空の同じ場所を見られるのが72秒だったからよ。")],
    [(M, "しかも周波数は、およそ1420メガヘルツ。宇宙で一番多い、水素が出す電波なの。")],
    [(M, "宇宙人が通信するなら、この周波数を使うかもしれない。そう考えられていたのよ。"), (Z, "ますます宇宙人っぽいのだ！")],
    [(M, "でも、同じ方向を何度観測しても、二度と見つからなかったの。"), (Z, "えー！")],
    [(M, "2017年には、彗星が原因という説も出たけど、発見者たちから否定されたわ。"), (Z, "じゃあ、正体は何なのだ？")],
    [(M, "2024年の新説はこう。マグネターという星の強烈なフレアが、冷たい水素の雲を一瞬だけ光らせた、というものよ。")],
    [(M, "ただし、これもまだ仮説。正体は、今も確定していないの。"), (Z, "50年近くたっても、謎のままなのだ。")],
    [(Z, "みんなは、宇宙人だと思うのだ？"), (M, "宇宙人？自然現象？アンタたちの考え、コメントで聞かせなさい。")],
]

# 6EQUJ5 の強さ(0-9, A=10 ... Z=35)
SEQ = "6EQUJ5"
SEQV = [int(c) if c.isdigit() else ord(c) - 55 for c in SEQ]


# ---------------------------------------------------------------- イラスト部品
def waves(c, src, t, n=5, color=(120, 230, 255), max_r=1400, speed=420, width=8):
    """src から広がる電波の輪。"""
    d = ImageDraw.Draw(c)
    for k in range(n):
        r = (t * speed + k * max_r / n) % max_r
        a = int(130 * (1 - r / max_r))
        d.arc([src[0] - r, src[1] - r, src[0] + r, src[1] + r], 20, 160, fill=color + (a,), width=width)


def glow(c, xy, r, color, alpha=200, blur=None):
    g = Image.new("RGBA", (int(r * 4), int(r * 4)), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([r, r, r * 3, r * 3], fill=color + (alpha,))
    g = g.filter(ImageFilter.GaussianBlur(blur or r * 0.6))
    c.alpha_composite(g, (int(xy[0] - r * 2), int(xy[1] - r * 2)))


def dish(c, cx, cy, s=1.0, tilt=-25):
    """電波望遠鏡(パラボラ)のイラスト。"""
    lay = Image.new("RGBA", (int(700 * s), int(700 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    o = 350 * s
    d.polygon([(o - 60 * s, o + 80 * s), (o + 60 * s, o + 80 * s), (o + 120 * s, o + 330 * s), (o - 120 * s, o + 330 * s)], fill=(150, 155, 170, 255))
    d.chord([o - 260 * s, o - 200 * s, o + 260 * s, o + 140 * s], 0, 180, fill=(225, 230, 240, 255), outline=(90, 95, 110, 255), width=int(8 * s))
    d.line([o, o - 30 * s, o, o - 230 * s], fill=(90, 95, 110, 255), width=int(10 * s))
    d.ellipse([o - 22 * s, o - 255 * s, o + 22 * s, o - 210 * s], fill=(255, 120, 90, 255))
    lay = lay.rotate(tilt, resample=Image.BICUBIC)
    c.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))


def paper(c, t, wow=False, x0=170, y0=1040, w=740, h=600):
    """記録用紙(※イメージ)。6EQUJ5 を縦に並べる。"""
    lay = Image.new("RGBA", (w, h), (246, 244, 232, 255))
    d = ImageDraw.Draw(lay)
    rng = random.Random(4)
    f = font(44, black=False)
    cols = 9
    for row in range(9):
        for col in range(cols):
            x, y = 40 + col * 76, 30 + row * 62
            if col == 4 and 1 <= row <= 6:
                ch = SEQ[row - 1]
                d.text((x, y), ch, font=font(48), fill=(20, 20, 20, 255))
            else:
                ch = rng.choice(["1", " ", " ", "1", "2", " ", "1", "3"])
                d.text((x, y), ch, font=f, fill=(110, 110, 110, 255))
    for k in range(0, h, 24):
        d.ellipse([8, k + 6, 18, k + 16], fill=(210, 205, 190, 255))
        d.ellipse([w - 18, k + 6, w - 8, k + 16], fill=(210, 205, 190, 255))
    if wow:
        p = min(1, t / 0.8)
        cx = 40 + 4 * 76 + 14
        d.rounded_rectangle([cx - 34, 80, cx + 54, 80 + int(380 * p)], radius=40, outline=(220, 30, 30, 255), width=7)
        if t > 0.9:
            d.text((cx + 90, 150), "Wow!", font=font(96), fill=(220, 30, 30, 255))
    lay = lay.rotate(-3, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(lay, (x0, y0))


def ufo(c, cx, cy, t):
    d = ImageDraw.Draw(c)
    bob = math.sin(t * 3) * 12
    glow(c, (cx, cy + 60 + bob), 120, (140, 255, 180), 90)
    d.ellipse([cx - 90, cy - 80 + bob, cx + 90, cy + 20 + bob], fill=(170, 230, 255, 200), outline=(60, 90, 110, 255), width=6)
    d.ellipse([cx - 230, cy - 20 + bob, cx + 230, cy + 70 + bob], fill=(150, 155, 175, 255), outline=(60, 60, 80, 255), width=6)
    for k in range(-2, 3):
        on = (int(t * 6) + k) % 2 == 0
        d.ellipse([cx + k * 80 - 14, cy + 14 + bob, cx + k * 80 + 14, cy + 42 + bob], fill=(255, 230, 90, 255) if on else (120, 110, 60, 255))


# ---------------------------------------------------------------- シーンごとの絵
# fn(canvas, t, p, gt, sc) -> (canvas, 字幕の中心y, 強調色)
def v_hook(c, t, p, gt, sc):
    src = (880, 520)
    glow(c, src, 40, (255, 255, 255), 230)
    waves(c, src, t, n=6)
    c.alpha_composite(E.EARTH, (int(W / 2 - E.EARTH.width / 2), 1420))
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    return c, 800, RED


def v_teaser(c, t, p, gt, sc):
    src = (880, 520)
    glow(c, src, 30, (255, 255, 255), 200)
    waves(c, src, t, n=5)
    return c, 780, YELLOW


def v_telescope(c, t, p, gt, sc):
    waves(c, (900, 300), t, n=4, max_r=1200)
    dish(c, W / 2, 1320, 1.1)
    E.mark_image(c, "※電波望遠鏡のイメージ（実物は形が異なる）", (60, 1700))
    return c, 700, YELLOW


def v_graph(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    x0, y0, w, h = 140, 1080, 800, 520
    d.rounded_rectangle([x0 - 20, y0 - 20, x0 + w + 20, y0 + h + 60], radius=20, fill=(0, 0, 0, 150))
    d.line([x0, y0 + h, x0 + w, y0 + h], fill=(200, 200, 210, 255), width=4)
    rng = random.Random(8)
    grow = min(1, t / 1.6)
    bw = w / 22
    for i in range(22):
        if 8 <= i < 14:
            v = SEQV[i - 8] / 30
            col = (255, 90, 90) if SEQ[i - 8] == "U" else (255, 200, 80)
        else:
            v = rng.random() * 0.06 + 0.02
            col = (120, 180, 230)
        bh = h * 0.92 * v * grow
        d.rectangle([x0 + i * bw + 4, y0 + h - bh, x0 + (i + 1) * bw - 4, y0 + h], fill=col + (255,))
    if grow >= 1:
        d.text((x0 + 11 * bw - 60, y0 - 10), "約30倍", font=font(56), fill=RED + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    d.text((x0, y0 + h + 8), "← 宇宙の雑音", font=font(34, black=False), fill=(200, 210, 230, 255))
    return c, 700, YELLOW


def v_printout(c, t, p, gt, sc):
    paper(c, t)
    E.mark_image(c, "※記録用紙のイメージ", (170, 1700))
    return c, 700, YELLOW


def v_scale(c, t, p, gt, sc):
    """強さの目盛り: 0〜9, A〜Z の順に強くなる。6EQUJ5 の文字だけ目盛り上に表示。"""
    d = ImageDraw.Draw(c)
    x0, x1, y = 110, 970, 1300
    for i in range(x1 - x0):
        k = i / (x1 - x0)
        d.line([x0 + i, y, x0 + i, y + 40], fill=(int(80 + 175 * k), int(160 - 90 * k), int(255 - 180 * k), 255))
    d.text((x0, y + 60), "0（弱い）", font=font(40), fill=(170, 200, 240, 255))
    d.text((x1 - 190, y + 60), "Z（強い）", font=font(40), fill=(255, 140, 140, 255))
    shown = min(len(SEQ), int(t / 0.35) + 1)
    for j, ch in enumerate(SEQ[:shown]):
        x = x0 + (x1 - x0) * SEQV[j] / 35
        lx = x + {"5": -20, "6": 20}.get(ch, 0)  # 5と6が重ならないよう少しずらす
        hot = ch == "U"
        f = font(70 if hot else 54)
        w = d.textlength(ch, font=f)
        d.line([x, y - 10, x, y - 40], fill=(255, 255, 255, 255), width=4)
        d.text((lx - w / 2, y - 130 - (20 if hot else 0)), ch, font=f, fill=(RED if hot else YELLOW) + (255,),
               stroke_width=4, stroke_fill=(0, 0, 0, 255))
    if t > 2.4:
        d.text((x1 - 540, y + 130), "U ＝ 雑音の約30倍", font=font(54), fill=RED + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return c, 700, YELLOW


def v_printout_wow(c, t, p, gt, sc):
    paper(c, t, wow=True)
    E.mark_image(c, "※記録用紙のイメージ", (170, 1700))
    return c, 700, RED


def v_rotation(c, t, p, gt, sc):
    ex, ey = W / 2, 1380
    c.alpha_composite(E.EARTH, (int(ex - E.EARTH.width / 2), int(ey - E.EARTH.height / 2)))
    ang = -70 + 140 * p
    d = ImageDraw.Draw(c)
    rx, ry = ex + 300 * math.sin(math.radians(ang)), ey - 300 * math.cos(math.radians(ang))
    tx, ty = ex + 900 * math.sin(math.radians(ang)), ey - 900 * math.cos(math.radians(ang))
    beam = Image.new("RGBA", c.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    left = math.radians(ang - 6)
    right = math.radians(ang + 6)
    bd.polygon([(rx, ry), (ex + 1100 * math.sin(left), ey - 1100 * math.cos(left)), (ex + 1100 * math.sin(right), ey - 1100 * math.cos(right))], fill=(120, 230, 255, 70))
    c.alpha_composite(beam)
    star = (W / 2, 900)
    hit = abs(ang) < 6
    glow(c, star, 30 if hit else 14, (255, 255, 160) if hit else (255, 255, 255), 255 if hit else 160)
    sec = int(72 * max(0, min(1, (6 - abs(ang)) / 12 + 0.5))) if hit else (0 if ang < 0 else 72)
    d.text((W - 300, 1650), f"{sec:02d}秒", font=font(70), fill=YELLOW + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return c, 620, YELLOW


def v_hydrogen(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1300
    glow(c, (cx, cy), 60, (255, 120, 120), 230)
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 90, 90, 255))
    d.text((cx - 20, cy - 34), "＋", font=font(50), fill=(255, 255, 255, 255))
    d.ellipse([cx - 260, cy - 140, cx + 260, cy + 140], outline=(150, 220, 255, 200), width=5)
    a = t * 2.5
    ex, ey = cx + 260 * math.cos(a), cy + 140 * math.sin(a)
    glow(c, (ex, ey), 22, (150, 220, 255), 230)
    d.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=(150, 220, 255, 255))
    d.text((cx - 150, cy + 200), "水素原子", font=font(56), fill=WHITE_ALPHA, stroke_width=4, stroke_fill=(0, 0, 0, 255))
    waves(c, (cx, cy), t, n=3, max_r=600, speed=250, width=5)
    return c, 690, YELLOW


WHITE_ALPHA = (255, 255, 255, 255)


def v_alien(c, t, p, gt, sc):
    ufo(c, W / 2, 1250, t)
    waves(c, (W / 2, 1250), t, n=3, max_r=700, speed=260, width=5, color=(140, 255, 180))
    E.mark_image(c, "※イメージ", (W - 230, 1640))
    return c, 690, YELLOW


def v_nodetect(c, t, p, gt, sc):
    dish(c, W / 2, 1360, 0.9, tilt=-15 + 15 * math.sin(t * 1.5))
    d = ImageDraw.Draw(c)
    if t > 0.6:
        d.rounded_rectangle([W / 2 - 230, 1020, W / 2 + 230, 1120], radius=20, fill=(0, 0, 0, 170), outline=(255, 90, 90, 255), width=4)
        s = "信号なし"
        f = font(60)
        d.text(((W - d.textlength(s, font=f)) / 2, 1030), s, font=f, fill=(255, 120, 120, 255))
    return c, 760, RED


def v_comet(c, t, p, gt, sc):
    E.paste_comet(c, (850 - p * 120, 1320), -18, scale=0.8)
    d = ImageDraw.Draw(c)
    if t > 1.2:
        k = min(1, (t - 1.2) / 0.25)
        cx, cy, r = W / 2, 1300, 190 * k
        d.line([cx - r, cy - r, cx + r, cy + r], fill=RED + (255,), width=26)
        d.line([cx - r, cy + r, cx + r, cy - r], fill=RED + (255,), width=26)
    return c, 740, YELLOW


def v_magnetar(c, t, p, gt, sc):
    mx, my = 230, 1150
    flare = 0.5 + 0.5 * math.sin(t * 9) if t < 2 else 0.3
    glow(c, (mx, my), 50 + 40 * flare, (200, 160, 255), 255)
    d = ImageDraw.Draw(c)
    d.ellipse([mx - 26, my - 26, mx + 26, my + 26], fill=(255, 255, 255, 255))
    d.text((mx - 110, my + 90), "マグネター", font=font(40), fill=(220, 200, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
    # フレアの光線
    k = min(1, t / 1.2)
    beam = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(beam).polygon([(mx, my - 20), (mx + 560 * k, my + 140 - 120), (mx + 560 * k, my + 140 + 120), (mx, my + 20)], fill=(220, 190, 255, 110))
    c.alpha_composite(beam.filter(ImageFilter.GaussianBlur(8)))
    # 水素の雲(フレアが届くと光る)
    cx, cy = 790, 1290
    lit = max(0, min(1, (t - 1.2) / 0.4)) * (1 if t < 3.2 else max(0, 1 - (t - 3.2) / 0.8))
    cloud = Image.new("RGBA", c.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(cloud)
    rng = random.Random(6)
    for _ in range(14):
        ox, oy, r = rng.randint(-150, 150), rng.randint(-90, 90), rng.randint(60, 120)
        col = (int(90 + 165 * lit), int(110 + 145 * lit), int(160 + 95 * lit), int(140 + 100 * lit))
        cd.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=col)
    c.alpha_composite(cloud.filter(ImageFilter.GaussianBlur(28)))
    d.text((cx - 120, cy + 170), "水素の雲", font=font(40), fill=(200, 230, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
    if lit > 0.3:
        waves(c, (cx, cy), t, n=3, max_r=500, speed=300, width=5)
    E.mark_image(c, "※イメージ", (W - 230, 1640))
    return c, 650, CYAN


def v_unresolved(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    s = 1 + 0.05 * math.sin(t * 3)
    f = font(int(420 * s))
    w = d.textlength("？", font=f)
    d.text(((W - w) / 2, 1020), "？", font=f, fill=(255, 214, 64, 230), stroke_width=10, stroke_fill=(0, 0, 0, 255))
    return c, 700, YELLOW


def v_question(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    for i, (txt, col) in enumerate([("宇宙人", (140, 255, 180)), ("自然現象", (120, 200, 255))]):
        x0 = 120 + i * 440
        bob = math.sin(t * 3 + i * 1.5) * 8
        d.rounded_rectangle([x0, 1360 + bob, x0 + 400, 1500 + bob], radius=30, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(60)
        d.text((x0 + (400 - d.textlength(txt, font=f)) / 2, 1388 + bob), txt, font=f, fill=col + (255,))
    return c, 720, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, telescope=v_telescope, graph=v_graph, printout=v_printout,
               scale=v_scale, printout_wow=v_printout_wow, rotation=v_rotation, hydrogen=v_hydrogen,
               alien=v_alien, nodetect=v_nodetect, comet=v_comet, magnetar=v_magnetar,
               unresolved=v_unresolved, question=v_question)


# ---------------------------------------------------------------- 効果音(効果音ラボ)
def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (4, 6, 10, 12):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("kira1", 0.5), S[3] + 1.6)                     # 約30倍
    add(se("text-impact3", 0.7), S[4] + 0.05)             # 6EQUJ5
    add(se("tin1", 0.6), S[5] + 0.05)                     # 暗号じゃない(ちーん)
    add(se("pa1", 0.6), S[6] + 0.9)                       # Wow! 書き込み
    add(se("kira1", 0.5), S[8] + 0.1)                     # 水素
    add(se("clock-tower-bell1", 0.5), S[10] + 0.05)       # 二度と観測されず
    add(se("pa1", 0.6), S[11] + 1.2)                      # 否定×
    add(se("correct2", 0.6), S[12] + 0.05)                # 最新の説
    add(se("kira1", 0.5), S[14] + 0.05)                   # 質問


def make_episode():
    return E.Episode("wow1977", "宇宙ミステリー #1", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.22)


if __name__ == "__main__":
    E.main(make_episode)
