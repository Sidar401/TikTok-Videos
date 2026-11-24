#!/usr/bin/env python3
"""Erster Satz LAUTER (Nutzer 24.11., Vorbild Novaro „Stern frisst Stern“: der Einstieg startet mit mehr Schwung/Lautstärke).
  python3 scripts/lauter_start.py videos/<name> [--db 4.5]
Nach sync.py und VOR logo_sting.einfuegen aufrufen (Merker in timings.json, mehrfach sicher).
Hebt voice.wav von 0 bis Ende Satz 1 um --db an (weicher Begrenzer, kein Übersteuern), 80 ms Übergang am Ende."""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

here = Path(sys.argv[1])
db = float(sys.argv[sys.argv.index("--db") + 1]) if "--db" in sys.argv else 4.5
tp = here / "timings.json"
T = json.loads(tp.read_text())
if T.get("lauter_start"):
    print("schon angewendet"); sys.exit(0)
a, sr = sf.read(str(here / "assets/voice.wav"))
n = int(T["saetze"][0]["end"] * sr)
g = 10 ** (db / 20)
x = a[:n] * g
x = np.tanh(x / 0.95) * 0.95 if np.abs(x).max() > 0.95 else x  # weicher Begrenzer
ramp = int(0.08 * sr)
w = np.ones(n); w[-ramp:] = np.linspace(1, 0, ramp)
mix = a[:n] * (1 - w.reshape((-1,) + (1,) * (a.ndim - 1))) + x * w.reshape((-1,) + (1,) * (a.ndim - 1))
a[:n] = mix
sf.write(str(here / "assets/voice.wav"), a, sr)
T["lauter_start"] = db
tp.write_text(json.dumps(T, ensure_ascii=False, indent=1))
rest = a[n:n + 5 * sr]
print(f"Satz 1 +{db} dB: RMS vorher {np.sqrt((a[:n]/g)**2).mean():.4f} → {np.sqrt((a[:n])**2).mean():.4f}; Rest {np.sqrt((rest)**2).mean():.4f}")
