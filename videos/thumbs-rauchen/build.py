#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für rauchen-kosten – Dark Glow. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, seite, titel  # noqa: E402

ZIG = (f'<svg viewBox="0 0 600 260" style="position:absolute;left:140px;top:760px;width:800px;height:347px;overflow:visible;z-index:2">'
       f'<rect x="40" y="150" width="420" height="60" rx="10" fill="#f2f2f2"/><rect x="40" y="150" width="130" height="60" rx="10" fill="{OR}"/>'
       f'<rect x="455" y="150" width="40" height="60" rx="8" fill="{ROT}" filter="drop-shadow(0 0 24px {ROT})"/>'
       f'<path d="M480 140 C440 100 520 80 480 40 C450 10 500 -10 470 -40" fill="none" stroke="#ffffff77" stroke-width="16" stroke-linecap="round"/></svg>')

TT = (titel([("So viel kostet", "w"), ("RAUCHEN", "box"), ("wirklich", "w")], 0, 220, 120, w=1080, align="center")
      + ZIG
      + f'<div style="position:absolute;left:0;top:1200px;width:1080px;text-align:center;font-weight:900;font-size:150px;color:{ROT};text-shadow:0 0 50px {ROT}aa">32.850 €</div>'
      + f'<div style="position:absolute;left:0;top:1380px;width:1080px;text-align:center;font-weight:900;font-size:66px;color:#fff">in nur 10 Jahren</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
