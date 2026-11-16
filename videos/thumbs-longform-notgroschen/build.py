#!/usr/bin/env python3
"""TikTok-Cover longform-notgroschen – fast leeres Spar-Glas (rot), „3 Monate“, Pille „Jeder 2. betroffen“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402

GLAS = ('<div style="position:absolute;left:300px;top:640px;width:480px;height:640px;border:14px solid #ffffffdd;border-top:none;border-radius:0 0 90px 90px;overflow:hidden;'
        'background:#ffffff0d;box-shadow:0 0 90px #ff4d4d55;z-index:2"><div style="position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(180deg,#ff4d4d,#ff4d4d99)"></div>'
        '<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;color:#fff;text-shadow:0 6px 0 #000">'
        '<div style="font-size:190px;line-height:1">3</div><div style="font-size:84px">Monate</div></div></div>'
        '<div style="position:absolute;left:276px;top:596px;width:528px;height:56px;border-radius:18px;background:#c9a46b;box-shadow:0 12px 24px #000;z-index:3"></div>')
TT = (titel([("Dein Notgroschen", "w"), ("reicht nicht!", "rot")], 0, 220, 100, w=1080, align="center") + GLAS
      + pill(200, 1380, "Jeder 2. betroffen", ROT, 80, -3) + pill(240, 1580, "So viel brauchst du", GRUEN, 66, 2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
