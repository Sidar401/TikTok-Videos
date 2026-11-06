#!/usr/bin/env python3
"""HundeFinanzTv Probe-Short im neuen Stil (Nutzer 6.11., nach Referenz „KI-Geldkreis“):
ein Leitbild, das Satz für Satz wächst (Geldfluss vom Chef bis aufs Konto), Beagle reagiert unten, Ein-Wort-Untertitel. Teilen-CTA."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GOLD, GRUEN, OR, ROT, TEILEN_SVG, build, cta_szene, outro_szene, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
BLAU = "#4d8ff0"


def knoten(id_, x, y, w, titel, betrag, farbe, extra=""):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:16px 0 18px;border-radius:26px;background:#16191b;'
            f'border:5px solid {farbe};box-shadow:0 0 40px {farbe}55;text-align:center;z-index:3">'
            f'<div style="font-weight:800;font-size:31px;color:#ffffffcc;white-space:nowrap">{titel}</div>'
            f'<div id="{id_}-z" style="font-weight:900;font-size:58px;line-height:1.05;color:{farbe};white-space:nowrap">{betrag}</div>{extra}</div>')


PFEILE = {  # id: (Pfad, Farbe)
    "a1": ("M340 535 L305 535", ROT),
    "a2": ("M540 625 L540 715", OR),
    "a3": ("M690 770 C720 760 740 730 760 715", ROT),
    "a4": ("M390 805 C360 830 340 860 322 880", ROT),
    "a5": ("M690 825 C720 870 730 930 745 960", ROT),
    "a6": ("M540 870 L540 1065", GRUEN),
}
SVG = ('<svg viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;z-index:2">'
       + "".join(f'<path id="{k}" d="{d}" fill="none" stroke="{f}" stroke-width="12" stroke-linecap="butt" filter="drop-shadow(0 0 10px {f})"/>'
                 for k, (d, f) in PFEILE.items()) + '</svg>')

LEITBILD = (
    t("ti", "WOHIN FLIESST DEIN GELD?", 392, 46, "glow-o")
    + SVG
    + knoten("k-chef", 340, 460, 400, "Dein Chef zahlt", "3.600 €", OR)
    + knoten("k-soz", 40, 460, 265, "Sozialkassen", "−600 €", ROT)
    + knoten("k-bru", 390, 715, 300, "Brutto", "3.000 €", OR)
    + knoten("k-st", 760, 640, 280, "Lohnsteuer", "−320 €", ROT)
    + knoten("k-re", 40, 820, 282, "Rente", "−279 €", BLAU)
    + knoten("k-kv", 745, 900, 290, "Krankenkasse", "−262 €", BLAU,
             '<div id="k-kv-x" style="font-weight:800;font-size:24px;color:#ffffffaa;margin-top:4px;white-space:nowrap">+ Pflege/ALV −111 €</div>')
    + knoten("k-kto", 340, 1065, 400, "Dein Konto", "2.000 €", "#9aa3a8")
    + f'<div id="k-pz" style="position:absolute;left:90px;top:1090px;padding:8px 26px 12px;border-radius:20px;background:{GRUEN};color:#111;font-weight:900;'
      f'font-size:58px;box-shadow:0 0 50px {GRUEN}99;transform:rotate(-6deg);z-index:4">56 %</div>'
    + partikel("kp", 540, 1140, 30, (GRUEN, GOLD, "#fff"), 560)
    # Beagle unten + Sprechblasen
    + f'<div id="bg" style="position:absolute;left:400px;top:1440px;width:280px;height:280px;border-radius:50%;overflow:hidden;border:8px solid {OR};'
      f'box-shadow:0 0 60px {OR}88;background:#16191b;z-index:4">{BEAGLE}</div>'
    + "".join(f'<div id="{i}" style="position:absolute;left:{x}px;top:1400px;padding:10px 30px 14px;border-radius:30px;background:#fff;color:#111;'
              f'font-weight:900;font-size:64px;z-index:5;box-shadow:0 10px 30px #000a">{txt}</div>'
              for i, txt, x in (("b1", "?", 700), ("b2", "Hä?!", 680), ("b3", "WOW!", 690)))
)


def leitbild_js(a, d):
    js = [
        f'tl.fromTo("#k-chef", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.35 }}, 0); tl.fromTo("#bg", {{ y: 0 }}, {{ y: -40, duration: 0.18, yoyo: true, repeat: 3, ease: "power1.out" }}, 0.1);',
        f'tl.fromTo("#k-chef", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.15, yoyo: true, repeat: 1 }}, {cap("s1", 1)});',
        # s2: Konto + Fragezeichen
        f'pop("#k-kto", {st("s2")} + 0.1); pop("#b1", {cap("s2", 2)}); tl.fromTo("#bg", {{ rotation: 0 }}, {{ rotation: -12, duration: 0.25, yoyo: true, repeat: 1 }}, {cap("s2", 2)});',
        f'tl.to("#b1", {{ opacity: 0, duration: 0.15 }}, {st("s3")} + 0.3);',
        # s3: Sozialkassen
        f'draw("#a1", {st("s3")} + 0.1, 0.3); pop("#k-soz", {st("s3")} + 0.3); pop("#b2", {cap("s3", 2)}); shake("#bg", {cap("s3", 2)});',
        f'tl.to("#b2", {{ opacity: 0, duration: 0.15 }}, {st("s4")} + 0.3);',
        # s4: Brutto + Lohnsteuer
        f'draw("#a2", {st("s4")}, 0.35); pop("#k-bru", {st("s4")} + 0.3); draw("#a3", {cap("s4", 1)}, 0.35); pop("#k-st", {cap("s4", 1)} + 0.3); shake("#k-st", {cap("s4", 2)});',
        # s5: Rente
        f'draw("#a4", {st("s5")}, 0.35); pop("#k-re", {st("s5")} + 0.3);',
        # s6: Krankenkasse + Pflege/ALV
        f'draw("#a5", {st("s6")}, 0.35); pop("#k-kv", {st("s6")} + 0.3); pop("#k-kv-x", {cap("s6", 1)});',
        # s7: Netto aufs Konto
        f'draw("#a6", {st("s7")}, 0.5); tl.fromTo("#k-kto", {{ borderColor: "#9aa3a8" }}, {{ borderColor: "{GRUEN}", duration: 0.3 }}, {st("s7")} + 0.4);',
        f'tl.fromTo("#k-kto-z", {{ color: "#9aa3a8" }}, {{ color: "{GRUEN}", duration: 0.3 }}, {st("s7")} + 0.4); zaehl("#k-kto-z", 0, 2028, {st("s7")} + 0.4, 0.9, " €");',
        f'slam("#k-pz", {cap("s7", 1)}); burst("#kp", {cap("s7", 1)} + 0.2); pop("#b3", {cap("s7", 1)}); tl.fromTo("#bg", {{ y: 0, scale: 1 }}, {{ y: -70, scale: 1.08, duration: 0.2, yoyo: true, repeat: 3 }}, {cap("s7", 1)});',
    ]
    return " ".join(js)


teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick's jemandem,<br/>der sich über sein<br/>Netto wundert!")
outro_html, outro_js = outro_szene(BEAGLE)

SZENEN = [
    (0.0, st("s8"), LEITBILD, leitbild_js),
    (st("s8"), st("sF"), teilen_html, teilen_js),
    (st("sF"), DAUER, outro_html, outro_js),
]

SFX = [(0.0, "boom"), (cap("s1", 1), "kasse"), (st("s2") + 0.1, "pop"), (cap("s2", 2), "ding"),
       (st("s3") + 0.1, "whoosh"), (st("s3") + 0.3, "pop"), (cap("s3", 2), "boom"),
       (st("s4"), "whoosh"), (st("s4") + 0.3, "pop"), (cap("s4", 1), "whoosh"), (cap("s4", 1) + 0.3, "pop"),
       (st("s5"), "whoosh"), (st("s5") + 0.3, "pop"), (st("s6"), "whoosh"), (st("s6") + 0.3, "pop"), (cap("s6", 1), "pop"),
       (st("s7"), "whoosh")] + [(st("s7") + 0.4 + i * 0.09, "tick") for i in range(10)] + \
      [(cap("s7", 1), "boom"), (cap("s7", 1) + 0.05, "kasse"), (st("s8"), "whoosh"), (st("sF"), "whoosh"), (st("sF") + 0.6, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX, ein_wort=1270, drift=False)
