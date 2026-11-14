#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (News v2, 71 s): Bitcoin stürzt am Wochenende weiter (≈65.000 $). Laufband. Endkarte → Longform Binance-Raub.
Freie Hintergründe (CC0/gemeinfrei), keine Quellen im Bild, keine Kapitel."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, hintergrund_foto, icon_gross, kalender, kasten, kit_assets,  # noqa: E402
                         kit_hg, laufband_szene, linie, marke, news_kopf, quelle, stempel, titel_zeile, vergleich, wechsel_js, zettel, zoom_js)
from glow_short import build, chip, partikel, t, zeiten  # noqa: E402
from motor import endkarte  # noqa: E402

BTC = "#f7931a"
kit_assets(HERE, ["bitcoin", "flagge-usa"])
shutil.copy(W / "renders/thumbnails/longform-binance-raub-tiktok.jpg", HERE / "assets/lf.jpg")
cap, st, en, DAUER = zeiten(HERE)
kit_hg(HERE, ["frei-code-monitor", "wallstreet", "handelssaal", "frei-euro", "frei-50euro", "frei-frankfurt-nacht"])
SZ, SFX = [], []
REIHE = [f"s{i}" for i in range(1, 15)]


def szene(sid, hg, html, js, sfx=()):
    i = len(SZ)
    a = st(sid)
    b = st(REIHE[REIHE.index(sid) + 1]) if sid != REIHE[-1] else DAUER
    SZ.append((a, b, (hintergrund_foto(f"bg{i}", hg) if hg else "") + html,
               lambda a_, d_, j=js, k=i, h=hg: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + (zoom_js(f"#bg{k}", a_, d_, 1.12) if h else "")))
    SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


KURS = linie("ku", [0.75, 0.68, 0.72, 0.5, 0.42, 0.3, 0.18, 0.06], 150, 820, 780, 300, ROT, punkte=[(0, "76.000 $"), (7, "≈ 65.000 $")])
szene("s1", "frei-code-monitor", KIT_CSS + titel_zeile("t1", "⚡ Wochenend-Crash", farbe=ROT) + marke("m1", "bitcoin", 0, 600, 140, text="BITCOIN", schild="▼", mitte=True) + KURS,
      lambda a, d: (KIT_JS + f' pop("#t1", {a}); pop("#m1", {a}); pop("#ku-w0", {a} + 0.2); draw("#ku-p", {a} + 0.2, 1.8); tl.fromTo("#ku-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 1.5);'
                    f' pop("#ku-w1", {cap("s1", 2)}); shake("#m1", {cap("s1", 2)});'),
      [(0.0, "eilmeldung"), (0.2, "kurve-runter"), (cap("s1", 2), "crash-bass")])

szene("s2", "frei-frankfurt-nacht", titel_zeile("t2", "Deine Meinung") + icon_gross("i2", "💬", 0, 600, 240, OR, True)
      + chip("c2a", "🛒 nachkaufen", GRUEN, 900, 56) + chip("c2b", "⏳ warten", OR, 1020, 56),
      lambda a, d: f'pop("#t2", {a}); pop("#i2", {a} + 0.1); pop("#c2a", {cap("s2", 1)}); pop("#c2b", {cap("s2", 2)});',
      [(st("s2"), "handy-benachrichtigung"), (cap("s2", 1), "pop"), (cap("s2", 2), "pop")])

szene("s3", "wallstreet", titel_zeile("t3", "Eine Woche") + kalender("k3", "7 TAGE", "BTC", 390, 610, 300, BTC) + tz("n3", "≈ −14 %", 980, 150, "glow-r"),
      lambda a, d: f'pop("#t3", {a}); pop("#k3", {a} + 0.1); slam("#n3", {cap("s3", 1)}); flash({cap("s3", 1)}, 0.4);',
      [(st("s3"), "swipe"), (cap("s3", 1), "bass-schlag")])

BASIS = 1150
BAL = (f'<div id="b4a" style="position:absolute;left:220px;top:{BASIS - 460}px;width:240px;height:460px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{BTC},{BTC}88);box-shadow:0 0 40px {BTC}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b4b" style="position:absolute;left:620px;top:{BASIS - 240}px;width:240px;height:240px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);box-shadow:0 0 40px {ROT}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b4ta" class="mono" style="position:absolute;left:140px;width:400px;top:{BASIS - 530}px;text-align:center;font-size:52px;color:{BTC};z-index:5">126.000 $</div>'
       f'<div id="b4tb" class="mono" style="position:absolute;left:540px;width:400px;top:{BASIS - 310}px;text-align:center;font-size:52px;color:{ROT};z-index:5">≈ 65.000 $</div>')
szene("s4", "handelssaal", titel_zeile("t4", "Seit dem Rekord") + BAL + stempel("s4x", "FAST −50 %", 540, 600, ROT, 54, 8) + quelle("q4", "Rekord Okt. 2025 · Stand 14.11.2026", 1170),
      lambda a, d: (f'pop("#t4", {a}); tl.fromTo("#b4a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s4", 0)}); pop("#b4ta", {cap("s4", 1)});'
                    f' tl.fromTo("#b4b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s4", 2)}); pop("#b4tb", {cap("s4", 2)} + 0.4); stempeln("#s4x", {cap("s4", 2)} + 0.8); pop("#q4", {cap("s4", 2)} + 1.0);'),
      [(st("s4"), "whoosh-weich"), (cap("s4", 2), "kurve-runter"), (cap("s4", 2) + 0.8, "stempel")])

LINIE = linie("l5", [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.62], 150, 700, 780, 300, GELB, punkte=[(3, "200-Wochen-Linie")])
KURS5 = linie("k5", [0.95, 0.9, 0.85, 0.8, 0.72, 0.62, 0.45, 0.28], 150, 700, 780, 300, BTC, punkte=[(0, "Bitcoin")])
szene("s5", "frei-code-monitor", titel_zeile("t5", "Wichtige Linie gerissen") + LINIE + KURS5 + stempel("s5x", "DURCHBROCHEN", 270, 1050, ROT, 60, -5),
      lambda a, d: (f'pop("#t5", {a}); draw("#l5-p", {cap("s5", 1)}, 1.2); pop("#l5-w0", {cap("s5", 3)}); draw("#k5-p", {a} + 0.2, 1.6); pop("#k5-w0", {cap("s5", 2)});'
                    f' stempeln("#s5x", {cap("s5", 3)} + 0.6);'),
      [(st("s5"), "spannung"), (cap("s5", 3) + 0.6, "glas-bricht")])

szene("s6", "wallstreet", titel_zeile("t6", "Grund 1: Zinsen", farbe=OR) + icon_gross("i6", "🏦", 140, 620, 240, OR) + icon_gross("i6b", "📈", 620, 620, 240, ROT)
      + chip("c6", "Notenbanker wollen höhere Zinsen", OR, 980, 44),
      lambda a, d: f'slam("#t6", {a}); pop("#i6", {cap("s6", 2)}); pop("#i6b", {cap("s6", 3)}); slam("#c6", {cap("s6", 3)} + 0.3);',
      [(st("s6"), "nv-boom-kurz"), (cap("s6", 3), "kurve-hoch")])

WP = (f'<div id="wp" style="position:absolute;left:140px;top:900px;width:800px;height:16px;border-radius:8px;background:#fff;box-shadow:0 0 30px #fff8;transform-origin:50% 50%;z-index:3"></div>'
      f'<div style="position:absolute;left:500px;top:916px;width:0;height:0;border-left:40px solid transparent;border-right:40px solid transparent;border-bottom:80px solid {GRAU};z-index:2"></div>')
szene("s7", "frei-euro", titel_zeile("t7", "Die Wippe") + WP + kasten("w7a", "sichere Anlagen<br/>+ Zinsen", 150, 700, 340, 180, GRUEN, 42)
      + marke("w7b", "bitcoin", 640, 740, 110, text="BTC"),
      lambda a, d: (f'pop("#t7", {a}); pop("#wp", {a}); pop("#w7a", {cap("s7", 1)}); pop("#w7b", {cap("s7", 2)});'
                    f' tl.fromTo("#wp", {{ rotation: 0 }}, {{ rotation: 8, duration: 0.6, ease: "back.out(2)" }}, {cap("s7", 3)});'
                    f' tl.fromTo("#w7a", {{ y: 0 }}, {{ y: 40, duration: 0.6, ease: "back.out(2)" }}, {cap("s7", 3)}); tl.fromTo("#w7b", {{ y: 0 }}, {{ y: -60, duration: 0.6, ease: "back.out(2)" }}, {cap("s7", 3)});'),
      [(st("s7"), "swipe"), (cap("s7", 3), "whoosh-schnell")])

ROHR = (f'<div id="r8" style="position:absolute;left:160px;top:860px;width:760px;height:100px;border-radius:50px;background:#1b1f22;border:5px solid {BTC};z-index:2"></div>'
        + "".join(f'<div class="dl" style="position:absolute;left:{200 + k * 90}px;top:885px;width:50px;height:50px;border-radius:50%;background:{BTC};box-shadow:0 0 16px {BTC};z-index:3"></div>' for k in range(8)))
szene("s8", "handelssaal", titel_zeile("t8", "Grund 2: Geld fließt ab", farbe=OR) + icon_gross("i8", "🇺🇸", 0, 600, 180, OR, True) + ROHR
      + tz("n8", "≈ −1,9 Mrd. $", 1000, 110, "glow-r") + quelle("q8", "Bitcoin-Fonds in den USA · seit über 1 Woche täglich", 1150),
      lambda a, d: (f'slam("#t8", {a}); pop("#i8", {cap("s8", 2)}); pop("#r8", {cap("s8", 2)} + 0.2);'
                    f' tl.fromTo(".dl", {{ x: 0, opacity: 1 }}, {{ x: 140, opacity: 0, duration: 0.6, stagger: 0.08, repeat: 3, ease: "power1.in" }}, {cap("s8", 3)});'
                    f' slam("#n8", {cap("s8", 4)}); pop("#q8", {cap("s8", 5)});'),
      [(st("s8"), "nv-boom-kurz"), (cap("s8", 3), "nv-sog"), (cap("s8", 4), "kasse")])

szene("s9", "frei-50euro", titel_zeile("t9", "Grund 3: Kredit-Wetten", farbe=OR) + icon_gross("i9", "🎰", 0, 640, 260, OR, True),
      lambda a, d: f'slam("#t9", {a}); pop("#i9", {cap("s9", 1)});',
      [(st("s9"), "nv-boom-kurz"), (cap("s9", 1), "muenzen-klimpern")])

szene("s10", "handelssaal", titel_zeile("t10", "In 24 Stunden") + tz("n10", "≈ 1,5 Mrd. $", 680, 140, "glow-r") + partikel("pa10", 540, 770, 28, (ROT, BTC, "#fff"), 560)
      + stempel("s10x", "ZWANGSWEISE AUFGELÖST", 190, 980, ROT, 42, -4),
      lambda a, d: f'pop("#t10", {a}); slam("#n10", {cap("s10", 2)}); burst("#pa10", {cap("s10", 2)} + 0.2); stempeln("#s10x", {cap("s10", 3)});',
      [(st("s10"), "whoosh-weich"), (cap("s10", 2), "glas-bricht"), (cap("s10", 3), "stempel")])

szene("s11", "wallstreet", titel_zeile("t11", "Die Wette") + kalender("k11", "BIS", "1.1.", 120, 620, 260, OR) + tz("n11", "23 %", 640, 170, "glow-o").replace("z-index:5;top", "z-index:5;left:220px;top")
      + chip("c11", "Chance auf unter 55.000 $", ROT, 990, 54),
      lambda a, d: f'pop("#t11", {a}); pop("#k11", {cap("s11", 2)}); pop("#c11", {cap("s11", 3)}); slam("#n11", {cap("s11", 4)});',
      [(st("s11"), "spannung"), (cap("s11", 4), "bass-schlag")])

szene("s12", "frei-frankfurt-nacht", titel_zeile("t12", "Und jetzt?", farbe=GELB)
      + vergleich("v12", "NICHT", "in Panik<br/>verkaufen", "ABER AUCH NICHT", "blind<br/>nachkaufen", ROT, ROT, 640, 300),
      lambda a, d: f'pop("#t12", {a}); pop("#v12-l", {cap("s12", 1)}); pop("#v12-r", {cap("s12", 3)});',
      [(st("s12"), "whoosh-weich"), (cap("s12", 1), "falsch"), (cap("s12", 3), "falsch")])

szene("s13", "wallstreet", titel_zeile("t13", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
      lambda a, d: f'pop("#t13", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
      [(st("s13"), "zeitung")])

mk_html, mk_js = endkarte("assets/lf.jpg", "Ganzes Video")
szene("s14", None, mk_html, mk_js, [(st("s14"), "whoosh-weich"), (st("s14") + 0.6, "pop")])

SZ.append((0.0, st("s14"), news_kopf("14.11.2026"), lambda a, d: "", 8))
SZ.append(laufband_szene([("BTC ▼ ≈ −14 % WOCHE", ROT), ("≈ 65.000 $", ROT), ("UNTER 200-WOCHEN-LINIE", ROT), ("1,5 MRD. $ LIQUIDIERT", ROT),
                          ("ETF-ABFLÜSSE ≈ 1,9 MRD. $", ROT), ("−47 % VOM REKORD", GELB)], DAUER))

if __name__ == "__main__":
    build(HERE, SZ, SFX)
    print(bildquellen(HERE))
