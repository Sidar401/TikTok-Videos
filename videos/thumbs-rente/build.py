#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für rentenluecke – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, seite, titel  # noqa: E402


def balken(x, h, farbe, label, wert, top=1560):
    return (f'<div style="position:absolute;left:{x}px;top:{top - h}px;width:300px;height:{h}px;border-radius:24px;background:linear-gradient(180deg,{farbe},{farbe}99);'
            f'box-shadow:0 0 50px {farbe}88;z-index:2;display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:24px 0">'
            f'<span style="font-weight:900;font-size:62px;color:#111">{wert}</span><span style="font-weight:800;font-size:44px;color:#111c">{label}</span></div>')


LUECKE = (f'<div style="position:absolute;left:640px;top:880px;width:300px;height:280px;border-radius:24px;border:7px dashed {OR};box-shadow:0 0 40px {OR}66;'
          f'display:flex;align-items:center;justify-content:center;z-index:2;font-weight:900;font-size:56px;white-space:nowrap;color:{OR};text-shadow:0 0 30px {OR}aa">−1.100 €</div>')

TT = (titel([("Wie viel Rente", "w"), ("bekommst DU", "w"), ("wirklich?", "box")], 0, 200, 118, w=1080, align="center")
      + balken(160, 680, GRUEN, "heute", "2.500 €") + balken(640, 380, "#9aa3a8", "Rente", "1.400 €") + LUECKE
      + f'<div style="position:absolute;left:0;top:1640px;width:1080px;text-align:center;font-weight:900;font-size:72px;color:{OR};text-shadow:0 0 40px {OR}88">Die Rentenlücke</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("60%", "60%"))
