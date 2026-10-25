#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für drei-konten – Stil „Dark Glow“. Aufruf: python3 build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, muenzen, pill, seite, titel  # noqa: E402


def karte(x, y, dreh, name, sub, c1, c2, nr):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:620px;height:390px;border-radius:36px;transform:rotate({dreh}deg);'
            f'background:linear-gradient(135deg,{c1},{c2});box-shadow:0 0 60px {c1}88, 0 30px 50px #000c;border:3px solid #ffffff33;z-index:2;padding:40px 46px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font-weight:900;font-size:62px;color:#111">{name}</div>'
            f'<div style="width:86px;height:86px;border-radius:50%;background:#111;color:#fff;font-weight:900;font-size:54px;display:flex;align-items:center;justify-content:center">{nr}</div></div>'
            f'<div style="margin-top:40px;width:110px;height:80px;border-radius:14px;background:linear-gradient(135deg,#fff2b0,#ffc533 60%,#b87800)"></div>'
            f'<div style="font-weight:800;font-size:40px;color:#111c;margin-top:30px">{sub}</div></div>')


TT = (titel([("Warum", "w"), ("EIN Konto", "rot"), ("nicht reicht", "w")], 0, 210, 124, w=1080, align="center")
      + karte(150, 830, -12, "Girokonto", "Gehalt & Fixkosten", "#4d8ff0", "#2a5cb8", 1)
      + karte(260, 1010, -3, "Tagesgeld", "Notgroschen + Zinsen", "#3ddc84", "#1f9a5a", 2)
      + karte(330, 1190, 7, "Depot", "ETF-Sparplan", "#ffa040", "#d46a00", 3)
      + muenzen(70, 1380, 6, 150)
      + pill(150, 1690, "Das 3-Konten-Modell", OR, 62))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "60%"))
