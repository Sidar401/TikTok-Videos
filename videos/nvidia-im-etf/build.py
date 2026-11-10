#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (Analyse-Look, ~70 s): Steckt Nvidia in deinem ETF? → verweist auf Longform „Nvidia-Krimi“ (nur „bei uns auf dem Kanal“)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, donut, flagge, hand, karte, kasten, kit_assets, kreis, linie,  # noqa: E402
                         logo_karte, pfeil, raster, stempel, unterstrich, zettel)
from glow_short import TEILEN_SVG, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402
from motor import endkarte  # noqa: E402

NV = "#76b900"
kit_assets(HERE, ["nvidia", "apple", "microsoft", "amazon", "google", "msci", "flagge-usa"])
cap, st, en, DAUER = zeiten(HERE)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def msci(id_, x, y, w=360, h=120):
    if (HERE / "assets/logos/msci.svg").exists():
        return logo_karte(id_, "msci", x, y, w, h, pad=0.2)
    return logo_karte(id_, "", x, y, w, h, text="MSCI", farbe="#002f6c", pad=0.2)


# 1 Hook: verteilt?
PUNKTE = "".join(f'<div class="vt" style="position:absolute;left:{140 + (i * 137) % 800}px;top:{470 + (i * 89) % 560}px;width:{34 + (i * 7) % 30}px;height:{34 + (i * 7) % 30}px;'
                 f'border-radius:50%;background:{(OR, GRUEN, "#4d8ff0", GELB)[i % 4]};box-shadow:0 0 16px {(OR, GRUEN, "#4d8ff0", GELB)[i % 4]};z-index:1;opacity:0.85"></div>' for i in range(28))
S1 = KIT_CSS + PUNKTE + tz("h1", "ETF-Sparplan", 560, 110, "glow-o").replace("z-index:5", "z-index:6") + hand("h2", "schön verteilt?", 540, 760, 80, GELB, -4, True)


def j1(a, d):
    return (KIT_JS + f' tl.fromTo(".vt", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, stagger: 0.03, ease: "back.out(2)" }}, {a});'
            f' slam("#h1", {a}); pop("#h2", {cap("s1", 2)});')


# 2 an einer Firma?
S2 = logo_karte("f-nv", "nvidia", 290, 560, 500, 150, glow=NV) + kreis("f-k", 540, 635, 330, 140, ROT) + tz("f-q", "eine Firma?", 830, 100, "glow-r")
SV = lambda a, d: f'pop("#f-q", {cap("s2", 1)}); pop("#f-nv", {cap("s2", 2)}); draw("#f-k-p", {cap("s2", 2)} + 0.3, 0.5);'  # noqa: E731

# 3 Hinweis
S3 = zettel("hw", "Keine Anlage&shy;beratung", 220, 560, 640, 86, GELB, -3)
J3 = lambda a, d: f'tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});'  # noqa: E731

# 4 MSCI World: 1.300 Firmen, 23 Länder
S4 = (msci("ms", 360, 450, 360, 120) + hand("ms-h", "World · beliebtester ETF", 540, 590, 52, GELB, -2, True) + raster("ms-r", 190, 690, 20, 8, 28, 8, "#4d8ff0", OR)
      + tz("ms-z", "1.300+ Firmen", 1000, 80) + chip("ms-c", "23 Länder", GRUEN, 1110, 56))


def j4(a, d):
    return (f'pop("#ms", {a}); pop("#ms-h", {cap("s4", 2)}); tl.fromTo("#ms-r .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.006 }}, {cap("s4", 3)});'
            f' pop("#ms-z", {cap("s4", 3)} + 0.3); pop("#ms-c", {cap("s4", 4)});')


# 5 größte Firma Nvidia ~6 %
S5 = (karte("g-k", 70, 440, 940, 840, "Größte Firma im MSCI World", "Anteil am Index") + donut("g-d", 540, 860, 240, [(0.058, NV), (0.942, "#3a4248")], 90)
      + logo_karte("g-nv", "nvidia", 360, 790, 360, 100, glow=NV) + tz("g-z", "≈ 6 %", 950, 70, "glow-g") + hand("g-h", "Platz 1!", 820, 560, 72, NV, 8, True))


def j5(a, d):
    return (f'pop("#g-k", {a}); draw("#g-d-1", {a} + 0.2, 0.6); pop("#g-nv", {cap("s5", 1)}); draw("#g-d-0", {cap("s5", 2)}, 0.4); slam("#g-z", {cap("s5", 2)} + 0.2);'
            f' pop("#g-h", {cap("s5", 1)} + 0.4);')


# 6 100 € → 6 €
S6 = (raster("hu", 270, 460, 10, 10, 46, 8, "#3a4248") + tz("hu-t", "100 € Sparplan", 1010, 64) + hand("hu-h", "≈ 6 € Nvidia", 760, 430, 60, NV, -6, True)
      + pfeil("hu-p", 740, 500, 560, 490, 0.3, NV, 7))


def j6(a, d):
    return (f'tl.fromTo("#hu .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.005 }}, {a}); pop("#hu-t", {a} + 0.3);'
            f' tl.to("#hu .q:nth-child(-n+6)", {{ background: "{NV}", boxShadow: "0 0 20px {NV}", duration: 0.2, stagger: 0.1 }}, {cap("s6", 1)});'
            f' pop("#hu-h", {cap("s6", 1)} + 0.6); draw("#hu-p-p", {cap("s6", 2)}, 0.4); pop("#hu-p-k", {cap("s6", 2)} + 0.35);')


# 7 Top 10 = 28 %, USA-Technik
TOP = [("nvidia", 90, 470), ("apple", 560, 470), ("microsoft", 90, 640), ("amazon", 560, 640), ("google", 90, 810)]
S7 = ("".join(logo_karte(f"tp-{n}", n, x, y, 430, 140) for n, x, y in TOP) + flagge("tp-us", "flagge-usa", 620, 820, 300, 4)
      + tz("tp-z", "Top 10 ≈ 28 %", 1020, 96, "glow-o") + unterstrich("tp-u", 230, 1140, 620, OR))


def j7(a, d):
    return ("".join(f' pop("#tp-{n}", {cap("s7", 2)} + {0.15 * i});' for i, (n, *_) in enumerate(TOP)) + f' pop("#tp-us", {cap("s7", 2)});'
            f' slam("#tp-z", {cap("s7", 4)}); draw("#tp-u-p", {cap("s7", 4)} + 0.3, 0.4);')


# 8 Teilen-CTA
cta_html, cta_js = cta_szene("te", TEILEN_SVG, "Schick das jemandem<br/>mit ETF-Sparplan!")

# 9 Rechnung −10 % × 6 % ≈ −0,6 %
ZEILE = 'style="display:flex;justify-content:space-between;font-size:58px;margin:18px 0"'
S9 = (f'<div id="rc" class="mono" style="position:absolute;left:120px;top:470px;width:840px;padding:50px 56px;border-radius:30px;background:#14181bee;border:3px solid #ffffff22;box-shadow:0 30px 60px #000;z-index:2;color:#fff">'
      f'<div style="font-family:Montserrat;font-weight:900;font-size:44px;color:{GRAU};margin-bottom:16px">Rechnung</div>'
      f'<div id="rc-1" {ZEILE}><span>Nvidia</span><span style="color:{ROT}">− 10 %</span></div>'
      f'<div id="rc-2" {ZEILE}><span>Anteil</span><span>× 6 %</span></div>'
      f'<div id="rc-l" style="height:6px;background:#fff;margin:24px 0;transform-origin:0 50%"></div>'
      f'<div id="rc-3" {ZEILE}><span>dein ETF</span><span style="color:{ROT};text-shadow:0 0 30px {ROT}">≈ − 0,6 %</span></div></div>'
      + stempel("rc-s", "≈ HALBES PROZENT", 200, 1060, OR, 60, -5))


def j9(a, d):
    return (f'pop("#rc", {a}); pop("#rc-1", {cap("s9", 1)}); pop("#rc-2", {cap("s9", 2)}); tl.fromTo("#rc-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4 }}, {cap("s9", 3)});'
            f' slam("#rc-3", {cap("s9", 3)} + 0.3); stempeln("#rc-s", {cap("s9", 4)});')


# 10 10.000 € → fast 60 €
S10 = (tz("zt-a", "Depot", 460, 64) + tz("zt-b", "10.000 €", 550, 150) + pfeil("zt-p", 540, 760, 540, 900, 0.0, ROT, 10)
       + tz("zt-z", "≈ −60 €", 920, 180, "glow-r") + hand("zt-h", "nur wegen EINER Aktie", 540, 1140, 60, GELB, -3, True) + logo_karte("zt-nv", "nvidia", 720, 820, 260, 80, glow=NV))


def j10(a, d):
    return (f'pop("#zt-a", {a}); slam("#zt-b", {a} + 0.1); draw("#zt-p-p", {cap("s10", 1)}, 0.3); pop("#zt-p-k", {cap("s10", 1)} + 0.25);'
            f' slam("#zt-z", {cap("s10", 1)} + 0.3); pop("#zt-nv", {cap("s10", 2)}); pop("#zt-h", {cap("s10", 2)} + 0.2);')


# 11 + 12 Kurs: 2 Tage −10 %, seit Rekord −30 %
KURS = linie("ku", [0.55, 0.72, 0.88, 0.97, 0.9, 0.8, 0.72, 0.62, 0.45, 0.3], 140, 650, 800, 480, ROT, punkte=[(3, "Rekord Okt."), (9, "−30 %")])
S11 = (karte("ku-k", 70, 440, 940, 840, "Nvidia-Aktie", "Rekord → heute") + KURS + logo_karte("ku-nv", "nvidia", 660, 470, 320, 90, glow=NV)
       + kreis("ku-kr", 820, 960, 130, 90, GELB, 6) + hand("ku-h", "2 Tage: −10 %", 640, 1120, 56, GELB, -3, True))


def j11(a, d):
    return (f'pop("#ku-k", {a}); pop("#ku-nv", {a} + 0.2); draw("#ku-p", {cap("s11", 1)}, 1.4); draw("#ku-kr-p", {cap("s11", 3)}, 0.5); pop("#ku-h", {cap("s11", 3)} + 0.3);'
            f' pop("#ku-w0", {cap("s12", 0)}); pop("#ku-w1", {cap("s12", 1)}); tl.fromTo("#ku-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s12", 1)});')


# 13 ETF schlecht? Nein – breiter gestreut
S13 = (kasten("bs-a", "Einzelaktie", 80, 520, 420, 200, ROT, 56, "1 Firma") + kasten("bs-b", "ETF", 580, 520, 420, 200, GRUEN, 70, "1.300+ Firmen")
       + stempel("bs-s", "NEIN!", 380, 800, GRUEN, 110, -6) + hand("bs-h", "viel breiter gestreut", 540, 1080, 62, GELB, -3, True))


def j13(a, d):
    return f'pop("#bs-a", {a}); pop("#bs-b", {a} + 0.2); stempeln("#bs-s", {cap("s13", 1)} + 0.4); pop("#bs-h", {cap("s13", 2)});'


# 14 wie stark hängt er an KI?
S14 = (karte("ki-k", 70, 440, 940, 840, "Wissen, woran es hängt", "Top-10 im MSCI World") + donut("ki-d", 540, 860, 230, [(0.28, OR), (0.72, "#3a4248")], 80)
       + tz("ki-z", "≈ 28 %", 800, 84, "glow-o") + hand("ki-h", "fast nur KI + Technik", 540, 1150, 54, GELB, -3, True))


def j14(a, d):
    return f'pop("#ki-k", {a}); draw("#ki-d-1", {a} + 0.2, 0.4); draw("#ki-d-0", {cap("s14", 1)}, 0.6); pop("#ki-z", {cap("s14", 1)} + 0.3); pop("#ki-h", {cap("s14", 2)});'


mk_html, mk_js = endkarte("assets/lf.jpg", "Ganzes Video")

SZENEN = [
    (0.0, st("s2"), S1, j1), (st("s2"), st("s3"), S2, SV), (st("s3"), st("s4"), S3, J3), (st("s4"), st("s5"), S4, j4), (st("s5"), st("s6"), S5, j5),
    (st("s6"), st("s7"), S6, j6), (st("s7"), st("s8"), S7, j7), (st("s8"), st("s9"), cta_html, cta_js), (st("s9"), st("s10"), S9, j9),
    (st("s10"), st("s11"), S10, j10), (st("s11"), st("s13"), S11, j11), (st("s13"), st("s14"), S13, j13), (st("s14"), st("s15"), S14, j14),
    (st("s15"), DAUER, mk_html, mk_js),
]
SFX = [(0.0, "bass-schlag"), (0.05, "pop"), (cap("s1", 2), "nv-pling-idee"), (st("s2"), "whoosh-schnell"), (cap("s2", 2), "nv-dun-dun-dun"), (st("s3"), "swipe"),
       (st("s4"), "whoosh-weich"), (cap("s4", 3), "zaehler"), (st("s5"), "whoosh-schnell"), (cap("s5", 2), "bass-schlag"), (st("s6"), "zaehler"), (cap("s6", 1), "muenzen-klimpern"),
       (st("s7"), "whoosh-weich")] + [(cap("s7", 2) + 0.15 * i, "pop") for i in range(5)] + [
       (cap("s7", 4), "stempel"), (st("s8"), "whoosh-weich"), (st("s9"), "taschenrechner"), (cap("s9", 3) + 0.3, "klick"), (cap("s9", 4), "stempel"),
       (st("s10"), "swipe"), (cap("s10", 1) + 0.3, "kurve-runter"), (st("s11"), "whoosh-weich"), (cap("s11", 1), "kurve-runter"), (cap("s12", 1), "bass-schlag"),
       (st("s13"), "swipe"), (cap("s13", 1) + 0.4, "richtig"), (st("s14"), "whoosh-weich"), (cap("s14", 1), "nv-pling-idee"), (st("s15"), "whoosh-weich"), (st("s15") + 0.3, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
