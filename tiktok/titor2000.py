#!/usr/bin/env python3
"""未来人 #1「2036年から来た男 ジョン・タイター」

  python3 tiktok/titor2000.py voice | preview | render

方針: 都市伝説として紹介し、予言は「外れた予言」として答え合わせする。「本物かも」で締めない。
"""
import math
import random

from PIL import Image, ImageDraw

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, font
from wow1977 import glow

SCENES = [
    dict(d=3.6, visual="hook", size=84, text=["2000年 ネット掲示板に", "[2036年から来た男]が", "現れた"]),
    dict(d=3.0, visual="teaser", size=76, text=["最後に", "[正体の説]も紹介"]),
    dict(d=4.5, visual="forum", size=72, text=["名前は[ジョン・タイター]", "2000〜2001年に", "書き込みを続けた"]),
    dict(d=4.5, visual="ibm", size=70, text=["任務は", "1975年のコンピューター", "[IBM 5100]を手に入れること"]),
    dict(d=4.5, visual="y2038", size=70, text=["2038年に起きる", "コンピューターの", "[時刻の問題]を直すため"]),
    dict(d=3.5, visual="real", size=76, text=["この[2038年問題]は", "実在する"]),
    dict(d=4.5, visual="secret", size=68, text=["IBM 5100の", "[関係者しか知らない機能]", "まで語っていた"]),
    dict(d=4.0, visual="boom", size=74, text=["信じる人が続出", "本や[グッズ]まで"]),
    dict(d=3.0, visual="predict", size=84, text=["では", "[予言]の答え合わせ"]),
    dict(d=4.5, visual="p1", size=72, text=["2004年ごろから", "アメリカで[内戦]", "→ 起きなかった"]),
    dict(d=4.5, visual="p2", size=72, text=["2004年の後", "[オリンピック]は開かれない", "→ 普通に開催"]),
    dict(d=3.5, visual="p3", size=76, text=["2015年に[世界大戦]", "→ 起きなかった"]),
    dict(d=5.0, visual="worldline", size=68, text=["でも彼は", "「[世界線]がずれれば", "未来も変わる」と"]),
    dict(d=5.5, visual="identity", size=66, text=["＜正体の説＞", "2009年の調査などで", "[フロリダの兄弟]が作った説", "（本人たちは否定）"]),
    dict(d=4.5, visual="steins", size=70, text=["ちなみに", "『シュタインズ・ゲート』の", "[元ネタ]にもなった"]),
    dict(d=5.5, visual="question", size=74, text=["当時のあなたなら", "[信じた]？[信じない]？", "コメントで教えて"]),
]

LINES = [
    [(Z, "2000年、ネットの掲示板に、2036年から来たという男が現れたのだ！")],
    [(M, "最後に、彼の正体として出てきた説も、わたくしが教えてあげるわ。")],
    [(M, "名前はジョン・タイター。2000年11月から2001年にかけて、掲示板に書き込みを続けたの。")],
    [(M, "彼は2036年から来た兵士で、任務は1975年のコンピューター、アイビーエム、ごーいちまるまるを手に入れることだったの。"), (Z, "なんで古いパソコンなのだ？")],
    [(M, "2038年に、古いコンピューターの時刻の計算が狂う問題が起きる。それを直すのに必要だ、という話だったの。")],
    [(M, "しかもこの2038年問題、本当に存在する問題なのよ。"), (Z, "リアルなのだ…！")],
    [(M, "さらに、ごーいちまるまるの、関係者くらいしか知らない機能まで語っていた、と言われているわ。")],
    [(M, "これで信じる人が一気に増えて、本やグッズまで作られたのよ。")],
    [(M, "では、彼の予言の答え合わせをしましょう。")],
    [(M, "2004年の大統領選挙のころから、アメリカで内戦が始まると言っていたけど、起きなかったわ。")],
    [(M, "2004年のあとは、オリンピックも開かれなくなると言ったけど、その後も普通に開かれているわね。"), (Z, "東京オリンピックもあったのだ！")],
    [(M, "2015年に世界大戦が起きる、という予言も外れたわ。")],
    [(M, "でも彼は、自分が来たことで世界線がずれて、未来は少しずつ変わる、と言っていたの。"), (Z, "外れても言い訳できるのだ！")],
    [(M, "約束の正体よ。2009年の調査などで、フロリダの、コンピューターに詳しい兄弟が作った、という説が出たの。本人たちは否定しているけどね。")],
    [(M, "ちなみにタイターは、日本のゲームやアニメ、シュタインズ・ゲートの元ネタにもなっているのよ。"), (Z, "そっちで知ってる人も多いのだ！")],
    [(Z, "みんなは当時、信じたと思うのだ？"), (M, "信じた？信じない？アンタたちの答え、コメントで聞かせなさい。")],
]

GREEN = (110, 255, 140)


# ---------------------------------------------------------------- 部品
def screen(c, x0, y0, w, h, lines, t, typing=True, size=40, color=GREEN):
    """古いパソコン画面風の掲示板(イメージ)。"""
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([x0 - 24, y0 - 24, x0 + w + 24, y0 + h + 24], radius=26, fill=(60, 60, 66, 255))
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(8, 22, 12, 255))
    for k in range(0, h, 6):
        d.line([x0, y0 + k, x0 + w, y0 + k], fill=(0, 0, 0, 70))
    f = font(size, black=False)
    shown = int(t * 28) if typing else 10 ** 6
    y = y0 + 24
    for ln in lines:
        s = ln[:max(0, shown)]
        shown -= len(ln)
        d.text((x0 + 24, y), s, font=f, fill=color + (255,))
        y += size * 1.45
    if int(t * 2) % 2 == 0:
        d.rectangle([x0 + 24, y + 4, x0 + 44, y + size], fill=color + (255,))


def oldpc(c, cx, cy, t, s=1.0):
    """1970年代の一体型コンピューター(イメージ)。"""
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([cx - 330 * s, cy - 220 * s, cx + 330 * s, cy + 200 * s], radius=20, fill=(200, 195, 180, 255), outline=(90, 85, 75, 255), width=5)
    d.rectangle([cx - 270 * s, cy - 180 * s, cx + 20 * s, cy + 10 * s], fill=(15, 30, 20, 255))
    for k in range(5):
        d.line([cx - 250 * s, cy - 150 * s + k * 32 * s, cx - 250 * s + (180 + 60 * math.sin(k + t)) * s, cy - 150 * s + k * 32 * s], fill=GREEN + (220,), width=int(6 * s))
    for r in range(4):
        for q in range(12):
            x = cx - 300 * s + q * 50 * s
            y = cy + 60 * s + r * 32 * s
            d.rectangle([x, y, x + 40 * s, y + 24 * s], fill=(120, 115, 105, 255))
    d.rectangle([cx + 60 * s, cy - 160 * s, cx + 290 * s, cy - 110 * s], fill=(60, 60, 60, 255))


def stamp(c, cx, cy, text, t, t0, col=RED, size=90):
    if t < t0:
        return
    k = min(1, (t - t0) / 0.18)
    lay = Image.new("RGBA", (520, 180), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([0, 0, 519, 179], radius=18, outline=col + (255,), width=12)
    f = font(size)
    ld.text(((520 - ld.textlength(text, font=f)) / 2, (180 - size * 1.3) / 2), text, font=f, fill=col + (255,))
    sc = 1.8 - 0.8 * k
    lay = lay.rotate(-10, expand=True, resample=Image.BICUBIC)
    lay = lay.resize((int(lay.width * sc), int(lay.height * sc)))
    c.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))


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
    screen(c, 110, 1060, 860, 520, ["> I am a time traveler", "> from the year 2036.", "", "> 2036年から来た"], t * 1.6)
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    E.mark_image(c, "※掲示板のイメージ", (60, 1690))
    return c, 720, RED


def v_teaser(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    f = font(380)
    d.text(((W - d.textlength("？", font=f)) / 2, 1080), "？", font=f, fill=YELLOW + (220,), stroke_width=10, stroke_fill=(0, 0, 0, 255))
    return c, 780, YELLOW


def v_forum(c, t, p, gt, sc):
    screen(c, 110, 1060, 860, 520, ["Name: John Titor", "Date: 2000 - 2001", "", "> from 2036"], t)
    E.mark_image(c, "※掲示板のイメージ", (60, 1690))
    return c, 680, YELLOW


def v_ibm(c, t, p, gt, sc):
    oldpc(c, W / 2, 1360, t)
    E.mark_image(c, "※古いコンピューターのイメージ", (60, 1700))
    return c, 660, YELLOW


def v_y2038(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    glitch = t > 1.2
    s = "2038/01/19 03:14:07" if not glitch else "1901/12/13 20:45:52"
    f = font(66)
    col = GREEN if not glitch else RED
    jx = random.Random(int(t * 20)).randint(-8, 8) if glitch else 0
    screen(c, 110, 1100, 860, 360, [], t, typing=False)
    d.text(((W - d.textlength(s, font=f)) / 2 + jx, 1230), s, font=f, fill=col + (255,))
    E.mark_image(c, "※イメージ", (60, 1600))
    return c, 680, YELLOW


def v_real(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    s = 1 + 0.05 * math.sin(t * 5)
    f = font(int(190 * s))
    txt = "2038"
    d.text(((W - d.textlength(txt, font=f)) / 2, 1150), txt, font=f, fill=YELLOW + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    stamp(c, W / 2, 1480, "実在", t, 0.8, col=(120, 230, 120))
    return c, 760, YELLOW


def v_secret(c, t, p, gt, sc):
    oldpc(c, W / 2, 1380, t, 0.9)
    d = ImageDraw.Draw(c)
    if t > 0.8:
        glow(c, (W / 2 + 160, 1240), 70, (255, 230, 120), 200)
        d.text((W / 2 + 120, 1190), "？", font=font(90), fill=YELLOW + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    return c, 660, YELLOW


def v_boom(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    rng = random.Random(3)
    items = ["本", "Tシャツ", "サイト", "ファン", "本", "考察"]
    for k, it in enumerate(items):
        if t < 0.3 + k * 0.35:
            continue
        x = 130 + (k % 3) * 290 + rng.randint(-20, 20)
        y = 1150 + (k // 3) * 260 + rng.randint(-20, 20)
        d.rounded_rectangle([x, y, x + 240, y + 180], radius=20, fill=(0, 0, 0, 160), outline=(255, 214, 64, 255), width=5)
        f = font(52)
        d.text((x + (240 - d.textlength(it, font=f)) / 2, y + 55), it, font=f, fill=WHITE + (255,))
    return c, 700, YELLOW


def v_predict(c, t, p, gt, sc):
    screen(c, 110, 1100, 860, 420, ["> PREDICTIONS", "> 2004 ...", "> 2015 ..."], t * 1.5)
    return c, 760, YELLOW


def _pred(c, t, year, label):
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([140, 1120, 940, 1500], radius=24, fill=(0, 0, 0, 170), outline=(200, 200, 210, 255), width=4)
    f = font(110)
    d.text(((W - d.textlength(year, font=f)) / 2, 1160), year, font=f, fill=WHITE + (255,))
    f2 = font(64)
    d.text(((W - d.textlength(label, font=f2)) / 2, 1320), label, font=f2, fill=(200, 210, 230, 255))
    stamp(c, W / 2 + 170, 1500, "ハズレ", t, 1.6)


def v_p1(c, t, p, gt, sc):
    _pred(c, t, "2004〜", "アメリカで内戦")
    return c, 680, YELLOW


def v_p2(c, t, p, gt, sc):
    _pred(c, t, "2004以降", "五輪が開かれない")
    return c, 680, YELLOW


def v_p3(c, t, p, gt, sc):
    _pred(c, t, "2015", "世界大戦")
    return c, 700, YELLOW


def v_worldline(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    x0, y0 = 120, 1450
    k = min(1, t / 2.0)
    d.line([x0, y0, x0 + 420, y0], fill=CYAN + (255,), width=10)
    for i, (dy, col) in enumerate([(-200, (255, 140, 140)), (0, CYAN), (200, (255, 214, 64))]):
        ex = x0 + 420 + 420 * k
        d.line([x0 + 420, y0, ex, y0 + dy * k], fill=col + (255,), width=10)
        d.ellipse([ex - 16, y0 + dy * k - 16, ex + 16, y0 + dy * k + 16], fill=col + (255,))
    d.text((x0, y0 + 40), "過去", font=font(44), fill=WHITE + (255,))
    d.text((x0 + 760, y0 - 300), "未来？", font=font(44), fill=WHITE + (255,))
    return c, 680, CYAN


def v_identity(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1390
    for i in (-1, 1):
        x = cx + i * 170
        d.ellipse([x - 70, cy - 170, x + 70, cy - 30], fill=(40, 40, 55, 255))
        d.rounded_rectangle([x - 120, cy - 20, x + 120, cy + 220], radius=60, fill=(40, 40, 55, 255))
        d.text((x - 24, cy - 140), "？", font=font(70), fill=YELLOW + (255,))
    E.mark_image(c, "※シルエットはイメージ", (60, 1700))
    return c, 640, YELLOW


def v_steins(c, t, p, gt, sc):
    oldpc(c, W / 2, 1400, t, 0.7)
    d = ImageDraw.Draw(c)
    glow(c, (W / 2, 1150), 60, (120, 230, 255), 160)
    return c, 680, YELLOW


def v_question(c, t, p, gt, sc):
    options(c, t, [("信じた", (255, 160, 120)), ("信じない", (150, 200, 255))])
    return c, 720, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, forum=v_forum, ibm=v_ibm, y2038=v_y2038, real=v_real, secret=v_secret,
               boom=v_boom, predict=v_predict, p1=v_p1, p2=v_p2, p3=v_p3, worldline=v_worldline,
               identity=v_identity, steins=v_steins, question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (5, 8, 13):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("kira1", 0.5), S[5] + 0.8)                     # 実在
    add(se("clock-tower-bell1", 0.45), S[8] + 0.05)       # 答え合わせ開始
    for k in (9, 10, 11):
        add(se("tin1", 0.5), S[k] + 1.6)                  # ハズレ
    add(se("correct2", 0.6), S[13] + 0.05)                # 正体
    add(se("kira1", 0.5), S[15] + 0.05)


def make_episode():
    return E.Episode("titor2000", "未来人 #1", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.22)


if __name__ == "__main__":
    E.main(make_episode)
