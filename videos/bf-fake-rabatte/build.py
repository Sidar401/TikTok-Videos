#!/usr/bin/env python3
"""HundeFinanzTv Short (News v2, ~63 s): Black Friday – 3 Tricks bei Fake-Rabatten. Teilen-CTA, kein Laufband (Verbraucherthema)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, icon_gross, kalender, kreis, news_kopf, quelle,  # noqa: E402
                         stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, tz  # noqa: E402

K = Kit(HERE, 17, ["frei-miami-nacht", "frei-euro", "frei-50euro", "frei-frankfurt-nacht", "frei-ocean-drive", "frei-sitzung", "frei-frankfurt-staedel", "frei-code-monitor"])
cap, st = K.cap, K.st
S = K.szene


def preisschild(id_, alt, neu, y, alt_farbe=GRAU):
    return (f'<div id="{id_}" style="position:absolute;left:190px;top:{y}px;width:700px;padding:34px 40px;border-radius:30px;background:#14181bee;border:6px solid {ROT};'
            f'box-shadow:0 0 60px {ROT}66;text-align:center;z-index:4;transform:rotate(-2deg)">'
            f'<div class="mono" style="font-size:72px;color:{alt_farbe};text-decoration:line-through;text-decoration-color:{ROT};text-decoration-thickness:8px">{alt}</div>'
            f'<div style="font-weight:900;font-size:150px;color:#fff;line-height:1;text-shadow:0 0 40px {ROT}">{neu}</div></div>')


S("s1", "frei-miami-nacht", KIT_CSS + titel_zeile("t1", "⚡ Black Friday", farbe=ROT) + icon_gross("i1", "🛍️", 0, 600, 300, ROT, True)
  + stempel("s1x", "-70 % ???", 270, 960, ROT, 90, -8),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#i1", {a}); stempeln("#s1x", {cap("s1", 1)});',
  [(0.0, "eilmeldung"), (cap("s1", 1), "stempel")])

S("s2", "frei-sitzung", titel_zeile("t2", "Studie") + tz("n2", "nur 37 %", 640, 170, "glow-o") + chip("c2", "glauben: wirklich billiger", OR, 900, 56)
  + quelle("q2", "BCG-Umfrage · Herbst 2026", 1010),
  lambda a, d: f'pop("#t2", {a}); slam("#n2", {cap("s2", 1)}); pop("#c2", {cap("s2", 3)}); pop("#q2", {cap("s2", 3)} + 0.3);', [(st("s2"), "swipe"), (cap("s2", 1), "bass-schlag")])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Schick's weiter") + icon_gross("i3", "📲", 0, 600, 280, OR, True) + chip("c3", "an deinen Schnäppchen-Jäger", OR, 950, 56),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a}); tl.fromTo("#i3", {{ rotation: -12 }}, {{ rotation: 12, duration: 0.15, yoyo: true, repeat: 5 }}, {a} + 0.3); slam("#c3", {cap("s3", 1)});',
  [(st("s3"), "handy-benachrichtigung")])

S("s4", "frei-euro", titel_zeile("t4", "Trick 1", farbe=GELB) + preisschild("p4", "999 €", "?", 620) ,
  lambda a, d: f'pop("#t4", {a}); slam("#p4", {cap("s4", 1)});', [(st("s4"), "whoosh-schnell"), (cap("s4", 1), "nv-platte-kratzer")])

S("s5", "frei-ocean-drive", titel_zeile("t5", "Die UVP-Falle") + zettel("z5", "„unverbindliche<br/>Preisempfehlung“", 190, 640, 700, 66, GELB, -3)
  + chip("c5", "verlangt fast niemand", ROT, 1010, 58),
  lambda a, d: f'pop("#t5", {a}); tl.fromTo("#z5", {{ y: -300, opacity: 0, rotation: -15 }}, {{ y: 0, opacity: 1, rotation: -3, duration: 0.5, ease: "back.out(1.4)" }}, {cap("s5", 1)}); slam("#c5", {cap("s5", 4)});',
  [(st("s5"), "papier-reissen"), (cap("s5", 4), "falsch")])

S("s6", "frei-miami-nacht", titel_zeile("t6", "Beispiel: Fernseher") + icon_gross("i6", "📺", 0, 560, 200, OR, True) + preisschild("p6", "UVP 450 €", "299 €", 820),
  lambda a, d: f'pop("#t6", {a}); pop("#i6", {cap("s6", 0)}); pop("#p6", {cap("s6", 1)}); tl.fromTo("#p6 > div:last-child", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {cap("s6", 2)});',
  [(st("s6"), "swipe"), (cap("s6", 2), "kasse")])

S("s7", "frei-50euro", titel_zeile("t7", "Klingt nach …") + tz("n7", "−34 %", 640, 260, "glow-g") + chip("c7", "Wow?!", GRUEN, 980, 64),
  lambda a, d: f'pop("#t7", {a}); slam("#n7", {cap("s7", 0)} + 0.4); pop("#c7", {cap("s7", 0)} + 0.9);', [(cap("s7", 0) + 0.4, "nv-staunen-wow")])

S("s8", "frei-sitzung", titel_zeile("t8", "Normaler Ladenpreis") + balken2("b8", "320 €", "299 €", 320, 299, GRAU, OR, basis=1150, hmax=440, unten=("sonst", "Black Friday")),
  lambda a, d: f'pop("#t8", {a});' + balken2_js("b8", cap("s8", 0), cap("s8", 1)), [(st("s8"), "swipe"), (cap("s8", 1), "kurve-runter")])

S("s9", "frei-euro", titel_zeile("t9", "Echter Rabatt", farbe=ROT) + tz("n9", "nur 7 %", 640, 220, "glow-r") + kreis("k9", 540, 760, 400, 170, ROT),
  lambda a, d: f'pop("#t9", {a}); slam("#n9", {cap("s9", 0)} + 0.4); draw("#k9-p", {cap("s9", 0)} + 0.8, 0.5);', [(cap("s9", 0) + 0.4, "nv-falsch-buzzer")])

UHR = (f'<div id="u10" class="mono" style="position:absolute;left:190px;top:640px;width:700px;padding:30px;border-radius:30px;background:#000c;border:6px solid {ROT};'
       f'box-shadow:0 0 70px {ROT}88;text-align:center;font-size:150px;color:{ROT};text-shadow:0 0 30px {ROT};z-index:4">09:59</div>')
S("s10", "frei-ocean-drive", titel_zeile("t10", "Trick 2: Countdown", farbe=GELB) + UHR + chip("c10", "„Nur noch 10 Minuten!“", ROT, 980, 60),
  lambda a, d: (f'pop("#t10", {a}); slam("#u10", {cap("s10", 1)}); pop("#c10", {cap("s10", 2)});'
                f' tl.fromTo("#u10", {{ opacity: 1 }}, {{ opacity: 0.35, duration: 0.25, yoyo: true, repeat: 7 }}, {cap("s10", 1)} + 0.4);'),
  [(st("s10"), "whoosh-schnell"), (cap("s10", 1), "uhr-tickt")])

S("s11", "frei-frankfurt-staedel", titel_zeile("t11", "Ruhig bleiben") + icon_gross("i11", "🧘", 0, 600, 280, GRUEN, True) + chip("c11", "Druck = teure Entscheidungen", OR, 950, 54),
  lambda a, d: f'pop("#t11", {a}); pop("#i11", {a} + 0.1); slam("#c11", {cap("s11", 1)});', [(st("s11"), "whoosh-weich")])

S("s12", "frei-miami-nacht", titel_zeile("t12", "Trick 3", farbe=GELB) + icon_gross("i12", "📈", 140, 620, 220, ROT) + icon_gross("i12b", "📉", 620, 620, 220, GRUEN)
  + chip("c12", "erst rauf … dann „Rabatt“", ROT, 950, 58),
  lambda a, d: f'pop("#t12", {a}); pop("#i12", {cap("s12", 0)} + 0.4); pop("#i12b", {cap("s12", 1)} + 0.4); slam("#c12", {cap("s12", 1)} + 0.6);',
  [(st("s12"), "swipe"), (cap("s12", 1) + 0.4, "kurve-hoch")])

S("s13", "frei-sitzung", titel_zeile("t13", "Die 30-Tage-Regel") + kalender("k13", "TAGE", "30", 390, 600, 300, GRUEN)
  + chip("c13", "Rabatt = vom niedrigsten Preis", GRUEN, 1000, 52) + quelle("q13", "Preisangabenverordnung § 11", 1110),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {cap("s13", 2)}); slam("#c13", {cap("s13", 1)}); pop("#q13", {cap("s13", 2)} + 0.3);',
  [(st("s13"), "hammer"), (cap("s13", 2), "richtig")])

S("s14", "frei-code-monitor", titel_zeile("t14", "Unser Tipp", farbe=GRUEN) + icon_gross("i14", "📝", 0, 600, 260, GRUEN, True) + chip("c14", "Merkliste + Preis von heute", GRUEN, 950, 56),
  lambda a, d: f'pop("#t14", {a}); pop("#i14", {cap("s14", 1)}); slam("#c14", {cap("s14", 2)});', [(st("s14"), "nv-pling-idee"), (cap("s14", 1), "tippen")])

S("s15", "frei-frankfurt-nacht", titel_zeile("t15", "Vergleichen") + vergleich("v15", "SEITE 1", "🔍 Preis A", "SEITE 2", "🔍 Preis B", GRUEN, GRUEN, y=620, h=280)
  + chip("c15", "rät die Verbraucherzentrale", OR, 980, 50),
  lambda a, d: f'pop("#t15", {a}); pop("#v15-l", {cap("s15", 1)}); pop("#v15-r", {cap("s15", 1)} + 0.3); slam("#c15", {cap("s15", 3)});',
  [(st("s15"), "swipe"), (cap("s15", 1), "klick"), (cap("s15", 1) + 0.3, "klick")])

S("s16", "frei-miami-nacht", titel_zeile("t16", "Black Friday 2026") + kalender("k16", "NOV", "27", 390, 600, 300, ROT) + chip("c16", "Freitag", ROT, 980, 60),
  lambda a, d: f'pop("#t16", {a}); slam("#k16", {cap("s16", 1)}); pop("#c16", {cap("s16", 2)});', [(st("s16"), "uhr-tickt")])

S("s17", "frei-euro", titel_zeile("t17", "Merk dir") + stempel("s17x", "BESTES SCHNÄPPCHEN", 150, 700, GRUEN, 50, -5)
  + chip("c17", "= nicht kaufen 😉", GRUEN, 960, 64),
  lambda a, d: f'pop("#t17", {a}); stempeln("#s17x", {cap("s17", 1)}); slam("#c17", {cap("s17", 2)});', [(cap("s17", 1), "stempel"), (cap("s17", 2), "nv-tusch")])

K.SZ.append((0.0, K.dauer, news_kopf("16.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
