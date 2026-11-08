#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für aktivrente."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, seite, titel  # noqa: E402

TT = (titel([("Rentner:", "w"), ("2.000 €", "box"), ("im Monat", "w")], 0, 220, 130, w=1080, align="center")
      + f'<div style="position:absolute;left:0;top:930px;width:1080px;display:flex;justify-content:center;z-index:3"><span style="padding:10px 44px;border:14px solid {GRUEN};'
        f'border-radius:30px;color:{GRUEN};font-weight:900;font-size:116px;transform:rotate(-6deg);box-shadow:0 0 70px {GRUEN}88">STEUERFREI</span></div>'
      + '<div style="position:absolute;left:0;top:1340px;width:1080px;text-align:center;font-weight:900;font-size:70px;color:#fff">Kennt fast keiner!</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
