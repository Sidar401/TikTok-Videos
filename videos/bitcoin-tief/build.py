#!/usr/bin/env python3
"""HundeFinanzTv Short (Analyse-Look, ~70 s): Bitcoin stürzt auf 3-Monats-Tief – 3 Gründe."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, flagge, hand, karte, kasten, kit_assets, kreis, linie,  # noqa: E402
                         logo_karte, pfeil, stempel, ticker, unterstrich, zettel)
from glow_short import TEILEN_SVG, build, cta_szene, partikel, t, zeiten  # noqa: E402

BTC = "#f7931a"
kit_assets(HERE, ["bitcoin", "flagge-usa"])
cap, st, en, DAUER = zeiten(HERE)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def muenze(id_, x, y, gr=260):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{gr}px;border-radius:50%;'
            f'background:radial-gradient(circle at 35% 30%,#ffd28a,{BTC} 55%,#a85e00);box-shadow:0 0 80px {BTC}aa, 0 30px 50px #000;'
            f'display:flex;align-items:center;justify-content:center;z-index:3"><img src="assets/logos/bitcoin.svg" style="width:78%" alt=""/></div>')


# 1–2 Hook: Absturz
KURS = linie("hk", [0.62, 0.75, 0.7, 0.86, 0.8, 0.6, 0.48, 0.3, 0.12], 120, 700, 840, 420, ROT, punkte=[(8, "73.500 $")])
TK = ticker("tk", [("BTC", BTC), ("▼ 3-MONATS-TIEF", ROT), ("< 75.000 $", None), ("−40 % vom Rekord", ROT)], 1200, ROT)
S1 = (KIT_CSS + muenze("hk-m", 830, 600, 170) + tz("hk-t", "tiefster Stand", 450, 80) + tz("hk-t2", "seit August", 550, 80, "glow-r")
      + KURS + TK + stempel("hk-s", "UNTER 75.000 $", 330, 760, ROT, 60, -6))


def j1(a, d):
    return (KIT_JS + f' tl.fromTo("#hk-m", {{ rotationY: 0, scale: 0 }}, {{ rotationY: 360, scale: 1, duration: 0.7, ease: "back.out(1.6)" }}, {a}); flash({a}, 0.5);'
            f' pop("#hk-t", {cap("s1", 1)}); slam("#hk-t2", {cap("s1", 2)}); draw("#hk-p", {cap("s1", 1)}, 1.6); stempeln("#hk-s", {cap("s2", 0)});'
            f' tl.fromTo("#hk-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s2", 1)}); pop("#hk-w0", {cap("s2", 2)}); lauf("#tk", {a}, {d});')


cta_html, cta_js = cta_szene("te", TEILEN_SVG, "Schick das jemandem,<br/>der Bitcoin hat!")
S4 = zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Erklärung", 200, 560, 680, 80, GELB, -3)
J4 = lambda a, d: f'tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});'  # noqa: E731

# 5–6 Rekord vs. heute: −40 %
S5 = (karte("rk-k", 70, 440, 940, 840, "Bitcoin in Dollar", "Rekord Okt. 2025 vs. heute")
      + f'<div id="rk-a" style="position:absolute;left:220px;top:{1180 - 500}px;width:240px;height:500px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{BTC},{BTC}88);box-shadow:0 0 40px {BTC}77;transform-origin:50% 100%;z-index:3"></div>'
      + f'<div id="rk-b" style="position:absolute;left:620px;top:{1180 - 295}px;width:240px;height:295px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);box-shadow:0 0 40px {ROT}77;transform-origin:50% 100%;z-index:3"></div>'
      + f'<div id="rk-ta" class="mono" style="position:absolute;left:140px;width:400px;top:610px;text-align:center;font-size:54px;color:{BTC};z-index:5">126.000 $</div>'
      + f'<div id="rk-tb" class="mono" style="position:absolute;left:540px;width:400px;top:810px;text-align:center;font-size:54px;color:{ROT};z-index:5">74.000 $</div>'
      + '<div class="mono" style="position:absolute;left:140px;width:400px;top:1195px;text-align:center;font-size:32px;color:#ffffffcc;z-index:5">Okt. 2025</div>'
      + '<div class="mono" style="position:absolute;left:540px;width:400px;top:1195px;text-align:center;font-size:32px;color:#ffffffcc;z-index:5">heute</div>'
      + pfeil("rk-p", 470, 690, 640, 800, -0.3, GELB, 8) + hand("rk-h", "−40 %", 760, 600, 110, GELB, -6, True))


def j5(a, d):
    return (f'pop("#rk-k", {a}); tl.fromTo("#rk-a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6, ease: "power3.out" }}, {cap("s5", 1)}); pop("#rk-ta", {cap("s5", 2)});'
            f' tl.fromTo("#rk-b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6, ease: "power3.out" }}, {cap("s5", 2)} + 0.8); pop("#rk-tb", {cap("s5", 2)} + 1.2);'
            f' draw("#rk-p-p", {cap("s6", 0)}, 0.4); pop("#rk-p-k", {cap("s6", 0)} + 0.35); slam("#rk-h", {cap("s6", 1)});')


def grund(n, titel, farbe):
    return (tz(f"g{n}-a", f"GRUND {n}", 520, 90, "glow-o") + tz(f"g{n}-b", f'<span class="box">{titel}</span>', 660, 100)
            + unterstrich(f"g{n}-u", 290, 820, 500, farbe))


def gj(n, sid):
    return lambda a, d: f'slam("#g{n}-a", {a}); pop("#g{n}-b", {cap(sid, 1)}); draw("#g{n}-u-p", {cap(sid, 1)} + 0.3, 0.4); flash({a}, 0.4);'


# 7 Grund 1: Inflation USA
S7 = grund(1, "Inflation USA", ROT) + flagge("g1-f", "flagge-usa", 400, 890, 280, -4)
J7 = lambda a, d: gj(1, "s7")(a, d) + f' pop("#g1-f", {cap("s7", 1)} + 0.2);'  # noqa: E731

# 8–9 Zinsen ↑ → sicheres Geld ↑, Bitcoin ↓ (Wippe)
WIPPE = (f'<div id="wp" style="position:absolute;left:140px;top:880px;width:800px;height:16px;border-radius:8px;background:#fff;box-shadow:0 0 30px #fff8;transform-origin:50% 50%;z-index:3"></div>'
         f'<div style="position:absolute;left:500px;top:896px;width:0;height:0;border-left:40px solid transparent;border-right:40px solid transparent;border-bottom:80px solid {GRAU};z-index:2"></div>')
S8 = (kasten("zi-a", "Inflation ↑", 80, 450, 400, 150, ROT, 56) + pfeil("zi-p", 490, 525, 590, 525, 0.0, "#fff", 8) + kasten("zi-b", "Zinsen ↑ ?", 600, 450, 400, 150, OR, 56)
      + WIPPE + kasten("zi-c", "sicheres Geld<br/>+ Zinsen", 150, 700, 330, 170, GRUEN, 44) + muenze("zi-m", 680, 660, 200)
      + hand("zi-h", "weniger attraktiv", 780, 1000, 54, GELB, -3, True))


def j8(a, d):
    return (f'pop("#zi-a", {a}); draw("#zi-p-p", {cap("s8", 1)}, 0.3); pop("#zi-p-k", {cap("s8", 1)} + 0.25); pop("#zi-b", {cap("s8", 2)});'
            f' pop("#wp", {st("s9")}); pop("#zi-c", {cap("s9", 1)}); pop("#zi-m", {cap("s9", 3)});'
            f' tl.fromTo("#wp", {{ rotation: 0 }}, {{ rotation: 8, duration: 0.6, ease: "back.out(2)" }}, {cap("s9", 4)});'
            f' tl.fromTo("#zi-c", {{ y: 0 }}, {{ y: 40, duration: 0.6, ease: "back.out(2)" }}, {cap("s9", 4)}); tl.fromTo("#zi-m", {{ y: 0 }}, {{ y: -60, duration: 0.6, ease: "back.out(2)" }}, {cap("s9", 4)});'
            f' pop("#zi-h", {cap("s9", 5)});')


# 10 Grund 2: Große Anleger ziehen ab
S10 = grund(2, "Geld fließt ab", ROT)
J10 = gj(2, "s10")

# 11 ETF-Abflüsse 1,3 Mrd. $
ROHR = (f'<div id="ab-r" style="position:absolute;left:160px;top:700px;width:760px;height:120px;border-radius:60px;background:#1b1f22;border:5px solid {BTC};z-index:2"></div>'
        + "".join(f'<div class="dl" style="position:absolute;left:{200 + k * 90}px;top:735px;width:50px;height:50px;border-radius:50%;background:{BTC};box-shadow:0 0 16px {BTC};z-index:3"></div>' for k in range(8)))
S11 = (tz("ab-t", "Bitcoin-ETFs in den USA", 470, 60) + flagge("ab-f", "flagge-usa", 440, 560, 200, -3) + ROHR + pfeil("ab-p", 900, 760, 1010, 1000, -0.2, ROT, 10)
       + tz("ab-z", "−1,3 Mrd. $", 960, 130, "glow-r") + hand("ab-h", "in nur 1 Woche", 540, 1130, 60, GELB, -3, True))


def j11(a, d):
    return (f'pop("#ab-t", {a}); pop("#ab-f", {cap("s11", 1)}); pop("#ab-r", {cap("s11", 1)} + 0.2);'
            f' tl.fromTo(".dl", {{ x: 0, opacity: 1 }}, {{ x: 140, opacity: 0, duration: 0.6, stagger: 0.08, repeat: 3, ease: "power1.in" }}, {cap("s11", 2)});'
            f' draw("#ab-p-p", {cap("s11", 2)}, 0.4); pop("#ab-p-k", {cap("s11", 2)} + 0.35); slam("#ab-z", {cap("s11", 3)}); pop("#ab-h", {cap("s11", 4)});')


# 12 Grund 3: Wetten auf Kredit
S12 = grund(3, "Wetten auf Kredit", OR).replace("font-size:100px", "font-size:80px")
J12 = gj(3, "s12")

# 13–14 Hebel: geliehenes Geld → Zwangsverkauf (Domino)
DOM = "".join(f'<div class="do" style="position:absolute;left:{150 + k * 120}px;top:860px;width:60px;height:240px;border-radius:10px;background:linear-gradient(180deg,{BTC},#a85e00);'
              f'box-shadow:0 0 20px {BTC}77;transform-origin:100% 100%;z-index:3"></div>' for k in range(7))
S13 = (kasten("hb-a", "eigenes Geld", 80, 450, 360, 140, GRUEN, 50) + tz("hb-plus", "+", 470, 100) + kasten("hb-b", "geliehenes Geld", 560, 450, 440, 140, ROT, 50)
       + hand("hb-h", "auf steigende Kurse", 540, 640, 56, GELB, -3, True) + DOM + stempel("hb-s", "AUTOMATISCH VERKAUFT", 140, 1150, ROT, 52, -5))


def j13(a, d):
    return (f'pop("#hb-a", {cap("s13", 0)}); pop("#hb-plus", {cap("s13", 0)} + 0.2); pop("#hb-b", {cap("s13", 0)} + 0.4); pop("#hb-h", {cap("s13", 1)});'
            f' tl.fromTo(".do", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, stagger: 0.05 }}, {cap("s13", 2)});'
            f' tl.to(".do", {{ rotation: 72, duration: 0.25, stagger: 0.12, ease: "power2.in" }}, {cap("s14", 1)}); stempeln("#hb-s", {cap("s14", 2)} + 0.3);')


# 15 > 1 Mrd. $ aufgelöst
S15 = (tz("li-a", "an einem Wochenende", 470, 64) + tz("li-z", "> 1 Mrd. $", 590, 150, "glow-r") + tz("li-u", "zwangsweise aufgelöst", 830, 70)
       + kreis("li-k", 540, 700, 440, 150, GELB) + partikel("li-p", 540, 700, 30, (ROT, BTC, "#fff"), 600) + stempel("li-s", "LIQUIDIERT", 330, 1010, ROT, 70, -6))


def j15(a, d):
    return (f'pop("#li-a", {cap("s15", 1)}); slam("#li-z", {cap("s15", 2)}); burst("#li-p", {cap("s15", 2)} + 0.2); draw("#li-k-p", {cap("s15", 2)} + 0.5, 0.5);'
            f' pop("#li-u", {cap("s15", 3)}); stempeln("#li-s", {cap("s15", 3)} + 0.5);')


# 16–17 Was heißt das für dich?
S16 = (tz("fd-t", "Was heißt das für dich?", 460, 70, "glow-o")
       + f'<div id="fd-1" style="position:absolute;left:120px;top:600px;width:840px;padding:34px 40px;border-radius:26px;background:#14181b;border:5px solid {ROT};box-shadow:0 0 40px {ROT}55;z-index:3;font-weight:900;font-size:56px;color:#fff">❌ nie auf Kredit</div>'
       + f'<div id="fd-2" style="position:absolute;left:120px;top:820px;width:840px;padding:34px 40px;border-radius:26px;background:#14181b;border:5px solid {GRUEN};box-shadow:0 0 40px {GRUEN}55;z-index:3;font-weight:900;font-size:50px;color:#fff">✅ nur Geld, dessen Verlust du verkraftest</div>'
       + muenze("fd-m", 455, 1080, 170))


def j16(a, d):
    return f'pop("#fd-t", {a}); pop("#fd-m", {a} + 0.2); slam("#fd-1", {cap("s17", 0)}); slam("#fd-2", {cap("s17", 2)});'


SZENEN = [
    (0.0, st("s3"), S1, j1), (st("s3"), st("s4"), cta_html, cta_js), (st("s4"), st("s5"), S4, J4), (st("s5"), st("s7"), S5, j5),
    (st("s7"), st("s8"), S7, J7), (st("s8"), st("s10"), S8, j8), (st("s10"), st("s11"), S10, J10), (st("s11"), st("s12"), S11, j11),
    (st("s12"), st("s13"), S12, J12), (st("s13"), st("s15"), S13, j13), (st("s15"), st("s16"), S15, j15), (st("s16"), DAUER, S16, j16),
]
SFX = [(0.0, "nv-boom-tief"), (0.05, "muenzen-klimpern"), (cap("s1", 1), "kurve-runter"), (cap("s2", 0), "stempel"), (cap("s2", 2), "bass-schlag"),
       (st("s3"), "whoosh-weich"), (st("s4"), "swipe"), (st("s5"), "whoosh-weich"), (cap("s5", 1), "kurve-hoch"), (cap("s5", 2) + 0.8, "kurve-runter"), (cap("s6", 1), "nv-dun-dun-dun"),
       (st("s7"), "nv-boom-kurz"), (st("s8"), "swipe"), (cap("s8", 2), "alarm"), (cap("s9", 4), "whoosh-schnell"), (st("s10"), "nv-boom-kurz"),
       (st("s11"), "whoosh-weich"), (cap("s11", 2), "nv-sog"), (cap("s11", 3), "kasse"), (st("s12"), "nv-boom-kurz"), (st("s13"), "swipe"),
       (cap("s14", 1), "nv-explosion-fern"), (cap("s14", 2) + 0.3, "stempel"), (st("s15"), "whoosh-weich"), (cap("s15", 2), "glas-bricht"), (cap("s15", 3) + 0.5, "stempel"),
       (st("s16"), "whoosh-weich"), (cap("s17", 0), "falsch"), (cap("s17", 2), "richtig")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
