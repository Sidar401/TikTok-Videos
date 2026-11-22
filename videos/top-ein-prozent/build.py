#!/usr/bin/env python3
"""HundeFinanzTv (~65 s, Stimme Dan, Tempo 1.12) – Top 1 % Vermögen Deutschland. NEUES FORMAT, Puffer ohne Datum.
Median ≈ 100.000 € (Bundesbank PHF 2023: ≈103–106 Tsd.), Top 1 % ab ≈ 2,3 Mio. €/Haushalt (je Studie 1,3–2,9 Mio.), hält ≈ 25–33 % des Vermögens;
Eigene Rechnung: 1.000 €/Monat @7 % → ≈ 39 J., 500 € → ≈ 49 J. bis 2,3 Mio. Kommentar-Overlay (stumm) s2–s3, Logo-Intro nach s4."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 10)  # nach s4

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 15, [])
cap, st = K.cap, K.st
S = K.szene
SFX_CTA = []


def titel(id_, text, y=340, farbe=D, gr=64):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=50):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.05">{text}</div>'


def balken(id_, y, breite, farbe, text, h=96, gr=38, x=110):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def bar(id_, a):
    return f'tl.fromTo("#{id_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, {a});'


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


# 10×10 Raster: 1 von 100 Haushalten
PUNKTE = "".join(f'<div class="pt" style="width:50px;height:50px;border-radius:50%;background:{"#f28a1e" if i == 0 else "#c9ced5"}"></div>' for i in range(100))
RASTER = f'<div id="ras" style="position:absolute;left:110px;top:400px;width:860px;display:grid;grid-template-columns:repeat(10,1fr);gap:16px;z-index:4;justify-items:center">{PUNKTE}</div>'

# s1 Hook
S("s1", None, nl.CSS + titel("t1", "Reichste 1 % in Deutschland", 340, D, 58) + gross("n1", "ab wie viel?", 490, O, 125) + gross("q1", "💰", 720, D, 230),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#n1", {a} + 0.15); pop("#q1", {cap("s1", 1)});')

# s2–s3: Rätsel + Kommentar-Overlay (stumm)
TXT = "Wie reich fühlst du dich?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s2"), len(TXT), SFX_CTA, 1.5)
S("s2", None, titel("t2", "Kleiner als gedacht", 380, D, 70) + gross("q2", "10 Mio.?", 540, R, 200) + pille("p2", "Nein – deutlich weniger", 820, G, "#fff", 46)
  + titel("t3", "Wie lange sparen?", 380, O, 70) + CTA,
  lambda a, d: (f'pop("#t2", {a}); pop("#q2", {a} + 0.2); pop("#p2", {cap("s2", 0)} + 1.2); tl.set("#t3", {{ opacity: 0 }}, 0);'
                + raus("t2", st("s3") - 0.05) + raus("q2", st("s3") - 0.05) + raus("p2", st("s3") - 0.05) + f' pop("#t3", {st("s3")});' + cta_js),
  SFX_CTA, bis="s4")
S("s4", None, titel("t4", "Schauen wir genau hin", 640, D, 78) + pille("p4", "Vermögen in Deutschland", 900, O, "#fff", 50),
  lambda a, d: f'pop("#t4", {a}); pop("#p4", {a} + 0.3);')

# s5 Mitte
S("s5", None, titel("t5", "Haushalt in der Mitte", 340, D, 60) + gross("n5", "≈ 100.000 €", 490, O, 125)
  + nl.karte("k5", "Zählt dazu", nl.zeile("r5a", "Haus, Auto, Konto, Aktien", "+", G) + nl.zeile("r5b", "Schulden", "−", R), y=760),
  lambda a, d: f'pop("#t5", {a}); pop("#n5", {cap("s5", 0)} + 0.2); pop("#k5", {cap("s5", 1)}); pop("#r5a", {cap("s5", 1)} + 0.3); pop("#r5b", {cap("s5", 2)});')

# s6 Top 1 %
S("s6", None, titel("t6", "Reichstes 1 % beginnt bei", 340, D, 56) + gross("n6", "≈ 2,3 Mio. €", 490, R, 125) + pille("p6", "pro Haushalt · Bundesbank", 760, D, "#fff", 44),
  lambda a, d: f'pop("#t6", {a}); pop("#n6", {cap("s6", 1)}); pop("#p6", {cap("s6", 2)});')

# s7 Spanne
SP = (f'<div id="sp" style="position:absolute;left:110px;top:560px;width:860px;height:110px;background:#e4e7ec;border-radius:14px;z-index:4;box-shadow:0 12px 26px #0002">'
      f'<div id="spb" style="position:absolute;left:0;top:0;width:{round(860 * (2.9 - 1.3) / 3)}px;height:110px;margin-left:{round(860 * 1.3 / 3)}px;background:{O};border-radius:14px;transform-origin:0 50%"></div></div>'
      f'<div style="position:absolute;left:110px;top:690px;width:860px;display:flex;justify-content:space-between;font-weight:800;font-size:40px;color:{D};z-index:4"><span>0</span><span>1 Mio.</span><span>2 Mio.</span><span>3 Mio.</span></div>')
S("s7", None, titel("t7", "Je nach Studie", 340, D, 62) + SP + pille("p7", "1,3 bis 2,9 Mio. €", 800, O, "#fff", 54),
  lambda a, d: f'pop("#t7", {a}); pop("#sp", {a} + 0.1); tl.fromTo("#spb", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8 }}, {cap("s7", 1)}); pop("#p7", {cap("s7", 2)});')

# s8 20×
S("s8", None, titel("t8", "Verglichen mit der Mitte", 340, D, 56) + gross("n8", "20×", 480, R, 330) + pille("p8", "mehr Vermögen", 900, R, "#fff", 52),
  lambda a, d: f'pop("#t8", {a}); pop("#n8", {a} + 0.2); pop("#p8", {cap("s8", 1)});')

# s9 Raster
S("s9", None, titel("t9", "1 von 100 Haushalten", 330, D, 58) + RASTER + gross("n9", "¼ – ⅓ vom Vermögen", 1110, O, 62),
  lambda a, d: f'pop("#t9", {a}); tl.fromTo("#ras .pt", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, stagger: 0.008, ease: "back.out(2)" }}, {a} + 0.2); pop("#n9", {cap("s9", 2)});')

# s10 / s11 Sparen
S("s10", None, titel("t10", "Bis 2,3 Mio. € sparen", 340, D, 58)
  + nl.karte("k10", "1.000 € im Monat · 7 % Rendite", f'<div style="font-weight:900;font-size:130px;color:{R};text-align:center;line-height:1.1">≈ 39 Jahre</div>', y=520),
  lambda a, d: f'pop("#t10", {a}); pop("#k10", {a} + 0.1);')
S("s11", None, titel("t11", "Bis 2,3 Mio. € sparen", 340, D, 58)
  + nl.karte("k11", "500 € im Monat · 7 % Rendite", f'<div style="font-weight:900;font-size:130px;color:{R};text-align:center;line-height:1.1">≈ 49 Jahre</div>', y=520),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {a} + 0.1);')

# s12 Quellen des Reichtums
S("s12", None, titel("t12", "Bei den Reichsten steckt es in", 340, D, 54) + pille("p12a", "Firmen", 520, O, "#fff", 66) + pille("p12b", "Immobilien", 680, G, "#fff", 66) + pille("p12c", "Erbe", 840, D, "#fff", 66),
  lambda a, d: f'pop("#t12", {a}); pop("#p12a", {cap("s12", 1)}); pop("#p12b", {cap("s12", 1)} + 0.5); pop("#p12c", {cap("s12", 1)} + 1.0);')

# s13–s14 Merk dir
S("s13", None, titel("t13", "Merk dir", 340, O, 70)
  + nl.karte("k13", "Reich ist …", nl.zeile("r13a", "nicht, was du verdienst", "✗", R) + nl.zeile("r13b", "sondern, was dir gehört", "✓", G), y=500),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.1); pop("#r13a", {cap("s13", 1)}); pop("#r13b", {cap("s13", 2)});', bis="s15")

# s15 Folgen
S("s15", None, f'<div id="fl15" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n15" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c15", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl15", {a}); pop("#n15", {a} + 0.2); pop("#c15", {cap("s15", 0)} + 0.4);')

K.SFX.extend([(0.05, "bass-schlag"), (cap("s6", 1), "mm-bumm"), (cap("s8", 0) + 0.2, "richtig"), (cap("s10", 1), "uhr-tickt"), (cap("s13", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", ""), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
