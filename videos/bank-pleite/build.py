#!/usr/bin/env python3
"""HundeFinanzTV Short (Dark Glow): Was passiert, wenn deine Bank pleite geht? (Teilen-CTA)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GRUEN, OR, ROT, TEILEN_SVG, build, chip, cta_szene, outro_szene, ring, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)


def bank(id_, x, y, w, farbe=OR):
    return (f'<svg id="{id_}" viewBox="0 0 200 180" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w * 0.9}px;overflow:visible;'
            f'filter:drop-shadow(0 0 24px {farbe});z-index:2"><path d="M10 60 L100 10 L190 60 Z" fill="none" stroke="{farbe}" stroke-width="8" stroke-linejoin="round"/>'
            + "".join(f'<rect x="{30 + i * 38}" y="72" width="16" height="70" rx="4" fill="{farbe}"/>' for i in range(4))
            + f'<rect x="10" y="150" width="180" height="16" rx="6" fill="{farbe}"/><text x="100" y="52" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="30" fill="{farbe}">€</text></svg>')


STEMPEL = (f'<div id="hk-s" style="position:absolute;left:0;top:760px;width:1080px;display:flex;justify-content:center;z-index:3">'
           f'<span style="padding:10px 40px;border:10px solid {ROT};border-radius:20px;color:{ROT};font-weight:900;font-size:110px;box-shadow:0 0 50px {ROT}88">PLEITE</span></div>')
CHECK = '<svg viewBox="0 0 100 100" style="width:56px;height:56px"><path d="M20 52 L42 72 L82 30" fill="none" stroke="#111" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>'
KONTEN = "".join(f'<div class="ko" style="display:flex;align-items:center;gap:24px;padding:22px 40px;border-radius:26px;background:#16191b;border:5px solid {GRUEN};'
                 f'box-shadow:0 0 36px {GRUEN}55"><div style="width:84px;height:84px;border-radius:50%;background:{GRUEN};display:flex;align-items:center;justify-content:center">{CHECK}</div>'
                 f'<span style="font-weight:900;font-size:68px;color:#fff">{k}</span></div>' for k in ["Girokonto", "Tagesgeld", "Festgeld"])
KURVE = (f'<svg viewBox="0 0 800 360" style="position:absolute;left:140px;top:500px;width:800px;height:320px;overflow:visible;z-index:2">'
         f'<path id="dp-l" d="M10 330 L150 280 L260 300 L400 190 L520 220 L680 90 L790 40" fill="none" stroke="{GRUEN}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" filter="drop-shadow(0 0 14px {GRUEN})"/></svg>')

teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick's jemandem,<br/>der das wissen muss!")
outro_html, outro_js = outro_szene(BEAGLE)

SZENEN = [
    (0.0, st("s2"),
     bank("hk-b", 290, 390, 500) + STEMPEL + t("hk-t", 'Dein Geld <span class="box">WEG?</span>', 1010, 96),
     lambda a, d: f'tl.fromTo("#hk-b", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.4 }}, {a}); slam("#hk-s", {cap("s1", 1)}); shake("#hk-b", {cap("s1", 1)} + 0.3);'),
    (st("s2"), cap("s2", 1),
     t("np-t", "Keine Panik!", 620, 128, "glow-g"),
     lambda a, d: f'slam("#np-t", {a});'),
    (cap("s2", 1), st("s3"),
     ring("ab-r", f'<div id="ab-z" style="font-weight:900;font-size:96px;line-height:1;white-space:nowrap;color:#fff;text-shadow:0 0 40px {GRUEN}">0 €</div>'
                  f'<div style="font-weight:900;font-size:50px;color:{GRUEN}">GESCHÜTZT</div>', 240, 410, 600, GRUEN) +
     t("ab-t", "pro Bank · EU-Gesetz", 1040, 64),
     lambda a, d: f'pop("#ab-r", {a}); zaehl("#ab-z", 0, 100000, {a} + 0.2, 1.2, " €"); pop("#ab-t", {cap("s2", 2)});'),
    (st("s3"), st("s4"),
     f'<div style="position:absolute;left:0;top:380px;width:1080px;display:flex;flex-direction:column;align-items:center;gap:40px;z-index:2">{KONTEN}</div>',
     lambda a, d: f'tl.fromTo(".ko", {{ x: -700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, stagger: 0.55, ease: "back.out(1.4)" }}, {a});'),
    (st("s4"), st("s5"),
     t("da-z", "> 100.000 €", 520, 150, "glow-r") + t("da-t", "nicht gesetzlich<br/>abgesichert", 760, 90),
     lambda a, d: f'slam("#da-z", {a}); shake("#da-z", {a} + 0.35); pop("#da-t", {cap("s4", 1)});'),
    (st("s5"), st("s6"),
     t("dp-q", "Dein Depot?", 380, 100, "glow-o") + KURVE + t("dp-t", 'gehört <span class="box">DIR</span>', 860, 130),
     lambda a, d: f'pop("#dp-q", {a}); draw("#dp-l", {a} + 0.4, 1.4); slam("#dp-t", {cap("s5", 1)});'),
    (st("s6"), st("s7"),
     t("vb-z", "100.000 € +", 400, 110, "glow-o") +
     bank("vb-1", 60, 640, 280) + bank("vb-2", 400, 640, 280, GRUEN) + bank("vb-3", 740, 640, 280, "#4d8ff0") +
     t("vb-t", "auf mehrere Banken", 1000, 76),
     lambda a, d: f'pop("#vb-z", {a}); pop("#vb-1", {cap("s6", 1)}); pop("#vb-2", {cap("s6", 1)} + 0.2); pop("#vb-3", {cap("s6", 1)} + 0.4); pop("#vb-t", {cap("s6", 1)} + 0.6);'),
    (st("s7"), st("sF"), teilen_html, teilen_js),
    (st("sF"), DAUER, outro_html, outro_js),
]

SFX = [(0.0, "boom"), (cap("s1", 1), "boom"), (st("s2"), "whoosh"), (st("s2") + 0.1, "pop"), (cap("s2", 1), "whoosh"), (cap("s2", 1) + 1.4, "ding"),
       (st("s3"), "whoosh"), (st("s3") + 0.3, "pop"), (st("s3") + 0.85, "pop"), (st("s3") + 1.4, "pop"),
       (st("s4"), "boom"), (st("s5"), "whoosh"), (cap("s5", 1), "pop"), (st("s6"), "whoosh"),
       (cap("s6", 1), "pop"), (cap("s6", 1) + 0.2, "pop"), (cap("s6", 1) + 0.4, "pop"), (st("s7"), "whoosh"), (st("sF"), "whoosh"), (st("sF") + 0.6, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
