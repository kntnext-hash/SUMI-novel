# Shared paper surfaces for the in-game interface.
init 10:
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
