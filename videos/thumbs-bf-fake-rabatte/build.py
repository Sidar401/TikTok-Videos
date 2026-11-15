#!/usr/bin/env python3
"""TikTok-Cover bf-fake-rabatte – Preisschild mit durchgestrichener UVP, „−34 %“ → Stempel FAKE, Pille „3 Tricks“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402

SCHILD = ('<div style="position:absolute;left:170px;top:640px;width:740px;padding:40px;border-radius:34px;background:#14181b;border:8px solid #ff4d4d;'
          'box-shadow:0 0 90px #ff4d4d88, 0 40px 60px #000;text-align:center;transform:rotate(-3deg);z-index:2">'
          '<div style="font-family:monospace;font-size:90px;color:#9aa0a6;text-decoration:line-through;text-decoration-color:#ff4d4d;text-decoration-thickness:10px">450 €</div>'
          '<div style="font-weight:900;font-size:210px;color:#fff;line-height:1;text-shadow:0 0 50px #ff4d4d">299 €</div></div>')
ICON = '<div style="position:absolute;left:760px;top:520px;font-size:200px;transform:rotate(12deg);z-index:3">🛍️</div>'
STEMPEL = ('<div style="position:absolute;left:250px;top:1130px;padding:14px 50px;border:12px solid #ff4d4d;border-radius:22px;color:#ff4d4d;font-weight:900;'
           'font-size:150px;letter-spacing:8px;transform:rotate(-10deg);text-shadow:0 0 40px #ff4d4d;box-shadow:0 0 40px #ff4d4d88;z-index:4">FAKE?</div>')
TT = (titel([("Black Friday", "w"), ("Fake-Rabatte", "rot")], 0, 220, 120, w=1080, align="center") + SCHILD + ICON + STEMPEL
      + pill(250, 1520, "3 Tricks erkennen", GRUEN, 74, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
