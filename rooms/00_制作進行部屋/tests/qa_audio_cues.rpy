init 20 python:
    import sys as qau_sys
    import types as qau_types
    import json as qau_json
    import os as qau_os
    qau = qau_sys.modules.setdefault("_audio_qa", qau_types.ModuleType("_audio_qa"))
    qau.hit = None
    qau.results = []
    def qau_observe(event, **kwargs):
        if event == "begin":
            filename, line = renpy.get_filename_line()
            source, original, part, count = adv_original_location(filename, line)
            page = (source, original, part)
            if page in story_sound_cues or (not part and page[:2] in story_sound_stops):
                qau.hit = page
    config.all_character_callbacks.append(qau_observe)
    def qau_record():
        expected = story_sound_cues.get(qau.hit, (None, 0))[0]
        actual = renpy.music.get_playing("sound")
        result = dict(location=qau.hit, expected=expected, actual=actual, passed=expected == actual)
        qau.results.append(result)
        with open(qau_os.path.join(config.basedir,"audio_results.json"),"w",encoding="utf-8") as handle:
            qau_json.dump(qau.results,handle,ensure_ascii=False,indent=2)
        assert expected == actual, repr(result)

testcase qa_audio_cues:
    advance until screen "main_menu" timeout 120
    $ qau.results.clear()
    $ qau.hit = None
    run Start("node_C01S02")
    advance until eval (qau.hit == ("story_ch01.rpy", 72, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues.get(qau.hit, (None, 0))[0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C02S05")
    advance until eval (qau.hit == ("story_ch02.rpy", 171, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues.get(qau.hit, (None, 0))[0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C02S05")
    advance until eval (qau.hit == ("story_ch02.rpy", 179, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues.get(qau.hit, (None, 0))[0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C03S05")
    advance until eval (qau.hit == ("story_ch03.rpy", 199, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues.get(qau.hit, (None, 0))[0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C04S06")
    advance until eval (qau.hit == ("story_ch04.rpy", 208, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues.get(qau.hit, (None, 0))[0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C11S07")
    advance until eval (qau.hit == ("story_ch11.rpy", 220, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues.get(qau.hit, (None, 0))[0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C04S03")
    advance until eval (qau.hit == ("story_ch04.rpy", 93, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C06S06")
    advance until eval (qau.hit == ("story_ch06.rpy", 229, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    advance until eval (qau.hit == ("story_ch06.rpy", 230, 0)) timeout 30
    pause until eval (renpy.music.get_playing("sound") is None) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C07S03")
    advance until eval (qau.hit == ("story_ch07.rpy", 106, 0)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
