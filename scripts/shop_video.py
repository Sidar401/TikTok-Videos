#!/usr/bin/env python3
"""TikTok-Shop-Video aus einer Konfig bauen (HundeWissenTv 2.0).

    python3 scripts/shop_video.py shop/<produkt>/<video>.json

Konfig (JSON):
  name      Ordnername unter videos/
  clips     Liste {src, from, dur, text}: src = Datei in assets/clips/,
            from = Startsekunde im Clip, dur = Länge, text = Untertitel
            (*Wort* wird orange hervorgehoben, "|" = Zeilenumbruch)
  produkt   {bild, preis, sterne, verkauft, cta}  für die Endkarte
  ende      Länge der Endkarte in s (Standard 3)

Die KI-Clips (Higgsfield) werden nicht committet; sie liegen in
videos/<name>/assets/clips/ (siehe clips.txt im Produktordner).
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def words_html(text, cid):
    """Untertitel in Wort-Spans zerlegen; *x* → orange, | → Umbruch."""
    out = []
    for li, line in enumerate(text.split("|")):
        if li:
            out.append("<br />")
        for wi, w in enumerate(line.split()):
            hot = w.startswith("*") and w.endswith("*")
            w = w.strip("*")
            cls = "w hot" if hot else "w"
            out.append(f'<span class="{cls}">{html.escape(w)}</span>')
    return " ".join(out).replace(" <br /> ", "<br />")


def build(cfg_path):
    cfg = json.loads(Path(cfg_path).read_text())
    name = cfg["name"]
    vdir = ROOT / "videos" / name
    if not vdir.exists():
        shutil.copytree(ROOT / "vorlage", vdir)
        shutil.rmtree(vdir / ".hyperframes", ignore_errors=True)
        pj = vdir / "package.json"
        pj.write_text(re.sub(r'"name":\s*"[^"]*"', f'"name": "{name}"', pj.read_text()))
    p = cfg["produkt"]
    src_bild = ROOT / p["bild"]
    shutil.copy(src_bild, vdir / "assets" / "produkt.png")

    t = 0.0
    vids, caps, cuts = [], [], []
    for i, c in enumerate(cfg["clips"], 1):
        d = c["dur"]
        vids.append(
            f'<video id="v{i}" class="clip vid" src="assets/clips/{c["src"]}" muted playsinline '
            f'data-start="{t:.2f}" data-duration="{d:.2f}" data-media-start="{c.get("from", 0):.2f}" '
            f'data-track-index="1"></video>'
        )
        if c.get("text"):
            caps.append(
                f'<div id="c{i}" class="cap clip" data-start="{t:.2f}" data-duration="{d:.2f}" '
                f'data-track-index="2"><div class="capin">{words_html(c["text"], i)}</div></div>'
            )
        cuts.append((i, t, d))
        t += d
    ende = cfg.get("ende", 3.0)
    t_end = t
    total = t + ende

    js_cuts = json.dumps([[i, round(s, 2), round(d, 2)] for i, s, d in cuts])
    doc = TEMPLATE
    for k, v in {
        "{{TOTAL}}": f"{total:.2f}",
        "{{VIDS}}": "\n      ".join(vids),
        "{{CAPS}}": "\n        ".join(caps),
        "{{T_END}}": f"{t_end:.2f}",
        "{{ENDE}}": f"{ende:.2f}",
        "{{CUTS}}": js_cuts,
        "{{PREIS}}": html.escape(p["preis"]),
        "{{STERNE}}": html.escape(p["sterne"]),
        "{{VERKAUFT}}": html.escape(p["verkauft"]),
        "{{CTA}}": html.escape(p.get("cta", "Unten im Warenkorb")),
        "{{BADGE}}": html.escape(p.get("badge", "Bestseller")),
    }.items():
        doc = doc.replace(k, v)
    (vdir / "index.html").write_text(doc)
    print(f"{vdir}/index.html · {total:.1f} s")


TEMPLATE = """<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      /* Shop-Vorlage HundeWissenTv 2.0 – erzeugt von scripts/shop_video.py */
      :root { --brand: #DB8622; --dark: #1B1D1F; --font: "Montserrat", sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      #root { position: relative; width: 100%; height: 100%; background: #000; font-family: var(--font); }
      #stage { position: absolute; inset: 0; overflow: hidden; }
      .vid { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }

      /* Untertitel: fette weiße Schrift mit Kontur, Schlüsselwort orange */
      .cap { position: absolute; left: 70px; width: 940px; top: 1000px; text-align: center; z-index: 5; }
      .capin { font-weight: 900; font-size: 78px; line-height: 1.12; color: #fff;
        -webkit-text-stroke: 14px #000; paint-order: stroke fill;
        text-shadow: 0 10px 28px rgba(0,0,0,0.55); }
      .w { display: inline-block; }
      .w.hot { color: var(--brand); }

      /* Endkarte */
      #end { position: absolute; inset: 0; z-index: 8;
        background: radial-gradient(circle at 50% 38%, #3a2a17 0%, var(--dark) 60%); }
      #glow { position: absolute; left: 140px; top: 330px; width: 800px; height: 800px; border-radius: 50%;
        background: radial-gradient(circle, rgba(219,134,34,0.55) 0%, rgba(219,134,34,0) 65%); }
      #e-badge { position: absolute; top: 230px; left: 0; width: 1080px; text-align: center; }
      #e-badge span { display: inline-block; background: var(--brand); color: #fff; font-weight: 900; font-size: 44px;
        padding: 12px 34px; border-radius: 999px; letter-spacing: 1px; }
      #e-prod { position: absolute; left: 215px; top: 380px; width: 650px; }
      #e-stars { position: absolute; top: 880px; left: 0; width: 1080px; text-align: center; color: #fff;
        font-weight: 800; font-size: 44px; }
      #e-stars b { color: #F2C418; }
      #e-price { position: absolute; top: 950px; left: 0; width: 1080px; text-align: center; }
      #e-price span { display: inline-block; background: #fff; color: var(--dark); font-weight: 900; font-size: 150px;
        line-height: 1; padding: 18px 50px 26px; border-radius: 34px; letter-spacing: -3px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
      #e-cta { position: absolute; top: 1170px; left: 110px; width: 860px; text-align: center; background: var(--brand);
        color: #fff; font-weight: 900; font-size: 58px; padding: 30px 20px; border-radius: 999px;
        box-shadow: 0 16px 50px rgba(219,134,34,0.45); }
      #e-arrow { position: absolute; top: 1330px; left: 495px; width: 90px; height: 100px; }
      #e-brand { position: absolute; top: 1460px; left: 0; width: 1080px; display: flex; justify-content: center;
        align-items: center; gap: 14px; color: rgba(255,255,255,0.8); font-weight: 800; font-size: 36px; }
      #e-brand img { width: 64px; height: 64px; border-radius: 50%; }

      #flash { position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 20; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
      <div id="stage">
      {{VIDS}}
      </div>

      <div id="captions" data-track-kind="captions">
        {{CAPS}}
      </div>

      <div id="end" class="clip" data-start="{{T_END}}" data-duration="{{ENDE}}" data-track-index="1" data-track-kind="graphics">
        <div id="glow"></div>
        <div id="e-badge"><span>{{BADGE}}</span></div>
        <img id="e-prod" src="assets/produkt.png" alt="" />
        <div id="e-stars"><b>★★★★★</b> {{STERNE}} · {{VERKAUFT}}</div>
        <div id="e-price"><span>{{PREIS}}</span></div>
        <div id="e-cta">{{CTA}} 🛒</div>
        <svg id="e-arrow" viewBox="0 0 100 110"><path d="M50 8 L50 90 M18 60 L50 94 L82 60" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" /></svg>
        <div id="e-brand"><img src="assets/beagle.png" alt="" />HundeWissenTv 2.0</div>
      </div>

      <div id="flash" class="clip" data-start="0" data-duration="{{TOTAL}}" data-track-index="3"></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      const cuts = {{CUTS}};
      const tEnd = {{T_END}};

      cuts.forEach(([i, s, d]) => {
        // Schnitt: kurzer Zoom-Punch, dann langsamer Drift
        tl.fromTo("#stage", { scale: 1.08 }, { scale: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, s);
        tl.to("#stage", { scale: 1.04, duration: Math.max(d - 0.25, 0.1), ease: "none" }, s + 0.25);
        // Untertitel: Wörter ploppen nacheinander auf
        const ws = document.querySelectorAll("#c" + i + " .w");
        if (ws.length) {
          tl.fromTo(ws, { scale: 0.4, opacity: 0, y: 20 },
            { scale: 1, opacity: 1, y: 0, duration: 0.18, ease: "back.out(2.4)", stagger: Math.min(0.09, 0.6 / ws.length) },
            i === 1 ? 0 : s + 0.05);
        }
      });
      // Erster Untertitel steht ab Frame 0 (Thumbnail)
      tl.set("#c1 .w", { scale: 1, opacity: 1, y: 0 }, 0);

      // Endkarte
      tl.fromTo("#flash", { opacity: 0.8 }, { opacity: 0, duration: 0.2, ease: "power2.out", immediateRender: false }, tEnd);
      tl.fromTo("#glow", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "power2.out" }, tEnd);
      tl.fromTo("#e-badge", { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, tEnd + 0.05);
      tl.fromTo("#e-prod", { y: 400, rotation: -20, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(1.5)" }, tEnd + 0.05);
      tl.to("#e-prod", { rotation: 4, y: -12, duration: 0.35, yoyo: true, repeat: 7, ease: "sine.inOut" }, tEnd + 0.6);
      tl.fromTo("#e-stars", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3 }, tEnd + 0.35);
      tl.fromTo("#e-price", { scale: 1.8, opacity: 0, rotation: -6 }, { scale: 1, opacity: 1, rotation: -2, duration: 0.3, ease: "power4.out" }, tEnd + 0.5);
      tl.fromTo("#e-cta", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }, tEnd + 0.8);
      tl.to("#e-cta", { scale: 1.05, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }, tEnd + 1.2);
      tl.fromTo("#e-arrow", { y: -20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25 }, tEnd + 1.0);
      tl.to("#e-arrow", { y: 26, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }, tEnd + 1.25);
      tl.fromTo("#e-brand", { opacity: 0 }, { opacity: 1, duration: 0.4 }, tEnd + 1.0);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    build(sys.argv[1])
