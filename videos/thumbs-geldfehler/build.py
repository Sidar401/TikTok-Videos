#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-geldfehler. Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from icons import GELDBEUTEL  # noqa: E402
from longform import ORANGE, ROT  # noqa: E402

POSTEN = [("Abos", "360 €"), ("Coffee to go", "720 €"), ("Verträge", "400 €"), ("Lieferdienst", "1.700 €"), ("Zu viel Auto", "1.800 €")]


def zettel(w, fs):
    rows = "".join(f'<div style="display:flex;justify-content:space-between;padding:6px 0"><span>{a}</span><b style="color:#111">{b}</b></div>' for a, b in POSTEN)
    return (f'<div style="width:{w}px;background:#faf5ef;border-radius:30px;padding:34px 46px;font-weight:700;font-size:{fs}px;color:#353a3d;transform:rotate(3deg);box-shadow:0 14px 0 #e8dccb">'
            f'<div style="font-weight:800;color:{ORANGE};border-bottom:4px dashed #d9cbb8;padding-bottom:10px;margin-bottom:8px">Deine Geldfehler</div>{rows}'
            f'<div style="display:flex;justify-content:space-between;align-items:center;border-top:5px solid #353a3d;margin-top:14px;padding-top:14px">'
            f'<span style="font-weight:800;color:#111">pro Jahr</span><span class="serif" style="font-size:{fs * 2:.0f}px;color:{ROT}">−5.800 €</span></div></div>')


V1 = f"""
  <div style="position:absolute;left:80px;top:200px;width:960px">
    <div class="serif" style="font-size:124px;line-height:1.02;color:{ROT};white-space:nowrap">10 Geldfehler</div>
    <div style="font-weight:900;font-size:80px;color:#111;margin-top:16px">die dich</div>
    <div style="display:inline-block;margin-top:14px;padding:14px 50px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:110px">ARM</div>
    <div style="display:inline-block;font-weight:900;font-size:80px;color:#111;margin-left:24px">halten</div>
  </div>
  <div style="position:absolute;left:1060px;top:170px">{zettel(740, 44)}</div>
"""

V2 = f"""
  <div style="position:absolute;left:150px;top:190px;width:640px;height:640px;border-radius:50%;background:{ROT};display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">
    <div style="font-weight:900;font-size:90px;margin-bottom:-50px">Nr.</div><div class="serif" style="font-size:440px;line-height:1">7</div></div>
  <div style="position:absolute;left:880px;top:250px;width:960px">
    <div class="serif" style="font-size:140px;line-height:1.02;color:#111">macht fast</div>
    <div style="display:inline-block;margin-top:20px;padding:14px 56px;border-radius:34px;background:{ORANGE};color:#fff;font-weight:900;font-size:150px;transform:rotate(-3deg)">JEDER</div>
  </div>
"""

V3 = f"""
  <div style="position:absolute;left:90px;top:240px;width:560px;height:560px;transform:rotate(-8deg)">{GELDBEUTEL}</div>
  <div style="position:absolute;left:700px;top:230px;width:1140px;text-align:center">
    <div class="serif" style="font-size:200px;line-height:1;color:{ROT};white-space:nowrap">−58.000&nbsp;€</div>
    <div style="font-weight:900;font-size:86px;color:#111;margin-top:24px">durch diese 10 Fehler</div>
    <div style="display:inline-block;margin-top:36px;padding:14px 46px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:64px">machst du sie auch?</div>
  </div>
"""

TIKTOK = f"""
  <div style="position:absolute;left:0;top:270px;width:1080px;text-align:center">
    <div class="serif" style="font-size:130px;line-height:1.02;color:{ROT}">10 Geldfehler</div>
    <div style="font-weight:900;font-size:76px;color:#111;margin-top:18px">die dich <span style="display:inline-block;padding:8px 40px;border-radius:26px;background:{ORANGE};color:#fff;font-size:96px">ARM</span> halten</div>
  </div>
  <div style="position:absolute;left:140px;top:820px">{zettel(800, 46)}</div>
"""

tiktok = len(sys.argv) > 1 and sys.argv[1] == "tiktok"
W, H, rand = (1080, 1920, 26) if tiktok else (1920, 1080, 30)
inhalt = [TIKTOK] if tiktok else [V1, V2, V3]
szenen = "\n".join(f'<div id="v{i}" class="scene clip" data-start="{i}" data-duration="1" data-track-index="1">{h}</div>' for i, h in enumerate(inhalt))
(HERE / "index.html").write_text(f"""<!doctype html>
<html lang="de" data-resolution="{"portrait" if tiktok else "landscape"}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Abril Fatface"; src: url("assets/fonts/abril-fatface.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #fff; font-family: Montserrat, sans-serif; }}
      .scene {{ position: absolute; inset: 0; }}
      .serif {{ font-family: "Abril Fatface", serif; }}
      #frame {{ position: absolute; inset: 0; border: {rand}px solid #DB8622; z-index: 10; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{len(inhalt)}" data-width="{W}" data-height="{H}">
{szenen}
      <div id="frame"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#root", {{ opacity: 1 }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("gebaut:", "TikTok-Cover" if tiktok else "3 Thumbnails")
