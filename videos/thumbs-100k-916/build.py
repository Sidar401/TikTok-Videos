#!/usr/bin/env python3
"""TikTok-Cover 9:16 (1080×1920) zu longform-100k, Variante 2. Inhalt im 3:4-Mittelbereich (Profil-Raster)."""
from pathlib import Path

HERE = Path(__file__).parent
BEAGLE = '<img src="assets/beagle.png" style="width:100%;height:100%;object-fit:contain" />'
PFEIL = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M10 88 L48 50 L62 64 L86 30" fill="none" stroke="#1f7a4d" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" /><path d="M66 22 L94 18 L90 46 Z" fill="#1f7a4d" /></svg>'
balken = "".join(
    f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">'
    f'<div class="serif" style="font-size:{s}px;color:{c};white-space:nowrap">{v}</div>'
    f'<div style="width:220px;height:{h}px;border-radius:16px 16px 0 0;background:{b}"></div></div>'
    for v, h, c, b, s in [("21.000 €", 150, "#1f7a4d", "#1f7a4d", 52), ("50.000 €", 320, "#c99a06", "#f2c418", 52),
                          ("100.000 €", 540, "#c99a06", "#f2c418", 60)])
INHALT = f"""
  <div style="position:absolute;left:0;top:270px;width:1080px;text-align:center">
    <div class="serif" style="font-size:132px;line-height:1.02;color:#111">So wirst du<br/>reich mit</div>
    <div style="display:inline-block;margin-top:34px;padding:18px 44px;border-radius:30px;background:#DB8622;color:#fff;font-weight:900;font-size:92px">2.000 € netto</div>
  </div>
  <div style="position:absolute;left:0;top:1080px;width:1080px;height:560px;display:flex;justify-content:center;align-items:flex-end;gap:36px">{balken}</div>
  <div style="position:absolute;left:70px;top:800px;width:230px;height:230px">{BEAGLE}</div>
  <div style="position:absolute;left:320px;top:810px;width:190px;height:190px">{PFEIL}</div>
"""
(HERE / "index.html").write_text(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Abril Fatface"; src: url("assets/fonts/abril-fatface.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #fff; font-family: Montserrat, sans-serif; }}
      .serif {{ font-family: "Abril Fatface", serif; }}
      #frame {{ position: absolute; inset: 0; border: 26px solid #DB8622; z-index: 10; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1080" data-height="1920">
      <div id="v" class="clip" data-start="0" data-duration="1" data-track-index="1" style="position:absolute;inset:0">{INHALT}</div>
      <div id="frame"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#v", {{ opacity: 1 }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("Cover gebaut")
