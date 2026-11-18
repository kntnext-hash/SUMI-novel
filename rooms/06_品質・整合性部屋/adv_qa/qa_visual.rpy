init 99 python:
    config.window_title = "SUMI ADV VISUAL QA"
    config.overlay_screens.append("qa_picker")
    def qa_jump_at(filename, line):
        matches = [n for n in renpy.game.script.all_stmts if n.filename.endswith(filename) and n.linenumber == line]
        assert len(matches) == 1, repr(matches)
        renpy.jump(matches[0].name)

screen qa_picker():
    zorder 200
    hbox:
        xalign 1.0
        yalign 0.0
        textbutton "QA" action Jump("qa_entry")


screen qa_selection():
    modal True
    zorder 300
    frame:
        xalign .5
        yalign .5
        vbox:
            spacing 12
            for caption in ["Early first", "Early reread", "Late first", "Late reread", "Ending first", "Ending reread", "Choice", "Longest", "Unlock title"]:
                textbutton caption action Return(caption) text_size 26
label qa_entry:
    nvl clear
    hide screen nvl
    call screen qa_selection
    $ reread = "reread" in _return
    if _return.startswith("Early"):
        $ qa_jump_at("story_ch01.rpy", 30)
    elif _return.startswith("Late"):
        $ qa_jump_at("story_ch08.rpy", 204)
    elif _return.startswith("Ending"):
        jump node_EDS05
    elif _return == "Longest":
        $ qa_jump_at("story_ch02.rpy", 186)
    elif _return == "Choice":
        jump node_C06S05
    else:
        $ persistent.unlocked_reread = True
        return


