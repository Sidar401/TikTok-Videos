#!/usr/bin/env python3
"""YouTube-Thumbnails (1920×1080) für longform-100k – je Variante 1 s, Snapshot bei 0.5/1.5/2.5 s."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import GELDSACK  # noqa: E402

BEAGLE = '<img src="assets/beagle.png" style="width:100%;height:100%;object-fit:contain" />'
PFEIL = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M10 88 L48 50 L62 64 L86 30" fill="none" stroke="#1f7a4d" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" /><path d="M66 22 L94 18 L90 46 Z" fill="#1f7a4d" /></svg>'

V1 = f"""
  <div style="position:absolute;left:90px;top:120px;width:560px;height:560px">{GELDSACK}</div>
  <div style="position:absolute;left:640px;top:150px;width:1220px">
    <div class="serif" style="font-size:160px;line-height:1;color:#111">0 →</div>
    <div class="serif" style="font-size:250px;line-height:1;color:#c99a06">100.000 €</div>
  </div>
  <div style="position:absolute;left:90px;top:760px;padding:22px 50px;border-radius:30px;background:#DB8622;color:#fff;font-weight:900;font-size:96px">mit normalem Gehalt</div>
  <div style="position:absolute;right:70px;bottom:60px;width:300px;height:300px">{BEAGLE}</div>
"""

balken = "".join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">'
    f'<div class="serif" style="font-size:{s}px;color:{c};white-space:nowrap">{v}</div>'
    f'<div style="width:200px;height:{h}px;border-radius:16px 16px 0 0;background:{b}"></div></div>'
    for v, h, c, b, s in [("21.000 €", 170, "#1f7a4d", "#1f7a4d", 56), ("50.000 €", 360, "#c99a06", "#f2c418", 56),
                          ("100.000 €", 620, "#c99a06", "#f2c418", 64)])
V2 = f"""
  <div style="position:absolute;left:80px;top:90px;width:900px">
    <div class="serif" style="font-size:150px;line-height:1.02;color:#111">So wirst du<br/>reich mit</div>
    <div style="display:inline-block;margin-top:30px;padding:18px 44px;border-radius:30px;background:#DB8622;color:#fff;font-weight:900;font-size:96px">2.000 € netto</div>
  </div>
  <div style="position:absolute;left:1000px;bottom:30px;display:flex;align-items:flex-end;gap:40px">{balken}</div>
  <div style="position:absolute;left:420px;top:700px;width:260px;height:260px">{PFEIL}</div>
  <div style="position:absolute;left:70px;bottom:40px;width:300px;height:300px">{BEAGLE}</div>
"""

V3 = f"""
  <div style="position:absolute;left:0;top:190px;width:1920px;display:flex;justify-content:center;align-items:center;gap:60px">
    <div style="text-align:center"><div style="font-weight:800;font-size:64px;color:#353a3d">Gehalt</div>
      <div class="serif" style="font-size:170px;color:#1f7a4d;line-height:1">2.000 €</div></div>
    <div class="serif" style="font-size:180px;color:#DB8622;line-height:1">→</div>
    <div style="text-align:center"><div style="font-weight:800;font-size:64px;color:#353a3d">Vermögen</div>
      <div class="serif" style="font-size:170px;color:#c99a06;line-height:1">100.000 €</div></div>
  </div>
  <div style="position:absolute;left:0;top:640px;width:1920px;text-align:center">
    <span style="display:inline-block;padding:26px 70px;border-radius:40px;background:#e24b4b;color:#fff;font-weight:900;font-size:130px;transform:rotate(-3deg)">Realistisch?!</span>
  </div>
  <div style="position:absolute;right:70px;bottom:50px;width:280px;height:280px">{BEAGLE}</div>
"""

szenen = "\n".join(
    f'<div id="v{i}" class="scene clip" data-start="{i}" data-duration="1" data-track-index="1">{h}</div>'
    for i, h in enumerate([V1, V2, V3]))
(HERE / "index.html").write_text(f"""<!doctype html>
<html lang="de" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Abril Fatface"; src: url("assets/fonts/abril-fatface.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #fff; font-family: Montserrat, sans-serif; }}
      .scene {{ position: absolute; inset: 0; }}
      .serif {{ font-family: "Abril Fatface", serif; }}
      #frame {{ position: absolute; inset: 0; border: 30px solid #DB8622; z-index: 10; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="3" data-width="1920" data-height="1080">
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
print("Thumbnails gebaut")
