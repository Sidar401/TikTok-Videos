#!/usr/bin/env python3
"""Cover 9:16 für longform-klarna."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, pill, seite, titel  # noqa: E402

ROT = "#ff4d4d"


def rechnung(x, y, b, f, rot, z):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:380px;padding:26px 30px;border-radius:24px;background:#f4f1ea;transform:rotate({rot}deg);'
            f'border-top:20px solid {f};box-shadow:0 24px 50px #000c, 0 0 50px {f}55;z-index:{z}"><div style="font-weight:800;font-size:32px;color:#555">später zahlen</div>'
            f'<div style="font-weight:900;font-size:80px;color:#111">{b}</div></div>')


TT = (titel([("Jetzt kaufen,", "w"), ("später ZAHLEN", "box")], 0, 200, 110, w=1080, align="center")
      + rechnung(120, 640, "49 €", OR, -8, 2) + rechnung(520, 700, "89 €", "#ffb3c7", 6, 3) + rechnung(300, 900, "120 €", "#4d8ff0", -3, 4)
      + pill(170, 1320, "Die Klarna-Falle", ROT, 84, -4)
      + '<div style="position:absolute;left:0;top:1540px;width:1080px;text-align:center;font-weight:900;font-size:62px;color:#fff">+ neue Regeln ab 20.11.</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
