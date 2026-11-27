#!/usr/bin/env python3
"""HundeFinanzTv Short 28.11.2026 (~46 s), dunkler Look, TREND: Haushaltsbegleitgesetz 2027 – Grundsicherung (Bürgergeld) Regelsatz 563 € bis Juni 2028 eingefroren,
Anpassung künftig 1. Juli (nächste 2028). Bundestag 27.11. beschlossen, Bundesrat offen; Paritätischer kritisiert. Neue Regeln: CTA vor Hinweis, kein Untertitel beim Kommentar-Bild."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
W_ = HERE.parent.parent
sys.path.insert(0, str(W_ / "scripts"))
import logo_sting as ls  # noqa: E402

_t = json.loads((HERE / "timings.json").read_text())
T0 = ls.einfuegen(HERE, next(s["end"] for s in _t["saetze"] if s["id"] == "s3") - 0.01)  # Logo-Intro nach s3

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS, news_kopf  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, O, W = "#22c55e", "#ff4d4d", nl.ORANGE, "#ffffff"
LOGOS = ["flagge-deutschland.svg"]
K = Kit(HERE, 9, ["frei-code-monitor"], logos=LOGOS)
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


def flagge(f, h=56):
    return f'<img src="assets/logos/{f}" style="height:{h}px;vertical-align:middle;border-radius:12px;box-shadow:0 0 0 6px #fff"/>'


def chip(id_, f, x, y, w=380, h=170):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:22px;box-shadow:0 0 50px #000a;z-index:5;'
            f'display:flex;align-items:center;justify-content:center"><img src="assets/logos/{f}" style="max-width:82%;max-height:70%"/></div>')


def pf(farbe):
    return f'<span style="color:{farbe}">{"▲" if farbe == G else "▼"}</span>'


# s1: Hook – stärkste Aussage sofort
S("s1", HG, nl.CSS + DUNKEL_CSS + gross("n1", "NULLRUNDE", 540, R, 136) + gross("n1b", "bis Mitte 2028", 740, W, 92) + pille("p1", "Grundsicherung · Bürgergeld", 960, O, "#fff", 50),
  lambda a, d: KIT_JS + f' tl.set("#n1", {{ opacity: 1 }}, 0); pop("#n1", {a}); pop("#n1b", {a} + 0.15); pop("#p1", {cap("s1", 2)});')

# s2–s3: Kommentar-Bild (ohne Untertitel)
TXT = "Betrifft dich das?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 960)
cta_js = nl.cta_overlay_js("co", st("s2"), len(TXT), SFX_CTA, 1.2)
S("s2", HG, titel("t2", "Regelsatz Alleinstehende", 520, W, 58)
  + nl.karte("k2", "Grundsicherung", nl.zeile("r2a", "pro Monat", "563 €", W, "") + nl.zeile("r2b", "nächste Anpassung", "1. Juli 2028", R, ""), y=610) + CTA,
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {a} + 0.15); pop("#r2a", {a} + 0.6); pop("#r2b", {cap("s3", 2)});' + cta_js, SFX_CTA, bis="s4")

# s4: Haushaltsbegleitgesetz
S("s4", HG, titel("t4", "Haushaltsbegleitgesetz 2027", 520, W, 54)
  + f'<div id="f4" style="position:absolute;left:290px;top:640px;width:500px;z-index:4">{flagge("flagge-deutschland.svg", 300)}</div>'
  + pille("p4", "Bundestag: beschlossen", 1000, G, "#fff", 54),
  lambda a, d: f'pop("#t4", {a}); pop("#f4", {a} + 0.1); pop("#p4", {cap("s4", 3)});')

# s5: Kritik
S("s5", HG, titel("t5", "Kritik", 520, W, 66)
  + nl.karte("k5", "Der Paritätische", nl.zeile("r5a", "bis Mitte 2028", "keine Erhöhung", R, ""), y=640),
  lambda a, d: f'pop("#t5", {a}); pop("#k5", {a} + 0.1); pop("#r5a", {cap("s5", 1)});')

# s6: Bundesrat
S("s6", HG, titel("t6", "Wie geht es weiter?", 520, W, 62)
  + nl.karte("k6", "Gesetzgebung", nl.zeile("r6a", "Bundestag", "beschlossen", G, pf(G)) + nl.zeile("r6b", "Bundesrat", "noch offen", O, ""), y=640),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {a} + 0.5); pop("#r6b", {cap("s6", 1)});')


def merk(sid):
    html = (titel(f"t{sid}", "Merk dir", 520, O, 70)
            + nl.karte(f"k{sid}", "Nullrunde bei steigenden Preisen", f'<div style="font-weight:900;font-size:62px;color:{R};text-align:center;padding:14px 0;line-height:1.15">das Geld ist weniger wert ▼</div>', y=660))
    return html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.15);'


def cta(sid, statisch=False):
    html = (beagle(f"fl{sid}", 520) + f'<div id="n{sid}" class="nk-gross" style="top:940px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
            + pille(f"c{sid}", "+ Folgen", 1060, O, "#fff", 58) + pille(f"t{sid}", "Video teilen ↗", 1190, "#1d2330", "#fff", 52))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#fl{sid}", {a}); pop("#n{sid}", {a} + 0.2); pop("#c{sid}", {cap(sid, 1)}); pop("#t{sid}", {cap(sid, 0)} + 0.4);'


h7, j7 = merk("s7")
S("s7", HG, h7, j7)
h8, j8 = cta("s8")
S("s8", HG, h8, j8)
h9, j9 = cta("s9", True)
S("s9", HG, h9, j9)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s4", 3), "richtig"), (cap("s5", 1), "falsch"), (cap("s8", 1), "klick")])
html, code = ls.szene(hell=False)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, news_kopf("28.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.ohne_untertitel_zwischen(HERE, st("s2"), st("s4"))  # kein Untertitel beim Kommentar-Bild (Nutzer 26.11.)
