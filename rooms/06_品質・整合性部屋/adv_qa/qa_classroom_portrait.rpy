label qa_classroom_first:
    $ reread = False
    jump node_C01S02

label qa_classroom_full:
    $ reread = True
    jump node_C01S02

init python:
    def qa_classroom_at(line):
        return renpy.get_screen("say") and adv_original_location(*renpy.get_filename_line())[:2] == ("story_ch01.rpy", line)

testcase qa_classroom_first:
    advance until screen "main_menu" timeout 120
    run Start("qa_classroom_first")
    advance until eval (qa_classroom_at(54)) timeout 40
    pause 1.5
    screenshot "classroom_first"
    advance until eval (qa_classroom_at(63)) timeout 40
    screenshot "classroom_first_cg"

testcase qa_classroom_full:
    advance until screen "main_menu" timeout 120
    run Start("qa_classroom_full")
    advance until eval (qa_classroom_at(54)) timeout 40
    pause 1.5
    screenshot "classroom_full"
