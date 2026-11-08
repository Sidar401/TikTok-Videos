#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow): Aktivrente – 2.000 € im Monat steuerfrei (Kommentar-CTA Mitte).
Nutzer hat den Folgen-Satz (s3) beim Einsprechen weggelassen – siehe skript-plan.json."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

OPA = (f'<svg id="op" viewBox="0 0 200 260" style="position:absolute;left:390px;top:460px;width:300px;height:390px;z-index:2">'
       f'<g filter="drop-shadow(0 0 20px {OR})"><circle cx="100" cy="60" r="46" fill="#f4f1ea"/><path d="M60 40 Q100 0 140 40" fill="none" stroke="#bbb" stroke-width="10"/>'
       f'<circle cx="82" cy="62" r="7" fill="#111"/><circle cx="118" cy="62" r="7" fill="#111"/><path d="M85 82 Q100 92 115 82" fill="none" stroke="#111" stroke-width="5"/>'
       f'<path d="M30 250 C30 150 170 150 170 250 Z" fill="{OR}"/><rect x="88" y="150" width="24" height="70" fill="#fff"/></g></svg>')
STEMPEL = (f'<div id="sf" style="position:absolute;left:0;top:900px;width:1080px;display:flex;justify-content:center;z-index:4">'
           f'<span style="padding:8px 40px;border:10px solid {GRUEN};border-radius:20px;color:{GRUEN};font-weight:900;font-size:100px;transform:rotate(-6deg);'
           f'box-shadow:0 0 50px {GRUEN}88;background:#0e1012dd">STEUERFREI</span></div>')

frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Kennst du jemanden,<br/>der im Rentenalter arbeitet?")

SZENEN = [
    (0.0, st("s2"), t("hk-a", "Rentner aufgepasst!", 430, 84, "glow-o") + t("hk-z", "2.000 €", 600, 230, "glow-g") + STEMPEL,
     lambda a, d: f'tl.fromTo("#hk-z", {{ scale: 1.2 }}, {{ scale: 1, duration: 0.35 }}, {a}); slam("#sf", {cap("s1", 2)}); shake("#sf", {cap("s1", 2)} + 0.3);'),
    (st("s2"), st("s4"), t("ar-t", '<span class="box">AKTIVRENTE</span>', 560, 130) + t("ar-u", "kennen viele nicht", 820, 80),
     lambda a, d: f'slam("#ar-t", {a}); pop("#ar-u", {cap("s2", 1)});'),
    (st("s4"), cap("s4", 3), OPA + chip("op-c", "Rentenalter erreicht", OR, 900, 60) + chip("op-d", "+ weiter angestellt", GRUEN, 1020, 60),
     lambda a, d: f'pop("#op", {a}); pop("#op-c", {cap("s4", 1)} - 0.3); pop("#op-d", {cap("s4", 2)});'),
    (cap("s4", 3), st("s5"), t("ls-a", "bis 2.000 € Lohn", 520, 100) + t("ls-z", "0 € Steuer", 680, 150, "glow-g") + partikel("ls-p", 540, 780, 26, (GRUEN, GOLD, "#fff"), 520),
     lambda a, d: f'pop("#ls-a", {a}); slam("#ls-z", {cap("s4", 4)}); burst("#ls-p", {cap("s4", 4)} + 0.25);'),
    (st("s5"), st("s6"), chip("jr-c", "pro Jahr", OR, 470, 70) + t("jr-z", "24.000 €", 620, 200, "glow-g") + t("jr-u", "steuerfrei", 880, 90),
     lambda a, d: f'pop("#jr-c", {a}); slam("#jr-z", {cap("s5", 1)}); pop("#jr-u", {cap("s5", 1)} + 0.4);'),
    (st("s6"), st("s7"), t("sp-a", "spart oft", 500, 100) + t("sp-z", "mehrere 100 €", 660, 120, "glow-g") + t("sp-u", "Steuern im Monat", 880, 80),
     lambda a, d: f'pop("#sp-a", {a}); slam("#sp-z", {cap("s6", 1)}); pop("#sp-u", {cap("s6", 2)});'),
    (st("s7"), st("s8"), frage_html, frage_js),
    (st("s8"), DAUER, t("wi-t", "Wichtig:", 460, 110, "glow-r") + chip("wi-1", "nur für Angestellte", OR, 660, 70) + chip("wi-2", "Kranken- & Pflegevers. bleiben", ROT, 820, 56),
     lambda a, d: f'pop("#wi-t", {a}); slam("#wi-1", {cap("s8", 1)}); slam("#wi-2", {cap("s8", 3)});'),
]

SFX = [(0.0, "boom"), (0.1, "kasse"), (cap("s1", 2), "boom"), (st("s2"), "whoosh"), (st("s2") + 0.1, "pop"), (st("s4"), "whoosh"), (cap("s4", 2), "pop"),
       (cap("s4", 3), "whoosh"), (cap("s4", 4), "ding"), (st("s5"), "whoosh"), (cap("s5", 1), "kasse"), (st("s6"), "whoosh"), (cap("s6", 1), "pop"),
       (st("s7"), "whoosh"), (st("s8"), "whoosh"), (cap("s8", 1), "pop"), (cap("s8", 3), "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
