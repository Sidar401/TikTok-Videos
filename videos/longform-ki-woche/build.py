#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News v2): Die Woche der Wahrheit für die KI-Börse (Tech-Ausverkauf 16.11., Nvidia-Zahlen 17.11. 22:20, Anthropic-IPO Do 19.11.).
Leitmotiv: Wochen-Kalender Mo/Di/Do mit Ampel. Regeln 16./17.11.: 1 CTA vorne (Teilen), Folgen in der Mitte (Beagle), wenige Sounds (mm-*), Laufband."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, foto_gross, icon_gross, laufband_szene, linie, news_kopf,  # noqa: E402
                         stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, logo, tz  # noqa: E402

NV, AN = "#76b900", "#d97757"
K = Kit(HERE, 33, ["wallstreet", "handelssaal", "frei-code-monitor", "frei-code-css", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-euro", "frei-sitzung", "frei-miami-nacht"],
        logos=["nvidia.svg", "nasdaq.svg", "flagge-suedkorea.png", "anthropic.svg", "claude.svg", "microsoft.svg", "amazon.svg", "google.svg"], fotos=["colette-kress.jpg", "jensen-huang.jpg"])
cap, st = K.cap, K.st
S = K.szene


def woche(id_, aktiv, y=600):
    """Leitmotiv: drei Tages-Karten MO / DI / DO; aktiv = Index, der leuchtet."""
    tage = [("MO", "Tech-Absturz", ROT), ("DI", "Nvidia-Zahlen", NV), ("DO", "Anthropic", AN)]
    h = ""
    for i, (tg, txt, f) in enumerate(tage):
        an = i in aktiv
        h += (f'<div id="{id_}{i}" style="position:absolute;left:{70 + i * 320}px;top:{y}px;width:300px;height:300px;border-radius:28px;background:{"#14181bee" if an else "#14181b88"};'
              f'border:6px solid {f if an else "#ffffff33"};box-shadow:{f"0 0 60px {f}77" if an else "none"};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;z-index:4">'
              f'<div style="font-weight:900;font-size:110px;color:{f if an else "#ffffff55"}">{tg}</div>'
              f'<div class="mono" style="font-size:30px;color:{"#fff" if an else "#ffffff55"}">{txt}</div></div>')
    return h


def woche_js(id_, a):
    return "".join(f' pop("#{id_}{i}", {a} + {0.25 * i});' for i in range(3))


S("s1", "handelssaal", KIT_CSS + titel_zeile("t1", "⚡ Woche der Wahrheit", farbe=ROT) + woche("w1", (0, 1, 2)) + chip("c1", "Boom oder Blase?", ROT, 980, 64),
  lambda a, d: KIT_JS + woche_js("w1", a) + f' pop("#t1", {a}); slam("#c1", {cap("s1", 2)});', [(0.0, "mm-bumm")])

S("s2", "wallstreet", titel_zeile("t2", "Diese Woche") + woche("w2", (0, 1, 2)) + chip("c2", "3 Termine – alles KI", OR, 980, 56),
  lambda a, d: woche_js("w2", a) + f' pop("#t2", {a}); pop("#c2", {cap("s2", 3)});', [])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Teil das Video") + icon_gross("i3", "📲", 0, 600, 280, OR, True) + chip("c3", "mit deinen Freunden", OR, 950, 56),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a}); slam("#c3", {cap("s3", 1)});', [(st("s3"), "mm-wusch")])

S("s4", "handelssaal", titel_zeile("t4", "Montag") + woche("w4", (0,)),
  lambda a, d: woche_js("w4", a) + f' pop("#t4", {a});', [])

S("s5", "wallstreet", titel_zeile("t5", "Tech weltweit", farbe=ROT) + logo("l5a", "nasdaq.svg", 600, 380, x=80, glow="#0996c7", pad=22)
  + logo("l5b", "flagge-suedkorea.png", 600, 380, x=620, glow="#cd2e3a", pad=0)
  + tz("n5a", "−2,7 %", 900, 90, "glow-r").replace('style="z-index:5;', 'style="z-index:5;left:40px;width:460px;')
  + tz("n5b", "−3,6 %", 900, 90, "glow-r").replace('style="z-index:5;', 'style="z-index:5;left:580px;width:460px;'),
  lambda a, d: f'pop("#t5", {a}); pop("#l5a", {cap("s5", 0)}); pop("#n5a", {cap("s5", 1)}); pop("#l5b", {cap("s5", 2)}); pop("#n5b", {cap("s5", 3)});', [(cap("s5", 1), "crash-bass")])

S("s6", "frei-code-monitor", titel_zeile("t6", "SK Hynix") + icon_gross("i6", "💾", 0, 580, 240, ROT, True) + tz("n6", "−7,9 %", 880, 170, "glow-r"),
  lambda a, d: f'pop("#t6", {a}); pop("#i6", {a} + 0.1); slam("#n6", {cap("s6", 1)});', [])

S("s7", "frei-sitzung", titel_zeile("t7", "Die Angst") + icon_gross("i7", "🕳️", 0, 600, 260, ROT, True) + chip("c7", "Milliarden in KI – kommen die zurück?", ROT, 920, 44),
  lambda a, d: f'pop("#t7", {a}); pop("#i7", {cap("s7", 1)}); slam("#c7", {cap("s7", 2)});', [])

S("s8", "handelssaal", titel_zeile("t8", "Im Zentrum") + logo("l8", "nvidia.svg", 640, 640, glow=NV, pad=34),
  lambda a, d: f'pop("#t8", {a}); slam("#l8", {cap("s8", 1)});', [(cap("s8", 1), "mm-bumm")])

K9 = linie("ku9", [0.95, 0.85, 0.7, 0.75, 0.55, 0.45, 0.35], 220, 640, 700, 420, ROT, punkte=[(0, "Rekord Okt."), (6, "−32 %")])
S("s9", "wallstreet", titel_zeile("t9", "Nvidia-Aktie") + K9,
  lambda a, d: f'pop("#t9", {a}); pop("#ku9-w0", {a} + 0.1); draw("#ku9-p", {a} + 0.2, 1.4); tl.fromTo("#ku9-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 0.9); pop("#ku9-w1", {cap("s9", 1)});', [])

S("s10", "frei-sitzung", titel_zeile("t10", "Neue Chefin") + foto_gross("f10a", "assets/fotos/jensen-huang.jpg", 80, 600, 420, 480, farbe=GRAU)
  + foto_gross("f10b", "assets/fotos/colette-kress.jpg", 580, 600, 420, 480, farbe=NV) + stempel("s10x", "RÜCKTRITT", 90, 1000, ROT, 48, -6),
  lambda a, d: f'pop("#t10", {a}); pop("#f10a", {cap("s10", 0)}); stempeln("#s10x", {cap("s10", 1)}); pop("#f10b", {cap("s10", 3)});', [(cap("s10", 3), "mm-kamera")])

UHR = (f'<div id="u11" class="mono" style="position:absolute;left:240px;top:860px;width:600px;padding:20px;border-radius:26px;background:#000c;border:6px solid {NV};'
       f'box-shadow:0 0 60px {NV}88;text-align:center;font-size:120px;color:{NV};text-shadow:0 0 30px {NV};z-index:4">22:20</div>')
S("s11", "handelssaal", titel_zeile("t11", "Dienstag") + woche("w11", (1,), 560) + UHR,
  lambda a, d: woche_js("w11", a) + f' pop("#t11", {a}); slam("#u11", {cap("s11", 1)});', [])

S("s12", "wallstreet", titel_zeile("t12", "Die Erwartung") + balken2("b12", "≈ 57 Mrd. $", "≈ 109 Mrd. $", 57, 109, GRAU, NV, unten=("vor 1 Jahr", "Erwartung · 3 Monate")),
  lambda a, d: f'pop("#t12", {a});' + balken2_js("b12", cap("s12", 2), cap("s12", 1)), [(cap("s12", 1), "mm-tippen")])

S("s13", "frei-euro", titel_zeile("t13", "Serie") + tz("n13", "16×", 600, 260, "glow-g") + chip("c13", "Erwartungen geschlagen", GRUEN, 940, 58),
  lambda a, d: f'pop("#t13", {a}); slam("#n13", {cap("s13", 0)} + 0.2); pop("#c13", {cap("s13", 2)});', [])

S("s14", "frei-code-css", titel_zeile("t14", "Diesmal zählt …", farbe=GELB) + icon_gross("i14", "🔭", 0, 600, 280, GELB, True) + chip("c14", "der Ausblick", GELB, 950, 66),
  lambda a, d: f'pop("#t14", {a}); pop("#i14", {a} + 0.1); slam("#c14", {cap("s14", 1)});', [])

S("s15", "frei-frankfurt-nacht", titel_zeile("t15", "Szenario 1", farbe=GRUEN) + icon_gross("i15", "😮‍💨", 0, 600, 260, GRUEN, True) + chip("c15", "Nachfrage wächst → Börse atmet auf", GRUEN, 940, 46),
  lambda a, d: f'pop("#t15", {a}); pop("#i15", {cap("s15", 1)}); slam("#c15", {cap("s15", 2)});', [])

S("s16", "handelssaal", titel_zeile("t16", "Szenario 2", farbe=ROT) + icon_gross("i16", "📉", 0, 600, 260, ROT, True) + chip("c16", "vorsichtig → Absturz geht weiter", ROT, 940, 46),
  lambda a, d: f'pop("#t16", {a}); pop("#i16", {cap("s16", 1)}); slam("#c16", {cap("s16", 2)});', [])

S("s17", "frei-frankfurt-staedel", titel_zeile("t17", "Folg uns") + folg_logo("fl17", 600, 360) + chip("c17", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t17", {a}); {folg_js("fl17", a)} slam("#c17", {cap("s17", 0)} + 0.4);', [(st("s17"), "mm-wusch")])

S("s18", "frei-code-monitor", titel_zeile("t18", "Donnerstag") + woche("w18", (2,)),
  lambda a, d: woche_js("w18", a) + f' pop("#t18", {a});', [])

S("s19", "frei-code-css", titel_zeile("t19", "Börsengang") + logo("l19", "anthropic.svg", 600, 640, glow=AN, pad=30) + logo("l19b", "claude.svg", 860, 360, glow=AN, pad=22),
  lambda a, d: f'pop("#t19", {a}); pop("#l19", {cap("s19", 0)}); pop("#l19b", {cap("s19", 2)});', [])

S("s20", "wallstreet", titel_zeile("t20", "Rekordverdächtig") + tz("n20", "Top 3", 620, 220, "glow-o") + chip("c20", "größte Börsengänge aller Zeiten", OR, 900, 50),
  lambda a, d: f'pop("#t20", {a}); slam("#n20", {cap("s20", 1)}); pop("#c20", {cap("s20", 2)});', [])

S("s21", "frei-sitzung", titel_zeile("t21", "Der Test", farbe=GELB) + icon_gross("i21", "🧪", 0, 600, 260, GELB, True) + chip("c21", "Wollen Anleger noch KI?", GELB, 920, 58),
  lambda a, d: f'pop("#t21", {a}); pop("#i21", {a} + 0.1); slam("#c21", {cap("s21", 2)});', [])

S("s22", "frei-euro", titel_zeile("t22", "Läuft es gut …") + vergleich("v22", "GUT", "✓ starkes Signal", "SCHLECHT", "⚠ Warnzeichen", GRUEN, ROT, y=620, h=300),
  lambda a, d: f'pop("#t22", {a}); pop("#v22-l", {cap("s22", 1)});', [])

S("s23", "handelssaal", titel_zeile("t23", "… oder schlecht") + vergleich("v23", "GUT", "✓ starkes Signal", "SCHLECHT", "⚠ Warnzeichen", GRUEN, ROT, y=620, h=300),
  lambda a, d: f'pop("#t23", {a}); pop("#v23-l", {a}); pop("#v23-r", {cap("s23", 1)});', [])

S("s24", "frei-frankfurt-nacht", titel_zeile("t24", "Und du?", farbe=GELB) + icon_gross("i24", "🫵", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t24", {a}); slam("#i24", {a} + 0.15);', [])

S("s25", "frei-sitzung", titel_zeile("t25", "Dein Welt-ETF") + icon_gross("i25", "🧺", 0, 580, 240, OR, True) + logo("l25", "nvidia.svg", 880, 440, glow=NV, pad=20),
  lambda a, d: f'pop("#t25", {a}); pop("#i25", {cap("s25", 1)}); pop("#l25", {cap("s25", 2)});', [])

S("s26", "wallstreet", titel_zeile("t26", "Alle setzen auf KI") + logo("l26a", "microsoft.svg", 600, 280, x=60, glow="#fff", pad=20) + logo("l26b", "amazon.svg", 600, 280, x=400, glow="#ff9900", pad=20)
  + logo("l26c", "google.svg", 600, 280, x=740, glow="#4285f4", pad=20) + chip("c26", "Milliarden in KI", OR, 900, 56),
  lambda a, d: f'pop("#t26", {a}); pop("#l26a", {cap("s26", 0)}); pop("#l26b", {cap("s26", 1)}); pop("#l26c", {cap("s26", 1)} + 0.3); slam("#c26", {cap("s26", 2)});', [])

S("s27", "frei-euro", titel_zeile("t27", "Dein Sparplan") + icon_gross("i27", "🎢", 0, 600, 280, OR, True),
  lambda a, d: f'pop("#t27", {a}); pop("#i27", {a} + 0.1); shake("#i27", {cap("s27", 1)});', [])

S("s28", "frei-frankfurt-staedel", titel_zeile("t28", "Was tun?", farbe=GRUEN) + tz("n28", "3", 600, 320, "glow-g") + chip("c28", "Tipps", GRUEN, 960, 60),
  lambda a, d: f'pop("#t28", {a}); slam("#n28", {a} + 0.2); pop("#c28", {a} + 0.5);', [])


def tipp(sid, n, icon, kopf, text, hg, sfx=None):
    S(sid, hg, titel_zeile(f"t{sid}", f"Tipp {n}", farbe=GRUEN) + icon_gross(f"i{sid}", icon, 0, 600, 220, GRUEN, True)
      + (f'<div id="k{sid}" style="position:absolute;left:120px;top:860px;width:840px;padding:30px 38px;border-radius:26px;background:#14181bee;border:5px solid {GRUEN};'
         f'box-shadow:0 0 40px {GRUEN}55;z-index:4"><div class="mono" style="font-size:28px;color:{GRUEN};letter-spacing:2px">{kopf}</div>'
         f'<div style="font-weight:900;font-size:52px;color:#fff;line-height:1.1;margin-top:8px">{text}</div></div>'),
      lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#i{s}", {a} + 0.1); pop("#k{s}", {cap(s, 1)});', [(cap(sid, 1), sfx)] if sfx else [])


tipp("s29", 1, "🧘", "KEINE PANIK", "nicht verkaufen,<br/>nur weil es rot ist", "frei-sitzung")
tipp("s30", 2, "🔍", "DEPOT PRÜFEN", "wie viel KI<br/>steckt wirklich drin?", "frei-code-monitor", "mm-tippen")
tipp("s31", 3, "🛒", "WEITER SPAREN", "fallende Kurse =<br/>günstiger einkaufen", "frei-euro")

S("s32", "frei-frankfurt-nacht", titel_zeile("t32", "Merk dir") + stempel("s32x", "1 WOCHE ≠ 20 JAHRE", 140, 720, OR, 62, -5),
  lambda a, d: f'pop("#t32", {a}); stempeln("#s32x", {cap("s32", 1)});', [(cap("s32", 1), "stempel")])

S("s33", "wallstreet", titel_zeile("t33", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t33", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});', [])

K.SZ.append((0.0, K.dauer, news_kopf("17.11.2026"), lambda a, d: "", 8))
K.SZ.append(laufband_szene([("NASDAQ 100 ▼ −2,7 %", ROT), ("KOSPI ▼ −3,6 %", ROT), ("SK HYNIX ▼ −7,9 %", ROT), ("NVDA ▼ ≈ −32 % VOM REKORD", ROT),
                            ("NVIDIA-ZAHLEN 22:20 UHR", GELB), ("ANTHROPIC-IPO DONNERSTAG", GELB)], K.dauer))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
