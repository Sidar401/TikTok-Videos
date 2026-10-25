#!/usr/bin/env python3
"""TikTok/Instagram-Cover (1080×1920) für auto-kosten – Stil „Dark Glow“. Aufruf: python3 build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402


def auto(x, y, w):
    k = "M40 300 L40 230 Q40 200 80 195 L170 190 L250 90 Q265 70 300 70 L560 70 Q600 70 625 95 L720 190 L800 200 Q840 205 840 240 L840 300 Z"
    return (f'<svg viewBox="0 0 880 420" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w * 0.477}px;overflow:visible;z-index:2">'
            f'<defs><filter id="ag" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>'
            f'<linearGradient id="af" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6b5e"/><stop offset="1" stop-color="#b8241c"/></linearGradient></defs>'
            f'<path d="{k}" fill="url(#af)"/>'
            f'<path d="M275 100 L410 100 L410 190 L205 190 Z M440 100 L570 100 Q590 100 605 115 L680 190 L440 190 Z" fill="#cfe6f5" opacity="0.85"/>'
            f'<path d="{k}" fill="none" stroke="{ROT}" stroke-width="30" stroke-linejoin="round" opacity="0.6" filter="url(#ag)"/>'
            f'<path d="{k}" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round" opacity="0.5"/>'
            f'<rect x="790" y="225" width="40" height="22" rx="8" fill="#ffc533"/>'
            + "".join(f'<circle cx="{cx}" cy="305" r="72" fill="#16191b" stroke="#353a3d" stroke-width="10"/><circle cx="{cx}" cy="305" r="30" fill="#9aa3a8"/>' for cx in (210, 670))
            + '</svg>')


KOSTEN = [(70, 1010, "Versicherung", -6), (620, 980, "Steuer", 5), (90, 1520, "Werkstatt", 4), (430, 1560, "Reifen", -5), (690, 1490, "Wertverlust", 6)]

TT = (titel([("Dein Auto", "w"), ("kostet dich", "w"), ("MEHR", "rot"), ("als du denkst", "w")], 0, 160, 112, w=1080, align="center")
      + auto(100, 1110, 880)
      + "".join(pill(x, y, t, "#2a2f33", 46, d).replace("color:#fff", f"color:{ROT};border:3px solid {ROT}") for x, y, t, d in KOSTEN)
      + f'<div style="position:absolute;left:720px;top:730px;font-weight:900;font-size:150px;color:{ROT};text-shadow:0 0 60px {ROT}aa;transform:rotate(10deg);z-index:3">?€</div>'
      + pill(220, 1700, "≈ 5.000 € pro Jahr", OR, 64))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "62%"))
