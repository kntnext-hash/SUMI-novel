# AGENTS｜イベント画像部屋

主担当：アート担当

## 役割

イベントCGの構図と生成指示を作成する。

## この部屋の禁止事項・固有ルール

- 顔の解放前のCGで透花の顔を描かない。解放場面のCGは stage 4 以降の専用シーケンスとして扱う。
- 生成プロンプトには visual_stage と face_visibility を必ず含める。
- 未作成のCGは `docs/ASSET_REGISTRY.csv` に PENDING で登録する。

## 共通ルール（全室）

- 正本：`docs/STORY_BIBLE.md` / `docs/COLOR_STAGES.md` / `docs/VISUAL_BIBLE.md`。矛盾を見つけたら独断で解消せず、`rooms/00_制作進行部屋` へ報告する。
- 未確定事項（`docs/OPEN_QUESTIONS.md`）をユーザーの承認前に正史化しない。
- 状態は `DRAFT → REVIEW → APPROVED → INTEGRATED → TESTED` で管理する。**APPROVED はユーザーが承認したときだけ。**
- 顔・色の先出し禁止（`docs/COLOR_STAGES.md`）。第5章まで透花の顔は画面にも本文にも出さない。
- 既存ファイルを勝手に上書き・削除しない。競合を見つけたら報告する。
- 実在しない成果物の存在を偽らない。未作成は `PENDING` と記録する。
