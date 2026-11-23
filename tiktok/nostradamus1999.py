#!/usr/bin/env python3
"""外れた人類滅亡説 #2「ノストラダムス 1999年7の月」

  python3 tiktok/nostradamus1999.py voice | preview | render
"""
import math
import random

from PIL import Image, ImageDraw

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, Z_CRY, font
from wow1977 import glow

SCENES = [
    dict(d=3.6, visual="hook", size=88, text=["1999年7月", "日本中が[ちょっとだけ]", "滅亡を覚悟した"]),
    dict(d=3.0, visual="teaser", size=76, text=["最後に", "予言した本人の[意外な一言]"]),
    dict(d=4.5, visual="who", size=70, text=["ノストラダムス", "16世紀フランスの", "[医師]・占星術師"]),
    dict(d=3.5, visual="doctor", size=74, text=["ペストの治療で", "[名を上げた]とも"]),
    dict(d=4.5, visual="quatrain", size=70, text=["「1999年7の月", "空から[恐怖の大王]が", "来るだろう」"]),
    dict(d=4.0, visual="rare", size=72, text=["年と月まで書いた詩は", "[かなりめずらしい]"]),
    dict(d=5.0, visual="boom", size=66, text=["1973年 日本で", "『ノストラダムスの大予言』", "[3か月で100万部]（当時の広告）"]),
    dict(d=4.0, visual="movie", size=74, text=["翌年には[映画化]", "滅亡説が日本中に"]),
    dict(d=5.0, visual="angol", size=66, text=["「アンゴルモアの大王」は", "モンゴルのこと？", "→ フランスの[地名]説も"]),
    dict(d=3.0, visual="fate", size=88, text=["そして", "[1999年7月]"]),
    dict(d=4.0, visual="calm", size=96, text=["……", "[何も起きなかった]"], reveal=(1, 1.4)),
    dict(d=5.5, visual="answer", size=68, text=["＜答え合わせ＞", "詩に[「人類滅亡」]とは", "書かれていない", "日本で広まった解釈"]),
    dict(d=5.0, visual="promise", size=70, text=["約束の意外な一言", "本人は予言を"]),
    dict(d=5.5, visual="question", size=76, text=["あなたは当時", "[信じてた]？[信じてない]？", "コメントで教えて"]),
]

LINES = [
    [(Z, "1999年7月、日本中がちょっとだけ、人類滅亡を覚悟したのだ！")],
    [(M, "最後に、予言した本人の意外な一言も、わたくしが教えてあげるわ。")],
    [(M, "ノストラダムスは、16世紀フランスの医師で、占星術師。1555年に予言集を出したの。")],
    [(M, "実はペストの治療で、名を上げたとも言われているのよ。"), (Z, "お医者さんだったのだ！？")],
    [(M, "その予言集に、こんな詩があるの。1999年7の月、空から恐怖の大王が来るだろう。")],
    [(M, "ほとんどの詩はあいまいなのに、これは年と月まで書いてある、めずらしい詩なのよ。")],
    [(M, "1973年、日本で、ごとうつとむさんの本、ノストラダムスの大予言が出て、3か月で100万部をうたう大ベストセラーになったの。")],
    [(M, "翌年には映画にもなって、1999年人類滅亡説は、日本中に広まったのよ。"), (Z_CRY, "ボクも怖くなってきたのだ…")],
    [(M, "詩に出てくるアンゴルモアの大王は、モンゴルのことだと言われたけど、フランスの地方の名前、アングーモワのことだという説もあるの。")],
    [(M, "そして、運命の1999年7月。")],
    [(Z, "……何も、起きなかったのだ。")],
    [(M, "答え合わせよ。詩そのものには、人類が滅亡するとは書かれていないの。1999年人類滅亡は、日本で広まった解釈だったのよ。")],
    [(M, "約束の意外な一言よ。ノストラダムス本人は、息子への手紙で、3797年までの予言を書いた、と言っていたの。"), (Z, "1999年で終わる気、なかったのだ！")],
    [(Z, "みんなは当時、信じてたのだ？"), (M, "信じてた？信じてない？まだ生まれてない？アンタたちの話、コメントで聞かせなさい。")],
]


# ---------------------------------------------------------------- 部品
def parchment(c, x0, y0, w, h, lines, size=50, rot=-2, hl=None, strike=None, t=0.0):
    lay = Image.new("RGBA", (w, h), (236, 220, 180, 255))
    d = ImageDraw.Draw(lay)
    for k in range(0, w, 6):
        d.line([k, 0, k, 8], fill=(210, 190, 150, 255))
        d.line([k, h - 8, k, h], fill=(210, 190, 150, 255))
    d.rectangle([0, 0, w - 1, h - 1], outline=(150, 120, 80, 255), width=6)
    f = font(size)
    y = (h - len(lines) * size * 1.5) / 2
    for i, ln in enumerate(lines):
        col = (150, 30, 30, 255) if hl == i else (60, 40, 20, 255)
        tw = d.textlength(ln, font=f)
        x = (w - tw) / 2
        d.text((x, y), ln, font=f, fill=col)
        if strike == i and t > 1.0:
            k = min(1, (t - 1.0) / 0.4)
            d.line([x - 10, y + size * 0.6, x - 10 + (tw + 20) * k, y + size * 0.6], fill=(220, 30, 30, 255), width=10)
        y += size * 1.5
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(lay, (int(x0), int(y0)))


def calendar(c, cx, cy, top, big, color=(200, 40, 50), s=1.0):
    d = ImageDraw.Draw(c)
    w, h = 280 * s, 300 * s
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=30, fill=(250, 248, 240, 255))
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy - h + 140], radius=30, fill=color + (255,))
    d.rectangle([cx - w, cy - h + 100, cx + w, cy - h + 140], fill=color + (255,))
    for txt, f, y, col in [(top, font(64), cy - h + 30, WHITE), (big, font(250), cy - h + 150, (30, 30, 30))]:
        d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col + (255,))


def figure(c, cx, cy, s=1.0):
    """帽子とひげの人物シルエット(イメージ)。"""
    d = ImageDraw.Draw(c)
    col = (40, 30, 60, 255)
    d.ellipse([cx - 90 * s, cy - 120 * s, cx + 90 * s, cy + 60 * s], fill=(225, 200, 170, 255))
    d.polygon([(cx - 80 * s, cy), (cx + 80 * s, cy), (cx + 40 * s, cy + 170 * s), (cx - 40 * s, cy + 170 * s)], fill=(230, 230, 230, 255))
    d.rounded_rectangle([cx - 110 * s, cy - 190 * s, cx + 110 * s, cy - 90 * s], radius=40, fill=col)
    d.rectangle([cx - 140 * s, cy - 110 * s, cx + 140 * s, cy - 85 * s], fill=col)
    d.polygon([(cx - 200 * s, cy + 140 * s), (cx + 200 * s, cy + 140 * s), (cx + 260 * s, cy + 420 * s), (cx - 260 * s, cy + 420 * s)], fill=col)
    d.ellipse([cx - 45 * s, cy - 50 * s, cx - 20 * s, cy - 30 * s], fill=(40, 30, 30, 255))
    d.ellipse([cx + 20 * s, cy - 50 * s, cx + 45 * s, cy - 30 * s], fill=(40, 30, 30, 255))


def options(c, t, items, y=1360):
    d = ImageDraw.Draw(c)
    for i, (txt, col) in enumerate(items):
        x0 = 120 + i * 440
        bob = math.sin(t * 3 + i * 1.5) * 8
        d.rounded_rectangle([x0, y + bob, x0 + 400, y + 140 + bob], radius=30, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(60)
        d.text((x0 + (400 - d.textlength(txt, font=f)) / 2, y + 28 + bob), txt, font=f, fill=col + (255,))


# ---------------------------------------------------------------- シーン
def v_hook(c, t, p, gt, sc):
    glow(c, (W / 2, 1050), 260, (255, 60, 40), int(120 + 60 * math.sin(t * 6)))
    shake = 6 * math.sin(t * 40) * max(0, 1 - t)
    calendar(c, W / 2 + shake, 1350, "1999年", "7月", s=0.9)
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    return c, 720, RED


def v_teaser(c, t, p, gt, sc):
    parchment(c, 200, 1080, 680, 420, ["……？？？？……"], size=70, rot=3)
    return c, 780, YELLOW


def v_who(c, t, p, gt, sc):
    figure(c, W / 2, 1250, 1.0)
    E.mark_image(c, "※人物のイメージ", (60, 1700))
    return c, 650, YELLOW


def v_doctor(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1340
    # 乳鉢と乳棒
    d.chord([cx - 220, cy - 120, cx + 220, cy + 200], 0, 180, fill=(200, 200, 210, 255), outline=(90, 90, 100, 255), width=6)
    ang = math.sin(t * 5) * 0.3
    d.line([cx, cy + 10, cx + 260 * math.sin(0.6 + ang), cy - 260 * math.cos(0.6 + ang)], fill=(150, 120, 90, 255), width=34)
    # バラ
    for k in range(5):
        a = k / 5 * 2 * math.pi + t
        d.ellipse([cx - 330 + 40 * math.cos(a) - 30, cy - 150 + 40 * math.sin(a) - 30, cx - 330 + 40 * math.cos(a) + 30, cy - 150 + 40 * math.sin(a) + 30], fill=(220, 60, 90, 255))
    d.ellipse([cx - 355, cy - 175, cx - 305, cy - 125], fill=(250, 110, 130, 255))
    E.mark_image(c, "※イメージ", (W - 230, 1680))
    return c, 720, YELLOW


def v_quatrain(c, t, p, gt, sc):
    parchment(c, 140, 1040, 800, 520, ["1999年7の月", "空から恐怖の大王が", "来るだろう"], size=64, hl=1)
    E.mark_image(c, "※第10巻72番の一部（日本語訳）", (140, 1680))
    return c, 650, YELLOW


def v_rare(c, t, p, gt, sc):
    rng = random.Random(3)
    for k in range(6):
        x = 70 + (k % 3) * 320
        y = 1050 + (k // 3) * 300
        hl = k == 4
        parchment(c, x, y, 280, 220, ["1999", "7の月"] if hl else ["？？？", "？？"], size=56, rot=rng.uniform(-6, 6), hl=0 if hl else None)
    if t > 0.8:
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([370, 1330, 680, 1580], radius=20, outline=RED + (255,), width=8)
    return c, 700, YELLOW


def v_boom(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    n = int(min(1, t / 2.5) * 14)
    for k in range(n):
        y = 1620 - k * 36
        x = W / 2 - 170 + (k % 2) * 16
        d.rectangle([x, y, x + 340, y + 32], fill=(200 - k * 4, 60, 60, 255), outline=(60, 20, 20, 255), width=3)
    cnt = int(100 * min(1, t / 2.5))
    s = f"{cnt}万部"
    f = font(110)
    d.text(((W - d.textlength(s, font=f)) / 2, 1020), s, font=f, fill=YELLOW + (255,), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※本の絵はイメージ", (60, 1700))
    return c, 650, YELLOW


def v_movie(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1300
    d.rounded_rectangle([cx - 380, cy - 230, cx + 380, cy + 230], radius=16, fill=(15, 15, 20, 255), outline=(200, 200, 210, 255), width=8)
    flick = 120 + int(60 * abs(math.sin(t * 20)))
    d.rectangle([cx - 350, cy - 200, cx + 350, cy + 200], fill=(flick, flick - 20, flick - 40, 255))
    f = font(80)
    s = "1974年 映画化"
    d.text((cx - d.textlength(s, font=f) / 2, cy - 50), s, font=f, fill=(30, 20, 20, 255))
    for k in range(-3, 4):
        d.ellipse([cx + k * 100 - 18, cy + 250, cx + k * 100 + 18, cy + 286], fill=(200, 200, 210, 255))
    return c, 700, YELLOW


def v_angol(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    for i, (title, sub, col) in enumerate([("モンゴル？", "よく言われた説", (150, 200, 255)), ("アングーモワ？", "フランスの地方名", (255, 214, 64))]):
        x0 = 90 + i * 470
        show = t > 0.3 + i * 1.6
        if not show:
            continue
        d.rounded_rectangle([x0, 1160, x0 + 430, 1440], radius=26, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(56)
        d.text((x0 + (430 - d.textlength(title, font=f)) / 2, 1220), title, font=f, fill=col + (255,))
        f2 = font(40, black=False)
        d.text((x0 + (430 - d.textlength(sub, font=f2)) / 2, 1320), sub, font=f2, fill=WHITE + (255,))
    return c, 680, YELLOW


def v_fate(c, t, p, gt, sc):
    glow(c, (W / 2, 1250), 220, (255, 60, 40), int(100 + 80 * math.sin(t * 5)))
    calendar(c, W / 2, 1350, "1999年", "7月", s=0.9)
    return c, 760, RED


def v_calm(c, t, p, gt, sc):
    c.alpha_composite(E.EARTH, (int(W / 2 - E.EARTH.width / 2), 1200))
    return c, 760, CYAN


def v_answer(c, t, p, gt, sc):
    parchment(c, 140, 1120, 800, 420, ["恐怖の大王が来るだろう", "人類は滅亡する"], size=60, strike=1, t=t)
    d = ImageDraw.Draw(c)
    if t > 1.4:
        d.text((560, 1470), "← 書いてない", font=font(48), fill=RED + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return c, 720, CYAN


def v_promise(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    pop = E.ease_out(min(1, max(0, (t - 1.2) / 0.5)))
    if pop > 0:
        f = font(int(230 * (0.6 + 0.4 * pop)))
        s = "3797年"
        d.text(((W - d.textlength(s, font=f)) / 2, 940), s, font=f, fill=YELLOW + (int(255 * pop),), stroke_width=12, stroke_fill=(0, 0, 0, 255))
        f2 = font(60)
        s2 = "までの予言を書いた"
        d.text(((W - d.textlength(s2, font=f2)) / 2, 1250), s2, font=f2, fill=WHITE + (int(255 * pop),), stroke_width=5, stroke_fill=(0, 0, 0, 255))
        s3 = "（息子への手紙＝予言集の序文より）"
        f3 = font(38, black=False)
        d.text(((W - d.textlength(s3, font=f3)) / 2, 1350), s3, font=f3, fill=(220, 220, 230, int(230 * pop)))
    return c, 640, YELLOW


def v_question(c, t, p, gt, sc):
    options(c, t, [("信じてた", (255, 120, 120)), ("信じてない", (150, 200, 255))])
    return c, 720, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, who=v_who, doctor=v_doctor, quatrain=v_quatrain, rare=v_rare,
               boom=v_boom, movie=v_movie, angol=v_angol, fate=v_fate, calm=v_calm, answer=v_answer,
               promise=v_promise, question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (4, 9, 10, 11, 12):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("clock-tower-bell1", 0.5), S[4] + 0.05)       # 詩
    add(se("kira1", 0.5), S[5] + 0.8)                    # めずらしい
    add(se("pa1", 0.6), S[6] + 2.5)                      # 100万部
    add(se("emergency-alert1", 0.35), S[9])              # 運命の1999年7月
    last = sc[10]["lines"][-1]
    add(se("tin1", 0.8), S[10] + last["start"] + last["dur"] + 0.05)  # 何も起きなかった
    add(se("correct2", 0.6), S[11] + 0.05)               # 答え合わせ
    add(se("text-impact3", 0.8), S[12] + 1.2)            # 3797年


def make_episode():
    return E.Episode("nostradamus1999", "外れた人類滅亡説 #2", [dict(s) for s in SCENES], LINES, VISUALS,
                     sfx=sfx, speed=1.22, lead={10: 1.0}, calm_scenes=(10,))


if __name__ == "__main__":
    E.main(make_episode)
