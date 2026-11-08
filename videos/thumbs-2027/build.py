#!/usr/bin/env python3
"""Thumbnails für longform-2027 – 16:9 (python3 build.py) und 9:16 (python3 build.py tiktok)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, seite, titel  # noqa: E402

ROT, GRUEN = "#ff4d4d", "#2fd27a"


def kalender(x, y, s=1.0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{420 * s:.0f}px;height:{470 * s:.0f}px;border-radius:{36 * s:.0f}px;background:#f4f1ea;overflow:hidden;'
            f'box-shadow:0 0 120px {OR}88;transform:rotate(4deg);z-index:2"><div style="height:{120 * s:.0f}px;background:{OR};color:#111;font-weight:900;font-size:{70 * s:.0f}px;'
            f'text-align:center;line-height:{120 * s:.0f}px">JAN</div><div style="text-align:center;font-weight:900;font-size:{150 * s:.0f}px;color:#111;line-height:{350 * s:.0f}px">2027</div></div>')


def stempel(txt, f, x, y, gr, rot):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;padding:6px 34px;border:10px solid {f};border-radius:20px;color:{f};font-weight:900;font-size:{gr}px;'
            f'transform:rotate({rot}deg);background:#0e1012ee;box-shadow:0 0 50px {f}88;z-index:3">{txt}</div>')


YT = (titel([("Das ändert sich", "w"), ("für DEIN Geld", "box")], 80, 140, 116)
      + kalender(1240, 220) + stempel("GEWINNER", GRUEN, 110, 600, 92, -5) + stempel("VERLIERER", ROT, 640, 760, 92, 4))
TT = (titel([("Das ändert sich", "w"), ("für DEIN Geld", "box")], 0, 170, 104, w=1080, align="center")
      + kalender(330, 640, 0.95) + stempel("GEWINNER", GRUEN, 120, 1240, 88, -5) + stempel("VERLIERER", ROT, 380, 1420, 84, 4)
      + '<div style="position:absolute;left:0;top:1640px;width:1080px;text-align:center;font-weight:900;font-size:62px;color:#fff">…bist du dabei?</div>')

if __name__ == "__main__":
    if "tiktok" in sys.argv:
        seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
    else:
        seite(HERE, [YT], tiktok=False, glow=("75%", "45%"))
