#!/usr/bin/env python3
"""VOICEVOX でセリフ音声を作り、効果音と合わせて1本の音声トラック + タイミング表を書き出す。

前提: VOICEVOX ENGINE が http://127.0.0.1:50021 で起動していること
      (例: docker run -d --name vv -p 127.0.0.1:50021:50021 voicevox/voicevox_engine:cpu-latest)
出力: tiktok/output/halley1910_audio.wav / tiktok/output/halley1910_timing.json
クレジット: VOICEVOX:ずんだもん / VOICEVOX:四国めたん (動画内と投稿説明欄に表記する)
"""
import io
import json
import os
import sys
import urllib.parse
import urllib.request
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = "http://127.0.0.1:50021"
SR = 48000
OUT_WAV = os.path.join(HERE, "output", "halley1910_audio.wav")
OUT_JSON = os.path.join(HERE, "output", "halley1910_timing.json")

Z, Z_CRY, M = 3, 76, 2  # ずんだもん(ノーマル) / ずんだもん(なみだめ) / 四国めたん(ノーマル)
NAME = {Z: "ずんだもん", Z_CRY: "ずんだもん", M: "四国めたん"}

# シーン番号(render_halley1910.py の SCENES と同じ順) -> セリフ [(話者, 文)]
# 口調: ずんだもん=一人称「ボク」・語尾「〜のだ/〜なのだ」
#       四国めたん=一人称「わたくし」・お嬢様風タメ口(「〜わよ」「〜かしら」)・二人称「アンタ(たち)」
LINES = [
    [(Z, "1910年、人類は、彗星のガスで死ぬって、本気で信じてたのだ！")],
    [(M, "最後に、この彗星が次に来る年も、わたくしが教えてあげるわ。")],
    [(M, "主役はハレー彗星よ。約76年ごとに、地球に近づく彗星なの。")],
    [(M, "1910年2月、アメリカの天文台が、彗星の尾から、有毒なシアン系のガスを見つけたのよ。")],
    [(M, "しかもこの年、地球はその尾の中を、通過する予定だったの。"), (Z, "えっ、ボクたち大ピンチなのだ！")],
    [(M, "ガスが大気に広がれば、生命が絶えるかも。そんな天文学者の説を、新聞が報じたのよ。")],
    [(Z_CRY, "世界中がパニックなのだー！")],
    [(M, "家の隙間や鍵穴を目張りして、閉じこもった人もいたそうよ。")],
    [(Z, "ガスマスクを買い込む人も、いたのだ！")],
    [(M, "露店では、彗星よけの薬なんてものまで、売られたのよ。"), (Z, "ぜったい効かないのだ。")],
    [(Z, "彗星よけの傘まで、登場したのだ！")],
    [(M, "教会に集まって、祈る人もいたわ。")],
    [(M, "そして運命の日。1910年、5月19日ごろ。")],
    [(Z, "……何も、起きなかったのだ。")],
    [(M, "答え合わせよ。尾のガスは、とてつもなく薄かったの。地球の大気のほうが、何千倍も濃いんだから。")],
    [(M, "約束の答えよ。ハレー彗星が次に来るのは、2061年。"), (Z, "そんなに先なのだ！？")],
    [(Z, "みんなは2061年、この彗星を見られるのだ？"), (M, "見られる？見られない？アンタたちの答え、コメントで聞かせなさい。")],
]
# シーンごとの最低尺(秒)。セリフが短くても絵を見せる時間を確保する
MIN_D = [3.6, 3.0, 4.0, 4.4, 4.0, 5.0, 3.0, 3.5, 3.5, 4.0, 3.5, 3.5, 4.0, 4.0, 5.5, 4.5, 5.5]
LEAD = {13: 1.0}  # シーン先頭の「間」(秒)。14「何も起きなかった」の前に溜める
GAP_LINE = 0.15   # 同じシーン内のセリフ間
TAIL = 0.35       # シーン最後のセリフ後の余白
SPEED = 1.15      # 少し早口(TikTok向け)


def post(path, params=None, body=None):
    url = ENGINE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def synth(speaker, text):
    q = json.loads(post("/audio_query", {"text": text, "speaker": speaker}))
    q["speedScale"] = SPEED
    q["outputSamplingRate"] = SR
    q["outputStereo"] = False
    q["prePhonemeLength"] = 0.05
    q["postPhonemeLength"] = 0.05
    wav = post("/synthesis", {"speaker": speaker}, q)
    with wave.open(io.BytesIO(wav)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a, q["kana"]


# ------------------------------------------------------------ 効果音(すべて数式で生成)
rng = np.random.default_rng(0)


def env(n, a=0.005, r=0.3):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)


def sfx_whoosh(dur=0.45):
    n = int(SR * dur)
    noise = rng.standard_normal(n)
    # 周波数が上がっていく簡易バンドパス(差分の重ね合わせ)
    out = np.zeros(n)
    t = np.arange(n) / n
    lp = 0.0
    for i in range(n):
        k = 0.02 + 0.25 * t[i]
        lp += k * (noise[i] - lp)
        out[i] = lp
    out = out - np.convolve(out, np.ones(30) / 30, "same")
    out *= np.sin(np.pi * t) ** 2
    return out / (np.abs(out).max() + 1e-9) * 0.35


def sfx_boom(dur=1.6):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 45 + 80 * np.exp(-t * 6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 2.2)
    click = rng.standard_normal(n) * np.exp(-t * 40) * 0.5
    return np.tanh((body + click) * 1.5) * 0.6


def sfx_pop(freq=880, dur=0.35):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2 * t)
    return s * env(n, 0.002, 0.08) * 0.3


def sfx_ding(dur=1.4):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(1046.5, 1), (1568, 0.5), (2093, 0.25)])
    return s * env(n, 0.003, 0.45) * 0.22


def sfx_alarm(dur=3.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 600 + 250 * np.sign(np.sin(2 * np.pi * 2.5 * t))
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5
    fade = np.minimum(1, t / 0.1) * np.minimum(1, (dur - t) / 0.4)
    return s * fade * 0.08


def sfx_drone(dur=4.0, f=55):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.5 * t + 0.3) + 0.3 * np.sin(2 * np.pi * f * 2.01 * t)
    fade = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 1.0)
    return s * fade * 0.12


def sfx_tape(dur=0.5):
    n = int(SR * dur)
    t = np.arange(n) / SR
    crackle = rng.standard_normal(n) * (rng.random(n) > 0.7)
    return crackle * np.minimum(1, t / 0.02) * np.exp(-t * 4) * 0.25


def sfx_shimmer(dur=2.5):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(10):
        st = int(k * 0.12 * SR)
        f = 1500 + 300 * k
        seg = np.sin(2 * np.pi * f * t[: n - st]) * np.exp(-t[: n - st] * 6)
        s[st:] += seg
    return s * 0.05


def main():
    try:
        urllib.request.urlopen(ENGINE + "/version", timeout=5)
    except Exception:
        sys.exit("VOICEVOX ENGINE に接続できません (127.0.0.1:50021)")
    scenes = []
    voice_clips = []
    t0 = 0.0
    for si, lines in enumerate(LINES):
        t = t0 + LEAD.get(si, 0.0) + 0.1
        entries = []
        for spk, text in lines:
            a, kana = synth(spk, text)
            dur = len(a) / SR
            entries.append(dict(speaker=NAME[spk], text=text, start=round(t - t0, 3), dur=round(dur, 3)))
            voice_clips.append((t, a))
            print(f"[{si + 1:02d}] {NAME[spk]} {dur:4.1f}s  {kana}")
            t += dur + GAP_LINE
        d = max(MIN_D[si], t - GAP_LINE + TAIL - t0)
        scenes.append(dict(start=round(t0, 3), d=round(d, 3), lines=entries))
        t0 += d
    total = t0
    n = int(SR * (total + 0.5))
    voice = np.zeros(n)
    for st, a in voice_clips:
        i = int(st * SR)
        voice[i:i + len(a)] += a
    fx = np.zeros(n)

    def add(clip, at):
        i = int(at * SR)
        if i < 0:
            clip, i = clip[-i:], 0
        fx[i:i + len(clip)] += clip[: n - i]

    S = [s["start"] for s in scenes]
    add(sfx_boom(), 0.0)
    for k in range(1, len(S)):
        if k not in (6, 13):
            add(sfx_whoosh(), S[k] - 0.22)
    add(sfx_shimmer(), S[3] + 0.6)             # スペクトル
    add(sfx_boom(1.2) * 0.7, S[6])              # パニック
    add(sfx_alarm(scenes[6]["d"]), S[6])
    add(sfx_tape(), S[7] + 0.1)
    add(sfx_tape(), S[7] + 0.45)
    for k in (8, 9, 10, 11):
        add(sfx_pop(660 + 110 * (k - 8)), S[k] + 0.05)
    add(sfx_pop(520), S[12] + 0.1)
    add(sfx_drone(scenes[13]["d"] + 0.5, 49), S[13] - 0.2)   # 静寂の前のうなり
    add(sfx_ding(), S[14] + 0.05)                # 答え合わせ
    add(sfx_boom(0.8) * 0.5, S[15] + 0.8)        # 2061年 ドン
    add(sfx_ding() * 0.8, S[15] + 0.8)
    add(sfx_pop(990), S[16] + 0.05)

    mix = voice * 1.0 + fx * 0.8
    # 声が鳴っている間は効果音を少し下げる(簡易ダッキング)
    venv = np.convolve(np.abs(voice), np.ones(2400) / 2400, "same")
    duck = 1 - 0.45 * np.clip(venv * 20, 0, 1)
    mix = voice + fx * 0.8 * duck
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump(dict(total=round(total, 3), scenes=scenes), open(OUT_JSON, "w"), ensure_ascii=False, indent=1)
    print(f"total {total:.1f}s ->", OUT_WAV)


if __name__ == "__main__":
    main()
