#!/usr/bin/env python3
"""HundeFinanzTv Short (Dark Glow): Deutschlandticket 2027 – 66,80 € (Kommentar-CTA in der Mitte, kein Schluss-CTA).
Aufnahme hatte den Folgen-Satz am Ende → Audio wurde umgeschnitten (s3 nach vorn, siehe skript-plan.json)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)


def ticket(id_, x, y, w, preis="", farbe=OR, z=2):
    h = w * 0.62
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;border-radius:{w * 0.06:.0f}px;z-index:{z};'
            f'background:linear-gradient(135deg,#23282c,#16191b);border:{max(4, w * 0.012):.0f}px solid {farbe};box-shadow:0 0 {w * 0.12:.0f}px {farbe}66;overflow:hidden">'
            f'<div style="position:absolute;left:0;top:0;width:100%;height:24%;background:{farbe}"></div>'
            f'<div style="position:absolute;left:7%;top:5%;font-weight:900;font-size:{w * 0.075:.0f}px;color:#111">DEUTSCHLANDTICKET</div>'
            f'<div style="position:absolute;left:7%;top:38%;width:22%;height:40%;border-radius:12px;background:#ffffff18;border:3px dashed #ffffff44"></div>'
            f'<div style="position:absolute;right:7%;bottom:12%;font-weight:900;font-size:{w * 0.13:.0f}px;color:#fff;white-space:nowrap">{preis}</div></div>')


STEMPEL = (f'<div id="hk-s" style="position:absolute;left:0;top:1040px;width:1080px;display:flex;justify-content:center;z-index:4">'
           f'<span style="padding:8px 40px;border:10px solid {ROT};border-radius:20px;color:{ROT};font-weight:900;font-size:110px;transform:rotate(-6deg);'
           f'box-shadow:0 0 50px {ROT}88;background:#0e1012cc">TEURER</span></div>')

JAHRE = [("2023", 49, "49 €"), ("2025", 58, "58 €"), ("2026", 63, "63 €"), ("2027", 66.8, "66,80 €")]
BALKEN = "".join(
    f'<div id="pb{i}" style="position:absolute;left:{150 + i * 210}px;top:{1240 - h * 9.5:.0f}px;width:160px;height:{h * 9.5:.0f}px;border-radius:18px 18px 0 0;'
    f'background:{ROT if i == 3 else OR};box-shadow:0 0 40px {(ROT if i == 3 else OR)}77;transform-origin:50% 100%;z-index:2"></div>'
    f'<div id="pz{i}" style="position:absolute;left:{110 + i * 210}px;top:{1240 - h * 9.5 - 70:.0f}px;width:240px;text-align:center;font-weight:900;font-size:46px;color:#fff;white-space:nowrap;z-index:3">{p}</div>'
    f'<div style="position:absolute;left:{110 + i * 210}px;top:1260px;width:240px;text-align:center;font-weight:800;font-size:40px;color:#ffffffaa">{j}</div>'
    for i, (j, h, p) in enumerate(JAHRE))
FAHRTEN = "".join(f'<div class="fa" style="position:absolute;left:{170 + (i % 5) * 150}px;top:{560 + (i // 5) * 120}px;width:120px;height:80px;border-radius:12px;'
                  f'background:#16191b;border:5px solid {GRUEN};box-shadow:0 0 20px {GRUEN}55;z-index:2"></div>' for i in range(20))
KALENDER = (f'<div id="kl" style="position:absolute;left:360px;top:480px;width:360px;height:380px;border-radius:30px;background:#f4f1ea;overflow:hidden;z-index:2;box-shadow:0 0 70px {GRUEN}55">'
            f'<div style="height:100px;background:{GRUEN};color:#111;font-weight:900;font-size:54px;text-align:center;line-height:100px">MONATLICH</div>'
            f'<svg viewBox="0 0 100 100" style="width:220px;height:220px;margin:30px 70px"><path d="M20 52 L42 74 L82 30" fill="none" stroke="{GRUEN}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Lohnt es sich<br/>für dich noch?")

SZENEN = [
    (0.0, st("s2"), ticket("hk-t", 190, 480, 700, "63 €") + STEMPEL + t("hk-a", "schon wieder", 920, 70),
     lambda a, d: f'tl.fromTo("#hk-t", {{ rotation: -6, scale: 1.1 }}, {{ rotation: 0, scale: 1, duration: 0.4 }}, {a}); slam("#hk-s", {cap("s1", 1)}); shake("#hk-t", {cap("s1", 1)} + 0.3);'),
    (st("s2"), st("s3"), chip("ja-c", "ab Januar 2027", OR, 470, 64) + t("ja-z", "66,80 €", 620, 230, "glow-r") + t("ja-u", "pro Monat", 900, 80),
     lambda a, d: f'pop("#ja-c", {a}); slam("#ja-z", {cap("s2", 1)}); shake("#ja-z", {cap("s2", 1)} + 0.3); pop("#ja-u", {cap("s2", 1)} + 0.4);'),
    (st("s3"), st("s4"), t("fo-t", "Folge", 520, 110) + t("fo-n", "HundeFinanzTv", 660, 110, "glow-o") + chip("fo-f", "+ Folgen", OR, 880, 90),
     lambda a, d: f'pop("#fo-t", {a}); pop("#fo-n", {a} + 0.2); slam("#fo-f", {a} + 0.5); tl.fromTo("#fo-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.0);'),
    (st("s4"), st("s5"), BALKEN + chip("pb-c", "+36 % seit dem Start", ROT, 430, 64),
     lambda a, d: " ".join(f'tl.fromTo("#pb{i}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.35, ease: "back.out(1.4)" }}, {a} + {i * 0.35:.2f}); pop("#pz{i}", {a} + {i * 0.35 + 0.2:.2f});' for i in range(4))
     + f' slam("#pb-c", {cap("s4", 1)});'),
    (st("s5"), st("s6"), t("jr-k", "pro Jahr", 480, 100, "glow-o") + t("jr-z", "801,60 €", 640, 180, "glow-r") + partikel("jr-p", 540, 760, 24, (ROT, OR, "#fff"), 520),
     lambda a, d: f'pop("#jr-k", {a}); slam("#jr-z", {cap("s5", 1)}); burst("#jr-p", {cap("s5", 1)} + 0.25);'),
    (st("s6"), st("s7"), t("lo-t", "Lohnt es sich?", 420, 110, "glow-o") + FAHRTEN + t("lo-z", "ab ca. 20 Fahrten / Monat", 1100, 64, "glow-g"),
     lambda a, d: f'pop("#lo-t", {a}); tl.fromTo(".fa", {{ scale: 0 }}, {{ scale: 1, duration: 0.15, stagger: 0.07, ease: "back.out(2)" }}, {cap("s6", 1)}); pop("#lo-z", {cap("s6", 2)});'),
    (st("s7"), st("s8"), KALENDER + t("kd-t", "kündbar", 920, 120, "glow-g") + t("kd-u", "jeden Monat", 1080, 70),
     lambda a, d: f'pop("#kl", {a}); slam("#kd-t", {cap("s7", 1)}); pop("#kd-u", {cap("s7", 2)});'),
    (st("s8"), st("s9"), frage_html, frage_js),
    (st("s9"), DAUER, chip("jt-c", "Tipp", GOLD, 440, 64) + ticket("jt-t", 240, 560, 600, "Job", GRUEN) + t("jt-a", "Frag deinen Chef", 980, 90) + t("jt-z", "oft deutlich günstiger", 1110, 70, "glow-g"),
     lambda a, d: f'pop("#jt-c", {a}); pop("#jt-t", {cap("s9", 1)}); pop("#jt-a", {a} + 0.3); slam("#jt-z", {cap("s9", 3)});'),
]

SFX = ([(0.0, "boom"), (cap("s1", 1), "boom"), (st("s2"), "whoosh"), (cap("s2", 1), "kasse"), (st("s3"), "whoosh"), (st("s3") + 0.5, "pop"), (st("s4"), "whoosh")]
       + [(st("s4") + i * 0.35, "pop") for i in range(4)] + [(cap("s4", 1), "boom"), (st("s5"), "whoosh"), (cap("s5", 1), "kasse"), (st("s6"), "whoosh")]
       + [(cap("s6", 1) + i * 0.14, "tick") for i in range(10)] + [(st("s7"), "whoosh"), (cap("s7", 1), "ding"), (st("s8"), "whoosh"), (st("s9"), "whoosh"), (cap("s9", 3), "ding")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
