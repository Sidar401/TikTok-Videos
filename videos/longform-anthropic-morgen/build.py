#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (18.11.): Anthropic geht morgen an die Börse – was du wissen musst.
Neuer Blickwinkel (vs. longform-anthropic-ipo / anthropic-boersengang): Ablauf des Tages, Ausgabepreis-Falle, Arm/Alibaba/Uber,
Sperrfrist, Nasdaq-100-Schnellregel (ETF-Depot). Erstes Video mit Logo-Intro (nach s6) und professionellem Einstieg.
Leitmotiv: Countdown-Uhr „15:30“ + Original-Logos groß im Hintergrund."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 26)  # Logo-Intro nach dem Einstieg (Pause in Stimme + Zeiten)

from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, foto_gross, hand, icon_gross, kalender, kasten,  # noqa: E402
                         kreis, laufband_szene, linie, news_kopf, pfeil, spanne, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, logo, tz  # noqa: E402

AN, NQ = "#d97757", "#0996c7"
K = Kit(HERE, 33, ["nyse", "frei-laptop", "frei-smartphone", "chips", "sitzungssaal", "frankfurt-skyline"],
        logos=["anthropic.svg", "claude.svg", "nasdaq.svg", "arm.svg", "alibaba.svg", "uber.svg"], fotos=["dario-amodei.jpg"])
cap, st = K.cap, K.st
S = K.szene


def wz(id_, datei, y=560, w=900, op=0.13):
    """Original-Logo groß und blass im Hintergrund (Nutzer 18.11., wie Eulen-Kanal)."""
    return (f'<img id="{id_}" src="assets/logos/{datei}" alt="" style="position:absolute;left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;'
            f'filter:brightness(0) invert(1);opacity:{op};z-index:1"/>')


def uhr(id_, text, y=640, farbe=OR, gr=170):
    return (f'<div id="{id_}" class="mono" style="position:absolute;left:190px;top:{y}px;width:700px;padding:18px 0;border-radius:28px;background:#000c;border:6px solid {farbe};'
            f'box-shadow:0 0 60px {farbe}88;text-align:center;font-size:{gr}px;color:{farbe};text-shadow:0 0 30px {farbe};z-index:4">{text}</div>')


# ---------- Einstieg (vor dem Logo-Intro) ----------
S("s1", "nyse", KIT_CSS + wz("w1", "anthropic.svg", 1000, 950, 0.10) + titel_zeile("t1", "⚡ Morgen, 15:30 Uhr", farbe=GELB) + uhr("u1", "15:30") + logo("l1", "nasdaq.svg", 900, 420, glow=NQ)
  + chip("c1", "größter KI-Börsengang aller Zeiten", OR, 1080, 48),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#u1", {a}); pop("#l1", {cap("s1", 1)}); slam("#c1", {cap("s1", 2)});', [(0.0, "mm-bumm")])

S("s2", "frei-laptop", titel_zeile("t2", "Wer geht an die Börse?") + logo("l2", "anthropic.svg", 600, 700, glow=AN, pad=34) + logo("l2b", "claude.svg", 800, 300, glow=AN, pad=22)
  + chip("c2", "Preis: schon heute Nacht", GELB, 1060, 54),
  lambda a, d: f'pop("#t2", {a}); pop("#l2", {cap("s2", 0)}); pop("#l2b", {cap("s2", 1)}); slam("#c2", {cap("s2", 2)});', [])

S("s3", "frei-smartphone", titel_zeile("t3", "Betrifft auch dich") + icon_gross("i3", "🧺", 0, 600, 280, OR, True) + hand("h3", "dein ETF-Depot?", 540, 940, 84, GELB, -4, True),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {cap("s3", 1)}); pop("#h3", {cap("s3", 2)});', [])

S("s4", "chips", wz("w4", "nasdaq.svg", 700, 900, 0.10) + titel_zeile("t4", "Den übersehen fast alle", farbe=GELB) + tz("n4", "?", 580, 340, "glow-o")
  + kreis("k4", 540, 760, 230, 230, GELB) + chip("c4", "kommt gleich", GELB, 1060, 56),
  lambda a, d: f'pop("#t4", {a}); slam("#n4", {cap("s4", 0)}); draw("#k4-p", {cap("s4", 1)}, 0.6); pop("#c4", {cap("s4", 2)});', [])

S("s5", "sitzungssaal", titel_zeile("t5", "Schreib's in die Kommentare") + vergleich("v5", "KAUFEN", "🚀 sofort dabei", "ABWARTEN", "⏳ erst mal schauen", GRUEN, GELB, y=640, h=330),
  lambda a, d: f'pop("#t5", {a}); pop("#v5-l", {cap("s5", 0)} + 0.3); pop("#v5-r", {cap("s5", 1)});', [(st("s5"), "mm-wusch")])

S("s6", "frankfurt-skyline", titel_zeile("t6", "Schritt für Schritt") + kasten("k6a", "Preis", 60, 680, 290, 220, GELB, 56, "heute Nacht")
  + kasten("k6b", "Start", 395, 680, 290, 220, OR, 56, "morgen") + kasten("k6c", "ETF", 730, 680, 290, 220, GRUEN, 56, "Dezember?"),
  lambda a, d: f'pop("#t6", {a}); pop("#k6a", {a} + 0.2); pop("#k6b", {a} + 0.45); pop("#k6c", {a} + 0.7);', [], bis="s7")

# ---------- Teil 1: der Ablauf ----------
S("s7", "nyse", titel_zeile("t7", "Heute Abend") + kalender("k7", "NOV", 18, 110, 620, 300, ROT, "Mittwoch") + icon_gross("i7", "🏦", 520, 640, 230, OR)
  + chip("c7", "Ausgabepreis wird festgelegt", OR, 1060, 50),
  lambda a, d: f'pop("#t7", {a}); pop("#k7", {a}); pop("#i7", {cap("s7", 1)}); slam("#c7", {cap("s7", 2)});', [])

S("s8", "frei-laptop", wz("w8", "anthropic.svg", 560, 900, 0.09) + titel_zeile("t8", "Geplanter Preis") + spanne("sp8", 140, 800, 800, 0.2, 0.8, "70 $", "78 $", GRUEN)
  + hand("h8", "pro Aktie", 540, 960, 70, GELB, -3, True),
  lambda a, d: f'pop("#t8", {a}); spann("#sp8", {cap("s8", 0)}); pop("#h8", {cap("s8", 1)});', [(cap("s8", 0), "mm-tippen")])

S("s9", "chips", titel_zeile("t9", "Riesige Nachfrage", farbe=GRUEN) + balken2("b9", "1×", "6–7×", 1, 6.5, GRAU, GRUEN, unten=("Aktien da", "Aktien gewünscht")),
  lambda a, d: f'pop("#t9", {a});' + balken2_js("b9", cap("s9", 1), cap("s9", 3)), [])

S("s10", "frei-smartphone", titel_zeile("t10", "Preis höher?", farbe=GELB) + spanne("sp10", 140, 800, 800, 0.2, 0.8, "70 $", "78 $", GRAU)
  + pfeil("p10", 780, 760, 960, 600, 0.3, GELB) + hand("h10", "über 78 $?", 760, 520, 80, GELB, -6),
  lambda a, d: f'pop("#t10", {a}); spann("#sp10", {a}); draw("#p10-p", {cap("s10", 1)}, 0.5); pop("#p10-k", {cap("s10", 1)} + 0.45); pop("#h10", {cap("s10", 1)} + 0.3);', [])

S("s11", "frankfurt-skyline", titel_zeile("t11", "Achtung", farbe=ROT) + uhr("u11", "15:30", 600, GRAU, 130) + pfeil("p11", 540, 800, 540, 940, 0.0, GELB)
  + kasten("k11", "erster Kurs: Stunden später", 140, 960, 800, 150, ROT, 50, "bei uns eher am Abend"),
  lambda a, d: f'pop("#t11", {a}); pop("#u11", {a}); draw("#p11-p", {cap("s11", 2)}, 0.4); pop("#p11-k", {cap("s11", 2)} + 0.35); pop("#k11", {cap("s11", 2)} + 0.3);', [])

S("s12", "sitzungssaal", titel_zeile("t12", "Die erste Falle", farbe=ROT) + icon_gross("i12", "🪤", 0, 600, 280, ROT, True) + stempel("s12x", "FALLE", 330, 960, ROT, 96, -8),
  lambda a, d: f'pop("#t12", {a}); pop("#i12", {a} + 0.1); stempeln("#s12x", {cap("s12", 1)});', [(cap("s12", 1), "stempel")])

S("s13", "nyse", titel_zeile("t13", "Was du zahlst") + vergleich("v13", "AUSGABEPREIS", "nur beim Zeichnen", "BÖRSENKURS", "das zahlst du", GRAU, OR, y=640, h=330),
  lambda a, d: f'pop("#t13", {a}); pop("#v13-l", {cap("s13", 1)}); pop("#v13-r", {cap("s13", 2)});', [])

L14 = linie("ku14", [0.3, 0.35, 0.6, 0.5, 0.8, 0.7, 0.92], 160, 640, 760, 400, OR, punkte=[(0, "Ausgabepreis"), (6, "Börsenkurs?")])
S("s14", "frei-laptop", titel_zeile("t14", "Am ersten Tag") + L14,
  lambda a, d: f'pop("#t14", {a}); pop("#ku14-w0", {a} + 0.1); draw("#ku14-p", {a} + 0.2, 1.2); tl.fromTo("#ku14-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 0.8); pop("#ku14-w1", {cap("s14", 1)});', [])

S("s15", "frankfurt-skyline", titel_zeile("t15", "Folg uns") + folg_logo("fl15", 600, 360) + chip("c15", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t15", {a}); {folg_js("fl15", a)} slam("#c15", {cap("s15", 0)} + 0.4);', [(st("s15"), "mm-wusch")])

# ---------- Teil 2: Blick zurück ----------
S("s16", "chips", titel_zeile("t16", "Blick zurück") + logo("l16a", "arm.svg", 640, 280, x=60, glow="#0091bd", pad=30) + logo("l16b", "alibaba.svg", 640, 280, x=400, glow="#ff6a00", pad=30)
  + logo("l16c", "uber.svg", 640, 280, x=740, glow="#fff", pad=30) + chip("c16", "der erste Handelstag", OR, 960, 56),
  lambda a, d: f'pop("#t16", {a}); pop("#l16a", {a} + 0.15); pop("#l16b", {a} + 0.35); pop("#l16c", {a} + 0.55); pop("#c16", {cap("s16", 1)});', [])


def tag1(sid, datei, glow, jahr, zahl, cls, hg, sfx=()):
    S(sid, hg, titel_zeile(f"t{sid}", f"Börsengang {jahr}") + logo(f"l{sid}", datei, 600, 560, glow=glow, pad=40) + tz(f"n{sid}", zahl, 880, 190, cls)
      + hand(f"h{sid}", "am 1. Tag", 540, 1090, 66, GELB, -3, True),
      lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#l{s}", {a} + 0.1); slam("#n{s}", {cap(s, 2)}); pop("#h{s}", {cap(s, 2)} + 0.3);', sfx)


tag1("s17", "arm.svg", "#0091bd", 2023, "+25 %", "glow-g", "frei-laptop")
tag1("s18", "alibaba.svg", "#ff6a00", 2014, "+38 %", "glow-g", "nyse")
tag1("s19", "uber.svg", "#ffffff", 2019, "−8 %", "glow-r", "frei-smartphone", [(cap("s19", 2), "mm-bumm")])

S("s20", "sitzungssaal", titel_zeile("t20", "Merk dir") + stempel("s20x", "KEINE GARANTIE", 170, 760, GELB, 84, -6),
  lambda a, d: f'pop("#t20", {a}); stempeln("#s20x", {cap("s20", 1)});', [])

# ---------- Teil 3: Sperrfrist ----------
S("s21", "frankfurt-skyline", titel_zeile("t21", "Kaum bekannt", farbe=GELB) + zettel("z21", "Was viele<br/>nicht wissen …", 270, 640, 540, 76, GELB, -4),
  lambda a, d: f'pop("#t21", {a}); tl.fromTo("#z21", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -4, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});', [])

S("s22", "chips", titel_zeile("t22", "Die Sperrfrist") + icon_gross("i22", "🔒", 0, 600, 280, OR, True) + chip("c22", "Mitarbeiter dürfen erst später verkaufen", OR, 980, 44),
  lambda a, d: f'pop("#t22", {a}); pop("#i22", {cap("s22", 1)}); pop("#c22", {cap("s22", 2)});', [])

S("s23", "nyse", wz("w23", "anthropic.svg", 1000, 900, 0.09) + titel_zeile("t23", "Bei Anthropic") + kalender("k23a", "TAG", 1, 120, 600, 300, ROT, "bis 10 % verkaufen")
  + kalender("k23b", "TAG", 27, 660, 600, 300, ROT, "weitere frei") + pfeil("p23", 440, 760, 640, 760, -0.2, GELB),
  lambda a, d: f'pop("#t23", {a}); pop("#k23a", {cap("s23", 1)}); draw("#p23-p", {cap("s23", 3)} - 0.3, 0.4); pop("#p23-k", {cap("s23", 3)}); pop("#k23b", {cap("s23", 3)});', [])

L24 = linie("ku24", [0.85, 0.8, 0.6, 0.65, 0.45, 0.5, 0.3], 160, 640, 760, 400, ROT, punkte=[(6, "Druck")])
S("s24", "frei-laptop", titel_zeile("t24", "In den ersten Wochen") + L24,
  lambda a, d: f'pop("#t24", {a}); draw("#ku24-p", {a} + 0.2, 1.2); tl.fromTo("#ku24-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 0.8); pop("#ku24-w0", {cap("s24", 2)});', [])

# ---------- Teil 4: der übersehene Punkt ----------
S("s25", "frankfurt-skyline", titel_zeile("t25", "Jetzt kommt's", farbe=GELB) + logo("l25", "nasdaq.svg", 680, 620, glow=NQ, pad=30) + kreis("k25", 540, 780, 380, 180, GELB),
  lambda a, d: f'pop("#t25", {a}); slam("#l25", {a} + 0.15); draw("#k25-p", {cap("s25", 1)}, 0.6);', [(st("s25"), "mm-bumm")])

S("s26", "sitzungssaal", titel_zeile("t26", "Neue Schnellregel") + kalender("k26", "SEIT", "MAI", 150, 620, 300, NQ, "2026") + icon_gross("i26", "⚡", 560, 640, 260, GELB),
  lambda a, d: f'pop("#t26", {a}); pop("#k26", {cap("s26", 0)}); slam("#i26", {cap("s26", 1)});', [])

S("s27", "nyse", titel_zeile("t27", "Ab in den Nasdaq 100") + logo("l27a", "anthropic.svg", 620, 380, x=60, glow=AN, pad=24)
  + pfeil("p27", 460, 700, 620, 700, -0.25, GELB) + kasten("k27", "Nasdaq 100", 640, 620, 380, 170, NQ, 54, "nach wenigen Wochen")
  + hand("h27", "voraussichtlich Dezember", 540, 920, 70, GELB, -3, True),
  lambda a, d: f'pop("#t27", {a}); pop("#l27a", {a} + 0.1); draw("#p27-p", {cap("s27", 1)}, 0.4); pop("#p27-k", {cap("s27", 1)} + 0.35); pop("#k27", {cap("s27", 1)} + 0.3); pop("#h27", {cap("s27", 3)});', [])

S("s28", "frei-smartphone", titel_zeile("t28", "Dein Nasdaq-100-ETF") + icon_gross("i28", "🧺", 0, 600, 300, OR, True) + logo("l28", "claude.svg", 760, 220, glow=AN, pad=18)
  + stempel("s28x", "AUTOMATISCH", 230, 1000, GRUEN, 70, -5),
  lambda a, d: f'pop("#t28", {a}); pop("#i28", {a} + 0.1); slam("#l28", {cap("s28", 1)}); stempeln("#s28x", {cap("s28", 2)});', [(cap("s28", 2), "stempel")])

S("s29", "chips", titel_zeile("t29", "Fonds müssen kaufen") + icon_gross("i29", "🛒", 0, 600, 260, OR, True) + pfeil("p29", 700, 900, 860, 680, 0.3, GRUEN)
  + chip("c29", "kann den Kurs bewegen", OR, 1000, 54),
  lambda a, d: f'pop("#t29", {a}); pop("#i29", {cap("s29", 1)}); draw("#p29-p", {cap("s29", 2)}, 0.5); pop("#p29-k", {cap("s29", 2)} + 0.45); pop("#c29", {cap("s29", 2)} + 0.2);', [])

# ---------- Teil 5: was tun ----------
S("s30", "frankfurt-skyline", titel_zeile("t30", "Und du?", farbe=GELB) + icon_gross("i30", "🫵", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t30", {a}); slam("#i30", {a} + 0.15);', [])

S("s31", "frei-laptop", titel_zeile("t31", "Wenn du kaufst", farbe=GRUEN) + kasten("k31a", "Betrag festlegen", 90, 640, 420, 230, GRUEN, 52, "vorher")
  + kasten("k31b", "Limit setzen", 570, 640, 420, 230, GRUEN, 52, "nicht teurer kaufen") + foto_gross("f31", "assets/fotos/dario-amodei.jpg", 390, 920, 300, 240, farbe=AN),
  lambda a, d: f'pop("#t31", {a}); pop("#k31a", {cap("s31", 1)}); pop("#k31b", {cap("s31", 2)}); pop("#f31", {a} + 0.3);', [])

S("s32", "nyse", titel_zeile("t32", "Wenn du unsicher bist") + icon_gross("i32", "🧘", 0, 600, 260, GRUEN, True) + chip("c32", "abwarten – über ETFs kommst du später ran", GRUEN, 960, 42),
  lambda a, d: f'pop("#t32", {a}); pop("#i32", {a} + 0.1); pop("#c32", {cap("s32", 2)});', [])

S("s33", "sitzungssaal", titel_zeile("t33", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t33", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});', [])

# Logo-Intro, Nachrichten-Kopf, Laufband
html, code = ls.szene()
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX += ls.sounds(T0)
K.SZ.append((0.0, K.dauer, news_kopf("18.11.2026"), lambda a, d: "", 8))
K.SZ.append(laufband_szene([("ANTHROPIC-IPO MORGEN", GELB), ("ANT · 70–78 $", GELB), ("NASDAQ START 15:30 UHR", None),
                            ("NVDA UMSATZ ▲ +103 %", GRUEN), ("DAX GESTERN ▼ −2,1 %", ROT)], K.dauer))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
