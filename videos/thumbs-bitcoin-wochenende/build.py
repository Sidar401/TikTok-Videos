#!/usr/bin/env python3
"""TikTok-Cover bitcoin-wochenende – Dark Glow: Waage/Linie-Motiv: gelbe 200-Wochen-Linie, Bitcoin-Kurve bricht durch, Münze fällt."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, chart, pill, seite, titel  # noqa: E402

BTC = "#f7931a"
MUENZE = (f'<div style="position:absolute;left:640px;top:1250px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd28a,{BTC} 55%,#a85e00);'
          f'box-shadow:0 0 100px {BTC}aa, 0 40px 60px #000;display:flex;align-items:center;justify-content:center;transform:rotate(24deg);z-index:3">'
          '<img src="assets/bitcoin.svg" style="width:80%"/></div>')
LINIE = ('<svg viewBox="0 0 1080 500" style="position:absolute;left:0;top:700px;width:1080px;height:500px;z-index:2">'
         '<path d="M60 380 L1020 220" stroke="#ffc533" stroke-width="14" stroke-dasharray="30 18" filter="drop-shadow(0 0 12px #ffc533)"/></svg>'
         '<div style="position:absolute;left:600px;top:840px;padding:6px 18px;border-radius:12px;background:#ffc533;color:#111;font-weight:900;font-size:40px;z-index:3">200-Wochen-Linie</div>')
K = [(0, 0.95), (0.18, 0.85), (0.35, 0.8), (0.5, 0.62), (0.62, 0.45), (0.74, 0.2), (0.82, 0.05)]
TT = (titel([("Bitcoin", "w"), ("BRICHT DURCH", "rot")], 0, 220, 108, w=1080, align="center") + LINIE + chart(K, 60, 720, 960, 520, ROT, pills=[(6, "≈ 65.000 $")])
      + MUENZE + pill(120, 1640, "−14 % in einer Woche", ROT, 64, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
