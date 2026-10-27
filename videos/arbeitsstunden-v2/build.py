#!/usr/bin/env python3
"""HundeFinanzTV Short im neuen Stil „Dark Glow“ (Probe): Wie lange musst du dafür arbeiten? – 27 s, Voice aus videos/arbeitsstunden."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GRUEN, OR, ROT, build, chip, handy, ring, t  # noqa: E402

UHR = (f'<svg viewBox="0 0 100 100" style="width:62%;height:62%"><circle cx="50" cy="50" r="44" fill="none" stroke="#fff" stroke-width="6"/>'
       f'<line id="uz-g" x1="50" y1="50" x2="50" y2="16" stroke="{OR}" stroke-width="7" stroke-linecap="round"/>'
       f'<line x1="50" y1="50" x2="72" y2="50" stroke="#fff" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="50" r="6" fill="{OR}"/></svg>')
TEILEN = (f'<svg viewBox="0 0 100 100" style="width:60%;height:60%"><path d="M22 74 Q26 40 58 38 L58 22 L84 48 L58 74 L58 58 Q36 57 22 74 Z" fill="{OR}"/></svg>')
TAGE = "".join(f'<div class="tg" style="width:150px;height:150px;border-radius:26px;background:#16191b;border:5px solid {OR};box-shadow:0 0 30px {OR}66;'
               f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:48px;color:#fff">{d}</div>' for d in ["Mo", "Di", "Mi", "Do", "Fr"] * 2)

SZENEN = [
    # Hook: Frame 0 schon voll
    (0.0, 1.98,
     handy("hk-h", 360, 330, 360, f'<div style="font-weight:900;font-size:86px;white-space:nowrap;color:#fff;text-shadow:0 0 40px {OR}">1.000 €</div>') +
     t("hk-t", 'Wie lange musst du<br/><span class="box">DAFÜR</span> arbeiten?', 1060, 84),
     lambda a, d: f'tl.fromTo("#hk-h", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.4, ease: "power3.out" }}, {a}); shake("#hk-h", {a} + 1.0);'),

    (1.98, 3.99,
     t("bs-t", "Beispiel:", 520, 90, "glow-o") + t("bs-u", "DU", 650, 300),
     lambda a, d: f'slam("#bs-t", {a}); slam("#bs-u", {a} + 0.35);'),

    (3.99, 6.27,
     t("ge-z", "0 €", 560, 210, "glow-g") + t("ge-s", "netto im Monat", 820, 70),
     lambda a, d: f'pop("#ge-z", {a}); zaehl("#ge-z", 0, 2000, {a}, 0.9, " €"); pop("#ge-s", {a} + 0.6);'),

    (6.27, 8.25,
     ring("st-r", UHR, 290, 400, 500) + t("st-z", "160 Std.", 980, 130, "glow-o"),
     lambda a, d: f'pop("#st-r", {a}); tl.fromTo("#uz-g", {{ rotation: 0 }}, {{ rotation: 720, svgOrigin: "50 50", duration: {d}, ease: "power1.inOut" }}, {a}); slam("#st-z", {a} + 0.5);'),

    (8.25, 10.01,
     t("fo-a", "2.000 €", 480, 150) + t("fo-b", "÷ 160 Std.", 680, 120, "glow-o"),
     lambda a, d: f'pop("#fo-a", {a}); pop("#fo-b", {a} + 0.5);'),

    (10.01, 11.48,
     t("lo-z", "12,50 €", 520, 220, "glow-g") + t("lo-s", "pro Stunde", 800, 80),
     lambda a, d: f'slam("#lo-z", {a}); pop("#lo-s", {a} + 0.4);'),

    (11.48, 12.43,
     handy("nh-h", 360, 360, 360, '<div style="font-weight:900;font-size:56px;color:#fff">NEU</div>'),
     lambda a, d: f'tl.fromTo("#nh-h", {{ y: 600, rotation: -20 }}, {{ y: 0, rotation: 0, duration: 0.4, ease: "back.out(1.6)" }}, {a});'),

    (12.43, 14.24,
     handy("pr-h", 360, 330, 360) + chip("pr-p", "1.000 €", ROT, 860, 120),
     lambda a, d: f'pop("#pr-h", {a}); slam("#pr-p", {a} + 0.6); shake("#pr-p", {a} + 0.9);'),

    (14.24, 15.97,
     ring("ar-r", f'<div id="ar-z" style="font-weight:900;font-size:190px;line-height:1;color:#fff;text-shadow:0 0 40px {OR}">80</div>'
                  f'<div style="font-weight:900;font-size:60px;color:{OR}">STUNDEN</div>', 240, 380, 600) +
     t("ar-t", "ARBEIT", 1040, 120, "glow-r"),
     lambda a, d: f'slam("#ar-r", {a}); zaehl("#ar-z", 0, 80, {a} + 0.1, 0.8, ""); shake("#ar-r", {a} + 0.95); pop("#ar-t", {a} + 0.7);'),

    (15.97, 17.77,
     f'<div id="wo-g" style="position:absolute;left:60px;top:430px;width:960px;display:grid;grid-template-columns:repeat(5,150px);gap:28px 52px;justify-content:center">{TAGE}</div>' +
     t("wo-t", '= <span class="box">2 WOCHEN</span>', 880, 110),
     lambda a, d: f'tl.fromTo(".tg", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.15, stagger: 0.07, ease: "back.out(2)" }}, {a}); slam("#wo-t", {a} + 0.8);'),

    (17.77, 21.69,
     ring("te-r", TEILEN, 340, 380, 400) + t("te-t", "Schick's jemandem,<br/>der das wissen muss!", 900, 76),
     lambda a, d: f'pop("#te-r", {a}); tl.fromTo("#te-r", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {a} + 0.4); pop("#te-t", {a} + 1.1);'),

    (21.69, 26.848,
     ring("ou-r", f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', 290, 330, 500) +
     t("ou-n", "HundeFinanzTV", 900, 96) + chip("ou-f", "+ Folgen", OR, 1040, 64),
     lambda a, d: f'pop("#ou-r", {a}); pop("#ou-n", {a} + 0.3); slam("#ou-f", {a} + 0.6); tl.fromTo("#ou-f", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.2);'),
]

SFX = [(0.0, "boom"), (1.0, "pop"), (1.98, "whoosh"), (2.33, "pop"), (3.99, "whoosh"), (4.85, "ding"), (6.27, "whoosh")] + \
      [(6.4 + k * 0.18, "tick") for k in range(9)] + \
      [(8.25, "whoosh"), (8.75, "pop"), (10.01, "boom"), (10.3, "ding"), (11.48, "whoosh"), (13.03, "boom"), (14.24, "whoosh"), (14.5, "kasse")] + \
      [(15.97 + k * 0.07, "tick") for k in range(10)] + \
      [(16.77, "boom"), (17.77, "whoosh"), (21.69, "whoosh"), (22.29, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
