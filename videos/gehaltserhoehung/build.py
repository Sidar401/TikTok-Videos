#!/usr/bin/env python3
"""HundeFinanzTV: Die Gehaltserhöhungs-Falle (mit Teilen-CTA)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, GELDSACK, T, balken, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


def coin(id_, txt, x, y, s=230, fs=60):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:#f2c418;'
            f'border:10px solid #c99a06;display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:{fs}px;color:#7a5a00">{txt}</div>')


def big(id_, txt, top, size=120, col="#111", left=0, width=1080):
    return f'<div id="{id_}" class="big" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;font-size:{size}px;color:{col}">{txt}</div>'


ZETTEL = """<svg viewBox="0 0 300 380" style="width:100%;height:100%">
  <rect x="10" y="10" width="280" height="360" rx="16" fill="#fff" stroke="#353a3d" stroke-width="8" />
  <text x="40" y="70" font-family="Montserrat" font-weight="800" font-size="30" fill="#111">Gehalt</text>
  <rect x="40" y="105" width="200" height="14" rx="7" fill="#eee" /><rect x="40" y="140" width="160" height="14" rx="7" fill="#eee" />
  <rect x="40" y="175" width="190" height="14" rx="7" fill="#eee" />
  <text x="150" y="300" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="64" fill="#1f7a4d">+200 €</text>
</svg>"""

ICONS = {
    "Essen": '<circle cx="50" cy="55" r="36" fill="#fff" stroke="#353a3d" stroke-width="6" /><circle cx="50" cy="55" r="22" fill="#DB8622" /><path d="M10 15 L10 45 M18 15 L18 45 M10 30 L18 30 M88 15 Q98 35 88 50 L88 90" stroke="#353a3d" stroke-width="5" fill="none" stroke-linecap="round" />',
    "Handy": '<rect x="28" y="6" width="44" height="88" rx="10" fill="#353a3d" /><rect x="33" y="16" width="34" height="64" rx="4" fill="#9ed0f0" /><circle cx="50" cy="87" r="3" fill="#fff" />',
    "Auto": '<path d="M10 62 L18 40 Q22 32 32 32 L68 32 Q78 32 82 40 L90 62 Z" fill="#e24b4b" /><rect x="6" y="58" width="88" height="20" rx="8" fill="#e24b4b" /><rect x="28" y="38" width="44" height="18" rx="4" fill="#cfe6f5" /><circle cx="26" cy="80" r="10" fill="#353a3d" /><circle cx="74" cy="80" r="10" fill="#353a3d" />',
}
KONSUM = '<div style="position:absolute;left:0;top:450px;width:1080px;display:flex;justify-content:center;gap:40px">' + "".join(
    f'<div id="ks-{i}" class="tile" style="width:290px"><svg viewBox="0 0 100 100">{svg}</svg><span>{n}</span></div>'
    for i, (n, svg) in enumerate(ICONS.items())) + "</div>"

PUFF = '<svg viewBox="0 0 400 300" style="width:100%;height:100%"><g fill="#d9dde0"><circle cx="140" cy="160" r="70" /><circle cx="230" cy="130" r="85" /><circle cx="300" cy="180" r="60" /><circle cx="190" cy="210" r="60" /></g></svg>'
GESCHENK = """<svg viewBox="0 0 200 200" style="width:100%;height:100%">
  <rect x="25" y="80" width="150" height="110" rx="10" fill="#e24b4b" /><rect x="15" y="55" width="170" height="40" rx="8" fill="#c23b3b" />
  <rect x="88" y="55" width="24" height="135" fill="#f2c418" />
  <path d="M100 55 Q60 10 50 40 Q45 60 100 55 Q155 60 150 40 Q140 10 100 55 Z" fill="#f2c418" />
</svg>"""
CHART = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M10 85 L40 55 L60 68 L90 25" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /><path d="M70 22 L92 22 L92 44" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>'
HAELFTE = """<svg viewBox="0 0 300 300" style="width:100%;height:100%">
  <path d="M150 20 A130 130 0 0 0 150 280 Z" fill="#DB8622" /><path d="M150 20 A130 130 0 0 1 150 280 Z" fill="#1f7a4d" />
  <line x1="150" y1="10" x2="150" y2="290" stroke="#fff" stroke-width="10" />
  <text x="85" y="170" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">50%</text>
  <text x="215" y="170" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">50%</text>
</svg>"""
PERSON = """<svg viewBox="0 0 200 300" style="width:100%;height:100%">
  <circle cx="100" cy="60" r="45" fill="#353a3d" /><path d="M30 290 Q30 120 100 115 Q170 120 170 290 Z" fill="#353a3d" />
  <path d="M165 170 Q200 190 195 220" stroke="#353a3d" stroke-width="26" stroke-linecap="round" fill="none" />
</svg>"""
TEILEN = """<svg viewBox="0 0 200 200" style="width:100%;height:100%">
  <circle cx="100" cy="100" r="95" fill="var(--brand)" />
  <path d="M60 140 Q65 85 115 80 L115 55 L155 98 L115 140 L115 112 Q80 110 60 140 Z" fill="#fff" />
</svg>"""

bars_html, bars_js = balken("vg", "30.000€", "eingezahlt", "76.000€", "nach 25 J.", 30 / 76)

SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Mehr Gehalt –<br />trotzdem <span style="color:#e24b4b">pleite</span>?', size=88) +
     box("intro-zettel", 350, 600, 380, 481, ZETTEL),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-zettel", t0)),

    ("begriff", "s2", "s2",
     big("bg-word", "Lifestyle-<br />Inflation", 440, 140, "#e24b4b"),
     lambda t0, d: f'\n      pop("#bg-word", {t0});'),

    ("konsum", "s3", "s3", KONSUM,
     lambda t0, d: "".join(f'\n      pop("#ks-{i}", {c("s3", i + 1)});' for i in range(3))),

    ("weg", "s4", "s4",
     big("wg-plus", "+200€", 500, 180, "#1f7a4d") + box("wg-puff", 240, 430, 600, 450, PUFF) + big("wg-null", "0€", 960, 140, "#e24b4b"),
     lambda t0, d: f"""
      pop("#wg-plus", {t0});
      tl.fromTo("#wg-plus", {{ opacity: 1 }}, {{ opacity: 0, scale: 0.5, duration: 0.3 }}, {c('s4', 2)} - 0.2);
      tl.fromTo("#wg-puff", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {c('s4', 2)});
      pop("#wg-null", {c('s4', 2)} + 0.3);"""),

    ("regel", "s5", "s5",
     big("rg-title", "Hälfte-Regel", 350, 110, "var(--brand)") + box("rg-pie", 290, 560, 500, 500, HAELFTE),
     lambda t0, d: f"""
      pop("#rg-title", {t0});
      tl.fromTo("#rg-pie", {{ rotation: -90, scale: 0.6, opacity: 0 }}, {{ rotation: 0, scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.6)" }}, {t0} + 0.2);"""),

    ("teilung", "s6", "s6",
     coin("tl-200", "200€", 395, 380, 290, 80) + coin("tl-a", "100€", 150, 760, 250, 70) + coin("tl-b", "100€", 680, 760, 250, 70) +
     box("tl-gift", 170, 1060, 210, 210, GESCHENK).replace("top:1060px", "top:1040px"),
     lambda t0, d: f"""
      pop("#tl-200", {t0});
      pop("#tl-a", {c('s6', 1)});
      pop("#tl-b", {c('s6', 1)} + 0.1);
      pop("#tl-gift", {c('s6', 1)} + 0.4);"""),

    ("invest", "s7", "s7",
     coin("iv-c", "100€", 160, 520, 280, 80) +
     '<svg id="iv-arrow" viewBox="0 0 120 60" style="position:absolute;left:470px;top:620px;width:170px;height:85px"><path d="M8 30 L100 30 M76 8 L104 30 L76 52" fill="none" stroke="#111" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></svg>' +
     box("iv-chart", 670, 470, 330, 330, CHART) + big("iv-txt", "investieren", 920, 100, "#1f7a4d"),
     lambda t0, d: f"""
      pop("#iv-c", {t0});
      pop("#iv-arrow", {t0} + 0.3);
      pop("#iv-chart", {c('s7', 1)});
      pop("#iv-txt", {c('s7', 1)} + 0.2);"""),

    ("ergebnis", "s8", "s8",
     box("eg-sack", 240, 330, 600, 600, GELDSACK) + big("eg-num", "≈ 76.000€", 960, 150, "#c99a06"),
     lambda t0, d: f"""
      pop("#eg-sack", {t0});
      pop("#eg-num", {c('s8', 1)});"""),

    ("vergleich", "s9", "s9", box("vg-art", 130, 330, 820, 820, bars_html),
     lambda t0, d: bars_js(t0, t0 + 0.6)),

    ("goennen", "s10", "s10",
     box("gn-dog", 60, 470, 500, 500, BEAGLE) + box("gn-gift", 600, 560, 360, 360, GESCHENK),
     lambda t0, d: f"""
      pop("#gn-dog", {t0});
      pop("#gn-gift", {c('s10', 2)} - 0.3);
      tl.fromTo("#gn-gift", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {c('s10', 2)});"""),

    ("finger", "s11", "s11",
     box("fg-person", 390, 380, 300, 450, PERSON) + coin("fg-c1", "€", 640, 760, 110, 50) + coin("fg-c2", "€", 720, 900, 100, 46) + coin("fg-c3", "€", 630, 1030, 90, 42),
     lambda t0, d: f'\n      pop("#fg-person", {t0});' + "".join(
         f'\n      tl.fromTo("#fg-c{i}", {{ y: -180, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power2.in" }}, {c("s11", 1)} + {(i - 1) * 0.3:.2f});' for i in (1, 2, 3))),

    ("teilen", "s12", "s12",
     box("tn-icon", 340, 420, 400, 400, TEILEN) + big("tn-txt", "Teile das Video!", 900, 100, "var(--brand)"),
     lambda t0, d: f"""
      pop("#tn-icon", {t0});
      tl.fromTo("#tn-icon", {{ rotation: -10 }}, {{ rotation: 10, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.35);
      pop("#tn-txt", {t0} + 0.2);"""),

    ("outro", "s13", "s13", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
