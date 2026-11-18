#!/usr/bin/env python3
"""TikTok-Cover longform-anthropic-morgen – Countdown-Uhr 15:30 + Anthropic-Logo groß, Stempel FALLE, Pill ETF (neues Motiv: Uhr statt Chart)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402

GELB = "#ffc533"
UHR = ('<div style="position:absolute;left:150px;top:560px;width:780px;padding:26px 0;border-radius:40px;background:#000d;border:10px solid ' + GELB + ';'
       'box-shadow:0 0 120px #ffc53388, 0 40px 60px #000;text-align:center;font-family:\'JetBrains Mono\',monospace;font-weight:800;font-size:250px;color:' + GELB + ';'
       'text-shadow:0 0 50px ' + GELB + ';z-index:2">15:30</div>')
AN = ('<div style="position:absolute;left:170px;top:1000px;width:740px;padding:44px 56px;border-radius:34px;background:#fff;transform:rotate(-3deg);'
      'box-shadow:0 0 90px #d9775799, 0 40px 60px #000;z-index:3"><img src="assets/anthropic.svg" style="width:100%;display:block"/></div>')
ST = ('<div style="position:absolute;left:600px;top:470px;padding:10px 30px;border:10px solid ' + ROT + ';border-radius:20px;color:' + ROT + ';font-weight:900;'
      'font-size:90px;letter-spacing:4px;transform:rotate(12deg);background:#0e1012dd;box-shadow:0 0 40px #ff4d4d88;z-index:4">FALLE!</div>')
TT = (titel([("Morgen geht's los", "w"), ("Anthropic-Aktie", "box")], 0, 200, 100, w=1080, align="center") + UHR + ST + AN
      + pill(130, 1380, "kommt in dein ETF?", GRUEN, 70, -2)
      + pill(360, 1580, "Do 19.11.", OR, 64, 2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "38%"))
