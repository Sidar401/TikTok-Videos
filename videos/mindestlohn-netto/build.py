#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow): Mindestlohn 14,60 € – was bleibt netto? (Teilen-CTA Mitte)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import GOLD, GRUEN, OR, ROT, TEILEN_SVG, build, chip, cta_szene, handy, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

UHR = (f'<svg id="uh" viewBox="0 0 200 200" style="position:absolute;left:340px;top:440px;width:400px;height:400px;z-index:2">'
       f'<circle cx="100" cy="100" r="88" fill="#16191b" stroke="{OR}" stroke-width="12" filter="drop-shadow(0 0 20px {OR})"/>'
       f'<rect id="uh-m" x="96" y="30" width="8" height="74" rx="4" fill="#fff"/><rect id="uh-h" x="95" y="55" width="10" height="50" rx="5" fill="{OR}"/>'
       f'<circle cx="100" cy="100" r="9" fill="#fff"/></svg>')
KONTO = handy("ko", 380, 440, 320,
              '<div style="font-weight:800;font-size:30px;color:#ffffffaa">Netto mehr</div>'
              f'<div id="ko-z" style="font-weight:900;font-size:76px;color:{GRUEN};white-space:nowrap">+80 €</div>'
              '<div style="font-weight:800;font-size:24px;color:#ffffff77">pro Monat · StKl 1</div>')

teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick das jemandem<br/>mit Mindestlohn!")

SZENEN = [
    (0.0, st("s2"), chip("hk-c", "ab Januar", OR, 440, 64) + t("hk-z", "14,60 €", 600, 230, "glow-g") + t("hk-u", "Mindestlohn", 890, 90),
     lambda a, d: f'pop("#hk-c", {a}); tl.fromTo("#hk-z", {{ scale: 1.2 }}, {{ scale: 1, duration: 0.35 }}, {a}); pop("#hk-u", {a} + 0.3);'),
    (st("s2"), st("s3"), t("fr-t", 'Was landet<br/><span class="box">WIRKLICH</span><br/>auf dem Konto?', 520, 110),
     lambda a, d: f'slam("#fr-t", {a}); shake("#fr-t", {a} + 0.4);'),
    (st("s3"), st("s4"), t("fo-t", "Folge", 520, 110) + t("fo-n", "HundeFinanzTv", 660, 110, "glow-o") + chip("fo-f", "+ Folgen", OR, 880, 90),
     lambda a, d: f'pop("#fo-t", {a}); pop("#fo-n", {a} + 0.2); slam("#fo-f", {a} + 0.5);'),
    (st("s4"), st("s5"), UHR + t("st-a", "13,90 € → 14,60 €", 900, 90) + chip("st-c", "+70 Cent pro Stunde", GRUEN, 1050, 70),
     lambda a, d: (f'pop("#uh", {a}); tl.fromTo("#uh-m", {{ rotation: 0, transformOrigin: "50% 94%" }}, {{ rotation: 720, duration: 3, ease: "power1.inOut" }}, {a});'
                   f' pop("#st-a", {a} + 0.3); slam("#st-c", {cap("s4", 1)});')),
    (st("s5"), st("s6"), chip("br-c", "Vollzeit · brutto", OR, 460, 64) + t("br-z", "+120 €", 620, 230, "glow-o") + t("br-u", "pro Monat", 900, 80),
     lambda a, d: f'pop("#br-c", {a}); slam("#br-z", {cap("s5", 1)}); pop("#br-u", {cap("s5", 1)} + 0.4);'),
    (st("s6"), st("s7"), KONTO + chip("nt-c", "nach Steuern & Abgaben", ROT, 1080, 56),
     lambda a, d: f'pop("#ko", {a}); pop("#nt-c", {a} + 0.4); zaehl("#ko-z", 0, 80, {cap("s6", 2)}, 0.8, " €"); tl.set("#ko-z", {{ opacity: 1 }}, {a});'),
    (st("s7"), st("s8"), teilen_html, teilen_js),
    (st("s8"), st("s9"), chip("mj-c", "Minijob-Grenze", OR, 460, 70) + t("mj-z", "633 €", 620, 230, "glow-g") + t("mj-u", "statt 603 €", 900, 80),
     lambda a, d: f'pop("#mj-c", {a}); slam("#mj-z", {cap("s8", 2)}); pop("#mj-u", {cap("s8", 2)} + 0.4);'),
    (st("s9"), DAUER, t("h-z", "≈ 43 Std.", 600, 200, "glow-o") + t("h-u", "pro Monat – wie bisher", 880, 70),
     lambda a, d: f'slam("#h-z", {cap("s9", 1)}); pop("#h-u", {cap("s9", 1)} + 0.4);'),
]
SZENEN[5] = (SZENEN[5][0], SZENEN[5][1], SZENEN[5][2].replace(">+80 €<", ">+0 €<"), SZENEN[5][3])

SFX = ([(0.0, "boom"), (0.1, "kasse"), (st("s2"), "whoosh"), (st("s2") + 0.1, "boom"), (st("s3"), "whoosh"), (st("s3") + 0.5, "pop"), (st("s4"), "whoosh")]
       + [(st("s4") + i * 0.3, "tick") for i in range(8)] + [(cap("s4", 1), "ding"), (st("s5"), "whoosh"), (cap("s5", 1), "kasse"), (st("s6"), "whoosh"),
                                                              (cap("s6", 2) + 0.8, "ding"), (st("s7"), "whoosh"), (st("s8"), "whoosh"), (cap("s8", 2), "pop"), (st("s9"), "whoosh"), (cap("s9", 1), "boom")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
