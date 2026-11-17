# Source line cues keep the generated story text and branching unchanged.
# See rooms/07_音響部屋/audio/README.md for manuscript references.
init 10 python:
    import os as audio_cue_os

    story_sound_cues = {
        ("story_ch01.rpy", 72): ("audio/school_chime_original.wav", 0.35),
        ("story_ch03.rpy", 199): ("audio/school_chime_original.wav", 0.30),
        ("story_ch11.rpy", 220): ("audio/school_chime_original.wav", 0.35),
        # Other students' phones; Sumi's own notifications remain disabled.
        ("story_ch02.rpy", 171): ("audio/notification_soft.wav", 0.22),
        ("story_ch02.rpy", 179): ("audio/notification_soft.wav", 0.40),
        ("story_ch04.rpy", 93): ("audio/notification_soft.wav", 0.40),
        ("story_ch04.rpy", 208): ("audio/notification_soft.wav", 0.40),
        ("story_ch06.rpy", 229): ("audio/ringtone_original.wav", 0.35),
        ("story_ch07.rpy", 106): ("audio/camera_shutter.wav", 0.40),
    }
    story_sound_stops = {("story_ch06.rpy", 230)}

    # Separate from one-shot effects so notifications do not cut off ambience.
    renpy.music.register_channel("story_ambience", mixer="sfx", loop=True)
    config.main_menu_stop_channels.append("story_ambience")
    story_ambience_cues = {
        ("story_ch03.rpy", 141): ("audio/rain_loop.wav", 0.30),
        ("story_ch11.rpy", 57): ("audio/fridge_loop.wav", 0.40),
    }

    def stop_story_ambience_at_node(name, abnormal):
        if name.startswith("node_"):
            renpy.music.stop(channel="story_ambience", fadeout=0.15)

    config.label_callbacks.append(stop_story_ambience_at_node)

    def play_story_sound(event, interact=True, **kwargs):
        if event != "begin" or not interact:
            return
        filename, line = renpy.get_filename_line()
        key = (audio_cue_os.path.basename(filename), line)
        if key in story_sound_stops:
            renpy.music.stop(channel="sound", fadeout=0.08)
        # Loop state must also be established when loading/rolling back to
        # this paragraph; one-shot sounds below should not be replayed then.
        ambience = story_ambience_cues.get(key)
        if ambience and not renpy.is_skipping():
            renpy.music.play(ambience[0], channel="story_ambience", loop=True,
                             fadein=0.20, relative_volume=ambience[1])
        if renpy.is_skipping() or renpy.in_rollback():
            return
        cue = story_sound_cues.get(key)
        if cue:
            renpy.music.play(cue[0], channel="sound", loop=False, relative_volume=cue[1])

    config.all_character_callbacks.append(play_story_sound)

define config.sample_sound = "audio/notification_soft.wav"
