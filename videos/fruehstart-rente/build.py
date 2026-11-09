#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (Dark Glow): Frühstart-Rente – was aus 10 € pro Kind wird → verweist auf YouTube-Longform „Das ändert sich 2027“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import GOLD, GRUEN, OR, build, chip, partikel, t, zeiten  # noqa: E402
from motor import endkarte  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

KIND = (f'<svg id="ki" viewBox="0 0 200 260" style="position:absolute;left:400px;top:430px;width:280px;height:364px;z-index:2">'
        f'<g filter="drop-shadow(0 0 22px {GRUEN})"><circle cx="100" cy="64" r="50" fill="{GRUEN}"/><path d="M30 250 C30 140 170 140 170 250 Z" fill="{GRUEN}"/></g>'
        f'<circle cx="82" cy="60" r="7" fill="#111"/><circle cx="118" cy="60" r="7" fill="#111"/><path d="M84 82 Q100 94 116 82" fill="none" stroke="#111" stroke-width="5"/></svg>')
SPAR = "".join(f'<div class="sp" style="position:absolute;left:{150 + (i % 6) * 135}px;top:{520 + (i // 6) * 110}px;width:110px;height:80px;border-radius:14px;'
               f'background:#16191b;border:4px solid {GOLD};box-shadow:0 0 18px {GOLD}55;display:flex;align-items:center;justify-content:center;'
               f'font-weight:900;font-size:34px;color:{GOLD};z-index:2">{6 + i}</div>' for i in range(12))
KURVE = (f'<svg viewBox="0 0 800 480" style="position:absolute;left:140px;top:500px;width:800px;height:480px;overflow:visible;z-index:2">'
         f'<path d="M10 470 L790 470" stroke="#ffffff33" stroke-width="4"/>'
         f'<path id="kv" d="M10 460 C300 455 520 420 650 300 C720 230 760 130 790 20" fill="none" stroke="{GRUEN}" stroke-width="14" stroke-linecap="round" filter="drop-shadow(0 0 16px {GRUEN})"/>'
         f'<text x="20" y="440" font-family="Montserrat" font-weight="900" font-size="34" fill="#fff">18</text>'
         f'<text x="740" y="440" font-family="Montserrat" font-weight="900" font-size="34" fill="#fff">67</text></svg>')

mk_html, mk_js = endkarte("assets/lf.jpg", "Ganzes Video")

SZENEN = [
    (0.0, st("s2"), KIND + t("hk-z", "10 €", 820, 200, "glow-g") + t("hk-u", "pro Kind · pro Monat", 1060, 64),
     lambda a, d: f'pop("#ki", {a}); tl.fromTo("#hk-z", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.35 }}, {a}); pop("#hk-u", {cap("s1", 2)});'),
    (st("s2"), st("s3"), t("rn-t", 'Wenig?<br/><span class="box">Rechnen wir!</span>', 560, 130),
     lambda a, d: f'slam("#rn-t", {a}); shake("#rn-t", {a} + 0.35);'),
    (st("s3"), st("s4"), chip("fr-c", "Frühstart-Rente", OR, 380, 70) + SPAR + t("fr-u", "Alter 6 bis 18 = 12 Jahre", 900, 64),
     lambda a, d: f'pop("#fr-c", {a}); tl.fromTo(".sp", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.12, ease: "back.out(2)" }}, {cap("s3", 1)}); pop("#fr-u", {cap("s3", 2)});'),
    (st("s4"), st("s5"), t("su-a", "eingezahlt", 500, 100) + t("su-z", "0 €", 650, 220, "glow-o"),
     lambda a, d: f'pop("#su-a", {a}); pop("#su-z", {a} + 0.2); zaehl("#su-z", 0, 1440, {cap("s4", 1)}, 0.9, " €");'),
    (st("s5"), st("s6"), chip("r6-c", "mit 6 % Rendite", GRUEN, 430, 70) + t("r6-z", "≈ 2.100 €", 590, 200, "glow-g") + t("r6-u", "mit 18 Jahren", 860, 80),
     lambda a, d: f'pop("#r6-c", {a}); slam("#r6-z", {cap("s5", 1)}); pop("#r6-u", {cap("s5", 1)} + 0.4);'),
    (st("s6"), st("s7"), KURVE + t("rz-z", "> 30.000 €", 1020, 150, "glow-g") + partikel("rz-p", 540, 1100, 30, (GRUEN, GOLD, "#fff"), 560),
     lambda a, d: f'draw("#kv", {a}, 2.4); slam("#rz-z", {cap("s6", 4)}); burst("#rz-p", {cap("s6", 4)} + 0.25);'),
    (st("s7"), st("s8"), t("el-a", "Eltern legen dazu?", 520, 96, "glow-o") + t("el-z", "noch viel mehr", 700, 130, "glow-g"),
     lambda a, d: f'pop("#el-a", {a}); slam("#el-z", {cap("s7", 2)});'),
    (st("s8"), DAUER, mk_html, mk_js),
]

SFX = [(0.0, "boom"), (0.1, "kasse"), (st("s2"), "whoosh"), (st("s2") + 0.05, "boom"), (st("s3"), "whoosh")] + \
      [(cap("s3", 1) + i * 0.12, "tick") for i in range(12)] + \
      [(st("s4"), "whoosh"), (cap("s4", 1) + 0.9, "ding"), (st("s5"), "whoosh"), (cap("s5", 1), "kasse"), (st("s6"), "whoosh"),
       (cap("s6", 4), "boom"), (st("s7"), "whoosh"), (cap("s7", 2), "pop"), (st("s8"), "whoosh"), (st("s8") + 0.3, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
