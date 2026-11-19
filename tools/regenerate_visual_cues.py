"""Regenerate node visual_cues from scenario.json, preserving ADV and story text.

Only nodes declaring visual_cues are regenerated. Existing cues elsewhere remain
in Muse_本文キュー.tsv. Physical-line consumers are remapped by paragraph identity.
Run after adding/changing scenario visual_cues; safe to repeat.
"""
import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
SOURCE = ROOT / 'kaononaiharu_long_complete/制作'
QA = ROOT / 'rooms/06_品質・整合性部屋/adv_qa'


def write(path, text):
    if path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')


def paragraphs(text):
    node, index = None, 0
    result = {}
    for line, value in enumerate(text.splitlines(), 1):
        if value.startswith('label node_'):
            node, index = value[11:-1], 0
        if node and (value.startswith('    "') and value.endswith('"') or value.startswith('    call adv_split_')):
            index += 1
            result[(node, index)] = (line, value)
    return result


def image_block(cue):
    transition = cue.get('transition', 'dissolve')
    result = ['    if reread:', f'        scene {cue["asset"].lower()}__full with {transition}',
              '    else:', f'        scene {cue["asset"].lower()}__{cue["stage"].lower()} with {transition}']
    if cue.get('pause'):
        result += ['    if not reread:', '        window hide', f'        pause {cue["pause"]}', '        window show']
    return result


def main():
    scenario = json.loads((SOURCE / 'scenario.json').read_text(encoding='utf-8'))
    targets = {key: node for key, node in scenario['nodes'].items() if 'visual_cues' in node}
    maps = {}
    for path in sorted(GAME.glob('story_*.rpy')):
        before = path.read_text(encoding='utf-8')
        old = paragraphs(before)
        chunks = re.split(r'(?=^label node_)', before, flags=re.M)
        for i, chunk in enumerate(chunks):
            if not chunk.startswith('label node_'):
                continue
            node = chunk.splitlines()[0][11:-1]
            if node not in targets:
                continue
            # Remove only standard generated scene blocks, including reveal pause.
            chunk = re.sub(r'    if reread:\n        scene [^\n]+\n    else:\n        scene [^\n]+\n(?:    if not reread:\n        window hide\n        pause [^\n]+\n        window show\n)?', '', chunk)
            cues = targets[node]['visual_cues']
            assert len({c['before_line'] for c in cues}) == len(cues)
            output, number = [], 0
            for line in chunk.splitlines(keepends=True):
                if line.startswith('    "') and line.rstrip().endswith('"') or line.startswith('    call adv_split_'):
                    number += 1
                    for cue in cues:
                        if cue['before_line'] == number:
                            assert targets[node]['lines'][number - 1].startswith(cue['match'])
                            output.append('\n'.join(image_block(cue)) + '\n')
                output.append(line)
            assert number == len(targets[node]['lines'])
            chunks[i] = ''.join(output)
        after = ''.join(chunks)
        new = paragraphs(after)
        assert old.keys() == new.keys()
        assert all(old[k][1] == new[k][1] for k in old), path
        maps[path.name] = {old[k][0]: new[k][0] for k in old}
        write(path, after)

    # Remap all ADV original paragraph references (including unchanged files).
    path = GAME / 'adv_passages.rpy'
    text = path.read_text(encoding='utf-8')
    text = re.sub(r"(\(\d+, '(story_[^']+)', )(\d+)(, \d+\),)",
                  lambda m: m[1] + str(maps[m[2]][int(m[3])]) + m[4], text)
    write(path, text)
    # All keyed one-shot, stop and ambience references must stay on same paragraph.
    path = GAME / 'audio_cues.rpy'
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(\("(story_[^"]+)", )(\d+)',
                  lambda m: m[1] + str(maps[m[2]][int(m[3])]), text)
    write(path, text)

    # Emit authoritative target-node metadata into the shared cue table.
    path = SOURCE / '画像と演出/Muse_本文キュー.tsv'
    reader = csv.DictReader(io.StringIO(path.read_text(encoding='utf-8')), delimiter='\t')
    fields, rows = reader.fieldnames, list(reader)
    output, done = [], set()
    for row in rows:
        node = row[fields[0]]
        if node not in targets:
            output.append(row)
        elif node not in done:
            done.add(node)
            for c in targets[node]['visual_cues']:
                values = [node, str(c['before_line']), c['match'], c['asset'], c['stage'],
                          c['asset'] + '__' + c['stage'] + '.png', c['asset'] + '__FULL.png', c.get('note', '')]
                output.append(dict(zip(fields, values)))
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fields, delimiter='\t', lineterminator='\n')
    writer.writeheader(); writer.writerows(output)
    write(path, stream.getvalue())

    # Expected dialogue locations and text digests change when their keys move.
    adv = {}
    label = None
    for line in (GAME / 'adv_passages.rpy').read_text(encoding='utf-8').splitlines():
        if line.startswith('label '):
            label = line[6:-1]; adv[label] = []
        elif label and line.startswith('    "'):
            adv[label].append(ast.literal_eval(line.strip()))
    text_at = {}
    locations = {}
    for path in GAME.glob('story_*.rpy'):
        for (node, idx), (line, statement) in paragraphs(path.read_text(encoding='utf-8')).items():
            key = path.name + ':' + str(line)
            text_at[key] = ''.join(adv[statement.split()[1]]) if statement.startswith('    call ') else ast.literal_eval(statement.strip())
            locations[(node, idx)] = key
    path = QA / 'qa_story_all.rpy'
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith('    $ qa_check('):
            call = ast.parse(line.strip()[2:]).body[0].value
            args = [ast.literal_eval(x) for x in call.args]
            args[3] = [[file, maps[file][num]] for file, num in args[3]]
            keys = sorted(file + ':' + str(num) for file, num in args[3])
            args[4] = hashlib.sha256('\n'.join(text_at[k] for k in keys).encode()).hexdigest()
            lines[i] = '    $ qa_check(' + ', '.join(repr(x) for x in args) + ')\n'
    text = re.sub(r'set\(range\(1, \d+\)\)', 'set(range(1, %d))' % (len(output) + 1), ''.join(lines))
    write(path, text)
    expectations = {key: dict(node=node, index=idx, ending=text_at[key] == '―― 終 ――', cues=[])
                    for (node, idx), key in locations.items()}
    for i, row in enumerate(output, 1):
        key = locations[(row[fields[0]], int(row[fields[1]]))]
        expectations[key]['cues'].append(dict(id=i, first=Path(row[fields[5]]).stem.lower(), reread=Path(row[fields[6]]).stem.lower()))
    (QA / 'qa_image_expectations.json').write_text(json.dumps(expectations, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(cues=len(output), paragraphs=len(locations), remapped={f:sum(a != b for a,b in m.items()) for f,m in maps.items() if any(a != b for a,b in m.items())})))


if __name__ == '__main__':
    main()
