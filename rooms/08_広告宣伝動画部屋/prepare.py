from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'python_lib'))
import shutil, json, hashlib
from PIL import Image, ImageDraw
ROOM=Path(__file__).resolve().parent
ROOT=ROOM.parents[2]
SOURCE=ROOT/'builds/kaononaiharu-adv-sound-review-win'
OUT=ROOM/'project/public'
OUT.mkdir(parents=True,exist_ok=True)
names=['BG_bridge_spring__0.webp','BG_bridge_spring__FULL.webp','CG_bridge_hello__0.webp']
names=[n for n in names if (SOURCE/'game/images'/n).exists()]
manifest=[]
for name in names:
 p=SOURCE/'game/images'/name; shutil.copy2(p,OUT/name)
 manifest.append({'file':name,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for folder,name in [('fonts','NotoSerifJP-Regular.otf'),('audio','park_wind_loop.wav'),('audio','bicycle_bell_single.wav')]:
 p=SOURCE/'game'/folder/name;shutil.copy2(p,OUT/name)
 manifest.append({'file':name,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOM/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
sheet=Image.new('RGB',(960,300*((len(names)+1)//2)), '#eeeeee');d=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
 im=Image.open(OUT/name).convert('RGB');im.thumbnail((480,270));x=i%2*480;y=i//2*300;sheet.paste(im,(x,y));d.text((x+8,y+275),name,fill='black')
sheet.save(ROOM/'source-contact.jpg')
print('Prepared',OUT)
