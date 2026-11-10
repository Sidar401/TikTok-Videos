#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für longform-inflation-ezb – Dark Glow, echtes EZB-Logo."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

LOGO = ('<div style="position:absolute;left:240px;top:1180px;width:600px;height:260px;border-radius:36px;background:#fff;'
        'box-shadow:0 0 80px #ffffff55;display:flex;align-items:center;justify-content:center;z-index:2">'
        '<img src="assets/ezb.svg" style="max-width:520px;max-height:200px"/></div>')
TT = (titel([("Inflation", "w"), ("wieder hoch!", "w")], 0, 230, 120, w=1080, align="center")
      + f'<div style="position:absolute;left:0;top:560px;width:1080px;text-align:center;font-weight:900;font-size:300px;color:{ROT};text-shadow:0 0 70px {ROT}aa;z-index:2">4 %</div>'
      + titel([("Zinsen RAUF?", "box")], 0, 920, 120, w=1080, align="center")
      + LOGO + pill(250, 1540, "Was heißt das für dich?", OR, 50, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
