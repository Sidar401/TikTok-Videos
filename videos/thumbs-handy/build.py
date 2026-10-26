#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für handyvertrag – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402

HANDY = (f'<div style="position:absolute;left:300px;top:820px;width:480px;height:860px;border-radius:70px;background:#16191b;border:10px solid {OR};'
         f'box-shadow:0 0 90px {OR}77, 0 40px 60px #000;transform:rotate(-6deg);z-index:2;padding:70px 40px">'
         f'<div style="width:120px;height:18px;border-radius:9px;background:#2a2f33;margin:-40px auto 50px"></div>'
         f'<div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:2px">VERTRAG</div>'
         f'<div style="font-weight:900;font-size:80px;white-space:nowrap;color:#fff;margin:10px 0 40px">50 €<span style="font-size:44px;color:#9aa3a8"> /Monat</span></div>'
         f'<div style="height:4px;background:#ffffff33;margin-bottom:34px"></div>'
         f'<div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:2px">NACH 2 JAHREN</div>'
         f'<div style="font-weight:900;font-size:92px;white-space:nowrap;color:{ROT};text-shadow:0 0 40px {ROT}aa">1.200 €</div></div>')

TT = (titel([("Dein Handyvertrag", "w"), ("ist ZU TEUER", "box")], 0, 230, 94, w=1080, align="center")
      + pill(260, 560, "+260 € sparen", GRUEN, 72, -4)
      + HANDY)

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "60%"))
