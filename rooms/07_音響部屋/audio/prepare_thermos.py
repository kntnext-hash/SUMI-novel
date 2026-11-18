"""REVIEW normal set-down cue. Retain full preview; do not invent a quiet take."""
import sys, json, hashlib
from pathlib import Path
root = Path(__file__).parent
sys.path.insert(0, str(root / '.qc_deps'))
import soundfile as sf
import numpy as np
source = root / 'thermos_792930_preview.mp3'
page = root / 'thermos_792930_source.html'
assert 'creativecommons.org/publicdomain/zero/1.0/' in page.read_text(encoding='utf-8')
data, rate = sf.read(source, always_2d=True)
peak = float(np.max(np.abs(data)))
gain = min(1.0, .5 / peak) if peak else 1.0
output = root / 'delivery/thermos_set_down.wav'
sf.write(output, data*gain, rate, subtype='PCM_16')
decoded, actual_rate = sf.read(output, always_2d=True)
record = dict(file=output.name, status='REVIEW', listening='PENDING_USER',
    author='qubodup', title='Put down item',
    source='https://freesound.org/people/qubodup/sounds/792930/',
    download='https://cdn.freesound.org/previews/792/792930_71257-hq.mp3',
    license='https://creativecommons.org/publicdomain/zero/1.0/',
    license_note='Individual sound page explicitly CC0. Description also links generic CC BY profile guidance; preserve both facts. Voluntary attribution below.',
    attribution='Put down item by qubodup (Freesound #792930), CC0 1.0. Public MP3 preview converted to PCM16 WAV; uniform attenuation if needed.',
    date='2026-11-19', group='S13', manuscript='C06S03 line 95: normal set-down on opposite desk only',
    source_description='Thermos flask half-full of warm tea, put down on wooden table; Shure SM7B / Triton FetHead / Steinberg UR22C / Audacity',
    fit_limitations='Flask base material unspecified. Recording description supports action and table; acoustic fit unlistened. No near-silent take delivered.',
    origin='Lossy public HQ MP3 preview, not original master WAV',
    processing='Full decoded preview, no cuts/fades or invented impacts; peak cap .5; PCM16',
    input_file=source.name, input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    source_page_sha256=hashlib.sha256(page.read_bytes()).hexdigest(),
    sha256=hashlib.sha256(output.read_bytes()).hexdigest(), gain=gain,
    seconds=len(decoded)/actual_rate, sample_rate=actual_rate, channels=decoded.shape[1],
    peak=float(np.max(np.abs(decoded))),
    clipped_samples=int(np.sum((decoded >= 32767/32768) | (decoded <= -1))))
assert record['clipped_samples'] == 0
(root / 'delivery/thermos_rights_qc.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(json.dumps(record, indent=2))
