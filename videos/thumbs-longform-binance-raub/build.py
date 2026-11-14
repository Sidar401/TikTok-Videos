#!/usr/bin/env python3
"""Thumbnails longform-binance-raub – Dark Glow: Handy-Mockup mit Jobangebot (neues Motiv), Binance-Logo, 6,3 Mrd. $ rot, Nordkorea-Flagge.
python3 build.py         → 16:9 (3 Varianten)   python3 build.py tiktok → 9:16"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

BN = "#F3BA2F"


def handy(x, y, s=1.0, dreh=-6):
    w, h = int(380 * s), int(760 * s)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{int(56*s)}px;background:#0b0d0e;border:{int(10*s)}px solid #2a2f33;'
            f'box-shadow:0 0 90px {OR}55, 0 40px 60px #000;transform:rotate({dreh}deg);z-index:2;overflow:hidden">'
            f'<div style="margin:{int(60*s)}px {int(22*s)}px 0;padding:{int(22*s)}px;border-radius:{int(24*s)}px;background:#fff;color:#111;font-weight:900;font-size:{int(34*s)}px;line-height:1.15">'
            f'💼 Neues Jobangebot<div style="font-weight:600;font-size:{int(24*s)}px;color:#555;margin-top:{int(10*s)}px">„Lade bitte diese Probeaufgabe herunter …“</div></div>'
            f'<div style="margin:{int(26*s)}px {int(22*s)}px 0;padding:{int(22*s)}px;border-radius:{int(20*s)}px;background:#1b1f22;border:{int(3*s)}px solid {ROT};color:#fff;'
            f'font-weight:900;font-size:{int(32*s)}px;text-align:center">📁 aufgabe.zip</div>'
            f'<div style="text-align:center;font-size:{int(150*s)}px;margin-top:{int(30*s)}px">☠️</div></div>')


def logo(x, y, w):
    return f'<img src="assets/binance.png" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;filter:drop-shadow(0 0 30px {BN}aa);z-index:3"/>'


def flagge(x, y, w, dreh=6):
    return (f'<img src="assets/flagge-nordkorea.svg" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:10px;transform:rotate({dreh}deg);'
            f'box-shadow:0 20px 40px #000;z-index:3"/>')


V1 = (titel([("Der größte", "w"), ("KRYPTO-RAUB", "rot")], 80, 120, 120, w=1000) + handy(1240, 170, 1.05, 6) + logo(90, 560, 520)
      + titel([("6,3 Mrd. $", "r")], 80, 700, 170) + pill(90, 930, "in 20 Minuten gestohlen", OR, 54, -2))
V2 = (titel([("Ein Jobangebot …", "w"), ("6,3 Mrd. $ WEG", "box")], 80, 150, 110, w=1100) + handy(1290, 170, 1.05, 5) + flagge(110, 640, 300, -5)
      + pill(470, 700, "Spur nach Nordkorea", ROT, 56, -2))
V3 = (titel([("So stahlen Hacker", "w"), ("6,3 MILLIARDEN", "rot")], 80, 160, 112, w=1150) + handy(1300, 160, 1.05, 6) + logo(100, 640, 460)
      + pill(100, 850, "Rekord: 4× größer als je zuvor", OR, 54, -2))
TT = (titel([("Der größte", "w"), ("KRYPTO-RAUB", "rot")], 0, 200, 112, w=1080, align="center") + handy(330, 560, 1.12, -5) + logo(200, 1450, 680)
      + titel([("6,3 Mrd. $", "r")], 0, 1560, 150, w=1080, align="center"))

if __name__ == "__main__":
    if "tiktok" in sys.argv:
        seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
    else:
        seite(HERE, [V1, V2, V3], glow=("70%", "50%"))
