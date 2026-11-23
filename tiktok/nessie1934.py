#!/usr/bin/env python3
"""UMA #1「ネッシーの"外科医の写真"は60年後に自白されていた」

  python3 tiktok/nessie1934.py voice | preview | render

実際の写真を使う場合は tiktok/assets/images/surgeons_photo.jpg を置く(無ければイラストで代用)。
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, font
from wow1977 import glow

PHOTO = os.path.join(E.ASSETS, "images", "surgeons_photo.jpg")

SCENES = [
    dict(d=3.6, visual="hook", size=86, text=["ネッシーの一番有名な写真", "実は[60年後に自白]", "されていた"]),
    dict(d=3.0, visual="teaser", size=76, text=["最後に", "[最新のDNA調査]の結果も"]),
    dict(d=4.0, visual="lake", size=74, text=["スコットランドの[ネス湖]", "1933年ごろから", "目撃談が話題に"]),
    dict(d=3.5, visual="hunter", size=74, text=["新聞社が", "[猛獣ハンター]を派遣"]),
    dict(d=5.0, visual="hippo", size=70, text=["巨大な足跡を発見！", "→ 博物館の鑑定は", "[カバの足の剥製]"]),
    dict(d=3.0, visual="shame", size=80, text=["ハンターは", "[大恥]をかく"]),
    dict(d=4.5, visual="photo", size=70, text=["1934年", "ロンドンの医師が撮った", "[ネッシーの写真]が新聞に"]),
    dict(d=4.0, visual="doctor", size=72, text=["「外科医の写真」と", "呼ばれたが実は[婦人科医]"]),
    dict(d=3.5, visual="sixty", size=72, text=["それから[60年]", "ネッシーの代表的な証拠に"]),
    dict(d=4.5, visual="confess", size=72, text=["1994年", "ハンターの身内が", "[ニセモノ]と告白"]),
    dict(d=4.5, visual="model", size=70, text=["正体は", "おもちゃの潜水艦に首をつけた", "[35cmほどの模型]"]),
    dict(d=4.0, visual="revenge", size=72, text=["動機は", "カバの足事件の[仕返し]？"]),
    dict(d=5.0, visual="dna", size=68, text=["＜最新調査＞", "2018年 ネス湖の水を", "[DNA]で調べた"]),
    dict(d=5.0, visual="eel", size=68, text=["[は虫類のDNA]は見つからず", "あちこちで", "[ウナギのDNA]"]),
    dict(d=4.5, visual="size", size=72, text=["ただし", "[大きさまではわからない]"]),
    dict(d=5.5, visual="question", size=76, text=["あなたはどう思う？", "ネッシーは[いる]？[いない]？", "コメントで教えて"]),
]

LINES = [
    [(Z, "ネッシーの一番有名な写真、実は60年後に、ニセモノだと自白されていたのだ！")],
    [(M, "最後に、ネス湖の最新DNA調査の結果も、わたくしが教えてあげるわ。")],
    [(M, "舞台はスコットランドのネス湖。1933年ごろから、怪物の目撃談が話題になったの。")],
    [(M, "イギリスの新聞、デイリーメールは、猛獣ハンターのウェザレルを、ネス湖に送り込んだのよ。")],
    [(M, "彼は巨大な足跡を見つけたけど、博物館で調べたら、カバの足の剥製で付けた跡だったの。"), (Z, "カバなのだ！？")],
    [(M, "ウェザレルは、すっかり笑い者になってしまったわ。")],
    [(M, "そして1934年。ロンドンの医師ウィルソンが撮ったという、ネッシーの写真が新聞に載ったの。")],
    [(M, "外科医の写真と呼ばれたけど、実はウィルソンは、婦人科のお医者さんだったのよ。"), (Z, "そこから違うのだ！")],
    [(M, "この写真は、60年ものあいだ、ネッシーの代表的な証拠として扱われたの。")],
    [(M, "ところが1994年、ウェザレルの身内だったスパーリングが、あれはニセモノだったと告白したの。")],
    [(M, "正体は、おもちゃの潜水艦に首をつけた、35センチほどの模型だったと言われているわ。"), (Z, "ちっちゃいのだ！")],
    [(M, "動機は、カバの足事件で恥をかかされた、新聞社への仕返しだったとも言われているのよ。")],
    [(M, "約束の最新調査よ。2018年、研究チームがネス湖の水を250ほど採って、中のDNAを調べたの。")],
    [(M, "首長竜のような、は虫類のDNAは見つからず、そのかわり、ウナギのDNAがあちこちで見つかったの。"), (Z, "ネッシーはウナギなのだ！？")],
    [(M, "ただし、DNAだけでは大きさまではわからないから、巨大ウナギかどうかは、謎のままよ。")],
    [(Z, "みんなは、ネッシーはいると思うのだ？"), (M, "いる？いない？アンタたちの考え、コメントで聞かせなさい。")],
]


# ---------------------------------------------------------------- 部品
def lake(c, t, y=1450, hills=True):
    d = ImageDraw.Draw(c)
    if hills:
        d.polygon([(0, y), (0, y - 180), (180, y - 280), (380, y - 150), (560, y - 300), (800, y - 160), (W, y - 260), (W, y)],
                  fill=(25, 40, 45, 255))
    d.rectangle([0, y, W, 1920], fill=(20, 45, 70, 255))
    for k in range(10):
        yy = y + 30 + k * 40
        off = (t * 40 + k * 37) % 200
        for x in range(-200, W, 200):
            d.line([x + off, yy, x + off + 90, yy], fill=(70, 110, 140, 160), width=3)


def nessie_silhouette(c, cx, cy, s=1.0, t=0.0, col=(20, 25, 30, 255)):
    d = ImageDraw.Draw(c)
    bob = math.sin(t * 2) * 6
    d.ellipse([cx - 120 * s, cy - 40 * s + bob, cx + 60 * s, cy + 30 * s + bob], fill=col)
    d.line([cx + 30 * s, cy + bob, cx + 90 * s, cy - 200 * s + bob], fill=col, width=int(34 * s))
    d.ellipse([cx + 70 * s, cy - 240 * s + bob, cx + 150 * s, cy - 190 * s + bob], fill=col)


def surgeons_photo(c, cx, cy, w=760, t=0.0):
    """実写真があれば表示、無ければモノクロ風のイラスト。"""
    if os.path.exists(PHOTO):
        im = Image.open(PHOTO).convert("RGB")
        h = int(w * im.height / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        is_real = True
    else:
        h = int(w * 0.75)
        im = Image.new("RGB", (w, h), (150, 150, 145))
        d = ImageDraw.Draw(im)
        for k in range(0, h, 6):
            g = 140 + int(15 * math.sin(k * 0.3))
            d.line([0, k, w, k], fill=(g, g, g - 5))
        tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        nessie_silhouette(tmp, w * 0.45, h * 0.72, 1.3, 0, (35, 35, 35, 255))
        im.paste(tmp, (0, 0), tmp)
        im = im.filter(ImageFilter.GaussianBlur(1.2))
        is_real = False
    fr = Image.new("RGBA", (w + 24, h + 24), (240, 240, 235, 255))
    fr.paste(im, (12, 12))
    c.alpha_composite(fr, (int(cx - fr.width / 2), int(cy - fr.height / 2)))
    cap = "1934年に新聞に載った写真（のちに捏造と判明）" if is_real else "※写真のイメージ"
    d = ImageDraw.Draw(c)
    f = font(34, black=False)
    d.text(((W - d.textlength(cap, font=f)) / 2, cy + fr.height / 2 + 14), cap, font=f, fill=(225, 225, 235, 255),
           stroke_width=2, stroke_fill=(0, 0, 0, 255))


def newspaper(c, cx, cy, title, t=0.0, rot=-4):
    lay = Image.new("RGBA", (700, 520), (238, 230, 205, 255))
    d = ImageDraw.Draw(lay)
    d.rectangle([0, 0, 699, 519], outline=(80, 70, 50, 255), width=6)
    f = font(54)
    d.text(((700 - d.textlength(title, font=f)) / 2, 26), title, font=f, fill=(25, 20, 15, 255))
    d.line([30, 110, 670, 110], fill=(40, 30, 20, 255), width=5)
    rng = random.Random(2)
    for row in range(10):
        for col in range(3):
            x0 = 30 + col * 220
            d.line([x0, 145 + row * 34, x0 + rng.randint(120, 195), 145 + row * 34], fill=(110, 100, 80, 255), width=11)
    d.text((30, 476), "※イメージ", font=font(28, black=False), fill=(90, 80, 60, 255))
    lay = lay.rotate(rot + math.sin(t * 2), expand=True, resample=Image.BICUBIC)
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
    surgeons_photo(c, W / 2, 1300, 720, t)
    d = ImageDraw.Draw(c)
    if t > 0.6:
        k = min(1, (t - 0.6) / 0.2)
        lay = Image.new("RGBA", (420, 140), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([0, 0, 419, 139], radius=16, outline=(230, 30, 30, 255), width=10)
        f = font(90)
        ld.text(((420 - ld.textlength("ニセモノ", font=f)) / 2, 10), "ニセモノ", font=f, fill=(230, 30, 30, 255))
        lay = lay.rotate(-12, expand=True, resample=Image.BICUBIC).resize((int(lay.width * (2 - k)), int(lay.height * (2 - k))))
        c.alpha_composite(lay, (int(W / 2 - lay.width / 2), int(1300 - lay.height / 2)))
    if t < 0.25:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.25))))
    return c, 720, RED


def v_teaser(c, t, p, gt, sc):
    lake(c, t)
    return c, 780, YELLOW


def v_lake(c, t, p, gt, sc):
    lake(c, t)
    if 1.2 < t:
        nessie_silhouette(c, 600, 1470, 0.8, t)
        d = ImageDraw.Draw(c)
        d.text((660, 1150), "？", font=font(120), fill=YELLOW + (255,), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※イメージ", (W - 230, 1700))
    return c, 700, YELLOW


def v_hunter(c, t, p, gt, sc):
    newspaper(c, W / 2, 1300, "ネス湖に猛獣ハンター", t)
    return c, 720, YELLOW


def v_hippo(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    lake(c, t, y=1700, hills=False)
    cx, cy = W / 2, 1300
    # 足跡(4本指の丸い跡)
    d.ellipse([cx - 150, cy - 110, cx + 150, cy + 150], fill=(90, 70, 50, 255))
    for k in range(4):
        a = math.pi * (1.15 + k * 0.23)
        x, y = cx + 170 * math.cos(a), cy - 40 + 150 * math.sin(a)
        d.ellipse([x - 45, y - 40, x + 45, y + 40], fill=(90, 70, 50, 255))
    if t > 2.0:
        k = min(1, (t - 2.0) / 0.3)
        f = font(int(110 * k) + 1)
        s = "カバ!?"
        d.text((cx - d.textlength(s, font=f) / 2, cy + 180), s, font=f, fill=RED + (255,), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※イメージ", (60, 1720))
    return c, 650, YELLOW


def v_shame(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    rng = random.Random(4)
    for k in range(12):
        x = rng.randint(80, W - 200)
        y = rng.randint(1050, 1650)
        f = font(rng.randint(50, 90))
        d.text((x + math.sin(t * 6 + k) * 6, y), "笑", font=f, fill=(255, 214, 64, 200), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    return c, 760, RED


def v_photo(c, t, p, gt, sc):
    s = 0.9 + 0.1 * E.ease_out(min(1, t / 0.6))
    surgeons_photo(c, W / 2, 1290, int(760 * s), t)
    return c, 660, YELLOW


def v_doctor(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    for i, (txt, col, strike) in enumerate([("外科医", (180, 180, 190), True), ("婦人科医", (255, 214, 64), False)]):
        x0 = 120 + i * 440
        if i == 1 and t < 1.6:
            continue
        d.rounded_rectangle([x0, 1200, x0 + 400, 1360], radius=26, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(66)
        tw = d.textlength(txt, font=f)
        d.text((x0 + (400 - tw) / 2, 1238), txt, font=f, fill=col + (255,))
        if strike and t > 1.0:
            d.line([x0 + 40, 1280, x0 + 360, 1280], fill=RED + (255,), width=12)
    return c, 720, YELLOW


def v_sixty(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    yr = 1934 + int(60 * min(1, t / 2.5))
    f = font(200)
    s = f"{yr}"
    d.text(((W - d.textlength(s, font=f)) / 2, 1150), s, font=f, fill=YELLOW + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return c, 720, YELLOW


def v_confess(c, t, p, gt, sc):
    newspaper(c, W / 2, 1310, "ネッシー写真は捏造", t, rot=3)
    return c, 680, RED


def v_model(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    lake(c, t, y=1500, hills=False)
    cx, cy = W / 2, 1460
    # おもちゃの潜水艦+首(模型)
    d.rounded_rectangle([cx - 230, cy - 50, cx + 170, cy + 30], radius=40, fill=(70, 70, 75, 255), outline=(30, 30, 35, 255), width=4)
    d.rectangle([cx - 40, cy - 100, cx + 30, cy - 50], fill=(70, 70, 75, 255))
    d.line([cx + 110, cy - 30, cx + 170, cy - 260], fill=(40, 35, 30, 255), width=32)
    d.ellipse([cx + 150, cy - 300, cx + 230, cy - 245], fill=(40, 35, 30, 255))
    # 定規
    if t > 1.5:
        d.rectangle([cx - 240, cy + 70, cx + 240, cy + 120], fill=(250, 230, 120, 255), outline=(120, 100, 40, 255), width=3)
        for k in range(0, 481, 24):
            d.line([cx - 240 + k, cy + 70, cx - 240 + k, cy + 70 + (30 if k % 120 == 0 else 15)], fill=(60, 50, 20, 255), width=3)
        s = "約35cm"
        f = font(60)
        d.text((cx - d.textlength(s, font=f) / 2, cy + 140), s, font=f, fill=YELLOW + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※模型のイメージ", (60, 1780))
    return c, 650, YELLOW


def v_revenge(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    newspaper(c, W / 2 + 160, 1340, "デイリー・メール", t, rot=6)
    s = 1 + 0.08 * math.sin(t * 6)
    f = font(int(170 * s))
    d.text((120, 1150), "怒", font=f, fill=RED + (255,), stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return c, 700, RED


def helix(c, cx, cy, t, h=560, col1=(120, 200, 255), col2=(255, 140, 180)):
    d = ImageDraw.Draw(c)
    for k in range(28):
        y = cy - h / 2 + k * h / 27
        a = k * 0.5 + t * 2
        x1, x2 = cx + 130 * math.sin(a), cx - 130 * math.sin(a)
        d.line([x1, y, x2, y], fill=(200, 200, 220, 150), width=4)
        d.ellipse([x1 - 12, y - 12, x1 + 12, y + 12], fill=col1 + (255,))
        d.ellipse([x2 - 12, y - 12, x2 + 12, y + 12], fill=col2 + (255,))


def v_dna(c, t, p, gt, sc):
    lake(c, t, y=1640, hills=False)
    helix(c, W / 2, 1290, t, h=500)
    return c, 640, CYAN


def eel(c, cx, cy, t, L=700):
    d = ImageDraw.Draw(c)
    pts = []
    for k in range(40):
        x = cx - L / 2 + k * L / 39
        y = cy + 40 * math.sin(k * 0.35 - t * 4)
        pts.append((x, y))
    for k in range(len(pts) - 1):
        w = int(14 + 26 * math.sin(math.pi * k / 39))
        d.line([pts[k], pts[k + 1]], fill=(90, 100, 60, 255), width=w)
    hx, hy = pts[-1]
    d.ellipse([hx - 30, hy - 26, hx + 34, hy + 26], fill=(90, 100, 60, 255))
    d.ellipse([hx + 8, hy - 12, hx + 20, hy], fill=(250, 250, 250, 255))


def v_eel(c, t, p, gt, sc):
    lake(c, t, y=1150, hills=False)
    d = ImageDraw.Draw(c)
    d.text((120, 1230), "は虫類", font=font(60), fill=WHITE + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    d.text((340, 1225), "×", font=font(80), fill=RED + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    if t > 1.5:
        eel(c, W / 2, 1520, t)
        d.text((620, 1230), "ウナギ", font=font(60), fill=YELLOW + (255,), stroke_width=4, stroke_fill=(0, 0, 0, 255))
        d.text((840, 1225), "○", font=font(80), fill=(120, 230, 120, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    E.mark_image(c, "※イメージ", (W - 230, 1760))
    return c, 650, YELLOW


def v_size(c, t, p, gt, sc):
    lake(c, t, y=1150, hills=False)
    eel(c, W / 2 - 150, 1400, t, L=300)
    s = 1 + 0.6 * (0.5 + 0.5 * math.sin(t * 2))
    eel(c, W / 2 + 60, 1620, t, L=int(300 * s))
    d = ImageDraw.Draw(c)
    d.text((W - 260, 1260), "？", font=font(160), fill=YELLOW + (255,), stroke_width=6, stroke_fill=(0, 0, 0, 255))
    return c, 720, YELLOW


def v_question(c, t, p, gt, sc):
    lake(c, t)
    options(c, t, [("いる", (120, 230, 120)), ("いない", (150, 200, 255))], y=1160)
    return c, 720, YELLOW


VISUALS = dict(hook=v_hook, teaser=v_teaser, lake=v_lake, hunter=v_hunter, hippo=v_hippo, shame=v_shame,
               photo=v_photo, doctor=v_doctor, sixty=v_sixty, confess=v_confess, model=v_model, revenge=v_revenge,
               dna=v_dna, eel=v_eel, size=v_size, question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (5, 9, 12):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("tin1", 0.6), S[4] + 2.0)                     # カバの足
    add(se("text-impact3", 0.6), S[9] + 0.05)            # 告白
    add(se("pa1", 0.6), S[10] + 1.5)                     # 35cm
    add(se("correct2", 0.6), S[12] + 0.05)               # 最新調査
    add(se("kira1", 0.5), S[13] + 1.5)                   # ウナギ
    add(se("kira1", 0.5), S[15] + 0.05)                  # 質問


def make_episode():
    return E.Episode("nessie1934", "UMA #1", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.22)


if __name__ == "__main__":
    E.main(make_episode)
