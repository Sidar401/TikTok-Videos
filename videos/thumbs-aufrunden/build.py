#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für aufrunden – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, muenzen, seite, titel  # noqa: E402

BON = (f'<div style="position:absolute;left:170px;top:820px;width:560px;padding:44px 50px;border-radius:36px;background:#16191b;border:6px solid {OR};'
       f'box-shadow:0 0 80px {OR}66, 0 30px 50px #000;transform:rotate(-4deg);z-index:2">'
       f'<div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:3px">EINKAUF</div>'
       f'<div style="font-weight:900;font-size:96px;white-space:nowrap;color:#ffffff88;text-decoration:line-through;text-decoration-color:{OR};text-decoration-thickness:10px">12,30 €</div>'
       f'<div style="font-weight:900;font-size:120px;white-space:nowrap;color:#fff">13,00 €</div></div>')

TT = (titel([("Sparen, ohne", "w"), ("es zu merken", "box")], 0, 220, 124, w=1080, align="center")
      + BON + muenzen(760, 1000, 6, 170)
      + f'<div style="position:absolute;left:0;top:1460px;width:1080px;text-align:center;font-weight:900;font-size:84px;color:{GRUEN};text-shadow:0 0 40px {GRUEN}88">+180 € / Jahr</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
