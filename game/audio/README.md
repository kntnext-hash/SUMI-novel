# 同梱音源

notification_soft.wav と school_chime_original.wav は、本作向けに正弦波・倍音・包絡線から独自生成した音源。第三者サンプルは使用していない。
制作ソースは rooms/07_音響部屋/audio/generate_tones.py、本文対応は同README。
初期実装の音量は暫定。再生APIの動作確認と聴覚による音色・バランス評価は別途記録する。

追加のringtone_original.wavも同じ独自合成方式。第6章C06S06の着信に一周期だけ再生し、会話「帰った？」の開始時に止める。第4章C04S03の「電話はそれからもう一回だけ鳴った」はメッセージ文脈のためnotification_soft.wavを使用する。
