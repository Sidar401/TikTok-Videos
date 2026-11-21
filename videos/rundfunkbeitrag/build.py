#!/usr/bin/env python3
"""HundeFinanzTv (~71 s, Stimme Dan) – Rundfunkbeitrag. NEUES FORMAT.
18,36 €/Monat pro Wohnung = 220,32 €/Jahr, ≈ 9 Mrd. €/Jahr, an ARD/ZDF/Deutschlandradio; KEF empfiehlt 18,64 € ab 2027 (+28 Cent),
16 Länder müssen zustimmen; BVerfG-Entscheidung zur Klage von ARD/ZDF steht aus; WG teilt; Befreiung (Bürgergeld/BAföG/Grundsicherung) auf Antrag.
Quellen: ZDFheute (KEF), Stuttgarter Zeitung."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
WURZEL = HERE.parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 15)  # Logo nach dem Open Loop (s4)

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
LOGOS = [f for f in ("ard.svg", "zdf.svg", "deutschlandradio.svg") if (WURZEL / "brand/logos" / f).exists()]
K = Kit(HERE, 14, [], logos=LOGOS + ["flagge-deutschland.svg"])
cap, st = K.cap, K.st
S = K.szene


def sender(id_, name, x, y, w=280):
    """Original-Logo, sonst Namens-Plakette."""
    datei = {"ARD": "ard.svg", "ZDF": "zdf.svg", "Deutschlandradio": "deutschlandradio.svg"}[name]
    inhalt = (f'<img src="assets/logos/{datei}" style="max-width:100%;max-height:90px"/>' if datei in LOGOS
              else f'<div style="font-weight:900;font-size:{56 if len(name) < 6 else 34}px;color:#00346e">{name}</div>')
    return f'<div id="{id_}" class="nk-karte" style="left:{x}px;top:{y}px;width:{w}px;height:170px;display:flex;align-items:center;justify-content:center;padding:20px">{inhalt}</div>'


def titel(id_, text, y=340, farbe=D, gr=70):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=52):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe}">{text}</div>'


# s1 Hook
S("s1", None, nl.CSS + titel("t1", "Fast jeder Haushalt zahlt", 340, D, 60) + gross("n1", "220 €", 470, R, 220) + pille("p1", "pro Jahr", 760, D, "#fff", 54)
  + sender("a1", "ARD", 90, 900) + sender("z1", "ZDF", 400, 900) + sender("d1", "Deutschlandradio", 710, 900),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#n1", {a}); pop("#p1", {cap("s1", 0)} + 0.4); pop("#a1", {cap("s1", 1)}); pop("#z1", {cap("s1", 1)} + 0.2); pop("#d1", {cap("s1", 1)} + 0.4);')

# s2 Teilen-CTA
S("s2", None, titel("t2", "Teile das mit jemandem,", 420, D, 62)
  + nl.karte("k2", "der sich weigert …", f'<div style="font-weight:900;font-size:64px;color:{O};text-align:center;padding:20px 0">den Rundfunkbeitrag<br/>zu bezahlen 😅</div>', y=580),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 2)});')

# s3–s4 Steigt + Open Loop
S("s3", None, titel("t3", "Und er soll steigen", 360, R) + gross("n3", "▲", 500, R, 200)
  + nl.karte("k4", "Gleich im Video", nl.zeile("r4a", "Wohin das Geld fließt", "?", O) + nl.zeile("r4b", "Wie du legal weniger zahlst", "✓", G), y=780),
  lambda a, d: f'pop("#t3", {a}); pop("#n3", {cap("s3", 1)}); pop("#k4", {cap("s4", 0)}); pop("#r4a", {cap("s4", 1)}); pop("#r4b", {cap("s4", 2)});', [], bis="s5")

# s5 Beitrag
S("s5", None, titel("t5", "Der Beitrag", 340) + nl.karte("k5", "Rundfunkbeitrag",
  nl.zeile("r5a", "Pro Monat", "18,36 €", O) + nl.zeile("r5b", "Gilt pro", "Wohnung", D) + nl.zeile("r5c", "Nicht pro", "Person", G, "✓"), y=520),
  lambda a, d: f'pop("#t5", {a}); pop("#k5", {a} + 0.1); pop("#r5a", {cap("s5", 1)}); pop("#r5b", {cap("s5", 2)}); pop("#r5c", {cap("s5", 3)});')

# s6–s7 Geld & Empfänger
S("s6", None, titel("t6", "Pro Jahr zusammen", 340) + gross("n6", "≈ 9 Mrd. €", 470, O, 150)
  + sender("a7", "ARD", 90, 780) + sender("z7", "ZDF", 400, 780) + sender("d7", "Deutschlandradio", 710, 780)
  + pille("p7", "den größten Teil bekommt die ARD", 1010, D, "#fff", 44),
  lambda a, d: (f'pop("#t6", {a}); pop("#n6", {cap("s6", 1)}); pop("#a7", {cap("s7", 1)}); pop("#z7", {cap("s7", 1)} + 0.2); pop("#d7", {cap("s7", 2)});'
                f' pop("#p7", {cap("s7", 3)});'), [], bis="s8")

# s8–s9 KEF-Empfehlung
S("s8", None, titel("t8", "Ab 2027?", 340, R) + nl.karte("k8", "Empfehlung der KEF",
  nl.zeile("r8a", "Heute", "18,36 €", D) + nl.zeile("r8b", "Ab 2027", "18,64 €", R, "▲") + nl.zeile("r9a", "Plus im Monat", "28 Cent", R)
  + nl.zeile("r9b", "Zustimmung nötig", "alle 16 Länder", O), y=500),
  lambda a, d: (f'pop("#t8", {a}); pop("#k8", {a} + 0.1); pop("#r8a", {cap("s8", 1)}); pop("#r8b", {cap("s8", 2)}); pop("#r9a", {cap("s9", 0)} + 0.3);'
                f' pop("#r9b", {cap("s9", 2)});'), [], bis="s10")

# s10 Verfassungsgericht
S("s10", None, titel("t10", "Bald entscheidet …", 340) + nl.karte("k10", "Bundesverfassungsgericht",
  nl.zeile("r10a", "Klage von", "ARD + ZDF", D) + nl.zeile("r10b", "Urteil", "steht noch aus", O), y=520),
  lambda a, d: f'pop("#t10", {a}); pop("#k10", {cap("s10", 1)}); pop("#r10a", {cap("s10", 2)}); pop("#r10b", {cap("s10", 3)});')

# s11 WG-Tipp
S("s11", None, titel("t11", "Spar-Tipp 1: WG", 340, G) + nl.karte("k11", "Beispiel: 3er-WG",
  nl.zeile("r11a", "Beitrag pro Wohnung", "18,36 €", D) + nl.zeile("r11b", "Pro Person", "6,12 €", G, "✓"), y=520),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {cap("s11", 1)}); pop("#r11a", {cap("s11", 2)}); pop("#r11b", {cap("s11", 3)});')

# s12 Befreiung
S("s12", None, titel("t12", "Spar-Tipp 2: Befreiung", 340, G, 62) + nl.karte("k12", "Befreit werden kann, wer bekommt:",
  nl.zeile("r12a", "Bürgergeld", "✓", G) + nl.zeile("r12b", "BAföG", "✓", G) + nl.zeile("r12c", "Grundsicherung", "✓", G), y=500)
  + pille("p12", "nur auf Antrag!", 1030, R, "#fff", 54),
  lambda a, d: (f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 0)} + 0.3); pop("#r12b", {cap("s12", 1)}); pop("#r12c", {cap("s12", 2)});'
                f' pop("#p12", {cap("s12", 4)});'))

# s13 Kommentar
S("s13", None, titel("t13", "Deine Meinung", 360) + nl.karte("k13", "Schreib’s in die Kommentare",
  f'<div style="font-weight:900;font-size:62px;color:{O};text-align:center;padding:20px 0">Findest du den<br/>Beitrag fair?</div>', y=560),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.2);')

# s14 Folgen
S("s14", None, f'<div id="fl14" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n14" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c14", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl14", {a}); pop("#n14", {a} + 0.2); pop("#c14", {cap("s14", 0)} + 0.4);')

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "22.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
