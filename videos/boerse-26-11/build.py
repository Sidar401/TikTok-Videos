#!/usr/bin/env python3
"""HundeFinanzTv Börsenrückblick 26.11.2026 (~47 s), DUNKLER Look (Nutzer 26.11.), Laufband.
Dax-Schluss 25.215,52 (+2,08 %, dpa-AFX); Rheinmetall ≈ +4,1 %, Siemens Energy +4,0 %, Infineon +3,6 % (eine Quelle); Nasdaq Mi. Schluss −0,62 % (Tief −4,6 %);
Nvidia Mi. Schluss −3,9 % (zeitweise > −9 %); Do. US-Feiertag Thanksgiving."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

_t = json.loads((HERE / "timings.json").read_text())
T0 = ls.einfuegen(HERE, next(s["end"] for s in _t["saetze"] if s["id"] == "s4") - 0.01)  # Logo-Intro nach s4

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS, laufband_szene, news_kopf  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, O, W = "#22c55e", "#ff4d4d", nl.ORANGE, "#ffffff"
LOGOS = ["infineon.svg", "siemens-energy.svg", "nvidia.svg", "flagge-usa.svg"]
if (HERE.parent.parent / "brand/logos/rheinmetall.svg").exists():
    LOGOS.append("rheinmetall.svg")
HAS_RH = "rheinmetall.svg" in LOGOS
K = Kit(HERE, 10, ["frei-code-monitor"], logos=LOGOS)
cap, st = K.cap, K.st
S = K.szene
HG = "frei-code-monitor"
SFX_CTA = []

DUNKEL_CSS = ("<style>.nk-karte{background:linear-gradient(180deg,#14171bf0,#0c0e11f5);border:2px solid #ffffff22;box-shadow:0 0 60px #000a}"
              ".nk-kt{color:#fff;border-bottom-color:#ffffff22}.nk-row{color:#e5e7eb}.nk-gross{color:#fff;text-shadow:0 6px 20px #000}"
              ".nk-row img,.nk-kt img{background:#fff;padding:8px 16px;border-radius:12px;margin-right:18px}</style>")


def titel(id_, text, y=520, farbe=W, gr=62):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.05;text-shadow:0 0 50px {farbe}99,0 6px 20px #000">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=50):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 0 40px {farbe}88;white-space:nowrap">{text}</span></div>')


def beagle(id_, y=520):
    return (f'<div id="{id_}" style="position:absolute;left:340px;top:{y}px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 0 50px {O}88;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>')


def lg(f, h=52):
    return f'<img src="assets/logos/{f}" style="height:{h}px;vertical-align:middle"/>'


def pf(farbe):
    return f'<span style="color:{farbe}">{"▲" if farbe == G else "▼"}</span>'


# s1: stärkste Zahl sofort
S("s1", HG, nl.CSS + DUNKEL_CSS + gross("n1", "+2,1 %", 520, G, 240) + pille("p1", "DAX heute", 820, "#1d2330", "#fff", 56) + pille("p1b", "kräftige Erholung", 960, O, "#fff", 50),
  lambda a, d: KIT_JS + f' tl.set("#n1", {{ opacity: 1 }}, 0); pop("#n1", {a}); pop("#p1", {a} + 0.15); pop("#p1b", {cap("s1", 1)});')

S("s2", HG, beagle("fl2", 520) + f'<div id="n2" class="nk-gross" style="top:940px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + pille("c2", "+ Folgen", 1060, O, "#fff", 58) + pille("t2", "Video teilen ↗", 1190, "#1d2330", "#fff", 52),
  lambda a, d: f'pop("#fl2", {a}); pop("#n2", {a} + 0.2); pop("#c2", {cap("s2", 1)}); pop("#t2", {cap("s2", 0)} + 0.4);')

TXT = "Kaufst du bei Kurserholung?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 960)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.2)
S("s3", HG, titel("t3", "Börse heute", 520, W, 62)
  + nl.karte("k3", "Deutschland · Schluss", nl.zeile("r3a", "Dax · 25.216 Punkte", "+2,1 %", G, pf(G)), y=600)
  + pille("p3", "gestern: tiefster Stand seit Juli", 810, O, "#fff", 44) + CTA,
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {a} + 0.15); pop("#r3a", {cap("s3", 1)}); pop("#p3", {cap("s4", 0)});' + cta_js, SFX_CTA, bis="s5")

rh = (lg("rheinmetall.svg", 60)) if HAS_RH else ""
S("s5", HG, titel("t5", "Größte Gewinner", 520, W, 62)
  + nl.karte("k5", "Dax-Werte heute", nl.zeile("r5a", rh if HAS_RH else "Rheinmetall", "≈ +4 %", G, pf(G)) + nl.zeile("r5b", lg("siemens-energy.svg", 60), "+4,0 %", G, pf(G))
             + nl.zeile("r5c", lg("infineon.svg", 60), "+3,6 %", G, pf(G)), y=620),
  lambda a, d: f'pop("#t5", {a}); pop("#k5", {a} + 0.1); pop("#r5a", {cap("s5", 1)}); pop("#r5b", {cap("s5", 2)}); pop("#r5c", {cap("s5", 2)} + 0.7);')

S("s6", HG, titel("t6", "Warum? Wall Street gestern", 520, W, 56)
  + nl.karte("k6", "Nasdaq am Mittwoch", nl.zeile("r6a", "Tief im Handel", "−4,6 %", R, pf(R)) + nl.zeile("r6b", "Schluss", "−0,6 %", G, ""), y=620),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {cap("s6", 0)} + 0.6); pop("#r6b", {cap("s6", 2)});')

S("s7", HG, titel("t7", "Nvidia am Mittwoch", 520, W, 62)
  + nl.karte("k7", lg("nvidia.svg", 60), nl.zeile("r7a", "Schluss", "−3,9 %", R, pf(R)) + nl.zeile("r7b", "Tief im Handel", "über −9 %", R, pf(R)), y=620),
  lambda a, d: f'pop("#t7", {a}); pop("#k7", {a} + 0.1); pop("#r7a", {cap("s7", 0)} + 0.4); pop("#r7b", {cap("s7", 2)});')

S("s8", HG, titel("t8", "Heute: Thanksgiving", 520, W, 66) + f'<div id="f8" style="position:absolute;left:290px;top:660px;width:500px;z-index:4"><img src="assets/logos/flagge-usa.svg" style="width:100%;border-radius:14px;box-shadow:0 0 50px #000"/></div>'
  + pille("p8", "US-Börse geschlossen", 1040, O, "#fff", 54),
  lambda a, d: f'pop("#t8", {a}); pop("#f8", {a} + 0.15); pop("#p8", {cap("s8", 1)});')


def merk(sid, statisch=False):
    html = (titel(f"t{sid}", "Merk dir", 520, O, 70)
            + nl.karte(f"k{sid}", "Nach einem Absturz", f'<div style="font-weight:900;font-size:68px;color:{G};text-align:center;padding:14px 0;line-height:1.15">kommt die Erholung schnell ▲</div>', y=660))
    return (html, (lambda a, d: "")) if statisch else (html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.15);')


h9, j9 = merk("s9")
S("s9", HG, h9, j9)
h10, j10 = merk("s10", True)
S("s10", HG, h10, j10)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "klick"), (cap("s5", 1), "richtig"), (cap("s6", 2), "richtig"), (cap("s7", 2), "falsch")])

html, code = ls.szene(hell=False)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append(laufband_szene([("DAX ▲ +2,1 %", G), ("25.216", W), ("RHEINMETALL ▲ ≈ +4 %", G), ("SIEMENS ENERGY ▲ +4,0 %", G), ("INFINEON ▲ +3,6 %", G),
                            ("NVIDIA (MI.) ▼ −3,9 %", R), ("NASDAQ (MI.) ▼ −0,6 %", R)], K.dauer, top=1560, farbe=G))
K.SZ.append((0.0, K.dauer, news_kopf("26.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
