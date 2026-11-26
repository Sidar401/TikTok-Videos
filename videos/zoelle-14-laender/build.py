#!/usr/bin/env python3
"""HundeFinanzTv Short 27.11.2026 (~45 s, dunkler Look, TREND): Trump schlägt Section-301-Zölle auf 14 Handelspartner vor (25.11.2026): China 20 %, EU 15 %,
noch nicht in Kraft (Konsultation, frühestens 2027). Reihenfolge: Hook → Inhalt → Merk dir → CTA → Hinweis; kein Untertitel beim Kommentar-Bild."""
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
from analyse_kit import KIT_JS, news_kopf  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, O, W = "#22c55e", "#ff4d4d", nl.ORANGE, "#ffffff"
HAS_TRUMP = (W_ / "brand/fotos/donald-trump.jpg").exists()
K = Kit(HERE, 9, ["frei-code-monitor"], logos=["flagge-usa.svg", "flagge-china.svg", "flagge-eu.svg"], fotos=(["donald-trump.jpg"] if HAS_TRUMP else []))
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


def flagge(f, h=56):
    return f'<img src="assets/logos/{f}" style="height:{h}px;vertical-align:middle"/>'


def foto(id_, y=500, d=400):
    return (f'<div id="{id_}" style="position:absolute;left:{(1080 - d) // 2}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 0 60px {O}88;z-index:4"><img src="assets/fotos/donald-trump.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 15%"/></div>'
            f'<div style="position:absolute;left:0;width:1080px;top:{y + d + 16}px;text-align:center;font-size:26px;font-weight:600;color:#cbd5e1;z-index:5">Foto: Offizielles Porträt · gemeinfrei</div>')


# s1 Hook
if HAS_TRUMP:
    h1 = nl.CSS + DUNKEL_CSS + foto("ph1", 480, 380) + gross("n1", "NEUE ZÖLLE", 920, R, 150) + pille("p1", "auf 14 Länder · auch Europa", 1110, "#1d2330", "#fff", 46)
else:
    h1 = nl.CSS + DUNKEL_CSS + gross("n1", "NEUE ZÖLLE", 580, R, 132) + gross("n1b", "14 Länder", 760, W, 170) + pille("p1", "auch Europa", 1010, O, "#fff", 60)
S("s1", HG, h1, lambda a, d: KIT_JS + f' tl.set("#n1", {{ opacity: 1 }}, 0); pop("#n1", {a}); pop("#p1", {a} + 0.2);' + (f' pop("#ph1", {a});' if HAS_TRUMP else f' pop("#n1b", {a} + 0.1);'))

# s2–s3: Kommentar-Bild (ohne Untertitel)
TXT = "Trifft dich das?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 960)
cta_js = nl.cta_overlay_js("co", st("s2"), len(TXT), SFX_CTA, 1.2)
S("s2", HG, titel("t2", "US-Vorschlag vom Mittwoch", 520, W, 56)
  + nl.karte("k2", "Neue Zölle", nl.zeile("r2a", flagge("flagge-usa.svg") + " Länder betroffen", "14", R, ""), y=610)
  + pille("p3", flagge("flagge-china.svg", 44) + " China: 20 %", 850, R, "#fff", 46) + CTA,
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {a} + 0.1); pop("#r2a", {a} + 0.5); pop("#p3", {cap("s3", 0)});' + cta_js, SFX_CTA, bis="s4")

# s4 EU 15 %
S("s4", HG, titel("t4", "Und die EU?", 520, W, 66) + f'<div id="f4" style="position:absolute;left:290px;top:640px;width:500px;z-index:4">{flagge("flagge-eu.svg", 300)}</div>'
  + gross("n4", "15 %", 980, R, 190) + pille("p4", "Grenze aus dem Abkommen 2025", 1210, O, "#fff", 44),
  lambda a, d: f'pop("#t4", {a}); pop("#f4", {a} + 0.1); pop("#n4", {cap("s4", 0)}); pop("#p4", {cap("s4", 2)});')

# s5 EU-Kommission
S("s5", HG, titel("t5", "Reaktion der EU", 520, W, 66)
  + nl.karte("k5", flagge("flagge-eu.svg", 52) + " EU-Kommission", nl.zeile("r5a", "Vorwürfe", "zurückgewiesen", R, "") + nl.zeile("r5b", "Gespräche", "gewünscht", G, ""), y=640),
  lambda a, d: f'pop("#t5", {a}); pop("#k5", {a} + 0.1); pop("#r5a", {cap("s5", 1)}); pop("#r5b", {cap("s5", 2)});')

# s6 noch nichts in Kraft
S("s6", HG, titel("t6", "Noch nicht in Kraft", 520, W, 66)
  + nl.karte("k6", "So geht es weiter", nl.zeile("r6a", "Öffentliche Anhörung", "zuerst", O, "") + nl.zeile("r6b", "Zölle gelten", "frühestens 2027", R, ""), y=640),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {cap("s6", 2)}); pop("#r6b", {cap("s6", 4)});')


def merk(sid):
    html = (titel(f"t{sid}", "Merk dir", 520, O, 70)
            + nl.karte(f"k{sid}", "Ein Vorschlag", f'<div style="font-weight:900;font-size:62px;color:{O};text-align:center;padding:14px 0;line-height:1.15">ist noch kein Zoll, aber die Börsen reagieren sofort</div>', y=660))
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

K.SFX.extend([(0.05, "bass-schlag"), (cap("s4", 0), "falsch"), (cap("s5", 2), "richtig"), (cap("s7", 1), "richtig"), (cap("s8", 1), "klick")])
html, code = ls.szene(hell=False)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, news_kopf("27.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.ohne_untertitel_zwischen(HERE, st("s2"), st("s4"))  # kein Untertitel beim Kommentar-Bild (Nutzer 26.11.)
