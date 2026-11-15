#!/usr/bin/env python3
"""TikTok-Cover klarna-ab-freitag – Klarna + PayPal-Logo, Knopf „Später bezahlen“ mit Stempel ABGELEHNT, Kalender 20.11."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, pill, seite, titel  # noqa: E402

KL = '<img src="assets/klarna.png" style="position:absolute;left:90px;top:600px;width:440px;transform:rotate(-5deg);filter:drop-shadow(0 0 60px #ffa8cdaa) drop-shadow(0 30px 40px #000);z-index:2"/>'
PP = ('<div style="position:absolute;left:580px;top:640px;width:420px;padding:26px;border-radius:26px;background:#fff;transform:rotate(5deg);'
      'box-shadow:0 0 60px #0070e088, 0 30px 40px #000;z-index:2"><img src="assets/paypal.png" style="width:100%;display:block"/></div>')
KNOPF = ('<div style="position:absolute;left:190px;top:1010px;width:700px;padding:36px 0;border-radius:80px;background:#ffa8cd;text-align:center;font-weight:900;'
         'font-size:74px;color:#111;box-shadow:0 0 70px #ffa8cd99;z-index:2">Später bezahlen</div>')
STEMPEL = ('<div style="position:absolute;left:160px;top:1180px;padding:14px 40px;border:12px solid #ff4d4d;border-radius:22px;color:#ff4d4d;font-weight:900;'
           'font-size:108px;letter-spacing:4px;transform:rotate(-9deg);background:#0e1012cc;text-shadow:0 0 40px #ff4d4d;box-shadow:0 0 40px #ff4d4d88;z-index:4">ABGELEHNT</div>')
TT = (titel([("Ab Freitag", "w"), ("neue Regeln!", "box")], 0, 220, 124, w=1080, align="center") + KL + PP + KNOPF + STEMPEL
      + pill(330, 1580, "ab 20.11.", ROT, 80, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
