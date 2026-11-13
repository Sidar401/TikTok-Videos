#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News-Format v2, 2:28): Die Commerzbank wird italienisch – UniCredit-Übernahme. Kein Laufband (keine Börsen-Eilmeldung)."""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (bildquellen, GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, donut, flagge, foto_gross, hand, hintergrund_foto, icon_gross,  # noqa: E402
                         kalender, kasten, kit_assets, kit_hg, news_kopf, pfeil, quelle, stempel, titel_zeile, unterstrich, vergleich,
                         wechsel_js, zettel, zoom_js)
from glow_short import build, chip, t, zeiten  # noqa: E402

CB = "#FFCC00"
UC = "#E2001A"
kit_assets(HERE, ["flagge-italien", "flagge-deutschland", "flagge-eu", "ezb", "comdirect"])
for f in ("commerzbank.png", "commerzbank-symbol.png", "hvb.png", "unicredit-symbol.png"):
    shutil.copy(W / "brand/logos" / f, HERE / "assets/logos" / f)
FQ = json.loads((W / "brand/fotos/quellen.json").read_text())
(HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)
for f in ("olaf-scholz.jpg", "andrea-orcel.jpg"):
    shutil.copy(W / "brand/fotos" / f, HERE / "assets/fotos" / f)
cap, st, en, DAUER = zeiten(HERE)
kit_hg(HERE, ["frei-commerzbank-turm", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-mailand-porta-nuova", "frei-50euro", "handelssaal", "frei-sitzung", "wallstreet", "wallstreet"])
SZ, SFX = [], []
REIHE = [f"s{i}" for i in range(1, 34)]


def szene(sid, hg, html, js, sfx=()):
    i = len(SZ)
    a = st(sid)
    b = st(REIHE[REIHE.index(sid) + 1]) if sid != REIHE[-1] else DAUER
    SZ.append((a, b, hintergrund_foto(f"bg{i}", hg) + html,
               lambda a_, d_, j=js, k=i: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + zoom_js(f"#bg{k}", a_, d_, 1.12)))
    SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def logo(id_, datei, y, w, x=None, glow=CB, pad=26):
    """Original-Logo auf weißer Karte (Wikimedia, gemeinfrei)."""
    pos = f"left:{x}px" if x is not None else f"left:{(1080 - w) // 2}px"
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;width:{w}px;padding:{pad}px;border-radius:24px;background:#fff;'
            f'box-shadow:0 0 60px {glow}66, 0 30px 50px #000;z-index:4"><img src="assets/logos/{datei}" alt="" style="width:100%;display:block"/></div>')


def uc_marke(id_, y, h=110, x=None, schild=None):
    """UniCredit: Original-Symbol + Wortmarke."""
    pos = f"left:{x}px" if x is not None else "left:0;width:1080px;justify-content:center"
    s = (f'<span class="mono" style="display:inline-block;padding:6px 18px;border-radius:12px;background:{UC};color:#fff;font-size:{h * 0.38:.0f}px">{schild}</span>' if schild else "")
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;display:flex;align-items:center;gap:{h * 0.22:.0f}px;z-index:4">'
            f'<img src="assets/logos/unicredit-symbol.png" alt="" style="height:{h}px;filter:drop-shadow(0 0 18px {UC}aa)"/>'
            f'<span style="font-weight:800;font-size:{h * 0.7:.0f}px;color:#fff;letter-spacing:-1px;text-shadow:0 0 20px #ffffff44">UniCredit</span>{s}</div>')


def foto(key, id_, x, y, w, h, farbe=OR):
    return foto_gross(id_, f"assets/fotos/{key}.jpg", x, y, w, h, FQ[f"{key}.jpg"]["einblenden"], farbe)


def kapitel(sid, n, titel, hg, gr=92):
    szene(sid, hg, tz(f"k{n}a", f"TEIL {n}", 600, 100, "glow-o") + tz(f"k{n}b", f'<span class="box">{titel}</span>', 750, gr)
          + unterstrich(f"k{n}u", 290, 900, 500, GELB),
          lambda a, d: f'slam("#k{n}a", {a}); pop("#k{n}b", {a} + 0.25); draw("#k{n}u-p", {a} + 0.6, 0.4); flash({a}, 0.4);',
          [(st(sid), "nv-dun-dun-dun" if n == 1 else "nv-boom-kurz")])


# ---------------- Intro ----------------
szene("s1", "frei-commerzbank-turm", KIT_CSS + titel_zeile("t1", "⚡ Übernahme", farbe=ROT) + logo("l1", "commerzbank.png", 610, 760)
      + pfeil("p1", 540, 780, 540, 900, 0.0, "#fff", 10) + flagge("f1", "flagge-italien", 390, 920, 300, -4) + stempel("s1x", "BALD ITALIENISCH?", 170, 1150, ROT, 64, -5),
      lambda a, d: (KIT_JS + f' pop("#t1", {a}); pop("#l1", {a}); draw("#p1-p", {cap("s1", 1)}, 0.3); pop("#p1-k", {cap("s1", 1)} + 0.25);'
                    f' pop("#f1", {cap("s1", 1)} + 0.3); stempeln("#s1x", {cap("s1", 1)} + 0.8);'),
      [(0.0, "eilmeldung"), (cap("s1", 1) + 0.3, "whoosh-schnell"), (cap("s1", 1) + 0.8, "stempel")])

szene("s2", "frei-frankfurt-nacht", titel_zeile("t2", "Commerzbank") + icon_gross("i2", "👥", 0, 600, 220, CB, True)
      + tz("n2", "≈ 11 Mio.", 840, 150, "glow-o") + quelle("q2", "Privat- und Unternehmerkunden in Deutschland", 1020) + stempel("s2x", "VOR DER ÜBERNAHME", 190, 1110, ROT, 56, -4),
      lambda a, d: f'pop("#t2", {a}); pop("#i2", {cap("s2", 1)}); slam("#n2", {cap("s2", 1)} + 0.3); pop("#q2", {cap("s2", 2)}); stempeln("#s2x", {cap("s2", 3)});',
      [(st("s2"), "whoosh-weich"), (cap("s2", 1) + 0.3, "zaehler"), (cap("s2", 3), "stempel")])

szene("s3", "frei-frankfurt-staedel", titel_zeile("t3", "Folg uns") + icon_gross("i3", "🔔", 0, 620, 260, OR, True) + chip("c3", "+ Folgen", OR, 940, 70)
      + quelle("q3", "jeden Tag die wichtigsten Geld-News", 1080),
      lambda a, d: (f'pop("#t3", {a}); pop("#i3", {a}); tl.fromTo("#i3", {{ rotation: -18 }}, {{ rotation: 18, duration: 0.14, yoyo: true, repeat: 5 }}, {a} + 0.3);'
                    f' slam("#c3", {cap("s3", 0)} + 0.4); pop("#q3", {cap("s3", 1)});'),
      [(st("s3"), "swipe"), (st("s3") + 0.3, "handy-benachrichtigung")])

szene("s4", "wallstreet", titel_zeile("t4", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
      lambda a, d: f'pop("#t4", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
      [(st("s4"), "zeitung")])

AG = [("① Wie kam es dazu?", 1, OR), ("② Wer entscheidet?", 2, "#4d8ff0"), ("③ Dein Konto", 3, GRUEN), ("④ Die Aktie", 4, CB)]
szene("s5", "frei-commerzbank-turm", titel_zeile("t5", "In diesem Video") + "".join(kasten(f"ag{i}", txt, 150, 610 + i * 150, 780, 120, f, 48) for i, (txt, _, f) in enumerate(AG)),
      lambda a, d: f'pop("#t5", {a});' + "".join(f' pop("#ag{i}", {cap("s5", c)});' for i, (_, c, _) in enumerate(AG)),
      [(st("s5"), "whoosh-weich")] + [(cap("s5", c), "klick") for _, c, _ in AG])

# ---------------- Teil 1 ----------------
kapitel("s6", 1, "Wie kam es dazu?", "frei-frankfurt-staedel")

szene("s7", "handelssaal", titel_zeile("t7", "Finanzkrise") + kalender("k7", "KRISE", "2008", 110, 620, 300, ROT) + icon_gross("i7", "🛟", 620, 620, 260, OR)
      + tz("n7", "18,2 Mrd. €", 960, 130, "glow-o") + quelle("q7", "Staatshilfen 2008/09 · Bankenrettungsfonds SoFFin", 1130),
      lambda a, d: f'pop("#t7", {a}); pop("#k7", {cap("s7", 0)}); pop("#i7", {cap("s7", 2)}); slam("#n7", {cap("s7", 3)}); pop("#q7", {cap("s7", 3)} + 0.4);',
      [(st("s7"), "alarm"), (cap("s7", 3), "kasse")])

szene("s8", "frei-frankfurt-nacht", titel_zeile("t8", "Der Staat steigt ein") + flagge("f8", "flagge-deutschland", 340, 620, 400, -3) + chip("c8", "größter Aktionär", OR, 940, 66),
      lambda a, d: f'pop("#t8", {a}); pop("#f8", {cap("s8", 0)}); slam("#c8", {cap("s8", 1)});',
      [(st("s8"), "swipe"), (cap("s8", 1), "pop")])

szene("s9", "wallstreet", titel_zeile("t9", "September 2024") + kalender("k9", "SEP", "2024", 90, 610, 250, ROT) + kasten("b9", "4,5 %<br/>Aktienpaket", 400, 640, 300, 200, OR, 48)
      + pfeil("p9", 720, 740, 820, 740, 0.0, "#fff", 9) + f'<img id="u9" src="assets/logos/unicredit-symbol.png" alt="" style="position:absolute;left:840px;top:660px;height:160px;z-index:4;filter:drop-shadow(0 0 24px {UC})"/>'
      + uc_marke("m9", 960, 110) + quelle("q9", "Verkauf durch den Bund · 11.09.2024", 1110),
      lambda a, d: (f'pop("#t9", {a}); pop("#k9", {a} + 0.1); pop("#b9", {cap("s9", 1)}); draw("#p9-p", {cap("s9", 2)}, 0.3); pop("#p9-k", {cap("s9", 2)} + 0.25);'
                    f' slam("#u9", {cap("s9", 3)}); pop("#m9", {cap("s9", 4)}); pop("#q9", {cap("s9", 4)} + 0.3); flash({cap("s9", 3)}, 0.4);'),
      [(st("s9"), "whoosh-weich"), (cap("s9", 2), "whoosh-schnell"), (cap("s9", 3), "bass-schlag")])

BS = [(150, 120, "2024"), (420, 260, "2025"), (690, 420, "2026")]
szene("s10", "handelssaal", titel_zeile("t10", "Immer mehr Aktien") + "".join(
      f'<div id="b10{i}" style="position:absolute;left:{x}px;top:{1150 - h}px;width:240px;height:{h}px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{UC},{UC}88);box-shadow:0 0 40px {UC}77;transform-origin:50% 100%;z-index:3"></div>'
      f'<div class="mono" style="position:absolute;left:{x}px;width:240px;top:1170px;text-align:center;font-size:34px;color:#ffffffcc;z-index:4">{j}</div>' for i, (x, h, j) in enumerate(BS))
      + icon_gross("i10", "🛒", 120, 600, 160),
      lambda a, d: f'pop("#t10", {a}); pop("#i10", {a} + 0.1);' + "".join(f' tl.fromTo("#b10{i}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {cap("s10", i)});' for i in range(3)),
      [(st("s10"), "swipe"), (cap("s10", 1), "kurve-hoch"), (cap("s10", 2), "muenzen-klimpern")])

szene("s11", "frei-sitzung", titel_zeile("t11", "Olaf Scholz") + foto("olaf-scholz", "f11", 290, 600, 500, 460, ROT)
      + zettel("z11", "„unfreundliche Attacke“", 170, 1110, 740, 60, GELB, -3) + quelle("q11", "damals Bundeskanzler · Sept. 2024", 570),
      lambda a, d: (f'pop("#t11", {a}); pop("#f11", {cap("s11", 0)} + 0.3); pop("#q11", {cap("s11", 1)}); flash({cap("s11", 0)} + 0.3, 0.4);'
                    f' tl.fromTo("#z11", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {cap("s11", 2)});'),
      [(st("s11"), "kamera-blitz"), (cap("s11", 2), "nv-falsch-buzzer")])

# ---------------- Teil 2 ----------------
kapitel("s12", 2, "Wer hat wie viel?", "frei-mailand-porta-nuova")

szene("s13", "frei-mailand-porta-nuova", titel_zeile("t13", "Anteil UniCredit") + donut("d13", 540, 850, 220, [(0.476, UC)], 80) + tz("n13", "47,6 %", 800, 100, "glow-r")
      + uc_marke("m13", 1120, 80) + quelle("q13", "Anteil an den Aktien", 1230),
      lambda a, d: f'pop("#t13", {a}); draw("#d13-0", {cap("s13", 0)}, 1.0); slam("#n13", {cap("s13", 1)}); pop("#m13", {cap("s13", 0)}); pop("#q13", {cap("s13", 1)});',
      [(st("s13"), "whoosh-weich"), (cap("s13", 0), "zaehler"), (cap("s13", 1), "bass-schlag")])

BAR = (f'<div id="g14" style="position:absolute;left:120px;top:780px;width:840px;height:110px;border-radius:55px;background:#1b1f22;border:5px solid #ffffff33;overflow:hidden;z-index:3">'
       f'<div id="g14f" style="width:49.65%;height:100%;background:linear-gradient(90deg,{UC}aa,{UC});box-shadow:0 0 40px {UC};transform-origin:0 50%"></div></div>'
       f'<div style="position:absolute;left:537px;top:750px;width:6px;height:170px;background:#fff;z-index:4"></div>'
       f'<div class="mono" style="position:absolute;left:440px;width:200px;top:930px;text-align:center;font-size:32px;color:#fff;z-index:4">50 %</div>')
szene("s14", "frei-mailand-porta-nuova", titel_zeile("t14", "Bei den Stimmen") + BAR + tz("n14", "49,65 %", 600, 110, "glow-r")
      + hand("h14", "fast die Hälfte!", 540, 1010, 70, GELB, -3, True) + quelle("q14", "eigene Aktien der Commerzbank haben kein Stimmrecht", 1140),
      lambda a, d: (f'pop("#t14", {a}); pop("#g14", {a}); pop("#q14", {cap("s14", 1)}); tl.fromTo("#g14f", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2, ease: "power2.out" }}, {cap("s14", 2)});'
                    f' slam("#n14", {cap("s14", 3)}); pop("#h14", {cap("s14", 3)} + 0.4);'),
      [(st("s14"), "swipe"), (cap("s14", 2), "spannung"), (cap("s14", 3), "bass-schlag")])

szene("s15", "frei-frankfurt-staedel", titel_zeile("t15", "Und der Staat?") + flagge("f15", "flagge-deutschland", 340, 620, 400, -3) + tz("n15", "≈ 13 %", 900, 160, "glow-o"),
      lambda a, d: f'pop("#t15", {a}); pop("#f15", {cap("s15", 0)}); slam("#n15", {cap("s15", 1)});',
      [(st("s15"), "whoosh-weich"), (cap("s15", 1), "kurve-runter")])

szene("s16", "frei-frankfurt-staedel", titel_zeile("t16", "EZB sagt ja") + logo("l16", "ezb.svg", 620, 460, glow="#4d8ff0") + stempel("s16x", "ZUGESTIMMT ✓", 250, 1000, GRUEN, 70, -5)
      + quelle("q16", "Oktober 2026", 1150),
      lambda a, d: f'pop("#t16", {a}); pop("#l16", {cap("s16", 0)}); stempeln("#s16x", {cap("s16", 1)}); pop("#q16", {cap("s16", 1)} + 0.3);',
      [(st("s16"), "swipe"), (cap("s16", 1), "stempel")])

szene("s17", "frei-sitzung", titel_zeile("t17", "Die Entscheidung") + kalender("k17", "NOV", "16", 120, 620, 300, ROT) + flagge("f17", "flagge-eu", 560, 650, 400, 3)
      + chip("c17", "Europäische Kommission", "#4d8ff0", 1060, 56),
      lambda a, d: f'pop("#t17", {a}); pop("#k17", {cap("s17", 0)}); pop("#f17", {cap("s17", 2)}); slam("#c17", {cap("s17", 2)} + 0.3);',
      [(st("s17"), "uhr-tickt"), (cap("s17", 2), "hammer")])

szene("s18", "frei-mailand-porta-nuova", titel_zeile("t18", "Grünes Licht?") + icon_gross("i18", "🚦", 120, 620, 260, GRUEN) + kalender("k18", "ANFANG", "2027", 620, 620, 300, UC)
      + stempel("s18x", "KONTROLLE", 280, 1050, UC, 80, -5),
      lambda a, d: f'pop("#t18", {a}); pop("#i18", {cap("s18", 0)}); pop("#k18", {cap("s18", 2)}); stempeln("#s18x", {cap("s18", 2)} + 0.6);',
      [(st("s18"), "swipe"), (cap("s18", 0), "richtig"), (cap("s18", 2) + 0.6, "stempel")])

szene("s19", "frei-sitzung", titel_zeile("t19", "Berlin ist dagegen") + flagge("f19", "flagge-deutschland", 120, 640, 320, -4) + icon_gross("i19", "🙅", 600, 610, 250, ROT)
      + stempel("s19x", "„FEINDLICH“", 260, 960, ROT, 80, -5) + chip("c19", "aber kaum noch aufzuhalten", OR, 1140, 50),
      lambda a, d: f'pop("#t19", {a}); pop("#f19", {cap("s19", 0)}); pop("#i19", {cap("s19", 1)}); stempeln("#s19x", {cap("s19", 2)}); slam("#c19", {cap("s19", 3)});',
      [(st("s19"), "whoosh-weich"), (cap("s19", 2), "stempel"), (cap("s19", 3), "nv-falsch-buzzer")])

# ---------------- Teil 3 ----------------
kapitel("s20", 3, "Was heißt das für dich?", "frei-commerzbank-turm", 72)

OK3 = [("Konto", 3), ("IBAN", 4), ("Karte", 4)]
szene("s21", "frei-commerzbank-turm", titel_zeile("t21", "Dein Konto") + logo("l21a", "commerzbank.png", 610, 440, x=80, pad=18) + logo("l21b", "comdirect.svg", 610, 400, x=600, glow=CB, pad=0)
      + "".join(kasten(f"ok{i}", f"✅ {n}", 100 + i * 300, 830, 280, 130, GRUEN, 50) for i, (n, _) in enumerate(OK3))
      + stempel("s21x", "BLEIBT ERST MAL", 220, 1060, GRUEN, 64, -4),
      lambda a, d: (f'pop("#t21", {a}); pop("#l21a", {cap("s21", 1)}); pop("#l21b", {cap("s21", 2)});'
                    + "".join(f' pop("#ok{i}", {cap("s21", c)} + {i * 0.4});' for i, (_, c) in enumerate(OK3)) + f' stempeln("#s21x", {cap("s21", 5)});'),
      [(st("s21"), "swipe"), (cap("s21", 3), "richtig"), (cap("s21", 5), "stempel")])

szene("s22", "frei-frankfurt-nacht", titel_zeile("t22", "Dein Erspartes") + icon_gross("i22", "🛡️", 0, 600, 240, GRUEN, True) + tz("n22", "100.000 €", 880, 140, "glow-g")
      + flagge("f22", "flagge-eu", 60, 640, 220, -6) + quelle("q22", "gesetzliche Einlagensicherung · pro Kunde und Bank", 1060),
      lambda a, d: f'pop("#t22", {a}); pop("#i22", {cap("s22", 0)}); pop("#f22", {cap("s22", 2)}); slam("#n22", {cap("s22", 3)}); pop("#q22", {cap("s22", 3)} + 0.4);',
      [(st("s22"), "whoosh-weich"), (cap("s22", 3), "kasse")])

szene("s23", "frei-frankfurt-staedel", titel_zeile("t23", "Aber langfristig …", farbe=GELB) + icon_gross("i23", "⏳", 0, 640, 300, GELB, True),
      lambda a, d: f'pop("#t23", {a}); slam("#i23", {cap("s23", 0)} + 0.2); tl.fromTo("#i23", {{ rotation: 0 }}, {{ rotation: 180, duration: 0.8 }}, {cap("s23", 1)});',
      [(st("s23"), "uhr-tickt")])

szene("s24", "frei-50euro", titel_zeile("t24", "Die HypoVereinsbank") + logo("l24a", "hvb.png", 600, 760, glow=UC, pad=20) + tz("pl24", "+", 760, 110)
      + logo("l24b", "commerzbank.png", 900, 760, pad=20) + stempel("s24x", "ZUSAMMENLEGUNG?", 190, 1100, OR, 64, -5),
      lambda a, d: (f'pop("#t24", {a}); pop("#l24a", {cap("s24", 2)}); pop("#pl24", {cap("s24", 3)}); pop("#l24b", {cap("s24", 4)}); stempeln("#s24x", {cap("s24", 5)});'),
      [(st("s24"), "whoosh-weich"), (cap("s24", 2), "pop"), (cap("s24", 5), "stempel")])

szene("s25", "frei-commerzbank-turm", titel_zeile("t25", "In Gefahr") + kasten("k25a", "🏦 Filialen", 80, 640, 440, 200, ROT, 56) + kasten("k25b", "👔 Arbeits&shy;plätze", 560, 640, 440, 200, ROT, 56)
      + stempel("s25x", "IN GEFAHR", 330, 940, ROT, 80, -6),
      lambda a, d: f'pop("#t25", {a}); slam("#k25a", {cap("s25", 1)}); slam("#k25b", {cap("s25", 2)}); stempeln("#s25x", {cap("s25", 3)});',
      [(st("s25"), "swipe"), (cap("s25", 1), "tuer-zu"), (cap("s25", 3), "stempel")])

szene("s26", "frei-sitzung", titel_zeile("t26", "Wie viele Jobs?") + vergleich("v26", "LAUT BERICHTEN", "mehrere<br/>tausend", "GEWERKSCHAFTEN", "bis zu<br/>15.000", OR, ROT, 620, 340)
      + quelle("q26", "Schätzungen · Medienberichte 2026", 1000),
      lambda a, d: f'pop("#t26", {a}); pop("#v26-l", {cap("s26", 1)}); pop("#v26-r", {cap("s26", 3)}); pop("#q26", {cap("s26", 3)} + 0.4);',
      [(st("s26"), "zeitung"), (cap("s26", 3), "alarm")])

szene("s27", "frei-frankfurt-nacht", titel_zeile("t27", "Deine Meinung") + icon_gross("i27", "💬", 0, 600, 260, OR, True)
      + chip("c27a", "Kunde bei der Commerzbank?", CB, 920, 50) + chip("c27b", "Würdest du wechseln?", OR, 1040, 56),
      lambda a, d: f'pop("#t27", {a}); pop("#i27", {a} + 0.1); pop("#c27a", {cap("s27", 2)}); slam("#c27b", {cap("s27", 3)});',
      [(st("s27"), "handy-benachrichtigung"), (cap("s27", 3), "pop")])

# ---------------- Teil 4 ----------------
kapitel("s28", 4, "Und die Aktie?", "handelssaal")

szene("s29", "frei-commerzbank-turm", titel_zeile("t29", "Rekordgewinn") + logo("l29", "commerzbank.png", 600, 560, pad=18) + tz("n29", "2,7 Mrd. €", 800, 140, "glow-g")
      + chip("c29", "Gewinn in 9 Monaten", GRUEN, 990, 54) + stempel("s29x", "REKORD", 360, 1080, CB, 80, -6),
      lambda a, d: f'pop("#t29", {a}); pop("#l29", {cap("s29", 0)}); pop("#c29", {cap("s29", 2)}); slam("#n29", {cap("s29", 3)}); stempeln("#s29x", {cap("s29", 4)});',
      [(st("s29"), "whoosh-weich"), (cap("s29", 3), "kasse"), (cap("s29", 4), "stempel")])

ZIEL = (f'<div id="g30" style="position:absolute;left:120px;top:800px;width:840px;height:110px;border-radius:55px;background:#1b1f22;border:5px solid #ffffff33;overflow:hidden;z-index:3">'
        f'<div id="g30f" style="width:79.4%;height:100%;background:linear-gradient(90deg,{GRUEN}aa,{GRUEN});box-shadow:0 0 40px {GRUEN};transform-origin:0 50%"></div></div>'
        f'<div class="mono" style="position:absolute;left:120px;top:930px;font-size:34px;color:{GRUEN};z-index:4">2,7 Mrd. € geschafft</div>'
        f'<div class="mono" style="position:absolute;left:600px;width:360px;top:930px;text-align:right;font-size:34px;color:#fff;z-index:4">Ziel: 3,4 Mrd. €</div>')
szene("s30", "frei-frankfurt-staedel", titel_zeile("t30", "Ziel fürs ganze Jahr") + icon_gross("i30", "🎯", 0, 590, 180, GRUEN, True) + ZIEL,
      lambda a, d: f'pop("#t30", {a}); pop("#i30", {a} + 0.1); pop("#g30", {cap("s30", 0)}); tl.fromTo("#g30f", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2, ease: "power2.out" }}, {cap("s30", 1)});',
      [(st("s30"), "swipe"), (cap("s30", 1), "kurve-hoch")])

szene("s31", "wallstreet", titel_zeile("t31", "Trotzdem: Aktie fällt") + icon_gross("i31", "📉", 120, 610, 240, ROT) + flagge("f31", "flagge-italien", 600, 650, 330, 4)
      + tz("q31", "Was machen die Italiener?", 980, 66, "glow-o"),
      lambda a, d: f'pop("#t31", {a}); slam("#i31", {cap("s31", 0)}); pop("#f31", {cap("s31", 4)}); pop("#q31", {cap("s31", 5)});',
      [(st("s31"), "kurve-runter"), (cap("s31", 5), "spannung")])

szene("s32", "frei-mailand-porta-nuova", titel_zeile("t32", "Fazit") + kalender("k32", "GERETTET", "2008", 80, 620, 260, CB) + pfeil("p32", 360, 760, 460, 760, 0.0, "#fff", 9)
      + foto("andrea-orcel", "f32", 490, 600, 500, 420, UC) + chip("c32", "UniCredit-Chef Andrea Orcel · Mailand", UC, 1090, 44),
      lambda a, d: (f'pop("#t32", {a}); pop("#k32", {cap("s32", 2)}); draw("#p32-p", {cap("s32", 3)}, 0.3); pop("#p32-k", {cap("s32", 3)} + 0.25);'
                    f' pop("#f32", {cap("s32", 4)}); flash({cap("s32", 4)}, 0.4); slam("#c32", {cap("s32", 4)} + 0.4);'),
      [(st("s32"), "nv-boom-kurz"), (cap("s32", 4), "kamera-blitz")])

szene("s33", "frei-commerzbank-turm", titel_zeile("t33", "Was jetzt?") + kasten("k33", "✅ Dein Konto: bleibt", 140, 620, 800, 140, GRUEN, 54)
      + kalender("k33b", "NOV", "16", 390, 820, 300, ROT) + chip("c33", "dann wissen wir mehr", OR, 1180, 50),
      lambda a, d: f'pop("#t33", {a}); pop("#k33", {cap("s33", 0)}); pop("#k33b", {cap("s33", 2)}); slam("#c33", {cap("s33", 3)});',
      [(st("s33"), "whoosh-weich"), (cap("s33", 0), "richtig"), (cap("s33", 2), "uhr-tickt")])

SZ.append((0.0, DAUER, news_kopf("13.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, SZ, SFX)
    print(bildquellen(HERE))
