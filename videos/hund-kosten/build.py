#!/usr/bin/env python3
"""HundeFinanzTv Short (~66 s, Stimme Dan) – Was kostet ein Hund im Leben? NEUES FORMAT (heller News-Look).
Mittelgroßer Hund, 13 Jahre: Anschaffung 1.000 €, Futter 50 €/Monat = 7.800 €, Tierarzt 300 €/Jahr = 3.900 €, Steuer+Haftpflicht 180 €/Jahr = 2.340 €,
Zubehör/Pflege 2.000 € → ≈ 17.000 € ≈ 110 €/Monat; Kreuzband-OP ≈ 2.500 €. Quellen: rechnercheck.de, Allianz, Sparkasse."""
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
K = Kit(HERE, 14, [], fotos=["beagle-foto.jpg"])
cap, st = K.cap, K.st
S = K.szene


def titel(id_, text, y=340, farbe=D, gr=70):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=54):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def foto_karte(id_, x, y, w, h, dreh=-3):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:18px;overflow:hidden;border:8px solid #fff;'
            f'box-shadow:0 18px 36px #0003;transform:rotate({dreh}deg);z-index:4"><img src="assets/fotos/beagle-foto.jpg" style="width:100%;height:100%;object-fit:cover"/></div>')


def wert_karte(id_, kopf, wert, x, y, w, farbe):
    return (f'<div id="{id_}" class="nk-karte" style="left:{x}px;top:{y}px;width:{w}px;text-align:center">'
            f'<div style="font-weight:700;font-size:38px;color:#3a414c">{kopf}</div>'
            f'<div style="font-weight:900;font-size:62px;color:{farbe};margin-top:8px;white-space:nowrap">{wert}</div></div>')


# s1–s2 Hook
S("s1", None, nl.CSS + titel("t1", "Hund = Kleinwagen?", 330, D, 78) + foto_karte("f1", 300, 470, 480, 384)
  + wert_karte("w1a", "Hund (13 Jahre)", "≈ 17.000 €", 70, 900, 440, O) + wert_karte("w1b", "Kleinwagen", "≈ 17.000 €", 570, 900, 440, D)
  + pille("p2", "Posten für Posten", 1170, D, "#fff", 46),
  lambda a, d: (KIT_JS + f' pop("#t1", {a}); pop("#f1", {a}); pop("#w1a", {cap("s1", 0)} + 0.6); pop("#w1b", {cap("s1", 1)});'
                f' pop("#p2", {cap("s2", 2)});'), [], bis="s3")

# s3 Open Loop
S("s3", None, titel("t3", "Am Ende: der Posten,<br/>den keiner einplant", 360, R, 62)
  + nl.karte("k3", "Kommt oft plötzlich", f'<div style="font-weight:900;font-size:180px;color:{R};text-align:center;line-height:1.1">?</div>', y=620),
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {cap("s3", 2)});')

# s4–s10 Die Rechnung (Leitmotiv: wachsende Rechnung)
ZEILEN = [("r5", "Anschaffung", "1.000 €"), ("r6", "Futter (50 €/Monat)", "7.800 €"), ("r7", "Tierarzt (300 €/Jahr)", "3.900 €"),
          ("r8", "Steuer + Haftpflicht", "2.340 €"), ("r9", "Zubehör & Pflege", "2.000 €")]
RECH = "".join(nl.zeile(i, l, w, D) for i, l, w in ZEILEN) + (
    f'<div id="r10" class="nk-row" style="border-top:3px solid {D};margin-top:10px;font-weight:800;color:{D}">Summe'
    f'<span class="v" style="color:{O};font-size:56px">≈ 17.000 €</span></div>')
S("s4", None, titel("t4", "Mittelgroßer Hund · 13 Jahre", 330, D, 52) + nl.karte("k4", "Die Rechnung", RECH, y=430)
  + pille("p10", "≈ 110 € im Monat", 1215, O, "#fff", 54),
  lambda a, d: (f'pop("#t4", {a}); pop("#k4", {cap("s5", 0)} - 0.2); pop("#r5", {cap("s5", 1)}); pop("#r6", {cap("s6", 1)}); pop("#r7", {cap("s7", 3)});'
                f' pop("#r8", {cap("s8", 2)}); pop("#r9", {cap("s9", 2)}); pop("#r10", {cap("s10", 1)}); pop("#p10", {cap("s10", 1)} + 0.8);'),
  [], bis="s11")

# s11 OP
S("s11", None, titel("t11", "Der Posten, der überrascht", 340, R, 60) + foto_karte("f11", 330, 470, 420, 336, 3)
  + wert_karte("w11", "Kreuzband-OP – auf einmal", "≈ 2.500 €", 160, 880, 760, R),
  lambda a, d: f'pop("#t11", {a}); pop("#f11", {cap("s11", 2)}); pop("#w11", {cap("s11", 4)});')

# s12 Tipp
S("s12", None, titel("t12", "Unser Tipp", 340, G) + nl.karte("k12", "So bist du vorbereitet",
  nl.zeile("r12a", "Jeden Monat Tierarzt-Topf", "✓", G) + nl.zeile("r12b", "OP-Versicherung prüfen", "✓", G), y=520),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 1)}); pop("#r12b", {cap("s12", 3)});')

# s13 Kommentar
S("s13", None, titel("t13", "Deine Meinung", 360) + nl.karte("k13", "Schreib’s in die Kommentare",
  f'<div style="font-weight:900;font-size:62px;color:{O};text-align:center;padding:20px 0">Was kostet dein<br/>Hund im Monat?</div>', y=560),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.2);')

# s14 Folgen
S("s14", None, f'<div id="fl14" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n14" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c14", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl14", {a}); pop("#n14", {a} + 0.2); pop("#c14", {cap("s14", 0)} + 0.4);')

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("GELD-WISSEN", ""), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
