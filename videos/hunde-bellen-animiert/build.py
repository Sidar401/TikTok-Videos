#!/usr/bin/env python3
"""HundeWissenTv animiert: eigene Grafiken zum Inhalt + Voiceover -> index.html."""
import json
from pathlib import Path

HERE = Path(__file__).parent
T = json.loads((HERE / "timings.json").read_text())
S = {s["id"]: s for s in T["saetze"]}
DAUER = T["dauer"]


def c(sid, i):
    """Startzeit der i-ten Untertitel-Box eines Satzes."""
    return S[sid]["captions"][i]["start"]


BEAGLE = '<img src="assets/beagle.png" alt="" style="width:100%;height:100%;object-fit:contain" />'

# Einfacher Hund (Seitenansicht), fill über currentColor
DOG = """<g fill="currentColor">
  <path d="M38 96 Q10 70 22 40" fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round" />
  <ellipse cx="110" cy="100" rx="78" ry="40" />
  <rect x="52" y="112" width="20" height="70" rx="9" /><rect x="80" y="116" width="20" height="66" rx="9" />
  <rect x="135" y="116" width="20" height="66" rx="9" /><rect x="162" y="112" width="20" height="70" rx="9" />
  <path d="M160 80 L190 40 L222 58 L186 110 Z" />
  <circle cx="208" cy="48" r="32" />
  <ellipse cx="240" cy="60" rx="30" ry="17" />
  <circle cx="268" cy="56" r="8" fill="#111" />
  <path d="M190 30 Q172 52 184 84 Q198 70 200 40 Z" fill="#000" opacity="0.35" />
  <circle cx="214" cy="40" r="5" fill="#fff" />
</g>"""

def dog_svg(color="#8a4a12", flip=False):
    """Gezeichneter Hund als eigenständiges SVG (füllt seinen Container)."""
    t = ' transform="translate(290 0) scale(-1 1)"' if flip else ""
    return f'<svg viewBox="0 -20 290 210" style="width:100%;height:100%;color:{color}"><g{t}>{DOG}</g></svg>'


PAW = """<svg viewBox="0 0 100 100" style="width:100%;height:100%"><g fill="#fff"><ellipse cx="50" cy="66" rx="24" ry="20" /><circle cx="24" cy="40" r="10" /><circle cx="40" cy="24" r="10" /><circle cx="60" cy="24" r="10" /><circle cx="76" cy="40" r="10" /></g></svg>"""

PERSON = """<g fill="currentColor"><circle cx="50" cy="28" r="22" /><path d="M14 130 Q14 62 50 58 Q86 62 86 130 Z" /></g>"""


def header(sid, text):
    return f'<div id="{sid}-head" class="head">{text}</div>'


SCENES = [
    ("intro", "s1", "s1", """
        <div class="stage">
          <div id="intro-dog" style="position:absolute;left:230px;top:180px;width:620px;height:620px">""" + BEAGLE + """</div>
          <div id="intro-bubble" class="bubble" style="left:640px;top:70px">WUFF!</div>
          <div id="intro-five" class="big" style="position:absolute;left:0;top:750px;width:1080px;text-align:center"><span class="orange">5</span> Gründe</div>
        </div>""", lambda t0, d: f"""
      pop("#intro-dog", {t0});
      pop("#intro-bubble", {t0} + 0.4);
      tl.fromTo("#intro-bubble", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.12, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {t0} + 0.75);
      pop("#intro-five", {c('s1', 2)});"""),

    ("revier", "s2", "s2", header("revier", "Grund 1: Revier") + """
        <div class="stage"><svg viewBox="0 0 1080 900" style="width:1080px;height:900px">
          <ellipse id="revier-zone" cx="400" cy="560" rx="330" ry="250" fill="#fdf1e3" stroke="#DB8622" stroke-width="8" stroke-dasharray="26 18" />
          <g id="revier-house">
            <rect x="250" y="380" width="300" height="230" fill="#f6efe1" stroke="#353a3d" stroke-width="8" />
            <path d="M220 395 L400 250 L580 395 Z" fill="#DB8622" stroke="#353a3d" stroke-width="8" stroke-linejoin="round" />
            <rect x="370" y="490" width="70" height="120" fill="#8a5a2b" />
          </g>
          <g transform="translate(560 560) scale(1.1)"><g id="revier-dog" style="color:#8a4a12">""" + DOG + """</g></g>
          <g transform="translate(840 440) scale(1.6)"><g id="revier-person" style="color:#353a3d">""" + PERSON + """</g></g>
          <g id="revier-alarm"><circle cx="760" cy="380" r="46" fill="#e24b4b" /><rect x="752" y="345" width="16" height="44" rx="8" fill="#fff" /><circle cx="760" cy="405" r="9" fill="#fff" /></g>
        </svg></div>""", lambda t0, d: f"""
      pop("#revier-head", {t0});
      pop("#revier-house", {t0} + 0.2);
      tl.fromTo("#revier-zone", {{ opacity: 0, scale: 0.8, svgOrigin: "400 560" }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {t0} + 0.5);
      pop("#revier-dog", {t0} + 0.8);
      tl.fromTo("#revier-person", {{ x: 200, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 1.4, ease: "power1.out" }}, {c('s2', 2)});
      pop("#revier-alarm", {c('s2', 3)});
      tl.fromTo("#revier-dog", {{ y: 0 }}, {{ y: -18, duration: 0.12, yoyo: true, repeat: 5, ease: "sine.out" }}, {c('s2', 3)} + 0.2);"""),

    ("angst", "s3", "s3", header("angst", "Grund 2: Angst") + """
        <div class="stage">
          <svg id="angst-cloud" viewBox="0 0 400 260" style="position:absolute;left:290px;top:40px;width:500px;height:325px">
            <path d="M80 190 Q20 190 30 140 Q30 95 85 95 Q100 40 165 45 Q220 20 260 70 Q330 60 340 120 Q385 135 365 180 Q355 195 320 195 Z" fill="#5d666b" />
            <path id="angst-bolt" d="M200 170 L160 250 L205 240 L180 320 L260 215 L215 225 L240 170 Z" fill="#f2c418" />
          </svg>
          <div id="angst-dog" style="position:absolute;left:240px;top:420px;width:600px;height:430px">""" + dog_svg() + """</div>
          <svg viewBox="0 0 100 100" style="position:absolute;left:770px;top:420px;width:90px;height:90px"><path id="angst-drop" d="M50 10 Q80 55 70 75 Q50 98 30 75 Q20 55 50 10 Z" fill="#6fb7e6" /></svg>
        </div>""", lambda t0, d: f"""
      pop("#angst-head", {t0});
      pop("#angst-cloud", {t0} + 0.2);
      tl.fromTo("#angst-bolt", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, yoyo: true, repeat: 5 }}, {c('s3', 1)});
      pop("#angst-dog", {t0} + 0.4);
      tl.fromTo("#angst-dog", {{ x: -8 }}, {{ x: 8, duration: 0.07, yoyo: true, repeat: 15, ease: "none" }}, {c('s3', 1)} + 0.2);
      tl.fromTo("#angst-drop", {{ y: -20, opacity: 0 }}, {{ y: 30, opacity: 1, duration: 0.8, ease: "power1.in" }}, {c('s3', 2)});"""),

    ("aufmerksam", "s4", "s4", header("aufmerksam", "Grund 3: Aufmerksamkeit") + """
        <div class="stage">
          <div id="auf-dog" style="position:absolute;left:60px;top:240px;width:500px;height:360px">""" + dog_svg() + """</div>
          <div id="auf-bubble" class="bubble" style="left:520px;top:140px">Hey!<br />Schau mich an!</div>
          <div id="auf-chain" style="position:absolute;left:0;top:720px;width:1080px;display:flex;justify-content:center;align-items:center;gap:30px">
            <div class="chip">WUFF</div>
            <svg viewBox="0 0 80 40" style="width:110px;height:55px"><path d="M5 20 L65 20 M50 6 L68 20 L50 34" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg>
            <div class="chip" style="background:#1f7a4d">Belohnung</div>
            <svg id="auf-check" viewBox="0 0 100 100" style="width:110px;height:110px"><circle cx="50" cy="50" r="46" fill="#111" /><path d="M28 52 L44 68 L74 36" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </div>
        </div>""", lambda t0, d: f"""
      pop("#aufmerksam-head", {t0});
      pop("#auf-dog", {t0} + 0.2);
      pop("#auf-bubble", {t0} + 0.5);
      pop("#auf-chain", {c('s4', 1)});
      pop("#auf-check", {c('s4', 2)});"""),

    ("langeweile", "s5", "s5", header("langeweile", "Grund 4: Langeweile") + """
        <div class="stage">
          <svg viewBox="0 0 400 400" style="position:absolute;left:340px;top:30px;width:400px;height:400px">
            <circle cx="200" cy="200" r="180" fill="#fff" stroke="#353a3d" stroke-width="18" />
            <g fill="#353a3d"><rect x="194" y="34" width="12" height="30" /><rect x="194" y="336" width="12" height="30" /><rect x="34" y="194" width="30" height="12" /><rect x="336" y="194" width="30" height="12" /></g>
            <rect id="lw-min" x="194" y="70" width="12" height="135" rx="6" fill="#DB8622" />
            <rect id="lw-hour" x="192" y="115" width="16" height="90" rx="8" fill="#353a3d" />
            <circle cx="200" cy="200" r="14" fill="#353a3d" />
          </svg>
          <div id="lw-row" style="position:absolute;left:0;top:500px;width:1080px;display:flex;justify-content:center;align-items:center;gap:40px">
            <div style="width:360px;height:260px">""" + dog_svg() + """</div>
            <div class="big">=</div>
            <svg viewBox="0 0 100 135" style="width:230px;height:310px;color:#353a3d">""" + PERSON + """</svg>
          </div>
          <div id="lw-z" class="big" style="position:absolute;left:800px;top:300px;color:#9aa3a8">Zzz</div>
        </div>""", lambda t0, d: f"""
      pop("#langeweile-head", {t0});
      tl.fromTo("#lw-min", {{ rotation: 0 }}, {{ rotation: 1080, duration: {d}, ease: "none", svgOrigin: "200 200" }}, {t0});
      tl.fromTo("#lw-hour", {{ rotation: 0 }}, {{ rotation: 90, duration: {d}, ease: "none", svgOrigin: "200 200" }}, {t0});
      pop("#lw-row", {c('s5', 1)});
      tl.fromTo("#lw-z", {{ y: 20, opacity: 0 }}, {{ y: -30, opacity: 1, duration: 1.4, ease: "sine.out" }}, {c('s5', 2)});"""),

    ("auslastung", "s6", "s6", header("auslastung", "Fehlende Auslastung") + """
        <div class="stage" style="display:flex;flex-direction:column;justify-content:center;gap:90px;padding:0 120px">
          <div class="meter"><div class="label">Kopf</div><div class="bar"><div id="al-b1" class="fill"></div></div></div>
          <div class="meter"><div class="label">Körper</div><div class="bar"><div id="al-b2" class="fill"></div></div></div>
        </div>""", lambda t0, d: f"""
      pop("#auslastung-head", {t0});
      tl.fromTo("#al-b1", {{ scaleX: 0 }}, {{ scaleX: 0.2, duration: 0.8, ease: "power2.out", transformOrigin: "0 50%" }}, {t0} + 0.4);
      tl.fromTo("#al-b2", {{ scaleX: 0 }}, {{ scaleX: 0.15, duration: 0.8, ease: "power2.out", transformOrigin: "0 50%" }}, {c('s6', 1)});"""),

    ("frust", "s7", "s7", header("frust", "Grund 5: Frustration") + """
        <div class="stage"><svg viewBox="0 0 1080 900" style="width:1080px;height:900px">
          <g transform="translate(270 330) scale(2.2)"><g id="frust-dog" style="color:#8a4a12">""" + DOG + """</g></g>
          <g fill="#c9a06a" stroke="#8a6a3a" stroke-width="5">
            <rect x="130" y="560" width="820" height="34" /><rect x="130" y="680" width="820" height="34" />
            <path d="M150 760 L150 500 L180 470 L210 500 L210 760 Z M290 760 L290 500 L320 470 L350 500 L350 760 Z M430 760 L430 500 L460 470 L490 500 L490 760 Z M570 760 L570 500 L600 470 L630 500 L630 760 Z M710 760 L710 500 L740 470 L770 500 L770 760 Z M850 760 L850 500 L880 470 L910 500 L910 760 Z" />
          </g>
          <g id="frust-steam" fill="#e24b4b"><circle cx="760" cy="230" r="34" /><circle cx="810" cy="185" r="26" /><circle cx="850" cy="145" r="18" /></g>
          <g transform="translate(900 300) scale(1.2)"><g id="frust-person" style="color:#353a3d">""" + PERSON + """
            <g fill="#e24b4b"><circle cx="85" cy="-10" r="14" /><circle cx="105" cy="-35" r="9" /></g></g></g>
        </svg></div>""", lambda t0, d: f"""
      pop("#frust-head", {t0});
      pop("#frust-dog", {t0} + 0.2);
      tl.fromTo("#frust-steam", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }}, {t0} + 0.8);
      tl.fromTo("#frust-steam", {{ scale: 1, svgOrigin: "800 190" }}, {{ scale: 1.15, duration: 0.25, yoyo: true, repeat: 5 }}, {t0} + 1.2);
      pop("#frust-person", {c('s7', 1)});"""),

    ("leine", "s8", "s8", header("leine", "Beispiel: an der Leine") + """
        <div class="stage">
          <svg viewBox="0 0 1080 900" style="position:absolute;inset:0;width:1080px;height:900px">
            <path id="leine-line" d="M150 120 C220 300 330 420 450 470" fill="none" stroke="#8a4a12" stroke-width="10" stroke-linecap="round" />
            <path d="M110 60 Q150 40 190 80 L180 140 Q150 160 120 140 Z" fill="#f1c9a5" stroke="#353a3d" stroke-width="5" />
            <path id="leine-sight" d="M560 470 L760 470" stroke="#111" stroke-width="8" stroke-dasharray="20 16" />
            <g transform="translate(760 360) scale(1.05)"><g id="leine-other" style="color:#353a3d">""" + DOG + """</g></g>
            <g id="leine-x" stroke="#e24b4b" stroke-width="22" stroke-linecap="round"><path d="M610 400 L710 540 M710 400 L610 540" /></g>
          </svg>
          <div id="leine-dog" style="position:absolute;left:200px;top:380px;width:380px;height:280px">""" + dog_svg() + """</div>
        </div>""", lambda t0, d: f"""
      pop("#leine-head", {t0});
      pop("#leine-dog", {t0} + 0.1);
      draw("#leine-line", {t0} + 0.2, 0.6);
      pop("#leine-other", {c('s8', 1)});
      tl.fromTo("#leine-sight", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {c('s8', 1)} + 0.3);
      pop("#leine-x", {c('s8', 2)});
      tl.fromTo("#leine-dog", {{ x: 0 }}, {{ x: 30, duration: 0.15, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {c('s8', 2)} + 0.2);"""),

    ("ebook", "s9", "s9", """
        <div class="stage">
          <div id="eb-book" style="position:absolute;left:290px;top:60px;width:500px;height:680px;border-radius:14px 30px 30px 14px;background:#DB8622;box-shadow:-18px 0 0 #a8621a, 0 30px 60px rgba(0,0,0,0.25);display:flex;flex-direction:column;align-items:center;padding-top:60px;gap:20px">
            <div style="font-family:Inter;font-weight:800;font-size:40px;color:#fff;letter-spacing:4px">E-BOOK</div>
            <div style="font-family:Inter;font-weight:800;font-size:76px;color:#fff;text-align:center;line-height:1.05">10 Tage<br />ANTI-<br />BELL-<br />PLAN</div>
            <div style="width:170px;height:170px;margin-top:20px">""" + PAW + """</div>
          </div>
          <svg id="eb-star" viewBox="0 0 200 200" style="position:absolute;left:640px;top:0;width:300px;height:300px">
            <path d="M100 5 L122 60 L180 40 L150 95 L195 130 L135 135 L140 195 L100 155 L60 195 L65 135 L5 130 L50 95 L20 40 L78 60 Z" fill="#f2c418" stroke="#111" stroke-width="5" />
            <text x="100" y="112" text-anchor="middle" font-family="Inter" font-weight="800" font-size="17" fill="#111" transform="rotate(-12 100 100)">KOSTENLOS</text>
          </svg>
          <div id="eb-link" style="position:absolute;left:0;top:790px;width:1080px;display:flex;justify-content:center">
            <div class="chip" style="font-size:58px;background:#111">Link in Bio &#8595;</div>
          </div>
        </div>""", lambda t0, d: f"""
      pop("#eb-book", {t0});
      tl.fromTo("#eb-book", {{ rotation: -4 }}, {{ rotation: 0, duration: 0.5, ease: "back.out(2)" }}, {t0});
      tl.fromTo("#eb-star", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, {c('s9', 1)} + 0.4);
      pop("#eb-link", {c('s9', 2)});
      tl.fromTo("#eb-link", {{ y: 0 }}, {{ y: 14, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {c('s9', 2)} + 0.4);"""),
]


def build():
    scenes, js, caps = [], [], []
    for sid, a, b, html, code in SCENES:
        t0 = S[a]["start"]
        t1 = DAUER if b == T["saetze"][-1]["id"] else S[b]["end"]
        d = round(t1 - t0, 3)
        scenes.append(f'      <div id="{sid}" class="scene clip" data-start="{t0}" data-duration="{d}" data-track-index="1">{html}\n      </div>')
        js.append(f"      // {sid}\n      (() => {{{code(t0, d)}\n      }})();")
    n = 0
    for s in T["saetze"]:
        for cp in s["captions"]:
            n += 1
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{cp["start"]}" data-duration="{round(cp["end"] - cp["start"], 3)}" data-track-index="2"><span>{cp["text"]}</span></div>')

    html = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --brand: #DB8622; --ink: #111; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #fff; font-family: "Inter", sans-serif; }}
      .scene {{ position: absolute; inset: 0; }}
      .stage {{ position: absolute; left: 0; top: 400px; width: 1080px; height: 900px; }}
      .head {{
        position: absolute; top: 300px; left: 50%; margin-left: -400px; width: 800px; text-align: center;
        padding: 14px 0 16px; border-radius: 60px; background: var(--brand); color: #fff;
        font-weight: 800; font-size: 54px;
      }}
      .big {{ font-family: "Inter"; font-weight: 800; font-size: 130px; color: var(--ink); }}
      .orange {{ color: var(--brand); }}
      .bubble {{
        position: absolute; padding: 26px 40px; border-radius: 40px; background: #111; color: #fff;
        font-weight: 800; font-size: 60px; line-height: 1.1; text-align: center;
      }}
      .chip {{ padding: 16px 34px; border-radius: 22px; background: var(--brand); color: #fff; font-weight: 800; font-size: 48px; }}
      .meter {{ display: flex; align-items: center; gap: 40px; }}
      .meter .label {{ width: 230px; font-weight: 800; font-size: 64px; color: var(--ink); }}
      .meter .bar {{ flex: 1; height: 90px; border-radius: 45px; background: #eee; border: 6px solid #353a3d; overflow: hidden; }}
      .meter .fill {{ width: 100%; height: 100%; background: #e24b4b; }}
      #brand {{
        position: absolute; top: 190px; left: 0; width: 1080px; display: flex; justify-content: center;
        align-items: center; gap: 14px; font-weight: 800; font-size: 42px; color: #353a3d; z-index: 5;
      }}
      #brand-dog {{ width: 80px; height: 80px; }}
      #frame {{ position: absolute; inset: 0; border: 26px solid var(--brand); z-index: 10; }}
      .cap {{ position: absolute; left: 0; top: 1360px; width: 1080px; display: flex; justify-content: center; z-index: 6; }}
      .cap span {{
        display: block; padding: 16px 34px 18px; border-radius: 18px; background: #111; color: #fff;
        font-weight: 600; font-size: 52px; line-height: 1.15; text-align: center; white-space: nowrap;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DAUER}" data-width="1080" data-height="1920">
{chr(10).join(scenes)}

      <div id="brand"><span>HundeWissenTv</span></div>
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
      const draw = (sel, at, dur) => {{
        const len = document.querySelector(sel).getTotalLength();
        tl.fromTo(sel, {{ strokeDasharray: len, strokeDashoffset: len }}, {{ strokeDashoffset: 0, duration: dur, ease: "power2.out" }}, at);
      }};

{chr(10).join(js)}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    (HERE / "index.html").write_text(html)
    print("index.html gebaut,", DAUER, "s")


if __name__ == "__main__":
    build()
