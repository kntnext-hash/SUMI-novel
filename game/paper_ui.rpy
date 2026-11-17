# Shared paper surfaces for the in-game interface.
init 10:
    style main_menu_frame:
        background Solid("#f3f1e9ed")
    style game_menu_outer_frame:
        background Solid("#f3f1e9f5")
        xfill True
        yfill True
    style main_menu_vbox:
        xmaximum 1000
        spacing 12
    style main_menu_title:
        color "#242424"
        size 72
        outlines [(3, "#f3f1e9", 0, 0)]
    style main_menu_subtitle is main_menu_text:
        color "#242424"
        size 32
        outlines [(2, "#f3f1e9", 0, 0)]
    style main_menu_version:
        color "#242424"
        outlines [(2, "#f3f1e9", 0, 0)]
    style navigation_button:
        hover_background Solid("#dedcd3")
        selected_background Solid("#dedcd3")
    style confirm_frame:
        background Frame("ui/ui_nvl_washi.png", 24, 24)
        padding (64, 48)
    style notify_text:
        color "#ffffff"
    style skip_text:
        color "#ffffff"
    style pref_vbox:
        xsize 420
    style radio_button:
        foreground None
        padding (16, 10)
        selected_background Solid("#d4d2c9")
        selected_idle_background Solid("#d4d2c9")
        selected_hover_background Solid("#c4c2b9")
        hover_background Solid("#e3e1d8")
    style check_button:
        foreground None
        padding (16, 10)
        selected_background Solid("#d4d2c9")
        selected_idle_background Solid("#d4d2c9")
        selected_hover_background Solid("#c4c2b9")
        hover_background Solid("#e3e1d8")
    style radio_button_text:
        selected_bold True
    style check_button_text:
        selected_bold True
    style slider:
        left_bar Solid("#646464")
        right_bar Solid("#d0cec6")
        thumb Solid("#242424", xsize=16, ysize=28)
        hover_thumb Solid("#000000", xsize=16, ysize=28)
    style choice_button:
        background Frame("ui/ui_choice_idle.png", 24, 24)
        hover_background Frame("ui/ui_choice_hover.png", 24, 24)
        padding (48, 28)
    style choice_button_text:
        color "#242424"
        hover_color "#000000"
    style slot_button:
        background Frame("ui/ui_slot_idle.png", 24, 24)
        hover_background Frame("ui/ui_slot_hover.png", 24, 24)
    style slot_button_text:
        color "#242424"
        hover_color "#000000"
    style quick_button:
        background Solid("#f3f1e9ee")
        hover_background Solid("#ffffff")
        padding (12, 8)
    style quick_button_text:
        color "#242424"
        hover_color "#000000"
        selected_color "#000000"
