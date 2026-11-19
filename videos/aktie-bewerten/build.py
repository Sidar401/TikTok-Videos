#!/usr/bin/env python3
"""HundeFinanzTv (~2:00, Stimme Dan) – Wie bewertet man eine Aktie? NEUES FORMAT (heller News-Look, Nutzer 19.11.).
4 Prüfungen: 1 Börsenwert (Preis × Aktien), 2 KGV (Pizzeria 150.000/10.000 = 15; A 5 €/0,10 = 50, B 500 €/50 = 10),
3 Wachstum (KGV ÷ Wachstum, 1 fair, > 2 teuer), 4 Schulden (KGV 5 = Falle). Alte dunkle Version: build-dunkel.py."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 18)  # bereits in voice.wav/timings.json (Merker) → nur Startzeit

import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS, linie  # noqa: E402
from glow_short import build  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
BLAU = "#2f6fd6"
K = Kit(HERE, 24, ["frei-euro", "frei-50euro", "frei-frankfurt-staedel", "frei-code-monitor"])
cap, st = K.cap, K.st
S = K.szene
NAMEN = ["Börsenwert", "KGV", "Wachstum", "Schulden"]


def gross(id_, text, y, farbe=D, gr=110):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.05">{text}</div>'


def titel(id_, text, y=330, farbe=D, gr=72):
    return gross(id_, text, y, farbe, gr)


def pruefliste(id_, aktiv, y=430):
    k = []
    for i, n in enumerate(NAMEN, 1):
        if i < aktiv:
            bg, rand, f, z = G, G, "#fff", "✓ "
        elif i == aktiv:
            bg, rand, f, z = O, O, "#fff", f"{i} "
        else:
            bg, rand, f, z = "#ffffff", "#d9dde3", "#8a909a", f"{i} "
        k.append(f'<div style="flex:1;padding:14px 0;border-radius:12px;background:{bg};border:2px solid {rand};color:{f};font-weight:800;font-size:27px;'
                 f'white-space:nowrap;text-align:center;box-shadow:0 6px 14px #0000001a">{z}{n}</div>')
    return f'<div id="{id_}" style="position:absolute;left:60px;width:960px;top:{y}px;display:flex;gap:14px;z-index:6">{"".join(k)}</div>'


def preisschild(id_, text, x, y, farbe, dreh=-6, gr=90):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:20px 44px 20px 76px;border-radius:18px 60px 60px 18px;background:{farbe};'
            f'color:#fff;font-weight:900;font-size:{gr}px;transform:rotate({dreh}deg);box-shadow:0 16px 30px #0000002e;z-index:4;white-space:nowrap">'
            f'<span style="position:absolute;left:24px;top:50%;width:26px;height:26px;margin-top:-13px;border-radius:50%;background:#fff"></span>{text}</div>')


def rechnung(id_, zeile, ergebnis, y, farbe, titel_=""):
    kt = f'<div class="nk-kt">{titel_}</div>' if titel_ else ""
    return (f'<div id="{id_}" class="nk-karte" style="left:110px;top:{y}px;width:860px;text-align:center">{kt}'
            f'<div style="font-size:52px;color:#3a414c;font-weight:600">{zeile}</div>'
            f'<div id="{id_}-e" style="margin-top:14px;font-weight:900;font-size:120px;color:{farbe}">{ergebnis}</div></div>')


def pizza(id_, cx, cy, r, stuecke):
    linien = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(2 * math.pi * i / stuecke):.0f}" y2="{cy + r * math.sin(2 * math.pi * i / stuecke):.0f}" '
                     f'stroke="#7a3e12" stroke-width="{max(1.5, 7 - stuecke / 12):.1f}"/>' for i in range(stuecke))
    salami = "".join(f'<circle cx="{cx + r * 0.6 * math.cos(a):.0f}" cy="{cy + r * 0.6 * math.sin(a):.0f}" r="{r * 0.11:.0f}" fill="#c0392b"/>'
                     for a in [0.4, 1.5, 2.6, 3.7, 4.8, 5.8])
    return (f'<svg id="{id_}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:3;filter:drop-shadow(0 14px 20px #0003)">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e3a447"/><circle cx="{cx}" cy="{cy}" r="{r * 0.88:.0f}" fill="#f6c35b"/>{salami}'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.25:.0f}" fill="#c0392b"/>{linien}</svg>')


def nummer(id_, n, x, y, farbe, unter):
    return (f'<div id="{id_}" class="nk-karte" style="left:{x}px;top:{y}px;width:210px;padding:26px 0;text-align:center">'
            f'<div style="font-weight:900;font-size:110px;color:{farbe};line-height:1">{n}</div>'
            f'<div style="font-weight:700;font-size:28px;color:#3a414c;margin-top:10px;white-space:nowrap">{unter}</div></div>')


def kreis(id_, cx, cy, rx, ry, farbe):
    return (f'<svg viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:6">'
            f'<ellipse id="{id_}-p" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{farbe}" stroke-width="8"/></svg>')


# ---------- Einstieg ----------
S("s1", None, nl.CSS + nl.foto("f1", "frei-euro") + titel("t1", "Welche ist teurer?", 360)
  + preisschild("p1a", "Aktie A: 5 €", 110, 560, G, -5) + preisschild("p1b", "Aktie B: 500 €", 170, 800, R, 4)
  + gross("q1", "?", 1010, O, 170),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#p1a", {a}); pop("#p1b", {cap("s1", 2)}); pop("#q1", {cap("s1", 2)} + 0.5);',
  [], bis="s2")

S("s2", None, titel("t2", "Der teuerste Fehler", 360, R)
  + nl.karte("k2", "Was Anfänger tun", nl.zeile("r2a", "Auf den Preis schauen", "✗", R) + nl.zeile("r2b", "„5 € = billig“", "✗", R), y=560),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 1)}); pop("#r2a", {cap("s2", 2)}); pop("#r2b", {cap("s2", 3)});')

N4 = "".join(nummer(f"k3{i}", i + 1, 70 + i * 240, 600, O, n) for i, n in enumerate(NAMEN))
S("s3", None, titel("t3", "4 Prüfungen der Profis", 380) + N4,
  lambda a, d: f'pop("#t3", {a}); ' + " ".join(f'pop("#k3{i}", {cap("s3", 1)} + {i * 0.25});' for i in range(4)))

N4b = "".join(nummer(f"k4{i}", "?" if i == 3 else i + 1, 70 + i * 240, 600, R if i == 3 else "#b8bec7", "vergessen alle" if i == 3 else n) for i, n in enumerate(NAMEN))
S("s4", None, titel("t4", "Nr. 4 vergessen fast alle", 380, R, 60) + N4b + kreis("kr4", 885, 735, 150, 175, R),
  lambda a, d: f'pop("#t4", {a}); ' + " ".join(f'pop("#k4{i}", {a} + {i * 0.1});' for i in range(4)) + f' draw("#kr4-p", {cap("s4", 1)}, 0.6); shake("#k43", {cap("s4", 2)});')

# ---------- 1 Börsenwert ----------
S("s5", None, nl.foto("f5", "frei-50euro") + titel("t5", "Nr. 1: Börsenwert", 330, O) + pruefliste("pl5", 1) + pizza("pz5", 540, 900, 280, 1),
  lambda a, d: f'pop("#t5", {a}); pop("#pl5", {a}); pop("#pz5", {a} + 0.2);', [], bis="s6")

S("s6", None, titel("t6", "Gleiche Pizza", 330) + pruefliste("pl6", 1) + pizza("pz6a", 290, 820, 200, 8) + pizza("pz6b", 790, 820, 200, 64)
  + f'<div id="h6a" style="position:absolute;left:90px;width:400px;top:1050px;text-align:center;font-weight:800;font-size:50px;color:{D};z-index:4">8 Stücke</div>'
  + f'<div id="h6b" style="position:absolute;left:590px;width:400px;top:1050px;text-align:center;font-weight:800;font-size:50px;color:{D};z-index:4">64 Stücke</div>',
  lambda a, d: f'pop("#t6", {a}); pop("#pz6a", {cap("s6", 2)}); pop("#h6a", {cap("s6", 2)} + 0.2); pop("#pz6b", {cap("s6", 3)}); pop("#h6b", {cap("s6", 3)} + 0.2);')

S("s7", None, titel("t7", "Die ganze Firma", 330) + pruefliste("pl7", 1) + rechnung("r7", "Kurs × Anzahl Aktien", "= Börsenwert", 620, O),
  lambda a, d: f'pop("#t7", {a}); pop("#pl7", {a}); pop("#r7", {cap("s7", 2)}); pop("#r7-e", {cap("s7", 3)});')

V8 = (nl.karte("v8a", "1 Mio. × 500 €", f'<div style="font-weight:900;font-size:56px;white-space:nowrap;color:{BLAU};text-align:center">500 Mio. €</div>', x=70, y=640, w=430)
      + nl.karte("v8b", "100 Mio. × 5 €", f'<div style="font-weight:900;font-size:56px;white-space:nowrap;color:{BLAU};text-align:center">500 Mio. €</div>', x=580, y=640, w=430)
      + gross("eq8", "=", 700, O, 120))
S("s8", None, titel("t8", "Gleich viel wert", 330) + pruefliste("pl8", 1) + V8,
  lambda a, d: f'pop("#t8", {a}); pop("#v8a", {cap("s8", 0)}); pop("#v8b", {cap("s8", 2)}); pop("#eq8", {cap("s8", 3)});')

# ---------- 2 KGV ----------
S("s9", None, nl.foto("f9", "frei-code-monitor") + titel("t9", "Nr. 2: das KGV", 330, O) + pruefliste("pl9", 2)
  + gross("n9", "KGV", 650, O, 220) + gross("h9", "Kurs-Gewinn-Verhältnis", 900, D, 58),
  lambda a, d: f'pop("#t9", {a}); pop("#pl9", {a}); pop("#n9", {cap("s9", 2)}); pop("#h9", {cap("s9", 1)});')

S("s10", None, nl.foto("f10", "frei-frankfurt-staedel") + titel("t10", "Deine Pizzeria", 330) + pruefliste("pl10", 2)
  + pizza("pz10", 260, 800, 170, 8) + preisschild("p10", "150.000 €", 470, 700, O, -4, 76)
  + nl.karte("k10", "Gewinn im Jahr", f'<div style="font-weight:900;font-size:80px;color:{G};text-align:center">+10.000 €</div>', y=1010, x=240, w=600),
  lambda a, d: f'pop("#t10", {a}); pop("#pl10", {a}); pop("#pz10", {cap("s10", 1)}); pop("#p10", {cap("s10", 2)}); pop("#k10", {cap("s10", 3)});')

S("s11", None, titel("t11", "Bis dein Geld zurück ist", 330, D, 64) + pruefliste("pl11", 2)
  + rechnung("r11", "150.000 € ÷ 10.000 €", "KGV 15", 600, O) + gross("j11", "0 Jahre", 1030, D, 76),
  lambda a, d: (f'pop("#t11", {a}); pop("#pl11", {a}); pop("#r11", {a} + 0.2); zaehl("#j11", 0, 15, {cap("s11", 0)} + 0.3, 1.5, " Jahre");'
                f' pop("#r11-e", {cap("s11", 2)});'))

S("s12", None, titel("t12", "Aktie A", 330, R) + pruefliste("pl12", 2) + preisschild("p12", "5 €", 400, 560, R, -5, 80)
  + rechnung("r12", "5 € ÷ 0,10 € Gewinn", "KGV 50", 780, R),
  lambda a, d: f'pop("#t12", {a}); pop("#pl12", {a}); pop("#p12", {a} + 0.1); pop("#r12", {cap("s12", 1)}); pop("#r12-e", {cap("s12", 2)});')

S("s13", None, titel("t13", "Aktie B", 330, G) + pruefliste("pl13", 2) + preisschild("p13", "500 €", 360, 560, G, 4, 80)
  + rechnung("r13", "500 € ÷ 50 € Gewinn", "KGV 10", 780, G)
  + f'<div id="s13x" style="position:absolute;left:0;width:1080px;top:1140px;display:flex;justify-content:center;z-index:5"><span style="padding:12px 40px;border-radius:50px;background:{G};color:#fff;font-weight:900;font-size:54px">✓ günstiger!</span></div>',
  lambda a, d: f'pop("#t13", {a}); pop("#pl13", {a}); pop("#p13", {a} + 0.1); pop("#r13", {cap("s13", 1)}); pop("#r13-e", {cap("s13", 2)}); pop("#s13x", {cap("s13", 3)});')

# ---------- 3 Wachstum ----------
S("s14", None, nl.foto("f14", "frei-code-monitor") + titel("t14", "Nr. 3: Wachstum", 330, O) + pruefliste("pl14", 3)
  + linie("lk14", [0.05, 0.12, 0.22, 0.36, 0.55, 0.78, 0.92], 140, 640, 800, 420, G, True, []),
  lambda a, d: f'pop("#t14", {a}); pop("#pl14", {a}); draw("#lk14-p", {a} + 0.2, 1.0);', [], bis="s15")

S("s15", None, titel("t15", "Hohes KGV = schlecht?", 330, D, 64) + pruefliste("pl15", 3)
  + linie("lk15", [0.05, 0.12, 0.22, 0.36, 0.55, 0.78, 0.92], 140, 620, 800, 360, G, True, [(6, "Gewinn ↑")])
  + gross("h15", "nicht unbedingt!", 1030, O, 64),
  lambda a, d: f'pop("#t15", {a}); pop("#pl15", {a}); pop("#h15", {cap("s15", 1)}); draw("#lk15-p", {cap("s15", 2)}, 1.2); pop("#lk15-w0", {cap("s15", 3)});')

S("s16", None, titel("t16", "Der Profi-Trick", 330) + pruefliste("pl16", 3) + rechnung("r16", "KGV ÷ Wachstum in %", "= ?", 620, O),
  lambda a, d: f'pop("#t16", {a}); pop("#pl16", {a}); pop("#r16", {cap("s16", 0)} + 0.3); pop("#r16-e", {cap("s16", 2)});')

SK = (f'<div id="sk17" style="position:absolute;left:90px;width:900px;top:900px;height:70px;border-radius:35px;'
      f'background:linear-gradient(90deg,{G} 0%,{G} 30%,#f3c33b 45%,#f3c33b 60%,{R} 75%);box-shadow:0 10px 24px #0002;z-index:4"></div>'
      + "".join(f'<div style="position:absolute;left:{x}px;top:990px;width:240px;text-align:center;font-weight:800;font-size:38px;color:{f};z-index:5">{t}</div>'
                for x, t, f in ((60, "unter 1", G), (420, "1 = fair", "#c79a12"), (780, "über 2", R)))
      + f'<div id="nd17" style="position:absolute;left:530px;top:860px;width:20px;height:150px;border-radius:10px;background:{D};box-shadow:0 6px 14px #0004;z-index:6"></div>')
S("s17", None, titel("t17", "KGV 30 ÷ 30 % = 1", 330) + pruefliste("pl17", 3) + gross("n17", "fair", 620, "#c79a12", 150) + SK,
  lambda a, d: (f'pop("#t17", {a}); pop("#pl17", {a}); pop("#sk17", {a} + 0.2); tl.fromTo("#nd17", {{ x: -420 }}, {{ x: 0, duration: 0.9, ease: "back.out(1.4)" }}, {cap("s17", 1)});'
                f' pop("#n17", {cap("s17", 2)}); tl.to("#nd17", {{ x: 380, duration: 0.7, ease: "power2.inOut" }}, {cap("s17", 3)});'
                f' tl.to("#n17", {{ color: "{R}", duration: 0.3 }}, {cap("s17", 3)} + 0.4);'))

S("s18", None, titel("t18", "Deine Meinung", 360)
  + nl.karte("k18", "Schreib’s in die Kommentare", f'<div style="font-weight:900;font-size:62px;color:{O};text-align:center;padding:20px 0">Welche Aktie<br/>als Nächstes?</div>', y=580),
  lambda a, d: f'pop("#t18", {a}); pop("#k18", {cap("s18", 1)});')

# ---------- 4 Schulden ----------
S("s19", None, nl.foto("f19", "frei-50euro") + titel("t19", "Nr. 4: Schulden", 330, R) + pruefliste("pl19", 4)
  + gross("n19", "Schulden", 680, R, 150) + gross("h19", "die Zahl, die alle vergessen", 900, D, 54),
  lambda a, d: f'pop("#t19", {a}); pop("#pl19", {a}); pop("#n19", {cap("s19", 2)}); pop("#h19", {cap("s19", 2)} + 0.3);')

B20 = (f'<div id="b20g" style="position:absolute;left:200px;top:620px;width:260px;height:420px;border-radius:14px 14px 4px 4px;background:{G};'
       f'box-shadow:0 10px 24px #0002;transform-origin:50% 100%;z-index:3"></div>'
       f'<div id="b20z" style="position:absolute;left:200px;top:620px;width:260px;height:300px;border-radius:14px 14px 0 0;background:repeating-linear-gradient(45deg,{R} 0 18px,#b02a2a 18px 36px);'
       f'transform-origin:50% 0%;z-index:4"></div>'
       f'<div style="position:absolute;left:140px;width:380px;top:1055px;text-align:center;font-weight:800;font-size:40px;color:{D};z-index:5">Gewinn</div>'
       f'<div id="l20" style="position:absolute;left:540px;top:680px;font-weight:800;font-size:50px;color:{R};z-index:5;line-height:1.3">← Zinsen<br/>&nbsp;&nbsp;fressen<br/>&nbsp;&nbsp;den Gewinn</div>')
S("s20", None, titel("t20", "Schulden + Zinsen", 330) + pruefliste("pl20", 4) + B20,
  lambda a, d: (f'pop("#t20", {a}); pop("#pl20", {a}); tl.fromTo("#b20g", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6 }}, {cap("s20", 1)});'
                f' tl.fromTo("#b20z", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.8, ease: "power2.in" }}, {cap("s20", 3)}); pop("#l20", {cap("s20", 3)} + 0.4);'))

S("s21", None, titel("t21", "Billig?", 330, O) + pruefliste("pl21", 4) + gross("n21", "KGV 5", 640, G, 210)
  + f'<div id="s21x" style="position:absolute;left:0;width:1080px;top:930px;display:flex;justify-content:center;z-index:5"><span style="padding:14px 50px;border-radius:50px;background:{R};color:#fff;font-weight:900;font-size:70px">⚠ Falle!</span></div>',
  lambda a, d: f'pop("#t21", {a}); pop("#pl21", {a}); pop("#n21", {cap("s21", 0)}); pop("#s21x", {cap("s21", 2)}); tl.to("#n21", {{ color: "{R}", duration: 0.3 }}, {cap("s21", 2)});')

# ---------- Fazit ----------
FZ = "".join(nl.zeile(f"fz{i}", t, "✓", G) for i, t in enumerate(["Börsenwert statt Preis", "Was kostet 1 € Gewinn?", "Wächst der Gewinn?", "Wie hoch sind die Schulden?"]))
S("s22", None, nl.foto("f22", "frei-euro") + titel("t22", "Fazit", 330, G) + nl.karte("k22", "Die 4 Profi-Prüfungen", FZ, y=480),
  lambda a, d: f'pop("#t22", {a}); pop("#k22", {a} + 0.1); ' + " ".join(f'pop("#fz{i}", {cap("s22", min(i + 1, 4))});' for i in range(4)), [], bis="s23")

S("s23", None, nl.karte("k23", "Kurzer Hinweis", f'<div style="font-size:52px;font-weight:800;color:{D};text-align:center;padding:30px 0">Keine Anlageberatung –<br/>nur erklärt.</div>', y=620),
  lambda a, d: f'pop("#k23", {a});')

S("s24", None, f'<div id="fl24" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n24" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + f'<div id="c24" style="position:absolute;left:350px;top:1040px;width:380px;padding:18px 0;border-radius:50px;background:{O};color:#fff;'
    f'font-weight:900;font-size:58px;text-align:center;box-shadow:0 12px 30px #f28a1e66;z-index:4">+ Folgen</div>',
  lambda a, d: (f'pop("#fl24", {a}); pop("#n24", {a} + 0.2); pop("#c24", {cap("s24", 0)} + 0.4);'
                f' tl.fromTo("#c24", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {cap("s24", 0)} + 0.8);'))

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("AKTIEN-WISSEN", ""), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
