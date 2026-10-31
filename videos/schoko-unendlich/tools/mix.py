"""Mischt Geräusche zu assets/sfx.wav (30 s)."""
import os, subprocess, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = os.path.join(ROOT, "..", "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
SR, DUR = 44100, 30.0
def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(SFX, name), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()
buf = np.zeros(int(SR * (DUR + 12)))
def put(name, t, vol=1.0, start=0.0, length=None):
    a = load(name)[int(start * SR):]
    if length: a = a[: int(length * SR)]
    i = int(t * SR); buf[i:i + len(a)] += a * vol
CUTS, ADD = [0.5, 1.5, 2.4, 3.2], [1, 1, 2, 2]
for j, tc in enumerate(CUTS):
    put(["whoosh-short.mp3", "whoosh.mp3"][j % 2], tc, 0.7)
    for k in range(ADD[j]):
        put("pop.mp3", tc + 0.45 + 0.12 * k + 0.38, 0.8)
put("impact-bass-1.mp3", 5.62, 0.9)
put("impact-bass-2.mp3", 7.02, 0.8)
put("whoosh.mp3", 7.7, 0.7)
put("whoosh-short.mp3", 8.3, 0.6)
for i in range(3): put("click.mp3", 8.8 + i * 0.22, 0.6)
put("whoosh-cinematic.mp3", 9.45, 0.45, length=1.4)
put("impact-bass-1.mp3", 10.52, 0.9)
put("pop.mp3", 11.3, 0.6)
for i in range(9): put(["click.mp3", "click-soft.mp3"][i % 2], 13.0 + i * 1.2 + 0.03, 0.75)
put("riser.mp3", 14.0, 0.35)
put("impact-bass-1.mp3", 24.02, 1.0)
put("impact-bass-2.mp3", 26.62, 1.0)
buf = buf[: int(SR * DUR)]
fade = int(0.4 * SR); buf[-fade:] *= np.linspace(1, 0, fade)
buf = buf / np.max(np.abs(buf)) * 0.89
with wave.open(os.path.join(ROOT, "assets", "sfx.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())
print("ok")
