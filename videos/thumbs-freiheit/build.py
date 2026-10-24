#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-freiheit. Freiheit (neu: Berg mit Flagge, Hängematte-freie Typo, Formel) Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import svg  # noqa: E402
from longform import GRUEN, ORANGE, ROT  # noqa: E402


def berg(w, h):
    return (f'<svg viewBox="0 0 100 80" style="width:{w}px;height:{h}px"><rect width="100" height="80" fill="#eaf4fb" rx="6" />'
            f'<path d="M0 80 L30 30 L45 50 L62 12 L100 80 Z" fill="#9aa3a8" stroke="#555c60" stroke-width="1.2" /><path d="M56 24 L62 12 L68 24 L64 22 L62 26 L60 22 Z" fill="#fff" />'
            f'<rect x="61.5" y="2" width="1" height="10" fill="#353a3d" /><path d="M62.5 2 L72 4.5 L62.5 7 Z" fill="{GRUEN}" />'
            f'<path d="M0 80 Q30 70 55 76 Q80 82 100 74 L100 80 Z" fill="#6fbf86" /></svg>')


V1 = f"""
  <div style="position:absolute;left:90px;top:170px">{berg(820, 656)}</div>
  <div style="position:absolute;left:980px;top:200px;width:880px">
    <div class="serif" style="font-size:120px;line-height:1.05;color:#111">So viel Geld,</div>
    <div class="serif" style="font-size:120px;line-height:1.05;color:#111">um <span style="color:{GRUEN}">NIE</span> wieder</div>
    <div class="serif" style="font-size:120px;line-height:1.05;color:#111">zu arbeiten</div>
  </div>
"""
V2 = f"""
  <div style="position:absolute;left:0;top:300px;width:1920px;display:flex;justify-content:center;align-items:center;gap:36px">
    <div style="padding:30px 50px;border-radius:30px;background:#3d7be0;color:#fff;font-weight:900;font-size:90px">Ausgaben</div>
    <div class="serif" style="font-size:130px;color:{ORANGE}">× 25</div>
    <div style="padding:30px 50px;border-radius:30px;background:{GRUEN};color:#fff;font-weight:900;font-size:90px">= FREI</div>
  </div>
  <div class="serif" style="position:absolute;left:0;top:640px;width:1920px;text-align:center;font-size:110px;color:#111">Die Formel für finanzielle Freiheit</div>
"""
V3 = f"""
  <div class="serif" style="position:absolute;left:0;top:120px;width:1920px;text-align:center;font-size:130px;color:#111">Nie wieder arbeiten?</div>
  <div style="position:absolute;left:0;top:380px;width:1920px;display:flex;justify-content:center;gap:50px">
    {"".join(f'<div style="width:540px;padding:40px 0;border-radius:30px;background:{c};color:#fff;text-align:center"><div style="font-weight:900;font-size:60px">{t}</div><div class="serif" style="font-size:88px;white-space:nowrap">{v}</div></div>' for t, v, c in [("Sparsam", "450.000 €", GRUEN), ("Normal", "750.000 €", "#3d7be0"), ("Luxus", "1,2 Mio. €", "#9b59b6")])}
  </div>
  <div style="position:absolute;left:0;top:820px;width:1920px;text-align:center;font-weight:900;font-size:70px;color:#353a3d">Welcher Gipfel ist deiner?</div>
"""
TIKTOK = f"""
  <div style="position:absolute;left:0;top:250px;width:1080px;text-align:center">
    <div class="serif" style="font-size:104px;line-height:1.05;color:#111">So viel Geld,<br/>um <span style="color:{GRUEN}">NIE</span> wieder<br/>zu arbeiten</div>
  </div>
  <div style="position:absolute;left:140px;top:820px">{berg(800, 640)}</div>
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
