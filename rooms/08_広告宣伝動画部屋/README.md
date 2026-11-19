# 08 広告宣伝動画制作室

『顔のない春』広告2本。状態：REVIEW。2026-11-19制作。採用画像・音源は17音ADV配布版 `kaononaiharu-adv-sound-review-win` より。

## 完成MP4

- `deliverables/kaononaiharu_vertical_15s.mp4`：1080×1920、9:16、15秒、30fps。
- `deliverables/kaononaiharu_horizontal_30s.mp4`：1920×1080、16:9、30秒、30fps。
- 両方H.264、yuv420p、BT.709 limited range、AAC 48kHz stereo、faststart。

共通広告コピー「あの日、きみはどんな顔をしていた？」は本文引用ではない。ADV画面の外に置き、同じ橋の無彩→色彩に重ねた。末尾は作品名『顔のない春』。全彩版の透花の表情・結末・終盤CGは使っていない。

## 編集構成

| 縦型 | 内容 |
|---|---|
| 0–5秒 | 同一の橋が1.25–2.6秒で色づく。共通コピーを3行表示 |
| 5–10秒 | 初周白筆の透花。顔を認識できない出会いを見せる |
| 10–12秒 | 再び色彩の橋、サブタイトル |
| 12–15秒 | 作品名・ジャンル・サブタイトル |

| 横型 | 内容 |
|---|---|
| 0–5秒 | 序盤の橋の実ADV画面。「耳から抜いてから気づく。もう吠えないんだった。」 |
| 5–10秒 | 初周白筆の出会い。「おはよう」 |
| 10–16秒 | 同じ出会いの末尾。「今日はもう鞄に入れてもよさそうだった。」 |
| 16–26秒 | 無彩の橋が17.25–18.6秒で色づく。共通広告コピー |
| 26–30秒 | 作品名・ジャンル・サブタイトル |

横型の実画面は配布物の隔離コピーをRen'Pyで起動し、既存の画面定義・本文・採用画像から撮影した静止キャプチャ。ゲーム画面を模造したものではない。広告の編集として各画面を5〜6秒保持。元の配布物と通常セーブは変更していない。

## 再編集

`project/` がRemotion編集プロジェクト。`src/Films.tsx` にカット尺、各Scene.tsxに画面・文字・色変化、`public/` に入力素材・実画面・音声ミックスがある。`package-lock.json` を同梱。

1. `project/` で `npm ci`。
2. `npm run dev -- --no-open` で編集プレビュー。
3. この室で `python -m pip install --target python_lib pillow numpy imageio-ffmpeg`。
4. 音を変更した場合 `python mix_audio.py`。
5. `./render.ps1` で2本のレンダー、配信用変換、全尺検査。

Chromeの実行場所が違う場合は `render.ps1` の `$chromePath` を変更する。元のRemotion書き出しは `masters/`、配信用は `deliverables/`。生成ライブラリ・隔離ゲーム・node_modulesは版管理から除外。

`prepare.py` と `capture_game.py` は同じSUMIフォルダ構成で入力を再取得するための制作スクリプト。通常の動画再編集には既に `public/` にある素材で足りる。原画・ゲーム本文の正本を編集しない。

## 検証と権利

- `qa/technical_QA.json`：最終MP4のSHA256、全フレーム数、全尺デコード結果、全音声サンプルのピーク・秒別RMS。
- `qa/vertical_contact.jpg` / `qa/horizontal_contact.jpg`：毎秒・カット直前直後・最終フレームの検品画像。
- `QA.md`：目視結果と未実施事項。
- `RIGHTS.md` / `sources.json`：商用広告利用条件と入力出典。

音は全尺を機械解析した。スピーカー／ヘッドホンの聴感評価は未実施であり、音色やバランスの聴感合格を意味しない。公開・広告出稿はこの制作依頼に含めて実行していない。
