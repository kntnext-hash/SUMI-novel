"""Original 32-bar instrumental; no external recordings or model weights."""
from pathlib import Path
import sys, json, hashlib, shutil
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.qc_deps'))
import numpy as np
import soundfile as sf

RATE = 48000
BEAT = 60 / 64
DURATION = 32 * 3 * BEAT + 8
mix = np.zeros((round(DURATION * RATE), 2), dtype=np.float64)
score = []

def note(beat, midi, beats, velocity, pan, pad=False):
    start = round(beat * BEAT * RATE)
    length = beats * BEAT + (3.5 if not pad else 1.8)
    t = np.arange(round(length * RATE)) / RATE
    f = 440 * 2 ** ((midi - 69) / 12)
    if pad:
        env = np.minimum(t / .8, 1) * np.minimum((length-t)/1.8, 1)
        y = (np.sin(2*np.pi*f*t) + .12*np.sin(2*np.pi*f*2*t)) * env * .26
    else:
        env = (1-np.exp(-t/.009)) * np.exp(-t/1.35) * np.minimum((length-t)/.4, 1)
        y = sum(a*np.sin(2*np.pi*f*k*t)*np.exp(-t*k*.13)
                for k,a in [(1,1),(2,.22),(3,.07),(4,.025)]) * env
    y *= velocity
    gains = np.array([np.cos((pan+1)*np.pi/4), np.sin((pan+1)*np.pi/4)])
    for delay, gain, reverse in [(0,1,False),(.137,.13,True),(.283,.085,False),(.491,.045,True)]:
        begin = start + round(delay*RATE)
        n = min(len(y), len(mix)-begin)
        if n > 0:
            mix[begin:begin+n] += y[:n,None] * (gains[::-1] if reverse else gains) * gain
    score.append(dict(beat=beat,midi=midi,beats=beats,velocity=velocity,pan=pan,instrument='warm_pad' if pad else 'soft_keys'))

# D(add9), Bm7, Gmaj7, A(sus); sparse 3/4, an answering second phrase.
chords = [(50,57,64),(47,54,62),(43,50,59),(45,52,62),
          (50,57,66),(47,54,62),(43,50,61),(45,52,64)]
melodies = [
    [(0,66,1),(1.5,69,1)], [(0,64,2)], [(0,62,1),(2,64,1)], [(0,61,2)],
    [(0,66,1),(1,64,1),(2,62,1)], [(0,59,2)], [(1,62,1),(2,64,1)], [(0,61,2)],
    [(0,66,1),(1.5,69,1)], [(0,71,2)], [(0,69,1),(2,66,1)], [(0,64,2)],
    [(0,62,1),(1.5,64,1)], [(0,66,2)], [(0,64,1),(1.5,61,1)], [(0,62,2.5)],
]
for bar in range(32):
    base = bar*3
    chord = chords[(bar//2)%8]
    # End with an open D chord, leaving room for the return to the title.
    if bar >= 30:
        chord = (50,57,64)
    note(base, chord[0], 2.3, .23, -.25)
    note(base+1, chord[1]+12, 1.2, .105, -.38)
    note(base+2, chord[2], 1.1, .095, .25)
    if bar % 2 == 0 and bar >= 8:
        for pitch in chord:
            note(base, pitch, 5.5, .055, .1, True)
    phrase = melodies[bar%16]
    for offset,pitch,duration in phrase:
        note(base+offset+.025, pitch, duration, .24 if bar<16 else .215, .18)
mix *= np.minimum(np.arange(len(mix))/ (RATE*1.2),1)[:,None]
mix *= np.minimum(np.arange(len(mix))[::-1]/(RATE*5),1)[:,None]
mix *= .36/np.max(np.abs(mix))
delivery = ROOT/'delivery'
delivery.mkdir(exist_ok=True)
wav = delivery/'spring_afterglow_original.wav'
sf.write(wav, mix, RATE, subtype='PCM_16')
game = ROOT.parents[2]/'game'
shutil.copy2(wav, game/'audio/spring_afterglow_original.wav')
decoded, rate = sf.read(game/'audio/spring_afterglow_original.wav')
report = dict(title='春の余白',status='REVIEW',composer='Codex, original symbolic score and additive synthesis',
    third_party_audio=False,ai_assisted=True,hearing_review='NOT_PERFORMED',tempo_bpm=64,meter='3/4',bars=32,
    duration_seconds=DURATION,sample_rate=rate,channels=2,peak_dbfs=float(20*np.log10(np.max(np.abs(decoded)))),
    rms_dbfs=float(20*np.log10(np.sqrt(np.mean(decoded**2)))),clipped_samples=int(np.sum(np.abs(decoded)>=1)),
    first_sample=decoded[0].tolist(),last_sample=decoded[-1].tolist(),
    files={str(p.relative_to(ROOT.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in [wav,game/'audio/spring_afterglow_original.wav']})
(delivery/'spring_afterglow_score.json').write_text(json.dumps(score,indent=2),encoding='utf-8')
(delivery/'spring_afterglow_qc.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
