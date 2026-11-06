#!/usr/bin/env python3
"""YouTube-Thumbnail 16:9 für longform-ki-blase – Dark Glow, oranger Rahmen."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, pill, seite, titel  # noqa: E402

ROT = "#ff4d4d"
BLASE = (f'<div style="position:absolute;left:1120px;top:170px;width:640px;height:640px;border-radius:50%;z-index:2;'
         f'background:radial-gradient(circle at 35% 30%, #ffffffdd 0 7%, #ff8a1f66 24%, #ff8a1f22 55%, #ff8a1f88 100%);border:8px solid {OR};box-shadow:0 0 140px {OR}88;'
         f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:190px;color:#fff;text-shadow:0 8px 0 #000">KI</div>'
         f'<svg viewBox="0 0 200 200" style="position:absolute;left:1500px;top:180px;width:260px;height:260px;z-index:3">'
         f'<path d="M20 30 L80 90 L60 110 L130 160 L110 180 L190 195" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round" filter="drop-shadow(0 0 12px #fff)"/></svg>')
YT = (titel([("Platzt jetzt die", "w"), ("KI-BLASE?", "box")], 90, 150, 140)
      + BLASE
      + pill(110, 640, "−2,5 Billionen $", ROT, 92, -4)
      + '<div style="position:absolute;left:110px;top:830px;font-weight:900;font-size:64px;color:#fff">…und was ist mit deinem ETF?</div>')

if __name__ == "__main__":
    seite(HERE, [YT], tiktok=False, glow=("75%", "45%"))
