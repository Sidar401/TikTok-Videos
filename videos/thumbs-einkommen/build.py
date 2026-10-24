#!/usr/bin/env python3
"""Thumbnails (1920×1080) + TikTok-Cover (1080×1920) für longform-einkommen. Neue Motive: Leiter, Skala, Podest. Ohne Logo/Beagle.
Aufruf: python3 build.py        -> 3 Varianten (je 1 s)
        python3 build.py tiktok -> 9:16-Cover (Variante 1)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from icons import person  # noqa: E402
from longform import svg  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT  # noqa: E402

BLAU, LILA = "#3d7be0", "#9b59b6"
STUFEN = [("6", "Top 1 %", LILA), ("5", "> 4.600 €", GRUEN), ("4", "2.300 – 4.600 €", BLAU), ("3", "≈ 2.300 €", GOLD), ("2", "1.400 – 2.300 €", ORANGE), ("1", "< 1.400 €", ROT)]


def leiter(w, h, fs):
    sp = "".join(f'<div style="display:flex;align-items:center;gap:16px;height:{h / 7:.0f}px;padding:0 24px;border-radius:16px;background:{c};color:#fff;font-weight:900;font-size:{fs}px">'
                 f'<span class="serif" style="font-size:{fs * 1.3:.0f}px">{n}</span>{t}</div>' for n, t, c in STUFEN)
    return (f'<div style="width:{w}px;height:{h}px;display:flex;flex-direction:column;justify-content:space-between;border-left:14px solid #8a5a2b;'
            f'border-right:14px solid #8a5a2b;padding:0 16px">{sp}</div>')


PFEIL = '<svg viewBox="0 0 100 60" style="width:100%;height:100%"><path d="M96 30 L50 4 L50 20 L4 20 L4 40 L50 40 L50 56 Z" fill="#111" /></svg>'

V1 = f"""
  <div style="position:absolute;left:110px;top:90px">{leiter(760, 900, 50)}</div>
  <div style="position:absolute;left:1030px;top:200px;width:820px">
    <div class="serif" style="font-size:170px;line-height:1;color:#111">Wo stehst</div>
    <div style="display:inline-block;margin-top:20px;padding:10px 60px;border-radius:40px;background:{ORANGE};color:#fff;font-weight:900;font-size:170px;transform:rotate(-3deg)">DU?</div>
  </div>
  <div style="position:absolute;left:880px;top:520px;width:170px;height:100px;transform:rotate(180deg)">{PFEIL}</div>
"""

SKALA = (f'<div style="position:relative;width:1600px;height:120px;border-radius:60px;background:linear-gradient(90deg,{ROT},{ORANGE},{GOLD},{BLAU},{GRUEN},{LILA})">'
         f'<div style="position:absolute;left:880px;top:-150px;display:flex;flex-direction:column;align-items:center">'
         f'<div style="padding:10px 34px;border-radius:24px;background:#111;color:#fff;font-weight:900;font-size:70px">DU?</div>'
         f'<div style="width:0;height:0;border-left:30px solid transparent;border-right:30px solid transparent;border-top:40px solid #111"></div></div></div>')
V2 = f"""
  <div class="serif" style="position:absolute;left:0;top:110px;width:1920px;text-align:center;font-size:150px;line-height:1;color:#111">
    Bist du <span style="color:{ROT}">arm</span> oder <span style="color:{GRUEN}">reich</span>?</div>
  <div style="position:absolute;left:160px;top:520px">{SKALA}</div>
  <div style="position:absolute;left:160px;top:660px;width:1600px;display:flex;justify-content:space-between;font-weight:900;font-size:60px;color:#353a3d">
    <span>1.400 €</span><span>2.300 €</span><span>4.600 €</span><span>Top 1 %</span></div>
  <div style="position:absolute;left:0;top:820px;width:1920px;text-align:center"><span style="display:inline-block;padding:14px 50px;border-radius:30px;background:{ORANGE};color:#fff;font-weight:900;font-size:70px">Die Einkommens-Leiter 2026</span></div>
"""

KRONE = svg('<path d="M10 80 L5 25 L30 45 L50 12 L70 45 L95 25 L90 80 Z" fill="#f2c418" stroke="#c99a06" stroke-width="4" stroke-linejoin="round" /><circle cx="50" cy="62" r="7" fill="#e24b4b" />')
PODEST = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px">'
                 f'<div class="serif" style="font-size:64px;color:{c}">{v}</div>'
                 f'<div style="width:260px;height:{h}px;border-radius:16px 16px 0 0;background:{c};display:flex;justify-content:center;padding-top:20px;color:#fff;font-weight:900;font-size:80px">{p}</div></div>'
                 for p, v, h, c in [("3", "2.300 €", 220, GOLD), ("1", "Top 1 %", 420, LILA), ("2", "4.600 €", 320, GRUEN)])
V3 = f"""
  <div style="position:absolute;left:90px;top:150px;width:900px">
    <div class="serif" style="font-size:140px;line-height:1.02;color:#111">Ab wann<br/>bist du</div>
    <div style="display:inline-block;margin-top:24px;padding:12px 56px;border-radius:36px;background:{GRUEN};color:#fff;font-weight:900;font-size:140px;transform:rotate(-3deg)">REICH?</div>
  </div>
  <div style="position:absolute;left:960px;bottom:30px;display:flex;align-items:flex-end;gap:10px">{PODEST}</div>
  <div style="position:absolute;left:1250px;top:170px;width:220px;height:220px">{KRONE}</div>
"""

TIKTOK = f"""
  <div style="position:absolute;left:0;top:250px;width:1080px;text-align:center">
    <div class="serif" style="font-size:150px;line-height:1;color:#111">Wo stehst</div>
    <div style="display:inline-block;margin-top:18px;padding:8px 56px;border-radius:36px;background:{ORANGE};color:#fff;font-weight:900;font-size:150px;transform:rotate(-3deg)">DU?</div>
  </div>
  <div style="position:absolute;left:150px;top:720px">{leiter(780, 900, 46)}</div>
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
