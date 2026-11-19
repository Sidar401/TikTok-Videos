#!/usr/bin/env python3
"""HundeFinanzTv (~2:00, Stimme Dan): Wie bewertet man eine Aktie? 4 Prüfungen der Profis:
1 Börsenwert (Preis × Aktien), 2 KGV (Pizzeria 150.000 € / 10.000 € = 15; A 5 €/0,10 € = 50, B 500 €/50 € = 10),
3 Wachstum (KGV ÷ Wachstum, 1 fair, > 2 teuer), 4 Schulden (KGV 5 als Falle). Leitmotiv: Pizza in Stücken + 4er-Prüfliste."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 18)  # Logo nach dem Open Loop (s4)

from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, hand, icon_gross, kasten, kreis, linie, news_kopf,  # noqa: E402
                         stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip  # noqa: E402
from lf_kit import Kit, folg_js, folg_logo  # noqa: E402

K = Kit(HERE, 24, ["frei-euro", "frei-50euro", "frei-frankfurt-nacht", "frei-frankfurt-staedel", "frei-sitzung", "frei-code-monitor"])
cap, st = K.cap, K.st
S = K.szene
BLAU = "#3aa0ff"
NAMEN = ["Börsenwert", "KGV", "Wachstum", "Schulden"]


def pruefliste(id_, aktiv, y=580):
    """Leitmotiv-Leiste: 4 Prüfungen, erledigte grün ✓, aktive orange."""
    k = []
    for i, n in enumerate(NAMEN, 1):
        f = GRUEN if i < aktiv else (OR if i == aktiv else "#ffffff33")
        txt = "#111" if i <= aktiv else "#ffffffaa"
        zeichen = "✓ " if i < aktiv else f"{i} "
        k.append(f'<div style="flex:1;padding:12px 0;border-radius:16px;background:{f if i <= aktiv else "#14181bcc"};border:3px solid {f};color:{txt};'
                 f'font-weight:900;font-size:27px;white-space:nowrap;text-align:center;box-shadow:0 0 {30 if i == aktiv else 0}px {f}">{zeichen}{n}</div>')
    return f'<div id="{id_}" style="position:absolute;left:60px;width:960px;top:{y}px;display:flex;gap:14px;z-index:6">{"".join(k)}</div>'


def pizza(id_, cx, cy, r, stuecke, x_label=""):
    """Pizza als SVG, in `stuecke` Stücke geschnitten."""
    linien = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(2 * math.pi * i / stuecke):.0f}" y2="{cy + r * math.sin(2 * math.pi * i / stuecke):.0f}" '
                     f'stroke="#7a3e12" stroke-width="{max(1.5, 7 - stuecke / 12):.1f}"/>' for i in range(stuecke))
    salami = "".join(f'<circle cx="{cx + r * 0.6 * math.cos(a):.0f}" cy="{cy + r * 0.6 * math.sin(a):.0f}" r="{r * 0.11:.0f}" fill="#c0392b"/>'
                     for a in [0.4, 1.5, 2.6, 3.7, 4.8, 5.8])
    return (f'<svg id="{id_}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:3;filter:drop-shadow(0 0 30px {OR}88)">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e3a447"/><circle cx="{cx}" cy="{cy}" r="{r * 0.88:.0f}" fill="#f6c35b"/>{salami}'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.25:.0f}" fill="#c0392b"/>{linien}</svg>')


def zahl(id_, text, y, farbe, gr=150, x=None, w=1080):
    pos = f"left:{x}px;width:{w}px" if x is not None else "left:0;width:1080px"
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;text-align:center;font-weight:900;font-size:{gr}px;color:{farbe};'
            f'text-shadow:0 0 50px {farbe}aa;z-index:5;white-space:nowrap">{text}</div>')


def preisschild(id_, text, x, y, farbe, dreh=-6, gr=90):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:20px 40px 20px 70px;border-radius:20px 60px 60px 20px;background:{farbe};'
            f'color:#111;font-weight:900;font-size:{gr}px;transform:rotate({dreh}deg);box-shadow:0 0 50px {farbe}88, 0 20px 30px #000;z-index:4">'
            f'<span style="position:absolute;left:22px;top:50%;width:26px;height:26px;margin-top:-13px;border-radius:50%;background:#111"></span>{text}</div>')


def rechnung(id_, zeile, ergebnis, y, farbe):
    return (f'<div id="{id_}" style="position:absolute;left:90px;width:900px;top:{y}px;padding:30px 0;border-radius:30px;background:#14181bee;border:5px solid {farbe};'
            f'box-shadow:0 0 60px {farbe}55;text-align:center;z-index:4"><div class="mono" style="font-size:54px;color:#fff">{zeile}</div>'
            f'<div id="{id_}-e" style="margin-top:14px;font-weight:900;font-size:110px;color:{farbe};text-shadow:0 0 40px {farbe}">{ergebnis}</div></div>')


# ---------- Einstieg ----------
S("s1", "frei-euro", KIT_CSS + titel_zeile("t1", "Welche ist teurer?", farbe=GELB)
  + preisschild("p1a", "Aktie A: 5 €", 90, 650, GRUEN, -6) + preisschild("p1b", "Aktie B: 500 €", 250, 900, ROT, 4)
  + zahl("q1", "?", 1050, GELB, 150),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#p1a", {a}); pop("#p1b", {cap("s1", 2)}); slam("#q1", {cap("s1", 2)} + 0.5);',
  [(0.0, "bass-schlag")])

S("s2", "frei-frankfurt-nacht", titel_zeile("t2", "Der teuerste Fehler", farbe=ROT) + icon_gross("i2", "🤦", 0, 640, 300, ROT, True)
  + stempel("s2x", "NUR AUF DEN PREIS SCHAUEN", 70, 1020, ROT, 52, -5),
  lambda a, d: f'pop("#t2", {a}); pop("#i2", {a} + 0.1); stempeln("#s2x", {cap("s2", 2)});',
  [(cap("s2", 2), "stempel")])

K4 = "".join(kasten(f"k3{i}", ic, 70 + i * 240, 700, 210, 260, OR, 90, n) for i, (ic, n) in enumerate(zip(["🍕", "➗", "📈", "🎒"], NAMEN)))
S("s3", "frei-sitzung", titel_zeile("t3", "4 Prüfungen der Profis") + K4,
  lambda a, d: f'pop("#t3", {a}); ' + " ".join(f'pop("#k3{i}", {cap("s3", 1)} + {i * 0.25});' for i in range(4)))

K4b = "".join(kasten(f"k4{i}", ic, 70 + i * 240, 700, 210, 260, GELB if i == 3 else "#ffffff55", 90, n) for i, (ic, n) in enumerate(zip(["🍕", "➗", "📈", "?"], NAMEN[:3] + ["vergessen alle"])))
S("s4", "frei-sitzung", titel_zeile("t4", "Nr. 4 vergessen fast alle", farbe=GELB, gr=56) + K4b + kreis("kr4", 885, 830, 150, 175, GELB),
  lambda a, d: f'pop("#t4", {a}); ' + " ".join(f'pop("#k4{i}", {a} + {i * 0.1});' for i in range(4)) + f' draw("#kr4-p", {cap("s4", 1)}, 0.6); shake("#k43", {cap("s4", 2)});',
  [(cap("s4", 1), "spannung")])

# ---------- 1 Börsenwert ----------
S("s5", "frei-50euro", titel_zeile("t5", "Nr. 1: Börsenwert", farbe=OR) + pruefliste("pl5", 1) + pizza("pz5", 540, 940, 260, 1),
  lambda a, d: f'pop("#t5", {a}); pop("#pl5", {a}); pop("#pz5", {a} + 0.2);')

S("s6", "frei-50euro", titel_zeile("t6", "Gleiche Pizza") + pruefliste("pl6", 1) + pizza("pz6a", 290, 900, 190, 8) + pizza("pz6b", 790, 900, 190, 64)
  + hand("h6a", "8 Stücke", 290, 1110, 58, "#fff", -3, True) + hand("h6b", "64 Stücke", 790, 1110, 58, "#fff", 3, True),
  lambda a, d: f'pop("#t6", {a}); pop("#pz6a", {cap("s6", 2)}); pop("#h6a", {cap("s6", 2)} + 0.2); pop("#pz6b", {cap("s6", 3)}); pop("#h6b", {cap("s6", 3)} + 0.2);')

S("s7", "frei-frankfurt-staedel", titel_zeile("t7", "Die ganze Firma") + pruefliste("pl7", 1)
  + rechnung("r7", "Kurs × Anzahl Aktien", "= Börsenwert", 720, OR),
  lambda a, d: f'pop("#t7", {a}); pop("#pl7", {a}); pop("#r7", {cap("s7", 2)}); slam("#r7-e", {cap("s7", 3)});')

S("s8", "frei-euro", titel_zeile("t8", "Gleich viel wert") + pruefliste("pl8", 1)
  + vergleich("v8", "1 MIO. × 500 €", "500 Mio. €", "100 MIO. × 5 €", "500 Mio. €", BLAU, BLAU, y=700, h=300)
  + zahl("eq8", "=", 760, GELB, 120),
  lambda a, d: f'pop("#t8", {a}); pop("#v8-l", {cap("s8", 0)}); pop("#v8-r", {cap("s8", 2)}); slam("#eq8", {cap("s8", 3)});')

# ---------- 2 KGV ----------
S("s9", "frei-code-monitor", titel_zeile("t9", "Nr. 2: das KGV", farbe=OR) + pruefliste("pl9", 2)
  + zahl("n9", "KGV", 700, OR, 200) + hand("h9", "Kurs-Gewinn-Verhältnis", 540, 960, 64, "#fff", -3, True),
  lambda a, d: f'pop("#t9", {a}); pop("#pl9", {a}); slam("#n9", {cap("s9", 2)}); pop("#h9", {cap("s9", 1)});')

S("s10", "frei-frankfurt-staedel", titel_zeile("t10", "Deine Pizzeria") + pruefliste("pl10", 2) + icon_gross("i10", "🍕", 90, 690, 260, OR)
  + preisschild("p10", "150.000 €", 430, 700, GELB, -4, 80) + chip("c10", "+10.000 € Gewinn im Jahr", GRUEN, 1000, 56),
  lambda a, d: f'pop("#t10", {a}); pop("#pl10", {a}); pop("#i10", {cap("s10", 1)}); pop("#p10", {cap("s10", 2)}); slam("#c10", {cap("s10", 3)});')

S("s11", "frei-frankfurt-nacht", titel_zeile("t11", "Bis dein Geld zurück ist") + pruefliste("pl11", 2)
  + rechnung("r11", "150.000 € ÷ 10.000 €", "KGV 15", 700, GELB) + zahl("j11", "0 Jahre", 1080, "#fff", 70),
  lambda a, d: (f'pop("#t11", {a}); pop("#pl11", {a}); pop("#r11", {a} + 0.2); zaehl("#j11", 0, 15, {cap("s11", 0)} + 0.3, 1.5, " Jahre");'
                f' slam("#r11-e", {cap("s11", 2)});'),
  [(cap("s11", 0) + 0.3, "zaehler")])

S("s12", "frei-50euro", titel_zeile("t12", "Aktie A", farbe=ROT) + pruefliste("pl12", 2) + preisschild("p12", "5 €", 330, 690, ROT, -5, 80)
  + rechnung("r12", "5 € ÷ 0,10 € Gewinn", "KGV 50", 880, ROT),
  lambda a, d: f'pop("#t12", {a}); pop("#pl12", {a}); pop("#p12", {a} + 0.1); pop("#r12", {cap("s12", 1)}); slam("#r12-e", {cap("s12", 2)});')

S("s13", "frei-euro", titel_zeile("t13", "Aktie B", farbe=GRUEN) + pruefliste("pl13", 2) + preisschild("p13", "500 €", 300, 690, GRUEN, 4, 80)
  + rechnung("r13", "500 € ÷ 50 € Gewinn", "KGV 10", 880, GRUEN) + stempel("s13x", "GÜNSTIGER!", 330, 1150, GRUEN, 64, -6),
  lambda a, d: f'pop("#t13", {a}); pop("#pl13", {a}); pop("#p13", {a} + 0.1); pop("#r13", {cap("s13", 1)}); slam("#r13-e", {cap("s13", 2)}); stempeln("#s13x", {cap("s13", 3)});',
  [(cap("s13", 3), "richtig")])

# ---------- 3 Wachstum ----------
S("s14", "frei-code-monitor", titel_zeile("t14", "Nr. 3: Wachstum", farbe=OR) + pruefliste("pl14", 3) + icon_gross("i14", "📈", 0, 700, 300, GRUEN, True),
  lambda a, d: f'pop("#t14", {a}); pop("#pl14", {a}); pop("#i14", {a} + 0.2);')

S("s15", "frei-frankfurt-staedel", titel_zeile("t15", "Hohes KGV = schlecht?") + pruefliste("pl15", 3)
  + linie("lk15", [0.05, 0.12, 0.22, 0.36, 0.55, 0.78, 0.92], 120, 780, 760, 330, GRUEN, True, [(6, "Gewinn ↑")])
  + hand("h15", "nicht unbedingt!", 300, 1140, 64, GELB, -4),
  lambda a, d: f'pop("#t15", {a}); pop("#pl15", {a}); pop("#h15", {cap("s15", 1)}); draw("#lk15-p", {cap("s15", 2)}, 1.2); pop("#lk15-w0", {cap("s15", 3)});')

S("s16", "frei-sitzung", titel_zeile("t16", "Der Profi-Trick") + pruefliste("pl16", 3) + rechnung("r16", "KGV ÷ Wachstum in %", "= ?", 720, OR),
  lambda a, d: f'pop("#t16", {a}); pop("#pl16", {a}); pop("#r16", {cap("s16", 0)} + 0.3); slam("#r16-e", {cap("s16", 2)});')

SK = ('<div id="sk17" style="position:absolute;left:90px;width:900px;top:960px;height:70px;border-radius:35px;'
      f'background:linear-gradient(90deg,{GRUEN} 0%,{GRUEN} 30%,{GELB} 45%,{GELB} 60%,{ROT} 75%);box-shadow:0 0 40px #0008;z-index:4"></div>'
      + "".join(f'<div class="mono" style="position:absolute;left:{x}px;top:1050px;width:240px;text-align:center;font-size:36px;color:{f};z-index:5">{t}</div>'
                for x, t, f in ((60, "unter 1", GRUEN), (420, "1 = fair", GELB), (780, "über 2", ROT)))
      + f'<div id="nd17" style="position:absolute;left:530px;top:920px;width:20px;height:150px;border-radius:10px;background:#fff;box-shadow:0 0 20px #fff;z-index:6"></div>')
S("s17", "frei-euro", titel_zeile("t17", "KGV 30 ÷ 30 % = 1") + pruefliste("pl17", 3) + zahl("n17", "fair", 700, GELB, 150) + SK,
  lambda a, d: (f'pop("#t17", {a}); pop("#pl17", {a}); pop("#sk17", {a} + 0.2); tl.fromTo("#nd17", {{ x: -420 }}, {{ x: 0, duration: 0.9, ease: "back.out(1.4)" }}, {cap("s17", 1)});'
                f' pop("#n17", {cap("s17", 2)}); tl.to("#nd17", {{ x: 380, duration: 0.7, ease: "power2.inOut" }}, {cap("s17", 3)}); tl.to("#n17", {{ color: "{ROT}", duration: 0.3 }}, {cap("s17", 3)} + 0.4);'))

S("s18", "frei-frankfurt-nacht", titel_zeile("t18", "Deine Meinung") + icon_gross("i18", "💬", 0, 640, 300, OR, True)
  + chip("c18", "Welche Aktie als Nächstes?", OR, 1020, 60),
  lambda a, d: f'pop("#t18", {a}); pop("#i18", {a} + 0.1); slam("#c18", {cap("s18", 1)});')

# ---------- 4 Schulden ----------
S("s19", "frei-code-monitor", titel_zeile("t19", "Nr. 4: Schulden", farbe=ROT) + pruefliste("pl19", 4) + icon_gross("i19", "🎒", 0, 700, 300, ROT, True)
  + hand("h19", "der schwere Rucksack", 540, 1050, 60, "#fff", -3, True),
  lambda a, d: f'pop("#t19", {a}); pop("#pl19", {a}); slam("#i19", {cap("s19", 2)}); pop("#h19", {cap("s19", 2)} + 0.3);')

B20 = (f'<div id="b20g" style="position:absolute;left:200px;top:700px;width:260px;height:420px;border-radius:18px 18px 4px 4px;background:linear-gradient(180deg,{GRUEN},{GRUEN}88);'
       f'box-shadow:0 0 40px {GRUEN}77;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b20z" style="position:absolute;left:200px;top:700px;width:260px;height:300px;border-radius:18px 18px 0 0;background:repeating-linear-gradient(45deg,{ROT} 0 18px,#a82020 18px 36px);'
       f'box-shadow:0 0 40px {ROT}aa;transform-origin:50% 0%;z-index:4"></div>'
       f'<div class="mono" style="position:absolute;left:140px;width:380px;top:1135px;text-align:center;font-size:38px;color:#fff;z-index:5">Gewinn</div>'
       f'<div id="l20" class="mono" style="position:absolute;left:560px;top:760px;font-size:46px;color:{ROT};z-index:5;line-height:1.3">← Zinsen<br/>&nbsp;&nbsp;fressen<br/>&nbsp;&nbsp;den Gewinn</div>')
S("s20", "frei-sitzung", titel_zeile("t20", "Schulden + Zinsen") + pruefliste("pl20", 4) + B20,
  lambda a, d: (f'pop("#t20", {a}); pop("#pl20", {a}); tl.fromTo("#b20g", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6 }}, {cap("s20", 1)});'
                f' tl.fromTo("#b20z", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.8, ease: "power2.in" }}, {cap("s20", 3)}); pop("#l20", {cap("s20", 3)} + 0.4);'))

S("s21", "frei-frankfurt-nacht", titel_zeile("t21", "Billig?", farbe=GELB) + pruefliste("pl21", 4) + zahl("n21", "KGV 5", 720, GRUEN, 200)
  + stempel("s21x", "FALLE!", 330, 980, ROT, 110, -8),
  lambda a, d: f'pop("#t21", {a}); pop("#pl21", {a}); slam("#n21", {cap("s21", 0)}); stempeln("#s21x", {cap("s21", 2)}); tl.to("#n21", {{ color: "{ROT}", duration: 0.3 }}, {cap("s21", 2)});',
  [(cap("s21", 2), "falsch")])

# ---------- Fazit ----------
FZ = "".join(f'<div id="fz{i}" style="position:absolute;left:120px;width:840px;top:{680 + i * 135}px;padding:18px 30px;border-radius:22px;background:#14181bee;border:4px solid {GRUEN};'
             f'font-weight:900;font-size:44px;white-space:nowrap;color:#fff;box-shadow:0 0 40px {GRUEN}44;z-index:4">✓ {t}</div>'
             for i, t in enumerate(["Börsenwert statt Preis", "Was kostet 1 € Gewinn?", "Wächst der Gewinn?", "Wie hoch sind die Schulden?"]))
S("s22", "frei-euro", titel_zeile("t22", "Fazit", farbe=GRUEN) + FZ,
  lambda a, d: f'pop("#t22", {a}); ' + " ".join(f'pop("#fz{i}", {cap("s22", min(i + 1, 4))});' for i in range(4)))

S("s23", "frei-sitzung", titel_zeile("t23", "Kurzer Hinweis") + zettel("z23", "Keine Anlage-<br/>beratung –<br/>nur erklärt", 260, 680, 560, 76, GELB, -3),
  lambda a, d: f'pop("#t23", {a}); pop("#z23", {a} + 0.1);')

S("s24", "frei-frankfurt-staedel", titel_zeile("t24", "Folg uns") + folg_logo("fl24", 600, 360) + chip("c24", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t24", {a}); {folg_js("fl24", a)} slam("#c24", {cap("s24", 0)} + 0.4);')

html, code = ls.szene()
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, news_kopf(""), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
