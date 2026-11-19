"""Verify and extract a release ZIP to a new QA directory, then inject tests."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile

p = argparse.ArgumentParser()
p.add_argument('zip', type=Path)
p.add_argument('destination', type=Path)
a = p.parse_args()
dest = a.destination.resolve()
if dest.exists():
    raise SystemExit('Destination already exists; use a new directory.')
with zipfile.ZipFile(a.zip) as z:
    for entry in z.infolist():
        target = (dest / entry.filename).resolve()
        if not target.is_relative_to(dest):
            raise SystemExit('Unsafe archive entry: ' + entry.filename)
    bad = z.testzip()
    if bad:
        raise SystemExit('ZIP CRC failure: ' + bad)
    z.extractall(dest)
games = [x for x in dest.rglob('game') if (x / 'script.rpy').is_file()]
if len(games) != 1:
    raise SystemExit('Expected one unpacked game directory: ' + repr(games))
game = games[0]
manifest = {
    'zip': str(a.zip.resolve()),
    'zip_sha256': hashlib.sha256(a.zip.read_bytes()).hexdigest(),
    'crc': 'PASS',
    'game': str(game),
    'files': {str(f.relative_to(game)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in game.rglob('*') if f.is_file()},
}
(dest / 'release_input_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
subprocess.run([sys.executable, str(Path(__file__).with_name('prepare_capture.py')), str(game)], check=True)
print(json.dumps({'basedir': str(game.parent), 'exe': str(game.parent / 'kaononaiharu.exe'),
                  'savedir': str(game.parent / 'qa17_saves')}, ensure_ascii=False))
