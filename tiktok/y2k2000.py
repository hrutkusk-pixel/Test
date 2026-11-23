#!/usr/bin/env python3
"""外れた人類滅亡説 #3「2000年問題」(立ち絵あり)

  python3 tiktok/y2k2000.py voice | preview | render
"""
import math
import random

from PIL import Image, ImageDraw

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, font
from wow1977 import glow

SCENES = [
    dict(d=3.6, visual="hook", size=84, text=["[世界中のコンピューター]が", "止まると言われた日"]),
    dict(d=3.0, visual="teaser", size=74, text=["最後に", "本当にトラブルが出た", "[意外な日]も紹介"]),
    dict(d=4.5, visual="digits", size=72, text=["昔のコンピューターは", "年を[下2ケタ]だけで", "記録していた"]),
    dict(d=4.5, visual="rollover", size=74, text=["1999年の次は[00年]", "→ 1900年と勘違い？"]),
    dict(d=4.0, visual="systems", size=72, text=["銀行・電気・交通…", "システムが[止まる]かも？"]),
    dict(d=4.5, visual="stock", size=70, text=["1999年10月", "日本政府も", "[食料と水の備蓄]を呼びかけ"]),
    dict(d=4.5, visual="survey", size=70, text=["でも当時の調査では", "[約半数]が", "「備蓄しない」"]),
    dict(d=5.0, visual="cost", size=66, text=["世界の対策費は", "[3000億〜6000億ドル]とも", "（推計）"]),
    dict(d=3.0, visual="countdown", size=86, text=["そして", "[2000年1月1日]"]),
    dict(d=4.0, visual="calm", size=88, text=["……", "[大きな混乱はなかった]"], reveal=(1, 1.4)),
    dict(d=5.0, visual="minor", size=68, text=["ただし", "原発の表示システムなどで", "[小さな不具合]はあった"]),
    dict(d=5.5, visual="answer", size=68, text=["＜答え合わせ＞", "大混乱にならなかったのは", "[対策が進んだから]", "という見方が多い"]),
    dict(d=4.0, visual="leap", size=74, text=["約束の意外な日", "[2000年2月29日]"]),
    dict(d=5.0, visual="rule", size=66, text=["100で割り切れる年はうるう年じゃない", "でも400で割り切れる年はうるう年", "→ [400年に1度]の特別なうるう年"]),
    dict(d=5.0, visual="atm", size=70, text=["郵便貯金のATM", "[約1200台]が動かず", "（午後に復旧）"]),
    dict(d=5.5, visual="question", size=74, text=["あなたは2000年問題", "[覚えてる]？[知らない]？", "コメントで教えて"]),
]

LINES = [
    [(Z, "世界中のコンピューターが止まる、と言われた日があったのだ！")],
    [(M, "最後に、本当にトラブルが目立った、意外な日も、わたくしが教えてあげるわ。")],
    [(M, "昔のコンピューターは、記憶する容量を節約するために、年を下2ケタだけで記録していたの。")],
    [(M, "すると、1999年の次は00年。コンピューターが、1900年と勘違いするかもしれない、というわけ。"), (Z, "100年タイムスリップなのだ！")],
    [(M, "銀行、電気、交通。いろんなシステムが止まるかもしれないと、世界中で心配されたのよ。")],
    [(M, "日本でも1999年10月、政府が、数日分の食料と水を備蓄するよう呼びかけたの。")],
    [(M, "でも当時の調査では、約半数の世帯が、備蓄はしないと答えていたそうよ。"), (Z, "意外とのんきなのだ！")],
    [(M, "対策にかかったお金は、世界で3000億から6000億ドル、日本円で数十兆円ともいわれているわ。")],
    [(M, "そして迎えた、2000年1月1日。")],
    [(Z, "……大きな混乱は、起きなかったのだ。")],
    [(M, "ただし、原子力発電所の表示システムなどで、小さな不具合はあったの。運転には影響しなかったけどね。")],
    [(M, "答え合わせよ。大混乱にならなかったのは、世界中で対策が進んだから、という見方が多いの。大げさだった、という声もあるけどね。"), (Z, "がんばった人たちがいたのだ！")],
    [(M, "約束の意外な日よ。トラブルが目立ったのは、2000年2月29日。うるう日だったの。")],
    [(M, "100で割り切れる年はうるう年じゃない。でも400で割り切れる年はうるう年。2000年は、400年に1度の特別なうるう年だったのよ。")],
    [(M, "その日、郵便貯金のATMが、全国で約1200台動かなくなったの。午後には直ったけどね。"), (Z, "本番はそっちだったのだ！")],
    [(Z, "みんなは、2000年問題、覚えてるのだ？"), (M, "覚えてる？知らない？アンタたちの思い出、コメントで聞かせなさい。")],
]

GREEN = (110, 255, 140)


def screen(c, x0, y0, w, h, text, color=GREEN, size=110, jitter=0):
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([x0 - 24, y0 - 24, x0 + w + 24, y0 + h + 24], radius=26, fill=(60, 60, 66, 255))
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(8, 22, 12, 255))
    for k in range(0, h, 6):
        d.line([x0, y0 + k, x0 + w, y0 + k], fill=(0, 0, 0, 70))
    f = font(size)
    d.text((x0 + (w - d.textlength(text, font=f)) / 2 + jitter, y0 + (h - size * 1.3) / 2), text, font=f, fill=color + (255,))


def options(c, t, items, y=1180):
    d = ImageDraw.Draw(c)
    for i, (txt, col) in enumerate(items):
        x0 = 120 + i * 440
        bob = math.sin(t * 3 + i * 1.5) * 8
        d.rounded_rectangle([x0, y + bob, x0 + 400, y + 140 + bob], radius=30, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(60)
        d.text((x0 + (400 - d.textlength(txt, font=f)) / 2, y + 28 + bob), txt, font=f, fill=col + (255,))


def calendar(c, cx, cy, top, big, color=(200, 40, 50), s=1.0):
    d = ImageDraw.Draw(c)
    w, h = 280 * s, 300 * s
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=30, fill=(250, 248, 240, 255))
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy - h + 140], radius=30, fill=color + (255,))
    d.rectangle([cx - w, cy - h + 100, cx + w, cy - h + 140], fill=color + (255,))
    for txt, f, y, col in [(top, font(64), cy - h + 30, WHITE), (big, font(220), cy - h + 160, (30, 30, 30))]:
        d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col + (255,))


# ---------------------------------------------------------------- シーン(立ち絵が下から出るので、絵は 1000〜1450 付近に置く)
def v_hook(c, t, p, gt, sc):
    j = random.Random(int(t * 25)).randint(-10, 10) if t > 0.4 else 0
    screen(c, 140, 1000, 800, 380, "ERROR" if int(t * 4) % 2 else "1900/01/01", RED, 110, j)
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    return c, 720, RED


def v_teaser(c, t, p, gt, sc):
    calendar(c, W / 2, 1220, "2000年", "？", (60, 90, 180), 0.75)
    return c, 700, YELLOW


def v_digits(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    f = font(170)
    x = W / 2 - d.textlength("1999", font=f) / 2
    a = 255 if t < 1.2 else int(255 * max(0.15, 1 - (t - 1.2) / 0.6))
    d.text((x, 1080), "19", font=f, fill=(200, 200, 210, a), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    d.text((x + d.textlength("19", font=f), 1080), "99", font=f, fill=YELLOW + (255,), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    return c, 680, YELLOW


def v_rollover(c, t, p, gt, sc):
    s = "99" if t < 1.0 else "00"
    col = GREEN if t < 1.0 else RED
    screen(c, 240, 1000, 600, 360, s, col, 200)
    if t > 1.6:
        d = ImageDraw.Draw(c)
        f = font(64)
        d.text(((W - d.textlength("= 1900年？", font=f)) / 2, 1400), "= 1900年？", font=f, fill=RED + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    return c, 680, YELLOW


def v_systems(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    for i, txt in enumerate(["銀行", "電気", "交通"]):
        x0 = 110 + i * 300
        on = (int(t * 3) + i) % 3 != 0
        col = (120, 230, 120) if on else RED
        d.rounded_rectangle([x0, 1050, x0 + 260, 1330], radius=24, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(66)
        d.text((x0 + (260 - d.textlength(txt, font=f)) / 2, 1110), txt, font=f, fill=WHITE + (255,))
        d.text((x0 + 95, 1210), "?" if on else "×", font=font(70), fill=col + (255,))
    return c, 700, YELLOW


def v_stock(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1250
    for k in range(3):
        x = cx - 300 + k * 110
        d.rounded_rectangle([x, cy - 160, x + 90, cy + 140], radius=20, fill=(140, 200, 255, 220), outline=(40, 80, 140, 255), width=4)
        d.rectangle([x + 30, cy - 190, x + 60, cy - 160], fill=(40, 80, 140, 255))
    d.rectangle([cx + 40, cy - 60, cx + 330, cy + 140], fill=(220, 180, 110, 255), outline=(120, 80, 40, 255), width=4)
    d.text((cx + 95, cy - 10), "食料", font=font(70), fill=(80, 40, 20, 255))
    E.mark_image(c, "※イメージ", (W - 230, 1440))
    return c, 650, YELLOW


def v_survey(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy, r = W / 2, 1230, 210
    k = min(1, t / 1.2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 110, 160, 255))
    d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 180 * k, fill=(255, 170, 90, 255))
    if k >= 1:
        d.text((cx + 40, cy - 40), "しない", font=font(52), fill=(40, 20, 10, 255))
        d.text((cx - 190, cy - 40), "する等", font=font(46), fill=WHITE + (255,))
    E.mark_image(c, "※割合はイメージ", (60, 1470))
    return c, 650, YELLOW


def v_cost(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    rng = random.Random(2)
    n = int(min(1, t / 2.0) * 26)
    for k in range(n):
        x = 140 + (k % 13) * 62 + rng.randint(-6, 6)
        y = 1380 - (k // 13) * 46
        d.rectangle([x, y, x + 54, y + 38], fill=(120, 190, 110, 255), outline=(40, 90, 40, 255), width=3)
        d.text((x + 14, y + 2), "$", font=font(30), fill=(30, 70, 30, 255))
    return c, 680, YELLOW


def v_countdown(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    n = max(0, 3 - int(t / 0.7))
    s = str(n) if n > 0 else "2000"
    f = font(260 if n > 0 else 220)
    if n == 0:
        glow(c, (W / 2, 1230), 200, (255, 214, 64), 160)
    d.text(((W - d.textlength(s, font=f)) / 2, 1080), s, font=f, fill=YELLOW + (255,), stroke_width=10, stroke_fill=(0, 0, 0, 255))
    return c, 760, YELLOW


def v_calm(c, t, p, gt, sc):
    screen(c, 240, 1050, 600, 300, "2000/01/01", GREEN, 80)
    return c, 760, CYAN


def v_minor(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    cx, cy = W / 2, 1230
    d.rounded_rectangle([cx - 330, cy - 170, cx + 330, cy + 170], radius=20, fill=(30, 34, 40, 255), outline=(150, 150, 160, 255), width=5)
    for k in range(4):
        y = cy - 120 + k * 70
        blink = k == 1 and int(t * 3) % 2 == 0
        d.ellipse([cx - 290, y, cx - 250, y + 40], fill=((255, 200, 60) if blink else (90, 200, 110)) + (255,))
        d.rectangle([cx - 220, y + 10, cx + 280, y + 30], fill=(80, 90, 100, 255))
    E.mark_image(c, "※表示盤のイメージ", (60, 1440))
    return c, 650, YELLOW


def v_answer(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    rng = random.Random(9)
    for k in range(int(min(1, t / 2) * 8)):
        x = 130 + (k % 4) * 220
        y = 1060 + (k // 4) * 180
        d.rounded_rectangle([x, y, x + 180, y + 140], radius=16, fill=(0, 0, 0, 160), outline=(120, 230, 120, 255), width=4)
        d.text((x + 55, y + 30), "OK", font=font(56), fill=(120, 230, 120, 255))
    return c, 650, CYAN


def v_leap(c, t, p, gt, sc):
    calendar(c, W / 2, 1230, "2000年2月", "29", (60, 90, 180), 0.8)
    return c, 720, YELLOW


def v_rule(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    rows = [("1900", "100で割り切れる → うるう年じゃない", (150, 200, 255)),
            ("2000", "400で割り切れる → うるう年！", YELLOW)]
    for i, (y4, txt, col) in enumerate(rows):
        if t < 0.4 + i * 1.6:
            continue
        y = 1060 + i * 190
        d.rounded_rectangle([80, y, 1000, y + 150], radius=20, fill=(0, 0, 0, 170), outline=col + (255,), width=5)
        d.text((110, y + 35), y4, font=font(70), fill=col + (255,))
        d.text((330, y + 50), txt, font=font(40), fill=WHITE + (255,))
    return c, 660, YELLOW


def v_atm(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    for k in range(3):
        x = 170 + k * 260
        d.rounded_rectangle([x, 1020, x + 220, 1400], radius=18, fill=(190, 195, 205, 255), outline=(80, 85, 95, 255), width=4)
        d.rectangle([x + 25, 1060, x + 195, 1180], fill=(20, 20, 25, 255))
        d.text((x + 50, 1095), "停止" if int(t * 2 + k) % 2 else "", font=font(48), fill=RED + (255,))
        d.rectangle([x + 40, 1220, x + 180, 1300], fill=(120, 125, 135, 255))
    E.mark_image(c, "※ATMのイメージ", (60, 1440))
    return c, 650, YELLOW


def v_question(c, t, p, gt, sc):
    options(c, t, [("覚えてる", (255, 214, 64)), ("知らない", (150, 200, 255))], y=1020)
    return c, 700, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, digits=v_digits, rollover=v_rollover, systems=v_systems, stock=v_stock,
               survey=v_survey, cost=v_cost, countdown=v_countdown, calm=v_calm, minor=v_minor, answer=v_answer,
               leap=v_leap, rule=v_rule, atm=v_atm, question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (8, 9, 12):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("pa1", 0.6), S[3] + 1.0)                      # 00
    add(se("emergency-alert1", 0.3), S[4])               # 止まるかも
    add(se("clock-tower-bell1", 0.5), S[8] + 2.0)        # 2000年
    last = sc[9]["lines"][-1]
    add(se("tin1", 0.8), S[9] + last["start"] + last["dur"] + 0.05)
    add(se("correct2", 0.6), S[11] + 0.05)               # 答え合わせ
    add(se("text-impact3", 0.7), S[12] + 0.05)           # 2/29
    add(se("kira1", 0.5), S[15] + 0.05)


def make_episode():
    return E.Episode("y2k2000", "外れた人類滅亡説 #3", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx,
                     speed=1.22, lead={9: 1.0}, calm_scenes=(9,), characters=True)


if __name__ == "__main__":
    E.main(make_episode)
