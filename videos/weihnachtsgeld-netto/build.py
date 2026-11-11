#!/usr/bin/env python3
"""HundeFinanzTv Short (Analyse-Look, ~68 s): Weihnachtsgeld – warum nur gut die Hälfte ankommt."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, donut, hand, kalender, karte, kasten, kit_assets, kreis,  # noqa: E402
                         pfeil, stempel, unterstrich, zettel)
from glow_short import BLASE_SVG, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402

WR = "#e6324b"  # Weihnachtsrot
kit_assets(HERE, [])
cap, st, en, DAUER = zeiten(HERE)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


GESCHENK = (f'<svg id="gk" viewBox="0 0 300 300" style="position:absolute;left:390px;top:420px;width:300px;height:300px;z-index:3;filter:drop-shadow(0 0 30px {WR})">'
            f'<rect x="30" y="110" width="240" height="170" rx="14" fill="{WR}"/><rect x="15" y="80" width="270" height="50" rx="10" fill="#ff5a6e"/>'
            f'<rect x="135" y="80" width="30" height="200" fill="{GELB}"/><path d="M150 80 Q100 20 80 60 Q90 85 150 80 Q210 85 220 60 Q200 20 150 80" fill="{GELB}"/></svg>')

# 1–2 Hook: 3.000 → 1.680
S1 = (KIT_CSS + GESCHENK + tz("h-a", "3.000 €", 760, 150) + pfeil("h-p", 540, 940, 540, 1050, 0.0, ROT, 10) + tz("h-b", "1.680 €", 1040, 150, "glow-r")
      + stempel("h-s", "WO IST DER REST?", 190, 1222, OR, 54, -4))


def j1(a, d):
    return (KIT_JS + f' tl.fromTo("#gk", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }}, {a}); slam("#h-a", {cap("s1", 0)} + 0.3);'
            f' draw("#h-p-p", {cap("s1", 2)}, 0.3); pop("#h-p-k", {cap("s1", 2)} + 0.25); slam("#h-b", {cap("s1", 3)}); stempeln("#h-s", {st("s2")});')


S3 = zettel("hw", "Keine Steuer&shy;beratung –<br/>nur Erklärung", 200, 560, 680, 80, GELB, -3)
J3 = lambda a, d: f'tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});'  # noqa: E731
fr_html, fr_js = cta_szene("fr", BLASE_SVG, "Bekommst du dieses Jahr<br/>Weihnachtsgeld?")
S4 = fr_html + chip("fr-a", "🎁 Ja", GRUEN, 1100, 56, 260) + chip("fr-b", "😕 Nein", ROT, 1100, 56, 600)
J4 = lambda a, d: fr_js(a, d) + f' pop("#fr-a", {cap("s4", 2)}); pop("#fr-b", {cap("s4", 2)} + 0.2);'  # noqa: E731

# 5 kein Gesetz
S5 = (f'<div id="pg" style="position:absolute;left:0;width:1080px;top:440px;text-align:center;font-weight:900;font-size:340px;color:#ffffff22;z-index:2">§</div>'
      + tz("pg-t", "gesetzlicher Anspruch?", 620, 70) + stempel("pg-s", "GIBT ES NICHT", 230, 820, ROT, 76, -6))
J5 = lambda a, d: f'pop("#pg", {a}); pop("#pg-t", {cap("s5", 1)}); stempeln("#pg-s", {cap("s5", 2)});'  # noqa: E731

# 6 drei Dokumente
DOKS = [("Arbeits&shy;vertrag", 70, "s6", 2), ("Tarif&shy;vertrag", 400, "s6", 3), ("Betriebs&shy;verein&shy;barung", 715, "s6", 6)]
DOC = lambda i, txt, x: (f'<div id="dk-{i}" style="position:absolute;left:{x}px;top:560px;width:280px;height:380px;border-radius:18px;background:#f4f1ea;box-shadow:0 30px 50px #000;z-index:3;padding:30px 22px">'  # noqa: E731
                         f'<div style="font-weight:900;font-size:30px;color:#222;line-height:1.1;hyphens:manual">{txt}</div>'
                         + "".join(f'<div style="height:12px;border-radius:6px;background:#ccc;margin-top:{26 if k == 0 else 16}px;width:{90 - k * 12}%"></div>' for k in range(5)) + '</div>')
S6 = "".join(DOC(i, txt, x) for i, (txt, x, *_) in enumerate(DOKS)) + hand("dk-h", "hier steht's drin", 540, 1010, 64, GELB, -3, True)
J6 = lambda a, d: "".join(f' tl.fromTo("#dk-{i}", {{ y: 300, rotation: {(-6, 0, 6)[i]}, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {cap(s, c)});'  # noqa: E731
                              for i, (_, _, s, c) in enumerate(DOKS)) + f' pop("#dk-h", {cap("s6", 6)} + 0.4);'

# 7 dreimal ohne Vorbehalt
S7 = ("".join(kalender(f"jx-{i}", "WEIHN.", str(2023 + i), 90 + i * 320, 520, 260, WR) + tz(f"jx-c{i}", "✓", 800, 120, "glow-g").replace("left: 0", "") .replace('style="z-index:5;top:800px', f'style="z-index:5;left:{90 + i * 320 - 410}px;top:800px') for i in range(3))
      + hand("jx-h", "3× ohne Vorbehalt → oft Anspruch", 540, 1020, 56, GELB, -3, True) + kreis("jx-k", 540, 680, 470, 190, GELB, 6))
J7 = lambda a, d: ("".join(f' pop("#jx-{i}", {cap("s7", 0)} + {0.25 * i}); slam("#jx-c{i}", {cap("s7", 2)} + {0.2 * i});' for i in range(3))  # noqa: E731
                   + f' pop("#jx-h", {cap("s7", 3)}); draw("#jx-k-p", {cap("s7", 4)}, 0.6);')

# 8 Einmalzahlung
S8 = tz("ez-t", "Jetzt zu den Abzügen", 470, 70, "glow-o") + kasten("ez-k", "Weihnachtsgeld<br/>= Einmalzahlung", 140, 620, 800, 300, OR, 70) + unterstrich("ez-u", 240, 960, 600, OR)
J8 = lambda a, d: f'pop("#ez-t", {a}); slam("#ez-k", {cap("s8", 2)}); draw("#ez-u-p", {cap("s8", 2)} + 0.3, 0.4);'  # noqa: E731

# 9–10 Wasserfall: 3.000 − Steuer − Sozialabgaben = 1.680
BASIS, SK = 1200, 0.165  # px pro €
W = [("wf-a", 140, 0, 3000, "#4d8ff0", "3.000 €", "brutto"), ("wf-b", 370, 1680 + 640, 680, ROT, "≈ −680 €", "Steuer"),
     ("wf-c", 600, 1680, 640, OR, "≈ −640 €", "Sozial-<br/>abgaben"), ("wf-d", 830, 0, 1680, GRUEN, "1.680 €", "netto")]
WF = karte("wf-k", 70, 430, 940, 900, "Weihnachtsgeld", "3.000 € · Steuerklasse 1 · ca.-Werte")
for id_, x, unten, hoehe, f, oben, lab in W:
    y = BASIS - (unten + hoehe) * SK
    WF += (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y:.0f}px;width:170px;height:{hoehe * SK:.0f}px;border-radius:12px;background:linear-gradient(180deg,{f},{f}99);'
           f'box-shadow:0 0 30px {f}77;transform-origin:50% 0;z-index:3"></div>'
           f'<div id="{id_}-o" class="mono" style="position:absolute;left:{x - 40}px;width:250px;top:{y - 56:.0f}px;text-align:center;font-size:34px;color:{f};z-index:4">{oben}</div>'
           f'<div class="mono" style="position:absolute;left:{x - 40}px;width:250px;top:{BASIS + 14}px;text-align:center;font-size:28px;color:#ffffffcc;line-height:1.1;z-index:4">{lab}</div>')


def j9(a, d):
    z = [a + 0.2, cap("s9", 0) + 0.4, cap("s9", 1) + 0.2, cap("s10", 2)]
    return (f'pop("#wf-k", {a});' + "".join(f' tl.fromTo("#{w[0]}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {t0}); pop("#{w[0]}-o", {t0} + 0.4);'
                                            for w, t0 in zip(W, z)))


# 11 Donut 55 %
S11 = (donut("do", 540, 820, 250, [(0.56, GRUEN), (0.44, ROT)], 90) + tz("do-z", "≈ 55 %", 760, 100, "glow-g") + tz("do-u", "bleiben", 880, 50)
       + hand("do-h", "fast die Hälfte weg!", 540, 1130, 64, ROT, -3, True))
J11 = lambda a, d: f'draw("#do-0", {a}, 0.7); pop("#do-z", {a} + 0.3); pop("#do-u", {a} + 0.5); draw("#do-1", {cap("s11", 1)}, 0.5); pop("#do-h", {cap("s11", 1)} + 0.3);'  # noqa: E731

# 12 Steuerklasse 5
S12 = (kasten("k1", "Klasse 1", 90, 560, 400, 200, GRUEN, 60, "≈ 55 % netto") + kasten("k5", "Klasse 5", 590, 560, 400, 200, ROT, 60, "noch weniger")
       + stempel("k5-s", "AUTSCH", 560, 820, ROT, 64, 8) + hand("k5-h", "oft Zweitverdiener in der Ehe", 540, 1020, 52, GELB, -3, True))
J12 = lambda a, d: f'pop("#k1", {a}); slam("#k5", {cap("s12", 0)} + 0.4); stempeln("#k5-s", {cap("s12", 1)}); pop("#k5-h", {cap("s12", 1)} + 0.4);'  # noqa: E731

# 13 Steuer fürs ganze Jahr
MON = "".join(f'<div class="mo" style="position:absolute;left:{110 + (i % 6) * 145}px;top:{620 + (i // 6) * 140}px;width:120px;height:110px;border-radius:16px;background:#14181b;'
              f'border:4px solid {OR if i < 11 else WR};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:32px;color:#fff;z-index:3">{m}</div>'
              for i, m in enumerate(["JAN", "FEB", "MÄR", "APR", "MAI", "JUN", "JUL", "AUG", "SEP", "OKT", "NOV", "DEZ"]))
S13 = tz("ja-t", "Geld zurück?", 470, 90, "glow-o") + MON + stempel("ja-s", "MEIST NICHT AUTOMATISCH", 130, 920, ROT, 44, -4) + hand("ja-h", "Steuer = fürs ganze Jahr gerechnet", 540, 1100, 50, GELB, -3, True)
J13 = lambda a, d: (f'pop("#ja-t", {a}); stempeln("#ja-s", {cap("s13", 1)}); tl.fromTo(".mo", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.05 }}, {cap("s13", 2)});'  # noqa: E731
                    f' pop("#ja-h", {cap("s13", 3)});')

# 14 Steuererklärung: Fahrtkosten + Arbeitsmittel
S14 = (kasten("se-k", "🧾 Steuererklärung", 190, 450, 700, 150, GRUEN, 60) + kasten("se-a", "🚗 Fahrtkosten", 70, 760, 440, 170, OR, 50)
       + kasten("se-b", "💻 Arbeitsmittel", 570, 760, 440, 170, OR, 50) + pfeil("se-p1", 290, 750, 450, 620, 0.2, GRUEN, 7) + pfeil("se-p2", 790, 750, 630, 620, -0.2, GRUEN, 7)
       + hand("se-h", "Geld zurück holen", 540, 1010, 64, GELB, -3, True) + partikel("se-x", 540, 520, 24, (GRUEN, GELB, "#fff"), 500))
J14 = lambda a, d: (f'pop("#se-k", {a}); burst("#se-x", {cap("s14", 2)}); pop("#se-a", {cap("s14", 3)}); draw("#se-p1-p", {cap("s14", 3)} + 0.2, 0.4); pop("#se-p1-k", {cap("s14", 3)} + 0.55);'  # noqa: E731
                    f' pop("#se-b", {cap("s14", 4)}); draw("#se-p2-p", {cap("s14", 4)} + 0.2, 0.4); pop("#se-p2-k", {cap("s14", 4)} + 0.55); pop("#se-h", {cap("s14", 4)} + 0.6);')

# 15 Fazit: mit gut der Hälfte planen
BAR = (f'<div id="ha" style="position:absolute;left:140px;top:640px;width:800px;height:120px;border-radius:60px;background:#ffffff14;overflow:hidden;z-index:3">'
       f'<div id="ha-g" style="width:56%;height:100%;background:linear-gradient(90deg,{GRUEN},{GRUEN}bb);box-shadow:0 0 40px {GRUEN};transform-origin:0 50%"></div></div>')
S15 = (tz("fz-t", "Plan mit gut der Hälfte", 470, 76, "glow-g") + BAR + tz("fz-a", "≈ 1.680 € von 3.000 €", 800, 56) + GESCHENK.replace('id="gk"', 'id="gk2"').replace("top:420px", "top:900px").replace("left:390px", "left:420px").replace("width:300px;height:300px", "width:240px;height:240px")
       + stempel("fz-s", "KEINE ÜBERRASCHUNG", 170, 1170, GRUEN, 52, -4))
J15 = lambda a, d: (f'pop("#fz-t", {a}); tl.fromTo("#ha-g", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.out" }}, {cap("s15", 1)}); pop("#fz-a", {cap("s15", 1)} + 0.6);'  # noqa: E731
                    f' tl.fromTo("#gk2", {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, {cap("s15", 2)}); stempeln("#fz-s", {cap("s15", 3)});')

SZENEN = [(0.0, st("s3"), S1, j1), (st("s3"), st("s4"), S3, J3), (st("s4"), st("s5"), S4, J4), (st("s5"), st("s6"), S5, J5), (st("s6"), st("s7"), S6, J6),
          (st("s7"), st("s8"), S7, J7), (st("s8"), st("s9"), S8, J8), (st("s9"), st("s11"), WF, j9), (st("s11"), st("s12"), S11, J11),
          (st("s12"), st("s13"), S12, J12), (st("s13"), st("s14"), S13, J13), (st("s14"), st("s15"), S14, J14), (st("s15"), DAUER, S15, J15)]
SFX = [(0.0, "kasse"), (cap("s1", 0) + 0.3, "bass-schlag"), (cap("s1", 2), "kurve-runter"), (cap("s1", 3), "nv-platte-kratzer"), (st("s2"), "stempel"),
       (st("s3"), "swipe"), (st("s4"), "handy-benachrichtigung"), (cap("s4", 2), "pop"), (st("s5"), "whoosh-weich"), (cap("s5", 2), "stempel"),
       (cap("s6", 2), "papier-reissen"), (cap("s6", 3), "pop"), (cap("s6", 6), "pop"), (st("s7"), "whoosh-weich"), (cap("s7", 2), "richtig"),
       (st("s8"), "whoosh-schnell"), (cap("s8", 2), "bass-schlag"), (st("s9"), "taschenrechner"), (cap("s9", 0) + 0.4, "kurve-runter"), (cap("s9", 1) + 0.2, "kurve-runter"),
       (cap("s10", 2), "kasse"), (st("s11"), "whoosh-weich"), (cap("s11", 1), "nv-falsch-buzzer"), (st("s12"), "swipe"), (cap("s12", 1), "stempel"),
       (st("s13"), "whoosh-weich"), (cap("s13", 1), "stempel"), (cap("s13", 2), "tippen"), (st("s14"), "whoosh-weich"), (cap("s14", 2), "muenzen-glas"),
       (st("s15"), "whoosh-weich"), (cap("s15", 3), "level-up")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
