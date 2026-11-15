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
W, H = (1920, 1080) if c.get("format") == "16:9" else (1080, 1920)
LAND = "html, body, #root { width: 1920px !important; height: 1080px !important; } .line { width: 1920px !important; } .tag { top: 48px !important; } .capw { top: 900px !important; font-size: 66px !important; } .hookbig { top: 300px !important; } .share { top: 560px !important; } .follow { top: 520px !important; } #word { top: 650px !important; font-size: 78px !important; } .hookdim { width: 1920px !important; height: 1080px !important; }"
if W > H: c["css"] = LAND + " " + c.get("css_land", "")
rep = {"{{W}}": str(W), "{{H}}": str(H), "{{RES}}": "landscape" if W > H else "portrait", "{{DUR}}": str(total), "{{TAG}}": c["tag"], "{{CSS}}": c.get("css", ""), "{{SCENE}}": scene}
voice = (proj / "words.json").exists()
if voice:
    w = json.load(open(proj / "words.json"))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice.wav")], capture_output=True, text=True).stdout)
    rep.update({"{{SHARE_TEXT}}": c.get("share_text", "+ Folgen"), "{{FOLLOW_TEXT}}": c.get("follow_text", "Folg uns für mehr! 👆"), "{{FOLLOW_PILL}}": c.get("follow_pill", "+ Folgen"), "{{HOOK}}": c["hook"], "{{HOOK_END}}": str(c["hook_end"]), "{{CAP_DUR}}": f"{total - c['hook_end']:.2f}", "{{SHARE_START}}": str(c["share"][0]), "{{SHARE_DUR}}": str(c["share"][1]),
                "{{FOLLOW}}": str(c["follow"]), "{{FOLLOW_DUR}}": f"{total - c['follow']:.2f}", "{{VOICE_DUR}}": f"{dur:.2f}", "{{WORDS}}": json.dumps(w["words"], ensure_ascii=False),
                "{{CHUNKS}}": json.dumps(w["chunks"]), "{{FIX}}": json.dumps(c.get("fix", {}), ensure_ascii=False)})
h = (kit / ("sauber_stimme_vorlage.html" if voice else "sauber_vorlage.html")).read_text()
for k, v in rep.items(): h = h.replace(k, v)
(proj / "index.html").write_text(h); print("index.html gebaut ·", proj.name, "· mit Stimme" if voice else "· ohne Stimme")
