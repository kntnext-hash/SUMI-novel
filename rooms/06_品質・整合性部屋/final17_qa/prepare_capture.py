"""Install QA-only natural-route screenshot tests into an isolated game copy."""
from pathlib import Path
import argparse

p = argparse.ArgumentParser()
p.add_argument('game', type=Path)
a = p.parse_args()
header = r'''
python early:
    config.savedir = config.basedir + "/qa17_saves"

init 999 python:
    import os as qa17_os
    import json as qa17_json
    import types as qa17_types
    import sys as qa17_sys
    config.savedir = config.basedir + "/qa17_saves"
    config.save_directory = "SUMI-final17-isolated"
    preferences.text_cps = 0
    config.skip_delay = 0
    qa17_state = qa17_sys.modules.setdefault("_qa17_capture", qa17_types.ModuleType("_qa17_capture"))
    qa17_state.seen = set()
    qa17_state.rows = []
    qa17_state.done = False
    qa17_targets = set("first_face lattice bath_print table_drink rabbit stone_pot screen_portrait train_shoulder can_reply can_pause bridge_ask gift glove child_name erase_tag hedge_book hedge_reveal again book_march book_ground garden_plan garden_joined market_flyer hands scissors lovers river_view seat_intro wire bird_candy candy_fingers hair_wind solo confess child_drain".split())

    def qa17_begin(mode, route):
        qa17_state.mode = mode
        qa17_state.route = route
        qa17_state.done = False

    def qa17_key():
        if not renpy.get_screen("say") or not renpy.get_screen("say").scope.get("what", "").strip():
            return None
        source, line, part, count = adv_original_location(*renpy.get_filename_line())
        if not source.startswith("story_"):
            return None
        for tag in sorted(renpy.get_showing_tags(layer="master")):
            if tag.startswith("cg_") and tag[3:].partition("__")[0] in qa17_targets:
                labels = [s for s in renpy.game.script.all_stmts if isinstance(s, renpy.ast.Label) and str(s.name).startswith("node_")
                    and s.filename.replace("\\", "/").rsplit("/",1)[-1] == source and s.linenumber <= line]
                node = max(labels,key=lambda s:s.linenumber).name if labels else source
                return (qa17_state.mode, str(node), tag)
        return None

    def qa17_event():
        key = qa17_key()
        if key is not None and key not in qa17_state.seen:
            return 1
        if renpy.get_screen("choice"):
            return 2
        if renpy.get_screen("main_menu"):
            return 3
        return 0

    def qa17_capture():
        key = qa17_key()
        assert key is not None
        assert reread == qa17_state.mode
        qa17_state.seen.add(key)
        source, line, part, count = adv_original_location(*renpy.get_filename_line())
        qa17_state.filename = ("full" if reread else "first") + "/%03d-%s-%s.png" % (len(qa17_state.rows)+1,key[1],key[2])
        qa17_state.rows.append(dict(file=qa17_state.filename,source=source,line=line,part=part,node=key[1],image=key[2],reread=reread,route=qa17_state.route,text=renpy.last_say().what))
        with open(qa17_os.path.join(config.basedir,"qa17_capture.json"),"w",encoding="utf-8") as f:
            qa17_json.dump(qa17_state.rows,f,ensure_ascii=False,indent=2)

    def qa17_choose():
        items = renpy.get_screen("choice").scope["items"]
        captions = [i.caption for i in items]
        if "わたしも" in captions:
            caption = "わたしも"
        elif "あの飴、買いに行こう" in captions:
            caption = "あの飴、買いに行こう" if qa17_state.route == "A" else "あのお店の話、続きがあるの"
        elif "今日はここまでにしていい？" in captions:
            caption = "今日はここまでにしていい？" if qa17_state.route == "B" else "あの日、下まで行きたかった"
        elif "うちに寄ってって" in captions:
            caption = "うちに寄ってって" if qa17_state.route == "C" else "透花、もうひとつ聞いて"
        else:
            raise AssertionError("Unexpected choice: " + repr(captions))
        return caption
'''
block = '''    if eval (not qa17_state.done):
        advance until eval qa17_event() timeout 900
        if eval (qa17_event() == 1):
            pause 0.3
            $ qa17_capture()
            screenshot qa17_state.filename
        elif eval (qa17_event() == 2):
            if eval (qa17_choose() == "わたしも"):
                click "わたしも"
            elif eval (qa17_choose() == "あの飴、買いに行こう"):
                click "あの飴、買いに行こう"
            elif eval (qa17_choose() == "あのお店の話、続きがあるの"):
                click "あのお店の話、続きがあるの"
            elif eval (qa17_choose() == "今日はここまでにしていい？"):
                click "今日はここまでにしていい？"
            elif eval (qa17_choose() == "あの日、下まで行きたかった"):
                click "あの日、下まで行きたかった"
            elif eval (qa17_choose() == "うちに寄ってって"):
                click "うちに寄ってって"
            elif eval (qa17_choose() == "透花、もうひとつ聞いて"):
                click "透花、もうひとつ聞いて"
        elif eval (qa17_event() == 3):
            $ qa17_state.done = True
'''
s = header
for name, mode, routes in [('qa17_smoke', True, 'D'), ('qa17_full', True, 'ABCD'), ('qa17_first', False, 'ABCD')]:
    s += '\ntestcase ' + name + ':\n    advance until screen "main_menu" timeout 120\n'
    s += '    $ qa17_state.seen.clear()\n    $ qa17_state.rows.clear()\n'
    for route in routes:
        s += f'    $ qa17_begin({mode}, "{route}")\n'
        s += '    run Start("' + ('reread_start' if mode else 'start') + '")\n    pause 0.3\n'
        s += block * 180
        s += '    $ assert qa17_state.done, "Capture event budget exhausted"\n'
    s += '    $ assert persistent.unlocked_reread\n'
(a.game / 'qa17_capture.rpy').write_text(s, encoding='utf-8')
print(a.game / 'qa17_capture.rpy')
