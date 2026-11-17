# Windows確認版の組立て

Windows上のPython標準ライブラリだけを使用する。ゲームのローカル画像・GUI・フォントを復元した作業コピーと、既存Windows配布物のRen’Pyランタイムが必要。
game/images・game/gui・game/fontsはGit管理外。これらが欠けるクリーンチェックアウトだけでは配布版を作れない。

```powershell
python tools/build_windows_review.py --runtime C:/path/to/kaononaiharu-0.9-full-light-win --output C:/path/to/new-review-win
```

出力は既存ディレクトリを指定できない。runtime/sourceの内側や祖先も禁止する。必要な画像・フォント・OP・ライセンスとSDK依存GUI補助コードの不在を検査してからコピーする。
ゲーム側の古いrpyc、saves、cache、qa_*を除外し、config.developer=Falseを配布物だけに追加する。
build_manifest.jsonはコピー元gameファイルと全同梱ファイルのSHA256を記録する。

`windows_icon.py`は新しい出力先exeのアイコンだけを更新する。Win32の[リソース更新API](https://learn.microsoft.com/en-us/windows/win32/menurc/adding-deleting-and-replacing-resources)を使用し、失敗時は未確定の変更を破棄する。更新後、実行せずにリソースを読み戻し、ICOの4画像と他リソース全件のバイト一致を検査する。元ランタイムのexeは変更しない。

## 2026-11-18 r3更新

- 電話通知・着信・停止の修正と作品アイコンを収録。4サイズのexeアイコン埋込み後に通常起動・OPからタイトルへの復帰・タイトルバー表示、lint exit 0を確認。
- ZIP：240,591,966 bytes、1712 entries、CRC全件合格。SHA256は `e5d81ccfe0477f3d929976ffe1aeb651cb728db493824085766e50045d9c24d1`。
- r3のgame/ui/APP_ICON.mdは組立て前の旧記述。本ソース側ではexeへの反映完了へ訂正済み。
- 音響仕上げ・試聴と最終統合検査は引き続き未完了。r3もREVIEW。

```powershell
python tools/package_windows_review.py C:/path/to/new-review-win C:/path/to/new-review-win.zip
```

ZIP作成前に台帳の全ファイルのサイズ・SHA256を再検査する。台帳にない起動後のキャッシュ・ログ・セーブは収録しない。圧縮後は全エントリーのCRCを検査し、ZIPのSHA256を隣接JSONへ出力する。

## 2026-11-18実績

- 確認版：workspace/builds/kaononaiharu-review-20261118-win
- ZIP：240,392,555 bytes、1708 entries、CRC全件合格。
- SHA256：5c8ea77db540dc1a674ee23fe1d8e92d7d5ecf3947b1fb8a954b51c4e293603a
- コピー元のDesktop配布物とは別のフォルダにあるexeでlint（exit 0）と引数なし通常起動を確認。
- タイトル→本編冒頭→ページ1スロット1保存→1行進行→日本語確認を経てロードし、元の本文・画像へ復帰。
- 新保存先は%APPDATA%/RenPy/kaononaiharu-long-1。旧試作版や旧0.9配布物の保存先とは分離。既存セーブの自動移行は行わない。
- 音響の残作業・聴覚確認などは継続中。この成果物はREVIEWであり、商品版完成の判定ではない。
