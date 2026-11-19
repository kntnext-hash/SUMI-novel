from pathlib import Path
import sys, subprocess, json
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'python_lib'))
import imageio_ffmpeg
F=imageio_ffmpeg.get_ffmpeg_exe()
P=R/'project/public'
for duration,bell in [(15,1.6),(30,17.0)]:
 graph=f'[0:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume=0.48,afade=t=in:d=0.5,afade=t=out:st={duration-2}:d=2[w];[1:a]volume=0.65,adelay={int(bell*1000)}:all=1[b];[w][b]amix=inputs=2:normalize=0,alimiter=limit=0.8:level=false,aresample=48000[a]'
 subprocess.run([F,'-hide_banner','-loglevel','error','-y','-stream_loop','-1','-i',str(P/'park_wind_loop.wav'),'-i',str(P/'bicycle_bell_single.wav'),'-filter_complex',graph,'-map','[a]','-t',str(duration),'-ac','2','-c:a','pcm_s16le',str(P/f'mix{duration}.wav')],check=True)
print(F)
