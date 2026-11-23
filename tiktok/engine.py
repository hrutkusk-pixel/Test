"""TikTok 縦型動画の共通エンジン(描画・字幕・音声合成・ミックス・書き出し)。

各エピソードのスクリプト(例: wow1977.py)が SCENES / LINES / VISUALS / 効果音の配置 を定義し、
engine.main(ep) を呼ぶ。

  python3 tiktok/<episode>.py voice    # VOICEVOX でセリフ生成 + BGM/効果音ミックス + タイミング表
  python3 tiktok/<episode>.py preview  # 各シーンの静止画
  python3 tiktok/<episode>.py render   # MP4 書き出し(並列)
"""
import io
import json
import math
import os
import random
import subprocess
import sys
import urllib.parse
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FONT_BLACK = os.path.join(HERE, "fonts", "NotoSansJP_900Black.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "NotoSansJP_700Bold.ttf")
OUTDIR = os.path.join(HERE, "output")
ASSETS = os.path.join(HERE, "assets")

YELLOW = (255, 214, 64)
RED = (255, 70, 70)
WHITE = (255, 255, 255)
CYAN = (120, 230, 255)

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
    return center_y - total / 2  # 字幕ブロックの上端


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


def overlay(canvas, rgba):
    canvas.alpha_composite(Image.new("RGBA", (W, H), rgba))


def mark_image(canvas, text="※イメージ", xy=(60, 1640)):
    d = ImageDraw.Draw(canvas)
    d.text(xy, text, font=font(32, black=False), fill=(220, 220, 230, 220), stroke_width=2, stroke_fill=(0, 0, 0, 200))


# ---------------------------------------------------------------- エピソード定義
class Episode:
    """1本の動画の設定。

    scenes : [dict(d=最低秒数, visual=名前, size=字幕サイズ, text=[行...])]
    lines  : シーンごとのセリフ [[(話者ID, 文), ...], ...]
    visuals: {visual名: fn(canvas, t, p, gt, sc) -> (canvas, text_y, hl_color)}
    sfx    : fn(add, se, scenes) 効果音の配置
    """

    def __init__(self, name, series_label, scenes, lines, visuals, sfx=None,
                 bgm="kimyou_na_annainin_MATSU.mp3", lead=None, calm_scenes=(), credit_lines=None, speed=1.15):
        self.name = name
        self.series_label = series_label
        self.scenes = scenes
        self.lines = lines
        self.visuals = visuals
        self.sfx = sfx
        self.bgm = os.path.join(ASSETS, "bgm", bgm) if bgm else None
        self.lead = lead or {}
        self.speed = speed
        self.calm_scenes = set(calm_scenes)   # BGM を止めて静寂を作るシーン
        self.credit_lines = credit_lines or ["VOICEVOX:ずんだもん", "VOICEVOX:四国めたん"]
        self.out_mp4 = os.path.join(OUTDIR, f"{name}.mp4")
        self.out_wav = os.path.join(OUTDIR, f"{name}_audio.wav")
        self.out_json = os.path.join(OUTDIR, f"{name}_timing.json")
        assert len(scenes) == len(lines)
        for s in scenes:
            s.setdefault("min_d", s["d"])  # 絵を見せる最低尺(音声が短くてもこれ以上)
        self.voiced = os.path.exists(self.out_json) and os.path.exists(self.out_wav)
        if self.voiced:
            tm = json.load(open(self.out_json))
            assert len(tm["scenes"]) == len(scenes), "台本が変わったので voice をやり直してください"
            for s, t in zip(scenes, tm["scenes"]):
                s["d"] = t["d"]
                s["lines"] = t["lines"]
        self.total = sum(s["d"] for s in scenes)
        self.n_frames = int(round(self.total * FPS))

    def timeline(self):
        t0 = 0.0
        for i, s in enumerate(self.scenes):
            yield i, s, t0
            t0 += s["d"]

    def scene_at(self, gt):
        last = None
        for i, s, t0 in self.timeline():
            last = (i, s, t0)
            if gt < t0 + s["d"]:
                return last
        return last


# ---------------------------------------------------------------- フレーム合成
SPEAKER_COLOR = {"ずんだもん": (120, 205, 80), "四国めたん": (240, 110, 170)}
_VIGNETTE = None


def speaker_badge(canvas, sc, t, text_top):
    for ln in sc.get("lines", []):
        if ln["start"] - 0.05 <= t <= ln["start"] + ln["dur"] + 0.1:
            name = ln["speaker"]
            d = ImageDraw.Draw(canvas)
            f = font(44)
            w = d.textlength(name, font=f)
            x, y = (W - w) / 2, max(378, text_top - 100)
            d.rounded_rectangle([x - 34, y - 8, x + w + 34, y + 62], radius=36, fill=SPEAKER_COLOR[name] + (235,))
            d.text((x, y - 4), name, font=f, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(30, 30, 30, 255))
            return


def credit(canvas, ep, si, t):
    if not ep.voiced or si != len(ep.scenes) - 1:
        return
    a = min(1.0, t / 0.5)
    d = ImageDraw.Draw(canvas)
    f = font(36, black=False)
    y = 1200
    for s in ep.credit_lines:
        w = d.textlength(s, font=f)
        d.text(((W - w) / 2, y), s, font=f, fill=(235, 235, 245, int(235 * a)),
               stroke_width=3, stroke_fill=(0, 0, 0, int(220 * a)))
        y += 52


def render_frame(ep, si, sc, t, gt):
    global _VIGNETTE
    p = t / sc["d"]
    canvas = bg_stars(gt)
    canvas, text_y, hl = ep.visuals[sc["visual"]](canvas, t, p, gt, sc)
    if _VIGNETTE is None:
        _VIGNETTE = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        vignette(_VIGNETTE, 0.55)
    canvas.alpha_composite(_VIGNETTE)
    label(canvas, ep.series_label)
    credit(canvas, ep, si, t)
    lines = sc["text"]
    reveal = sc.get("reveal")  # 例: (1, 1.5) → 1.5秒までは先頭1行だけ
    if reveal and t < reveal[1]:
        lines = lines[:reveal[0]]
    appear = 1.0 if reveal else min(1.0, t / 0.45)
    top = draw_text_block(canvas, lines, sc["size"], text_y, appear, hl_color=hl)
    speaker_badge(canvas, sc, t, top)
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, int(W * gt / ep.total), 10], fill=YELLOW + (255,))
    return canvas.convert("RGB")


# ---------------------------------------------------------------- 書き出し
_EP = None


def _render_range(args):
    a, b, path = args
    ep = _EP
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-profile:v", "high", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        gt = fi / FPS
        i, s, t0 = ep.scene_at(gt)
        proc.stdin.write(render_frame(ep, i, s, gt - t0, gt).tobytes())
    proc.stdin.close()
    proc.wait()
    return path


def render(ep):
    global _EP
    import multiprocessing as mp
    import tempfile
    _EP = ep
    os.makedirs(OUTDIR, exist_ok=True)
    workers = max(1, os.cpu_count() or 1)
    tmp = tempfile.mkdtemp(prefix="render_", dir=OUTDIR)
    step = -(-ep.n_frames // workers)
    jobs = [(k, min(k + step, ep.n_frames), os.path.join(tmp, f"part{j:02d}.mp4"))
            for j, k in enumerate(range(0, ep.n_frames, step))]
    print(f"{ep.n_frames} frames ({ep.total:.1f}s) / {len(jobs)} workers", flush=True)
    with mp.get_context("fork").Pool(len(jobs)) as pool:
        parts = pool.map(_render_range, jobs)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    audio_in = ["-i", ep.out_wav] if ep.voiced else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, *audio_in,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-ac", "2",
                    "-t", f"{ep.total:.3f}", "-movflags", "+faststart", ep.out_mp4], check=True)
    for p in parts + [lst]:
        os.remove(p)
    os.rmdir(tmp)
    print("done:", ep.out_mp4, f"{ep.total:.1f}s")


def preview(ep):
    pdir = os.path.join(OUTDIR, "preview", ep.name)
    os.makedirs(pdir, exist_ok=True)
    for i, s, t0 in ep.timeline():
        t = s["lines"][0]["start"] + 0.3 if s.get("lines") else s["d"] * 0.7
        if s.get("reveal"):
            t = max(t, s["reveal"][1] + 0.3)
        t = min(t, s["d"] - 0.05)
        render_frame(ep, i, s, t, t0 + t).save(os.path.join(pdir, f"scene{i + 1:02d}.png"))
    print("preview:", pdir)


# ---------------------------------------------------------------- 音声(VOICEVOX)
ENGINE = "http://127.0.0.1:50021"
SR = 48000
Z, Z_CRY, M = 3, 76, 2  # ずんだもん(ノーマル) / ずんだもん(なみだめ) / 四国めたん(ノーマル)
NAME = {Z: "ずんだもん", Z_CRY: "ずんだもん", M: "四国めたん"}
GAP_LINE, TAIL, SPEED = 0.15, 0.35, 1.15
BGM_GAIN, BGM_DUCK, SE_GAIN = 0.28, 0.45, 0.55


def _post(path, params=None, body=None):
    url = ENGINE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def synth(speaker, text, speed=SPEED):
    q = json.loads(_post("/audio_query", {"text": text, "speaker": speaker}))
    q.update(speedScale=speed, outputSamplingRate=SR, outputStereo=False, prePhonemeLength=0.05, postPhonemeLength=0.05)
    wav = _post("/synthesis", {"speaker": speaker}, q)
    with wave.open(io.BytesIO(wav)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a, q["kana"]


def load_audio(path, channels):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(channels), "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, channels).copy()


def se(name, gain=1.0):
    a = load_audio(os.path.join(ASSETS, "se", name + ".mp3"), 1)[:, 0]
    return a / (np.abs(a).max() + 1e-9) * gain


def voice(ep):
    try:
        urllib.request.urlopen(ENGINE + "/version", timeout=5)
    except Exception:
        sys.exit("VOICEVOX ENGINE に接続できません (127.0.0.1:50021)")
    scenes, clips, t0 = [], [], 0.0
    for si, lines in enumerate(ep.lines):
        t = t0 + ep.lead.get(si, 0.0) + 0.1
        entries = []
        for spk, text in lines:
            a, kana = synth(spk, text, ep.speed)
            dur = len(a) / SR
            entries.append(dict(speaker=NAME[spk], text=text, start=round(t - t0, 3), dur=round(dur, 3)))
            clips.append((t, a))
            print(f"[{si + 1:02d}] {NAME[spk]} {dur:4.1f}s  {kana}")
            t += dur + GAP_LINE
        d = max(ep.scenes[si]["min_d"], t - GAP_LINE + TAIL - t0)
        scenes.append(dict(start=round(t0, 3), d=round(d, 3), lines=entries))
        t0 += d
    total = t0
    n = int(SR * (total + 0.5))
    vo = np.zeros(n)
    for st, a in clips:
        i = int(st * SR)
        vo[i:i + len(a)] += a
    fx = np.zeros(n)

    def add(clip, at):
        i = int(at * SR)
        if i < 0:
            clip, i = clip[-i:], 0
        m = min(len(clip), n - i)
        if m > 0:
            fx[i:i + m] += clip[:m]

    if ep.sfx:
        ep.sfx(add, se, scenes)
    venv = np.convolve(np.abs(vo), np.ones(4800) / 4800, "same")
    talking = np.convolve(np.clip(venv * 25, 0, 1), np.ones(9600) / 9600, "same")
    gain = BGM_GAIN * (1 - (1 - BGM_DUCK) * talking)
    tt = np.arange(n) / SR
    for k in ep.calm_scenes:
        c0, c1 = scenes[k]["start"] - 0.3, scenes[k]["start"] + scenes[k]["d"]
        gain *= np.clip(np.maximum((c0 - tt) / 0.6, (tt - c1) / 0.8), 0, 1)
    gain *= np.clip((total - tt) / 2.0, 0, 1)
    bgm = np.zeros((n, 2), np.float32)
    if ep.bgm and os.path.exists(ep.bgm):
        b = load_audio(ep.bgm, 2)
        # 動画より短い曲はつなげてループ(つなぎ目は0.5秒クロスフェード)
        xf = int(SR * 0.5)
        out = b.copy()
        while len(out) < n and len(b) > 2 * xf:
            ramp = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
            head = out[-xf:] * (1 - ramp) + b[:xf] * ramp
            out = np.concatenate([out[:-xf], head, b[xf:]])
        out = out[:n]
        bgm[:len(out)] = out
    else:
        print("BGM なしで書き出します:", ep.bgm)
    mix = (vo + fx * SE_GAIN * (1 - 0.35 * talking))[:, None] + bgm * gain[:, None]
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    os.makedirs(OUTDIR, exist_ok=True)
    with wave.open(ep.out_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump(dict(total=round(total, 3), scenes=scenes), open(ep.out_json, "w"), ensure_ascii=False, indent=1)
    print(f"total {total:.1f}s ->", ep.out_wav)


def main(make_episode):
    """make_episode: Episode を返す関数(voice 後に尺を読み直すため関数で渡す)。"""
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    if cmd == "voice":
        voice(make_episode())
    elif cmd == "preview":
        preview(make_episode())
    elif cmd == "render":
        render(make_episode())
    elif cmd == "all":
        voice(make_episode())
        ep = make_episode()
        preview(ep)
        render(ep)
    else:
        sys.exit("usage: voice | preview | render | all")
