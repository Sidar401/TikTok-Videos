#!/usr/bin/env python3
"""Thumbnails für longform-domino – 16:9 (python3 build.py) und 9:16 (python3 build.py tiktok). Dark Glow, oranger Rahmen."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, pill, seite, titel  # noqa: E402

ROT, BLAU, GRUEN = "#ff4d4d", "#4d8ff0", "#2fd27a"
STEINE = [("WAHL", BLAU), ("KI", OR), ("CHIPS", GRUEN), ("DEPOT", ROT)]


def dominos(x0, y, abst, w=200, h=360, fallen=(55, 30, 12, 0)):
    out = []
    for i, (txt, f) in enumerate(STEINE):
        out.append(f'<div style="position:absolute;left:{x0 + i * abst}px;top:{y}px;width:{w}px;height:{h}px;border-radius:24px;background:#16191b;border:8px solid {f};'
                   f'box-shadow:0 0 60px {f}88;transform-origin:100% 100%;transform:rotate({fallen[i]}deg);z-index:{6 - i};display:flex;align-items:center;justify-content:center;'
                   f'flex-direction:column;gap:{int(h * 0.12)}px"><div style="width:{int(w * 0.22)}px;height:{int(w * 0.22)}px;border-radius:50%;background:#fff"></div>'
                   f'<div style="width:70%;height:6px;background:{f}"></div><div style="width:{int(w * 0.22)}px;height:{int(w * 0.22)}px;border-radius:50%;background:#fff"></div></div>')
    return "".join(out)


YT = (titel([("Diese WAHL", "w"), ("crasht die Börse", "box")], 80, 130, 120)
      + dominos(1000, 330, 210)
      + pill(110, 560, "−2,5 Billionen $", ROT, 96, -4)
      + '<div style="position:absolute;left:110px;top:780px;font-weight:900;font-size:64px;color:#fff">Der Domino-Effekt erklärt</div>')
TT = (titel([("Diese WAHL", "w"), ("crasht die", "w"), ("BÖRSE", "box")], 0, 170, 120, w=1080, align="center")
      + dominos(150, 760, 190, 180, 330)
      + pill(150, 1300, "−2,5 Billionen $", ROT, 92, -4)
      + '<div style="position:absolute;left:0;top:1520px;width:1080px;text-align:center;font-weight:900;font-size:62px;color:#fff">Der Domino-Effekt</div>')

if __name__ == "__main__":
    if "tiktok" in sys.argv:
        seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
    else:
        seite(HERE, [YT], tiktok=False, glow=("75%", "45%"))
