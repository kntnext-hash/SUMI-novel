# Run the two testcases in separate processes with the same isolated savedir.
init 90 python:
    import json as qs_json
    import os as qs_os
    import sys as qs_sys
    import types as qs_types
    qs = qs_sys.modules.setdefault("_adv_checkpoint_qa", qs_types.ModuleType("_adv_checkpoint_qa"))
    qs.cues = []
    qs.location = None
    qs.play = renpy.music.play

    def qs_play(filenames, *args, **kwargs):
        if filenames == "audio/school_chime_original.wav":
            qs.cues.append(list(adv_original_location(*renpy.get_filename_line())))
        return qs.play(filenames, *args, **kwargs)
    renpy.music.play = qs_play

    def qs_say(event, **kwargs):
        if event == "begin":
            qs.location = list(adv_original_location(*renpy.get_filename_line()))
    config.all_character_callbacks.append(qs_say)

    def qs_snapshot():
        return dict(mode=reread, location=qs.location, history=[entry.what for entry in _history_list[-3:]],
                    images=sorted([tag, list(renpy.get_attributes(tag) or ())] for tag in renpy.get_showing_tags()),
                    ambience=renpy.music.get_playing("story_ambience"))

    def qs_result(name, data):
        with open(qs_os.path.join(config.basedir, name + ".json"), "w", encoding="utf-8") as file:
            qs_json.dump(data, file, indent=2, ensure_ascii=False)

testcase qa_split_checkpoint:
    pause until screen "main_menu" timeout 30
    run Start("node_C03S05")
    advance until eval (qs.location == ["story_ch03.rpy", 199, 0, 2]) timeout 60
    pause until eval (renpy.music.get_playing("sound") == "audio/school_chime_original.wav") timeout 5
    advance until eval (qs.location == ["story_ch03.rpy", 199, 1, 2]) timeout 10
    pause 0.2
    $ qs.saved = qs_snapshot()
    assert eval (qs.saved["history"][-2].startswith("廊下で") and qs.saved["history"][-1].startswith("六時のチャイム"))
    assert eval (len(qs.cues) == 1)
    run FileSave("middle", confirm=False, page="split")
    pause until eval (renpy.can_load("split-middle")) timeout 10
    advance until eval (qs.location[:3] == ["story_ch03.rpy", 200, 0]) timeout 10
    run Rollback()
    pause until eval (qs.location == ["story_ch03.rpy", 199, 1, 2]) timeout 10
    pause 0.2
    assert eval (qs_snapshot() == qs.saved)
    assert eval (len(qs.cues) == 1)
    $ qs_result("split_checkpoint", dict(saved=qs.saved, cues=qs.cues))

testcase qa_split_checkpoint_restart:
    pause until screen "main_menu" timeout 30
    $ qs.saved = qs_json.load(open(qs_os.path.join(config.basedir, "split_checkpoint.json"), encoding="utf-8"))["saved"]
    run FileLoad("middle", confirm=False, page="split")
    pause until eval (qs.location == ["story_ch03.rpy", 199, 1, 2]) timeout 10
    pause 0.2
    assert eval (qs_snapshot() == qs.saved and not qs.cues)
    $ qs.restored = qs_snapshot()
    run Rollback()
    pause until eval (qs.location == ["story_ch03.rpy", 199, 0, 2]) timeout 10
    assert eval (not qs.cues)
    advance until eval (qs.location == ["story_ch03.rpy", 199, 1, 2]) timeout 10
    pause 0.2
    assert eval (qs_snapshot() == qs.saved and not qs.cues)
    advance until eval (qs.location[:3] == ["story_ch03.rpy", 200, 0]) timeout 10
    $ qs_result("split_checkpoint_restart", dict(restored=qs.restored, next=qs_snapshot(), cues=qs.cues))
