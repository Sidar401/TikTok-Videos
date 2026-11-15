#!/usr/bin/env python3
"""TikTok-Cover longform-anthropic-ipo – Anthropic-Logo, Claude-Symbol, Nasdaq, Datum Do 19.11., 1,4 Billionen $."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, chart, pill, seite, titel  # noqa: E402

AN = ('<div style="position:absolute;left:140px;top:620px;width:800px;padding:50px 60px;border-radius:36px;background:#fff;'
      'box-shadow:0 0 90px #ff8a1f88, 0 40px 60px #000;z-index:2"><img src="assets/anthropic.svg" style="width:100%;display:block"/></div>')
CL = ('<div style="position:absolute;left:600px;top:880px;width:380px;padding:24px 30px;border-radius:24px;background:#fff;transform:rotate(5deg);'
      'box-shadow:0 0 50px #d9775788, 0 30px 40px #000;z-index:3"><img src="assets/claude.svg" style="width:100%;display:block"/></div>')
NQ = ('<div style="position:absolute;left:90px;top:900px;width:280px;padding:20px;border-radius:22px;background:#fff;transform:rotate(-5deg);'
      'box-shadow:0 0 40px #ffffff55, 0 30px 40px #000;z-index:3"><img src="assets/nasdaq.svg" style="width:100%;display:block"/></div>')
K = [(0, 0.2), (0.25, 0.35), (0.5, 0.3), (0.75, 0.6), (1, 0.9)]
TT = (titel([("Die KI hinter Claude", "w"), ("geht an die Börse", "box")], 0, 220, 96, w=1080, align="center") + AN + CL + NQ
      + chart(K, 140, 1110, 800, 240, GRUEN, fill=True)
      + pill(170, 1400, "bis 1,4 Billionen $", GRUEN, 80, -2)
      + pill(300, 1600, "Donnerstag 19.11.", ROT, 64, 2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "40%"))
