#!/usr/bin/env python3
"""Demo-Shop-Video OHNE KI-Clips und OHNE Stimme (nur Grafik + Produktfoto).

    python3 scripts/shop_demo.py shop/<produkt>/demo-<x>.json

Konfig (JSON):
  name     Ordnername unter videos/
  produkt  {bild, preis, sterne, verkauft, cta, badge}  (wie shop_video.py)
  ende     Länge der Endkarte in s (Standard 3)
  szenen   Liste von Szenen:
    text    Untertitel (*Wort* = orange, | = neue Zeile)
    dur     Länge in s
    bg      "hell" | "dunkel" | "orange"
    rein    wie das Produkt kommt: "unten" | "pop" | "links" | "rechts" | "dreh" | "weg" (kein Produkt)
    haupt   optional: großes Emoji in der Mitte (gut bei rein="weg")
    gross   optional: großer Stempel (z. B. "8 h", "15 €", "1.")
    emojis  optional: Liste Emojis, die um das Produkt ploppen
    chips   optional: Liste kurzer Merkmale (Kästchen unten)
    durch   optional: Text, der rot durchgestrichen wird (z. B. "60 € Sofa")
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from shop_video import TEMPLATE as SHOP_TEMPLATE, words_html  # noqa: E402

# Endkarte + Grund-CSS aus der abgenommenen Shop-Vorlage übernehmen
END_CSS = SHOP_TEMPLATE.split("/* Endkarte */")[1].split("</style>")[0]
END_HTML = SHOP_TEMPLATE.split("<div id=\"end\"")[1].split("<div id=\"flash\"")[0]
END_JS = SHOP_TEMPLATE.split("// Endkarte")[1].split("window.__timelines[\"main\"]")[0]

BG = {
    "hell": "radial-gradient(circle at 50% 45%, #FFFFFF 0%, #FFEBD2 70%, #F8D6AE 100%)",
    "dunkel": "radial-gradient(circle at 50% 45%, #3a2a17 0%, #1B1D1F 65%)",
    "orange": "radial-gradient(circle at 50% 45%, #F3A64C 0%, #DB8622 60%, #B86A12 100%)",
}

# Sternförmig verteilte Plätze für Emojis um das Produkt
EMOJI_POS = [(150, 620), (840, 660), (110, 1180), (880, 1220), (480, 520), (500, 1380)]


def scene_html(i, s, t):
    d = s["dur"]
    rein = s.get("rein", "pop")
    parts = [f'<div class="bgfill" style="background:{BG[s.get("bg", "hell")]}"></div>']
    if rein != "weg":
        parts.append(f'<div class="pglow" id="g{i}"></div>')
        parts.append(f'<img class="prod" id="p{i}" src="assets/produkt.png" alt="" />')
        parts.append(f'<div class="shadow" id="sh{i}"></div>')
    if s.get("haupt"):
        parts.append(f'<div class="haupt" id="h{i}">{s["haupt"]}</div>')
    for k, e in enumerate(s.get("emojis", [])):
        x, y = EMOJI_POS[k % len(EMOJI_POS)]
        parts.append(f'<div class="emo e{i}" style="left:{x}px;top:{y}px">{e}</div>')
    if s.get("gross"):
        parts.append(f'<div class="gross" id="gr{i}"><span>{html.escape(s["gross"])}</span></div>')
    if s.get("durch"):
        parts.append(f'<div class="durch" id="du{i}"><span>{html.escape(s["durch"])}<i></i></span></div>')
    if s.get("chips"):
        chips = "".join(f'<span class="chip ch{i}">{html.escape(c)}</span>' for c in s["chips"])
        parts.append(f'<div class="chips">{chips}</div>')
    parts.append(f'<div class="cap" id="c{i}"><div class="capin">{words_html(s["text"], i)}</div></div>')
    dark = (" dark" if s.get("bg") in ("dunkel", "orange") else "") + f' bg-{s.get("bg", "hell")}'
    return (f'<div id="s{i}" class="clip scene{dark}" data-start="{t:.2f}" data-duration="{d:.2f}" '
            f'data-track-index="1">\n          ' + "\n          ".join(parts) + "\n        </div>")


def scene_js(i, s, t):
    d = s["dur"]
    rein = s.get("rein", "pop")
    js = [f"// Szene {i}", f'tl.fromTo("#s{i} .bgfill", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.4, ease: "power3.out" }}, {t});']
    if rein != "weg":
        start = {
            "unten": "{ y: 900, rotation: 25, opacity: 1 }",
            "pop": "{ scale: 0.2, opacity: 0 }",
            "links": "{ x: -1000, rotation: -60, opacity: 1 }",
            "rechts": "{ x: 1000, rotation: 60, opacity: 1 }",
            "dreh": "{ scale: 0.3, rotation: -360, opacity: 0 }",
        }[rein]
        js += [
            f'tl.fromTo("#p{i}", {start}, {{ x: 0, y: 0, scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(1.6)" }}, {t + 0.05:.2f});',
            f'tl.fromTo("#g{i}", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.6, ease: "power2.out" }}, {t + 0.1:.2f});',
            f'tl.fromTo("#sh{i}", {{ scaleX: 0.3, opacity: 0 }}, {{ scaleX: 1, opacity: 1, duration: 0.5 }}, {t + 0.2:.2f});',
            # „Rollen“: leichtes Wackeln + Hüpfen, solange die Szene läuft
            f'tl.to("#p{i}", {{ rotation: 6, y: -18, duration: 0.32, yoyo: true, repeat: {max(int((d - 0.7) / 0.32), 1) // 2 * 2 - 1}, ease: "sine.inOut" }}, {t + 0.62:.2f});',
            f'tl.to("#g{i}", {{ scale: 1.08, duration: {max(d - 0.7, 0.2):.2f}, ease: "sine.inOut" }}, {t + 0.7:.2f});',
        ]
    if s.get("haupt"):
        js += [f'tl.fromTo("#h{i}", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, {t + 0.05:.2f});',
               f'tl.to("#h{i}", {{ scale: 1.06, rotation: 4, duration: 0.4, yoyo: true, repeat: {max(int((d - 0.6) / 0.4), 1) // 2 * 2 - 1}, ease: "sine.inOut" }}, {t + 0.5:.2f});']
    if s.get("emojis"):
        js += [
            f'tl.fromTo("#s{i} .emo", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.5)", stagger: 0.12 }}, {t + 0.35:.2f});',
            f'tl.to("#s{i} .emo", {{ y: -25, duration: 0.5, yoyo: true, repeat: {max(int((d - 1) / 0.5), 1) // 2 * 2 - 1}, ease: "sine.inOut", stagger: 0.08 }}, {t + 0.9:.2f});',
        ]
    if s.get("gross"):
        js.append(f'tl.fromTo("#gr{i}", {{ scale: 2.6, opacity: 0, rotation: -14 }}, {{ scale: 1, opacity: 1, rotation: -6, duration: 0.28, ease: "power4.out" }}, {t + 0.45:.2f});')
        js.append(f'tl.fromTo("#s{i}", {{ x: -14 }}, {{ x: 0, duration: 0.25, ease: "elastic.out(1, 0.3)" }}, {t + 0.73:.2f});')
    if s.get("durch"):
        js.append(f'tl.fromTo("#du{i}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {t + 0.3:.2f});')
        js.append(f'tl.fromTo("#du{i} i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power2.in" }}, {t + 0.9:.2f});')
    if s.get("chips"):
        js.append(f'tl.fromTo("#s{i} .chip", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.18 }}, {t + 0.6:.2f});')
    if i > 1:
        js.append(f'tl.fromTo("#c{i} .w", {{ scale: 0.4, opacity: 0, y: 20 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.18, ease: "back.out(2.4)", stagger: 0.07 }}, {t + 0.05:.2f});')
        js.append(f'tl.fromTo("#flash", {{ opacity: 0.5 }}, {{ opacity: 0, duration: 0.15, immediateRender: false }}, {t:.2f});')
    else:  # erster Untertitel steht ab Frame 0 (Vorschaubild) und pulsiert
        js.append('tl.fromTo("#c1 .capin", { scale: 1 }, { scale: 1.07, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut" }, 0.4);')
    return "\n      ".join(js)


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
    shutil.copy(ROOT / p["bild"], vdir / "assets" / "produkt.png")

    t, scenes, js = 0.0, [], []
    for i, s in enumerate(cfg["szenen"], 1):
        scenes.append(scene_html(i, s, t))
        js.append(scene_js(i, s, t))
        t += s["dur"]
    ende = cfg.get("ende", 3.0)
    total = t + ende

    end_html = END_HTML
    for k, v in {
        "{{T_END}}": f"{t:.2f}", "{{ENDE}}": f"{ende:.2f}",
        "{{PREIS}}": html.escape(p["preis"]), "{{STERNE}}": html.escape(p["sterne"]),
        "{{VERKAUFT}}": html.escape(p["verkauft"]), "{{CTA}}": html.escape(p.get("cta", "Unten im Warenkorb")),
        "{{BADGE}}": html.escape(p.get("badge", "Bestseller")),
    }.items():
        end_html = end_html.replace(k, v)

    doc = (DEMO.replace("{{END_CSS}}", END_CSS)
           .replace("{{TOTAL}}", f"{total:.2f}")
           .replace("{{SCENES}}", "\n        ".join(scenes))
           .replace("{{END}}", '<div id="end"' + end_html)
           .replace("{{JS}}", "\n\n      ".join(js))
           .replace("{{END_JS}}", END_JS.replace("tEnd", f"{t:.2f}")))
    (vdir / "index.html").write_text(doc)
    print(f"{vdir}/index.html · {total:.1f} s")


DEMO = """<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      /* Demo-Shop-Vorlage HundeWissenTv 2.0 (ohne KI-Clips) – erzeugt von scripts/shop_demo.py */
      @font-face { font-family: "Noto Color Emoji"; src: local("Noto Color Emoji"); }
      :root { --brand: #DB8622; --dark: #1B1D1F; --font: "Montserrat", sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      #root { position: relative; width: 100%; height: 100%; background: #000; font-family: var(--font); }
      .scene { position: absolute; inset: 0; overflow: hidden; }
      .bgfill { position: absolute; inset: -80px; }
      .pglow { position: absolute; left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.75) 0%, rgba(255,255,255,0) 65%); }
      .dark .pglow { background: radial-gradient(circle, rgba(219,134,34,0.6) 0%, rgba(219,134,34,0) 65%); }
      .prod { position: absolute; left: 165px; top: 640px; width: 750px; filter: drop-shadow(0 30px 40px rgba(0,0,0,0.35)); }
      .shadow { position: absolute; left: 290px; top: 1270px; width: 500px; height: 60px; border-radius: 50%;
        background: radial-gradient(ellipse, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 70%); }
      .haupt { position: absolute; left: 0; width: 1080px; top: 700px; text-align: center; font-size: 420px; line-height: 1;
        font-family: "Noto Color Emoji", sans-serif; }
      .emo { position: absolute; font-size: 120px; line-height: 1; width: 140px; text-align: center;
        font-family: "Noto Color Emoji", sans-serif; }

      /* Untertitel oben, nie über dem Produkt */
      .cap { position: absolute; left: 60px; width: 960px; top: 230px; text-align: center; z-index: 5; }
      .capin { font-weight: 900; font-size: 84px; line-height: 1.12; color: #fff;
        -webkit-text-stroke: 14px #000; paint-order: stroke fill; text-shadow: 0 10px 28px rgba(0,0,0,0.45); }
      .w { display: inline-block; }
      .w.hot { color: var(--brand); }
      .bg-orange .w.hot { color: #FFE14D; }

      .gross { position: absolute; left: 0; width: 1080px; top: 1380px; text-align: center; z-index: 4; }
      .gross span { display: inline-block; background: #fff; color: var(--dark); font-weight: 900; font-size: 170px;
        line-height: 1; padding: 20px 56px 30px; border-radius: 36px; letter-spacing: -4px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.45); border: 8px solid var(--brand); }
      .durch { position: absolute; left: 0; width: 1080px; top: 1420px; text-align: center; z-index: 4; }
      .durch span { display: inline-block; color: #fff; font-weight: 900; font-size: 96px;
        -webkit-text-stroke: 10px #000; paint-order: stroke fill; }
      .durch span { position: relative; }
      .durch i { position: absolute; left: -10px; right: -10px; top: 50%; height: 18px; background: #E24B4B;
        border-radius: 9px; transform-origin: left center; transform: rotate(-4deg); }
      .chips { position: absolute; left: 60px; width: 960px; top: 1400px; display: flex; flex-wrap: wrap;
        justify-content: center; gap: 22px; z-index: 4; }
      .chip { background: #fff; color: var(--dark); font-weight: 900; font-size: 52px; padding: 18px 34px;
        border-radius: 999px; box-shadow: 0 12px 30px rgba(0,0,0,0.25); border: 6px solid var(--brand); }

      /* Endkarte */{{END_CSS}}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
      <div id="scenes">
        {{SCENES}}
      </div>

      {{END}}
      <div id="flash" class="clip" data-start="0" data-duration="{{TOTAL}}" data-track-index="3"></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });

      {{JS}}

      // Endkarte{{END_JS}}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    build(sys.argv[1])
