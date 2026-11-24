#!/usr/bin/env python3
"""HundeFinanzTv (~114 s, Stimme Dan, Tempo 1.12, 1. Satz +4,5 dB) – Gedankenspiel: Crash spart den USA Zinsen (24.11.2026). NEUES FORMAT.
Zahlen: US-Schulden 40,71 Bio. $ (20.11., Treasury), ~⅓ der handelbaren Schuld in 12 Mon. (GAO: 9,7 Bio. $ FY2026), Zinsen ≈ 1 Bio. (bis 1,4) $/Jahr,
1 Pp × 10 Bio. $ = ≈ 100 Mrd. $ (eigene Rechnung), 10J-Rendite 4,99 % (27.10.) → ≈ 4,25 % (Mitte Nov.; Quellen teils widersprüchlich), Sept.: > 5 % bei globalem Ausverkauf.
Wichtig: Gedankenspiel, KEIN Beleg für Absicht."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

_t = json.loads((HERE / "timings.json").read_text())
T0 = ls.einfuegen(HERE, next(s["end"] for s in _t["saetze"] if s["id"] == "s5") - 0.01)  # Logo-Intro nach s5

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 24, [], logos=["flagge-usa.svg"])
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


def flagge(id_, y, w=300, h=170):
    return (f'<div id="{id_}" class="nk-karte" style="left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;padding:18px">'
            f'<img src="assets/logos/flagge-usa.svg" style="width:100%;height:{h - 36}px;object-fit:contain"/></div>')


def balken(id_, y, breite, farbe, text, h=96, gr=38, x=110):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def bar(id_, a):
    return f'tl.fromTo("#{id_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, {a});'


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


def kk(id_, kopf, text, y):
    return nl.karte(id_, kopf, f'<div style="font-weight:800;font-size:52px;color:{D};text-align:center;padding:14px 0;line-height:1.25">{text}</div>', y=y)


# s1 Hook (laut)
S("s1", None, nl.CSS + nl.karte("k1a", "Dein Depot", f'<div style="font-weight:900;font-size:110px;color:{R};text-align:center;line-height:1.1">Verlust ▼</div>', y=330)
  + nl.karte("k1b", "Die USA", f'<div style="font-weight:900;font-size:110px;color:{G};text-align:center;line-height:1.1">sparen ▲ ?</div>', y=700)
  + pille("p1", "Milliarden", 1040, O, "#fff", 60),
  lambda a, d: KIT_JS + f' pop("#k1a", {a}); pop("#k1b", {a} + 0.5); pop("#p1", {a} + 1.2);')

# s2 Gedankenspiel
S("s2", None, titel("t2", "Nur ein Gedankenspiel", 380, O, 70) + gross("w2", "💭", 520, D, 220)
  + kk("k2", "Wichtig", "Dass eine Regierung einen Crash will,<br/><span style=\"color:#d23c3c\">ist nicht bewiesen</span>", 840),
  lambda a, d: f'pop("#t2", {a}); pop("#w2", {a} + 0.2); pop("#k2", {cap("s2", 1)});')

# s3–s4 Zahlen + Kommentar-Overlay (stumm)
TXT = "Droht ein Börsencrash?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.4)
S("s3", None, titel("t3", "Die Zahlen sind krass", 380, D, 66) + gross("n3", "40,71 Bio. $", 520, R, 130) + titel("t4", "Was heißt das für dein Depot?", 400, O, 50) + gross("q4", "?", 520, R, 220) + CTA,
  lambda a, d: (f'pop("#t3", {a}); pop("#n3", {cap("s3", 1)}); tl.set("#t4", {{ opacity: 0 }}, 0); tl.set("#q4", {{ opacity: 0 }}, 0);' + raus("t3", st("s4") - 0.05) + raus("n3", st("s4") - 0.05)
                + f' pop("#t4", {st("s4")}); pop("#q4", {st("s4")} + 0.2);' + cta_js), SFX_CTA, bis="s5")
S("s5", None, titel("t5", "Schauen wir genau hin", 640, D, 78) + pille("p5", "Schulden · Zinsen · Anleger", 900, O, "#fff", 46),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {a} + 0.3);')

# s6 Schulden
S("s6", None, titel("t6", "US-Staatsschulden", 340, D, 62) + flagge("f6", 440) + gross("n6", "40,71 Bio. $", 660, R, 130) + pille("p6", "Stand 20. November", 880, D, "#fff", 44),
  lambda a, d: f'pop("#t6", {a}); pop("#f6", {a} + 0.1); pop("#n6", {cap("s6", 1)}); pop("#p6", {cap("s6", 2)});')
S("s7", None, titel("t7", "In 12 Monaten neu finanzieren", 340, D, 54) + gross("n7", "⅓", 440, O, 260) + kk("k7", "Dieses Jahr (GAO)", "≈ <span style=\"color:#d23c3c\">9,7 Billionen $</span>", 800),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {a} + 0.15); pop("#k7", {cap("s7", 2)});')
S("s8", None, titel("t8", "Der Trick", 340, O, 66)
  + nl.karte("k8", "So läuft es", nl.zeile("r8a", "Alte Schulden fällig", "▼", R) + nl.zeile("r8b", "Neue Schulden aufnehmen", "▲", O) + nl.zeile("r8c", "Alte damit bezahlen", "✓", G), y=500),
  lambda a, d: f'pop("#t8", {a}); pop("#k8", {a} + 0.1); pop("#r8a", {a} + 0.6); pop("#r8b", {cap("s8", 2)}); pop("#r8c", {cap("s8", 3)});')
S("s9", None, titel("t9", "Das Problem", 340, D, 66) + gross("n9", "Zinsen ▲", 480, R, 200) + pille("p9", "höher als vor ein paar Jahren", 800, R, "#fff", 46),
  lambda a, d: f'pop("#t9", {a}); pop("#n9", {a} + 0.2); pop("#p9", {cap("s9", 1)});')
S("s10", None, titel("t10", "Nur für Zinsen", 340, D, 64) + gross("n10", "≈ 1 Bio. $", 470, R, 190) + pille("p10", "pro Jahr (bis zu 1,4 Bio.)", 800, R, "#fff", 46),
  lambda a, d: f'pop("#t10", {a}); pop("#n10", {cap("s10", 1)}); pop("#p10", {cap("s10", 3)});')

# s11–s13 Mechanismus
S("s11", None, titel("t11", "Der Mechanismus", 340, O, 66)
  + nl.karte("k11", "Schritt 1", f'<div style="font-weight:900;font-size:70px;color:{R};text-align:center;line-height:1.2">Aktien ▼<br/>Anleger: Angst</div>', y=520),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {cap("s11", 1)});')
S("s12", None, titel("t12", "Der Mechanismus", 340, O, 66)
  + nl.karte("k12", "Schritt 2", f'<div style="font-weight:900;font-size:62px;color:{D};text-align:center;line-height:1.2">Flucht in sichere<br/><span style="color:{G}">US-Staatsanleihen</span></div>', y=520),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {cap("s12", 1)});')
S("s13", None, titel("t13", "Der Mechanismus", 340, O, 66)
  + nl.karte("k13", "Schritt 3", nl.zeile("r13a", "Nachfrage", "▲", G) + nl.zeile("r13b", "Rendite (= Zins für den Staat)", "▼", G), y=520),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.1); pop("#r13a", {cap("s13", 1)}); pop("#r13b", {cap("s13", 2)});')

# s14–s15 Rechnung
S("s14", None, titel("t14", "Die Rechnung", 340, D, 66)
  + nl.karte("k14", "Zinsen −1 Prozentpunkt", nl.zeile("r14a", "Schulden zum Ersetzen", "≈ 10 Bio. $", D) + nl.zeile("r14b", "× 1 %", "=", D)
             + f'<div id="r14c" class="nk-row" style="border-top:3px solid {D};margin-top:8px;font-weight:800;color:{D}">Ersparnis / Jahr<span class="v" style="color:{G};font-size:56px">≈ 100 Mrd. $</span></div>', y=480),
  lambda a, d: f'pop("#t14", {a}); pop("#k14", {a} + 0.1); pop("#r14a", {cap("s14", 1)}); pop("#r14b", {cap("s14", 2)}); pop("#r14c", {cap("s14", 3)});')
S("s15", None, gross("n15", "100 Mrd. $", 400, G, 180) + pille("p15", "jedes Jahr", 700, G, "#fff", 56) + pille("p15b", "durch nur 1 Prozentpunkt", 840, D, "#fff", 46),
  lambda a, d: f'pop("#n15", {a}); pop("#p15", {cap("s15", 1)}); pop("#p15b", {cap("s15", 2)});')

# s16 Rendite gefallen
S("s16", None, titel("t16", "Rendite 10-jährige US-Anleihen", 340, D, 52) + balken("b16a", 520, 760, O, "Ende Oktober · ≈ 4,99 %") + balken("b16b", 650, 650, G, "Mitte November · ≈ 4,25 % ▼")
  + pille("p16", "Quellen teils uneinheitlich", 820, D, "#fff", 40),
  lambda a, d: f'pop("#t16", {a}); {bar("b16a", cap("s16", 1))} {bar("b16b", cap("s16", 3))} pop("#p16", {cap("s16", 3)} + 0.8);')

# s17–s18 Gegenbeweis
S("s17", None, titel("t17", "Aber Vorsicht!", 340, R, 70) + kk("k17", "September 2026", "Globaler Ausverkauf:<br/>Rendite <span style=\"color:#d23c3c\">über 5 % ▲</span>", 540),
  lambda a, d: f'pop("#t17", {a}); pop("#k17", {cap("s17", 1)});')
S("s18", None, titel("t18", "Also gilt nicht automatisch", 340, D, 56)
  + nl.karte("k18", "Aktien ▼", nl.zeile("r18a", "Zinsen sinken immer?", "✗", R) + nl.zeile("r18b", "Manchmal ja, manchmal nein", "≈", O), y=520),
  lambda a, d: f'pop("#t18", {a}); pop("#k18", {a} + 0.1); pop("#r18a", {cap("s18", 1)}); pop("#r18b", {cap("s18", 2)});')

# s19–s20 Gegenargumente
S("s19", None, titel("t19", "Ein Crash kostet auch", 340, D, 62)
  + nl.karte("k19", "Folgen", nl.zeile("r19a", "Wirtschaft schwächer", "▼", R) + nl.zeile("r19b", "Das kostet den Staat selbst Geld", "€", R), y=520),
  lambda a, d: f'pop("#t19", {a}); pop("#k19", {a} + 0.1); pop("#r19a", {cap("s19", 1)}); pop("#r19b", {cap("s19", 2)});')
S("s20", None, titel("t20", "Beleg für einen gewollten Crash?", 340, D, 52) + gross("n20", "Keiner", 480, R, 220) + pille("p20", "nur eine Überlegung", 820, D, "#fff", 50),
  lambda a, d: f'pop("#t20", {a}); pop("#n20", {cap("s20", 1)}); pop("#p20", {cap("s20", 3)});')

# s21 Depot
S("s21", None, titel("t21", "Und dein Depot?", 340, D, 66)
  + nl.karte("k21", "Bei einem Crash", nl.zeile("r21a", "Du", "Verlust sofort ▼", R) + nl.zeile("r21b", "Zinsvorteil Staat", "nichts für dich", O), y=500),
  lambda a, d: f'pop("#t21", {a}); pop("#k21", {a} + 0.1); pop("#r21a", {cap("s21", 1)}); pop("#r21b", {cap("s21", 2)});')

# s22 Merk dir
S("s22", None, titel("t22", "Merk dir", 340, O, 70)
  + nl.karte("k22", "An der Börse geht es um", nl.zeile("r22a", "Aktienkurse", "✓", G) + nl.zeile("r22b", "Zinsen", "✓", G) + nl.zeile("r22c", "Schulden", "✓", G), y=500),
  lambda a, d: f'pop("#t22", {a}); pop("#k22", {a} + 0.1); pop("#r22a", {cap("s22", 1)}); pop("#r22b", {cap("s22", 1)} + 0.6); pop("#r22c", {cap("s22", 2)});')


def folgen(sid, statisch=False):
    html = (f'<div id="fl{sid}" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
            f'<div id="n{sid}" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille(f"c{sid}", "+ Folgen", 1040, O, "#fff", 58))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#fl{sid}", {a}); pop("#n{sid}", {a} + 0.2); pop("#c{sid}", {cap(sid, 0)} + 0.4);'


h23, j23 = folgen("s23")
S("s23", None, h23, j23)
h24, j24 = folgen("s24", True)
S("s24", None, h24, j24)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "alarm"), (cap("s7", 1), "uhr-tickt"), (cap("s10", 1), "kasse"), (cap("s13", 2), "kurve-runter"),
              (cap("s14", 3), "richtig"), (cap("s17", 1), "falsch"), (cap("s22", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("BÖRSENNEWS", "24.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
