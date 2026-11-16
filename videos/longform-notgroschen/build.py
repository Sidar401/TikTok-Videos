#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News v2, ~2:30): Notgroschen reicht bei jedem Zweiten nur 3 Monate (Civey/Debeka 9/2026).
Leitmotiv: Spar-Glas, das sich füllt/leert. Teilen- + Folgen-CTA (Beagle-Logo), keine Kapitel, Hinweis am Ende, kein Laufband."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, icon_gross, kalender, news_kopf, quelle,  # noqa: E402
                         stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, tz  # noqa: E402

K = Kit(HERE, 34, ["frei-euro", "frei-50euro", "frei-sitzung", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-code-monitor", "frei-miami-nacht", "frei-ocean-drive"])
cap, st = K.cap, K.st
S = K.szene


def glas(id_, stand, x=340, y=600, w=400, h=520, farbe=GRUEN, text=""):
    """Leitmotiv Spar-Glas: Füllstand 0..1 (JS: fuell(id, von, bis, t))."""
    fh = int(h * stand)
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:10px solid #ffffffcc;border-top:none;'
            f'border-radius:0 0 70px 70px;overflow:hidden;background:#ffffff0d;box-shadow:0 0 60px {farbe}55;z-index:3">'
            f'<div id="{id_}-f" style="position:absolute;left:0;right:0;bottom:0;height:{fh}px;background:linear-gradient(180deg,{farbe},{farbe}99);transform-origin:50% 100%"></div>'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:90px;color:#fff;text-shadow:0 6px 0 #000">{text}</div></div>'
            f'<div style="position:absolute;left:{x - 20}px;top:{y - 40}px;width:{w + 40}px;height:44px;border-radius:14px;background:#c9a46b;box-shadow:0 10px 20px #000;z-index:4"></div>')


def fuell(id_, a, von=0.0, bis=1.0, dauer=0.8):
    return f' tl.fromTo("#{id_}-f", {{ scaleY: {von} }}, {{ scaleY: {bis}, duration: {dauer}, ease: "power2.out" }}, {a});'


S("s1", "frei-euro", KIT_CSS + titel_zeile("t1", "⚡ Notgroschen-Check", farbe=ROT) + glas("g1", 1.0, farbe=ROT, text="3 Mon.") + chip("c1", "dann ist das Geld weg", ROT, 1160, 52),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#g1", {a});' + fuell("g1", cap("s1", 2), 1, 0.08, 2.2) + f' slam("#c1", {cap("s1", 3)});',
  [(0.0, "eilmeldung"), (cap("s1", 2), "kurve-runter")])

S("s2", "frei-50euro", titel_zeile("t2", "Noch schlimmer") + tz("n2", "1 von 5", 620, 190, "glow-r") + chip("c2", "nicht mal 4 Wochen", ROT, 900, 60),
  lambda a, d: f'pop("#t2", {a}); slam("#n2", {cap("s2", 0)} + 0.3); pop("#c2", {cap("s2", 2)});', [(cap("s2", 0) + 0.3, "bass-schlag")])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Schick's weiter") + icon_gross("i3", "📲", 0, 600, 280, OR, True) + chip("c3", "an alle ohne Notgroschen", OR, 950, 56),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a}); tl.fromTo("#i3", {{ rotation: -12 }}, {{ rotation: 12, duration: 0.15, yoyo: true, repeat: 5 }}, {a} + 0.3); slam("#c3", {cap("s3", 1)});',
  [(st("s3"), "handy-benachrichtigung")])

S("s4", "frei-frankfurt-staedel", titel_zeile("t4", "Folg uns") + folg_logo("fl4", 600, 360) + chip("c4", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t4", {a}); {folg_js("fl4", a)} slam("#c4", {cap("s4", 0)} + 0.4);', [(st("s4"), "swipe"), (st("s4") + 0.4, "level-up")])

S("s5", "frei-sitzung", titel_zeile("t5", "Die Umfrage") + icon_gross("i5", "📋", 0, 600, 260, OR, True) + chip("c5", "Civey für Debeka", OR, 950, 60),
  lambda a, d: f'pop("#t5", {a}); pop("#i5", {cap("s5", 1)}); slam("#c5", {cap("s5", 2)});', [(st("s5"), "zeitung")])

S("s6", "frei-code-monitor", titel_zeile("t6", "September 2026") + tz("n6", "1.000", 640, 200, "glow-o") + chip("c6", "Erwachsene · ohne Rentner", OR, 920, 54),
  lambda a, d: f'pop("#t6", {a}); slam("#n6", {cap("s6", 1)}); pop("#c6", {cap("s6", 2)});', [(st("s6"), "zaehler")])

DON = (f'<div id="d7" style="position:absolute;left:290px;top:600px;width:500px;height:500px;border-radius:50%;'
       f'background:conic-gradient({ROT} 0 51%, #ffffff1a 51% 100%);box-shadow:0 0 70px {ROT}66;z-index:3"></div>'
       f'<div style="position:absolute;left:420px;top:730px;width:240px;height:240px;border-radius:50%;background:#14181b;z-index:4;display:flex;align-items:center;justify-content:center;'
       f'font-weight:900;font-size:80px;color:#fff">51 %</div>')
S("s7", "frei-euro", titel_zeile("t7", "Höchstens 3 Monate") + DON,
  lambda a, d: f'pop("#t7", {a}); tl.fromTo("#d7", {{ rotation: -120, scale: 0.5 }}, {{ rotation: 0, scale: 1, duration: 0.8, ease: "back.out(1.4)" }}, {cap("s7", 0)});',
  [(cap("s7", 0), "nv-sog")])

S("s8", "frei-50euro", titel_zeile("t8", "Über ½ Jahr") + balken2("b8", "51 %", "23 %", 51, 23, ROT, GRUEN, unten=("max. 3 Monate", "> 6 Monate")),
  lambda a, d: f'pop("#t8", {a});' + balken2_js("b8", st("s8") + 0.1, cap("s8", 1)), [(cap("s8", 1), "pop")])

S("s9", "frei-sitzung", titel_zeile("t9", "Frauen trifft es härter") + icon_gross("i9", "👩", 140, 620, 220, ROT) + icon_gross("i9b", "👨", 620, 620, 220, GRAU)
  + chip("c9", "fast doppelt so oft: keinen Monat", ROT, 950, 50),
  lambda a, d: f'pop("#t9", {a}); pop("#i9", {cap("s9", 1)}); pop("#i9b", {cap("s9", 3)}); slam("#c9", {cap("s9", 2)});', [(st("s9"), "swipe"), (cap("s9", 2), "alarm")])

S("s10", "frei-frankfurt-nacht", titel_zeile("t10", "Warum gefährlich?", farbe=GELB) + icon_gross("i10", "⚠️", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t10", {a}); slam("#i10", {a} + 0.2);', [(st("s10"), "spannung")])

S("s11", "frei-ocean-drive", titel_zeile("t11", "Das Leben fragt nicht") + icon_gross("i11", "🎲", 0, 620, 280, OR, True),
  lambda a, d: f'pop("#t11", {a}); tl.fromTo("#i11", {{ rotation: -200, scale: 0.3 }}, {{ rotation: 0, scale: 1, duration: 0.7, ease: "back.out(1.6)" }}, {a} + 0.1);', [(st("s11"), "whoosh-schnell")])

S("s12", "frei-miami-nacht", titel_zeile("t12", "Plötzlich …") + icon_gross("i12a", "🧺", 90, 640, 200, ROT) + icon_gross("i12b", "🚗", 440, 640, 200, ROT) + icon_gross("i12c", "💼", 790, 640, 200, ROT)
  + chip("c12", "Rechnung · Werkstatt · Job weg", ROT, 940, 52),
  lambda a, d: f'pop("#t12", {a}); pop("#i12a", {cap("s12", 0)}); pop("#i12b", {cap("s12", 1)}); pop("#i12c", {cap("s12", 2)}); slam("#c12", {cap("s12", 2)} + 0.4);',
  [(cap("s12", 0), "falsch"), (cap("s12", 1), "falsch"), (cap("s12", 2), "tuer-zu")])

KONTO = (f'<div id="k13" class="mono" style="position:absolute;left:190px;top:640px;width:700px;padding:40px;border-radius:30px;background:#14181bee;border:6px solid {ROT};'
         f'box-shadow:0 0 60px {ROT}66;text-align:center;z-index:4"><div style="font-size:34px;color:{GRAU}">Kontostand</div>'
         f'<div style="font-size:130px;color:{ROT};text-shadow:0 0 30px {ROT}">−850 €</div></div>')
S("s13", "frei-code-monitor", titel_zeile("t13", "Ab in den Dispo") + KONTO,
  lambda a, d: f'pop("#t13", {a}); slam("#k13", {cap("s13", 1)});', [(cap("s13", 1), "handy-benachrichtigung")])

S("s14", "frei-50euro", titel_zeile("t14", "Dispo-Zinsen", farbe=ROT) + tz("n14", "> 10 %", 640, 230, "glow-r") + chip("c14", "pro Jahr", ROT, 920, 60),
  lambda a, d: f'pop("#t14", {a}); slam("#n14", {cap("s14", 1)}); pop("#c14", {cap("s14", 1)} + 0.3);', [(cap("s14", 1), "kurve-hoch")])

S("s15", "frei-sitzung", titel_zeile("t15", "Die Schuldenfalle") + icon_gross("i15", "🧺", 120, 680, 200, OR) + tz("p15", "→", 700, 120) + icon_gross("i15b", "⛰️", 640, 620, 280, ROT),
  lambda a, d: f'pop("#t15", {a}); pop("#i15", {a} + 0.1); pop("#p15", {cap("s15", 1)}); slam("#i15b", {cap("s15", 2)});', [(cap("s15", 2), "nv-erdbeben")])

S("s16", "frei-frankfurt-staedel", titel_zeile("t16", "Wie viel brauchst du?", farbe=GELB) + glas("g16", 0.0, text="?"),
  lambda a, d: f'pop("#t16", {a}); pop("#g16", {a});', [(st("s16"), "spannung")])

S("s17", "frei-sitzung", titel_zeile("t17", "Faustregel") + glas("g17", 1.0, text="2–3×") + chip("c17", "Netto-Gehälter · rät die Verbraucherzentrale", GRUEN, 1160, 36),
  lambda a, d: f'pop("#t17", {a}); pop("#g17", {a});' + fuell("g17", cap("s17", 1), 0, 1, 1.2) + f' slam("#c17", {cap("s17", 2)});', [(cap("s17", 1), "muenzen-glas")])

S("s18", "frei-miami-nacht", titel_zeile("t18", "Beispiel: Leonie") + icon_gross("i18", "👩‍💼", 0, 600, 240, OR, True) + tz("n18", "2.000 € netto", 900, 100, "glow-o"),
  lambda a, d: f'pop("#t18", {a}); pop("#i18", {a} + 0.1); slam("#n18", {cap("s18", 1)});', [(st("s18"), "swipe"), (cap("s18", 1), "kasse")])

S("s19", "frei-euro", titel_zeile("t19", "Leonies Notgroschen") + glas("g19", 1.0, text="") + tz("n19", "4.000 – 6.000 €", 1150, 90, "glow-g"),
  lambda a, d: f'pop("#t19", {a}); pop("#g19", {a});' + fuell("g19", a + 0.2, 0, 1, 1.4) + f' slam("#n19", {cap("s19", 1)});', [(st("s19"), "muenzen-glas"), (cap("s19", 1), "kasse")])

S("s20", "frei-frankfurt-nacht", titel_zeile("t20", "Klingt viel?") + icon_gross("i20", "😳", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t20", {a}); slam("#i20", {a} + 0.15);', [(st("s20"), "nv-staunen-wow")])

S("s21", "frei-code-monitor", titel_zeile("t21", "So baust du ihn auf", farbe=GRUEN) + tz("n21", "3", 600, 340, "glow-g") + chip("c21", "Schritte", GRUEN, 1000, 60),
  lambda a, d: f'pop("#t21", {a}); slam("#n21", {cap("s21", 1)}); pop("#c21", {cap("s21", 1)} + 0.3);', [(cap("s21", 1), "nv-boom-kurz")])


def schritt(sid, n, icon, kopf, text, hg, sfx):
    S(sid, hg, titel_zeile(f"t{sid}", f"Schritt {n}", farbe=GRUEN) + icon_gross(f"i{sid}", icon, 0, 600, 220, GRUEN, True)
      + (f'<div id="k{sid}" style="position:absolute;left:120px;top:860px;width:840px;padding:30px 38px;border-radius:26px;background:#14181bee;border:5px solid {GRUEN};'
         f'box-shadow:0 0 40px {GRUEN}55;z-index:4"><div class="mono" style="font-size:28px;color:{GRUEN};letter-spacing:2px">{kopf}</div>'
         f'<div style="font-weight:900;font-size:52px;color:#fff;line-height:1.1;margin-top:8px">{text}</div></div>'),
      lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#i{s}", {a} + 0.1); pop("#k{s}", {cap(s, 1)});', [(st(sid), "swipe"), (cap(sid, 1), sfx)])


schritt("s22", 1, "🧮", "AUSRECHNEN", "Was brauchst du<br/>wirklich im Monat?", "frei-sitzung", "taschenrechner")

LISTE = "".join(f'<div id="l23{i}" style="position:absolute;left:200px;top:{600 + i * 120}px;width:680px;padding:18px 30px;border-radius:20px;background:#14181bee;border:4px solid {OR};'
                f'font-weight:900;font-size:50px;color:#fff;z-index:4">{t_}</div>' for i, t_ in enumerate(["🏠 Miete", "🛒 Essen", "🛡️ Versicherungen", "📱 Handy"]))
S("s23", "frei-euro", titel_zeile("t23", "Deine Grundlage") + LISTE + chip("c23", "nicht dein Wunsch-Budget", ROT, 1110, 46),
  lambda a, d: f'pop("#t23", {a});' + "".join(f' pop("#l23{i}", {cap("s23", min(i, 2))} + {0.25 * i});' for i in range(4)) + f' slam("#c23", {cap("s23", 3)});',
  [(cap("s23", 0), "pop"), (cap("s23", 3), "falsch")])

schritt("s24", 2, "🤖", "AUTOMATISCH SPAREN", "am Gehalts-Tag<br/>per Dauerauftrag", "frei-code-monitor", "klick")

S("s25", "frei-50euro", titel_zeile("t25", "100 € im Monat") + glas("g25", 1.0, text="") + tz("n25", "3.600 €", 1140, 110, "glow-g"),
  lambda a, d: f'pop("#t25", {a}); pop("#g25", {a});' + fuell("g25", a + 0.2, 0, 1, 2.0) + f' slam("#n25", {cap("s25", 2)});',
  [(st("s25"), "zaehler"), (cap("s25", 2), "kasse")])

schritt("s26", 3, "🏦", "GETRENNT PARKEN", "eigenes Tagesgeld-<br/>konto, nicht Girokonto", "frei-frankfurt-nacht", "tresor")

S("s27", "frei-sitzung", titel_zeile("t27", "Tagesgeld") + vergleich("v27", "JEDERZEIT", "✓ ran", "BONUS", "✓ Zinsen", GRUEN, GRUEN, y=620, h=280)
  + chip("c27", "und nicht aus Versehen ausgeben", OR, 960, 50),
  lambda a, d: f'pop("#t27", {a}); pop("#v27-l", {cap("s27", 0)}); pop("#v27-r", {cap("s27", 1)}); slam("#c27", {cap("s27", 2)});', [(cap("s27", 0), "richtig"), (cap("s27", 1), "geld-erhalten")])

S("s28", "frei-miami-nacht", titel_zeile("t28", "Ganz wichtig", farbe=ROT) + stempel("s28x", "NICHT IN AKTIEN", 210, 680, ROT, 68, -6) + stempel("s28y", "NICHT IN BITCOIN", 200, 880, ROT, 68, 4),
  lambda a, d: f'pop("#t28", {a}); stempeln("#s28x", {cap("s28", 1)}); stempeln("#s28y", {cap("s28", 2)});', [(cap("s28", 1), "stempel"), (cap("s28", 2), "stempel")])

S("s29", "frei-code-monitor", titel_zeile("t29", "Das Risiko") + icon_gross("i29", "📉", 0, 600, 300, ROT, True) + chip("c29", "Geld gebraucht = Kurs unten?", ROT, 960, 54),
  lambda a, d: f'pop("#t29", {a}); slam("#i29", {cap("s29", 1)}); pop("#c29", {cap("s29", 2)});', [(cap("s29", 1), "kurve-runter")])

S("s30", "frei-50euro", titel_zeile("t30", "Am Wochenende") + vergleich("v30", "GOLD", "−31 %", "BITCOIN", "≈ ½ wert", ROT, ROT, y=620, h=280)
  + chip("c30", "seit Rekord", GRAU, 960, 46),
  lambda a, d: f'pop("#t30", {a}); pop("#v30-l", {cap("s30", 1)}); pop("#v30-r", {cap("s30", 2)}); pop("#c30", {cap("s30", 2)} + 0.3);', [(cap("s30", 1), "crash-bass")])

S("s31", "frei-frankfurt-staedel", titel_zeile("t31", "Selbstständig / Kinder?") + glas("g31", 1.0, farbe=OR, text="6×") + chip("c31", "eher 6 Monatsgehälter", OR, 1160, 52),
  lambda a, d: f'pop("#t31", {a}); pop("#g31", {a});' + fuell("g31", cap("s31", 1), 0, 1, 1.2) + f' slam("#c31", {cap("s31", 2)});', [(cap("s31", 1), "muenzen-glas")])

S("s32", "frei-sitzung", titel_zeile("t32", "Danach") + icon_gross("i32", "🪜", 0, 600, 280, GRUEN, True) + chip("c32", "nächste Stufe: Sparplan", GRUEN, 950, 56),
  lambda a, d: f'pop("#t32", {a}); pop("#i32", {a} + 0.1); slam("#c32", {cap("s32", 2)});', [(st("s32"), "level-up")])

S("s33", "frei-euro", titel_zeile("t33", "Merk dir") + stempel("s33x", "SCHUTZ VOR ARMUT", 170, 720, GRUEN, 60, -5) + chip("c33", "nicht reich – aber sicher", GRUEN, 980, 56),
  lambda a, d: f'pop("#t33", {a}); stempeln("#s33x", {cap("s33", 2)}); pop("#c33", {cap("s33", 1)});', [(cap("s33", 2), "stempel"), (cap("s33", 2) + 0.4, "nv-tusch")])

S("s34", "frei-frankfurt-nacht", titel_zeile("t34", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t34", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
  [(st("s34"), "zeitung")])

K.SZ.append((0.0, K.dauer, news_kopf("16.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
