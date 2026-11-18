init 98 python:
    import sys as th_sys
    import types as th_types
    th = th_sys.modules.setdefault("_thermos_qa", th_types.ModuleType("_thermos_qa"))
    th.hits = []
    th.location = None
    th.play = renpy.music.play
    def th_play(files, *args, **kwargs):
        if files == "audio/thermos_set_down.wav":
            th.hits.append(adv_original_location(*renpy.get_filename_line()))
        return th.play(files, *args, **kwargs)
    renpy.music.play = th_play
    def th_say(event, **kwargs):
        if event == "begin":
            th.location = adv_original_location(*renpy.get_filename_line())
    config.all_character_callbacks.append(th_say)
    def th_at(line, part):
        return th.location and th.location[:3] == ("story_ch06.rpy", line, part)
    def th_start():
        matches = [s for s in renpy.game.script.all_stmts if s.filename.endswith("story_ch06.rpy") and s.linenumber == 78]
        assert len(matches)==1
        renpy.jump(matches[0].name)
label th_start:
    $ th_start()

testcase qa_thermos_save:
    advance until screen "main_menu" timeout 120
    run Start("th_start")
    advance until eval (th_at(79,0)) timeout 30
    assert eval (not th.hits and _last_say_what.endswith("ほとんど音がしなかった。"))
    advance until eval (th_at(79,1)) timeout 30
    assert eval (th.hits == [("story_ch06.rpy",79,1,2)] and _last_say_what.startswith("向かいの机に"))
    pause until eval (renpy.music.get_playing("sound") == "audio/thermos_set_down.wav") timeout 2
    run FileSave("desk", confirm=False, page="thermos")
    pause until eval (renpy.can_load("thermos-desk")) timeout 10
    advance until eval (th_at(80,0)) timeout 10
    assert eval (len(th.hits)==1)

testcase qa_thermos_restart:
    advance until screen "main_menu" timeout 120
    run FileLoad("desk", confirm=False, page="thermos")
    pause until eval (th_at(79,1)) timeout 10
    assert eval (not th.hits and _last_say_what.startswith("向かいの机に"))
    run Rollback()
    pause until eval (th_at(79,0)) timeout 10
    assert eval (not th.hits and _last_say_what.endswith("ほとんど音がしなかった。"))
    advance until eval (th_at(79,1)) timeout 10
    assert eval (th.hits == [("story_ch06.rpy",79,1,2)])
    advance until eval (th_at(80,0)) timeout 10
    assert eval (len(th.hits)==1)

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    run Start("reread_start")
    pause until eval (reread and renpy.get_screen("say")) timeout 30
    run Jump("th_start")
    advance until eval (th_at(79,0)) timeout 30
    assert eval (reread and len(th.hits)==1)
    advance until eval (th_at(79,1)) timeout 10
    assert eval (reread and th.hits == [("story_ch06.rpy",79,1,2)] * 2)
