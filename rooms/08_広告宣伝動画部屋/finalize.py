"""Normalize distribution MP4 to limited-range BT.709 and exact requested duration."""
from pathlib import Path
import sys,subprocess
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'python_lib'))
import imageio_ffmpeg
F=imageio_ffmpeg.get_ffmpeg_exe()
(R/'masters').mkdir(exist_ok=True)
for name,seconds in [('vertical',15),('horizontal',30)]:
 if len(sys.argv)>1 and sys.argv[1]!=name:continue
 target=R/f'deliverables/kaononaiharu_{name}_{seconds}s.mp4'
 master=R/'masters'/target.name
 if not master.exists():target.rename(master)
 subprocess.run([F,'-hide_banner','-loglevel','error','-y','-i',str(master),'-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-c:a','aac','-b:a','192k','-ar','48000','-t',str(seconds),'-movflags','+faststart',str(target)],check=True)
 print('Finalized',name,flush=True)
