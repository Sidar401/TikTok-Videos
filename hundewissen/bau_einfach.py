#!/usr/bin/env python3
"""HundeWissenTv – einfaches Magazin-Video (ruhige Bilder, 3 Szenen + Logo-Schluss) aus einer Beschreibung bauen.

Aufruf: python3 hundewissen/bau_einfach.py <name>   (Daten unten in VIDEOS)
Regeln (Nutzer 16.11.): keine Wackel-/Bewegungs-Effekte am Hund, kein Fortschrittsbalken, ruhigeres Tempo,
Schluss immer mit großem Logo + „Folg uns für mehr“.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
T = [(0.0, 4.2), (4.2, 8.4), (8.4, 12.4)]  # Szenenzeiten
SCHLUSS = 12.4
DUR = 15

VIDEOS = {
    "hw-e-kratzen": [
        dict(kick="Juckreiz", h="Warum kratzt sich dein Hund <i>so oft?</i>", size=104, pose="kratzend", ph=560,
             caps=["kratzt sich dein hund <b>ständig</b>?", "das kann viele <b>gründe</b> haben"]),
        dict(kick="Meistens harmlos", h="Ab und zu ist das <i>ganz normal.</i>", size=100, pose="verwirrt", ph=540,
             extra='<div class="note x" style="left:90px;top:1150px;transform:rotate(-6deg)">*kratz, kratz*</div>',
             caps=["ab und zu kratzen ist <b>normal</b>", "genau wie <b>bei uns</b>"]),
        dict(kick="Aber Achtung", h="Kratzt er dauernd? <i>Ab zum Tierarzt.</i>", size=92, pose="brille", ph=540, px=600,
             extra='<div class="chip x" style="top:880px">🐜 Flöhe?</div><div class="chip x" style="top:1010px">🌾 Allergie?</div><div class="chip x" style="top:1140px">🏜️ Trockene Haut?</div>',
             caps=["kratzt er sich aber <b>dauernd</b>", "dann lieber zum <b>tierarzt</b>"]),
    ],
    "hw-e-schnueffeln": [
        dict(kick="Gassi-Tipp", h="Lass ihn ruhig <i>schnüffeln!</i>", size=110, pose="schnueffelnd", ph=520,
             caps=["zieh nicht ständig an der <b>leine</b>", "lass ihn ruhig <b>schnüffeln</b>"]),
        dict(kick="Kopfarbeit", h="Schnüffeln ist <i>Training fürs Gehirn.</i>", size=100, pose="brille", ph=540,
             extra='<div class="note x" style="left:80px;top:1180px;transform:rotate(-5deg)">Nase = Superkraft</div>',
             caps=["schnüffeln ist <b>kopfarbeit</b>", "das macht ihn <b>zufrieden</b>"]),
        dict(kick="Der Effekt", h="Danach ist er <i>schön müde.</i>", size=110, pose="schlafend", ph=420,
             extra='<div class="note x" style="left:700px;top:900px;font-size:70px">Zzz</div>',
             caps=["und danach schläft er", "<b>wie ein baby</b>"]),
    ],
    "hw-e-hundeblick": [
        dict(kick="Der Hundeblick", h="Diesem Blick <i>kann keiner</i> widerstehen.", size=96, pose="bettelnd", ph=580,
             caps=["kennst du diesen <b>hundeblick</b>?", "da wird jeder <b>schwach</b>"]),
        dict(kick="Die Forschung", h="Dafür hat er <i>einen extra Muskel.</i>", size=100, pose="ueberrascht", ph=560, px=600,
             extra='<div class="call x" style="left:60px;top:1180px">hebt die Augenbraue ↗</div>',
             src="Studie: University of Portsmouth (2019)",
             caps=["hunde haben einen <b>extra muskel</b>", "für die innere <b>augenbraue</b>"]),
        dict(kick="Clever", h="Wölfe haben ihn <i>fast nie.</i>", size=110, pose="stolz", ph=540,
             caps=["wölfe haben ihn <b>fast nie</b>", "den blick gibt's <b>nur für uns</b>"]),
    ],
    "hw-e-hecheln": [
        dict(kick="Sommer-Wissen", h="Hunde schwitzen <i>kaum.</i>", size=112, pose="freudig", ph=560,
             caps=["hunde können <b>kaum schwitzen</b>", "nur ein bisschen über die <b>pfoten</b>"]),
        dict(kick="Die Kühlung", h="Sie kühlen sich <i>durch Hecheln.</i>", size=104, pose="rennend", ph=440,
             extra='<div class="note x" style="left:560px;top:880px;transform:rotate(-5deg)">Zunge = Klimaanlage</div>',
             caps=["sie kühlen sich durch <b>hecheln</b>", "die zunge wirkt wie eine <b>klimaanlage</b>"]),
        dict(kick="Tipp", h="Immer <i>frisches Wasser</i> dabei.", size=108, pose="trinkend", ph=520,
             caps=["darum im sommer <b>immer</b>", "<b>frisches wasser</b> mitnehmen"]),
    ],
}

HTML = """<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/magazin.css" />
    <style>
      .pose {{ position: absolute; filter: drop-shadow(0 26px 30px #00000030); }}
      .shadow {{ position: absolute; height: 40px; border-radius: 50%; background: radial-gradient(#0000002a, transparent 70%); }}
      .chip {{ position: absolute; left: 80px; padding: 16px 34px 20px; border-radius: 40px; background: #fbf8f2; border: 2px solid #1d1b1922; box-shadow: 0 14px 30px #0000001a; font-weight: 800; font-size: 44px; }}
      .call {{ position: absolute; padding: 14px 30px 18px; border-radius: 40px; background: #fbf8f2; border: 2px solid #1d1b1922; box-shadow: 0 14px 30px #0000001a; font-weight: 800; font-size: 40px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{SCENES}
{CAPS}
      <div id="logo"><img src="assets/beagle.png" alt="" /></div>
      <div id="name">HundeWissenTv</div>
      <div id="cta"><div class="ring"><img src="assets/beagle.png" alt="" /></div><div class="n">HundeWissenTv</div><div class="t">Folg uns für mehr Hundewissen!</div><div class="pill"><span>+ Folgen</span></div></div>
      <div id="grain"></div>
    </div>
    <script>
      const DUR = {DUR};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
    <script src="assets/magazin.js"></script>
    <script>
      kopf2();
{JS}
      schluss({SCHLUSS});
      tl.to({{}}, {{ duration: 0.01 }}, DUR - 0.01);
    </script>
  </body>
</html>
"""


def bau(name):
    d = ROOT / "videos" / name
    if not d.exists():
        subprocess.run(["bash", str(ROOT / "hundewissen/neu.sh"), name], check=True)
    for f in ["magazin.css", "magazin.js"]:
        (d / "assets" / f).write_bytes((ROOT / "hundewissen/magazin" / f).read_bytes())
    scenes, caps, js = [], [], []
    for i, (sz, (a, b)) in enumerate(zip(VIDEOS[name], T), 1):
        w0, h0 = Image.open(ROOT / f"brand/aussie/{sz['pose']}.png").size
        ph = sz["ph"]; pw = round(w0 * ph / h0)
        if pw > 860: pw = 860; ph = round(h0 * pw / w0)
        cx = sz.get("px", 540); top = 1400 - ph
        src = f'<div class="src" style="top:1418px">{sz["src"]}</div>' if sz.get("src") else ""
        scenes.append(f'''      <div id="s{i}" class="scene">
        <div class="kick" style="top: 440px">{sz["kick"]}</div>
        <div id="h{i}" class="h" style="top: 492px; font-size: {sz["size"]}px">{sz["h"]}</div>
        <div class="shadow" style="left:{cx - pw * 0.42:.0f}px;top:1378px;width:{pw * 0.84:.0f}px"></div>
        <img id="p{i}" class="pose" src="assets/aussie/{sz["pose"]}.png" style="left:{cx - pw / 2:.0f}px;top:{top}px;width:{pw}px" alt="" />
        <div id="x{i}">{sz.get("extra", "")}</div>{src}
      </div>''')
        m = (a + b) / 2
        for k, (c, ca, cb) in enumerate(zip(sz["caps"], [a, m], [m, b])):
            caps.append(f'      <div id="k{i}{k}" class="cap">{c}</div>')
            js.append(f'      show("#k{i}{k}", {ca}, {cb});')
        js.append(f'      up("#h{i}", {a + 0.25}, 0.6);')
        js.append(f'      tl.fromTo("#p{i}", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }}, {a + 0.5});')
        js.append(f'      tl.fromTo("#x{i} .x", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, stagger: 0.35, ease: "power3.out" }}, {a + 1.4});')
    js.insert(0, f'      scenes([["#s1", 0, {T[0][1]}], ["#s2", {T[1][0]}, {T[1][1]}], ["#s3", {T[2][0]}, {SCHLUSS + 0.2}]]);')
    (d / "index.html").write_text(HTML.format(DUR=DUR, SCENES="\n".join(scenes), CAPS="\n".join(caps), JS="\n".join(js), SCHLUSS=SCHLUSS))
    print("gebaut:", d)


if __name__ == "__main__":
    for n in sys.argv[1:] or VIDEOS:
        bau(n)
