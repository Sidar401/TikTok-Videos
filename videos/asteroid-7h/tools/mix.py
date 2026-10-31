"""Ton für asteroid-7h -> assets/sfx.wav (30 s)"""
import os, subprocess, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = os.path.join(ROOT, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
SR, DUR = 44100, 30.0
cache = {}
def snd(n):
    if n not in cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX, n), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        cache[n] = np.frombuffer(raw, dtype=np.float32).copy()
    return cache[n]
def pitch(a, s):
    r = 2 ** (s / 12); return np.interp(np.arange(0, len(a) - 1, r), np.arange(len(a)), a)
buf = np.zeros(int(SR * (DUR + 12)))
def put(a, t, v=1.0, cut=None):
    if cut: a = a[: int(cut * SR)]
    i = int(t * SR); buf[i:i + len(a)] += a * v

# Alarm + Countdown
put(snd("error.mp3"), 0.0, 0.8)
put(snd("glitch-2.mp3"), 0.0, 0.25, cut=0.5)
t = 1.0
while t < 7.9:
    put(pitch(snd("click.mp3"), (t - 1) * 1.6), t, 0.55); t += 0.25 - 0.12 * (t - 1) / 7
put(snd("whoosh-cinematic.mp3"), 6.2, 0.6)
put(snd("impact-bass-2.mp3"), 8.0, 0.7)
put(snd("sparkle.mp3"), 9.0, 0.35)
put(snd("pop.mp3"), 9.0, 0.6)
# Was wenn größer?
put(snd("riser.mp3")[int(8.0 * SR):], 10.4, 0.5)
put(snd("whoosh.mp3"), 11.9, 0.7)
# 6 Stufen
for i in range(6):
    s = 12.0 + 2.4 * i
    put(snd("whoosh-short.mp3"), s, 0.55)
    put(snd(["impact-bass-1.mp3", "impact-bass-2.mp3"][i % 2]), s + 1.0, 0.45 + 0.11 * i)
    if i >= 4: put(snd("glitch-1.mp3"), s + 1.02, 0.18 * (i - 3), cut=0.7)
    put(pitch(snd("pop.mp3"), i * 2), s + 1.05, 0.5)
# Schluss
put(snd("whoosh.mp3"), 26.4, 0.5)
put(snd("notification.mp3"), 28.0, 0.5)
buf = buf[: int(SR * DUR)]
f = int(0.3 * SR); buf[-f:] *= np.linspace(1, 0, f)
buf = buf / np.max(np.abs(buf)) * 0.89
with wave.open(os.path.join(ROOT, "assets", "sfx.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())
print("ok")
