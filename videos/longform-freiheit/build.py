#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): Wie viel Geld, um nie wieder zu arbeiten? – Sophies Bergtour.
Leitmotiv: Freiheits-Berg mit drei Gipfeln und Zwischenstationen, Sophie klettert mit. Beagle nur im CTA."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import BLASE, ICON, RECHNER, TEILEN, folgen, person  # noqa: E402
from lf_szenen import Zeit, balken3, chips_zeit  # noqa: E402

Z = Zeit(HERE)
st = Z.st
BLAU, LILA = "#3d7be0", "#9b59b6"
SOPHIE = person(GRUEN, "#c0603a")

RUCKSACK = svg('<rect x="22" y="22" width="56" height="70" rx="16" fill="#1f7a4d" /><path d="M36 22 Q36 8 50 8 Q64 8 64 22" fill="none" stroke="#145c39" stroke-width="6" />'
               '<rect x="32" y="52" width="36" height="26" rx="6" fill="#2c9a63" /><rect x="46" y="58" width="8" height="6" rx="2" fill="#f2c418" />')

# ---------- Leitmotiv: Berg ----------
ORTE = {"basis": (95, 650), "ruhe": (215, 555), "teilzeit": (315, 440), "pass": (380, 320), "normal": (430, 185),
        "sparsam": (170, 345), "luxus": (660, 75)}
GIPFEL = [("sparsam", "450.000 €", GRUEN), ("normal", "750.000 €", BLAU), ("luxus", "1,2 Mio. €", LILA)]
STATIONEN = [("ruhe", "Ruhe-Hütte"), ("teilzeit", "Teilzeit-Alm"), ("pass", "Selbstläufer-Pass")]
BERG = svg(
    '<rect x="0" y="0" width="800" height="720" fill="#eaf4fb" />'
    '<path d="M0 720 L170 330 L300 520 L430 170 L560 400 L660 60 L800 330 L800 720 Z" fill="#9aa3a8" />'
    '<path d="M0 720 L170 330 L300 520 L430 170 L560 400 L660 60 L800 330 L800 720 Z" fill="none" stroke="#555c60" stroke-width="6" stroke-linejoin="round" />'
    '<path d="M140 400 L170 330 L200 400 L185 390 L170 405 L155 390 Z" fill="#fff" /><path d="M395 250 L430 170 L465 250 L448 240 L430 258 L412 240 Z" fill="#fff" />'
    '<path d="M625 140 L660 60 L700 140 L680 130 L660 150 L642 130 Z" fill="#fff" />'
    '<path d="M0 720 L0 640 Q200 600 400 660 Q600 700 800 640 L800 720 Z" fill="#6fbf86" />'
    '<path d="M95 650 Q160 600 215 555 Q270 500 315 440 Q350 380 380 320 Q410 250 430 185" fill="none" stroke="#DB8622" stroke-width="7" stroke-dasharray="14 12" stroke-linecap="round" />',
    vb="0 0 800 720")


def berg(uid, ort, zeilen, von=None, flaggen=True):
    """Berg links (800×720), Sophie geht von `von` nach `ort`; rechts Zeilen [(text, sid, art)]."""
    von = von or ort
    x0, y0 = ORTE[von]
    x1, y1 = ORTE[ort]
    marker = ""
    for k, lab in STATIONEN:
        x, y = ORTE[k]
        marker += (f'<div style="position:absolute;left:{x + 26}px;top:{y - 26}px;padding:6px 16px;border-radius:16px;background:#fff;border:3px solid #353a3d;'
                   f'font-weight:800;font-size:24px;color:#353a3d;white-space:nowrap">{lab}</div>'
                   f'<div style="position:absolute;left:{x - 14}px;top:{y - 14}px;width:28px;height:28px;border-radius:50%;background:#DB8622;border:4px solid #fff"></div>')
    if flaggen:
        for k, wert, farbe in GIPFEL:
            x, y = ORTE[k]
            marker += (f'<div style="position:absolute;left:{x - 4}px;top:{y - 70}px;width:6px;height:70px;background:#353a3d"></div>'
                       f'<div style="position:absolute;left:{x + 2}px;top:{y - 70}px;padding:6px 14px;background:{farbe};color:#fff;font-weight:900;font-size:26px;white-space:nowrap;'
                       f'border-radius:0 10px 10px 0">{wert}</div>')
    sophie = (f'<div id="{uid}-p" style="position:absolute;left:{x0 - 40}px;top:{y0 - 104}px;width:80px;height:104px;z-index:3">'
              f'<div id="{uid}-pb" style="width:100%;height:100%">{SOPHIE}</div></div>')
    stil = {"h": "font-family:'Abril Fatface',serif;font-size:90px;line-height:1.05;color:#111",
            "s": "font-weight:800;font-size:50px;line-height:1.2;color:#353a3d",
            "k": "font-weight:700;font-size:40px;line-height:1.25;color:#555c60",
            "r": "font-weight:800;font-size:48px;line-height:1.2;color:#e24b4b",
            "g": "font-weight:800;font-size:50px;line-height:1.2;color:#1f7a4d"}
    rechts = "".join(f'<div id="{uid}-z{k}" style="{stil[a]}">{t}</div>' for k, (t, _, a) in enumerate(zeilen))
    html = (f'<div style="position:absolute;left:100px;top:130px;width:800px;height:720px;border-radius:30px;overflow:hidden">{BERG}{marker}{sophie}</div>'
            f'<div style="position:absolute;left:980px;top:140px;width:840px;height:680px;display:flex;flex-direction:column;justify-content:center;gap:22px">{rechts}</div>')

    def js(t0, d):
        out = []
        if (x0, y0) != (x1, y1):
            out.append(f'tl.fromTo("#{uid}-p", {{ x: 0, y: 0 }}, {{ x: {x1 - x0}, y: {y1 - y0}, duration: 1.6, ease: "power2.inOut" }}, {t0} + 0.2);')
            out.append(f'tl.fromTo("#{uid}-pb", {{ y: 0 }}, {{ y: -10, duration: 0.2, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {t0} + 0.2);')
        for k, (_, sid, _) in enumerate(zeilen):
            a = st(sid) if sid else t0
            out.append(f'tl.fromTo("#{uid}-z{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {max(a, t0 + 0.1)});')
        return " ".join(out)
    return dict(html=html, js=js)


def intro():
    pills = "".join(f'<div id="in-{i}" style="padding:16px 50px;border-radius:50px;background:{c};color:#fff;font-weight:900;font-size:80px">{t}</div>'
                    for i, (t, c) in enumerate([("1 Million?", BLAU), ("2 Millionen?", LILA), ("viel weniger?", GRUEN)]))
    html = (f'<div class="mitte" style="gap:60px"><div id="in-t" class="serif" style="font-size:118px;line-height:1.05;color:#111;text-align:center">'
            f'Wie viel Geld, um <span style="color:#1f7a4d">NIE</span><br />wieder zu arbeiten?</div><div style="display:flex;gap:30px">{pills}</div></div>')
    return dict(html=html, js=lambda t0, d: f' tl.fromTo("#in-t", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});'
                + "".join(f' pop("#in-{i}", {st("s2")} + {i * 0.7:.1f});' for i in range(3)))


def sophie_intro():
    fakten = [("28 Jahre", "s12"), ("Erzieherin", "s12"), ("2.400 € netto", "s13"), ("kaum Erspartes", "s13"), ("Bewegung: FIRE", "s16")]
    chips = "".join(f'<div id="so-c{i}" class="chip" style="background:{GRUEN if i == 4 else "#353a3d"}">{t}</div>' for i, (t, _) in enumerate(fakten))
    html = (f'<div class="mitte" style="flex-direction:row;gap:90px"><div id="so-p" style="display:flex;flex-direction:column;align-items:center;gap:16px">'
            f'<div style="width:320px;height:420px">{SOPHIE}</div><div class="chip" style="background:{GRUEN}">Sophie</div></div>'
            f'<div style="display:flex;flex-direction:column;align-items:flex-start;gap:22px">{chips}</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#so-p", {t0});' + "".join(f' pop("#so-c{i}", {st(s)} + {(i % 2) * 0.5});' for i, (_, s) in enumerate(fakten)))


def formel():
    teile = [("Ausgaben pro Jahr", BLAU), ("× 25", ORANGE), ("= dein Gipfel", GRUEN)]
    t = "".join(f'<div id="fo-{i}" style="padding:26px 46px;border-radius:30px;background:{c};color:#fff;font-weight:900;font-size:72px">{x}</div>' for i, (x, c) in enumerate(teile))
    html = (f'<div class="mitte" style="gap:50px"><div style="display:flex;gap:30px;align-items:center">{t}</div>'
            f'<div id="fo-s" style="font-weight:800;font-size:56px;color:#353a3d">1 € Ausgaben im Jahr = 25 € Vermögen</div></div>')
    return dict(html=html, js=lambda t0, d: "".join(f' pop("#fo-{i}", {t0} + {0.3 + i * 0.6:.1f});' for i in range(3)) + f' pop("#fo-s", {st("s28")});')


def hebel():
    karten = [("1", "Weniger brauchen", "stärkster Hebel · Wohnen, Auto, Essen", "s80", "s81"), ("2", "Mehr verdienen", "Erhöhungen nicht direkt ausgeben", "s83", "s85"),
              ("3", "Geld arbeiten lassen", "früh starten · breit gestreut", "s86", "s87")]
    k = "".join(f'<div id="he-{i}" style="width:520px;padding:34px 36px;border-radius:30px;background:#faf5ef;border-top:16px solid {c}">'
                f'<div class="serif" style="font-size:90px;color:{c};line-height:1">{n}</div><div style="font-weight:900;font-size:52px;color:#111;margin:10px 0">{t}</div>'
                f'<div id="he-u{i}" style="font-weight:700;font-size:36px;color:#555c60">{u}</div></div>'
                for i, ((n, t, u, _, _), c) in enumerate(zip(karten, (GRUEN, BLAU, ORANGE))))
    html = f'<div class="mitte"><div style="display:flex;gap:36px">{k}</div></div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#he-{i}", {st(a) if i else t0}); pop("#he-u{i}", {st(b)});' for i, (_, _, _, a, b) in enumerate(karten)))


def kuehlschrank():
    berg_mini = svg('<path d="M10 90 L50 15 L90 90 Z" fill="#9aa3a8" stroke="#555c60" stroke-width="3" /><path d="M40 34 L50 15 L60 34 Z" fill="#fff" />', vb="0 0 100 100")
    html = (f'<div class="mitte" style="flex-direction:row;gap:100px"><div id="ks-k" style="position:relative;width:420px;height:640px;border-radius:30px;background:#f4f6f7;border:8px solid #9aa3a8">'
            f'<div style="position:absolute;left:0;right:0;top:210px;height:8px;background:#9aa3a8"></div><div style="position:absolute;right:26px;top:80px;width:14px;height:90px;border-radius:7px;background:#9aa3a8"></div>'
            f'<div style="position:absolute;left:70px;top:260px;width:280px;height:340px;background:#fff;border:4px solid #353a3d;transform:rotate(-3deg)">'
            f'<div style="position:absolute;inset:20px 20px 60px">{berg_mini}</div>'
            f'<div id="ks-f" style="position:absolute;left:46px;bottom:62px;width:24px;height:220px;background:#e24b4b;transform-origin:bottom center;transform:scaleY(0.15)"></div></div></div>'
            f'<div style="display:flex;flex-direction:column;gap:30px;max-width:900px"><div id="ks-t" class="serif" style="font-size:90px;color:#111;line-height:1.05">Sophies Berg am Kühlschrank</div>'
            f'<div id="ks-s" style="font-weight:800;font-size:50px;color:#1f7a4d">jeden Monat ein Stück höher</div>'
            f'<div id="ks-u" style="font-weight:700;font-size:42px;color:#555c60">kleine Rituale halten dich dran</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#ks-k", {t0}); pop("#ks-t", {t0} + 0.3); pop("#ks-s", {t0} + 1.2); tl.to("#ks-f", {{ scaleY: 0.7, duration: 4, ease: "power1.inOut" }}, {t0} + 1.2); pop("#ks-u", {st("s96")});')


KAPITEL = {"k1": "Einstieg", "k2": "Die 4-%-Regel", "k3": "Die 3 Gipfel", "k4": "Zwischenstationen", "k5": "3 Hebel & Sophies Plan"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s2", "frei", intro()),
    ("s3", "s5", "split", dict(icon=ICON(RECHNER), text="Bauchgefühl statt Zahl", sub="dabei: eine überraschend einfache Rechnung", sub_at=st("s4") - st("s3"))),
    ("s6", "s10", "frei", berg("b0", "basis", [("Die Bergtour zur Freiheit", None, "h"), ("Gipfel: dein Geld arbeitet für dich", "s7", "s"),
                                                 ("schon die ersten Etappen verändern dein Leben", "s9", "k"), ("nicht reich geboren? Egal!", "s10", "g")])),
    ("s11", "s16", "frei", sophie_intro()),
    ("s17", "s19", "split", dict(icon=ICON(BLASE), text="Nie wieder arbeiten – was machst du zuerst?", sub="Schreib's in die Kommentare!", sub_at=st("s19") - st("s17"))),
    ("s20", "s21", "frei", folgen("+ Folgen")),
    ("s22", "s22", "split", dict(icon=ICON(RUCKSACK), text="Rucksack auf – ab ins Basislager!", farbe=GRUEN)),
    # ---- 4-%-Regel ----
    ("s23", "s26", "zahl", dict(zahl="4 %", sub="pro Jahr entnehmen – hat historisch 30+ Jahre gereicht", farbe=GRUEN)),
    ("s27", "s29", "frei", formel()),
    ("s30", "s31", "frei", chips_zeit(Z, "bs", "Ein Beispiel", [("750.000 €", BLAU, None), ("4 % = 30.000 € pro Jahr", GRUEN, "s30"), ("der Rest wächst weiter", ORANGE, "s31")])),
    ("s32", "s32", "split", dict(icon=ICON(RUCKSACK), text="Entscheidend: wie viel du BRAUCHST", farbe=GRUEN)),
    ("s33", "s37", "frei", chips_zeit(Z, "vo", "Ehrlich bleiben", [("keine Garantie", ROT, "s33"), ("Steuern & Krankenversicherung", ROT, "s34"),
                                                                  ("lieber 3 – 3,5 % rechnen", ORANGE, "s35"), ("Inflation", ORANGE, "s36"), ("als Kompass top ✓", GRUEN, "s37")])),
    # ---- 3 Gipfel ----
    ("s38", "s38", "frei", berg("b1", "basis", [("Drei Gipfel", None, "h"), ("Sparsam · Normal · Luxus", None, "s")])),
    ("s39", "s45", "frei", berg("b2", "sparsam", [("Gipfel 1: Sparsam", None, "h"), ("1.500 € im Monat", "s40", "s"), ("= 18.000 € im Jahr", "s41", "k"),
                                                     ("× 25 = 450.000 €", "s42", "g"), ("kleine Wohnung · Urlaub in Deutschland", "s44", "k")], von="basis")),
    ("s46", "s49", "frei", berg("b3", "normal", [("Gipfel 2: Normal", None, "h"), ("2.500 € im Monat", "s47", "s"), ("× 25 = 750.000 €", "s48", "g"),
                                                    ("Auto · Urlaub · Freunde & Familie", "s49", "k")], von="sparsam")),
    ("s50", "s53", "frei", berg("b4", "luxus", [("Gipfel 3: Luxus", None, "h"), ("4.000 € im Monat", "s51", "s"), ("= 1,2 Mio. €", "s52", "g"),
                                                   ("nur mit sehr hohem Einkommen", "s53", "r")], von="normal")),
    ("s54", "s56", "frei", balken3(Z, "gi", [("Sparsam", "450.000 €", 200, GRUEN, None), ("Normal", "750.000 €", 330, BLAU, None), ("Luxus", "1,2 Mio. €", 530, LILA, None)],
                                     "über 700.000 € Unterschied", "s55")),
    ("s57", "s59", "zahl", dict(zahl="−100 € / Monat", sub="= 30.000 € weniger, die du brauchst", farbe=GRUEN)),
    # ---- Zwischenstationen ----
    ("s60", "s61", "kapitel", dict(titel='Die <span style="color:#DB8622">Zwischenstationen</span>')),
    ("s62", "s66", "frei", berg("b5", "ruhe", [("Die Ruhe-Hütte", None, "h"), ("6 Monatsausgaben auf der Kante", "s63", "s"), ("Auto kaputt? Kündigung? Kein Drama.", "s64", "k"),
                                                  ("die halbe Freiheit", "s65", "g"), ("Sophie: ≈ 15.000 €", "s66", "s")], von="basis")),
    ("s67", "s71", "frei", berg("b6", "teilzeit", [("Die Teilzeit-Alm", None, "h"), ("Geld deckt einen Teil deiner Kosten", "s68", "s"),
                                                      ("1.000 € im Monat = 300.000 €", "s70", "g"), ("Sophie: 3 Tage pro Woche arbeiten", "s71", "s")], von="ruhe")),
    ("s72", "s77", "frei", berg("b7", "pass", [("Der Selbstläufer-Pass", None, "h"), ("dein Geld wächst allein zum Gipfel", "s73", "s"),
                                                  ("mit 40: 200.000 € → mit 67: über 1 Mio.", "s75", "g"), ("„Coast FIRE“", "s77", "s")], von="teilzeit")),
    # ---- 3 Hebel & Plan ----
    ("s78", "s79", "kapitel", dict(titel='Die <span style="color:#1f7a4d">3 Hebel</span>')),
    ("s80", "s88", "frei", hebel()),
    ("s89", "s94", "frei", chips_zeit(Z, "pl", "Sophies Plan", [("Ziel: 750.000 €", BLAU, "s89"), ("300 € im Monat (12 %)", GRUEN, "s90"), ("Sparrate ↑ bei jedem Gehaltsplus", GRUEN, "s91"),
                                                               ("1. Etappe: Ruhe-Hütte", ORANGE, "s92"), ("nach ≈ 4 Jahren erreicht", ORANGE, "s93")])),
    ("s95", "s97", "frei", kuehlschrank()),
    ("s98", "s101", "frei", berg("b8", "normal", [("Freiheit heißt …", None, "h"), ("arbeiten dürfen – nicht müssen", "s99", "g"), ("Nein sagen können", "s100", "s"),
                                                     ("Zeit – unbezahlbar", "s101", "g")], von="pass")),
    ("s102", "s103", "split", dict(icon=ICON(BLASE), text="Welcher Gipfel ist deiner?", sub="Sparsam, Normal oder Luxus – ab in die Kommentare!", sub_at=st("s103") - st("s102"))),
    ("s104", "s104", "split", dict(icon=ICON(TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s105", "s105", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
