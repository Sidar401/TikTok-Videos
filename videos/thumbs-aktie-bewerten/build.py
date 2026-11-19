#!/usr/bin/env python3
"""TikTok-Cover aktie-bewerten – zwei Preisschilder 5 € (rot, TEURER) vs 500 € (grün, BILLIGER), großes Fragezeichen, Pill „4 Profi-Checks“ (neu: Preisschild-Duell)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402


def schild(text, x, y, f, dreh, unter):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({dreh}deg);z-index:3">'
            f'<div style="position:relative;padding:30px 60px 30px 110px;border-radius:30px 90px 90px 30px;background:{f};color:#111;font-weight:900;font-size:150px;'
            f'box-shadow:0 0 80px {f}aa, 0 30px 50px #000"><span style="position:absolute;left:34px;top:50%;width:44px;height:44px;margin-top:-22px;border-radius:50%;background:#111"></span>{text}</div>'
            f'<div style="margin-top:18px;text-align:center;font-weight:900;font-size:64px;color:{f};text-shadow:0 0 30px {f}">{unter}</div></div>')


TT = (titel([("Welche Aktie", "w"), ("ist billiger?", "box")], 0, 200, 110, w=1080, align="center")
      + schild("5 €", 120, 640, ROT, -7, "TEURER!") + schild("500 €", 300, 1010, GRUEN, 5, "BILLIGER!")
      + pill(230, 1500, "4 Profi-Checks ✓", OR, 76, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
