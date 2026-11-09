#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow): Lohnsteuer-Freibetrag – jeden Monat mehr Netto (Teilen-CTA als 3. Satz)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import GOLD, GRUEN, OR, ROT, TEILEN_SVG, build, chip, cta_szene, handy, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

KAL = "".join(f'<div class="mo" style="position:absolute;left:{130 + (i % 4) * 210}px;top:{640 + (i // 4) * 150}px;width:180px;height:120px;border-radius:18px;'
              f'background:#16191b;border:5px solid {GRUEN};box-shadow:0 0 24px {GRUEN}55;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:2">'
              f'<div style="font-weight:800;font-size:30px;color:#ffffffaa">{m}</div><div style="font-weight:900;font-size:40px;color:{GRUEN}">+ €</div></div>'
              for i, m in enumerate(["JAN", "FEB", "MÄR", "APR", "MAI", "JUN", "JUL", "AUG", "SEP", "OKT", "NOV", "DEZ"]))
AUTO = (f'<svg id="au" viewBox="0 0 300 140" style="position:absolute;left:60px;top:560px;width:300px;height:140px;z-index:3">'
        f'<g filter="drop-shadow(0 0 18px {OR})"><path d="M20 90 L50 40 L200 40 L250 90 L280 95 L280 115 L20 115 Z" fill="{OR}"/>'
        f'<circle cx="80" cy="118" r="20" fill="#222" stroke="#fff" stroke-width="5"/><circle cx="220" cy="118" r="20" fill="#222" stroke="#fff" stroke-width="5"/>'
        f'<rect x="70" y="50" width="55" height="35" rx="6" fill="#16191b"/><rect x="135" y="50" width="55" height="35" rx="6" fill="#16191b"/></g></svg>')
STRASSE = f'<div style="position:absolute;left:60px;top:730px;width:960px;height:10px;background:repeating-linear-gradient(90deg,#ffffff55 0 60px,transparent 60px 110px);z-index:1"></div>'
ELSTER = handy("el", 380, 450, 320, '<div style="font-weight:900;font-size:50px;color:#fff">ELSTER</div>'
                                    f'<div style="font-weight:800;font-size:26px;color:#ffffffaa;text-align:center">Antrag auf<br/>Lohnsteuer-<br/>Ermäßigung</div>'
                                    f'<div style="width:120px;height:120px;border-radius:50%;background:{GRUEN};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:80px;color:#111">✓</div>')

teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick das einem Pendler!")

SZENEN = [
    (0.0, st("s2"), KAL + t("hk-t", 'Steuergeld<br/><span class="box">JEDEN</span> Monat', 400, 76),
     lambda a, d: f'tl.fromTo("#hk-t", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.35 }}, {a}); tl.fromTo(".mo", {{ scale: 0 }}, {{ scale: 1, duration: 0.18, stagger: 0.07, ease: "back.out(2)" }}, {a} + 0.1);'),
    (st("s2"), st("s3"), t("fb-t", '<span class="box">Lohnsteuer-<br/>Freibetrag</span>', 540, 110) + chip("fb-c", "jetzt für 2027 beantragen", GRUEN, 900, 64),
     lambda a, d: f'slam("#fb-t", {cap("s2", 1)}); pop("#fb-c", {cap("s2", 3)});'),
    (st("s3"), st("s4"), teilen_html, teilen_js),
    (st("s4"), st("s5"), AUTO + STRASSE + t("km-z", "30 km", 820, 170, "glow-o") + t("km-u", "× 220 Tage", 1020, 90),
     lambda a, d: f'tl.fromTo("#au", {{ x: -300 }}, {{ x: 640, duration: 3.2, ease: "power1.inOut" }}, {a}); pop("#km-z", {cap("s4", 1)}); pop("#km-u", {cap("s4", 2)});'),
    (st("s5"), st("s6"), t("fk-a", "Fahrtkosten", 440, 90, "glow-o") + t("fk-z", "≈ 2.500 €", 580, 190) + chip("fk-c", "> 1.000 € über der Pauschale", GRUEN, 860, 60),
     lambda a, d: f'pop("#fk-a", {a}); slam("#fk-z", {cap("s5", 1)}); pop("#fk-c", {cap("s5", 2)});'),
    (st("s6"), st("s7"), t("mn-a", "jeden Monat", 480, 100) + t("mn-z", "+30 €", 640, 230, "glow-g") + t("mn-u", "mehr netto", 920, 90) + partikel("mn-p", 540, 760, 26, (GRUEN, GOLD, "#fff"), 520),
     lambda a, d: f'pop("#mn-a", {a}); slam("#mn-z", {cap("s6", 3)}); burst("#mn-p", {cap("s6", 3)} + 0.25); pop("#mn-u", {cap("s6", 3)} + 0.4);'),
    (st("s7"), st("s8"), ELSTER, lambda a, d: f'pop("#el", {a});'),
    (st("s8"), DAUER, t("wi-t", "Wichtig:", 480, 110, "glow-r") + t("wi-u", 'dann <span class="box">Steuererklärung</span><br/>Pflicht', 680, 90),
     lambda a, d: f'pop("#wi-t", {a}); slam("#wi-u", {cap("s8", 2)});'),
]

SFX = ([(0.0, "boom")] + [(0.1 + i * 0.07, "tick") for i in range(12)] +
       [(st("s2"), "whoosh"), (cap("s2", 1), "boom"), (st("s3"), "whoosh"), (st("s4"), "whoosh"), (cap("s4", 1), "pop"), (st("s5"), "whoosh"),
        (cap("s5", 1), "kasse"), (st("s6"), "whoosh"), (cap("s6", 3), "ding"), (st("s7"), "whoosh"), (st("s8"), "whoosh"), (cap("s8", 2), "boom")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
