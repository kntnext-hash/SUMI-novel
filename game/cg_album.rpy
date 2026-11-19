init python:
    def build_cg_album():
        groups = {}
        for path in sorted(renpy.list_files()):
            if path.startswith("images/CG_") and path.endswith(".webp"):
                name, stage = path[10:-5].rsplit("__", 1)
                groups.setdefault(name, []).append((stage, path))
        return tuple(groups.items())

    def viewed_cg_stages(variants):
        return [(stage, path) for stage, path in variants
                if renpy.seen_image(path[7:-5].lower())]

define cg_album_entries = build_cg_album()


screen cg_album():
    tag menu
    default page = 0
    default selected = None
    default variant = 0
    add Solid("#f2ede5")

    if selected is None:
        text _("CGギャラリー") xpos 100 ypos 45 size 52 color "#382f32"
        grid 4 3:
            align (0.5, 0.5)
            spacing 18
            for index in range(page * 12, page * 12 + 12):
                if index < len(cg_album_entries):
                    $ viewed = viewed_cg_stages(cg_album_entries[index][1])
                    button:
                        xysize (380, 214)
                        padding (0, 0)
                        background Solid("#dfd8cf")
                        action [SetScreenVariable("selected", index), SetScreenVariable("variant", 0)]
                        sensitive bool(viewed)
                        if viewed:
                            add Transform(viewed[0][1], xysize=(380, 214))
                        else:
                            text _("未開放") align (0.5, 0.5) size 26 color "#645a57"
                else:
                    null
        hbox:
            align (0.5, 0.93)
            spacing 48
            textbutton _("前へ") action SetScreenVariable("page", page - 1) sensitive page > 0
            text "[page + 1] / [(len(cg_album_entries) + 11) // 12]" size 32 color "#382f32" yalign 0.5
            textbutton _("次へ") action SetScreenVariable("page", page + 1) sensitive (page + 1) * 12 < len(cg_album_entries)
        textbutton _("戻る") xpos 100 yalign 0.93 action Return()
    else:
        $ viewed = viewed_cg_stages(cg_album_entries[selected][1])
        add Transform(viewed[variant][1], xysize=(1632, 918)) xalign 0.5
        hbox:
            align (0.5, 0.94)
            spacing 46
            for i, (stage, path) in enumerate(viewed):
                $ caption = _("全彩再読") if stage == "FULL" else _("初周") if len([s for s, p in cg_album_entries[selected][1] if s != "FULL"]) == 1 else _("初周") + " " + stage
                textbutton caption action SetScreenVariable("variant", i) selected variant == i
        textbutton _("一覧へ") xpos 100 yalign 0.94 action SetScreenVariable("selected", None)
        key "game_menu" action SetScreenVariable("selected", None)

