#!/usr/bin/env python3
"""Thumbnail (1920×1080, YouTube) + Cover (1080×1920, TikTok/Instagram) für longform-freiheit – Stil „Dark Glow“.
Aufruf: python3 build.py | python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, buendel, muenzen, seite, titel  # noqa: E402

NIE = f'<span style="display:inline-block;padding:0 22px 6px;border-radius:18px;background:{OR};color:#111;text-shadow:none;box-shadow:0 0 50px {OR}88">NIE</span>'


def berg(x, y, w):
    h = w * 0.82
    kontur = "M0 820 L240 380 L370 560 L560 110 L1000 820"
    return (f'<svg viewBox="0 0 1000 820" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:2">'
            f'<defs><linearGradient id="bf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OR}" stop-opacity="0.6"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></linearGradient>'
            f'<filter id="bg" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<path d="{kontur} Z" fill="url(#bf)"/>'
            f'<path d="M500 250 L560 110 L640 255 L600 230 L570 270 L540 235 Z" fill="#fff" opacity="0.9"/>'
            f'<path d="{kontur}" fill="none" stroke="{OR}" stroke-width="30" stroke-linejoin="round" opacity="0.7" filter="url(#bg)"/>'
            f'<path d="{kontur}" fill="none" stroke="{OR}" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{kontur}" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" opacity="0.6"/>'
            f'<path d="M150 820 L240 650 L330 720 L430 560 L520 640" fill="none" stroke="#ffffff55" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round"/>'
            f'<line x1="560" y1="110" x2="560" y2="-60" stroke="#fff" stroke-width="10"/>'
            f'<path d="M565 -60 L760 -20 L565 20 Z" fill="{OR}" filter="drop-shadow(0 0 20px {OR})"/>'
            f'<text x="635" y="-8" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="46" fill="#111">FREI</text></svg>')


YT = (berg(60, 200, 880) + muenzen(830, 800, 5, 130)
      + titel([("So viel Geld,", "w"), (f"um {NIE} wieder", "w"), ("zu arbeiten", "w")], 990, 300, 104))

TT = (titel([("So viel Geld,", "w"), (f"um {NIE} wieder", "w"), ("zu arbeiten", "w")], 0, 220, 108, w=1080, align="center")
      + berg(130, 860, 820) + muenzen(830, 1360, 6, 150) + buendel(60, 1440, 0.8, 4))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [YT], tiktok=tiktok, glow=("35%", "55%"))
