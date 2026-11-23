"""坂本アヒル氏の立ち絵素材(PSDTool形式のPSD)から表情を合成する。

レイヤー名の規則(PSDTool): 「*」で始まる兄弟は1つだけ表示(排他)、「!」で始まるものは常に表示。
選択は {"グループ/パス": "*選ぶレイヤー名"} で指定する(先頭の * ! は省略可)。
素材: tiktok/assets/images/chars/*.psd(git 管理外)
"""
import os

from psd_tools import PSDImage

HERE = os.path.dirname(os.path.abspath(__file__))
CHARS = os.path.join(HERE, "assets", "images", "chars")
PSD_FILES = {"ずんだもん": "zundamon_sakamoto_2.3.psd", "四国めたん": "metan_sakamoto_2.1.psd"}

_psd = {}


def _open(name):
    if name not in _psd:
        _psd[name] = PSDImage.open(os.path.join(CHARS, PSD_FILES[name]))
    return _psd[name]


def _strip(n):
    return n.lstrip("*!")


def _find(group, path):
    g = group
    for part in path.split("/"):
        for l in g:
            if _strip(l.name) == part:
                g = l
                break
        else:
            raise KeyError(path)
    return g


def compose(name, sel):
    """sel: {"グループパス": "レイヤー名"}。指定したレイヤーを表示し、同じグループの他の * レイヤーを隠す。"""
    psd = _open(name)
    saved = []

    def setv(layer, v):
        saved.append((layer, layer.visible))
        layer.visible = v

    for path, choice in sel.items():
        g = _find(psd, path)
        for l in g:
            if l.name.startswith("*"):
                setv(l, _strip(l.name) == choice)
        # 親グループも見えるようにする
        parts = path.split("/")
        for i in range(1, len(parts) + 1):
            setv(_find(psd, "/".join(parts[:i])), True)
    img = psd.composite(force=True)
    for layer, v in reversed(saved):
        layer.visible = v
    return img.convert("RGBA")


# ---------------------------------------------------------------- 表情プリセット
# 口は "open"/"closed" で切り替え(口パク)。目は "blink" でまばたき。
Z_BASE = {"服装1": "いつもの服", "服装1/左腕": "基本", "服装1/右腕": "基本", "顔色": "ほっぺ", "枝豆": "枝豆通常",
          "目": "目セット", "目/目セット": "普通白目", "目/目セット/黒目": "普通目"}
M_BASE = {"白ロリ服/右腕": "普通", "白ロリ服/左腕": "普通", "顔色": "普通2", "目": "目セット", "目/目セット": "普通白目",
          "目/目セット/黒目": "普通目"}

EXPR = {
    "ずんだもん": {
        "normal":    dict(base=Z_BASE, eye={}, brow="普通眉", closed="むふ", open="ほあー", blink="UU"),
        "happy":     dict(base=Z_BASE, eye={"目": "にっこり"}, brow="普通眉", closed="むふ", open="ほあー", blink="にっこり",
                          extra={"服装1/右腕": "手を挙げる"}),
        "surprised": dict(base=Z_BASE, eye={"目/目セット": "見開き白目"}, brow="上がり眉", closed="お", open="ほー", blink="UU"),
        "troubled":  dict(base=Z_BASE, eye={"目": "ジト目"}, brow="困り眉1", closed="むー", open="んあー", blink="UU",
                          extra={"枝豆": "枝豆萎え"}),
        "think":     dict(base=Z_BASE, eye={"目/目セット/黒目": "目逸らし"}, brow="困り眉2", closed="んー", open="ほあ", blink="UU",
                          extra={"服装1/左腕": "考える"}),
    },
    "四国めたん": {
        "normal":    dict(base=M_BASE, eye={}, brow="ごきげん", closed="ほほえみ", open="わあー", blink="目閉じ"),
        "smug":      dict(base=M_BASE, eye={"目/目セット/黒目": "カメラ目線"}, brow="太眉ごきげん", closed="にやり", open="▽",
                          blink="目閉じ", extra={"白ロリ服/右腕": "指差す"}),
        "surprised": dict(base=M_BASE, eye={"目/目セット": "見開き白目"}, brow="こまり", closed="お", open="わあー", blink="目閉じ"),
        "troubled":  dict(base=M_BASE, eye={"目/目セット/黒目": "目そらし"}, brow="こまり", closed="む", open="うえー", blink="目閉じ"),
    },
}


def render_state(name, expr="normal", mouth="closed", blink=False):
    e = EXPR[name].get(expr, EXPR[name]["normal"])
    sel = dict(e["base"])
    sel.update(e.get("extra", {}))
    sel.update(e["eye"])
    sel["眉"] = e["brow"]
    sel["口"] = e[mouth]
    if blink:
        sel["目"] = e["blink"]
    return compose(name, sel)
