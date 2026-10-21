#!/usr/bin/env python3
"""Baut index.html aus timings.json (Szenen + Untertitel + Voiceover)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
T = json.loads((HERE / "timings.json").read_text())
S = {s["id"]: s for s in T["saetze"]}
DAUER = T["dauer"]


def st(i):
    return S[i]["start"]


def en(i):
    return S[i]["end"]


BEAGLE = '<img src="assets/beagle.png" alt="" style="width:100%;height:100%;object-fit:contain" />'

# (id, von-Satz, bis-Satz, html, js)  -- js nutzt t0 = Szenenstart
SCENES = [
    ("geldsack", "s1", "s1", """
        <div id="geldsack-art" class="art"><svg viewBox="0 0 400 400">
          <g transform="translate(0,45) scale(0.9)" style="transform-origin:200px 200px"><g id="geldsack-coins" fill="#f2c418" stroke="#c99a06" stroke-width="3">
            <rect x="250" y="300" width="110" height="22" rx="8" /><rect x="250" y="276" width="110" height="22" rx="8" />
            <rect x="250" y="252" width="110" height="22" rx="8" /><rect x="250" y="228" width="110" height="22" rx="8" />
            <rect x="250" y="204" width="110" height="22" rx="8" /><rect x="265" y="180" width="110" height="22" rx="8" />
          </g>
          <g id="geldsack-bag">
            <path d="M150 110 C120 70 140 50 160 70 C175 50 205 50 220 70 C240 50 260 70 230 110 Z" fill="#1f7a4d" />
            <rect x="145" y="104" width="90" height="18" rx="9" fill="#f2c418" />
            <path d="M150 120 C60 170 40 330 120 340 L260 340 C340 330 320 170 230 120 Z" fill="#1f7a4d" />
            <path d="M155 135 C90 180 75 300 125 325" fill="none" stroke="#2c9a63" stroke-width="10" stroke-linecap="round" />
            <circle cx="190" cy="245" r="62" fill="#f2c418" />
            <text x="190" y="272" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="80" fill="#1f7a4d">€</text>
          </g></g>
          <text id="geldsack-100" x="190" y="62" text-anchor="middle" class="serif" font-size="68" fill="#111">100€</text>
        </svg></div>""", """
      pop("#geldsack-art", t0);
      tl.fromTo("#geldsack-coins", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, t0 + 0.2);
      pop("#geldsack-100", t0 + 0.5);
      drift("#geldsack-bag", t0 + 0.4, d - 0.4);"""),

    ("achtung", "s2", "s2", """
        <div class="art" style="position:relative">
          <div id="achtung-dog" style="position:absolute;left:110px;top:120px;width:600px;height:600px">""" + BEAGLE + """</div>
          <svg id="achtung-mark" viewBox="0 0 120 200" style="position:absolute;left:640px;top:60px;width:150px;height:250px">
            <rect x="35" y="10" width="50" height="120" rx="25" fill="var(--brand)" />
            <circle cx="60" cy="170" r="27" fill="var(--brand)" />
          </svg>
        </div>""", """
      pop("#achtung-dog", t0);
      tl.fromTo("#achtung-mark", { y: -40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "back.out(2.5)" }, t0 + 0.25);
      tl.fromTo("#achtung-mark", { rotation: 0 }, { rotation: 8, duration: 0.08, yoyo: true, repeat: 3, ease: "none" }, t0 + 0.6);"""),

    ("vergleich", "s3", "s5", """
        <div class="cmp">
          <div id="vgl-h1" style="grid-column:1"><div class="head">Konto</div><div class="sub">0 %</div></div>
          <div id="vgl-div" class="divider"></div>
          <div id="vgl-h2" style="grid-column:3"><div class="head">ETF</div><div class="sub">~7 %</div></div>
          <div id="vgl-a1" class="arrow" style="grid-column:1">
            <svg viewBox="0 0 70 110"><path d="M40 6 C10 30 8 70 40 98" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" /><path d="M24 92 L42 100 L44 80" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </div>
          <div id="vgl-a2" class="arrow" style="grid-column:3">
            <svg viewBox="0 0 70 110"><path d="M30 6 C60 30 62 70 30 98" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" /><path d="M46 92 L28 100 L26 80" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </div>
          <div id="vgl-n1" class="num green" style="grid-column:1">36.000€</div>
          <div style="grid-column:3">
            <div id="vgl-n2" class="num gold">113.000€</div>
          </div>
        </div>""", """
      pop("#vgl-h1", t0);
      tl.fromTo("#vgl-div", { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: "power2.out", transformOrigin: "top" }, t0 + 0.1);
      pop("#vgl-a1", t0 + 0.6);
      pop("#vgl-n1", %(s3n)s);
      pop("#vgl-h2", %(s4)s);
      pop("#vgl-a2", %(s4)s + 1.2);
      pop("#vgl-n2", %(s5)s + 0.2);
      tl.fromTo("#vgl-n2", { scale: 1 }, { scale: 1.12, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }, %(s5)s + 0.7);"""),

    ("balken", "s6", "s6", """
        <div class="art"><svg viewBox="0 0 400 400">
          <line x1="40" y1="350" x2="370" y2="350" stroke="#111" stroke-width="6" />
          <rect id="balken-1" x="80" y="275" width="100" height="75" fill="#1f7a4d" />
          <rect id="balken-2" x="230" y="115" width="100" height="235" fill="#f2c418" />
          <text x="130" y="262" text-anchor="middle" class="serif" font-size="30" fill="#1f7a4d" id="balken-l1">36.000€</text>
          <text x="280" y="102" text-anchor="middle" class="serif" font-size="30" fill="#c99a06" id="balken-l2">113.000€</text>
          <text id="balken-x3" x="200" y="60" text-anchor="middle" class="serif" font-size="70" fill="var(--brand)">x3</text>
        </svg></div>""", """
      tl.fromTo("#balken-1", { attr: { y: 350, height: 0 } }, { attr: { y: 275, height: 75 }, duration: 0.4, ease: "power2.out" }, t0);
      tl.fromTo("#balken-2", { attr: { y: 350, height: 0 } }, { attr: { y: 115, height: 235 }, duration: 0.7, ease: "power2.out" }, t0 + 0.3);
      pop("#balken-l1", t0 + 0.3);
      pop("#balken-l2", t0 + 0.9);
      pop("#balken-x3", t0 + 1.2);"""),

    ("zins", "s7", "s7", """
        <div class="art"><svg viewBox="0 0 400 400">
          <path d="M40 40 L40 340 L370 340" fill="none" stroke="#111" stroke-width="8" stroke-linecap="square" />
          <path id="zins-solid" d="M60 300 C140 290 220 285 300 270" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" />
          <path id="zins-dots" d="M60 295 C170 270 240 200 300 95" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 16" />
          <text id="zins-label" class="serif" x="70" y="100" font-size="70" fill="#1f7a4d">~7%</text>
          <g id="zins-check"><circle cx="320" cy="80" r="42" fill="#111" />
            <path d="M300 82 L315 97 L342 66" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></g>
        </svg></div>""", """
      draw("#zins-solid", t0, 0.6);
      tl.fromTo("#zins-dots", { opacity: 0 }, { opacity: 1, duration: 0.5 }, t0 + 0.4);
      pop("#zins-label", t0 + 0.7);
      pop("#zins-check", t0 + 1.0);"""),

    ("arbeitet", "s8", "s8", """
        <div class="art"><svg viewBox="0 0 400 400">
          <g id="arbeitet-g1"><circle cx="120" cy="130" r="58" fill="none" stroke="#353a3d" stroke-width="26" stroke-dasharray="22 14" />
            <circle cx="120" cy="130" r="30" fill="#353a3d" /></g>
          <g id="arbeitet-g2"><circle cx="300" cy="120" r="42" fill="none" stroke="#9aa3a8" stroke-width="22" stroke-dasharray="18 12" />
            <circle cx="300" cy="120" r="20" fill="#9aa3a8" /></g>
          <g id="arbeitet-coin"><circle cx="200" cy="260" r="100" fill="#f2c418" stroke="#c99a06" stroke-width="8" />
            <text x="200" y="300" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="120" fill="#c99a06">€</text></g>
        </svg></div>""", """
      pop("#arbeitet-coin", t0);
      tl.fromTo("#arbeitet-g1", { rotation: 0 }, { rotation: 120, duration: d, ease: "none", svgOrigin: "120 130" }, t0);
      tl.fromTo("#arbeitet-g2", { rotation: 0 }, { rotation: -160, duration: d, ease: "none", svgOrigin: "300 120" }, t0);
      pop("#arbeitet-g1", t0 + 0.15);
      pop("#arbeitet-g2", t0 + 0.3);"""),

    ("schlaf", "s9", "s9", """
        <div class="art"><svg viewBox="0 0 400 400">
          <circle cx="200" cy="200" r="170" fill="#353a3d" />
          <path id="schlaf-moon" d="M230 90 A110 110 0 1 0 300 280 A90 90 0 1 1 230 90 Z" fill="#f2c418" />
          <g fill="#fff"><circle id="schlaf-st1" cx="110" cy="120" r="7" /><circle id="schlaf-st2" cx="300" cy="140" r="5" /><circle id="schlaf-st3" cx="140" cy="300" r="5" /></g>
          <text id="schlaf-z" x="225" y="130" font-family="Montserrat" font-weight="800" font-size="46" fill="#fff">Zzz</text>
        </svg></div>""", """
      pop("#schlaf-moon", t0);
      tl.fromTo(["#schlaf-st1", "#schlaf-st2", "#schlaf-st3"], { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.15 }, t0 + 0.2);
      tl.fromTo("#schlaf-z", { y: 20, opacity: 0 }, { y: -20, opacity: 1, duration: d - 0.5, ease: "sine.out" }, t0 + 0.4);"""),

    ("outro", "s10", "s10", """
        <div style="display:flex;flex-direction:column;align-items:center;gap:30px">
          <div id="outro-dog" style="width:560px;height:560px">""" + BEAGLE + """</div>
          <div id="outro-name" style="font-family:Montserrat;font-weight:800;font-size:92px;color:#111">HundeFinanzTV</div>
          <div id="outro-btn" style="padding:18px 64px;border-radius:60px;background:var(--brand);color:#fff;font-family:Montserrat;font-weight:700;font-size:56px">+ Folgen</div>
        </div>""", """
      pop("#outro-dog", t0);
      pop("#outro-name", t0 + 0.25);
      pop("#outro-btn", t0 + 0.5);
      tl.fromTo("#outro-btn", { scale: 1 }, { scale: 1.08, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }, t0 + 1.1);"""),
]


def build():
    tpl = (HERE / "index.html").read_text()
    head = tpl[: tpl.index("<body>")]
    scenes_html, js = [], []
    for sid, a, b, html, code in SCENES:
        t0, t1 = st(a), en(b)
        if b == "s10":
            t1 = DAUER
        scenes_html.append(
            f'      <div id="{sid}" class="scene clip" data-start="{t0}" data-duration="{round(t1 - t0, 3)}" data-track-index="1">{html}\n      </div>'
        )
        vals = {"s3n": S["s3"]["captions"][1]["start"] + 0.6, "s4": st("s4"), "s5": st("s5")}
        js.append(f"      // {sid}\n      (() => {{ const t0 = {t0}, d = {round(t1 - t0, 3)};{code % vals if '%(' in code else code}\n      }})();")
    caps = []
    n = 0
    for s in T["saetze"]:
        for c in s["captions"]:
            n += 1
            caps.append(
                f'        <div id="c{n}" class="cap clip" data-start="{c["start"]}" data-duration="{round(c["end"] - c["start"], 3)}" data-track-index="2"><span>{c["text"]}</span></div>'
            )
    body = f"""<body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DAUER}" data-width="1080" data-height="1920">
{chr(10).join(scenes_html)}

      <div id="brand"><div id="brand-dog">{BEAGLE}</div><span>HundeFinanzTV</span></div>
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
      const drift = (sel, at, dur) =>
        tl.fromTo(sel, {{ scale: 1 }}, {{ scale: 1.05, duration: dur, ease: "sine.inOut" }}, at);
      const draw = (sel, at, dur) => {{
        const len = document.querySelector(sel).getTotalLength();
        tl.fromTo(sel, {{ strokeDasharray: len, strokeDashoffset: len }}, {{ strokeDashoffset: 0, duration: dur, ease: "power2.out" }}, at);
      }};

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
