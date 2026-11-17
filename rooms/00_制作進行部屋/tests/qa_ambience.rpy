init 20 python:
    import os as qaa_os
    import json as qaa_json
    import sys as qaa_sys
    import types as qaa_types
    qaa = qaa_sys.modules.setdefault("_ambience_qa", qaa_types.ModuleType("_ambience_qa"))
    qaa.location = None
    qaa.results = []
    def qaa_observe(event, **kwargs):
        if event == "begin":
            filename, line = renpy.get_filename_line()
            qaa.location = (qaa_os.path.basename(filename), line)
    config.all_character_callbacks.append(qaa_observe)
    def qaa_record(name, expected):
        actual = renpy.music.get_playing("story_ambience")
        row = dict(test=name, location=qaa.location, expected=expected, actual=actual, passed=actual == expected)
        qaa.results.append(row)
        with open(qaa_os.path.join(config.basedir,"ambience_results.json"),"w",encoding="utf-8") as handle:
            qaa_json.dump(qaa.results,handle,ensure_ascii=False,indent=2)
        assert row["passed"], repr(row)

testcase qa_ambience:
    run Start("node_C03S03")
    advance until eval (qaa.location == ("story_ch03.rpy", 141)) timeout 60
    pause until eval (renpy.music.get_playing("story_ambience") == "audio/rain_loop.wav") timeout 5
    # More than two file durations, proving full-file looping remains active.
    pause 9.0
    $ qaa_record("rain_loops", "audio/rain_loop.wav")
    $ renpy.music.play("audio/notification_soft.wav", channel="sound")
    pause 0.2
    $ qaa_record("notification_preserves_rain", "audio/rain_loop.wav")
    advance until eval (qaa.location == ("story_ch03.rpy", 150)) timeout 20
    pause until eval (renpy.music.get_playing("story_ambience") is None) timeout 5
    $ qaa_record("rain_stops_next_morning", None)
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    run Start("node_C11S02")
    advance until eval (qaa.location == ("story_ch11.rpy", 57)) timeout 60
    pause until eval (renpy.music.get_playing("story_ambience") == "audio/fridge_loop.wav") timeout 5
    $ qaa_record("fridge_begins", "audio/fridge_loop.wav")
    run FileSave("qa-ambience", confirm=False)
    advance until eval (qaa.location == ("story_ch11.rpy", 66)) timeout 20
    pause until eval (renpy.music.get_playing("story_ambience") is None) timeout 5
    $ qaa_record("fridge_stops_classroom", None)
    run FileLoad("qa-ambience", confirm=False)
    pause until eval (renpy.music.get_playing("story_ambience") == "audio/fridge_loop.wav") timeout 10
    $ qaa_record("save_load_restores_fridge", "audio/fridge_loop.wav")
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    pause until eval (renpy.music.get_playing("story_ambience") is None) timeout 5
    $ qaa_record("main_menu_stops_fridge", None)
