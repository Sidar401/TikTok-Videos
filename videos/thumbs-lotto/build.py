#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-lotto. Lotto (neu: Lottokugeln, fallender Kontostand, Krone kaputt) Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import svg  # noqa: E402
from longform import GRUEN, ORANGE, ROT  # noqa: E402


def kugeln(gr):
    farben = [ROT, "#3d7be0", GRUEN, ORANGE, "#9b59b6", "#c99a06"]
    return "".join(f'<div style="width:{gr}px;height:{gr}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 12%,{c} 13%);display:flex;align-items:center;justify-content:center">'
                   f'<div style="width:{gr * 0.55:.0f}px;height:{gr * 0.55:.0f}px;border-radius:50%;background:#fff;color:#111;font-weight:900;font-size:{gr * 0.28:.0f}px;display:flex;align-items:center;justify-content:center">{z}</div></div>'
                   for z, c in zip([7, 13, 21, 29, 36, 42], farben))


V1 = f"""
  <div style="position:absolute;left:0;top:110px;width:1920px;display:flex;justify-content:center;gap:30px">{kugeln(190)}</div>
  <div style="position:absolute;left:0;top:400px;width:1920px;text-align:center">
    <div class="serif" style="font-size:150px;line-height:1;color:#c99a06">1 Million gewonnen …</div>
    <div style="display:inline-block;margin-top:30px;padding:14px 60px;border-radius:36px;background:{ROT};color:#fff;font-weight:900;font-size:130px;transform:rotate(-3deg)">… und PLEITE!</div>
  </div>
"""
V2 = f"""
  <div style="position:absolute;left:120px;top:230px;width:820px;padding:50px;border-radius:40px;background:#1d2125">
    <div style="font-weight:800;font-size:44px;color:#9aa3a8">KONTOSTAND</div>
    <div class="serif" style="font-size:118px;white-space:nowrap;color:#1f7a4d;text-decoration:line-through;text-decoration-color:{ROT};text-decoration-thickness:12px">1.000.000 €</div>
    <div class="serif" style="font-size:150px;color:{ROT}">0 €</div>
  </div>
  <div style="position:absolute;left:1020px;top:260px;width:820px">
    <div class="serif" style="font-size:130px;line-height:1.05;color:#111">In 4 Jahren</div>
    <div class="serif" style="font-size:130px;line-height:1.05;color:{ROT}">alles weg?!</div>
  </div>
"""
V3 = f"""
  <div class="serif" style="position:absolute;left:0;top:140px;width:1920px;text-align:center;font-size:140px;line-height:1.05;color:#111">Warum Lottogewinner<br/><span style="color:{ROT}">pleite gehen</span></div>
  <div style="position:absolute;left:0;top:560px;width:1920px;display:flex;justify-content:center;gap:30px">{kugeln(200)}</div>
"""
TIKTOK = f"""
  <div style="position:absolute;left:0;top:260px;width:1080px;display:flex;flex-wrap:wrap;justify-content:center;gap:20px;padding:0 120px">{kugeln(180)}</div>
  <div style="position:absolute;left:0;top:760px;width:1080px;text-align:center">
    <div class="serif" style="font-size:110px;line-height:1.05;color:#c99a06">1 Million<br/>gewonnen …</div>
    <div style="display:inline-block;margin-top:24px;padding:12px 50px;border-radius:34px;background:{ROT};color:#fff;font-weight:900;font-size:110px;transform:rotate(-3deg)">… und PLEITE!</div>
  </div>
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
