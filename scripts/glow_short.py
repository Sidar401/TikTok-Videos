"""Neuer Short-Stil „Dark Glow“ (ab 27.10., Nutzer-Feedback: mehr Tempo, Hook, Sound).

Dunkler Raster-Hintergrund + oranges Leuchten (wie die Thumbnails), oranger Rahmen, Beagle-Logo oben durchgehend (Nutzer 27.10.), Bildwechsel alle 1–2 s,
Zoom-Drift pro Szene, große Wort-für-Wort-Untertitel (aktives Wort orange), Soundeffekte (lokal synthetisiert).

  from glow_short import *
  SZENEN = [(t0, t1, html, lambda t0, d: js), ...]     # Zeiten in s
  SFX = [(t, "whoosh"|"pop"|"ding"|"boom"|"tick"|"kasse"), ...]
  build(HERE, SZENEN, SFX)  → index.html + assets/mix.wav
"""
import json
from pathlib import Path

import numpy as np
import soundfile as sf

OR, GRUEN, ROT, GOLD, BG = "#ff8a1f", "#2fd27a", "#ff4d4d", "#ffc533", "#0e1012"
SR = 44100

CSS = f"""
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: Montserrat, sans-serif; overflow: hidden;
        background: radial-gradient(ellipse at 50% 42%, #ff8a1f33 0%, #ff8a1f0d 38%, transparent 62%), radial-gradient(ellipse at 50% 50%, #1b1f22 0%, {BG} 75%); }}
      #raster {{ position: absolute; inset: 0; background-image: linear-gradient(#ffffff0c 2px, transparent 2px), linear-gradient(90deg, #ffffff0c 2px, transparent 2px); background-size: 90px 90px; }}
      .scene {{ position: absolute; inset: 0; }}
      .inner {{ position: absolute; inset: 0; }}
      .t {{ position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; line-height: 1.02; letter-spacing: -1px; color: #fff; }}
      .glow-o {{ color: {OR}; text-shadow: 0 0 50px {OR}aa; }}
      .glow-g {{ color: {GRUEN}; text-shadow: 0 0 50px {GRUEN}aa; }}
      .glow-r {{ color: {ROT}; text-shadow: 0 0 50px {ROT}aa; }}
      .box {{ display: inline-block; padding: 6px 34px 14px; border-radius: 24px; background: {OR}; color: #111; box-shadow: 0 0 60px {OR}88; }}
      #logo {{ position: absolute; left: 445px; top: 135px; width: 190px; height: 190px; border-radius: 50%; overflow: hidden; border: 5px solid #DB8622; box-shadow: 0 0 30px #ff8a1f88; z-index: 5; }}
      #logo img {{ width: 100%; height: 100%; object-fit: cover; }}
      #brand {{ position: absolute; left: 0; top: 335px; width: 1080px; text-align: center; font-weight: 800; font-size: 30px; color: #ffffffcc; letter-spacing: 2px; z-index: 5; }}
      #frame {{ position: absolute; inset: 0; border: 26px solid #DB8622; z-index: 10; }}
      .cap {{ position: absolute; left: 60px; top: 1330px; width: 960px; text-align: center; z-index: 6; }}
      .cap span {{ display: inline-block; margin: 0 11px; font-weight: 900; font-size: 74px; line-height: 1.15; color: #fff; text-shadow: 0 6px 0 #000, 0 0 30px #000; }}
"""


def t(id_, html, top, size=120, cls=""):
    return f'<div id="{id_}" class="t {cls}" style="top:{top}px;font-size:{size}px">{html}</div>'


def ring(id_, inner, x, y, gr, farbe=OR):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{gr}px;border-radius:50%;background:#16191b;'
            f'border:10px solid {farbe};box-shadow:0 0 80px {farbe}88, inset 0 0 40px #000;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:2">{inner}</div>')


def handy(id_, x, y, w, inhalt="", farbe=OR):
    h = w * 1.9
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{w * 0.16}px;background:#16191b;'
            f'border:8px solid {farbe};box-shadow:0 0 90px {farbe}77, 0 40px 60px #000;z-index:2;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">'
            f'<div style="position:absolute;top:22px;width:30%;height:14px;border-radius:7px;background:#2a2f33"></div>{inhalt}</div>')


def chip(id_, txt, farbe, top, size=60, x=None):
    pos = f"left:{x}px" if x is not None else "left:0;width:1080px;display:flex;justify-content:center"
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{top}px;z-index:3"><span style="display:inline-block;padding:12px 34px 16px;border-radius:22px;'
            f'background:{farbe};color:#111;font-weight:900;font-size:{size}px;box-shadow:0 0 50px {farbe}88">{txt}</span></div>')


TEILEN_SVG = (f'<svg viewBox="0 0 100 100" style="width:60%;height:60%"><path d="M22 74 Q26 40 58 38 L58 22 L84 48 L58 74 L58 58 Q36 57 22 74 Z" fill="{OR}"/></svg>')
BLASE_SVG = ('<svg viewBox="0 0 100 100" style="width:62%;height:62%"><path d="M12 14 L88 14 Q94 14 94 20 L94 62 Q94 68 88 68 L42 68 L22 88 L26 68 L12 68 Q6 68 6 62 L6 20 Q6 14 12 14 Z" '
             'fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/><circle cx="32" cy="41" r="6" fill="#ff8a1f"/><circle cx="50" cy="41" r="6" fill="#ff8a1f"/><circle cx="68" cy="41" r="6" fill="#ff8a1f"/></svg>')


def cta_szene(uid, svg, text):
    """Teilen-/Kommentar-Szene: leuchtender Ring + Text. Liefert (html, js)."""
    html = ring(f"{uid}-r", svg, 340, 380, 400) + t(f"{uid}-t", text, 900, 66)
    return html, lambda a, d: (f'pop("#{uid}-r", {a}); tl.fromTo("#{uid}-r", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {a} + 0.4);'
                               f' pop("#{uid}-t", {a} + 0.6);')


def outro_szene(beagle):
    html = (ring("ou-r", f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{beagle}</div>', 290, 330, 500) +
            t("ou-n", "HundeFinanzTV", 900, 96) + chip("ou-f", "+ Folgen", OR, 1040, 64))
    return html, lambda a, d: (f'pop("#ou-r", {a}); pop("#ou-n", {a} + 0.3); slam("#ou-f", {a} + 0.6);'
                               f' tl.fromTo("#ou-f", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.2);')


def zeiten(here):
    """cap(sid, i) = Start der i-ten Untertitel-Box, st(sid)/en(sid) = Satzgrenzen."""
    T = json.loads((Path(here) / "timings.json").read_text())
    S = {s["id"]: s for s in T["saetze"]}
    return (lambda sid, i: S[sid]["captions"][min(i, len(S[sid]["captions"]) - 1)]["start"],
            lambda sid: S[sid]["start"], lambda sid: S[sid]["end"], T["dauer"])


# ---------------- Soundeffekte (synthetisch, lizenzfrei) ----------------
def _env(n, a=0.005, d=0.2):
    t_ = np.arange(n) / SR
    return np.minimum(1, t_ / a) * np.exp(-t_ / d)


def _sfx(art):
    rng = np.random.default_rng(7)
    if art == "whoosh":
        n = int(0.4 * SR)
        x = rng.standard_normal(n)
        y = np.zeros(n)
        for i in range(1, n):  # Tiefpass mit wanderndem Koeffizienten
            a = 0.02 + 0.25 * np.sin(np.pi * i / n)
            y[i] = y[i - 1] + a * (x[i] - y[i - 1])
        return 0.5 * y * np.sin(np.pi * np.arange(n) / n) ** 2
    if art == "pop":
        n = int(0.09 * SR)
        f = np.linspace(900, 300, n)
        return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.03)
    if art == "tick":
        n = int(0.03 * SR)
        return 0.35 * np.sin(2 * np.pi * 2200 * np.arange(n) / SR) * _env(n, 0.001, 0.006)
    if art == "ding":
        n = int(0.8 * SR)
        k = np.arange(n) / SR
        return 0.3 * (np.sin(2 * np.pi * 1760 * k) + 0.5 * np.sin(2 * np.pi * 2640 * k)) * _env(n, 0.002, 0.25)
    if art == "boom":
        n = int(0.5 * SR)
        f = np.linspace(110, 38, n)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.003, 0.18)
        return 0.8 * s + 0.15 * rng.standard_normal(n) * _env(n, 0.001, 0.02)
    if art == "kasse":
        a, b = _sfx("ding"), _sfx("ding")
        b = np.interp(np.arange(len(b)) * 1.19, np.arange(len(b)), b)  # höher
        out = np.zeros(int(0.9 * SR))
        out[: len(a)] += a
        o = int(0.09 * SR)
        out[o: o + len(b) - o] += b[: len(out) - o][: len(b) - o]
        out[: int(0.05 * SR)] += 0.2 * rng.standard_normal(int(0.05 * SR)) * _env(int(0.05 * SR), 0.001, 0.01)
        return out
    raise ValueError(art)


def mix(here, sfx, dauer):
    v, sr = sf.read(str(Path(here) / "assets/voice.wav"))
    if v.ndim > 1:
        v = v.mean(axis=1)
    assert sr == SR, sr
    out = np.zeros(max(len(v), int(dauer * SR)) + SR)
    out[: len(v)] += v / (np.abs(v).max() + 1e-9) * 0.9
    for zeit, art in sfx:
        s = _sfx(art) * 0.55
        i = int(zeit * SR)
        out[i: i + len(s)] += s[: len(out) - i]
    out = out[: int(dauer * SR)]
    out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write(str(Path(here) / "assets/mix.wav"), out, SR)


# ---------------- Bau ----------------
def build(here, szenen, sfx):
    here = Path(here)
    T = json.loads((here / "timings.json").read_text())
    dauer = T["dauer"]
    out, js = [], []
    for n, (a, b, html, code) in enumerate(szenen):
        d = round(b - a, 3)
        sid = f"z{n}"
        out.append(f'      <div id="{sid}" class="scene clip" data-start="{a}" data-duration="{d}" data-track-index="1"><div id="{sid}-i" class="inner">{html}</div></div>')
        js.append(f'      tl.fromTo("#{sid}-i", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {d}, ease: "none" }}, {a});')
        js.append(f"      {code(a, d)}")
    caps, n = [], 0
    for s in T["saetze"]:
        for cp in s["captions"]:
            n += 1
            words = cp["text"].split()
            L = sum(len(w) + 1 for w in words)
            cur, spans = cp["start"], []
            for k, w in enumerate(words):
                spans.append(f'<span id="w{n}-{k}">{w}</span> ')
                ende = cur + (cp["end"] - cp["start"]) * (len(w) + 1) / L
                js.append(f'      tl.fromTo("#w{n}-{k}", {{ color: "#ffffff", scale: 1 }}, {{ color: "{OR}", scale: 1.12, duration: 0.08 }}, {round(cur, 3)});')
                if k < len(words) - 1:
                    js.append(f'      tl.to("#w{n}-{k}", {{ color: "#ffffff", scale: 1, duration: 0.08 }}, {round(ende, 3)});')
                cur = ende
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{cp["start"]}" data-duration="{round(cp["end"] - cp["start"], 3)}" data-track-index="2">{"".join(spans)}</div>')
    mix(here, sfx, dauer)
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
      <div id="raster"></div>
{chr(10).join(out)}
      <div id="logo"><img src="assets/beagle.png" alt="" /></div>
      <div id="brand">HUNDEFINANZTV</div>
      <div id="frame"></div>
      <div id="captions" data-track-kind="captions">
{chr(10).join(caps)}
      </div>
      <audio id="voice" src="assets/mix.wav" data-start="0" data-duration="{dauer}" data-track-index="3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const pop = (sel, at) => tl.fromTo(sel, {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.2)" }}, at);
      const slam = (sel, at) => tl.fromTo(sel, {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.28, ease: "power4.in" }}, at);
      const shake = (sel, at) => tl.fromTo(sel, {{ x: -14 }}, {{ x: 14, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }}, at);
      const draw = (sel, at, dur) => {{
        const len = document.querySelector(sel).getTotalLength();
        tl.fromTo(sel, {{ strokeDasharray: len, strokeDashoffset: len }}, {{ strokeDashoffset: 0, duration: dur, ease: "power2.out" }}, at);
      }};
      const zaehl = (sel, von, bis, at, dur, nach) => {{
        const o = {{ v: von }};
        tl.fromTo(o, {{ v: von }}, {{ v: bis, duration: dur, ease: "power2.out", onUpdate: () => {{
          document.querySelector(sel).textContent = Math.round(o.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + (nach || ""); }} }}, at);
      }};
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (here / "index.html").write_text(html)
    print("index.html gebaut,", dauer, "s,", len(szenen), "Szenen,", len(sfx), "Sounds")
