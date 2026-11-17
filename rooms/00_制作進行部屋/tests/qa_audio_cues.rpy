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
            key = (qau_os.path.basename(filename), line)
            if key in story_sound_cues:
                qau.hit = key
    config.all_character_callbacks.append(qau_observe)
    def qau_record():
        expected = story_sound_cues[qau.hit][0]
        actual = renpy.music.get_playing("sound")
        result = dict(location=qau.hit, expected=expected, actual=actual, passed=expected == actual)
        qau.results.append(result)
        with open(qau_os.path.join(config.basedir,"audio_results.json"),"w",encoding="utf-8") as handle:
            qau_json.dump(qau.results,handle,ensure_ascii=False,indent=2)
        assert expected == actual, repr(result)

testcase qa_audio_cues:
    $ qau.results.clear()
    $ qau.hit = None
    run Start("node_C01S02")
    advance until eval (qau.hit == ("story_ch01.rpy", 72)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C02S05")
    advance until eval (qau.hit == ("story_ch02.rpy", 171)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C02S05")
    advance until eval (qau.hit == ("story_ch02.rpy", 179)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C03S05")
    advance until eval (qau.hit == ("story_ch03.rpy", 199)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C04S06")
    advance until eval (qau.hit == ("story_ch04.rpy", 208)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qau.hit = None
    run Start("node_C11S07")
    advance until eval (qau.hit == ("story_ch11.rpy", 220)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == story_sound_cues[qau.hit][0]) timeout 5
    $ qau_record()
