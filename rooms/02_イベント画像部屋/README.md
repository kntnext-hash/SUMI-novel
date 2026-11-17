# 02_イベント画像部屋｜イベント画像部屋

- 主担当：アート担当

## 目的

イベントCGの構図と生成指示を作成する。

## 成果物

- shotlists/：CGショットリスト
- prompts/：生成プロンプト
- assets/：採用CG
- reviews/：画の検証記録

## 長編版の04室への受け渡し

[長編イベントCGの対応表](shotlists/長編イベントCG_04室受渡対応表.tsv) は、共通入力 `kaononaiharu_long_complete/制作/画像と演出/` の画像生成一覧と本文キューを結び、キューごとに本採用原画と初周の出力名を記載する。同じ画像を複数回使う場面も各行に残した。原画のパスは `SUMI-novel` からの相対パス。

同じ制作ワークスペースでは [本採用FULLの場面順一覧](private_sources/本採用_FULL/場面順一覧.html) から原寸の絵を確認できる。本採用PNGは非公開のローカル素材で、別のチェックアウトで作業するときは同フォルダを受け渡し、表のSHA256で版を照合する。

初周は「初周導出元」列を使う。路地の返事 `CG_can_reply__3.png` は直前の `CG_can_pause__3.png` と同じ絵を別名で書き出す。再読は各行の「採用FULL原画」を使う。

## 状態管理

`DRAFT → REVIEW → APPROVED → INTEGRATED → TESTED`（APPROVED はユーザーの承認時のみ）
