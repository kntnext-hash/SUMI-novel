# AGENTS｜イベント画像部屋

主担当：アート担当

## 役割

イベントCGの構図と生成指示を作成する。

## この部屋の禁止事項・固有ルール

- 顔の解放前のCGで透花の顔を描かない。解放場面のCGは stage 4 以降の専用シーケンスとして扱う。
- 生成プロンプトには visual_stage と face_visibility を必ず含める。
- 未作成のCGは `docs/ASSET_REGISTRY.csv` に PENDING で登録する。

## 長編イベントCGの画像参照

新規生成、再生成、部分修正の各呼び出しで、次の3枚をこの順で画像入力（ImageGen の `referenced_image_paths`）に指定する。パスはこの部屋を起点に解決する。

1. `private_sources/style_references/桜彩る二人の制服少女.png` — 二人のプロポーション、制服、共通の墨線と透明水彩。
2. `private_sources/style_references/桜舞う透花の水彩インク肖像.png` — 透花の目元、栗色の髪の流れ、リボン。
3. `private_sources/style_references/墨と水彩に咲く澄と白百合.png` — 澄の顔立ち、黒髪の輪郭、墨の濃淡。

修正対象の原画や連続カットは4枚目以降に添え、プロンプトで各画像の役割と修正範囲を示す。構図・表情・衣装・季節・登場人数はその場面の本文に合わせる。小物や無人のカットでは3枚から筆致、紙白、水彩のにじみだけを参照する。採用前に元の3枚と見比べる。

## 共通ルール（全室）

- 正本：`docs/STORY_BIBLE.md` / `docs/COLOR_STAGES.md` / `docs/VISUAL_BIBLE.md`。矛盾を見つけたら独断で解消せず、`rooms/00_制作進行部屋` へ報告する。
- 未確定事項（`docs/OPEN_QUESTIONS.md`）をユーザーの承認前に正史化しない。
- 状態は `DRAFT → REVIEW → APPROVED → INTEGRATED → TESTED` で管理する。**APPROVED はユーザーが承認したときだけ。**
- 顔・色の先出し禁止（`docs/COLOR_STAGES.md`）。第5章まで透花の顔は画面にも本文にも出さない。
- 既存ファイルを勝手に上書き・削除しない。競合を見つけたら報告する。
- 実在しない成果物の存在を偽らない。未作成は `PENDING` と記録する。
