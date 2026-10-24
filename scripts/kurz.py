#!/usr/bin/env python3
"""Short (9:16) aus einem Longform-Video schneiden – ohne neue Voice.

  python3 scripts/kurz.py videos/longform-lotto videos/short-lotto-1 s1 s14-s15 s35-s47 s22 [--ende 1.5]

Abschnitte = Satz-IDs bzw. Bereiche. Legt im Ziel an:
  assets/ (gsap, Fonts, Beagle) + assets/voice.wav (geschnitten), timings.json (verschoben), skript.json (Teilmenge).
Satz-IDs bleiben erhalten, damit build.py weiter st("s36") usw. nutzen kann.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

LUECKE = 0.2  # Stille zwischen zwei Abschnitten

ap = argparse.ArgumentParser()
ap.add_argument("quelle")
ap.add_argument("ziel")
ap.add_argument("teile", nargs="+")
ap.add_argument("--ende", type=float, default=1.5, help="Stille am Ende für die Endkarte (s)")
a = ap.parse_args()

q, z = Path(a.quelle), Path(a.ziel)
(z / "assets").mkdir(parents=True, exist_ok=True)
for f in (q / "assets").iterdir():
    if f.name.startswith("voice"):
        continue
    (shutil.copytree if f.is_dir() else shutil.copy)(f, z / "assets" / f.name, **({"dirs_exist_ok": True} if f.is_dir() else {}))

T = json.loads((q / "timings.json").read_text())
ids = [s["id"] for s in T["saetze"]]
S = {s["id"]: s for s in T["saetze"]}
SK = {s["id"]: s for s in json.loads((q / "skript.json").read_text())["saetze"]}

neu, sk, cuts, pos = [], [], [], 0.0
for teil in a.teile:
    von, _, bis = teil.partition("-")
    bis = bis or von
    block = ids[ids.index(von): ids.index(bis) + 1]
    t0, t1 = S[block[0]]["start"], S[block[-1]]["end"]
    off = pos - t0
    for i in block:
        s = S[i]
        neu.append({"id": i, "start": round(s["start"] + off, 3), "end": round(s["end"] + off, 3),
                    "captions": [{"text": c["text"], "start": round(c["start"] + off, 3), "end": round(c["end"] + off, 3)} for c in s["captions"]]})
        sk.append(SK[i])
    cuts.append((t0, t1))
    pos += (t1 - t0) + LUECKE
dauer = round(pos - LUECKE + a.ende, 3)

# Audio: Abschnitte ausschneiden, mit Lücken verbinden, Endstille anhängen
filt, labels = [], []
for k, (t0, t1) in enumerate(cuts):
    filt.append(f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={t1 - t0 - 0.03:.3f}:d=0.03,apad=pad_dur={LUECKE}[a{k}]")
    labels.append(f"[a{k}]")
filt.append(f"{''.join(labels)}concat=n={len(cuts)}:v=0:a=1,apad=whole_dur={dauer}[out]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(q / "assets/voice.wav"), "-filter_complex", ";".join(filt),
                "-map", "[out]", "-t", str(dauer), str(z / "assets/voice.wav")], check=True)

(z / "timings.json").write_text(json.dumps({"dauer": dauer, "saetze": neu}, ensure_ascii=False, indent=1))
(z / "skript.json").write_text(json.dumps({"titel": f"Short aus {q.name}", "saetze": sk}, ensure_ascii=False, indent=1))
print(f"{z}: {len(neu)} Sätze, {dauer} s")
