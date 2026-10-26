#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für black-friday – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, seite, titel  # noqa: E402

SCHILD = (f'<div style="position:absolute;left:170px;top:860px;width:740px;padding:50px 60px;border-radius:44px;background:#16191b;border:8px solid {OR};'
          f'box-shadow:0 0 90px {OR}77, 0 40px 60px #000;transform:rotate(-4deg);z-index:2">'
          f'<div style="font-weight:900;font-size:90px;color:#9aa3a8;text-decoration:line-through;text-decoration-color:{ROT};text-decoration-thickness:12px">UVP 199 €</div>'
          f'<div style="font-weight:900;font-size:200px;line-height:1;color:#fff">99 €</div>'
          f'<div style="position:absolute;right:-30px;top:-50px;padding:14px 34px;border-radius:24px;background:{ROT};color:#fff;font-weight:900;font-size:80px;'
          f'transform:rotate(10deg);box-shadow:0 0 40px {ROT}aa">−50 %?</div></div>')

TT = (titel([("BLACK FRIDAY", "w"), ("3 Tricks", "box"), ("der Händler", "w")], 0, 220, 118, w=1080, align="center")
      + SCHILD
      + f'<div style="position:absolute;left:0;top:1440px;width:1080px;text-align:center;font-weight:900;font-size:76px;color:{OR};text-shadow:0 0 40px {OR}88">Fake-Rabatt?</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
