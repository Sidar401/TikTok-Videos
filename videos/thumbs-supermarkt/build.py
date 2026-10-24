#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-supermarkt. Neue Motive: voller Einkaufswagen, Regal mit Auge, Preisschild. Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from icons import WAGEN  # noqa: E402
from longform import svg  # noqa: E402
from longform import GRUEN, ORANGE, ROT  # noqa: E402

LILA = "#9b59b6"
AUGE = svg('<ellipse cx="50" cy="50" rx="46" ry="28" fill="#fff" stroke="#111" stroke-width="6" /><circle cx="50" cy="50" r="18" fill="#3d7be0" /><circle cx="50" cy="50" r="8" fill="#111" /><circle cx="56" cy="44" r="4" fill="#fff" />')


def voller_wagen(gr):
    farben = [ROT, GRUEN, ORANGE, "#3d7be0", LILA, "#f2c418", ROT, GRUEN, "#3d7be0"]
    berg = "".join(f'<div style="position:absolute;left:{28 + (i % 5) * 9}%;top:{8 - (i // 5) * 9}%;width:{gr * 0.12:.0f}px;height:{gr * 0.14:.0f}px;border-radius:8px;background:{c};transform:rotate({(i * 17) % 30 - 15}deg)"></div>'
                   for i, c in enumerate(farben))
    return f'<div style="position:relative;width:{gr}px;height:{gr}px">{berg}{WAGEN}</div>'


V1 = f"""
  <div style="position:absolute;left:70px;top:200px">{voller_wagen(640)}</div>
  <div style="position:absolute;left:820px;top:160px;width:1020px">
    <div class="serif" style="font-size:130px;line-height:1.02;color:#111">Der Supermarkt</div>
    <div style="display:inline-block;margin:18px 0;padding:10px 50px;border-radius:34px;background:{ROT};color:#fff;font-weight:900;font-size:140px;transform:rotate(-3deg)">TRICKST</div>
    <div class="serif" style="font-size:130px;line-height:1.02;color:#111">dich aus!</div>
  </div>
"""

REGAL = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;width:760px;padding:22px 34px;border-bottom:16px solid #8a5a2b;background:#faf5ef">'
                f'<span style="font-weight:900;font-size:50px;color:{c}">{t}</span><span class="serif" style="font-size:64px;color:{c}">{p}</span></div>'
                for t, p, c in [("Marke", "3,49 €", ROT), ("Eigenmarke", "1,79 €", GRUEN)])
V2 = f"""
  <div style="position:absolute;left:90px;top:420px;border-left:16px solid #8a5a2b;border-right:16px solid #8a5a2b">{REGAL}</div>
  <div style="position:absolute;left:290px;top:200px;width:320px;height:190px">{AUGE}</div>
  <div style="position:absolute;left:970px;top:280px;width:880px">
    <div class="serif" style="font-size:120px;line-height:1.05;color:#111">Achtung</div>
    <div style="display:inline-block;margin-top:18px;padding:10px 46px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:92px">AUGENHÖHE!</div>
    <div style="font-weight:900;font-size:60px;color:#353a3d;margin-top:30px">Hier zahlst du fast das Doppelte</div>
  </div>
"""

V3 = f"""
  <div style="position:absolute;left:120px;top:320px;padding:40px 70px;background:#f2c418;border:10px solid #111;border-radius:28px;transform:rotate(-6deg)">
    <span class="serif" style="font-size:260px;line-height:1;color:#111">4,<span style="font-size:160px;vertical-align:top">99</span></span></div>
  <div style="position:absolute;left:880px;top:300px;width:960px">
    <div class="serif" style="font-size:140px;line-height:1.02;color:#111">Fällst du</div>
    <div class="serif" style="font-size:140px;line-height:1.02;color:{ROT}">darauf rein?</div>
    <div style="display:inline-block;margin-top:30px;padding:12px 46px;border-radius:30px;background:{GRUEN};color:#fff;font-weight:900;font-size:64px">10 Supermarkt-Tricks</div>
  </div>
"""

TIKTOK = f"""
  <div style="position:absolute;left:0;top:250px;width:1080px;text-align:center">
    <div class="serif" style="font-size:120px;line-height:1.02;color:#111">Der Supermarkt</div>
    <div style="display:inline-block;margin:16px 0;padding:8px 50px;border-radius:34px;background:{ROT};color:#fff;font-weight:900;font-size:130px;transform:rotate(-3deg)">TRICKST</div>
    <div class="serif" style="font-size:120px;line-height:1.02;color:#111">dich aus!</div>
  </div>
  <div style="position:absolute;left:190px;top:900px">{voller_wagen(700)}</div>
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
