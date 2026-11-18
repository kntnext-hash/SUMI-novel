init 999 python:
    import time as face_clock
    from renpy.test.testsettings import _test
    _test.force = True
    _test.screenshot_directory = "tests/face_release"
    def visual_face_jump(filename, line):
        targets = [s for s in renpy.game.script.all_stmts if s.filename.endswith(filename) and s.linenumber == line]
        assert len(targets) == 1, (filename, line)
        renpy.jump(targets[0].name)

label visual_face_pause_first:
    $ reread = False
    $ visual_face_jump("story_ch08.rpy", 204)

label visual_face_reply_first:
    $ reread = False
    $ visual_face_jump("story_ch08.rpy", 212)

label visual_face_pause_reread:
    $ reread = True
    $ visual_face_jump("story_ch08.rpy", 204)

label visual_face_reply_reread:
    $ reread = True
    $ visual_face_jump("story_ch08.rpy", 212)

label visual_face_reveal_first:
    $ reread = False
    $ visual_face_jump("story_ch10.rpy", 238)

label visual_face_reveal_reread:
    $ reread = True
    $ visual_face_jump("story_ch10.rpy", 238)

testcase qa_face_comparison:
    advance until screen "main_menu" timeout 120
    $ preferences.text_cps = 0
    run Start("visual_face_pause_first")
    pause until eval (renpy.get_screen("say") and (renpy.get_screen("say").scope.get("what") or "").startswith("「向こうはもう覚えてないと思う」") and reread == False) timeout 30
    $ face_wait = face_clock.monotonic() + 4.0
    pause until eval (face_clock.monotonic() >= face_wait) timeout 60
    screenshot "pause_first.png"
    run Jump("visual_face_reply_first")
    pause until eval (renpy.get_screen("say") and (renpy.get_screen("say").scope.get("what") or "").startswith("「何でもないよ」") and reread == False) timeout 30
    $ face_wait = face_clock.monotonic() + 4.0
    pause until eval (face_clock.monotonic() >= face_wait) timeout 60
    screenshot "reply_first.png"
    run Jump("visual_face_pause_reread")
    pause until eval (renpy.get_screen("say") and (renpy.get_screen("say").scope.get("what") or "").startswith("「向こうはもう覚えてないと思う」") and reread == True) timeout 30
    $ face_wait = face_clock.monotonic() + 4.0
    pause until eval (face_clock.monotonic() >= face_wait) timeout 60
    screenshot "pause_reread.png"
    run Jump("visual_face_reply_reread")
    pause until eval (renpy.get_screen("say") and (renpy.get_screen("say").scope.get("what") or "").startswith("「何でもないよ」") and reread == True) timeout 30
    $ face_wait = face_clock.monotonic() + 4.0
    pause until eval (face_clock.monotonic() >= face_wait) timeout 60
    screenshot "reply_reread.png"
    run Jump("visual_face_reveal_first")
    advance until eval (renpy.get_screen("say") and (renpy.get_screen("say").scope.get("what") or "").startswith("片方の眉が少し高かった。") and reread == False) timeout 30
    $ face_wait = face_clock.monotonic() + 4.0
    pause until eval (face_clock.monotonic() >= face_wait) timeout 60
    screenshot "reveal_first.png"
    run Jump("visual_face_reveal_reread")
    advance until eval (renpy.get_screen("say") and (renpy.get_screen("say").scope.get("what") or "").startswith("片方の眉が少し高かった。") and reread == True) timeout 30
    $ face_wait = face_clock.monotonic() + 4.0
    pause until eval (face_clock.monotonic() >= face_wait) timeout 60
    screenshot "reveal_reread.png"
