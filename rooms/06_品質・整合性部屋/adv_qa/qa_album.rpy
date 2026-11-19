testcase qa_album:
    advance until screen "main_menu" timeout 120
    run Function(renpy.mark_image_unseen, "cg_again__5")
    run Function(renpy.mark_image_unseen, "cg_again__full")
    assert eval (len(cg_album_entries) == 53 and sum(len(v) for n,v in cg_album_entries) == 110)
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
