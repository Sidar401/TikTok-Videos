#!/usr/bin/env python3
"""TikTok-Cover dticket-zustimmung – DB-Logo, Ticket-Karte mit Stempel ABO WEG, Pille „bis 30.11. zustimmen“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import ROT, pill, seite, titel  # noqa: E402

DB = '<img src="assets/db.svg" style="position:absolute;left:720px;top:560px;width:260px;transform:rotate(8deg);filter:drop-shadow(0 0 50px #f01414aa) drop-shadow(0 20px 30px #000);z-index:3"/>'
TICKET = ('<div style="position:absolute;left:160px;top:720px;width:780px;height:450px;border-radius:36px;transform:rotate(4deg);'
          'background:linear-gradient(135deg,#e8eef2,#c9d3da);box-shadow:0 0 90px #ff8a1f88, 0 40px 60px #000;z-index:2;overflow:hidden">'
          '<div style="position:absolute;left:0;top:0;width:100%;height:27%;background:#f01414"></div>'
          '<div style="position:absolute;left:44px;top:26px;font-weight:900;font-size:54px;color:#fff;white-space:nowrap">DEUTSCHLAND-TICKET</div>'
          '<div style="position:absolute;left:44px;bottom:34px;font-weight:900;font-size:120px;color:#111">66,80 €</div></div>')
STEMPEL = ('<div style="position:absolute;left:150px;top:1190px;padding:14px 40px;border:12px solid #ff4d4d;border-radius:22px;color:#ff4d4d;font-weight:900;'
           'font-size:112px;letter-spacing:4px;transform:rotate(-8deg);background:#0e1012cc;text-shadow:0 0 40px #ff4d4d;box-shadow:0 0 40px #ff4d4d88;z-index:4">ABO WEG?</div>')
TT = (titel([("Bahn-Kunden", "w"), ("aufgepasst!", "box")], 0, 220, 124, w=1080, align="center") + DB + TICKET + STEMPEL
      + pill(150, 1580, "bis 30.11. zustimmen", ROT, 66, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
