#!/usr/bin/env python3
"""HundeFinanzTv Willkommens-Video 1 „Der Münzwurf“ – 30 s, ohne Stimme, Beat + Soundeffekte."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GOLD, GRUEN, OR, ROT, buchstaben, build, chip, partikel, ring, t  # noqa: E402
from musik import beat  # noqa: E402

DAUER = 30.0
DROP = 14.0
IR = "immediateRender: false"


def muenze(id_, x, y, d, z=3):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;z-index:{z};'
            f'background:radial-gradient(circle at 35% 30%, #fff3b0 0%, {GOLD} 35%, #d99a00 75%, #a86f00 100%);border:{d * 0.04:.0f}px solid #b47c00;'
            f'box-shadow:0 0 {d * 0.25:.0f}px {GOLD}aa, inset 0 0 {d * 0.08:.0f}px #8a5a00;display:flex;align-items:center;justify-content:center">'
            f'<div style="width:72%;height:72%;border-radius:50%;border:{d * 0.025:.0f}px solid #b47c0099;display:flex;align-items:center;justify-content:center;'
            f'font-weight:900;font-size:{d * 0.42:.0f}px;color:#8a5a00;text-shadow:0 2px 0 #fff6">€</div></div>')


def welle(id_, cx, cy, farbe=OR):
    return (f'<div id="{id_}" style="position:absolute;left:{cx - 200}px;top:{cy - 200}px;width:400px;height:400px;border-radius:50%;'
            f'border:14px solid {farbe};box-shadow:0 0 40px {farbe};opacity:0;z-index:2"></div>')


def welle_js(sel, at):
    return f'tl.fromTo("{sel}", {{ scale: 0.3, opacity: 1 }}, {{ scale: 3.2, opacity: 0, duration: 0.8, ease: "power2.out" }}, {at});'


# 0–2.5: Münze fällt
S_MUENZE = (muenze("cn", 360, 620, 360) + welle("cn-w", 540, 800) + partikel("cn-p", 540, 800, 34, (GOLD, OR, "#fff"), 640) +
            t("cn-t", "Alles beginnt mit", 1140, 76) + t("cn-z", '<span class="box">1 Euro</span>', 1250, 120))
J_MUENZE = (f'tl.fromTo("#cn", {{ y: -1150, rotationY: 0, transformPerspective: 900 }}, {{ y: 0, rotationY: 1440, duration: 0.65, ease: "power3.in" }}, 0);'
            f' tl.fromTo("#cn", {{ scaleY: 0.82, scaleX: 1.12 }}, {{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "elastic.out(1, 0.4)" }}, 0.65);'
            + welle_js("#cn-w", 0.65) + ' burst("#cn-p", 0.65, 1.1); flash(0.65, 0.35);'
            f' tl.fromTo("#cn-t", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.3 }}, 0); slam("#cn-z", 0.7); shake("#cn", 0.7);'
            f' tl.to("#cn", {{ rotationY: 360, duration: 1.2, ease: "power1.inOut" }}, 1.2);')

# 2.5–5: Chart wächst aus der Münze
CHART = (f'<svg viewBox="0 0 900 760" style="position:absolute;left:90px;top:560px;width:900px;height:760px;overflow:visible;z-index:2">'
         f'<defs><linearGradient id="ch-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GRUEN}" stop-opacity="0.45"/><stop offset="1" stop-color="{GRUEN}" stop-opacity="0"/></linearGradient></defs>'
         + "".join(f'<path d="M0 {y} L900 {y}" stroke="#ffffff14" stroke-width="3"/>' for y in (160, 320, 480, 640)) +
         f'<path id="ch-a" d="M60 700 C260 690 380 610 500 470 C600 350 700 250 860 60 L860 740 L60 740 Z" fill="url(#ch-g)"/>'
         f'<path id="ch-l" d="M60 700 C260 690 380 610 500 470 C600 350 700 250 860 60" fill="none" stroke="{GRUEN}" stroke-width="16" stroke-linecap="round" filter="drop-shadow(0 0 20px {GRUEN})"/>'
         f'<circle id="ch-d" cx="860" cy="60" r="24" fill="#fff" filter="drop-shadow(0 0 24px {GRUEN})"/></svg>')
S_CHART = (CHART + muenze("ch-m", 90, 1205, 120) + partikel("ch-p", 950, 620, 20, (GRUEN, "#fff"), 300) +
           t("ch-t", 'und wird <span class="box">MEHR</span>', 1400, 110))
J_CHART = lambda a, d: (f'pop("#ch-m", {a}); draw("#ch-l", {a} + 0.15, 1.4); tl.fromTo("#ch-a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8 }}, {a} + 0.6);'  # noqa: E731
                        f' tl.fromTo("#ch-d", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, {a} + 1.5);'
                        f' burst("#ch-p", {a} + 1.55, 0.8); glitch("#ch-t", {a} + 0.3); pop("#ch-t", {a} + 0.3);')

# 5–7: Logo-Reveal
LOGO = (f'<div id="lg" style="position:absolute;left:290px;top:520px;width:500px;height:500px;border-radius:50%;overflow:hidden;border:12px solid {OR};'
        f'box-shadow:0 0 120px {OR}aa;background:#16191b;z-index:3">{BEAGLE}'
        f'<div id="lg-s" style="position:absolute;top:-20%;left:0;width:110px;height:140%;background:linear-gradient(90deg,transparent,#ffffffaa,transparent);transform:rotate(20deg)"></div></div>')
S_LOGO = (LOGO + welle("lg-w", 540, 770) + partikel("lg-p", 540, 770, 36, (OR, GOLD, "#fff"), 700) +
          buchstaben("lg-n", "HundeFinanzTv", 1110, 112, "glow-o") + t("lg-u", "Geld einfach erklärt", 1260, 62))
J_LOGO = lambda a, d: (f'tl.fromTo(["#logo", "#brand"], {{ opacity: 1 }}, {{ opacity: 0, duration: 0.15 }}, {a});'  # noqa: E731
                       f' tl.fromTo("#lg", {{ scale: 0, rotation: -260 }}, {{ scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.7)" }}, {a});'
                       + welle_js("#lg-w", f"{a} + 0.5") + f' burst("#lg-p", {a} + 0.5, 1.2);'
                       f' tl.fromTo("#lg-s", {{ x: -200 }}, {{ x: 650, duration: 0.6, ease: "power2.inOut" }}, {a} + 0.9);'
                       f' letters("#lg-n", {a} + 0.55); pop("#lg-u", {a} + 1.2);'
                       f' tl.fromTo(["#logo", "#brand"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, {IR} }}, {a} + {d});')


# 7–10: Wort-Schläge
def wort(uid, txt, cls, size=150):
    return (t(f"{uid}", txt, 820, size, cls) + partikel(f"{uid}-p", 540, 900, 22, ("#fff", OR) if cls != "glow-g" else (GRUEN, "#fff", GOLD), 560))


def wort_js(uid):
    return lambda a, d: (f'slam("#{uid}", {a}); burst("#{uid}-p", {a} + 0.25, 0.8); shake("#{uid}", {a} + 0.28);')


# 10–12: Münzregen
REGEN = "".join(muenze(f"rg{i}", 90 + (i * 167) % 820, 700 + (i % 3) * 30, 150) for i in range(12))
S_REGEN = REGEN + t("rg-t", "Was dich hier", 1260, 96) + t("rg-u", '<span class="box">erwartet</span>', 1380, 110)
J_REGEN = lambda a, d: (''.join(  # noqa: E731
    f'tl.fromTo("#rg{i}", {{ y: -1100, rotation: {(-1) ** i * 200} }}, {{ y: {(i // 4) * 140}, rotation: 0, duration: 0.45, ease: "bounce.out" }}, {a} + {i * 0.08:.2f}); '
    for i in range(12)) + f'pop("#rg-t", {a} + 0.6); slam("#rg-u", {a} + 0.9);')

# 12–14 (Breakdown): drei Themen-Karten
KARTEN = [("Spar-Tricks", OR, 620), ("ETF &amp; Zinsen", GRUEN, 860), ("Geld-Fallen", ROT, 1100)]
S_KARTEN = "".join(
    f'<div id="kk{i}" style="position:absolute;left:150px;top:{y}px;width:780px;padding:34px 0;border-radius:30px;background:#16191b;border:6px solid {f};'
    f'box-shadow:0 0 60px {f}66;text-align:center;font-weight:900;font-size:84px;color:#fff;z-index:3">{txt}</div>' for i, (txt, f, y) in enumerate(KARTEN))
J_KARTEN = lambda a, d: ''.join(  # noqa: E731
    f'tl.fromTo("#kk{i}", {{ x: {(-1) ** i * 1100}, rotation: {(-1) ** i * 8} }}, {{ x: 0, rotation: 0, duration: 0.4, ease: "back.out(1.5)" }}, {a} + {i * 0.55:.2f}); '
    for i in range(3)) + f'tl.fromTo("#kk0, #kk1, #kk2", {{ scale: 1 }}, {{ scale: 1.04, duration: 0.25, yoyo: true, repeat: 1 }}, {a} + 1.6);'

# 14 DROP: jeden Tag
S_TAG = (t("tg-a", "JEDEN", 640, 190, "") + t("tg-b", '<span class="box">TAG</span>', 840, 240) + t("tg-c", "neue Videos", 1170, 100, "glow-o") +
         welle("tg-w", 540, 960) + partikel("tg-p", 540, 960, 44, (OR, GOLD, "#fff", GRUEN), 900))
J_TAG = lambda a, d: (f'flash({a}); slam("#tg-a", {a}); slam("#tg-b", {a} + 0.25); shake("#tg-b", {a} + 0.5); burst("#tg-p", {a} + 0.25, 1.4);'  # noqa: E731
                      + welle_js("#tg-w", f"{a} + 0.25") + f' pop("#tg-c", {a} + 0.7);')

# 16.5–19: Duell ohne/mit Plan
S_DUELL = (f'<div style="position:absolute;left:150px;top:1240px;width:780px;height:6px;background:#ffffff33;z-index:2"></div>'
           f'<div id="du-l" style="position:absolute;left:170px;top:1040px;width:260px;height:200px;border-radius:20px 20px 0 0;background:{ROT};box-shadow:0 0 50px {ROT}88;transform-origin:50% 100%;z-index:2"></div>'
           f'<div id="du-r" style="position:absolute;left:650px;top:560px;width:260px;height:680px;border-radius:20px 20px 0 0;background:{GRUEN};box-shadow:0 0 50px {GRUEN}88;transform-origin:50% 100%;z-index:2"></div>'
           f'<div id="du-lt" class="t" style="top:1280px;left:-240px;font-size:64px">Ohne Plan</div><div id="du-rt" class="t glow-g" style="top:1280px;left:240px;font-size:64px">Mit Plan</div>'
           + t("du-v", "VS", 700, 110, "glow-o"))
J_DUELL = lambda a, d: (f'tl.fromTo("#du-l", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power3.out" }}, {a} + 0.1);'  # noqa: E731
                        f' tl.fromTo("#du-r", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 1.0, ease: "power3.out" }}, {a} + 0.6); slam("#du-v", {a} + 0.3);'
                        f' pop("#du-lt", {a} + 0.1); pop("#du-rt", {a} + 0.6);')


# 19–21.5: 50-30-20-Donut
def donut():
    r, u = 230, 2 * 3.14159 * 230
    teile, off = [], 0
    for i, (p, f) in enumerate([(0.5, OR), (0.3, "#4d8ff0"), (0.2, GRUEN)]):
        teile.append(f'<circle id="do{i}" cx="300" cy="300" r="{r}" fill="none" stroke="{f}" stroke-width="90" stroke-dasharray="{u * p - 8:.1f} {u:.1f}" '
                     f'stroke-dashoffset="{-off:.1f}" transform="rotate(-90 300 300)" filter="drop-shadow(0 0 16px {f})"/>')
        off += u * p
    return (f'<svg viewBox="0 0 600 600" style="position:absolute;left:240px;top:560px;width:600px;height:600px;overflow:visible;z-index:2">{"".join(teile)}'
            f'<text x="300" y="285" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="80" fill="#fff">50·30·20</text>'
            f'<text x="300" y="350" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#ffffffaa">die Regel</text></svg>')


S_DONUT = (donut() + chip("dn-a", "50 % Leben", OR, 1220, 54, 70) + chip("dn-b", "30 % Spaß", "#4d8ff0", 1220, 54, 590) +
           chip("dn-c", "20 % Sparen", GRUEN, 1350, 60))
J_DONUT = lambda a, d: (f'tl.fromTo("#do0, #do1, #do2", {{ scale: 0, rotation: -120, transformOrigin: "50% 50%" }}, {{ scale: 1, rotation: 0, duration: 0.45, stagger: 0.18, ease: "back.out(1.6)" }}, {a});'  # noqa: E731
                        f' pop("#dn-a", {a} + 0.5); pop("#dn-b", {a} + 0.7); slam("#dn-c", {a} + 0.95);')

# 21.5–24: Bereit?
S_BEREIT = ("".join(welle(f"br-w{i}", 540, 900) for i in range(4)) + t("br-t", "Bereit?", 820, 180, "glow-o") +
            t("br-u", "Dein Geld. Dein Plan.", 1100, 74))
J_BEREIT = lambda a, d: (''.join(welle_js(f"#br-w{i}", f"{a} + {i * 0.5}") for i in range(4)) +  # noqa: E731
                         f' slam("#br-t", {a}); tl.fromTo("#br-t", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.25, yoyo: true, repeat: 7 }}, {a} + 0.3); pop("#br-u", {a} + 0.8);')

# 24–30: Outro
RING = ring("ou-r", f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', 290, 420, 500)
S_OUT1 = RING + t("ou-a", "Willkommen bei", 1010, 72) + buchstaben("ou-n", "HundeFinanzTv", 1110, 104, "glow-o") + partikel("ou-p", 540, 670, 30)
J_OUT1 = lambda a, d: (f'tl.fromTo(["#logo", "#brand"], {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2, {IR} }}, {a});'  # noqa: E731
                       f' tl.fromTo("#ou-r", {{ scale: 0, rotationY: 540, transformPerspective: 900 }}, {{ scale: 1, rotationY: 0, duration: 0.7, ease: "back.out(1.4)" }}, {a});'
                       f' burst("#ou-p", {a} + 0.5); pop("#ou-a", {a} + 0.5); letters("#ou-n", {a} + 0.8);')
S_OUT2 = RING.replace("ou-r", "o2-r") + t("o2-t", "Folge uns!", 1010, 110, "glow-o") + t("o2-u", "jeden Tag neue Videos", 1160, 60) + chip("o2-f", "+ Folgen", OR, 1300, 84)
J_OUT2 = lambda a, d: (f'glitch("#o2-t", {a}); pop("#o2-u", {a} + 0.3); slam("#o2-f", {a} + 0.6);'  # noqa: E731
                       f' tl.fromTo("#o2-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.0);')

SZENEN = [
    (0.0, 2.5, S_MUENZE, lambda a, d: J_MUENZE),
    (2.5, 5.0, S_CHART, J_CHART),
    (5.0, 7.0, S_LOGO, J_LOGO),
    (7.0, 8.0, wort("w1", "SPAREN.", ""), wort_js("w1")),
    (8.0, 9.0, wort("w2", "INVESTIEREN.", "glow-o", 124), wort_js("w2")),
    (9.0, 10.0, wort("w3", "MEHR GELD.", "glow-g"), wort_js("w3")),
    (10.0, 12.0, S_REGEN, J_REGEN),
    (12.0, DROP, S_KARTEN, J_KARTEN),
    (DROP, 16.5, S_TAG, J_TAG),
    (16.5, 19.0, S_DUELL, J_DUELL),
    (19.0, 21.5, S_DONUT, J_DONUT),
    (21.5, 24.0, S_BEREIT, J_BEREIT),
    (24.0, 27.0, S_OUT1, J_OUT1),
    (27.0, DAUER, S_OUT2, J_OUT2),
]

SFX = ([(0.0, "whoosh"), (0.65, "boom"), (0.7, "kasse"), (2.5, "whoosh"), (4.0, "ding"), (5.0, "whoosh"), (5.5, "boom"), (5.9, "ding"),
        (7.0, "boom"), (8.0, "boom"), (9.0, "boom"), (9.05, "kasse"), (10.0, "whoosh")] +
       [(10.2 + i * 0.08, "tick") for i in range(12)] +
       [(12.0, "whoosh"), (12.55, "whoosh"), (13.1, "whoosh"), (DROP, "boom"), (DROP + 0.25, "pop"), (16.5, "whoosh"), (16.8, "pop"), (17.1, "pop"),
        (19.0, "whoosh"), (19.5, "pop"), (19.7, "pop"), (19.95, "ding"), (21.5, "whoosh"), (24.0, "whoosh"), (24.5, "ding"), (27.0, "whoosh"), (27.6, "pop")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX, dauer=DAUER, musik=beat(DAUER, pausen=[(12.0, DROP)], seed=5))
