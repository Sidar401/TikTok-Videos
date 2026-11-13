#!/usr/bin/env python3
"""HundeFinanzTv Short (News-Format v2, ~75 s): Bitcoin-Crash am Freitag, dem 13. – 3 Auslöser. Laufband (Börsen-Eilmeldung)."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, flagge, foto_gross, hintergrund_foto, icon_gross, kalender, kasten,  # noqa: E402
                         kit_assets, kit_hg, laufband_szene, linie, marke, news_kopf, kreis, pfeil, quelle, stempel,
                         titel_zeile, wechsel_js, zettel, zoom_js)
from glow_short import build, chip, partikel, t, zeiten  # noqa: E402

BTC = "#f7931a"
kit_assets(HERE, ["bitcoin", "nvidia", "flagge-usa"])
(HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)
shutil.copy(W / "brand/fotos/jensen-huang.jpg", HERE / "assets/fotos/jensen-huang.jpg")
cap, st, en, DAUER = zeiten(HERE)
HGS = ["bitcoin-muenzen", "bitcoin-laptop", "handelssaal", "nyse", "wallstreet", "nvidia-zentrale", "chips"]
kit_hg(HERE, HGS)
SZ, SFX = [], []
REIHE = [f"s{i}" for i in range(1, 17)]


def szene(sid, hg, html, js, sfx=(), bis=None):
    i = len(SZ)
    a = st(sid)
    b = st(bis) if bis else (st(REIHE[REIHE.index(sid) + 1]) if sid != REIHE[-1] else DAUER)
    SZ.append((a, b, hintergrund_foto(f"bg{i}", hg) + html,
               lambda a_, d_, j=js, k=i: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + zoom_js(f"#bg{k}", a_, d_, 1.12)))
    SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


# s1 Hook
szene("s1", "bitcoin-muenzen", KIT_CSS + titel_zeile("t1", "⚡ Freitag, der 13.", farbe=ROT)
      + marke("m1", "bitcoin", 0, 640, 150, text="BITCOIN", schild="▼ CRASH", mitte=True)
      + kalender("k1", "FREITAG", "13", 170, 850, 250, ROT) + icon_gross("i1", "📉", 630, 860, 230, ROT),
      lambda a, d: (KIT_JS + f' pop("#t1", {a}); pop("#m1", {a}); pop("#k1", {a} + 0.2); slam("#i1", {cap("s1", 1)}); shake("#m1", {cap("s1", 1)}); flash({cap("s1", 1)}, 0.5);'),
      [(0.0, "eilmeldung"), (cap("s1", 1), "crash-bass")])

# s2 Folgen-CTA
szene("s2", "bitcoin-laptop", titel_zeile("t2", "Folg uns") + icon_gross("i2", "🔔", 0, 630, 260, OR, True)
      + chip("c2", "+ Folgen", OR, 940, 70) + quelle("q2", "jeden Tag neue Videos", 1080),
      lambda a, d: (f'pop("#t2", {a}); pop("#i2", {a} + 0.1); tl.fromTo("#i2", {{ rotation: -18 }}, {{ rotation: 18, duration: 0.14, yoyo: true, repeat: 5 }}, {a} + 0.3);'
                    f' slam("#c2", {cap("s2", 0)} + 0.4); pop("#q2", {cap("s2", 1)});'),
      [(st("s2"), "whoosh-weich"), (st("s2") + 0.3, "handy-benachrichtigung")])

# s3 unter 69.000 $
KURS = linie("ku", [0.5, 0.72, 0.66, 0.8, 0.62, 0.55, 0.38, 0.22, 0.06], 150, 650, 780, 400, ROT, punkte=[(3, "75.000 $"), (8, "68.600 $")])
szene("s3", "handelssaal", titel_zeile("t3", "Unter 69.000 $") + KURS + quelle("q3", "tiefster Stand seit 3 Monaten · 13.11.2026", 1120),
      lambda a, d: (f'pop("#t3", {a}); draw("#ku-p", {a} + 0.1, 1.4); pop("#ku-w0", {a} + 0.6); pop("#ku-w1", {cap("s3", 0)} + 1.0);'
                    f' tl.fromTo("#ku-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {a} + 1.0); pop("#q3", {cap("s3", 1)});'),
      [(st("s3"), "ticker-rauschen"), (st("s3") + 0.1, "kurve-runter")])

# s4 24 Stunden fast −7 %
szene("s4", "bitcoin-muenzen", titel_zeile("t4", "In 24 Stunden") + marke("m4", "bitcoin", 0, 650, 140, text="BTC", schild="≈ −7 %", mitte=True)
      + icon_gross("i4", "⏱️", 0, 850, 210, OR, True) + quelle("q4", "CoinGecko · 13.11.2026, morgens", 1110),
      lambda a, d: f'pop("#t4", {a}); pop("#i4", {cap("s4", 0)}); pop("#m4", {a} + 0.2); slam("#m4-s", {cap("s4", 1)}); pop("#q4", {cap("s4", 1)} + 0.3);',
      [(st("s4"), "swipe"), (st("s4") + 0.3, "uhr-tickt"), (cap("s4", 1), "bass-schlag")])

# s5 Hinweis
szene("s5", "wallstreet", titel_zeile("t5", "Kurzer Hinweis") + zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 650, 680, 74, GELB, -3),
      lambda a, d: f'pop("#t5", {a}); tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});',
      [(st("s5"), "zeitung")])

# s6 Rekord vs. heute
BASIS = 1110
BAL = (f'<div id="b6a" style="position:absolute;left:220px;top:{BASIS - 440}px;width:240px;height:440px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{BTC},{BTC}88);box-shadow:0 0 40px {BTC}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b6b" style="position:absolute;left:620px;top:{BASIS - 240}px;width:240px;height:240px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);box-shadow:0 0 40px {ROT}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b6ta" class="mono" style="position:absolute;left:140px;width:400px;top:{BASIS - 510}px;text-align:center;font-size:52px;color:{BTC};z-index:5">126.000 $</div>'
       f'<div id="b6tb" class="mono" style="position:absolute;left:540px;width:400px;top:{BASIS - 310}px;text-align:center;font-size:52px;color:{ROT};z-index:5">68.600 $</div>')
szene("s6", "nyse", titel_zeile("t6", "Seit dem Rekord") + BAL + stempel("s6x", "−45 %", 600, 640, ROT, 80, 8) + quelle("q6", "Rekord Okt. 2025 · heute 13.11.2026", 1130),
      lambda a, d: (f'pop("#t6", {a}); tl.fromTo("#b6a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s6", 0)}); pop("#b6ta", {cap("s6", 1)});'
                    f' tl.fromTo("#b6b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s6", 2)}); pop("#b6tb", {cap("s6", 2)} + 0.4); stempeln("#s6x", {cap("s6", 3)}); pop("#q6", {cap("s6", 3)} + 0.3);'),
      [(st("s6"), "whoosh-weich"), (cap("s6", 1), "kurve-hoch"), (cap("s6", 2), "kurve-runter"), (cap("s6", 3), "stempel")])

# s7 Auslöser 1: Nvidia
szene("s7", "nvidia-zentrale", titel_zeile("t7", "Auslöser Nr. 1", farbe=OR) + marke("m7", "nvidia", 0, 720, 170, wortmarke="nvidia", mitte=True)
      + quelle("q7", "ausgerechnet …", 960),
      lambda a, d: f'slam("#t7", {a}); pop("#q7", {cap("s7", 0)} + 0.3); pop("#m7", {cap("s7", 1)}); flash({cap("s7", 1)}, 0.4);',
      [(st("s7"), "nv-boom-kurz"), (cap("s7", 1), "whoosh-schnell")])

# s8 Huang raus, Aktie −14 % zum Start
szene("s8", "nvidia-zentrale", titel_zeile("t8", "Chef tritt zurück") + foto_gross("f8", "assets/fotos/jensen-huang.jpg", 300, 600, 480, 400, "Foto: Peter Dasilva · CC BY 4.0", "#76b900")
      + marke("m8", "nvidia", 0, 1060, 90, wortmarke="nvidia", schild="−14 % zum Start", mitte=True),
      lambda a, d: (f'pop("#t8", {a}); pop("#f8", {cap("s8", 0)}); flash({cap("s8", 0)}, 0.4); pop("#m8", {cap("s8", 1)}); slam("#m8-s", {cap("s8", 2)}); shake("#m8", {cap("s8", 2)});'),
      [(st("s8"), "kamera-blitz"), (cap("s8", 1), "tuer-zu"), (cap("s8", 2), "crash-bass")])

# s9 Angst an der ganzen Börse
szene("s9", "nyse", titel_zeile("t9", "Angst an der Börse") + icon_gross("i9", "😱", 0, 610, 250, ROT, True)
      + marke("m9", "bitcoin", 0, 920, 110, text="BITCOIN", mitte=True) + chip("c9", "gilt als besonders riskant", ROT, 1070, 46),
      lambda a, d: f'pop("#t9", {a}); slam("#i9", {cap("s9", 0)}); pop("#m9", {cap("s9", 1)}); pop("#c9", {cap("s9", 2)});',
      [(st("s9"), "whoosh-weich"), (cap("s9", 0), "alarm"), (cap("s9", 2), "klick")])

# s10 Auslöser 2: große Anleger ziehen Geld ab
szene("s10", "wallstreet", titel_zeile("t10", "Auslöser Nr. 2", farbe=OR) + icon_gross("i10a", "🏦", 150, 660, 230) + pfeil("p10", 430, 780, 640, 780, 0.0, ROT, 10)
      + icon_gross("i10b", "💸", 680, 660, 230, ROT) + quelle("q10", "große Anleger ziehen Geld ab", 990),
      lambda a, d: (f'slam("#t10", {a}); pop("#i10a", {cap("s10", 1)}); draw("#p10-p", {cap("s10", 2)}, 0.3); pop("#p10-k", {cap("s10", 2)} + 0.25);'
                    f' tl.fromTo("#i10b", {{ x: -200, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4 }}, {cap("s10", 2)} + 0.2); pop("#q10", {cap("s10", 2)});'),
      [(st("s10"), "nv-boom-kurz"), (cap("s10", 2), "nv-sog")])

# s11 ETF-Abflüsse
ROHR = (f'<div id="r11" style="position:absolute;left:160px;top:880px;width:760px;height:100px;border-radius:50px;background:#1b1f22;border:5px solid {BTC};z-index:2"></div>'
        + "".join(f'<div class="dl" style="position:absolute;left:{200 + k * 90}px;top:905px;width:50px;height:50px;border-radius:50%;background:{BTC};box-shadow:0 0 16px {BTC};z-index:3"></div>' for k in range(8)))
szene("s11", "nyse", titel_zeile("t11", "Bitcoin-ETFs (USA)") + flagge("fl11", "flagge-usa", 150, 610, 170, -4) + kalender("k11", "TAGE", "8", 700, 580, 220, ROT)
      + ROHR + tz("n11", "−1,4 Mrd. $", 995, 96, "glow-r") + quelle("q11", "Abflüsse in 5 Handelstagen · Spot-ETFs", 1130),
      lambda a, d: (f'pop("#t11", {a}); pop("#fl11", {a} + 0.2); pop("#k11", {cap("s11", 1)}); pop("#r11", {cap("s11", 1)} + 0.3);'
                    f' tl.fromTo(".dl", {{ x: 0, opacity: 1 }}, {{ x: 140, opacity: 0, duration: 0.6, stagger: 0.08, repeat: 3, ease: "power1.in" }}, {cap("s11", 2)});'
                    f' slam("#n11", {cap("s11", 3)}); pop("#q11", {cap("s11", 3)} + 0.3);'),
      [(st("s11"), "whoosh-weich"), (cap("s11", 2), "nv-sog"), (cap("s11", 3), "kasse")])

# s12 Auslöser 3: Wetten auf Kredit
szene("s12", "handelssaal", titel_zeile("t12", "Auslöser Nr. 3", farbe=OR) + icon_gross("i12", "🎰", 0, 640, 260, OR, True) + chip("c12", "Wetten auf Kredit", ROT, 960, 64),
      lambda a, d: f'slam("#t12", {a}); pop("#i12", {cap("s12", 0)} + 0.2); slam("#c12", {cap("s12", 1)});',
      [(st("s12"), "nv-boom-kurz"), (cap("s12", 1), "muenzen-klimpern")])

# s13 geliehenes Geld → rausgeworfen
DOM = "".join(f'<div class="do" style="position:absolute;left:{170 + k * 120}px;top:820px;width:60px;height:220px;border-radius:10px;background:linear-gradient(180deg,{BTC},#a85e00);'
              f'box-shadow:0 0 20px {BTC}77;transform-origin:100% 100%;z-index:3"></div>' for k in range(7))
szene("s13", "bitcoin-laptop", titel_zeile("t13", "Geliehenes Geld") + kasten("k13a", "eigenes Geld", 80, 610, 400, 130, GRUEN, 48) + tz("pl13", "+", 610, 100)
      + kasten("k13b", "geliehenes Geld", 600, 610, 400, 130, ROT, 48) + DOM + stempel("s13x", "RAUSGEWORFEN", 230, 1060, ROT, 60, -5),
      lambda a, d: (f'pop("#t13", {a}); pop("#k13a", {a} + 0.1); pop("#pl13", {a} + 0.3); pop("#k13b", {cap("s13", 0)} + 0.3);'
                    f' tl.fromTo(".do", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, stagger: 0.05 }}, {cap("s13", 1)});'
                    f' tl.to(".do", {{ rotation: 72, duration: 0.25, stagger: 0.1, ease: "power2.in" }}, {cap("s13", 2)}); stempeln("#s13x", {cap("s13", 2)} + 0.6);'),
      [(st("s13"), "swipe"), (cap("s13", 2), "nv-explosion-fern"), (cap("s13", 2) + 0.6, "stempel")])

# s14 1,4 Mrd. $ aufgelöst
szene("s14", "handelssaal", titel_zeile("t14", "In 24 Stunden") + tz("n14", "> 1,4 Mrd. $", 680, 140, "glow-r") + kreis("kr14", 540, 770, 460, 150, GELB)
      + partikel("pa14", 540, 770, 30, (ROT, BTC, "#fff"), 600) + stempel("s14x", "ZWANGSWEISE AUFGELÖST", 170, 980, ROT, 44, -4) + quelle("q14", "Krypto-Liquidationen · 13.11.2026", 1120),
      lambda a, d: (f'pop("#t14", {a}); slam("#n14", {cap("s14", 1)}); burst("#pa14", {cap("s14", 1)} + 0.2); draw("#kr14-p", {cap("s14", 1)} + 0.4, 0.5);'
                    f' stempeln("#s14x", {cap("s14", 2)}); pop("#q14", {cap("s14", 2)} + 0.3);'),
      [(st("s14"), "whoosh-weich"), (cap("s14", 1), "glas-bricht"), (cap("s14", 2), "stempel")])

# s15 Angst-Barometer 20/100
GAUGE = ('<svg id="g15" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:3">'
         '<defs><linearGradient id="g15g" x1="0" x2="1"><stop offset="0" stop-color="#e5484d"/><stop offset="0.5" stop-color="#f5c542"/><stop offset="1" stop-color="#2fbf71"/></linearGradient></defs>'
         '<path d="M280 1040 A260 260 0 0 1 800 1040" fill="none" stroke="url(#g15g)" stroke-width="56" stroke-linecap="round"/>'
         '<circle cx="540" cy="1040" r="28" fill="#fff"/></svg>'
         f'<div id="g15n" style="position:absolute;left:532px;top:820px;width:16px;height:220px;border-radius:8px;background:#fff;box-shadow:0 0 20px #fff;transform-origin:50% 100%;z-index:4"></div>')
szene("s15", "bitcoin-muenzen", titel_zeile("t15", "Angst-Barometer") + GAUGE + tz("n15", "20", 610, 110, "glow-r")
      + stempel("s15x", "EXTREME ANGST", 260, 1090, ROT, 56, -4),
      lambda a, d: (f'pop("#t15", {a}); pop("#g15", {a} + 0.1); tl.fromTo("#g15n", {{ rotation: 60 }}, {{ rotation: -54, duration: 1.0, ease: "back.out(1.4)" }}, {cap("s15", 1)});'
                    f' slam("#n15", {cap("s15", 1)} + 0.8); stempeln("#s15x", {cap("s15", 2)});'),
      [(st("s15"), "swipe"), (cap("s15", 1), "spannung"), (cap("s15", 2), "nv-dun-dun-dun")])

# s16 Merk dir
KA = 'style="position:absolute;left:120px;width:840px;padding:34px 40px;border-radius:26px;background:#14181bee;z-index:3;font-weight:900;font-size:50px;color:#fff;'
szene("s16", "wallstreet", titel_zeile("t16", "Merk dir", farbe=GELB)
      + f'<div id="c16a" {KA}top:640px;border:5px solid {ROT};box-shadow:0 0 40px {ROT}55">😱 Panik-Verkauf<div style="font-size:38px;color:#ffffffbb;margin-top:8px">macht den Verlust endgültig</div></div>'
      + f'<div id="c16b" {KA}top:880px;border:5px solid {ROT};box-shadow:0 0 40px {ROT}55">💳 Kauf auf Kredit<div style="font-size:38px;color:#ffffffbb;margin-top:8px">kann dich alles kosten</div></div>',
      lambda a, d: f'pop("#t16", {a}); slam("#c16a", {cap("s16", 1)}); slam("#c16b", {cap("s16", 3)});',
      [(st("s16"), "whoosh-weich"), (cap("s16", 1), "falsch"), (cap("s16", 3), "falsch")])

SZ.append((0.0, DAUER, news_kopf("13.11.2026"), lambda a, d: "", 8))
SZ.append(laufband_szene([("BTC ▼ −6,8 %", ROT), ("UNTER 69.000 $", ROT), ("NVIDIA ▼ −4,3 %", ROT), ("1,4 MRD. $ LIQUIDIERT", ROT),
                          ("ANGST-INDEX 20", GELB), ("ETF-ABFLÜSSE 8 TAGE", ROT)], DAUER))

if __name__ == "__main__":
    build(HERE, SZ, SFX)
