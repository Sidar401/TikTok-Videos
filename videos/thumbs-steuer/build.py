#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-steuer – Stil „Dark Glow“ (scripts/thumbs.py).
Aufruf: python3 build.py | python3 build.py tiktok   ·   Export: python3 ../../scripts/thumbs.py export . steuer"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, buendel, chart, muenzen, pill, seite, titel  # noqa: E402

STEIG = [(0, 0.05), (0.16, 0.22), (0.3, 0.16), (0.5, 0.48), (0.66, 0.42), (0.84, 0.75), (1, 0.97)]

V1 = (titel([("Das Finanzamt", "w"), ("schuldet dir", "w"), ("GELD!", "box")], 90, 80, 150)
      + chart(STEIG, 330, 760, 1400, 230, OR, pills=[(0, "0 €"), (6, "+2.500 €")])
      + buendel(1420, 30, 0.9, 4) + buendel(1650, 130, 0.8, 3) + muenzen(1560, 240, 5, 130))

V2 = (f'<div style="position:absolute;left:70px;top:60px;font-weight:900;font-size:600px;line-height:1;color:{OR};text-shadow:0 0 80px {OR}aa, 0 14px 0 #000;z-index:3">7</div>'
      + titel([("legale", "w"), ("Steuertricks", "o"), ("für JEDEN", "box")], 520, 150, 140)
      + buendel(1330, 760, 1.0, 4) + muenzen(1640, 700, 6, 150))

V3 = (titel([("Bis zu 4 Jahre", "w"), ("RÜCKWIRKEND!", "box")], 90, 50, 130)
      + pill(1310, 70, "= über 2.500 €", OR, 64)
      + chart([(0.125, 0.12), (0.375, 0.36), (0.625, 0.6), (0.875, 0.88)], 140, 480, 1640, 380, OR,
              pills=[(0, "+650 €"), (1, "+650 €"), (2, "+650 €"), (3, "+650 €")], achse=["2022", "2023", "2024", "2025"]))

TT = (buendel(150, 170, 1.0, 4) + muenzen(680, 230, 6, 190)
      + titel([("Das Finanzamt", "w"), ("schuldet dir", "w"), ("GELD!", "box")], 0, 640, 118, w=1080, align="center")
      + chart(STEIG, 140, 1270, 800, 300, OR, pills=[(0, "0 €"), (6, "+2.500 €")]))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [V1, V2, V3], tiktok=tiktok)
