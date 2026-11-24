#!/usr/bin/env python3
"""UMA #2「捕まえたら賞金が出る日本のUMA ツチノコ」(立ち絵あり)

  python3 tiktok/tsuchinoko.py voice | preview | render

資料画像(あれば使う / 無ければイラスト):
  assets/images/tsuchinoko_nozuchi.png   和漢三才図会「野槌蛇」の挿絵
  assets/images/tsuchinoko_birodo.jpg    ビロードスズメの幼虫
  assets/images/tsuchinoko_aojita.jpg    アオジタトカゲ
"""
import math
import random

from PIL import ImageDraw

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, font
from wow1977 import glow

SCENES = [
    dict(d=3.6, visual="hook", size=84, text=["捕まえたら[賞金]が出る", "日本のUMA"]),
    dict(d=3.0, visual="teaser", size=76, text=["最後に", "[正体の有力説]も紹介"]),
    dict(d=4.5, visual="what", size=72, text=["その名は[ツチノコ]", "ビール瓶のような太い胴", "細いしっぽ"]),
    dict(d=5.0, visual="nozuchi", size=66, text=["江戸時代の百科事典", "『和漢三才図会』にも", "[野槌蛇]として登場"]),
    dict(d=4.0, visual="boom", size=74, text=["1970年代", "[ツチノコブーム]到来"]),
    dict(d=4.0, visual="search", size=72, text=["各地で", "[懸賞金つき]の捜索が始まる"]),
    dict(d=4.5, visual="oku", size=70, text=["1992年 兵庫県千種町（当時）", "懸賞金なんと[2億円]"]),
    dict(d=4.5, visual="festa", size=68, text=["岐阜県東白川村は", "平成元年から毎年", "[つちのこフェスタ]"]),
    dict(d=5.0, visual="prize", size=68, text=["賞金は100万円スタート", "見つからないと[毎年1万円]アップ", "2026年は134万円"]),
    dict(d=5.0, visual="birodo", size=68, text=["2022年 兵庫で発見!?", "→ 正体は", "[ガの幼虫]だった"]),
    dict(d=5.5, visual="aojita", size=66, text=["＜正体の有力説＞", "外国のトカゲ", "[アオジタトカゲ]の見間違い？"]),
    dict(d=4.5, visual="legs", size=70, text=["短い足が見えにくく", "[太いヘビ]に見えるとも"]),
    dict(d=4.5, visual="unknown", size=72, text=["ただし", "[決定的な証拠]はまだない"]),
    dict(d=5.5, visual="question", size=74, text=["賞金134万円", "[探しに行く]？[行かない]？", "コメントで教えて"]),
]

LINES = [
    [(Z, "捕まえたら賞金がもらえる、日本のユーマがいるのだ！")],
    [(M, "最後に、正体の有力説も、わたくしが教えてあげるわ。")],
    [(M, "その名はツチノコ。ビール瓶みたいに太い胴に、細いしっぽのヘビ、と言われているわ。")],
    [(M, "実は江戸時代の百科事典、和漢三才図会にも、野槌蛇という名前で、絵入りで紹介されているの。"), (Z, "江戸時代からいたのだ！？")],
    [(M, "1970年代には、オカルトブームとともに、空前の、ツチノコの人気が巻き起こったのよ。")],
    [(M, "そして各地で、懸賞金つきのツチノコ探しが始まったの。")],
    [(M, "1992年には、兵庫県の千種町が、なんと2億円の懸賞金を打ち出したのよ。"), (Z, "2億円なのだ！？")],
    [(M, "岐阜県の東白川村では、平成元年から毎年、ツチノコ探しのお祭り、ツチノコ、フェスタを開いているの。")],
    [(M, "賞金は100万円から始まって、見つからないたびに毎年1万円ずつ増えて、2026年は134万円よ。"), (Z, "まだ誰も見つけてないのだ……", "troubled")],
    [(M, "2022年には、兵庫県でツチノコっぽい生き物が見つかったけど、専門家が調べたら、ビロードスズメというガの幼虫だったの。"), (Z, "イモムシなのだ！？")],
    [(M, "約束の有力説よ。ヘビの研究所の専門家は、外国から入ってきたアオジタトカゲを、見間違えた可能性を挙げているわ。")],
    [(M, "アオジタトカゲは足が短くて見えにくいから、太いヘビに見えるかもしれない、とも言われているのよ。")],
    [(M, "ただし、決定的な証拠はまだないから、ツチノコの正体は、はっきりしていないの。")],
    [(Z, "みんなは、ツチノコを探しに行くのだ？", "normal+small"), (M, "行く？行かない？アンタたちの答え、コメントで聞かせなさい。")],
]


# ---------------------------------------------------------------- 部品(立ち絵が下に出るので絵は 980〜1450 付近)
def tsuchinoko(c, cx, cy, s=1.0, t=0.0, col=(120, 100, 70)):
    """ツチノコのイラスト(イメージ)。"""
    d = ImageDraw.Draw(c)
    bob = math.sin(t * 3) * 6
    d.ellipse([cx - 190 * s, cy - 70 * s + bob, cx + 150 * s, cy + 70 * s + bob], fill=col + (255,), outline=(60, 45, 30, 255), width=5)
    d.line([cx - 180 * s, cy + bob, cx - 300 * s, cy + 30 * s + bob], fill=col + (255,), width=int(26 * s))
    d.ellipse([cx + 110 * s, cy - 55 * s + bob, cx + 230 * s, cy + 45 * s + bob], fill=col + (255,), outline=(60, 45, 30, 255), width=5)
    d.ellipse([cx + 180 * s, cy - 30 * s + bob, cx + 200 * s, cy - 10 * s + bob], fill=(20, 20, 20, 255))
    for k in range(5):
        x = cx - 130 * s + k * 60 * s
        d.arc([x - 25 * s, cy - 40 * s + bob, x + 25 * s, cy + 40 * s + bob], 270, 90, fill=(90, 70, 45, 255), width=4)


def money(c, text, cy=1180, size=170, col=YELLOW):
    d = ImageDraw.Draw(c)
    f = font(size)
    d.text(((W - d.textlength(text, font=f)) / 2, cy), text, font=f, fill=col + (255,), stroke_width=9, stroke_fill=(0, 0, 0, 255))


def forest(c, t, y=1450):
    d = ImageDraw.Draw(c)
    d.rectangle([0, y, W, 1920], fill=(20, 45, 25, 255))
    rng = random.Random(4)
    for k in range(9):
        x = rng.randint(0, W)
        h = rng.randint(250, 450)
        d.polygon([(x, y - h), (x - 90, y), (x + 90, y)], fill=(25, 60, 35, 255))


def options(c, t, items, y=1020):
    d = ImageDraw.Draw(c)
    for i, (txt, col) in enumerate(items):
        x0 = 120 + i * 440
        bob = math.sin(t * 3 + i * 1.5) * 8
        d.rounded_rectangle([x0, y + bob, x0 + 400, y + 140 + bob], radius=30, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(56)
        d.text((x0 + (400 - d.textlength(txt, font=f)) / 2, y + 32 + bob), txt, font=f, fill=col + (255,))


# ---------------------------------------------------------------- シーン
def v_hook(c, t, p, gt, sc):
    forest(c, t)
    tsuchinoko(c, W / 2, 1300, 1.1, t)
    money(c, "￥", 960, 200)
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    E.mark_image(c, "※イメージ", (W - 230, 1470))
    return c, 720, RED


def v_teaser(c, t, p, gt, sc):
    forest(c, t)
    d = ImageDraw.Draw(c)
    f = font(300)
    d.text(((W - d.textlength("？", font=f)) / 2, 1000), "？", font=f, fill=YELLOW + (220,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return c, 760, YELLOW


def v_what(c, t, p, gt, sc):
    forest(c, t)
    tsuchinoko(c, W / 2, 1250, 1.2, t)
    E.mark_image(c, "※イメージ", (W - 230, 1470))
    return c, 680, YELLOW


def v_nozuchi(c, t, p, gt, sc):
    def fb(cv):
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([200, 980, 880, 1450], radius=10, fill=(236, 222, 186, 255), outline=(140, 110, 70, 255), width=6)
        tsuchinoko(cv, 560, 1220, 0.9, 0, (90, 80, 70))
        d.text((240, 1000), "野槌蛇", font=font(56), fill=(60, 40, 20, 255))
        E.mark_image(cv, "※挿絵のイメージ", (60, 1470))
    E.image_slot(c, "tsuchinoko_nozuchi.png", W / 2 - 110, 1190, 820, 720, "『和漢三才図会』野槌蛇（出典：国立国会図書館）", fb, t)
    return c, 660, YELLOW


def v_boom(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    rng = random.Random(3)
    for k in range(int(min(1, t / 2) * 10)):
        x, y = rng.randint(120, 860), rng.randint(980, 1380)
        d.rounded_rectangle([x, y, x + 200, y + 90], radius=14, fill=(0, 0, 0, 160), outline=(255, 214, 64, 255), width=4)
        d.text((x + 22, y + 18), "ツチノコ!?", font=font(40), fill=WHITE + (255,))
    return c, 720, YELLOW


def v_search(c, t, p, gt, sc):
    forest(c, t)
    d = ImageDraw.Draw(c)
    for k in range(4):
        x = 160 + k * 230 + math.sin(t * 2 + k) * 20
        d.ellipse([x - 30, 1300, x + 30, 1360], fill=(240, 200, 160, 255))
        d.rectangle([x - 35, 1360, x + 35, 1450], fill=(60, 90, 160, 255))
        d.line([x + 30, 1380, x + 90, 1330], fill=(200, 200, 200, 255), width=8)
        d.ellipse([x + 80, 1310, x + 120, 1350], outline=(200, 200, 200, 255), width=6)
    E.mark_image(c, "※イメージ", (W - 230, 1470))
    return c, 700, YELLOW


def v_oku(c, t, p, gt, sc):
    k = E.ease_out(min(1, max(0, (t - 0.8) / 0.4)))
    if k > 0:
        money(c, "2億円", 1080, int(230 * (0.6 + 0.4 * k)))
    return c, 680, YELLOW


def v_festa(c, t, p, gt, sc):
    forest(c, t)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([190, 1000, 890, 1180], radius=20, fill=(200, 60, 50, 255), outline=(255, 255, 255, 255), width=6)
    s = "つちのこフェスタ"
    f = font(72)
    d.text(((W - d.textlength(s, font=f)) / 2, 1040), s, font=f, fill=WHITE + (255,))
    tsuchinoko(c, W / 2, 1330, 0.7, t)
    E.mark_image(c, "※イメージ", (W - 230, 1470))
    return c, 660, YELLOW


def v_prize(c, t, p, gt, sc):
    v = 100 + int(34 * min(1, t / 3.0))
    money(c, f"{v}万円", 1080, 190)
    d = ImageDraw.Draw(c)
    f = font(48)
    s = "（2026年）" if v >= 134 else ""
    d.text(((W - d.textlength(s, font=f)) / 2, 1330), s, font=f, fill=WHITE + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return c, 650, YELLOW


def caterpillar(cv):
    d = ImageDraw.Draw(cv)
    cx, cy = W / 2, 1230
    for k in range(7):
        x = cx - 240 + k * 75
        r = 60 + 15 * math.sin(k / 6 * math.pi)
        d.ellipse([x - r, cy - r, x + r, cy + r], fill=(110, 140, 70, 255), outline=(60, 80, 40, 255), width=4)
    d.ellipse([cx + 200, cy - 70, cx + 300, cy + 20], fill=(110, 140, 70, 255), outline=(60, 80, 40, 255), width=4)
    d.ellipse([cx + 245, cy - 45, cx + 265, cy - 25], fill=(20, 20, 20, 255))
    E.mark_image(cv, "※イメージ", (W - 230, 1470))


def v_birodo(c, t, p, gt, sc):
    E.image_slot(c, "tsuchinoko_birodo.jpg", W / 2, 1160, 880, 470, "ビロードスズメの幼虫", caterpillar, t,
                 credit="※AI生成イメージ")
    return c, 650, YELLOW


def skink(cv, t=0.0):
    d = ImageDraw.Draw(cv)
    cx, cy = W / 2, 1230
    d.ellipse([cx - 260, cy - 70, cx + 160, cy + 70], fill=(170, 150, 110, 255), outline=(80, 70, 50, 255), width=5)
    for k in range(6):
        x = cx - 220 + k * 70
        d.line([x, cy - 60, x + 20, cy + 60], fill=(110, 90, 60, 255), width=10)
    d.ellipse([cx + 120, cy - 55, cx + 260, cy + 45], fill=(170, 150, 110, 255), outline=(80, 70, 50, 255), width=5)
    d.polygon([(cx - 250, cy), (cx - 380, cy + 25), (cx - 250, cy + 30)], fill=(170, 150, 110, 255))
    for lx in (cx - 170, cx + 70):
        d.rectangle([lx, cy + 55, lx + 26, cy + 95], fill=(150, 130, 95, 255))
    tongue = int(t * 2) % 2 == 0
    if tongue:
        d.polygon([(cx + 255, cy), (cx + 330, cy - 12), (cx + 330, cy + 12)], fill=(60, 90, 220, 255))
    E.mark_image(cv, "※イメージ", (W - 230, 1470))


def v_aojita(c, t, p, gt, sc):
    E.image_slot(c, "tsuchinoko_aojita.jpg", W / 2, 1160, 880, 470, "アオジタトカゲ", lambda cv: skink(cv, t), t,
                 credit="Photo: Michael Gäbler / CC BY-SA 3.0（トリミング）")
    return c, 650, CYAN


def v_legs(c, t, p, gt, sc):
    skink(c, t)
    d = ImageDraw.Draw(c)
    if t > 1.0:
        for lx in (W / 2 - 157, W / 2 + 83):
            d.ellipse([lx - 45, 1270, lx + 45, 1350], outline=RED + (255,), width=6)
    return c, 680, YELLOW


def v_unknown(c, t, p, gt, sc):
    forest(c, t)
    d = ImageDraw.Draw(c)
    f = font(300)
    d.text(((W - d.textlength("？", font=f)) / 2, 1000), "？", font=f, fill=YELLOW + (220,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return c, 720, YELLOW


def v_question(c, t, p, gt, sc):
    forest(c, t)
    options(c, t, [("探しに行く", (255, 214, 64)), ("行かない", (150, 200, 255))])
    return c, 700, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, what=v_what, nozuchi=v_nozuchi, boom=v_boom, search=v_search, oku=v_oku,
               festa=v_festa, prize=v_prize, birodo=v_birodo, aojita=v_aojita, legs=v_legs, unknown=v_unknown,
               question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (6, 10):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("text-impact3", 0.7), S[6] + 0.8)               # 2億円
    add(se("kira1", 0.5), S[8] + 3.0)                      # 134万円
    add(se("tin1", 0.6), S[9] + sc[9]["lines"][0]["dur"] - 1.0)  # ガの幼虫
    add(se("correct2", 0.6), S[10] + 0.05)                 # 有力説
    add(se("kira1", 0.5), S[13] + 0.05)


def make_episode():
    return E.Episode("tsuchinoko", "UMA #2", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.22,
                     characters=True, endcard=True)


if __name__ == "__main__":
    E.main(make_episode)
