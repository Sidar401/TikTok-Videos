#!/usr/bin/env python3
"""HundeFinanzTv (~66 s, Stimme Dan, Tempo 1.12) – Rente 2027 +4,09 %, aber Beitrag 2028. NEUES FORMAT (für 24.11.).
Rentenversicherungsbericht 2026 (Kabinett 18.11.): +4,09 % ab 1.7.2027 (Rentenwert 42,52 → 44,26 €), >21 Mio. Rentner, Prognose 4,75 → 4,4 → 4,1,
Beitrag 2027 18,6 %, 2028 19,8 %. Eigene Rechnung: 1.500 € × 4,09 % ≈ 61 €; 0,6 Pkt. AN-Anteil × 3.000 € = 18 €. Ende: Folgen vorletzt, Hinweis letzt."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 13.5)  # Logo-Intro nach s4

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


def balken(id_, y, breite, farbe, text, h=96, gr=38, x=110):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def bar(id_, a):
    return f'tl.fromTo("#{id_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, {a});'


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


# s1 Hook
S("s1", None, nl.CSS + titel("t1", "Rente ab Juli 2027", 340, D, 62) + gross("n1", "+4,09 %", 480, G, 200) + pille("p1", "mehr Rente für alle", 800, G, "#fff", 52),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#n1", {a} + 0.15); pop("#p1", {cap("s1", 1)});')

# s2–s3 Haken + Kommentar-Overlay (stumm)
TXT = "Wie viel Rente bekommst du?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s2"), len(TXT), SFX_CTA, 1.5)
S("s2", None, titel("t2", "Aber ein Haken!", 380, R, 76) + gross("w2", "⚠️", 520, R, 230) + pille("p2", "betrifft vor allem dich", 820, D, "#fff", 46)
  + titel("t3", "Was kostet es ab 2028?", 380, O, 70) + gross("q3", "?", 520, R, 240) + CTA,
  lambda a, d: (f'pop("#t2", {a}); pop("#w2", {a} + 0.2); pop("#p2", {cap("s2", 1)}); tl.set("#t3", {{ opacity: 0 }}, 0); tl.set("#q3", {{ opacity: 0 }}, 0);'
                + raus("t2", st("s3") - 0.05) + raus("w2", st("s3") - 0.05) + raus("p2", st("s3") - 0.05) + f' pop("#t3", {st("s3")}); pop("#q3", {st("s3")} + 0.2);' + cta_js),
  SFX_CTA, bis="s4")
S("s4", None, titel("t4", "Schauen wir genau hin", 640, D, 78) + pille("p4", "Rente 2027", 900, O, "#fff", 50),
  lambda a, d: f'pop("#t4", {a}); pop("#p4", {a} + 0.3);')

# s5 Rentner
S("s5", None, titel("t5", "Diese Menschen bekommen mehr", 340, D, 54) + gross("n5", "21 Mio.+", 480, O, 230) + pille("p5", "Rentner in Deutschland", 800, O, "#fff", 50),
  lambda a, d: f'pop("#t5", {a}); pop("#n5", {cap("s5", 1)}); pop("#p5", {cap("s5", 2)});')

# s6 Rechnung
S("s6", None, titel("t6", "Beispiel-Rechnung", 340, D, 64)
  + nl.karte("k6", "Pro Monat", nl.zeile("r6a", "Rente heute", "1.500 €", D) + nl.zeile("r6b", "Erhöhung", "+4,09 %", G, "▲")
             + f'<div id="r6c" class="nk-row" style="border-top:3px solid {D};margin-top:8px;font-weight:800;color:{D}">Mehr Geld<span class="v" style="color:{G};font-size:56px">≈ +61 €</span></div>', y=500)
  + pille("p6", "brutto, vor Abzügen", 1000, D, "#fff", 42),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {cap("s6", 1)}); pop("#r6b", {cap("s6", 1)} + 0.5); pop("#r6c", {cap("s6", 2)}); pop("#p6", {cap("s6", 3)});')

# s7–s8 Prognose gesenkt
S("s7", None, titel("t7", "Vor einem Jahr", 340, D, 64) + gross("n7", "4,75 %", 480, O, 250) + pille("p7", "so lautete die Prognose", 800, D, "#fff", 46),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {cap("s7", 1)}); pop("#p7", {cap("s7", 2)});')
S("s8", None, titel("t8", "Prognose 2027", 340, D, 62) + balken("b8a", 500, 760, "#8a93a1", "Nov. 2025 · 4,75 %") + balken("b8b", 630, 700, O, "Frühjahr 2026 · 4,4 %") + balken("b8c", 760, 655, R, "Jetzt · 4,1 %")
  + pille("p8", "3× gesenkt ▼", 920, R, "#fff", 52),
  lambda a, d: f'pop("#t8", {a}); {bar("b8a", cap("s8", 0) + 0.3)} {bar("b8b", cap("s8", 1))} {bar("b8c", cap("s8", 1) + 1.0)} pop("#p8", {cap("s8", 3)});')
S("s9", None, titel("t9", "Verbindlich erst im", 340, D, 62) + gross("n9", "Frühjahr 2027", 460, O, 100)
  + nl.karte("k9", "Bis dahin", f'<div style="font-weight:800;font-size:52px;color:{D};text-align:center;padding:14px 0">Modellrechnung,<br/><span style="color:{R}">noch keine Garantie</span></div>', y=700),
  lambda a, d: f'pop("#t9", {a}); pop("#n9", {cap("s9", 0)} + 0.3); pop("#k9", {cap("s9", 2)});')

# s10–s12 Beitrag
S("s10", None, titel("t10", "Der Haken: Rentenbeitrag", 340, R, 60) + gross("n10", "18,6 %", 480, D, 250) + pille("p10", "2027 noch stabil", 800, D, "#fff", 50),
  lambda a, d: f'pop("#t10", {a}); pop("#n10", {cap("s10", 1)}); pop("#p10", {cap("s10", 3)});')
S("s11", None, titel("t11", "Rentenbeitrag", 340, D, 64) + balken("b11a", 520, 560, "#8a93a1", "2027 · 18,6 %") + balken("b11b", 650, 600, R, "2028 · 19,8 % ▲")
  + pille("p11", "laut Rentenbericht", 800, D, "#fff", 44),
  lambda a, d: f'pop("#t11", {a}); {bar("b11a", a + 0.3)} {bar("b11b", cap("s11", 1))} pop("#p11", {cap("s11", 2)});')
S("s12", None, titel("t12", "Bei 3.000 € brutto", 340, D, 64)
  + nl.karte("k12", "Dein Anteil (die Hälfte)", nl.zeile("r12a", "Mehr Beitrag", "+0,6 %", R) + nl.zeile("r12b", "Im Monat", "≈ +18 €", R, "▲"), y=520),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 1)}); pop("#r12b", {cap("s12", 3)});')

# s13 Merk dir
S("s13", None, titel("t13", "Merk dir", 340, O, 70)
  + nl.karte("k13", "Rente 2027/28", nl.zeile("r13a", "Rentner", "mehr Geld", G, "▲") + nl.zeile("r13b", "Arbeitnehmer", "mehr Beitrag", R, "▲"), y=500),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.1); pop("#r13a", {cap("s13", 1)}); pop("#r13b", {cap("s13", 2)});')


def folgen(sid, statisch=False):
    html = (f'<div id="fl{sid}" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
            f'<div id="n{sid}" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille(f"c{sid}", "+ Folgen", 1040, O, "#fff", 58))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#fl{sid}", {a}); pop("#n{sid}", {a} + 0.2); pop("#c{sid}", {cap(sid, 0)} + 0.4);'


h14, j14 = folgen("s14")
S("s14", None, h14, j14)
h15, j15 = folgen("s15", True)
S("s15", None, h15, j15)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "alarm"), (cap("s6", 2), "kasse"), (cap("s8", 3), "kurve-runter"), (cap("s11", 1), "kurve-hoch"), (cap("s13", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "24.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
