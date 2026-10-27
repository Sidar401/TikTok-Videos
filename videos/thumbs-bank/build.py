#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für bank-pleite – Dark Glow. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, seite, titel  # noqa: E402

BANK = (f'<svg viewBox="0 0 200 180" style="position:absolute;left:240px;top:780px;width:600px;height:540px;filter:drop-shadow(0 0 30px {OR});z-index:2">'
        f'<path d="M10 60 L100 10 L190 60 Z" fill="none" stroke="{OR}" stroke-width="8" stroke-linejoin="round"/>'
        + "".join(f'<rect x="{30 + i * 38}" y="72" width="16" height="70" rx="4" fill="{OR}"/>' for i in range(4))
        + f'<rect x="10" y="150" width="180" height="16" rx="6" fill="{OR}"/></svg>')
STEMPEL = (f'<div style="position:absolute;left:0;top:1000px;width:1080px;display:flex;justify-content:center;z-index:3"><span style="padding:10px 40px;'
           f'border:12px solid {ROT};border-radius:20px;background:#0e1012cc;color:{ROT};font-weight:900;font-size:130px;transform:rotate(-10deg);box-shadow:0 0 60px {ROT}88">PLEITE</span></div>')

TT = (titel([("Deine Bank", "w"), ("geht pleite –", "w"), ("Geld WEG?", "box")], 0, 220, 116, w=1080, align="center")
      + BANK + STEMPEL
      + f'<div style="position:absolute;left:0;top:1450px;width:1080px;text-align:center;font-weight:900;font-size:72px;color:{GRUEN};text-shadow:0 0 40px {GRUEN}88">bis 100.000 € geschützt?</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
