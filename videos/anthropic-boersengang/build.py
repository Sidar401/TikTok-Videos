#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (61–75 s, Analyse-Look): Anthropic-Börsengang → verweist auf YouTube-Longform „KI-Blase“."""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, balken, donut, hand, karte, kasten, kit_assets, kreis,  # noqa: E402
                         logo_karte, pfeil, racks, raster, spanne, stempel, ticker, unterstrich, zettel)
from glow_short import TEILEN_SVG, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402
from motor import endkarte  # noqa: E402


def tz(*a, **k):
    """t() über Analyse-Karten (z-index 5)."""
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)

LOGOS = ["anthropic", "claude", "nasdaq", "google", "nvidia", "microsoft", "amd", "broadcom", "micron"]
kit_assets(HERE, LOGOS)
shutil.copy(HERE.parent.parent / "renders/thumbnails/longform-ki-blase-1.jpg", HERE / "assets/lf.jpg")
cap, st, en, DAUER = zeiten(HERE)
TSMC_ROT = "#e60012"

# 1 Hook ---------------------------------------------------------------
TICK = ticker("tk", [("ANT", GRUEN), ("▲ IPO", GRUEN), ("NASDAQ", None), ("70–78 $", GELB), ("KI", OR), ("825 Mio.", None)], 1190)
S1 = (KIT_CSS + t("h1", "Der größte", 450, 104) + t("h2", '<span class="box">BÖRSENGANG</span>', 590, 108) + t("h3", "aller Zeiten", 760, 96, "glow-o")
      + logo_karte("h-an", "anthropic", 240, 930, 600, 150) + TICK + partikel("h-p", 540, 650, 26, (OR, GELB, "#fff"), 560))


def j1(a, d):
    return (KIT_JS + f' slam("#h1", {a}); slam("#h2", {a} + 0.25); flash({a} + 0.25, 0.6); burst("#h-p", {a} + 0.3); pop("#h3", {cap("s1", 1)});'
            f' tl.fromTo("#h-an", {{ y: 300, opacity: 0, rotation: 8 }}, {{ y: 0, opacity: 1, rotation: -2, duration: 0.5, ease: "back.out(1.7)" }}, {cap("s1", 2)});'
            f' tl.fromTo("#tk", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {a} + 0.4); lauf("#tk", {a}, {d});')


# 2 Claude → Anthropic → Nasdaq ------------------------------------------
S2 = (logo_karte("c-an", "anthropic", 190, 450, 700, 170) + hand("c-h1", "die Firma hinter …", 540, 650, 64, GELB, -3, True)
      + logo_karte("c-cl", "claude", 90, 760, 440, 150, glow="#d97757") + pfeil("c-pf", 560, 840, 700, 1000, 0.35)
      + logo_karte("c-nq", "nasdaq", 560, 1010, 440, 150, glow="#0996c7") + hand("c-h2", "Börse in New York", 780, 1180, 52, "#9fd8ee", 2, True))


def j2(a, d):
    return (f'pop("#c-an", {a}); pop("#c-h1", {cap("s2", 1)}); pop("#c-cl", {cap("s2", 2)}); draw("#c-pf-p", {cap("s2", 3)}, 0.45); pop("#c-pf-k", {cap("s2", 3)} + 0.4);'
            f' pop("#c-nq", {cap("s2", 3)} + 0.35); pop("#c-h2", {cap("s2", 3)} + 0.7);')


# 3 Hinweis ------------------------------------------------------------
S3 = (zettel("hw-z", "Keine Anlage&shy;beratung –<br/>nur eine Erklärung", 200, 560, 680, 86, GELB, -3) + stempel("hw-s", "INFO", 640, 940, OR, 70, 12))


def j3(a, d):
    return (f'tl.fromTo("#hw-z", {{ y: -500, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});'
            f' stempeln("#hw-s", {cap("s3", 1)});')


# 4 Preisspanne -------------------------------------------------------
S4 = (karte("pr-k", 90, 440, 900, 760, "Preis pro Aktie", "S-1 Börsenprospekt · Spanne") + spanne("pr-s", 170, 760, 740, 0.22, 0.78, "70 $", "78 $")
      + tz("pr-z", "70 – 78 $", 900, 130, "glow-g") + hand("pr-h", "← Spanne, Endpreis kommt noch", 540, 1110, 50, GELB, -2, True))


def j4(a, d):
    return f'pop("#pr-k", {a}); spann("#pr-s", {cap("s4", 1)}); slam("#pr-z", {cap("s4", 1)} + 0.3); pop("#pr-h", {cap("s4", 1)} + 0.9);'


# 5 825 Mio. Aktien + Kürzel ANT -----------------------------------------
S5 = (raster("ak-r", 150, 470, 15, 8, 40, 14, OR, GELB) + t("ak-z", "825", 900, 190, "glow-o") + t("ak-u", "Mio. Aktien", 1095, 64)
      + f'<div id="ak-tk" class="mono" style="position:absolute;left:700px;top:430px;padding:14px 30px;border-radius:18px;background:#0b0d0e;border:4px solid {GRUEN};'
        f'color:{GRUEN};font-size:70px;box-shadow:0 0 50px {GRUEN}77;transform:rotate(6deg);z-index:5">ANT ▲</div>')


def j5(a, d):
    return (f'tl.fromTo("#ak-r .q", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, stagger: 0.008, ease: "back.out(2)" }}, {a});'
            f' pop("#ak-z", {cap("s5", 1)}); zaehl("#ak-z", 0, 825, {cap("s5", 1)}, 1.1); pop("#ak-u", {cap("s5", 1)} + 0.2); slam("#ak-tk", {cap("s5", 2)} + 0.3);')


# 6 Käufer-Netz -------------------------------------------------------
NETZ = [("google", 70, 430), ("nvidia", 620, 430), ("microsoft", 70, 600), ("amd", 620, 600), ("broadcom", 70, 940), ("micron", 620, 940), ("tsmc", 345, 1070)]
S6 = logo_karte("n-an", "anthropic", 300, 770, 480, 120, glow=OR, pad=0.2)
for i, (nm, x, y) in enumerate(NETZ):
    cx, cy = x + 195, y + 60
    tx, ty = (540, 770) if cy < 830 else (540, 890)
    S6 += pfeil(f"n-l{i}", cx, cy + (60 if cy < 830 else -60), tx + (cx - 540) * 0.25, ty, 0.12, OR, 6)
    S6 += (logo_karte(f"n-{nm}", nm, x, y, 390, 120, pad=0.2) if nm != "tsmc" else logo_karte("n-tsmc", "", x, y, 390, 120, text="tsmc", farbe=TSMC_ROT))
S6 += chip("n-sum", "zusammen 26 Mrd. $", GRUEN, 1195, 56)


def j6(a, d):
    zeitpunkte = [cap("s6", 0) + 0.5, cap("s6", 1), cap("s6", 1) + 0.45, cap("s6", 1) + 0.95, cap("s6", 2), cap("s6", 3), cap("s6", 4) + 0.2]
    js = f'pop("#n-an", {a});'
    for i, ((nm, *_), z) in enumerate(zip(NETZ, zeitpunkte)):
        js += f' pop("#n-{nm}", {z}); draw("#n-l{i}-p", {z} + 0.1, 0.35); pop("#n-l{i}-k", {z} + 0.4);'
    return js + f' slam("#n-sum", {cap("s6", 5)}); tl.fromTo("#n-an", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 3 }}, {cap("s6", 5)});'


# 7 Bewertung 1,4 Billionen ----------------------------------------------
S7 = (t("bw-a", "Anthropic wäre wert", 470, 70) + t("bw-z", "1,4", 590, 300, "glow-g") + t("bw-u", "Billionen $", 920, 110)
      + kreis("bw-k", 540, 760, 330, 210, GELB) + hand("bw-h", "bis zu! (alle Aktien gezählt)", 540, 1100, 54, GELB, -3, True)
      + partikel("bw-p", 540, 760, 30, (GRUEN, GELB, "#fff"), 600))


def j7(a, d):
    return (f'pop("#bw-a", {a}); slam("#bw-z", {cap("s7", 1)}); burst("#bw-p", {cap("s7", 1)} + 0.2); pop("#bw-u", {cap("s7", 1)} + 0.3);'
            f' draw("#bw-k-p", {cap("s7", 1)} + 0.6, 0.6); pop("#bw-h", {cap("s7", 1)} + 1.1);')


# 8 Teilen-CTA -----------------------------------------------------------
cta_html, cta_js = cta_szene("te", TEILEN_SVG, "Schick das jemandem,<br/>der KI-Aktien kauft!")

# 9+10 Umsatz-Analyse ---------------------------------------------------
BASIS = 1180
S9 = (karte("um-k", 70, 430, 940, 880, "Umsatz", "jeweils erste 9 Monate") + balken("um-a", 230, BASIS, 230, 60, GRAU, "2,5 Mrd. $", "2025", 48)
      + balken("um-b", 620, BASIS, 230, 520, GRUEN, "33,2 Mrd. $", "2026", 56) + pfeil("um-pf", 360, 1050, 600, 720, -0.3, GELB, 8)
      + hand("um-h", "13×!", 330, 760, 130, GELB, -8) + kreis("um-kr", 735, 615, 210, 70, GELB, 6))


def j9(a, d):
    return (f'pop("#um-k", {a}); wachs("#um-a", {cap("s9", 3)}); pop("#um-a-o", {cap("s9", 3)} + 0.4);'
            f' wachs("#um-b", {cap("s10", 2)}, 0.9); pop("#um-b-o", {cap("s10", 2)} + 0.8); draw("#um-pf-p", {cap("s10", 3)}, 0.5); pop("#um-pf-k", {cap("s10", 3)} + 0.45);'
            f' slam("#um-h", {cap("s10", 3)} + 0.4); draw("#um-kr-p", {cap("s10", 3)} + 0.9, 0.5);')


# 11 Unterm Strich -----------------------------------------------------
ZEILE = 'style="display:flex;justify-content:space-between;font-size:54px;margin:14px 0"'
S11 = (f'<div id="us-k" class="mono" style="position:absolute;left:120px;top:470px;width:840px;padding:50px 56px;border-radius:30px;background:#14181bee;'
       f'border:3px solid #ffffff22;box-shadow:0 30px 60px #000;z-index:2;color:#fff">'
       f'<div style="font-family:Montserrat;font-weight:900;font-size:44px;color:{GRAU};margin-bottom:20px">Erste 9 Monate 2026</div>'
       f'<div {ZEILE}><span>Umsatz</span><span style="color:{GRUEN}">+ 33,2 Mrd.</span></div>'
       f'<div {ZEILE}><span>Kosten …</span><span style="color:#ffffffaa">…</span></div>'
       f'<div id="us-l" style="height:6px;background:#fff;margin:26px 0;transform-origin:0 50%"></div>'
       f'<div id="us-v" {ZEILE}><span>Ergebnis</span><span style="color:{ROT};text-shadow:0 0 30px {ROT}">− 104 Mrd. $</span></div></div>'
       + unterstrich("us-u", 520, 950, 400, ROT) + stempel("us-s", "VERLUST", 300, 1060, ROT, 84, -8))


def j11(a, d):
    return (f'pop("#us-k", {a}); tl.fromTo("#us-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4 }}, {cap("s11", 1)}); slam("#us-v", {cap("s11", 2)});'
            f' draw("#us-u-p", {cap("s11", 2)} + 0.4, 0.4); stempeln("#us-s", {cap("s11", 2)} + 0.8);')


# 12 Donut: 94 von 104 nur Papier -------------------------------------
S12 = (donut("do", 540, 800, 250, [(94.3 / 104, GRAU), (9.7 / 104, ROT)], 90) + tz("do-z", "104", 720, 120) + tz("do-u", "Mrd. $ Verlust", 850, 40)
       + hand("do-h1", "94 Mrd. = nur Papier", 380, 450, 66, GELB, -6, True) + pfeil("do-p1", 300, 530, 360, 640, -0.2, GELB, 7)
       + chip("do-c", "📄 Verlust auf dem Papier", OR, 1140, 58))


def j12(a, d):
    return (f'pop("#do-z", {a}); pop("#do-u", {a} + 0.15); draw("#do-1", {a} + 0.2, 0.3); draw("#do-0", {cap("s12", 1)}, 0.9);'
            f' pop("#do-h1", {cap("s12", 1)} + 0.6); draw("#do-p1-p", {cap("s12", 1)} + 0.9, 0.4); pop("#do-p1-k", {cap("s12", 1)} + 1.25); slam("#do-c", {cap("s12", 3)});')


# 13 Warum: Anleihe → Aktie -------------------------------------------
KURVE = ('<svg id="an-kv" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;z-index:3">'
         f'<path id="an-kv-p" d="M150 1110 L300 1080 L420 1050 L520 960 L640 930 L760 800 L900 690" fill="none" stroke="{GRUEN}" stroke-width="12" stroke-linecap="round" '
         f'stroke-linejoin="round" style="filter:drop-shadow(0 0 14px {GRUEN})"/></svg>')
S13 = (kasten("an-a", "Anleihe", 80, 450, 380, 170, OR, 60, "Geld geliehen") + pfeil("an-p", 470, 535, 610, 535, 0.0, "#fff", 8)
       + hand("an-h", "später", 540, 455, 50, GELB, -4, True) + kasten("an-b", "Aktie", 620, 450, 380, 170, GRUEN, 60, "Tausch")
       + karte("an-k", 90, 700, 900, 470) + hand("an-t", "Firmenwert ↑", 170, 730, 64, GRUEN, -2) + KURVE
       + stempel("an-s", "ANLEIHE MEHR WERT", 140, 1000, OR, 52, -6))


def j13(a, d):
    return (f'pop("#an-a", {cap("s13", 0)}); pop("#an-h", {cap("s13", 1)}); draw("#an-p-p", {cap("s13", 1)}, 0.4); pop("#an-p-k", {cap("s13", 1)} + 0.35); pop("#an-b", {cap("s13", 2)});'
            f' pop("#an-k", {cap("s13", 3)}); pop("#an-t", {cap("s13", 3)} + 0.2); draw("#an-kv-p", {cap("s13", 4)}, 0.8); stempeln("#an-s", {cap("s13", 5)} + 0.2);')


# 14 Echtes Geschäft: nur 1,3 Mrd. ------------------------------------
BASIS2 = 1150
S14 = (karte("eg-k", 70, 430, 940, 880, "Verlust (9 Monate)", "Papier vs. echtes Geschäft") + balken("eg-a", 220, BASIS2, 240, 520, GRAU, "94,3 Mrd.", "Papier", 52)
       + balken("eg-b", 620, BASIS2, 240, 8, ROT, "1,3 Mrd.", "Geschäft", 64) + kreis("eg-kr", 740, 1130, 190, 70, GELB, 6)
       + hand("eg-h", "nur das hier ist echt!", 760, 930, 54, GELB, -6, True))


def j14(a, d):
    return (f'pop("#eg-k", {a}); wachs("#eg-a", {a} + 0.2); pop("#eg-a-o", {a} + 0.6); wachs("#eg-b", {cap("s14", 2)}, 0.3); slam("#eg-b-o", {cap("s14", 2)});'
            f' draw("#eg-kr-p", {cap("s14", 2)} + 0.4, 0.5); pop("#eg-h", {cap("s14", 2)} + 0.8);')


# 15 900 Mrd. für Rechenzentren ----------------------------------------
CHIP = (f'<svg id="rz-c" viewBox="0 0 200 200" style="position:absolute;left:800px;top:420px;width:200px;height:200px;z-index:4;filter:drop-shadow(0 0 20px {OR})">'
        f'<rect x="45" y="45" width="110" height="110" rx="14" fill="#1b1f22" stroke="{OR}" stroke-width="8"/><rect x="75" y="75" width="50" height="50" rx="6" fill="{OR}"/>'
        + "".join(f'<rect x="{60 + k * 30}" y="15" width="10" height="28" rx="4" fill="{OR}"/><rect x="{60 + k * 30}" y="157" width="10" height="28" rx="4" fill="{OR}"/>'
                  f'<rect x="15" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{OR}"/><rect x="157" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{OR}"/>' for k in range(3))
        + '</svg>')
S15 = (racks("rz-r", 130, 700, 4, 180, 420, 40) + CHIP + t("rz-z", "900", 400, 190, "glow-o") + t("rz-u", "Mrd. $ zugesagt", 600, 60)
       + hand("rz-h", "für Rechenzentren + Chips", 540, 1150, 58, GELB, -3, True))


def j15(a, d):
    return (f'pop("#rz-z", {cap("s15", 1)}); zaehl("#rz-z", 0, 900, {cap("s15", 1)}, 1.2); pop("#rz-u", {cap("s15", 1)} + 0.3); blink("#rz-r", {cap("s15", 3)});'
            f' tl.fromTo("#rz-c", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }}, {cap("s15", 4)}); pop("#rz-h", {cap("s15", 4)} + 0.3);')


mk_html, mk_js = endkarte("assets/lf.jpg", "Ganzes Video")

SZENEN = [
    (0.0, st("s2"), S1, j1), (st("s2"), st("s3"), S2, j2), (st("s3"), st("s4"), S3, j3), (st("s4"), st("s5"), S4, j4),
    (st("s5"), st("s6"), S5, j5), (st("s6"), st("s7"), S6, j6), (st("s7"), st("s8"), S7, j7), (st("s8"), st("s9"), cta_html, cta_js),
    (st("s9"), st("s11"), S9, j9), (st("s11"), st("s12"), S11, j11), (st("s12"), st("s13"), S12, j12), (st("s13"), st("s14"), S13, j13),
    (st("s14"), st("s15"), S14, j14), (st("s15"), st("s16"), S15, j15), (st("s16"), DAUER, mk_html, mk_js),
]

SFX = [(0.0, "bass-schlag"), (0.25, "nv-boom-kurz"), (cap("s1", 2), "whoosh-schnell"), (st("s2"), "whoosh-weich"), (cap("s2", 2), "pop"), (cap("s2", 3), "klick"),
       (st("s3"), "swipe"), (cap("s3", 1), "stempel"), (st("s4"), "whoosh-weich"), (cap("s4", 1), "karte-piep"), (st("s5"), "zaehler"), (cap("s5", 2) + 0.3, "kurve-hoch"),
       (st("s6"), "whoosh-schnell"), (cap("s6", 0) + 0.5, "pop"), (cap("s6", 1), "pop"), (cap("s6", 1) + 0.45, "pop"), (cap("s6", 1) + 0.95, "pop"), (cap("s6", 2), "pop"),
       (cap("s6", 3), "pop"), (cap("s6", 4) + 0.2, "pop"), (cap("s6", 5), "kasse"), (cap("s7", 1), "nv-boom-tief"), (cap("s7", 1) + 0.6, "level-up"),
       (st("s8"), "whoosh-weich"), (st("s9"), "nv-sog"), (cap("s10", 2), "kurve-hoch"), (cap("s10", 3) + 0.4, "nv-pling-idee"),
       (st("s11"), "whoosh-schnell"), (cap("s11", 2), "kurve-runter"), (cap("s11", 2) + 0.8, "stempel"), (st("s12"), "whoosh-weich"), (cap("s12", 3), "papier-reissen"),
       (st("s13"), "swipe"), (cap("s13", 4), "kurve-hoch"), (cap("s13", 5) + 0.2, "stempel"), (st("s14"), "whoosh-weich"), (cap("s14", 2), "richtig"),
       (st("s15"), "whoosh-schnell"), (cap("s15", 1), "zaehler"), (cap("s15", 3), "tippen"), (st("s16"), "whoosh-weich"), (st("s16") + 0.3, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
