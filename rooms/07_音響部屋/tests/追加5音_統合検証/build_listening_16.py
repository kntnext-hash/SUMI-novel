"""Render a chapter-indexed offline listening review from the shipped Ren'Py cue code."""
import ast
import base64
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import re
import textwrap
from types import SimpleNamespace
import wave

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
GAME = REPO / "game"
previous = HERE.parent / "四候補_統合試写" / "build_listening.py"
spec = importlib.util.spec_from_file_location("pcm_mix", previous)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

# Time markers specify a reader's example pace. All audio cues come from the game.
SCENES = [
 ("第1章", "自転車2台の通過", "2台の山が0.60秒ずれて聞こえるか。挨拶を遮らないか。", "01", [(0,29),(5.8,34)],7.4),
 ("第1章", "学校のチャイム", "校内の距離感と会話に対する音量。", "01", [(0,72)],6),
 ("第1章", "ベルと通り過ぎる自転車", "青の出現は無音。続く一度のベルと、後ろから遠ざかる車輪。","01",[(0,226),(2,227),(7.8,228)],9.4),
 ("第1章", "橋の風", "髪を揺らす風の弱さ、ループの継ぎ目、翌朝の停止。","01",[(0,228),(2,229),(6,230),(10,231),(14,232),(18,237)],20),
 ("第2章", "他の生徒の通知・小音量", "通知を切った本人の携帯と取り違えない距離か。","02",[(0,171)],3),
 ("第2章", "他の生徒の通知・近く", "同じ通知が近くで鳴る場面の差。","02",[(0,179)],3),
 ("第3章", "傘に当たる雨", "雨の粒、読書中の音量、ループの境界。","03",[(0,141)],16),
 ("第3章", "六時のチャイム", "段落を送ってもチャイムの開始は一度だけか。","03",[(0,199),(2.2,199,1)],7),
 ("第4章", "携帯の通知・一度目", "本文の送信と鳴り方の対応。","04",[(0,93)],3),
 ("第4章", "携帯の通知・二度目", "メッセージを受け取った時の短さ。","04",[(0,208)],3),
 ("第6章", "水筒を向かいの机へ", "手前は無音。次の机の一打だけが硬く聞こえるか。回想の段落にも注意。","06",[(0,79),(4,79,1),(6.2,80)],9),
 ("第6章", "電話の着信と停止", "着信音が会話「帰った？」へ重ならないか。","06",[(0,229),(2.5,230)],5),
 ("第7章", "シャッター", "ゴール後の撮影一回に聞こえるか。","07",[(0,106)],3),
 ("第7章", "本が一冊落ちる音", "本の重さと床への接触。","07",[(0,209)],4),
 ("第9章", "映画館の木片・紙・鈴", "木片と紙、一打、手渡しの無音、紙に続く二打の違い。","09",[(0,142),(4,143),(6.5,144),(9,145),(11,146)],15),
 ("第11章", "冷蔵庫と湯を捨てる音", "冷蔵庫の低い持続音と湯捨てを聞き分けられるか。","11",[(0,57)],16),
 ("第11章", "学校のチャイム", "後半で同じチャイムの音量が場面に合うか。","11",[(0,220)],6),
 ("分岐 ERS01", "裏門で遠くに聞こえる流水", "遠い水道に聞こえるか。栓を閉めた行で音が止まるか。","r",[(0,32),(2,33),(5,34),(8,35),(11,36),(16,37)],18)
]
NAMES={"bicycle_pass_full":"車輪","bicycle_bell_single":"ベル","school_chime_original":"チャイム","notification_soft":"通知","ringtone_original":"着信","rain_loop":"雨","fridge_loop":"冷蔵庫","kitchen_sink_loop":"流水","park_wind_loop":"風","thermos_set_down":"水筒","camera_shutter":"シャッター","book_drop":"本の落下","pot_water":"湯捨て","cinema_wood_paper":"木片と紙","cinema_paper_two_bells":"紙と鈴二打","small_bell_single":"鈴一打"}

class Trace(renderer.TrackLog):
    def register_channel(self, *args, **kwargs):
        pass

    def play(self, files, channel, loop, relative_volume, fadein=0):
        if channel in self.active:
            self.stop(channel, 0)
        super().play(files,channel,loop,relative_volume,fadein)

def base_name(item):
    return Path(item.split(">")[-1]).stem

def main():
    sources={}
    for p in (GAME/"audio").glob("*.wav"):
        with wave.open(str(p)) as w:
            pcm=np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").reshape(-1,w.getnchannels())
            assert w.getsampwidth()==2 and w.getnchannels() in (1,2)
            sources[p.name]=(w.getframerate(),np.broadcast_to(pcm,(len(pcm),2)))
    assert set(NAMES)=={Path(s).stem for s in sources}
    script=(GAME/"audio_cues.rpy").read_text("utf8")
    code=textwrap.dedent(script.split("init 10 python:\n",1)[1].split("\ndefine config.",1)[0])
    adv=(GAME/"adv_passages.rpy").read_text("utf8");lines=adv.splitlines()
    parts={(src,int(n),i):ast.literal_eval(lines[int(first)-1+i].strip()) for first,src,n,count in re.findall(r"\((\d+), '(story_[^']+)', (\d+), (\d+)\)",adv) for i in range(int(count))}
    items=[]; observed=set(); all_positions=set(); verification=[]
    for ch,title,question,chapter,markers,duration in SCENES:
        filename="story_end_r.rpy" if chapter=="r" else f"story_ch{chapter}.rpy"
        original=(GAME/filename).read_text("utf8").splitlines()
        trace=Trace()
        engine=SimpleNamespace(music=trace,is_skipping=lambda:False,in_rollback=lambda:False,get_filename_line=lambda:(filename,line))
        env=dict(renpy=engine,adv_original_location=lambda f,l:(f,l,part,1),config=SimpleNamespace(main_menu_stop_channels=[],label_callbacks=[],all_character_callbacks=[]))
        exec(compile(code,"audio_cues.rpy","exec"),env)
        pages=[]
        for time,line,*extra in markers:
            part=extra[0] if extra else 0
            txt=parts.get((filename,line,part))
            if txt is None:txt=ast.literal_eval(original[line-1].strip())
            trace.now=time
            env["play_story_sound"]("begin")
            pages.append(dict(t=time,text=txt,ref=f"{filename} {line}行",sounds=[]))
            all_positions.add((filename,line,part))
        for e in trace.events:
            names=[]
            for clip in e["files"] if isinstance(e["files"],list) else [e["files"]]:
                if clip.startswith("<silence"):continue
                k=base_name(clip);observed.add(k);names.append(NAMES[k])
            for page in pages:
                if page["t"]==e["at"]:
                    page["sounds"]+=names
        pcm=renderer.mix(trace.events,duration,sources)
        if title.startswith("水筒"):
            assert len(trace.events)==1 and trace.events[0]["at"]==4 and not pcm[:4*renderer.RATE].any() and not pcm[6*renderer.RATE:].any()
        if title in ("橋の風","裏門で遠くに聞こえる流水"):
            assert not pcm[round(trace.events[0]["stop"]*renderer.RATE):].any()
        buf=io.BytesIO()
        with wave.open(buf,"wb") as w:
            w.setparams((2,2,renderer.RATE,0,"NONE","not compressed"));w.writeframes(pcm.tobytes())
        wav=buf.getvalue();encoded=base64.b64encode(wav).decode()
        assert base64.b64decode(encoded)==wav
        items.append(dict(ch=ch,title=title,question=question,pages=pages,wav=encoded))
        verification.append(dict(scene=title,duration=duration,events=trace.events,wav_sha256=hashlib.sha256(wav).hexdigest()))
    assert observed==set(NAMES) and set(env['story_sound_cues'])<=all_positions and set(env['story_ambience_cues'])<=set(x[:2] for x in all_positions)
    title="顔のない春｜製品版16音の試聴"
    data=json.dumps(items,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    template=(HERE/"listening_16_template.html").read_text("utf8")
    credits=html.escape((GAME/"licenses/AUDIO_SOURCES.md").read_text("utf8"))
    credits=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'\1　\2',credits)
    credits=re.sub(r'(https?://[^\s）|]+)',r'<a href="\1">\1</a>',credits)
    out=template.replace("{{TITLE}}",title).replace("{{DATA}}",data).replace("{{CREDITS}}",credits)
    dest=REPO.parent/"builds"/"顔のない春_ADV製品16音_本文付き試聴.html";dest.write_text(out,"utf8")
    checks=dict(game_audio_cues_sha256=hashlib.sha256((GAME/"audio_cues.rpy").read_bytes()).hexdigest(),
                source_wavs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((GAME/"audio").glob("*.wav"))},scenes=verification)
    (HERE/"listening_16_verified.json").write_text(json.dumps(checks,ensure_ascii=False,indent=2)+"\n","utf8")
    print(len(items),len(observed),len(out))

if __name__=="__main__": main()
