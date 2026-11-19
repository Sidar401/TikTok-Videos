"""Novaro-Intro „Umlaufbahn“ (Nutzer 19.11.: „das dritte nehmen wir ab sofort“) – 3 s nach dem 2. Satz.
Logo (avatar.png) ploppt in die Mitte, goldene Umlaufbahn zeichnet sich, kleiner Mond kreist,
„Novaro“ + „WELTALL | PLANETEN | WISSEN“ fahren darunter ein. Stimme pausiert solange.

1) Nach schnitt.py:   python3 wissen/kit/intro.py videos/<name>      -> Pause in voice.wav + words.json, druckt t0
2) szene.json:        "intro": t0   (sauber_bau.py baut es dann automatisch ein)
3) cues.json:         Sounds kommen automatisch dazu? Nein -> selbst eintragen: whoosh-tief t0 (0.22), pling-idee t0+0.45 (0.16)
Zeiten in szene.js über W(wort) verschieben sich automatisch mit (words.json)."""
import json, math, subprocess, sys
from pathlib import Path

DAUER = 3.0
CSS = """
#in-bg { position:absolute; inset:0; z-index:60; opacity:0; background:#000 url(assets/tex/stars_milky_way.jpg) center/cover; overflow:hidden; }
#in-bg::before { content:""; position:absolute; inset:0; background:rgba(0,0,0,.62); }
#in-st { position:absolute; inset:0; z-index:61; }
.in-orb { position:absolute; left:110px; top:700px; width:860px; height:300px; transform:rotate(-14deg); }
.in-orb .e { position:absolute; inset:0; border:3px solid rgba(255,210,63,.67); border-radius:50%; }
#in-o1 { z-index:1; } #in-o1 .e { clip-path: inset(0 0 50% 0); } #in-o2 { z-index:3; } #in-o2 .e { clip-path: inset(50% 0 0 0); }
#in-av { position:absolute; left:365px; top:575px; width:350px; height:350px; border-radius:50%; background:url(assets/avatar.png) center/cover; box-shadow:0 0 90px rgba(255,210,63,.55); z-index:2; }
.in-moon { position:absolute; left:0; top:0; width:56px; height:56px; margin:-28px 0 0 -28px; border-radius:50%; background:url(assets/tex/moon.jpg) center/200% 100%; box-shadow:inset -14px -8px 18px rgba(0,0,0,.8), 0 0 20px rgba(255,255,255,.27); }
#in-nm { position:absolute; left:0; right:0; top:1080px; text-align:center; font:900 128px "Inter Display", Inter, sans-serif; color:#fff; letter-spacing:2px; text-shadow:0 0 40px rgba(0,0,0,.6); }
#in-tg { position:absolute; left:0; right:0; top:1235px; text-align:center; font:600 36px Inter, sans-serif; color:#ffd23f; letter-spacing:3px; white-space:nowrap; }
#in-tg i { font-style:normal; color:rgba(255,255,255,.67); padding:0 10px; }
"""


def html(t0):
    return (f'<div id="in-box" class="clip" data-start="{t0}" data-duration="{DAUER}" data-track-index="9"><div id="in-bg"></div><div id="in-st">'
            '<div id="in-o1" class="in-orb"><div class="e"></div><div id="in-m1" class="in-moon"></div></div>'
            '<div id="in-av"></div><div id="in-o2" class="in-orb"><div class="e"></div><div id="in-m2" class="in-moon"></div></div><div id="in-nm">Novaro</div><div id="in-tg">WELTALL<i>|</i>PLANETEN<i>|</i>WISSEN</div></div></div>')


def js(t0):
    # Mond läuft auf der Ellipse (im gekippten Rahmen: Mitte 430/150, Radien 430/150); oben = hinter dem Logo
    n, pts = 36, []
    for i in range(n + 1):
        a = -0.15 - i / n * 2 * math.pi * 0.85       # startet rechts, läuft oben herum (hinten), dann unten (vorn)
        x, y = 430 + 430 * math.cos(a), 150 + 150 * math.sin(a)
        pts.append((x, y))
    k1 = ", ".join(f'{{ left: {x:.1f}, top: {y:.1f}, opacity: {1 if y < 150 else 0} }}' for x, y in pts)
    k2 = ", ".join(f'{{ left: {x:.1f}, top: {y:.1f}, opacity: {0 if y < 150 else 1} }}' for x, y in pts)
    return f"""
      tl.fromTo("#in-bg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.18 }}, {t0});
      tl.fromTo("#in-av", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.55, ease: "back.out(2.2)" }}, {t0 + 0.05});
      tl.fromTo(".in-orb", {{ opacity: 0, scale: 0.4, rotation: -14 }}, {{ opacity: 1, scale: 1, rotation: -14, duration: 0.6, ease: "expo.out" }}, {t0 + 0.3});
      tl.set("#in-m1", {{ left: 860, top: 150, opacity: 0 }}, {t0}); tl.set("#in-m2", {{ left: 860, top: 150, opacity: 1 }}, {t0});
      tl.to("#in-m1", {{ keyframes: [{k1}], duration: {DAUER - 0.4}, ease: "none" }}, {t0 + 0.3});
      tl.to("#in-m2", {{ keyframes: [{k2}], duration: {DAUER - 0.4}, ease: "none" }}, {t0 + 0.3});
      tl.fromTo("#in-nm", {{ opacity: 0, y: 60, clipPath: "inset(0 0 100% 0)" }}, {{ opacity: 1, y: 0, clipPath: "inset(0 0 0% 0)", duration: 0.55, ease: "power3.out" }}, {t0 + 0.6});
      tl.fromTo("#in-tg", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {t0 + 0.95});
      tl.fromTo("#in-st", {{ scale: 1 }}, {{ scale: 1.04, duration: {DAUER}, ease: "none" }}, {t0});
      tl.to(["#in-bg", "#in-st"], {{ opacity: 0, duration: 0.25 }}, {t0 + DAUER - 0.25});
"""


def apply(h, t0):
    h = h.replace("</style>", CSS + "</style>", 1)
    h = h.replace('<audio id="voice"', html(t0) + '\n      <audio id="voice"', 1)
    h = h.replace("      tl.to({}, { duration: 0.01 }", js(t0) + "      tl.to({}, { duration: 0.01 }", 1)
    return h


def einfuegen(proj, nach=2):
    """Pause von DAUER s nach Zeile `nach` (Chunk-Ende) in voice.wav + words.json. Mehrfach-Aufruf sicher."""
    proj = Path(proj); wp = proj / "words.json"; W = json.load(open(wp))
    if "intro" in W:
        return W["intro"]
    c_end, c_next = W["chunks"][nach - 1][1], W["chunks"][nach][0]
    t0 = round((c_end + c_next) / 2, 2)
    v = proj / "assets/voice.wav"; tmp = proj / "assets/voice-tmp.wav"
    f = f"[0]atrim=0:{t0},asetpts=N/SR/TB[a];[0]atrim={t0},asetpts=N/SR/TB[b];aevalsrc=0:d={DAUER}:s=44100[z];[a][z][b]concat=n=3:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-filter_complex", f, "-map", "[o]", "-ar", "44100", "-ac", "1", str(tmp)], check=True)
    tmp.replace(v)
    for w in W["words"]:
        if w["s"] >= t0: w["s"] = round(w["s"] + DAUER, 3); w["e"] = round(w["e"] + DAUER, 3)
    W["chunks"] = [[s + DAUER, e + DAUER] if s >= t0 else [s, e] for s, e in W["chunks"]]
    W["intro"] = t0
    json.dump(W, open(wp, "w"), ensure_ascii=False)
    return t0


if __name__ == "__main__":
    print("intro t0 =", einfuegen(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2))
