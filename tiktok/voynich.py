#!/usr/bin/env python3
"""未解決ミステリー #1「600年誰にも読めない本 ヴォイニッチ手稿」(短い型・立ち絵あり)

  python3 tiktok/voynich.py voice | preview | render

画像: イェール大学バイネキ稀覯本図書館 Beinecke MS 408(15世紀の写本=パブリックドメイン。
      Yale のオープンアクセス方針でパブリックドメイン作品の画像は利用自由)
      assets/images/voynich/*.jpg(git 管理外)
"""
import math
import os

from PIL import Image, ImageDraw

import engine as E
from engine import CYAN, RED, W, WHITE, YELLOW, M, Z, font

VDIR = os.path.join(E.IMAGES, "voynich")
CREDIT = "Beinecke MS 408, Yale University"
_cache = {}


def page(name, w, crop=None):
    key = (name, w, crop)
    if key not in _cache:
        im = Image.open(os.path.join(VDIR, name + ".jpg")).convert("RGB")
        if crop:
            iw, ih = im.size
            im = im.crop((int(crop[0] * iw), int(crop[1] * ih), int(crop[2] * iw), int(crop[3] * ih)))
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        _cache[key] = im
    return _cache[key]


def show(c, name, cx, cy, w, t, crop=None, zoom=0.06, pop=True, label=None):
    """写本のページを表示(登場ズーム+ゆっくり寄る)。左下にクレジット。"""
    k = E.ease_out(min(1.0, t / 0.35)) if pop else 1.0
    s = (0.8 + 0.2 * k) * (1 + zoom * min(1.0, t / 4.0))
    im = page(name, w, crop)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
    fr = Image.new("RGBA", (im.width + 16, im.height + 16), (20, 16, 12, 255))
    fr.paste(im, (8, 8))
    d = ImageDraw.Draw(fr)
    cf = font(22, black=False)
    txt = label or CREDIT
    tw = d.textlength(txt, font=cf)
    d.rectangle([8, fr.height - 8 - 34, 8 + tw + 18, fr.height - 8], fill=(0, 0, 0, 170))
    d.text((17, fr.height - 8 - 31), txt, font=cf, fill=(235, 235, 235, 255))
    c.alpha_composite(fr, (int(cx - fr.width / 2), int(cy - fr.height / 2)))
    return fr.size


SCENES = [
    dict(d=3.0, visual="hook", size=100, text=["[600年]", "誰にも読めない本"]),
    dict(d=4.5, visual="letters", size=72, text=["名前は[ヴォイニッチ手稿]", "見たことのない文字で", "びっしり"]),
    dict(d=4.5, visual="plants", size=72, text=["描かれた植物の多くは", "[何の植物か特定できない]"]),
    dict(d=4.5, visual="carbon", size=70, text=["炭素年代測定で", "羊皮紙は[1404〜1438年]ごろ"]),
    dict(d=5.0, visual="new2024", size=66, text=["＜新発見① 2024年＞", "特殊な光で撮影すると", "1ページ目に[隠れた文字]"]),
    dict(d=5.0, visual="new2025", size=66, text=["＜新発見② 2025年＞", "15世紀の[トランプとサイコロ]で", "そっくりな暗号文が作れた"]),
    dict(d=4.5, visual="new2026", size=66, text=["＜新発見③ 2026年＞", "ページが[バラバラの順番]で", "綴じられていた？"]),
    dict(d=4.0, visual="still", size=78, text=["それでも", "[まだ誰も読めていない]"]),
    dict(d=4.5, visual="question", size=76, text=["この本の正体は", "[暗号]？[デタラメ]？"]),
]

LINES = [
    [(Z, "600年間、誰にも読めない本があるのだ！", "surprised+big+hold")],
    [(M, "名前はヴォイニッチ手稿。約240ページが、見たことのない文字でびっしり書かれているの。")],
    [(M, "描かれた植物の多くは、どれが何の植物なのか、はっきり特定できないのよ。"), (Z, "謎すぎるのだ！")],
    [(M, "2009年の炭素年代測定で、羊皮紙は、1404年から1438年ごろのものとわかったわ。")],
    [(M, "ここから最新情報よ。2024年、特殊な光で撮影したら、1ページ目の余白に、消された文字が見つかったの。昔の持ち主が解読を試みた跡かもしれないわ。")],
    [(M, "2025年には、15世紀のトランプとサイコロを使う暗号で、この本そっくりの文章が作れる、という研究も出たの。"), (Z, "暗号の可能性があるのだ！")],
    [(M, "さらに2026年10月には、昔、製本したときに、ページの順番がバラバラになっていた可能性がある、という研究も発表されたわ。")],
    [(Z, "それでも、まだ誰も読めていないのだ……", "troubled")],
    [(Z, "みんなは、この本の正体、何だと思うのだ？", "normal+small"), (M, "暗号？デタラメ？コメントで聞かせなさい。")],
]


# ---------------------------------------------------------------- シーン
def v_hook(c, t, p, gt, sc):
    E.overlay(c, (30, 20, 10, 90))
    show(c, "13r", W / 2 + 170, 1250, 560, t, zoom=0.12)
    if t < 0.2:
        E.overlay(c, (255, 255, 255, int(255 * (1 - t / 0.2))))
    return c, 560, RED


def v_letters(c, t, p, gt, sc):
    # 文字部分を大きく(13r 上部)
    show(c, "13r", W / 2, 1150, 900, t, crop=(0.12, 0.06, 0.88, 0.30), zoom=0.08)
    return c, 640, YELLOW


def v_plants(c, t, p, gt, sc):
    show(c, "33v", W / 2 - 150, 1220, 480, t)
    if t > 0.6:
        show(c, "9v", W / 2 + 200, 1260, 420, t - 0.6)
    return c, 640, YELLOW


def v_carbon(c, t, p, gt, sc):
    show(c, "Front_cover", W / 2 - 160, 1250, 420, t, label="Beinecke MS 408（表紙）")
    d = ImageDraw.Draw(c)
    n = 1404 + int(34 * min(1.0, t / 2.0))
    f = font(84)
    d.text((620, 1080), "1404", font=f, fill=YELLOW + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    d.text((680, 1180), "〜", font=f, fill=WHITE + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    d.text((620, 1280), str(n), font=f, fill=YELLOW + (255,), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    return c, 640, YELLOW


def v_new2024(c, t, p, gt, sc):
    size = show(c, "1r", W / 2 - 60, 1250, 560, t)
    # 右の余白を光らせる(隠れた文字の位置のイメージ)
    if t > 1.0:
        a = int(110 + 60 * math.sin(t * 6))
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
        x0 = W / 2 - 60 + size[0] / 2 - 90
        ImageDraw.Draw(lay).rounded_rectangle([x0, 1250 - size[1] / 2 + 60, x0 + 70, 1250 - size[1] / 2 + 330],
                                              radius=12, outline=(120, 230, 255, 255), width=6, fill=(120, 230, 255, a // 3))
        c.alpha_composite(lay)
    return c, 620, CYAN


def v_new2025(c, t, p, gt, sc):
    show(c, "67r", W / 2, 1150, 820, t)
    d = ImageDraw.Draw(c)
    # トランプとサイコロ(イメージ)
    for i in range(3):
        x = 150 + i * 70
        d.rounded_rectangle([x, 1330, x + 120, 1500], radius=12, fill=(250, 250, 245, 255), outline=(60, 60, 60, 255), width=4)
        d.text((x + 30, 1380), "♠♥♦"[i], font=font(56), fill=((30, 30, 30) if i == 0 else (200, 30, 40)) + (255,))
    rot = t * 3
    cx, cy = 820, 1420
    pts = [(cx + 70 * math.cos(rot + k * math.pi / 2), cy + 70 * math.sin(rot + k * math.pi / 2)) for k in range(4)]
    d.polygon(pts, fill=(250, 250, 245, 255), outline=(60, 60, 60, 255))
    for k in (-1, 0, 1):
        d.ellipse([cx + k * 22 - 8, cy + k * 22 - 8, cx + k * 22 + 8, cy + k * 22 + 8], fill=(30, 30, 30, 255))
    E.mark_image(c, "※トランプ・サイコロはイメージ", (60, 1530))
    return c, 600, YELLOW


def v_new2026(c, t, p, gt, sc):
    # ページがシャッフルされるイメージ
    order = ["33v", "9v", "99r", "13r"]
    for i, name in enumerate(order):
        ph = t * 1.5 + i * 1.3
        x = W / 2 + 230 * math.sin(ph) * (0.4 + 0.6 * min(1.0, t / 1.5))
        y = 1230 + 40 * math.cos(ph * 1.3)
        im = page(name, 300)
        c.alpha_composite(im.convert("RGBA").rotate(8 * math.sin(ph), expand=True), (int(x - 160), int(y - 230)))
    E.mark_image(c, "Beinecke MS 408, Yale University ／ 並び替えはイメージ", (60, 1530))
    return c, 600, YELLOW


def v_still(c, t, p, gt, sc):
    E.overlay(c, (0, 0, 0, 80))
    show(c, "99r", W / 2, 1200, 520, t, zoom=0.03)
    return c, 700, RED


def v_question(c, t, p, gt, sc):
    d = ImageDraw.Draw(c)
    for i, (txt, col) in enumerate([("暗号", (255, 214, 64)), ("デタラメ", (150, 200, 255))]):
        x0 = 120 + i * 440
        bob = math.sin(t * 3 + i * 1.5) * 8
        d.rounded_rectangle([x0, 1020 + bob, x0 + 400, 1160 + bob], radius=30, fill=(0, 0, 0, 170), outline=col + (255,), width=6)
        f = font(60)
        d.text((x0 + (400 - d.textlength(txt, font=f)) / 2, 1048 + bob), txt, font=f, fill=col + (255,))
    return c, 700, YELLOW


VISUALS = dict(hook=v_hook, letters=v_letters, plants=v_plants, carbon=v_carbon, new2024=v_new2024,
               new2025=v_new2025, new2026=v_new2026, still=v_still, question=v_question)


def sfx(add, se, sc):
    S = [s["start"] for s in sc]
    add(se("text-impact1", 0.9), 0.0)
    for k in range(1, len(S)):
        if k not in (4, 7):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)
    add(se("kira1", 0.5), S[3] + 2.0)                       # 年代
    add(se("correct2", 0.6), S[4] + 0.05)                   # 新発見①
    add(se("kira1", 0.5), S[4] + 1.2)
    add(se("pa1", 0.6), S[5] + 0.1)                         # 新発見②
    add(se("pa1", 0.6), S[6] + 0.1)                         # 新発見③
    add(se("tin1", 0.6), S[7] + 0.4)                        # まだ読めない
    add(se("kira1", 0.5), S[8] + 0.05)


def make_episode():
    return E.Episode("voynich", "未解決ミステリー #1", [dict(s) for s in SCENES], LINES, VISUALS, sfx=sfx, speed=1.3,
                     characters=True, endcard=True, hook_mode=True,
                     credit_lines=["VOICEVOX:ずんだもん", "VOICEVOX:四国めたん", "立ち絵:坂本アヒル",
                                   "画像:Beinecke MS 408, Yale University"])


if __name__ == "__main__":
    E.main(make_episode)
