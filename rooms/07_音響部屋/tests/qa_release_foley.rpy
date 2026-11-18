init 90 python:
    import sys as qf_sys
    import types as qf_types
    qf = qf_sys.modules.setdefault("_foley_qa", qf_types.ModuleType("_foley_qa"))
    qf.loc = None
    def qf_update(event, **kwargs):
        if event == "begin":
            qf.loc = adv_original_location(*renpy.get_filename_line())[:2]
    config.all_character_callbacks.append(qf_update)

testcase qa_release_foley:
    pause until screen "main_menu" timeout 90
    run Start("node_C07S05")
    advance until eval (qf.loc == ("story_ch07.rpy", 209)) timeout 120
    pause until eval (renpy.music.get_playing("sound") == "audio/book_drop.wav") timeout 3
    pause 2
    assert eval (not renpy.music.get_playing("sound"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    run Start("node_C11S02")
    advance until eval (qf.loc == ("story_ch11.rpy", 57)) timeout 120
    pause until eval (renpy.music.get_playing("sound") == "audio/pot_water.wav" and renpy.music.get_playing("story_ambience") == "audio/fridge_loop.wav") timeout 3
    advance until eval (qf.loc == ("story_ch11.rpy", 66)) timeout 20
    pause until eval (not renpy.music.get_playing("sound") and not renpy.music.get_playing("story_ambience")) timeout 5
    assert eval (not renpy.music.get_playing("sound") and not renpy.music.get_playing("story_ambience"))
