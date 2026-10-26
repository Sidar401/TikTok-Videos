#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für wochen-challenge – Stil „Dark Glow“. Aufruf: python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, muenzen, pill, seite, titel  # noqa: E402

BARS = "".join(f'<div style="position:absolute;left:{110 + i * 16.5:.1f}px;top:{1560 - (i + 1) * 11}px;width:12px;height:{(i + 1) * 11}px;border-radius:4px;'
               f'background:{GRUEN if (i + 1) % 13 == 0 else OR};box-shadow:0 0 14px {OR}88;z-index:2"></div>' for i in range(52))

TT = (titel([("1 € pro Woche", "w"), ("mehr sparen …", "w"), ("= 1.378 €", "box")], 0, 220, 116, w=1080, align="center")
      + pill(215, 830, "52-Wochen-Challenge", OR, 62)
      + BARS
      + muenzen(150, 1010, 6, 150)
      + pill(110, 1600, "Woche 1: 1 €", "#2a2f33", 46).replace("color:#fff", f"color:{OR};border:3px solid {OR}")
      + pill(570, 1600, "Woche 52: 52 €", "#2a2f33", 46).replace("color:#fff", f"color:{GRUEN};border:3px solid {GRUEN}"))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "65%"))
