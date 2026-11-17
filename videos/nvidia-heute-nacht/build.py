#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (News v2, ~68 s): Nvidia-Zahlen heute 22:20 nach Tech-Ausverkauf → verweist auf longform-huang-raus.
Neue Regeln 16.11.: vorne nur Kommentar-CTA, Folgen-CTA (Beagle-Logo) in der Mitte, wenige Sounds (mm-*), Laufband (Börsen-Eilmeldung)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, foto_gross, icon_gross, kalender, laufband_szene, linie,  # noqa: E402
                         news_kopf, quelle, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, logo, tz  # noqa: E402

NV = "#76b900"
K = Kit(HERE, 17, ["wallstreet", "handelssaal", "frei-code-monitor", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-euro", "frei-sitzung", "frei-miami-nacht"],
        logos=["nvidia.svg", "nasdaq.svg", "flagge-suedkorea.png"], fotos=["jensen-huang.jpg"])
cap, st = K.cap, K.st
S = K.szene

UHR = (f'<div id="u1" class="mono" style="position:absolute;left:240px;top:880px;width:600px;padding:20px;border-radius:26px;background:#000c;border:6px solid {NV};'
       f'box-shadow:0 0 60px {NV}88;text-align:center;font-size:120px;color:{NV};text-shadow:0 0 30px {NV};z-index:4">22:20</div>')
S("s1", "wallstreet", KIT_CSS + titel_zeile("t1", "⚡ Heute Nacht", farbe=ROT) + logo("l1", "nvidia.svg", 600, 600, glow=NV, pad=30) + UHR,
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1", {a}); slam("#u1", {cap("s1", 1)});', [(0.0, "mm-bumm")])

S("s2", "handelssaal", titel_zeile("t2", "Die Zahlen kommen") + logo("l2", "nvidia.svg", 620, 560, glow=NV, pad=26) + chip("c2", "wichtigster Chip-Konzern der Welt", NV, 900, 48),
  lambda a, d: f'pop("#t2", {a}); pop("#l2", {cap("s2", 1)}); slam("#c2", {cap("s2", 3)});', [])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Deine Meinung") + icon_gross("i3", "💬", 0, 580, 220, OR, True)
  + chip("c3a", "📈 steigt morgen", GRUEN, 860, 56) + chip("c3b", "📉 fällt morgen", ROT, 980, 56),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.1); pop("#c3a", {cap("s3", 2)}); pop("#c3b", {cap("s3", 2)} + 0.4);', [(st("s3"), "mm-wusch")])

S("s4", "handelssaal", titel_zeile("t4", "Gestern", farbe=ROT) + icon_gross("i4", "💥", 0, 600, 300, ROT, True),
  lambda a, d: f'pop("#t4", {a}); slam("#i4", {cap("s4", 1)}); shake("#i4", {cap("s4", 1)} + 0.2);', [(cap("s4", 1), "crash-bass")])

S("s5", "wallstreet", titel_zeile("t5", "Tech weltweit") + logo("l5a", "nasdaq.svg", 600, 380, x=80, glow="#0996c7", pad=22)
  + logo("l5b", "flagge-suedkorea.png", 600, 380, x=620, glow="#cd2e3a", pad=0)
  + tz("n5a", "−2,7 %", 900, 90, "glow-r").replace('style="z-index:5;', 'style="z-index:5;left:40px;width:460px;') + tz("n5b", "−3,6 %", 900, 90, "glow-r").replace('style="z-index:5;', 'style="z-index:5;left:580px;width:460px;'),
  lambda a, d: f'pop("#t5", {a}); pop("#l5a", {cap("s5", 0)}); pop("#n5a", {cap("s5", 2)}); pop("#l5b", {cap("s5", 3)}); pop("#n5b", {cap("s5", 3)} + 0.3);', [])

S("s6", "frei-code-monitor", titel_zeile("t6", "SK Hynix") + icon_gross("i6", "💾", 0, 580, 240, ROT, True) + tz("n6", "−7,9 %", 880, 170, "glow-r"),
  lambda a, d: f'pop("#t6", {a}); pop("#i6", {a} + 0.1); slam("#n6", {cap("s6", 1)});', [])

S("s7", "frei-sitzung", titel_zeile("t7", "Die große Frage", farbe=GELB) + icon_gross("i7", "🤖", 0, 600, 260, GELB, True) + chip("c7", "Läuft das KI-Geschäft noch?", GELB, 920, 56),
  lambda a, d: f'pop("#t7", {a}); pop("#i7", {a} + 0.1); slam("#c7", {cap("s7", 1)});', [])

S("s8", "frei-frankfurt-staedel", titel_zeile("t8", "Folg uns") + folg_logo("fl8", 600, 360) + chip("c8", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t8", {a}); {folg_js("fl8", a)} slam("#c8", {cap("s8", 0)} + 0.4);', [(st("s8"), "mm-wusch")])

S("s9", "handelssaal", titel_zeile("t9", "Die Erwartung") + tz("n9", "≈ 109 Mrd. $", 640, 150, "glow-g") + chip("c9", "Umsatz in 3 Monaten", GRUEN, 880, 56),
  lambda a, d: f'pop("#t9", {a}); slam("#n9", {cap("s9", 1)}); pop("#c9", {cap("s9", 2)});', [(cap("s9", 1), "mm-tippen")])

S("s10", "wallstreet", titel_zeile("t10", "Vor einem Jahr") + balken2("b10", "≈ 57 Mrd. $", "≈ 109 Mrd. $", 57, 109, GRAU, NV, basis=1150, hmax=460, unten=("2025", "Erwartung")),
  lambda a, d: f'pop("#t10", {a});' + balken2_js("b10", st("s10") + 0.1, cap("s10", 1)), [])

S("s11", "frei-euro", titel_zeile("t11", "Serie") + tz("n11", "16×", 600, 260, "glow-g") + chip("c11", "Erwartungen geschlagen", GRUEN, 940, 58),
  lambda a, d: f'pop("#t11", {a}); slam("#n11", {cap("s11", 0)} + 0.2); pop("#c11", {cap("s11", 2)});', [])

S("s12", "frei-sitzung", titel_zeile("t12", "Diesmal anders") + foto_gross("f12", "assets/fotos/jensen-huang.jpg", 290, 580, 500, 560)
  + stempel("s12x", "ZURÜCKGETRETEN", 200, 1060, ROT, 56, -5),
  lambda a, d: f'pop("#t12", {a}); pop("#f12", {cap("s12", 2)}); stempeln("#s12x", {cap("s12", 3)});', [(cap("s12", 2), "mm-kamera")])

K13 = linie("ku13", [0.95, 0.85, 0.7, 0.75, 0.55, 0.45, 0.35], 220, 640, 700, 420, ROT, punkte=[(0, "Rekord 6.10."), (6, "−32 %")])
S("s13", "handelssaal", titel_zeile("t13", "Nvidia-Aktie") + K13,
  lambda a, d: f'pop("#t13", {a}); pop("#ku13-w0", {a} + 0.1); draw("#ku13-p", {a} + 0.2, 1.4); tl.fromTo("#ku13-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 0.9); pop("#ku13-w1", {cap("s13", 1)});',
  [(cap("s13", 1), "mm-bumm")])

S("s14", "frei-frankfurt-nacht", titel_zeile("t14", "Und du?") + icon_gross("i14", "🧺", 0, 580, 240, OR, True) + chip("c14", "Nvidia = Schwergewicht im Welt-ETF", OR, 900, 46),
  lambda a, d: f'pop("#t14", {a}); pop("#i14", {cap("s14", 1)}); slam("#c14", {cap("s14", 2)});', [])

S("s15", "frei-euro", titel_zeile("t15", "Dein Sparplan") + icon_gross("i15", "🎢", 0, 600, 280, OR, True),
  lambda a, d: f'pop("#t15", {a}); pop("#i15", {a} + 0.1); shake("#i15", {cap("s15", 1)});', [])

S("s16", "wallstreet", titel_zeile("t16", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t16", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});', [])

MK = (titel_zeile("mk-t", "Ganzes Video") + f'<div id="mk-b" style="position:absolute;left:371px;top:690px;width:338px;height:600px;border-radius:30px;overflow:hidden;'
      f'border:8px solid {OR};box-shadow:0 0 80px {OR}88;z-index:3"><img src="assets/lf.jpg" style="width:100%;height:100%;object-fit:cover" alt=""/></div>'
      + chip("mk-c", "Jetzt auf unserem Kanal", OR, 580, 50))
S("s17", None, MK,
  lambda a, d: (f'pop("#mk-t", {a}); tl.fromTo("#mk-b", {{ scale: 0.6, rotation: -6, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {a} + 0.2);'
                f' pop("#mk-c", {a} + 0.6);'),
  [(st("s17"), "mm-wusch")])

K.SZ.append((0.0, st("s17"), news_kopf("17.11.2026"), lambda a, d: "", 8))
K.SZ.append(laufband_szene([("NVDA ▼ ≈ −32 % VOM REKORD", ROT), ("NASDAQ 100 ▼ −2,7 %", ROT), ("KOSPI ▼ −3,6 %", ROT), ("SK HYNIX ▼ −7,9 %", ROT),
                            ("NVIDIA-ZAHLEN 22:20 UHR", GELB), ("ERWARTUNG ≈ 109 MRD. $", GELB)], st("s17")))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
