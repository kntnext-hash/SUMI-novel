init 95 python:
    import json as theme_qa_json
    import os as theme_qa_os
    config.label_overrides['splashscreen'] = 'theme_qa_no_op'
    theme_qa_rows = []
    theme_qa_text = None
    def theme_qa_observe(event, **kwargs):
        global theme_qa_text
        if event == 'begin':
            theme_qa_text = renpy.last_say().what
    config.all_character_callbacks.append(theme_qa_observe)
    def theme_qa_check(name, condition):
        theme_qa_rows.append(dict(test=name,passed=bool(condition),playing=renpy.music.get_playing('music')))
        with open(theme_qa_os.path.join(config.basedir,'theme_results.json'),'w',encoding='utf-8') as out:
            theme_qa_json.dump(theme_qa_rows,out,ensure_ascii=False,indent=2)
        assert condition, name

label theme_qa_no_op:
    return

testcase qa_theme_music:
    pause until screen 'main_menu' timeout 90
    pause 0.5
    $ theme_qa_check('title_music', renpy.music.get_playing('music') == config.main_menu_music)
    run ShowMenu('preferences')
    pause 0.2
    $ theme_qa_check('music_slider_visible', config.has_music and renpy.get_screen('preferences') is not None)
    run Preference('music volume', 0.23)
    $ theme_qa_check('music_volume_adjustable', abs(preferences.get_volume('music') - 0.23) < 0.001)
    run Preference('music mute', 'enable')
    $ theme_qa_check('music_mute', preferences.get_mute('music'))
    run Preference('music mute', 'disable')
    run Return()
    run Start('start')
    pause 1.0
    $ theme_qa_check('story_stops_title', renpy.music.get_playing('music') is None)
    run MainMenu(confirm=False)
    pause until screen 'main_menu' timeout 30
    $ preferences.text_cps = 0
    run Start('node_EAS04')
    advance until eval (theme_qa_text == '―― 終 ――') timeout 60
    pause 0.3
    $ theme_qa_check('end_a_theme', renpy.music.get_playing('music') == config.main_menu_music)
    run MainMenu(confirm=False)
    pause until screen 'main_menu' timeout 30
    $ theme_qa_text = None
    run Start('node_EBS04')
    advance until eval (theme_qa_text == '―― 終 ――') timeout 60
    pause 0.3
    $ theme_qa_check('end_b_theme', renpy.music.get_playing('music') == config.main_menu_music)
    run MainMenu(confirm=False)
    pause until screen 'main_menu' timeout 30
    $ theme_qa_text = None
    run Start('node_ECS04')
    advance until eval (theme_qa_text == '―― 終 ――') timeout 60
    pause 0.3
    $ theme_qa_check('end_c_theme', renpy.music.get_playing('music') == config.main_menu_music)
    run MainMenu(confirm=False)
    pause until screen 'main_menu' timeout 30
    $ theme_qa_text = None
    run Start('node_EDS04')
    advance until eval (theme_qa_text == '―― 終 ――') timeout 60
    pause 0.3
    $ theme_qa_check('end_d_theme', renpy.music.get_playing('music') == config.main_menu_music)
    run MainMenu(confirm=False)
    pause until screen 'main_menu' timeout 30
    run Start('reread_start')
    pause 1.0
    $ theme_qa_check('reread_stops_theme', renpy.music.get_playing('music') is None)
