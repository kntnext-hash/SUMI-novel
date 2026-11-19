# Completion records are separate from personal saves. Legacy clear flags remain valid.
default persistent.completed_endings = set()

init python:
    def merge_completed_endings(old, new, current):
        return set(old or ()) | set(new or ()) | set(current or ())

    renpy.register_persistent("completed_endings", merge_completed_endings)

    ending_titles = (("A", "一個ずつ"), ("B", "途中のページ"),
                     ("C", "おかわり"), ("D", "もう一度、そっちから"))

    def record_completed_ending(event, **kwargs):
        if event != "begin":
            return
        stmt = renpy.game.script.lookup(renpy.game.context().current)
        if not isinstance(stmt, renpy.ast.Say) or stmt.what != "―― 終 ――":
            return
        filename = stmt.filename.replace("\\", "/").rsplit("/", 1)[-1]
        for code, title in ending_titles:
            if filename == "story_end_" + code.lower() + ".rpy":
                persistent.completed_endings = set(persistent.completed_endings or ()) | {code}
                persistent.unlocked_reread = True
                renpy.save_persistent()
                break

    config.all_character_callbacks.append(record_completed_ending)

    def last_choice_entry():
        # Resolve the original statement, retaining generated script/save identities.
        matches = [stmt for stmt in renpy.game.script.all_stmts
                   if isinstance(stmt, renpy.ast.Say)
                   and stmt.filename.replace("\\", "/").endswith("/story_ch12.rpy")
                   and stmt.what == "「もう一軒だけ寄ってく？」"]
        if len(matches) != 1:
            raise Exception("Last-choice entry must resolve to exactly one story statement.")
        return matches[0].name

label ending_revisit_first:
    if not persistent.unlocked_reread:
        return
    $ reread = False
    jump ending_revisit_begin

label ending_revisit_full:
    if not persistent.unlocked_reread:
        return
    $ reread = True
    jump ending_revisit_begin

label ending_revisit_begin:
    if not persistent.unlocked_reread:
        return
    stop music fadeout 0.3
    $ stop_story_audio_at_node("node_C12S06", False)
    nvl clear
    if reread:
        scene cg_book_march__full with dissolve
    else:
        scene cg_book_march__5 with dissolve
    $ renpy.block_rollback()
    $ renpy.jump(last_choice_entry())

screen ending_navigation():
    if main_menu and persistent.unlocked_reread:
        textbutton _("最後の選択から") action ShowMenu("ending_revisit")
    textbutton _("エンディング一覧") action ShowMenu("ending_records")

screen ending_revisit():
    tag menu
    use game_menu(_("最後の選択から"), scroll="viewport", spacing=32):
        if persistent.unlocked_reread:
            text _("第12章の最後の選択に戻ります。")
            text _("セーブデータは上書きされません。") size 28
            textbutton _("初周の色彩で読む") action Start("ending_revisit_first")
            textbutton _("全彩再読で読む") action Start("ending_revisit_full")
        else:
            text _("物語を一度読み終えると利用できます。")

screen ending_records():
    tag menu
    use game_menu(_("エンディング一覧"), scroll="viewport", spacing=30):
        $ completed = set(persistent.completed_endings or ())
        $ completed_count = len(completed)
        text _("読了した結末　[completed_count] / 4")
        for code, title in ending_titles:
            if code in completed:
                text "[code]　[title]　— 読了"
            else:
                text "[code]　未読" color "#777777"
        if persistent.unlocked_reread and not completed:
            text _("旧版のクリア記録を引き継いでいます。\n各エンディングの読了記録は、次に読み終えたときに追加されます。") size 26
        if persistent.unlocked_reread:
            textbutton _("最後の選択から") action ShowMenu("ending_revisit")
