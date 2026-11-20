#!/usr/bin/env python3
"""HundeFinanzTv Börsentag 20.11.2026 (~75 s, NEUES FORMAT). DAX −2,60 % auf 24.802,78 (6. Minustag, unter 25.000, unter 200-Tage-Linie),
MDAX −2,59 %, Infineon −7,9 %, Siemens Energy −6,6 %, Nasdaq im Handel ≈ −3 % (AMD, Micron), Zinssorgen + starker Dollar,
DAX-Woche > −7 % (Rekord ≈ 27.002 vor gut einer Woche). Quellen: dpa-AFX/finanzen.net, Motley Fool, Benzinga."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 13)  # Logo nach dem Open Loop (s3)

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 15, ["frei-frankfurt-nacht", "nyse"],
        logos=["infineon.svg", "siemens-energy.svg", "nasdaq.svg", "amd.svg", "micron.svg", "flagge-deutschland.svg", "flagge-usa.svg"])
cap, st = K.cap, K.st
S = K.szene


def titel(id_, text, y=340, farbe=D, gr=70):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=54):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def logo_kachel(id_, datei, wert, x, y, w=400, farbe=R):
    return (f'<div id="{id_}" class="nk-karte" style="left:{x}px;top:{y}px;width:{w}px;text-align:center;padding:30px">'
            f'<img src="assets/logos/{datei}" style="max-width:300px;max-height:90px"/>'
            f'<div style="font-weight:900;font-size:72px;color:{farbe};margin-top:14px">{wert}</div></div>')


# s1 Einstieg (Vorlage: Kurve, Logo, Name, Satz, 3 Tages-Kacheln)
S("s1", None, nl.CSS + nl.kurve_hinten("kv1")
  + f'<div id="lg1" style="position:absolute;left:340px;top:520px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
    f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n1" class="nk-gross" style="top:935px;font-size:56px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + f'<div id="t1" class="nk-gross" style="top:1030px;font-size:62px;line-height:1.15">Alles, was heute<br/>an der Börse passiert ist</div>'
  + f'<div id="b1" style="position:absolute;left:0;width:1080px;top:1215px;display:flex;justify-content:center;z-index:4"><span style="padding:14px 40px;border-radius:50px;background:{O};color:#fff;font-weight:800;font-size:46px">in 60 Sekunden</span></div>'
  + nl.mini_kachel("m1a", 60, 1370, "DAX", "−2,6 %", R, -3) + nl.mini_kachel("m1b", 400, 1395, "infineon.svg", "−7,9 %", R, 2)
  + nl.mini_kachel("m1c", 740, 1370, "nasdaq.svg", "▼ −3 %", R, -2),
  lambda a, d: (KIT_JS + f' draw("#kv1-p", {a}, 1.2); tl.fromTo("#kv1-f", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8 }}, {a} + 0.4);'
                f' tl.fromTo("#lg1", {{ scale: 0.85 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)" }}, {a}); pop("#n1", {a} + 0.2); pop("#t1", {a} + 0.35);'
                f' pop("#b1", {cap("s1", 2)}); pop("#m1a", {cap("s1", 2)} + 0.25); pop("#m1b", {cap("s1", 2)} + 0.45); pop("#m1c", {cap("s1", 2)} + 0.65);'))

# s2 Heute 👇
S("s2", None, titel("t2", "Heute 👇", 340, D, 84)
  + nl.karte("k2", "DAX", f'<div style="font-weight:900;font-size:110px;color:{R};text-align:center;line-height:1.1">unter<br/>25.000</div>', y=500)
  + pille("p2", "6. Minus-Tag in Folge", 1060, R, "#fff", 52),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 1)}); pop("#p2", {cap("s2", 2)});')

# s3 Open Loop
S("s3", None, titel("t3", "Die Zahl der Woche", 360, O)
  + nl.karte("k3", "Wichtig für dein Depot", f'<div style="font-weight:900;font-size:180px;color:{O};text-align:center;line-height:1.1">?</div>', y=560),
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {cap("s3", 1)});')

# s4–s5 DAX + MDAX
S("s4", None, nl.foto("f4", "frei-frankfurt-nacht")
  + f'<img id="l4" src="assets/logos/flagge-deutschland.svg" style="position:absolute;left:470px;top:350px;width:140px;border-radius:6px;box-shadow:0 6px 14px #0002;z-index:4"/>'
  + nl.karte("k4", "Deutschland heute", nl.zeile("r4a", "DAX", "24.803", D) + nl.zeile("r4b", "Veränderung", "−2,6 % ▼", R)
             + nl.zeile("r5", "MDAX", "−2,6 % ▼", R), y=500),
  lambda a, d: f'pop("#l4", {a}); pop("#k4", {a} + 0.1); pop("#r4a", {cap("s4", 1)}); pop("#r4b", {cap("s4", 2)}); pop("#r5", {cap("s5", 1)});',
  [], bis="s6")

# s6 Infineon + Siemens Energy
S("s6", None, titel("t6", "Tech-Werte unter Druck", 340, R, 64)
  + logo_kachel("c6a", "infineon.svg", "−7,9 %", 90, 520) + logo_kachel("c6b", "siemens-energy.svg", "−6,6 %", 590, 520),
  lambda a, d: f'pop("#t6", {a}); pop("#c6a", {cap("s6", 2)}); pop("#c6b", {cap("s6", 3)});')

# s7–s8 New York
S("s7", None, nl.foto("f7", "nyse") + nl.logo_frei("l7", "nasdaq.svg", 340, 360, 400)
  + nl.karte("k7", "New York (im Handel)", nl.zeile("r7", "Nasdaq", "≈ −3 % ▼", R), y=560)
  + logo_kachel("c8a", "amd.svg", "verkauft", 90, 850, 400) + logo_kachel("c8b", "micron.svg", "verkauft", 590, 850, 400),
  lambda a, d: (f'pop("#l7", {a}); pop("#k7", {cap("s7", 1)}); pop("#r7", {cap("s7", 3)}); pop("#c8a", {cap("s8", 0)} + 0.4); pop("#c8b", {cap("s8", 1)});'),
  [], bis="s9")

# s9 Gründe
S("s9", None, titel("t9", "Die Gründe", 340) + nl.karte("k9", "Warum es fällt",
  nl.zeile("r9a", "Angst vor höheren Zinsen", "▲", R) + nl.zeile("r9b", "Starker US-Dollar", "▲", R), y=520),
  lambda a, d: f'pop("#t9", {a}); pop("#k9", {a} + 0.1); pop("#r9a", {cap("s9", 1)}); pop("#r9b", {cap("s9", 2)});')

# s10–s11 Zahl der Woche (Kurve Rekord → heute)
P = [(0, 0.92), (1, 0.97), (2, 0.8), (3, 0.62), (4, 0.5), (5, 0.38), (6, 0.22), (7, 0.08)]
PFAD = "M" + " L".join(f"{60 + i * 100} {40 + 300 * (1 - v)}" for i, v in P)
KURVE = (f'<svg viewBox="0 0 800 380" style="width:780px;height:370px"><path d="{PFAD} L760 380 L60 380 Z" fill="{R}22"/>'
         f'<path id="dx-p" d="{PFAD}" fill="none" stroke="{R}" stroke-width="7"/><circle cx="760" cy="316" r="12" fill="{R}"/>'
         f'<text x="600" y="296" font-size="40" font-weight="700" fill="{R}" style="font-family:Montserrat">24.803</text>'
         f'<text x="120" y="30" font-size="30" fill="#555" style="font-family:Montserrat">Rekord ≈ 27.000</text></svg>')
S("s10", None, titel("t10", "Die Zahl der Woche", 330, O) + nl.karte("k10", "DAX", KURVE, y=450)
  + f'<div id="n10" class="nk-gross" style="top:1010px;font-size:150px;color:{R}">−7 %</div>',
  lambda a, d: f'pop("#t10", {a}); pop("#k10", {a} + 0.1); draw("#dx-p", {cap("s10", 0)}, 1.4); pop("#n10", {cap("s10", 2)});', [], bis="s12")

# s12–s13 Was heißt das für dich
S("s12", None, titel("t12", "Heißt für dich", 340, G) + nl.karte("k12", "Ruhig bleiben",
  nl.zeile("r12", "ETF-Depot im Minus", "normal", D) + nl.zeile("r13", "Sparplan kauft", "günstiger", G, "✓"), y=520),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12", {cap("s12", 1)}); pop("#r13", {cap("s13", 1)});', [], bis="s14")

# s14 Hinweis
S("s14", None, nl.karte("k14", "Kurzer Hinweis", f'<div style="font-size:52px;font-weight:800;color:{D};text-align:center;padding:30px 0">Keine Anlageberatung –<br/>nur erklärt.</div>', y=620),
  lambda a, d: f'pop("#k14", {a});')

# s15 Folgen
S("s15", None, f'<div id="fl15" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n15" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c15", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl15", {a}); pop("#n15", {a} + 0.2); pop("#c15", {cap("s15", 0)} + 0.4);')

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("BÖRSENNEWS", "20.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
    nl.ohne_untertitel(HERE, st("s2") - 0.05)
