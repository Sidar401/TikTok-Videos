#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News v2, 2:43): Musk plant den größten Deal der Geschichte – Tesla + SpaceX.
Keine Kapitel, Hinweis am Ende, freie Hintergründe, Original-Logos (gemeinfrei), Musk-Foto gemeinfrei (US-Verteidigungsministerium)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, donut, flagge, foto_gross, icon_gross, kalender, kasten,  # noqa: E402
                         kit_assets, news_kopf, quelle, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip, partikel  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, logo, tz  # noqa: E402

TS = "#e82127"
SX = "#2b6cb0"
kit_assets(HERE, ["flagge-china", "flagge-usa", "flagge-deutschland"])
K = Kit(HERE, 38, ["frei-miami-nacht", "frei-miami-omni", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "wallstreet", "handelssaal", "frei-sitzung", "frei-euro", "frei-code-monitor"],
        logos=["tesla-symbol.png", "tesla-schrift.png", "spacex.png", "starlink.png", "vodafone.png", "barclays-voll.png"], fotos=["elon-musk.jpg"])
cap, st = K.cap, K.st
S = K.szene
MUSK = "assets/fotos/elon-musk.jpg"


def tesla(id_, y, w=300, x=None):
    return logo(id_, "tesla-symbol.png", y, w, x, glow=TS, pad=26)


def spacex(id_, y, w=440, x=None):
    return logo(id_, "spacex.png", y, w, x, glow=SX, pad=20)


S("s1", "frei-miami-nacht", KIT_CSS + titel_zeile("t1", "⚡ Musks Mega-Plan", farbe=ROT) + foto_gross("f1", MUSK, 310, 600, 460, 470, "", OR)
  + stempel("s1x", "GRÖSSTER DEAL DER GESCHICHTE", 120, 1110, ROT, 38, -4),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#f1", {a}); flash({a} + 0.1, 0.4); stempeln("#s1x", {cap("s1", 1)});',
  [(0.0, "eilmeldung"), (0.05, "kamera-blitz"), (cap("s1", 1), "stempel")])

S("s2", "frei-miami-omni", titel_zeile("t2", "Tesla + SpaceX") + tesla("l2a", 600, 220, 90) + tz("pl2", "+", 640, 120).replace("z-index:5;top", "z-index:5;left:-120px;top") + spacex("l2b", 640, 400, 560)
  + tz("n2", "≈ 3,5 Bio. $", 900, 130, "glow-o"),
  lambda a, d: f'pop("#t2", {a}); pop("#l2a", {cap("s2", 0)}); pop("#pl2", {cap("s2", 0)} + 0.3); pop("#l2b", {cap("s2", 0)} + 0.6); slam("#n2", {cap("s2", 4)});',
  [(st("s2"), "whoosh-weich"), (cap("s2", 4), "kasse")])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Deine Meinung") + icon_gross("i3", "💬", 0, 600, 240, OR, True)
  + chip("c3a", "📈 ich wäre dabei", GRUEN, 900, 54) + chip("c3b", "🙅 niemals", ROT, 1020, 54),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.1); pop("#c3a", {cap("s3", 1)}); pop("#c3b", {cap("s3", 2)});',
  [(st("s3"), "handy-benachrichtigung"), (cap("s3", 1), "pop")])

S("s4", "frei-frankfurt-staedel", titel_zeile("t4", "Folg uns") + icon_gross("i4", "🔔", 0, 620, 260, OR, True) + chip("c4", "+ Folgen", OR, 940, 70),
  lambda a, d: f'pop("#t4", {a}); pop("#i4", {a}); tl.fromTo("#i4", {{ rotation: -18 }}, {{ rotation: 18, duration: 0.14, yoyo: true, repeat: 5 }}, {a} + 0.3); slam("#c4", {cap("s4", 0)} + 0.4);',
  [(st("s4"), "swipe"), (st("s4") + 0.3, "handy-benachrichtigung")])

S("s5", "wallstreet", titel_zeile("t5", "Laut Bloomberg") + icon_gross("i5", "📰", 0, 620, 240, OR, True) + chip("c5", "Gespräche kommen gut voran", GRUEN, 940, 56)
  + quelle("q5", "Bericht vom 12.11.2026", 1060),
  lambda a, d: f'pop("#t5", {a}); pop("#i5", {a} + 0.1); slam("#c5", {cap("s5", 2)}); pop("#q5", {cap("s5", 2)} + 0.3);',
  [(st("s5"), "zeitung")])

S("s6", "frei-sitzung", titel_zeile("t6", "Wann?") + kalender("k6a", "DEZ", "2026", 110, 640, 300, OR) + tz("o6", "oder", 760, 60) + kalender("k6b", "ANFANG", "2027", 670, 640, 300, GRAU),
  lambda a, d: f'pop("#t6", {a}); pop("#k6a", {cap("s6", 1)}); pop("#o6", {cap("s6", 2)}); pop("#k6b", {cap("s6", 2)} + 0.2);',
  [(st("s6"), "uhr-tickt")])

S("s7", "frei-euro", titel_zeile("t7", "Der alte Rekord") + logo("l7", "vodafone.png", 610, 520, glow=ROT) + kalender("k7", "JAHR", "2000", 110, 840, 240, ROT)
  + chip("c7", "kauft Mannesmann", OR, 880, 52, 420) + tz("n7", "≈ 180 Mrd. $", 1060, 110, "glow-o"),
  lambda a, d: f'pop("#t7", {a}); pop("#l7", {cap("s7", 1)}); pop("#k7", {cap("s7", 2)}); pop("#c7", {cap("s7", 2)} + 0.3); slam("#n7", {cap("s7", 3)});',
  [(st("s7"), "swipe"), (cap("s7", 3), "kasse")])

S("s8", "handelssaal", titel_zeile("t8", "Tesla allein") + balken2("b8", "180 Mrd.", "1,5 Bio.", 180, 1500, GRAU, TS, unten=("Rekord 2000", "Tesla heute"))
  + stempel("s8x", "MEHR ALS 8×", 110, 760, OR, 50, -6),
  lambda a, d: f'pop("#t8", {a});' + balken2_js("b8", a + 0.1, cap("s8", 1)) + f' stempeln("#s8x", {cap("s8", 1)} + 0.8);',
  [(st("s8"), "whoosh-weich"), (cap("s8", 1), "kurve-hoch"), (cap("s8", 1) + 0.8, "stempel")])

S("s9", "frei-miami-nacht", titel_zeile("t9", "Warum?", farbe=GELB) + icon_gross("i9", "🤔", 0, 640, 300, GELB, True),
  lambda a, d: f'pop("#t9", {a}); slam("#i9", {a} + 0.2);', [(st("s9"), "spannung")])

S("s10", "wallstreet", titel_zeile("t10", "SpaceX an der Börse") + spacex("l10", 610, 520) + kalender("k10", "SEIT", "JUNI", 390, 790, 300, SX)
  + chip("c10", "größter Börsengang in Amerika", OR, 1130, 50),
  lambda a, d: f'pop("#t10", {a}); pop("#l10", {cap("s10", 0)}); pop("#k10", {cap("s10", 1)}); slam("#c10", {cap("s10", 3)});',
  [(st("s10"), "boersenglocke"), (cap("s10", 3), "pop")])

S("s11", "handelssaal", titel_zeile("t11", "Wer ist mehr wert?") + balken2("b11", "≈ 2 Bio. $", "≈ 1,5 Bio. $", 2000, 1500, SX, TS, unten=("SpaceX", "Tesla")),
  lambda a, d: f'pop("#t11", {a});' + balken2_js("b11", cap("s11", 1), cap("s11", 3)),
  [(st("s11"), "swipe"), (cap("s11", 1), "kurve-hoch")])

S("s12", "frei-code-monitor", titel_zeile("t12", "Februar 2026") + kasten("k12", "🤖 xAI<br/>Musks KI-Firma", 120, 640, 380, 220, OR, 46) + tz("p12", "→", 700, 110)
  + spacex("l12", 700, 340, 640),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {cap("s12", 1)}); pop("#p12", {cap("s12", 1)} + 0.4); pop("#l12", {cap("s12", 1)} + 0.6);',
  [(st("s12"), "whoosh-weich"), (cap("s12", 1) + 0.4, "nv-sog")])

S("s13", "frei-miami-omni", titel_zeile("t13", "Das Herz von SpaceX") + logo("l13", "starlink.png", 620, 460, glow="#fff") + icon_gross("i13", "🛰️", 0, 860, 220, "#fff", True),
  lambda a, d: f'pop("#t13", {a}); pop("#l13", {cap("s13", 1)}); pop("#i13", {cap("s13", 2)}); tl.fromTo("#i13", {{ x: -200 }}, {{ x: 200, duration: 2.5, ease: "none" }}, {cap("s13", 2)});',
  [(st("s13"), "swipe"), (cap("s13", 2), "nv-sog")])

S("s14", "frei-code-monitor", titel_zeile("t14", "Starlink 2025") + donut("d14", 540, 860, 220, [(0.61, SX)], 80) + tz("n14", "61 %", 810, 110, "glow-o")
  + chip("c14", "11,4 Mrd. $ Umsatz", GRUEN, 1120, 54),
  lambda a, d: f'pop("#t14", {a}); pop("#c14", {cap("s14", 2)}); draw("#d14-0", {cap("s14", 3)}, 1.0); slam("#n14", {cap("s14", 3)} + 0.8);',
  [(st("s14"), "zaehler"), (cap("s14", 2), "kasse")])

S("s15", "frei-miami-nacht", titel_zeile("t15", "Und Tesla?") + tesla("l15", 640, 300) + tz("q15", "?", 1000, 160, "glow-o"),
  lambda a, d: f'pop("#t15", {a}); pop("#l15", {a} + 0.1); slam("#q15", {a} + 0.4);', [(st("s15"), "spannung")])

S("s16", "wallstreet", titel_zeile("t16", "Tesla im Umbau") + icon_gross("i16", "🛻", 0, 610, 240, GRAU, True) + kalender("k16", "MITTE", "2027", 390, 880, 300, ROT)
  + stempel("s16x", "CYBERTRUCK: ENDE", 230, 1130, ROT, 48, -4),
  lambda a, d: f'pop("#t16", {a}); pop("#i16", {cap("s16", 1)}); pop("#k16", {cap("s16", 2)}); stempeln("#s16x", {cap("s16", 2)} + 0.5);',
  [(st("s16"), "swipe"), (cap("s16", 2) + 0.5, "stempel")])

S("s17", "frei-code-monitor", titel_zeile("t17", "Die neue Wette") + "".join(icon_gross(f"i17{i}", e, 110 + i * 300, 640, 200, OR) for i, e in enumerate(["🚕", "🤖", "🧠"]))
  + "".join(chip(f"c17{i}", t_, OR, 900, 44, 90 + i * 300) for i, t_ in enumerate(["Robotaxi", "Roboter", "KI"])),
  lambda a, d: f'pop("#t17", {a});' + "".join(f' pop("#i17{i}", {cap("s17", i + 1)}); pop("#c17{i}", {cap("s17", i + 1)} + 0.2);' for i in range(3)),
  [(st("s17"), "whoosh-weich"), (cap("s17", 1), "pop"), (cap("s17", 2), "pop"), (cap("s17", 3), "pop")])

DACH = (f'<div id="d18" style="position:absolute;left:110px;top:620px;width:860px;height:380px;border-radius:30px;border:6px solid {OR};background:#14181bdd;box-shadow:0 0 60px {OR}55;z-index:3"></div>'
        + "".join(f'<div class="e18" style="position:absolute;left:{170 + i * 200}px;top:720px;font-size:140px;z-index:4">{e}</div>' for i, e in enumerate(["🚀", "🛰️", "🧠", "🚗"])))
S("s18", "frei-miami-omni", titel_zeile("t18", "Musks Idee") + DACH + chip("c18", "alles unter einem Dach", OR, 1060, 56),
  lambda a, d: f'pop("#t18", {a}); pop("#d18", {a}); tl.fromTo(".e18", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, stagger: 0.35, ease: "back.out(2)" }}, {cap("s18", 0)}); slam("#c18", {cap("s18", 2)});',
  [(st("s18"), "swipe"), (cap("s18", 2), "pop")])

S("s19", "frei-frankfurt-nacht", titel_zeile("t19", "Elon Musk") + foto_gross("f19", MUSK, 310, 600, 460, 430, "", OR) + chip("c19", "Chef von Tesla UND SpaceX", OR, 1100, 52),
  lambda a, d: f'pop("#t19", {a}); pop("#f19", {a}); slam("#c19", {cap("s19", 1)});', [(st("s19"), "kamera-blitz")])

S("s20", "frei-sitzung", titel_zeile("t20", "Musk sagt") + zettel("z20", "„Eine gute Idee“", 200, 700, 680, 90, GELB, -3),
  lambda a, d: f'pop("#t20", {a}); tl.fromTo("#z20", {{ y: -300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {cap("s20", 1)});',
  [(st("s20"), "zeitung")])

S("s21", "wallstreet", titel_zeile("t21", "Aber …", farbe=ROT) + tz("n21", "3", 640, 320, "glow-r") + chip("c21", "große Hürden", ROT, 1040, 60),
  lambda a, d: f'pop("#t21", {a}); slam("#n21", {cap("s21", 0)} + 0.4); pop("#c21", {cap("s21", 0)} + 0.8);', [(st("s21"), "nv-dun-dun-dun")])

S("s22", "frei-miami-nacht", titel_zeile("t22", "Hürde 1: China", farbe=OR) + flagge("f22a", "flagge-china", 100, 650, 340, -4) + flagge("f22b", "flagge-usa", 640, 650, 340, 4)
  + chip("c22a", "Tesla-Werk Shanghai", TS, 920, 40) + chip("c22b", "SpaceX + US-Militär", SX, 1010, 40),
  lambda a, d: f'slam("#t22", {a}); pop("#f22a", {cap("s22", 1)}); pop("#c22a", {cap("s22", 1)} + 0.3); pop("#f22b", {cap("s22", 2)}); pop("#c22b", {cap("s22", 3)});',
  [(st("s22"), "nv-boom-kurz"), (cap("s22", 2), "pop")])

S("s23", "frei-miami-nacht", titel_zeile("t23", "Das Problem") + stempel("s23x", "PASST SCHWER ZUSAMMEN", 170, 760, ROT, 46, -5),
  lambda a, d: f'pop("#t23", {a}); stempeln("#s23x", {a} + 0.3);', [(st("s23"), "stempel")])

S("s24", "frei-sitzung", titel_zeile("t24", "Hürde 2: Abstimmung", farbe=OR) + icon_gross("i24", "🗳️", 0, 600, 220, OR, True)
  + vergleich("v24", "NÖTIG", "> 50 % aller<br/>Tesla-Aktien", "NICHT NUR", "50 % der<br/>Wählenden", GRUEN, GRAU, 870, 260),
  lambda a, d: f'slam("#t24", {a}); pop("#i24", {cap("s24", 1)}); pop("#v24-l", {cap("s24", 2)}); pop("#v24-r", {cap("s24", 4)});',
  [(st("s24"), "nv-boom-kurz"), (cap("s24", 2), "klick")])

S("s25", "frei-sitzung", titel_zeile("t25", "Musk selbst") + zettel("z25", "„ziemlich hohe Hürde“", 180, 700, 720, 80, GELB, -3),
  lambda a, d: f'pop("#t25", {a}); tl.fromTo("#z25", {{ y: -300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {cap("s25", 1)});',
  [(st("s25"), "zeitung")])

S("s26", "handelssaal", titel_zeile("t26", "Hürde 3: Macht", farbe=OR) + icon_gross("i26", "👑", 0, 640, 300, GELB, True),
  lambda a, d: f'slam("#t26", {a}); slam("#i26", {a} + 0.3);', [(st("s26"), "nv-boom-kurz")])

S("s27", "wallstreet", titel_zeile("t27", "Normalerweise") + tz("n27", "1 Aktie = 1 Stimme", 760, 96, "glow-o"),
  lambda a, d: f'pop("#t27", {a}); slam("#n27", {cap("s27", 1)});', [(st("s27"), "klick")])

S("s28", "frei-frankfurt-nacht", titel_zeile("t28", "Musks Anteil") + logo("l28", "barclays-voll.png", 600, 380, glow="#00aeef", pad=14)
  + donut("d28", 540, 930, 200, [(0.37, OR)], 70) + tz("n28", "37 %", 885, 100, "glow-o") + quelle("q28", "Schätzung Barclays · Besitz", 1170),
  lambda a, d: f'pop("#t28", {a}); pop("#l28", {cap("s28", 0)}); draw("#d28-0", {cap("s28", 1)}, 1.0); slam("#n28", {cap("s28", 2)}); pop("#q28", {cap("s28", 2)} + 0.3);',
  [(st("s28"), "swipe"), (cap("s28", 2), "zaehler")])

S("s29", "frei-frankfurt-nacht", titel_zeile("t29", "Musks Stimmen") + chip("c29", "SpaceX-Aktien: 10-faches Stimmrecht", OR, 610, 44)
  + donut("d29", 540, 930, 200, [(0.56, ROT)], 70) + tz("n29", "56 %", 885, 100, "glow-r"),
  lambda a, d: f'pop("#t29", {a}); pop("#c29", {cap("s29", 1)}); draw("#d29-0", {cap("s29", 3)}, 1.0); slam("#n29", {cap("s29", 4)});',
  [(st("s29"), "swipe"), (cap("s29", 4), "bass-schlag")])

S("s30", "handelssaal", titel_zeile("t30", "Heißt") + foto_gross("f30", MUSK, 360, 600, 360, 330, "", ROT) + stempel("s30x", "ENTSCHEIDET FAST ALLES", 160, 1010, ROT, 44, -4),
  lambda a, d: f'pop("#t30", {a}); pop("#f30", {a}); stempeln("#s30x", {cap("s30", 1)});', [(st("s30"), "stempel")])

S("s31", "wallstreet", titel_zeile("t31", "Tesla-Aktionäre?") + tesla("l31", 640, 280) + tz("q31", "?", 980, 140, "glow-o"),
  lambda a, d: f'pop("#t31", {a}); pop("#l31", {a} + 0.1); slam("#q31", {cap("s31", 1)});', [(st("s31"), "spannung")])

S("s32", "handelssaal", titel_zeile("t32", "Der Tausch") + tesla("l32a", 660, 220, 110) + tz("p32", "⇄", 700, 130) + spacex("l32b", 700, 340, 620),
  lambda a, d: f'pop("#t32", {a}); pop("#l32a", {cap("s32", 0)}); slam("#p32", {cap("s32", 1)}); pop("#l32b", {cap("s32", 1)} + 0.2);',
  [(st("s32"), "swipe"), (cap("s32", 1), "whoosh-schnell")])

S("s33", "frei-euro", titel_zeile("t33", "Der Preis") + icon_gross("i33", "💰", 0, 620, 240, GRUEN, True) + chip("c33", "Aufschlag nötig", GRUEN, 940, 64),
  lambda a, d: f'pop("#t33", {a}); pop("#i33", {cap("s33", 1)}); slam("#c33", {cap("s33", 2)});', [(st("s33"), "kasse")])

S("s34", "frei-frankfurt-staedel", titel_zeile("t34", "Auch Deutschland") + flagge("f34", "flagge-deutschland", 340, 620, 400, -3) + icon_gross("i34", "🏭", 0, 900, 180, OR, True)
  + chip("c34", "Tesla-Werk Grünheide", TS, 1110, 52),
  lambda a, d: f'pop("#t34", {a}); pop("#f34", {cap("s34", 1)}); pop("#i34", {cap("s34", 2)}); slam("#c34", {cap("s34", 3)});', [(st("s34"), "swipe")])

S("s35", "wallstreet", titel_zeile("t35", "Betroffen?") + tesla("l35", 620, 200, 140) + icon_gross("i35", "🧺", 620, 600, 200, OR) + chip("c35", "Tesla-Aktie ODER Welt-ETF", OR, 900, 50),
  lambda a, d: f'pop("#t35", {a}); pop("#l35", {cap("s35", 0)}); pop("#i35", {cap("s35", 1)}); slam("#c35", {cap("s35", 3)});', [(st("s35"), "klick")])

S("s36", "frei-sitzung", titel_zeile("t36", "Stand heute") + icon_gross("i36", "📝", 0, 620, 240, GRAU, True) + stempel("s36x", "NOCH NICHTS UNTERSCHRIEBEN", 130, 960, OR, 38, -4),
  lambda a, d: f'pop("#t36", {a}); pop("#i36", {a} + 0.1); stempeln("#s36x", {cap("s36", 1)});', [(st("s36"), "stempel")])

S("s37", "frei-miami-nacht", titel_zeile("t37", "Ein Mann an der Spitze") + foto_gross("f37", MUSK, 310, 600, 460, 430, "", GELB) + icon_gross("i37", "👑", 0, 540, 140, GELB, True)
  + partikel("pa37", 540, 820, 26, (GELB, OR, "#fff"), 520),
  lambda a, d: f'pop("#t37", {a}); pop("#f37", {cap("s37", 1)}); slam("#i37", {cap("s37", 3)}); burst("#pa37", {cap("s37", 3)} + 0.2);',
  [(st("s37"), "spannung"), (cap("s37", 3), "nv-tusch")])

S("s38", "wallstreet", titel_zeile("t38", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t38", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
  [(st("s38"), "zeitung")])

K.SZ.append((0.0, K.dauer, news_kopf("15.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
