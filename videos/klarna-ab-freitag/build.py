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
K = Kit(HERE, 16, ["frei-frankfurt-nacht", "frei-euro", "frei-50euro", "frei-sitzung", "frei-frankfurt-staedel", "frei-miami-nacht", "frei-code-monitor", "frei-ocean-drive"],
        logos=["klarna.png", "paypal.png"])
cap, st = K.cap, K.st
S = K.szene


def knopf(id_, text, farbe, y, w=640):
    return (f'<div id="{id_}" style="position:absolute;left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;padding:26px 0;border-radius:60px;background:{farbe};'
            f'box-shadow:0 0 60px {farbe}99, 0 20px 30px #000;text-align:center;font-weight:900;font-size:54px;color:#111;z-index:4">{text}</div>')


S("s1", "frei-frankfurt-nacht", KIT_CSS + titel_zeile("t1", "⚡ Ab Freitag", farbe=ROT) + logo("l1a", "klarna.png", 600, 380, x=80, karte=False, glow=KL)
  + logo("l1b", "paypal.png", 640, 420, x=560, glow=PP, pad=26) + stempel("s1x", "ABGELEHNT?", 230, 900, ROT, 90, -8),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1a", {a}); pop("#l1b", {a} + 0.15); stempeln("#s1x", {cap("s1", 3)});',
  [(0.0, "eilmeldung"), (cap("s1", 3), "nv-falsch-buzzer")])

S("s2", "frei-sitzung", titel_zeile("t2", "Neue Regeln") + kalender("k2", "NOV", "20", 160, 620, 280, ROT) + flagge("f2", "flagge-deutschland", 540, 650, 380, 3)
  + chip("c2", "Ratenkauf · Kauf auf Rechnung", OR, 1000, 52),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 0)}); pop("#f2", {cap("s2", 1)}); slam("#c2", {cap("s2", 2)});', [(st("s2"), "swipe"), (cap("s2", 0), "uhr-tickt")])

S("s3", "frei-frankfurt-staedel", titel_zeile("t3", "Folg uns") + folg_logo("fl3", 600, 360) + chip("c3", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t3", {a}); {folg_js("fl3", a)} slam("#c3", {cap("s3", 0)} + 0.4);', [(st("s3"), "swipe"), (st("s3") + 0.4, "level-up")])

S("s4", "frei-miami-nacht", titel_zeile("t4", "Bisher") + icon_gross("i4", "👆", 0, 580, 240, GRUEN, True) + knopf("b4", "Später bezahlen ✓", KL, 900),
  lambda a, d: f'pop("#t4", {a}); pop("#i4", {cap("s4", 0)}); tl.fromTo("#i4", {{ y: 0 }}, {{ y: 60, duration: 0.18, yoyo: true, repeat: 1 }}, {cap("s4", 0)} + 0.4); pop("#b4", {cap("s4", 1)});',
  [(cap("s4", 0) + 0.4, "klick"), (cap("s4", 1), "richtig")])

S("s5", "frei-euro", titel_zeile("t5", "Jetzt neu", farbe=GELB) + icon_gross("i5", "🔎", 0, 600, 260, GELB, True) + chip("c5", "Kannst du dir das leisten?", GELB, 950, 58),
  lambda a, d: f'pop("#t5", {a}); slam("#i5", {cap("s5", 1)}); pop("#c5", {cap("s5", 2)});', [(st("s5"), "whoosh-weich"), (cap("s5", 1), "taschenrechner")])

S("s6", "frei-50euro", titel_zeile("t6", "Gilt auch für …") + vergleich("v6", "KLEINE BETRÄGE", "unter 200 €", "OHNE ZINSEN", "0 % Raten", OR, OR, y=620, h=300),
  lambda a, d: f'pop("#t6", {a}); pop("#v6-l", {cap("s6", 1)}); pop("#v6-r", {cap("s6", 2)});', [(cap("s6", 1), "pop"), (cap("s6", 2), "pop")])

S("s7", "frei-sitzung", titel_zeile("t7", "Der Grund") + flagge("f7", "flagge-eu", 290, 600, 500, -3) + chip("c7", "EU-Regel für Verbraucherkredite", OR, 1000, 50),
  lambda a, d: f'pop("#t7", {a}); pop("#f7", {cap("s7", 1)}); slam("#c7", {cap("s7", 2)});', [(st("s7"), "hammer")])

S("s8", "frei-code-monitor", titel_zeile("t8", "Ehrlich gesagt …") + knopf("b8", "Später bezahlen", KL, 640) + tz("eq8", "=", 780, 110) + stempel("s8x", "KLEINER KREDIT", 210, 960, ROT, 70, -5),
  lambda a, d: f'pop("#t8", {a}); pop("#b8", {a} + 0.1); pop("#eq8", {cap("s8", 1)}); stempeln("#s8x", {cap("s8", 2)});', [(cap("s8", 2), "stempel")])

S("s9", "frei-ocean-drive", titel_zeile("t9", "Die Falle", farbe=ROT) + zettel("z9", "MAHNUNG<br/>+ Gebühren", 230, 640, 620, 78, "#ff6b6b", -4)
  + icon_gross("i9", "😵‍💫", 760, 560, 160, ROT),
  lambda a, d: f'pop("#t9", {a}); pop("#i9", {cap("s9", 1)}); tl.fromTo("#z9", {{ y: -300, opacity: 0, rotation: -15 }}, {{ y: 0, opacity: 1, rotation: -4, duration: 0.5, ease: "back.out(1.4)" }}, {cap("s9", 2)});',
  [(st("s9"), "alarm"), (cap("s9", 2), "papier-reissen")])

S("s10", "frei-frankfurt-nacht", titel_zeile("t10", "Gute Nachricht", farbe=GRUEN) + icon_gross("i10", "🛡️", 0, 600, 300, GRUEN, True),
  lambda a, d: f'pop("#t10", {a}); slam("#i10", {cap("s10", 1)});', [(st("s10"), "level-up")])

S("s11", "frei-euro", titel_zeile("t11", "Widerrufsrecht") + kalender("k11", "TAGE", "14", 390, 600, 300, GRUEN) + chip("c11", "Kauf auf später zurücknehmen", GRUEN, 1000, 50),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {cap("s11", 2)}); slam("#c11", {cap("s11", 2)} + 0.3);', [(st("s11"), "swipe"), (cap("s11", 2), "richtig")])

S("s12", "frei-sitzung", titel_zeile("t12", "Abgelehnt?") + icon_gross("i12", "📄", 0, 600, 260, OR, True) + chip("c12", "Anbieter muss begründen", OR, 950, 58),
  lambda a, d: f'pop("#t12", {a}); pop("#i12", {cap("s12", 1)}); slam("#c12", {cap("s12", 2)});', [(st("s12"), "zeitung")])

S("s13", "frei-miami-nacht", titel_zeile("t13", "Achtung", farbe=ROT) + kalender("k13", "NOV", "27", 390, 600, 300, ROT) + chip("c13", "Black Friday", ROT, 1000, 64),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {cap("s13", 1)}); slam("#c13", {cap("s13", 1)} + 0.3);', [(st("s13"), "alarm")])

S("s14", "frei-ocean-drive", titel_zeile("t14", "Auf Rechnung?") + knopf("b14", "Später bezahlen", KL, 640) + stempel("s14x", "ABGELEHNT", 270, 880, ROT, 90, -8),
  lambda a, d: f'pop("#t14", {a}); pop("#b14", {cap("s14", 0)}); stempeln("#s14x", {cap("s14", 2)});', [(cap("s14", 2), "nv-falsch-buzzer")])

S("s15", "frei-frankfurt-staedel", titel_zeile("t15", "Unser Tipp", farbe=GRUEN) + icon_gross("i15", "💡", 0, 600, 260, GRUEN, True) + chip("c15", "nur kaufen, was du heute zahlen kannst", GRUEN, 950, 38),
  lambda a, d: f'pop("#t15", {a}); pop("#i15", {a} + 0.1); slam("#c15", {cap("s15", 1)});', [(st("s15"), "nv-pling-idee")])

MK = (titel_zeile("mk-t", "Ganzes Video") + f'<div id="mk-b" style="position:absolute;left:371px;top:690px;width:338px;height:600px;border-radius:30px;overflow:hidden;'
      f'border:8px solid {OR};box-shadow:0 0 80px {OR}88;z-index:3"><img src="assets/lf.jpg" style="width:100%;height:100%;object-fit:cover" alt=""/></div>'
      + chip("mk-c", "Jetzt auf unserem Kanal", OR, 580, 50))
S("s16", None, MK,
  lambda a, d: (f'pop("#mk-t", {a}); tl.fromTo("#mk-b", {{ scale: 0.6, rotation: -6, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {a} + 0.2);'
                f' pop("#mk-c", {a} + 0.6); tl.fromTo("#mk-c", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {a} + 1.0);'),
  [(st("s16"), "whoosh-weich"), (st("s16") + 0.6, "pop")])

K.SZ.append((0.0, st("s16"), news_kopf("16.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
