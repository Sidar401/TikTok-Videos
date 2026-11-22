#!/usr/bin/env python3
"""3 Demo-Videos (10 s, ohne Stimme) für die neuen animierten CTAs. Aufruf: python3 scripts/cta_demo.py"""
import sys
from pathlib import Path
W = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(W / "scripts"))
import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402

D, O, R = nl.DUNKEL, nl.ORANGE, nl.R
INHALT = (f'<div class="nk-karte" style="left:110px;top:330px;width:860px;text-align:center;opacity:.9"><div class="nk-kt">Glühwein 2026</div>'
          f'<div style="font-weight:900;font-size:120px;color:{R}">5 €</div><div style="font-size:40px;color:#3a414c">pro Tasse</div></div>')
for nr, (html, js) in enumerate([
        (nl.cta_kommentar("ck", "Bei uns 4,50 € 🍷", "Bei uns 4,50 € 🍷", 760), "kommentar"),
        (nl.cta_folgen("cf", 640), "folgen"),
        (nl.cta_teilen("ct", "mit deinem Glühwein-Buddy", 900), "teilen")], 1):
    sfx = []
    code = {"kommentar": lambda a, d: nl.cta_kommentar_js("ck", 1.0, 17, 1.6, sfx),
            "folgen": lambda a, d: nl.cta_folgen_js("cf", 1.0, sfx),
            "teilen": lambda a, d: nl.cta_teilen_js("ct", 1.0, sfx)}[js]
    code(0, 10)  # füllt sfx einmal
    js_text = code(0, 10)
    sfx = sfx[:len(sfx) // 2]
    code = lambda a, d, j=js_text: j
    here = W / f"videos/cta-demo-{nr}"
    szenen = [(0.0, 10.0, nl.CSS + INHALT + html, code, 1), (0.0, 10.0, nl.kopf("NEWS", "22.11.2026"), lambda a, d: "", 8)]
    gs.build(here, szenen, sfx, dauer=10.0, drift=False)
    nl.hell(here)
    print(here.name, sfx)
