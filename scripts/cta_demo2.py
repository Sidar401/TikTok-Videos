#!/usr/bin/env python3
"""3 Demos (10 s, ohne Stimme) im Stil des Nutzer-Vorbilds: dunkles Overlay-Feld unten + Banner. Aufruf: python3 scripts/cta_demo2.py"""
import sys
from pathlib import Path
W = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(W / "scripts"))
import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402

R = nl.R
INHALT = (f'<div class="nk-karte" style="left:110px;top:380px;width:860px;text-align:center"><div class="nk-kt">Glühwein 2026</div>'
          f'<div style="font-weight:900;font-size:150px;color:{R}">5 €</div><div style="font-size:44px;color:#3a414c">pro Tasse</div></div>')
DEMOS = [("Kommentare", "Meine Meinung dazu", "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", ""),
         ("HundeFinanzTv folgen", "@hundefinanztv", "Folgen", "FOLGE UNS", "FÜR MEHR GELD-TIPPS", ""),
         ("Teilen mit …", "Mein Freund, der Glühwein liebt", "Senden", "TEILE DAS", "MIT EINEM FREUND", "")]
for nr, (ti, tx, kn, b1, b2, k2) in enumerate(DEMOS, 1):
    sfx = []
    js = nl.cta_overlay_js("co", 1.0, len(tx), sfx)
    here = W / f"videos/cta-demo-{nr}"
    szenen = [(0.0, 10.0, nl.CSS + INHALT + nl.cta_overlay("co", ti, tx, kn, b1, b2, 1300, k2), lambda a, d, j=js: j, 1),
              (0.0, 10.0, nl.kopf("NEWS", "22.11.2026"), lambda a, d: "", 8)]
    gs.build(here, szenen, sfx, dauer=10.0, drift=False)
    nl.hell(here)
