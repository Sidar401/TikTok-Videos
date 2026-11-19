#!/usr/bin/env python3
"""HundeFinanzTv (73 s, Stimme Dan): Wirecard – DAX-Konzern 24 Mrd. €, 1,9 Mrd. € fehlen, Urteil vor Weihnachten möglich,
DAX-Aufstieg 2018 statt Commerzbank, FT-Warnung, BaFin zeigt Journalisten an, Juni 2020 Knall (−95 %, Pleite),
Braun U-Haft (Unschuldsvermutung), Marsalek in Moskau. Leitmotiv: Wirecard-Kurs (Aufstieg → Absturz) + leerer Tresor."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
WURZEL = HERE.parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 19)  # Logo nach dem Open Loop (s4)

from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, hand, icon_gross, kalender, kreis, linie, news_kopf,  # noqa: E402
                         person, pfeil, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, folg_js, folg_logo, logo  # noqa: E402

WC = (WURZEL / "brand/logos/wirecard.svg").exists()
K = Kit(HERE, 13, ["handelssaal", "wallstreet", "frei-code-css", "frei-miami-omni"],
        logos=["commerzbank.png", "ft.svg"] + (["wirecard.svg"] if WC else []))
cap, st = K.cap, K.st
S = K.szene
WCB = "#1b3c6e"


def wirecard(id_, y, w, x=None):
    if WC:
        return logo(id_, "wirecard.svg", y, w, x=x, pad=30, glow=WCB)
    pos = f"left:{x}px" if x is not None else f"left:{(1080 - w) // 2}px"
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;width:{w}px;padding:26px 0;border-radius:24px;background:#fff;text-align:center;'
            f'font-weight:900;font-size:{w * 0.16:.0f}px;color:{WCB};letter-spacing:-1px;box-shadow:0 0 60px #3a7bd566, 0 30px 50px #000;z-index:4">wirecard</div>')


def zahl(id_, text, y, farbe, gr=170):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;text-align:center;font-weight:900;font-size:{gr}px;color:{farbe};'
            f'text-shadow:0 0 50px {farbe}aa;z-index:5">{text}</div>')


def plakette(id_, text, x, y, farbe, w=380, size=60, schrift="#fff"):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:22px 0;border-radius:22px;background:{farbe};color:{schrift};'
            f'font-weight:900;font-size:{size}px;text-align:center;box-shadow:0 0 40px {farbe}88, 0 20px 30px #000;z-index:4">{text}</div>')


# s1 Hook
S("s1", "handelssaal", KIT_CSS + titel_zeile("t1", "⚡ Ein DAX-Konzern", farbe=GELB) + wirecard("l1", 600, 560)
  + zahl("n1", "24 Mrd. €", 820, GRUEN, 150) + stempel("s1x", "−1,9 Mrd. € FEHLEN", 110, 1040, ROT, 70, -6),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1", {a}); pop("#n1", {cap("s1", 1)}); stempeln("#s1x", {cap("s1", 3)}); shake("#n1", {cap("s1", 3)} + 0.2);',
  [(0.0, "bass-schlag")])

# s2 größter Bilanzskandal
S("s2", "wallstreet", titel_zeile("t2", "Das ist Wirecard") + wirecard("l2", 640, 480)
  + stempel("s2x", "BILANZ-SKANDAL", 170, 900, ROT, 80, -8),
  lambda a, d: f'pop("#t2", {a}); pop("#l2", {a} + 0.1); stempeln("#s2x", {cap("s2", 1)});',
  [(cap("s2", 1), "stempel")])

# s3 Urteil vor Weihnachten
S("s3", "frei-miami-omni", titel_zeile("t3", "Urteil vor Weihnachten?", gr=52) + icon_gross("i3", "⚖️", 140, 640, 260, GELB)
  + kalender("k3", "DEZ", "?", 600, 620, 300, ROT) + chip("c3", "seit Dezember 2022 vor Gericht", OR, 1020, 46),
  lambda a, d: f'pop("#t3", {a}); pop("#c3", {cap("s3", 0)} + 0.4); pop("#i3", {cap("s3", 1)}); pop("#k3", {cap("s3", 2)});')

# s4 Wer fehlt? (Open Loop)
S("s4", "frei-code-css", titel_zeile("t4", "Wer fehlt?", farbe=ROT) + icon_gross("i4", "🪑", 0, 640, 300, ROT, True)
  + zahl("q4", "?", 560, GELB, 220) + kreis("kr4", 540, 790, 230, 230, GELB) + hand("h4", "nicht auf der Anklagebank", 540, 1080, 62, "#fff", -3, True),
  lambda a, d: (f'pop("#t4", {a}); pop("#i4", {cap("s4", 2)}); pop("#h4", {cap("s4", 3)}); slam("#q4", {cap("s4", 4)}); draw("#kr4-p", {cap("s4", 5)}, 0.6);'),
  [(cap("s4", 4), "spannung")])

# s5 2018 DAX: Commerzbank raus, Wirecard rein
S("s5", "handelssaal", titel_zeile("t5", "2018: Ab in den DAX", farbe=GRUEN)
  + vergleich("v5", "RAUS", "Commerz-<br/>bank", "REIN", "Wirecard", ROT, GRUEN, y=640, h=300)
  + linie("lk5", [0.05, 0.1, 0.2, 0.3, 0.45, 0.6, 0.8, 0.97], 120, 1000, 740, 150, GRUEN, True, [(7, "≈ 200 €")]),
  lambda a, d: f'pop("#t5", {a}); pop("#v5-r", {cap("s5", 1)}); pop("#v5-l", {cap("s5", 3)}); draw("#lk5-p", {cap("s5", 0)} + 0.3, 1.4); pop("#lk5-w0", {cap("s5", 2)});')

# s6 Financial Times warnt
S("s6", "wallstreet", titel_zeile("t6", "Die Warnung") + logo("l6", "ft.svg", 600, 260, x=140, pad=24, glow="#fcd0b1")
  + zettel("z6", "Hier stimmt<br/>was nicht!", 470, 640, 470, 70, GELB, 4) + hand("h6", "schon Jahre vorher", 540, 1050, 64, "#fff", -3, True),
  lambda a, d: f'pop("#t6", {a}); pop("#l6", {a} + 0.1); pop("#h6", {cap("s6", 1)}); pop("#z6", {cap("s6", 2)});')

# s7 BaFin zeigt Journalisten an
S("s7", "frei-miami-omni", titel_zeile("t7", "Die Finanzaufsicht") + plakette("b7", "BaFin", 70, 640, "#00447c", 360, 72)
  + pfeil("p7", 450, 720, 650, 720, 0.2, ROT) + person("pj7", "Journalisten", "Financial Times", 680, 590, 300, ROT)
  + stempel("s7x", "ANZEIGE", 200, 960, ROT, 80, -8) + hand("h7", "statt gegen Wirecard!", 500, 1100, 48, GELB, -4),
  lambda a, d: (f'pop("#t7", {a}); pop("#b7", {a} + 0.1); draw("#p7-p", {cap("s7", 2)}, 0.4); pop("#p7-k", {cap("s7", 2)} + 0.4); pop("#pj7", {cap("s7", 2)} + 0.3);'
                f' stempeln("#s7x", {cap("s7", 2)} + 0.4); pop("#h7", {cap("s7", 2)} + 0.8);'),
  [(cap("s7", 2) + 0.4, "falsch")])

# s8 Juni 2020: 1,9 Mrd. gab es nie
S("s8", "frei-code-css", titel_zeile("t8", "Juni 2020: der Knall", farbe=ROT) + icon_gross("i8", "🗄️", 0, 610, 280, OR, True)
  + zahl("n8", "1,9 Mrd. €", 900, GELB, 130) + stempel("s8x", "GAB ES WOHL NIE", 150, 1050, ROT, 70, -6),
  lambda a, d: f'pop("#t8", {a}); pop("#i8", {cap("s8", 1)}); pop("#n8", {cap("s8", 1)} + 0.3); stempeln("#s8x", {cap("s8", 2)});',
  [(cap("s8", 2), "tresor")])

# s9 Absturz −95 %, pleite
S("s9", "handelssaal", titel_zeile("t9", "Der Absturz", farbe=ROT)
  + linie("lk9", [0.95, 0.93, 0.9, 0.35, 0.12, 0.05, 0.03], 120, 640, 840, 360, ROT, True, [(0, "104 €"), (6, "−95 %")])
  + stempel("s9x", "PLEITE", 300, 1060, ROT, 100, -8),
  lambda a, d: f'pop("#t9", {a}); pop("#lk9-w0", {a} + 0.2); draw("#lk9-p", {cap("s9", 1)}, 1.0); pop("#lk9-w1", {cap("s9", 2)}); stempeln("#s9x", {cap("s9", 2)} + 0.8);',
  [(cap("s9", 1), "kurve-runter")])

# s10 Braun in U-Haft
S("s10", "wallstreet", titel_zeile("t10", "Der Chef") + person("pb10", "Markus Braun", "Ex-Chef", 120, 600, 380, OR)
  + chip("c10", "U-Haft seit 2020", ROT, 680, 46, x=560) + zettel("z10", "bestreitet<br/>alles", 590, 820, 380, 60, GELB, 4)
  + hand("h10", "es gilt die Unschuldsvermutung", 540, 1130, 50, "#fff", -2, True),
  lambda a, d: f'pop("#t10", {a}); pop("#pb10", {a} + 0.1); pop("#c10", {cap("s10", 2)}); pop("#z10", {cap("s10", 3)}); pop("#h10", {cap("s10", 4)});')

# s11 Marsalek: Flucht nach Moskau
ROUTE = ('<svg id="r11" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:3">'
         f'<path id="r11-p" d="M220 990 Q520 700 830 640" fill="none" stroke="{GELB}" stroke-width="10" stroke-dasharray="26 18" style="filter:drop-shadow(0 0 12px {GELB})"/></svg>')
ORT = lambda id_, t, x, y, f: (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;z-index:5;text-align:center"><div style="width:34px;height:34px;margin:0 auto;border-radius:50%;'
                               f'background:{f};box-shadow:0 0 30px {f}"></div><div style="margin-top:8px;font-weight:900;font-size:48px;color:#fff;text-shadow:0 0 20px #000">{t}</div></div>')
S("s11", "frei-miami-omni", titel_zeile("t11", "Die Flucht", farbe=GELB) + person("pm11", "Jan Marsalek", "Ex-Vorstand", 90, 600, 300, ROT)
  + ROUTE + ORT("o11a", "München", 120, 972, OR) + ORT("o11b", "Moskau", 740, 622, ROT)
  + f'<div id="fl11" style="position:absolute;left:190px;top:930px;font-size:90px;z-index:6">✈️</div>'
  + chip("c11", "russischer Geheimdienst?", ROT, 1150, 50),
  lambda a, d: (f'pop("#t11", {a}); pop("#pm11", {a} + 0.1); pop("#o11a", {cap("s11", 1)}); draw("#r11-p", {cap("s11", 1)} + 0.2, 1.6);'
                f' tl.fromTo("#fl11", {{ x: 0, y: 0, rotation: -20 }}, {{ x: 560, y: -300, rotation: 10, duration: 1.6, ease: "power1.inOut" }}, {cap("s11", 1)} + 0.2); tl.to("#fl11", {{ opacity: 0, duration: 0.3 }}, {cap("s11", 1)} + 1.8);'
                f' pop("#o11b", {cap("s11", 3)}); slam("#c11", {cap("s11", 4)});'))

# s12 Lehre: streuen
S("s12", "handelssaal", titel_zeile("t12", "Unsere Lehre", farbe=GRUEN) + icon_gross("i12", "🧺", 0, 620, 300, GRUEN, True)
  + chip("c12", "nie alles auf eine Aktie", GRUEN, 1000, 60) + hand("h12", "auch kein DAX-Konzern ist sicher", 540, 1130, 52, GELB, -3, True),
  lambda a, d: f'pop("#t12", {a}); pop("#i12", {a} + 0.1); slam("#c12", {cap("s12", 1)}); pop("#h12", {cap("s12", 3)});')

# s13 Folgen (letzter Satz)
S("s13", "wallstreet", titel_zeile("t13", "Folg uns") + folg_logo("fl13", 600, 360) + chip("c13", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t13", {a}); {folg_js("fl13", a)} slam("#c13", {cap("s13", 0)} + 0.4);')

html, code = ls.szene()
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, news_kopf("19.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
