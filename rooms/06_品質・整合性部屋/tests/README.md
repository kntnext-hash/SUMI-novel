# 長編Ren’Py到達テスト

状態はREVIEW。00室が配布版の複製環境で実行するためのテスト。エンジンへの組込み・実行は未実施。

qa_story_all.rpy と qa_image_expectations.json をテスト用配布版の game にコピーし、配布版ディレクトリで実行する。

```powershell
.\kaononaiharu.exe test qa_story_all
```

同梱 renpy/test/testexecution.py の test コマンド、testparser.py の testcase・advance until・click・run・Python文を使用。画面を描画できるWindows環境が必要。全8回の通読なので実行時間は長い。各選択肢／END待ちの上限は1800秒。

初周A/B/C/D、再読A/B/C/Dの順に通常の start / reread_start から進行する。第6章の二択はA/Cで前者、B/Dで後者。場面への直接ジャンプを使わず、UIの選択肢をクリックする。

statement_callbacks の現在ファイル・行と label_callbacks を記録し、各ルートで期待する全本文行とノードに到達したことを終了後に検証する。期待値は現行18本の story*.rpy の行番号を固定したもの。99ノード、本文2586行＋END表示4行を初周・再読の両方で網羅する。ソースに行追加が入れば期待値も更新が必要。

各ルート完了時に配布版直下 qa_story_coverage.json を更新する。8件の結果、missing_labels / missing_lines がすべて空、エンジンのテスト成功を完了条件とする。タイトルに早期復帰しても不足行で失敗する。本文実行中に reread の値も検査する。

最初に persistent.unlocked_reread をFalseにするため、専用のユーザーデータ領域で実行すること。各ENDでTrueになることと、再読開始前に解放済みであることを検証する。メインメニューの再読ボタンの解放表示、セーブロード、画像画素の合否は00室の実機検証で扱う。

画像検証はall_character_callbacksのbeginで行う。say実行前に完了したsceneを、masterレイヤーのget_showing_tagsとget_attributesで照合する。全178キューを元TSV順で保持し、同じ行の4か所の重複指示は最後を表示期待値とする。上書きされた指示も同じ行の処理対象IDとして記録するが、その画像が描画された証明とはしない。

キューのないsayでは直前の期待画像を保持する。END表示4行はblackを期待する。全2590行の照合到達と、8ルート終了時に初周・再読のそれぞれで178キューIDを網羅したことを必須にした。余分なmaster画像も不一致になる。失敗時はqa_image_failure.jsonへ位置・期待画像・実画像・同一行キューを保存する。coverageにはimage_checked・cue_ids_checked・missing_imagesを追加する。

この検査は表示画像名と属性の一致を扱う。画像ファイル内容の正しさや遷移途中の画素は画像QAと実機確認で扱う。期待値JSONは現在の配布版と同じ行配置のrenpy_test_run/gameから本文をscenario.jsonと照合して生成し、178キューすべての画像名が配布版に定義されていることを確認した。実行中プロセスへの変更は行っていない。

ソース読解・静的照合・追加Pythonの構文検査まで実施。追加した画像照合のエンジン実行は00室待ち。
