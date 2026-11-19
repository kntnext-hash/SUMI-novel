init 98 python:
    def fw_at(line):
        return renpy.get_screen("say") and adv_original_location(*renpy.get_filename_line())[:3] == ("story_ch05.rpy", line, 0)
    def fw_playing():
        return renpy.music.get_playing("sound") == "audio/firework_single_5.wav" and (renpy.music.get_pos("sound") or 0.0) > 0.02
testcase qa_review_fireworks:
    advance until screen "main_menu" timeout 120
    run Start("node_C05S05")
    advance until eval (fw_at(178)) timeout 90
    pause until eval (fw_playing()) timeout 3
    advance until eval (fw_at(225)) timeout 90
    assert eval (not fw_playing())
    advance until eval (fw_at(226)) timeout 20
    pause until eval (fw_playing()) timeout 3
