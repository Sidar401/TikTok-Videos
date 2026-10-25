#!/usr/bin/env python3
"""Thumbnail (1920×1080, YouTube) + Cover (1080×1920, TikTok/Instagram) für longform-zwei-leben – Stil „Dark Glow“.
Aufruf: python3 build.py | python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, chart, seite, titel  # noqa: E402
from icons import person  # noqa: E402

STEIG = [(0, 0.05), (0.2, 0.18), (0.35, 0.14), (0.55, 0.45), (0.7, 0.4), (0.85, 0.7), (1, 0.97)]
FALL = [(0, 0.6), (0.2, 0.52), (0.35, 0.58), (0.55, 0.34), (0.7, 0.4), (0.85, 0.15), (1, 0.04)]


def glow(x, y, farbe, gr=900):
    return f'<div style="position:absolute;left:{x - gr / 2}px;top:{y - gr / 2}px;width:{gr}px;height:{gr}px;border-radius:50%;background:radial-gradient(circle,{farbe}33 0%,transparent 65%);z-index:0"></div>'


def avatar(x, y, farbe, haar, gr=230):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{gr}px;border-radius:50%;background:#1b1f22;border:8px solid {farbe};'
            f'box-shadow:0 0 60px {farbe}99;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;z-index:2">'
            f'<div style="width:78%;height:85%">{person(farbe, haar)}</div></div>')


def zahl(x, y, text, farbe, gr=118, w=None, align="left"):
    ww = f"width:{w}px;" if w else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{ww}text-align:{align};font-weight:900;font-size:{gr}px;line-height:1;white-space:nowrap;'
            f'color:{farbe};text-shadow:0 0 50px {farbe}aa;z-index:3">{text}</div>')


def name(x, y, text, gr=58, w=None, align="left"):
    ww = f"width:{w}px;" if w else ""
    return f'<div style="position:absolute;left:{x}px;top:{y}px;{ww}text-align:{align};font-weight:900;font-size:{gr}px;color:#fff;text-shadow:0 5px 0 #000;z-index:3">{text}</div>'


VS = (f'<div style="position:absolute;left:957px;top:220px;width:6px;height:820px;background:linear-gradient({OR}00,{OR},{OR}00);box-shadow:0 0 30px {OR};z-index:1"></div>'
      f'<div style="position:absolute;left:890px;top:520px;width:140px;height:140px;border-radius:50%;background:{OR};color:#111;font-weight:900;font-size:62px;'
      f'display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 10px #0e1012, 0 0 60px {OR};z-index:4">VS</div>')

YT = (glow(480, 600, GRUEN) + glow(1440, 600, ROT)
      + titel([("Gleiches Gehalt!", "box")], 0, 40, 100, w=1920, align="center")
      + VS
      + avatar(100, 250, GRUEN, "#353a3d") + name(370, 300, "Leon mit 40") + zahl(100, 520, "+137.000 €", GRUEN)
      + chart(STEIG, 110, 720, 760, 260, GRUEN)
      + avatar(1590, 250, ROT, "#8a5a2b") + name(1060, 300, "Felix mit 40", w=500, align="right") + zahl(1060, 520, "−8.000 €", ROT, w=760, align="right")
      + chart(FALL, 1050, 720, 760, 260, ROT))

TT = (glow(540, 480, GRUEN, 1000) + glow(540, 1450, ROT, 1000)
      + avatar(110, 230, GRUEN, "#353a3d", 250) + name(400, 280, "Leon mit 40", 64) + zahl(400, 380, "+137.000 €", GRUEN, 100)
      + chart(STEIG, 110, 560, 860, 220, GRUEN)
      + titel([("Gleiches Gehalt!", "box")], 0, 880, 104, w=1080, align="center")
      + avatar(110, 1130, ROT, "#8a5a2b", 250) + name(400, 1180, "Felix mit 40", 64) + zahl(400, 1280, "−8.000 €", ROT, 100)
      + chart(FALL, 110, 1460, 860, 220, ROT))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [YT], tiktok=tiktok, glow=("50%", "50%"))
