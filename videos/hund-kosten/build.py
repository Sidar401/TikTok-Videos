#!/usr/bin/env python3
"""HundeFinanzTV: Was kostet ein Hund wirklich? -> index.html (aus timings.json)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
T = json.loads((HERE / "timings.json").read_text())
S = {s["id"]: s for s in T["saetze"]}
DAUER = T["dauer"]


def c(sid, i):
    """Startzeit der i-ten Untertitel-Box eines Satzes."""
    return S[sid]["captions"][min(i, len(S[sid]["captions"]) - 1)]["start"]


BEAGLE = '<img src="assets/beagle.png" alt="" style="width:100%;height:100%;object-fit:contain" />'

# Napf voller Münzen (Hund + Geld)
BOWL = """<svg viewBox="0 0 400 300" style="width:100%;height:100%">
  <g fill="#f2c418" stroke="#c99a06" stroke-width="4">
    <ellipse cx="150" cy="120" rx="40" ry="16" /><ellipse cx="200" cy="105" rx="40" ry="16" /><ellipse cx="250" cy="120" rx="40" ry="16" />
    <ellipse cx="175" cy="90" rx="40" ry="16" /><ellipse cx="225" cy="85" rx="40" ry="16" /><ellipse cx="200" cy="65" rx="40" ry="16" />
  </g>
  <path d="M60 130 L340 130 L310 250 Q200 275 90 250 Z" fill="#DB8622" />
  <ellipse cx="200" cy="130" rx="140" ry="22" fill="#a8621a" />
  <g fill="#fff" opacity="0.9"><ellipse cx="200" cy="205" rx="22" ry="18" /><circle cx="175" cy="180" r="8" /><circle cx="192" cy="170" r="8" /><circle cx="210" cy="170" r="8" /><circle cx="226" cy="180" r="8" /></g>
</svg>"""

TILE = '<div id="{id}" class="tile"><svg viewBox="0 0 100 100">{svg}</svg><span>{label}</span></div>'
ICONS = [
    ("kosten-t1", "Futter", '<path d="M15 50 L85 50 L78 82 Q50 90 22 82 Z" fill="#DB8622" /><ellipse cx="50" cy="50" rx="35" ry="8" fill="#8a4a12" />'),
    ("kosten-t2", "Tierarzt", '<rect x="18" y="30" width="64" height="50" rx="8" fill="#e24b4b" /><rect x="38" y="20" width="24" height="14" rx="4" fill="none" stroke="#e24b4b" stroke-width="6" /><path d="M50 42 L50 70 M36 56 L64 56" stroke="#fff" stroke-width="9" stroke-linecap="round" />'),
    ("kosten-t3", "Versicherung", '<path d="M50 12 L82 24 Q82 66 50 88 Q18 66 18 24 Z" fill="#3d7be0" /><path d="M36 50 L46 60 L66 38" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />'),
    ("kosten-t4", "Hundesteuer", '<rect x="22" y="12" width="56" height="76" rx="6" fill="#f6efe1" stroke="#353a3d" stroke-width="5" /><text x="50" y="66" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#353a3d">§</text>'),
]

SCENES = [
    ("intro", "s1", "s1", """
        <div id="intro-title" style="position:absolute;top:290px;left:40px;width:1000px;text-align:center;font-family:Montserrat;font-weight:800;font-size:92px;line-height:1.05;color:#111">Was kostet dein<br /><span style="color:var(--brand)">Hund</span> wirklich?</div>
        <div id="intro-bowl" style="position:absolute;left:110px;top:600px;width:760px;height:570px">""" + BOWL + """</div>
        <div id="intro-q" class="serif" style="position:absolute;left:790px;top:520px;font-size:300px;line-height:1;color:#e24b4b">?</div>""",
     lambda t0, d: f"""
      tl.fromTo("#intro-title", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});
      tl.fromTo("#intro-bowl", {{ scale: 0.94 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});
      tl.fromTo("#intro-q", {{ rotation: -15, scale: 0.6 }}, {{ rotation: 10, scale: 1, duration: 0.5, ease: "back.out(2.5)" }}, {t0} + 0.3);"""),

    ("kosten", "s2", "s2", """
        <div style="position:absolute;left:90px;top:330px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:40px">"""
     + "".join(TILE.format(id=i, svg=s, label=l) for i, l, s in ICONS) + """
        </div>""",
     lambda t0, d: "".join(f'\n      pop("#{i}", {t0} + {k * 0.35:.2f});' for k, (i, _, _) in enumerate(ICONS))),

    ("monat", "s3", "s3", """
        <div class="art" style="position:absolute;left:130px;top:330px">
          <svg viewBox="0 0 400 400">
            <rect x="60" y="70" width="280" height="250" rx="22" fill="#fff" stroke="#353a3d" stroke-width="10" />
            <rect x="60" y="70" width="280" height="70" rx="22" fill="#DB8622" />
            <rect x="60" y="120" width="280" height="20" fill="#DB8622" />
            <rect x="110" y="45" width="18" height="50" rx="9" fill="#353a3d" /><rect x="272" y="45" width="18" height="50" rx="9" fill="#353a3d" />
            <text id="monat-num" x="200" y="265" text-anchor="middle" class="serif" font-size="96" fill="#111">100€</text>
          </svg>
        </div>
        <div id="monat-sub" class="serif" style="position:absolute;left:0;top:1170px;width:1080px;text-align:center;font-size:84px;color:#111">pro Monat</div>""",
     lambda t0, d: f"""
      pop("#monat .art", {t0});
      pop("#monat-num", {c('s3', 1)} - 0.4);
      pop("#monat-sub", {c('s3', 1)});"""),

    ("jahre", "s4", "s4", """
        <div style="position:absolute;left:0;top:360px;width:1080px;text-align:center" class="serif">
          <div id="jahre-a" style="font-size:120px;color:#111">13 Jahre</div>
          <div id="jahre-arrow" style="height:230px;display:flex;justify-content:center;align-items:center">
            <svg viewBox="0 0 70 110" style="width:120px;height:200px"><path d="M35 6 L35 96 M14 76 L35 100 L56 76" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </div>
          <div id="jahre-b" style="font-size:150px;color:#e24b4b">≈ 16.000€</div>
        </div>""",
     lambda t0, d: f"""
      pop("#jahre-a", {t0});
      pop("#jahre-arrow", {t0} + 0.4);
      pop("#jahre-b", {c('s4', 1)});
      tl.fromTo("#jahre-b", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {c('s4', 1)} + 0.45);"""),

    ("notfall", "s5", "s5", """
        <div class="art" style="position:absolute;left:130px;top:330px">
          <svg viewBox="0 0 400 400">
            <rect id="notfall-kit" x="70" y="130" width="260" height="200" rx="26" fill="#e24b4b" />
            <rect x="150" y="95" width="100" height="50" rx="14" fill="none" stroke="#e24b4b" stroke-width="16" />
            <path d="M200 175 L200 285 M145 230 L255 230" stroke="#fff" stroke-width="30" stroke-linecap="round" />
            <g id="notfall-bang"><circle cx="330" cy="110" r="48" fill="#f2c418" stroke="#111" stroke-width="5" /><rect x="321" y="76" width="18" height="44" rx="9" fill="#111" /><circle cx="330" cy="138" r="10" fill="#111" /></g>
          </svg>
        </div>
        <div id="notfall-plus" class="serif" style="position:absolute;left:0;top:1150px;width:1080px;text-align:center;font-size:84px;color:#e24b4b">+ Notfälle</div>""",
     lambda t0, d: f"""
      pop("#notfall .art", {t0});
      tl.fromTo("#notfall-bang", {{ rotation: -20, svgOrigin: "330 110" }}, {{ rotation: 20, duration: 0.1, yoyo: true, repeat: 5, ease: "none" }}, {t0} + 0.4);
      pop("#notfall-plus", {c('s5', 1)});"""),

    ("tipp", "s6", "s6", """
        <div id="tipp-head" style="position:absolute;top:300px;left:0;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:80px;color:var(--brand)">Mein Tipp</div>
        <div id="tipp-dog" style="position:absolute;left:40px;top:470px;width:480px;height:480px">""" + BEAGLE + """</div>
        <svg id="tipp-pig" viewBox="0 0 300 260" style="position:absolute;left:540px;top:560px;width:480px;height:416px">
          <ellipse cx="150" cy="150" rx="120" ry="90" fill="#f4a6b5" />
          <circle cx="250" cy="140" r="38" fill="#f4a6b5" /><ellipse cx="265" cy="140" rx="20" ry="16" fill="#e98a9c" />
          <circle cx="258" cy="136" r="4" fill="#8a3a4a" /><circle cx="272" cy="136" r="4" fill="#8a3a4a" />
          <circle cx="215" cy="110" r="7" fill="#111" /><path d="M200 70 L225 40 L235 80 Z" fill="#e98a9c" />
          <rect x="85" y="225" width="30" height="34" rx="10" fill="#e98a9c" /><rect x="180" y="225" width="30" height="34" rx="10" fill="#e98a9c" />
          <rect x="120" y="62" width="70" height="12" rx="6" fill="#8a3a4a" />
        </svg>
        <div id="tipp-coin" class="serif" style="position:absolute;left:740px;top:380px;width:150px;height:150px;border-radius:50%;background:#f2c418;border:8px solid #c99a06;display:flex;align-items:center;justify-content:center;font-size:56px;color:#7a5a00">100€</div>""",
     lambda t0, d: f"""
      pop("#tipp-head", {t0});
      pop("#tipp-dog", {t0} + 0.15);
      pop("#tipp-pig", {t0} + 0.4);
      tl.fromTo("#tipp-coin", {{ y: -120, opacity: 0 }}, {{ y: 120, opacity: 1, duration: 0.7, ease: "power2.in" }}, {c('s6', 1)});
      tl.fromTo("#tipp-coin", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.15 }}, {c('s6', 1)} + 0.7);
      tl.fromTo("#tipp-pig", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }}, {c('s6', 1)} + 0.7);"""),

    ("rendite", "s7", "s7", """
        <div class="art" style="position:absolute;left:130px;top:330px"><svg viewBox="0 0 400 400">
          <line x1="30" y1="350" x2="370" y2="350" stroke="#111" stroke-width="6" />
          <rect id="rendite-b1" x="70" y="200" width="110" height="150" fill="#1f7a4d" />
          <rect id="rendite-b2" x="220" y="118" width="110" height="232" fill="#f2c418" />
          <text id="rendite-l1" x="125" y="185" text-anchor="middle" class="serif" font-size="32" fill="#1f7a4d">15.600€</text>
          <text id="rendite-l2" x="275" y="103" text-anchor="middle" class="serif" font-size="32" fill="#c99a06">24.200€</text>
          <text x="125" y="385" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="22" fill="#353a3d">gespart</text>
          <text x="275" y="385" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="22" fill="#353a3d">mit ~7 %</text>
          <text id="rendite-plus" x="200" y="50" text-anchor="middle" class="serif" font-size="52" fill="var(--brand)">+8.600€</text>
        </svg></div>""",
     lambda t0, d: f"""
      tl.fromTo("#rendite-b1", {{ attr: {{ y: 350, height: 0 }} }}, {{ attr: {{ y: 200, height: 150 }}, duration: 0.5, ease: "power2.out" }}, {t0});
      pop("#rendite-l1", {t0} + 0.4);
      tl.fromTo("#rendite-b2", {{ attr: {{ y: 350, height: 0 }} }}, {{ attr: {{ y: 118, height: 232 }}, duration: 0.8, ease: "power2.out" }}, {c('s7', 1)} - 0.3);
      pop("#rendite-l2", {c('s7', 1)} + 0.5);
      pop("#rendite-plus", {c('s7', 1)} + 0.9);"""),

    ("selbst", "s8", "s8", """
        <div id="selbst-bowl" style="position:absolute;left:190px;top:450px;width:700px;height:525px">""" + BOWL + """</div>
        <svg id="selbst-check" viewBox="0 0 100 100" style="position:absolute;left:760px;top:360px;width:200px;height:200px"><circle cx="50" cy="50" r="46" fill="#1f7a4d" /><path d="M28 52 L44 68 L74 36" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>""",
     lambda t0, d: f"""
      pop("#selbst-bowl", {t0});
      pop("#selbst-check", {t0} + 0.5);"""),

    ("outro", "s9", "s9", """
        <div style="position:absolute;left:0;top:330px;width:1080px;display:flex;flex-direction:column;align-items:center;gap:30px">
          <div id="outro-dog" style="width:520px;height:520px">""" + BEAGLE + """</div>
          <div id="outro-name" style="font-family:Montserrat;font-weight:800;font-size:92px;color:#111">HundeFinanzTV</div>
          <div id="outro-btn" style="padding:18px 64px;border-radius:60px;background:var(--brand);color:#fff;font-family:Montserrat;font-weight:700;font-size:56px">+ Folgen</div>
        </div>""",
     lambda t0, d: f"""
      pop("#outro-dog", {t0});
      pop("#outro-name", {t0} + 0.25);
      pop("#outro-btn", {t0} + 0.5);
      tl.fromTo("#outro-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {t0} + 1.1);"""),
]

EXTRA_CSS = """
      .scene { position: absolute; inset: 0; top: 0; height: 1920px; display: block; }
      .tile { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 30px 10px; border-radius: 30px; background: #faf5ef; }
      .tile svg { width: 230px; height: 230px; }
      .tile span { font-family: Montserrat; font-weight: 800; font-size: 54px; color: #111; }
    </style>"""


def build():
    tpl = (HERE / "index.html").read_text()
    head = tpl[: tpl.index("<body>")]
    if ".tile {" not in head:
        head = head.replace("    </style>", EXTRA_CSS, 1)
    scenes, js, caps = [], [], []
    last = T["saetze"][-1]["id"]
    for sid, a, b, html, code in SCENES:
        t0 = S[a]["start"]
        t1 = DAUER if b == last else S[b]["end"]
        d = round(t1 - t0, 3)
        scenes.append(f'      <div id="{sid}" class="scene clip" data-start="{t0}" data-duration="{d}" data-track-index="1">{html}\n      </div>')
        js.append(f"      // {sid}\n      (() => {{{code(t0, d)}\n      }})();")
    n = 0
    for s in T["saetze"]:
        for cp in s["captions"]:
            n += 1
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{cp["start"]}" data-duration="{round(cp["end"] - cp["start"], 3)}" data-track-index="2"><span>{cp["text"]}</span></div>')
    body = f"""<body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DAUER}" data-width="1080" data-height="1920">
{chr(10).join(scenes)}

      <div id="brand"><span>HundeFinanzTV</span></div>
      <div id="frame"></div>

      <div id="captions" data-track-kind="captions">
{chr(10).join(caps)}
      </div>

      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DAUER}" data-track-index="3"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      const pop = (sel, at) =>
        tl.fromTo(sel, {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, at);

{chr(10).join(js)}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (HERE / "index.html").write_text(head + body)
    print("index.html gebaut,", DAUER, "s")


if __name__ == "__main__":
    build()
