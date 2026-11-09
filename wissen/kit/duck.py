#!/usr/bin/env python3
"""Effekte leiser machen, solange gesprochen wird (Ducking).
Aufruf: python3 -I wissen/kit/duck.py videos/<name>   (nach mix.py)
liest assets/sfx.wav + assets/voice.wav, überschreibt assets/sfx.wav."""
import sys, wave, numpy as np
from pathlib import Path
p = Path(sys.argv[1]) / "assets"
def rd(f):
    w = wave.open(str(f)); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    return x, sr
s, sr = rd(p / "sfx.wav"); v, vsr = rd(p / "voice.wav")
if vsr != sr: v = np.interp(np.arange(0, len(v), vsr / sr), np.arange(len(v)), v)
v = np.pad(v, (0, max(0, len(s) - len(v))))[: len(s)]
win = int(sr * 0.05); env = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, "same"))
talk = (env > 0.01).astype(float)
k = int(sr * 0.15); talk = np.convolve(talk, np.ones(k) / k, "same").clip(0, 1)  # weiche Übergänge
gain = 1 - 0.75 * talk  # beim Sprechen nur noch 25 %
s = s * gain
with wave.open(str(p / "sfx.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((s.clip(-1, 1) * 32767).astype(np.int16).tobytes())
print("Ducking ok")
