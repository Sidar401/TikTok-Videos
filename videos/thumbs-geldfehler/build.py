#!/usr/bin/env python3
"""Thumbnail (1920×1080, YouTube) + Cover (1080×1920, TikTok/Instagram) für longform-geldfehler – Stil „Dark Glow“.
Aufruf: python3 build.py | python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, buendel, chart, muenzen, pill, seite, titel  # noqa: E402

FALL = [(0, 0.95), (0.15, 0.78), (0.3, 0.7), (0.45, 0.5), (0.6, 0.45), (0.75, 0.22), (0.9, 0.05)]

YT = (titel([("−58.000 €", "r"), ("durch diese", "w"), ("10 FEHLER", "box")], 90, 90, 165)
      + pill(90, 760, "machst du sie auch?", OR, 64)
      + chart(FALL, 1150, 420, 700, 480, ROT, pills=[(1, "Abos"), (3, "Auto"), (5, "Lieferdienst")])
      + buendel(1430, 40, 0.8, 4) + muenzen(1690, 90, 6, 140))

POSTEN = [("Abos", "360 €"), ("Coffee to go", "720 €"), ("Verträge", "400 €"), ("Lieferdienst", "1.700 €"), ("Zu viel Auto", "1.800 €")]
ZEILEN = "".join(f'<div style="display:flex;justify-content:space-between;font-weight:800;font-size:52px;color:#fff"><span style="color:#cfd6db">{a}</span><span>{b}</span></div>'
                 for a, b in POSTEN)
TT = (titel([("10 GELDFEHLER", "o"), ("die dich", "w"), ("ARM halten", "box")], 0, 250, 112, w=1080, align="center")
      + f'''<div style="position:absolute;left:110px;top:820px;width:860px;padding:46px 54px;border-radius:44px;background:#16191b;border:4px solid {OR};
             box-shadow:0 0 80px {OR}66, 0 30px 60px #000;transform:rotate(-2deg);display:flex;flex-direction:column;gap:18px;z-index:2">
          <div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:3px">DEINE GELDFEHLER</div>{ZEILEN}
          <div style="height:5px;background:#ffffff55;margin:10px 0"></div>
          <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:800;font-size:52px;color:#fff">pro Jahr</span>
          <span style="font-weight:900;font-size:100px;white-space:nowrap;color:{ROT};text-shadow:0 0 50px {ROT}aa">−5.800 €</span></div></div>'''
      + muenzen(820, 660, 5, 150))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [YT], tiktok=tiktok)
