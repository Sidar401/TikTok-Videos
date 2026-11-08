#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für mindestlohn-netto."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, pill, seite, titel  # noqa: E402

TT = (titel([("Mindestlohn", "w"), ("14,60 €", "box")], 0, 220, 140, w=1080, align="center")
      + '<div style="position:absolute;left:0;top:780px;width:1080px;text-align:center;font-weight:900;font-size:90px;color:#fff">Was bleibt</div>'
      + '<div style="position:absolute;left:0;top:890px;width:1080px;text-align:center;font-weight:900;font-size:110px;color:#fff">WIRKLICH?</div>'
      + f'<div style="position:absolute;left:0;top:1120px;width:1080px;text-align:center;font-weight:900;font-size:220px;color:{GRUEN};text-shadow:0 0 70px {GRUEN}aa">+80 €</div>'
      + pill(330, 1420, "netto im Monat", OR, 64, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
