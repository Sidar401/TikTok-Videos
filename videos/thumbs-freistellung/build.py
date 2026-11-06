#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für freistellungsauftrag – Dark Glow. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, muenzen, pill, seite, titel  # noqa: E402

TT = (titel([("Deine Bank", "w"), ("zieht dir", "w"), ("STEUERN AB", "box")], 0, 220, 120, w=1080, align="center")
      + muenzen(150, 860, 6, 210) + muenzen(430, 800, 8, 230) + muenzen(730, 880, 5, 200)
      + pill(620, 760, "−26 %", "#ff4d4d", 96, 8)
      + f'<div style="position:absolute;left:0;top:1290px;width:1080px;text-align:center;font-weight:900;font-size:190px;color:{GRUEN};text-shadow:0 0 60px {GRUEN}aa">1.000 €</div>'
      + '<div style="position:absolute;left:0;top:1520px;width:1080px;text-align:center;font-weight:900;font-size:62px;color:#fff">wären steuerfrei!</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
