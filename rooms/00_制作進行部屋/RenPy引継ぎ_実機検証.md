# Ren’Py引継ぎと実機検証（2026-11-18）

状態は制作継続。実装の担当はユーザー指示でCodexへ変更。

## 編集対象
game/ に0.9-full-light配布物の24本のrpyと素材を取り込んだ。ローカルのimages・fonts・guiは既存配布物からコピーし、Gitでは除外。ビルド用ランタイムはDesktop/kaononaiharu-win/kaononaiharu-0.9-full-light-winにあるRen’Py 8.5.3。

## 確認した事実
- guisupport.rpyはscaleだけに修正。配布物のRen’Pyでlintを完了。
- Windowsでタイトルから本編を開始できた。
- 初周C01S01の1行目をページ1・スロット1に保存。2行目へ進め、ロード画面の確認ダイアログを通じて保存を読込み、1行目と無彩の玄関画像へ復帰した。
- UIは仮メニューが英語、NVL本文が小さい、黒い背景窓が大きい。03室へ修正用素材を依頼。

## 実行中・未完了
- 06室がRen’Pyのtest機構を用いた全ルート・初周再読のテストを作成中。
- 全分岐の実行、画像切替の全件検証、終盤・再読・再起動後のセーブロードは未完了。
- 02室はOP既存素材と不足を調査、03室は商品版UI、07室は音源の制作・調達を整理。
- 次の実装はgame/へ行い、UI変更後は両解像度・長文表示を検証する。

## 全ルート自動検証の開始
06室の qa_story_all.rpy を専用コピー renpy_test_run/game に配置し、Ren’Py test qa_story_all --savedir isolated_saves で起動。2026-11-18時点の検証プロセスは137212。出力はワークスペース直下 renpy_test_run/run_stdout.txt と run_stderr.txt。8ルートの結果は qa_story_coverage.json に出る予定。プロセスの生存を確認済み、テスト合否はまだ未確定。次回はこのプロセスとログを確認して継続する。
