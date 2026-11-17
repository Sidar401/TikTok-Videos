#!/usr/bin/env python3
"""TikTok-Cover nvidia-heute-nacht – Nvidia-Logo, Uhr 22:20, Crash-Linie, „Alles oder nichts?“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, chart, pill, seite, titel  # noqa: E402

LOGO = ('<div style="position:absolute;left:190px;top:600px;width:700px;padding:40px;border-radius:34px;background:#fff;box-shadow:0 0 90px #76b900aa, 0 30px 50px #000;z-index:2">'
        '<img src="assets/nvidia.svg" style="width:100%;display:block"/></div>')
UHR = ('<div style="position:absolute;left:250px;top:860px;width:580px;padding:20px;border-radius:28px;background:#000;border:10px solid #76b900;text-align:center;'
       'font-family:monospace;font-weight:900;font-size:170px;color:#76b900;text-shadow:0 0 40px #76b900;box-shadow:0 0 80px #76b90088;transform:rotate(-3deg);z-index:3">22:20</div>')
K = [(0, 0.9), (0.2, 0.75), (0.45, 0.8), (0.7, 0.4), (1, 0.15)]
TT = (titel([("Die Börse zittert", "w"), ("Heute Nacht!", "rot")], 0, 220, 108, w=1080, align="center") + LOGO + UHR
      + chart(K, 110, 1170, 860, 300, ROT, fill=True) + pill(150, 1150, "−32 %", ROT, 70, -4)
      + pill(260, 1560, "Alles oder nichts?", OR, 70, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
