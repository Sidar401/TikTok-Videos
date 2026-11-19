#!/usr/bin/env python3
"""HundeFinanzTv Börsentag 19.11.2026 (~74 s, NEUES FORMAT: heller News-Look). Anthropic 83 $ → 111,50 $ (+34 %, 81,3 Mrd. $ Rekord),
DAX −1,06 % auf 25.463,81 (Rekord 27.001), Fed-Protokoll: weitere Zinserhöhungen möglich, Bitcoin ≈ 63.800 $ (−22 % in 1 Monat),
Gold Tief seit Sept. 2025, Walmart Zahlen besser (188,8 vs 187,2 Mrd. $, EPS 0,65 vs 0,64, Prognose erhöht), Aktie ≈ −2 %."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 12)  # Logo nach dem Open Loop (s3)

import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from glow_short import build  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D = nl.G, nl.R, nl.DUNKEL
K = Kit(HERE, 15, [], logos=["anthropic.svg", "claude.svg", "fed.png", "bitcoin.svg", "walmart.svg", "nasdaq.svg", "flagge-deutschland.svg"])
cap, st = K.cap, K.st
S = K.szene


def pops(ids_zeiten):
    return " ".join(f'pop("#{i}", {t});' for i, t in ids_zeiten)


# s1–s2 Einstieg
S("s1", None, nl.CSS
  + f'<div id="t1" class="nk-gross" style="top:360px;font-size:66px;line-height:1.15">Alles, was heute<br/>an der Börse passiert ist</div>'
  + f'<div id="b1" style="position:absolute;left:390px;top:570px;padding:14px 40px;border-radius:50px;background:{D};color:#fff;font-weight:800;font-size:46px;z-index:4">in 60 Sekunden</div>'
  + f'<div id="k1a" class="nk-karte" style="left:110px;top:760px;width:400px;text-align:center"><img src="assets/logos/anthropic.svg" style="width:300px"/>'
    f'<div style="font-weight:800;font-size:78px;color:{G};margin-top:24px">+34 %</div></div>'
  + f'<div id="k1b" class="nk-karte" style="left:570px;top:760px;width:400px;text-align:center"><div style="font-weight:800;font-size:58px;color:{D}">DAX</div>'
    f'<div style="font-weight:800;font-size:78px;color:{R};margin-top:14px">−1,1 %</div></div>',
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#b1", {cap("s1", 2)}); pop("#k1a", {cap("s2", 0)} + 0.6); pop("#k1b", {cap("s2", 2)});',
  [], bis="s3")

# s3 Open Loop: die Angst
S("s3", None, nl.logo_frei("l3", "fed.png", 400, 380, 280)
  + nl.karte("k3", "Was steckt dahinter?", f'<div style="font-weight:900;font-size:150px;color:{R};text-align:center;line-height:1.1">?</div>'
             f'<div style="text-align:center;font-size:40px;color:#3a414c">Die Angst, die auch<br/>dein Depot trifft</div>', y=720),
  lambda a, d: f'pop("#l3", {a}); pop("#k3", {cap("s3", 1)});')

# s4–s6 Anthropic
ANT = (nl.zeile("r4a", "Ausgabepreis", "83 $") + nl.zeile("r4b", "Erster Kurs", "111,50 $", G, "▲")
       + nl.zeile("r4c", "Plus", "+34 %", G, "✓") + nl.zeile("r4d", "Erlös", "81,3 Mrd. $", D, "🏆"))
S("s4", None, nl.logo_frei("l4", "anthropic.svg", 210, 360, 660) + nl.logo_frei("l4b", "claude.svg", 390, 490, 300)
  + nl.karte("k4", "Anthropic Börsengang", ANT, y=670),
  lambda a, d: (f'pop("#l4", {a}); pop("#l4b", {cap("s4", 2)}); pop("#k4", {cap("s5", 0)} - 0.3);'
                + pops([("r4a", cap("s5", 0)), ("r4b", cap("s5", 1)), ("r4c", cap("s5", 1) + 0.6), ("r4d", cap("s6", 0))])),
  [], bis="s7")

# s7 DAX-Kurve
P = [(0, 0.55), (1, 0.62), (2, 0.78), (3, 0.95), (4, 0.7), (5, 0.42), (6, 0.25), (7, 0.12)]
PFAD = "M" + " L".join(f"{60 + i * 100} {40 + 300 * (1 - v)}" for i, v in P)
KURVE = (f'<svg viewBox="0 0 800 380" style="width:780px;height:370px"><path id="dx-f" d="{PFAD} L760 380 L60 380 Z" fill="{R}22"/>'
         f'<path id="dx-p" d="{PFAD}" fill="none" stroke="{R}" stroke-width="7"/><circle id="dx-k" cx="760" cy="304" r="12" fill="{R}"/>'
         f'<text x="600" y="350" font-size="40" font-weight="700" fill="{R}" style="font-family:Montserrat">25.464</text>'
         f'<text x="270" y="30" font-size="30" fill="#555" style="font-family:Montserrat">Rekord 27.001</text></svg>')
S("s7", None, f'<img id="l7" src="assets/logos/flagge-deutschland.svg" style="position:absolute;left:470px;top:350px;width:140px;border-radius:6px;box-shadow:0 6px 14px #0002;z-index:4"/>'
  + nl.karte("k7", "DAX – letzte 8 Tage", KURVE + nl.zeile("r7a", "Heute", "−1,06 %", R) + nl.zeile("r7b", "Seit Rekord", "≈ −5 %", R), y=480),
  lambda a, d: f'pop("#l7", {a}); pop("#k7", {a} + 0.1); draw("#dx-p", {a} + 0.3, 1.4); pop("#r7a", {cap("s7", 1)}); pop("#r7b", {cap("s7", 1)} + 0.8);')

# s8–s9 Notenbank
FED = (f'<div id="q8" style="font-size:44px;color:{D};line-height:1.35;padding:10px 0 20px">„Weitere Zinserhöhungen<br/>könnten nötig sein.“</div>'
       + nl.zeile("r8a", "Zinsen", "▲ höher", R) + nl.zeile("r8b", "Kredite", "teurer", R) + nl.zeile("r8c", "Aktien", "weniger attraktiv", R))
S("s8", None, nl.logo_frei("l8", "fed.png", 420, 340, 240) + nl.karte("k8", "Protokoll der US-Notenbank", FED, y=620),
  lambda a, d: (f'pop("#l8", {a}); pop("#k8", {cap("s8", 1)}); pop("#q8", {cap("s8", 2)});'
                + pops([("r8a", cap("s9", 0)), ("r8b", cap("s9", 1)), ("r8c", cap("s9", 2))])),
  [], bis="s10")

# s10–s11 Bitcoin & Gold
GOLD = '<div style="width:150px;height:70px;border-radius:8px;background:linear-gradient(135deg,#f6dc7d,#c99a2e 60%,#f1d27a);box-shadow:0 6px 14px #0002"></div>'
KG = (f'<div id="r10" style="display:flex;align-items:center;gap:30px;padding:26px 0;border-bottom:2px solid #eef0f3"><img src="assets/logos/bitcoin.svg" style="width:120px"/>'
      f'<div><div style="font-weight:700;font-size:46px;color:{D}">Bitcoin</div><div style="font-size:32px;color:#777">≈ 63.800 $</div></div>'
      f'<div style="margin-left:auto;font-weight:800;font-size:50px;color:{R};text-align:right">−22 %<div style="font-size:26px;color:#888;font-weight:500">seit 1 Monat</div></div></div>'
      f'<div id="r11" style="display:flex;align-items:center;gap:30px;padding:26px 0">{GOLD}'
      f'<div><div style="font-weight:700;font-size:46px;color:{D}">Gold</div><div style="font-size:32px;color:#777">≈ 3.700 $</div></div>'
      f'<div style="margin-left:auto;font-weight:800;font-size:44px;color:{R};text-align:right">Tief<div style="font-size:26px;color:#888;font-weight:500">seit Sept. 2025</div></div></div>')
S("s10", None, nl.karte("k10", "Krypto &amp; Gold", KG, y=420),
  lambda a, d: f'pop("#k10", {a}); pop("#r10", {cap("s10", 0)} + 0.4); pop("#r11", {cap("s11", 0)});', [], bis="s12")

# s12 Walmart
WM = (f'<div class="nk-row" style="font-size:28px;color:#999;padding:4px 0"><span style="margin-left:auto;width:240px;text-align:right">Ist</span>'
      f'<span style="width:240px;text-align:right">Erwartet</span><span style="width:80px"></span></div>'
      + "".join(f'<div id="r12{k}" class="nk-row" style="font-size:36px">{l}<span style="margin-left:auto;width:240px;text-align:right;font-weight:800;color:{G}">{x}</span>'
                f'<span style="width:240px;text-align:right">{y}</span><span class="nk-ok" style="width:80px;text-align:right">✓</span></div>'
                for k, (l, x, y) in enumerate((("Umsatz", "188,8 Mrd. $", "187,2 Mrd. $"), ("Gewinn je Aktie", "0,65 $", "0,64 $"), ("Prognose", "erhöht", "–"))))
      + f'<div id="r12x" class="nk-row" style="border-top:2px solid #e8eaee;margin-top:10px">Aktie heute<span class="v" style="color:{R}">≈ −2 %</span></div>')
S("s12", None, nl.logo_frei("l12", "walmart.svg", 290, 360, 500) + nl.karte("k12", "Walmart Quartalszahlen", WM, y=540),
  lambda a, d: (f'pop("#l12", {a}); pop("#k12", {a} + 0.2);'
                + pops([("r120", cap("s12", 0) + 0.5), ("r121", cap("s12", 1)), ("r122", cap("s12", 1) + 0.5), ("r12x", cap("s12", 3))])))

# s13 Fazit: Überblick
T13 = [("anthropic.svg", "+34 %", True), ("nasdaq.svg", "im Minus", False), (None, "DAX −1,1 %", False), (None, "Zinsen ▲", False),
       ("bitcoin.svg", "−22 % / Monat", False), ("walmart.svg", "≈ −2 %", False)]
RASTER = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">' + "".join(nl.kachel(f"c13{i}", f, t, g) for i, (f, t, g) in enumerate(T13)) + '</div>'
S("s13", None, nl.karte("k13", "Börse heute, 19.11.", RASTER + '<div style="margin-top:20px;font-size:24px;color:#8a909a;text-align:right">Stand 19.11., ca. 18 Uhr</div>', y=380),
  lambda a, d: f'pop("#k13", {a}); ' + pops([(f"c13{i}", a + 0.25 + i * 0.25) for i in range(6)]))

# s14 Hinweis
S("s14", None, nl.karte("k14", "Kurzer Hinweis", f'<div style="font-size:52px;font-weight:800;color:{D};text-align:center;padding:30px 0">Keine Anlageberatung –<br/>nur erklärt.</div>', y=700),
  lambda a, d: f'pop("#k14", {a});')

# s15 Folgen
S("s15", None, f'<div id="fl15" style="position:absolute;left:340px;top:520px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {nl.ORANGE};'
  f'box-shadow:0 20px 50px #0003;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n15" class="nk-gross" style="top:960px;font-size:64px">HundeFinanzTv</div>'
  + f'<div id="c15" style="position:absolute;left:350px;top:1080px;width:380px;padding:18px 0;border-radius:50px;background:{nl.ORANGE};color:#fff;'
    f'font-weight:900;font-size:58px;text-align:center;box-shadow:0 12px 30px #f28a1e66;z-index:4">+ Folgen</div>',
  lambda a, d: (f'pop("#fl15", {a}); pop("#n15", {a} + 0.2); pop("#c15", {cap("s15", 0)} + 0.4);'
                f' tl.fromTo("#c15", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {cap("s15", 0)} + 0.8);'))

html, code = ls.szene()
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("BÖRSENNEWS", "19.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
