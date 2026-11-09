#!/usr/bin/env python3
"""Cover 9:16 für fruehstart-rente."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, pill, seite, titel  # noqa: E402

TT = (titel([("Der Staat zahlt", "w"), ("deinem KIND", "box")], 0, 200, 110, w=1080, align="center")
      + f'<div style="position:absolute;left:0;top:640px;width:1080px;text-align:center;font-weight:900;font-size:240px;color:#fff">10 €</div>'
      + '<div style="position:absolute;left:0;top:900px;width:1080px;text-align:center;font-size:120px;font-weight:900;color:#ff8a1f">↓</div>'
      + f'<div style="position:absolute;left:0;top:1060px;width:1080px;text-align:center;font-weight:900;font-size:200px;color:{GRUEN};text-shadow:0 0 70px {GRUEN}aa">30.000 €</div>'
      + pill(330, 1340, "Frühstart-Rente", OR, 70, -3))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "55%"))
