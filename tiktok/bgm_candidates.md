# BGM メモ

## 現在の標準
- 「奇妙な案内人」by MATSU（OpenTracks） https://opentracks.com/bgm/detail/12153 — 全シリーズ共通で使用中

## 今後の候補（2026-11-23 選定・作曲者条件確認済み：規約内なら許可不要、クレジット任意、無断転載・AI学習・大幅な改変は禁止）
| 曲 | 長さ | 向き |
|---|---|---|
| 仄青く眠る、海底遺跡 by 蒲鉾さちこ https://opentracks.com/bgm/detail/15037 | 2:02 | 神秘的アンビエント。宇宙系 |
| 銀色都市の秘密 by 蒲鉾さちこ https://opentracks.com/bgm/detail/17202 | 1:39（ループ仕様） | 謎解き・ドキュメンタリー調 |
| 踊る、宇宙の中で by 蒲鉾さちこ https://opentracks.com/bgm/detail/15926 | 0:58（ループ仕様） | 明るめエレクトロ。流星群など |

- 使うときは `tiktok/assets/bgm/` に置き、エピソードの `make_episode()` で `bgm="ファイル名.mp3"` を指定（短い曲は自動でループ）
