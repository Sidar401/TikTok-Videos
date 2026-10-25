#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für etf-erklaert – Stil „Dark Glow“. Aufruf: python3 build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, chart, pill, seite, titel  # noqa: E402

FARBEN = ["#b36bdb", "#ffc533", "#4d8ff0", "#3ddc84", ROT, "#e0e0e0", OR, "#2c9a63", "#ff6fae", "#4dd0e1"]


def korb(x, y, w):
    teile = "".join(f'<g transform="rotate({(-1) ** i * (4 + i % 3 * 3)} {80 + (i % 5) * 88 + 38} {(i // 5) * 74 + 50})">'
                    f'<rect x="{80 + (i % 5) * 88}" y="{(i // 5) * 74 + 12}" width="76" height="76" rx="14" fill="{c}"/>'
                    f'<rect x="{80 + (i % 5) * 88}" y="{(i // 5) * 74 + 12}" width="76" height="26" rx="12" fill="#ffffff44"/></g>'
                    for i, c in enumerate(FARBEN))
    rand = "M40 170 L560 170 L500 420 L100 420 Z"
    return (f'<svg viewBox="0 0 600 440" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w * 0.733}px;overflow:visible;z-index:2">'
            f'<defs><filter id="kg" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="12"/></filter>'
            f'<linearGradient id="kf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2f33"/><stop offset="1" stop-color="#121517"/></linearGradient></defs>'
            f'{teile}'
            f'<path d="M110 175 Q300 -200 490 175" fill="none" stroke="{OR}" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="{rand}" fill="url(#kf)"/>'
            f'<path d="{rand}" fill="none" stroke="{OR}" stroke-width="30" stroke-linejoin="round" opacity="0.7" filter="url(#kg)"/>'
            f'<path d="{rand}" fill="none" stroke="{OR}" stroke-width="14" stroke-linejoin="round"/>'
            f'<text x="300" y="330" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="78" fill="#fff">ETF</text></svg>')


TT = (titel([("Was ist", "w"), ("eigentlich", "w"), ("ein ETF?", "box")], 0, 200, 124, w=1080, align="center")
      + chart([(0, 0.05), (0.2, 0.2), (0.35, 0.14), (0.55, 0.45), (0.7, 0.4), (0.75, 0.7), (0.85, 0.95)], 90, 1000, 900, 520, GRUEN,
              pills=[(6, "≈ 7 % / Jahr")])
      + korb(170, 920, 740)
      + f'<div style="position:absolute;left:110px;top:800px;font-weight:900;font-size:220px;color:{ROT};text-shadow:0 0 60px {ROT}aa;transform:rotate(-12deg);z-index:3">?</div>'
      + pill(180, 1620, "1.000+ Firmen in 1 Korb", OR, 58))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "60%"))
