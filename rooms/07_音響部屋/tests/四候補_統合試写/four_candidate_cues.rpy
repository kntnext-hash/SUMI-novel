# Standalone trial layer. Copy with its four credited WAV files into a QA game.
init 15 python:
    four_bike_channels = ("four_bike_near", "four_bike_far")
    for four_channel in four_bike_channels:
        renpy.music.register_channel(four_channel, mixer="sfx", loop=False)
    renpy.music.register_channel("four_outdoors", mixer="sfx", loop=True)
    config.main_menu_stop_channels.extend((*four_bike_channels, "four_outdoors"))

    def four_stop_bikes(fade=0.08):
        for channel in four_bike_channels:
            renpy.music.stop(channel=channel, fadeout=fade)

    def four_reset(name, abnormal):
        if name.startswith("node_"):
            four_stop_bikes()
            renpy.music.stop(channel="four_outdoors", fadeout=0.1)

    def four_audio(event, interact=True, **kwargs):
        if event != "begin" or not interact:
            return
        source, line, part, total = adv_original_location(*renpy.get_filename_line())
        if not source.startswith("story_"):
            return
        bed = None
        if source == "story_ch01.rpy" and 229 <= line <= 232:
            bed = ("audio/park_wind_loop.wav", 0.22)
        elif source == "story_end_r.rpy" and 33 <= line <= 36:
            bed = ("audio/kitchen_sink_loop.wav", 0.13)
        current = renpy.music.get_playing("four_outdoors")
        if not bed or renpy.is_skipping():
            if current:
                renpy.music.stop(channel="four_outdoors", fadeout=0.0)
        elif current != bed[0]:
            renpy.music.play(bed[0], channel="four_outdoors", loop=True, fadein=0.25,
                             relative_volume=bed[1])

        if part or source != "story_ch01.rpy":
            return
        if line in (34, 229) or renpy.is_skipping():
            four_stop_bikes()
        if renpy.in_rollback() or renpy.is_skipping():
            return
        if line == 29:
            # The pair approaches side by side. Offset the peaks of the single recording.
            renpy.music.play("<from 2.15 to 7.3>audio/bicycle_pass_full.wav",
                             channel="four_bike_near", loop=False, fadein=0.09, relative_volume=0.38)
            renpy.music.play("<from 1.55 to 6.8>audio/bicycle_pass_full.wav",
                             channel="four_bike_far", loop=False, fadein=0.09, relative_volume=0.25)
        elif line == 227:
            renpy.music.play("audio/bicycle_bell_single.wav", channel="sound", loop=False, relative_volume=0.31)
            renpy.music.play(["<silence 0.45>", "<from 3.2 to 7.7>audio/bicycle_pass_full.wav"],
                             channel="four_bike_near", loop=False, relative_volume=0.3)

    config.label_callbacks.append(four_reset)
    config.all_character_callbacks.append(four_audio)
