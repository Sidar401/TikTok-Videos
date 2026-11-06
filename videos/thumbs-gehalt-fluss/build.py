#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für gehalt-fluss – Dark Glow. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, pill, seite, titel  # noqa: E402


def box(y, oben, zahl, farbe):
    return (f'<div style="position:absolute;left:190px;top:{y}px;width:700px;padding:20px 0 26px;border-radius:34px;background:#16191b;border:8px solid {farbe};'
            f'box-shadow:0 0 70px {farbe}77;text-align:center;z-index:2"><div style="font-weight:800;font-size:54px;color:#ffffffcc">{oben}</div>'
            f'<div style="font-weight:900;font-size:150px;line-height:1;color:{farbe};text-shadow:0 0 50px {farbe}88">{zahl}</div></div>')


PFEIL = (f'<svg viewBox="0 0 100 300" style="position:absolute;left:490px;top:1000px;width:100px;height:300px;z-index:1">'
         f'<path d="M50 0 L50 250 M15 215 L50 260 L85 215" fill="none" stroke="{OR}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>')

TT = (titel([("Wohin fließt", "w"), ("DEIN GELD?", "box")], 0, 200, 124, w=1080, align="center")
      + box(640, "Dein Chef zahlt", "3.600 €", OR) + PFEIL + box(1300, "Du bekommst", "2.028 €", GRUEN)
      + pill(60, 1070, "−600 €", "#ff4d4d", 58, -8) + pill(730, 1040, "−320 €", "#ff4d4d", 58, 7)
      + pill(70, 1190, "−279 €", "#ff4d4d", 50, 5) + pill(760, 1170, "−373 €", "#ff4d4d", 50, -6))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
