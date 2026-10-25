#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-freiheit – Stil „Dark Glow“ (scripts/thumbs.py).
Aufruf: python3 build.py | python3 build.py tiktok   ·   Export: python3 ../../scripts/thumbs.py export . freiheit"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, buendel, chart, muenzen, seite, titel  # noqa: E402

STEIG = [(0, 0.05), (0.15, 0.2), (0.3, 0.3), (0.45, 0.26), (0.65, 0.58), (0.8, 0.54), (1, 0.97)]
GIPFEL = [(0.03, 0.05), (0.2, 0.45), (0.3, 0.28), (0.5, 0.66), (0.62, 0.48), (0.84, 0.96), (0.97, 0.75)]

V1 = (titel([("NIE WIEDER", "w"), ("ARBEITEN", "box"), ("ab wie viel €?", "o")], 90, 70, 150)
      + chart(STEIG, 330, 740, 1400, 250, OR, pills=[(2, "450.000 €"), (4, "750.000 €"), (6, "1,2 Mio. €")])
      + buendel(1430, 40, 0.9, 5) + muenzen(1680, 150, 6, 140))

V2 = (titel([("Ausgaben", "w"), ("× 25 =", "o"), ("FREIHEIT", "box")], 90, 110, 165)
      + f'''<div style="position:absolute;left:1060px;top:200px;width:780px;padding:46px 50px;border-radius:44px;background:#16191b;border:4px solid {OR};
             box-shadow:0 0 80px {OR}66, 0 30px 60px #000;z-index:2;display:flex;flex-direction:column;gap:14px">
          <div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:3px">BEISPIEL</div>
          <div style="font-weight:900;font-size:66px;color:#fff;white-space:nowrap">2.500 € / Monat</div>
          <div style="font-weight:800;font-size:56px;color:#9aa3a8">× 12 × 25</div>
          <div style="font-weight:900;font-size:116px;line-height:1;white-space:nowrap;color:{OR};text-shadow:0 0 50px {OR}aa">750.000 €</div></div>'''
      + muenzen(1040, 820, 4, 130) + buendel(1560, 840, 0.75, 3))

V3 = (titel([("Welcher Gipfel", "w"), ("ist DEINER?", "box")], 90, 50, 130)
      + chart(GIPFEL, 100, 440, 1720, 500, OR, pills=[(1, "450.000 €"), (3, "750.000 €"), (5, "1,2 Mio. €")]))

TT = (buendel(160, 170, 1.0, 5) + muenzen(700, 250, 6, 180)
      + titel([("NIE WIEDER", "w"), ("ARBEITEN", "box"), ("ab wie viel €?", "o")], 0, 640, 120, w=1080, align="center")
      + chart(STEIG, 150, 1300, 780, 300, OR, pills=[(2, "450.000 €"), (6, "1,2 Mio. €")]))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [V1, V2, V3], tiktok=tiktok)
