#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-zwei-leben. Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from icons import person  # noqa: E402
from longform import GRUEN, ORANGE, ROT  # noqa: E402

LEON = person(GRUEN, "#353a3d")
FELIX = person(ROT, "#8a5a2b")


def fig(p, w):
    return f'<div style="width:{w}px;height:{w * 1.3:.0f}px">{p}</div>'


def haelfte(p, name, betrag, farbe, w, h, fs, ausr="center"):
    return (f'<div style="width:{w}px;height:{h}px;background:{farbe};display:flex;flex-direction:column;align-items:center;justify-content:{ausr};padding:110px 0;gap:10px;color:#fff">'
            f'<div style="background:#fff;border-radius:50%;padding:20px">{fig(p, int(fs * 2.4))}</div>'
            f'<div style="font-weight:900;font-size:{fs * 0.7:.0f}px">{name} mit 40</div>'
            f'<div class="serif" style="font-size:{fs * 1.4:.0f}px;line-height:1">{betrag}</div></div>')


V1 = f"""
  <div style="position:absolute;inset:0;display:flex">{haelfte(LEON, "Leon", "+137.000 €", GRUEN, 960, 1080, 100)}{haelfte(FELIX, "Felix", "−8.000 €", ROT, 960, 1080, 100)}</div>
  <div style="position:absolute;left:0;top:50px;width:1920px;text-align:center"><span style="display:inline-block;padding:14px 50px;border-radius:30px;background:#fff;color:#111;font-weight:900;font-size:70px;transform:rotate(-2deg)">Gleiches Gehalt!</span></div>
"""

V2 = f"""
  <div class="serif" style="position:absolute;left:0;top:90px;width:1920px;text-align:center;font-size:130px;line-height:1.05;color:#111">
    <span style="color:{GRUEN}">Reich</span> mit 40 oder<br/><span style="color:{ROT}">pleite</span> mit 40?</div>
  <div style="position:absolute;left:0;top:500px;width:1920px;display:flex;justify-content:center;align-items:flex-end;gap:160px">
    <div style="display:flex;flex-direction:column;align-items:center;gap:14px">{fig(LEON, 300)}<div style="padding:8px 36px;border-radius:30px;background:{GRUEN};color:#fff;font-weight:900;font-size:56px">Leon</div></div>
    <div class="serif" style="font-size:140px;color:{ORANGE};margin-bottom:120px">vs</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:14px">{fig(FELIX, 300)}<div style="padding:8px 36px;border-radius:30px;background:{ROT};color:#fff;font-weight:900;font-size:56px">Felix</div></div>
  </div>
"""

V3 = f"""
  <div style="position:absolute;left:80px;top:230px;display:flex;align-items:flex-end;gap:10px">{fig(LEON, 330)}{fig(FELIX, 330)}</div>
  <div style="position:absolute;left:790px;top:250px;width:1060px;text-align:center">
    <div class="serif" style="font-size:220px;line-height:1;color:{GRUEN};white-space:nowrap">145.000&nbsp;€</div>
    <div style="font-weight:900;font-size:90px;color:#111;margin-top:20px">Unterschied</div>
    <div style="display:inline-block;margin-top:30px;padding:14px 46px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:68px">bei GLEICHEM Gehalt</div>
  </div>
"""

TIKTOK = f"""
  <div style="position:absolute;inset:0;display:flex;flex-direction:column">{haelfte(LEON, "Leon", "+137.000 €", GRUEN, 1080, 960, 95, "flex-end")}{haelfte(FELIX, "Felix", "−8.000 €", ROT, 1080, 960, 95, "flex-start")}</div>
  <div style="position:absolute;left:0;top:900px;width:1080px;text-align:center"><span style="display:inline-block;padding:16px 50px;border-radius:30px;background:#fff;color:#111;font-weight:900;font-size:76px;box-shadow:0 8px 0 rgba(0,0,0,0.15)">Gleiches Gehalt!</span></div>
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
