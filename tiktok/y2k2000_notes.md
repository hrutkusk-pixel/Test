# 外れた人類滅亡説 #3「2000年問題」（立ち絵あり）

- 動画: `tiktok/output/y2k2000.mp4`（約106秒）
- 再生成: `python3 tiktok/y2k2000.py voice` → `preview` → `render`
- 立ち絵: 話している人が画面下から出る（ずんだもん＝左、四国めたん＝右）。ずんだもんの短いリアクションと四国めたんの「答え合わせ」「約束」は大きく表示（LINES の3番目に "+big" / "+small" で個別指定可）。`Episode(..., characters=True)` で有効

## 構成
1. つかみ: 世界中のコンピューターが止まると言われた日
2. 予告: 最後に本当にトラブルが出た意外な日
3. 昔のコンピューターは年を下2ケタで記録 → 99の次は00 → 1900年と勘違い？
4. 銀行・電気・交通が止まるかも？
5. ★1999年10月、日本政府も数日分の食料と水の備蓄を呼びかけ
6. ★でも当時の調査では約半数が「備蓄しない」
7. 世界の対策費は3000億〜6000億ドルとも（推計）
8. 2000年1月1日 → 大きな混乱はなかった
9. ★ただし原発の表示システムなどで小さな不具合（運転に影響なし）
10. 答え合わせ: 対策が進んだからという見方が多い（大げさだったという声も）
11. ★約束の意外な日: 2000年2月29日（400年に1度の特別なうるう年）
12. ★郵便貯金のATM約1200台が動かず（午後に復旧）
13. 覚えてる？知らない？

## 表現の判断メモ
- 「何も起きなかった」ではなく「大きな混乱はなかった」（実際に小さな不具合はあったため）
- 対策費は推計に幅があるので「とも」「推計」。日本円換算は「数十兆円」とおおまかに
- ATM約1200台は当時の報道ベース（郵政省発表の一次資料は未確認）
- 「大げさだった」という見方も併記して一方的にしない

## 立ち絵の利用条件
- 坂本アヒル氏「ずんだもん立ち絵素材2.3」「四国めたん立ち絵素材2.1」（pixiv 92641351 / 92641379、ユーザー提供の配布ZIP）
- 同梱 readme: 「良識の範囲内で、動画やアイコン等、自由にご利用ください。公式の規約に準じての商用利用や、改変・加工しての利用も可能です。クレジット表記や、ニコニコでのコンテンツツリー登録は任意です。」＋公式ガイドラインを読むこと
- 公式ガイドライン（https://zunko.jp/guideline.html ・Q&A https://zunko.jp/guideline_qa.html を直接確認）: 個人の動画での広告収入・クリエイター奨励プログラム程度は「非商用の範囲」で申請不要
- **注意: 企業スポンサー付きPR・商品紹介動画は別扱い（有償）**。TikTok Shop アフィリエイト等で立ち絵を使う前に要確認
- 禁止: キャラのイメージを著しく悪くする利用、特定の個人・団体への非難、政治・宗教、嘘やフェイク、情報商材 など
- クレジットは任意だが動画末尾に「立ち絵:坂本アヒル」と表示
- 表情・口パク: `tiktok/tachie.py`（PSDTool形式のレイヤーを合成）。素材PSDは `tiktok/assets/images/chars/`（git 管理外）

## 投稿キャプション案
```
「世界中のコンピューターが止まる」と言われた2000年問題
本当にトラブルが目立ったのは、元日じゃなく"意外な日"だった…
あなたは2000年問題、覚えてる？👇

VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵:坂本アヒル
BGM: 奇妙な案内人 by MATSU（OpenTracks）
SE: 効果音ラボ

#2000年問題 #Y2K #平成 #雑学 #ずんだもん
```

## 事実確認に使ったソース（2026-11-23 検索）
- 政府の備蓄呼びかけ（1999年10月29日）・世論調査: https://www.japantimes.co.jp/news/1999/10/29/national/public-urged-to-stockpile-food-ahead-of-y2k ／ https://www.japantimes.co.jp/news/1999/12/02/national/y2k-poll-finds-homes-wary-but-unprepared ／ https://japan.kantei.go.jp/y2k/991029readiness.html
- 対策費の推計: https://www.britannica.com/technology/Y2K-bug ／ https://encyclopedia.uia.org/problem/non-compliance-computer-equipment-year-2000-transition
- 1月1日の結果・原発の軽微な不具合: https://www.tepco.co.jp/cc/press/00010101-j.html ／ https://www.mofa.go.jp/y2k/kinfo_00028.html ／ https://atomica.jaea.go.jp/data/pdf/ATOMICA_01-04-01-10.pdf.zip
- 対策が功を奏したという見方: https://theconversation.com/if-you-think-the-millennium-bug-was-a-hoax-here-comes-a-history-lesson-129042
- うるう日（2000年2月29日）の障害・ATM約1200台: https://scan.netsecurity.ne.jp/article/2000/03/02/131.html ／ https://www.fsa.go.jp/p_fsa/2000_mon/2000_mon/2_120229.html ／ https://www.japantimes.co.jp/news/2000/03/01/national/leap-day-efforts-not-enough-aoki
