#!/usr/bin/env python3
"""TikTok-Cover longform-gta6-aktie – Dark Glow: GTA-VI-Logo groß, Take-Two-Logo, Kurve mit Fragezeichen „Hit oder Crash?“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, ROT, chart, pill, seite, titel  # noqa: E402

GTA = ('<img src="assets/gta6.png" style="position:absolute;left:250px;top:560px;width:580px;filter:drop-shadow(0 0 70px #ff4fa3aa) drop-shadow(0 30px 40px #000);z-index:2"/>')
T2 = ('<div style="position:absolute;left:760px;top:1000px;width:220px;padding:20px;border-radius:24px;background:#fff;box-shadow:0 0 50px #ffffff55;transform:rotate(6deg);z-index:3">'
      '<img src="assets/taketwo.png" style="width:100%;display:block"/></div>')
K = [(0, 0.3), (0.2, 0.55), (0.4, 0.45), (0.55, 0.8), (0.7, 0.62)]
TT = (titel([("Die Aktie hinter", "w"), ("GTA 6", "box")], 0, 220, 110, w=1080, align="center") + GTA + T2
      + chart(K, 90, 1300, 620, 300, GRUEN, pills=[(4, "231 $")], fill=True)
      + '<div style="position:absolute;left:700px;top:1290px;font-weight:900;font-size:220px;color:#ff4d4d;text-shadow:0 0 60px #ff4d4d;z-index:3">?</div>'
      + pill(180, 1660, "Hit oder Crash am 19.11.?", ROT, 56, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "40%"))
