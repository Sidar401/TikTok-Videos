#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-lebenskosten.
Aufruf: python3 build.py        -> index.html mit 3 Varianten (je 1 s)
        python3 build.py tiktok -> index.html als 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from icons import GELDBEUTEL, person  # noqa: E402
from longform import GRUEN, ORANGE, ROT  # noqa: E402

BEAGLE = '<img src="assets/beagle.png" style="width:100%;height:100%;object-fit:contain" />'
POSTEN = [("Miete", "1.500 €"), ("Essen", "900 €"), ("Auto", "450 €"), ("Kinder", "400 €"), ("Freizeit", "300 €")]


def zettel(w, fs):
    rows = "".join(f'<div style="display:flex;justify-content:space-between;padding:6px 0"><span>{a}</span><b style="color:#111">{b}</b></div>' for a, b in POSTEN)
    return (f'<div style="width:{w}px;background:#faf5ef;border-radius:30px;padding:36px 46px;font-weight:700;font-size:{fs}px;color:#353a3d;transform:rotate(3deg);box-shadow:0 14px 0 #e8dccb">'
            f'<div style="font-weight:800;color:{ORANGE};border-bottom:4px dashed #d9cbb8;padding-bottom:10px;margin-bottom:8px">Pro Monat</div>{rows}'
            f'<div style="display:flex;justify-content:space-between;align-items:center;border-top:5px solid #353a3d;margin-top:14px;padding-top:14px">'
            f'<span style="font-weight:800;color:#111">Summe</span><span class="serif" style="font-size:{fs * 2.1:.0f}px;color:{ROT}">4.000 €</span></div></div>')


def figuren(*leute):
    return '<div style="display:flex;align-items:flex-end;gap:8px">' + "".join(
        f'<div style="width:{w}px;height:{w * 1.35:.0f}px">{p}</div>' for p, w in leute) + "</div>"


V1 = f"""
  <div style="position:absolute;left:90px;top:190px;width:900px">
    <div class="serif" style="font-size:136px;line-height:1.02;color:#111">So viel Geld<br/>brauchst du</div>
    <div style="display:inline-block;margin-top:30px;padding:16px 44px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:92px">WIRKLICH</div>
    <div style="font-weight:900;font-size:74px;color:#353a3d;margin-top:22px">zum Leben</div>
  </div>
  <div style="position:absolute;left:1060px;top:170px">{zettel(720, 48)}</div>
  <div style="position:absolute;left:820px;bottom:50px;width:250px;height:250px">{BEAGLE}</div>
"""

grp = [(figuren((person("#3d7be0", "#353a3d"), 300)), "Single", "1.500 €", "#3d7be0"),
       (figuren((person(ORANGE, "#8a5a2b"), 230), (person(GRUEN, "#353a3d"), 230)), "Paar", "2.700 €", GRUEN),
       (figuren((person(GRUEN, "#353a3d"), 160), (person(ORANGE, "#8a5a2b"), 160), (person("#3d7be0", "#8a5a2b"), 100), (person(ORANGE, "#f2c418"), 100)), "Familie", "4.000 €", ROT)]
V2 = f"""
  <div class="serif" style="position:absolute;left:0;top:70px;width:1920px;text-align:center;font-size:120px;color:#111">Was kostet das Leben?</div>
  <div style="position:absolute;left:0;top:230px;width:1920px;display:flex;justify-content:center;gap:50px">
    {"".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:18px;width:540px"><div style="height:420px;display:flex;align-items:flex-end">{g}</div>'
             f'<div style="font-weight:900;font-size:58px;color:#353a3d">{n}</div>'
             f'<div class="serif" style="padding:8px 36px;border-radius:26px;background:{c};color:#fff;font-size:96px">{v}</div></div>' for g, n, v, c in grp)}
  </div>
"""

V3 = f"""
  <div style="position:absolute;left:110px;top:240px;width:560px;height:560px;transform:rotate(-6deg)">{GELDBEUTEL}</div>
  <div style="position:absolute;left:780px;top:230px;width:1060px">
    <div class="serif" style="font-size:150px;line-height:1.02;color:#111">Reicht dein<br/>Gehalt?</div>
    <div style="display:inline-block;margin-top:40px;padding:22px 56px;border-radius:36px;background:{ROT};color:#fff;font-weight:900;font-size:96px;transform:rotate(-3deg)">4.000 € / Monat</div>
  </div>
  <div style="position:absolute;right:80px;bottom:60px;width:260px;height:260px">{BEAGLE}</div>
"""

TIKTOK = f"""
  <div style="position:absolute;left:0;top:270px;width:1080px;text-align:center">
    <div class="serif" style="font-size:118px;line-height:1.02;color:#111">So viel Geld<br/>brauchst du</div>
    <div style="display:inline-block;margin-top:26px;padding:14px 44px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:86px">WIRKLICH</div>
    <div style="font-weight:900;font-size:66px;color:#353a3d;margin-top:14px">zum Leben</div>
  </div>
  <div style="position:absolute;left:150px;top:900px">{zettel(780, 48)}</div>
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
