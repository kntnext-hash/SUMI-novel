"""Check the additional CG cues against protected text, audio and source metadata."""
import ast
import csv
import hashlib
import json
import re
from pathlib import Path
from regenerate_visual_cues import ROOT, GAME, SOURCE, QA, paragraphs


def main():
    review = ROOT / 'rooms/01_物語作成部屋/reviews/CGキュー追加_20261120'
    backup = review / 'protection'
    result = {}
    count = 0
    for path in GAME.glob('story_*.rpy'):
        old = paragraphs((backup / 'game' / path.name).read_text(encoding='utf-8'))
        new = paragraphs(path.read_text(encoding='utf-8'))
        assert old.keys() == new.keys()
        assert all(old[k][1] == new[k][1] for k in old), path
        count += len(new)
    result['unchanged_paragraphs'] = count

    def audio(base):
        text = (base / 'game/audio_cues.rpy').read_text(encoding='utf-8')
        entries = []
        for m in re.finditer(r'\("(story_[^"]+)", (\d+)(?:, (\d+))?\)', text):
            file, num, part = m.groups()
            lines = (base / 'game' / file).read_text(encoding='utf-8').splitlines()
            entries.append((file, lines[int(num)-1], part))
        return entries
    assert audio(backup) == audio(ROOT)
    result['audio_locations_preserved'] = len(audio(ROOT))
    adv = (GAME / 'adv_passages.rpy').read_text(encoding='utf-8').splitlines()
    count = 0
    for line in adv:
        if re.match(r"        \(\d+, 'story_", line):
            first, file, original, pages = ast.literal_eval(line.strip().rstrip(','))
            statement = (GAME / file).read_text(encoding='utf-8').splitlines()[original-1]
            assert statement.startswith('    call ')
            assert adv[first-2] == 'label ' + statement.split()[1] + ':'
            assert all(s.startswith('    "') for s in adv[first-1:first+pages-1])
            count += 1
    result['adv_mappings_valid'] = count
    for path in (backup / 'game/images').glob('CG_hands*'):
        assert path.read_bytes() == (GAME / 'images' / path.name).read_bytes()
    result['hands_images_unchanged'] = 3
    scenario = json.loads((SOURCE / 'scenario.json').read_text(encoding='utf-8'))
    rows = list(csv.reader((SOURCE / '画像と演出/Muse_本文キュー.tsv').open(encoding='utf-8-sig'), delimiter='\t'))[1:]
    assert len(rows) == 180
    for row in rows:
        assert row[2] in scenario['nodes'][row[0]]['lines'][int(row[1])-1], row
    result['source_cues_valid'] = len(rows)
    # Verify the immediate scene at each target paragraph in both reading modes.
    for node, filename in [('C05S06', 'story_ch05.rpy'), ('C08S07', 'story_ch08.rpy'), ('ERS02', 'story_end_r.rpy')]:
        text = (GAME / filename).read_text(encoding='utf-8')
        locations = paragraphs(text)
        lines = text.splitlines()
        for cue in scenario['nodes'][node]['visual_cues']:
            physical, _ = locations[(node, cue['before_line'])]
            block = '\n'.join(lines[max(0, physical-10):physical-1])
            assert 'scene ' + cue['asset'].lower() + '__' + cue['stage'].lower() + ' with ' in block
            assert 'scene ' + cue['asset'].lower() + '__full with ' in block
    data = json.loads((QA / 'qa_image_expectations.json').read_text(encoding='utf-8'))
    ids = [c['id'] for row in data.values() for c in row['cues']]
    assert sorted(ids) == list(range(1, 181))
    assert len(data) == 2590
    result['qa_cue_ids'] = len(ids)
    (review / 'static_results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
