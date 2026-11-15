#!/usr/bin/env python3
"""TikTok-Cover gold-bitcoin-absturz – Goldbarren + Bitcoin-Symbol, roter Crash-Pfeil, „−31 %“ / „½“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, chart, pill, seite, titel  # noqa: E402

GOLD = ('<div style="position:absolute;left:80px;top:640px;width:440px;height:190px;border-radius:18px;background:linear-gradient(160deg,#fff3b0 0%,#f5c542 35%,#b8860b 100%);'
        'box-shadow:0 0 90px #f5c542aa, 0 30px 50px #000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:76px;color:#7a5a00;letter-spacing:6px;transform:rotate(-6deg);z-index:2">GOLD</div>')
BTC = '<img src="assets/bitcoin.svg" style="position:absolute;left:620px;top:560px;width:360px;filter:drop-shadow(0 0 70px #f7931aaa) drop-shadow(0 30px 40px #000);transform:rotate(8deg);z-index:2"/>'
K = [(0, 0.9), (0.2, 0.75), (0.4, 0.8), (0.6, 0.45), (0.8, 0.3), (1, 0.05)]
TT = (titel([("Gold UND Bitcoin", "w"), ("stürzen ab", "rot")], 0, 220, 100, w=1080, align="center") + GOLD + BTC
      + chart(K, 110, 1000, 860, 360, ROT, fill=True)
      + pill(150, 900, "−31 %", ROT, 80, -4) + pill(640, 960, "½ wert", ROT, 76, 4)
      + pill(120, 1560, "Wo ist Geld noch sicher?", OR, 58, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
