#!/usr/bin/env python3
"""Zeitplan aus der Sprachaufnahme: Szenen an Satz-Zeilen koppeln, Pause fürs Logo-Intro in die Stimme schneiden.
Aufruf (aus Python): plan(name, szenen_zeilen=[0,1,2,...], intro_nach=3, kommentar_zeile=2, schluss_zeile=12, teil="TEIL 1 VON 3", teilen_zeile=None)
Schreibt videos/<name>/assets/voice.wav + Eintrag in hundewissen/plaene.json."""
import json, subprocess
from pathlib import Path
import numpy as np, soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
INTRO = 3.0


def plan(name, szenen_zeilen, intro_nach=None, kommentar_zeile=None, schluss_zeile=None, teil=None, teilen_zeile=None):
    d = ROOT / "videos" / name
    Z = json.loads((d / "zeilen.json").read_text())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "assets/voice-orig.mp3"), "-ac", "1", "-ar", "44100", str(d / "assets/voice-roh.wav")], check=True)
    y, sr = sf.read(str(d / "assets/voice-roh.wav"))
    t_ins = None
    if intro_nach is not None:
        t_ins = round((Z[intro_nach][1] + Z[intro_nach + 1][0]) / 2, 2)
        i = int(t_ins * sr); y = np.concatenate([y[:i], np.zeros(int(INTRO * sr)), y[i:]])
    sf.write(str(d / "assets/voice.wav"), y, sr)
    sh = lambda t: round(t + (INTRO if t_ins is not None and t >= t_ins else 0), 2)
    starts = [0.0 if k == 0 else sh(Z[z][0]) - 0.15 for k, z in enumerate(szenen_zeilen)]
    ende_sprache = sh(Z[-1][1])
    schluss = sh(Z[schluss_zeile][0]) - 0.1 if schluss_zeile is not None else ende_sprache + 0.3
    grenzen = starts[1:] + [schluss]
    zeiten = []
    for a, b in zip(starts, grenzen):
        if t_ins is not None and a < t_ins < b: b = t_ins  # Szene vor dem Intro endet am Intro
        zeiten.append((round(a, 2), round(b, 2)))
    dur = round(max(ende_sprache + 1.2, schluss + 3.2), 2)
    p = dict(zeiten=zeiten, t_intro=t_ins, schluss=round(schluss, 2), dur=dur)
    if kommentar_zeile is not None: p["ka"] = round(sh(Z[kommentar_zeile][0]) - 0.1, 2)
    if teilen_zeile is not None: p["teilen"] = round(sh(Z[teilen_zeile][0]), 2)
    if teil: p["teil"] = teil
    pf = ROOT / "hundewissen/plaene.json"
    alle = json.loads(pf.read_text()) if pf.exists() else {}
    alle[name] = p; pf.write_text(json.dumps(alle, indent=1, ensure_ascii=False))
    return p
