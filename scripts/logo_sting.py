"""Logo-Intro nach dem Einstieg (Nutzer 18.11., Vorbild Finanzbär): Beagle-Logo knallt in die Mitte,
rutscht nach links, „HundeFinanzTv“ fährt von rechts rein, darunter „GELD | BÖRSE | NEWS“.

  import logo_sting as ls
  html, code = ls.szene(querformat=False)          # Szene für SZENEN: (t0, t0+ls.DAUER, html, code)
  SFX += ls.sounds(t0)
Das Dauer-Logo oben wird während der Szene automatisch ausgeblendet.
"""
DAUER = 3.0
TAG = "GELD <i>|</i> BÖRSE <i>|</i> NEWS"


def szene(querformat=False):
    if querformat:  # 1920×1080
        L, cy, lg, fn, ft, nx, w = 380, 540, 300, 112, 50, 720, 1920
    else:           # 1080×1920
        L, cy, lg, fn, ft, nx, w = 50, 880, 250, 80, 42, 320, 1080
    mitte = (w - lg) / 2
    html = f"""<style>
#ls-bg {{ position:absolute; inset:0; background: radial-gradient(ellipse at 50% {cy / (1080 if querformat else 1920) * 100:.0f}%, #ff8a1f55 0%, #ff8a1f14 30%, transparent 60%), #0e1012; z-index:7; }}
#ls-ring {{ position:absolute; left:{mitte - 40}px; top:{cy - lg / 2 - 40}px; width:{lg + 80}px; height:{lg + 80}px; border-radius:50%; border:6px solid #ff8a1f; z-index:8; }}
#ls-logo {{ position:absolute; left:{mitte}px; top:{cy - lg / 2}px; width:{lg}px; height:{lg}px; border-radius:50%; overflow:hidden;
  border:8px solid #DB8622; box-shadow:0 0 70px #ff8a1fbb, 0 20px 40px #000; z-index:9; }}
#ls-logo img {{ width:100%; height:100%; object-fit:cover; }}
#ls-txt {{ position:absolute; left:{nx}px; top:{cy - fn * 0.78}px; z-index:9; clip-path: inset(0 0 0 0); }}
#ls-name {{ font-weight:900; font-size:{fn}px; line-height:1; color:#fff; letter-spacing:-1px; white-space:nowrap; text-shadow:0 0 40px #0008; }}
#ls-name b {{ color:#ff8a1f; text-shadow:0 0 40px #ff8a1faa; }}
#ls-tag {{ margin-top:{fn * 0.22:.0f}px; font-weight:900; font-size:{ft}px; color:#ff8a1f; letter-spacing:2px; white-space:nowrap; }}
#ls-tag i {{ font-style:normal; color:#ffffffcc; padding:0 6px; }}
</style>
<div id="ls-bg"></div><div id="ls-ring"></div>
<div id="ls-logo"><img src="assets/beagle.png" alt="" /></div>
<div id="ls-txt"><div id="ls-name">HundeFinanz<b>Tv</b></div><div id="ls-tag">{TAG}</div></div>"""
    dx = L - mitte

    def code(a, d):
        return f"""tl.set(["#logo", "#brand"], {{ opacity: 0 }}, {a}); tl.set(["#logo", "#brand"], {{ opacity: 1 }}, {a + d});
      tl.fromTo("#ls-logo", {{ scale: 0, rotation: -25 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2.4)" }}, {a});
      flash({a + 0.12}, 0.35);
      tl.fromTo("#ls-ring", {{ scale: 0.6, opacity: 1 }}, {{ scale: 1.7, opacity: 0, duration: 0.7, ease: "power2.out" }}, {a + 0.15});
      tl.fromTo(["#ls-logo", "#ls-ring"], {{ x: 0 }}, {{ x: {dx}, duration: 0.5, ease: "power3.inOut" }}, {a + 0.75});
      tl.fromTo("#ls-txt", {{ x: 260, opacity: 0, clipPath: "inset(0 0 0 100%)" }}, {{ x: 0, opacity: 1, clipPath: "inset(0 0 0 0%)", duration: 0.55, ease: "power3.out" }}, {a + 0.9});
      tl.fromTo("#ls-tag", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power2.out" }}, {a + 1.35});
      tl.fromTo("#ls-bg", {{ scale: 1 }}, {{ scale: 1.08, duration: {d}, ease: "none" }}, {a});
      tl.to(["#ls-logo", "#ls-txt"], {{ scale: 1.02, duration: 1.2, ease: "none" }}, {a + 1.4});
      tl.to(["#ls-logo", "#ls-txt"], {{ opacity: 0, duration: 0.2 }}, {a + d - 0.2});"""
    return html, code


def sounds(t0):
    return [(t0 + 0.05, "mm-bumm"), (t0 + 0.8, "mm-wusch")]


def einfuegen(here, ab=30.0):
    """Nach sync.py aufrufen: Pause von DAUER s an der ersten Satzgrenze ab `ab` Sekunden in voice.wav + timings.json.
    Gibt die Startzeit des Logo-Intros zurück (für SZENEN/SFX). Mehrfach-Aufruf sicher (Merker in timings.json)."""
    import json
    from pathlib import Path
    import numpy as np, soundfile as sf
    here = Path(here); tp = here / "timings.json"; T = json.loads(tp.read_text())
    if "logo_intro" in T:
        return T["logo_intro"]
    t0 = next((s["end"] for s in T["saetze"] if s["end"] >= ab), T["saetze"][-1]["end"])
    vp = here / "assets/voice.wav"; a, sr = sf.read(str(vp))
    i = int(t0 * sr); stille = np.zeros((int(DAUER * sr),) + a.shape[1:])
    sf.write(str(vp), np.concatenate([a[:i], stille, a[i:]]), sr)
    for s in T["saetze"]:
        if s["start"] >= t0 - 1e-3:
            s["start"] = round(s["start"] + DAUER, 3); s["end"] = round(s["end"] + DAUER, 3)
            for c in s["captions"]:
                c["start"] = round(c["start"] + DAUER, 3); c["end"] = round(c["end"] + DAUER, 3)
    T["dauer"] = round(T["dauer"] + DAUER, 3); T["logo_intro"] = t0
    tp.write_text(json.dumps(T, ensure_ascii=False, indent=1))
    return t0
