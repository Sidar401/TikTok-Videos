#!/usr/bin/env python3
"""TikTok-Cover schufa-gratis – Dark Glow, Tacho 100–999 + Schufa-Logo."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, ROT, pill, seite, titel  # noqa: E402

GELB, SB = "#ffd54a", "#00a0e3"
cx, cy, r = 540, 1330, 340
s = []
for a, b, f in [(100, 500, ROT), (500, 776, GELB), (776, 999, GRUEN)]:
    w0, w1 = math.pi * (1 - (a - 100) / 899), math.pi * (1 - (b - 100) / 899)
    s.append(f'<path d="M{cx + r * math.cos(w0):.0f} {cy - r * math.sin(w0):.0f} A{r} {r} 0 0 1 {cx + r * math.cos(w1):.0f} {cy - r * math.sin(w1):.0f}" fill="none" stroke="{f}" stroke-width="70" style="filter:drop-shadow(0 0 20px {f})"/>')
w = math.pi * (1 - (900 - 100) / 899)
s.append(f'<path d="M{cx - 24} {cy} L{cx + (r - 50) * math.cos(w):.0f} {cy - (r - 50) * math.sin(w):.0f} L{cx + 18} {cy} Z" fill="#fff" stroke="#fff" stroke-width="10" stroke-linejoin="round"/><circle cx="{cx}" cy="{cy}" r="36" fill="#fff"/>')
TACHO = f'<svg viewBox="0 0 1080 1920" style="position:absolute;inset:0;width:1080px;height:1920px;z-index:2">{"".join(s)}</svg>'
LOGO = ('<div style="position:absolute;left:290px;top:700px;width:500px;height:150px;border-radius:30px;background:#fff;padding:24px 50px;display:flex;align-items:center;'
        f'justify-content:center;box-shadow:0 0 90px {SB}88;transform:rotate(-3deg);z-index:3"><img src="assets/schufa.svg" style="max-width:100%;max-height:100%"/></div>')
TT = (titel([("Dein Score", "w"), ("GRATIS", "box"), ("in 1 Minute", "w")], 0, 200, 120, w=1080, align="center") + LOGO + TACHO
      + pill(390, 1430, "100 – 999", "#ff8a1f", 70, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
