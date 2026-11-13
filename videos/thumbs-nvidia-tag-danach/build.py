#!/usr/bin/env python3
"""TikTok-Cover nvidia-tag-danach – Dark Glow: Nvidia-Logo + V-Kurve (−14 % → −4 %), Frage-Typo."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, chart, pill, seite, titel  # noqa: E402

NV = "#76b900"
SYM = Path(HERE / "assets/nv-symbol.svg").read_text().replace("<svg ", f'<svg fill="{NV}" style="width:170px;height:170px;filter:drop-shadow(0 0 30px {NV})" ', 1)
LOGO = (f'<div style="position:absolute;left:0;top:620px;width:1080px;display:flex;justify-content:center;align-items:center;gap:36px;z-index:3">{SYM}'
        '<img src="assets/nv-wort.svg" style="height:110px;filter:brightness(0) invert(1) drop-shadow(0 0 20px #ffffff55)"/></div>')
V = [(0, 0.85), (0.12, 0.12), (0.3, 0.3), (0.5, 0.42), (0.7, 0.5), (0.85, 0.6), (1, 0.66)]
TT = (titel([("Tag 1 ohne", "w"), ("JENSEN HUANG", "box")], 0, 230, 120, w=1080, align="center") + LOGO
      + chart(V, 110, 1080, 860, 480, GRUEN, pills=[(1, "−14 %"), (5, "nur −4 %")])
      + pill(150, 1680, "Die Börse überrascht 🤯", OR, 60, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
