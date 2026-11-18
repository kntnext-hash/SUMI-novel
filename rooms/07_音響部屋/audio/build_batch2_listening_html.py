"""Single offline HTML: exact submitted WAVs, manuscript quotes, initial listening windows."""
import base64, hashlib, html, json, sys
from pathlib import Path
root = Path(__file__).parent
repo = root.parents[2]
workspace = repo.parent
sys.path.insert(0, str(root/'.qc_deps'))
import soundfile as sf
import numpy as np
delivery = root/'delivery'
rights = json.loads((delivery/'batch2_20261119_rights_qc.json').read_text(encoding='utf-8'))
edits = json.loads((delivery/'batch2_20261119_edits_qc.json').read_text(encoding='utf-8'))
records = {r['file']:r for r in rights+edits}
groups = [
 ('傘の雨', '03',171,'C03S03','骨・縁の独立層ではない。近い雨の粒と背景の声・車、ループの継ぎ目を確認。', ['rain_umbrella_close_full.wav','rain_umbrella_close_loop_candidate.wav']),
 ('地面の雨', '03',171,'C03S03','22.05kHzの圧縮音源。高域のざらつきと傘の雨との強さの差を確認。', ['rain_concrete_full.wav','rain_concrete_loop_candidate.wav']),
 ('濡れた道の足音', '03',252,'C03S05','靴音の湿り・人数・歩調と背景交通を確認。走り止まり二歩の音ではない。', ['wet_asphalt_steps_full.wav']),
 ('紙袋', '09',231,'C09S06','短い候補0.31秒が袋の一動作として聞こえるか、余韻が切れていないか全長と比較。', ['paper_bag_handling_full.wav','paper_bag_first_cluster_candidate.wav']),
 ('紙を折る', '06',38,'C06S01','繰り返しの折り音。本文の後方の紙の音に合うか確認。角はじきや布の代用にはしない。', ['paper_folding_full.wav']),
 ('花火の一発', '05',232,'C05S05','作者が一発に分離した音。遠い花火として鋭すぎないか、余韻を確認。映像より後に鳴らす。', ['firework_single_5.wav']),
 ('靴を脱ぐ・履く', '10',218,'C10S05','最初の短区間が履く動作かは未判定。脱ぐ音・紐を結ぶ音を混ぜず履く区間を選ぶ。', ['shoes_off_on_full.wav']),
 ('扉を閉める', '10',218,'C10S05','家の扉として重さ・材質・残響が合うか。靴→閉扉→吸気の順。', ['door_close_medium.wav']),
 ('空缶を入れる', '08',185,'C08S04','一投と跳ね返りか、複数投下かを全長と比較。残液入りの路面二打とは別用途。', ['can_into_trash_full.wav','can_into_trash_first_cluster_candidate.wav']),
 ('木床の踏み鳴らし', '05',58,'C05S02','踏む回数・床の響き・強さを確認。屋外の踵二打に流用しない。', ['foot_stomp_wood_full.wav']),
 ('戸口のベル', 'EA',29,'EAS01','入店時の録音。「閉まる直前のひと鳴り」に使える区間か、開閉音の混入と打数を確認。', ['shop_door_bell_full.wav']),
]
payload = {}
sections = []
manifest = []
for index,(title,prefix,line,node,check,files) in enumerate(groups):
    manuscript = next((repo/'kaononaiharu_long_complete/本文').glob(prefix+'_*'))
    quote = manuscript.read_text(encoding='utf-8-sig').splitlines()[line-1]
    cards=[]
    for name in files:
        row=records[name]
        path=delivery/name
        raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==row['sha256']
        data,rate=sf.read(path,always_2d=True)
        duration=len(data)/rate
        # Listening navigation only: not a new edit or a semantic event boundary.
        if duration<=8:
            start,end=0.,duration
            reason='短い素材なので全長を確認'
        else:
            block=round(.02*rate)
            count=len(data)//block
            rms=np.sqrt(np.mean(data[:count*block].reshape(count,block,-1)**2,axis=(1,2)))
            hot=np.flatnonzero(rms >= max(.005,float(rms.max())*.08))
            start=max(0.,int(hot[0])*block/rate-.15) if len(hot) else 0.
            end=min(duration,start+6.)
            reason='最初の波形活動付近から6秒。動作・混入音は未判定'
        loop=bool(row.get('loop'))
        kind='ループ候補' if loop else ('切出し候補' if 'candidate' in name else '全長素材')
        source=next((r for r in rights if r['file']==row.get('input_file')),row)
        author=source.get('author','')
        payload[name]=dict(data=base64.b64encode(raw).decode('ascii'),start=start,end=end,duration=duration,loop=loop)
        manifest.append(dict(file=name,start=start,end=end,reason=reason,loop=loop,sha256=row['sha256'],manuscript=manuscript.name,line=line,node=node))
        extra=''
        if loop:
            extra='<button class="seam" data-file="'+name+'">継ぎ目を聴く（末尾2秒→先頭2秒）</button>'
        crop=row.get('crop_seconds')
        origin=('元音の %.3f〜%.3f秒。'%tuple(crop)) if crop and 'candidate' in name else ''
        cards.append(f'''<article class="sound"><span class="tag">{kind}</span><h3>{html.escape(name)}</h3>
<p class="meta">全長 {duration:.3f}秒 · {rate/1000:g} kHz · {data.shape[1]} ch</p>
<div class="buttons"><button class="short primary" data-file="{name}">最初に聴く：{start:.2f}〜{end:.2f}秒</button>{extra}</div>
<p class="basis">{html.escape(origin+reason)}。採否の判定はしていません。</p>
<details><summary>全長を聴く・比較する</summary><audio controls preload="none" data-file="{name}" aria-label="{name} 全長"></audio></details>
<p class="credit">{html.escape(author)} · CC0 · <a href="{html.escape(row['source'])}" target="_blank" rel="noopener">配布元</a></p></article>''')
    sections.append(f'''<section id="g{index}"><div class="context"><p class="eyebrow">{index+1:02d} / {node} · 本文{line}行</p><h2>{title}</h2><blockquote>{html.escape(quote)}</blockquote><p class="source">{html.escape(manuscript.name)}</p><p class="check"><strong>採否の確認点</strong><br>{check}</p></div><div class="sounds">{''.join(cards)}</div></section>''')
nav=''.join(f'<a href="#g{i}">{html.escape(g[0])}</a>' for i,g in enumerate(groups))
template='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>顔のない春｜第2便 音響試聴</title><style>
:root{color-scheme:light;--paper:#f5f2eb;--ink:#272b2a;--muted:#666d69;--accent:#226c68}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,"Yu Gothic",sans-serif;line-height:1.7}header,main{max-width:1160px;margin:auto;padding:36px 28px}header{padding-bottom:20px}h1{font-size:clamp(26px,4vw,40px);margin:8px 0 14px;letter-spacing:.04em}h2{font-size:24px;margin:6px 0 18px}h3{font-size:14px;overflow-wrap:anywhere;margin:10px 0 4px}.eyebrow,.tag{font-size:12px;color:var(--accent);letter-spacing:.06em}.intro{max-width:800px}.notice{border-left:3px solid var(--accent);padding:10px 18px;background:#e9efea}nav{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}nav a{color:var(--ink);font-size:13px;text-decoration:none;border:1px solid #cbd1c9;border-radius:20px;padding:5px 12px}a{color:var(--accent)}.toolbar{position:sticky;top:0;z-index:2;background:#f5f2ebf5;border-block:1px solid #d8dacf;padding:12px 24px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}.toolbar span{font-size:13px;overflow-wrap:anywhere}.toolbar label{font-size:13px}input{vertical-align:middle;max-width:140px}button{font:inherit;font-size:13px;border:1px solid #aebeb7;border-radius:5px;padding:9px 13px;background:#fff;cursor:pointer}button:hover{background:#edf4f0}button:focus-visible,summary:focus-visible,a:focus-visible{outline:3px solid #cf941d;outline-offset:3px}.primary{background:var(--accent);color:white;border-color:var(--accent)}.primary:hover{background:#174e4b}section{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:32px;padding:32px 0;border-bottom:1px solid #cfd4cc;scroll-margin-top:110px}blockquote{margin:0;padding-left:17px;border-left:2px solid #c3cbc2;font-family:"Yu Mincho",serif;font-size:16px;line-height:1.95;white-space:pre-wrap}.source,.meta,.basis,.credit{font-size:12px;color:var(--muted)}.check{font-size:14px;background:#e9ede5;padding:14px 16px;margin-top:22px}.check strong{font-size:12px;color:var(--accent)}.sound{background:#fffefb;border:1px solid #d8ded4;border-radius:8px;padding:20px;margin-bottom:14px}.tag{background:#edf2e9;padding:3px 8px;border-radius:4px}.buttons{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}audio{width:100%;margin:12px 0}summary{font-size:13px;cursor:pointer;margin-top:12px}.footer{padding-top:25px;color:var(--muted);font-size:12px}@media(max-width:720px){header,main{padding:22px 16px}section{grid-template-columns:1fr;gap:12px}.toolbar{padding:10px 16px;gap:10px}.toolbar #status{width:100%}.sound{padding:16px}blockquote{font-size:15px}}
</style></head><body><header><p class="eyebrow">SUMI / 顔のない春 / 2026.11.19 / REVIEW</p><h1>本文と聴く、音の候補。</h1><p class="intro">第2便の15WAVを11の動作で比較。まず短い区間、迷ったら全長へ。別の音を再生すると前の音は止まります。</p><div class="notice">音声はこのHTMLに埋め込み済み。ネット接続不要です。<strong>試聴による採否は未判定</strong>。短区間は波形から選んだ案内で、意味のある一動作とは限りません。</div><nav>__NAV__</nav></header><div class="toolbar"><button id="stop">すべて停止</button><label>試聴音量 <input id="volume" aria-label="試聴音量" type="range" min="0" max="1" step="0.05" value="0.65"></label><span id="status" role="status" aria-live="polite">待機中 · 自動再生しません</span></div><main>__SECTIONS__<p class="footer">11件の実録由来WAV＋4件の編集候補。原音・権利・切出し記録は別途納品済み。音量は音源間でラウドネス統一していません。配布元リンク以外の外部依存はありません。</p></main><script type="application/json" id="sounds">__PAYLOAD__</script><script>
const sounds=JSON.parse(document.getElementById('sounds').textContent), cache=new Map();
let ctx,gain,active=null,version=0;const status=document.getElementById('status'),volume=document.getElementById('volume');
function stopAll(message='停止しました'){version++;if(active){try{active.stop()}catch{}active=null}document.querySelectorAll('audio').forEach(a=>a.pause());status.textContent=message;}
async function playWindow(name,seam=false){stopAll('読込中：'+name);const token=version;try{ctx??=new(window.AudioContext||window.webkitAudioContext)();await ctx.resume();if(!gain){gain=ctx.createGain();gain.connect(ctx.destination)}gain.gain.value=Number(volume.value);let buffer=cache.get(name);if(!buffer){const raw=Uint8Array.from(atob(sounds[name].data),c=>c.charCodeAt(0));buffer=await ctx.decodeAudioData(raw.buffer);cache.set(name,buffer)}if(token!==version)return;const s=ctx.createBufferSource();s.buffer=buffer;s.connect(gain);const item=sounds[name];active=s;s.onended=()=>{if(active===s){active=null;status.textContent='確認区間が終了：'+name}};if(seam){s.loop=true;s.loopStart=0;s.loopEnd=buffer.duration;s.start(0,Math.max(0,buffer.duration-2));s.stop(ctx.currentTime+4);status.textContent='継ぎ目を再生中：末尾2秒 → 先頭2秒 · '+name}else{s.start(0,item.start,item.end-item.start);status.textContent='短区間を再生中：'+name}}catch(e){status.textContent='再生できません：'+e.message;console.error(e)}}
document.querySelectorAll('.short').forEach(b=>b.onclick=()=>playWindow(b.dataset.file));document.querySelectorAll('.seam').forEach(b=>b.onclick=()=>playWindow(b.dataset.file,true));document.getElementById('stop').onclick=()=>stopAll();
document.querySelectorAll('audio').forEach(a=>{a.volume=Number(volume.value);a.parentElement.addEventListener('toggle',()=>{if(a.parentElement.open&&!a.src)a.src='data:audio/wav;base64,'+sounds[a.dataset.file].data});a.addEventListener('play',()=>{version++;if(active){try{active.stop()}catch{}active=null}document.querySelectorAll('audio').forEach(other=>{if(other!==a)other.pause()});status.textContent='全長を再生中：'+a.dataset.file});a.addEventListener('ended',()=>status.textContent='全長が終了：'+a.dataset.file)});
volume.oninput=()=>{if(gain)gain.gain.value=Number(volume.value);document.querySelectorAll('audio').forEach(a=>a.volume=Number(volume.value))};
</script></body></html>'''
output=workspace/'builds/audio_batch2_listening_20261119.html'
output.write_text(template.replace('__NAV__',nav).replace('__SECTIONS__',''.join(sections)).replace('__PAYLOAD__',json.dumps(payload,separators=(',',':'))),encoding='utf-8')
(root/'delivery/batch2_listening_windows.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(str(output));print('WAVs',len(payload),'bytes',output.stat().st_size)
