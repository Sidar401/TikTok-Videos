#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-lotto – Stil „Dark Glow“ (scripts/thumbs.py).
Aufruf: python3 build.py | python3 build.py tiktok   ·   Export: python3 ../../scripts/thumbs.py export . lotto"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, buendel, chart, kugel, muenzen, pill, seite, titel  # noqa: E402

BLAU, LILA, GOLD = "#3d7be0", "#9b59b6", "#e0a800"
FALL = [(0, 0.95), (0.18, 0.78), (0.32, 0.84), (0.52, 0.5), (0.68, 0.56), (0.84, 0.22), (1, 0.04)]

V1 = (titel([("1 MILLION", "w"), ("gewonnen …", "o"), ("… und PLEITE!", "box")], 90, 80, 150)
      + chart(FALL, 330, 760, 1400, 230, ROT, pills=[(0, "1 Mio. €"), (6, "0 €")])
      + kugel(1440, 60, 7, ROT, 200) + kugel(1660, 150, 42, BLAU, 170) + kugel(1230, 130, 21, "#e08a00", 140))

V2 = (titel([("In 4 Jahren", "w"), ("ALLES", "w"), ("WEG?!", "box")], 90, 170, 140)
      + f'''<div style="position:absolute;left:1060px;top:200px;width:780px;padding:50px 56px;border-radius:44px;background:#16191b;border:4px solid {OR};
             box-shadow:0 0 80px {OR}66, 0 30px 60px #000;z-index:2">
          <div style="font-weight:800;font-size:44px;color:#9aa3a8;letter-spacing:3px">KONTOSTAND</div>
          <div style="font-weight:900;font-size:100px;color:#ffffff88;white-space:nowrap;text-decoration:line-through;text-decoration-color:{ROT};text-decoration-thickness:14px">1.000.000 €</div>
          <div style="font-weight:900;font-size:230px;line-height:1;color:{ROT};text-shadow:0 0 50px {ROT}aa">0 €</div></div>'''
      + muenzen(1150, 790, 5, 150) + buendel(1380, 800, 0.9, 3))

V3 = (titel([("Warum Lottogewinner", "w"), ("PLEITE gehen", "box")], 90, 50, 130)
      + chart([(0.1, 0.8), (0.3, 0.42), (0.5, 0.36), (0.7, 0.15), (0.9, 0.02)], 140, 500, 1640, 380, ROT,
              pills=[(0, "1.000.000 €"), (1, "200.000 €"), (4, "0 €")], achse=["Gewinn", "Jahr 1", "Jahr 2", "Jahr 3", "Jahr 4"]))

TT = (kugel(170, 300, 7, ROT, 200) + kugel(440, 250, 42, BLAU, 200) + kugel(710, 300, 21, "#e08a00", 200)
      + titel([("1 MILLION", "w"), ("gewonnen …", "o"), ("… und PLEITE!", "box")], 0, 600, 125, w=1080, align="center")
      + chart(FALL, 140, 1240, 800, 330, ROT, pills=[(0, "1 Mio. €"), (6, "0 €")]))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [V1, V2, V3], tiktok=tiktok)
