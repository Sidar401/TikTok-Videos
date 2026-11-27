#!/usr/bin/env python3
"""HundeFinanzTv Börsenrückblick 27.11.2026 (~51 s), dunkler Look, Laufband, neue Regeln (CTA vor Hinweis, kein Untertitel beim Kommentar-Bild).
Dax Schluss 25.441,24 (+0,90 %, Woche +2,6 %), Rheinmetall +3,3 %, Infineon/Siemens Energy/Hochtief +1,7–2,7 %; Nasdaq 100 +2,61 % (Woche +6,8 %),
Dow +1,18 %, S&P 500 +1,60 % (verkürzter Black-Friday-Handel). Quelle dpa-AFX."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
W_ = HERE.parent.parent
sys.path.insert(0, str(W_ / "scripts"))
import logo_sting as ls  # noqa: E402

_t = json.loads((HERE / "timings.json").read_text())
T0 = ls.einfuegen(HERE, next(s["end"] for s in _t["saetze"] if s["id"] == "s4") - 0.01)  # Logo-Intro nach s4

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS, laufband_szene, news_kopf  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, O, W = "#22c55e", "#ff4d4d", nl.ORANGE, "#ffffff"
LOGOS = ["infineon.svg", "siemens-energy.svg", "rheinmetall.svg", "nvidia.svg", "nasdaq.svg", "flagge-usa.svg"]
K = Kit(HERE, 10, ["frei-code-monitor"], logos=LOGOS)
cap, st = K.cap, K.st
S = K.szene
HG = "frei-code-monitor"
SFX_CTA = []

DUNKEL_CSS = ("<style>.nk-karte{background:linear-gradient(180deg,#14171bf0,#0c0e11f5);border:2px solid #ffffff22;box-shadow:0 0 60px #000a}"
              ".nk-kt{color:#fff;border-bottom-color:#ffffff22}.nk-row{color:#e5e7eb}.nk-gross{color:#fff;text-shadow:0 6px 20px #000}"
              ".nk-row img,.nk-kt img{background:#fff;padding:6px 12px;border-radius:10px;margin-right:18px}</style>")


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


def lg(f, h=60):
    return f'<img src="assets/logos/{f}" style="height:{h}px;vertical-align:middle"/>'


def chip(id_, f, x, y, w=380, h=170):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:22px;box-shadow:0 0 50px #000a;z-index:5;'
            f'display:flex;align-items:center;justify-content:center"><img src="assets/logos/{f}" style="max-width:82%;max-height:70%"/></div>')


def pf(farbe):
    return f'<span style="color:{farbe}">{"▲" if farbe == G else "▼"}</span>'


# s1: stärkste Zahl sofort
S("s1", HG, nl.CSS + DUNKEL_CSS + gross("n1", "+0,9 %", 520, G, 240) + pille("p1", "DAX heute", 820, "#1d2330", "#fff", 56) + pille("p1b", "Wochenplus: +2,6 %", 960, O, "#fff", 50),
  lambda a, d: KIT_JS + f' tl.set("#n1", {{ opacity: 1 }}, 0); pop("#n1", {a}); pop("#p1", {a} + 0.15); pop("#p1b", {cap("s1", 1)});')

# s2–s3: Kommentar-Bild (ohne Untertitel)
TXT = "Was machst du mit deinem Depot?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 960)
cta_js = nl.cta_overlay_js("co", st("s2"), len(TXT), SFX_CTA, 1.2)
S("s2", HG, titel("t2", "Börse heute", 520, W, 62)
  + nl.karte("k2", "Deutschland · Schluss", nl.zeile("r2a", "Dax · 25.441 Punkte", "+0,9 %", G, pf(G)), y=600)
  + pille("p3", "Woche: +2,6 %", 850, O, "#fff", 50) + CTA,
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {a} + 0.15); pop("#r2a", {a} + 0.6); pop("#p3", {cap("s3", 0)});' + cta_js, SFX_CTA, bis="s4")

# s4: KI-Erholung
S("s4", HG, titel("t4", "Treiber: KI-Erholung", 520, W, 62) + chip("c4a", "nvidia.svg", 90, 700) + chip("c4b", "infineon.svg", 610, 700) + pille("p4", "Chip-Aktien erholt", 940, G, "#fff", 54),
  lambda a, d: f'pop("#t4", {a}); pop("#c4a", {a} + 0.15); pop("#c4b", {cap("s4", 1)}); pop("#p4", {cap("s4", 1)} + 0.4);')

# s5: Gewinner
S("s5", HG, titel("t5", "Größte Gewinner", 520, W, 62)
  + nl.karte("k5", "Dax-Werte heute", nl.zeile("r5a", lg("rheinmetall.svg"), "+3,3 %", G, pf(G)) + nl.zeile("r5b", lg("siemens-energy.svg"), "+1,7–2,7 %", G, pf(G))
             + nl.zeile("r5c", lg("infineon.svg"), "+1,7–2,7 %", G, pf(G)), y=620),
  lambda a, d: f'pop("#t5", {a}); pop("#k5", {a} + 0.1); pop("#r5a", {a} + 0.6); pop("#r5b", {cap("s5", 2)}); pop("#r5c", {cap("s5", 3)});')

# s6–s7: Wall Street
S("s6", HG, titel("t6", "Wall Street · Black Friday", 520, W, 56)
  + nl.karte("k6", lg("flagge-usa.svg", 46) + " verkürzter Handel", nl.zeile("r6a", lg("nasdaq.svg", 52), "+2,6 %", G, pf(G)) + nl.zeile("r6b", "Dow Jones", "+1,2 %", G, pf(G))
             + nl.zeile("r6c", "S&amp;P 500", "+1,6 %", G, pf(G)), y=610)
  + pille("p7", "Nasdaq 100 in der Woche: +6,8 %", 1010, O, "#fff", 46),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {a} + 0.6); pop("#r6b", {cap("s6", 3)}); pop("#r6c", {cap("s6", 4)}); pop("#p7", {cap("s7", 0)} + 0.4);', bis="s8")


def merk(sid):
    html = (titel(f"t{sid}", "Merk dir", 520, O, 70)
            + nl.karte(f"k{sid}", "Die KI-Aktien", f'<div style="font-weight:900;font-size:62px;color:{O};text-align:center;padding:14px 0;line-height:1.15">bleiben der Taktgeber der Börse</div>', y=660))
    return html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.15);'


def cta(sid, statisch=False):
    html = (beagle(f"fl{sid}", 520) + f'<div id="n{sid}" class="nk-gross" style="top:940px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
            + pille(f"c{sid}", "+ Folgen", 1060, O, "#fff", 58) + pille(f"t{sid}", "Video teilen ↗", 1190, "#1d2330", "#fff", 52))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#fl{sid}", {a}); pop("#n{sid}", {a} + 0.2); pop("#c{sid}", {cap(sid, 1)}); pop("#t{sid}", {cap(sid, 0)} + 0.4);'


h8, j8 = merk("s8")
S("s8", HG, h8, j8)
h9, j9 = cta("s9")
S("s9", HG, h9, j9)
h10, j10 = cta("s10", True)
S("s10", HG, h10, j10)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s5", 1), "richtig"), (cap("s6", 3), "richtig"), (cap("s9", 1), "klick")])
html, code = ls.szene(hell=False)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append(laufband_szene([("DAX ▲ +0,9 %", G), ("25.441", W), ("RHEINMETALL ▲ +3,3 %", G), ("SIEMENS ENERGY ▲", G), ("INFINEON ▲", G),
                            ("NASDAQ 100 ▲ +2,6 %", G), ("DOW ▲ +1,2 %", G), ("S&P 500 ▲ +1,6 %", G)], K.dauer, top=1560, farbe=G))
K.SZ.append((0.0, K.dauer, news_kopf("27.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.ohne_untertitel_zwischen(HERE, st("s2"), st("s4"))  # kein Untertitel beim Kommentar-Bild (Nutzer 26.11.)
