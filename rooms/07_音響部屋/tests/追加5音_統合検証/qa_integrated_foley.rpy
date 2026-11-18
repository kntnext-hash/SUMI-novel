init 98 python:
    def fq_at(f, l):
        return renpy.get_screen("say") and adv_original_location(*renpy.get_filename_line())[:2] == (f, l)
    def fq_track(ch, name):
        return (renpy.music.get_playing(ch) or "").endswith(name)
    def fq_pos(ch):
        return renpy.music.get_pos(ch) or 0.0
    def fq_jump(file, line):
        matches = [s for s in renpy.game.script.all_stmts if s.filename.endswith(file) and s.linenumber==line]
        assert len(matches)==1
        renpy.jump(matches[0].name)
label fq_bike:
    $ fq_jump("story_ch01.rpy", 29)
label fq_bridge:
    $ fq_jump("story_ch01.rpy", 226)
label fq_sink:
    $ fq_jump("story_end_r.rpy", 33)

testcase qa_integrated_foley:
    advance until screen "main_menu" timeout 120
    run Start("fq_bike")
    pause until eval (fq_track("story_bicycle_near","bicycle_pass_full.wav") and fq_track("story_bicycle_far","bicycle_pass_full.wav")) timeout 8
    pause until eval (fq_pos("story_bicycle_near") > 0.3 and fq_pos("story_bicycle_far") > 0.3) timeout 8
    assert eval (not renpy.music.get_playing("sound"))
    run Jump("fq_bridge")
    pause until eval (fq_at("story_ch01.rpy",226)) timeout 10
    assert eval (not renpy.music.get_playing("sound") and not renpy.music.get_playing("story_ambience"))
    advance until eval (fq_at("story_ch01.rpy",227)) timeout 10
    pause until eval (fq_track("sound","bicycle_bell_single.wav") and fq_pos("sound") > 0.05) timeout 5
    pause until eval (fq_track("story_bicycle_near","bicycle_pass_full.wav") and fq_pos("story_bicycle_near") > 0.1) timeout 6
    advance until eval (fq_at("story_ch01.rpy",229)) timeout 10
    pause until eval (fq_track("story_ambience","park_wind_loop.wav") and fq_pos("story_ambience") > 0.15) timeout 5
    advance until eval (fq_at("story_ch01.rpy",232)) timeout 10
    assert eval (fq_track("story_ambience","park_wind_loop.wav"))
    advance until eval (fq_at("story_ch01.rpy",237)) timeout 15
    pause until eval (not renpy.music.get_playing("story_ambience")) timeout 5
    run Jump("fq_sink")
    pause until eval (fq_track("story_ambience","kitchen_sink_loop.wav") and fq_pos("story_ambience") > 0.15) timeout 6
    advance until eval (fq_at("story_end_r.rpy",36)) timeout 10
    assert eval (fq_track("story_ambience","kitchen_sink_loop.wav"))
    advance until eval (fq_at("story_end_r.rpy",37)) timeout 10
    pause until eval (not renpy.music.get_playing("story_ambience")) timeout 5
    assert eval (not renpy.music.get_playing("sound"))

testcase qa_integrated_bed_save:
    advance until screen "main_menu" timeout 120
    run Start("fq_sink")
    advance until eval (fq_at("story_end_r.rpy",35)) timeout 15
    pause until eval (fq_track("story_ambience","kitchen_sink_loop.wav") and fq_pos("story_ambience") > 0.1) timeout 8
    run FileSave("water", confirm=False, page="integrated")
    pause until eval (renpy.can_load("integrated-water")) timeout 10
    run Jump("fq_bridge")
    advance until eval (fq_at("story_ch01.rpy",230)) timeout 15
    pause until eval (fq_track("story_ambience","park_wind_loop.wav") and fq_pos("story_ambience") > 0.1) timeout 8
    run FileSave("wind", confirm=False, page="integrated")
    pause until eval (renpy.can_load("integrated-wind")) timeout 10

testcase qa_integrated_bed_restart:
    advance until screen "main_menu" timeout 120
    run FileLoad("wind",confirm=False,page="integrated")
    pause until eval (fq_at("story_ch01.rpy",230) and fq_track("story_ambience","park_wind_loop.wav")) timeout 10
    advance until eval (fq_at("story_ch01.rpy",237)) timeout 20
    pause until eval (not renpy.music.get_playing("story_ambience")) timeout 6
    run FileLoad("water",confirm=False,page="integrated")
    pause until eval (fq_at("story_end_r.rpy",35) and fq_track("story_ambience","kitchen_sink_loop.wav")) timeout 10
    advance until eval (fq_at("story_end_r.rpy",37)) timeout 15
    pause until eval (not renpy.music.get_playing("story_ambience")) timeout 6
    assert eval (not renpy.music.get_playing("sound"))
