#!/usr/bin/env python3
"""HundeFinanzTv Longform 16:9 (Dark Glow): Platzt die KI-Blase? Der KI-Geldkreis und dein ETF (Kommentar-CTA).
Leitbild: KI-Geldkreis aus Firmen-Plaketten (Namen in Firmenfarben, keine echten Logos – Nutzer 6.11.)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import glow_short as g  # noqa: E402

g.querformat()
from finanz import BEAGLE  # noqa: E402
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, partikel, ring, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
BLAU, NV = "#4d8ff0", "#76b900"
GL = lambda f: f'filter="drop-shadow(0 0 18px {f})"'  # noqa: E731


def svg(id_, inhalt, x, y, w, h, vb, z=2):
    return f'<svg id="{id_}" viewBox="{vb}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:{z}">{inhalt}</svg>'


# ---------- Firmen-Plaketten (keine echten Logos) ----------
def _icon(firma):
    if firma == "Microsoft":
        return ('<svg viewBox="0 0 22 22" style="width:46px;height:46px"><rect width="10" height="10" fill="#f25022"/><rect x="12" width="10" height="10" fill="#7fba00"/>'
                '<rect y="12" width="10" height="10" fill="#00a4ef"/><rect x="12" y="12" width="10" height="10" fill="#ffb900"/></svg>')
    if firma == "OpenAI":
        return ('<svg viewBox="0 0 40 40" style="width:48px;height:48px"><g fill="none" stroke="#fff" stroke-width="3.2">'
                + "".join(f'<ellipse cx="20" cy="20" rx="16" ry="7" transform="rotate({a} 20 20)"/>' for a in (0, 60, 120)) + '</g></svg>')
    if firma == "Nvidia":
        return (f'<svg viewBox="0 0 40 30" style="width:54px;height:40px"><path d="M2 15 C10 3 30 3 38 15 C30 27 10 27 2 15 Z" fill="none" stroke="{NV}" stroke-width="4"/>'
                f'<circle cx="20" cy="15" r="6" fill="{NV}"/></svg>')
    if firma == "AMD":
        return '<svg viewBox="0 0 30 30" style="width:40px;height:40px"><path d="M4 4 H26 V26 L18 18 V12 H12 Z" fill="#fff"/><path d="M4 12 L12 20 H4 Z" fill="#fff"/></svg>'
    if firma == "Apple":
        return '<svg viewBox="0 0 30 34" style="width:36px;height:42px"><path d="M15 9 C10 6 3 8 3 18 C3 26 9 33 12 33 C14 33 15 32 15 32 C15 32 16 33 18 33 C21 33 27 26 27 18 C27 8 20 6 15 9 Z" fill="#ddd"/><path d="M15 9 C15 5 17 2 21 1" stroke="#ddd" stroke-width="2.5" fill="none"/></svg>'
    return ""


FARBEN = {"Microsoft": ("#ffffff", "#00a4ef"), "OpenAI": ("#ffffff", "#ffffff"), "Nvidia": (NV, NV), "Oracle": ("#ffffff", "#c74634"),
          "AMD": ("#ffffff", "#e5e5e5"), "Apple": ("#ffffff", "#bbbbbb")}


def plakette(id_, firma, cx, cy, s=1.0, z=3):
    tf, rand = FARBEN[firma]
    name = {"Oracle": "ORACLE", "Nvidia": "NVIDIA", "AMD": "AMD"}.get(firma, firma)
    bg = "#c74634" if firma == "Oracle" else "#111417"
    w, h = 330 * s, 116 * s
    return (f'<div id="{id_}" style="position:absolute;left:{cx - w / 2:.0f}px;top:{cy - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;border-radius:{22 * s:.0f}px;'
            f'background:{bg};border:{5 * s:.0f}px solid {rand};box-shadow:0 0 {40 * s:.0f}px {rand}66;display:flex;align-items:center;justify-content:center;gap:{14 * s:.0f}px;'
            f'z-index:{z}"><div style="transform:scale({s})">{_icon(firma)}</div>'
            f'<span style="font-weight:900;font-size:{50 * s:.0f}px;color:{tf};letter-spacing:{1 if firma in ("Oracle", "Nvidia") else -1}px">{name}</span></div>')


def geldsack(id_, txt, cx, cy, farbe=GOLD, gr=40):
    return (f'<div id="{id_}" style="position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);padding:8px 22px 10px;border-radius:16px;background:{farbe};'
            f'color:#111;font-weight:900;font-size:{gr}px;white-space:nowrap;box-shadow:0 0 30px {farbe}99;z-index:4">{txt}</div>')


def karte(id_, txt, farbe, top, gr=86, w=1300):
    return (f'<div id="{id_}" style="position:absolute;left:{960 - w / 2:.0f}px;top:{top}px;width:{w}px;padding:30px 0 36px;border-radius:30px;background:#16191b;'
            f'border:6px solid {farbe};box-shadow:0 0 60px {farbe}55;text-align:center;font-weight:900;font-size:{gr}px;color:#fff;z-index:2">{txt}</div>')


def regel(n, txt, farbe=OR):
    return (f'<div id="rg{n}" style="position:absolute;left:260px;top:300px;width:1400px;height:380px;border-radius:40px;background:#16191b;border:8px solid {farbe};'
            f'box-shadow:0 0 80px {farbe}55;display:flex;align-items:center;gap:60px;padding:0 70px;z-index:2">'
            f'<div style="flex:none;width:220px;height:220px;border-radius:50%;background:{farbe};color:#111;font-weight:900;font-size:150px;display:flex;align-items:center;justify-content:center">{n}</div>'
            f'<div style="font-weight:900;font-size:92px;line-height:1.05;color:#fff">{txt}</div></div>')


def regel_js(n):
    return lambda a, d: f'tl.fromTo("#rg{n}", {{ x: -1600, rotation: -4 }}, {{ x: 0, rotation: 0, duration: 0.45, ease: "back.out(1.4)" }}, {a});'


PFEIL_AB = (f'<path d="M0 0 L0 120 M-40 80 L0 125 L40 80" fill="none" stroke="{ROT}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------- KI-Geldkreis (s10–s19) ----------
P = {"OpenAI": (960, 250), "Microsoft": (430, 250), "Oracle": (1500, 520), "Nvidia": (960, 760), "AMD": (430, 680)}
KREIS_PF = {
    "p-ms": ("M600 250 L790 250", BLAU),
    "p-or": ("M1130 260 C1330 280 1460 360 1500 455", OR),
    "p-nv": ("M1480 585 C1420 700 1240 760 1130 760", ROT),
    "p-zu": ("M890 700 C800 560 800 420 890 310", NV),
    "p-amd": ("M560 640 C700 500 800 380 880 310", "#e5e5e5"),
}
RZ = svg("rz", f'<g {GL(OR)}>' + "".join(f'<rect x="0" y="{i * 34}" width="150" height="26" rx="6" fill="#23282c" stroke="{OR}" stroke-width="3"/>'
                                         f'<circle cx="18" cy="{i * 34 + 13}" r="5" fill="{GRUEN}"/><rect x="34" y="{i * 34 + 10}" width="90" height="6" rx="3" fill="#ffffff44"/>' for i in range(4)) + '</g>',
         885, 440, 150, 136, "0 0 150 136")
KREIS = (svg("kr-ring", f'<circle cx="960" cy="510" r="420" fill="none" stroke="{OR}" stroke-width="8" stroke-dasharray="30 26" opacity="0.8" {GL(OR)}/>', 0, 0, 1920, 1080, "0 0 1920 1080", 1)
         + svg("kr-pf", "".join(f'<path id="{k}" d="{d}" fill="none" stroke="{f}" stroke-width="12" stroke-linecap="butt" {GL(f)}/>' for k, (d, f) in KREIS_PF.items()),
               0, 0, 1920, 1080, "0 0 1920 1080")
         + "".join(plakette(f"pk-{k.lower()}", k, *xy) for k, xy in P.items())
         + RZ + t("rz-t", "Rechenzentren", 590, 34, "glow-o")
         + geldsack("g-ms", "27 %", 695, 205, BLAU) + geldsack("g-or", "300 Mrd $", 1400, 300, OR) + geldsack("g-nv", "Chips", 1390, 720, ROT)
         + geldsack("g-zu", "100 Mrd $", 760, 520, NV) + geldsack("g-amd", "Deal + Anteile", 600, 470, "#e5e5e5", 32)
         + f'<div id="kr-st" style="position:absolute;left:560px;top:380px;padding:14px 50px;border:12px solid {ROT};border-radius:24px;color:{ROT};font-weight:900;'
           f'font-size:110px;transform:rotate(-8deg);background:#0e1012cc;box-shadow:0 0 60px {ROT}88;z-index:6">VERSPROCHEN</div>')


def kreis_js(a, d):
    js = [
        f'tl.fromTo("#kr-ring", {{ rotation: 0, opacity: 0, transformOrigin: "960px 510px" }}, {{ rotation: 0, opacity: 0, duration: 0.01 }}, {a});',
        f'pop("#pk-openai", {a} + 0.1); tl.fromTo("#pk-openai", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }}, {cap("s10", 2)});',
        f'pop("#rz", {st("s11")} + 0.2); pop("#rz-t", {cap("s11", 2)});',
        f'pop("#pk-microsoft", {st("s12")} + 0.3); draw("#p-ms", {cap("s12", 1)}, 0.4); pop("#g-ms", {cap("s12", 2)});',
        f'pop("#pk-oracle", {cap("s13", 1)}); draw("#p-or", {cap("s13", 2)}, 0.5); slam("#g-or", {cap("s13", 3)});',
        f'pop("#pk-nvidia", {cap("s14", 1)}); draw("#p-nv", {cap("s14", 1)} + 0.4, 0.5); pop("#g-nv", {cap("s14", 2)});',
        f'tl.fromTo("#pk-nvidia", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.2, yoyo: true, repeat: 1 }}, {st("s15")} + 0.3); draw("#p-zu", {cap("s15", 1)}, 0.6); slam("#g-zu", {cap("s15", 2)});',
        f'tl.fromTo("#p-zu", {{ opacity: 1 }}, {{ opacity: 0.35, duration: 0.2, yoyo: true, repeat: 5 }}, {st("s16")} + 0.3);',
        # s17: Kreis leuchtet und dreht sich
        f'tl.fromTo("#kr-ring", {{ opacity: 0, scale: 0.85, transformOrigin: "960px 510px" }}, {{ opacity: 1, scale: 1, duration: 0.5, immediateRender: false }}, {st("s17")});',
        f'tl.fromTo("#kr-ring", {{ rotation: 0 }}, {{ rotation: 360, duration: {st("s19") - st("s17"):.2f}, ease: "none", immediateRender: false }}, {st("s17")});',
        ' '.join(f'tl.fromTo("#{k}", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.18, yoyo: true, repeat: 1 }}, {cap("s17", i)});' for i, k in ((1, "pk-openai"), (2, "pk-oracle"), (4, "pk-nvidia"))),
        f'pop("#pk-amd", {cap("s18", 1)}); draw("#p-amd", {cap("s18", 2)}, 0.5); pop("#g-amd", {cap("s18", 4)});',
        f'tl.to("#kr-pf, #kr-ring", {{ opacity: 0.35, duration: 0.3 }}, {st("s19")} + 0.2); slam("#kr-st", {cap("s19", 2)}); shake("#kr-st", {cap("s19", 2)} + 0.3);',
    ]
    return " ".join(js)


# ---------- weitere Bausteine ----------
CRASH = svg("cr-l", f'<path id="cr-p" d="M0 60 L120 90 L220 50 L330 110 L420 80 L520 140 L560 380 L640 330 L720 520" fill="none" stroke="{ROT}" stroke-width="14" '
                    f'stroke-linejoin="round" stroke-linecap="round" {GL(ROT)}/>', 1180, 260, 600, 560, "0 0 720 540")
DOTCOM = svg("dc", f'<path d="M0 520 L1200 520" stroke="#ffffff33" stroke-width="4"/><path id="dc-l" d="M10 500 C200 480 300 420 420 300 C480 220 520 120 560 60 C600 120 640 260 700 380 '
                   f'C760 470 820 500 900 490 C1000 470 1100 430 1190 400" fill="none" stroke="{OR}" stroke-width="14" stroke-linecap="round" {GL(OR)}/>'
                   f'<text x="560" y="40" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="40" fill="#fff">2000</text>', 360, 280, 1200, 540, "0 0 1200 540")
ERHOL = svg("eh", f'<path d="M0 520 L1300 520" stroke="#ffffff33" stroke-width="4"/><path id="eh-l" d="M10 420 L150 300 L260 430 L380 360 L470 330 L560 480 L660 360 L800 300 L920 230 L1050 170 L1180 90 L1290 40" '
                  f'fill="none" stroke="{GRUEN}" stroke-width="14" stroke-linejoin="round" stroke-linecap="round" {GL(GRUEN)}/>'
                  f'<text x="260" y="490" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="36" fill="{ROT}">Dotcom</text>'
                  f'<text x="560" y="540" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="36" fill="{ROT}">Finanzkrise</text>', 310, 260, 1300, 560, "0 0 1300 560")
GLOBUS = svg("gl", f'<g fill="none" stroke="{BLAU}" stroke-width="10" {GL(BLAU)}><circle cx="200" cy="200" r="180"/><ellipse cx="200" cy="200" rx="80" ry="180"/>'
                   f'<path d="M20 200 H380 M45 110 H355 M45 290 H355"/></g>', 760, 200, 400, 400, "0 0 400 400")
R_D, U_D = 220, 2 * 3.14159 * 220
DONUT = svg("dn", f'<circle cx="250" cy="250" r="{R_D}" fill="none" stroke="#2a3036" stroke-width="90"/>'
                  f'<circle id="dn-u" cx="250" cy="250" r="{R_D}" fill="none" stroke="{BLAU}" stroke-width="96" stroke-dasharray="{U_D * 0.72:.1f} {U_D:.1f}" transform="rotate(-90 250 250)" {GL(BLAU)}/>'
                  f'<text x="250" y="270" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="90" fill="#fff">72 %</text>', 260, 230, 500, 500, "0 0 500 500")
URNE = svg("ur", f'<g {GL(BLAU)}><rect x="40" y="120" width="320" height="260" rx="24" fill="#16191b" stroke="{BLAU}" stroke-width="12"/><rect x="120" y="110" width="160" height="22" rx="8" fill="{BLAU}"/>'
                 f'<rect id="ur-z" x="150" y="10" width="100" height="130" rx="8" fill="#fff"/><text x="200" y="300" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="64" fill="#fff">USA</text></g>',
           300, 250, 400, 400, "0 0 400 400")
BLASE = (f'<div id="bl" style="position:absolute;left:660px;top:200px;width:600px;height:600px;border-radius:50%;z-index:2;'
         f'background:radial-gradient(circle at 35% 30%, #ffffffcc 0 6%, #ff8a1f55 22%, #ff8a1f22 55%, #ff8a1f66 100%);border:6px solid {OR}88;box-shadow:0 0 120px {OR}66;'
         f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:110px;color:#fff;text-shadow:0 4px 0 #000">KI</div>')
KALENDER = (f'<div id="kl" style="position:absolute;left:760px;top:220px;width:400px;height:420px;border-radius:30px;background:#f4f1ea;overflow:hidden;z-index:2;box-shadow:0 0 70px {ROT}55">'
            f'<div style="height:110px;background:{ROT};color:#fff;font-weight:900;font-size:60px;text-align:center;line-height:110px">NOV</div>'
            f'<div style="text-align:center;font-weight:900;font-size:230px;color:#111;line-height:300px">5</div></div>')
NOTGROSCHEN = svg("ng", f'<g {GL(GRUEN)}><rect x="20" y="40" width="360" height="300" rx="30" fill="#16191b" stroke="{GRUEN}" stroke-width="12"/>'
                        f'<circle cx="200" cy="190" r="70" fill="none" stroke="{GRUEN}" stroke-width="12"/><path d="M200 130 V250 M140 190 H260" stroke="{GRUEN}" stroke-width="10"/>'
                        f'<rect x="60" y="340" width="40" height="30" fill="{GRUEN}"/><rect x="300" y="340" width="40" height="30" fill="{GRUEN}"/></g>', 1180, 260, 400, 380, "0 0 400 380")


def balken_h(id_, label, wert, breite, farbe, top):
    return (f'<div class="t" style="left:260px;width:auto;text-align:left;top:{top - 70}px;font-size:48px">{label}</div>'
            f'<div id="{id_}" style="position:absolute;left:260px;top:{top}px;width:{breite}px;height:110px;border-radius:0 24px 24px 0;background:{farbe};'
            f'box-shadow:0 0 50px {farbe}77;transform-origin:0 50%;z-index:2"></div>'
            f'<div id="{id_}-z" class="t" style="left:{280 + breite}px;width:auto;top:{top + 14}px;font-size:70px;color:{farbe};white-space:nowrap">{wert}</div>')


TOP = [("Nvidia", "5,2 %", 520), ("Apple", "5,1 %", 510), ("Microsoft", "3,7 %", 370)]
POSITIONEN = "".join(plakette(f"tp{i}", f, 420, 290 + i * 170, 0.9) +
                     f'<div id="tb{i}" style="position:absolute;left:640px;top:{250 + i * 170}px;width:{w}px;height:80px;border-radius:0 20px 20px 0;background:{OR};'
                     f'box-shadow:0 0 40px {OR}66;transform-origin:0 50%;z-index:2"></div>'
                     f'<div id="tl{i}" class="t" style="left:{660 + w}px;width:auto;top:{252 + i * 170}px;font-size:62px">{p}</div>' for i, (f, p, w) in enumerate(TOP))

BEAGLE_RING = lambda id_, x, y, gr: ring(id_, f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', x, y, gr)  # noqa: E731

S = []


def sz(a, b, html, js):
    S.append((a, b, html, js))


# Hook
sz(0.0, cap("s1", 2), t("h1-z", "−2,5 Billionen $", 330, 170, "glow-r") + chip("h1-c", "an EINEM Tag", ROT, 640, 80),
   lambda a, d: f'tl.fromTo("#h1-z", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.4 }}, {a}); shake("#h1-z", 0.5); pop("#h1-c", {cap("s1", 1)});')
sz(cap("s1", 2), st("s2"), CRASH + "",
   lambda a, d: f'draw("#cr-p", {a}, 1.4); pop("#h2-t", {a} + 0.2);')
S[-1] = (S[-1][0], S[-1][1], CRASH + f'<div id="h2-t" class="t" style="left:140px;width:1000px;top:330px;font-size:120px">Börsenwert<br/><span class="box">VERNICHTET</span></div>', S[-1][3])
sz(st("s2"), st("s3"), t("n-k", "NASDAQ", 250, 110, "glow-o") + t("n-z", "−6,4 %", 400, 260, "glow-r") + chip("n-c", "schlimmster Tag seit Corona 2020", ROT, 730, 64),
   lambda a, d: f'pop("#n-k", {a}); slam("#n-z", {cap("s2", 1)}); shake("#n-z", {cap("s2", 1)} + 0.3); pop("#n-c", {cap("s2", 2)});')
sz(st("s3"), cap("s3", 2), t("ch-k", "Chip-Aktien", 280, 110) + t("ch-z", "−12 %", 430, 280, "glow-r"),
   lambda a, d: f'pop("#ch-k", {a}); slam("#ch-z", {cap("s3", 1)});')
sz(cap("s3", 2), st("s4"), t("dx-k", "DAX", 260, 120, "glow-o") + t("dx-z", "unter 26.000", 430, 170) + svg("dx-p", PFEIL_AB, 1640, 420, 120, 140, "-60 0 120 140"),
   lambda a, d: f'pop("#dx-k", {a}); slam("#dx-z", {cap("s3", 3)}); tl.fromTo("#dx-p", {{ y: -60 }}, {{ y: 30, duration: 0.4, yoyo: true, repeat: 3 }}, {cap("s3", 3)} + 0.2);')
sz(st("s4"), st("s5"), BLASE + partikel("bl-p", 960, 500, 40, (OR, "#fff", GOLD), 700),
   lambda a, d: (f'pop("#bl", {a}); tl.fromTo("#bl", {{ scaleX: 1, scaleY: 1 }}, {{ scaleX: 1.06, scaleY: 0.95, duration: 0.25, yoyo: true, repeat: 7 }}, {a} + 0.3);'
                 f' tl.to("#bl", {{ scale: 1.6, opacity: 0, duration: 0.15 }}, {cap("s4", 1)} + 1.2); burst("#bl-p", {cap("s4", 1)} + 1.2, 1.2); flash({cap("s4", 1)} + 1.2, 0.5);'))
sz(st("s5"), st("s6"), t("e-t", "Und was heißt das für", 300, 100) + t("e-z", '<span class="box">DEINEN ETF?</span>', 470, 170),
   lambda a, d: f'pop("#e-t", {a}); slam("#e-z", {cap("s5", 1)});')
sz(st("s6"), cap("s6", 3), t("ka-t", "Noch nie eine KI-Aktie gekauft?", 380, 100),
   lambda a, d: f'pop("#ka-t", {a});')
ETF_BOX = (f'<div id="eb" style="position:absolute;left:460px;top:190px;width:1000px;height:520px;border-radius:40px;border:8px dashed {OR};z-index:1"></div>'
           f'<div class="t glow-o" style="top:220px;font-size:60px">Dein ETF</div>'
           + plakette("eb1", "Nvidia", 720, 420, 0.85) + plakette("eb2", "Microsoft", 1200, 420, 0.85) + plakette("eb3", "Apple", 960, 600, 0.85))
sz(cap("s6", 3), st("s7"), ETF_BOX + chip("eb-c", "steckst trotzdem drin", OR, 740, 56),
   lambda a, d: f'pop("#eb", {a}); pop("#eb1", {a} + 0.3); pop("#eb2", {a} + 0.5); pop("#eb3", {a} + 0.7); pop("#eb-c", {cap("s6", 4)});')
TITEL_RING = svg("tr", f'<circle cx="960" cy="480" r="380" fill="none" stroke="{OR}" stroke-width="10" stroke-dasharray="36 26" {GL(OR)}/>', 0, 0, 1920, 1080, "0 0 1920 1080", 1)
sz(st("s7"), st("s8"), TITEL_RING + t("ti-a", "DER", 300, 90, "glow-o") + t("ti-b", "KI-GELDKREIS", 400, 190) + chip("ti-c", "+ was du jetzt tun solltest", GRUEN, 680, 56),
   lambda a, d: (f'tl.fromTo("#tr", {{ rotation: 0, transformOrigin: "960px 480px" }}, {{ rotation: 120, duration: {d:.2f}, ease: "none" }}, {a}); pop("#ti-a", {a});'
                 f' slam("#ti-b", {cap("s7", 1)}); pop("#ti-c", {cap("s7", 2)});'))
sz(st("s8"), st("s9"), karte("hw", "Keine Anlageberatung", ROT, 300, 110) + t("hw-t", "nur eine Erklärung, damit du die Nachrichten verstehst", 600, 54),
   lambda a, d: f'pop("#hw", {a} + 0.2); pop("#hw-t", {cap("s8", 2)});')
sz(st("s9"), st("s10"), BEAGLE_RING("fo-r", 790, 110, 340) + t("fo-t", "Folge HundeFinanzTv", 480, 96) + chip("fo-f", "+ Folgen", OR, 640, 70),
   lambda a, d: f'pop("#fo-r", {a}); pop("#fo-t", {cap("s9", 2)}); slam("#fo-f", {cap("s9", 2)} + 0.4); tl.fromTo("#fo-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {cap("s9", 3)});')
# Leitbild
sz(st("s10"), st("s20"), KREIS, kreis_js)
sz(st("s20"), st("s21"), balken_h("bz", "Zusagen", "1,4 Billionen $", 880, ROT, 330) + balken_h("bu", "Umsatz pro Jahr", "50 Mrd $", 42, GRUEN, 640),
   lambda a, d: (f'tl.fromTo("#bz", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.out" }}, {cap("s20", 1)}); pop("#bz-z", {cap("s20", 2)});'
                 f' tl.fromTo("#bu", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, {cap("s20", 4)}); pop("#bu-z", {cap("s20", 4)} + 0.4);'))
sz(st("s21"), st("s22"), t("vg-a", "Als würdest du mit", 240, 80) + t("vg-b", "2.000 € im Monat", 360, 120, "glow-g") + t("vg-c", "Verträge über", 530, 80) + t("vg-d", "700.000 €", 640, 170, "glow-r"),
   lambda a, d: f'pop("#vg-a", {a}); pop("#vg-b", {cap("s21", 1)}); pop("#vg-c", {cap("s21", 2)}); slam("#vg-d", {cap("s21", 3)}); shake("#vg-d", {cap("s21", 3)} + 0.3);')
sz(st("s22"), st("s23"), KALENDER + t("kf-t", "kalte Füße", 700, 110, "glow-o"),
   lambda a, d: f'tl.fromTo("#kl", {{ rotation: -20, scale: 0.5, opacity: 0 }}, {{ rotation: 0, scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {a}); pop("#kf-t", {cap("s22", 1)}); shake("#kf-t", {cap("s22", 1)} + 0.4);')
sz(st("s23"), st("s24"), URNE + t("us-a", "US-Wahlen", 300, 110, "glow-o").replace("left:0;width:1920px", "") + f'<div id="us-b" class="t" style="left:760px;width:1000px;top:480px;font-size:72px">KI-Rechenzentren<br/><span class="box">gebremst?</span></div>',
   lambda a, d: f'pop("#ur", {a}); tl.fromTo("#ur-z", {{ y: -80 }}, {{ y: 60, duration: 0.6, ease: "power2.in" }}, {a} + 0.3); pop("#us-b", {cap("s23", 3)});')
S[-1] = (S[-1][0], S[-1][1], S[-1][2].replace('id="us-a" class="t glow-o" style="top:300px', 'id="us-a" class="t glow-o" style="left:760px;width:1000px;top:300px'), S[-1][3])
PFEILE_RAIN = "".join(svg(f"ra{i}", PFEIL_AB, 200 + i * 220, 150 + (i % 3) * 30, 90, 120, "-60 0 120 140") for i, _ in enumerate(range(7)))
sz(st("s24"), st("s25"), PFEILE_RAIN + t("zw-t", "Zwangsverkäufe", 470, 120, "glow-r") + t("zw-u", "ALLE WOLLEN RAUS", 650, 90),
   lambda a, d: (" ".join(f'tl.fromTo("#ra{i}", {{ y: -300, opacity: 0 }}, {{ y: 40, opacity: 1, duration: 0.5, ease: "power2.in" }}, {a} + {i * 0.12:.2f});' for i in range(7))
                 + f' pop("#zw-t", {a} + 0.2); slam("#zw-u", {cap("s24", 2)}); shake("#zw-u", {cap("s24", 2)} + 0.3);'))
sz(st("s25"), st("s26"), t("ae-t", 'Der Anfang<br/><span class="box">vom Ende?</span>', 300, 150),
   lambda a, d: f'slam("#ae-t", {cap("s25", 1)} - 0.3); shake("#ae-t", {cap("s25", 1)});')
sz(st("s26"), st("s27"), DOTCOM + t("dc-t", "Dotcom-Blase", 190, 70, "glow-o") + t("dc-z", "−80 %", 560, 150, "glow-r"),
   lambda a, d: f'draw("#dc-l", {a} + 0.2, 2.6); pop("#dc-t", {a}); slam("#dc-z", {cap("s26", 3)});')
S[-1] = (S[-1][0], S[-1][1], S[-1][2].replace('id="dc-z" class="t glow-r" style="top:560px', 'id="dc-z" class="t glow-r" style="left:350px;top:560px'), S[-1][3])
sz(st("s27"), st("s28"), t("ue-t", "Der Unterschied: echte Gewinne", 230, 80, "glow-g") + plakette("ue1", "Nvidia", 480, 520) + plakette("ue2", "Microsoft", 960, 520) + plakette("ue3", "Apple", 1440, 520)
   + "".join(geldsack(f"ue-g{i}", "$$$", 480 + i * 480, 680, GRUEN, 60) for i in range(3)),
   lambda a, d: f'pop("#ue-t", {a}); pop("#ue1", {cap("s27", 1)}); pop("#ue2", {cap("s27", 2)}); pop("#ue3", {cap("s27", 2)} + 0.4);'
                + " ".join(f' slam("#ue-g{i}", {cap("s27", 3)} + {i * 0.2:.1f});' for i in range(3)))
sz(st("s28"), st("s29"), t("te-t", "Trotzdem: viele Aktien sind teuer", 250, 80) + chip("te-1", "−20 %", ROT, 470, 130, 560) + chip("te-2", "−30 %", ROT, 470, 130, 1000)
   + t("te-u", "wäre nichts Ungewöhnliches", 720, 70),
   lambda a, d: f'pop("#te-t", {a}); slam("#te-1", {cap("s28", 3)}); slam("#te-2", {cap("s28", 3)} + 0.4); pop("#te-u", {cap("s28", 4)});')
sz(st("s29"), st("s30"), t("di-t", 'Was heißt das für', 280, 110) + t("di-z", '<span class="box">DICH?</span>', 440, 200),
   lambda a, d: f'pop("#di-t", {a}); slam("#di-z", {cap("s29", 1)});')
sz(st("s30"), st("s31"), GLOBUS + t("mw-t", "MSCI World", 640, 130, "glow-o") + chip("mw-c", "beliebtester ETF in Deutschland", OR, 820, 50),
   lambda a, d: f'tl.fromTo("#gl", {{ rotation: -30, scale: 0 }}, {{ rotation: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {a}); pop("#mw-t", {cap("s30", 1)}); pop("#mw-c", {cap("s30", 2)});')
sz(st("s31"), st("s32"), DONUT + f'<div id="us-t" class="t" style="left:860px;width:900px;top:330px;font-size:90px;text-align:left">sind<br/><span class="box">US-Firmen</span></div>'
   + f'<div id="us-w" class="t" style="left:860px;width:900px;top:180px;font-size:56px;text-align:left;color:#ffffffaa">„die ganze Welt“?</div>',
   lambda a, d: (f'pop("#us-w", {a}); tl.fromTo("#dn-u", {{ strokeDashoffset: {U_D * 0.72:.1f} }}, {{ strokeDashoffset: 0, duration: 1.0, ease: "power2.out" }}, {cap("s31", 2)});'
                 f' slam("#us-t", {cap("s31", 3)});'))
sz(st("s32"), cap("s32", 3), POSITIONEN,
   lambda a, d: " ".join(f'pop("#tp{i}", {cap("s32", 1 if i == 0 else 2)} + {i * 0.3:.1f}); tl.fromTo("#tb{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5 }}, {cap("s32", 1 if i == 0 else 2)} + {i * 0.3 + 0.2:.1f}); pop("#tl{i}", {cap("s32", 1 if i == 0 else 2)} + {i * 0.3 + 0.6:.1f});' for i in range(3)))
sz(cap("s32", 3), st("s33"), t("tz-a", "Top 10 Firmen", 280, 100, "glow-o") + t("tz-z", "> 25 %", 420, 230) + t("tz-u", "des ganzen ETFs", 700, 70),
   lambda a, d: f'pop("#tz-a", {a}); slam("#tz-z", {a} + 0.3); pop("#tz-u", {a} + 0.6);')
NINA = (f'<div id="ni" style="position:absolute;left:660px;top:230px;width:600px;padding:40px 0;border-radius:40px;background:#16191b;border:6px solid {OR};box-shadow:0 0 60px {OR}55;text-align:center;z-index:2">'
        f'<div style="width:180px;height:180px;margin:0 auto;border-radius:50%;background:{OR};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:110px;color:#111">N</div>'
        f'<div style="font-weight:900;font-size:90px;color:#fff;margin-top:20px">Nina, 28</div></div>')
sz(st("s33"), st("s34"), NINA, lambda a, d: f'pop("#ni", {a});')
sz(st("s34"), st("s35"), chip("sp-c", "200 € / Monat · seit 5 Jahren", OR, 280, 64) + t("sp-z", "0 €", 430, 220, "glow-g") + t("sp-t", "im Depot", 700, 80),
   lambda a, d: f'pop("#sp-c", {a}); pop("#sp-z", {cap("s34", 3)}); zaehl("#sp-z", 0, 15000, {cap("s34", 3)}, 1.4, " €"); pop("#sp-t", {cap("s34", 4)});')
sz(st("s35"), st("s36"), t("df-k", "KI-Crash, z. B. −25 %", 260, 80, "glow-r") + t("df-z", "15.000 €", 420, 220),
   lambda a, d: (f'pop("#df-k", {a}); tl.fromTo("#df-z", {{ color: "{GRUEN}", textShadow: "0 0 50px {GRUEN}aa" }}, {{ color: "{ROT}", textShadow: "0 0 50px {ROT}aa", duration: 0.3 }}, {cap("s35", 1)});'
                 f' zaehl("#df-z", 15000, 11250, {cap("s35", 1)}, 1.4, " €"); shake("#df-z", {cap("s35", 2)} + 0.6);'))
sz(st("s36"), st("s37"), t("vr-t", "4 REGELN", 200, 150, "glow-o") + "".join(
    f'<div id="vr{i}" style="position:absolute;left:{360 + i * 320}px;top:470px;width:240px;height:240px;border-radius:50%;background:{OR};color:#111;font-weight:900;font-size:150px;'
    f'display:flex;align-items:center;justify-content:center;box-shadow:0 0 60px {OR}88;z-index:2">{i + 1}</div>' for i in range(4)),
   lambda a, d: f'pop("#vr-t", {cap("s36", 1)});' + " ".join(f' pop("#vr{i}", {cap("s36", 1)} + {0.3 + i * 0.25:.2f});' for i in range(4)))
sz(st("s37"), st("s38"), regel(1, "Nicht in Panik<br/>verkaufen", ROT), regel_js(1))
sz(st("s38"), st("s39"), ERHOL + t("eh-t", "Der Weltmarkt hat sich jedes Mal erholt", 170, 60, "glow-g"),
   lambda a, d: f'draw("#eh-l", {a} + 0.2, 4.5); pop("#eh-t", {cap("s38", 3)});')
sz(st("s39"), st("s40"), regel(2, "Sparplan<br/>weiterlaufen lassen", GRUEN), regel_js(2))
sz(st("s40"), st("s41"), chip("an-c", "Kurse fallen", ROT, 230, 70) + t("an-z", "200 € = mehr Anteile", 420, 130, "glow-g") + chip("an-s", "Aktien im Angebot", GOLD, 680, 80),
   lambda a, d: f'pop("#an-c", {a}); slam("#an-z", {cap("s40", 2)}); tl.fromTo("#an-s", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: -4, duration: 0.4, ease: "back.out(2)" }}, {cap("s40", 3)});')
sz(st("s41"), st("s42"), regel(3, "Breiter<br/>streuen", BLAU), regel_js(3))
sz(st("s42"), st("s43"), chip("bs-1", "USA", BLAU, 320, 110, 300) + chip("bs-2", "+ Europa", OR, 320, 110, 760) + chip("bs-3", "+ Schwellenländer", GRUEN, 560, 100)
   + t("bs-t", "weniger abhängig von US-Tech", 780, 60),
   lambda a, d: f'pop("#bs-1", {a}); pop("#bs-2", {cap("s42", 3)}); pop("#bs-3", {cap("s42", 4)}); pop("#bs-t", {cap("s42", 5)});')
sz(st("s43"), cap("s43", 3), regel(4, "Nur Geld für<br/>10+ Jahre", GOLD), regel_js(4))
sz(cap("s43", 3), st("s44"), NOTGROSCHEN + f'<div id="ng-t" class="t" style="left:240px;width:900px;top:360px;font-size:100px">+ Notgroschen<br/><span class="box">auf Tagesgeld</span></div>',
   lambda a, d: f'pop("#ng", {a}); slam("#ng-t", {a} + 0.3);')
KLEIN = (svg("kk-r", f'<circle cx="960" cy="500" r="300" fill="none" stroke="{OR}" stroke-width="8" stroke-dasharray="30 24" {GL(OR)}/>', 0, 0, 1920, 1080, "0 0 1920 1080", 1)
         + plakette("kk1", "OpenAI", 960, 200, 0.8) + plakette("kk2", "Oracle", 1260, 500, 0.8) + plakette("kk3", "Nvidia", 960, 800, 0.8) + plakette("kk4", "Microsoft", 660, 500, 0.8)
         + t("kk-t", "Milliarden im Kreis", 460, 70, "glow-o"))
sz(st("s44"), st("s45"), KLEIN, lambda a, d: (f'tl.fromTo("#kk-r", {{ rotation: 0, transformOrigin: "960px 500px" }}, {{ rotation: 200, duration: {d:.2f}, ease: "none" }}, {a});'
                                            + " ".join(f' pop("#kk{i}", {a} + {0.2 + i * 0.25:.2f});' for i in range(1, 5)) + f' pop("#kk-t", {cap("s44", 2)});'))
sz(st("s45"), st("s46"), t("ob-a", "Blase?", 240, 150, "glow-o") + t("ob-b", "weiß niemand", 420, 100) + chip("ob-c", "aber über deinen ETF bist du dabei", OR, 640, 64),
   lambda a, d: f'pop("#ob-a", {a}); pop("#ob-b", {cap("s45", 1)}); pop("#ob-c", {cap("s45", 2)});')
sz(st("s46"), st("s47"), t("ru-a", "Panik", 250, 140, "glow-r") + t("ru-x", "✕", 210, 220, "glow-r") + t("ru-b", "ruhig bleiben + weitersparen", 560, 90, "glow-g"),
   lambda a, d: f'pop("#ru-a", {a}); slam("#ru-x", {cap("s46", 1)}); pop("#ru-b", {cap("s46", 2)});')
sz(st("s47"), st("sF"), BLASE.replace('id="bl"', 'id="bl2"').replace("left:660px;top:200px;width:600px;height:600px", "left:180px;top:220px;width:520px;height:520px")
   + svg("cm", BLASE_SVG.replace('<svg viewBox="0 0 100 100" style="width:62%;height:62%">', '').replace("</svg>", ""), 1450, 200, 300, 300, "0 0 100 100")
   + f'<div id="ja" style="position:absolute;left:800px;top:520px;padding:20px 60px;border-radius:30px;background:{GRUEN};color:#111;font-weight:900;font-size:100px;z-index:3">JA</div>'
   + f'<div id="nein" style="position:absolute;left:1180px;top:520px;padding:20px 60px;border-radius:30px;background:{ROT};color:#fff;font-weight:900;font-size:100px;z-index:3">NEIN</div>'
   + f'<div id="kq" class="t" style="left:760px;width:1000px;top:260px;font-size:84px">Platzt die Blase?</div>',
   lambda a, d: f'pop("#bl2", {a}); pop("#kq", {cap("s47", 2)}); slam("#ja", {cap("s47", 3)}); slam("#nein", {cap("s47", 3)} + 0.3); pop("#cm", {cap("s47", 4)});')
sz(st("sF"), DAUER, BEAGLE_RING("ou-r", 790, 110, 340) + t("ou-n", "HundeFinanzTv", 480, 110) + chip("ou-f", "+ Folgen", OR, 640, 74),
   lambda a, d: f'pop("#ou-r", {a}); pop("#ou-n", {a} + 0.3); slam("#ou-f", {a} + 0.6); tl.fromTo("#ou-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.0);')

SZENEN = S
SFX = [(a, "whoosh") for a, *_ in S[1:]] + [(0.0, "boom"), (cap("s2", 1), "boom"), (cap("s3", 1), "boom"), (cap("s4", 1) + 1.2, "boom"), (cap("s6", 3) + 0.3, "pop"),
                                            (st("s9") + 0.4, "pop"), (cap("s13", 3), "kasse"), (cap("s15", 2), "kasse"), (cap("s19", 2), "boom"), (cap("s21", 3), "boom"),
                                            (cap("s26", 3), "boom"), (cap("s34", 3) + 1.4, "ding"), (cap("s35", 1), "tick"), (cap("s35", 1) + 0.3, "tick"), (cap("s35", 1) + 0.6, "tick"),
                                            (cap("s47", 3), "pop"), (cap("s47", 3) + 0.3, "pop"), (st("sF") + 0.6, "pop")]

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
