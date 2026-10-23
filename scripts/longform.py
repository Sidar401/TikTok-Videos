"""16:9-Longform-Videos für HundeFinanzTV (1920×1080).

Ein Video-`build.py` definiert SZENEN und ruft `build(HERE, SZENEN, KAPITEL)` auf.
Szene = (satz_von, satz_bis, art, daten). Arten:
  "split"  : Bild links (icon-SVG/HTML), Text rechts  -> dict(icon=..., text=..., sub=..., farbe=...)
  "zahl"   : große Zahl mittig + Untertitel          -> dict(zahl=..., sub=..., farbe=...)
  "kapitel": Kapitelkarte                           -> dict(nr=..., titel=...)
  "chips"  : Reihe von Schildern, nacheinander       -> dict(titel=..., chips=[(text, farbe, durchgestrichen)])
  "frei"   : eigenes HTML + JS                       -> dict(html=..., js=lambda t0, d: "...")
KAPITEL = {"k1": "Einstieg", ...} -> Anzeige oben rechts, je nach `kapitel` im skript.json.
"""
import json
from pathlib import Path

ORANGE, GRUEN, GOLD, ROT, INK = "#DB8622", "#1f7a4d", "#c99a06", "#e24b4b", "#111"
W, H = 1920, 1080

CSS = """
      @font-face { font-family: "Abril Fatface"; src: url("assets/fonts/abril-fatface.woff2") format("woff2"); }
      :root { --brand: #DB8622; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #fff; }
      #root { position: relative; width: 100%; height: 100%; background: #fff; font-family: Montserrat, sans-serif; }
      .scene { position: absolute; inset: 0; }
      .serif { font-family: "Abril Fatface", serif; }
      .bild { position: absolute; left: 150px; top: 150px; width: 760px; height: 700px; display: flex; align-items: center; justify-content: center; }
      .bild > * { max-width: 100%; max-height: 100%; }
      .txt { position: absolute; left: 980px; top: 150px; width: 800px; height: 700px; display: flex; flex-direction: column; justify-content: center; gap: 26px; }
      .txt .h { font-family: "Abril Fatface", serif; font-size: 96px; line-height: 1.08; color: #111; }
      .txt .s { font-weight: 800; font-size: 52px; line-height: 1.2; color: #353a3d; }
      .mitte { position: absolute; left: 0; top: 150px; width: 1920px; height: 700px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 30px; text-align: center; }
      .zahl { font-family: "Abril Fatface", serif; font-size: 230px; line-height: 1; }
      .zsub { font-weight: 800; font-size: 64px; color: #111; }
      .kap { display: flex; flex-direction: column; align-items: center; gap: 24px; }
      .kap .nr { padding: 16px 52px; border-radius: 60px; background: var(--brand); color: #fff; font-weight: 800; font-size: 56px; }
      .kap .t { font-family: "Abril Fatface", serif; font-size: 150px; color: #111; }
      .chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; max-width: 1600px; }
      .chip { position: relative; padding: 24px 46px; border-radius: 26px; color: #fff; font-weight: 800; font-size: 58px; }
      .chip.x::after { content: ""; position: absolute; left: 8%; right: 8%; top: 50%; height: 10px; background: #111; border-radius: 5px; transform: rotate(-8deg); }
      .ctitel { font-family: "Abril Fatface", serif; font-size: 100px; color: #111; }
      #brand { position: absolute; left: 60px; top: 44px; font-weight: 800; font-size: 40px; color: #353a3d; z-index: 5; }
      .kapanz { position: absolute; right: 60px; top: 38px; padding: 10px 30px; border-radius: 40px; background: #faf5ef; color: #a8621a; font-weight: 800; font-size: 34px; z-index: 5; }
      #frame { position: absolute; inset: 0; border: 18px solid var(--brand); z-index: 10; }
      .cap { position: absolute; left: 0; top: 905px; width: 1920px; display: flex; justify-content: center; z-index: 6; }
      .cap span { display: block; padding: 14px 40px 16px; border-radius: 22px; background: var(--brand); color: #fff; font-weight: 600; font-size: 50px; line-height: 1.15; white-space: nowrap; }
"""


def svg(inner, vb="0 0 100 100", w="100%", h="100%"):
    return f'<svg viewBox="{vb}" style="width:{w};height:{h}">{inner}</svg>'


def _szene(sid, t0, d, art, x):
    if art == "split":
        col = x.get("farbe", INK)
        sub = f'<div class="s" id="{sid}-s">{x["sub"]}</div>' if x.get("sub") else ""
        html = (f'<div class="bild" id="{sid}-b">{x["icon"]}</div>'
                f'<div class="txt"><div class="h" id="{sid}-h" style="color:{col}">{x["text"]}</div>{sub}</div>')
        js = f'pop("#{sid}-b", {t0}); pop("#{sid}-h", {t0} + 0.2);' + (f' pop("#{sid}-s", {t0} + {x.get("sub_at", 0.6)});' if sub else "")
    elif art == "zahl":
        html = (f'<div class="mitte"><div class="zahl" id="{sid}-z" style="color:{x.get("farbe", INK)}">{x["zahl"]}</div>'
                + (f'<div class="zsub" id="{sid}-s">{x["sub"]}</div>' if x.get("sub") else "") + "</div>")
        js = f'pop("#{sid}-z", {t0}); tl.fromTo("#{sid}-z", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.2, yoyo: true, repeat: 1 }}, {t0} + 0.45);' + (f' pop("#{sid}-s", {t0} + 0.3);' if x.get("sub") else "")
    elif art == "kapitel":
        html = (f'<div class="mitte"><div class="kap"><div class="nr" id="{sid}-n">Schritt {x["nr"]}</div>'
                f'<div class="t" id="{sid}-t">{x["titel"]}</div></div></div>') if x.get("nr") else (
                f'<div class="mitte"><div class="kap"><div class="t" id="{sid}-t">{x["titel"]}</div></div></div>')
        js = (f'pop("#{sid}-n", {t0});' if x.get("nr") else "") + f' tl.fromTo("#{sid}-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t0} + 0.15);'
    elif art == "chips":
        chips = "".join(f'<div class="chip{" x" if c[2] else ""}" id="{sid}-c{i}" style="background:{c[1]}">{c[0]}</div>' for i, c in enumerate(x["chips"]))
        titel = f'<div class="ctitel" id="{sid}-t">{x["titel"]}</div>' if x.get("titel") else ""
        html = f'<div class="mitte">{titel}<div class="chips">{chips}</div></div>'
        step = min(0.6, max(0.2, (d - 0.6) / max(1, len(x["chips"]))))
        js = (f'pop("#{sid}-t", {t0});' if titel else "") + "".join(f' pop("#{sid}-c{i}", {t0} + {0.3 + i * step:.2f});' for i in range(len(x["chips"])))
    elif art == "frei":
        html, js = x["html"], x["js"](t0, d)
    else:
        raise ValueError(art)
    return html, js


def build(here, szenen, kapitel_namen):
    here = Path(here)
    t = json.loads((here / "timings.json").read_text())
    sk = {s["id"]: s for s in json.loads((here / "skript.json").read_text())["saetze"]}
    S = {s["id"]: s for s in t["saetze"]}
    dauer, last = t["dauer"], t["saetze"][-1]["id"]
    out, js, caps, kaps = [], [], [], []
    for n, (a, b, art, x) in enumerate(szenen):
        t0 = S[a]["start"]
        t1 = dauer if b == last else S[b]["end"]
        d = round(t1 - t0, 3)
        sid = f"z{n}"
        html, code = _szene(sid, t0, d, art, x)
        out.append(f'      <div id="{sid}" class="scene clip" data-start="{t0}" data-duration="{d}" data-track-index="1">{html}</div>')
        js.append(f"      {code}")
    # Kapitel-Anzeige oben rechts
    cur, start = None, 0.0
    for s in t["saetze"]:
        k = sk[s["id"]].get("kapitel")
        if k != cur:
            if cur:
                kaps.append((cur, start, s["start"]))
            cur, start = k, s["start"]
    kaps.append((cur, start, dauer))
    kap_html = "\n".join(f'      <div id="kap-{k}" class="kapanz clip" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="4">{kapitel_namen.get(k, "")}</div>'
                         for k, a, b in kaps if kapitel_namen.get(k))
    n = 0
    for s in t["saetze"]:
        for cp in s["captions"]:
            n += 1
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{cp["start"]}" data-duration="{round(cp["end"] - cp["start"], 3)}" data-track-index="2"><span>{cp["text"]}</span></div>')
    html = f"""<!doctype html>
<html lang="de" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/gsap.min.js"></script>
    <style>{CSS}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dauer}" data-width="1920" data-height="1080">
{chr(10).join(out)}

      <div id="brand">HundeFinanzTV</div>
{kap_html}
      <div id="frame"></div>
      <div id="captions" data-track-kind="captions">
{chr(10).join(caps)}
      </div>
      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{dauer}" data-track-index="3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const pop = (sel, at) =>
        tl.fromTo(sel, {{ scale: 0.85, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, at);
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (here / "index.html").write_text(html)
    print("index.html gebaut,", dauer, "s,", len(szenen), "Szenen")
