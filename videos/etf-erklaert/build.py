#!/usr/bin/env python3
"""HundeFinanzTV: Was ist ein ETF? (mit Kommentar-CTA)"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CROSS, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


def big(id_, txt, top, size=120, col="#111", left=0, width=1080):
    return f'<div id="{id_}" class="big" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;font-size:{size}px;color:{col}">{txt}</div>'


FARBEN = ["#3d7be0", "#1f7a4d", "#DB8622", "#e24b4b", "#8a5a2b", "#9b59b6", "#f2c418", "#353a3d", "#2c9a63"]


def korb(p, n=0, rot=None):
    """Einkaufskorb; n Aktien-Kästchen darin (id p-k0..), rot = Index eines roten Kästchens."""
    items = ""
    for i in range(n):
        x, y = 95 + (i % 5) * 44, 105 - (i // 5) * 40
        col = "#e24b4b" if i == rot else FARBEN[i % len(FARBEN)]
        items += f'<rect id="{p}-k{i}" x="{x}" y="{y}" width="38" height="34" rx="6" fill="{col}" />'
    return f"""<svg viewBox="0 0 400 300" style="width:100%;height:100%">
  {items}
  <path d="M40 130 L360 130 L325 280 L75 280 Z" fill="#DB8622" />
  <g stroke="#a8621a" stroke-width="8"><line x1="120" y1="150" x2="130" y2="260" /><line x1="200" y1="150" x2="200" y2="260" /><line x1="280" y1="150" x2="270" y2="260" /></g>
  <path d="M90 130 Q200 -10 310 130" fill="none" stroke="#353a3d" stroke-width="14" stroke-linecap="round" />
</svg>"""


AKTIE = """<svg viewBox="0 0 240 300" style="width:100%;height:100%">
  <rect x="10" y="10" width="220" height="280" rx="20" fill="#fff" stroke="#353a3d" stroke-width="8" />
  <text x="120" y="70" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="36" fill="#111">Aktie</text>
  <path d="M40 230 L90 170 L130 200 L200 110" fill="none" stroke="#1f7a4d" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" />
</svg>"""

GLOBUS = """<svg viewBox="0 0 300 300" style="width:100%;height:100%">
  <circle cx="150" cy="150" r="135" fill="#9ed0f0" />
  <path d="M70 80 Q100 60 130 80 Q140 110 110 120 Q90 140 70 120 Z M160 70 Q210 60 230 100 Q220 130 190 125 Q170 110 160 70 Z M120 170 Q160 160 175 195 Q165 240 135 250 Q115 220 120 170 Z M210 170 Q240 165 250 190 Q235 215 215 205 Z" fill="#2c9a63" />
  <circle cx="150" cy="150" r="135" fill="none" stroke="#353a3d" stroke-width="8" />
</svg>"""

PREIS = """<svg viewBox="0 0 400 260" style="width:100%;height:100%">
  <path d="M20 40 L280 40 L380 130 L280 220 L20 220 Z" fill="#1f7a4d" />
  <circle cx="300" cy="130" r="16" fill="#fff" />
  <text x="150" y="155" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="70" fill="#fff">0,2 %</text>
</svg>"""

ZACKEN = """<svg viewBox="0 0 400 320" style="width:100%;height:100%">
  <path d="M30 20 L30 290 L380 290" fill="none" stroke="#111" stroke-width="7" />
  <path id="zk-line" d="M40 250 L70 220 L95 240 L125 190 L150 215 L180 170 L205 200 L235 140 L260 175 L290 110 L315 150 L345 70 L370 90" fill="none" stroke="#1f7a4d" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" />
  <path id="zk-trend" d="M40 255 L370 70" stroke="#DB8622" stroke-width="7" stroke-dasharray="14 12" />
</svg>"""

BLASE = """<svg viewBox="0 0 300 260" style="width:100%;height:100%">
  <path d="M30 20 L270 20 Q290 20 290 40 L290 170 Q290 190 270 190 L120 190 L60 245 L75 190 L30 190 Q10 190 10 170 L10 40 Q10 20 30 20 Z" fill="#fff" stroke="#111" stroke-width="10" stroke-linejoin="round" />
  <circle cx="95" cy="105" r="16" fill="#111" /><circle cx="150" cy="105" r="16" fill="#111" /><circle cx="205" cy="105" r="16" fill="#111" />
</svg>"""


def chip(id_, txt, col="#353a3d"):
    return f'<div id="{id_}" style="padding:26px 60px;border-radius:28px;background:{col};color:#fff;font-family:Montserrat;font-weight:800;font-size:84px">{txt}</div>'


def kal(i):
    return (f'<div id="sp-{i}" style="position:relative;width:150px;height:150px">'
            f'<svg viewBox="0 0 100 100" style="width:100%;height:100%"><rect x="8" y="16" width="84" height="76" rx="12" fill="#fff" stroke="#353a3d" stroke-width="7" /><rect x="8" y="16" width="84" height="24" rx="10" fill="#DB8622" /></svg>'
            f'<div style="position:absolute;left:45px;top:62px;width:60px;height:60px;border-radius:50%;background:#f2c418;border:5px solid #c99a06"></div></div>')


SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Was ist eigentlich<br />ein <span style="color:var(--brand)">ETF</span>?') +
     box("intro-korb", 240, 600, 600, 450, korb("ik", 9)) + big("intro-q", "?", 520, 200, "#e24b4b", 800, 200),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-korb", t0) + f'\n      pop("#intro-q", {t0} + 0.3);'),

    ("korb", "s2", "s2", box("kb-korb", 190, 470, 700, 525, korb("kb")),
     lambda t0, d: f'\n      pop("#kb-korb", {t0});'),

    ("einzeln", "s3", "s3",
     box("ez-aktie", 90, 470, 240, 300, AKTIE) + box("ez-x", 250, 430, 120, 120, CROSS) +
     box("ez-korb", 420, 520, 600, 450, korb("ez", 10)),
     lambda t0, d: f"""
      pop("#ez-aktie", {t0});
      pop("#ez-x", {c('s3', 1)});
      pop("#ez-korb", {c('s3', 2)});
      tl.fromTo("#ez-korb rect", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, stagger: 0.08, ease: "power2.out" }}, {c('s3', 2)} + 0.2);"""),

    ("welt", "s4", "s4",
     box("wt-globus", 290, 340, 500, 500, GLOBUS) + big("wt-num", "1.000+", 880, 150, "#1f7a4d") +
     '<div id="wt-sub" style="position:absolute;left:0;top:1060px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:60px;color:#111">Unternehmen</div>',
     lambda t0, d: f"""
      pop("#wt-globus", {t0});
      tl.fromTo("#wt-globus", {{ rotation: -10 }}, {{ rotation: 10, duration: {d}, ease: "sine.inOut" }}, {t0});
      pop("#wt-num", {c('s4', 2)});
      pop("#wt-sub", {c('s4', 3)});"""),

    ("firmen", "s5", "s5",
     '<div style="position:absolute;left:0;top:450px;width:1080px;display:flex;flex-direction:column;align-items:center;gap:40px">' +
     chip("fm-1", "Apple", "#353a3d") + chip("fm-2", "Microsoft", "#3d7be0") + chip("fm-3", "Nestlé", "#8a5a2b") + "</div>",
     lambda t0, d: "".join(f'\n      pop("#fm-{i}", {c("s5", 0)} + {0.4 + (i - 1) * 0.6:.2f});' for i in (1, 2, 3))),

    ("schlecht", "s6", "s6",
     box("sc-korb", 190, 420, 700, 525, korb("sc", 10, rot=4)) +
     '<svg id="sc-arrow" viewBox="0 0 80 120" style="position:absolute;left:880px;top:380px;width:110px;height:165px"><path d="M40 10 L40 100 M12 72 L40 106 L68 72" fill="none" stroke="#e24b4b" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" /></svg>' +
     big("sc-txt", "kaum Einfluss", 1000, 90, "#1f7a4d"),
     lambda t0, d: f"""
      pop("#sc-korb", {t0});
      pop("#sc-arrow", {t0} + 0.3);
      tl.fromTo("#sc-k4", {{ y: 0 }}, {{ y: 14, duration: 0.15, yoyo: true, repeat: 3 }}, {t0} + 0.4);
      pop("#sc-txt", {c('s6', 1)});"""),

    ("streuung", "s7", "s7",
     big("st-word", "Streuung", 350, 130, "var(--brand)") +
     '<div style="position:absolute;left:240px;top:600px;width:600px;display:grid;grid-template-columns:repeat(5,1fr);gap:20px">' + "".join(
         f'<div class="st-b" style="height:100px;border-radius:16px;background:{FARBEN[i % len(FARBEN)]}"></div>' for i in range(15)) + "</div>",
     lambda t0, d: f"""
      pop("#st-word", {t0});
      tl.fromTo(".st-b", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, stagger: 0.06, ease: "back.out(2)" }}, {t0} + 0.3);"""),

    ("guenstig", "s8", "s8",
     box("gs-tag", 190, 450, 700, 455, PREIS) +
     '<div id="gs-sub" style="position:absolute;left:0;top:960px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:64px;color:#111">Kosten pro Jahr</div>',
     lambda t0, d: f"""
      pop("#gs-tag", {t0});
      tl.fromTo("#gs-tag", {{ rotation: -8 }}, {{ rotation: 0, duration: 0.6, ease: "back.out(3)" }}, {t0});
      pop("#gs-sub", {c('s8', 2)});"""),

    ("sparplan", "s9", "s9",
     big("sp-word", "Sparplan", 350, 120, "#1f7a4d") +
     '<div style="position:absolute;left:0;top:620px;width:1080px;display:flex;justify-content:center;gap:24px">' + "".join(kal(i) for i in range(5)) + "</div>" +
     '<div id="sp-sub" style="position:absolute;left:0;top:860px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:60px;color:#111">jeden Monat automatisch</div>',
     lambda t0, d: f'\n      pop("#sp-word", {t0});' + "".join(f'\n      pop("#sp-{i}", {c("s9", 1)} + {i * 0.18:.2f});' for i in range(5)) + f'\n      pop("#sp-sub", {c("s9", 2)});'),

    ("schwanken", "s10", "s10",
     box("zk-art", 140, 360, 800, 640, ZACKEN) + big("zk-txt", "langfristig ↑", 1040, 90, "var(--brand)"),
     lambda t0, d: f"""
      pop("#zk-art", {t0});
      draw("#zk-line", {t0} + 0.1, 1.4);
      tl.fromTo("#zk-trend", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c('s10', 2)});
      pop("#zk-txt", {c('s10', 2)} + 0.2);"""),

    ("frage", "s11", "s11",
     box("fr-dog", 290, 330, 500, 500, BEAGLE) + big("fr-q", "Hast du schon<br />einen ETF?", 880, 100),
     lambda t0, d: f"""
      pop("#fr-dog", {t0});
      pop("#fr-q", {t0} + 0.2);"""),

    ("kommentar", "s12", "s12",
     box("km-blase", 340, 360, 400, 347, BLASE) +
     '<div style="position:absolute;left:0;top:800px;width:1080px;display:flex;justify-content:center;gap:50px">' +
     chip("km-ja", "JA", "#1f7a4d") + chip("km-nein", "NEIN", "#e24b4b") + "</div>",
     lambda t0, d: f"""
      pop("#km-blase", {t0});
      pop("#km-ja", {c('s12', 0)} + 0.4);
      pop("#km-nein", {c('s12', 0)} + 0.8);"""),

    ("outro", "s13", "s13", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
