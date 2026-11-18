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

testcase qa_four_foley:
    advance until screen "main_menu" timeout 120
    run Start("fq_bike")
    pause until eval (fq_track("four_bike_near","bicycle_pass_full.wav") and fq_track("four_bike_far","bicycle_pass_full.wav")) timeout 8
    pause until eval (fq_pos("four_bike_near") > 0.3 and fq_pos("four_bike_far") > 0.3) timeout 8
    assert eval (not renpy.music.get_playing("sound"))
    run Jump("fq_bridge")
    pause until eval (fq_at("story_ch01.rpy",226)) timeout 10
    assert eval (not renpy.music.get_playing("sound") and not renpy.music.get_playing("four_outdoors"))
    advance until eval (fq_at("story_ch01.rpy",227)) timeout 10
    pause until eval (fq_track("sound","bicycle_bell_single.wav") and fq_pos("sound") > 0.05) timeout 5
    pause until eval (fq_track("four_bike_near","bicycle_pass_full.wav") and fq_pos("four_bike_near") > 0.1) timeout 6
    advance until eval (fq_at("story_ch01.rpy",229)) timeout 10
    pause until eval (fq_track("four_outdoors","park_wind_loop.wav") and fq_pos("four_outdoors") > 0.15) timeout 5
    advance until eval (fq_at("story_ch01.rpy",232)) timeout 10
    assert eval (fq_track("four_outdoors","park_wind_loop.wav"))
    advance until eval (fq_at("story_ch01.rpy",237)) timeout 15
    pause until eval (not renpy.music.get_playing("four_outdoors")) timeout 5
    run Jump("fq_sink")
    pause until eval (fq_track("four_outdoors","kitchen_sink_loop.wav") and fq_pos("four_outdoors") > 0.15) timeout 6
    advance until eval (fq_at("story_end_r.rpy",36)) timeout 10
    assert eval (fq_track("four_outdoors","kitchen_sink_loop.wav"))
    advance until eval (fq_at("story_end_r.rpy",37)) timeout 10
    pause until eval (not renpy.music.get_playing("four_outdoors")) timeout 5
    assert eval (not renpy.music.get_playing("sound"))
