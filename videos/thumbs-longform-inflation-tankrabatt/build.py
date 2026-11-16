#!/usr/bin/env python3
"""TikTok-Cover longform-inflation-tankrabatt – „2,8 %“ groß, Zapfsäulen-Display „+16,7 ct“ ab Januar, Pille „Der Trick dahinter“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

ZAHL = '<div style="position:absolute;left:0;width:1080px;top:540px;text-align:center;font-weight:900;font-size:260px;color:#ff8a1f;text-shadow:0 0 70px #ff8a1f;z-index:2">2,8 %</div>'
ZAPF = ('<div style="position:absolute;left:200px;top:900px;width:680px;padding:34px;border-radius:34px;background:#0b0d0f;border:10px solid #ff4d4d;'
        'box-shadow:0 0 90px #ff4d4d88, 0 30px 50px #000;text-align:center;transform:rotate(-3deg);z-index:3"><div style="font-size:90px">⛽</div>'
        '<div style="font-family:monospace;font-weight:900;font-size:130px;white-space:nowrap;color:#ff4d4d;text-shadow:0 0 40px #ff4d4d;line-height:1">+16,7 ct</div>'
        '<div style="font-family:monospace;font-size:44px;color:#ccc">ab Januar?</div></div>')
TT = (titel([("Inflation sinkt –", "w"), ("aber Vorsicht!", "box")], 0, 220, 112, w=1080, align="center") + ZAHL + ZAPF
      + pill(200, 1560, "Der Trick dahinter", "#ffd34d", 72, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
