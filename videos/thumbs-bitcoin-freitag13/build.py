#!/usr/bin/env python3
"""TikTok-Cover bitcoin-freitag13 – Dark Glow: Kalenderblatt „Freitag 13“ + Angst-Barometer (Nadel auf 20) + Bitcoin-Münze."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, pill, seite, titel  # noqa: E402

BTC = "#f7931a"
KAL = ('<div style="position:absolute;left:90px;top:640px;width:380px;height:420px;border-radius:34px;background:#fff;box-shadow:0 0 80px #ff4d4d66, 0 40px 60px #000;'
       'transform:rotate(-8deg);overflow:hidden;z-index:2"><div style="height:120px;background:#ff4d4d;color:#fff;font-weight:900;font-size:64px;display:flex;align-items:center;justify-content:center">FREITAG</div>'
       '<div style="font-weight:900;font-size:240px;color:#111;text-align:center;line-height:300px">13</div></div>')
MUENZE = (f'<div style="position:absolute;left:600px;top:620px;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd28a,{BTC} 55%,#a85e00);'
          f'box-shadow:0 0 120px {BTC}aa, 0 40px 60px #000;display:flex;align-items:center;justify-content:center;transform:rotate(14deg);z-index:2">'
          '<img src="assets/bitcoin.svg" style="width:80%"/></div>')
GAUGE = ('<svg viewBox="0 0 1080 700" style="position:absolute;left:0;top:1120px;width:1080px;height:700px;z-index:2">'
         '<defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#ff4d4d"/><stop offset="0.5" stop-color="#f5c542"/><stop offset="1" stop-color="#2fd27a"/></linearGradient></defs>'
         '<path d="M220 520 A320 320 0 0 1 860 520" fill="none" stroke="url(#gg)" stroke-width="70" stroke-linecap="round"/>'
         '<line x1="540" y1="520" x2="540" y2="250" stroke="#fff" stroke-width="22" stroke-linecap="round" transform="rotate(-54 540 520)"/>'
         '<circle cx="540" cy="520" r="40" fill="#fff"/></svg>')
TT = (titel([("Freitag, der 13.", "w"), ("BITCOIN CRASHT", "rot")], 0, 210, 116, w=1080, align="center") + KAL + MUENZE + GAUGE
      + pill(250, 1690, "Angst-Index: 20 😱", ROT, 70, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
