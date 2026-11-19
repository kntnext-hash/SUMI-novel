testcase qa_album:
    advance until screen "main_menu" timeout 120
    run Function(renpy.mark_image_unseen, "cg_again__5")
    run Function(renpy.mark_image_unseen, "cg_again__full")
    assert eval (len(cg_album_entries) == 55 and sum(len(v) for n,v in cg_album_entries) == 114)
    run Function(renpy.mark_image_unseen, "cg_hedge_reveal__5")
    run Function(renpy.mark_image_unseen, "cg_hedge_reveal__full")
    run Function(renpy.mark_image_unseen, "cg_garden_joined__3")
    run Function(renpy.mark_image_unseen, "cg_garden_joined__full")
    assert eval (not viewed_cg_stages(dict(cg_album_entries)["hedge_reveal"]) and not viewed_cg_stages(dict(cg_album_entries)["garden_joined"]))
    run Function(renpy.mark_image_seen, "cg_hedge_reveal__5")
    run Function(renpy.mark_image_seen, "cg_garden_joined__3")
    assert eval ([s for s, p in viewed_cg_stages(dict(cg_album_entries)["hedge_reveal"])] == ["5"])
    assert eval ([s for s, p in viewed_cg_stages(dict(cg_album_entries)["garden_joined"])] == ["3"])
    run Function(renpy.mark_image_seen, "cg_hedge_reveal__full")
    run Function(renpy.mark_image_seen, "cg_garden_joined__full")
    assert eval (len(viewed_cg_stages(dict(cg_album_entries)["hedge_reveal"])) == 2 and len(viewed_cg_stages(dict(cg_album_entries)["garden_joined"])) == 2)
    assert eval (not viewed_cg_stages(dict(cg_album_entries)["again"]))
    run Function(renpy.mark_image_seen, "cg_again__5")
    run ShowMenu("cg_album")
    pause until screen "cg_album" timeout 5
    assert eval (len(viewed_cg_stages(dict(cg_album_entries)["again"])) == 1)
    run Function(renpy.mark_image_seen, "cg_again__full")
    assert eval (len(viewed_cg_stages(dict(cg_album_entries)["again"])) == 2)
    click pos (390, 303)
    pause until "一覧へ" timeout 5
    click "全彩再読"
    click "一覧へ"
    click "次へ"
    click "前へ"
    click "戻る"
    pause until screen "main_menu" timeout 5

