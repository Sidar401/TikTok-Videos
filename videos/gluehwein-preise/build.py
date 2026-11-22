#!/usr/bin/env python3
"""HundeFinanzTv (~64 s, Stimme Dan, Tempo 1.05) – Glühwein-Preise 2026. NEUES FORMAT + Kommentar-Overlay (wie cta-demo-1) bei Satz 2.
Ø 4,50–5 €/Tasse, München bis 7 €, günstig ≈ 3,50 €, Pfand 2–3 €; 0,2 l → 25 €/l vs. Supermarkt < 3 €/l; MwSt 19 %: 5 € = 4,20 € + 0,80 €;
Budget: 2 Tassen + Wurst ≈ 15 €. Quellen: ms-aktuell, tageskarte, inside-digital."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 11)  # Logo nach dem Open Loop (s3)

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 13, [])
cap, st = K.cap, K.st
S = K.szene
SFX_CTA = []


def titel(id_, text, y=340, farbe=D, gr=70):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=50):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe}">{text}</div>'


TASSE = (f'<div class="nk-karte" id="tk1" style="left:110px;top:360px;width:860px;text-align:center"><div class="nk-kt">Glühwein 2026</div>'
         f'<div style="font-weight:900;font-size:170px;color:{R};line-height:1.1">5 €</div><div style="font-size:46px;color:#3a414c">pro Tasse</div></div>')
CTA = nl.cta_overlay("co", "Kommentare", "Meine Meinung dazu", "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 840)
cta_js = nl.cta_overlay_js("co", st("s2"), len("Meine Meinung dazu"), SFX_CTA, 1.2)

# s1–s2 Hook + Kommentar-Overlay (Satz 2)
S("s1", None, nl.CSS + TASSE + pille("p1", "auf vielen Weihnachtsmärkten", 780, D, "#fff", 44) + CTA,
  lambda a, d: (KIT_JS + f' pop("#tk1", {a}); pop("#p1", {cap("s1", 1)}); tl.to("#p1", {{ opacity: 0, duration: 0.2 }}, {st("s2")} - 0.1);' + cta_js),
  SFX_CTA, bis="s3")

# s3 Open Loop
S("s3", None, titel("t3", "Wie viel kassiert der Staat?", 360, R, 60)
  + nl.karte("k3", "Gleich die Rechnung", f'<div style="font-weight:900;font-size:180px;color:{R};text-align:center;line-height:1.1">?</div>', y=560),
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {cap("s3", 1)});')

# s4–s6 Preise
S("s4", None, titel("t4", "Preise 2026", 340) + nl.karte("k4", "Glühwein pro Tasse",
  nl.zeile("r4", "Im Schnitt", "4,50 – 5 €", O) + nl.zeile("r5", "München", "bis 7 €", R, "▲") + nl.zeile("r6", "Günstigste Märkte", "≈ 3,50 €", G), y=520),
  lambda a, d: f'pop("#t4", {a}); pop("#k4", {a} + 0.1); pop("#r4", {cap("s4", 1)}); pop("#r5", {cap("s5", 1)}); pop("#r6", {cap("s6", 1)});', [], bis="s7")

# s7 Pfand
S("s7", None, titel("t7", "Dazu: Pfand", 340) + nl.karte("k7", "Für die Tasse", nl.zeile("r7", "Pfand", "2 – 3 €", O), y=520)
  + pille("p7", "manchmal mehr als der Glühwein!", 860, R, "#fff", 46),
  lambda a, d: f'pop("#t7", {a}); pop("#k7", {cap("s7", 0)} + 0.3); pop("#r7", {cap("s7", 1)}); pop("#p7", {cap("s7", 2)});')

# s8–s9 Rechnung pro Liter
S("s8", None, titel("t8", "Jetzt rechnen wir", 340) + nl.karte("k8", "Pro Liter",
  nl.zeile("r8", "Eine Tasse", "200 ml", D) + nl.zeile("r9a", "5 € ÷ 0,2 Liter", "=", D), y=500) + gross("n9", "25 € / Liter", 900, R, 120),
  lambda a, d: f'pop("#t8", {a}); pop("#k8", {a} + 0.1); pop("#r8", {cap("s8", 1)}); pop("#r9a", {cap("s9", 0)}); pop("#n9", {cap("s9", 1)});', [], bis="s10")

# s10 Supermarkt-Vergleich
S("s10", None, titel("t10", "Zum Vergleich", 340) + nl.karte("k10", "Ein Liter Glühwein",
  nl.zeile("r10a", "Weihnachtsmarkt", "25 €", R) + nl.zeile("r10b", "Supermarkt", "unter 3 €", G), y=500) + pille("p10", "fast 10× teurer", 860, R, "#fff", 56),
  lambda a, d: f'pop("#t10", {a}); pop("#k10", {a} + 0.1); pop("#r10a", {cap("s10", 0)} + 0.3); pop("#r10b", {cap("s10", 1)}); pop("#p10", {cap("s10", 2)});')

# s11 Mehrwertsteuer: Balken 4,20 € + 0,80 €
BAR = (f'<div id="b11" style="position:absolute;left:110px;top:640px;width:860px;height:120px;display:flex;border-radius:16px;overflow:hidden;box-shadow:0 12px 26px #0002;z-index:4">'
       f'<div style="flex:420;background:{O};color:#fff;font-weight:900;font-size:48px;display:flex;align-items:center;justify-content:center">4,20 € Glühwein</div>'
       f'<div id="b11s" style="flex:110;background:{R};color:#fff;font-weight:900;font-size:36px;white-space:nowrap;display:flex;align-items:center;justify-content:center">0,80 €</div></div>')
S("s11", None, titel("t11", "Und der Staat?", 340, R) + gross("n11", "5 € Tasse", 470, D, 90) + BAR
  + pille("p11", "≈ 80 Cent Mehrwertsteuer (19 %)", 820, R, "#fff", 46),
  lambda a, d: (f'pop("#t11", {a}); pop("#n11", {cap("s11", 1)}); tl.fromTo("#b11", {{ scaleX: 0, transformOrigin: "0 50%" }}, {{ scaleX: 1, duration: 0.7 }}, {cap("s11", 1)} + 0.3);'
                f' pop("#p11", {cap("s11", 2)}); tl.fromTo("#b11s", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.25, yoyo: true, repeat: 3 }}, {cap("s11", 2)});'))

# s12 Tipp: Budget
S("s12", None, titel("t12", "Unser Tipp: Budget", 340, G) + nl.karte("k12", "Schnell zusammen",
  nl.zeile("r12a", "2 Tassen Glühwein", "10 €", D) + nl.zeile("r12b", "1 Bratwurst", "≈ 5 €", D)
  + f'<div id="r12c" class="nk-row" style="border-top:3px solid {D};margin-top:8px;font-weight:800;color:{D}">Summe<span class="v" style="color:{R};font-size:56px">≈ 15 €</span></div>', y=500),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 2)}); pop("#r12b", {cap("s12", 3)}); pop("#r12c", {cap("s12", 4)});')

# s13 Folgen
S("s13", None, f'<div id="fl13" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n13" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c13", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl13", {a}); pop("#n13", {a} + 0.2); pop("#c13", {cap("s13", 0)} + 0.4);')

K.SFX.extend([(0.05, "bass-schlag"), (cap("s7", 2), "falsch"), (cap("s9", 0), "taschenrechner"),
              (cap("s12", 4), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "22.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
