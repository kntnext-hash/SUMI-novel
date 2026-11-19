"""Capture the real 17-SFX Ren'Py renderer in an isolated copy; never edit the distribution."""
from pathlib import Path
import shutil, subprocess, os, json
ROOM=Path(__file__).resolve().parent
ROOT=ROOM.parents[2]
SOURCE=ROOT/'builds/kaononaiharu-adv-sound-review-win'
CAPTURE=ROOM/'capture-game'
if not (CAPTURE/'game').exists():
 shutil.copytree(SOURCE/'game',CAPTURE/'game',ignore=shutil.ignore_patterns('cache','saves','*.rpyc'))
out=ROOM/'project/public'
out.mkdir(parents=True,exist_ok=True)
scenes=[
 ('adv_bridge','bg_bridge_spring__0','耳から抜いてから気づく。もう吠えないんだった。'),
 ('adv_hello','cg_bridge_hello__0','「おはよう」'),
 ('adv_bag','cg_bridge_hello__0','今日はもう鞄に入れてもよさそうだった。'),
]
lines=['init 999 python:','    import os as ad_os','    config.label_overrides["splashscreen"] = "ad_capture"','    config.window_title = "SUMI AD CAPTURE - isolated"','    config.save_directory = "sumi-ad-capture"','    def ad_shot():',f'        renpy.screenshot(ad_os.path.join({json.dumps(str(out))}, ad_name + ".png"))','        renpy.end_interaction(True)','','screen ad_timer():','    timer 1.0 action Function(ad_shot)','','label ad_capture:','    $ preferences.text_cps = 0','    $ preferences.fullscreen = False','    $ quick_menu = True']
for name,tag,body in scenes:
 lines += ['    scene '+tag, '    $ ad_name = "'+name+'"','    show screen ad_timer','    '+json.dumps(body,ensure_ascii=False),'    hide screen ad_timer']
lines += ['    $ renpy.quit()']
(CAPTURE/'game/ad_capture.rpy').write_text('\n'.join(lines),encoding='utf8')
result=subprocess.run([str(SOURCE/'kaononaiharu.exe'),str(CAPTURE)],cwd=SOURCE,env={**os.environ,'RENPY_PATH_TO_SAVES':str(CAPTURE/'isolated-saves')},timeout=90)
print('Capture result',result.returncode,[(n,(out/(n+'.png')).exists()) for n,_,_ in scenes])
