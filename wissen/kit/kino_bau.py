#!/usr/bin/env python3
"""Baut videos/<name>/index.html aus wissen/kit/kino_vorlage.html.
Aufruf: python3 wissen/kit/kino_bau.py videos/<name>
liest:  szene.json  {"tag": "10. NOVEMBER 2026", "hook": "...html...", "hook_end": 2.9, "share": [3.5, 2.6],
                     "follow": 26.8, "fix": {"vierundzwanzigsten": "24."}, "css": ""}
        szene.js    (Inhalt der Szene: baut die Welt und setzt renderAt = (t) => {...})
        words.json  (von schnitt.py), assets/voice.wav
"""
import json, subprocess, sys
from pathlib import Path

proj = Path(sys.argv[1]); kit = Path(__file__).resolve().parent
c = json.load(open(proj / "szene.json")); w = json.load(open(proj / "words.json"))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice.wav")], capture_output=True, text=True).stdout)
scene = "\n".join("        " + l for l in (proj / "szene.js").read_text().splitlines())
total = c.get("dauer", 30)
rep = {"{{DUR}}": str(total), "{{TAG}}": c["tag"], "{{HOOK}}": c["hook"], "{{HOOK_END}}": str(c["hook_end"]), "{{CAP_DUR}}": f"{total - c['hook_end']:.2f}",
       "{{SHARE_START}}": str(c["share"][0]), "{{SHARE_DUR}}": str(c["share"][1]), "{{FOLLOW}}": str(c["follow"]), "{{FOLLOW_DUR}}": f"{total - c['follow']:.2f}",
       "{{VOICE_DUR}}": f"{dur:.2f}", "{{WORDS}}": json.dumps(w["words"], ensure_ascii=False), "{{CHUNKS}}": json.dumps(w["chunks"]),
       "{{FIX}}": json.dumps(c.get("fix", {}), ensure_ascii=False), "{{CSS}}": c.get("css", ""), "{{SCENE}}": scene}
h = (kit / "kino_vorlage.html").read_text()
for k, v in rep.items(): h = h.replace(k, v)
(proj / "index.html").write_text(h)
print("index.html gebaut ·", proj.name, f"· Stimme {dur:.2f} s")
