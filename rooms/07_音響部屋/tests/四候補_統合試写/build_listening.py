"""Build four self-contained audition scenes from the integration patch."""
import ast
import base64
import hashlib
import html
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
DELIVERY = REPO / "rooms" / HERE.parents[1].name / "audio" / "delivery"
GAME = REPO / "game"
TARGET = REPO.parent / "builds" / "顔のない春_追加4候補_本文付き試聴.html"
RATE = 48000
PATCH = (HERE / "four_candidate_cues.rpy").read_text("utf8")
FUNCS = [n for n in ast.parse(textwrap.dedent(PATCH.split("init 15 python:\n")[1])).body if isinstance(n, ast.FunctionDef)]

SCENES = [
    ("橋で並ぶ自転車", "story_ch01.rpy", [(0,29),(5.8,34)],7.4,"2台の通過音の山は0.60秒差。先に聞こえる方を0.38、後の方を0.25に設定。"),
    ("青を見つけた後のベル", "story_ch01.rpy", [(0,226),(2,227),(7.8,228)],9.4,"青の出現は無音。2秒でベルを1回開始し、0.45秒後に1台の通過音。ベル0.31、通過音0.30。"),
    ("橋の風から翌朝へ", "story_ch01.rpy", [(0,228),(2,229),(6,230),(10,231),(14,232),(18,237)],20,"2秒で風を開始。11.7秒のループ境界を通り、18秒の翌朝で停止。相対音量0.22。"),
    ("裏門の会話と遠い流水", "story_end_r.rpy", [(0,32),(2,33),(5,34),(8,35),(11,36),(16,37)],18,"2秒の「二等？」で流水を開始。11.7秒のループ境界を通り、16秒の栓を閉める一文で即時停止。相対音量0.13。")
]

class TrackLog:
    def __init__(self):
        self.active = {}
        self.events = []
        self.now = 0.0

    def get_playing(self, ch):
        event = self.active.get(ch)
        return event["files"] if event else None

    def play(self, files, channel, loop, relative_volume, fadein=0):
        event = dict(files=files, channel=channel, at=self.now, loop=loop, gain=relative_volume, fade=fadein)
        self.active[channel] = event
        self.events.append(event)

    def stop(self, channel, fadeout):
        event = self.active.pop(channel, None)
        if event:
            event.update(stop=self.now, release=fadeout)

def cue_log(source, markers):
    music = TrackLog()
    renpy = SimpleNamespace(music=music, is_skipping=lambda:False, in_rollback=lambda:False,
                            get_filename_line=lambda:(source,line))
    ns = dict(renpy=renpy, adv_original_location=lambda f,l:(f,l,0,1), four_bike_channels=("four_bike_near","four_bike_far"))
    exec(compile(ast.Module(body=FUNCS,type_ignores=[]), "four_candidate_cues.rpy", "exec"),ns)
    for point,line in markers:
        music.now=point
        ns["four_audio"]("begin")
    return music.events

def mix(events, duration, sources):
    out=np.zeros((round(duration*RATE),2),np.float64)
    for e in events:
        pos=e["at"]
        for item in (e["files"] if isinstance(e["files"],list) else [e["files"]]):
            silence=re.fullmatch(r"<silence ([\d.]+)>",item)
            if silence:
                pos+=float(silence[1])
                continue
            m=re.fullmatch(r"(?:<from ([\d.]+) to ([\d.]+)>)?audio/(.+)",item)
            assert m,item
            rate,raw=sources[m[3]]
            start=float(m[1] or 0)
            end=float(m[2]) if m[2] else len(raw)/rate
            length=round((end-start)*RATE)
            indices=np.arange(length)*rate/RATE+round(start*rate)
            clip=np.stack([np.interp(indices,np.arange(len(raw)),raw[:,i]) for i in range(2)],axis=1)
            stop=e.get("stop",duration)
            count=min(len(out)-round(pos*RATE),round((stop+e.get("release",0)-pos)*RATE))
            if not e["loop"]:count=min(count,length)
            if count<=0:continue
            frames=np.arange(count)
            layer=clip[frames%length]
            gain=np.full(count,e["gain"])
            if e["fade"]:
                gain*=np.minimum(1,frames/(RATE*e["fade"]))
            if e.get("release"):
                gain*=np.minimum(1,np.maximum(0,(stop+e["release"]-pos-frames/RATE)/e["release"]))
            out[round(pos*RATE):round(pos*RATE)+count]+=layer*gain[:,None]
            pos+=count/RATE
    assert np.max(np.abs(out))<32767
    return np.rint(out).astype("<i2")

def main():
    sources={}
    for asset in json.loads((HERE/"assets.json").read_text()):
        f=DELIVERY/asset["file"]
        assert hashlib.sha256(f.read_bytes()).hexdigest()==asset["sha256"]
        with wave.open(str(f)) as w:
            assert w.getsampwidth()==2 and w.getnchannels() in (1,2)
            raw=np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").reshape(-1,w.getnchannels())
            sources[f.name]=(w.getframerate(),np.broadcast_to(raw,(len(raw),2)))
    sections=[]; proof=[]
    for idx,(title,file,markers,duration,detail) in enumerate(SCENES):
        events=cue_log(file,markers)
        assert len(events)==[2,2,1,1][idx]
        if idx==0:
            assert [e["gain"] for e in events]==[.38,.25] and events[0]["files"].startswith("<from 2.15 to 7.3>") and events[1]["files"].startswith("<from 1.55 to 6.8>")
        elif idx==1:
            assert [e["at"] for e in events]==[2,2] and events[0]["files"]=="audio/bicycle_bell_single.wav" and events[1]["files"][0]=="<silence 0.45>"
        else:
            assert events[0]["at"]==2 and events[0]["stop"]==[18,16][idx-2] and events[0]["loop"]
        pcm=mix(events,duration,sources)
        if idx:
            assert not pcm[:2*RATE].any()
        if idx>=2:
            end=round(events[0]["stop"]*RATE);assert not pcm[end:].any() and pcm[14*RATE:15*RATE].any()
        buf=io.BytesIO()
        with wave.open(buf,"wb") as w:
            w.setparams((2,2,RATE,0,"NONE","not compressed"));w.writeframes(pcm.tobytes())
        wav=buf.getvalue();b64=base64.b64encode(wav).decode()
        with wave.open(io.BytesIO(base64.b64decode(b64)),"rb") as w:
            assert w.readframes(w.getnframes())==pcm.tobytes()
        original=(GAME/file).read_text("utf8").splitlines()
        texts=[(t,ast.literal_eval(original[n-1].strip())) for t,n in markers]
        cue_buttons="".join(f'<button type="button" data-t="{t}">{t:g}秒</button>' for t,_ in texts)
        text_data=html.escape(json.dumps(texts,ensure_ascii=False),quote=True)
        sections.append(f'<section data-lines="{text_data}"><h2>{title}</h2><p>{detail}</p><blockquote>{html.escape(texts[0][1])}</blockquote><audio controls preload="none" src="data:audio/wav;base64,{b64}"></audio><div aria-label="本文の送り位置">{cue_buttons}</div></section>')
        proof.append(dict(scene=title,seconds=duration,events=events,sha256=hashlib.sha256(wav).hexdigest()))
    document="""<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>顔のない春｜追加4候補の試聴</title>
<style>*{box-sizing:border-box}body{max-width:800px;margin:3rem auto;padding:0 1.25rem;background:#f7f5ef;color:#25251f;font-family:system-ui,sans-serif;line-height:1.75}h1,h2,blockquote{font-family:serif}section{padding:1rem 0 2rem;border-top:1px solid #a7a18e}blockquote{margin:1em 0;padding:.8em 1.2em;border-left:3px solid #97886b;background:#fff;min-height:5em}audio{width:100%}button{cursor:pointer;padding:.35em .8em;margin:.45em .4em 0 0}button[aria-current=true]{background:#373c33;color:white}a{color:#374a3f}</style>
<h1>顔のない春｜追加4候補の試聴</h1><p>再生中の本文は音に合わせて切り替わります。秒数を押すとその本文位置に移動します。本文を送る間隔は試聴用の例です。各音には試写案の相対音量を適用し、音量の自動調整はしていません。</p>"""+"".join(sections)+"""
<h2>録音の出典</h2><ul><li><a href="https://freesound.org/people/13gkopeckak/sounds/378911/">自転車ベル · 13gkopeckak / Freesound 378911</a></li><li><a href="https://freesound.org/people/beskhu/sounds/276001/">自転車通過 · beskhu / Freesound 276001</a></li><li><a href="https://opengameart.org/content/park-ambiences">風 · Thimras / Park Ambiences</a></li><li><a href="https://opengameart.org/content/general-household-sound-effects">流水 · bretbernhoft / General Household Sound Effects</a></li></ul><p>4録音はすべて <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>。ベル・通過音は元録音から区間を採り、風・流水は継ぎ目を処理した納品版を使用しました。</p>
<script>const slots=[...document.querySelectorAll("section")];for(const s of slots){const a=s.querySelector("audio"),lines=JSON.parse(s.dataset.lines),btn=[...s.querySelectorAll("button")];function update(){let i=0;while(i+1<lines.length&&a.currentTime>=lines[i+1][0])i++;s.querySelector("blockquote").textContent=lines[i][1];btn.forEach((b,j)=>b.setAttribute("aria-current",String(i===j)));}for(const b of btn)b.addEventListener("click",()=>{a.currentTime=Number(b.dataset.t);update()});a.addEventListener("play",()=>slots.forEach(t=>{const n=t.querySelector("audio");if(n!==a)n.pause()}));for(const e of ["timeupdate","seeked","loadedmetadata"])a.addEventListener(e,update);update()}</script></html>"""
    TARGET.write_text(document,"utf8")
    (HERE/"本文付き試聴_生成検査.json").write_text(json.dumps(proof,ensure_ascii=False,indent=2)+"\n","utf8")
    print(TARGET.name,TARGET.stat().st_size)

if __name__=="__main__": main()
