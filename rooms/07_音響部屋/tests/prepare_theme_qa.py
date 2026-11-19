from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parent
game = ROOT.parents[2]/'game'
target = ROOT/'theme_run'/'game'
target.mkdir(parents=True,exist_ok=True)
for source in game.glob('*.rpy'):
    shutil.copy2(source,target/source.name)
options = target/'options.rpy'
options.write_text(options.read_text(encoding='utf-8').replace('kaononaiharu-long-1','sumi-theme-qa-20261119'),encoding='utf-8')
shutil.copy2(ROOT/'qa_theme_music.rpy',target/'qa_theme_music.rpy')
(target/'qa_searchpath.rpy').write_text('init 99 python:\n    config.searchpath.append('+repr(str(game))+')\n    config.save_directory = "sumi_theme_isolated_20261119"\n',encoding='utf-8')
print(target.parent)
