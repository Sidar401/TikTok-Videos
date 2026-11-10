#!/usr/bin/env python3
"""TikTok-Cover nvidia-im-etf – Dark Glow, Raster 100 € mit 6 Nvidia-Feldern."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import pill, seite, titel  # noqa: E402

NV = "#76b900"
Q = "".join(f'<div style="position:absolute;left:{190 + (i % 10) * 72}px;top:{880 + (i // 10) * 72}px;width:60px;height:60px;border-radius:12px;'
            f'background:{NV if i < 6 else "#3a4248"};box-shadow:{"0 0 24px " + NV if i < 6 else "none"}"></div>' for i in range(100))
LOGO = ('<div style="position:absolute;left:250px;top:400px;width:580px;height:170px;border-radius:30px;background:#fff;padding:26px 50px;display:flex;align-items:center;'
        f'justify-content:center;box-shadow:0 0 90px {NV}88;transform:rotate(-3deg);z-index:3"><img src="assets/nvidia.svg" style="max-width:100%;max-height:100%"/></div>')
TT = (titel([("Steckt", "w")], 0, 220, 130, w=1080, align="center") + titel([("in deinem ETF?", "box")], 0, 640, 110, w=1080, align="center") + LOGO + Q
      + pill(420, 1640, "≈ 6 € von 100 €", NV, 60, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
