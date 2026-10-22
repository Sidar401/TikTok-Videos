#!/usr/bin/env python3
"""HundeFinanzTV: Was dein Auto wirklich kostet (mit Teilen-CTA)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CROSS, GELDSACK, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


def big(id_, txt, top, size=120, col="#111", left=0, width=1080):
    return f'<div id="{id_}" class="big" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;font-size:{size}px;color:{col}">{txt}</div>'


def auto(col="#e24b4b"):
    return f"""<svg viewBox="0 0 400 220" style="width:100%;height:100%">
  <path d="M30 140 L60 80 Q72 58 100 58 L280 58 Q310 58 325 80 L360 140 Z" fill="{col}" />
  <rect x="15" y="130" width="370" height="55" rx="20" fill="{col}" />
  <path d="M110 74 L180 74 L180 128 L85 128 Z M200 74 L275 74 Q290 74 300 90 L320 128 L200 128 Z" fill="#cfe6f5" />
  <circle cx="100" cy="190" r="30" fill="#353a3d" /><circle cx="100" cy="190" r="12" fill="#ccc" />
  <circle cx="300" cy="190" r="30" fill="#353a3d" /><circle cx="300" cy="190" r="12" fill="#ccc" />
  <rect x="360" y="140" width="22" height="14" rx="4" fill="#f2c418" />
</svg>"""


ICONS = [
    ("Sprit", '<rect x="18" y="14" width="44" height="76" rx="8" fill="#e24b4b" /><rect x="26" y="24" width="28" height="20" rx="3" fill="#fff" /><path d="M62 34 L78 46 L78 78 Q78 86 70 86" fill="none" stroke="#353a3d" stroke-width="6" stroke-linecap="round" />'),
    ("Versicherung", '<path d="M50 10 L84 22 Q84 64 50 90 Q16 64 16 22 Z" fill="#3d7be0" /><path d="M36 50 L46 60 L66 38" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />'),
    ("Steuer", '<rect x="22" y="10" width="56" height="80" rx="6" fill="#f6efe1" stroke="#353a3d" stroke-width="5" /><text x="50" y="66" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#353a3d">§</text>'),
    ("Werkstatt", '<path d="M70 12 A20 20 0 0 0 52 40 L14 78 Q10 86 18 90 Q24 94 30 88 L66 50 A20 20 0 0 0 92 30 L80 38 L68 34 L64 22 Z" fill="#353a3d" />'),
    ("Reifen", '<circle cx="50" cy="50" r="40" fill="#353a3d" /><circle cx="50" cy="50" r="18" fill="#ccc" /><g stroke="#555" stroke-width="5"><line x1="50" y1="10" x2="50" y2="26" /><line x1="50" y1="74" x2="50" y2="90" /><line x1="10" y1="50" x2="26" y2="50" /><line x1="74" y1="50" x2="90" y2="50" /></g>'),
    ("Wertverlust", '<path d="M12 22 L40 52 L58 38 L88 76" fill="none" stroke="#e24b4b" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /><path d="M66 78 L90 78 L90 54" fill="none" stroke="#e24b4b" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" />'),
]
GRID = '<div style="position:absolute;left:60px;top:330px;width:960px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px">' + "".join(
    f'<div id="kt-{i}" class="tile" style="padding:22px 6px"><svg viewBox="0 0 100 100" style="width:170px;height:170px">{svg}</svg><span style="font-size:{40 if len(n) > 9 else 46}px">{n}</span></div>'
    for i, (n, svg) in enumerate(ICONS)) + "</div>"

CHART = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M10 85 L40 55 L60 68 L90 25" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /><path d="M70 22 L92 22 L92 44" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>'
KRONE = '<svg viewBox="0 0 200 160" style="width:100%;height:100%"><path d="M20 140 L10 40 L60 80 L100 20 L140 80 L190 40 L180 140 Z" fill="#f2c418" stroke="#c99a06" stroke-width="8" stroke-linejoin="round" /><circle cx="100" cy="110" r="14" fill="#e24b4b" /></svg>'
TEILEN = """<svg viewBox="0 0 200 200" style="width:100%;height:100%">
  <circle cx="100" cy="100" r="95" fill="var(--brand)" />
  <path d="M60 140 Q65 85 115 80 L115 55 L155 98 L115 140 L115 112 Q80 110 60 140 Z" fill="#fff" />
</svg>"""


def coin(id_, txt, x, y, s=260, fs=72):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:#f2c418;'
            f'border:10px solid #c99a06;display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:{fs}px;color:#7a5a00">{txt}</div>')


def pin(id_, label, x):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:560px;width:150px;height:150px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--brand)">'
            f'<div style="transform:rotate(45deg);width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:70px;color:#fff">{label}</div></div>')


SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Dein Auto kostet dich<br /><span style="color:#e24b4b">mehr</span>, als du denkst', size=74) +
     box("intro-auto", 140, 640, 800, 440, auto()) + big("intro-q", "?€", 520, 130, "#e24b4b", 760, 260),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-auto", t0) + f'\n      pop("#intro-q", {t0} + 0.3);'),

    ("sprit", "s2", "s2",
     '<div id="sp-tile" class="tile" style="position:absolute;left:340px;top:450px;width:400px"><svg viewBox="0 0 100 100" style="width:300px;height:300px">' + ICONS[0][1] + '</svg><span style="font-size:70px">Sprit</span></div>',
     lambda t0, d: f'\n      pop("#sp-tile", {t0});'),

    ("kosten", "s3", "s3", GRID,
     lambda t0, d: f'\n      pop("#kt-0", {t0});' + "".join(f'\n      pop("#kt-{i}", {c("s3", 0)} + {0.5 + (i - 1) * 0.9:.2f});' for i in range(1, 6))),

    ("monat", "s4", "s4",
     big("mn-num", "400€", 500, 230, "#e24b4b") +
     '<div id="mn-sub" style="position:absolute;left:0;top:800px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:80px;color:#111">pro Monat</div>',
     lambda t0, d: f"""
      pop("#mn-num", {c('s4', 1)} - 0.3);
      pop("#mn-sub", {c('s4', 1)});"""),

    ("jahr", "s5", "s5",
     big("jr-num", "≈ 5.000€", 500, 200, "#e24b4b") +
     '<div id="jr-sub" style="position:absolute;left:0;top:780px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:80px;color:#111">pro Jahr</div>',
     lambda t0, d: f"""
      pop("#jr-num", {t0});
      tl.fromTo("#jr-num", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 }}, {t0} + 0.5);
      pop("#jr-sub", {t0} + 0.3);"""),

    ("vergleich", "s6", "s6",
     box("vg-teuer", 60, 380, 600, 330, auto("#e24b4b")) + box("vg-x", 560, 360, 120, 120, CROSS) +
     box("vg-guenstig", 420, 820, 520, 286, auto("#1f7a4d")) +
     big("vg-txt", "−200€ / Monat", 1120, 76, "#1f7a4d").replace("top:1120px", "top:1110px"),
     lambda t0, d: f"""
      pop("#vg-teuer", {t0});
      pop("#vg-x", {c('s6', 2)} - 0.2);
      tl.fromTo("#vg-guenstig", {{ x: 400, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.6, ease: "power3.out" }}, {c('s6', 1)});
      pop("#vg-txt", {c('s6', 2)});"""),

    ("invest", "s7", "s7",
     coin("iv-c", "200€", 150, 520) +
     '<svg id="iv-arrow" viewBox="0 0 120 60" style="position:absolute;left:460px;top:620px;width:170px;height:85px"><path d="M8 30 L100 30 M76 8 L104 30 L76 52" fill="none" stroke="#111" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></svg>' +
     box("iv-chart", 670, 470, 330, 330, CHART) + big("iv-txt", "investieren", 920, 100, "#1f7a4d"),
     lambda t0, d: f"""
      pop("#iv-c", {t0});
      pop("#iv-arrow", {t0} + 0.4);
      pop("#iv-chart", {c('s7', 1)});
      pop("#iv-txt", {c('s7', 1)} + 0.2);"""),

    ("ergebnis", "s8", "s8",
     box("eg-sack", 240, 330, 600, 600, GELDSACK) + big("eg-num", "≈ 98.000€", 960, 150, "#c99a06"),
     lambda t0, d: f"""
      pop("#eg-sack", {t0});
      pop("#eg-num", {c('s8', 1)});"""),

    ("luxus", "s9", "s9",
     box("lx-dog", 40, 480, 480, 480, BEAGLE) + box("lx-krone", 580, 520, 380, 304, KRONE) + box("lx-x", 860, 460, 140, 140, CROSS),
     lambda t0, d: f"""
      pop("#lx-dog", {t0});
      pop("#lx-krone", {t0} + 0.2);
      pop("#lx-x", {c('s9', 1)});"""),

    ("weg", "s10", "s10",
     pin("ab-a", "A", 120) + pin("ab-b", "B", 810) +
     '<svg viewBox="0 0 1080 60" style="position:absolute;left:0;top:780px;width:1080px;height:60px"><line id="ab-road" x1="190" y1="30" x2="890" y2="30" stroke="#353a3d" stroke-width="14" stroke-dasharray="40 26" /></svg>' +
     box("ab-auto", 160, 655, 300, 165, auto("#1f7a4d")) + big("ab-txt", "nicht arm machen", 1080, 76, "#e24b4b").replace("top:1080px", "top:1070px"),
     lambda t0, d: f"""
      pop("#ab-a", {t0});
      pop("#ab-b", {t0} + 0.2);
      tl.fromTo("#ab-auto", {{ x: 0 }}, {{ x: 480, duration: {round(c('s10', 2) - t0 + 0.2, 2)}, ease: "power1.inOut" }}, {t0} + 0.3);
      pop("#ab-txt", {c('s10', 2)});"""),

    ("teilen", "s11", "s11",
     box("tn-icon", 340, 420, 400, 400, TEILEN) + big("tn-txt", "Teile das Video!", 900, 100, "var(--brand)"),
     lambda t0, d: f"""
      pop("#tn-icon", {t0});
      tl.fromTo("#tn-icon", {{ rotation: -10 }}, {{ rotation: 10, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.35);
      pop("#tn-txt", {t0} + 0.2);"""),

    ("outro", "s12", "s12", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
