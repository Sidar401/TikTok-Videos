#!/usr/bin/env python3
"""HundeFinanzTv Willkommens-Video 2 „Countdown zur Million“ – 30 s, ohne Stimme, Beat + Soundeffekte."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GOLD, GRUEN, OR, ROT, buchstaben, build, chip, partikel, ring, t  # noqa: E402
from musik import beat  # noqa: E402

DAUER = 30.0
DROP = 20.0


def svg(id_, inhalt, x, y, w, h, vb="0 0 400 300", z=2):
    return (f'<svg id="{id_}" viewBox="{vb}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:{z}">{inhalt}</svg>')


GL = lambda f: f'filter="drop-shadow(0 0 18px {f})"'  # noqa: E731

SCHWEIN = (f'<g {GL(OR)}><ellipse cx="200" cy="170" rx="140" ry="105" fill="#ff9ab0"/><circle cx="330" cy="165" r="42" fill="#ff7f9d"/>'
           f'<circle cx="320" cy="160" r="7" fill="#7a2a3c"/><circle cx="342" cy="160" r="7" fill="#7a2a3c"/><path d="M140 80 L170 40 L190 85 Z" fill="#ff7f9d"/>'
           f'<circle cx="270" cy="130" r="9" fill="#222"/><rect x="170" y="62" width="70" height="14" rx="7" fill="#7a2a3c"/>'
           f'<rect x="110" y="250" width="34" height="46" rx="10" fill="#ff7f9d"/><rect x="240" y="250" width="34" height="46" rx="10" fill="#ff7f9d"/></g>'
           f'<g id="mz-m"><circle cx="205" cy="-40" r="34" fill="{GOLD}" stroke="#c98a00" stroke-width="6"/><text x="205" y="-27" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="38" fill="#8a5a00">€</text></g>')


def stapel():
    s = ""
    for k, (x, h) in enumerate([(40, 4), (130, 7), (220, 10), (310, 14)]):
        for i in range(h):
            s += (f'<g class="st{k}"><ellipse cx="{x + 30}" cy="{290 - i * 18}" rx="40" ry="13" fill="{GOLD}" stroke="#c98a00" stroke-width="4"/></g>')
    return f'<g {GL(GOLD)}>{s}</g>'


KURVE = (f'<path d="M0 290 L400 290" stroke="#ffffff33" stroke-width="4"/>'
         f'<path id="kv-l" d="M10 280 L70 250 L110 262 L170 200 L210 215 L270 140 L310 160 L390 30" fill="none" stroke="{GRUEN}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" {GL(GRUEN)}/>'
         f'<circle id="kv-p" cx="390" cy="30" r="16" fill="{GRUEN}" {GL(GRUEN)}/>')
SCHNEE = "".join(f'<circle class="sb" cx="{60 + i * 75}" cy="{260 - i * 22}" r="{14 + i * 11}" fill="none" stroke="{OR}" stroke-width="8" {GL(OR)}/>' for i in range(5))
KARTE = (f'<rect x="40" y="50" width="320" height="200" rx="24" fill="#2a2f33" stroke="#9aa3a8" stroke-width="6"/><rect x="40" y="95" width="320" height="38" fill="#111"/>'
         f'<rect x="70" y="165" width="60" height="44" rx="8" fill="{GOLD}"/><text x="330" y="225" text-anchor="end" font-family="Montserrat" font-weight="900" font-size="34" fill="#9aa3a8">-3.400 €</text>'
         f'<path id="kt-x1" d="M60 40 L340 260" stroke="{ROT}" stroke-width="22" stroke-linecap="round" {GL(ROT)}/><path id="kt-x2" d="M340 40 L60 260" stroke="{ROT}" stroke-width="22" stroke-linecap="round" {GL(ROT)}/>')
KALENDER = (f'<rect x="80" y="40" width="240" height="240" rx="26" fill="#f2f2f2"/><rect x="80" y="40" width="240" height="70" rx="26" fill="{OR}"/>'
            f'<rect x="80" y="80" width="240" height="30" fill="{OR}"/><rect x="130" y="20" width="18" height="50" rx="9" fill="#555"/><rect x="252" y="20" width="18" height="50" rx="9" fill="#555"/>'
            f'<text id="kl-j" x="200" y="230" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="110" fill="#111">1</text>')
RAKETE = (f'<g id="rk"><path d="M200 20 C250 70 260 150 245 220 L155 220 C140 150 150 70 200 20 Z" fill="#f2f2f2"/><circle cx="200" cy="110" r="28" fill="#4d8ff0" stroke="#222" stroke-width="6"/>'
          f'<path d="M155 170 L110 240 L160 225 Z" fill="{ROT}"/><path d="M245 170 L290 240 L240 225 Z" fill="{ROT}"/>'
          f'<path id="rk-f" d="M170 225 Q200 330 230 225 Z" fill="{OR}" {GL(OR)}/></g>')
HAUS = (f'<g {GL(GOLD)}><path d="M50 150 L200 30 L350 150" fill="none" stroke="{GOLD}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<rect x="90" y="140" width="220" height="150" rx="10" fill="none" stroke="{GOLD}" stroke-width="14"/><rect x="175" y="200" width="50" height="90" rx="6" fill="{GOLD}"/>'
        f'<rect x="115" y="170" width="40" height="40" rx="6" fill="{OR}"/><rect x="245" y="170" width="40" height="40" rx="6" fill="{OR}"/></g>')


def station(uid, motiv, wort, farbe, unter):
    return (svg(f"{uid}-s", motiv, 190, 760, 700, 525) + t(f"{uid}-w", wort, 1390, 112, f"glow-{farbe}") + t(f"{uid}-u", unter, 1540, 56))


def st_js(uid, extra=""):
    return lambda a, d: (f'tl.fromTo("#{uid}-s", {{ scale: 0.4, rotation: -10, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, {a});'
                         f' tl.fromTo("#{uid}-w", {{ x: 700, skewX: -25 }}, {{ x: 0, skewX: 0, duration: 0.3, ease: "power4.out" }}, {a} + 0.1);'
                         f' pop("#{uid}-u", {a} + 0.4); {extra.format(a=a)}')


ZAEHLER = (f'<div id="zl" style="position:absolute;left:0;top:430px;width:1080px;text-align:center;font-weight:900;font-size:150px;line-height:1;white-space:nowrap;'
           f'color:{OR};text-shadow:0 0 60px {OR}aa;z-index:6">0 €</div>'
           f'<div style="position:absolute;left:140px;top:620px;width:800px;height:26px;border-radius:13px;background:#ffffff18;z-index:6;overflow:hidden">'
           f'<div id="zl-b" style="width:100%;height:100%;border-radius:13px;background:linear-gradient(90deg,{OR},{GOLD});box-shadow:0 0 30px {OR};transform-origin:left center"></div></div>'
           f'<div id="zl-z" style="position:absolute;left:0;top:660px;width:1080px;text-align:center;font-weight:800;font-size:40px;color:#ffffff99;z-index:6">Ziel: 1.000.000 €</div>')

STATIONEN = [
    ("sp", SCHWEIN, "SPAREN", "o", "jeder Euro zählt", "tl.fromTo(\"#mz-m\", {{ y: 0 }}, {{ y: 120, duration: 0.5, ease: \"power2.in\" }}, {a} + 0.5);"),
    ("ms", stapel(), "JEDEN MONAT", "o", "Stück für Stück", "tl.fromTo(\"#ms-s ellipse\", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.12, stagger: 0.03 }}, {a} + 0.2);"),
    ("kv", KURVE, "INVESTIEREN", "g", "Geld arbeitet für dich", "draw(\"#kv-l\", {a} + 0.15, 1.1); pop(\"#kv-p\", {a} + 1.2);"),
    ("zz", SCHNEE, "ZINSESZINS", "o", "Zinsen auf Zinsen", "tl.fromTo(\".sb\", {{ scale: 0, transformOrigin: \"50% 50%\" }}, {{ scale: 1, duration: 0.3, stagger: 0.15, ease: \"back.out(2)\" }}, {a} + 0.2);"),
    ("kt", KARTE, "SCHULDEN WEG", "r", "teure Kredite zuerst", "draw(\"#kt-x1\", {a} + 0.5, 0.2); draw(\"#kt-x2\", {a} + 0.75, 0.2); shake(\"#kt-s\", {a} + 0.95);"),
    ("kl", KALENDER, "GEDULD", "o", "Jahre statt Tage", ""),
    ("rk", RAKETE, "ZEIT", "g", "der stärkste Hebel", "tl.fromTo(\"#rk\", {{ y: 40 }}, {{ y: -40, duration: 1.6, ease: \"power2.in\" }}, {a}); tl.fromTo(\"#rk-f\", {{ scaleY: 0.7, transformOrigin: \"50% 0%\" }}, {{ scaleY: 1.3, duration: 0.08, yoyo: true, repeat: 19 }}, {a});"),
    ("hs", HAUS, "FREIHEIT", "o", "Geld, das dich trägt", ""),
]

SZENEN = [
    (0.0, 2.0, t("hk-q", 'Wie wird daraus<br/><span class="box">1 MILLION?</span>', 900, 104) + partikel("hk-p", 540, 1000, 24),
     lambda a, d: f'tl.fromTo("#hk-q", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.35, ease: "power3.out" }}, {a}); burst("#hk-p", {a} + 0.05, 0.9); shake("#hk-q", 1.0);'),
]
for i, (uid, motiv, wort, f, unter, extra) in enumerate(STATIONEN):
    SZENEN.append((2.0 + 2 * i, 4.0 + 2 * i, station(uid, motiv, wort, f, unter), st_js(uid, extra)))
# Kalender zählt Jahre hoch
SZENEN[6] = (SZENEN[6][0], SZENEN[6][1], SZENEN[6][2],
             lambda a, d: st_js("kl")(a, d) + f' zaehl("#kl-j", 1, 20, {a} + 0.3, 1.3, "");')

# Breakdown 18–20: „Fast…“
SZENEN.append((18.0, DROP, t("fa-t", "fast …", 1200, 160, "glow-o") + t("fa-u", "noch ein bisschen", 1420, 64),
               lambda a, d: f'pop("#fa-t", {a}); tl.fromTo("#fa-t", {{ scale: 1 }}, {{ scale: 1.25, duration: {d}, ease: "power2.in" }}, {a}); pop("#fa-u", {a} + 0.6);'))

# Zähler-Ebene 0–20 (eigene Spur, liegt über den Stationen)
SZENEN.append((0.0, DROP, ZAEHLER,
               lambda a, d: (f'const zo = {{ v: 0 }}; const zt = () => {{ document.querySelector("#zl").textContent = Math.round(zo.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " €"; }};'
                             f' tl.fromTo(zo, {{ v: 0 }}, {{ v: 980000, duration: 17.6, ease: "power2.in", onUpdate: zt }}, 0.4);'
                             f' tl.to(zo, {{ v: 999999, duration: 1.8, ease: "power2.out", onUpdate: zt }}, 18);'
                             f' tl.fromTo("#zl-b", {{ scaleX: 0 }}, {{ scaleX: 0.98, duration: 17.6, ease: "power2.in" }}, 0.4); tl.to("#zl-b", {{ scaleX: 1, duration: 1.8 }}, 18);'
                             f' tl.fromTo("#zl", {{ color: "{OR}" }}, {{ color: "{GRUEN}", duration: 0.4 }}, 8);'
                             + "".join(f' tl.fromTo("#zl", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.25 }}, {2.0 + 2 * k});' for k in range(9))
                             + f' tl.fromTo("#zl", {{ x: -6 }}, {{ x: 6, duration: 0.04, yoyo: true, repeat: 49, ease: "none" }}, 18);'), 4))

# DROP: Million
SZENEN.append((DROP, 23.5,
               t("mi-z", "1.000.000 €", 700, 150, "") + t("mi-t", 'du schaffst das', 1000, 90) +
               partikel("mi-p1", 540, 800, 40, (GOLD, OR, "#fff", GRUEN), 760) + partikel("mi-p2", 540, 800, 30, (GOLD, "#fff"), 1000, (6, 16)),
               lambda a, d: (f'flash({a}); slam("#mi-z", {a}); burst("#mi-p1", {a} + 0.05, 1.3); burst("#mi-p2", {a} + 0.15, 1.6); shake("#mi-z", {a} + 0.3);'
                             f' tl.fromTo("#mi-z", {{ color: "#ffffff", textShadow: "0 0 30px {GOLD}" }}, {{ color: "{GOLD}", textShadow: "0 0 90px {GOLD}", duration: 0.6 }}, {a} + 0.3);'
                             f' letters("#mi-t", {a} + 1.0); flash({a} + 2.0, 0.4);')))
# Willkommen
LOGO = ring("wk-r", f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', 290, 420, 500)
SZENEN.append((23.5, 27.0, LOGO + t("wk-a", "Willkommen bei", 1010, 72) + buchstaben("wk-n", "HundeFinanzTv", 1110, 104, "glow-o") + partikel("wk-p", 540, 670, 30, (OR, GOLD, "#fff"), 600),
               lambda a, d: (f'tl.fromTo(["#logo", "#brand"], {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2 }}, {a});'
                             f' tl.fromTo("#wk-r", {{ scale: 0, rotation: -200 }}, {{ scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.6)" }}, {a}); burst("#wk-p", {a} + 0.5);'
                             f' pop("#wk-a", {a} + 0.6); letters("#wk-n", {a} + 0.9);')))
SZENEN.append((27.0, DAUER, LOGO.replace("wk-r", "en-r") + t("en-t", 'Dein Weg zu<br/><span class="box">mehr Geld</span>', 1010, 100) +
               t("en-u", "jeden Tag neue Videos", 1300, 60) + chip("en-f", "+ Folgen", OR, 1430, 80),
               lambda a, d: (f'glitch("#en-t", {a}); pop("#en-u", {a} + 0.4); slam("#en-f", {a} + 0.8);'
                             f' tl.fromTo("#en-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.2);')))

SFX = [(0.0, "boom"), (0.05, "pop")] + [(2.0 + 2 * k, "whoosh") for k in range(8)] + [(2.6, "kasse"), (8.2, "ding"), (10.5, "boom"), (10.75, "boom"),
       (14.0, "whoosh"), (16.2, "ding"), (18.0, "whoosh"), (DROP, "boom"), (DROP + 0.05, "kasse"), (23.5, "whoosh"), (24.0, "pop"), (24.4, "ding"),
       (27.0, "whoosh"), (27.8, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX, dauer=DAUER, musik=beat(DAUER, pausen=[(18.0, DROP)]))
