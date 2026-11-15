#!/usr/bin/env python3
"""Lange Texte (Longform): Stimme in Teilen erzeugen und zusammenfügen.
Aufruf: python3 wissen/kit/lang_stimme.py videos/<name> [zeilen_pro_teil=6]
Schreibt wie stimme.py: assets/voice-orig.mp3, alignment.json, kontrolle.json (alle Teile)."""
import json, subprocess, sys, tempfile, time
from pathlib import Path
proj = Path(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
kit = Path(__file__).resolve().parent; GAP = 0.45
lines = [l.strip() for l in (proj / "sprechtext.txt").read_text().splitlines() if l.strip()]
parts = [lines[i:i + n] for i in range(0, len(lines), n)]
tmp = Path(tempfile.mkdtemp(prefix="lang_")); allc, alls, alle, wavs, texts, kontr = [], [], [], [], [], []; off = 0.0
for k, p in enumerate(parts):
    d = tmp / f"t{k}"; d.mkdir(); (d / "s.txt").write_text("\n".join(p))
    for v in range(4):
        r = subprocess.run([sys.executable, str(kit / "stimme.py"), str(d), str(d / "s.txt")], capture_output=True, text=True)
        if r.returncode == 0: break
        print("Teil", k + 1, "Versuch", v + 1, "fehlgeschlagen:", r.stderr.strip().splitlines()[-1][:120]); time.sleep(15)
    else: sys.exit("Abbruch")
    a = json.load(open(d / "alignment.json")); al = a["alignment"]; kontr.append(json.load(open(d / "kontrolle.json")))
    w = d / "v.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(d / "assets/voice-orig.mp3"), "-ar", "44100", "-ac", "1", str(w)], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(w)], capture_output=True, text=True).stdout)
    if k: allc.append("\n"); alls.append(off - GAP); alle.append(off)
    allc += al["characters"]; alls += [t + off for t in al["character_start_times_seconds"]]; alle += [t + off for t in al["character_end_times_seconds"]]
    texts.append(a["text"]); wavs.append(w); off += dur + GAP
    print(f"Teil {k + 1}/{len(parts)} ok · {dur:.1f} s · Abweichungen: {kontr[-1]['abweichungen']}")
sil = tmp / "sil.wav"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(GAP), str(sil)], check=True)
lst = tmp / "l.txt"; lst.write_text("".join(f"file '{w}'\nfile '{sil}'\n" for w in wavs))
(proj / "assets").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-b:a", "192k", str(proj / "assets/voice-orig.mp3")], check=True)
json.dump({"text": "\n".join(texts), "alignment": {"characters": allc, "character_start_times_seconds": alls, "character_end_times_seconds": alle}}, open(proj / "alignment.json", "w"), ensure_ascii=False)
json.dump({"teile": kontr}, open(proj / "kontrolle.json", "w"), ensure_ascii=False, indent=1)
print(f"Fertig: {off:.1f} s gesamt")
