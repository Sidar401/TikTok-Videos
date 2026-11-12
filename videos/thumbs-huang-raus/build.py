#!/usr/bin/env python3
"""TikTok-Cover longform-huang-raus – Dark Glow, echtes Foto (CC BY 4.0, Peter Dasilva) + RAUS-Stempel."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, pill, seite, titel  # noqa: E402

NV = "#76b900"
FOTO = (f'<div style="position:absolute;left:240px;top:620px;width:600px;height:600px;border-radius:50%;overflow:hidden;border:14px solid {NV};box-shadow:0 0 120px {NV}88;z-index:2">'
        '<img src="assets/jensen-huang.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 15%"/></div>'
        '<div style="position:absolute;left:0;top:1600px;width:1080px;text-align:center;font-family:monospace;font-size:24px;color:#ffffff88;z-index:3">Foto: Peter Dasilva · CC BY 4.0</div>')
STEMPEL = (f'<div style="position:absolute;left:300px;top:1000px;padding:10px 50px;border:14px solid {ROT};border-radius:22px;color:{ROT};font-weight:900;font-size:170px;'
           f'letter-spacing:6px;transform:rotate(-10deg);background:#0e1012dd;box-shadow:0 0 60px {ROT}88;z-index:4">RAUS!</div>')
LOGO = ('<div style="position:absolute;left:290px;top:490px;width:500px;height:120px;border-radius:26px;background:#fff;padding:20px 44px;display:flex;align-items:center;justify-content:center;'
        f'box-shadow:0 0 80px {NV}88;z-index:3"><img src="assets/nvidia.svg" style="max-width:100%;max-height:100%"/></div>')
TT = (titel([("Nvidia-Chef", "w"), ("Jensen Huang", "box")], 0, 170, 110, w=1080, align="center") + LOGO + FOTO + STEMPEL
      + pill(170, 1330, "Was heißt das für deinen ETF?", "#ff8a1f", 50, -3) + pill(340, 1460, "Aktie −13 %", ROT, 64, 3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
