#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow): Die Bank zieht dir Steuern ab – Freistellungsauftrag (Kommentar-CTA)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, cta_szene, handy, outro_szene, partikel, t, zeiten  # noqa: E402
from thumbs import muenzen  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)


def muenze(id_, x, y, d=110):
    return (f'<div id="{id_}" class="mz" style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;z-index:3;'
            f'background:radial-gradient(circle at 35% 30%, #fff3b0 0%, {GOLD} 40%, #c98a00 100%);border:5px solid #b47c00;box-shadow:0 0 24px {GOLD}88;'
            f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:{d * 0.45:.0f}px;color:#8a5a00">€</div>')


MAGNET = (f'<svg id="hk-m" viewBox="0 0 300 260" style="position:absolute;left:360px;top:690px;width:360px;height:312px;overflow:visible;z-index:2">'
          f'<path d="M50 20 L50 130 A100 100 0 0 0 250 130 L250 20" fill="none" stroke="{ROT}" stroke-width="70" filter="drop-shadow(0 0 24px {ROT})"/>'
          f'<rect x="15" y="0" width="70" height="44" fill="#c9d0d4"/><rect x="215" y="0" width="70" height="44" fill="#c9d0d4"/>'
          f'<text x="150" y="150" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="46" fill="#fff">BANK</text></svg>')
MUENZEN_HK = "".join(muenze(f"hm{i}", 150 + i * 160, 1150 - (i % 2) * 40) for i in range(5))

R, U = 200, 2 * 3.14159 * 200
TORTE = (f'<svg viewBox="0 0 500 500" style="position:absolute;left:290px;top:470px;width:500px;height:500px;overflow:visible;z-index:2">'
         f'<circle cx="250" cy="250" r="{R}" fill="none" stroke="{GRUEN}" stroke-width="110" filter="drop-shadow(0 0 18px {GRUEN})"/>'
         f'<circle id="tt-r" cx="250" cy="250" r="{R}" fill="none" stroke="{ROT}" stroke-width="120" stroke-dasharray="{U * 0.264:.1f} {U:.1f}" '
         f'transform="rotate(-90 250 250)" filter="drop-shadow(0 0 22px {ROT})"/>'
         f'<text x="250" y="240" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="48" fill="#fff">Zinsen &amp;</text>'
         f'<text x="250" y="295" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="48" fill="#fff">ETF-Gewinne</text></svg>')

SCHILD = (f'<svg id="fr-s" viewBox="0 0 300 340" style="position:absolute;left:330px;top:440px;width:420px;height:476px;overflow:visible;z-index:2">'
          f'<path d="M150 10 L280 60 L280 170 C280 250 220 300 150 330 C80 300 20 250 20 170 L20 60 Z" fill="#16191b" stroke="{GRUEN}" stroke-width="16" '
          f'filter="drop-shadow(0 0 30px {GRUEN})"/>'
          f'<text x="150" y="185" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="54" fill="{GRUEN}">1.000 €</text>'
          f'<text x="150" y="235" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#fff">steuerfrei</text></svg>')

CHECK = (f'<svg id="ap-c" viewBox="0 0 100 100" style="width:150px;height:150px"><circle cx="50" cy="50" r="46" fill="{GRUEN}"/>'
         f'<path id="ap-h" d="M28 52 L44 68 L74 36" fill="none" stroke="#111" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')
APP = handy("ap", 380, 440, 320,
            f'<div style="font-weight:900;font-size:34px;color:#fff;text-align:center;line-height:1.15">Freistellungs-<br/>auftrag</div>{CHECK}'
            f'<div style="font-weight:800;font-size:26px;color:#ffffffaa;text-align:center">1.000 €<br/>eingetragen</div>')
UHR = (f'<svg viewBox="0 0 200 200" style="position:absolute;left:760px;top:430px;width:200px;height:200px;z-index:3">'
       f'<circle cx="100" cy="100" r="80" fill="#16191b" stroke="#ffffff22" stroke-width="16"/>'
       f'<circle id="uh-r" cx="100" cy="100" r="80" fill="none" stroke="{OR}" stroke-width="16" stroke-linecap="round" transform="rotate(-90 100 100)"/>'
       f'<text x="100" y="115" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="46" fill="#fff">2 Min</text></svg>')

frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Hast du schon einen?")
outro_html, outro_js = outro_szene(BEAGLE)

SZENEN = [
    (0.0, st("s2"),
     t("hk-t", 'Deine Bank zieht dir<br/><span class="box">STEUERN</span> ab', 420, 80) + MAGNET + MUENZEN_HK,
     lambda a, d: (f'tl.fromTo("#hk-t", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.35 }}, {a}); shake("#hk-m", {a} + 0.4);'
                   + "".join(f' tl.fromTo("#hm{i}", {{ x: 0, y: 0, rotation: 0 }}, {{ x: {540 - 55 - (150 + i * 160)}, y: {890 - (1150 - (i % 2) * 40)}, rotation: 360, scale: 0.5, duration: 0.45, ease: "power3.in" }}, {a} + {0.6 + i * 0.45:.2f});' for i in range(5))
                   + f' tl.fromTo("#hk-m", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.12, yoyo: true, repeat: 15 }}, {a} + 0.9);')),
    (st("s2"), cap("s2", 2),
     TORTE + chip("tt-c", "automatisch abgezogen", ROT, 1040, 56),
     lambda a, d: f'tl.fromTo("#tt-r", {{ strokeDashoffset: {U * 0.264:.1f} }}, {{ strokeDashoffset: 0, duration: 0.8, ease: "power2.out" }}, {a} + 0.6); pop("#tt-c", {cap("s2", 1)});'),
    (cap("s2", 2), st("s3"),
     t("pz-z", "26 %", 520, 300, "glow-r") + t("pz-t", "ans Finanzamt", 900, 90),
     lambda a, d: f'slam("#pz-z", {a}); shake("#pz-z", {a} + 0.3); pop("#pz-t", {a} + 0.4);'),
    (st("s3"), cap("s3", 2),
     SCHILD + chip("fr-c", "pro Jahr", GRUEN, 970, 60) + partikel("fr-p", 540, 680, 26, (GRUEN, "#fff", GOLD), 560),
     lambda a, d: f'tl.fromTo("#fr-s", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }}, {a}); burst("#fr-p", {a} + 0.3); pop("#fr-c", {cap("s3", 1)});'),
    (cap("s3", 2), st("s4"),
     t("nu-a", "aber NUR mit", 500, 96) + t("nu-b", '<span class="box">Freistellungs-<br/>auftrag</span>', 680, 104),
     lambda a, d: f'pop("#nu-a", {a}); slam("#nu-b", {cap("s3", 3)} - 0.1);'),
    (st("s4"), st("s5"),
     chip("jo-c", "Beispiel: Jonas", OR, 470, 60) + t("jo-z", "+500 €", 640, 200, "glow-g") + t("jo-t", "Zinsen im Jahr", 900, 80) + muenzen(780, 980, 5, 150),
     lambda a, d: f'pop("#jo-c", {a}); pop("#jo-z", {a} + 0.2); zaehl("#jo-z", 0, 500, {a} + 0.2, 1.0, " €"); pop("#jo-t", {cap("s4", 1)});'),
    (st("s5"), st("s6"),
     t("we-k", "ohne Auftrag", 470, 90, "glow-o") + t("we-z", "−130 €", 620, 230, "glow-r") + t("we-t", "einfach weg", 940, 90) +
     "".join(muenze(f"wm{i}", 230 + i * 160, 1080, 100) for i in range(4)),
     lambda a, d: (f'pop("#we-k", {a}); slam("#we-z", {cap("s5", 1)}); shake("#we-z", {cap("s5", 1)} + 0.3); pop("#we-t", {cap("s5", 1)} + 0.5);'
                   + "".join(f' tl.fromTo("#wm{i}", {{ y: 0, opacity: 1, rotation: 0 }}, {{ y: 500, opacity: 0, rotation: {(-1) ** i * 90}, duration: 0.6, ease: "power2.in" }}, {cap("s5", 1)} + {0.3 + i * 0.12:.2f});' for i in range(4)))),
    (st("s6"), st("s7"),
     APP + UHR,
     lambda a, d: (f'pop("#ap", {a}); tl.fromTo("#ap-c", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, {a} + 0.6); draw("#ap-h", {a} + 0.75, 0.3);'
                   f' draw("#uh-r", {a} + 0.3, 2.2);')),
    (st("s7"), st("s8"), frage_html, frage_js),
    (st("s8"), DAUER, outro_html, outro_js),
]

SFX = ([(0.0, "boom"), (0.4, "whoosh")] + [(0.6 + i * 0.45 + 0.4, "pop") for i in range(5)] +
       [(st("s2"), "whoosh"), (st("s2") + 0.6, "tick"), (st("s2") + 0.8, "tick"), (st("s2") + 1.0, "tick"), (cap("s2", 2), "boom"),
        (st("s3"), "whoosh"), (st("s3") + 0.3, "ding"), (cap("s3", 2), "whoosh"), (cap("s3", 3) - 0.1, "boom"),
        (st("s4"), "whoosh"), (st("s4") + 1.2, "kasse"), (st("s5"), "whoosh"), (cap("s5", 1), "boom"),
        (st("s6"), "whoosh"), (st("s6") + 0.75, "ding"), (st("s7"), "whoosh"), (st("s8"), "whoosh"), (st("s8") + 0.6, "pop")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
