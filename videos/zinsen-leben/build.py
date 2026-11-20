#!/usr/bin/env python3
"""HundeFinanzTv (~1:42, Stimme Dan) – Wie viel Geld, um von Zinsen zu leben? NEUES FORMAT (heller News-Look).
2.000 €/Monat = 24.000 €/Jahr, 4-%-Regel (Trinity-Studie 1998) → 600.000 €; 7 %: 200 € ≈ 42 J., 500 € ≈ 30 J., 1.000 € ≈ 22 J.;
500 € × 30 J. = 180.000 € eingezahlt, ≈ 610.000 € (430.000 € Zinseszins); 10 J. später ≈ 260.000 €; 2 % Inflation: 2.000 € → 1.100 € Kaufkraft;
Teilziel 300.000 € = 1.000 €/Monat.   Aufruf: python3 build.py [--quer]  (16:9 für YouTube → index.html wird überschrieben, Render vorher!)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
QUER = "--quer" in sys.argv
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 11)  # Logo nach dem Open Loop (s3)

import glow_short as gs  # noqa: E402
if QUER:
    gs.querformat()
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
import lf_kit  # noqa: E402
from lf_kit import Kit  # noqa: E402
if QUER:
    nl.foto = lambda *a, **k: ''  # Fotos würden nur als schmaler Streifen erscheinen
if QUER:  # 9:16-Szene (Inhalt y 300–1280) mittig ins 16:9-Bild legen, unter die Kopfzeile, über die Untertitel
    lf_kit.rahmen = lambda html, quer: (f'<div class="qbox" style="position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;'
                                        f'transform:translate(558px,-74px) scale(0.745)">{html}</div>') if quer else html

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
GRAU = "#9aa3ae"
K = Kit(HERE, 22, ["frei-gold", "frankfurt-skyline"], quer=QUER)
cap, st = K.cap, K.st
S = K.szene


def titel(id_, text, y=340, farbe=D, gr=70):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=54):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def rechnung(id_, zeile, ergebnis, y, farbe, titel_=""):
    kt = f'<div class="nk-kt">{titel_}</div>' if titel_ else ""
    return (f'<div id="{id_}" class="nk-karte" style="left:110px;top:{y}px;width:860px;text-align:center">{kt}'
            f'<div style="font-size:50px;color:#3a414c;font-weight:600">{zeile}</div>'
            f'<div id="{id_}-e" style="margin-top:12px;font-weight:900;font-size:116px;color:{farbe}">{ergebnis}</div></div>')


def balken_h(id_, y, label, jahre, max_j, farbe, text):
    """Waagerechter Balken fürs Spar-Wettrennen."""
    w = int(620 * jahre / max_j)
    return (f'<div id="{id_}" style="position:absolute;left:110px;top:{y}px;width:860px;z-index:4">'
            f'<div style="font-weight:800;font-size:40px;color:{D};margin-bottom:10px">{label}</div>'
            f'<div style="display:flex;align-items:center;gap:20px"><div id="{id_}-b" style="width:{w}px;height:70px;border-radius:12px;background:{farbe};'
            f'transform-origin:0 50%;box-shadow:0 8px 18px #0002"></div><div style="font-weight:900;font-size:52px;color:{farbe};white-space:nowrap">{text}</div></div></div>')


def turm(id_, x, y, h, w=260, farbe=G, unten="", oben=""):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y - h}px;width:{w}px;height:{h}px;border-radius:14px 14px 4px 4px;'
            f'background:repeating-linear-gradient(180deg,{farbe} 0 34px,{farbe}cc 34px 40px);box-shadow:0 12px 24px #0002;transform-origin:50% 100%;z-index:3"></div>'
            f'<div id="{id_}-o" style="position:absolute;left:{x - 60}px;width:{w + 120}px;top:{y - h - 70}px;text-align:center;font-weight:900;font-size:50px;color:{farbe};z-index:5">{oben}</div>'
            f'<div style="position:absolute;left:{x - 60}px;width:{w + 120}px;top:{y + 14}px;text-align:center;font-weight:700;font-size:34px;color:#3a414c;z-index:5">{unten}</div>')


def wachs(sel, t, dauer=0.8):
    return f' tl.fromTo("{sel}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: {dauer}, ease: "power3.out" }}, {t});'


def breit(sel, t, dauer=0.8):
    return f' tl.fromTo("{sel}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {dauer}, ease: "power3.out" }}, {t});'


# s1–s2 Hook
S("s1", None, nl.CSS + nl.foto("f1", "frei-gold") + titel("t1", "Wie viel Geld brauchst du,<br/>um nie wieder<br/>arbeiten zu müssen?", 340, D, 64)
  + turm("tm1", 410, 1180, 520, 260, O, "", "???") + pille("p2", "live gerechnet", 1210, D, "#fff", 46),
  lambda a, d: KIT_JS + f' pop("#t1", {a});' + wachs("#tm1", a + 0.2, 1.2) + f' pop("#tm1-o", {a} + 1.2); pop("#p2", {cap("s2", 2)});',
  [], bis="s3")

# s3 Open Loop: der Trick
S("s3", None, titel("t3", "Am Ende: der Trick", 360, O)
  + nl.karte("k3", "Dein Ziel erreichen", f'<div style="font-weight:900;font-size:110px;color:{G};text-align:center;line-height:1.1">10 Jahre<br/><span style="font-size:70px">früher</span></div>', y=560),
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {cap("s3", 2)});')

# s4–s5 Ziel
S("s4", None, titel("t4", "Dein Ziel", 340) + nl.karte("k4", "Zum Leben", nl.zeile("r4", "Pro Monat", "2.000 €", O) + nl.zeile("r5", "Pro Jahr", "24.000 €", O), y=520),
  lambda a, d: f'pop("#t4", {a}); pop("#k4", {a} + 0.1); pop("#r4", {cap("s4", 2)}); pop("#r5", {cap("s5", 0)} + 0.3);', [], bis="s6")

# s6–s7 4-%-Regel (Kreis mit 4-%-Stück)
KREIS = (f'<svg id="kr6" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:3">'
         f'<circle cx="540" cy="860" r="260" fill="{G}"/><path id="kr6-s" d="M540 860 L540 600 A260 260 0 0 1 603 608 Z" fill="{O}" transform="rotate(0 540 860)"/></svg>'
         f'<div id="kl6a" style="position:absolute;left:0;width:1080px;top:1150px;text-align:center;font-weight:900;font-size:50px;color:{O};z-index:5">4 % entnehmen</div>'
         f'<div id="kl6b" style="position:absolute;left:0;width:1080px;top:1220px;text-align:center;font-weight:900;font-size:50px;color:{G};z-index:5">96 % arbeiten weiter</div>')
S("s6", None, titel("t6", "Die 4-%-Regel", 330, O) + KREIS,
  lambda a, d: (f'pop("#t6", {a}); pop("#kr6", {cap("s6", 1)}); tl.fromTo("#kr6-s", {{ scale: 1 }}, {{ scale: 1.12, transformOrigin: "540px 860px", duration: 0.4, yoyo: true, repeat: 1 }}, {cap("s7", 1)});'
                f' pop("#kl6a", {cap("s7", 1)}); pop("#kl6b", {cap("s7", 2)});'), [], bis="s8")

# s8 Studie
S("s8", None, titel("t8", "Getestet", 340) + nl.karte("k8", "US-Studie (Trinity-Studie, 1998)",
  nl.zeile("r8a", "4 % pro Jahr entnehmen", "✓", G) + nl.zeile("r8b", "Geld reichte fast immer", "≥ 30 Jahre", G, "✓"), y=520),
  lambda a, d: f'pop("#t8", {a}); pop("#k8", {a} + 0.1); pop("#r8a", {cap("s8", 1)}); pop("#r8b", {cap("s8", 3)});')

# s9–s10 600.000 €
S("s9", None, titel("t9", "Dein Zielbetrag", 340) + rechnung("r9", "24.000 € ÷ 4 %", "600.000 €", 520, G)
  + pille("p10", "Klingt viel?", 1000, O, "#fff", 60),
  lambda a, d: f'pop("#t9", {a}); pop("#r9", {cap("s9", 0)}); pop("#r9-e", {cap("s9", 1)}); pop("#p10", {cap("s10", 0)});', [], bis="s11")

# s11–s13 Spar-Wettrennen
REN = (balken_h("b11", 560, "200 € im Monat", 42, 42, R, "≈ 42 Jahre") + balken_h("b12", 760, "500 € im Monat", 30, 42, O, "≈ 30 Jahre")
       + balken_h("b13", 960, "1.000 € im Monat", 22, 42, G, "≈ 22 Jahre"))
S("s11", None, titel("t11", "Bis 600.000 € – bei 7 % Rendite", 360, D, 52) + REN,
  lambda a, d: (f'pop("#t11", {a});' + f' pop("#b11", {cap("s11", 0)});' + breit("#b11-b", cap("s11", 2)) + f' pop("#b12", {cap("s12", 0)});' + breit("#b12-b", cap("s12", 1))
                + f' pop("#b13", {cap("s13", 0)});' + breit("#b13-b", cap("s13", 2))), [], bis="s14")

# s14 Kommentar-CTA
S("s14", None, titel("t14", "Deine Meinung", 360)
  + nl.karte("k14", "Schreib’s in die Kommentare", f'<div style="font-weight:900;font-size:62px;color:{O};text-align:center;padding:20px 0">Wie viel müsstest<br/>du sparen?</div>', y=560),
  lambda a, d: f'pop("#t14", {a}); pop("#k14", {cap("s14", 1)});')

# s15–s16 Eingezahlt vs. Zinsen
S("s15", None, titel("t15", "Der Aha-Moment", 330, O) + turm("tm15a", 230, 1150, 190, 240, GRAU, "selbst eingezahlt", "180.000 €")
  + turm("tm15b", 610, 1150, 640, 240, G, "Zinsen auf Zinsen", "430.000 €"),
  lambda a, d: f'pop("#t15", {a});' + wachs("#tm15a", cap("s15", 3)) + f' pop("#tm15a-o", {cap("s15", 3)} + 0.6);' + wachs("#tm15b", cap("s16", 0), 1.2) + f' pop("#tm15b-o", {cap("s16", 0)} + 1.1);',
  [], bis="s17")

# s17 Startzeitpunkt
S("s17", None, titel("t17", "Der größte Trick: früh starten", 330, D, 54) + turm("tm17a", 230, 1150, 660, 240, G, "jetzt starten (30 J.)", "≈ 610.000 €")
  + turm("tm17b", 610, 1150, 280, 240, R, "später (20 J.)", "≈ 260.000 €"),
  lambda a, d: f'pop("#t17", {a});' + wachs("#tm17a", cap("s17", 1)) + f' pop("#tm17a-o", {cap("s17", 1)} + 0.7);' + wachs("#tm17b", cap("s17", 4)) + f' pop("#tm17b-o", {cap("s17", 4)} + 0.7);')

# s18–s19 Inflation
INF = (nl.zeile("r18", "Steuern", "▲ Ziel größer", R) + nl.zeile("r19a", "2.000 € heute", "2.000 €", D)
       + nl.zeile("r19b", "in 30 Jahren wert", "≈ 1.100 € ▼", R))
S("s18", None, titel("t18", "Aber Achtung", 340, R) + nl.karte("k18", "Steuern & Inflation (2 %)", INF, y=520),
  lambda a, d: f'pop("#t18", {a}); pop("#k18", {a} + 0.1); pop("#r18", {cap("s18", 1)}); pop("#r19a", {cap("s19", 1)}); pop("#r19b", {cap("s19", 2)});', [], bis="s20")

# s20 Teilziel
S("s20", None, nl.foto("f20", "frankfurt-skyline") + titel("t20", "Unser Tipp: Teilziel", 340, G) + rechnung("r20", "300.000 € × 4 %", "+1.000 €", 520, G, "Pro Monat extra"),
  lambda a, d: f'pop("#t20", {a}); pop("#r20", {cap("s20", 1)}); pop("#r20-e", {cap("s20", 3)});')

# s21 Hinweis
S("s21", None, nl.karte("k21", "Kurzer Hinweis", f'<div style="font-size:52px;font-weight:800;color:{D};text-align:center;padding:30px 0">Keine Anlageberatung –<br/>nur gerechnet.</div>', y=620),
  lambda a, d: f'pop("#k21", {a});')

# s22 Folgen
S("s22", None, f'<div id="fl22" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n22" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c22", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl22", {a}); pop("#n22", {a} + 0.2); pop("#c22", {cap("s22", 0)} + 0.4);')

html, code = ls.szene(querformat=QUER, hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf_quer("GELD-WISSEN", "") if QUER else nl.kopf("GELD-WISSEN", ""), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
