#!/usr/bin/env python3
"""HundeFinanzTv Longform (News v2, ~3:17): EU-Bargeldgrenze 10.000 € ab 10.7.2027 (AMLR).
python3 build.py       → 9:16 (TikTok/Instagram)
python3 build.py quer  → 16:9 (YouTube): Szenen mittig + Fakten-Karte rechts, KEINE Kapitel-Leiste (Nutzer 14.11.).
Leitmotiv: Geldschein-Stapel mit roter 10.000-€-Linie. Regeln 16./17.11.: 1 CTA vorne (Kommentar „Bargeld“), Folgen in der Mitte, wenige Sounds."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import glow_short  # noqa: E402
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, QUER_CSS, ROT, bildquellen, flagge, icon_gross, kalender, kit_assets, news_kopf,  # noqa: E402
                         rahmen, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, folg_js, folg_logo, logo, tz  # noqa: E402

QUER = "quer" in sys.argv
EU = "#2b5cd8"
kit_assets(HERE, ["flagge-eu", "flagge-deutschland"])
K = Kit(HERE, 42, ["frei-euro", "frei-50euro", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-sitzung", "frei-code-monitor", "frei-miami-nacht", "frei-ocean-drive", "wallstreet"],
        quer=QUER, logos=["bundesbank.png", "flagge-frankreich.png", "flagge-spanien.png", "flagge-griechenland.png"])
cap, st = K.cap, K.st
S = K.szene


def stapel(id_, betrag, x=340, basis=1150, w=400, hmax=480, maxw=15000, linie=True, farbe=GRUEN):
    """Leitmotiv: Geldschein-Stapel (Höhe ~ Betrag) + rote 10.000-€-Grenzlinie."""
    h = int(hmax * betrag / maxw)
    lg = int(hmax * 10000 / maxw)
    scheine = "".join(f'<div style="position:absolute;left:0;right:0;bottom:{i * 14}px;height:12px;border-radius:3px;background:{farbe if i % 2 else farbe + "cc"}"></div>'
                      for i in range(max(1, h // 14)))
    li = (f'<div id="{id_}-l" style="position:absolute;left:{x - 140}px;top:{basis - lg}px;width:{w + 280}px;height:0;border-top:8px dashed {ROT};'
          f'filter:drop-shadow(0 0 12px {ROT});z-index:5"></div><div id="{id_}-lt" class="mono" style="position:absolute;left:{x + w + 20}px;top:{basis - lg - 54}px;'
          f'font-size:34px;color:{ROT};z-index:5">10.000 €</div>') if linie else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{basis - h}px;width:{w}px;height:{h}px;transform-origin:50% 100%;'
            f'filter:drop-shadow(0 0 30px {farbe}77);z-index:4">{scheine}</div>'
            f'<div id="{id_}-b" style="position:absolute;left:{x}px;width:{w}px;top:{basis + 16}px;text-align:center;font-weight:900;font-size:60px;color:#fff;z-index:5">'
            f'{betrag:,.0f} €</div>'.replace(",", ".") + li)


def stapel_js(id_, a, b=None):
    return (f' tl.fromTo("#{id_}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.8, ease: "power2.out" }}, {a}); pop("#{id_}-b", {a} + 0.6);'
            + (f' tl.fromTo("#{id_}-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5 }}, {b}); pop("#{id_}-lt", {b} + 0.3);' if b is not None else ""))


S("s1", "frei-euro", KIT_CSS + (QUER_CSS if QUER else "") + titel_zeile("t1", "⚡ Bargeld-Grenze", farbe=ROT) + flagge("f1", "flagge-eu", 380, 600, 320, -3)
  + kalender("k1", "AB JULI", "2027", 380, 860, 320, ROT),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#f1", {a}); pop("#k1", {cap("s1", 0)});', [(0.0, "mm-bumm")])

S("s2", "frei-50euro", titel_zeile("t2", "Neue EU-Regel") + stapel("st2", 10000, linie=True),
  lambda a, d: f'pop("#t2", {a});' + stapel_js("st2", a + 0.1, cap("s2", 1)), [])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Kommentier mal") + icon_gross("i3", "💬", 0, 580, 220, OR, True) + chip("c3", "„Bargeld“", OR, 860, 90),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.1); slam("#c3", {cap("s3", 4)});', [(st("s3"), "mm-wusch")])

S("s4", "frei-sitzung", titel_zeile("t4", "Bargeld abgeschafft?") + stempel("s4x", "FALSCH", 300, 720, ROT, 110, -8),
  lambda a, d: f'pop("#t4", {a}); stempeln("#s4x", {cap("s4", 1)});', [(cap("s4", 1), "stempel")])

S("s5", "frei-code-monitor", titel_zeile("t5", "Aber es ändert sich …") + icon_gross("i5", "🔍", 0, 600, 280, GELB, True),
  lambda a, d: f'pop("#t5", {a}); pop("#i5", {a} + 0.1);', [])

S("s6", "wallstreet", titel_zeile("t6", "Gegen Geldwäsche") + flagge("f6", "flagge-eu", 290, 600, 500, -2) + chip("c6", "EU-Verordnung", EU, 980, 60),
  lambda a, d: f'pop("#t6", {a}); pop("#f6", {a} + 0.1); slam("#c6", {cap("s6", 1)});', [])

S("s7", "frei-euro", titel_zeile("t7", "Ab wann?") + kalender("k7", "JULI 2027", "10", 160, 600, 300, ROT) + tz("n7", "27 Länder", 660, 110, "glow-o").replace('style="z-index:5;', 'style="z-index:5;left:500px;width:520px;')
  + chip("c7", "gilt direkt – überall gleich", OR, 1000, 52),
  lambda a, d: f'pop("#t7", {a}); pop("#k7", {cap("s7", 1)}); pop("#n7", {cap("s7", 3)}); slam("#c7", {cap("s7", 3)} + 0.3);', [(cap("s7", 1), "mm-tippen")])

S("s8", "frei-sitzung", titel_zeile("t8", "Deutschland") + flagge("f8", "flagge-deutschland", 340, 600, 400, 3) + chip("c8", "kein eigenes Gesetz nötig", OR, 920, 56),
  lambda a, d: f'pop("#t8", {a}); pop("#f8", {a} + 0.1); slam("#c8", {cap("s8", 1)});', [])

S("s9", "frei-frankfurt-nacht", titel_zeile("t9", "Was wird verboten?", farbe=ROT) + icon_gross("i9", "🚫", 0, 600, 300, ROT, True),
  lambda a, d: f'pop("#t9", {a}); slam("#i9", {a} + 0.2);', [])

S("s10", "frei-miami-nacht", titel_zeile("t10", "Bar an Händler") + stapel("st10", 12000, farbe=ROT) + chip("c10", "über 10.000 € → verboten", ROT, 1250, 46),
  lambda a, d: f'pop("#t10", {a});' + stapel_js("st10", cap("s10", 0), cap("s10", 0) + 0.6) + f' slam("#c10", {cap("s10", 1)});', [(cap("s10", 1), "mm-bumm")])

S("s11", "frei-ocean-drive", titel_zeile("t11", "Beispiel: Auto") + icon_gross("i11", "🚗", 0, 560, 220, OR, True) + tz("n11", "15.000 €", 800, 140, "glow-o")
  + stempel("s11x", "NICHT MEHR BAR", 180, 1000, ROT, 60, -6),
  lambda a, d: f'pop("#t11", {a}); pop("#i11", {cap("s11", 1)}); slam("#n11", {cap("s11", 3)}); stempeln("#s11x", {cap("s11", 4)});', [(cap("s11", 4), "stempel")])

S("s12", "frei-sitzung", titel_zeile("t12", "Schon ab 3.000 €") + icon_gross("i12", "🪪", 0, 600, 260, GELB, True) + chip("c12", "Ausweis zeigen – z. B. Autohaus", GELB, 920, 50),
  lambda a, d: f'pop("#t12", {a}); pop("#i12", {cap("s12", 2)}); slam("#c12", {cap("s12", 3)});', [(cap("s12", 2), "mm-kamera")])

S("s13", "frei-frankfurt-staedel", titel_zeile("t13", "Was bleibt erlaubt?", farbe=GRUEN) + icon_gross("i13", "✅", 0, 620, 300, GRUEN, True),
  lambda a, d: f'pop("#t13", {a}); slam("#i13", {a} + 0.2);', [])

S("s14", "frei-euro", titel_zeile("t14", "Bargeld zu Hause") + icon_gross("i14", "🏠", 0, 580, 260, GRUEN, True) + chip("c14", "✓ erlaubt – egal wie viel", GRUEN, 900, 56),
  lambda a, d: f'pop("#t14", {a}); pop("#i14", {a} + 0.1); slam("#c14", {cap("s14", 1)});', [])

S("s15", "frei-50euro", titel_zeile("t15", "Bar sparen") + icon_gross("i15", "🐷", 0, 580, 260, GRUEN, True) + chip("c15", "✓ erlaubt", GRUEN, 900, 60),
  lambda a, d: f'pop("#t15", {a}); pop("#i15", {a} + 0.1); slam("#c15", {cap("s15", 0)} + 0.4);', [])

S("s16", "frei-sitzung", titel_zeile("t16", "Privat an privat") + icon_gross("i16a", "🙋", 160, 600, 220, GRUEN) + tz("p16", "🤝", 640, 120) + icon_gross("i16b", "🙋‍♂️", 700, 600, 220, GRUEN)
  + chip("c16", "nicht betroffen", GRUEN, 920, 60),
  lambda a, d: f'pop("#t16", {a}); pop("#i16a", {cap("s16", 0)}); pop("#i16b", {cap("s16", 1)}); pop("#p16", {cap("s16", 1)} + 0.2); slam("#c16", {cap("s16", 1)} + 0.5);', [])

S("s17", "frei-ocean-drive", titel_zeile("t17", "Auto vom Nachbarn") + icon_gross("i17", "🚙", 0, 580, 240, GRUEN, True) + chip("c17", "💶 bar zahlen ✓", GRUEN, 900, 60),
  lambda a, d: f'pop("#t17", {a}); pop("#i17", {cap("s17", 1)}); slam("#c17", {cap("s17", 3)});', [])

S("s18", "frei-frankfurt-staedel", titel_zeile("t18", "Folg uns") + folg_logo("fl18", 600, 360) + chip("c18", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t18", {a}); {folg_js("fl18", a)} slam("#c18", {cap("s18", 0)} + 0.4);', [(st("s18"), "mm-wusch")])

S("s19", "frei-frankfurt-nacht", titel_zeile("t19", "Warum das Ganze?", farbe=GELB) + icon_gross("i19", "🤔", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t19", {a}); slam("#i19", {a} + 0.2);', [])

S("s20", "frei-code-monitor", titel_zeile("t20", "Bargeld = keine Spur") + icon_gross("i20", "👣", 0, 600, 260, GRAU, True) + chip("c20", "schwer nachzuverfolgen", OR, 920, 56),
  lambda a, d: f'pop("#t20", {a}); pop("#i20", {a} + 0.1); slam("#c20", {cap("s20", 1)});', [])

S("s21", "frei-miami-nacht", titel_zeile("t21", "Geldwäsche") + icon_gross("i21", "🧼", 140, 620, 220, ROT) + icon_gross("i21b", "💶", 620, 620, 220, ROT)
  + chip("c21", "Drogen · Betrug → „sauberes“ Geld", ROT, 920, 48),
  lambda a, d: f'pop("#t21", {a}); pop("#i21", {cap("s21", 0)}); pop("#i21b", {cap("s21", 2)}); slam("#c21", {cap("s21", 2)} + 0.3);', [])

S("s22", "frei-sitzung", titel_zeile("t22", "Deutschland beliebt") + flagge("f22", "flagge-deutschland", 340, 600, 400, -3) + stempel("s22x", "KEINE GRENZE", 230, 900, ROT, 70, -6),
  lambda a, d: f'pop("#t22", {a}); pop("#f22", {cap("s22", 1)}); stempeln("#s22x", {cap("s22", 4)});', [(cap("s22", 4), "stempel")])

S("s23", "wallstreet", titel_zeile("t23", "Andere Länder") + icon_gross("i23", "🌍", 0, 620, 300, OR, True),
  lambda a, d: f'pop("#t23", {a}); pop("#i23", {a} + 0.1);', [])


def land(id_, datei, wert, x, y=600):
    return (logo(f"{id_}f", datei, y, 280, x=x, karte=False, glow="#ffffff")
            + f'<div id="{id_}w" style="position:absolute;left:{x - 20}px;width:320px;top:{y + 210}px;text-align:center;font-weight:900;font-size:62px;color:{ROT};'
              f'text-shadow:0 0 30px {ROT};z-index:5">{wert}</div>')


S("s24", "frei-euro", titel_zeile("t24", "Barzahl-Grenzen") + land("l24a", "flagge-frankreich.png", "1.000 €", 60) + land("l24b", "flagge-spanien.png", "1.000 €", 400)
  + land("l24c", "flagge-griechenland.png", "500 €", 740),
  lambda a, d: (f'pop("#t24", {a}); pop("#l24af", {cap("s24", 0)}); pop("#l24bf", {cap("s24", 0)} + 0.3); pop("#l24aw", {cap("s24", 1)}); pop("#l24bw", {cap("s24", 1)} + 0.2);'
                f' pop("#l24cf", {cap("s24", 2)}); pop("#l24cw", {cap("s24", 3)});'), [(cap("s24", 1), "mm-tippen")])

S("s25", "frei-50euro", titel_zeile("t25", "Im Vergleich") + balken2("b25", "500–1.000 €", "10.000 €", 1000, 10000, ROT, GRUEN, unten=("FR · ES · GR", "EU ab 2027")),
  lambda a, d: f'pop("#t25", {a});' + balken2_js("b25", st("s25") + 0.1, cap("s25", 1)), [])

S("s26", "frei-sitzung", titel_zeile("t26", "Gibt es schon heute") + icon_gross("i26", "📜", 0, 620, 280, OR, True),
  lambda a, d: f'pop("#t26", {a}); pop("#i26", {a} + 0.1);', [])

S("s27", "frei-frankfurt-staedel", titel_zeile("t27", "Immobilien") + icon_gross("i27", "🏡", 0, 580, 260, ROT, True) + chip("c27", "seit 2023: nicht mehr bar", ROT, 900, 56),
  lambda a, d: f'pop("#t27", {a}); pop("#i27", {a} + 0.1); slam("#c27", {cap("s27", 2)});', [])

S("s28", "frei-euro", titel_zeile("t28", "Gold kaufen") + icon_gross("i28", "🪙", 0, 580, 260, GELB, True) + chip("c28", "ohne Ausweis: bis knapp 2.000 €", GELB, 900, 52),
  lambda a, d: f'pop("#t28", {a}); pop("#i28", {a} + 0.1); slam("#c28", {cap("s28", 1)});', [])

S("s29", "frei-miami-nacht", titel_zeile("t29", "Reisen") + icon_gross("i29", "🛃", 0, 580, 260, OR, True) + chip("c29", "ab 10.000 € bar → beim Zoll anmelden", OR, 900, 46),
  lambda a, d: f'pop("#t29", {a}); pop("#i29", {cap("s29", 1)}); slam("#c29", {cap("s29", 3)});', [])

S("s30", "frei-code-monitor", titel_zeile("t30", "Bargeld noch wichtig?", farbe=GELB) + logo("l30", "bundesbank.png", 640, 640, glow="#fff", pad=30),
  lambda a, d: f'pop("#t30", {a}); pop("#l30", {a} + 0.2);', [])

DON = (f'<div id="d31" style="position:absolute;left:290px;top:600px;width:500px;height:500px;border-radius:50%;'
       f'background:conic-gradient({OR} 0 45%, #ffffff1a 45% 100%);box-shadow:0 0 70px {OR}66;z-index:3"></div>'
       f'<div style="position:absolute;left:420px;top:730px;width:240px;height:240px;border-radius:50%;background:#14181b;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:center">'
       f'<div style="font-weight:900;font-size:80px;color:#fff">45 %</div><div class="mono" style="font-size:24px;color:{GRAU}">bar · 2025</div></div>')
S("s31", "frei-50euro", titel_zeile("t31", "Einkäufe bar bezahlt") + DON,
  lambda a, d: f'pop("#t31", {a}); tl.fromTo("#d31", {{ rotation: -120, scale: 0.5 }}, {{ rotation: 0, scale: 1, duration: 0.8, ease: "back.out(1.4)" }}, {cap("s31", 1)});', [])

S("s32", "frei-sitzung", titel_zeile("t32", "Zum ersten Mal") + tz("n32", "< ½", 620, 260, "glow-o") + chip("c32", "weniger als die Hälfte", OR, 960, 58),
  lambda a, d: f'pop("#t32", {a}); slam("#n32", {a} + 0.2); pop("#c32", {cap("s32", 1)});', [])

S("s33", "frei-frankfurt-nacht", titel_zeile("t33", "Trotzdem wichtig") + tz("n33", "80 %", 600, 240, "glow-g") + chip("c33", "wollen weiter bar zahlen können", GRUEN, 940, 52),
  lambda a, d: f'pop("#t33", {a}); slam("#n33", {cap("s33", 0)}); pop("#c33", {cap("s33", 2)});', [])

S("s34", "frei-ocean-drive", titel_zeile("t34", "Geldautomaten") + balken2("b34", "57.000", "≈ 50.000", 57, 50, GRAU, ROT, unten=("2020", "2024")),
  lambda a, d: f'pop("#t34", {a});' + balken2_js("b34", cap("s34", 2), cap("s34", 3)), [])

S("s35", "frei-frankfurt-staedel", titel_zeile("t35", "Und für dich?", farbe=GELB) + icon_gross("i35", "🫵", 0, 620, 300, GELB, True),
  lambda a, d: f'pop("#t35", {a}); slam("#i35", {a} + 0.15);', [])

S("s36", "frei-euro", titel_zeile("t36", "Im Alltag") + icon_gross("i36", "🛒", 0, 580, 260, GRUEN, True) + chip("c36", "ändert sich fast nichts", GRUEN, 900, 58),
  lambda a, d: f'pop("#t36", {a}); pop("#i36", {a} + 0.1); slam("#c36", {cap("s36", 0)} + 0.4);', [])

S("s37", "frei-sitzung", titel_zeile("t37", "Aber …", farbe=GRUEN) + tz("n37", "3", 600, 320, "glow-g") + chip("c37", "Dinge, die du wissen solltest", GRUEN, 960, 54),
  lambda a, d: f'pop("#t37", {a}); slam("#n37", {a} + 0.2); pop("#c37", {cap("s37", 1)});', [])


def tipp(sid, n, icon, kopf, text, hg, sfx=None):
    S(sid, hg, titel_zeile(f"t{sid}", f"Tipp {n}", farbe=GRUEN) + icon_gross(f"i{sid}", icon, 0, 600, 220, GRUEN, True)
      + (f'<div id="k{sid}" style="position:absolute;left:120px;top:860px;width:840px;padding:30px 38px;border-radius:26px;background:#14181bee;border:5px solid {GRUEN};'
         f'box-shadow:0 0 40px {GRUEN}55;z-index:4"><div class="mono" style="font-size:28px;color:{GRUEN};letter-spacing:2px">{kopf}</div>'
         f'<div style="font-weight:900;font-size:52px;color:#fff;line-height:1.1;margin-top:8px">{text}</div></div>'),
      lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#i{s}", {a} + 0.1); pop("#k{s}", {cap(s, 1)});', [(cap(sid, 1), sfx)] if sfx else [])


tipp("s38", 1, "🏦", "GROSSE KÄUFE", "beim Händler lieber<br/>per Überweisung", "frei-code-monitor")
tipp("s39", 2, "🧾", "BELEGE AUFHEBEN", "Bank kann bei Einzahlung<br/>nach Herkunft fragen", "frei-sitzung", "mm-tippen")
tipp("s40", 3, "🏠", "NOTVORRAT", "ein bisschen Bargeld<br/>zu Hause ist okay", "frei-euro")

S("s41", "frei-frankfurt-nacht", titel_zeile("t41", "Merk dir") + stempel("s41x", "BARGELD BLEIBT", 200, 680, GRUEN, 70, -5) + chip("c41", "bar an Händler: max. 10.000 €", OR, 940, 46),
  lambda a, d: f'pop("#t41", {a}); stempeln("#s41x", {cap("s41", 1)}); slam("#c41", {cap("s41", 3)});', [(cap("s41", 1), "stempel")])

S("s42", "wallstreet", titel_zeile("t42", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t42", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});', [])

K.SZ.append((0.0, K.dauer, rahmen(news_kopf("17.11.2026"), QUER), lambda a, d: "", 8))

if QUER:
    RECHTS = (f'<div id="re" style="position:absolute;left:1440px;top:300px;width:410px;padding:28px;border-radius:26px;background:#14181bee;border:3px solid {EU}88;z-index:4">'
              f'<img src="assets/logos/flagge-eu.svg" style="width:200px;border-radius:8px"/>'
              f'<div class="mono" style="font-size:28px;color:{GRAU};margin-top:20px">ab 10. Juli 2027</div>'
              f'<div style="font-weight:900;font-size:64px;color:{ROT};text-shadow:0 0 30px {ROT}">max. 10.000 €</div>'
              f'<div class="mono" style="font-size:28px;color:{GRAU}">bar an Händler · privat frei</div></div>')
    K.SZ.append((st("s2"), K.dauer, RECHTS, lambda a, d: f'tl.fromTo("#re", {{ x: 80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5 }}, {a});', 5))
    glow_short.querformat()

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
