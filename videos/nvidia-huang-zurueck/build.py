#!/usr/bin/env python3
"""HundeFinanzTv (~63 s, Stimme Dan, Tempo 1.12) – Nvidia: Huang ist zurück (23.11.2026). NEUES FORMAT + Laufband.
Quellen: finanzen.net/Yahoo/aktiencheck: Huang nach 11 Tagen wieder CEO, Aktie vorbörslich +27…+32 % (160–166 $), Tief ≈ 125,53 $, seit Anf. Okt. fast −50 %,
Verwaltungsrat: offen/führungsstark/kein Sicherheitsrisiko, Trump für Rückkehr, Ermittlungen laufen weiter. Vorbörsliche Werte!"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 9)  # nach s4

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 15, [], logos=["nvidia.svg"], fotos=["jensen-huang.jpg", "colette-kress.jpg"])
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


def foto(id_, datei, x, y, w, h, pos="50% 15%"):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:8px solid #fff;border-radius:12px;overflow:hidden;'
            f'box-shadow:0 18px 40px #0003;z-index:4"><img src="assets/fotos/{datei}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}"/></div>')


def logo(id_, datei, y, w=520, h=170):
    return (f'<div id="{id_}" class="nk-karte" style="left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;padding:22px">'
            f'<img src="assets/logos/{datei}" style="width:100%;height:{h - 44}px;object-fit:contain"/></div>')


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


def laufband(dauer):
    teile = [("NVDA ▲ +27 % bis +32 % vorbörslich", G), ("Huang ▲ zurück nach 11 Tagen", G), ("Tief ≈ 125 $ ▼", R)]
    t = "".join(f'<span style="margin:0 34px;color:{f}">{tx}</span><span style="color:{O}">●</span>' for tx, f in teile)
    html = (f'<div id="lb" style="position:absolute;left:0;top:1215px;width:1080px;height:84px;background:#fff;border-top:3px solid #e2e5ea;border-bottom:3px solid #e2e5ea;'
            f'overflow:hidden;z-index:8"><div id="lb-s" style="position:absolute;left:0;top:14px;white-space:nowrap;font-weight:800;font-size:42px">{t * 10}</div></div>')
    return (0.0, dauer, html, lambda a, d: f'tl.fromTo("#lb-s", {{ x: 0 }}, {{ x: {-int(d * 90)}, duration: {d}, ease: "none" }}, 0);', 9)


# s1 Hook
S("s1", None, nl.CSS + logo("l1", "nvidia.svg", 330) + gross("n1", "+30 %", 540, G, 270) + pille("p1", "vorbörslich · an einem Tag", 880, G, "#fff", 46),
  lambda a, d: KIT_JS + f' pop("#l1", {a}); pop("#n1", {a} + 0.1); pop("#p1", {cap("s1", 1)});')

# s2 Huang zurück
S("s2", None, foto("f2", "jensen-huang.jpg", 250, 330, 580, 640) + pille("p2", "Jensen Huang ist zurück", 1010, O, "#fff", 52),
  lambda a, d: f'pop("#f2", {a}); pop("#p2", {cap("s2", 1)});')

# s3–s4 Open Loop + Kommentar-Overlay (stumm)
TXT = "Kaufst du jetzt?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 790)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.3)
S("s3", None, titel("t3", "Was ist noch offen?", 380, D, 70) + gross("q3", "?", 500, R, 200) + CTA,
  lambda a, d: f'pop("#t3", {a}); pop("#q3", {a} + 0.2);' + cta_js, SFX_CTA, bis="s5")
S("s5", None, gross("n5", "11 Tage", 340, R, 190) + pille("p5", "nach dem Rücktritt", 600, D, "#fff", 50)
  + foto("f5", "jensen-huang.jpg", 330, 740, 420, 430),
  lambda a, d: f'pop("#n5", {a}); pop("#p5", {cap("s5", 1)}); pop("#f5", {cap("s5", 2)});')

# s6 Kress
S("s6", None, titel("t6", "Seitdem Übergangschefin", 330, D, 56) + foto("f6", "colette-kress.jpg", 300, 460, 480, 560, "50% 20%")
  + pille("p6", "Colette Kress", 1060, O, "#fff", 52),
  lambda a, d: f'pop("#t6", {a}); pop("#f6", {a} + 0.15); pop("#p6", {cap("s6", 1)});')

# s7 Tief
S("s7", None, titel("t7", "Nvidia-Aktie", 340, D, 64)
  + nl.karte("k7", "Kurs", nl.zeile("r7a", "Tief", "≈ 125 $", R, "▼") + nl.zeile("r7b", "Seit Oktober", "fast −50 %", R), y=500),
  lambda a, d: f'pop("#t7", {a}); pop("#k7", {a} + 0.1); pop("#r7a", {cap("s7", 1)}); pop("#r7b", {cap("s7", 2)});')

# s8 Sprung
S("s8", None, titel("t8", "Jetzt vorbörslich", 340, D, 62) + gross("n8", "bis 166 $", 480, G, 190) + pille("p8", "bis zu +32 %", 800, G, "#fff", 60),
  lambda a, d: f'pop("#t8", {a}); pop("#n8", {cap("s8", 0)} + 0.3); pop("#p8", {cap("s8", 2)});')

# s9 Verwaltungsrat
S("s9", None, titel("t9", "Der Verwaltungsrat sagt", 340, D, 58)
  + nl.karte("k9", "Huang ist …", nl.zeile("r9a", "offen", "✓", G) + nl.zeile("r9b", "führungsstark", "✓", G) + nl.zeile("r9c", "kein Sicherheitsrisiko", "✓", G), y=500),
  lambda a, d: f'pop("#t9", {a}); pop("#k9", {a} + 0.1); pop("#r9a", {cap("s9", 1)}); pop("#r9b", {cap("s9", 2)}); pop("#r9c", {cap("s9", 3)});')

# s10 Trump
S("s10", None, titel("t10", "Politischer Rückhalt", 340, D, 58)
  + nl.karte("k10", "US-Präsident Trump", f'<div style="font-weight:800;font-size:56px;color:{D};text-align:center;padding:16px 0">hat sich für die<br/><span style="color:{O}">Rückkehr starkgemacht</span></div>', y=520),
  lambda a, d: f'pop("#t10", {a}); pop("#k10", {a} + 0.15);')

# s11–s12 Vorsicht
S("s11", None, titel("t11", "Alles gut also?", 380, D, 66) + gross("w11", "⚠️", 520, R, 230) + pille("p11", "Ermittlungen laufen weiter", 830, R, "#fff", 52),
  lambda a, d: f'pop("#t11", {a}); pop("#w11", {a} + 0.2); pop("#p11", {cap("s11", 1)});')
S("s12", None, titel("t12", "Die Rückkehr klärt nur", 340, D, 60)
  + nl.karte("k12", "Geklärt / Offen", nl.zeile("r12a", "Wer führt die Firma", "✓", G) + nl.zeile("r12b", "Wie die Untersuchungen enden", "?", R), y=520),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 1)}); pop("#r12b", {cap("s12", 2)});')

# s13–s14 Depot + Hinweis
S("s13", None, titel("t13", "Und dein Depot?", 340, D, 66)
  + nl.karte("k13", "Globaler ETF", nl.zeile("r13a", "Nvidia steckt drin", "✓", G) + nl.zeile("r13b", "Wenn Nvidia steigt", "▲", G) + nl.zeile("r13c", "Wenn Nvidia fällt", "▼", R), y=500),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.1); pop("#r13a", {cap("s13", 1)}); pop("#r13b", {cap("s13", 2)}); pop("#r13c", {cap("s13", 3)});', bis="s15")

# s15 Folgen
S("s15", None, f'<div id="fl15" style="position:absolute;left:340px;top:420px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n15" class="nk-gross" style="top:860px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c15", "+ Folgen", 980, O, "#fff", 58),
  lambda a, d: f'pop("#fl15", {a}); pop("#n15", {a} + 0.2); pop("#c15", {cap("s15", 0)} + 0.4);')

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "mm-kamera"), (cap("s7", 1), "kurve-runter"), (cap("s8", 0) + 0.3, "kurve-hoch"), (cap("s11", 1), "alarm"), (cap("s12", 2), "falsch")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("BÖRSENNEWS", "23.11.2026"), lambda a, d: "", 8))
K.SZ.append(laufband(K.dauer))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
