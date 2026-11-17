#!/usr/bin/env python3
"""TikTok-Cover longform-ki-woche – Wochen-Kalender MO/DI/DO (Absturz · Nvidia · Anthropic), „Boom oder Blase?“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402


def tag(x, y, kurz, inhalt, farbe, dreh):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:300px;height:360px;border-radius:30px;background:#14181b;border:8px solid {farbe};'
            f'box-shadow:0 0 70px {farbe}88, 0 30px 40px #000;transform:rotate({dreh}deg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;z-index:3">'
            f'<div style="font-weight:900;font-size:120px;color:{farbe}">{kurz}</div>{inhalt}</div>')


MO = tag(50, 640, "MO", '<div style="font-size:110px">📉</div>', "#ff4d4d", -5)
DI = tag(390, 610, "DI", '<div style="background:#fff;border-radius:14px;padding:12px"><img src="assets/nvidia.svg" style="width:220px;display:block"/></div>', "#76b900", 0)
DO = tag(730, 640, "DO", '<div style="background:#fff;border-radius:14px;padding:16px"><img src="assets/anthropic.svg" style="width:220px;display:block"/></div>', "#d97757", 5)
TT = (titel([("Die Woche", "w"), ("der Wahrheit", "rot")], 0, 220, 124, w=1080, align="center") + MO + DI + DO
      + pill(130, 1200, "Boom oder Blase?", OR, 80, -3) + pill(300, 1420, "für deinen ETF", "#2ecc71", 66, 2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
