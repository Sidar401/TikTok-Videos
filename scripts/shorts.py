"""9:16-Shorts aus Longform-Videos für HundeFinanzTV (1080×1920).

Ablauf: `scripts/new-video.sh <name>` → `python3 scripts/kurz.py <longform> videos/<name> s1 s14-s15 …`
→ build.py definiert SZENEN und ruft `build(HERE, SZENEN, banner)` auf.
Szene = (satz_von, satz_bis, art, daten); bis = letzter Satz → läuft bis Videoende (Endkarte).
  "split": Bild oben, Text darunter -> dict(icon=..., text=..., sub=..., farbe=..., sub_at=...)
  "zahl" : große Zahl mittig        -> dict(zahl=..., sub=..., farbe=...)
  "frei" : eigenes HTML + JS        -> dict(html=..., js=lambda t0, d: "...")
`banner` = Hinweis oben aufs Hauptvideo (läuft das ganze Video).
"""
import json
from pathlib import Path

from icons import BEAGLE

ORANGE, GRUEN, GOLD, ROT, INK, DUNKEL = "#DB8622", "#1f7a4d", "#c99a06", "#e24b4b", "#111", "#1d2125"

CSS = """
      @font-face { font-family: "Abril Fatface"; src: url("assets/fonts/abril-fatface.woff2") format("woff2"); }
      :root { --brand: #DB8622; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #fff; }
      #root { position: relative; width: 100%; height: 100%; background: #fff; font-family: Montserrat, sans-serif; }
      .scene { position: absolute; inset: 0; }
      .serif { font-family: "Abril Fatface", serif; }
      .bild { position: absolute; left: 190px; top: 330px; width: 700px; height: 560px; display: flex; align-items: center; justify-content: center; }
      .bild > * { max-width: 100%; max-height: 100%; }
      .txt { position: absolute; left: 70px; top: 920px; width: 940px; height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 22px; text-align: center; }
      .txt .h { font-family: "Abril Fatface", serif; font-size: 92px; line-height: 1.08; color: #111; }
      .txt .s { font-weight: 800; font-size: 50px; line-height: 1.2; color: #353a3d; }
      .mitte { position: absolute; left: 60px; top: 300px; width: 960px; height: 1030px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px; text-align: center; }
      .zahl { font-family: "Abril Fatface", serif; font-size: 170px; line-height: 1; }
      .zsub { font-weight: 800; font-size: 58px; color: #111; }
      .chip { padding: 20px 40px; border-radius: 24px; color: #fff; font-weight: 800; font-size: 54px; }
      #brand { position: absolute; left: 0; top: 176px; width: 1080px; text-align: center; font-weight: 800; font-size: 40px; color: #353a3d; z-index: 5; }
      #banner { position: absolute; left: 0; top: 236px; width: 1080px; display: flex; justify-content: center; z-index: 5; }
      #banner span { display: flex; align-items: center; gap: 14px; padding: 8px 26px; border-radius: 30px; background: #faf5ef; color: #a8621a; font-weight: 800; font-size: 30px; }
      #frame { position: absolute; inset: 0; border: 26px solid var(--brand); z-index: 10; }
      .cap { position: absolute; left: 0; top: 1360px; width: 1080px; display: flex; justify-content: center; z-index: 6; }
      .cap span { display: block; max-width: 880px; padding: 20px 44px 22px; border-radius: 28px; background: var(--brand); color: #fff; font-weight: 600; font-size: 54px; line-height: 1.15; text-align: center; }
"""

PLAY_KLEIN = '<svg viewBox="0 0 30 22" style="width:34px;height:25px"><rect width="30" height="22" rx="6" fill="#e24b4b" /><path d="M12 6 L20 11 L12 16 Z" fill="#fff" /></svg>'


def svg(inner, vb="0 0 100 100", w="100%", h="100%"):
    return f'<svg viewBox="{vb}" style="width:{w};height:{h}">{inner}</svg>'


def endkarte(frage, teaser, uid="ek"):
    """CTA am Ende: offene Frage → ganzes Video auf YouTube + Folgen (Beagle erlaubt, da CTA-Szene)."""
    play = svg('<rect x="4" y="14" width="92" height="72" rx="18" fill="#e24b4b" /><path d="M40 34 L66 50 L40 66 Z" fill="#fff" />')
    html = ('<div class="mitte" style="gap:40px">'
            f'<div id="{uid}-f" class="serif" style="font-size:96px;line-height:1.08;color:#111">{frage}</div>'
            f'<div id="{uid}-t" style="font-weight:800;font-size:52px;color:#e24b4b">{teaser}</div>'
            f'<div id="{uid}-k" style="display:flex;align-items:center;gap:30px;padding:30px 44px;border-radius:36px;background:#faf5ef;border:6px solid #353a3d">'
            f'<div style="width:150px;height:150px">{play}</div><div style="text-align:left"><div style="font-weight:800;font-size:56px;color:#111">Ganzes Video</div>'
            f'<div style="font-weight:700;font-size:44px;color:#555c60">auf YouTube: HundeFinanzTV</div></div></div>'
            f'<div style="display:flex;align-items:center;gap:36px"><div id="{uid}-dog" style="width:230px;height:230px">{BEAGLE}</div>'
            f'<div id="{uid}-btn" style="padding:22px 60px;border-radius:70px;background:var(--brand);color:#fff;font-weight:800;font-size:62px">+ Folgen</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#{uid}-f", {t0}); pop("#{uid}-t", {t0} + 0.5); pop("#{uid}-k", {t0} + 1.0);'
                f' tl.fromTo("#{uid}-k", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.3, yoyo: true, repeat: 3 }}, {t0} + 1.6);'
                f' pop("#{uid}-dog", {t0} + 1.4); pop("#{uid}-btn", {t0} + 1.6);')


def _szene(sid, t0, d, art, x):
    if art == "split":
        sub = f'<div class="s" id="{sid}-s">{x["sub"]}</div>' if x.get("sub") else ""
        html = (f'<div class="bild" id="{sid}-b">{x["icon"]}</div>'
                f'<div class="txt"><div class="h" id="{sid}-h" style="color:{x.get("farbe", INK)}">{x["text"]}</div>{sub}</div>')
        js = f'pop("#{sid}-b", {t0}); pop("#{sid}-h", {t0} + 0.2);' + (f' pop("#{sid}-s", {t0} + {x.get("sub_at", 0.6)});' if sub else "")
    elif art == "zahl":
        html = (f'<div class="mitte"><div class="zahl" id="{sid}-z" style="color:{x.get("farbe", INK)}">{x["zahl"]}</div>'
                + (f'<div class="zsub" id="{sid}-s">{x["sub"]}</div>' if x.get("sub") else "") + "</div>")
        js = f'pop("#{sid}-z", {t0});' + (f' pop("#{sid}-s", {t0} + 0.3);' if x.get("sub") else "")
    elif art == "frei":
        html, js = x["html"], x["js"](t0, d)
    else:
        raise ValueError(art)
    return html, js


def build(here, szenen, banner):
    here = Path(here)
    t = json.loads((here / "timings.json").read_text())
    S = {s["id"]: s for s in t["saetze"]}
    dauer, last = t["dauer"], t["saetze"][-1]["id"]
    out, js, caps = [], [], []
    for n, (a, b, art, x) in enumerate(szenen):
        t0 = S[a]["start"]
        # nächste Szene beginnt nahtlos (Lücken zwischen Abschnitten überbrücken)
        t1 = dauer if b == last else (S[szenen[n + 1][0]]["start"] if n + 1 < len(szenen) else S[b]["end"])
        d = round(t1 - t0, 3)
        sid = f"z{n}"
        html, code = _szene(sid, t0, d, art, x)
        out.append(f'      <div id="{sid}" class="scene clip" data-start="{t0}" data-duration="{d}" data-track-index="1">{html}</div>')
        js.append(f"      {code}")
    n = 0
    for s in t["saetze"]:
        for cp in s["captions"]:
            n += 1
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{cp["start"]}" data-duration="{round(cp["end"] - cp["start"], 3)}" data-track-index="2"><span>{cp["text"]}</span></div>')
    html = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>{CSS}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dauer}" data-width="1080" data-height="1920">
{chr(10).join(out)}

      <div id="brand">HundeFinanzTV</div>
      <div id="banner"><span>{PLAY_KLEIN}{banner}</span></div>
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
