#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (News v2, 2:20): GTA 6 – lohnt sich die Take-Two-Aktie noch? Original-Logos (Wikimedia, gemeinfrei),
freie Hintergründe (CC0/gemeinfrei), keine Quellen im Bild. Kein Laufband (keine Eilmeldung)."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, bildquellen, hand, icon_gross, kalender, kasten, kit_assets, kit_hg,  # noqa: E402
                         hintergrund_foto, linie, news_kopf, quelle, raster, stempel, titel_zeile, unterstrich, vergleich, wechsel_js,
                         zettel, zoom_js)
from glow_short import build, chip, partikel, t, zeiten  # noqa: E402

GTA = "#ff4fa3"
T2C = "#ffffff"
kit_assets(HERE, [])
for f in ("taketwo.png", "rockstar.png", "gta6.png", "gta-serie.png", "cdprojekt.png", "bofa.png", "rdr2.png"):
    shutil.copy(W / "brand/logos" / f, HERE / "assets/logos" / f)
cap, st, en, DAUER = zeiten(HERE)
kit_hg(HERE, ["frei-miami-nacht", "frei-miami-omni", "frei-ocean-drive", "frei-controller", "handelssaal", "wallstreet", "frei-frankfurt-nacht", "frei-euro"])
SZ, SFX = [], []
REIHE = [f"s{i}" for i in range(1, 31)]


def szene(sid, hg, html, js, sfx=()):
    i = len(SZ)
    a = st(sid)
    b = st(REIHE[REIHE.index(sid) + 1]) if sid != REIHE[-1] else DAUER
    SZ.append((a, b, hintergrund_foto(f"bg{i}", hg) + html,
               lambda a_, d_, j=js, k=i: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + zoom_js(f"#bg{k}", a_, d_, 1.12)))
    SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def logo(id_, datei, y, w, x=None, karte=True, glow=OR, pad=22):
    """Original-Logo (gemeinfrei, Wikimedia). karte=True: auf weißer Karte (für dunkle Logos)."""
    pos = f"left:{x}px" if x is not None else f"left:{(1080 - w) // 2}px"
    stil = (f"padding:{pad}px;border-radius:24px;background:#fff;box-shadow:0 0 60px {glow}66, 0 30px 50px #000"
            if karte else f"filter:drop-shadow(0 0 30px {glow}aa) drop-shadow(0 20px 30px #000)")
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;width:{w}px;{stil};z-index:4">'
            f'<img src="assets/logos/{datei}" alt="" style="width:100%;display:block"/></div>')


def kapitel(sid, n, titel, hg, gr=92):
    szene(sid, hg, tz(f"k{n}a", f"TEIL {n}", 600, 100, "glow-o") + tz(f"k{n}b", f'<span class="box">{titel}</span>', 750, gr)
          + unterstrich(f"k{n}u", 290, 900, 500, GELB),
          lambda a, d: f'slam("#k{n}a", {a}); pop("#k{n}b", {a} + 0.25); draw("#k{n}u-p", {a} + 0.6, 0.4); flash({a}, 0.4);',
          [(st(sid), "nv-dun-dun-dun" if n == 1 else "nv-boom-kurz")])


# ---------------- Intro ----------------
szene("s1", "frei-miami-nacht", KIT_CSS + titel_zeile("t1", "⚡ In 5 Tagen", farbe=ROT) + logo("l1", "gta6.png", 590, 440, karte=False, glow=GTA)
      + kalender("k1", "NOV", "19", 760, 900, 220, GTA) + icon_gross("i1", "📉", 80, 930, 200, ROT),
      lambda a, d: (KIT_JS + f' pop("#t1", {a}); pop("#l1", {a}); pop("#k1", {cap("s1", 0)} + 0.4); slam("#i1", {cap("s1", 4)}); shake("#l1", {cap("s1", 4)});'),
      [(0.0, "eilmeldung"), (cap("s1", 0) + 0.4, "pop"), (cap("s1", 4), "crash-bass")])

szene("s2", "frei-miami-omni", titel_zeile("t2", "GTA 6 + Take-Two") + logo("l2a", "gta6.png", 620, 300, x=110, karte=False, glow=GTA)
      + tz("pl2", "+", 720, 110) + logo("l2b", "taketwo.png", 640, 300, x=650, pad=26),
      lambda a, d: f'pop("#t2", {a}); pop("#l2a", {cap("s2", 0)}); pop("#pl2", {cap("s2", 1)}); pop("#l2b", {cap("s2", 1)} + 0.2);',
      [(st("s2"), "whoosh-weich"), (cap("s2", 1) + 0.2, "pop")])

szene("s3", "frei-ocean-drive", titel_zeile("t3", "Markier jemanden …") + icon_gross("i3", "🤒", 0, 600, 240, OR, True)
      + kalender("k3", "NOV", "19", 120, 900, 220, GTA) + chip("c3", "„Bin leider krank“ 😏", OR, 960, 50, 380),
      lambda a, d: (f'pop("#t3", {a}); pop("#i3", {a} + 0.1); tl.fromTo("#i3", {{ rotation: -10 }}, {{ rotation: 10, duration: 0.2, yoyo: true, repeat: 5 }}, {a} + 0.4);'
                    f' pop("#k3", {cap("s3", 1)}); slam("#c3", {cap("s3", 1)} + 0.4);'),
      [(st("s3"), "handy-benachrichtigung"), (cap("s3", 1) + 0.4, "nv-staunen-wow")])

szene("s4", "wallstreet", titel_zeile("t4", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
      lambda a, d: f'pop("#t4", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
      [(st("s4"), "zeitung")])

# ---------------- Teil 1 ----------------
kapitel("s5", 1, "Die Firma hinter GTA", "frei-controller", 80)

szene("s6", "frei-controller", titel_zeile("t6", "Wem gehört GTA?") + logo("l6a", "gta-serie.png", 600, 220, x=90, karte=False, glow="#fff")
      + logo("l6b", "rockstar.png", 600, 220, x=430, karte=False, glow="#ffab00") + logo("l6c", "taketwo.png", 600, 220, x=770, pad=18)
      + "".join(f'<div id="pf6{i}" style="position:absolute;left:{320 + i * 340}px;top:690px;font-size:70px;color:#fff;z-index:5">→</div>' for i in range(2))
      + chip("c6", "Rockstar gehört zu Take-Two", OR, 960, 54),
      lambda a, d: (f'pop("#t6", {a}); pop("#l6a", {a} + 0.1); pop("#pf60", {cap("s6", 1)} - 0.2); pop("#l6b", {cap("s6", 1)}); pop("#pf61", {cap("s6", 2)} - 0.2);'
                    f' pop("#l6c", {cap("s6", 2)}); slam("#c6", {cap("s6", 2)} + 0.5);'),
      [(st("s6"), "swipe"), (cap("s6", 1), "pop"), (cap("s6", 2), "pop")])

szene("s7", "wallstreet", titel_zeile("t7", "Börsenwert") + logo("l7", "taketwo.png", 600, 240, pad=22) + tz("n7", "≈ 43 Mrd. $", 930, 140, "glow-o")
      + quelle("q7", "Schlusskurs 11.11.2026", 1110),
      lambda a, d: f'pop("#t7", {a}); pop("#l7", {a} + 0.1); slam("#n7", {cap("s7", 1)}); pop("#q7", {cap("s7", 1)} + 0.4);',
      [(st("s7"), "whoosh-weich"), (cap("s7", 1), "kasse")])

szene("s8", "handelssaal", titel_zeile("t8", "Der Haken", farbe=ROT) + icon_gross("i8", "⚠️", 0, 600, 200, ROT, True) + tz("n8", "−298 Mio. $", 860, 130, "glow-r")
      + chip("c8", "Verlust im letzten Geschäftsjahr", ROT, 1060, 50),
      lambda a, d: f'pop("#t8", {a}); slam("#i8", {cap("s8", 0)}); slam("#n8", {cap("s8", 2)}); pop("#c8", {cap("s8", 3)}); shake("#n8", {cap("s8", 3)});',
      [(st("s8"), "alarm"), (cap("s8", 2), "crash-bass")])

szene("s9", "frei-miami-nacht", titel_zeile("t9", "Alles hängt an …") + logo("l9", "gta6.png", 620, 420, karte=False, glow=GTA) + stempel("s9x", "EINE HOFFNUNG", 230, 1080, GTA, 64, -4),
      lambda a, d: f'pop("#t9", {a}); pop("#l9", {cap("s9", 1)}); flash({cap("s9", 1)}, 0.4); stempeln("#s9x", {cap("s9", 1)} + 0.6);',
      [(st("s9"), "spannung"), (cap("s9", 1) + 0.6, "stempel")])

# ---------------- Teil 2 ----------------
kapitel("s10", 2, "Die Rechnung", "frei-euro")

szene("s11", "handelssaal", titel_zeile("t11", "Erwartung Analysten") + icon_gross("i11", "🎮", 0, 600, 200, GTA, True)
      + tz("n11", "35–55 Mio.", 850, 130, "glow-o") + chip("c11", "verkaufte Spiele im 1. Geschäftsjahr", OR, 1040, 46),
      lambda a, d: f'pop("#t11", {a}); pop("#i11", {cap("s11", 0)}); slam("#n11", {cap("s11", 2)}); pop("#c11", {cap("s11", 3)});',
      [(st("s11"), "swipe"), (cap("s11", 2), "zaehler")])

RC = 'style="display:flex;justify-content:space-between;font-size:58px;margin:18px 0"'
szene("s12", "frei-euro", titel_zeile("t12", "Rechnung")
      + f'<div id="rc" class="mono" style="position:absolute;left:120px;top:620px;width:840px;padding:46px 56px;border-radius:30px;background:#14181bee;border:3px solid #ffffff22;box-shadow:0 30px 60px #000;z-index:3;color:#fff">'
        f'<div id="rc1" {RC}><span>Kopien</span><span>50 Mio.</span></div><div id="rc2" {RC}><span>Preis</span><span>× 90 $</span></div>'
        f'<div id="rcl" style="height:6px;background:#fff;margin:24px 0;transform-origin:0 50%"></div>'
        f'<div id="rc3" {RC}><span>Umsatz</span><span style="color:{GRUEN};text-shadow:0 0 30px {GRUEN}">≈ 4,5 Mrd. $</span></div></div>',
      lambda a, d: (f'pop("#t12", {a}); pop("#rc", {a}); pop("#rc1", {cap("s12", 0)}); pop("#rc2", {cap("s12", 1)});'
                    f' tl.fromTo("#rcl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4 }}, {cap("s12", 2)}); slam("#rc3", {cap("s12", 2)} + 0.3);'),
      [(st("s12"), "taschenrechner"), (cap("s12", 2) + 0.3, "kasse")])

szene("s13", "wallstreet", titel_zeile("t13", "Nur ein Zehntel") + raster("r13", 300, 620, 10, 10, 40, 8, "#3a4248")
      + quelle("q13", "4,5 Mrd. $ Umsatz vs. 43 Mrd. $ Börsenwert", 1110),
      lambda a, d: (f'pop("#t13", {a}); tl.fromTo("#r13 .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.004 }}, {a});'
                    f' tl.to("#r13 .q:nth-child(-n+10)", {{ background: "{GRUEN}", boxShadow: "0 0 20px {GRUEN}", duration: 0.2, stagger: 0.05 }}, {cap("s13", 1)}); pop("#q13", {cap("s13", 2)});'),
      [(st("s13"), "zaehler"), (cap("s13", 1), "muenzen-klimpern")])

szene("s14", "frei-ocean-drive", titel_zeile("t14", "Über viele Jahre") + logo("l14", "gta6.png", 600, 300, karte=False, glow=GTA)
      + "".join(kalender(f"j14{i}", "JAHR", str(i + 1), 110 + i * 300, 930, 220, [GTA, OR, GRUEN][i]) for i in range(3)),
      lambda a, d: f'pop("#t14", {a}); pop("#l14", {a} + 0.1);' + "".join(f' pop("#j14{i}", {cap("s14", 3)} + {i * 0.3});' for i in range(3)),
      [(st("s14"), "whoosh-weich"), (cap("s14", 3), "uhr-tickt")])

# ---------------- Teil 3 ----------------
kapitel("s15", 3, "Die Geschichte", "frei-frankfurt-nacht")

szene("s16", "frei-ocean-drive", titel_zeile("t16", "GTA 5 · 2013") + logo("l16", "gta-serie.png", 600, 280, karte=False, glow="#fff")
      + tz("n16", "800 Mio. $", 900, 140, "glow-g") + chip("c16", "am ersten Tag", GRUEN, 1080, 56),
      lambda a, d: f'pop("#t16", {a}); pop("#l16", {a} + 0.1); slam("#n16", {cap("s16", 1)}); pop("#c16", {cap("s16", 2)}); flash({cap("s16", 1)}, 0.3);',
      [(st("s16"), "swipe"), (cap("s16", 1), "kasse")])

szene("s17", "handelssaal", titel_zeile("t17", "Und die Aktie?") + logo("l17", "taketwo.png", 600, 200, pad=18) + tz("n17", "+1,2 %", 850, 140, "glow-o")
      + quelle("q17", "Schluss 18.09.2013: 17,20 $", 1040) + hand("h17", "nur!", 820, 900, 90, GELB, -8, True),
      lambda a, d: f'pop("#t17", {a}); pop("#l17", {a} + 0.1); slam("#n17", {cap("s17", 2)}); pop("#h17", {cap("s17", 2)} + 0.4); pop("#q17", {cap("s17", 3)});',
      [(st("s17"), "spannung"), (cap("s17", 2), "nv-falsch-buzzer")])

szene("s18", "frei-miami-omni", titel_zeile("t18", "Das große Geld") + tz("n18", "225 Mio.", 640, 140, "glow-g") + chip("c18a", "verkaufte Exemplare", GRUEN, 820, 52)
      + chip("c18b", "+ jahrelang GTA Online", OR, 960, 56),
      lambda a, d: f'pop("#t18", {a}); slam("#n18", {cap("s18", 2)}); pop("#c18a", {cap("s18", 2)} + 0.3); slam("#c18b", {cap("s18", 3)});',
      [(st("s18"), "whoosh-weich"), (cap("s18", 2), "zaehler"), (cap("s18", 3), "pop")])

K19 = linie("ku19", [0.04, 0.1, 0.22, 0.45, 0.6, 0.55, 0.72, 0.68, 0.9], 150, 640, 780, 420, GRUEN, punkte=[(0, "17 $"), (8, "200 $ +")])
szene("s19", "wallstreet", titel_zeile("t19", "Take-Two seit 2013") + K19 + quelle("q19", "Aktienkurs 2013 → heute", 1110),
      lambda a, d: (f'pop("#t19", {a}); pop("#ku19-w0", {a}); draw("#ku19-p", {a} + 0.2, 1.8); tl.fromTo("#ku19-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 1.6);'
                    f' pop("#ku19-w1", {cap("s19", 1)}); pop("#q19", {cap("s19", 1)} + 0.3);'),
      [(st("s19"), "kurve-hoch"), (cap("s19", 1), "richtig")])

K20 = linie("ku20", [0.55, 0.8, 0.95, 0.7, 0.85, 0.6, 0.45, 0.4], 150, 860, 780, 240, ROT, punkte=[(2, "Hoch"), (7, "≈ −25 %")]).replace("top:760px", "top:860px")
szene("s20", "frei-ocean-drive", titel_zeile("t20", "Red Dead Redemption 2") + logo("l20", "rdr2.png", 560, 420, karte=False, glow=ROT) + K20
      + quelle("q20", "Take-Two-Aktie · Okt./Nov. 2018", 1140),
      lambda a, d: (f'pop("#t20", {a}); pop("#l20", {cap("s20", 2)}); pop("#ku20-w0", {cap("s20", 3)}); draw("#ku20-p", {cap("s20", 3)}, 1.6);'
                    f' tl.fromTo("#ku20-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s20", 4)}); pop("#ku20-w1", {cap("s20", 5)}); pop("#q20", {cap("s20", 5)} + 0.3);'),
      [(st("s20"), "whoosh-weich"), (cap("s20", 3), "kurve-runter")])

szene("s21", "frei-frankfurt-nacht", titel_zeile("t21", "Cyberpunk 2077") + logo("l21", "cdprojekt.png", 600, 520, pad=26, glow=ROT) + tz("n21", "≈ −50 %", 760, 150, "glow-r")
      + stempel("s21x", "VERBUGGT", 300, 960, ROT, 76, -6) + quelle("q21", "CD-Projekt-Aktie · Dezember 2020", 1130),
      lambda a, d: (f'pop("#t21", {a}); pop("#l21", {cap("s21", 1)}); stempeln("#s21x", {cap("s21", 2)}); slam("#n21", {cap("s21", 4)}); shake("#n21", {cap("s21", 4)});'
                    f' pop("#q21", {cap("s21", 4)} + 0.4);'),
      [(st("s21"), "swipe"), (cap("s21", 2), "nv-platte-kratzer"), (cap("s21", 4), "glas-bricht")])

szene("s22", "frei-controller", titel_zeile("t22", "Deine Meinung") + icon_gross("i22", "💬", 0, 600, 240, OR, True)
      + chip("c22", "GTA 6 am ersten Tag kaufen?", GTA, 900, 56) + chip("c22a", "🛒 ja", GRUEN, 1040, 56, 250) + chip("c22b", "🙅 nein", ROT, 1040, 56, 610),
      lambda a, d: f'pop("#t22", {a}); pop("#i22", {a} + 0.1); slam("#c22", {cap("s22", 2)}); pop("#c22a", {cap("s22", 2)} + 0.4); pop("#c22b", {cap("s22", 2)} + 0.6);',
      [(st("s22"), "handy-benachrichtigung"), (cap("s22", 2), "pop")])

# ---------------- Teil 4 ----------------
kapitel("s23", 4, "Die Aktie heute", "handelssaal")

K24 = linie("ku24", [0.55, 0.72, 0.95, 0.8, 0.55, 0.25, 0.1], 150, 640, 780, 400, ROT, punkte=[(2, "266 $"), (6, "190 $")])
szene("s24", "wallstreet", titel_zeile("t24", "Take-Two 2026") + K24 + quelle("q24", "Sommer → Ende Oktober 2026", 1110),
      lambda a, d: (f'pop("#t24", {a}); draw("#ku24-p", {a} + 0.1, 2.0); pop("#ku24-w0", {cap("s24", 1)}); tl.fromTo("#ku24-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s24", 2)});'
                    f' pop("#ku24-w1", {cap("s24", 2)} + 0.6); pop("#q24", {cap("s24", 2)} + 0.8);'),
      [(st("s24"), "ticker-rauschen"), (cap("s24", 2), "kurve-runter")])

K25 = linie("ku25", [0.55, 0.72, 0.95, 0.8, 0.55, 0.25, 0.1, 0.35, 0.6], 150, 640, 780, 400, GRUEN, punkte=[(6, "190 $"), (8, "231 $")])
szene("s25", "wallstreet", titel_zeile("t25", "Comeback?") + K25 + chip("c25", "+22 % seit Ende Oktober", GRUEN, 1100, 50),
      lambda a, d: (f'pop("#t25", {a}); draw("#ku25-p", {a}, 1.4); pop("#ku25-w0", {a} + 0.4); pop("#ku25-w1", {cap("s25", 2)}); tl.fromTo("#ku25-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 1.2);'
                    f' slam("#c25", {cap("s25", 2)} + 0.3);'),
      [(st("s25"), "kurve-hoch"), (cap("s25", 2), "richtig")])

szene("s26", "handelssaal", titel_zeile("t26", "Die Messlatte") + logo("l26", "bofa.png", 600, 640, pad=24, glow="#e31837")
      + tz("n26", "≥ 1,9 Mrd. $", 820, 140, "glow-o") + chip("c26", "nur um die Erwartungen zu erfüllen", OR, 1020, 46),
      lambda a, d: f'pop("#t26", {a}); pop("#l26", {cap("s26", 0)}); slam("#n26", {cap("s26", 2)}); pop("#c26", {cap("s26", 4)});',
      [(st("s26"), "zeitung"), (cap("s26", 2), "bass-schlag")])

szene("s27", "wallstreet", titel_zeile("t27", "Alter Börsen-Spruch") + vergleich("v27", "KAUFE", "das Gerücht", "VERKAUFE", "die Nachricht", GRUEN, ROT, 640, 300),
      lambda a, d: f'pop("#t27", {a}); pop("#v27-l", {cap("s27", 2)}); pop("#v27-r", {cap("s27", 3)});',
      [(st("s27"), "swipe"), (cap("s27", 2), "klick"), (cap("s27", 3), "klick")])

szene("s28", "handelssaal", titel_zeile("t28", "Heißt") + kasten("k28a", "📈 vorher<br/>gekauft", 80, 640, 420, 230, GRUEN, 54) + tz("p28", "→", 720, 110)
      + kasten("k28b", "📉 zum Start<br/>verkauft", 580, 640, 420, 230, ROT, 54) + kalender("k28c", "NOV", "19", 410, 920, 260, GTA),
      lambda a, d: f'pop("#t28", {a}); pop("#k28a", {cap("s28", 1)}); pop("#p28", {cap("s28", 2)}); pop("#k28b", {cap("s28", 2)} + 0.2); pop("#k28c", {cap("s28", 3)});',
      [(st("s28"), "whoosh-weich"), (cap("s28", 2), "kurve-runter")])

szene("s29", "frei-miami-nacht", titel_zeile("t29", "Wer jetzt kauft …") + logo("l29", "gta6.png", 600, 300, karte=False, glow=GTA)
      + f'<div id="x29" style="position:absolute;left:0;width:1080px;top:960px;text-align:center;font-weight:900;font-size:78px;color:#fff;z-index:5">GTA 6 wird ein Hit</div>'
      + f'<div id="x29l" style="position:absolute;left:180px;top:1005px;width:720px;height:10px;background:{ROT};transform-origin:0 50%;z-index:6"></div>',
      lambda a, d: (f'pop("#t29", {a}); pop("#l29", {a} + 0.1); pop("#x29", {cap("s29", 2)}); tl.fromTo("#x29l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4 }}, {cap("s29", 2)} + 0.9);'),
      [(st("s29"), "spannung"), (cap("s29", 2) + 0.9, "nv-platte-kratzer")])

szene("s30", "frei-miami-omni", titel_zeile("t30", "… wettet auf mehr") + logo("l30", "gta6.png", 590, 280, karte=False, glow=GTA)
      + stempel("s30x", "GRÖSSER ALS ERWARTET", 170, 930, GRUEN, 48, -4) + partikel("pa30", 540, 900, 26, (GTA, OR, "#fff"), 520),
      lambda a, d: f'pop("#t30", {a}); pop("#l30", {a} + 0.1); stempeln("#s30x", {cap("s30", 1)}); burst("#pa30", {cap("s30", 1)} + 0.2);',
      [(st("s30"), "whoosh-weich"), (cap("s30", 1), "nv-tusch")])

SZ.append((0.0, DAUER, news_kopf("14.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, SZ, SFX)
    print(bildquellen(HERE))
