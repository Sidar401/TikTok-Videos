#!/usr/bin/env python3
"""TikTok-Cover geldautomaten-gratis – gezeichneter Geldautomat mit roter Gebühr, Stempel „ABZOCKE?“, Logos Rewe/Lidl, Pill 3 Wege (neues Motiv: Automat)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, pill, seite, titel  # noqa: E402

T = "".join('<div style="width:110px;height:76px;border-radius:10px;background:#3a4147;box-shadow:inset 0 -5px 0 #0006"></div>' for _ in range(9))
ATM = ('<div style="position:absolute;left:240px;top:560px;width:600px;height:820px;border-radius:40px;background:linear-gradient(180deg,#2d3338,#16191c);'
       f'border:10px solid {ROT};box-shadow:0 0 120px #ff4d4d88, 0 40px 60px #000;z-index:2;transform:rotate(-3deg)">'
       f'<div style="position:absolute;left:0;width:100%;top:34px;text-align:center;font-family:\'JetBrains Mono\',monospace;font-size:40px;color:{ROT};letter-spacing:6px">GELDAUTOMAT</div>'
       '<div style="position:absolute;left:60px;top:110px;width:480px;height:270px;border-radius:22px;background:radial-gradient(#13324a,#0a1a26);display:flex;flex-direction:column;'
       'align-items:center;justify-content:center"><div style="font-family:\'JetBrains Mono\',monospace;font-size:40px;color:#ffffffaa">Gebühr</div>'
       f'<div style="font-weight:900;font-size:150px;color:{ROT};text-shadow:0 0 40px {ROT}">6 €</div></div>'
       f'<div style="position:absolute;left:105px;top:420px;display:grid;grid-template-columns:repeat(3,110px);gap:24px">{T}</div>'
       f'<div style="position:absolute;left:110px;bottom:50px;width:380px;height:26px;border-radius:8px;background:#050607;box-shadow:0 0 24px {GRUEN}"></div></div>')
ST = (f'<div style="position:absolute;left:430px;top:470px;padding:10px 30px;border:10px solid {ROT};border-radius:20px;color:{ROT};font-weight:900;'
      'font-size:76px;letter-spacing:4px;transform:rotate(10deg);background:#0e1012dd;box-shadow:0 0 40px #ff4d4d88;z-index:4">ABZOCKE?</div>')
LG = ''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:18px;border-radius:24px;background:#fff;transform:rotate({r}deg);'
             f'box-shadow:0 0 50px #ffffff55, 0 20px 40px #000;z-index:3"><img src="assets/{f}" style="width:100%;display:block"/></div>'
             for f, x, y, w, r in (("rewe.svg", 70, 1250, 260, -6), ("lidl.svg", 820, 1200, 190, 6)))
TT = (titel([("Geldautomat weg?", "w"), ("So geht's GRATIS", "box")], 0, 200, 100, w=1080, align="center") + ATM + ST + LG
      + pill(300, 1500, "3 Wege ✓", GRUEN, 80, -2))

if __name__ == "__main__":
    seite(HERE, [TT], tiktok=True, glow=("50%", "45%"))
