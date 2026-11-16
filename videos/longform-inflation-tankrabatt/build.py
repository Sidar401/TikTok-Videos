#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News v2, ~2:37): Inflation Okt. 2026 2,8 % (Destatis) – Tankrabatt bis 31.12. drückt die Zahl.
Leitmotiv: Zapfsäulen-Anzeige (Preis pro Liter). Kommentar- + Folgen-CTA (Beagle-Logo), Hinweis am Ende, kein Laufband."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, flagge, icon_gross, kalender, kit_assets, linie, news_kopf,  # noqa: E402
                         quelle, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, tz  # noqa: E402

kit_assets(HERE, ["flagge-deutschland"])
K = Kit(HERE, 33, ["frei-frankfurt-nacht", "frei-euro", "frei-50euro", "frei-sitzung", "frei-frankfurt-staedel", "frei-miami-nacht", "frei-ocean-drive", "frei-code-monitor"])
cap, st = K.cap, K.st
S = K.szene


def zapf(id_, preis, unter="pro Liter", farbe=OR, y=620):
    """Leitmotiv: Zapfsäulen-Display."""
    return (f'<div id="{id_}" style="position:absolute;left:220px;top:{y}px;width:640px;padding:30px 30px 26px;border-radius:30px;background:#0b0d0f;border:8px solid {farbe};'
            f'box-shadow:0 0 70px {farbe}77, 0 30px 50px #000;text-align:center;z-index:4"><div style="font-size:70px">⛽</div>'
            f'<div id="{id_}-p" class="mono" style="font-size:130px;color:{farbe};text-shadow:0 0 30px {farbe};line-height:1.05">{preis}</div>'
            f'<div class="mono" style="font-size:34px;color:{GRAU}">{unter}</div></div>')


def plakette(id_, text, y=600, farbe=OR):
    return (f'<div id="{id_}" style="position:absolute;left:140px;top:{y}px;width:800px;padding:34px 20px;border-radius:28px;background:#fff;color:#111;text-align:center;'
            f'font-weight:900;font-size:58px;box-shadow:0 0 60px {farbe}77, 0 30px 40px #000;z-index:4">📊 {text}</div>')


S("s1", "frei-euro", KIT_CSS + titel_zeile("t1", "⚡ Inflation", farbe=ROT) + tz("n1", "2,8 %", 600, 240, "glow-o") + icon_gross("i1", "🛒", 0, 900, 200, ROT, True)
  + stempel("s1x", "GEFÜHLT MEHR?", 400, 1010, ROT, 46, 8),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#n1", {a}); pop("#i1", {cap("s1", 2)}); stempeln("#s1x", {cap("s1", 3)});',
  [(0.0, "eilmeldung"), (cap("s1", 3), "stempel")])

S("s2", "frei-frankfurt-nacht", titel_zeile("t2", "Ab Januar …", farbe=GELB) + kalender("k2", "JAN", "1", 390, 620, 300, ROT) + chip("c2", "könnte es dich treffen", ROT, 1000, 56),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 1)}); slam("#c2", {cap("s2", 2)});', [(st("s2"), "spannung"), (cap("s2", 1), "uhr-tickt")])

S("s3", "frei-sitzung", titel_zeile("t3", "Deine Meinung") + icon_gross("i3", "💬", 0, 600, 240, OR, True) + chip("c3", "wird bei dir alles teurer?", OR, 920, 54),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.1); slam("#c3", {cap("s3", 1)});', [(st("s3"), "handy-benachrichtigung")])

S("s4", "frei-frankfurt-staedel", titel_zeile("t4", "Folg uns") + folg_logo("fl4", 600, 360) + chip("c4", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t4", {a}); {folg_js("fl4", a)} slam("#c4", {cap("s4", 0)} + 0.4);', [(st("s4"), "swipe"), (st("s4") + 0.4, "level-up")])

S("s5", "frei-sitzung", titel_zeile("t5", "Die offizielle Zahl") + plakette("p5", "Statistisches Bundesamt", 600) + tz("n5", "+2,8 %", 820, 150, "glow-o")
  + chip("c5", "Oktober vs. Vorjahr", OR, 1030, 50),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {cap("s5", 1)}); slam("#n5", {cap("s5", 2)}); pop("#c5", {cap("s5", 3)});', [(st("s5"), "zeitung"), (cap("s5", 2), "bass-schlag")])

S("s6", "frei-50euro", titel_zeile("t6", "Im Vergleich") + balken2("b6", "3,3 %", "2,8 %", 3.3, 2.8, ROT, OR, unten=("September", "Oktober")),
  lambda a, d: f'pop("#t6", {a});' + balken2_js("b6", st("s6") + 0.1, cap("s6", 1)), [(cap("s6", 1), "kurve-runter")])

S("s7", "frei-frankfurt-nacht", titel_zeile("t7", "Gute Nachricht?", farbe=GRUEN) + icon_gross("i7", "👍", 0, 620, 300, GRUEN, True),
  lambda a, d: f'pop("#t7", {a}); slam("#i7", {a} + 0.2);', [(st("s7"), "richtig")])

K8 = linie("ku8", [0.1, 0.25, 0.38, 0.5, 0.6, 0.68, 0.75], 150, 640, 780, 420, ROT, punkte=[(6, "Preise")])
S("s8", "frei-ocean-drive", titel_zeile("t8", "Aber …", farbe=ROT) + K8 + chip("c8", "steigen weiter – nur langsamer", ROT, 1110, 46),
  lambda a, d: f'pop("#t8", {a}); draw("#ku8-p", {a} + 0.1, 1.6); tl.fromTo("#ku8-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 0.8); pop("#ku8-w0", {cap("s8", 1)}); slam("#c8", {cap("s8", 2)});',
  [(st("s8"), "kurve-hoch")])

S("s9", "frei-sitzung", titel_zeile("t9", "Merk dir") + stempel("s9x", "NIE BILLIGER", 220, 720, ROT, 80, -6) + chip("c9", "Inflation = Preise steigen", OR, 980, 54),
  lambda a, d: f'pop("#t9", {a}); stempeln("#s9x", {cap("s9", 1)}); pop("#c9", {cap("s9", 1)} + 0.4);', [(cap("s9", 1), "stempel")])

S("s10", "frei-miami-nacht", titel_zeile("t10", "Preistreiber Nr. 1") + icon_gross("i10", "⚡", 140, 620, 220, ROT) + icon_gross("i10b", "🔥", 620, 620, 220, ROT) + tz("n10", "+12,2 %", 900, 150, "glow-r"),
  lambda a, d: f'pop("#t10", {a}); pop("#i10", {cap("s10", 0)}); pop("#i10b", {cap("s10", 1)}); slam("#n10", {cap("s10", 1)} + 0.3);', [(st("s10"), "swipe"), (cap("s10", 1) + 0.3, "kurve-hoch")])

S("s11", "frei-code-monitor", titel_zeile("t11", "Der Grund") + icon_gross("i11", "🛢️", 0, 600, 260, ROT, True) + chip("c11", "Iran-Krieg seit Februar", ROT, 930, 56),
  lambda a, d: f'pop("#t11", {a}); pop("#i11", {cap("s11", 0)}); slam("#c11", {cap("s11", 1)});', [(st("s11"), "nv-explosion-fern")])

S("s12", "frei-frankfurt-nacht", titel_zeile("t12", "Warum dann gefallen?", farbe=GELB) + icon_gross("i12", "🤔", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t12", {a}); slam("#i12", {a} + 0.2);', [(st("s12"), "spannung")])

S("s13", "frei-ocean-drive", titel_zeile("t13", "Der Tankrabatt") + zapf("z13", "−16,7 ct", "pro Liter günstiger", GRUEN),
  lambda a, d: f'pop("#t13", {a}); slam("#z13", {a} + 0.2);', [(st("s13"), "nv-tusch")])

S("s14", "frei-miami-nacht", titel_zeile("t14", "Seit 1. Oktober") + kalender("k14", "OKT", "1", 160, 620, 260, GRUEN) + icon_gross("i14", "⛽", 560, 620, 260, GRUEN)
  + chip("c14", "Steuer auf Benzin & Diesel ↓", GRUEN, 950, 50) + quelle("q14", "14,04 ct Energiesteuer + Mehrwertsteuer ≈ 16,7 ct", 1050),
  lambda a, d: f'pop("#t14", {a}); pop("#k14", {cap("s14", 0)}); pop("#i14", {cap("s14", 1)}); slam("#c14", {cap("s14", 2)}); pop("#q14", {cap("s14", 4)});',
  [(st("s14"), "swipe"), (cap("s14", 4), "kasse")])

S("s15", "frei-sitzung", titel_zeile("t15", "Bestätigt") + plakette("p15", "Statistisches Bundesamt", 620) + zettel("z15", "„Tankrabatt dämpft<br/>die Inflation“", 240, 820, 600, 56, GELB, -3),
  lambda a, d: f'pop("#t15", {a}); pop("#p15", {cap("s15", 1)}); pop("#z15", {cap("s15", 2)});', [(st("s15"), "zeitung")])

S("s16", "frei-frankfurt-nacht", titel_zeile("t16", "Aber: nur bis …", farbe=ROT) + kalender("k16", "DEZ", "31", 390, 620, 300, ROT) + chip("c16", "dann ist Schluss", ROT, 1000, 58),
  lambda a, d: f'pop("#t16", {a}); slam("#k16", {cap("s16", 1)}); pop("#c16", {cap("s16", 2)});', [(st("s16"), "alarm")])

S("s17", "frei-code-monitor", titel_zeile("t17", "Verlängerung?") + stempel("s17x", "NICHT BESCHLOSSEN", 140, 720, ROT, 66, -5),
  lambda a, d: f'pop("#t17", {a}); stempeln("#s17x", {cap("s17", 1)});', [(cap("s17", 1), "stempel")])

S("s18", "frei-ocean-drive", titel_zeile("t18", "Ab Januar", farbe=ROT) + zapf("z18", "+16,7 ct", "pro Liter wieder drauf", ROT) + icon_gross("i18", "📈", 780, 1000, 150, ROT),
  lambda a, d: f'pop("#t18", {a}); slam("#z18", {cap("s18", 1)}); pop("#i18", {cap("s18", 3)});', [(cap("s18", 1), "kurve-hoch"), (cap("s18", 3), "falsch")])

S("s19", "frei-miami-nacht", titel_zeile("t19", "Beispiel: 50 Liter") + vergleich("v19", "PRO MONAT", "+ 8 €", "PRO JAHR", "+ 100 €", OR, ROT, y=620, h=300),
  lambda a, d: f'pop("#t19", {a}); pop("#v19-l", {cap("s19", 2)}); pop("#v19-r", {cap("s19", 3)});', [(cap("s19", 2), "kasse"), (cap("s19", 3), "kasse")])

S("s20", "frei-sitzung", titel_zeile("t20", "Der Trick", farbe=GELB) + icon_gross("i20", "🎩", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t20", {a}); tl.fromTo("#i20", {{ rotation: -30, scale: 0.4 }}, {{ rotation: 0, scale: 1, duration: 0.5, ease: "back.out(1.8)" }}, {a} + 0.1);', [(st("s20"), "nv-pling-idee")])

KORB = "".join(f'<div id="w21{i}" style="position:absolute;left:{120 + (i % 3) * 300}px;top:{620 + (i // 3) * 200}px;width:240px;padding:20px 0;border-radius:22px;background:#14181bee;'
               f'border:4px solid {f};text-align:center;z-index:4"><div style="font-size:70px">{e}</div><div class="mono" style="font-size:34px;color:{f}">{p}</div></div>'
               for i, (e, p, f) in enumerate([("⚡", "+12 %", ROT), ("🧈", "−19 %", GRUEN), ("🍞", "+", OR), ("🚗", "+", OR), ("👕", "≈", GRAU), ("🏠", "+", OR)]))
S("s21", "frei-50euro", titel_zeile("t21", "2,8 % = Durchschnitt") + KORB,
  lambda a, d: f'pop("#t21", {a});' + "".join(f' pop("#w21{i}", {cap("s21", 1)} + {0.12 * i});' for i in range(6)), [(cap("s21", 1), "pop")])

S("s22", "frei-euro", titel_zeile("t22", "Billiger: Butter", farbe=GRUEN) + icon_gross("i22", "🧈", 0, 600, 260, GRUEN, True) + tz("n22", "−19 %", 900, 150, "glow-g"),
  lambda a, d: f'pop("#t22", {a}); pop("#i22", {cap("s22", 2)}); slam("#n22", {cap("s22", 3)});', [(cap("s22", 3), "kurve-runter")])

S("s23", "frei-miami-nacht", titel_zeile("t23", "Teurer: Energie", farbe=ROT) + icon_gross("i23", "⚡", 0, 600, 260, ROT, True) + chip("c23", "zahlst du jeden Tag", ROT, 930, 58),
  lambda a, d: f'pop("#t23", {a}); slam("#i23", {cap("s23", 0)}); slam("#c23", {cap("s23", 1)});', [(cap("s23", 0), "bass-schlag")])

S("s24", "frei-sitzung", titel_zeile("t24", "Deine Inflation") + balken2("b24", "2,8 %", "gefühlt?", 2.8, 5, OR, ROT, unten=("offiziell", "persönlich")),
  lambda a, d: f'pop("#t24", {a});' + balken2_js("b24", st("s24") + 0.1, cap("s24", 2)), [(cap("s24", 2), "kurve-hoch")])

S("s25", "frei-frankfurt-nacht", titel_zeile("t25", "Und dein Geld?", farbe=GELB) + icon_gross("i25", "💶", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t25", {a}); slam("#i25", {a} + 0.2);', [(st("s25"), "spannung")])

S("s26", "frei-code-monitor", titel_zeile("t26", "Girokonto ohne Zinsen") + icon_gross("i26", "🧊", 0, 600, 260, ROT, True) + chip("c26", "verliert jedes Jahr an Wert", ROT, 930, 54),
  lambda a, d: f'pop("#t26", {a}); pop("#i26", {cap("s26", 1)}); slam("#c26", {cap("s26", 2)});', [(cap("s26", 2), "glas-bricht")])

S("s27", "frei-50euro", titel_zeile("t27", "Beispiel: 10.000 €") + balken2("b27", "10.000 €", "9.720 €", 10000, 9720, GRAU, ROT, unten=("heute", "Kaufkraft in 1 Jahr"))
  + stempel("s27x", "−280 €", 640, 600, ROT, 60, 8),
  lambda a, d: f'pop("#t27", {a});' + balken2_js("b27", cap("s27", 0), cap("s27", 1)) + f' stempeln("#s27x", {cap("s27", 2)});', [(cap("s27", 2), "nv-falsch-buzzer")])


def tipp(sid, n, icon, kopf, text, hg, sfx):
    S(sid, hg, titel_zeile(f"t{sid}", f"Tipp {n}", farbe=GRUEN) + icon_gross(f"i{sid}", icon, 0, 600, 220, GRUEN, True)
      + (f'<div id="k{sid}" style="position:absolute;left:120px;top:860px;width:840px;padding:30px 38px;border-radius:26px;background:#14181bee;border:5px solid {GRUEN};'
         f'box-shadow:0 0 40px {GRUEN}55;z-index:4"><div class="mono" style="font-size:28px;color:{GRUEN};letter-spacing:2px">{kopf}</div>'
         f'<div style="font-weight:900;font-size:52px;color:#fff;line-height:1.1;margin-top:8px">{text}</div></div>'),
      lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#i{s}", {a} + 0.1); pop("#k{s}", {cap(s, 1)});', [(st(sid), "swipe"), (cap(sid, 1), sfx)])


tipp("s28", 1, "🏦", "TAGESGELD PRÜFEN", "gleicht es einen Teil<br/>der Inflation aus?", "frei-sitzung", "tresor")
tipp("s29", 2, "⛽", "IM DEZEMBER TANKEN", "falls der Rabatt<br/>nicht verlängert wird", "frei-ocean-drive", "kasse")
tipp("s30", 3, "🔌", "TARIFE VERGLEICHEN", "Strom & Gas –<br/>dort steigt es am meisten", "frei-code-monitor", "klick")

S("s31", "frei-frankfurt-staedel", titel_zeile("t31", "Langfristig") + icon_gross("i31", "🧺", 0, 600, 260, GRUEN, True) + chip("c31", "breit gestreuter Sparplan", GRUEN, 930, 56),
  lambda a, d: f'pop("#t31", {a}); pop("#i31", {cap("s31", 1)}); slam("#c31", {cap("s31", 3)});', [(st(("s31")), "nv-pling-idee")])

S("s32", "frei-euro", titel_zeile("t32", "Merk dir") + stempel("s32x", "INFLATION ↓ ≠ PREISE ↓", 110, 720, OR, 56, -5),
  lambda a, d: f'pop("#t32", {a}); stempeln("#s32x", {cap("s32", 1)});', [(cap("s32", 1), "stempel"), (cap("s32", 1) + 0.4, "nv-tusch")])

S("s33", "frei-frankfurt-nacht", titel_zeile("t33", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t33", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
  [(st("s33"), "zeitung")])

K.SZ.append((0.0, K.dauer, news_kopf("16.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
