#!/usr/bin/env python3
"""HundeFinanzTV Short (Dark Glow): So viel kostet dich Rauchen (Kommentar-CTA)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import BLASE_SVG, GRUEN, OR, ROT, build, chip, cta_szene, outro_szene, ring, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

ZIGARETTE = (f'<svg viewBox="0 0 600 260" style="position:absolute;left:140px;top:420px;width:800px;height:347px;overflow:visible;z-index:2">'
             f'<rect x="40" y="150" width="420" height="60" rx="10" fill="#f2f2f2"/><rect x="40" y="150" width="130" height="60" rx="10" fill="{OR}"/>'
             f'<rect x="455" y="150" width="40" height="60" rx="8" fill="{ROT}" filter="drop-shadow(0 0 24px {ROT})"/>'
             f'<path id="rk-r" d="M480 140 C440 100 520 80 480 40 C450 10 500 -10 470 -40" fill="none" stroke="#ffffff88" stroke-width="16" stroke-linecap="round"/></svg>')
PACK = (f'<div id="pk" style="position:absolute;left:340px;top:360px;width:400px;height:520px;border-radius:30px;background:linear-gradient(160deg,#2a2f33,#16191b);'
        f'border:8px solid {OR};box-shadow:0 0 80px {OR}66;z-index:2;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:50px">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:130px;border-radius:22px 22px 0 0;background:{ROT}"></div>'
        f'<div style="font-weight:900;font-size:60px;color:#fff;letter-spacing:4px">20 STÜCK</div></div>')
KURVE = (f'<svg viewBox="0 0 800 380" style="position:absolute;left:140px;top:380px;width:800px;height:380px;overflow:visible;z-index:2">'
         f'<path d="M10 370 L790 370" stroke="#ffffff33" stroke-width="4"/>'
         f'<path id="iv-l" d="M10 360 C250 340 450 270 790 30" fill="none" stroke="{GRUEN}" stroke-width="14" stroke-linecap="round" filter="drop-shadow(0 0 16px {GRUEN})"/></svg>')

frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Rauchst du – oder<br/>hast du aufgehört?")
outro_html, outro_js = outro_szene(BEAGLE)

SZENEN = [
    (0.0, st("s2"),
     ZIGARETTE + t("hk-t", 'So viel kostet<br/><span class="box">RAUCHEN</span>', 900, 120),
     lambda a, d: f'tl.fromTo("#rk-r", {{ y: 0, opacity: 0.9 }}, {{ y: -40, opacity: 0.2, duration: {d}, ease: "none" }}, {a}); tl.fromTo("#hk-t", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.4 }}, {a});'),
    (st("s2"), st("s3"),
     PACK + chip("pk-p", "≈ 9 €", ROT, 940, 110),
     lambda a, d: f'pop("#pk", {a}); slam("#pk-p", {cap("s2", 0)} + 0.9); shake("#pk-p", {cap("s2", 0)} + 1.2);'),
    (st("s3"), st("s4"),
     t("ja-k", "1 Schachtel × 365 Tage", 460, 66, "glow-o") + t("ja-z", "0 €", 600, 200) + t("ja-s", "pro Jahr", 860, 80),
     lambda a, d: f'pop("#ja-k", {a}); pop("#ja-z", {cap("s3", 2)}); zaehl("#ja-z", 0, 3285, {cap("s3", 2)}, 1.0, " €"); pop("#ja-s", {cap("s3", 2)} + 0.5);'),
    (st("s4"), st("s5"),
     t("zj-k", "10 JAHRE", 420, 120, "glow-o") + t("zj-z", "32.850 €", 640, 190, "glow-r") + t("zj-s", "einfach verraucht", 900, 70),
     lambda a, d: f'pop("#zj-k", {a}); slam("#zj-z", {a} + 0.7); shake("#zj-z", {a} + 1.0); pop("#zj-s", {a} + 1.4);'),
    (st("s5"), st("s6"),
     KURVE + chip("iv-c", "investiert · 7 %", GRUEN, 820, 60) + t("iv-z", "0 €", 960, 170, "glow-g"),
     lambda a, d: f'draw("#iv-l", {a} + 0.2, 2.0); pop("#iv-c", {cap("s5", 2)}); pop("#iv-z", {cap("s5", 3)}); zaehl("#iv-z", 0, 46000, {cap("s5", 3)}, 1.1, " €");'),
    (st("s6"), st("s7"), frage_html, frage_js),
    (st("s7"), DAUER, outro_html, outro_js),
]

SFX = [(0.0, "boom"), (st("s2"), "whoosh"), (cap("s2", 0) + 0.9, "boom"), (st("s3"), "whoosh")] + \
      [(cap("s3", 2) + k * 0.1, "tick") for k in range(10)] + \
      [(cap("s3", 2) + 1.0, "ding"), (st("s4"), "whoosh"), (st("s4") + 0.7, "kasse"), (st("s5"), "whoosh"),
       (cap("s5", 2), "pop"), (cap("s5", 3) + 1.1, "ding"), (st("s6"), "whoosh"), (st("s7"), "whoosh"), (st("s7") + 0.6, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
