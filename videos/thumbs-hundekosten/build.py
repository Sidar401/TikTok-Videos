#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-hundekosten. Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from icons import AUTO, HUND_NEUTRAL as HUND  # noqa: E402
from longform import ORANGE, ROT  # noqa: E402

POSTEN = [("Anschaffung", "2.200 €"), ("Futter & Co.", "23.400 €"), ("Urlaub", "3.900 €"), ("Notfall-OP", "3.000 €"), ("Seniorenjahre", "1.800 €")]


def zettel(w, fs):
    rows = "".join(f'<div style="display:flex;justify-content:space-between;padding:6px 0"><span>{a}</span><b style="color:#111">{b}</b></div>' for a, b in POSTEN)
    return (f'<div style="width:{w}px;background:#faf5ef;border-radius:30px;padding:34px 46px;font-weight:700;font-size:{fs}px;color:#353a3d;transform:rotate(3deg);box-shadow:0 14px 0 #e8dccb">'
            f'<div style="font-weight:800;color:{ORANGE};border-bottom:4px dashed #d9cbb8;padding-bottom:10px;margin-bottom:8px">Ein Hundeleben</div>{rows}'
            f'<div style="display:flex;justify-content:space-between;align-items:center;border-top:5px solid #353a3d;margin-top:14px;padding-top:14px">'
            f'<span style="font-weight:800;color:#111">Summe</span><span class="serif" style="font-size:{fs * 2:.0f}px;color:{ROT}">34.000 €</span></div></div>')


V1 = f"""
  <div style="position:absolute;left:90px;top:150px;width:900px">
    <div class="serif" style="font-size:132px;line-height:1.02;color:#111">So viel kostet<br/>ein Hund</div>
    <div style="display:inline-block;margin-top:30px;padding:16px 44px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:92px">WIRKLICH</div>
  </div>
  <div style="position:absolute;left:1040px;top:150px">{zettel(760, 44)}</div>
  <div style="position:absolute;left:560px;top:560px;width:420px;height:420px">{HUND}</div>
"""

V2 = f"""
  <div style="position:absolute;left:0;top:110px;width:1920px;display:flex;justify-content:center;align-items:center;gap:70px">
    <div style="width:470px;height:470px">{HUND}</div>
    <div class="serif" style="font-size:260px;color:{ORANGE}">=</div>
    <div style="width:520px;height:520px">{AUTO}</div>
  </div>
  <div style="position:absolute;left:0;top:700px;width:1920px;text-align:center">
    <span style="display:inline-block;padding:20px 64px;border-radius:40px;background:{ROT};color:#fff;font-weight:900;font-size:118px;transform:rotate(-2deg)">Hund = Kleinwagen?!</span>
  </div>
"""

V3 = f"""
  <div style="position:absolute;left:90px;top:250px;width:620px;height:620px">{HUND}</div>
  <div style="position:absolute;left:760px;top:250px;width:1080px;text-align:center">
    <div class="serif" style="font-size:250px;line-height:1;color:{ROT}">34.000 €</div>
    <div style="font-weight:900;font-size:100px;color:#111;margin-top:20px">für EINEN Hund?!</div>
    <div style="display:inline-block;margin-top:40px;padding:14px 46px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:64px">vom Welpen bis ins Alter</div>
  </div>
"""

TIKTOK = f"""
  <div style="position:absolute;left:0;top:270px;width:1080px;text-align:center">
    <div class="serif" style="font-size:116px;line-height:1.02;color:#111">So viel kostet<br/>ein Hund</div>
    <div style="display:inline-block;margin-top:26px;padding:14px 44px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:86px">WIRKLICH</div>
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
