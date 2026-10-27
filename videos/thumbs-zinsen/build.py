#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für million-zinsen – Dark Glow. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, buendel, muenzen, seite, titel  # noqa: E402

TT = (titel([("1 Million Euro", "w"), ("bringt dir", "w"), ("PRO TAG …", "box")], 0, 220, 116, w=1080, align="center")
      + muenzen(120, 820, 7, 200) + buendel(380, 860, 1.2, 6) + muenzen(780, 840, 6, 180)
      + f'<div style="position:absolute;left:0;top:1260px;width:1080px;text-align:center;font-weight:900;font-size:210px;color:{GRUEN};text-shadow:0 0 60px {GRUEN}aa">55 €</div>'
      + f'<div style="position:absolute;left:0;top:1500px;width:1080px;text-align:center;font-weight:900;font-size:62px;color:#fff">ohne zu arbeiten</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
