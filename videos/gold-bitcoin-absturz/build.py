#!/usr/bin/env python3
"""HundeFinanzTv Short (News v2, ~72 s): Gold UND Bitcoin stürzen gleichzeitig. Kommentar- + Folgen-CTA (Beagle-Logo), Laufband, Hinweis am Ende."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, icon_gross, kalender, laufband_szene, linie, news_kopf,  # noqa: E402
                         quelle, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, logo, tz  # noqa: E402

GOLD = "#f5c542"
BTC = "#f7931a"
K = Kit(HERE, 17, ["wallstreet", "handelssaal", "frei-euro", "frei-50euro", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-sitzung", "frei-code-monitor"],
        logos=["bitcoin.svg", "fed.png", "anthropic.svg"])
cap, st = K.cap, K.st
S = K.szene


def barren(id_, x, y, w=300):
    h = int(w * 0.42)
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:14px;'
            f'background:linear-gradient(160deg,#fff3b0 0%,{GOLD} 35%,#b8860b 100%);box-shadow:0 0 60px {GOLD}99, 0 24px 40px #000;'
            f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:{w // 7}px;color:#7a5a00;letter-spacing:4px;z-index:4">GOLD</div>')


def btc(id_, x, y, w):
    return f'<img id="{id_}" src="assets/logos/bitcoin.svg" alt="" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;filter:drop-shadow(0 0 50px {BTC}aa) drop-shadow(0 20px 30px #000);z-index:4"/>'


S("s1", "handelssaal", KIT_CSS + titel_zeile("t1", "⚡ Doppel-Absturz", farbe=ROT) + barren("g1", 110, 680, 380) + btc("b1", 640, 620, 300)
  + icon_gross("i1", "📉", 0, 900, 180, ROT, True),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#g1", {a}); pop("#b1", {a} + 0.1); slam("#i1", {cap("s1", 1)}); shake("#g1", {cap("s1", 1)}); shake("#b1", {cap("s1", 1)});',
  [(0.0, "eilmeldung"), (cap("s1", 1), "crash-bass")])

S("s2", "wallstreet", titel_zeile("t2", "Die Kurse") + vergleich("v2", "GOLD", "&lt; 3.900 $", "BITCOIN", "kurz 62.000 $", ROT, ROT, y=620, h=300)
  + quelle("q2", "Nacht auf Sonntag · Börsendaten", 960),
  lambda a, d: f'pop("#t2", {a}); pop("#v2-l", {cap("s2", 1)}); pop("#v2-r", {cap("s2", 3)}); pop("#q2", {cap("s2", 3)} + 0.3);',
  [(st("s2"), "swipe"), (cap("s2", 1), "kurve-runter"), (cap("s2", 3), "kurve-runter")])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Deine Wahl") + barren("g3", 70, 660, 300) + btc("b3", 660, 600, 260) + tz("v3", "oder", 700, 70)
  + chip("c3", "💬 schreib's in die Kommentare", OR, 960, 52),
  lambda a, d: f'pop("#t3", {a}); pop("#g3", {cap("s3", 1)}); pop("#v3", {cap("s3", 2)} - 0.2); pop("#b3", {cap("s3", 2)}); slam("#c3", {cap("s3", 0)} + 0.3);',
  [(st("s3"), "handy-benachrichtigung"), (cap("s3", 2), "pop")])

S("s4", "frei-frankfurt-staedel", titel_zeile("t4", "Folg uns") + folg_logo("fl4", 600, 360) + chip("c4", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t4", {a}); {folg_js("fl4", a)} slam("#c4", {cap("s4", 0)} + 0.4);', [(st("s4"), "swipe"), (st("s4") + 0.4, "level-up")])

K5 = linie("ku5", [0.45, 0.62, 0.95, 0.8, 0.7, 0.55, 0.45, 0.32, 0.22, 0.18], 120, 640, 840, 440, GOLD, punkte=[(2, "≈ 5.600 $")])
S("s5", "frei-euro", titel_zeile("t5", "Gold · 2026") + K5 + chip("c5", "Rekord im Januar", GOLD, 1110, 50),
  lambda a, d: f'pop("#t5", {a}); draw("#ku5-p", {a} + 0.1, 1.2); tl.fromTo("#ku5-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 0.6); pop("#ku5-w0", {cap("s5", 2)}); pop("#c5", {cap("s5", 2)} + 0.3);',
  [(st("s5"), "kurve-hoch"), (cap("s5", 2), "pop")])

S("s6", "handelssaal", titel_zeile("t6", "Gold heute", farbe=ROT) + balken2("b6", "5.600 $", "3.890 $", 5600, 3890, GOLD, ROT, basis=1130, hmax=420, unten=("Januar", "jetzt"))
  + stempel("s6x", "−31 %", 660, 640, ROT, 70, 8),
  lambda a, d: f'pop("#t6", {a});' + balken2_js("b6", st("s6") + 0.1, cap("s6", 1)) + f' stempeln("#s6x", {cap("s6", 2)});',
  [(cap("s6", 1), "kurve-runter"), (cap("s6", 2), "stempel")])

S("s7", "wallstreet", titel_zeile("t7", "Bitcoin-Rekord") + btc("b7", 380, 600, 320) + tz("n7", "≈ 126.000 $", 980, 120, "glow-g") + chip("c7", "Oktober 2025", GRUEN, 1110, 46),
  lambda a, d: f'pop("#t7", {a}); pop("#b7", {a}); slam("#n7", {cap("s7", 1)}); pop("#c7", {cap("s7", 1)} + 0.3);', [(st("s7"), "whoosh-weich"), (cap("s7", 1), "kasse")])

HALB = (f'<div id="h8" style="position:absolute;left:340px;top:620px;width:400px;height:400px;border-radius:50%;background:conic-gradient({BTC} 0 50%, #ffffff18 50% 100%);'
        f'box-shadow:0 0 70px {BTC}88;z-index:3"></div>')
S("s8", "frei-50euro", titel_zeile("t8", "Jetzt", farbe=ROT) + HALB + tz("n8", "nur noch ½", 1060, 100, "glow-r"),
  lambda a, d: f'pop("#t8", {a}); tl.fromTo("#h8", {{ rotation: -180, scale: 0.4 }}, {{ rotation: 0, scale: 1, duration: 0.7, ease: "back.out(1.4)" }}, {a} + 0.1); slam("#n8", {cap("s8", 1)});',
  [(st("s8"), "nv-sog"), (cap("s8", 1), "glas-bricht")])

S("s9", "frei-sitzung", titel_zeile("t9", "Eigentlich …") + icon_gross("i9", "🛡️", 0, 600, 280, GOLD, True) + chip("c9", "„Schutz, wenn's kracht“", GOLD, 960, 58),
  lambda a, d: f'pop("#t9", {a}); pop("#i9", {cap("s9", 1)}); slam("#c9", {cap("s9", 1)} + 0.3);', [(st("s9"), "tresor")])

S("s10", "handelssaal", titel_zeile("t10", "Warum zusammen?", farbe=GELB) + icon_gross("i10", "🤔", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t10", {a}); slam("#i10", {a} + 0.2);', [(st("s10"), "spannung")])

S("s11", "wallstreet", titel_zeile("t11", "Grund 1: Zinsen", farbe=GELB) + logo("l11", "fed.png", 580, 320, x=140, karte=True, glow="#fff", pad=24)
  + kalender("k11", "DEZ", "9", 640, 600, 240, ROT) + chip("c11", "Zins-Erhöhung möglich", ROT, 1000, 54),
  lambda a, d: f'pop("#t11", {a}); pop("#l11", {cap("s11", 1)}); pop("#k11", {cap("s11", 2)}); slam("#c11", {cap("s11", 2)} + 0.3);',
  [(st("s11"), "swipe"), (cap("s11", 2), "uhr-tickt")], )

S("s12", "frei-euro", titel_zeile("t12", "Zinsen locken") + vergleich("v12", "SPARBUCH · ANLEIHEN", "Zinsen ↑", "GOLD · BITCOIN", "0 Zinsen", GRUEN, ROT, y=620, h=300),
  lambda a, d: f'pop("#t12", {a}); pop("#v12-l", {cap("s12", 0)}); pop("#v12-r", {cap("s12", 2)});', [(cap("s12", 0), "geld-erhalten"), (cap("s12", 2), "falsch")])

S("s13", "handelssaal", titel_zeile("t13", "Grund 2: Abflüsse", farbe=GELB) + btc("b13", 400, 600, 280) + tz("n13", "−1,3 Mrd. $", 940, 120, "glow-r")
  + chip("c13", "aus Bitcoin-ETFs · 1 Woche", ROT, 1100, 46),
  lambda a, d: f'pop("#t13", {a}); pop("#b13", {cap("s13", 1)}); tl.to("#b13", {{ y: 120, opacity: 0.4, duration: 1.2 }}, {cap("s13", 3)}); slam("#n13", {cap("s13", 3)}); pop("#c13", {cap("s13", 4)});',
  [(st("s13"), "swipe"), (cap("s13", 3), "kurve-runter")])

S("s14", "frei-code-monitor", titel_zeile("t14", "Vermutung") + logo("l14", "anthropic.svg", 620, 620, glow="#d97757", pad=30) + kalender("k14", "DO", "19.11.", 140, 820, 280, "#d97757")
  + zettel("z14", "Geld frei für den<br/>Börsengang?", 500, 860, 460, 46, GELB, 4),
  lambda a, d: f'pop("#t14", {a}); pop("#l14", {cap("s14", 3)}); pop("#k14", {cap("s14", 4)}); pop("#z14", {cap("s14", 2)});',
  [(st("s14"), "whoosh-weich"), (cap("s14", 3), "pop")])

S("s15", "frei-sitzung", titel_zeile("t15", "Merk dir") + icon_gross("i15", "⚓", 0, 600, 260, OR, True) + stempel("s15x", "AUCH SICHER SCHWANKT", 120, 940, OR, 50, -5),
  lambda a, d: f'pop("#t15", {a}); pop("#i15", {a} + 0.1); tl.fromTo("#i15", {{ rotation: -14 }}, {{ rotation: 14, duration: 0.5, yoyo: true, repeat: 3 }}, {a} + 0.3); stempeln("#s15x", {cap("s15", 1)});',
  [(cap("s15", 1), "stempel")])

S("s16", "frei-frankfurt-nacht", titel_zeile("t16", "Lieber verteilen", farbe=GRUEN) + icon_gross("i16", "🧺", 0, 600, 260, GRUEN, True)
  + chip("c16a", "Aktien", GRUEN, 900, 50) + chip("c16b", "Gold", GOLD, 990, 50) + chip("c16c", "Tagesgeld", GRUEN, 1080, 50),
  lambda a, d: f'pop("#t16", {a}); pop("#i16", {cap("s16", 1)}); pop("#c16a", {cap("s16", 2)}); pop("#c16b", {cap("s16", 2)} + 0.25); pop("#c16c", {cap("s16", 2)} + 0.5);',
  [(st("s16"), "nv-pling-idee")])

S("s17", "wallstreet", titel_zeile("t17", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t17", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
  [(st("s17"), "zeitung")])

K.SZ.append((0.0, K.dauer, news_kopf("16.11.2026"), lambda a, d: "", 8))
K.SZ.append(laufband_szene([("GOLD ▼ ≈ 3.890 $", ROT), ("−31 % SEIT JANUAR", ROT), ("BTC ▼ ≈ 65.000 $", ROT), ("NACHTS KURZ 62.000 $", ROT),
                            ("ETF-ABFLÜSSE ≈ 1,3 MRD. $", ROT), ("FED-ZINSEN? 9.12.", GELB)], K.dauer))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
