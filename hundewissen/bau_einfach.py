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
    "hw-f-schokolade": [
        dict(h="Schokolade ist <i>giftig</i> für Hunde.", size=104, pose="bettelnd", ph=580,
             caps=["dein hund bettelt um <b>schokolade</b>?", "bitte <b>niemals</b> geben"]),
        dict(h="Schuld ist der Stoff <i>Theobromin.</i>", size=100, pose="ueberrascht", ph=560, px=690,
             extra='<div class="chip x" style="top:1000px">🍫 je dunkler,</div><div class="chip x" style="top:1130px">desto gefährlicher</div>',
             caps=["schuld ist <b>theobromin</b>", "dunkle schokolade ist <b>am schlimmsten</b>"]),
        dict(h="Hat er genascht? <i>Sofort zum Tierarzt.</i>", size=96, pose="zeigend", ph=560,
             caps=["hat er doch genascht?", "dann <b>sofort zum tierarzt</b>"]),
    ],
    "hw-f-schlaf": [
        dict(h="Dein Hund schläft <i>ständig?</i>", size=112, pose="gaehnend", ph=580,
             caps=["schläft dein hund <b>den ganzen tag</b>?", "das ist <b>völlig normal</b>"]),
        dict(h="Erwachsene Hunde: <i>12 bis 14 Stunden.</i>", size=100, pose="schlafend", ph=440,
             caps=["erwachsene hunde schlafen", "<b>12 bis 14 stunden</b> am tag"]),
        dict(h="Welpen sogar <i>bis zu 20.</i>", size=112, pose="rueckenlage", ph=380,
             caps=["welpen schlafen", "sogar <b>noch viel mehr</b>"]),
    ],
    "hw-f-kopfschief": [
        dict(h="Warum legt er den Kopf <i>schief?</i>", size=104, pose="verwirrt", ph=580,
             caps=["dein hund legt den kopf <b>schief</b>?", "das hat einen <b>grund</b>"]),
        dict(h="Er hört <i>ganz genau hin.</i>", size=112, pose="brille", ph=580, src="Studie: Universität Budapest (2022)",
             caps=["er will dich <b>besser verstehen</b>", "vor allem bei wörtern, die er <b>kennt</b>"]),
        dict(h="Sag mal <i>„Gassi“</i> – und schau hin!", size=104, pose="freudig", ph=560,
             caps=["probier's aus: sag mal <b>gassi</b>", "und achte auf <b>seinen kopf</b>"]),
    ],
    "hw-f-dunkel": [
        dict(h="Im Dunkeln sieht er <i>besser als du.</i>", size=104, pose="stolz", ph=560,
             caps=["im dunkeln sieht dein hund", "<b>viel besser</b> als du"]),
        dict(h="Sein Auge hat einen <i>Licht-Spiegel.</i>", size=104, pose="ueberrascht", ph=580,
             caps=["hinter der netzhaut sitzt ein <b>spiegel</b>", "der das restlicht <b>verstärkt</b>"]),
        dict(h="Dafür sieht er <i>weniger Farben.</i>", size=104, pose="rennend", ph=440,
             caps=["dafür sieht er <b>weniger farben</b>", "aber <b>bewegung</b> erkennt er super"]),
    ],
    "hw-g-zaehne": [
        dict(h="Putzt du deinem Hund <i>die Zähne?</i>", size=104, pose="zahnbuerste", ph=560,
             caps=["putzt du deinem hund <b>die zähne</b>?", "das solltest du <b>unbedingt</b>"]),
        dict(h="Die meisten haben mit 3 Jahren <i>Zahnprobleme.</i>", size=92, pose="krank", ph=400, src="Tierärzte-Verband AVMA",
             caps=["die meisten hunde haben mit 3 jahren", "schon <b>probleme mit den zähnen</b>"]),
        dict(h="Nur <i>Hunde-Zahnpasta</i> nehmen!", size=104, pose="aufmerksam", ph=580, px=700,
             extra='<div class="chip x" style="top:1000px">❌ Menschen-Zahnpasta</div><div class="chip x" style="top:1130px">✅ Hunde-Zahnpasta</div>',
             caps=["nimm nie <b>deine eigene</b> zahnpasta", "sondern <b>spezielle für hunde</b>"]),
    ],
    "hw-g-schuldblick": [
        dict(h="Fühlt er sich <i>wirklich schuldig?</i>", size=104, pose="schuldig", ph=580,
             caps=["kennst du diesen <b>blick</b>?", "als hätte er ein <b>schlechtes gewissen</b>"]),
        dict(h="Er reagiert auf <i>deine Stimme.</i>", size=104, pose="aufmerksam", ph=580, src="Studie: Barnard College, New York (2009)",
             caps=["forscher sagen: er reagiert", "auf <b>deinen ärger</b>, nicht auf schuld"]),
        dict(h="Schimpfen danach <i>bringt nichts.</i>", size=104, pose="traurig", ph=540,
             caps=["schimpfen im nachhinein", "<b>versteht er nicht</b>"]),
    ],
    "hw-g-winterpfoten": [
        dict(h="Schnee macht Spaß – <i>aber Vorsicht!</i>", size=100, pose="schnee", ph=520,
             caps=["schnee macht <b>riesig spaß</b>", "aber pass auf <b>seine pfoten</b> auf"]),
        dict(h="Streusalz <i>reizt die Pfoten.</i>", size=110, pose="pfoetchen", ph=580,
             caps=["streusalz kann die pfoten", "<b>wund und rissig</b> machen"]),
        dict(h="Nach dem Gassi: <i>Pfoten abspülen.</i>", size=100, pose="badewanne", ph=480,
             caps=["darum nach dem gassi", "die pfoten mit <b>warmem wasser</b> abspülen"]),
    ],
    "hw-g-buddeln": [
        dict(h="Warum buddelt er <i>ständig Löcher?</i>", size=100, pose="buddeln", ph=540,
             caps=["buddelt dein hund <b>ständig löcher</b>?", "dafür gibt es <b>gründe</b>"]),
        dict(h="Oft steckt <i>Langeweile</i> dahinter.", size=104, pose="gelangweilt", ph=380,
             extra='<div class="chip x" style="top:860px">🦴 Etwas verstecken</div><div class="chip x" style="top:990px">😎 Kühler Liegeplatz</div>',
             caps=["er versteckt etwas, sucht kühle", "oder ihm ist <b>einfach langweilig</b>"]),
        dict(h="Mehr Spielen hilft <i>am besten.</i>", size=104, pose="ball", ph=560,
             caps=["mehr <b>spielen und schnüffeln</b>", "dann buddelt er <b>weniger</b>"]),
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
      <div id="cta"><div class="ring"><img src="assets/beagle.png" alt="" /></div><div class="n">HundeWissenTv</div><div class="pill"><span>+ Folgen</span></div></div>
      <div id="grain"></div>
      <div id="frame"></div>
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
        <div id="h{i}" class="h" style="top: 470px; font-size: {sz["size"]}px">{sz["h"]}</div>
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
