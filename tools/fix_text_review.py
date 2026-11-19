"""Apply the four manuscript/ADV corrections and rebuild page cue locations.

Run from any directory after regenerating the story and ADV passages.
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SOURCE = ROOT / "kaononaiharu_long_complete"
CORRECTIONS = {
    "出る前丁寧に": "出る前に丁寧に",
    "五月に透花さんが机で写真を見せてくれた":
        "五月に透花が机で写真を見せてくれた",
}


def replace_text(path):
    original = path.read_bytes().decode("utf-8")
    revised = original
    for before, after in CORRECTIONS.items():
        revised = revised.replace(before, after)
    if revised != original:
        path.write_bytes(revised.encode("utf-8"))


def fix_adv():
    path = GAME / "adv_passages.rpy"
    original = path.read_text(encoding="utf-8")
    old_lines = original.splitlines()
    # Recover original story locations before changing any ADV line numbers.
    old_rows = {}
    for line in old_lines:
        if re.match(r"        \(\d+, 'story_", line):
            first, source, number, count = ast.literal_eval(line.strip().rstrip(","))
            old_rows[first] = (source, number)
    labels = {}
    current = None
    for number, line in enumerate(old_lines, 1):
        if line.startswith("label adv_split_"):
            current = line
        if number in old_rows:
            if current is None:
                raise ValueError("ADV location has no label")
            labels[current] = old_rows[number]

    revised = []
    current = None
    for line in old_lines:
        if line.startswith("label adv_split_"):
            current = line
        if line.startswith('    "') and line.endswith('"'):
            text = ast.literal_eval(line.strip())
            # Only a whole spoken page gets this punctuation correction.
            # Narrative such as と聞くと、「お風呂」。 retains its punctuation.
            if re.fullmatch(r"「[^「」]*」。", text):
                text = text[:-1]
                line = "    " + json.dumps(text, ensure_ascii=False)
            if current == "label adv_split_C01S04_6:" and text.startswith("「またありました」"):
                previous = ast.literal_eval(revised.pop().strip())
                line = "    " + json.dumps(previous + text, ensure_ascii=False)
        revised.append(line)

    start = revised.index("    for first, source, original, count in (") + 1
    end = revised.index("    ):", start)
    # Each tuple remains one line, so replacing these rows does not move labels.
    rows = []
    for label, (source, number) in labels.items():
        label_index = revised.index(label)
        page_lines = []
        for index in range(label_index + 1, len(revised)):
            if revised[index] == "    return":
                break
            if revised[index].startswith('    "'):
                page_lines.append(index + 1)
        if page_lines != list(range(page_lines[0], page_lines[0] + len(page_lines))):
            raise ValueError("Noncontiguous ADV pages: " + label)
        rows.append("        " + repr((page_lines[0], source, number, len(page_lines))) + ",")
    if len(rows) != end - start:
        raise ValueError("Location table size changed unexpectedly")
    revised[start:end] = rows
    result = "\n".join(revised) + "\n"
    if result != original:
        path.write_bytes(result.encode("utf-8"))


def main():
    paths = list((SOURCE / "本文").glob("*.md"))
    paths += [SOURCE / "制作/scenario.json"]
    paths += list(SOURCE.glob("*長編全稿.md"))
    paths += list(GAME.glob("story_*.rpy"))
    for path in paths:
        replace_text(path)
    fix_adv()


if __name__ == "__main__":
    main()
