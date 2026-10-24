#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): 10 Supermarkt-Tricks – Rundgang mit Jana.
Leitmotiv: Supermarkt-Grundriss, Jana läuft von Station zu Station, „Extras im Wagen“ wachsen mit. Beagle nur im CTA."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import BLASE, HANDY, ICON, KAL3, TEILEN, WAGEN, doppel, folgen, person  # noqa: E402
from lf_szenen import Zeit, balken3, chips_zeit, karte  # noqa: E402

Z = Zeit(HERE)
st = Z.st
BLAU, LILA, BRAUN, GRAU = "#3d7be0", "#9b59b6", "#8a5a2b", "#c9c2b6"

# ---------- Icons ----------
GEHIRN = svg('<path d="M50 14 Q30 6 20 22 Q6 26 10 44 Q2 58 16 68 Q18 86 38 84 Q46 94 50 84 Q54 94 62 84 Q82 86 84 68 Q98 58 90 44 Q94 26 80 22 Q70 6 50 14 Z" fill="#f4a6b8" stroke="#c0607a" stroke-width="4" />'
             '<path d="M50 16 L50 84 M30 34 Q40 40 32 50 M70 34 Q60 40 68 50 M28 62 Q38 60 40 70 M72 62 Q62 60 60 70" fill="none" stroke="#c0607a" stroke-width="3" stroke-linecap="round" />')
APFEL = svg('<path d="M50 30 Q30 14 16 32 Q4 52 20 76 Q34 96 50 86 Q66 96 80 76 Q96 52 84 32 Q70 14 50 30 Z" fill="#e24b4b" /><path d="M50 30 Q52 16 60 8" fill="none" stroke="#8a5a2b" stroke-width="5" stroke-linecap="round" />'
            '<path d="M54 18 Q70 8 78 20 Q64 26 54 18 Z" fill="#2c9a63" /><ellipse cx="34" cy="44" rx="7" ry="11" fill="#fff" opacity="0.5" /><circle cx="70" cy="60" r="3" fill="#cfe6f5" /><circle cx="62" cy="72" r="2.5" fill="#cfe6f5" />')
CROISSANT = svg('<path d="M10 70 Q20 30 50 26 Q80 30 90 70 Q78 62 70 66 Q62 50 50 50 Q38 50 30 66 Q22 62 10 70 Z" fill="#e0a050" stroke="#a8621a" stroke-width="3" />'
                '<path d="M30 66 Q34 44 50 42 M70 66 Q66 44 50 42 M50 26 L50 50" fill="none" stroke="#a8621a" stroke-width="3" /><path d="M30 18 Q34 10 30 4 M50 16 Q54 8 50 2 M70 18 Q74 10 70 4" fill="none" stroke="#9aa3a8" stroke-width="3" stroke-linecap="round" />')
NOTE = svg('<circle cx="30" cy="74" r="12" fill="#353a3d" /><circle cx="72" cy="64" r="12" fill="#353a3d" /><rect x="38" y="20" width="6" height="56" fill="#353a3d" /><rect x="80" y="10" width="6" height="56" fill="#353a3d" />'
           '<path d="M38 20 L86 10 L86 22 L38 32 Z" fill="#353a3d" />')
SCHOKO = svg('<rect x="14" y="20" width="72" height="62" rx="6" fill="#6b3f1f" />' + "".join(f'<rect x="{20 + (i % 3) * 22}" y="{26 + (i // 3) * 18}" width="18" height="14" rx="2" fill="#8a5a2b" />' for i in range(9)) +
             '<path d="M14 54 L86 54 L86 82 L14 82 Z" fill="#e24b4b" /><text x="50" y="74" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="14" fill="#fff">SCHOKO</text>')
APP = svg('<rect x="26" y="4" width="48" height="92" rx="9" fill="#353a3d" /><rect x="31" y="14" width="38" height="70" rx="3" fill="#fff" />'
          '<text x="50" y="44" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#e24b4b">−10 %</text>'
          '<ellipse cx="50" cy="64" rx="13" ry="8" fill="none" stroke="#353a3d" stroke-width="3" /><circle cx="50" cy="64" r="4" fill="#353a3d" />')
KORB = svg('<path d="M14 40 L86 40 L78 88 L22 88 Z" fill="#DB8622" /><path d="M28 40 Q50 4 72 40" fill="none" stroke="#353a3d" stroke-width="6" />' + "".join(
    f'<line x1="{30 + i * 14}" y1="46" x2="{32 + i * 12}" y2="84" stroke="#a8621a" stroke-width="3" />' for i in range(4)))
TELLER = svg('<ellipse cx="50" cy="60" rx="42" ry="24" fill="#fff" stroke="#353a3d" stroke-width="4" /><ellipse cx="50" cy="58" rx="26" ry="13" fill="#e9b97a" />'
             '<path d="M38 52 Q50 44 62 52" fill="none" stroke="#a8621a" stroke-width="3" /><path d="M10 20 L10 40 M16 20 L16 40 M22 20 L22 40 M16 40 L16 70" stroke="#9aa3a8" stroke-width="3" stroke-linecap="round" />')
ZETTEL_L = svg('<rect x="18" y="4" width="64" height="92" rx="4" fill="#fffbe6" stroke="#353a3d" stroke-width="3" />' + "".join(
    f'<path d="M26 {20 + i * 15} l4 4 l7 -9" fill="none" stroke="#1f7a4d" stroke-width="3" stroke-linecap="round" /><rect x="42" y="{18 + i * 15}" width="{30 - (i % 2) * 8}" height="4" rx="2" fill="#555c60" />' for i in range(5)))
POKAL = svg('<path d="M28 10 L72 10 L70 40 Q66 58 50 60 Q34 58 30 40 Z" fill="#f2c418" stroke="#c99a06" stroke-width="3" /><path d="M28 16 Q10 16 14 32 Q18 42 30 40 M72 16 Q90 16 86 32 Q82 42 70 40" fill="none" stroke="#c99a06" stroke-width="4" />'
            '<rect x="44" y="60" width="12" height="16" fill="#c99a06" /><rect x="30" y="76" width="40" height="12" rx="3" fill="#8a5a2b" />')
JANA = person(LILA, "#a8321f")

# ---------- Leitmotiv: Grundriss ----------
STATION = {0: (95, 670), 1: (95, 610), 2: (130, 470), 3: (130, 230), 4: (500, 115), 5: (350, 330), 6: (470, 330), 7: (590, 330), 8: (590, 470), 9: (560, 625), 10: (700, 625)}
KARTE = svg(
    '<rect x="6" y="6" width="768" height="708" rx="18" fill="#faf5ef" stroke="#353a3d" stroke-width="8" /><rect x="40" y="700" width="110" height="20" fill="#fff" />'
    '<text x="95" y="700" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#353a3d">Eingang ↑</text>'
    '<rect x="36" y="360" width="190" height="200" rx="12" fill="#bfe3c8" /><text x="131" y="390" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#1f7a4d">Obst &amp; Gemüse</text>'
    '<rect x="36" y="130" width="190" height="200" rx="12" fill="#f1d9b5" /><text x="131" y="160" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#8a5a2b">Bäckerei</text>'
    '<rect x="270" y="30" width="470" height="60" rx="10" fill="#cfe6f5" /><text x="505" y="68" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#3d7be0">Kühlregal: Milch · Butter · Eier</text>'
    + "".join(f'<rect x="{290 + i * 125}" y="170" width="70" height="{340 if i < 3 else 200}" rx="8" fill="#d9d2c7" />' for i in range(4))
    + '<rect x="470" y="580" width="280" height="22" rx="6" fill="#353a3d" /><text x="610" y="690" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#353a3d">Kasse</text>'
    '<rect x="520" y="650" width="60" height="16" rx="4" fill="#555c60" /><rect x="660" y="650" width="60" height="16" rx="4" fill="#555c60" />',
    vb="0 0 780 720")


def plan(uid, station, zeilen, extras=(), neu=(), von=None):
    """Grundriss links (780×720), Jana läuft von `von` (Standard: station-1) zur Station; rechts Zeilen [(text, sid, art)].
    extras: schon im Wagen (Chips); neu: [(text, sid)] kommen in dieser Szene dazu."""
    von = station - 1 if von is None else von
    marken = "".join(
        f'<div style="position:absolute;left:{x - 24}px;top:{y - 24}px;width:48px;height:48px;border-radius:50%;'
        f'background:{ROT if n == station else (ORANGE if n < station else "#fff")};border:4px solid {"#353a3d" if n <= station else GRAU};'
        f'color:{"#fff" if n <= station else GRAU};font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center">{n}</div>'
        for n, (x, y) in STATION.items() if n > 0)
    x0, y0 = STATION[max(von, 0)]
    jana = (f'<div id="{uid}-j" style="position:absolute;left:{x0 - 48}px;top:{y0 - 118}px;width:96px;height:122px;z-index:3">'
            f'<div id="{uid}-jb" style="width:100%;height:100%">{JANA}</div></div>')
    stil = {"h": "font-family:'Abril Fatface',serif;font-size:92px;line-height:1.05;color:#111",
            "s": "font-weight:800;font-size:50px;line-height:1.2;color:#353a3d",
            "k": "font-weight:700;font-size:40px;line-height:1.25;color:#555c60",
            "r": "font-weight:800;font-size:50px;line-height:1.2;color:#e24b4b",
            "g": "font-weight:800;font-size:50px;line-height:1.2;color:#1f7a4d"}
    rechts = "".join(f'<div id="{uid}-z{k}" style="{stil[a]}">{t}</div>' for k, (t, _, a) in enumerate(zeilen))
    alle = list(extras) + [t for t, _ in neu]
    wagen = ""
    if alle:
        chips = "".join(f'<span id="{uid}-e{k}" style="display:inline-block;margin:6px;padding:8px 22px;border-radius:30px;background:{ROT};color:#fff;font-weight:800;font-size:34px">{t}</span>'
                        for k, t in enumerate(alle))
        wagen = (f'<div style="position:absolute;left:980px;top:700px;width:840px"><div style="font-weight:800;font-size:34px;color:#353a3d;margin-bottom:4px">'
                 f'Extra im Wagen (nicht auf dem Zettel):</div>{chips}</div>')
    html = (f'<div style="position:absolute;left:110px;top:120px;width:780px;height:720px">{KARTE}{marken}{jana}</div>'
            f'<div style="position:absolute;left:980px;top:130px;width:840px;height:560px;display:flex;flex-direction:column;justify-content:center;gap:22px">{rechts}</div>{wagen}')

    def js(t0, d):
        x1, y1 = STATION[station]
        out = [f'tl.fromTo("#{uid}-j", {{ x: 0, y: 0 }}, {{ x: {x1 - x0}, y: {y1 - y0}, duration: 1.4, ease: "power2.inOut" }}, {t0} + 0.2);',
               f'tl.fromTo("#{uid}-jb", {{ y: 0 }}, {{ y: -10, duration: 0.18, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {t0} + 0.2);']
        for k, (_, sid, _) in enumerate(zeilen):
            a = st(sid) if sid else t0
            out.append(f'tl.fromTo("#{uid}-z{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {max(a, t0 + 0.1)});')
        for k, (_, sid) in enumerate(neu):
            out.append(f'pop("#{uid}-e{len(extras) + k}", {st(sid) + 0.8});')
        return " ".join(out)
    return dict(html=html, js=js)


def intro():
    html = ('<div class="mitte" style="flex-direction:row;gap:80px">'
            f'<div id="in-w" style="width:480px;height:480px">{WAGEN}</div>'
            '<div style="text-align:left"><div id="in-t1" class="serif" style="font-size:150px;line-height:1;color:#111">10 Supermarkt-</div>'
            '<div id="in-t2" class="serif" style="font-size:150px;line-height:1;color:#e24b4b">Tricks</div>'
            '<div id="in-t3" style="font-weight:800;font-size:64px;color:#353a3d;margin-top:20px">die dich jedes Jahr Geld kosten</div></div></div>')

    def js(t0, d):
        return "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-w", "in-t1", "in-t2", "in-t3"))
    return dict(html=html, js=js)


def jana_zettel():
    items = ["Nudeln", "Tomaten", "Käse", "Milch", "Salat"]
    zettel = ('<div id="jz-z" style="width:520px;padding:40px 50px;background:#fffbe6;border:4px solid #353a3d;border-radius:10px;transform:rotate(-3deg)">'
              '<div style="font-weight:800;font-size:46px;color:#a8621a;margin-bottom:16px">Janas Zettel</div>'
              + "".join(f'<div id="jz-{i}" style="font-weight:700;font-size:48px;color:#111;padding:6px 0;border-bottom:2px dashed #d9cbb8">☐ {t}</div>' for i, t in enumerate(items)) + '</div>')
    html = (f'<div class="mitte" style="flex-direction:row;gap:120px"><div id="jz-p" style="display:flex;flex-direction:column;align-items:center;gap:16px">'
            f'<div style="width:320px;height:410px">{JANA}</div><div class="chip" style="background:{LILA}">Jana</div></div>{zettel}</div>')
    return dict(html=html, js=lambda t0, d: f'pop("#jz-p", {t0}); pop("#jz-z", {st("s11")});' + "".join(f' pop("#jz-{i}", {st("s11")} + {0.5 + i * 0.35:.2f});' for i in range(5)))


def wagen_vergleich():
    def w(gr, lab, farbe):
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px"><div style="width:{gr}px;height:{gr}px;position:relative">{WAGEN}'
                f'<div style="position:absolute;left:38%;top:20%;display:flex;gap:6px">' + "".join(f'<div style="width:{gr // 12}px;height:{gr // 12}px;border-radius:4px;background:{c}"></div>' for c in (ROT, GRUEN, ORANGE)) +
                f'</div></div><div class="chip" style="background:{farbe}">{lab}</div></div>')
    html = f'<div class="mitte" style="flex-direction:row;align-items:flex-end;gap:120px"><div id="wv-a">{w(240, "früher", BLAU)}</div><div id="wv-b">{w(480, "heute", ROT)}</div></div>'
    return dict(html=html, js=lambda t0, d: f'pop("#wv-a", {t0}); pop("#wv-b", {t0} + 0.6); tl.fromTo("#wv-b", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.3, yoyo: true, repeat: 1 }}, {st("s23")});')


def regal():
    boden = [("oben: Premium", "4,29 €", "#555c60", None), ("Augenhöhe: Marke", "3,49 €", ROT, "s45"),
             ("Kinderhöhe: Süßes & Müsli", "2,99 €", LILA, "s48"), ("unten: Eigenmarke", "1,79 €", GRUEN, "s47")]
    zeilen = "".join(f'<div id="rg-{i}" style="display:flex;justify-content:space-between;align-items:center;width:1100px;padding:22px 40px;border-bottom:16px solid #8a5a2b;background:#faf5ef">'
                     f'<span style="font-weight:800;font-size:52px;color:{c}">{t}</span><span class="serif" style="font-size:64px;color:{c}">{p}</span></div>'
                     for i, (t, p, c, _) in enumerate(boden))
    html = f'<div class="mitte"><div style="border-left:16px solid #8a5a2b;border-right:16px solid #8a5a2b">{zeilen}</div></div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#rg-{i}", {st(s) if s else t0});' for i, (_, _, _, s) in enumerate(boden)))


def preisschild():
    html = ('<div class="mitte" style="flex-direction:row;gap:90px">'
            '<div id="ps-a" style="padding:40px 70px;background:#f2c418;border:8px solid #111;border-radius:24px;transform:rotate(-4deg)">'
            '<span class="serif" style="font-size:240px;line-height:1;color:#111">4,<span style="font-size:150px;vertical-align:top">99</span></span></div>'
            '<div id="ps-p" class="serif" style="font-size:140px;color:#DB8622">→</div>'
            '<div id="ps-b" style="text-align:center"><div style="font-weight:800;font-size:56px;color:#555c60">gefühlt</div>'
            '<div class="serif" style="font-size:200px;line-height:1;color:#e24b4b">4 €</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#ps-a", {t0}); pop("#ps-p", {st("s52")}); pop("#ps-b", {st("s52")} + 0.4);')


def mogelpackung():
    def pack(i, g, extra=""):
        return (f'<div id="mp-{i}" style="display:flex;flex-direction:column;align-items:center;gap:16px"><div style="width:300px;height:400px;border-radius:20px;background:{ORANGE};'
                f'position:relative;overflow:hidden;border:6px solid #353a3d"><div style="position:absolute;left:0;right:0;bottom:0;height:{g * 0.7:.0f}px;background:#f2c418"></div>'
                f'<div style="position:absolute;top:40px;width:100%;text-align:center;color:#fff;font-weight:900;font-size:60px">MÜSLI</div>'
                f'<div style="position:absolute;bottom:20px;width:100%;text-align:center;font-weight:900;font-size:56px;color:#111">{g} g</div></div>'
                f'<div class="serif" style="font-size:64px;color:#111">2,49 €{extra}</div></div>')
    html = (f'<div class="mitte" style="gap:40px"><div style="display:flex;align-items:flex-end;gap:120px">{pack("a", 500)}{pack("b", 400)}</div>'
            f'<div id="mp-t" class="chip" style="background:{ROT}">+20 % versteckt teurer</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#mp-a", {t0}); pop("#mp-b", {st("s63")}); pop("#mp-t", {st("s64")});')


def gegen(nr, titel):
    return karte(f"Gegentrick {nr}", titel, GRUEN, uid=f"gt{nr}")


EXTRA3 = ["Croissant"]
EXTRA4 = EXTRA3 + ["Chips", "Saft"]
EXTRA7 = EXTRA4 + ["XXL-Käse"]
EXTRA9 = EXTRA7 + ["Schokoriegel"]

KAPITEL = {"k1": "Einstieg", "k2": "Eingang & Gänge", "k3": "Regale & Preise", "k4": "An der Kasse", "k5": "Rechnung & Gegentricks"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s3", "frei", intro()),
    ("s4", "s6", "split", dict(icon=ICON(GEHIRN), text="Kein Zufall – Psychologie", sub="Experten planen jeden Zentimeter", sub_at=st("s6") - st("s4"))),
    ("s7", "s8", "frei", plan("p0", 0, [("Vom Eingang bis zur Kasse", None, "h"), ("ein Trick nach dem anderen", "s8", "r")], von=0)),
    ("s9", "s11", "frei", jana_zettel()),
    ("s12", "s13", "frei", chips_zeit(Z, "ue", "Heute", [("10 Tricks aufdecken", ROT, "s12"), ("Kosten pro Jahr", ORANGE, "s13"), ("Gegentricks", GRUEN, None)])),
    ("s14", "s16", "split", dict(icon=ICON(BLASE), text="Welcher Trick hat dich erwischt?", sub="Merk dir die Nummer!", sub_at=st("s16") - st("s14"))),
    ("s17", "s18", "frei", folgen("+ Folgen")),
    # ---- Eingang & Gänge ----
    ("s19", "s21", "frei", plan("p1", 1, [("Trick 1", "s20", "h"), ("Der Einkaufswagen", "s20", "s"), ("immer größer geworden", "s21", "r")], von=0)),
    ("s22", "s24", "frei", wagen_vergleich()),
    ("s25", "s27", "frei", plan("p2", 2, [("Trick 2", None, "h"), ("Obst & Gemüse vorne", None, "s"), ("bunt, frisch, besprüht", "s26", "k"), ("sogar warmes Licht", "s27", "r")])),
    ("s28", "s30", "split", dict(icon=ICON(APFEL), text="Gutes Gefühl = mehr kaufen", sub="langsamer gehen → mehr sehen → mehr kaufen", sub_at=st("s29") - st("s28"))),
    ("s31", "s33", "frei", plan("p3", 3, [("Trick 3", None, "h"), ("Musik & Duft", None, "s"), ("ruhige Musik → langsamer gehen", "s33", "r")])),
    ("s34", "s36", "split", dict(icon=doppel(CROISSANT, NOTE), text="Duft macht Appetit", sub='<span style="color:#e24b4b">+ Croissant im Wagen</span>', sub_at=st("s36") - st("s34"))),
    ("s37", "s42", "frei", plan("p4", 4, [("Trick 4", None, "h"), ("Milch & Co. ganz hinten", None, "s"), ("vorbei an hunderten Produkten", "s40", "r")],
                                 extras=EXTRA3, neu=[("Chips", "s42"), ("Saft", "s42")])),
    # ---- Regale & Preise ----
    ("s43", "s43", "kapitel", dict(titel="Jetzt wird's <span style=\"color:#e24b4b\">raffiniert</span>")),
    ("s44", "s46", "frei", plan("p5", 5, [("Trick 5", None, "h"), ("Augenhöhe = Kaufhöhe", None, "s"), ("Hersteller zahlen für die besten Plätze", "s46", "r")], extras=EXTRA4)),
    ("s47", "s49", "frei", regal()),
    ("s50", "s50", "frei", plan("p6", 6, [("Trick 6", None, "h"), ("Die magische 99", None, "r")], extras=EXTRA4)),
    ("s51", "s53", "frei", preisschild()),
    ("s54", "s57", "frei", plan("p7", 7, [("Trick 7", None, "h"), ("Mengenangebote", None, "s"), ("3 für 2 · XXL · +20 % gratis", "s55", "r")], extras=EXTRA4, neu=[("XXL-Käse", "s57")])),
    ("s58", "s60", "split", dict(icon=ICON(KORB), text="Großpackung ≠ günstiger", farbe=ROT, sub='<span style="color:#1f7a4d">Profi-Tipp: Grundpreis pro kg prüfen</span>', sub_at=st("s60") - st("s58"))),
    ("s61", "s61", "frei", plan("p8", 8, [("Trick 8", None, "h"), ("Die Mogelpackung", None, "r")], extras=EXTRA7)),
    ("s62", "s65", "frei", mogelpackung()),
    # ---- Kasse ----
    ("s66", "s68", "frei", plan("p9", 9, [("An der Kasse", None, "h"), ("noch 2 Tricks", "s67", "s"), ("Trick 9: Quengelware", "s68", "r")], extras=EXTRA7)),
    ("s69", "s73", "split", dict(icon=ICON(SCHOKO), text="Süßes genau an der Kasse", sub="Wartezeit + Kinderhöhe = Spontankauf", sub_at=st("s70") - st("s69"))),
    ("s74", "s75", "frei", plan("p10", 10, [("Trick 10", None, "h"), ("Kundenkarten & Apps", None, "s"), ("„Haben Sie unsere App?“", "s75", "r")], extras=EXTRA9)),
    ("s76", "s79", "split", dict(icon=ICON(APP), text="Rabatt gegen deine Daten", farbe=ROT, sub="persönliche Angebote locken dich zurück", sub_at=st("s78") - st("s76"))),
    ("s80", "s83", "frei", balken3(Z, "kb", [("geplant", "15 €", 190, GRUEN, None), ("bezahlt", "32 €", 410, ROT, "s82")], "mehr als das Doppelte!", "s83")),
    # ---- Rechnung & Gegentricks ----
    ("s84", "s85", "split", dict(icon=ICON(GEHIRN), text="Viele Käufe: spontan im Laden")),
    ("s86", "s88", "frei", chips_zeit(Z, "re", "Die Rechnung", [("100 € pro Woche", BLAU, "s86"), ("davon 10 % durch Tricks", ORANGE, "s87"), ("= über 500 € im Jahr", ROT, "s88")])),
    ("s89", "s89", "zahl", dict(zahl="1.000 €+", sub="pro Jahr für Familien", farbe=ROT)),
    ("s90", "s91", "split", dict(icon=ICON(POKAL), text="Den Spieß umdrehen: 6 Gegentricks", farbe=GRUEN)),
    ("s92", "s92", "frei", gegen(1, "Nie hungrig einkaufen")),
    ("s93", "s94", "split", dict(icon=ICON(TELLER), text="Satt = weniger Snacks im Wagen", farbe=GRUEN)),
    ("s95", "s95", "frei", gegen(2, "Korb statt Wagen")),
    ("s96", "s96", "split", dict(icon=ICON(KORB), text="Voller Korb = schwer = weniger", farbe=GRUEN)),
    ("s97", "s97", "frei", gegen(3, "Oben & unten schauen")),
    ("s98", "s99", "split", dict(icon=ICON(ZETTEL_L), text="Eigenmarken: oft genauso gut", farbe=GRUEN, sub="im Blindtest kaum ein Unterschied", sub_at=st("s99") - st("s98"))),
    ("s100", "s100", "frei", gegen(4, "Grundpreis vergleichen")),
    ("s101", "s101", "frei", gegen(5, "Einkaufszettel")),
    ("s102", "s102", "split", dict(icon=ICON(ZETTEL_L), text="Nicht auf dem Zettel? Bleibt im Regal!", farbe=GRUEN)),
    ("s103", "s103", "frei", gegen(6, "1× pro Woche einkaufen")),
    ("s104", "s105", "split", dict(icon=KAL3, text="Weniger Besuche = weniger Tricks", farbe=GRUEN, sub="und du sparst Zeit", sub_at=st("s105") - st("s104"))),
    ("s106", "s107", "frei", plan("p11", 9, [("Janas 2. Einkauf", None, "h"), ("satt · Zettel · Korb", None, "g"), ("5 Sachen · 16 € · fertig ✓", "s107", "g")], von=0)),
    ("s108", "s109", "split", dict(icon=ICON(BLASE), text="Welcher Trick hat dich erwischt?", sub="Schreib die Nummer in die Kommentare!", sub_at=st("s109") - st("s108"))),
    ("s110", "s110", "split", dict(icon=doppel(HANDY, TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s111", "s111", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
