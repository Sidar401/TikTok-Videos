#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für anthropic-boersengang – Dark Glow, echte Logos."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, ROT, pill, seite, titel  # noqa: E402


def karte(bild, x, y, w, h, dreh):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:34px;background:#fff;padding:30px 50px;'
            f'box-shadow:0 0 90px #ffffff55;display:flex;align-items:center;justify-content:center;transform:rotate({dreh}deg);z-index:2">'
            f'<img src="assets/{bild}.svg" style="max-width:100%;max-height:100%"/></div>')


TT = (titel([("Größter", "w"), ("BÖRSENGANG", "box"), ("aller Zeiten?", "w")], 0, 210, 108, w=1080, align="center")
      + karte("anthropic", 140, 760, 800, 190, -3) + karte("nasdaq", 560, 990, 380, 120, 4)
      + f'<div style="position:absolute;left:0;top:1170px;width:1080px;text-align:center;font-weight:900;font-size:118px;white-space:nowrap;color:{GRUEN};text-shadow:0 0 60px {GRUEN}aa">1,4 Billionen $</div>'
      + pill(190, 1380, "aber −104 Mrd. Verlust?!", ROT, 58, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
