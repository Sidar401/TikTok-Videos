#!/usr/bin/env python3
"""HundeFinanzTV: Dein Handyvertrag ist zu teuer (Teilen-CTA). Leitmotiv: zwei Rechnungen „Vertrag“ vs. „Einzeln“ im Duell."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import CHECK, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402
from icons import TEILEN  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}
GRUEN, ROT, OR = "#1f7a4d", "#e24b4b", "#DB8622"


def c(sid, i):
    return cap(t, sid, i)


def big(id_, txt, top, size=120, col="#111"):
    return f'<div id="{id_}" class="big" style="position:absolute;left:0;top:{top}px;width:1080px;font-size:{size}px;line-height:1.05;color:{col}">{txt}</div>'


def handy(screen="", w=300):
    return f"""<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" />
  <rect x="22" y="40" width="256" height="480" rx="20" fill="#fff" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" />{screen}</svg>"""


def rechnung(zeile, betrag, col):
    return (f'<text x="150" y="120" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#888">{zeile}</text>'
            f'<text x="150" y="200" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="36" fill="{col}">{betrag}</text>'
            '<rect x="50" y="300" width="200" height="14" rx="7" fill="#eee" /><rect x="50" y="335" width="160" height="14" rx="7" fill="#eee" />')


SIM = f"""<svg viewBox="0 0 200 260" style="width:100%;height:100%">
  <path d="M20 10 L140 10 L190 60 L190 250 L20 250 Z" fill="{OR}" />
  <rect x="55" y="90" width="100" height="120" rx="14" fill="#f2c418" stroke="#c99a06" stroke-width="5" />
  <path d="M55 130 L155 130 M55 170 L155 170 M105 90 L105 210" stroke="#c99a06" stroke-width="5" /></svg>"""

PREIS = f"""<svg viewBox="0 0 400 200" style="width:100%;height:100%">
  <path d="M10 60 L270 60 L380 100 L270 140 L10 140 Z" fill="{GRUEN}" /><circle cx="300" cy="100" r="12" fill="#fff" />
  <text x="140" y="118" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="56" fill="#fff">700 €</text></svg>"""


def spalte(id_, kopf, zeilen, summe, col, x):
    z = "".join(f'<div id="{id_}-z{i}" style="display:flex;justify-content:space-between;font-family:Montserrat;font-weight:700;font-size:36px;white-space:nowrap;color:#353a3d">'
                f'<span>{a}</span><span>{b}</span></div>' for i, (a, b) in enumerate(zeilen))
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:340px;width:470px;padding:36px 30px;border-radius:30px;background:#faf5ef;'
            f'border-top:16px solid {col};display:flex;flex-direction:column;gap:22px">'
            f'<div style="font-family:Montserrat;font-weight:800;font-size:54px;color:{col}">{kopf}</div>{z}'
            f'<div style="height:5px;background:#353a3d"></div>'
            f'<div id="{id_}-s" class="big" style="font-size:96px;color:{col};text-align:right">{summe}</div></div>')


SCENES = [
    ("hook", "s1", "s2",
     title("hk-t", 'Dein Handyvertrag<br />ist <span style="color:#e24b4b">zu teuer</span>', 290, 84) +
     box("hk-h", 390, 600, 300, 560, handy(rechnung("Rechnung", "50 € / Monat", ROT))),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-h", t0) +
     f'\n      tl.fromTo("#hk-h", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {S["s2"]["start"]});'),

    ("vertrag", "s3", "s4",
     box("vt-h", 390, 330, 300, 560, handy(rechnung("Vertrag", "50 €", "#111"))) +
     big("vt-x", "× 24 Monate", 920, 80, "#555c60") +
     big("vt-n", "1.200 €", 1030, 150, ROT),
     lambda t0, d: f"""
      pop("#vt-h", {t0});
      pop("#vt-x", {S['s4']['start']});
      pop("#vt-n", {c('s4', 1)} - 0.3);
      zaehl("#vt-n", 50, 1200, {c('s4', 1)} - 0.3, 1.2, " €");"""),

    ("laden", "s5", "s5",
     box("la-h", 160, 360, 300, 560, handy()) +
     box("la-p", 480, 520, 480, 240, PREIS) +
     big("la-t", "im Laden", 980, 96, GRUEN),
     lambda t0, d: f"""
      pop("#la-h", {t0});
      pop("#la-p", {c('s5', 1)});
      tl.fromTo("#la-p", {{ rotation: -6 }}, {{ rotation: 0, duration: 0.4, ease: "back.out(3)" }}, {c('s5', 1)});
      pop("#la-t", {c('s5', 1)} + 0.2);"""),

    ("alternative", "s6", "s7",
     big("al-t", "Die Alternative", 300, 100, GRUEN) +
     box("al-h", 180, 470, 260, 485, handy()) +
     big("al-p", "+", 600, 160) +
     box("al-s", 640, 520, 260, 338, SIM) +
     big("al-n", "ab 10 € / Monat", 1030, 84, OR),
     lambda t0, d: f"""
      pop("#al-t", {t0});
      pop("#al-h", {c('s6', 1)});
      pop("#al-p", {c('s6', 2)} - 0.2);
      pop("#al-s", {c('s6', 2)});
      pop("#al-n", {c('s7', 1)});"""),

    ("duell", "s8", "s10",
     spalte("dv", "Vertrag", [("50 € × 24", "1.200 €")], "1.200 €", ROT, 50) +
     spalte("de", "Einzeln", [("Tarif 10 € × 24", "240 €"), ("Handy", "700 €")], "940 €", GRUEN, 560) +
     f'<div id="du-g" style="position:absolute;left:140px;top:960px;width:800px;display:flex;align-items:center;justify-content:center;gap:24px;'
     f'padding:24px;border-radius:30px;background:{GRUEN}"><div style="width:100px;height:100px">{CHECK.replace("#1f7a4d", "#fff").replace("stroke=\"#fff\"", "stroke=\"#1f7a4d\"")}</div>'
     f'<span style="font-family:Montserrat;font-weight:800;font-size:72px;color:#fff">+260 € gespart</span></div>',
     lambda t0, d: f"""
      pop("#dv", {t0});
      pop("#de", {t0} + 0.2);
      tl.fromTo("#de-z0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {c('s8', 1)});
      tl.fromTo("#de-z1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {c('s8', 2)});
      tl.fromTo("#de-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {S['s9']['start']});
      tl.fromTo("#de-s", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }}, {S['s9']['start']} + 0.4);
      pop("#du-g", {S['s10']['start']});"""),

    ("laenger", "s11", "s11",
     box("lg-h", 390, 330, 300, 560, handy(rechnung("noch 1 Jahr", "weiter nutzen", GRUEN))) +
     big("lg-t", "= noch mehr<br />gespart", 940, 100, GRUEN),
     lambda t0, d: f"""
      pop("#lg-h", {t0});
      tl.fromTo("#lg-h", {{ rotation: 0 }}, {{ rotation: 360, duration: 0.8, ease: "power2.inOut" }}, {c('s11', 1)});
      pop("#lg-t", {c('s11', 2)});"""),

    ("teilen", "s12", "s13",
     box("te-i", 340, 380, 400, 400, TEILEN) +
     big("te-t", "Schick's jemandem,<br />der gerade wechseln will!", 880, 72, OR),
     lambda t0, d: f"""
      pop("#te-i", {t0});
      tl.fromTo("#te-i", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#te-t", {c('s12', 1)});"""),

    ("outro", "s14", "s14", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
