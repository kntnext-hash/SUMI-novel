# ADV版 Windows 配布ZIPの音源検査

2026-11-19、kaononaiharu-adv-split-win.zip の game/audio 内にある全WAVを展開し、全尺のPCMサンプルからピークとRMSを算出した。9点とも制作原本とバイト単位で一致し、無音ファイルとフルスケール到達サンプルは0件。RMSは左右全サンプルの二乗平均平方根。値はゲーム内の音量設定適用前。

| WAV | 秒 | Hz | ch | ピーク dBFS | RMS dBFS |
|---|---:|---:|---:|---:|---:|
| camera_shutter.wav | 0.880 | 44100 | 2 | -8.0 | -34.0 |
| cinema_paper_two_bells.wav | 2.627 | 48000 | 2 | -6.0 | -23.7 |
| cinema_wood_paper.wav | 1.797 | 48000 | 2 | -8.0 | -33.0 |
| fridge_loop.wav | 6.700 | 44100 | 1 | -12.0 | -23.4 |
| notification_soft.wav | 0.650 | 48000 | 1 | -9.9 | -23.1 |
| rain_loop.wav | 3.850 | 48000 | 2 | -6.0 | -22.8 |
| ringtone_original.wav | 2.200 | 48000 | 1 | -9.9 | -25.5 |
| school_chime_original.wav | 4.000 | 48000 | 1 | -9.9 | -22.3 |
| small_bell_single.wav | 1.400 | 44100 | 2 | -6.0 | -23.9 |

同梱の game/audio/README.md は通知・着信・学校チャイムの3点を本作向け独自合成と記載。残り6点について game/licenses/AUDIO_SOURCES.md と CINEMA_SOUND_TIMELINE.json にCC0素材の出典・加工記録がある。音色、ゲーム内での音量バランス、鈴の打数の聞こえ方、ループの継ぎ目は未試聴。
