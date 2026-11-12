#!/usr/bin/env python3
"""DEMO (ohne Stimme, 30 s): neues News-Format – Nachrichten-Kopf, Überschrift pro Szene, ~2,5-s-Wechsel, große Symbole,
Original-Logos mit Symbol + Kurs-Schild, große freie Fotos, Börsen-Laufband."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, NEWS_JS, OR, ROT, foto_gross, hand, icon_gross, kalender, kit_assets, kreis,  # noqa: E402
                         laufband_szene, linie, marke, news_kopf, person, stempel, titel_zeile, zettel)
from glow_short import build, chip, t  # noqa: E402
from musik import beat  # noqa: E402

kit_assets(HERE, ["nvidia", "amd"])
(HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)
for f in ("jensen-huang.jpg", "colette-kress.jpg"):
    shutil.copy(W / "brand/fotos" / f, HERE / "assets/fotos" / f)
NV = "#76b900"
D = 2.5
SZ, SFX = [], []


def text(id_, s):
    return t(id_, s, 1330, 72).replace('style="top:', 'style="z-index:6;top:', 1)


def szene(i, html, js, sfx=()):
    a = round(i * D, 2)
    SZ.append((a, round(a + D, 2), html, js))
    SFX.extend((a + dt, s) for dt, s in sfx)


szene(0, KIT_CSS + titel_zeile("t0", "⚡ Eilmeldung", farbe=ROT) + foto_gross("f0", "assets/fotos/jensen-huang.jpg", 290, 590, 500, 560, "Foto: Peter Dasilva · CC BY 4.0", NV)
      + stempel("s0", "RAUS!", 420, 960, ROT, 110, -10) + text("x0", "Jensen Huang ist raus"),
      lambda a, d: KIT_JS + " " + NEWS_JS + f' pop("#t0", {a}); pop("#f0", {a} + 0.15); flash({a} + 0.15, 0.6); stempeln("#s0", {a} + 0.9); pop("#x0", {a} + 0.3);',
      [(0, "eilmeldung"), (0.15, "kamera-blitz"), (0.9, "stempel")])
szene(1, titel_zeile("t1", "33 Jahre Chef") + marke("m1", "nvidia", 0, 610, 130, wortmarke="nvidia", mitte=True)
      + kalender("k1a", "START", "1993", 150, 830, 240, NV) + kalender("k1b", "ENDE", "2026", 690, 830, 240, ROT) + text("x1", "seit der Gründung 1993"),
      lambda a, d: f'pop("#t1", {a}); pop("#m1", {a} + 0.2); pop("#k1a", {a} + 0.6); pop("#k1b", {a} + 1.0); pop("#x1", {a} + 0.3);',
      [(0, "whoosh-schnell"), (1.0, "pop")])
szene(2, titel_zeile("t2", "Rücktritt – sofort") + icon_gross("i2", "🚪", 0, 640, 320, ROT, True) + text("x2", "mit sofortiger Wirkung"),
      lambda a, d: f'pop("#t2", {a}); tl.fromTo("#i2", {{ scale: 0.4, rotation: -10 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2)" }}, {a} + 0.3); shake("#i2", {a} + 0.7); pop("#x2", {a} + 0.3);',
      [(0, "whoosh-weich"), (0.7, "tuer-zu")])
szene(3, titel_zeile("t3", "Neue Chefin (Interim)") + icon_gross("i3", "🤝", 120, 640, 170) + foto_gross("f3", "assets/fotos/colette-kress.jpg", 420, 600, 460, 520, "Foto: SiliconANGLE theCUBE · CC BY 3.0", "#4d8ff0")
      + text("x3", "Colette Kress übernimmt"),
      lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.2); pop("#f3", {a} + 0.4); pop("#x3", {a} + 0.3);', [(0, "swipe"), (0.2, "handschlag"), (0.4, "kamera-blitz")])
szene(4, titel_zeile("t4", "Zum 1. Mal: Vorsitzender", gr=52) + person("p4", "Harvey Jones", "Ex-Chef Synopsys", 330, 610, 420, GELB) + text("x4", "Jones leitet den Rat"),
      lambda a, d: f'pop("#t4", {a}); pop("#p4", {a} + 0.3); pop("#x4", {a} + 0.3);', [(0, "whoosh-schnell"), (0.3, "koffer-klick")])
szene(5, titel_zeile("t5", "Aktie vorbörslich") + marke("m5", "nvidia", 0, 700, 150, wortmarke="nvidia", mitte=True) + t("n5", "−13 %", 900, 220, "glow-r")
      + text("x5", "Absturz vor Börsenstart"),
      lambda a, d: f'pop("#t5", {a}); pop("#m5", {a} + 0.2); slam("#n5", {a} + 0.7); shake("#m5", {a} + 0.7); pop("#x5", {a} + 0.3);', [(0, "whoosh-weich"), (0.7, "crash-bass")])
KURS = linie("ku", [0.6, 0.8, 0.97, 0.88, 0.74, 0.6, 0.42, 0.2, 0.06], 150, 700, 780, 400, ROT, punkte=[(2, "239 $"), (8, "< 155 $")]).replace("", "")
szene(6, titel_zeile("t6", "Seit Oktober: −37 %") + KURS + kreis("ku-k", 880, 1080, 120, 80, GELB, 6) + text("x6", "über 1/3 weniger wert"),
      lambda a, d: f'pop("#t6", {a}); draw("#ku-p", {a} + 0.2, 1.2); pop("#ku-w0", {a} + 0.6); pop("#ku-w1", {a} + 1.4); draw("#ku-k-p", {a} + 1.6, 0.4); pop("#x6", {a} + 0.3);',
      [(0, "ticker-rauschen"), (0.2, "kurve-runter")])
BAL = (f'<div id="b7a" style="position:absolute;left:220px;top:{1150 - 480}px;width:240px;height:480px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{NV},{NV}88);transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b7b" style="position:absolute;left:620px;top:{1150 - 240}px;width:240px;height:240px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);transform-origin:50% 100%;z-index:3"></div>'
       f'<div class="mono" style="position:absolute;left:140px;width:400px;top:610px;text-align:center;font-size:56px;color:{NV};z-index:5">400 $</div>'
       f'<div class="mono" style="position:absolute;left:540px;width:400px;top:850px;text-align:center;font-size:56px;color:{ROT};z-index:5">200 $</div>')
szene(7, titel_zeile("t7", "Kursziel halbiert") + BAL + stempel("s7", "BERNSTEIN", 560, 640, OR, 50, 8) + text("x7", "Analysten werden skeptisch"),
      lambda a, d: (f'pop("#t7", {a}); tl.fromTo("#b7a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4 }}, {a} + 0.2); tl.fromTo("#b7b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4 }}, {a} + 0.7);'
                    f' stempeln("#s7", {a} + 1.2); pop("#x7", {a} + 0.3);'), [(0, "zeitung"), (1.2, "hammer")])
szene(8, titel_zeile("t8", "Die Gewinner") + marke("m8a", "-", 0, 640, 120, wortmarke="amd", schild="▲", mitte=True) + marke("m8b", "broadcom", 0, 860, 120, text="BROADCOM", schild="▲", mitte=True)
      + text("x8", "Konkurrenz legt zu"),
      lambda a, d: f'pop("#t8", {a}); pop("#m8a", {a} + 0.2); pop("#m8b", {a} + 0.6); pop("#x8", {a} + 0.3);', [(0, "swipe"), (0.2, "kurve-hoch"), (0.6, "pop")])
szene(9, titel_zeile("t9", "Trump: Tim Cook?!") + icon_gross("i9", "📱", 0, 600, 200, mitte=True)
      + zettel("z9", "„Eine Legende ersetzt eine Legende!“", 180, 860, 720, 54, GELB, -3) + text("x9", "Trump will Tim Cook"),
      lambda a, d: f'pop("#t9", {a}); pop("#i9", {a} + 0.2); tl.fromTo("#z9", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {a} + 0.6); pop("#x9", {a} + 0.3);',
      [(0, "handy-benachrichtigung"), (0.6, "nv-staunen-wow")])
szene(10, titel_zeile("t10", "Zahlen am 17.11.") + icon_gross("i10", "🔔", 140, 640, 260, GELB) + kalender("k10", "NOV", "17", 600, 640, 300, ROT) + text("x10", "der erste große Test"),
      lambda a, d: f'pop("#t10", {a}); tl.fromTo("#i10", {{ rotation: -20 }}, {{ rotation: 20, duration: 0.15, yoyo: true, repeat: 5 }}, {a} + 0.2); pop("#k10", {a} + 0.5); pop("#x10", {a} + 0.3);',
      [(0, "whoosh-weich"), (0.2, "boersenglocke")])
szene(11, titel_zeile("t11", "Nvidia ohne Jensen") + icon_gross("i11", "👎", 0, 620, 280, ROT, True) + stempel("s11", "UNDENKBAR?", 280, 980, OR, 70, -6)
      + text("x11", "vor 1 Woche undenkbar"),
      lambda a, d: f'pop("#t11", {a}); slam("#i11", {a} + 0.2); stempeln("#s11", {a} + 0.9); pop("#x11", {a} + 0.3);', [(0, "whoosh-schnell"), (0.9, "nv-tusch")])

SZ.append((0.0, 30.0, news_kopf("12.11.2026"), lambda a, d: "", 8))
SZ.append(laufband_szene([("NVIDIA ▼ −13 %", ROT), ("HUANG TRITT ZURÜCK", None), ("AMD ▲", GRUEN), ("BROADCOM ▲", GRUEN), ("KURSZIEL 400 → 200 $", ROT), ("DAX ▲ 27.000", GRUEN)], 30.0))

if __name__ == "__main__":
    build(HERE, SZ, SFX, dauer=30.0, musik=beat(30.0) * 0.35)
