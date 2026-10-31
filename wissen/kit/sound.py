"""Neuer Sound: Beat (scripts/musik.py) mit Breakdown vor jedem Drop + Effekte obendrauf.
Aufruf: python3 wissen/kit/sound.py <cues.json> <out.wav> <dauer> --drops 18.5,25.0 [--musik 0.55]"""
import argparse, json, os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from musik import beat  # noqa: E402
SFX = os.path.join(HERE, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
SR = 44100
ap = argparse.ArgumentParser()
ap.add_argument("cues"); ap.add_argument("out"); ap.add_argument("dauer", type=float)
ap.add_argument("--drops", default=""); ap.add_argument("--musik", type=float, default=0.55)
ap.add_argument("--sfx", type=float, default=0.75); ap.add_argument("--bpm", type=int, default=124)
a = ap.parse_args()
drops = [float(x) for x in a.drops.split(",") if x]
pausen = [(max(0.0, d - 1.9), d) for d in drops if d >= 2.0]
m = beat(a.dauer, bpm=a.bpm, pausen=pausen)[: int(SR * a.dauer)]
cache = {}
def snd(n):
    if n not in cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX, n + ".mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        cache[n] = np.frombuffer(raw, dtype=np.float32).copy()
    return cache[n]
def pitch(x, s):
    if not s: return x
    r = 2 ** (s / 12); return np.interp(np.arange(0, len(x) - 1, r), np.arange(len(x)), x)
fx = np.zeros(int(SR * (a.dauer + 12)))
for c in json.load(open(a.cues)):
    x = snd(c["s"])[int(c.get("from", 0) * SR):]
    if c.get("cut"): x = x[: int(c["cut"] * SR)]
    x = pitch(x, c.get("p", 0)); i = int(c["t"] * SR); fx[i:i + len(x)] += x * c.get("v", 1.0)
fx = fx[: len(m)]
fx = fx / (np.abs(fx).max() + 1e-9)
mix = a.musik * m + a.sfx * fx
f = int(0.4 * SR); mix[-f:] *= np.linspace(1, 0, f)
mix = np.tanh(mix * 1.3) / np.tanh(1.3)          # sanft lauter machen ohne Übersteuern
mix = mix / (np.abs(mix).max() + 1e-9) * 0.89
with wave.open(a.out, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("Sound ok · Drops:", drops)
