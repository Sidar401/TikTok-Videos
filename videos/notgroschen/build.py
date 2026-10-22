#!/usr/bin/env python3
"""HundeFinanzTV: Wie viel Notgroschen brauchst du?"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, SPARSCHWEIN, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


SCHIRM = """<svg viewBox="0 0 400 300" style="width:100%;height:100%">
  <path d="M20 170 Q200 -40 380 170 Q335 140 290 170 Q245 140 200 170 Q155 140 110 170 Q65 140 20 170 Z" fill="#DB8622" />
  <path d="M200 170 L200 285 Q200 300 185 300 Q170 300 170 285" fill="none" stroke="#353a3d" stroke-width="12" stroke-linecap="round" />
</svg>"""

KAL = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><rect x="8" y="16" width="84" height="76" rx="12" fill="#fff" stroke="#353a3d" stroke-width="7" /><rect x="8" y="16" width="84" height="24" rx="10" fill="{col}" /><rect x="26" y="6" width="9" height="20" rx="4" fill="#353a3d" /><rect x="65" y="6" width="9" height="20" rx="4" fill="#353a3d" /></svg>'
MONATE = '<div style="display:flex;gap:18px;justify-content:center">' + "".join(
    f'<div id="mo-{i}" style="width:140px;height:140px">{KAL.format(col="#1f7a4d" if i < 3 else "#9bc9ad")}</div>' for i in range(6)) + "</div>"

WASCH = """<svg viewBox="0 0 300 340" style="width:100%;height:100%">
  <rect x="20" y="20" width="260" height="300" rx="24" fill="#f6efe1" stroke="#353a3d" stroke-width="10" />
  <line x1="20" y1="80" x2="280" y2="80" stroke="#353a3d" stroke-width="8" />
  <circle cx="70" cy="50" r="12" fill="#353a3d" /><rect x="110" y="42" width="80" height="16" rx="8" fill="#9aa3a8" />
  <circle cx="150" cy="200" r="88" fill="#cfe6f5" stroke="#353a3d" stroke-width="10" />
  <path d="M90 215 Q120 190 150 215 Q180 240 210 215" fill="none" stroke="#6fb7e6" stroke-width="10" />
</svg>"""
RAUCH = """<svg viewBox="0 0 200 200" style="width:100%;height:100%"><g fill="#9aa3a8" opacity="0.85"><circle cx="70" cy="140" r="40" /><circle cx="110" cy="95" r="48" /><circle cx="150" cy="50" r="34" /></g></svg>"""
WARN = """<svg viewBox="0 0 100 90" style="width:100%;height:100%"><path d="M50 5 L95 85 L5 85 Z" fill="#f2c418" stroke="#111" stroke-width="5" stroke-linejoin="round" /><rect x="45" y="30" width="10" height="30" rx="5" fill="#111" /><circle cx="50" cy="71" r="6" fill="#111" /></svg>"""
KIT = """<svg viewBox="0 0 300 260" style="width:100%;height:100%"><rect x="20" y="60" width="260" height="190" rx="26" fill="#e24b4b" /><rect x="100" y="25" width="100" height="50" rx="14" fill="none" stroke="#e24b4b" stroke-width="16" /><path d="M150 105 L150 205 M100 155 L200 155" stroke="#fff" stroke-width="30" stroke-linecap="round" /></svg>"""
BANK = """<svg viewBox="0 0 400 360" style="width:100%;height:100%">
  <path d="M30 120 L200 30 L370 120 Z" fill="#DB8622" />
  <rect x="40" y="120" width="320" height="24" fill="#a8621a" />
  <g fill="#f6efe1" stroke="#353a3d" stroke-width="6"><rect x="70" y="150" width="40" height="150" /><rect x="150" y="150" width="40" height="150" /><rect x="230" y="150" width="40" height="150" /><rect x="300" y="150" width="40" height="150" /></g>
  <rect x="30" y="300" width="340" height="34" fill="#353a3d" />
  <text x="200" y="102" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="52" fill="#fff">%</text>
</svg>"""


def coin(i, x, y):
    return (f'<div id="zi-{i}" style="position:absolute;left:{x}px;top:{y}px;width:150px;height:150px;border-radius:50%;background:#f2c418;'
            f'border:8px solid #c99a06;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:56px;color:#7a5a00">€</div>')


def stufe(id_, nr, txt, icon, top, left):
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:640px;display:flex;align-items:center;gap:26px;'
            f'padding:26px 34px;border-radius:30px;background:#faf5ef">'
            f'<div style="width:90px;height:90px;border-radius:50%;background:var(--brand);color:#fff;font-family:Montserrat;font-weight:800;font-size:56px;display:flex;align-items:center;justify-content:center">{nr}</div>'
            f'<div style="flex:1;font-family:Montserrat;font-weight:800;font-size:56px;color:#111">{txt}</div>'
            f'<div style="width:100px;height:100px">{icon}</div></div>')


CHART = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M10 85 L40 55 L60 68 L90 25" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /><path d="M70 22 L92 22 L92 44" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>'

SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Wie viel <span style="color:var(--brand)">Notgroschen</span><br />brauchst du?', size=76) +
     box("intro-schirm", 290, 560, 500, 375, SCHIRM) + box("intro-pig", 330, 820, 420, 364, SPARSCHWEIN),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-pig", t0) + f"""
      tl.fromTo("#intro-schirm", {{ y: -40, rotation: -6 }}, {{ y: 0, rotation: 0, duration: 0.6, ease: "back.out(2)" }}, {t0});"""),

    ("monate", "s2", "s2",
     '<div id="mo-num" class="big" style="position:absolute;left:0;top:360px;width:1080px;font-size:200px;color:#1f7a4d">3–6</div>'
     '<div id="mo-label" style="position:absolute;left:0;top:620px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:68px;color:#111">Monatsausgaben</div>'
     '<div style="position:absolute;left:0;top:800px;width:1080px">' + MONATE + '</div>',
     lambda t0, d: f'\n      pop("#mo-num", {t0});\n      pop("#mo-label", {t0} + 0.2);' + "".join(f'\n      pop("#mo-{i}", {c("s2", 1)} + {i * 0.15:.2f});' for i in range(6))),

    ("rechnung", "s3", "s3",
     '<div class="big" style="position:absolute;left:0;top:360px;width:1080px">'
     '<div id="rc-a" style="font-size:130px">1.500€ <span style="font-size:70px">/ Monat</span></div>'
     '<div id="rc-arrow" style="height:230px;display:flex;justify-content:center;align-items:center"><svg viewBox="0 0 70 110" style="width:110px;height:190px"><path d="M35 6 L35 96 M14 76 L35 100 L56 76" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg></div>'
     '<div id="rc-b" style="font-size:120px;color:#c99a06">4.500€ – 9.000€</div></div>',
     lambda t0, d: f"""
      pop("#rc-a", {t0});
      pop("#rc-arrow", {c('s3', 2)} - 0.4);
      pop("#rc-b", {c('s3', 2)});"""),

    ("wasch", "s4", "s4",
     box("ws-m", 290, 430, 500, 567, WASCH) + box("ws-rauch", 640, 300, 280, 280, RAUCH) + box("ws-warn", 150, 380, 200, 180, WARN),
     lambda t0, d: f"""
      pop("#ws-m", {t0});
      tl.fromTo("#ws-m", {{ rotation: -3 }}, {{ rotation: 3, duration: 0.08, yoyo: true, repeat: 9, ease: "none" }}, {c('s4', 1)});
      tl.fromTo("#ws-rauch", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }}, {c('s4', 1)} + 0.2);
      pop("#ws-warn", {c('s4', 2)});"""),

    ("tierarzt", "s5", "s5",
     box("ta-dog", 50, 480, 500, 500, BEAGLE) + box("ta-kit", 560, 560, 440, 381, KIT),
     lambda t0, d: f"""
      pop("#ta-dog", {t0});
      pop("#ta-kit", {c('s5', 1)});
      tl.fromTo("#ta-kit", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {c('s5', 1)} + 0.35);"""),

    ("tagesgeld", "s6", "s6",
     box("tg-pig", 80, 700, 380, 329, SPARSCHWEIN) + box("tg-bank", 500, 520, 500, 450, BANK) +
     '<div id="tg-label" class="big" style="position:absolute;left:0;top:360px;width:1080px;font-size:100px">Tagesgeld</div>',
     lambda t0, d: f"""
      pop("#tg-label", {t0});
      pop("#tg-pig", {t0} + 0.1);
      pop("#tg-bank", {c('s6', 1)});
      tl.fromTo("#tg-pig", {{ x: 0 }}, {{ x: 120, duration: 0.8, ease: "power2.inOut" }}, {c('s6', 1)} + 0.3);"""),

    ("zinsen", "s7", "s7",
     coin(0, 300, 860) + coin(1, 465, 860) + coin(2, 630, 860) + coin(3, 382, 700) + coin(4, 547, 700) +
     '<div id="zi-plus" class="big" style="position:absolute;left:0;top:420px;width:1080px;font-size:150px;color:#1f7a4d">+ Zinsen</div>',
     lambda t0, d: "".join(f'\n      pop("#zi-{i}", {t0} + {i * 0.18:.2f});' for i in range(5)) + f'\n      pop("#zi-plus", {c("s7", 1)});'),

    ("stufen", "s8", "s8",
     stufe("st-1", "1", "Notgroschen", CHECK, 500, 80) + stufe("st-2", "2", "Investieren", CHART, 760, 360),
     lambda t0, d: f"""
      pop("#st-1", {t0});
      pop("#st-2", {c('s8', 1)});"""),

    ("outro", "s9", "s9", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
