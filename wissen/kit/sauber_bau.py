#!/usr/bin/env python3
"""Sauberer Look (freigegeben 14.11.). Baut videos/<name>/index.html.
Ohne words.json: sauber_vorlage.html (Demo ohne Stimme).
Mit words.json: sauber_stimme_vorlage.html (Stimme, Untertitel, Hook, "+ Folgen", Folg-Box).
szene.json: {"tag": "...", "dauer": 65, "hook": "...", "hook_end": 4.0, "share": [4.3, 3.4], "follow": 61.8, "fix": {}, "css": ""}
In szene.js: renderAt = (t) => {...}; dort am Ende cap(t) aufrufen (nur mit Stimme)."""
import json, subprocess, sys
from pathlib import Path
proj = Path(sys.argv[1]); kit = Path(__file__).resolve().parent
c = json.load(open(proj / "szene.json")); total = c["dauer"]
scene = "\n".join("        " + l for l in (proj / "szene.js").read_text().splitlines())
rep = {"{{DUR}}": str(total), "{{TAG}}": c["tag"], "{{CSS}}": c.get("css", ""), "{{SCENE}}": scene}
voice = (proj / "words.json").exists()
if voice:
    w = json.load(open(proj / "words.json"))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice.wav")], capture_output=True, text=True).stdout)
    rep.update({"{{HOOK}}": c["hook"], "{{HOOK_END}}": str(c["hook_end"]), "{{CAP_DUR}}": f"{total - c['hook_end']:.2f}", "{{SHARE_START}}": str(c["share"][0]), "{{SHARE_DUR}}": str(c["share"][1]),
                "{{FOLLOW}}": str(c["follow"]), "{{FOLLOW_DUR}}": f"{total - c['follow']:.2f}", "{{VOICE_DUR}}": f"{dur:.2f}", "{{WORDS}}": json.dumps(w["words"], ensure_ascii=False),
                "{{CHUNKS}}": json.dumps(w["chunks"]), "{{FIX}}": json.dumps(c.get("fix", {}), ensure_ascii=False)})
h = (kit / ("sauber_stimme_vorlage.html" if voice else "sauber_vorlage.html")).read_text()
for k, v in rep.items(): h = h.replace(k, v)
(proj / "index.html").write_text(h); print("index.html gebaut ·", proj.name, "· mit Stimme" if voice else "· ohne Stimme")
