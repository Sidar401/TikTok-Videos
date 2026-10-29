#!/usr/bin/env python3
"""HundeFinanzTv Willkommens-Video 3 „Die Kamerafahrt“ – 30 s, ohne Stimme, Beat + Soundeffekte.
Eine Kamera rast nach unten durch eine dunkle Geld-Welt (Parallax), jede Station stellt eine Frage, am Ende öffnet sich der Tresor."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE  # noqa: E402
from glow_short import GOLD, GRUEN, OR, ROT, buchstaben, build, chip, partikel, ring, t  # noqa: E402
from musik import beat  # noqa: E402

DAUER = 30.0
TAKT = 2.4          # Zeit pro Station
N = 9               # Stationen
FAHRT = 0.45        # Dauer einer Kamerafahrt
TRESOR = N * TAKT   # 21.6
AUF = 22.8          # Tresor geht auf (Drop)
H = 1920
GL = lambda f: f'filter="drop-shadow(0 0 18px {f})"'  # noqa: E731


def svg(id_, inhalt, x, y, w, h, vb):
    return f'<svg id="{id_}" viewBox="{vb}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:2">{inhalt}</svg>'


def frage(k, txt, cls="glow-o", top=520, size=90):
    return t(f"f{k}", txt, top, size, cls)


# ---------- Stationen (Motiv-HTML, JS bei Ankunft a) ----------
EURO = (f'<div id="m0" style="position:absolute;left:290px;top:820px;width:500px;height:500px;border-radius:50%;border:14px solid {OR};'
        f'box-shadow:0 0 120px {OR}aa, inset 0 0 60px {OR}55;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:320px;color:{OR};'
        f'text-shadow:0 0 60px {OR};z-index:2">€</div>')
BALKEN = "".join(
    f'<div class="bk" style="position:absolute;left:{150 + i * 210}px;top:{1350 - h}px;width:150px;height:{h}px;border-radius:18px 18px 0 0;background:{f};'
    f'box-shadow:0 0 40px {f}88;transform-origin:50% 100%;z-index:2"></div><div class="t" style="left:{150 + i * 210 - 540 + 75}px;top:1380px;font-size:40px">{n}</div>'
    for i, (n, h, f) in enumerate([("Miete", 520, OR), ("Essen", 300, GOLD), ("Abos", 160, ROT), ("Rest", 90, GRUEN)]))
KURVE = svg("m2", f'<path d="M0 500 L800 500" stroke="#ffffff33" stroke-width="5"/><path id="m2-l" d="M10 490 C300 480 480 380 600 230 C680 130 740 70 790 20" fill="none" '
                  f'stroke="{GRUEN}" stroke-width="16" stroke-linecap="round" {GL(GRUEN)}/>', 140, 820, 800, 500, "0 0 800 500")
KACHELN = "".join(f'<div class="kc" style="position:absolute;left:{190 + (i % 10) * 72}px;top:{790 + (i // 10) * 72}px;width:60px;height:60px;border-radius:12px;'
                  f'background:{[OR, GRUEN, "#4d8ff0", GOLD][(i * 7) % 4]};box-shadow:0 0 18px #0008;z-index:2"></div>' for i in range(80))
PROZENT = (f'<div id="m4" style="position:absolute;left:0;top:830px;width:1080px;text-align:center;font-weight:900;font-size:300px;line-height:1;color:{GRUEN};'
           f'text-shadow:0 0 80px {GRUEN};z-index:2">0 %</div>' + t("m4-u", "pro Jahr im Schnitt*", 1160, 56) + t("m4-s", "*historisch, keine Garantie", 1250, 36))
WARN = svg("m5", f'<path d="M250 30 L480 440 L20 440 Z" fill="none" stroke="{ROT}" stroke-width="26" stroke-linejoin="round" {GL(ROT)}/>'
                 f'<rect x="234" y="160" width="32" height="160" rx="16" fill="{ROT}"/><circle cx="250" cy="380" r="22" fill="{ROT}"/>', 290, 800, 500, 460, "0 0 500 460")
UHR = svg("m6", f'<circle cx="250" cy="250" r="220" fill="none" stroke="{GOLD}" stroke-width="22" {GL(GOLD)}/>'
                + "".join(f'<rect x="244" y="44" width="12" height="36" rx="6" fill="{GOLD}" transform="rotate({i * 30} 250 250)"/>' for i in range(12))
                + f'<rect id="m6-h" x="240" y="120" width="20" height="140" rx="10" fill="#fff"/><rect id="m6-m" x="244" y="70" width="12" height="190" rx="6" fill="{OR}"/>'
                + f'<circle cx="250" cy="250" r="20" fill="#fff"/>', 290, 820, 500, 500, "0 0 500 500")
PFEIL = svg("m8", f'<path d="M150 0 L150 300 M40 200 L150 320 L260 200" fill="none" stroke="{OR}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round" {GL(OR)}/>',
            390, 860, 300, 340, "0 0 300 340")

STATIONEN = [
    (frage(0, 'Wohin geht<br/><span class="box">dein Geld?</span>', "", 450, 112) + EURO,
     lambda a: f'tl.fromTo("#m0", {{ rotationY: -180, transformPerspective: 900 }}, {{ rotationY: 0, duration: 0.8, ease: "back.out(1.4)" }}, {a}); tl.fromTo("#f0", {{ scale: 1.2 }}, {{ scale: 1, duration: 0.3 }}, {a});'),
    (frage(1, "Wo versickert es?") + BALKEN,
     lambda a: f'tl.fromTo("#w1 .bk", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.35, stagger: 0.12, ease: "back.out(1.5)" }}, {a});'),
    (frage(2, "Wie wird es mehr?", "glow-g") + KURVE,
     lambda a: f'draw("#m2-l", {a}, 1.2);'),
    (frage(3, "Was ist ein ETF?") + KACHELN + t("m3-u", "viele Firmen in einem Korb", 1420, 54),
     lambda a: f'tl.fromTo("#w3 .kc", {{ scale: 0, rotation: 90 }}, {{ scale: 1, rotation: 0, duration: 0.25, stagger: {{ each: 0.012, from: "center" }} }}, {a}); pop("#m3-u", {a} + 0.9);'),
    (frage(4, "Wie viel Rendite?", "glow-g") + PROZENT,
     lambda a: f'zaehl("#m4", 0, 7, {a}, 1.0, " %"); pop("#m4-u", {a} + 0.6); pop("#m4-s", {a} + 0.8);'),
    (frage(5, "Wo lauern Fallen?", "glow-r") + WARN,
     lambda a: f'pop("#m5", {a}); shake("#m5", {a} + 0.35); tl.fromTo("#m5", {{ opacity: 1 }}, {{ opacity: 0.4, duration: 0.15, yoyo: true, repeat: 5, {"immediateRender: false"} }}, {a} + 0.8);'),
    (frage(6, "Wann bist du frei?", "glow-o") + UHR,
     lambda a: f'tl.fromTo("#m6-m", {{ rotation: 0, transformOrigin: "50% 100%" }}, {{ rotation: 1080, duration: 2.0, ease: "power2.inOut" }}, {a}); tl.fromTo("#m6-h", {{ rotation: 0, transformOrigin: "50% 100%" }}, {{ rotation: 90, duration: 2.0, ease: "power2.inOut" }}, {a});'),
    (frage(7, 'Wir zeigen<br/><span class="box">es dir.</span>', "", 700, 130) + partikel("m7-p", 540, 900, 30, (OR, GOLD, "#fff"), 700),
     lambda a: f'slam("#f7", {a}); burst("#m7-p", {a} + 0.25);'),
    (frage(8, "Alle Antworten<br/>liegen hier drin", "", 560, 96) + PFEIL,
     lambda a: f'tl.fromTo("#m8", {{ y: -40 }}, {{ y: 40, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {a});'),
]


# ---------- Parallax-Ebenen ----------
def ebene(id_, n, faktor, groesse, alpha):
    zeichen = ["€", "%", "€", "+", "€", "↑"]
    s = "".join(f'<div style="position:absolute;left:{(i * 397) % 980 + 20}px;top:{(i * 733) % int(H * N * faktor + H)}px;font-weight:900;'
                f'font-size:{groesse[0] + (i * 37) % (groesse[1] - groesse[0])}px;color:{[OR, GOLD, "#ffffff"][i % 3]}{alpha};transform:rotate({(i * 23) % 60 - 30}deg)">{zeichen[i % 6]}</div>'
                for i in range(n))
    return f'<div id="{id_}" style="position:absolute;left:0;top:0;width:1080px;height:{int(H * N * faktor + H)}px;z-index:{1 if faktor < 1 else 4}">{s}</div>'


WELT = (ebene("pl-b", 60, 0.45, (40, 90), "22") +
        f'<div id="welt" style="position:absolute;left:0;top:0;width:1080px;height:{H * N}px;z-index:2">'
        + "".join(f'<div id="w{k}" style="position:absolute;left:0;top:{k * H}px;width:1080px;height:{H}px">{html}</div>' for k, (html, _) in enumerate(STATIONEN))
        + '</div>' + ebene("pl-f", 26, 1.6, (120, 220), "30"))


def welt_js(a, d):
    js = []
    for k in range(N):
        an = k * TAKT
        if k:
            js.append(f'tl.to("#welt", {{ y: {-k * H}, duration: {FAHRT}, ease: "power4.inOut" }}, {an - FAHRT:.2f});')
            js.append(f'tl.to("#pl-b", {{ y: {-k * H * 0.45:.0f}, duration: {FAHRT}, ease: "power4.inOut" }}, {an - FAHRT:.2f});')
            js.append(f'tl.to("#pl-f", {{ y: {-k * H * 1.6:.0f}, duration: {FAHRT}, ease: "power4.inOut" }}, {an - FAHRT:.2f});')
            js.append(f'tl.fromTo("#welt", {{ scaleY: 1, rotation: 0 }}, {{ scaleY: 1.06, rotation: {(-1) ** k * 2}, duration: {FAHRT / 2}, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {an - FAHRT:.2f});')
            js.append(f'pop("#f{k}", {an - 0.1:.2f});')
        js.append(STATIONEN[k][1](round(an, 2)))
    return " ".join(js)


# ---------- Tresor ----------
SPEICHEN = "".join(f'<rect x="242" y="90" width="16" height="320" rx="8" fill="#9aa3a8" transform="rotate({i * 45} 250 250)"/>' for i in range(4))
TUER = (f'<div id="ts-t" style="position:absolute;left:190px;top:560px;width:700px;height:700px;border-radius:50%;z-index:4;'
        f'background:radial-gradient(circle at 40% 35%, #4a5257, #23272a 70%);border:24px solid #6c757a;box-shadow:0 0 80px {OR}66, inset 0 0 60px #000;transform-origin:0% 50%">'
        f'<svg id="ts-r" viewBox="0 0 500 500" style="position:absolute;left:75px;top:75px;width:502px;height:502px">'
        f'<circle cx="250" cy="250" r="200" fill="none" stroke="#9aa3a8" stroke-width="20"/>{SPEICHEN}<circle cx="250" cy="250" r="50" fill="{OR}"/></svg></div>')
INNEN = (f'<div id="ts-i" style="position:absolute;left:190px;top:560px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle, {GOLD}cc 0%, {OR}66 45%, #0e1012 75%);z-index:2"></div>'
         + ring("ts-l", f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', 340, 710, 400))
S_TRESOR = (INNEN + TUER + partikel("ts-p", 540, 910, 44, (GOLD, OR, "#fff"), 900) + t("ts-a", "Der Tresor öffnet sich …", 1380, 64) +
            t("ts-w", "Willkommen!", 1380, 130, "glow-o"))
J_TRESOR = lambda a, d: (f'tl.fromTo("#ts-t", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {a}); pop("#ts-a", {a} + 0.2);'  # noqa: E731
                         f' tl.fromTo("#ts-r", {{ rotation: 0 }}, {{ rotation: 540, duration: {AUF - a - 0.4:.2f}, ease: "power2.inOut" }}, {a} + 0.3);'
                         f' tl.fromTo("#ts-t", {{ rotationY: 0, transformPerspective: 1400 }}, {{ rotationY: -105, duration: 0.6, ease: "power3.in", immediateRender: false }}, {AUF} - 0.3);'
                         f' tl.to("#ts-t", {{ opacity: 0, duration: 0.2 }}, {AUF} + 0.3); flash({AUF}); burst("#ts-p", {AUF}, 1.4);'
                         f' tl.fromTo("#ts-l", {{ scale: 0.3 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {AUF}); tl.to("#ts-a", {{ opacity: 0, duration: 0.15 }}, {AUF} - 0.2);'
                         f' slam("#ts-w", {AUF} + 0.2); tl.fromTo(["#logo", "#brand"], {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2, immediateRender: false }}, {AUF} - 0.2);')

RING = ring("ou-r", f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', 290, 420, 500)
S_OUT = (RING + buchstaben("ou-n", "HundeFinanzTv", 1000, 104, "glow-o") + t("ou-u", "jeden Tag neue Videos rund ums Geld", 1150, 46) +
         chip("ou-f", "+ Folgen", OR, 1280, 84))
J_OUT = lambda a, d: (f'pop("#ou-r", {a}); letters("#ou-n", {a} + 0.1); pop("#ou-u", {a} + 0.6); slam("#ou-f", {a} + 0.9);'  # noqa: E731
                      f' tl.fromTo("#ou-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.3);')

SZENEN = [
    (0.0, TRESOR, WELT, welt_js),
    (TRESOR, 26.0, S_TRESOR, J_TRESOR),
    (26.0, DAUER, S_OUT, J_OUT),
]

SFX = ([(0.0, "boom"), (0.1, "whoosh")] + [(k * TAKT - FAHRT, "whoosh") for k in range(1, N)] +
       [(TAKT + 0.1, "pop"), (TAKT + 0.22, "pop"), (TAKT + 0.34, "pop"), (2 * TAKT + 1.2, "ding"), (3 * TAKT + 0.5, "kasse"),
        (4 * TAKT, "tick"), (4 * TAKT + 0.15, "tick"), (4 * TAKT + 0.3, "tick"), (4 * TAKT + 1.0, "ding"), (5 * TAKT + 0.3, "boom"),
        (7 * TAKT, "boom"), (TRESOR, "whoosh")] + [(TRESOR + 0.3 + i * 0.12, "tick") for i in range(7)] +
       [(AUF, "boom"), (AUF + 0.05, "kasse"), (AUF + 0.2, "ding"), (26.0, "whoosh"), (26.9, "pop")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX, dauer=DAUER, musik=beat(DAUER, pausen=[(19.2, AUF)], seed=9))
