#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow) aus longform-steuer: 4 Jahre rückwirkend = über 2.500 € – Verweis aufs ganze Video."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import GOLD, GRUEN, OR, ROT, build, chip, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)

AMT = (f'<svg id="hk-a" viewBox="0 0 300 260" style="position:absolute;left:330px;top:720px;width:420px;height:364px;overflow:visible;z-index:2">'
       f'<g filter="drop-shadow(0 0 22px {ROT})"><path d="M20 80 L150 14 L280 80 Z" fill="none" stroke="{ROT}" stroke-width="12" stroke-linejoin="round"/>'
       + "".join(f'<rect x="{46 + i * 56}" y="96" width="24" height="110" rx="6" fill="{ROT}"/>' for i in range(4))
       + f'<rect x="20" y="214" width="260" height="22" rx="8" fill="{ROT}"/></g>'
       f'<text x="150" y="66" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="19" fill="{ROT}">FINANZAMT</text></svg>')
SCHEINE = "".join(
    f'<div class="sc" style="position:absolute;left:{120 + (i % 3) * 300}px;top:{1180 - (i // 3) * 40}px;width:170px;height:90px;border-radius:10px;'
    f'background:linear-gradient(135deg,#9fe0a8,#4caf6a);border:4px solid #2e7d4a;box-shadow:0 0 24px {GRUEN}66;z-index:3;display:flex;align-items:center;'
    f'justify-content:center;font-weight:900;font-size:40px;color:#1b5e33">100 €</div>' for i in range(6))

FORMULAR = (f'<div id="fo" style="position:absolute;left:300px;top:470px;width:480px;height:600px;border-radius:24px;background:#f4f1ea;z-index:2;'
            f'box-shadow:0 0 70px {OR}55;padding:50px 46px">'
            f'<div style="font-weight:900;font-size:40px;color:#222">Steuererklärung</div>'
            + "".join(f'<div style="margin-top:34px;height:22px;width:{w}%;border-radius:11px;background:#d6d0c4"></div>' for w in (90, 70, 85, 60, 78))
            + f'<div id="fo-s" style="position:absolute;left:40px;top:330px;width:400px;padding:16px 0;border:10px solid {GRUEN};border-radius:20px;text-align:center;'
            f'font-weight:900;font-size:96px;color:{GRUEN};transform:rotate(-8deg);background:#f4f1eadd">+<span id="fo-z">650</span> €</div></div>')


def jahr(i, j):
    return (f'<div id="jr{i}" style="position:absolute;left:{90 + i * 235}px;top:620px;width:200px;height:230px;border-radius:24px;background:#16191b;'
            f'border:6px solid {OR};box-shadow:0 0 40px {OR}66;z-index:2;overflow:hidden">'
            f'<div style="height:60px;background:{OR}"></div><div style="text-align:center;font-weight:900;font-size:64px;color:#fff;margin-top:36px">{j}</div></div>'
            f'<div id="jp{i}" style="position:absolute;left:{90 + i * 235}px;top:880px;width:200px;text-align:center;font-weight:900;font-size:44px;white-space:nowrap;'
            f'color:{GRUEN};text-shadow:0 0 30px {GRUEN};z-index:2">+650 €</div>')


JAHRE = "".join(jahr(i, j) for i, j in enumerate([2022, 2023, 2024, 2025]))
JAHRE_OHNE = "".join(jahr(i, j).split("<div id=\"jp")[0] for i, j in enumerate([2022, 2023, 2024, 2025]))

SZENEN = [
    (0.0, st("s91"),
     t("hk-t", 'Du schenkst dem Staat<br/><span class="box">GELD!</span>', 420, 76) + AMT + SCHEINE,
     lambda a, d: (f'tl.fromTo("#hk-t", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.35 }}, {a}); shake("#hk-t", {cap("s1", 3)});'
                   f' tl.fromTo("#hk-a", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.2, yoyo: true, repeat: 7 }}, {a} + 0.6);'
                   f' tl.fromTo(".sc", {{ x: 0, y: 0, opacity: 1, rotation: 0 }}, {{ x: (i) => 420 - 120 - (i % 3) * 300, y: (i) => -340 + Math.floor(i / 3) * 40,'
                   f' opacity: 0, rotation: (i) => (i % 2 ? 40 : -40), scale: 0.4, duration: 0.6, stagger: 0.35, ease: "power2.in" }}, {a} + 1.0);')),
    (st("s91"), cap("s91", 1),
     chip("tm-c", "Beispiel: Tim, 35", OR, 520, 60) + t("tm-t", "1 Steuer-<br/>erklärung", 720, 130),
     lambda a, d: f'pop("#tm-c", {a}); slam("#tm-t", {a} + 0.3);'),
    (cap("s91", 1), st("s93"),
     FORMULAR + partikel("fo-p", 540, 870, 26, (GRUEN, GOLD, "#fff"), 520),
     lambda a, d: f'pop("#fo", {a}); slam("#fo-s", {a} + 0.35); burst("#fo-p", {a} + 0.6); zaehl("#fo-z", 0, 650, {a} + 0.35, 0.8, "");'),
    (st("s93"), cap("s93", 3),
     t("ru-t", "Der Knaller:", 560, 100, "glow-o") + t("ru-u", 'Bis zu<br/><span class="box">4 JAHRE</span><br/>nachholen!', 760, 120),
     lambda a, d: f'pop("#ru-t", {a}); slam("#ru-u", {cap("s93", 1)});'),
    (cap("s93", 3), st("s95"),
     t("ja-t", "rückwirkend", 440, 96, "glow-o") + JAHRE_OHNE,
     lambda a, d: (f'tl.fromTo("#jr0, #jr1, #jr2, #jr3", {{ y: -500, rotation: -15 }}, {{ y: 0, rotation: 0, duration: 0.35, stagger: 0.18, ease: "back.out(1.6)" }}, {a}); pop("#ja-t", {a});')),
    (st("s95"), cap("s95", 3),
     t("su-t", "jedes Jahr", 440, 96, "glow-o") + JAHRE.replace('id="jr', 'id="kr').replace('id="jp', 'id="kp'),
     lambda a, d: ' '.join(f'pop("#kp{i}", {a} + {0.3 + i * 0.35:.2f});' for i in range(4)) + f' pop("#su-t", {a});'),
    (cap("s95", 3), st("s96"),
     t("gs-k", "zusammen", 500, 96, "glow-o") + t("gs-z", "über 2.500 €", 690, 130, "glow-g") + partikel("gs-p", 540, 760, 40, (GRUEN, GOLD, "#fff"), 720),
     lambda a, d: f'pop("#gs-k", {a}); slam("#gs-z", {a} + 0.1); burst("#gs-p", {a} + 0.35, 1.2); shake("#gs-z", {a} + 0.4); flash({a} + 0.1, 0.4);'),
    (st("s96"), en("s96"),
     t("vf-t", "sonst", 470, 90) + t("vf-z", "VERFALLEN", 620, 150, "glow-r") +
     chip("vf-c", "2022 nur noch bis 31.12.2026!", ROT, 900, 54),
     lambda a, d: f'pop("#vf-t", {a}); slam("#vf-z", {cap("s96", 2)} - 0.2); shake("#vf-z", {cap("s96", 2)} + 0.1); pop("#vf-c", {cap("s96", 2)} + 0.3);'),
    (en("s96"), DAUER,
     t("en-a", "Alle", 430, 90) + t("en-b", '<span class="box">7 Steuertricks</span>', 560, 112) + t("en-c", "im ganzen Video", 760, 90, "glow-o") +
     t("en-p", "👇", 900, 150) + chip("en-f", "Video unten antippen", OR, 1110, 64),
     lambda a, d: (f'pop("#en-a", {a}); slam("#en-b", {a} + 0.2); pop("#en-c", {a} + 0.5);'
                   f' tl.fromTo("#en-p", {{ y: -20 }}, {{ y: 30, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {a} + 0.6); pop("#en-f", {a} + 0.8);')),
]

SFX = [(0.0, "boom"), (1.0, "whoosh"), (1.35, "whoosh"), (1.7, "whoosh"), (cap("s1", 3), "kasse"), (st("s91"), "whoosh"), (st("s91") + 0.3, "pop"),
       (cap("s91", 1), "whoosh"), (cap("s91", 1) + 0.35, "boom"), (cap("s91", 1) + 1.1, "kasse"), (st("s93"), "whoosh"), (cap("s93", 1), "boom"),
       (cap("s93", 3), "whoosh")] + [(cap("s93", 3) + i * 0.18 + 0.2, "pop") for i in range(4)] + \
      [(st("s95"), "whoosh")] + [(st("s95") + 0.3 + i * 0.35, "tick") for i in range(4)] + \
      [(cap("s95", 3), "boom"), (cap("s95", 3) + 0.1, "kasse"), (st("s96"), "whoosh"), (cap("s96", 2) - 0.2, "boom"), (en("s96"), "whoosh"), (en("s96") + 0.2, "ding")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
