# Source line cues keep the generated story text and branching unchanged.
# See rooms/07_音響部屋/audio/README.md for manuscript references.
init 10 python:
    # Audio locations use the original paragraph and zero-based ADV page.
    story_sound_cues = {
        ("story_ch05.rpy", 178, 0): ("audio/firework_single_5.wav", 0.26),
        ("story_ch05.rpy", 226, 0): ("audio/firework_single_5.wav", 0.18),
        ("story_ch01.rpy", 227, 0): ("audio/bicycle_bell_single.wav", 0.31),
        ("story_ch06.rpy", 79, 1): ("audio/thermos_set_down.wav", 0.42),
        ("story_ch01.rpy", 72, 0): ("audio/school_chime_original.wav", 0.35),
        ("story_ch03.rpy", 199, 0): ("audio/school_chime_original.wav", 0.30),
        ("story_ch11.rpy", 220, 0): ("audio/school_chime_original.wav", 0.35),
        # Other students' phones; Sumi's own notifications remain disabled.
        ("story_ch02.rpy", 171, 0): ("audio/notification_soft.wav", 0.22),
        ("story_ch02.rpy", 179, 0): ("audio/notification_soft.wav", 0.40),
        ("story_ch04.rpy", 93, 0): ("audio/notification_soft.wav", 0.40),
        ("story_ch04.rpy", 208, 0): ("audio/notification_soft.wav", 0.40),
        ("story_ch06.rpy", 229, 0): ("audio/ringtone_original.wav", 0.35),
        ("story_ch07.rpy", 106, 0): ("audio/camera_shutter.wav", 0.40),
        ("story_ch07.rpy", 209, 0): ("audio/book_drop.wav", 0.40),
        ("story_ch11.rpy", 57, 0): ("audio/pot_water.wav", 0.65),
        ("story_ch09.rpy", 142, 0): ("audio/cinema_wood_paper.wav", 0.40),
        ("story_ch09.rpy", 143, 0): ("audio/small_bell_single.wav", 0.40),
        ("story_ch09.rpy", 146, 0): ("audio/cinema_paper_two_bells.wav", 0.40),
    }
    story_sound_stops = {
        ("story_ch06.rpy", 230),
        # The bell is deliberately silent while it is passed between them.
        ("story_ch09.rpy", 144),
        ("story_ch09.rpy", 145),
    }

    # Separate from one-shot effects so notifications do not cut off ambience.
    renpy.music.register_channel("story_ambience", mixer="sfx", loop=True)
    bicycle_channels = ("story_bicycle_near", "story_bicycle_far")
    for channel in bicycle_channels:
        renpy.music.register_channel(channel, mixer="sfx", loop=False)
    config.main_menu_stop_channels.extend(("story_ambience",) + bicycle_channels)
    bicycle_pass = "audio/bicycle_pass_full.wav"
    bridge_wind = "audio/park_wind_loop.wav"
    courtyard_water = "audio/kitchen_sink_loop.wav"

    def stop_story_bicycles():
        for channel in bicycle_channels:
            renpy.music.stop(channel=channel, fadeout=0.08)

    def play_story_bicycles(line):
        if line == 29:
            renpy.music.play("<from 2.15 to 7.3>" + bicycle_pass, channel="story_bicycle_near",
                             loop=False, fadein=0.09, relative_volume=0.38)
            renpy.music.play("<from 1.55 to 6.8>" + bicycle_pass, channel="story_bicycle_far",
                             loop=False, fadein=0.09, relative_volume=0.25)
        elif line == 227:
            renpy.music.play(["<silence 0.45>", "<from 3.2 to 7.7>" + bicycle_pass],
                             channel="story_bicycle_near", loop=False, relative_volume=0.30)

    story_ambience_cues = {
        ("story_ch03.rpy", 141): ("audio/rain_loop.wav", 0.30),
        ("story_ch11.rpy", 57): ("audio/fridge_loop.wav", 0.40),
    }

    def stop_story_audio_at_node(name, abnormal):
        if name.startswith("node_"):
            renpy.music.stop(channel="story_ambience", fadeout=0.15)
            renpy.music.stop(channel="sound", fadeout=0.08)
            stop_story_bicycles()

    config.label_callbacks.append(stop_story_audio_at_node)

    def play_story_sound(event, interact=True, **kwargs):
        if event != "begin" or not interact:
            return
        filename, line = renpy.get_filename_line()
        source, original, part, count = adv_original_location(filename, line)
        key = (source, original)
        if not source.startswith("story_"):
            return
        if not part and key in story_sound_stops:
            renpy.music.stop(channel="sound", fadeout=0.08)
        if source == "story_ch01.rpy" and (original in (34, 229) or renpy.is_skipping()):
            stop_story_bicycles()

        # Restore sustained sounds even when a save resumes inside their range.
        ambience = story_ambience_cues.get(key) if not part else None
        if source == "story_ch01.rpy" and 229 <= original <= 232:
            ambience = (bridge_wind, 0.22)
        elif source == "story_end_r.rpy" and 33 <= original <= 36:
            ambience = (courtyard_water, 0.13)
        playing = renpy.music.get_playing("story_ambience")
        if ambience and not renpy.is_skipping():
            if playing != ambience[0]:
                fade = 0.25 if ambience[0] in (bridge_wind, courtyard_water) else 0.20
                renpy.music.play(ambience[0], channel="story_ambience", loop=True,
                                 fadein=fade, relative_volume=ambience[1])
        elif playing in (bridge_wind, courtyard_water) or key in (("story_ch01.rpy", 237), ("story_end_r.rpy", 37)):
            renpy.music.stop(channel="story_ambience", fadeout=0)

        if renpy.is_skipping() or renpy.in_rollback():
            return
        if source == "story_ch01.rpy" and not part:
            play_story_bicycles(original)
        cue = story_sound_cues.get((source, original, part))
        if cue:
            renpy.music.play(cue[0], channel="sound", loop=False, relative_volume=cue[1])

    config.all_character_callbacks.append(play_story_sound)

define config.sample_sound = "audio/notification_soft.wav"
