#!/usr/bin/env python3
"""Neuer sauberer Look (ab 14.11.): baut videos/<name>/index.html aus sauber_vorlage.html + szene.json + szene.js.
szene.json: {"tag": "14. NOVEMBER 2026", "dauer": 15, "css": ""}"""
import json, sys
from pathlib import Path
proj = Path(sys.argv[1]); kit = Path(__file__).resolve().parent
c = json.load(open(proj / "szene.json"))
scene = "\n".join("        " + l for l in (proj / "szene.js").read_text().splitlines())
h = (kit / "sauber_vorlage.html").read_text()
for k, v in {"{{DUR}}": str(c["dauer"]), "{{TAG}}": c["tag"], "{{CSS}}": c.get("css", ""), "{{SCENE}}": scene}.items(): h = h.replace(k, v)
(proj / "index.html").write_text(h); print("index.html gebaut ·", proj.name)
