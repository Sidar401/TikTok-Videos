#!/usr/bin/env python3
"""TikTok-Cover longform-commerzbank – Dark Glow: Commerzbank-Logo, Italien-Flagge, Stimmen-Balken 49,65 %."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

UC = "#E2001A"
LOGO = ('<div style="position:absolute;left:110px;top:640px;width:860px;padding:36px;border-radius:30px;background:#fff;box-shadow:0 0 90px #FFCC0088, 0 40px 60px #000;'
        'transform:rotate(-4deg);z-index:2"><img src="assets/commerzbank.png" style="width:100%;display:block"/></div>')
FLAGGE = ('<div style="position:absolute;left:290px;top:930px;width:500px;height:333px;display:flex;border-radius:18px;overflow:hidden;box-shadow:0 0 80px #ce2b3788, 0 40px 60px #000;'
          'transform:rotate(5deg);z-index:2"><div style="flex:1;background:#009246"></div><div style="flex:1;background:#fff"></div><div style="flex:1;background:#ce2b37"></div></div>')
BAR = (f'<div style="position:absolute;left:110px;top:1420px;width:860px;height:120px;border-radius:60px;background:#1b1f22;border:5px solid #ffffff44;overflow:hidden;z-index:2">'
       f'<div style="width:49.65%;height:100%;background:linear-gradient(90deg,{UC}aa,{UC});box-shadow:0 0 40px {UC}"></div></div>'
       f'<img src="assets/unicredit-symbol.png" style="position:absolute;left:130px;top:1430px;height:100px;z-index:3"/>'
       f'<div style="position:absolute;left:560px;top:1440px;font-weight:900;font-size:70px;color:#fff;z-index:3">49,65 %</div>')
TT = (titel([("Die Commerzbank", "w"), ("wird ITALIENISCH", "box")], 0, 230, 96, w=1080, align="center") + LOGO + FLAGGE + BAR
      + pill(230, 1600, "Stimmen für UniCredit", ROT, 60, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
