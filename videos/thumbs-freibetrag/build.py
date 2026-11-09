#!/usr/bin/env python3
"""Cover 9:16 für lohnsteuer-freibetrag."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, pill, seite, titel  # noqa: E402

TT = (titel([("Jeden Monat", "w"), ("MEHR NETTO", "box")], 0, 220, 120, w=1080, align="center")
      + f'<div style="position:absolute;left:0;top:720px;width:1080px;text-align:center;font-weight:900;font-size:260px;color:{GRUEN};text-shadow:0 0 70px {GRUEN}aa">+30 €</div>'
      + '<div style="position:absolute;left:0;top:1030px;width:1080px;text-align:center;font-weight:900;font-size:72px;color:#fff">für Pendler</div>'
      + pill(150, 1250, "Lohnsteuer-Freibetrag", OR, 62, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
