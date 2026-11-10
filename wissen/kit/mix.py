"""Mischt Geräusche nach einer Liste. Aufruf: python3 -I mix.py <cues.json> <out.wav> <dauer>
cues: [{"s":"pop","t":1.2,"v":0.6,"p":0,"from":0,"cut":null}, ...]"""
import json, os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(HERE, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
EIGEN = os.path.join(HERE, "sounds")  # eigene ElevenLabs-Sounds (Rechte bei uns)
SR = 44100
cues, out, dur = json.load(open(sys.argv[1])), sys.argv[2], float(sys.argv[3])
cache = {}
def snd(n):
    if n not in cache:
        f = os.path.join(EIGEN, n + ".mp3")
        f = f if os.path.exists(f) else os.path.join(SFX, n + ".mp3")
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        cache[n] = np.frombuffer(raw, dtype=np.float32).copy()
    return cache[n]
def pitch(a, s):
    if not s: return a
    r = 2 ** (s / 12); return np.interp(np.arange(0, len(a) - 1, r), np.arange(len(a)), a)
buf = np.zeros(int(SR * (dur + 12)))
for c in cues:
    a = snd(c["s"])[int(c.get("from", 0) * SR):]
    if c.get("cut"): a = a[: int(c["cut"] * SR)]
    a = pitch(a, c.get("p", 0))
    i = int(c["t"] * SR); buf[i:i + len(a)] += a * c.get("v", 1.0)
buf = buf[: int(SR * dur)]
f = int(0.3 * SR); buf[-f:] *= np.linspace(1, 0, f)
buf = buf / max(1e-9, np.max(np.abs(buf))) * 0.89
with wave.open(out, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())
print("Ton ok:", len(cues), "Geräusche")
