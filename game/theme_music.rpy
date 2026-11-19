# Original title/end theme, isolated from generated story and screen files.
init 30 python:
    config.has_music = True
    config.main_menu_music = "audio/spring_afterglow_original.wav"

    def spring_theme_at_label(name, abnormal):
        # Start/restart/replay must not bring title music into the manuscript.
        if name in ("start", "reread_start", "opening_replay") or name.startswith("node_"):
            renpy.music.stop(channel="music", fadeout=0.6)

    def spring_theme_at_say(event, interact=True, **kwargs):
        if event != "begin" or not interact:
            return
        source, line = renpy.get_filename_line()
        source, original, part, count = adv_original_location(source, line)
        if not source.startswith("story_"):
            return
        # Text-based cue survives regeneration and ADV paragraph splitting.
        ending = source.startswith("story_end_") and renpy.last_say().what == "―― 終 ――"
        playing = renpy.music.get_playing(channel="music")
        if ending:
            # A rapid skip may reach this card during the title's pending
            # fadeout. Always replace that queue instead of trusting get_playing.
            renpy.music.play(config.main_menu_music, channel="music", loop=True, fadein=2.0)
        elif playing == config.main_menu_music:
            # Also covers load and rollback from the end card into prose.
            renpy.music.stop(channel="music", fadeout=0.35)

    config.label_callbacks.append(spring_theme_at_label)
    config.all_character_callbacks.append(spring_theme_at_say)
