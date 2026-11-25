#!/usr/bin/env python3
"""HundeFinanzTv Börsenrückblick 25.11.2026 (~44 s). Dax Schluss 24.702,13 (−1,26 %), Infineon −6,5 %, VW +4,6 %, BMW +3,7 % (dpa-AFX); Nasdaq/Nvidia nur zeitweise. Fester erster Satz, CTA Satz 2, Hinweis zuletzt."""
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
from analyse_kit import KIT_JS, laufband_szene  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 10, [])
cap, st = K.cap, K.st
S = K.szene
SFX_CTA = []


def titel(id_, text, y=340, farbe=D, gr=64):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=50):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.05">{text}</div>'


def beagle(id_, y=330):
    return (f'<div id="{id_}" style="position:absolute;left:340px;top:{y}px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>')


# s1: fester erster Satz, stärkste Zahl sofort im Bild
S("s1", None, nl.CSS + gross("n1", "−1,3 %", 340, R, 250) + pille("p1", "DAX heute", 700, D, "#fff", 56)
  + pille("p1b", "tiefster Stand seit Juli", 860, O, "#fff", 50),
  lambda a, d: KIT_JS + f' tl.set("#n1", {{ opacity: 1 }}, 0); pop("#n1", {a}); pop("#p1", {a} + 0.15); pop("#p1b", {cap("s1", 1)});')

S("s2", None, beagle("fl2", 340) + f'<div id="n2" class="nk-gross" style="top:770px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + pille("c2", "+ Folgen", 890, O, "#fff", 58) + pille("t2", "Video teilen ↗", 1040, D, "#fff", 52),
  lambda a, d: f'pop("#fl2", {a}); pop("#n2", {a} + 0.2); pop("#c2", {cap("s2", 1)}); pop("#t2", {cap("s2", 0)} + 0.4);')

TXT = "Was kaufst du bei Kursrutsch?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.2)
S("s3", None, titel("t3", "Börse heute", 380, D, 66)
  + nl.karte("k3", "Deutschland", nl.zeile("r3a", "Dax", "−1,3 %", R, f"<span style=\"color:{R}\">▼</span>"), y=480)
  + pille("p3", "Flucht aus KI-Aktien", 760, O, "#fff", 52) + CTA,
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {a} + 0.15); pop("#r3a", {cap("s3", 1)}); pop("#p3", {cap("s4", 0)});' + cta_js, SFX_CTA, bis="s5")

S("s5", None, titel("t5", "Größter Verlierer", 340, D, 64) + gross("n5", "Infineon", 470, D, 150) + gross("n5b", "−6,5 %", 650, R, 220),
  lambda a, d: f'pop("#t5", {a}); pop("#n5", {a} + 0.15); pop("#n5b", {cap("s5", 1)});')

S("s6", None, titel("t6", "Autowerte im Plus", 340, D, 64)
  + nl.karte("k6", "Gewinner", nl.zeile("r6a", "Volkswagen", "+4,5 %", G, "▲") + nl.zeile("r6b", "BMW", "+3,5 %", G, "▲"), y=500),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {cap("s6", 1)}); pop("#r6b", {cap("s6", 2)});')

S("s7", None, titel("t7", "USA · zeitweise", 340, D, 64)
  + nl.karte("k7", "Technik-Aktien", nl.zeile("r7a", "Nasdaq", "−4 %", R, f"<span style=\"color:{R}\">▼</span>") + nl.zeile("r7b", "Nvidia", "−8 %", R, f"<span style=\"color:{R}\">▼</span>"), y=500),
  lambda a, d: f'pop("#t7", {a}); pop("#k7", {a} + 0.1); pop("#r7a", {cap("s7", 2)}); pop("#r7b", {cap("s8", 0)} + 0.2);', bis="s9")


def merk(sid, statisch=False):
    html = (titel(f"t{sid}", "Merk dir", 340, O, 70)
            + nl.karte(f"k{sid}", "Wenn KI-Aktien fallen", f'<div style="font-weight:900;font-size:68px;color:{R};text-align:center;padding:14px 0;line-height:1.15">fällt der ganze Markt ▼</div>', y=500))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.15);'


h9, j9 = merk("s9")
S("s9", None, h9, j9)
h10, j10 = merk("s10", True)
S("s10", None, h10, j10)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "klick"), (cap("s5", 1), "kurve-runter"), (cap("s6", 1), "richtig"), (cap("s7", 2), "falsch")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append(laufband_szene([("DAX ▼ −1,3 %", R), ("24.702", "#fff"), ("INFINEON ▼ −6,5 %", R), ("VW ▲ +4,5 %", G), ("BMW ▲ +3,5 %", G),
                           ("NASDAQ ▼ ≈ −4 %", R), ("NVIDIA ▼ ≈ −8 %", R)], K.dauer, top=1640))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "25.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
