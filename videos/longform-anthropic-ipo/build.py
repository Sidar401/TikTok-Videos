#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News v2, 2:32): Anthropic-Börsengang am 19.11. – lohnt sich der Kauf am ersten Tag?
Keine Kapitel, Hinweis am Ende, freie Hintergründe, Original-Logos (gemeinfrei), kein Personenfoto."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, flagge, icon_gross, kalender, linie, news_kopf, quelle,  # noqa: E402
                         raster, stempel, titel_zeile, vergleich, zettel)
from analyse_kit import kit_assets  # noqa: E402
from glow_short import build, chip, partikel  # noqa: E402
from lf_kit import Kit, balken2, balken2_js, logo, tz  # noqa: E402

AN = "#d97757"
kit_assets(HERE, ["flagge-deutschland"])
K = Kit(HERE, 36, ["frei-code-monitor", "frei-code-css", "wallstreet", "handelssaal", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-euro", "frei-50euro", "frei-sitzung", "frei-miami-omni"],
        logos=["anthropic.svg", "claude.svg", "nasdaq.svg", "spacex.png", "meta.png", "google.svg", "amazon.svg", "openai.svg"])
cap, st = K.cap, K.st
S = K.szene

S("s1", "frei-code-monitor", KIT_CSS + titel_zeile("t1", "⚡ Börsengang", farbe=ROT) + logo("l1", "anthropic.svg", 610, 620, glow=AN, pad=30)
  + tz("n1", "bis 1,4 Bio. $", 820, 130, "glow-o") + kalender("k1", "DO", "19.11.", 400, 1000, 280, AN),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#k1", {cap("s1", 0)}); pop("#l1", {cap("s1", 1)}); slam("#n1", {cap("s1", 2)});',
  [(0.0, "eilmeldung"), (cap("s1", 2), "kasse")])

S("s2", "frei-code-css", titel_zeile("t2", "Die Firma hinter …") + logo("l2", "claude.svg", 660, 620, glow=AN, pad=30),
  lambda a, d: f'pop("#t2", {a}); pop("#l2", {cap("s2", 3)}); flash({cap("s2", 3)}, 0.3);', [(st("s2"), "whoosh-weich"), (cap("s2", 3), "pop")])

S("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Deine Meinung") + icon_gross("i3", "💬", 0, 600, 240, OR, True)
  + chip("c3a", "🛒 am 1. Tag kaufen", GRUEN, 900, 54) + chip("c3b", "⏳ erst mal abwarten", OR, 1020, 54),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.1); pop("#c3a", {cap("s3", 1)}); pop("#c3b", {cap("s3", 2)});',
  [(st("s3"), "handy-benachrichtigung"), (cap("s3", 1), "pop")])

S("s4", "frei-frankfurt-staedel", titel_zeile("t4", "Folg uns") + icon_gross("i4", "🔔", 0, 620, 260, OR, True) + chip("c4", "+ Folgen", OR, 940, 70),
  lambda a, d: f'pop("#t4", {a}); pop("#i4", {a}); tl.fromTo("#i4", {{ rotation: -18 }}, {{ rotation: 18, duration: 0.14, yoyo: true, repeat: 5 }}, {a} + 0.3); slam("#c4", {cap("s4", 0)} + 0.4);',
  [(st("s4"), "swipe"), (st("s4") + 0.3, "handy-benachrichtigung")])

S("s5", "wallstreet", titel_zeile("t5", "Preis pro Aktie") + tz("n5", "70 – 78 $", 680, 170, "glow-o") + chip("c5", "Preisspanne", OR, 920, 56),
  lambda a, d: f'pop("#t5", {a}); slam("#n5", {cap("s5", 2)}); pop("#c5", {cap("s5", 2)} + 0.3);', [(st("s5"), "swipe"), (cap("s5", 2), "kasse")])

S("s6", "handelssaal", titel_zeile("t6", "So viele Aktien") + tz("n6", "825 Mio.", 600, 140, "glow-o") + raster("r6", 300, 800, 10, 6, 40, 8, AN),
  lambda a, d: f'pop("#t6", {a}); slam("#n6", {cap("s6", 1)}); tl.fromTo("#r6 .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.01 }}, {cap("s6", 1)} + 0.3);',
  [(st("s6"), "zaehler")])

S("s7", "frei-euro", titel_zeile("t7", "Das Geld") + icon_gross("i7", "💰", 0, 600, 240, GRUEN, True) + tz("n7", "≈ 64 Mrd. $", 880, 140, "glow-g"),
  lambda a, d: f'pop("#t7", {a}); pop("#i7", {cap("s7", 1)}); slam("#n7", {cap("s7", 1)} + 0.4);', [(st("s7"), "whoosh-weich"), (cap("s7", 1) + 0.4, "kasse")])

BASIS = 1150
BAR = [("SpaceX", 75, "#2b6cb0", "75 Mrd."), ("Anthropic", 64, AN, "64 Mrd."), ("Aramco", 29.4, GRAU, "29 Mrd.")]
B8 = "".join(f'<div id="b8{i}" style="position:absolute;left:{110 + i * 300}px;top:{BASIS - int(460 * v / 75)}px;width:240px;height:{int(460 * v / 75)}px;border-radius:16px 16px 4px 4px;'
             f'background:linear-gradient(180deg,{f},{f}88);box-shadow:0 0 40px {f}77;transform-origin:50% 100%;z-index:3"></div>'
             f'<div id="b8t{i}" class="mono" style="position:absolute;left:{70 + i * 300}px;width:320px;top:{BASIS - int(460 * v / 75) - 66}px;text-align:center;font-size:42px;color:{f};z-index:5">{w}</div>'
             f'<div class="mono" style="position:absolute;left:{70 + i * 300}px;width:320px;top:{BASIS + 14}px;text-align:center;font-size:32px;color:#fff;z-index:4">{n}</div>'
             for i, (n, v, f, w) in enumerate(BAR))
S("s8", "wallstreet", titel_zeile("t8", "Größte Börsengänge") + B8 + stempel("s8x", "PLATZ 2", 400, 1215, AN, 46, -5),
  lambda a, d: (f'pop("#t8", {a});' + "".join(f' tl.fromTo("#b8{i}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {t_}); pop("#b8t{i}", {t_} + 0.3);'
                                               for i, t_ in enumerate([cap("s8", 2), cap("s8", 0), st("s9") + 0.5])) + f' stempeln("#s8x", {cap("s8", 1)});'),
  [(st("s8"), "swipe"), (cap("s8", 1), "stempel"), (st("s9") + 0.5, "pop")], bis="s10")

S("s10", "handelssaal", titel_zeile("t10", "Hier wird gehandelt") + logo("l10", "nasdaq.svg", 640, 560, glow="#0996c7", pad=30) + kalender("k10", "DO", "19.11.", 400, 900, 280, AN),
  lambda a, d: f'pop("#t10", {a}); pop("#l10", {cap("s10", 2)}); pop("#k10", {cap("s10", 2)} + 0.4);', [(st("s10"), "boersenglocke")])

S("s11", "frei-code-css", titel_zeile("t11", "Warum so viel?", farbe=GELB) + icon_gross("i11", "🤔", 0, 640, 300, GELB, True),
  lambda a, d: f'pop("#t11", {a}); slam("#i11", {a} + 0.2);', [(st("s11"), "spannung")])

S("s12", "frei-code-monitor", titel_zeile("t12", "Rasantes Wachstum") + icon_gross("i12", "🚀", 0, 640, 300, AN, True),
  lambda a, d: f'pop("#t12", {a}); tl.fromTo("#i12", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "back.out(1.6)" }}, {a});', [(st("s12"), "whoosh-schnell")])

S("s13", "frei-frankfurt-nacht", titel_zeile("t13", "Große Geldgeber") + logo("l13a", "google.svg", 640, 380, 80, pad=26, glow="#4285f4") + logo("l13b", "amazon.svg", 660, 380, 620, pad=26, glow="#ff9900")
  + chip("c13", "u. a.", GRAU, 960, 44),
  lambda a, d: f'pop("#t13", {a}); pop("#l13a", {cap("s13", 2)}); pop("#l13b", {cap("s13", 2)} + 0.3); pop("#c13", {cap("s13", 1)});', [(st("s13"), "swipe"), (cap("s13", 2), "pop")])

S("s14", "frei-50euro", titel_zeile("t14", "3. Quartal 2026") + tz("n14", "≈ 17 Mrd. $", 700, 150, "glow-g") + chip("c14", "Umsatz in nur 3 Monaten", GRUEN, 940, 54),
  lambda a, d: f'pop("#t14", {a}); slam("#n14", {cap("s14", 1)}); pop("#c14", {cap("s14", 2)});', [(st("s14"), "kasse")])

S("s15", "frei-euro", titel_zeile("t15", "Aufs Jahr gerechnet") + tz("n15", "≈ 81 Mrd. $", 700, 150, "glow-g") + quelle("q15", "laut Börsenprospekt · Stand Ende Okt. 2026", 920),
  lambda a, d: f'pop("#t15", {a}); slam("#n15", {cap("s15", 2)}); pop("#q15", {cap("s15", 1)});', [(st("s15"), "zaehler"), (cap("s15", 2), "kasse")])

S("s16", "frei-code-css", titel_zeile("t16", "Wer zahlt?") + icon_gross("i16", "🏢", 140, 640, 220, OR) + icon_gross("i16b", "💻", 620, 640, 220, OR) + chip("c16", "Firmen · zum Programmieren", OR, 940, 52),
  lambda a, d: f'pop("#t16", {a}); pop("#i16", {cap("s16", 0)}); pop("#i16b", {cap("s16", 2)}); slam("#c16", {cap("s16", 2)} + 0.3);', [(st("s16"), "swipe")])

S("s17", "frei-code-monitor", titel_zeile("t17", "Die Rivalen") + logo("l17a", "claude.svg", 640, 380, 80, pad=20, glow=AN) + tz("v17", "vs.", 690, 80)
  + logo("l17b", "openai.svg", 650, 380, 620, pad=20, glow="#fff"),
  lambda a, d: f'pop("#t17", {a}); pop("#l17a", {a} + 0.1); pop("#v17", {cap("s17", 2)} - 0.3); pop("#l17b", {cap("s17", 2)});', [(st("s17"), "swipe"), (cap("s17", 2), "nv-boom-kurz")])

S("s18", "handelssaal", titel_zeile("t18", "Aber …", farbe=ROT) + stempel("s18x", "NOCH VERLUSTE", 250, 640, ROT, 62, -5)
  + icon_gross("i18", "🏭", 140, 860, 200, GRAU) + icon_gross("i18b", "💾", 620, 860, 200, GRAU) + chip("c18", "Rechenzentren + Chips = Milliarden", ROT, 1110, 44),
  lambda a, d: f'pop("#t18", {a}); stempeln("#s18x", {cap("s18", 1)}); pop("#i18", {cap("s18", 2)}); pop("#i18b", {cap("s18", 3)}); pop("#c18", {cap("s18", 3)} + 0.3);',
  [(st("s18"), "alarm"), (cap("s18", 1), "stempel")])

S("s19", "wallstreet", titel_zeile("t19", "Preis gesunken") + icon_gross("i19", "📉", 0, 640, 300, ROT, True),
  lambda a, d: f'pop("#t19", {a}); slam("#i19", {cap("s19", 1)});', [(st("s19"), "kurve-runter")])

S("s20", "handelssaal", titel_zeile("t20", "Erwarteter Wert") + balken2("b20", "2 Bio. $", "1,4 Bio. $", 2000, 1400, GRAU, AN, unten=("Anfang Okt.", "jetzt")),
  lambda a, d: f'pop("#t20", {a});' + balken2_js("b20", cap("s20", 1), cap("s20", 3)), [(st("s20"), "swipe"), (cap("s20", 3), "kurve-runter")])

S("s21", "frei-sitzung", titel_zeile("t21", "Die große Frage", farbe=GELB) + tz("n21", "Am 1. Tag kaufen?", 720, 96, "glow-o") + icon_gross("i21", "❓", 0, 880, 200, GELB, True),
  lambda a, d: f'pop("#t21", {a}); slam("#n21", {cap("s21", 1)}); pop("#i21", {cap("s21", 2)});', [(st("s21"), "spannung")])

S("s22", "frei-sitzung", titel_zeile("t22", "Die Geschichte") + icon_gross("i22", "⚖️", 0, 640, 280, OR, True),
  lambda a, d: f'pop("#t22", {a}); pop("#i22", {cap("s22", 1)}); tl.fromTo("#i22", {{ rotation: -10 }}, {{ rotation: 10, duration: 0.4, yoyo: true, repeat: 3 }}, {cap("s22", 1)} + 0.3);',
  [(st("s22"), "whoosh-weich")])

S("s23", "frei-miami-omni", titel_zeile("t23", "SpaceX · Juni 2026") + logo("l23", "spacex.png", 640, 520, glow="#2b6cb0", pad=20) + tz("n23", "+19 %", 860, 170, "glow-g") + chip("c23", "am 1. Tag", GRUEN, 1080, 52),
  lambda a, d: f'pop("#t23", {a}); pop("#l23", {a} + 0.1); slam("#n23", {cap("s23", 1)}); pop("#c23", {cap("s23", 1)} + 0.3);', [(st("s23"), "swipe"), (cap("s23", 1), "kurve-hoch")])

K24 = linie("ku24", [0.9, 0.75, 0.6, 0.45, 0.3, 0.2], 150, 820, 780, 300, ROT, punkte=[(0, "38 $"), (5, "≈ 19 $")])
S("s24", "wallstreet", titel_zeile("t24", "Facebook · 2012") + logo("l24", "meta.png", 600, 440, glow="#0866ff", pad=20) + K24 + tz("n24", "≈ −50 %", 1130, 90, "glow-r"),
  lambda a, d: (f'pop("#t24", {a}); pop("#l24", {cap("s24", 0)}); pop("#ku24-w0", {cap("s24", 2)}); draw("#ku24-p", {cap("s24", 3)}, 1.4);'
                f' tl.fromTo("#ku24-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s24", 4)}); pop("#ku24-w1", {cap("s24", 5)}); slam("#n24", {cap("s24", 5)} + 0.3);'),
  [(st("s24"), "swipe"), (cap("s24", 3), "kurve-runter")])

K25 = linie("ku25", [0.05, 0.03, 0.12, 0.25, 0.4, 0.55, 0.75, 0.95], 150, 760, 780, 380, GRUEN, punkte=[(1, "Tief"), (7, "später")])
S("s25", "handelssaal", titel_zeile("t25", "Wer durchhielt …") + K25 + stempel("s25x", "REICH BELOHNT", 300, 1180, GRUEN, 52, -5),
  lambda a, d: f'pop("#t25", {a}); draw("#ku25-p", {a} + 0.1, 1.8); pop("#ku25-w0", {a} + 0.3); pop("#ku25-w1", {cap("s25", 2)}); stempeln("#s25x", {cap("s25", 2)} + 0.3);',
  [(st("s25"), "kurve-hoch"), (cap("s25", 2) + 0.3, "stempel")])

S("s26", "frei-frankfurt-nacht", titel_zeile("t26", "Heute") + logo("l26", "meta.png", 640, 560, glow="#0866ff", pad=24) + chip("c26", "eine der wertvollsten Firmen der Welt", OR, 900, 42),
  lambda a, d: f'pop("#t26", {a}); pop("#l26", {cap("s26", 0)}); slam("#c26", {cap("s26", 3)});', [(st("s26"), "whoosh-weich")])

S("s27", "frei-frankfurt-staedel", titel_zeile("t27", "Und für dich?") + flagge("f27", "flagge-deutschland", 340, 620, 400, -3) + icon_gross("i27", "🔒", 0, 900, 160, OR, True)
  + chip("c27", "kaufen erst ab Börsenhandel", OR, 1100, 50),
  lambda a, d: f'pop("#t27", {a}); pop("#f27", {cap("s27", 1)}); pop("#i27", {cap("s27", 2)}); slam("#c27", {cap("s27", 4)});', [(st("s27"), "swipe")])

S("s28", "handelssaal", titel_zeile("t28", "Die ersten Stunden") + icon_gross("i28", "🎢", 0, 640, 300, ROT, True),
  lambda a, d: f'pop("#t28", {a}); slam("#i28", {cap("s28", 1)}); shake("#i28", {cap("s28", 2)});', [(st("s28"), "spannung"), (cap("s28", 2), "whoosh-schnell")])

S("s29", "wallstreet", titel_zeile("t29", "Worauf viele achten") + tz("n29", "3", 640, 320, "glow-o"),
  lambda a, d: f'pop("#t29", {a}); slam("#n29", {a} + 0.3);', [(st("s29"), "nv-boom-kurz")])


def tipp(sid, n, icon, kopf, text, hg, sfx):
    S(sid, hg, titel_zeile(f"t{sid}", f"Nr. {n}", farbe=GRUEN) + icon_gross(f"i{sid}", icon, 0, 610, 220, GRUEN, True)
      + (f'<div id="k{sid}" style="position:absolute;left:120px;top:880px;width:840px;padding:30px 38px;border-radius:26px;background:#14181bee;border:5px solid {GRUEN};'
         f'box-shadow:0 0 40px {GRUEN}55;z-index:4"><div class="mono" style="font-size:28px;color:{GRUEN};letter-spacing:2px">{kopf}</div>'
         f'<div style="font-weight:900;font-size:52px;color:#fff;line-height:1.1;margin-top:8px">{text}</div></div>'),
      lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#i{s}", {a} + 0.1); pop("#k{s}", {cap(s, 0)} + 0.3);', [(st(sid), "swipe"), (cap(sid, 0) + 0.3, sfx)])


tipp("s30", 1, "⏱️", "NICHT SOFORT", "warten, bis sich<br/>der Kurs beruhigt", "frei-code-monitor", "uhr-tickt")
tipp("s31", 2, "🎯", "LIMIT SETZEN", "nicht teurer kaufen<br/>als geplant", "frei-code-css", "klick")
tipp("s32", 3, "🏦", "NUR FREIES GELD", "das man einige Jahre<br/>nicht braucht", "frei-euro", "muenzen-klimpern")

S("s33", "frei-sitzung", titel_zeile("t33", "Merk dir") + stempel("s33x", "NAME ≠ KAUFGRUND", 220, 740, OR, 52, -5),
  lambda a, d: f'pop("#t33", {a}); stempeln("#s33x", {cap("s33", 1)});', [(st("s33"), "stempel")])

S("s34", "frei-frankfurt-nacht", titel_zeile("t34", "Übrigens") + icon_gross("i34", "🧺", 0, 620, 240, OR, True) + chip("c34", "Welt-ETF: Anthropic erst später drin", OR, 940, 46),
  lambda a, d: f'pop("#t34", {a}); pop("#i34", {cap("s34", 0)}); slam("#c34", {cap("s34", 2)});', [(st("s34"), "klick")])

S("s35", "frei-code-monitor", titel_zeile("t35", "Donnerstag") + kalender("k35", "NOV", "19", 390, 620, 300, AN) + chip("c35", "wir halten dich auf dem Laufenden", OR, 1000, 46),
  lambda a, d: f'pop("#t35", {a}); pop("#k35", {a} + 0.1); slam("#c35", {cap("s35", 1)});', [(st("s35"), "uhr-tickt")])

S("s36", "wallstreet", titel_zeile("t36", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
  lambda a, d: f'pop("#t36", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
  [(st("s36"), "zeitung")])

K.SZ.append((0.0, K.dauer, news_kopf("15.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    print(bildquellen(HERE))
