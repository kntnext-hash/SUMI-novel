init python:
    def qa_cg_at(prefix):
        screen = renpy.get_screen("say")
        return screen is not None and screen.scope.get("what", "").startswith(prefix)

label qa_hands_first:
    $ reread = False
    jump node_C05S06
label qa_hands_full:
    $ reread = True
    jump node_C05S06
label qa_garden_first:
    $ reread = False
    jump node_C08S07
label qa_garden_full:
    $ reread = True
    jump node_C08S07
label qa_hedge_first:
    $ reread = False
    jump node_ERS02
label qa_hedge_full:
    $ reread = True
    jump node_ERS02

testcase qa_hands_first:
    advance until screen "main_menu" timeout 120
    run Start("qa_hands_first")
    advance until eval (qa_cg_at("透花が手のひらを上に")) timeout 60
    assert eval (not renpy.showing("cg_hands__1c"))
    advance until eval (qa_cg_at("指を入れた。")) timeout 20
    assert eval (renpy.showing("cg_hands__1c"))
    screenshot "hands_before_color"
    advance until eval (qa_cg_at("透花の指に色があった。")) timeout 20
    assert eval (renpy.showing("cg_hands__2"))
    screenshot "hands_color"

testcase qa_hands_full:
    advance until screen "main_menu" timeout 120
    run Start("qa_hands_full")
    advance until eval (qa_cg_at("透花が手のひらを上に")) timeout 60
    assert eval (not renpy.showing("cg_hands__full"))
    advance until eval (qa_cg_at("指を入れた。")) timeout 20
    assert eval (renpy.showing("cg_hands__full"))
    screenshot "hands_full"

testcase qa_garden_first:
    advance until screen "main_menu" timeout 120
    run Start("qa_garden_first")
    advance until eval (qa_cg_at("『いいよ。庭の右側はわたし。左は透花』")) timeout 60
    assert eval (renpy.showing("cg_garden_joined__3"))
    screenshot "garden_joined_first"
    advance until eval (qa_cg_at("月曜には二人分の庭を")) timeout 30
    assert eval (renpy.showing("bg_room_jun__3"))

testcase qa_garden_full:
    advance until screen "main_menu" timeout 120
    run Start("qa_garden_full")
    advance until eval (qa_cg_at("『いいよ。庭の右側はわたし。左は透花』")) timeout 60
    assert eval (renpy.showing("cg_garden_joined__full"))
    screenshot "garden_joined_full"
    advance until eval (qa_cg_at("月曜には二人分の庭を")) timeout 30
    assert eval (renpy.showing("bg_room_jun__full"))

testcase qa_hedge_first:
    advance until screen "main_menu" timeout 120
    run Start("qa_hedge_first")
    advance until eval (qa_cg_at("「ちがう。いつから、わたしだって知ってたの」")) timeout 60
    assert eval (renpy.showing("cg_hedge_reveal__5"))
    screenshot "hedge_reveal_first"
    advance until eval (qa_cg_at("冊子のページを押さえたまま")) timeout 40
    assert eval (renpy.showing("cg_hedge_book__5"))

testcase qa_hedge_full:
    advance until screen "main_menu" timeout 120
    run Start("qa_hedge_full")
    advance until eval (qa_cg_at("「ちがう。いつから、わたしだって知ってたの」")) timeout 60
    assert eval (renpy.showing("cg_hedge_reveal__full"))
    screenshot "hedge_reveal_full"
    advance until eval (qa_cg_at("冊子のページを押さえたまま")) timeout 40
    assert eval (renpy.showing("cg_hedge_book__full"))
