#!/usr/bin/env python3
"""HundeFinanzTv Short (Analyse-Look, ~63 s): Schufa-Score gratis abfragen in 1 Minute."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, hand, kalender, karte, kasten, kit_assets, kreis,  # noqa: E402
                         logo_karte, pfeil, stempel, unterstrich, zettel)
from glow_short import TEILEN_SVG, build, chip, cta_szene, handy, partikel, t, zeiten  # noqa: E402

SB = "#00a0e3"
kit_assets(HERE, ["schufa"])
cap, st, en, DAUER = zeiten(HERE)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def schufa(id_, x, y, w=420, h=130):
    return logo_karte(id_, "schufa", x, y, w, h, glow=SB, pad=0.2)


def tacho(id_, cx, cy, r, wert=None):
    """Halbkreis-Tacho 100–999 (rot→gelb→grün). Nadel id-n; JS: nadel("#id", t, wert)."""
    zonen = [(100, 500, ROT), (500, 776, GELB), (776, 999, GRUEN)]
    s = []
    for a, b, f in zonen:
        w0 = math.pi * (1 - (a - 100) / 899)
        w1 = math.pi * (1 - (b - 100) / 899)
        p0 = (cx + r * math.cos(w0), cy - r * math.sin(w0))
        p1 = (cx + r * math.cos(w1), cy - r * math.sin(w1))
        s.append(f'<path id="{id_}-z{f[1:]}" d="M{p0[0]:.0f} {p0[1]:.0f} A{r} {r} 0 0 1 {p1[0]:.0f} {p1[1]:.0f}" fill="none" stroke="{f}" stroke-width="56" style="filter:drop-shadow(0 0 14px {f}88)"/>')
    s.append(f'<g id="{id_}-n"><path d="M{cx - 14} {cy} L{cx} {cy - r + 40} L{cx + 14} {cy} Z" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="26" fill="#fff"/></g>')
    lab = "".join(f'<text x="{cx + (r + 70) * math.cos(math.pi * (1 - (v - 100) / 899)):.0f}" y="{cy - (r + 70) * math.sin(math.pi * (1 - (v - 100) / 899)) + 14:.0f}" '
                  f'fill="#fff" font-family="JetBrains Mono" font-weight="800" font-size="38" text-anchor="middle">{v}</text>' for v in (100, 500, 776, 999))
    return f'<svg id="{id_}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;z-index:3">{"".join(s)}{lab}</svg>'


def nadel(sel, at, wert, dur=0.9):
    return f'tl.fromTo("{sel}-n", {{ rotation: -90, svgOrigin: "540 1050" }}, {{ rotation: {-90 + 180 * (wert - 100) / 899:.1f}, svgOrigin: "540 1050", duration: {dur}, ease: "back.out(1.4)" }}, {at});'


ICON = lambda id_, sym, txt, x: (f'<div id="{id_}" style="position:absolute;left:{x}px;top:780px;width:280px;height:280px;border-radius:30px;background:#14181b;border:5px solid {SB};'  # noqa: E731
                                 f'box-shadow:0 0 40px {SB}55;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;z-index:3">'
                                 f'<div style="font-size:120px">{sym}</div><div style="font-weight:900;font-size:34px;color:#fff">{txt}</div></div>')

S1 = KIT_CSS + schufa("a-s", 330, 450, 420, 130) + hand("a-h", "entscheidet mit …", 540, 620, 60, GELB, -3, True) + ICON("a-1", "💳", "Kredit", 70) + ICON("a-2", "📱", "Handyvertrag", 400) + ICON("a-3", "🏠", "Wohnung", 730)
J1 = lambda a, d: KIT_JS + f' pop("#a-s", {a}); pop("#a-h", {a} + 0.3); pop("#a-1", {cap("s1", 1)}); pop("#a-2", {cap("s1", 2)}); pop("#a-3", {cap("s1", 3)});'  # noqa: E731

PH = handy("b-h", 330, 440, 420, '<div style="font-weight:900;font-size:40px;color:#fff">Dein Score</div>'
           f'<div class="mono" style="font-size:110px;color:{GRUEN};text-shadow:0 0 30px {GRUEN}">???</div>', SB)
S2 = PH + chip("b-c", "⏱ 1 Minute", SB, 1250 - 40, 56) + stempel("b-s", "KOSTENLOS", 470, 560, GRUEN, 64, 10)
J2 = lambda a, d: f'pop("#b-h", {a}); stempeln("#b-s", {cap("s2", 1)}); slam("#b-c", {cap("s2", 2)});'  # noqa: E731

cta_html, cta_js = cta_szene("te", TEILEN_SVG, "Schick das jemandem,<br/>der eine Wohnung sucht!")
S4 = zettel("hw", "Keine Finanz&shy;beratung –<br/>nur Erklärung", 200, 560, 680, 80, GELB, -3)
J4 = lambda a, d: f'tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});'  # noqa: E731

KZ = ('<svg id="be-x" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:5">'
      f'<path id="be-x1" d="M110 520 L490 760" stroke="{ROT}" stroke-width="14" stroke-linecap="round"/><path id="be-x2" d="M490 520 L110 760" stroke="{ROT}" stroke-width="14" stroke-linecap="round"/></svg>')
S5 = (kasten("be-a", "🏛 Behörde", 80, 520, 420, 240, GRAU, 60) + KZ + kasten("be-b", "🏢 private Firma", 580, 520, 420, 240, SB, 54)
      + schufa("be-s", 380, 860, 320, 100) + hand("be-h", "ein Unternehmen, kein Amt", 540, 1010, 56, GELB, -3, True))
J5 = lambda a, d: (f'pop("#be-a", {a}); draw("#be-x1", {cap("s5", 1)}, 0.2); draw("#be-x2", {cap("s5", 1)} + 0.2, 0.2); pop("#be-b", {cap("s5", 2)});'  # noqa: E731
                   f' pop("#be-s", {cap("s5", 2)} + 0.3); pop("#be-h", {cap("s5", 2)} + 0.5);')

S6 = kalender("ne-k", "MÄRZ", "2026", 120, 500, 340, SB) + schufa("ne-s", 520, 560, 440, 140) + stempel("ne-st", "NEUER SCORE", 300, 930, OR, 76, -6)
J6 = lambda a, d: f'pop("#ne-k", {a}); pop("#ne-s", {cap("s6", 1)}); stempeln("#ne-st", {cap("s6", 1)} + 0.3);'  # noqa: E731

S7 = (karte("ta-k", 70, 440, 940, 860, "Schufa-Score", "Skala 100 – 999") + tacho("ta", 540, 1050, 320)
      + tz("ta-z", "", 1080, 10) + hand("ta-h", "je höher, desto besser", 540, 1150, 56, GELB, -2, True)
      + kreis("ta-kr", 870, 860, 130, 110, GRUEN, 7) + chip("ta-c", "776+ = hervorragend", GRUEN, 560, 52))


def j7(a, d):
    return (f'pop("#ta-k", {a}); tl.fromTo("#ta", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, transformOrigin: "540px 1050px" }}, {cap("s7", 0)});'
            + nadel("#ta", cap("s7", 1), 999, 1.0) + f' pop("#ta-h", {cap("s7", 2)});'
            + nadel("#ta", st("s8"), 776, 0.6).replace("rotation: -90,", "rotation: 90,") + f' slam("#ta-c", {cap("s8", 1)}); draw("#ta-kr-p", {cap("s8", 1)} + 0.3, 0.5);')


KR = "".join(f'<div class="kr" style="position:absolute;left:{130 + (i % 4) * 210}px;top:{600 + (i // 4) * 170}px;width:180px;height:140px;border-radius:22px;background:#14181b;'
             f'border:4px solid {SB};box-shadow:0 0 24px {SB}55;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:64px;color:#fff;z-index:3">{i + 1}</div>' for i in range(12))
S9 = schufa("kr-s", 360, 440, 360, 110) + KR + stempel("kr-st", "OFFENGELEGT", 290, 1110, GRUEN, 70, -5)
J9 = lambda a, d: (f'pop("#kr-s", {a}); tl.fromTo(".kr", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.25, stagger: 0.07, ease: "back.out(2)" }}, {cap("s9", 2)});'  # noqa: E731
                   f' stempeln("#kr-st", {cap("s9", 3)} + 0.5);')

STEP = lambda i, sym, txt, sub, y, f: (f'<div id="sp-{i}" style="position:absolute;left:90px;top:{y}px;width:900px;height:200px;border-radius:30px;background:#14181b;border:5px solid {f};'  # noqa: E731
                                      f'box-shadow:0 0 40px {f}55;display:flex;align-items:center;gap:30px;padding:0 40px;z-index:3">'
                                      f'<div style="width:120px;height:120px;border-radius:50%;background:{f};color:#111;font-weight:900;font-size:70px;display:flex;align-items:center;justify-content:center">{i}</div>'
                                      f'<div><div style="font-weight:900;font-size:54px;color:#fff">{sym} {txt}</div><div class="mono" style="font-size:30px;color:{GRAU};margin-top:6px">{sub}</div></div></div>')
S10 = (tz("sp-t", "So geht's:", 440, 70, "glow-o") + STEP(1, "📲", "App oder Webseite", "offizielle Schufa", 560, SB) + STEP(2, "✉️", "Konto anlegen", "E-Mail + Passwort", 800, OR)
       + STEP(3, "🪪", "Wer bist du?", "z. B. Online-Ausweis", 1040, GRUEN))
J10 = lambda a, d: (f'pop("#sp-t", {a}); slam("#sp-1", {cap("s10", 1)}); slam("#sp-2", {st("s11")}); slam("#sp-3", {cap("s12", 2)});')  # noqa: E731

PH2 = handy("fi-h", 330, 440, 420, '<div style="font-weight:900;font-size:40px;color:#fff">Dein Score</div>'
            f'<div id="fi-z" class="mono" style="font-size:120px;color:{GRUEN};text-shadow:0 0 30px {GRUEN}">0</div>'
            f'<div class="mono" style="font-size:30px;color:{GRAU}">von 999</div>', SB)
S13 = PH2 + stempel("fi-s", "DAUERHAFT GRATIS", 230, 1180, GRUEN, 58, -5) + partikel("fi-p", 540, 800, 26, (GRUEN, SB, "#fff"), 520)
J13 = lambda a, d: f'pop("#fi-h", {a}); zaehl("#fi-z", 0, 812, {a} + 0.3, 1.4); burst("#fi-p", {a} + 1.6); stempeln("#fi-s", {cap("s13", 2)});'  # noqa: E731

S14 = (zettel("my-z", "„Abfragen macht den Score schlechter?“", 170, 480, 740, 62, GELB, -3) + stempel("my-s", "FALSCH", 330, 850, ROT, 110, -8)
       + chip("my-c", "✅ eigene Abfrage = kein Einfluss", GRUEN, 1110, 42))
J14 = lambda a, d: (f'tl.fromTo("#my-z", {{ y: -400, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, {a}); stempeln("#my-s", {cap("s14", 3)});'  # noqa: E731
                    f' pop("#my-c", {cap("s14", 3)} + 0.5);')

ZEILEN = [("Girokonto", "✓", GRUEN), ("Handyvertrag", "✓", GRUEN), ("Kredit offen", "✗ falsch!", ROT), ("Kreditkarte", "✓", GRUEN)]
DOC = (f'<div id="da-k" class="mono" style="position:absolute;left:120px;top:470px;width:840px;padding:44px 50px;border-radius:30px;background:#f4f1ea;box-shadow:0 30px 60px #000;z-index:2;color:#222">'
       f'<div style="font-family:Montserrat;font-weight:900;font-size:46px;margin-bottom:18px">Deine gespeicherten Daten</div>'
       + "".join(f'<div id="da-{i}" style="display:flex;justify-content:space-between;font-size:44px;margin:16px 0;padding-bottom:10px;border-bottom:2px dashed #ccc">'
                 f'<span>{a}</span><span style="color:{f};font-weight:800">{b}</span></div>' for i, (a, b, f) in enumerate(ZEILEN)) + '</div>')
LUPE = (f'<svg id="da-l" viewBox="0 0 200 200" style="position:absolute;left:560px;top:600px;width:240px;height:240px;z-index:5;filter:drop-shadow(0 0 20px {GELB})">'
        f'<circle cx="80" cy="80" r="56" fill="#ffffff10" stroke="{GELB}" stroke-width="14"/><path d="M122 122 L180 180" stroke="{GELB}" stroke-width="20" stroke-linecap="round"/></svg>')
S15 = DOC + LUPE + stempel("da-s", "BERICHTIGEN!", 300, 1100, OR, 72, -6)
J15 = lambda a, d: (f'pop("#da-k", {a});' + "".join(f' pop("#da-{i}", {cap("s15", 1)} + {0.2 * i});' for i in range(4))  # noqa: E731
                    + f' tl.fromTo("#da-l", {{ x: 300, y: 300, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.5 }}, {cap("s15", 2)}); stempeln("#da-s", {cap("s15", 3)});')

S16 = (tz("ge-a", "besserer Score", 480, 90, "glow-g") + pfeil("ge-p", 540, 600, 540, 760, 0.0, "#fff", 10) + tz("ge-b", "bessere Zinsen", 780, 90, "glow-o")
       + tz("ge-c", "= mehr Geld für dich", 960, 70) + partikel("ge-x", 540, 850, 30, (GRUEN, GELB, "#fff"), 600) + unterstrich("ge-u", 250, 1060, 580, GRUEN))
J16 = lambda a, d: (f'pop("#ge-a", {a}); draw("#ge-p-p", {a} + 0.4, 0.3); pop("#ge-p-k", {a} + 0.65); slam("#ge-b", {cap("s16", 1)}); pop("#ge-c", {cap("s16", 1)} + 0.4);'  # noqa: E731
                    f' burst("#ge-x", {cap("s16", 1)} + 0.3); draw("#ge-u-p", {cap("s16", 1)} + 0.7, 0.4);')

SZENEN = [(0.0, st("s2"), S1, J1), (st("s2"), st("s3"), S2, J2), (st("s3"), st("s4"), cta_html, cta_js), (st("s4"), st("s5"), S4, J4),
          (st("s5"), st("s6"), S5, J5), (st("s6"), st("s7"), S6, J6), (st("s7"), st("s9"), S7, j7), (st("s9"), st("s10"), S9, J9),
          (st("s10"), st("s13"), S10, J10), (st("s13"), st("s14"), S13, J13), (st("s14"), st("s15"), S14, J14), (st("s15"), st("s16"), S15, J15),
          (st("s16"), DAUER, S16, J16)]
SFX = [(0.0, "bass-schlag"), (cap("s1", 1), "pop"), (cap("s1", 2), "pop"), (cap("s1", 3), "pop"), (st("s2"), "handy-benachrichtigung"), (cap("s2", 1), "stempel"),
       (cap("s2", 2), "uhr-tickt"), (st("s3"), "whoosh-weich"), (st("s4"), "swipe"), (st("s5"), "whoosh-schnell"), (cap("s5", 1), "falsch"), (cap("s5", 2), "richtig"),
       (st("s6"), "whoosh-weich"), (cap("s6", 1) + 0.3, "stempel"), (st("s7"), "whoosh-weich"), (cap("s7", 1), "kurve-hoch"), (cap("s8", 1), "level-up"),
       (st("s9"), "swipe"), (cap("s9", 2), "tippen"), (cap("s9", 3) + 0.5, "stempel"), (st("s10"), "whoosh-weich"), (cap("s10", 1), "klick"), (st("s11"), "klick"),
       (cap("s12", 2), "karte-piep"), (st("s13"), "zaehler"), (st("s13") + 1.6, "geld-erhalten"), (cap("s13", 2), "stempel"), (st("s14"), "swipe"), (cap("s14", 3), "nv-falsch-buzzer"),
       (cap("s14", 3) + 0.5, "richtig"), (st("s15"), "papier-reissen"), (cap("s15", 2), "whoosh-schnell"), (cap("s15", 3), "stempel"), (st("s16"), "whoosh-weich"),
       (cap("s16", 1) + 0.3, "muenzen-glas")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
