#!/usr/bin/env python3
"""TikTok-Cover longform-musk-megadeal – Musk-Foto (gemeinfrei), Tesla + SpaceX → 1 Konzern, 3,5 Billionen $."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, pill, seite, titel  # noqa: E402

FOTO = ('<div style="position:absolute;left:290px;top:560px;width:500px;height:620px;border-radius:36px;overflow:hidden;'
        'box-shadow:0 0 0 8px #DB8622, 0 0 80px #ff8a1f88, 0 40px 60px #000;z-index:2">'
        '<img src="assets/elon-musk.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%"/></div>')
def karte(src, x, y, w, dreh):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:22px;border-radius:26px;background:#fff;'
            f'box-shadow:0 0 50px #ffffff55, 0 30px 40px #000;transform:rotate({dreh}deg);z-index:3"><img src="assets/{src}" style="width:100%;display:block"/></div>')
PLUS = '<div style="position:absolute;left:0;width:1080px;top:1230px;text-align:center;font-weight:900;font-size:120px;color:#fff;text-shadow:0 0 40px #ff8a1f;z-index:4">+</div>'
TT = (titel([("Musk plant den", "w"), ("Mega-Deal", "box")], 0, 220, 120, w=1080, align="center") + FOTO
      + karte("tesla-symbol.png", 80, 1150, 190, -6) + karte("spacex.png", 600, 1200, 400, 5)
      + pill(230, 1460, "= 3,5 Billionen $", GRUEN, 84, -2)
      + pill(250, 1640, "Größter Deal ever?", OR, 60, 2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "40%"))
