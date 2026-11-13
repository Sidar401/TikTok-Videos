#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (News-Format v2, ~70 s): Nvidia – Tag 1 ohne Jensen Huang. Laufband. Endkarte → Longform „Huang raus“."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, foto_gross, hintergrund_foto, icon_gross, kalender, kit_assets, kit_hg,  # noqa: E402
                         laufband_szene, linie, marke, news_kopf, quelle, raster, stempel, titel_zeile, wechsel_js, zettel, zoom_js)
from glow_short import build, chip, t, zeiten  # noqa: E402
from motor import endkarte  # noqa: E402

NV = "#76b900"
kit_assets(HERE, ["nvidia"])
(HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)
for f in ("jensen-huang.jpg", "colette-kress.jpg"):
    shutil.copy(W / "brand/fotos" / f, HERE / "assets/fotos" / f)
shutil.copy(W / "renders/thumbnails/longform-huang-raus-tiktok.jpg", HERE / "assets/lf.jpg")
HUANG = "Foto: Peter Dasilva · CC BY 4.0"
KRESS = "Foto: SiliconANGLE theCUBE · CC BY 3.0"
cap, st, en, DAUER = zeiten(HERE)
kit_hg(HERE, ["nvidia-zentrale", "nyse", "handelssaal", "wallstreet", "chips", "sitzungssaal"])
SZ, SFX = [], []
REIHE = [f"s{i}" for i in range(1, 18)]


def szene(sid, hg, html, js, sfx=()):
    i = len(SZ)
    a = st(sid)
    b = st(REIHE[REIHE.index(sid) + 1]) if sid != REIHE[-1] else DAUER
    SZ.append((a, b, (hintergrund_foto(f"bg{i}", hg) if hg else "") + html,
               lambda a_, d_, j=js, k=i, h=hg: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + (zoom_js(f"#bg{k}", a_, d_, 1.12) if h else "")))
    SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


# s1 Hook
szene("s1", "nvidia-zentrale", KIT_CSS + titel_zeile("t1", "⚡ Tag 1 ohne Huang", farbe=ROT)
      + foto_gross("f1", "assets/fotos/jensen-huang.jpg", 290, 600, 500, 430, HUANG, NV) + stempel("s1x", "WEG!", 400, 940, ROT, 110, -10),
      lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#f1", {a}); stempeln("#s1x", {cap("s1", 0)} + 0.4); pop("#t1", {cap("s1", 1)});' + zoom_js("#f1", a + 0.5, 2.0, 1.05),
      [(0.0, "eilmeldung"), (0.05, "kamera-blitz"), (cap("s1", 0) + 0.4, "stempel")])

# s2 33 Jahre
ZL = f'<div id="zl" style="position:absolute;left:330px;top:760px;width:420px;height:12px;border-radius:6px;background:linear-gradient(90deg,{NV},{ROT});transform-origin:0 50%;z-index:2"></div>'
szene("s2", "nvidia-zentrale", titel_zeile("t2", "Nach 33 Jahren") + marke("m2", "nvidia", 0, 610, 100, wortmarke="nvidia", mitte=True)
      + kalender("k2a", "START", "1993", 90, 760, 240, NV) + ZL + kalender("k2b", "ENDE", "2026", 750, 760, 240, ROT),
      lambda a, d: (f'pop("#t2", {a}); pop("#m2", {cap("s2", 0)}); pop("#k2a", {cap("s2", 1)}); tl.fromTo("#zl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8 }}, {cap("s2", 1)} + 0.2);'
                    f' pop("#k2b", {cap("s2", 2)});'),
      [(st("s2"), "whoosh-weich"), (cap("s2", 1), "uhr-tickt"), (cap("s2", 2), "tuer-zu")])

# s3 Teilen-CTA
szene("s3", "handelssaal", titel_zeile("t3", "Teil das Video") + icon_gross("i3", "📤", 0, 620, 250, OR, True)
      + chip("c3", "an alle mit Nvidia oder ETF", OR, 960, 52),
      lambda a, d: (f'pop("#t3", {a}); pop("#i3", {a} + 0.1); tl.fromTo("#i3", {{ y: 0 }}, {{ y: -30, duration: 0.2, yoyo: true, repeat: 3 }}, {a} + 0.4);'
                    f' slam("#c3", {cap("s3", 1)});'),
      [(st("s3"), "swipe"), (st("s3") + 0.3, "handy-benachrichtigung")])

# s4 Hinweis
szene("s4", "wallstreet", titel_zeile("t4", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
      lambda a, d: f'pop("#t4", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
      [(st("s4"), "zeitung")])

# s5 Handelsstart −14 %
szene("s5", "nyse", titel_zeile("t5", "Handelsstart") + icon_gross("i5", "🔔", 0, 610, 200, GELB, True)
      + marke("m5", "nvidia", 0, 870, 130, wortmarke="nvidia", schild="−14 %", mitte=True) + quelle("q5", "Eröffnung · 12.11.2026", 1100),
      lambda a, d: (f'pop("#t5", {a}); tl.fromTo("#i5", {{ rotation: -20 }}, {{ rotation: 20, duration: 0.15, yoyo: true, repeat: 5 }}, {a}); pop("#m5", {cap("s5", 0)} + 0.3);'
                    f' slam("#m5-s", {cap("s5", 2)}); shake("#m5", {cap("s5", 2)}); flash({cap("s5", 2)}, 0.4); pop("#q5", {cap("s5", 2)} + 0.4);'),
      [(st("s5"), "boersenglocke"), (cap("s5", 1), "crash-bass")])

# s6 Käufer greifen zu
szene("s6", "handelssaal", titel_zeile("t6", "Doch dann …", farbe=GELB) + icon_gross("i6", "🛒", 0, 620, 240, GRUEN, True)
      + chip("c6", "Käufer greifen zu", GRUEN, 940, 64),
      lambda a, d: f'pop("#t6", {a}); pop("#i6", {cap("s6", 1)}); slam("#c6", {cap("s6", 2)});',
      [(st("s6"), "spannung"), (cap("s6", 2), "kurve-hoch")])

# s7 Schluss −4 % bei 166 $
KURS = linie("ku", [0.75, 0.12, 0.2, 0.35, 0.3, 0.45, 0.5, 0.55, 0.58], 150, 640, 780, 380, GRUEN, punkte=[(0, "173,73 $"), (1, "−14 %"), (8, "166,19 $")])
szene("s7", "nyse", titel_zeile("t7", "Am Ende des Tages") + KURS + chip("c7", "nur −4,3 %", OR, 1070, 54) + quelle("q7", "Schluss 12.11.2026 · Vortag 173,73 $", 1160),
      lambda a, d: (f'pop("#t7", {a}); pop("#ku-w0", {a}); draw("#ku-p", {a} + 0.2, 1.8); pop("#ku-w1", {a} + 0.5); tl.fromTo("#ku-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 1.5);'
                    f' slam("#c7", {cap("s7", 2)}); pop("#ku-w2", {cap("s7", 3)}); pop("#q7", {cap("s7", 3)} + 0.3);'),
      [(st("s7"), "ticker-rauschen"), (st("s7") + 0.2, "kurve-hoch"), (cap("s7", 2), "klick"), (cap("s7", 3), "kasse")])

# s8 nachbörslich +1 %
szene("s8", "nvidia-zentrale", titel_zeile("t8", "Nach Börsenschluss") + icon_gross("i8", "🌙", 0, 620, 200, GELB, True)
      + marke("m8", "nvidia", 0, 870, 120, wortmarke="nvidia", schild="▲ +1 %", mitte=True) + quelle("q8", "nachbörslich ≈ 167,82 $", 1090),
      lambda a, d: f'pop("#t8", {a}); pop("#i8", {cap("s8", 0)}); pop("#m8", {cap("s8", 1)}); slam("#m8-s", {cap("s8", 2)}); pop("#q8", {cap("s8", 2)} + 0.4);',
      [(st("s8"), "whoosh-weich"), (cap("s8", 2), "richtig")])

# s9 Woche −11 %
szene("s9", "wallstreet", titel_zeile("t9", "Trotzdem") + icon_gross("k9", "📉", 0, 620, 220, ROT, True) + chip("c9", "nur diese Woche", OR, 860, 54) + tz("n9", "−11 %", 960, 150, "glow-r"),
      lambda a, d: f'slam("#t9", {a}); pop("#k9", {cap("s9", 1)}); pop("#c9", {cap("s9", 1)} + 0.2); slam("#n9", {cap("s9", 2)}); flash({cap("s9", 2)}, 0.4);',
      [(st("s9"), "nv-boom-kurz"), (cap("s9", 2), "kurve-runter")])

# s10 Kursziel 315 → 185
BASIS = 1110
BAL = (f'<div id="b10a" style="position:absolute;left:220px;top:{BASIS - 430}px;width:240px;height:430px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{NV},{NV}88);box-shadow:0 0 40px {NV}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b10b" style="position:absolute;left:620px;top:{BASIS - 252}px;width:240px;height:252px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);box-shadow:0 0 40px {ROT}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b10ta" class="mono" style="position:absolute;left:140px;width:400px;top:{BASIS - 500}px;text-align:center;font-size:56px;color:{NV};z-index:5">315 $</div>'
       f'<div id="b10tb" class="mono" style="position:absolute;left:540px;width:400px;top:{BASIS - 322}px;text-align:center;font-size:56px;color:{ROT};z-index:5">185 $</div>')
szene("s10", "sitzungssaal", titel_zeile("t10", "Kursziel gesenkt") + BAL + stempel("s10x", "−41 %", 620, 640, ROT, 70, 8) + quelle("q10", "Kursziel eines Analysehauses · 12.11.2026", 1130),
      lambda a, d: (f'pop("#t10", {a}); pop("#t10", {cap("s10", 1)}); tl.fromTo("#b10a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s10", 2)}); pop("#b10ta", {cap("s10", 2)} + 0.3);'
                    f' tl.fromTo("#b10b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s10", 2)} + 1.0); pop("#b10tb", {cap("s10", 2)} + 1.3); stempeln("#s10x", {cap("s10", 2)} + 1.8); pop("#q10", {cap("s10", 2)} + 2.0);'),
      [(st("s10"), "zeitung"), (cap("s10", 2) + 1.0, "kurve-runter"), (cap("s10", 2) + 1.8, "hammer")])

# s11 Colette Kress
szene("s11", "sitzungssaal", titel_zeile("t11", "Übergangschefin") + foto_gross("f11", "assets/fotos/colette-kress.jpg", 290, 600, 500, 450, KRESS, "#4d8ff0"),
      lambda a, d: f'pop("#t11", {a}); pop("#f11", {cap("s11", 1)}); flash({cap("s11", 1)}, 0.4);',
      [(st("s11"), "swipe"), (cap("s11", 1), "kamera-blitz")])

# s12 seit 2013, bleibt Finanzchefin
szene("s12", "nvidia-zentrale", titel_zeile("t12", "Colette Kress") + kalender("k12", "SEIT", "2013", 140, 620, 300, NV)
      + icon_gross("f12", "💼", 620, 650, 250, "#4d8ff0") + chip("c12", "+ bleibt Finanzchefin", OR, 1060, 52),
      lambda a, d: f'pop("#t12", {a}); pop("#f12", {a}); pop("#k12", {cap("s12", 0)} + 0.3); slam("#c12", {cap("s12", 2)});',
      [(st("s12"), "whoosh-weich"), (cap("s12", 0) + 0.3, "pop"), (cap("s12", 2), "klick")])

# s13 Warum?
szene("s13", "handelssaal", titel_zeile("t13", "Warum so schnell?", farbe=GELB) + icon_gross("i13", "🤔", 0, 640, 300, GELB, True),
      lambda a, d: f'pop("#t13", {a}); slam("#i13", {a} + 0.2);',
      [(st("s13"), "nv-staunen-wow")])

# s14 Nachfrage ≠ Chef
CHIP = (f'<svg id="ch" viewBox="0 0 200 200" style="position:absolute;left:390px;top:610px;width:300px;height:300px;z-index:4;filter:drop-shadow(0 0 30px {NV})">'
        f'<rect x="45" y="45" width="110" height="110" rx="14" fill="#1b1f22" stroke="{NV}" stroke-width="8"/><rect x="75" y="75" width="50" height="50" rx="6" fill="{NV}"/>'
        + "".join(f'<rect x="{60 + k * 30}" y="15" width="10" height="28" rx="4" fill="{NV}"/><rect x="{60 + k * 30}" y="157" width="10" height="28" rx="4" fill="{NV}"/>'
                  f'<rect x="15" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{NV}"/><rect x="157" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{NV}"/>' for k in range(3)) + '</svg>')
szene("s14", "chips", titel_zeile("t14", "Die Hoffnung") + CHIP + stempel("s14x", "NACHFRAGE ≠ CHEF", 170, 970, GRUEN, 58, -4),
      lambda a, d: (f'pop("#t14", {a}); tl.fromTo("#ch", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.8)" }}, {cap("s14", 2)});'
                    f' stempeln("#s14x", {cap("s14", 3)});'),
      [(st("s14"), "whoosh-weich"), (cap("s14", 2), "pop"), (cap("s14", 3), "stempel")])

# s15 17. November Zahlen
szene("s15", "nyse", titel_zeile("t15", "Der echte Test") + kalender("k15", "NOV", "17", 140, 620, 320, ROT) + icon_gross("i15", "📊", 600, 640, 260, OR)
      + chip("c15", "Quartalszahlen", OR, 1060, 60),
      lambda a, d: f'pop("#t15", {a}); pop("#k15", {cap("s15", 1)}); pop("#i15", {cap("s15", 3)}); slam("#c15", {cap("s15", 3)} + 0.2);',
      [(st("s15"), "swipe"), (cap("s15", 1), "uhr-tickt"), (cap("s15", 3), "spannung")])

# s16 6 % im MSCI World
szene("s16", "wallstreet", titel_zeile("t16", "Dein ETF") + raster("ms", 300, 610, 10, 10, 40, 8, "#3a4248")
      + quelle("q16", "MSCI World · Nvidia ≈ 6 von 100 €", 1110),
      lambda a, d: (f'pop("#t16", {a}); tl.fromTo("#ms .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.005 }}, {a});'
                    f' tl.to("#ms .q:nth-child(-n+6)", {{ background: "{NV}", boxShadow: "0 0 20px {NV}", duration: 0.2, stagger: 0.1 }}, {cap("s16", 0)} + 0.5); pop("#q16", {cap("s16", 1)});'),
      [(st("s16"), "zaehler"), (cap("s16", 0) + 0.5, "muenzen-klimpern")])

# s17 Endkarte (Motor)
mk_html, mk_js = endkarte("assets/lf.jpg", "Ganzes Video")
szene("s17", None, mk_html, mk_js, [(st("s17"), "whoosh-weich"), (st("s17") + 0.6, "pop")])

SZ.append((0.0, st("s17"), news_kopf("13.11.2026"), lambda a, d: "", 8))
SZ.append(laufband_szene([("NVIDIA ▼ −4,3 %", ROT), ("ZUM START −14 %", ROT), ("SCHLUSS 166,19 $", None), ("NACHBÖRSLICH ▲ +1 %", GRUEN),
                          ("WOCHE −11 %", ROT), ("ZAHLEN AM 17.11.", GELB)], DAUER))

if __name__ == "__main__":
    build(HERE, SZ, SFX)
