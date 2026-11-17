init 20 python:
    import json as qac_json
    import os as qac_os
    import sys as qac_sys
    import types as qac_types
    qac = qac_sys.modules.setdefault("_cinema_sound_qa", qac_types.ModuleType("_cinema_sound_qa"))
    qac.location = None
    qac.results = []
    def qac_observe(event, **kwargs):
        if event == "begin":
            filename, line = renpy.get_filename_line()
            qac.location = (qac_os.path.basename(filename), line)
    config.all_character_callbacks.append(qac_observe)
    def qac_record(name, expected):
        actual = renpy.music.get_playing("sound")
        row = dict(test=name, location=qac.location, expected=expected, actual=actual, passed=actual == expected)
        qac.results.append(row)
        with open(qac_os.path.join(config.basedir,"cinema_sound_results.json"),"w",encoding="utf-8") as handle:
            qac_json.dump(qac.results,handle,ensure_ascii=False,indent=2)
        assert row["passed"], repr(row)

testcase qa_cinema_sound:
    run Start("node_C09S04")
    advance until eval (qac.location == ("story_ch09.rpy", 142)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == "audio/cinema_wood_paper.wav") timeout 5
    $ qac_record("wood_then_paper", "audio/cinema_wood_paper.wav")
    advance until eval (qac.location == ("story_ch09.rpy", 143)) timeout 20
    pause until eval (renpy.music.get_playing("sound") == "audio/small_bell_single.wav") timeout 5
    $ qac_record("one_bell", "audio/small_bell_single.wav")
    # Move on while the 1.4-second bell tail could still be playing.
    advance until eval (qac.location == ("story_ch09.rpy", 144)) timeout 20
    pause until eval (renpy.music.get_playing("sound") is None) timeout 5
    $ qac_record("silent_bell_against_sleeve", None)
    advance until eval (qac.location == ("story_ch09.rpy", 145)) timeout 20
    $ qac_record("silent_bell_in_palm", None)
    advance until eval (qac.location == ("story_ch09.rpy", 146)) timeout 20
    pause until eval (renpy.music.get_playing("sound") == "audio/cinema_paper_two_bells.wav") timeout 5
    $ qac_record("paper_then_two_bells", "audio/cinema_paper_two_bells.wav")
    advance until eval (qac.location == ("story_ch09.rpy", 155)) timeout 20
    pause until eval (renpy.music.get_playing("sound") is None) timeout 5
    $ qac_record("leaving_cinema_stops_sound", None)
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    run Start("node_C09S04")
    advance until eval (qac.location == ("story_ch09.rpy", 146)) timeout 60
    pause until eval (renpy.music.get_playing("sound") == "audio/cinema_paper_two_bells.wav") timeout 5
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    pause until eval (renpy.music.get_playing("sound") is None) timeout 5
    $ qac_record("main_menu_stops_cinema_sound", None)
