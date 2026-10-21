#!/usr/bin/env python3
"""HundeWissenTv-Short: Slideshow-Bilder + Voiceover -> index.html (aus timings.json)."""
import json
from pathlib import Path

HERE = Path(__file__).parent
T = json.loads((HERE / "timings.json").read_text())
DAUER = T["dauer"]
ORANGE = "#DB8622"

# Kamerafahrt pro Bild: (scale von, scale bis, x-Pan in px)
MOVES = [(1.0, 1.1, 0), (1.08, 1.0, -30), (1.0, 1.08, 30), (1.08, 1.0, 30), (1.0, 1.1, -30),
         (1.1, 1.0, 0), (1.0, 1.08, 30), (1.08, 1.0, -30), (1.0, 1.06, 0)]


def build():
    scenes, caps, js = [], [], []
    n = 0
    for i, s in enumerate(T["saetze"], 1):
        t0 = s["start"]
        t1 = DAUER if i == len(T["saetze"]) else s["end"]
        d = round(t1 - t0, 3)
        a, b, x = MOVES[(i - 1) % len(MOVES)]
        scenes.append(f'''      <div id="b{i}" class="slide clip" data-start="{t0}" data-duration="{d}" data-track-index="1">
        <img class="bg" src="assets/bilder/{i:02d}-bg.jpg" alt="" />
        <div class="photo"><img id="b{i}-img" src="assets/bilder/{i:02d}.jpg" alt="" /></div>
      </div>''')
        js.append(f'      tl.fromTo("#b{i}-img", {{ scale: {a}, x: 0 }}, {{ scale: {b}, x: {x}, duration: {d}, ease: "sine.inOut" }}, {t0});')
        js.append(f'      tl.fromTo("#b{i} .photo", {{ scale: 0.96, opacity: 0.4 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "power3.out" }}, {t0});')
        for c in s["captions"]:
            n += 1
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{c["start"]}" data-duration="{round(c["end"] - c["start"], 3)}" data-track-index="2"><span>{c["text"]}</span></div>')

    html = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      :root {{ --brand: {ORANGE}; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #000; }}
      .slide {{ position: absolute; inset: 0; overflow: hidden; }}
      .slide .bg {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .photo {{
        position: absolute; left: 0; top: 300px; width: 1080px; height: 1080px; overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
      }}
      .photo img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
      #brand {{
        position: absolute; top: 190px; left: 0; width: 1080px; display: flex; justify-content: center;
        align-items: center; gap: 14px; font-family: "Inter", sans-serif; font-weight: 800; font-size: 44px;
        color: #fff; z-index: 5;
      }}
      #brand-dog {{ width: 80px; height: 80px; }}
      #brand-dog img {{ width: 100%; height: 100%; object-fit: contain; }}
      #frame {{ position: absolute; inset: 0; border: 26px solid var(--brand); z-index: 10; }}
      .cap {{ position: absolute; left: 0; top: 1225px; width: 1080px; display: flex; justify-content: center; z-index: 6; }}
      .cap span {{
        display: block; max-width: 980px; padding: 14px 30px 16px; border-radius: 18px; background: #fff;
        color: #111; font-family: "Inter", sans-serif; font-weight: 600; font-size: 48px; line-height: 1.15; white-space: nowrap;
        text-align: center;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DAUER}" data-width="1080" data-height="1920">
{chr(10).join(scenes)}

      <div id="brand"><div id="brand-dog"><img src="assets/beagle.png" alt="" /></div><span>HundeWissenTv</span></div>
      <div id="frame"></div>

      <div id="captions" data-track-kind="captions">
{chr(10).join(caps)}
      </div>

      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{DAUER}" data-track-index="3"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
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
