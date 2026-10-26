#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für dreissig-tage-regel – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, seite, titel  # noqa: E402

TAGE = "".join(f'<div style="width:118px;height:118px;border-radius:20px;background:#16191b;border:4px solid {OR if i < 29 else GRUEN};'
               f'box-shadow:0 0 18px {OR if i < 29 else GRUEN}66;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;'
               f'color:{"#ffffff55" if i < 29 else GRUEN};position:relative">{i + 1}'
               + (f'<svg viewBox="0 0 100 100" style="position:absolute;inset:14px"><path d="M15 15 L85 85 M85 15 L15 85" stroke="{OR}" stroke-width="12" stroke-linecap="round"/></svg>' if i < 29 else "")
               + '</div>' for i in range(30))

TT = (titel([("Die 30-Tage-", "w"), ("Regel", "box")], 0, 220, 130, w=1080, align="center")
      + f'<div style="position:absolute;left:100px;top:700px;width:880px;display:grid;grid-template-columns:repeat(6,118px);gap:34px 30px;z-index:2">{TAGE}</div>'
      + f'<div style="position:absolute;left:0;top:1560px;width:1080px;text-align:center;font-weight:900;font-size:76px;color:#fff">gegen <span style="color:{ROT}">Spontankäufe</span></div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
