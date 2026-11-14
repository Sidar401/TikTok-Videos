#!/usr/bin/env python3
"""HundeFinanzTv Longform (News v2, 2:04): Der größte Krypto-Raub der Geschichte – Binance 6,3 Mrd. $.
python3 build.py        → 9:16 (TikTok/Instagram)
python3 build.py quer   → 16:9 (YouTube): Szenen mittig skaliert + Kapitel-Leiste links + Fakten-Karte rechts, Hintergrund bildfüllend.
Original-Logos (Wikimedia, gemeinfrei), freie Hintergründe (CC0/gemeinfrei), keine Quellen im Bild, kein Personenfoto (Programmierer = Privatperson → Silhouette)."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
import glow_short  # noqa: E402
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, QUER_CSS, ROT, bildquellen, flagge, hintergrund_foto, icon_gross, kalender,  # noqa: E402
                         kasten, kit_assets, kit_hg, news_kopf, person, quelle, rahmen, stempel, titel_zeile, unterstrich, vergleich, wechsel_js,
                         zettel, zoom_js)
from glow_short import build, chip, partikel, t, zeiten  # noqa: E402

QUER = "quer" in sys.argv
BN = "#F3BA2F"
kit_assets(HERE, ["flagge-nordkorea"])
for f in ("binance.png", "binance-symbol.png", "bybit.png", "fbi.png"):
    shutil.copy(W / "brand/logos" / f, HERE / "assets/logos" / f)
cap, st, en, DAUER = zeiten(HERE)
kit_hg(HERE, ["frei-code-monitor", "frei-code-css", "frei-frankfurt-nacht", "handelssaal", "wallstreet", "frei-50euro", "frei-controller", "frei-euro"])
SZ, SFX = [], []
REIHE = [f"s{i}" for i in range(1, 31)]


def bg(id_, key):
    h = hintergrund_foto(id_, key)
    return h.replace("width:1080px;height:1920px", "width:1920px;height:1080px") if QUER else h


def szene(sid, hg, html, js, sfx=()):
    i = len(SZ)
    a = st(sid)
    b = st(REIHE[REIHE.index(sid) + 1]) if sid != REIHE[-1] else DAUER
    SZ.append((a, b, bg(f"bg{i}", hg) + rahmen(html, QUER),
               lambda a_, d_, j=js, k=i: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + zoom_js(f"#bg{k}", a_, d_, 1.12)))
    SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def logo(id_, datei, y, w, x=None, karte=False, glow=BN, pad=22):
    pos = f"left:{x}px" if x is not None else f"left:{(1080 - w) // 2}px"
    stil = (f"padding:{pad}px;border-radius:24px;background:#fff;box-shadow:0 0 60px {glow}66, 0 30px 50px #000" if karte
            else f"filter:drop-shadow(0 0 30px {glow}aa) drop-shadow(0 20px 30px #000)")
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;width:{w}px;{stil};z-index:4">'
            f'<img src="assets/logos/{datei}" alt="" style="width:100%;display:block"/></div>')


def kapitel(sid, n, titel, hg, gr=92):
    szene(sid, hg, tz(f"k{n}a", f"TEIL {n}", 600, 100, "glow-o") + tz(f"k{n}b", f'<span class="box">{titel}</span>', 750, gr)
          + unterstrich(f"k{n}u", 290, 900, 500, GELB),
          lambda a, d: f'slam("#k{n}a", {a}); pop("#k{n}b", {a} + 0.25); draw("#k{n}u-p", {a} + 0.6, 0.4); flash({a}, 0.4);',
          [(st(sid), "nv-dun-dun-dun" if n == 1 else "nv-boom-kurz")])


def karte_text(id_, kopf, text, y, farbe, x=120, w=840, gr=50):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:30px 38px;border-radius:26px;background:#14181bee;border:5px solid {farbe};'
            f'box-shadow:0 0 40px {farbe}55;z-index:4"><div class="mono" style="font-size:28px;color:{farbe};letter-spacing:2px">{kopf}</div>'
            f'<div style="font-weight:900;font-size:{gr}px;color:#fff;line-height:1.1;margin-top:8px">{text}</div></div>')


# ---------------- Intro ----------------
szene("s1", "frei-code-monitor", KIT_CSS + (QUER_CSS if QUER else "") + titel_zeile("t1", "⚡ Rekord-Raub", farbe=ROT) + logo("l1", "binance.png", 615, 600)
      + tz("n1", "6,3 Mrd. $", 760, 160, "glow-r") + icon_gross("i1", "⏱️", 120, 980, 170, OR) + tz("m1", "in 20 Min.", 1010, 90, "glow-o").replace("z-index:5;top", "z-index:5;left:120px;top"),
      lambda a, d: (KIT_JS + f' pop("#t1", {a}); pop("#l1", {a}); slam("#n1", {cap("s1", 0)} + 0.2); shake("#n1", {cap("s1", 1)}); pop("#i1", {cap("s1", 2)}); pop("#m1", {cap("s1", 2)} + 0.2);'),
      [(0.0, "eilmeldung"), (cap("s1", 0) + 0.2, "crash-bass"), (cap("s1", 2), "uhr-tickt")])

szene("s2", "frei-code-css", titel_zeile("t2", "Größter Krypto-Raub") + stempel("s2x", "REKORD", 340, 640, ROT, 110, -8) + icon_gross("i2", "💼", 0, 860, 220, OR, True)
      + chip("c2", "begann mit einem Jobangebot", OR, 1110, 50),
      lambda a, d: f'pop("#t2", {a}); stempeln("#s2x", {cap("s2", 1)}); pop("#i2", {cap("s2", 3)}); slam("#c2", {cap("s2", 3)} + 0.3);',
      [(st("s2"), "whoosh-weich"), (cap("s2", 1), "stempel"), (cap("s2", 3), "koffer-klick")])

szene("s3", "frei-frankfurt-nacht", titel_zeile("t3", "Teil das Video") + icon_gross("i3", "📤", 0, 620, 250, OR, True) + chip("c3", "an alle, die einen Job suchen", OR, 960, 52),
      lambda a, d: (f'pop("#t3", {a}); pop("#i3", {a} + 0.1); tl.fromTo("#i3", {{ y: 0 }}, {{ y: -30, duration: 0.2, yoyo: true, repeat: 3 }}, {a} + 0.4); slam("#c3", {cap("s3", 1)});'),
      [(st("s3"), "swipe"), (st("s3") + 0.3, "handy-benachrichtigung")])

# ---------------- Teil 1 ----------------
kapitel("s4", 1, "Die Falle", "frei-code-monitor")

BLASE = (f'<div id="b5" style="position:absolute;left:470px;top:640px;width:520px;padding:30px 34px;border-radius:30px 30px 30px 6px;background:#fff;color:#111;'
         f'font-weight:900;font-size:44px;line-height:1.15;box-shadow:0 20px 50px #000;z-index:4">„Wir haben einen Traumjob für dich!“'
         f'<div class="mono" style="font-size:24px;color:#666;margin-top:10px">angeblicher Personalvermittler</div></div>')
szene("s5", "frei-code-css", titel_zeile("t5", "Juni 2026") + person("p5", "Entwickler", "Binance", 90, 620, 340, BN) + BLASE
      + logo("l5", "binance-symbol.png", 1000, 140, x=650),
      lambda a, d: f'pop("#t5", {a}); pop("#p5", {cap("s5", 1)}); pop("#l5", {cap("s5", 3)}); pop("#b5", {cap("s5", 5)});',
      [(st("s5"), "whoosh-weich"), (cap("s5", 5), "handy-benachrichtigung")])

szene("s6", "frei-controller", titel_zeile("t6", "Auf Jobsuche") + icon_gross("i6", "🔎", 0, 630, 260, GELB, True) + chip("c6", "„klingt gut – ich mache mit“", GRUEN, 980, 50),
      lambda a, d: f'pop("#t6", {a}); pop("#i6", {cap("s6", 0)}); slam("#c6", {cap("s6", 2)});',
      [(st("s6"), "swipe"), (cap("s6", 2), "klick")])

szene("s7", "frei-code-monitor", titel_zeile("t7", "Gespräch Nr. 2") + vergleich("v7", "GESPRÄCH 1", "Personal&shy;vermittler", "GESPRÄCH 2", "„Chef“", OR, ROT, 620, 300)
      + stempel("s7x", "FIRMA GIBT ES NICHT", 150, 990, ROT, 58, -5),
      lambda a, d: f'pop("#t7", {a}); pop("#v7-l", {a} + 0.1); pop("#v7-r", {cap("s7", 1)}); stempeln("#s7x", {cap("s7", 3)});',
      [(st("s7"), "whoosh-weich"), (cap("s7", 3), "stempel")])

DATEI = (f'<div id="d8" style="position:absolute;left:290px;top:640px;width:500px;padding:40px;border-radius:30px;background:#14181bee;border:5px solid {OR};'
         f'box-shadow:0 0 50px {OR}66;z-index:4;text-align:center"><div style="font-size:150px">📁</div>'
         f'<div class="mono" style="font-size:40px;color:#fff;margin-top:10px">probeaufgabe.zip</div></div>')
szene("s8", "frei-code-css", titel_zeile("t8", "Die Probeaufgabe") + DATEI + tz("ar8", "⬇", 1000, 140, "glow-o"),
      lambda a, d: f'pop("#t8", {a}); pop("#d8", {cap("s8", 1)}); slam("#ar8", {cap("s8", 2)}); tl.fromTo("#ar8", {{ y: 0 }}, {{ y: 30, duration: 0.3, yoyo: true, repeat: 3 }}, {cap("s8", 2)} + 0.3);',
      [(st("s8"), "swipe"), (cap("s8", 2), "klick")])

szene("s9", "frei-code-monitor", titel_zeile("t9", "Schadsoftware", farbe=ROT) + icon_gross("i9", "🦠", 140, 620, 260, ROT) + icon_gross("i9b", "🛡️", 620, 620, 260, GRAU)
      + tz("x9", "❌", 700, 160).replace("z-index:5;top", "z-index:6;left:240px;top") + chip("c9", "Virenschutz merkt nichts", ROT, 1000, 54),
      lambda a, d: f'pop("#t9", {a}); slam("#i9", {cap("s9", 1)}); pop("#i9b", {cap("s9", 2)}); slam("#x9", {cap("s9", 3)}); pop("#c9", {cap("s9", 3)} + 0.3);',
      [(st("s9"), "alarm"), (cap("s9", 3), "nv-falsch-buzzer")])

# ---------------- Teil 2 ----------------
kapitel("s10", 2, "Der Raub", "handelssaal")

ZL = f'<div id="zl11" style="position:absolute;left:350px;top:760px;width:380px;height:12px;border-radius:6px;background:linear-gradient(90deg,{GRAU},{ROT});transform-origin:0 50%;z-index:2"></div>'
szene("s11", "frei-code-css", titel_zeile("t11", "Monatelang unbemerkt") + kalender("k11a", "JUNI", "2026", 90, 650, 250, GRAU) + ZL + kalender("k11b", "OKTOBER", "2026", 740, 650, 250, ROT)
      + icon_gross("i11", "🕵️", 0, 930, 200, GRAU, True),
      lambda a, d: (f'pop("#t11", {a}); pop("#k11a", {a} + 0.1); tl.fromTo("#zl11", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2 }}, {cap("s11", 0)}); pop("#k11b", {cap("s11", 1)});'
                    f' pop("#i11", {cap("s11", 1)} + 0.3);'),
      [(st("s11"), "uhr-tickt"), (cap("s11", 1) + 0.3, "nv-sog")])

szene("s12", "frei-code-monitor", titel_zeile("t12", "Der Angriff", farbe=ROT) + kalender("k12", "OKT", "29", 390, 620, 300, ROT) + stempel("s12x", "ANGRIFF", 300, 1020, ROT, 90, -6),
      lambda a, d: f'pop("#t12", {a}); pop("#k12", {cap("s12", 0)}); stempeln("#s12x", {cap("s12", 1)}); flash({cap("s12", 1)}, 0.5);',
      [(st("s12"), "spannung"), (cap("s12", 1), "crash-bass")])

KETTEN = "".join(f'<div class="kt" style="position:absolute;left:{105 + (k % 5) * 180}px;top:{960 + (k // 5) * 110}px;width:150px;height:80px;border-radius:16px;background:#14181b;'
                 f'border:4px solid {BN};box-shadow:0 0 20px {BN}66;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:34px;color:{BN};z-index:3">#{k + 1}</div>' for k in range(10))
szene("s13", "frei-50euro", titel_zeile("t13", "In 20 Minuten") + tz("u13", "20:00", 590, 120, "glow-o") + tz("n13", "> 6 Mrd. $", 760, 130, "glow-r") + KETTEN,
      lambda a, d: (f'pop("#t13", {a}); pop("#u13", {a}); slam("#n13", {cap("s13", 1)});'
                    f' tl.fromTo(".kt", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, stagger: 0.08, ease: "back.out(2)" }}, {cap("s13", 2)});'
                    f' tl.to(".kt", {{ borderColor: "{ROT}", color: "{ROT}", boxShadow: "0 0 20px {ROT}", duration: 0.2, stagger: 0.06 }}, {cap("s13", 3)});'),
      [(st("s13"), "uhr-tickt"), (cap("s13", 1), "kasse"), (cap("s13", 2), "pop"), (cap("s13", 3), "alarm")])

BASIS = 1150
BAL = (f'<div id="b14a" style="position:absolute;left:220px;top:{BASIS - 110}px;width:240px;height:110px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{GRAU},{GRAU}88);transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b14b" style="position:absolute;left:620px;top:{BASIS - 460}px;width:240px;height:460px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);box-shadow:0 0 40px {ROT}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b14ta" class="mono" style="position:absolute;left:140px;width:400px;top:{BASIS - 180}px;text-align:center;font-size:52px;color:#fff;z-index:5">1,5 Mrd. $</div>'
       f'<div id="b14tb" class="mono" style="position:absolute;left:540px;width:400px;top:{BASIS - 530}px;text-align:center;font-size:52px;color:{ROT};z-index:5">6,3 Mrd. $</div>')
szene("s14", "wallstreet", titel_zeile("t14", "Der alte Rekord") + logo("l14a", "bybit.png", 600, 300, x=190, karte=True, glow=GRAU, pad=18) + logo("l14b", "binance.png", 1170, 300, x=590)
      + BAL + quelle("q14", "Bybit Feb. 2025 · Binance Okt. 2026", 1250),
      lambda a, d: (f'pop("#t14", {a}); pop("#l14a", {cap("s14", 3)}); tl.fromTo("#b14a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s14", 2)}); pop("#b14ta", {cap("s14", 2)} + 0.3);'
                    f' tl.fromTo("#b14b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.8 }}, {cap("s14", 4)} + 0.4); pop("#b14tb", {cap("s14", 4)} + 1.0); pop("#l14b", {cap("s14", 4)} + 1.0); pop("#q14", {cap("s14", 4)} + 1.2);'),
      [(st("s14"), "swipe"), (cap("s14", 2), "pop"), (cap("s14", 4) + 0.4, "kurve-hoch")])

szene("s15", "frei-code-monitor", titel_zeile("t15", "Rund viermal so groß") + tz("n15", "× 4", 700, 300, "glow-r") + partikel("pa15", 540, 860, 26, (ROT, BN, "#fff"), 520),
      lambda a, d: f'pop("#t15", {a}); slam("#n15", {cap("s15", 1)}); burst("#pa15", {cap("s15", 1)} + 0.2); shake("#n15", {cap("s15", 1)} + 0.2);',
      [(st("s15"), "whoosh-weich"), (cap("s15", 1), "bass-schlag")])

# ---------------- Teil 3 ----------------
kapitel("s16", 3, "Spur nach Nordkorea", "frei-code-css", 82)

szene("s17", "frei-code-monitor", titel_zeile("t17", "Die Ermittler") + logo("l17", "fbi.png", 610, 300, x=110, glow="#4d8ff0") + flagge("f17", "flagge-nordkorea", 560, 660, 400, 3)
      + chip("c17", "Hackergruppe aus Nordkorea – laut FBI", ROT, 1020, 44) + chip("c17b", "auch hinter dem Bybit-Raub?", OR, 1120, 46),
      lambda a, d: f'pop("#t17", {a}); pop("#l17", {cap("s17", 0)}); pop("#f17", {cap("s17", 2)}); slam("#c17", {cap("s17", 3)}); pop("#c17b", {cap("s17", 5)});',
      [(st("s17"), "whoosh-weich"), (cap("s17", 2), "nv-sog"), (cap("s17", 5), "klick")])

szene("s18", "frei-code-css", titel_zeile("t18", "Die Antwort") + flagge("f18", "flagge-nordkorea", 290, 640, 500, -3) + stempel("s18x", "„WAREN WIR NICHT“", 200, 980, OR, 54, -5),
      lambda a, d: f'pop("#t18", {a}); pop("#f18", {a} + 0.1); stempeln("#s18x", {cap("s18", 0)} + 0.4);',
      [(st("s18"), "swipe"), (cap("s18", 0) + 0.4, "stempel")])

szene("s19", "wallstreet", titel_zeile("t19", "Geld eingefroren") + icon_gross("i19", "🧊", 0, 600, 220, "#7fd3ff", True)
      + karte_text("k19a", "BESCHLAGNAHMT", "> 1,2 Mrd. $", 870, "#4d8ff0", 80, 440, 54) + karte_text("k19b", "EINGEFROREN", "≈ 3 Mrd. $", 870, "#7fd3ff", 560, 440, 54),
      lambda a, d: f'pop("#t19", {a}); pop("#i19", {a} + 0.1); pop("#k19a", {cap("s19", 1)}); pop("#k19b", {cap("s19", 3)});',
      [(st("s19"), "nv-sog"), (cap("s19", 1), "hammer"), (cap("s19", 3), "pop")])

szene("s20", "frei-controller", titel_zeile("t20", "Deine Meinung") + icon_gross("i20", "💬", 0, 600, 240, OR, True)
      + chip("c20", "Hättest du die Datei geladen?", OR, 900, 54) + chip("c20a", "😬 ja", ROT, 1040, 56, 250) + chip("c20b", "🙅 nie", GRUEN, 1040, 56, 610),
      lambda a, d: f'pop("#t20", {a}); pop("#i20", {a} + 0.1); slam("#c20", {cap("s20", 1)}); pop("#c20a", {cap("s20", 2)}); pop("#c20b", {cap("s20", 2)} + 0.2);',
      [(st("s20"), "handy-benachrichtigung"), (cap("s20", 2), "pop")])

# ---------------- Teil 4 ----------------
kapitel("s21", 4, "Die Kunden", "frei-euro")

szene("s22", "frei-euro", titel_zeile("t22", "Alles ersetzt") + logo("l22", "binance.png", 600, 600) + tz("n22", "6,3 Mrd. $", 780, 150, "glow-g")
      + stempel("s22x", "AUS EIGENEN RESERVEN", 190, 1000, GRUEN, 48, -4),
      lambda a, d: f'pop("#t22", {a}); pop("#l22", {cap("s22", 0)}); slam("#n22", {cap("s22", 1)}); stempeln("#s22x", {cap("s22", 2)});',
      [(st("s22"), "whoosh-weich"), (cap("s22", 1), "kasse"), (cap("s22", 2), "stempel")])

szene("s23", "frei-frankfurt-nacht", titel_zeile("t23", "Die Kunden") + icon_gross("i23", "✅", 0, 630, 260, GRUEN, True) + chip("c23", "kein Kunde verliert Geld", GRUEN, 980, 60),
      lambda a, d: f'pop("#t23", {a}); slam("#i23", {cap("s23", 0)}); slam("#c23", {cap("s23", 1)});',
      [(st("s23"), "richtig")])

FORM = (f'<div id="fm24" style="position:absolute;left:190px;top:620px;width:700px;padding:36px 40px;border-radius:26px;background:#fff;color:#111;box-shadow:0 30px 60px #000;z-index:3">'
        f'<div style="font-weight:900;font-size:46px">Entschädigung beantragen</div>'
        f'<div style="margin-top:22px;height:56px;border-radius:12px;background:#eee"></div><div style="margin-top:16px;height:56px;border-radius:12px;background:#eee"></div>'
        f'<div style="margin-top:22px;padding:16px;border-radius:14px;background:{BN};font-weight:900;font-size:38px;text-align:center">Jetzt einloggen</div></div>')
szene("s24", "frei-code-css", titel_zeile("t24", "Die zweite Welle", farbe=ROT) + FORM + stempel("s24x", "FÄLSCHUNG", 300, 840, ROT, 100, -10),
      lambda a, d: f'pop("#t24", {a}); pop("#fm24", {cap("s24", 2)}); stempeln("#s24x", {cap("s24", 3)}); shake("#fm24", {cap("s24", 3)});',
      [(st("s24"), "alarm"), (cap("s24", 3), "stempel")])

# ---------------- Teil 5 ----------------
kapitel("s25", 5, "So schützt du dich", "frei-frankfurt-nacht")


def tipp(sid, n, icon, kopf, text, hg, sfx):
    szene(sid, hg, titel_zeile(f"t{sid}", f"Tipp {n}", farbe=GRUEN) + icon_gross(f"i{sid}", icon, 0, 610, 220, GRUEN, True)
          + karte_text(f"k{sid}", kopf, text, 880, GRUEN, gr=52),
          lambda a, d, s=sid: f'pop("#t{s}", {a}); pop("#i{s}", {a} + 0.1); pop("#k{s}", {cap(s, 0)} + 0.3);',
          [(st(sid), "swipe"), (cap(sid, 0) + 0.3, sfx)])


tipp("s26", 1, "📱", "LINKS IN NACHRICHTEN", "App selbst öffnen –<br/>nie auf Links klicken", "frei-code-monitor", "klick")
tipp("s27", 2, "🔑", "WIEDERHERSTELLUNGS-WÖRTER", "Niemals herausgeben –<br/>egal wer fragt", "frei-code-css", "koffer-klick")
tipp("s28", 3, "📁", "DATEIEN VON FREMDEN", "Nie herunterladen –<br/>auch nicht für Bewerbungen", "frei-controller", "tuer-zu")

szene("s29", "frei-frankfurt-nacht", titel_zeile("t29", "Die Lehre") + icon_gross("i29", "🤝", 0, 610, 240, OR, True)
      + vergleich("v29", "NICHT DIE", "Technik", "SONDERN", "Vertrauen", GRAU, OR, 900, 230),
      lambda a, d: f'pop("#t29", {a}); pop("#i29", {cap("s29", 1)}); pop("#v29-l", {cap("s29", 2)}); pop("#v29-r", {cap("s29", 4)});',
      [(st("s29"), "spannung"), (cap("s29", 4), "nv-tusch")])

szene("s30", "wallstreet", titel_zeile("t30", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
      lambda a, d: f'pop("#t30", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
      [(st("s30"), "zeitung")])

SZ.append((0.0, DAUER, rahmen(news_kopf("14.11.2026"), QUER), lambda a, d: "", 8))

# ---------------- 16:9: Kapitel-Leiste links + Fakten-Karte rechts ----------------
if QUER:
    KAP = [(0.0, st("s4"), "Intro"), (st("s4"), st("s10"), "1 · Die Falle"), (st("s10"), st("s16"), "2 · Der Raub"), (st("s16"), st("s21"), "3 · Nordkorea"),
           (st("s21"), st("s25"), "4 · Die Kunden"), (st("s25"), DAUER, "5 · Schutz")]
    for i, (a0, a1, txt) in enumerate(KAP):
        html = (f'<div id="kl{i}" style="position:absolute;left:100px;top:330px;width:400px;z-index:4">'
                f'<div class="mono" style="font-size:30px;color:{GRAU}">KAPITEL</div><div style="font-weight:900;font-size:50px;color:#fff;line-height:1.1;margin-top:8px">{txt}</div>'
                f'<div style="margin-top:22px;height:8px;width:{60 + 50 * i}px;border-radius:4px;background:{OR};box-shadow:0 0 20px {OR}"></div></div>')
        SZ.append((a0, a1, html, (lambda j: lambda a, d: f'tl.fromTo("#kl{j}", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4 }}, {a});')(i), 4))
    RECHTS = (f'<div id="re" style="position:absolute;left:1440px;top:300px;width:410px;padding:28px;border-radius:26px;background:#14181bee;border:3px solid {BN}66;z-index:4">'
              f'<img src="assets/logos/binance.png" style="width:300px"/>'
              f'<div class="mono" style="font-size:28px;color:{GRAU};margin-top:20px">gestohlen am 29.10.2026</div>'
              f'<div style="font-weight:900;font-size:64px;color:{ROT};text-shadow:0 0 30px {ROT}">6,3 Mrd. $</div>'
              f'<div class="mono" style="font-size:28px;color:{GRAU}">in ≈ 20 Minuten · 10 Blockchains</div></div>')
    SZ.append((st("s2"), DAUER, RECHTS, lambda a, d: f'tl.fromTo("#re", {{ x: 80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5 }}, {a});', 5))
    glow_short.querformat()

if __name__ == "__main__":
    build(HERE, SZ, SFX)
    print(bildquellen(HERE))
