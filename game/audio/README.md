# 同梱音源

notification_soft.wav と school_chime_original.wav は、本作向けに正弦波・倍音・包絡線から独自生成した音源。第三者サンプルは使用していない。
制作ソースは rooms/07_音響部屋/audio/generate_tones.py、本文対応は同README。
初期実装の音量は暫定。再生APIの動作確認と聴覚による音色・バランス評価は別途記録する。

追加のringtone_original.wavも同じ独自合成方式。第6章C06S06の着信に一周期だけ再生し、会話「帰った？」の開始時に止める。第4章C04S03の「電話はそれからもう一回だけ鳴った」はメッセージ文脈のためnotification_soft.wavを使用する。

雨と冷蔵庫の実録ループを追加（REVIEW）。出典と加工記録はgame/licenses/AUDIO_SOURCES.md。
第3章C03S03の傘を差す本文（rpy141）と、第11章C11S02の冷蔵庫の音（rpy57）で再生。次のnode進入で停止し、タイトル復帰時も停止する。専用story_ambienceチャンネルをsfxミキサーへ接続し、効果音の音量設定を共有する。通知などの単発音はsoundチャンネルを維持。
両素材の録音対象と本文対応を照合。音色・バランス・ループ境界の聴覚評価は未完了。
