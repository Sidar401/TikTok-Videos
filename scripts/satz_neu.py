#!/usr/bin/env python3
"""Einzelne Sätze neu einsprechen (spart Credits) und in die fertige Stimme einsetzen.

  python3 scripts/satz_neu.py videos/<name> s4 s7 s10   [--tempo 1.12]

Ablauf: skript.json ist schon korrigiert. Die genannten Sätze werden per ElevenLabs neu erzeugt (stimme.py, nur diese Sätze),
mit gleichem Tempo synchronisiert, auf die Lautstärke der alten Stimme angeglichen und an ihre Stelle in assets/voice.wav gesetzt.
Danach läuft sync.py mit Tempo 1.0 über die neue Gesamtstimme → neue timings.json/Untertitel. Alte Stimme: assets/voice-vorher.wav.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

WURZEL = Path(__file__).resolve().parent.parent
SR = 44100


def lese(p):
    x, sr = sf.read(str(p))
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        raise SystemExit(f"{p}: {sr} Hz statt {SR}")
    return x


def rms(x):
    x = x[np.abs(x) > 0.01]
    return float(np.sqrt(np.mean(x ** 2))) if len(x) else 1e-6


def stuecke(timings, audio):
    S = timings["saetze"]
    out = {}
    for i, s in enumerate(S):
        a = int(s["start"] * SR)
        b = int((S[i + 1]["start"] if i + 1 < len(S) else len(audio) / SR) * SR)
        out[s["id"]] = audio[a:b]
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tempo = float(sys.argv[sys.argv.index("--tempo") + 1]) if "--tempo" in sys.argv else 1.12
    if "--tempo" in sys.argv:
        args.remove(str(tempo)) if str(tempo) in args else None
    v = Path(args[0]).resolve()
    neu_ids = args[1:]
    skript = json.loads((v / "skript.json").read_text())
    alt_t = json.loads((v / "timings.json").read_text())
    alt_wav = v / "assets/voice.wav"
    shutil.copy(alt_wav, v / "assets/voice-vorher.wav")
    alt = lese(alt_wav)

    tmp = v / ".satz-neu"
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "assets").mkdir(parents=True)
    teile = [s for s in skript["saetze"] if s["id"] in neu_ids]
    (tmp / "skript.json").write_text(json.dumps({"titel": "neu", "saetze": teile}, ensure_ascii=False))
    subprocess.run([sys.executable, str(WURZEL / "scripts/stimme.py"), str(tmp)], check=True)
    subprocess.run([sys.executable, str(WURZEL / "scripts/sync.py"), str(tmp), str(tmp / "assets/voice-original.mp3"), "--tempo", str(tempo)], check=True)
    neu = lese(tmp / "assets/voice.wav")
    neu_t = json.loads((tmp / "timings.json").read_text())

    A, N = stuecke(alt_t, alt), stuecke(neu_t, neu)
    faktor = rms(alt) / rms(neu)
    print(f"Lautstärke angleichen: ×{faktor:.2f}")
    kette = []
    for s in skript["saetze"]:
        if s["id"] in N:
            kette.append(np.clip(N[s["id"]] * faktor, -0.99, 0.99))
        else:
            kette.append(A[s["id"]])
    gesamt = np.concatenate(kette)
    sf.write(str(v / "assets/voice-neu.wav"), gesamt, SR)
    subprocess.run([sys.executable, str(WURZEL / "scripts/sync.py"), str(v), str(v / "assets/voice-neu.wav"), "--tempo", "1.0"], check=True)
    shutil.rmtree(tmp)
    print("fertig:", len(neu_ids), "Sätze ersetzt")


if __name__ == "__main__":
    main()
