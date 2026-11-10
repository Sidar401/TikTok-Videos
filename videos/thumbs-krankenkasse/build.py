#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für krankenkasse-wechsel – Dark Glow."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, seite, titel  # noqa: E402

BLAU = "#4d8ff0"
KARTE = (f'<div style="position:absolute;left:170px;top:700px;width:740px;height:460px;border-radius:40px;background:linear-gradient(135deg,{BLAU},#2a5bb8);'
         f'box-shadow:0 0 100px {BLAU}88;transform:rotate(-5deg);z-index:2">'
         f'<div style="position:absolute;left:55px;top:55px;width:130px;height:96px;border-radius:16px;background:#ffc533"></div>'
         f'<div style="position:absolute;left:55px;top:210px;font-weight:900;font-size:60px;color:#fff">Krankenkasse</div>'
         f'<div style="position:absolute;left:55px;top:320px;width:420px;height:24px;border-radius:12px;background:#ffffff55"></div></div>')
TT = (titel([("Zahlst du", "w"), ("ZU VIEL?", "box")], 0, 230, 140, w=1080, align="center")
      + KARTE
      + f'<div style="position:absolute;left:0;top:1260px;width:1080px;text-align:center;font-weight:900;font-size:190px;color:{GRUEN};text-shadow:0 0 60px {GRUEN}aa;z-index:3">≈ 130 €</div>'
      + '<div style="position:absolute;left:0;top:1500px;width:1080px;text-align:center;font-weight:900;font-size:64px;color:#fff">pro Jahr sparen</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
