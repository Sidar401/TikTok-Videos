#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow, wie freistellungsauftrag): Wohin fließt dein Gehalt? – Chef 3.600 € → Konto 2.028 € (Teilen-CTA).
Erste Fassung im Leitbild-Stil gefiel dem Nutzer nicht (zu viele Hundelogos) → build-probe-leitbild.py."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GRUEN, OR, ROT, TEILEN_SVG, build, chip, cta_szene, handy, outro_szene, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
BLAU = "#4d8ff0"


def svg(id_, inhalt, x, y, w, h, vb):
    return f'<svg id="{id_}" viewBox="{vb}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:2">{inhalt}</svg>'


GL = lambda f: f'filter="drop-shadow(0 0 20px {f})"'  # noqa: E731

KONTO = handy("ko", 380, 430, 320,
              '<div style="font-weight:800;font-size:30px;color:#ffffffaa">Kontostand</div>'
              '<div id="ko-z" style="font-weight:900;font-size:64px;color:#9aa3a8;white-space:nowrap">+2.000 €</div>'
              '<div style="font-weight:800;font-size:26px;color:#ffffff77">Gehalt Oktober</div>')
AMT = svg("st-a", f'<g {GL(ROT)}><path d="M20 80 L150 14 L280 80 Z" fill="none" stroke="{ROT}" stroke-width="12" stroke-linejoin="round"/>'
                  + "".join(f'<rect x="{46 + i * 56}" y="96" width="24" height="110" rx="6" fill="{ROT}"/>' for i in range(4))
                  + f'<rect x="20" y="214" width="260" height="22" rx="8" fill="{ROT}"/></g>', 330, 430, 420, 364, "0 0 300 260")
SANDUHR = svg("re-s", f'<g {GL(BLAU)}><path d="M60 20 L240 20 M60 380 L240 380" stroke="{BLAU}" stroke-width="22" stroke-linecap="round"/>'
                      f'<path d="M80 30 C80 140 150 160 150 200 C150 240 80 260 80 370 L220 370 C220 260 150 240 150 200 C150 160 220 140 220 30 Z" fill="none" stroke="{BLAU}" stroke-width="14"/>'
                      f'<path id="re-o" d="M100 60 L200 60 C190 130 160 150 150 175 C140 150 110 130 100 60 Z" fill="{OR}"/>'
                      f'<path id="re-u" d="M150 260 C120 300 105 330 100 360 L200 360 C195 330 180 300 150 260 Z" fill="{OR}"/></g>', 390, 430, 300, 400, "0 0 300 400")
KREUZ = svg("kv-k", f'<g {GL(BLAU)}><circle cx="150" cy="150" r="140" fill="#16191b" stroke="{BLAU}" stroke-width="14"/>'
                    f'<path d="M115 60 H185 V115 H240 V185 H185 V240 H115 V185 H60 V115 H115 Z" fill="{ROT}"/></g>', 390, 430, 300, 300, "0 0 300 300")


def balken(id_, x, h, farbe, oben, zahl):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{1200 - h}px;width:260px;height:{h}px;border-radius:24px 24px 0 0;background:{farbe};'
            f'box-shadow:0 0 50px {farbe}77;transform-origin:50% 100%;z-index:2"></div>'
            f'<div id="{id_}-t" class="t" style="left:{x - 410}px;top:{1200 - h - 120}px;font-size:58px;color:{farbe};white-space:nowrap">{zahl}</div>'
            f'<div class="t" style="left:{x - 410}px;top:1215px;font-size:40px">{oben}</div>')


teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick's jemandem,<br/>der sich über sein<br/>Netto wundert!")
outro_html, outro_js = outro_szene(BEAGLE)

SZENEN = [
    (0.0, cap("s1", 1),
     t("hk-a", "Dein Chef zahlt", 470, 96) + t("hk-z", "3.600 €", 640, 230, "glow-o") + chip("hk-c", "für DICH – jeden Monat", OR, 950, 60),
     lambda a, d: f'tl.fromTo("#hk-z", {{ scale: 1.2 }}, {{ scale: 1, duration: 0.35 }}, {a}); pop("#hk-c", {a} + 0.5);'),
    (cap("s1", 1), st("s2"),
     t("hk2-z", "3.600 €", 560, 230, "glow-o") + t("hk2-t", "im Monat", 860, 90) + partikel("hk2-p", 540, 680, 26, (OR, "#fff"), 520),
     lambda a, d: f'slam("#hk2-z", {a}); burst("#hk2-p", {a} + 0.25); pop("#hk2-t", {a} + 0.4);'),
    (st("s2"), cap("s2", 2),
     KONTO + t("ko-t", "auf deinem Konto", 1080, 70),
     lambda a, d: f'pop("#ko", {a}); pop("#ko-t", {a} + 0.3); zaehl("#ko-z", 0, 2000, {a} + 0.4, 0.9, " €");'),
    (cap("s2", 2), st("s3"),
     t("re-q", 'Wo ist der<br/><span class="box">REST?</span>', 480, 130) + t("re-z", "−1.600 €", 900, 120, "glow-r"),
     lambda a, d: f'slam("#re-q", {a}); shake("#re-q", {a} + 0.3); pop("#re-z", {a} + 0.5);'),
    (st("s3"), cap("s3", 2),
     t("so-z", "−600 €", 500, 220, "glow-r") + chip("so-c", "Chef → Sozialkassen", ROT, 800, 64),
     lambda a, d: f'slam("#so-z", {a}); pop("#so-c", {cap("s3", 1)});'),
    (cap("s3", 2), st("s4"),
     t("ni-a", "siehst du", 500, 100) + t("ni-b", '<span class="box">NIE</span>', 650, 200) + t("ni-c", "auf deinem Zettel", 940, 70),
     lambda a, d: f'pop("#ni-a", {a}); slam("#ni-b", {a} + 0.15); pop("#ni-c", {a} + 0.5);'),
    (st("s4"), cap("s4", 1),
     t("br-k", "Brutto", 500, 110, "glow-o") + t("br-z", "3.000 €", 660, 220),
     lambda a, d: f'pop("#br-k", {a}); slam("#br-z", {a} + 0.3);'),
    (cap("s4", 1), st("s5"),
     AMT + t("lst-z", "−320 €", 830, 190, "glow-r") + chip("lst-c", "Lohnsteuer", ROT, 1060, 60),
     lambda a, d: f'pop("#st-a", {a}); slam("#lst-z", {a} + 0.3); shake("#lst-z", {a} + 0.6); pop("#lst-c", {cap("s4", 2)});'),
    (st("s5"), st("s6"),
     SANDUHR + t("re2-z", "−279 €", 870, 190, "glow-r") + chip("re2-c", "Rente", BLAU, 1100, 60),
     lambda a, d: (f'pop("#re-s", {a}); tl.fromTo("#re-o", {{ scaleY: 1, transformOrigin: "50% 100%" }}, {{ scaleY: 0.3, duration: 2.4 }}, {a});'
                   f' tl.fromTo("#re-u", {{ scaleY: 0.3, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 2.4 }}, {a}); slam("#re2-z", {cap("s5", 1)} - 0.4); pop("#re2-c", {cap("s5", 1)});')),
    (st("s6"), cap("s6", 1),
     KREUZ + t("kv-z", "−262 €", 780, 190, "glow-r") + chip("kv-c", "Krankenkasse", BLAU, 1010, 60),
     lambda a, d: f'tl.fromTo("#kv-k", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(1.8)" }}, {a}); slam("#kv-z", {a} + 0.4); pop("#kv-c", {a} + 0.7);'),
    (cap("s6", 1), st("s7"),
     t("pa-t", "dazu noch", 480, 90, "glow-o") + chip("pa-1", "Pflege −72 €", ROT, 650, 80) + chip("pa-2", "Arbeitslosenvers. −39 €", ROT, 830, 64),
     lambda a, d: f'pop("#pa-t", {a}); slam("#pa-1", {a} + 0.1); slam("#pa-2", {cap("s6", 2)});'),
    (st("s7"), cap("s7", 1),
     balken("bc", 160, 560, OR, "Chef zahlt", "3.600 €") + balken("bk", 660, 315, GRUEN, "Du bekommst", "2.028 €"),
     lambda a, d: (f'tl.fromTo("#bc", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {a}); pop("#bc-t", {a} + 0.4);'
                   f' tl.fromTo("#bk", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {a} + 0.5); pop("#bk-t", {a} + 0.9);')),
    (cap("s7", 1), st("s8"),
     t("ha-a", "nur", 470, 100) + t("ha-z", "56 %", 600, 280, "glow-g") + t("ha-t", "von dem, was du kostest", 930, 64) + partikel("ha-p", 540, 740, 30, (GRUEN, "#fff", OR), 600),
     lambda a, d: f'pop("#ha-a", {a}); slam("#ha-z", {a} + 0.15); burst("#ha-p", {a} + 0.4); shake("#ha-z", {a} + 0.45); pop("#ha-t", {a} + 0.6);'),
    (st("s8"), st("sF"), teilen_html, teilen_js),
    (st("sF"), DAUER, outro_html, outro_js),
]

SFX = [(0.0, "boom"), (cap("s1", 1), "kasse"), (st("s2"), "whoosh"), (st("s2") + 0.4, "tick"), (st("s2") + 0.6, "tick"), (st("s2") + 0.8, "tick"),
       (cap("s2", 2), "boom"), (st("s3"), "whoosh"), (cap("s3", 2), "whoosh"), (cap("s3", 2) + 0.15, "boom"),
       (st("s4"), "whoosh"), (cap("s4", 1), "whoosh"), (cap("s4", 1) + 0.3, "boom"), (st("s5"), "whoosh"), (cap("s5", 1) - 0.4, "pop"),
       (st("s6"), "whoosh"), (st("s6") + 0.4, "pop"), (cap("s6", 1), "whoosh"), (cap("s6", 1) + 0.1, "pop"), (cap("s6", 2), "pop"),
       (st("s7"), "whoosh"), (st("s7") + 0.5, "whoosh"), (cap("s7", 1), "boom"), (cap("s7", 1) + 0.15, "ding"),
       (st("s8"), "whoosh"), (st("sF"), "whoosh"), (st("sF") + 0.6, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
