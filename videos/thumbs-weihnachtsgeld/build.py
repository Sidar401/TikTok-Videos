#!/usr/bin/env python3
"""TikTok-Cover weihnachtsgeld-netto – Dark Glow, Geschenk wird halbiert."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, pill, seite, titel  # noqa: E402

WR, GELB = "#e6324b", "#ffd54a"
G = (f'<svg viewBox="0 0 300 300" style="position:absolute;left:{{x}}px;top:0;width:420px;height:420px;z-index:2;transform:rotate({{d}}deg);filter:drop-shadow(0 0 40px {WR})">'
     f'<rect x="30" y="110" width="240" height="170" rx="14" fill="{WR}"/><rect x="15" y="80" width="270" height="50" rx="10" fill="#ff5a6e"/>'
     f'<rect x="135" y="80" width="30" height="200" fill="{GELB}"/><path d="M150 80 Q100 20 80 60 Q90 85 150 80 Q210 85 220 60 Q200 20 150 80" fill="{GELB}"/></svg>')
HALB = ('<div style="position:absolute;left:330px;top:760px;width:210px;height:440px;overflow:hidden;z-index:2">' + G.format(x=0, d=-6) + '</div>'
        '<div style="position:absolute;left:600px;top:800px;width:210px;height:440px;overflow:hidden;z-index:2;transform:rotate(10deg)">'
        + G.format(x=-210, d=-6) + '</div>'
        '<svg viewBox="0 0 1080 1920" style="position:absolute;inset:0;width:1080px;height:1920px;z-index:3"><path d="M565 720 L560 1260" stroke="#fff" stroke-width="10" stroke-dasharray="26 18"/></svg>')
TT = (titel([("Weihnachtsgeld", "w"), ("HALB WEG?", "rot")], 0, 220, 120, w=1080, align="center") + HALB
      + '<div style="position:absolute;left:0;top:1300px;width:1080px;text-align:center;font-weight:900;font-size:96px;white-space:nowrap;color:#fff">3.000 € → <span style="color:#ff4d4d;text-shadow:0 0 50px #ff4d4daa">1.680 €</span></div>'
      + pill(330, 1520, "Wo ist der Rest?", "#ff8a1f", 66, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
