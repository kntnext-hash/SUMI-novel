# 『顔のない春 ――きみの色が見えるまで。』
# 本編は story_*.rpy（scenario.json から自動変換）。

define narrator = Character(None, kind=adv, window_style="story_adv_window", what_style="story_adv_text")

style story_adv_window is default:
    xpos 60
    ypos 630
    xsize 1800
    ysize 380
    padding (48, 24)
    background Frame("ui/ui_nvl_washi.png", 24, 24)

style story_adv_text is default:
    font gui.text_font
    size 36
    color "#242424"
    xsize 1704
    line_spacing 10

default reread = False

label start:
    $ reread = False
    jump node_C01S01

label reread_start:
    $ reread = True
    jump node_C01S01
