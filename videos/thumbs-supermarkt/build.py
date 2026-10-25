#!/usr/bin/env python3
"""Thumbnail (1920×1080, YouTube) + Cover (1080×1920, TikTok/Instagram) für longform-supermarkt – Stil „Dark Glow“.
Aufruf: python3 build.py | python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, seite, titel  # noqa: E402

WAREN = [(150, 70, 80, 100, "#ffc533", -8), (225, 62, 90, 105, ROT, 4), (305, 66, 80, 100, "#2c9a63", -10), (375, 60, 85, 100, "#4d8ff0", 3),
         (440, 92, 80, 92, "#b36bdb", 6), (165, 145, 92, 80, ROT, -6), (245, 150, 80, 80, GRUEN, 0), (310, 150, 75, 80, OR, 8),
         (380, 150, 80, 80, "#4d8ff0", -3)]


def wagen(x, y, w):
    ware = "".join(f'<g transform="rotate({r} {bx + bw / 2} {by + bh / 2})"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{c}"/>'
                   f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh * 0.35}" rx="10" fill="#ffffff33"/><rect x="{bx + bw * 0.2}" y="{by + bh * 0.5}" width="{bw * 0.6}" height="{bh * 0.18}" rx="4" fill="#ffffffcc"/></g>'
                   for bx, by, bw, bh, c, r in WAREN)
    korb = "M20 40 L95 40 L150 300 L470 300 L530 150 L118 150"
    return (f'<svg viewBox="0 0 560 420" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w * 0.75}px;overflow:visible;z-index:2">'
            f'<defs><filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="12"/></filter></defs>'
            f'{ware}'
            f'<path d="{korb}" fill="none" stroke="{OR}" stroke-width="34" stroke-linejoin="round" stroke-linecap="round" opacity="0.7" filter="url(#gl)"/>'
            f'<path d="M128 195 L505 195 M138 245 L488 245" stroke="{OR}" stroke-width="8" opacity="0.5"/>'
            f'<path d="{korb}" fill="none" stroke="{OR}" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{korb}" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" opacity="0.5"/>'
            f'<circle cx="190" cy="370" r="34" fill="#16191b" stroke="{OR}" stroke-width="14"/><circle cx="430" cy="370" r="34" fill="#16191b" stroke="{OR}" stroke-width="14"/></svg>')


def preis(x, y, text, dreh=-8, gr=60):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;padding:10px 34px 14px 54px;background:#ffc533;color:#111;font-weight:900;font-size:{gr}px;white-space:nowrap;'
            f'clip-path:polygon(28px 0,100% 0,100% 100%,28px 100%,0 50%);transform:rotate({dreh}deg);filter:drop-shadow(0 0 20px #ffc53399);z-index:3">{text}</div>')


YT = (wagen(40, 340, 720) + preis(470, 250, "nur 0,99 €?", -10)
      + titel([("Der Supermarkt", "w"), ("TRICKST", "rot"), ("dich aus!", "w")], 790, 330, 114))

TT = (titel([("Der Supermarkt", "w"), ("TRICKST", "rot"), ("dich aus!", "w")], 0, 220, 120, w=1080, align="center")
      + wagen(140, 960, 800) + preis(600, 880, "nur 0,99 €?", -10, 56))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [YT], tiktok=tiktok, glow=("30%", "50%"))
