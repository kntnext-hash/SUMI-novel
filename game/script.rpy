# 『顔のない春 ――きみの色が見えるまで。』
# 本編は story_*.rpy（scenario.json から自動変換）。表示形式は NVL。

define narrator = Character(None, kind=nvl)

define config.adv_nvl_transition = Dissolve(0.25)
define config.nvl_adv_transition = Dissolve(0.25)

default reread = False

label start:
    $ reread = False
    jump node_C01S01

label reread_start:
    $ reread = True
    jump node_C01S01
