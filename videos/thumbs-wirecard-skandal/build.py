#!/usr/bin/env python3
"""TikTok-Cover wirecard-skandal – riesige „1,9 Mrd. €“ mit roter Absturz-Kurve, Wirecard-Logo, Stempel SKANDAL, Pill Wo ist Marsalek? (neu: Zahl + Absturz)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

GELB = "#ffc533"
WC = (HERE / "assets/wirecard.svg").exists()
LOGO = (f'<img src="assets/wirecard.svg" style="width:100%;display:block"/>' if WC else
        '<div style="font-weight:900;font-size:120px;color:#1b3c6e;text-align:center;letter-spacing:-2px">wirecard</div>')
LG = ('<div style="position:absolute;left:240px;top:650px;width:600px;padding:36px 50px;border-radius:34px;background:#fff;transform:rotate(-3deg);'
      f'box-shadow:0 0 90px #3a7bd599, 0 40px 60px #000;z-index:3">{LOGO}</div>')
ZAHL = (f'<div style="position:absolute;left:0;width:1080px;top:900px;text-align:center;font-weight:900;font-size:200px;line-height:1;white-space:nowrap;color:{GELB};'
        f'text-shadow:0 0 60px {GELB}aa, 0 10px 0 #000;z-index:4">1,9 Mrd.€</div>')
KURVE = ('<svg viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:2">'
         f'<path d="M90 1120 L330 1080 L520 1110 L640 1500 L800 1680 L990 1720" fill="none" stroke="{ROT}" stroke-width="22" stroke-linejoin="round" '
         'style="filter:drop-shadow(0 0 24px #ff4d4d)"/></svg>')
ST = (f'<div style="position:absolute;left:560px;top:1180px;padding:10px 30px;border:10px solid {ROT};border-radius:20px;color:{ROT};font-weight:900;'
      'font-size:90px;letter-spacing:4px;transform:rotate(-10deg);background:#0e1012dd;box-shadow:0 0 40px #ff4d4d88;z-index:5">WEG!</div>')
TT = (titel([("Einfach weg?", "w"), ("Wirecard-Skandal", "box")], 0, 200, 110, w=1080, align="center") + KURVE + LG + ZAHL + ST
      + pill(110, 1560, "Wo ist Marsalek?", OR, 72, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
