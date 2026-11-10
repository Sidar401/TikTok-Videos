#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (Dark Glow): Krankenkasse wechseln – rund 130 € im Jahr → verweist auf YouTube-Longform „Das ändert sich 2027“."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, cta_szene, handy, partikel, t, zeiten  # noqa: E402
from motor import endkarte  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
BLAU = "#4d8ff0"

KARTE = (f'<div id="kk" style="position:absolute;left:190px;top:470px;width:700px;height:440px;border-radius:36px;background:linear-gradient(135deg,{BLAU},#2a5bb8);'
         f'box-shadow:0 0 90px {BLAU}88;z-index:2;transform:rotate(-4deg)">'
         f'<div style="position:absolute;left:50px;top:50px;width:120px;height:90px;border-radius:14px;background:{GOLD}"></div>'
         f'<div style="position:absolute;left:50px;top:190px;font-weight:900;font-size:56px;color:#fff">Gesundheitskarte</div>'
         f'<div style="position:absolute;left:50px;top:290px;width:400px;height:22px;border-radius:11px;background:#ffffff55"></div>'
         f'<div style="position:absolute;left:50px;top:340px;width:280px;height:22px;border-radius:11px;background:#ffffff55"></div></div>')


def balken(id_, x, h, f, oben, unten):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{1100 - h}px;width:260px;height:{h}px;border-radius:24px 24px 0 0;background:{f};'
            f'box-shadow:0 0 50px {f}77;transform-origin:50% 100%;z-index:2"></div>'
            f'<div id="{id_}-t" class="t" style="left:{x - 410}px;top:{1100 - h - 130}px;font-size:90px;color:{f}">{oben}</div>'
            f'<div class="t" style="left:{x - 410}px;top:1120px;font-size:46px">{unten}</div>')


frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Wie viel Zusatzbeitrag<br/>zahlst du?")
mk_html, mk_js = endkarte("assets/lf.jpg", "Ganzes Video")

SZENEN = [
    (0.0, st("s2"), KARTE + t("hk-t", 'Zahlst du<br/><span class="box">ZU VIEL?</span>', 1040, 120),
     lambda a, d: f'tl.fromTo("#kk", {{ rotation: -14, scale: 1.15 }}, {{ rotation: -4, scale: 1, duration: 0.45 }}, {a}); slam("#hk-t", {cap("s1", 1)}); shake("#hk-t", {cap("s1", 2)});'),
    (st("s2"), st("s3"), t("zb-a", "Zusatzbeitrag", 500, 110, "glow-o") + t("zb-b", "jede Kasse anders", 690, 90) + chip("zb-c", "riesige Unterschiede", ROT, 880, 70),
     lambda a, d: f'pop("#zb-a", {cap("s2", 0)} + 0.4); pop("#zb-b", {cap("s2", 1)}); slam("#zb-c", {cap("s2", 3)});'),
    (st("s3"), st("s4"), balken("b1", 220, 520, OR, "2,9 %", "Durchschnitt") + balken("b2", 600, 390, GRUEN, "2,2 %", "günstigste"),
     lambda a, d: (f'tl.fromTo("#b1", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {cap("s3", 1)}); pop("#b1-t", {cap("s3", 1)} + 0.4);'
                   f' tl.fromTo("#b2", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {cap("s3", 3)}); pop("#b2-t", {cap("s3", 3)} + 0.4);')),
    (st("s4"), st("s5"), chip("sp-c", "bei 3.000 € brutto", OR, 440, 70) + t("sp-a", "≈ 11 € / Monat", 600, 110) + t("sp-z", "≈ 130 €", 780, 230, "glow-g")
     + t("sp-u", "pro Jahr gespart", 1060, 80) + partikel("sp-p", 540, 900, 28, (GRUEN, GOLD, "#fff"), 520),
     lambda a, d: f'pop("#sp-c", {a}); pop("#sp-a", {cap("s4", 1)}); slam("#sp-z", {cap("s4", 2)}); burst("#sp-p", {cap("s4", 2)} + 0.25); pop("#sp-u", {cap("s4", 2)} + 0.4);'),
    (st("s5"), st("s6"), handy("hy", 380, 440, 320, '<div style="font-weight:900;font-size:40px;color:#fff;text-align:center">Neue Kasse<br/>wählen</div>'
                                              f'<div style="width:120px;height:120px;border-radius:50%;background:{GRUEN};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:80px;color:#111">✓</div>')
     + chip("hy-c", "5 Min online", GRUEN, 1100, 70) + chip("hy-d", "neue Kasse kündigt für dich", OR, 1230, 54),
     lambda a, d: f'pop("#hy", {a}); slam("#hy-c", {cap("s5", 1)}); pop("#hy-d", {cap("s5", 3)});'),
    (st("s6"), st("s7"), t("lg-a", "Leistungen?", 520, 120, "glow-o") + t("lg-b", "fast gleich", 700, 170, "glow-g"),
     lambda a, d: f'pop("#lg-a", {cap("s6", 1)}); slam("#lg-b", {cap("s6", 3)});'),
    (st("s7"), st("s8"), frage_html, frage_js),
    (st("s8"), DAUER, mk_html, mk_js),
]

SFX = [(0.0, "boom"), (cap("s1", 1), "boom"), (st("s2"), "whoosh"), (cap("s2", 3), "pop"), (st("s3"), "whoosh"), (cap("s3", 1), "pop"), (cap("s3", 3), "pop"),
       (st("s4"), "whoosh"), (cap("s4", 2), "kasse"), (st("s5"), "whoosh"), (cap("s5", 1), "ding"), (st("s6"), "whoosh"), (st("s7"), "whoosh"),
       (st("s8"), "whoosh"), (st("s8") + 0.3, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
