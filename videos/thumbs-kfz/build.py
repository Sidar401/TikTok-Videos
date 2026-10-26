#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für kfz-wechsel – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402

KAL = (f'<div style="position:absolute;left:290px;top:820px;width:500px;height:500px;border-radius:50px;background:#16191b;border:8px solid {OR};'
       f'box-shadow:0 0 90px {OR}77, 0 40px 60px #000;transform:rotate(-5deg);overflow:hidden;z-index:2">'
       f'<div style="height:130px;background:{OR};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:76px;color:#111">NOVEMBER</div>'
       f'<div style="text-align:center;font-weight:900;font-size:290px;line-height:360px;color:#fff;text-shadow:0 0 40px {OR}aa">30</div></div>')

TT = (titel([("Autoversicherung", "w"), ("bis 30.11.", "box"), ("wechseln!", "w")], 0, 210, 100, w=1080, align="center")
      + KAL
      + pill(140, 1420, "780 €", ROT, 80, -4).replace(">780 €<", "><s>780 €</s><")
      + pill(600, 1420, "520 €", GRUEN, 80, 4)
      + f'<div style="position:absolute;left:0;top:1600px;width:1080px;text-align:center;font-weight:900;font-size:80px;color:{GRUEN};text-shadow:0 0 40px {GRUEN}88">+260 € pro Jahr</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
