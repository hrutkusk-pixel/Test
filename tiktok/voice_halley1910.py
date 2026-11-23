#!/usr/bin/env python3
"""VOICEVOX でセリフ音声を作り、BGM・効果音と合わせて1本の音声トラック + タイミング表を書き出す。

前提: VOICEVOX ENGINE が http://127.0.0.1:50021 で起動していること
      (例: docker run -d --name vv -p 127.0.0.1:50021:50021 voicevox/voicevox_engine:cpu-latest)
出力: tiktok/output/halley1910_audio.wav / tiktok/output/halley1910_timing.json
クレジット: VOICEVOX:ずんだもん / VOICEVOX:四国めたん (動画内と投稿説明欄に表記する)
"""
import io
import json
import os
import subprocess
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
    [(M, "そしてこの年、地球はちょうど、その尾の中を通過する予定だったの。"), (Z, "えっ、ボクたち大ピンチなのだ！")],
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


# ------------------------------------------------------------ BGM・効果音(素材ファイル)
# 素材は tiktok/assets/ に置く(再配布禁止のため git 管理外)
#   BGM : OpenTracks「奇妙な案内人」by MATSU  https://opentracks.com/bgm/detail/12153
#   効果音: 効果音ラボ https://soundeffect-lab.info/
ASSETS = os.path.join(HERE, "assets")
BGM_FILE = os.path.join(ASSETS, "bgm", "kimyou_na_annainin_MATSU.mp3")
BGM_GAIN = 0.28        # 声がないとき
BGM_DUCK = 0.45        # 声があるときは BGM_GAIN * BGM_DUCK まで下げる
SE_GAIN = 0.55


def load_audio(path, channels):
    """ffmpeg で読み込んで float32 (n, channels) を返す。"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(channels), "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, channels).copy()


def se(name, gain=1.0):
    a = load_audio(os.path.join(ASSETS, "se", name + ".mp3"), 1)[:, 0]
    return a / (np.abs(a).max() + 1e-9) * gain


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
        m = min(len(clip), n - i)
        fx[i:i + m] += clip[:m]

    S = [s["start"] for s in scenes]
    sc = scenes
    add(se("text-impact1", 0.9), 0.0)                       # つかみ
    for k in range(1, len(S)):
        if k not in (6, 13, 14, 15):
            add(se("highspeed-movement1", 0.35), S[k] - 0.18)  # 場面転換
    add(se("kira1", 0.5), S[3] + 0.6)                       # スペクトル
    add(se("emergency-alert1", 0.45), S[6])                 # パニック
    add(se("cellophane-tape-cut1", 0.7), S[7] + 0.1)        # 目張り
    add(se("cellophane-tape-cut1", 0.6), S[7] + 0.9)
    for k in (8, 9, 10):
        add(se("pa1", 0.6), S[k] + 0.05)                    # マスク・薬・傘
    add(se("church-bell1", 0.5), S[11] + 0.05)              # 教会
    add(se("clock-tower-bell1", 0.6), S[12] + 0.05)         # 運命の日
    last = sc[13]["lines"][-1]
    add(se("tin1", 0.8), S[13] + last["start"] + last["dur"] + 0.05)  # 何も起きなかった → チーン
    add(se("correct2", 0.6), S[14] + 0.05)                  # 答え合わせ
    add(se("text-impact3", 0.8), S[15] + 0.8)               # 2061年
    add(se("kira1", 0.5), S[16] + 0.05)                     # 最後の質問

    # BGM: 声の間は下げる(ダッキング)。「何も起きなかった」のシーンは一度止めて静寂を作る
    venv = np.convolve(np.abs(voice), np.ones(4800) / 4800, "same")
    talking = np.clip(venv * 25, 0, 1)
    talking = np.convolve(talking, np.ones(9600) / 9600, "same")  # ゆっくり上下させる
    gain = BGM_GAIN * (1 - (1 - BGM_DUCK) * talking)
    t = np.arange(n) / SR
    calm0, calm1 = S[13] - 0.3, S[13] + sc[13]["d"]
    gain *= np.clip(np.maximum((calm0 - t) / 0.6, (t - calm1) / 0.8), 0, 1)
    gain *= np.clip((total - t) / 2.0, 0, 1)                # 最後2秒でフェードアウト
    bgm = np.zeros((n, 2), np.float32)
    if os.path.exists(BGM_FILE):
        b = load_audio(BGM_FILE, 2)[:n]
        bgm[:len(b)] = b
    else:
        print("BGM が見つからないため BGM なしで書き出します:", BGM_FILE)
    fx_duck = 1 - 0.35 * talking
    mono = voice + fx * SE_GAIN * fx_duck
    mix = mono[:, None] + bgm * gain[:, None]
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump(dict(total=round(total, 3), scenes=scenes), open(OUT_JSON, "w"), ensure_ascii=False, indent=1)
    print(f"total {total:.1f}s ->", OUT_WAV)


if __name__ == "__main__":
    main()
