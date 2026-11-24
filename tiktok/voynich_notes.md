# 未解決ミステリー #1「600年誰にも読めない本 ヴォイニッチ手稿」（短い型・立ち絵あり）

- 動画: `tiktok/output/voynich.mp4`（約63秒）
- 再生成: `python3 tiktok/voynich.py voice` → `preview` → `render`

## 構成
1. つかみ: 600年、誰にも読めない本（0秒目から写本13rの実物画像）
2. ヴォイニッチ手稿、約240ページ、見たことのない文字でびっしり
3. 描かれた植物の多くは何の植物か特定できない
4. 2009年の炭素年代測定: 羊皮紙は1404〜1438年ごろ
5. 新発見① 2024年: マルチスペクトル撮影で1ページ目の余白に消された文字（17世紀の持ち主マルチの解読の試みか）
6. 新発見② 2025年: 15世紀のトランプとサイコロで作れる暗号（Naibbe暗号）でそっくりな文章が作れた
7. 新発見③ 2026年10月: 製本時にページ順がバラバラになっていた可能性（Davis & Layfield, Digital Medievalist）
8. それでもまだ誰も読めていない
9. 暗号？デタラメ？ → エンドカード

## 表現の判断メモ
- 「地球上に存在しない植物」は言い過ぎなので「特定できない」
- 炭素年代測定でわかったのは羊皮紙の年代（書かれた時期そのものではない）ので「羊皮紙は」
- 2025年の研究: 本人も「この方法で作られたわけではないだろう」と述べている → 「作れる、という研究」止まり
- 2026年の研究: 証拠はまだ不確か → 「可能性がある」
- ルドルフ2世が600ドゥカートで買った話は伝聞（1665/66年のマルチの手紙）なので今回は不使用
- 浴場のページ（裸の女性の絵）は TikTok の表示制限を避けるため使わない
- 「AIで解読した」系の主張は検証されていないので扱わない

## 画像
- イェール大学バイネキ稀覯本図書館 Beinecke MS 408（15世紀の写本＝パブリックドメイン）
  - デジタル版: https://collections.library.yale.edu/catalog/2002046 （IIIF で取得、Access: Public）
  - Yale のオープンアクセス方針: パブリックドメイン作品のデジタル画像は誰でも目的を問わず利用可 https://news.yale.edu/2011/05/10/digital-images-yale-s-vast-cultural-collections-now-available-free ／ バイネキ: パブリックドメインの資料は許可不要 https://beinecke.library.yale.edu/node/65850
  - 使用ページ: 13r, 33v, 9v, 1r, 67r, 99r, 表紙（assets/images/voynich/、git 管理外）
  - 各画像の左下とエンドクレジットに「Beinecke MS 408, Yale University」

## 投稿キャプション案
```
600年間、誰にも読めない本「ヴォイニッチ手稿」
2024〜2026年に相次いだ"最新の発見"とは…
あなたは暗号だと思う？デタラメだと思う？👇

VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵:坂本アヒル
BGM: 奇妙な案内人 by MATSU（OpenTracks）
SE: 効果音ラボ
画像: Beinecke MS 408, Yale University

#ヴォイニッチ手稿 #未解決 #ミステリー #雑学 #ずんだもん
```

## 事実確認に使ったソース（2026-11-24 検索）
- 炭素年代測定（2009年、1404〜1438年）: https://www.eurekalert.org/news-releases/624074 ／ https://www.voynich.nu/extra/carbon.html
- 2024年マルチスペクトル撮影: https://www.theartnewspaper.com/2024/09/25/voynich-manuscript-scans-reveal-early-decoding-attempt ／ https://www.medievalists.net/2024/09/hidden-secrets-of-the-voynich-manuscript-revealed-through-cutting-edge-scans/
- 2025年 Naibbe 暗号（Cryptologia）: https://tandfonline.com/doi/full/10.1080/01611194.2025.2566408 ／ https://www.livescience.com/archaeology/mysterious-voynich-manuscript-may-be-a-cipher-a-new-study-suggests
- 2026年10月 製本順の研究: https://www.livescience.com/archaeology/undeciphered-voynich-manuscript-may-have-been-bound-out-of-order-study-finds ／ https://archaeologymag.com/2026/10/voynich-manuscript-was-bound-in-the-wrong-order/
- 来歴（マルチの手紙・600ドゥカート）: https://www.theartnewspaper.com/2023/01/13/unknown-history-of-600-year-old-coded-voynich-manuscript-revealed-by-researcher
