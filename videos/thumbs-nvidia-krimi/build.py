#!/usr/bin/env python3
"""Thumbnails longform-nvidia-krimi: 16:9 (3 Varianten) + 9:16 (Aufruf mit 'tiktok'). Dark Glow, echte Logos."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, chart, pill, seite, titel  # noqa: E402

NV = "#76b900"


def karte(bild, x, y, w, h, dreh=0, pad=26):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;background:#fff;padding:{pad}px {pad + 20}px;'
            f'box-shadow:0 0 90px {NV}88;display:flex;align-items:center;justify-content:center;transform:rotate({dreh}deg);z-index:2">'
            f'<img src="assets/{bild}.svg" style="max-width:100%;max-height:100%"/></div>')


def flagge(n, x, y, w, dreh):
    return (f'<img src="assets/{n}.svg" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:10px;outline:4px solid #ffffff55;'
            f'box-shadow:0 20px 40px #000c;transform:rotate({dreh}deg);z-index:2"/>')


FRAGE = '<div style="position:absolute;left:{x}px;top:{y}px;font-weight:900;font-size:{s}px;color:#ff4d4d;text-shadow:0 0 60px #ff4d4daa;z-index:3">?</div>'
CRASH = [(0, 0.9), (0.15, 0.82), (0.3, 0.88), (0.45, 0.7), (0.6, 0.74), (0.75, 0.4), (0.9, 0.18), (1, 0.08)]

V1 = (titel([("SPIONAGE-", "w"), ("KRIMI", "box"), ("bei Nvidia", "w")], 90, 150, 150) + karte("nvidia", 1100, 140, 640, 190, -4)
      + chart(CRASH, 1020, 430, 720, 420, ROT, pills=[(7, "−30 %")]) + flagge("flagge-china", 120, 760, 260, -6) + FRAGE.format(x=420, y=700, s=260)
      + pill(560, 880, "dein ETF betroffen?", "#ff8a1f", 64, -3))
V2 = (titel([("Nvidia-Chef", "w"), ("& die SPIONIN?", "box")], 90, 160, 130) + karte("nvidia", 1180, 160, 560, 170, 4)
      + chart(CRASH, 1000, 470, 700, 380, ROT, pills=[(7, "−250 Mrd. $")]) + flagge("flagge-usa", 110, 640, 280, -5) + flagge("flagge-china", 430, 680, 280, 6))
V3 = (titel([("−1,7 BILLIONEN $", "rot"), ("bei Nvidia", "w")], 90, 170, 140) + karte("nvidia", 1200, 520, 560, 170, -3)
      + flagge("flagge-china", 140, 600, 300, -6) + FRAGE.format(x=470, y=520, s=300) + pill(1060, 790, "Spionage-Verdacht", ROT, 64, 4))
TT = (titel([("SPIONAGE-", "w"), ("KRIMI", "box"), ("bei Nvidia", "w")], 0, 200, 130, w=1080, align="center") + karte("nvidia", 190, 760, 700, 200, -3)
      + chart(CRASH, 120, 1060, 780, 420, ROT, pills=[(7, "−30 %")]) + flagge("flagge-china", 90, 1560, 240, -6) + pill(380, 1600, "dein ETF?", "#ff8a1f", 70, -3))

if __name__ == "__main__":
    if "tiktok" in sys.argv:
        seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
    else:
        seite(HERE, [V1, V2, V3], glow=("72%", "45%"))
