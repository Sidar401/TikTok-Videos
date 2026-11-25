#!/usr/bin/env python3
"""HundeFinanzTv (~74 s, Stimme Dan, Tempo 1.12) – Hast du genug gespart? Faustregel nach Alter (Fidelity). NEUES FORMAT, Puffer ohne Datum.
Fidelity-Richtwert (USA): 1× Jahresgehalt mit 30, 3× mit 40, 6× mit 50, 8× mit 60, 10× mit 67; Annahme 15 % Sparquote ab 25, ≥ 50 % Aktien.
Eigene Rechnung: 40.000 € brutto → 40.000 / 120.000 / 240.000 / 320.000 / 400.000 €; 15 % = 6.000 €/Jahr = 500 €/Monat.
Hook-Stil A (normal). Teilen-/Folgen-CTA als Satz 2 (Regel 25.11.), Hinweis letzter Satz."""
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
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 15, [])
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


def balken(id_, y, breite, farbe, text, h=96, gr=40, x=110):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def bar(id_, a):
    return f'tl.fromTo("#{id_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, {a});'


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


def kk(id_, kopf, text, y):
    return nl.karte(id_, kopf, f'<div style="font-weight:800;font-size:52px;color:{D};text-align:center;padding:14px 0;line-height:1.25">{text}</div>', y=y)


def beagle(id_, y=330):
    return (f'<div id="{id_}" style="position:absolute;left:340px;top:{y}px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>')


# s1 Hook A
S("s1", None, nl.CSS + titel("t1", "Mit 40 Jahren", 340, D, 66) + gross("n1", "3×", 450, G, 330) + pille("p1", "Jahresgehalt gespart?", 850, G, "#fff", 56),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#n1", {a} + 0.2); pop("#p1", {cap("s1", 1)});')

# s2 CTA Teilen + Folgen
S("s2", None, beagle("fl2", 340) + f'<div id="n2" class="nk-gross" style="top:770px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + pille("c2", "+ Folgen", 890, O, "#fff", 58) + pille("t2", "Video teilen ↗", 1040, D, "#fff", 52),
  lambda a, d: f'pop("#fl2", {a}); pop("#n2", {a} + 0.2); pop("#c2", {cap("s2", 1)}); pop("#t2", {cap("s2", 0)} + 0.4);')

# s3–s4 Open Loop + Kommentar-Overlay (stumm)
TXT = "Wie viel hast du schon gespart?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.4)
S("s3", None, titel("t3", "Wie viel im Monat?", 380, O, 70) + gross("q3", "?", 520, R, 220) + CTA,
  lambda a, d: f'pop("#t3", {a}); pop("#q3", {a} + 0.2);' + cta_js, SFX_CTA, bis="s5")
S("s5", None, titel("t5", "Die Faustregel", 340, O, 70)
  + nl.karte("k5", "Fidelity · USA", nl.zeile("r5a", "Richtwert", "Jahresgehälter", D) + nl.zeile("r5b", "Bis zum Ruhestand mit", "67", O), y=500),
  lambda a, d: f'pop("#t5", {a}); pop("#k5", {a} + 0.1); pop("#r5a", {cap("s5", 1)}); pop("#r5b", {cap("s5", 3)});')

# s6–s7 Treppe
W = {30: 86, 40: 258, 50: 516, 60: 688, 67: 860}
S("s6", None, titel("t6", "So viel Gehalt gespart", 340, D, 60) + balken("b30", 480, 400, "#8a93a1", "Mit 30 · 1×") + balken("b40", 610, 560, G, "Mit 40 · 3×") + balken("b50", 740, 760, O, "Mit 50 · 6×"),
  lambda a, d: f'pop("#t6", {a}); {bar("b30", cap("s6", 0) + 0.2)} {bar("b40", cap("s6", 2))} {bar("b50", cap("s6", 3))}')
S("s7", None, titel("t7", "So viel Gehalt gespart", 340, D, 60) + balken("b60", 480, 700, O, "Mit 60 · 8×") + balken("b67", 610, 860, R, "Mit 67 · 10×") + pille("p7", "Jahresgehälter", 800, D, "#fff", 46),
  lambda a, d: f'pop("#t7", {a}); {bar("b60", a + 0.2)} {bar("b67", cap("s7", 2))} pop("#p7", {cap("s7", 2)} + 0.5);')

# s8–s9 Beispiel
S("s8", None, titel("t8", "Beispiel", 340, D, 64)
  + nl.karte("k8", "Brutto im Jahr", nl.zeile("r8a", "Gehalt", "40.000 €", D) + nl.zeile("r8b", "Mit 40 gespart", "≈ 120.000 €", G, "✓"), y=500),
  lambda a, d: f'pop("#t8", {a}); pop("#k8", {a} + 0.1); pop("#r8a", {cap("s8", 1)}); pop("#r8b", {cap("s8", 2)});')
S("s9", None, titel("t9", "Mit 67", 340, D, 66) + gross("n9", "400.000 €", 480, G, 150) + pille("p9", "= 10 Jahresgehälter", 800, G, "#fff", 52),
  lambda a, d: f'pop("#t9", {a}); pop("#n9", {a} + 0.2); pop("#p9", {cap("s9", 1)});')

# s10 unmöglich?
S("s10", None, titel("t10", "3× mit 40?", 380, D, 80) + gross("w10", "😰", 520, D, 230) + pille("p10", "klingt unmöglich", 840, R, "#fff", 52),
  lambda a, d: f'pop("#t10", {a}); pop("#w10", {a} + 0.2); pop("#p10", {cap("s10", 1)});')

# s11–s12 Zahl dahinter
S("s11", None, titel("t11", "Die Zahl dahinter", 340, D, 64) + gross("n11", "15 %", 460, O, 250) + pille("p11", "des Gehalts · ab 25", 800, O, "#fff", 52),
  lambda a, d: f'pop("#t11", {a}); pop("#n11", {cap("s11", 1)}); pop("#p11", {cap("s11", 2)});')
S("s12", None, titel("t12", "Bei 40.000 € Gehalt", 340, D, 64)
  + nl.karte("k12", "15 % sparen", nl.zeile("r12a", "Im Jahr", "6.000 €", O)
             + f'<div id="r12b" class="nk-row" style="border-top:3px solid {D};margin-top:8px;font-weight:800;color:{D}">Im Monat<span class="v" style="color:{G};font-size:60px">≈ 500 €</span></div>', y=500),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 1)}); pop("#r12b", {cap("s12", 3)});')

# s13 Vorsicht
S("s13", None, titel("t13", "Aber Vorsicht", 340, R, 70) + gross("w13", "⚠️", 450, D, 190)
  + kk("k13", "Nur eine Faustregel aus den USA", "In Deutschland kommt noch die<br/><span style=\"color:#22a35a\">gesetzliche Rente</span> dazu", 760),
  lambda a, d: f'pop("#t13", {a}); pop("#w13", {a} + 0.2); pop("#k13", {cap("s13", 3)});')


def merk(sid, statisch=False):
    html = (titel(f"t{sid}", "Merk dir", 340, O, 70)
            + nl.karte(f"k{sid}", "Beim Sparen", nl.zeile(f"r{sid}a", "Früh anfangen", "✓", G) + nl.zeile(f"r{sid}b", "Auch kleine Beträge helfen", "✓", G)
                       + nl.zeile(f"r{sid}c", "Regel nicht genau erreichen", "✓", G), y=500))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.1); pop("#r{sid}a", {cap(sid, 0)} + 0.4); pop("#r{sid}b", {cap(sid, 1)}); pop("#r{sid}c", {cap(sid, 2)});'


h14, j14 = merk("s14")
S("s14", None, h14, j14)
h15, j15 = merk("s15", True)
S("s15", None, h15, j15)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "klick"), (cap("s6", 2), "kurve-hoch"), (cap("s9", 1), "kasse"), (cap("s10", 1), "falsch"), (cap("s12", 3), "richtig"), (cap("s13", 0), "alarm"), (cap("s14", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("GELD-WISSEN", ""), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
