#!/usr/bin/env python3
"""UMA #2 ツチノコ【短い版・新しい型のテスト】

新しい型:
  - 0秒目から強い絵と動き+大きい立ち絵、つかみは短い2行、上のラベルは出さない
  - いきなり結論(賞金と正体)を言い、理由で引っ張る
  - 見せ場を絞って50〜60秒、話す速さ1.3
絵とイラストは tsuchinoko.py のものを再利用。

  python3 tiktok/tsuchinoko_short.py voice | preview | render
"""
import math

from PIL import Image, ImageDraw

import engine as E
from engine import CYAN, RED, W, YELLOW, M, Z, font
import tsuchinoko as T

SCENES = [
    dict(d=3.0, visual="hook", size=104, text=["[134万円]の懸賞金", "正体はトカゲ？"]),
    dict(d=4.5, visual="festa", size=72, text=["岐阜県東白川村", "毎年[つちのこフェスタ]", "賞金はいま134万円"]),
    dict(d=3.5, visual="unfound", size=80, text=["なのに", "[誰も捕まえていない]"]),
    dict(d=4.0, visual="oku", size=74, text=["1992年には", "[懸賞金2億円]の町も"]),
    dict(d=4.5, visual="birodo", size=72, text=["見つかった!?", "→ 正体は[ガの幼虫]"]),
    dict(d=5.5, visual="aojita", size=70, text=["＜有力説＞", "[アオジタトカゲ]の見間違い", "足が短く太いヘビに見える"]),
    dict(d=5.0, visual="nozuchi", size=70, text=["でも江戸時代の本にも", "[野槌蛇]として登場", "正体はまだ謎"]),
    dict(d=4.5, visual="question", size=76, text=["賞金134万円", "[探しに行く]？[行かない]？"]),
]

LINES = [
    [(Z, "見つけたら134万円！その正体は、トカゲかもしれないのだ！", "surprised+big+hold")],
    [(M, "岐阜県の東白川村では、平成元年から毎年、ツチノコ探しのお祭りを開いていて、賞金はいま134万円なの。")],
    [(Z, "でも、まだ誰も捕まえてないのだ……", "troubled")],
    [(M, "1992年には、兵庫県の千種町が、2億円の懸賞金を出したこともあるわ。"), (Z, "2億円なのだ！？")],
    [(M, "2022年に兵庫で見つかったツチノコっぽい生き物は、調べたらガの幼虫だったの。"), (Z, "イモムシなのだ！？")],
    [(M, "有力説は、外国から来たアオジタトカゲの見間違い。足が短いから、太いヘビに見えるかもしれないのよ。", "smug")],
    [(M, "ただ、江戸時代の百科事典にも、野槌蛇として載っているの。正体は、まだはっきりしていないわ。"), (Z, "ロマンなのだ！")],
    [(Z, "みんなは、探しに行くのだ？", "normal+small"), (M, "行く？行かない？コメントで聞かせなさい。")],
]


def v_hook(c, t, p, gt, sc):
    """0秒目から動く: ツチノコがズームで飛び込み、134万円のハンコ。"""
    T.forest(c, t)
    k = E.ease_out(min(1.0, t / 0.35))
    T.tsuchinoko(c, W / 2 + 230, 1300, 0.5 + 0.7 * k, t)
    if t > 0.35:
        q = min(1.0, (t - 0.35) / 0.15)
        lay = Image.new("RGBA", (560, 170), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([0, 0, 559, 169], radius=20, outline=(230, 30, 30, 255), width=12)
        f = font(110)
        ld.text(((560 - ld.textlength("134万円", font=f)) / 2, 12), "134万円", font=f, fill=(230, 30, 30, 255))
        lay = lay.rotate(-10, expand=True, resample=Image.BICUBIC)
        sc_ = 1.8 - 0.8 * q
        lay = lay.resize((int(lay.width * sc_), int(lay.height * sc_)))
        c.alpha_composite(lay, (int(W / 2 + 220 - lay.width / 2), int(1080 - lay.height / 2)))
    return c, 600, RED


def v_unfound(c, t, p, gt, sc):
    T.forest(c, t)
    d = ImageDraw.Draw(c)
    f = font(260)
    s = "0匹"
    d.text(((W - d.textlength(s, font=f)) / 2, 980), s, font=f, fill=YELLOW + (255,), stroke_width=10, stroke_fill=(0, 0, 0, 255))
    return c, 700, RED


VISUALS = dict(T.VISUALS)
VISUALS.update(hook=v_hook, unfound=v_unfound)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    add(se("text-impact3", 0.7), 0.4)                       # 134万円ハンコ
    for k in range(1, len(S)):
        if k not in (2, 5):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("tin1", 0.6), S[2] + 0.3)                        # 誰も捕まえていない
    add(se("pa1", 0.6), S[3] + 0.8)                         # 2億円
    add(se("correct2", 0.6), S[5] + 0.05)                   # 有力説
    add(se("kira1", 0.5), S[7] + 0.05)


def make_episode():
    return E.Episode("tsuchinoko_short", "UMA #2", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.3,
                     characters=True, endcard=True, hook_mode=True)


if __name__ == "__main__":
    E.main(make_episode)
