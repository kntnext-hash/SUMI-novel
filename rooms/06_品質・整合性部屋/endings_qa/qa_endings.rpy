init 999 python:
    config.save_directory = "SUMI-ending-isolated-qa"
    config.savedir = config.basedir + "/isolated_saves"
    preferences.text_cps = 0
    config.skip_delay = 0

default qa_unused = False

label qa_legacy_a:
    $ reread = False
    jump node_EAS04

label qa_legacy_d:
    $ reread = True
    jump node_EDS05

testcase legacy:
    advance until screen "main_menu" timeout 120
    run Start("qa_legacy_a")
    pause 0.5
    $ renpy.save("legacy-a")
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("qa_legacy_d")
    pause 0.5
    $ renpy.save("legacy-d")
    advance until screen "main_menu" timeout 120
    $ renpy.save_persistent()

init python:
    def qa_choice(caption):
        s = renpy.get_screen("choice")
        return s is not None and any(i.caption == caption for i in s.scope.get("items", ()))

    def qa_revisit_image(full):
        assert reread == full
        assert renpy.showing("cg_book_march__full" if full else "cg_book_march__5")

    def qa_records(expected):
        assert set(persistent.completed_endings or ()) == set(expected), repr(persistent.completed_endings)

testcase endings:
    advance until screen "main_menu" timeout 120
    $ persistent.completed_endings = set()
    $ persistent.unlocked_reread = True
    $ qa_records("")
    $ assert persistent.unlocked_reread
    $ assert merge_completed_endings({"A"}, {"B"}, {"D"}) == {"A", "B", "D"}
    run ShowMenu("ending_records")
    pause 0.3
    run Return()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    $ qa_records("")
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    $ renpy.load("legacy-a")
    pause 0.3
    $ assert not reread
    $ qa_records("")
    advance until screen "main_menu" timeout 120
    $ qa_records("A")
    $ renpy.load("legacy-d")
    pause 0.3
    $ assert reread
    $ qa_records("A")
    advance until screen "main_menu" timeout 120
    $ qa_records("AD")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あの飴、買いに行こう"
    advance until screen "main_menu" timeout 120
    $ qa_records("A")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "今日はここまでにしていい？"
    advance until screen "main_menu" timeout 120
    $ qa_records("B")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "うちに寄ってって"
    advance until screen "main_menu" timeout 120
    $ qa_records("C")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "透花、もうひとつ聞いて"
    advance until screen "main_menu" timeout 120
    $ qa_records("D")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あの飴、買いに行こう"
    advance until screen "main_menu" timeout 120
    $ qa_records("A")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "今日はここまでにしていい？"
    advance until screen "main_menu" timeout 120
    $ qa_records("B")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "うちに寄ってって"
    advance until screen "main_menu" timeout 120
    $ qa_records("C")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "透花、もうひとつ聞いて"
    advance until screen "main_menu" timeout 120
    $ qa_records("D")
    $ persistent.unlocked_reread = False
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until screen "main_menu" timeout 30
    $ qa_records("")
    run ShowMenu("ending_records")
    pause 0.3
    run Return()
    $ persistent.unlocked_reread = True
    $ persistent.completed_endings = {"A", "B"}
    $ renpy.save_persistent()

init python:
    def qa_portrait_entry():
        return next(s.name for s in renpy.game.script.all_stmts if isinstance(s, renpy.ast.Say) and s.what == "「また会ったね」" and "story_ch01" in s.filename)

label qa_portrait_first:
    $ reread = False
    scene bg_room_apr__0
    $ renpy.jump(qa_portrait_entry())

label qa_portrait_full:
    $ reread = True
    scene bg_room_apr__full
    $ renpy.jump(qa_portrait_entry())

testcase visual:
    advance until screen "main_menu" timeout 120
    $ qa_records("AB")
    pause 1.0
    screenshot "title.png"
    run ShowMenu("ending_records")
    pause 1.0
    screenshot "records.png"
    run ShowMenu("ending_revisit")
    pause 1.0
    screenshot "revisit.png"
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    pause 0.5
    screenshot "choice-first.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    pause 0.5
    screenshot "choice-full.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("qa_portrait_first")
    pause 1.0
    screenshot "portrait-first.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("qa_portrait_full")
    pause 1.0
    screenshot "portrait-full.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    $ persistent.completed_endings = set()
    $ persistent.unlocked_reread = False
    run ShowMenu("ending_records")
    pause 1.0
    screenshot "records-locked.png"

testcase final:
    advance until screen "main_menu" timeout 120
    $ persistent.completed_endings = set()
    $ persistent.unlocked_reread = True
    $ qa_records("")
    $ assert persistent.unlocked_reread
    $ assert merge_completed_endings({"A"}, {"B"}, {"D"}) == {"A", "B", "D"}
    run ShowMenu("ending_records")
    pause 0.3
    run Return()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    $ qa_records("")
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    $ renpy.load("legacy-a")
    pause 0.3
    $ assert not reread
    $ qa_records("")
    advance until screen "main_menu" timeout 120
    $ qa_records("A")
    $ renpy.load("legacy-d")
    pause 0.3
    $ assert reread
    $ qa_records("A")
    advance until screen "main_menu" timeout 120
    $ qa_records("AD")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あの飴、買いに行こう"
    advance until screen "main_menu" timeout 120
    $ qa_records("A")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "今日はここまでにしていい？"
    advance until screen "main_menu" timeout 120
    $ qa_records("B")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "うちに寄ってって"
    advance until screen "main_menu" timeout 120
    $ qa_records("C")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(False)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "透花、もうひとつ聞いて"
    advance until screen "main_menu" timeout 120
    $ qa_records("D")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あの飴、買いに行こう"
    advance until screen "main_menu" timeout 120
    $ qa_records("A")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "今日はここまでにしていい？"
    advance until screen "main_menu" timeout 120
    $ qa_records("B")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "うちに寄ってって"
    advance until screen "main_menu" timeout 120
    $ qa_records("C")
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    $ qa_revisit_image(True)
    click "あのお店の話、続きがあるの"
    advance until eval qa_choice("今日はここまでにしていい？") timeout 120
    click "あの日、下まで行きたかった"
    advance until eval qa_choice("うちに寄ってって") timeout 120
    click "透花、もうひとつ聞いて"
    advance until screen "main_menu" timeout 120
    $ qa_records("D")
    $ persistent.unlocked_reread = False
    $ persistent.completed_endings = set()
    run Start("ending_revisit_full")
    advance until screen "main_menu" timeout 30
    $ qa_records("")
    run ShowMenu("ending_records")
    pause 0.3
    run Return()
    $ persistent.unlocked_reread = True
    $ persistent.completed_endings = {"A", "B"}
    $ renpy.save_persistent()
    advance until screen "main_menu" timeout 120
    $ qa_records("AB")
    pause 1.0
    screenshot "final-title.png"
    run ShowMenu("ending_records")
    pause 1.0
    screenshot "final-records.png"
    run ShowMenu("ending_revisit")
    pause 1.0
    screenshot "final-revisit.png"
    run Start("ending_revisit_first")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    pause 0.5
    screenshot "final-choice-first.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("ending_revisit_full")
    advance until eval qa_choice("あの飴、買いに行こう") timeout 30
    pause 0.5
    screenshot "final-choice-full.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("qa_portrait_first")
    pause 1.0
    screenshot "final-portrait-first.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    run Start("qa_portrait_full")
    pause 1.0
    screenshot "final-portrait-full.png"
    run MainMenu(confirm=False)
    advance until screen "main_menu" timeout 30
    $ persistent.completed_endings = set()
    $ persistent.unlocked_reread = False
    run ShowMenu("ending_records")
    pause 1.0
    screenshot "final-records-locked.png"
