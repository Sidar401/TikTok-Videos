#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für dispo-falle – Stil „Dark Glow“. Aufruf: python3 build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, chart, pill, seite, titel  # noqa: E402

KARTE = (f'<div style="position:absolute;left:150px;top:880px;width:780px;height:480px;border-radius:44px;transform:rotate(-6deg);'
         f'background:linear-gradient(135deg,#2c3236,#121517);border:5px solid {OR};box-shadow:0 0 90px {OR}88, 0 40px 60px #000;padding:50px 56px;z-index:2">'
         f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="width:130px;height:96px;border-radius:16px;'
         f'background:linear-gradient(135deg,#fff2b0,#ffc533 60%,#b87800)"></div><div style="font-weight:900;font-size:44px;color:#9aa3a8;letter-spacing:3px">GIROKONTO</div></div>'
         f'<div style="margin-top:70px;font-weight:900;font-size:150px;line-height:1;color:{ROT};text-shadow:0 0 50px {ROT}cc;white-space:nowrap">−2.000 €</div></div>')

TT = (titel([("Dein Dispo", "w"), ("ist eine", "w"), ("KOSTENFALLE", "box")], 0, 200, 112, w=1080, align="center")
      + chart([(0, 0.9), (0.2, 0.75), (0.4, 0.78), (0.6, 0.45), (0.8, 0.35), (1, 0.05)], 80, 900, 920, 640, OR)
      + KARTE
      + pill(600, 780, "10 % Zinsen", OR, 60, 6)
      + pill(170, 1500, "200 € im Jahr weg", "#2a2f33", 64, -3).replace("color:#fff", f"color:{OR};border:4px solid {OR}"))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "60%"))
