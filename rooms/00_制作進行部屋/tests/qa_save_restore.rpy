# Test-only fixtures: isolated savedir required.
init -90 python:
    import sys as qsr_sys
    import types as qsr_types
    import json as qsr_json
    import os as qsr_os
    qsr = qsr_sys.modules.setdefault("_save_restore_qa", qsr_types.ModuleType("_save_restore_qa"))
    qsr.results = []
    qsr.position = None
    qsr.output = "save_restore_results.json"

    def qsr_say(event, **kwargs):
        if event == "begin":
            filename, line = renpy.get_filename_line()
            if qsr_os.path.basename(filename).startswith("story"):
                qsr.position = [qsr_os.path.basename(filename), line]
    config.all_character_callbacks.append(qsr_say)

    def qsr_snapshot():
        return dict(mode=reread, position=qsr.position,
                    images=sorted([tag, list(renpy.get_attributes(tag) or ())] for tag in renpy.get_showing_tags()),
                    text=_history_list[-1].what if _history_list else None)

    def qsr_check(name):
        actual = qsr_snapshot()
        result = dict(checkpoint=name, expected=qsr.expected, actual=actual, passed=actual == qsr.expected)
        qsr.results.append(result)
        with open(qsr_os.path.join(config.basedir, qsr.output), "w", encoding="utf-8") as f:
            qsr_json.dump(qsr.results, f, ensure_ascii=False, indent=2)
        assert actual == qsr.expected, repr(result)

label qa_save_C01S01_0:
    $ reread = False
    jump node_C01S01

label qa_save_C01S02_0:
    $ reread = False
    jump node_C01S02

label qa_save_C06S05_0:
    $ reread = False
    jump node_C06S05

label qa_save_C12S06_0:
    $ reread = False
    jump node_C12S06

label qa_save_EDS01_0:
    $ reread = False
    jump node_EDS01

label qa_save_C01S01_1:
    $ reread = True
    jump node_C01S01

label qa_save_C01S02_1:
    $ reread = True
    jump node_C01S02

label qa_save_C06S05_1:
    $ reread = True
    jump node_C06S05

label qa_save_C12S06_1:
    $ reread = True
    jump node_C12S06

label qa_save_EDS01_1:
    $ reread = True
    jump node_EDS01

testcase qa_save_restore:
    $ qsr.results.clear()
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S01_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == False)
    run FileSave("C01S01_0", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-C01S01_0"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("C01S01_0", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("C01S01_0")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C06S05_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == False)
    run FileSave("C06S05_0", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-C06S05_0"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("C06S05_0", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("C06S05_0")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C12S06_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == False)
    run FileSave("C12S06_0", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-C12S06_0"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("C12S06_0", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("C12S06_0")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_EDS01_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == False)
    run FileSave("EDS01_0", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-EDS01_0"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("EDS01_0", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("EDS01_0")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S01_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == True)
    run FileSave("C01S01_1", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-C01S01_1"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("C01S01_1", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("C01S01_1")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C06S05_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == True)
    run FileSave("C06S05_1", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-C06S05_1"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("C06S05_1", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("C06S05_1")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C12S06_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == True)
    run FileSave("C12S06_1", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-C12S06_1"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("C12S06_1", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("C12S06_1")

    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_EDS01_1")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr.expected = qsr_snapshot()
    assert eval (qsr.expected['mode'] == True)
    run FileSave("EDS01_1", confirm=False, page="qa")
    pause 0.3
    assert eval (renpy.can_load("qa-EDS01_1"))
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.position = None
    run Start("qa_save_C01S02_0")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    assert eval (reread != qsr.expected['mode'])
    run FileLoad("EDS01_1", confirm=False, page="qa")
    pause 1.0
    $ qsr_check("EDS01_1")

testcase qa_saved_restart:
    $ qsr.saved = qsr_json.load(open(qsr_os.path.join(config.basedir, "save_restore_results.json"), encoding="utf-8"))
    assert eval (len(qsr.saved) == 8 and all(item['passed'] for item in qsr.saved))
    $ qsr.results.clear()
    $ qsr.output = "save_restart_results.json"
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[0]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[0]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[0]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[1]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[1]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[1]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[2]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[2]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[2]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[3]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[3]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[3]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[4]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[4]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[4]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[5]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[5]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[5]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[6]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[6]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[6]['checkpoint'])
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 30
    $ qsr.expected = qsr.saved[7]['expected']
    $ qsr.position = None
    run FileLoad(qsr.saved[7]['checkpoint'], confirm=False, page="qa")
    pause until eval (qsr.position is not None) timeout 30
    pause 0.3
    $ qsr_check(qsr.saved[7]['checkpoint'])
