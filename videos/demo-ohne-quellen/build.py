#!/usr/bin/env python3
"""DEMO (ohne Stimme, 30 s): News-Format ohne Fotografen-Namen im Bild.
Hintergründe nur CC0/gemeinfrei (keine Namensnennung nötig), Personenfoto ohne Quellenzeile – Quellen stehen in bildquellen.txt (Beschreibung)."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, donut, flagge, foto_gross, hintergrund_foto, icon_gross,  # noqa: E402
                         kalender, kit_assets, kit_hg, news_kopf, quelle, stempel, titel_zeile, wechsel_js, zoom_js)
from glow_short import build, chip, t  # noqa: E402
from musik import beat  # noqa: E402

UC = "#E2001A"
kit_assets(HERE, ["flagge-italien", "flagge-deutschland", "flagge-eu"])
for f in ("commerzbank.png", "unicredit-symbol.png"):
    shutil.copy(W / "brand/logos" / f, HERE / "assets/logos" / f)
(HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)
shutil.copy(W / "brand/fotos/olaf-scholz.jpg", HERE / "assets/fotos/olaf-scholz.jpg")
D = 2.5
HG = ["frei-frankfurt-nacht", "frei-frankfurt-staedel", "handelssaal", "frei-euro", "wallstreet", "frei-50euro",
      "frei-frankfurt-nacht", "handelssaal", "frei-frankfurt-staedel", "frei-euro", "wallstreet", "frei-frankfurt-nacht"]
kit_hg(HERE, set(HG))
SZ, SFX = [], []


def text(id_, s):
    return t(id_, s, 1330, 72).replace('style="top:', 'style="z-index:6;top:', 1)


def logo(id_, datei, y, w):
    return (f'<div id="{id_}" style="position:absolute;left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;padding:24px;border-radius:24px;background:#fff;'
            f'box-shadow:0 0 60px #FFCC0066, 0 30px 50px #000;z-index:4"><img src="assets/logos/{datei}" alt="" style="width:100%;display:block"/></div>')


def szene(i, html, js, sfx=()):
    a = round(i * D, 2)
    SZ.append((a, round(a + D, 2), hintergrund_foto(f"bg{i}", HG[i]) + html,
               (lambda j, k: lambda a, d: j(a, d) + (wechsel_js(f"z{k}", a, k) if k else "") + zoom_js(f"#bg{k}", a, d, 1.12))(js, i)))
    SFX.extend((a + dt, s) for dt, s in sfx)


szene(0, KIT_CSS + titel_zeile("t0", "⚡ Übernahme", farbe=ROT) + logo("l0", "commerzbank.png", 640, 760) + flagge("f0", "flagge-italien", 390, 860, 300, -4)
      + text("x0", "Die Commerzbank wird italienisch"),
      lambda a, d: KIT_JS + f' pop("#t0", {a}); pop("#l0", {a}); pop("#f0", {a} + 0.6); pop("#x0", {a} + 0.2);', [(0, "eilmeldung"), (0.6, "whoosh-schnell")])
szene(1, titel_zeile("t1", "Commerzbank") + icon_gross("i1", "👥", 0, 620, 220, "#FFCC00", True) + t("n1", "≈ 11 Mio.", 880, 150, "glow-o") + text("x1", "Kunden in Deutschland"),
      lambda a, d: f'pop("#t1", {a}); pop("#i1", {a} + 0.2); slam("#n1", {a} + 0.6); pop("#x1", {a} + 0.2);', [(0, "swipe"), (0.6, "zaehler")])
szene(2, titel_zeile("t2", "Finanzkrise") + kalender("k2", "KRISE", "2008", 110, 640, 300, ROT) + icon_gross("i2", "🛟", 620, 640, 260, OR) + text("x2", "Der Staat rettet die Bank"),
      lambda a, d: f'pop("#t2", {a}); pop("#k2", {a} + 0.2); pop("#i2", {a} + 0.6); pop("#x2", {a} + 0.2);', [(0, "alarm")])
szene(3, titel_zeile("t3", "Rettung") + t("n3", "18,2 Mrd. €", 760, 150, "glow-o") + quelle("q3", "Staatshilfen 2008/09", 960) + text("x3", "über 18 Milliarden Euro"),
      lambda a, d: f'pop("#t3", {a}); slam("#n3", {a} + 0.3); pop("#q3", {a} + 0.7); pop("#x3", {a} + 0.2);', [(0, "whoosh-weich"), (0.3, "kasse")])
szene(4, titel_zeile("t4", "Olaf Scholz") + foto_gross("f4", "assets/fotos/olaf-scholz.jpg", 290, 600, 500, 480, "Foto: Raimond Spekking · CC BY-SA 4.0", ROT)
      + text("x4", "„unfreundliche Attacke“"),
      lambda a, d: f'pop("#t4", {a}); pop("#f4", {a} + 0.15); flash({a} + 0.15, 0.4); pop("#x4", {a} + 0.4);', [(0, "kamera-blitz")])
szene(5, titel_zeile("t5", "Anteil UniCredit") + donut("d5", 540, 860, 220, [(0.476, UC)], 80) + t("n5", "47,6 %", 810, 100, "glow-r") + text("x5", "fast die Hälfte"),
      lambda a, d: f'pop("#t5", {a}); draw("#d5-0", {a} + 0.2, 1.0); slam("#n5", {a} + 1.1); pop("#x5", {a} + 0.2);', [(0, "swipe"), (0.2, "zaehler"), (1.1, "bass-schlag")])
szene(6, titel_zeile("t6", "Die Entscheidung") + kalender("k6", "NOV", "16", 120, 640, 300, ROT) + flagge("f6", "flagge-eu", 560, 670, 400, 3) + text("x6", "Die EU entscheidet"),
      lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.2); pop("#f6", {a} + 0.7); pop("#x6", {a} + 0.2);', [(0, "uhr-tickt"), (0.7, "hammer")])
szene(7, titel_zeile("t7", "Berlin ist dagegen") + flagge("f7", "flagge-deutschland", 120, 660, 320, -4) + icon_gross("i7", "🙅", 600, 630, 250, ROT)
      + stempel("s7", "„FEINDLICH“", 260, 980, ROT, 80, -5) + text("x7", "Regierung protestiert"),
      lambda a, d: f'pop("#t7", {a}); pop("#f7", {a} + 0.2); pop("#i7", {a} + 0.5); stempeln("#s7", {a} + 1.0); pop("#x7", {a} + 0.2);', [(0, "whoosh-weich"), (1.0, "stempel")])
szene(8, titel_zeile("t8", "Dein Konto") + chip("c8a", "✅ Konto", GRUEN, 660, 60, 140) + chip("c8b", "✅ IBAN", GRUEN, 820, 60, 140) + chip("c8c", "✅ Karte", GRUEN, 980, 60, 140)
      + text("x8", "bleibt erst einmal gleich"),
      lambda a, d: f'pop("#t8", {a}); pop("#c8a", {a} + 0.2); pop("#c8b", {a} + 0.5); pop("#c8c", {a} + 0.8); pop("#x8", {a} + 0.2);', [(0, "swipe"), (0.2, "richtig")])
szene(9, titel_zeile("t9", "Dein Erspartes") + icon_gross("i9", "🛡️", 0, 620, 240, GRUEN, True) + t("n9", "100.000 €", 900, 140, "glow-g") + text("x9", "gesetzlich geschützt"),
      lambda a, d: f'pop("#t9", {a}); pop("#i9", {a} + 0.2); slam("#n9", {a} + 0.6); pop("#x9", {a} + 0.2);', [(0, "whoosh-weich"), (0.6, "kasse")])
szene(10, titel_zeile("t10", "Rekordgewinn") + logo("l10", "commerzbank.png", 620, 560) + t("n10", "2,7 Mrd. €", 820, 140, "glow-g")
      + stempel("s10", "REKORD", 360, 1030, "#FFCC00", 80, -6) + text("x10", "in nur 9 Monaten"),
      lambda a, d: f'pop("#t10", {a}); pop("#l10", {a} + 0.1); slam("#n10", {a} + 0.5); stempeln("#s10", {a} + 1.1); pop("#x10", {a} + 0.2);', [(0, "swipe"), (1.1, "stempel")])
szene(11, titel_zeile("t11", "Und jetzt?") + icon_gross("i11", "🤔", 0, 640, 300, GELB, True) + text("x11", "Was planen die Italiener?"),
      lambda a, d: f'pop("#t11", {a}); slam("#i11", {a} + 0.2); pop("#x11", {a} + 0.2);', [(0, "spannung")])

SZ.append((0.0, 30.0, news_kopf("13.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, SZ, SFX, dauer=30.0, musik=beat(30.0) * 0.35)
    print(bildquellen(HERE))
