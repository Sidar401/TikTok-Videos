#!/usr/bin/env python3
"""HundeFinanzTV Short (Dark Glow): 1 Million – so viel Zinsen pro Tag (Teilen-CTA)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GOLD, GRUEN, OR, TEILEN_SVG, build, chip, cta_szene, outro_szene, t, zeiten  # noqa: E402
from thumbs import buendel, muenzen  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick's jemandem,<br/>der vom Reichsein träumt!")
outro_html, outro_js = outro_szene(BEAGLE)


def icon_chip(id_, txt, y, x):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:22px 44px;border-radius:28px;background:#16191b;border:5px solid {OR};'
            f'box-shadow:0 0 40px {OR}66;font-weight:900;font-size:70px;color:#fff;z-index:2">{txt}</div>')


SZENEN = [
    (0.0, st("s2"),
     t("hk-z", "1.000.000 €", 380, 128) + muenzen(140, 640, 7, 190) + buendel(380, 700, 1.1, 5) + muenzen(760, 660, 6, 170) +
     chip("hk-c", "auf dem Tagesgeld", OR, 1080, 62),
     lambda a, d: f'zaehl("#hk-z", 0, 1000000, {a}, 1.2, " €"); tl.fromTo("#hk-z", {{ scale: 1.2 }}, {{ scale: 1, duration: 0.5 }}, {a}); pop("#hk-c", {cap("s1", 2)});'),
    (st("s2"), st("s3"),
     t("zi-a", "× 2 % Zinsen", 460, 110, "glow-o") + t("zi-b", "= 20.000 €", 680, 170, "glow-g") + t("zi-c", "pro Jahr", 900, 80),
     lambda a, d: f'pop("#zi-a", {a}); slam("#zi-b", {cap("s2", 1)}); pop("#zi-c", {cap("s2", 1)} + 0.4);'),
    (st("s3"), st("s4"),
     t("ta-z", "55 €", 420, 300, "glow-g") + t("ta-s", 'jeden <span class="box">TAG</span>', 790, 120) + t("ta-u", "ohne einen Finger zu rühren", 1000, 56),
     lambda a, d: f'slam("#ta-z", {cap("s3", 1)} - 0.2); pop("#ta-s", {cap("s3", 1)} + 0.3); pop("#ta-u", {cap("s3", 2)});'),
    (st("s4"), st("s5"),
     icon_chip("nt-1", "nachts", 400, 300) + icon_chip("nt-2", "am Wochenende", 600, 190) + icon_chip("nt-3", "im Urlaub", 800, 260) +
     t("nt-z", "+55 €", 1020, 110, "glow-g"),
     lambda a, d: f'pop("#nt-1", {a}); pop("#nt-2", {cap("s4", 1)}); pop("#nt-3", {cap("s4", 1)} + 0.8); pop("#nt-z", {cap("s4", 1)} + 1.2);'),
    (st("s5"), st("s6"),
     t("st-k", "nach Steuern", 440, 100, "glow-o") + t("st-z", "≈ 40 €", 620, 230, "glow-g") + t("st-s", "jeden Tag", 920, 90),
     lambda a, d: f'pop("#st-k", {a}); slam("#st-z", {cap("s5", 1)}); pop("#st-s", {cap("s5", 1)} + 0.4);'),
    (st("s6"), st("s7"), teilen_html, teilen_js),
    (st("s7"), DAUER, outro_html, outro_js),
]

SFX = [(0.0, "boom"), (1.2, "kasse"), (cap("s1", 2), "pop"), (st("s2"), "whoosh"), (cap("s2", 1), "ding"), (st("s3"), "whoosh"), (cap("s3", 1) - 0.2, "boom"),
       (st("s4"), "whoosh"), (cap("s4", 1), "pop"), (cap("s4", 1) + 0.8, "pop"), (cap("s4", 1) + 1.2, "kasse"),
       (st("s5"), "whoosh"), (cap("s5", 1), "ding"), (st("s6"), "whoosh"), (st("s7"), "whoosh"), (st("s7") + 0.6, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
