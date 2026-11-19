# 広告用音源の利用条件確認

確認日：2026-11-19。既存の17音ADV配布版 `builds/kaononaiharu-adv-sound-review-win` から2音だけを複製。音楽・台詞音声は追加していない。

| 素材 | 作者・一次出典 | 確認結果 | 広告での加工 |
|---|---|---|---|
| park_wind_loop.wav | Thimras / [Park ambiences](https://opengameart.org/content/park-ambiences) | 配布元の検索取得本文にCC0明記。直接取得は403。既存同梱台帳の作者・出典・CC0と一致 | 既存11.7秒ループを反復、0.48倍、冒頭0.5秒・末尾2秒フェード |
| bicycle_bell_single.wav | 13gkopeckak / [bell.wav, 378911](https://freesound.org/people/13gkopeckak/sounds/378911/) | 一次ページのCreative Commons 0と商用利用可の記載を取得確認 | 既存単発を0.65倍。縦1.6秒、横17秒で各1回 |

[CC0 1.0公式条件](https://creativecommons.org/publicdomain/zero/1.0/)は複製・改変・配布・実演を商用目的でも許可する。広告動画への同期・音量調整・反復に利用でき、著作権上の追加許諾・必須クレジットはない。作者による本作品への推奨を示唆しない。

公開元での素材種別は風の環境録音と自転車ベル。会話・歌・市販音楽を追加していない。出典・入力SHA256は `sources.json`、編集処理は `mix_audio.py`。2本とも同じ素材だがベルの配置時刻を変えた。

画像は同配布版の採用WebP。フルカラー人物の顔の元絵は完成映像に使わず、初周白筆の人物画像と無人の橋の無彩／フルカラー対を使用。重要な結末・最初の顔解放・終盤CGは未使用。

フォントは同梱NotoSerifJP-Regular.otf。OFLを `project/public/NotoSerifCJK-OFL.txt` に複製。映像の文字描画に使用。
