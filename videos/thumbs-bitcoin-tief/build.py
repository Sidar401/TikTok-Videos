#!/usr/bin/env python3
"""TikTok-Cover bitcoin-tief – Dark Glow, Bitcoin-Münze mit Riss + Crash-Linie."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, chart, pill, seite, titel  # noqa: E402

BTC = "#f7931a"
MUENZE = (f'<div style="position:absolute;left:330px;top:640px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd28a,{BTC} 55%,#a85e00);'
          f'box-shadow:0 0 120px {BTC}aa, 0 40px 60px #000;display:flex;align-items:center;justify-content:center;transform:rotate(-12deg);z-index:2">'
          '<img src="assets/bitcoin.svg" style="width:80%"/></div>'
          '<svg viewBox="0 0 420 420" style="position:absolute;left:330px;top:640px;width:420px;height:420px;z-index:3;transform:rotate(-12deg)">'
          '<path d="M210 0 L190 90 L240 150 L180 230 L230 300 L200 420" fill="none" stroke="#111" stroke-width="12" stroke-linejoin="round"/></svg>')
CRASH = [(0, 0.85), (0.15, 0.95), (0.3, 0.8), (0.45, 0.88), (0.6, 0.6), (0.75, 0.45), (0.9, 0.2), (1, 0.08)]
TT = (titel([("Bitcoin", "w"), ("STÜRZT AB", "rot")], 0, 220, 130, w=1080, align="center") + MUENZE
      + chart(CRASH, 100, 1110, 820, 330, ROT, pills=[(7, "−40 %")]) + pill(170, 1540, "3-Monats-Tief – warum?", BTC, 60, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
