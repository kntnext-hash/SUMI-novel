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
    }
    story_sound_stops = {("story_ch06.rpy", 230)}

    def play_story_sound(event, interact=True, **kwargs):
        if event != "begin" or not interact:
            return
        filename, line = renpy.get_filename_line()
        key = (audio_cue_os.path.basename(filename), line)
        if key in story_sound_stops:
            renpy.music.stop(channel="sound", fadeout=0.08)
        if renpy.is_skipping() or renpy.in_rollback():
            return
        cue = story_sound_cues.get(key)
        if cue:
            renpy.music.play(cue[0], channel="sound", loop=False, relative_volume=cue[1])

    config.all_character_callbacks.append(play_story_sound)

define config.sample_sound = "audio/notification_soft.wav"
