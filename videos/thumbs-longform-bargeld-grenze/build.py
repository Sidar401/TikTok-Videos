#!/usr/bin/env python3
"""Thumbnails longform-bargeld-grenze – Geldschein-Stapel über roter 10.000-€-Linie, EU-Flagge, „ab 2027“.
python3 build.py → 16:9 (3 Varianten)   python3 build.py tiktok → 9:16"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402


def stapel(x, y, w=380, h=520):
    sch = "".join(f'<div style="position:absolute;left:0;right:0;bottom:{i * 20}px;height:17px;border-radius:4px;background:{"#2ecc71" if i % 2 else "#27ae60"};'
                  f'border-top:3px solid #a7f3c1"></div>' for i in range(h // 20))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;filter:drop-shadow(0 0 50px #2ecc7188) drop-shadow(0 30px 40px #000);z-index:2">{sch}</div>'
            f'<div style="position:absolute;left:{x - 80}px;top:{y + int(h * 0.3)}px;width:{w + 160}px;border-top:14px dashed #ff4d4d;filter:drop-shadow(0 0 16px #ff4d4d);z-index:3"></div>'
            f'<div style="position:absolute;left:{x + w + 30}px;top:{y + int(h * 0.3) - 80}px;font-weight:900;font-size:70px;color:#ff4d4d;text-shadow:0 0 30px #ff4d4d;z-index:3">10.000 €</div>')


def eu(x, y, w, dreh=-6):
    return f'<img src="assets/flagge-eu.svg" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:12px;transform:rotate({dreh}deg);box-shadow:0 20px 40px #000;z-index:3"/>'


V1 = (titel([("Bargeld-Grenze", "w"), ("ab 2027!", "rot")], 80, 150, 120, w=1100) + stapel(1180, 300, 300) + eu(90, 600, 300)
      + pill(450, 680, "Was jetzt verboten ist", OR, 56, -2))
V2 = (titel([("Nur noch", "w"), ("10.000 € bar?", "box")], 80, 170, 130, w=1000) + stapel(1180, 300, 300) + eu(100, 620, 280, 5)
      + pill(430, 700, "Die EU-Regel erklärt", OR, 56, -2))
V3 = (titel([("Wird Bargeld", "w"), ("abgeschafft?", "rot")], 80, 160, 130, w=1000) + stapel(1180, 300, 300) + eu(90, 630, 300)
      + pill(450, 700, "Die Wahrheit", GRUEN, 60, -2))
TT = (titel([("Bargeld-Grenze", "w"), ("ab 2027!", "rot")], 0, 220, 120, w=1080, align="center") + eu(90, 580, 300, -6) + stapel(330, 660, 300, 560)
      + pill(110, 1460, "Nur noch 10.000 € bar?", OR, 64, -2))

if __name__ == "__main__":
    if "tiktok" in sys.argv:
        seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
    else:
        seite(HERE, [V1, V2, V3], glow=("70%", "50%"))
