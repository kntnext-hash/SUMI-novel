"""Decode every final video frame and audio sample, create timestamped review sheets."""
from pathlib import Path
import sys, subprocess, json, hashlib, math
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'python_lib'))
import numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
F=imageio_ffmpeg.get_ffmpeg_exe();Q=R/'qa';Q.mkdir(exist_ok=True)
result=[]
for name,seconds,w,h in [('vertical',15,1080,1920),('horizontal',30,1920,1080)]:
 if len(sys.argv)>1 and sys.argv[1]!=name:continue
 p=R/f'deliverables/kaononaiharu_{name}_{seconds}s.mp4'
 meta=subprocess.run([F,'-hide_banner','-i',str(p)],capture_output=True,text=True,encoding='utf8',errors='replace').stderr
 (Q/f'{name}_streams.txt').write_text(meta,encoding='utf8')
 check=subprocess.run([F,'-v','error','-xerror','-i',str(p),'-f','null','-'],capture_output=True,text=True,encoding='utf8',errors='replace')
 assert check.returncode==0,check.stderr
 dw,dh=(90,160) if name=='vertical' else (160,90)
 data=subprocess.run([F,'-v','error','-i',str(p),'-vf',f'scale={dw}:{dh}','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True).stdout
 frames=np.frombuffer(data,np.uint8).reshape(-1,dh,dw,3)
 assert len(frames)==seconds*30,(name,len(frames))
 assert f'{w}x{h}' in meta
 assert 'yuv420p' in meta and 'aac' in meta and '48000 Hz' in meta
 means=frames.mean((1,2,3));assert means.min()>15
 a=subprocess.run([F,'-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True,check=True).stdout
 audio=np.frombuffer(a,np.float32).reshape(-1,2)
 peak=float(abs(audio).max());assert peak<1
 chunks=[float(np.sqrt(np.mean(audio[t*48000:(t+1)*48000]**2))) for t in range(seconds)]
 indices=sorted(set(list(range(0,seconds*30,30))+[seconds*30-1]+([149,150,299,300,359,360] if name=='vertical' else [149,150,299,300,479,480,779,780])))
 times=[n/30 for n in indices]
 selector='select='+ '+'.join(f'eq(n\\,{n})' for n in indices)
 subprocess.run([F,'-v','error','-y','-i',str(p),'-vf',selector,'-fps_mode','vfr','-q:v','2',str(Q/f'{name}_frame_%03d.jpg')],check=True)
 thumbs=[]
 for idx,t in enumerate(times):
  path=Q/f'{name}_frame_{idx+1:03d}.jpg'
  im=Image.open(path).convert('RGB');im.thumbnail((216,384) if name=='vertical' else (480,270));thumbs.append((t,im))
 cw,ch=(226,414) if name=='vertical' else (490,300);cols=5 if name=='vertical' else 3
 sheet=Image.new('RGB',(cw*cols,ch*math.ceil(len(thumbs)/cols)), '#e8e5df');draw=ImageDraw.Draw(sheet)
 for i,(t,im) in enumerate(thumbs):
  x=i%cols*cw;y=i//cols*ch;sheet.paste(im,(x,y));draw.text((x+5,y+ch-24),f'{t:.3f} s',fill='#222222')
 sheet.save(Q/f'{name}_contact.jpg',quality=93)
 result.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'width':w,'height':h,'fps':30,'frames_decoded':len(frames),'duration_seconds':seconds,'full_decode_errors':check.stderr,'minimum_frame_luma_mean':float(means.min()),'audio_samples_per_channel':len(audio),'audio_peak_dbfs':20*math.log10(peak),'audio_clipped_samples':int((abs(audio)>=1).sum()),'audio_rms_each_second':chunks,'audio_last_10ms_peak':float(abs(audio[-480:]).max()),'visual_review_timestamps':times})
 (Q/'technical_QA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(name,'PASS',len(frames),'frames;',round(20*math.log10(peak),2),'dBFS',flush=True)
