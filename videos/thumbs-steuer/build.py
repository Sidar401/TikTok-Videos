#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-steuer. Steuer-Tresor (neu: Tresor, Stempel, Geldregen-Zahl) Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import svg  # noqa: E402
from longform import GRUEN, ORANGE, ROT  # noqa: E402


def tresor(gr):
    s = "".join(f'<div style="position:absolute;left:{gr / 2 + gr * 0.32 * __import__("math").cos(__import__("math").radians(-90 + i * 60)) - gr * 0.08:.0f}px;top:{gr / 2 + gr * 0.32 * __import__("math").sin(__import__("math").radians(-90 + i * 60)) - gr * 0.08:.0f}px;width:{gr * 0.16:.0f}px;height:{gr * 0.16:.0f}px;border-radius:50%;background:{GRUEN if i < 4 else "#555c60"};border:5px solid #f2c418"></div>' for i in range(6))
    return (f'<div style="position:relative;width:{gr}px;height:{gr}px;border-radius:40px;background:#353a3d;box-shadow:inset 0 0 0 16px #555c60, 0 16px 0 #222">{s}'
            f'<div style="position:absolute;left:{gr * 0.4:.0f}px;top:{gr * 0.4:.0f}px;width:{gr * 0.2:.0f}px;height:{gr * 0.2:.0f}px;border-radius:50%;background:#f2c418"></div></div>')


V1 = f"""
  <div style="position:absolute;left:100px;top:220px">{tresor(620)}</div>
  <div style="position:absolute;left:820px;top:200px;width:1020px">
    <div class="serif" style="font-size:120px;line-height:1.05;color:#111">Das Finanzamt</div>
    <div class="serif" style="font-size:120px;line-height:1.05;color:#111">schuldet dir</div>
    <div style="display:inline-block;margin-top:20px;padding:12px 50px;border-radius:34px;background:{GRUEN};color:#fff;font-weight:900;font-size:120px;transform:rotate(-3deg)">GELD!</div>
  </div>
"""
V2 = f"""
  <div class="serif" style="position:absolute;left:0;top:120px;width:1920px;text-align:center;font-size:150px;line-height:1;color:#111">7 legale <span style="color:{GRUEN}">Steuertricks</span></div>
  <div style="position:absolute;left:0;top:400px;width:1920px;display:flex;justify-content:center;gap:24px">
    {"".join(f'<div style="width:200px;height:200px;border-radius:50%;background:{GRUEN if i < 5 else "#555c60"};border:10px solid #f2c418;color:#fff;font-family:Abril Fatface;font-size:110px;display:flex;align-items:center;justify-content:center">{"✓" if i < 5 else i + 1}</div>' for i in range(7))}
  </div>
  <div style="position:absolute;left:0;top:720px;width:1920px;text-align:center"><span style="display:inline-block;padding:14px 50px;border-radius:30px;background:{ROT};color:#fff;font-weight:900;font-size:80px">die fast keiner nutzt</span></div>
"""
V3 = f"""
  <div style="position:absolute;left:110px;top:200px;padding:30px 60px;border:16px solid {ROT};border-radius:24px;color:{ROT};font-weight:900;font-size:120px;transform:rotate(-10deg)">VERSCHENKT!</div>
  <div style="position:absolute;left:0;top:520px;width:1920px;text-align:center">
    <div class="serif" style="font-size:250px;line-height:1;color:{GRUEN}">2.500 €</div>
    <div style="font-weight:900;font-size:76px;color:#111;margin-top:10px">holst du dir vom Finanzamt zurück</div>
  </div>
"""
TIKTOK = f"""
  <div style="position:absolute;left:0;top:250px;width:1080px;text-align:center">
    <div class="serif" style="font-size:112px;line-height:1.05;color:#111">Das Finanzamt<br/>schuldet dir</div>
    <div style="display:inline-block;margin-top:20px;padding:10px 50px;border-radius:34px;background:{GRUEN};color:#fff;font-weight:900;font-size:120px;transform:rotate(-3deg)">GELD!</div>
  </div>
  <div style="position:absolute;left:220px;top:880px">{tresor(640)}</div>
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
