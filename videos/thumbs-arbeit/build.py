#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für arbeitsstunden – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

UHR = (f'<div style="position:absolute;left:290px;top:820px;width:500px;height:500px;border-radius:50%;background:#16191b;border:12px solid {OR};'
       f'box-shadow:0 0 90px {OR}77, 0 40px 60px #000;z-index:2;display:flex;flex-direction:column;align-items:center;justify-content:center">'
       f'<div style="font-weight:900;font-size:170px;line-height:1;color:#fff;text-shadow:0 0 40px {OR}aa">80</div>'
       f'<div style="font-weight:800;font-size:64px;color:{OR}">Stunden</div></div>')

TT = (titel([("Wie lange musst", "w"), ("du dafür", "w"), ("ARBEITEN?", "box")], 0, 200, 102, w=1080, align="center")
      + pill(90, 760, "Handy: 1.000 €", ROT, 62, -6)
      + UHR
      + f'<div style="position:absolute;left:0;top:1420px;width:1080px;text-align:center;font-weight:900;font-size:76px;color:#fff">= 2 volle <span style="color:{OR}">Wochen</span></div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
