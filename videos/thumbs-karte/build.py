#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für karte-bargeld – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, seite, titel  # noqa: E402

KARTE = (f'<div style="position:absolute;left:90px;top:860px;width:440px;height:280px;border-radius:30px;background:linear-gradient(135deg,#4d8ff0,#2a5cb8);'
         f'box-shadow:0 0 60px #4d8ff088, 0 30px 50px #000c;transform:rotate(-8deg);z-index:2;padding:36px">'
         f'<div style="width:90px;height:66px;border-radius:12px;background:linear-gradient(135deg,#fff2b0,#ffc533 60%,#b87800)"></div></div>')
SCHEINE = "".join(f'<div style="position:absolute;left:{570 + i * 10}px;top:{880 - i * 22}px;width:420px;height:220px;border-radius:20px;'
                  f'background:linear-gradient(135deg,#9fdc8c,#4d9a43);border:4px solid #2f5a28;box-shadow:0 0 40px {GRUEN}55;transform:rotate(6deg);z-index:2"></div>'
                  for i in range(4))
VS = (f'<div style="position:absolute;left:465px;top:1180px;width:150px;height:150px;border-radius:50%;background:{OR};color:#111;font-weight:900;font-size:66px;'
      f'display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 10px #0e1012, 0 0 60px {OR};z-index:4">VS</div>')

TT = (titel([("Karte oder", "w"), ("Bargeld?", "box")], 0, 220, 140, w=1080, align="center")
      + KARTE + SCHEINE + VS
      + f'<div style="position:absolute;left:0;top:1440px;width:1080px;text-align:center;font-weight:900;font-size:70px;line-height:1.15;color:#fff">Womit gibst du<br/><span style="color:{OR}">mehr aus?</span></div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
