#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für gehaltserhoehung – Stil „Dark Glow“. Aufruf: python3 build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, chart, pill, seite, titel  # noqa: E402

GEHALT = [(0, 0.3), (0.3, 0.3), (0.32, 0.62), (0.62, 0.62), (0.64, 0.92), (1, 0.92)]
AUSGABEN = [(0, 0.12), (0.2, 0.2), (0.4, 0.45), (0.55, 0.55), (0.75, 0.82), (1, 0.9)]

TT = (titel([("Mehr Gehalt –", "w"), ("trotzdem", "w"), ("PLEITE?", "box")], 0, 200, 124, w=1080, align="center")
      + chart(GEHALT, 110, 930, 860, 520, GRUEN, fill=False)
      + chart(AUSGABEN, 110, 930, 860, 520, OR, fill=True)
      + pill(120, 820, "+200 € Gehalt", GRUEN, 54)
      + pill(560, 1300, "Ausgaben", OR, 54)
      + pill(220, 1600, "Lifestyle-Inflation", "#2a2f33", 64).replace("color:#fff", f"color:{OR};border:4px solid {OR}"))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "60%"))
