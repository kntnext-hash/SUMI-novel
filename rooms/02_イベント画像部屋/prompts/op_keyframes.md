# OPキーフレーム生成プロンプト（10カット）

2026-11-13、ユーザーの依頼で澪が作成。プロトタイプOP（約30秒、各カット約3秒）の場面画像10枚を生成するための指示。
共通ルール：全カット `face_visibility: none`（顔は描かない）。色は stage 0（無彩）を基本とし、stage 1 のカットでも**青は空の領域だけ**。赤・ピンク等の彩色は一切禁止（VISUAL_BIBLE／COLOR_STAGES の先出し禁止に従う）。
出力：1920×1080（16:9）、ファイル名 `op_cut01.png` 〜 `op_cut10.png`、保存先 `rooms/02_イベント画像部屋/assets/op/`。

## 共通スタイル（全カットのプロンプト末尾に付ける）

```
Japanese sumi-e ink painting with delicate watercolor wash on textured washi paper, ink outlines with brush variation, dry-brush strokes and ink bleeding, no cel shading, no flat anime coloring, no text, no letters, no numbers, no watermark, cinematic 16:9 composition
```

## 共通ネガティブ

```
no faces, no facial features, no eyes, no noses, no mouths, people appear only as faceless silhouettes seen from behind or far away, no red, no pink, no orange, no warm colors
```

## カット一覧

### cut01｜通学路の朝（visual_stage: 0 / face_visibility: none）
```
A quiet school road in a small Japanese town in early morning, empty street, utility poles and power lines, houses and low mountains in the distance, entirely monochrome sumi-e ink gradations from deep black to pale gray, misty air, generous negative space
```

### cut02｜電線と空（visual_stage: 0 / face_visibility: none）
```
Low angle view of a pale gray sky crossed by black power lines and a utility pole, a single crow silhouette perched on a wire far away, monochrome ink wash, the sky rendered as layered gray washes with soft bleeding edges, quiet and still
```

### cut03｜駅ホームの群衆（visual_stage: 0 / face_visibility: none）
```
A train station platform in the morning, a crowd of commuters seen only from behind as dark ink silhouettes with softly blurred outlines, a train arriving with motion blur, monochrome sumi-e, no individual faces, anonymous and quiet atmosphere
```

### cut04｜透花の後ろ姿（visual_stage: 0 / face_visibility: none）
キャラクター参照（`rooms/03_その他素材生成部屋/characters/references/ref_face_duo_full_color.jpg`）を入力し、髪型とシルエットだけを参照する。色はコピーせず、顔は描かない。
```
A high school girl seen from behind, long wavy hair reaching her chest and a large ribbon on the side of her head, school uniform and a school bag, standing still on a quiet street, rendered entirely in monochrome ink tones, the ribbon and hair expressed only through ink gradation, lonely and gentle mood
```

### cut05｜すれ違う二人（visual_stage: 0 / face_visibility: none）
参照は cut04 と同じ。2人は向き合わず、すれ違う構図にする。
```
Two high school girls passing each other on a narrow street, both seen from behind and in profile silhouette at a distance, one with long straight black hair and one with long wavy hair and a side ribbon, a quiet gap of empty space between them, monochrome sumi-e ink wash, no faces visible
```

### cut06｜教室の窓辺（visual_stage: 0 / face_visibility: none）
```
An empty classroom in soft gray light, rows of desks, a window with a curtain gently lifted by the wind, pale ink wash, dust in the air, monochrome, stillness of early spring before anyone arrives
```

### cut07｜水たまりの空（visual_stage: 1 / face_visibility: none）
色は映り込む空の端の、ごく薄い青のみ。
```
A rain puddle on an asphalt road reflecting a gray sky, monochrome ink painting, only at the very edge of the reflected sky a faint pale blue wash begins to bleed into the gray, subtle and quiet, ripples spreading slowly
```

### cut08｜空に青が滲む（visual_stage: 1 / face_visibility: none）
第1章末キュー（CUE_ch01_blue）と対になるカット。青は空だけに、画面の約1/4まで。
```
A wide sky above a small town with power lines, most of the image in monochrome ink gray, from the upper corner a soft pale blue watercolor wash bleeds and spreads into the sky like ink in water, the blue covers about a quarter of the sky, the town below remains monochrome
```

### cut09｜桜の木（visual_stage: 1 / face_visibility: none）
桜は色付けしない（ピンク禁止）。花は墨の濃淡で描き、空の青だけが残る。
```
A cherry tree in full bloom drawn entirely in monochrome ink gradations, the blossoms expressed in pale gray washes without any pink, petals falling quietly, behind the branches a sky with a faint pale blue wash, the rest of the scene monochrome
```

### cut10｜タイトル背景（visual_stage: 1 / face_visibility: none）
上半分はタイトル文字を置く余白として空ける。
```
A wide quiet landscape of a school road leading toward low mountains under a broad sky, the upper half of the image is mostly empty pale sky with a gentle pale blue watercolor wash, the road and town below in monochrome ink, large negative space in the upper half for a title, serene ending mood
```

## 生成後の扱い

- 生成した画像は `docs/ASSET_REGISTRY.csv` の OP_cut01〜10 を PENDING から更新する。
- 動き付け（パン／ズーム／滲み／動画化）は素材の段階では行わない。実装・演出側の工程で扱う。
- 顔が描かれたカット、青以外の色が入ったカットは採用しない（先出し禁止違反として差し戻す）。
