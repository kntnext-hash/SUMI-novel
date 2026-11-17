"""Create a local audition page with exact candidate WAVs and source records."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import wave

PRIORITY = {
    "small_bell_single.wav": ("鈴・一打", "一度だけ鳴るか。余分な打音や声がないか。"),
    "small_bell_double_preview.wav": ("鈴・二打", "はっきり二度鳴るか。間隔が不自然でないか。"),
    "can_single.wav": ("缶", "落下音として自然か。残液入り缶には別素材が必要か。"),
    "paper_crushed_-_1.wav": ("紙を握る", "紙のぐしゃっとした音か。破る音に聞こえないか。"),
    "camera_shutter.wav": ("シャッター", "一回の撮影音として自然か。"),
    "rain_loop.wav": ("雨", "傘に当たる雨として自然か。繰返しの継ぎ目が目立たないか。"),
    "fridge_loop.wav": ("冷蔵庫", "静かな台所で使える機械音か。繰返しの継ぎ目が目立たないか。"),
    "notification_soft.wav": ("通知", "耳に刺さらないか。短いメッセージ通知として自然か。"),
    "school_chime_original.wav": ("学校チャイム", "学校のチャイムとして違和感がないか。"),
    "ringtone_original.wav": ("着信", "会話前の着信として違和感がないか。"),
}


def build(project, output):
    project, output = project.resolve(), output.resolve()
    if output.exists():
        raise ValueError("Use a fresh output directory.")
    delivery = project / "rooms/07_音響部屋/audio/delivery"
    files = {p.name: p for p in delivery.glob("*.wav")}
    files.update({p.name: p for p in (project / "game/audio").glob("*.wav")})
    output.mkdir(parents=True)
    (output / "audio").mkdir()
    (output / "records").mkdir()
    records = list(delivery.glob("*.json")) + list((delivery.parent).glob("*rights*.json"))
    for source in records:
        shutil.copy2(source, output / "records" / source.name)
    rows, cards = [], []
    for name in list(PRIORITY) + sorted(set(files) - set(PRIORITY)):
        source = files.get(name)
        if source is None:
            continue
        with wave.open(str(source), "rb") as stream:
            duration = stream.getnframes() / stream.getframerate()
        target = output / "audio" / name
        shutil.copy2(source, target)
        adopted = source.parent == project / "game/audio"
        row = {"file": name, "source": source.relative_to(project).as_posix(),
               "seconds": duration, "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
               "in_game": adopted, "listening": "PENDING"}
        rows.append(row)
        label, question = PRIORITY.get(name, (name, "録音対象・余分な音・音量・本文場面への適合を確認。"))
        cards.append('<section><h2>' + html.escape(label) + '</h2><p>' + html.escape(name)
                     + f' · {duration:.2f}秒 · ' + ('組込み済み・試聴待ち' if adopted else '候補・未採用')
                     + '</p><audio controls preload="none" src="audio/' + html.escape(name, quote=True)
                     + '"></audio><p>' + html.escape(question) + '</p></section>')
    page = '''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>顔のない春 音の確認</title><style>body{font:18px/1.7 system-ui;max-width:850px;margin:36px auto;padding:0 20px;background:#f4f1ea;color:#242424}section{background:white;border:1px solid #ccc;padding:20px;margin:20px 0;border-radius:8px}h2{font-size:22px;margin:0}audio{width:100%}p{overflow-wrap:anywhere}</style>
<h1>顔のない春 — 音の確認</h1><p>最初の10点が優先です。再生は自動では始まりません。素材単体の音量であり、ゲーム内の音量調整は反映していません。REVIEW・全点の聴覚確認は未完了です。</p>
<p>音が違う・余分な音がある場合は「ファイル名と気になった点」を伝えてください。出典・加工記録は同梱records、実ファイルのハッシュはmanifest.jsonです。</p>'''
    (output / "音の確認.html").write_text(page + "\n".join(cards) + "</html>", encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "files": len(rows), "priority": len(PRIORITY)}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(Path(__file__).resolve().parents[1], args.output)
