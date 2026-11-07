#!/usr/bin/env python3
"""TikTok-Cover (1080×1920) für deutschlandticket-2027 – Dark Glow."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, pill, seite, titel  # noqa: E402

ROT = "#ff4d4d"
TICKET = (f'<div style="position:absolute;left:140px;top:740px;width:800px;height:500px;border-radius:44px;background:linear-gradient(135deg,#23282c,#16191b);'
          f'border:10px solid {OR};box-shadow:0 0 100px {OR}77;overflow:hidden;transform:rotate(-5deg);z-index:2">'
          f'<div style="height:120px;background:{OR};font-weight:900;font-size:56px;color:#111;padding:28px 50px">DEUTSCHLANDTICKET</div>'
          f'<div style="position:absolute;right:50px;bottom:60px;font-weight:900;font-size:150px;color:#fff">66,80 €</div></div>')
TT = (titel([("Schon wieder", "w"), ("TEURER!", "box")], 0, 230, 130, w=1080, align="center")
      + TICKET + pill(600, 560, "+36 %", ROT, 100, 8)
      + '<div style="position:absolute;left:0;top:1360px;width:1080px;text-align:center;font-weight:900;font-size:70px;color:#fff">Lohnt es sich noch?</div>')

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "50%"))
