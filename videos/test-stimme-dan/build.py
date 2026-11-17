#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (News v2, ~63 s): Ab 20.11. neue Regeln für Klarna/PayPal „Später bezahlen“ → verweist auf longform-klarna.
Folgen-CTA mit Beagle-Logo, kein Laufband (Verbraucherthema), kein Anlage-Hinweis (keine Anlage)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, flagge, icon_gross, kalender, kit_assets, news_kopf,  # noqa: E402
                         quelle, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, folg_js, folg_logo, logo, tz  # noqa: E402

KL = "#ffa8cd"
PP = "#0070e0"
kit_assets(HERE, ["flagge-eu", "flagge-deutschland"])
K = Kit(HERE, 3, ["frei-frankfurt-nacht", "frei-euro", "frei-50euro", "frei-sitzung", "frei-frankfurt-staedel", "frei-miami-nacht", "frei-code-monitor", "frei-ocean-drive"],
        logos=["klarna.png", "paypal.png"])
cap, st = K.cap, K.st
S = K.szene


def knopf(id_, text, farbe, y, w=640):
    return (f'<div id="{id_}" style="position:absolute;left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;padding:26px 0;border-radius:60px;background:{farbe};'
            f'box-shadow:0 0 60px {farbe}99, 0 20px 30px #000;text-align:center;font-weight:900;font-size:54px;color:#111;z-index:4">{text}</div>')


S("s1", "frei-frankfurt-nacht", KIT_CSS + titel_zeile("t1", "⚡ Ab Freitag", farbe=ROT) + logo("l1a", "klarna.png", 600, 380, x=80, karte=False, glow=KL)
  + logo("l1b", "paypal.png", 640, 420, x=560, glow=PP, pad=26) + stempel("s1x", "ABGELEHNT?", 230, 900, ROT, 90, -8),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1a", {a}); pop("#l1b", {a} + 0.15); stempeln("#s1x", {cap("s1", 3)});',
  [(0.0, "eilmeldung"), (cap("s1", 3), "mm-bumm")])

S("s2", "frei-sitzung", titel_zeile("t2", "Neue Regeln") + kalender("k2", "NOV", "20", 160, 620, 280, ROT) + flagge("f2", "flagge-deutschland", 540, 650, 380, 3)
  + chip("c2", "Ratenkauf · Kauf auf Rechnung", OR, 1000, 52),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 0)}); pop("#f2", {cap("s2", 1)}); slam("#c2", {cap("s2", 2)});', [(st("s2"), "swipe"), (cap("s2", 0), "uhr-tickt")])

S("s3", "frei-frankfurt-staedel", titel_zeile("t3", "Folg uns") + folg_logo("fl3", 600, 360) + chip("c3", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t3", {a}); {folg_js("fl3", a)} slam("#c3", {cap("s3", 0)} + 0.4);', [(st("s3"), "swipe")])

K.SZ.append((0.0, K.dauer, news_kopf(""), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
