#!/usr/bin/env python3
"""HundeFinanzTV: Die Abo-Falle."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, GELDSACK, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


ICONS = {
    "Streaming": '<rect x="10" y="20" width="80" height="55" rx="8" fill="#e24b4b" /><path d="M42 36 L62 47.5 L42 59 Z" fill="#fff" /><rect x="35" y="80" width="30" height="7" rx="3" fill="#353a3d" />',
    "Musik": '<circle cx="50" cy="50" r="42" fill="#1f7a4d" /><path d="M40 68 L40 32 L66 26 L66 60" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round" /><circle cx="35" cy="68" r="8" fill="#fff" /><circle cx="61" cy="62" r="8" fill="#fff" />',
    "Fitness": '<rect x="28" y="44" width="44" height="12" rx="4" fill="#353a3d" /><rect x="14" y="30" width="16" height="40" rx="5" fill="#DB8622" /><rect x="70" y="30" width="16" height="40" rx="5" fill="#DB8622" /><rect x="5" y="38" width="10" height="24" rx="4" fill="#DB8622" /><rect x="85" y="38" width="10" height="24" rx="4" fill="#DB8622" />',
    "Cloud": '<path d="M28 72 Q8 72 10 54 Q12 38 30 40 Q36 20 56 22 Q74 24 76 42 Q94 42 92 58 Q90 72 74 72 Z" fill="#3d7be0" />',
}
TILES = '<div style="position:absolute;left:90px;top:330px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:40px">' + "".join(
    f'<div id="ab-t{i}" class="tile"><svg viewBox="0 0 100 100">{svg}</svg><span>{name}</span></div>'
    for i, (name, svg) in enumerate(ICONS.items())) + "</div>"

PHONE_ROWS = "".join(
    f'<g transform="translate(40 {120 + i * 95})"><rect width="220" height="78" rx="14" fill="#faf5ef" />'
    f'<svg x="10" y="10" width="58" height="58" viewBox="0 0 100 100">{svg}</svg>'
    f'<text x="205" y="50" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="28" fill="#e24b4b">−15 €</text></g>'
    for i, svg in enumerate(ICONS.values()))
PHONE = f"""<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" />
  <rect x="22" y="40" width="256" height="480" rx="20" fill="#fff" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" />
  <text x="150" y="95" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="26" fill="#111">Abos</text>
  {PHONE_ROWS}
</svg>"""

CHART = """<svg viewBox="0 0 400 400" style="width:100%;height:100%">
  <path d="M40 40 L40 340 L370 340" fill="none" stroke="#111" stroke-width="8" stroke-linecap="square" />
  <path id="zins-dots" d="M60 300 C170 275 240 200 300 95" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 16" />
  <text id="zins-label" class="serif" x="70" y="100" font-size="70" fill="#1f7a4d">~7%</text>
  <text id="zins-years" x="205" y="385" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#353a3d">20 Jahre</text>
  <g id="zins-check"><circle cx="320" cy="80" r="42" fill="#111" /><path d="M300 82 L315 97 L342 66" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></g>
</svg>"""

AUSZUG = """<svg viewBox="0 0 400 480" style="width:100%;height:100%">
  <rect x="40" y="20" width="320" height="440" rx="16" fill="#fff" stroke="#353a3d" stroke-width="8" />
  <text x="70" y="75" font-family="Montserrat" font-weight="800" font-size="30" fill="#111">Kontoauszug</text>
  <g font-family="Montserrat" font-weight="700" font-size="22">
    <text x="70" y="140" fill="#353a3d">Miete</text><text x="330" y="140" text-anchor="end" fill="#353a3d">−650 €</text>
    <rect id="az-h1" x="58" y="160" width="284" height="42" rx="8" fill="#f2c418" opacity="0.5" />
    <text x="70" y="190" fill="#111">Streaming</text><text x="330" y="190" text-anchor="end" fill="#e24b4b">−15 €</text>
    <text x="70" y="240" fill="#353a3d">Einkauf</text><text x="330" y="240" text-anchor="end" fill="#353a3d">−84 €</text>
    <rect id="az-h2" x="58" y="260" width="284" height="42" rx="8" fill="#f2c418" opacity="0.5" />
    <text x="70" y="290" fill="#111">Fitness</text><text x="330" y="290" text-anchor="end" fill="#e24b4b">−15 €</text>
    <rect id="az-h3" x="58" y="310" width="284" height="42" rx="8" fill="#f2c418" opacity="0.5" />
    <text x="70" y="340" fill="#111">Cloud</text><text x="330" y="340" text-anchor="end" fill="#e24b4b">−15 €</text>
    <text x="70" y="390" fill="#353a3d">Tanken</text><text x="330" y="390" text-anchor="end" fill="#353a3d">−60 €</text>
  </g>
</svg>"""

MINI = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:30px">' + "".join(
    f'<div style="position:relative;width:200px;height:200px"><svg viewBox="0 0 100 100" style="width:100%;height:100%">{svg}</svg>'
    f'<div id="wk-m{i}" style="position:absolute;right:-14px;top:-14px;width:80px;height:80px">{CHECK if i == 1 else CROSS}</div></div>'
    for i, svg in enumerate(ICONS.values())) + "</div>"

SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Diese Abos fressen<br />dein <span style="color:#e24b4b">Vermögen</span>', size=88) +
     box("intro-phone", 340, 540, 400, 747, PHONE),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-phone", t0)),

    ("liste", "s2", "s2", TILES,
     lambda t0, d: "".join(f'\n      pop("#ab-t{i}", {t0} + {i * 0.45:.2f});' for i in range(4))),

    ("monat", "s3", "s3",
     '<div class="big" style="position:absolute;left:0;top:380px;width:1080px">'
     '<div id="mn-a" style="font-size:130px">4 × 15€</div>'
     '<div id="mn-arrow" style="height:230px;display:flex;justify-content:center;align-items:center"><svg viewBox="0 0 70 110" style="width:110px;height:190px"><path d="M35 6 L35 96 M14 76 L35 100 L56 76" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg></div>'
     '<div id="mn-b" style="font-size:150px;color:#e24b4b">60€ <span style="font-size:80px;color:#111">/ Monat</span></div></div>',
     lambda t0, d: f"""
      pop("#mn-a", {t0});
      pop("#mn-arrow", {c('s3', 1)} - 0.4);
      pop("#mn-b", {c('s3', 1)});"""),

    ("jahr", "s4", "s4",
     '<div id="jr-num" class="big" style="position:absolute;left:0;top:500px;width:1080px;font-size:210px;color:#e24b4b">720€</div>'
     '<div id="jr-sub" style="position:absolute;left:0;top:800px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:80px;color:#111">pro Jahr</div>',
     lambda t0, d: f"""
      pop("#jr-num", {t0});
      tl.fromTo("#jr-num", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 }}, {t0} + 0.5);
      pop("#jr-sub", {t0} + 0.3);"""),

    ("zins", "s5", "s5",
     box("zins-art", 130, 330, 820, 820, CHART),
     lambda t0, d: f"""
      tl.fromTo("#zins-dots", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {t0});
      pop("#zins-years", {t0} + 0.3);
      pop("#zins-label", {c('s5', 1)});
      pop("#zins-check", {c('s5', 1)} + 0.4);"""),

    ("ende", "s6", "s6",
     box("ende-sack", 240, 330, 600, 600, GELDSACK) +
     '<div id="ende-num" class="big" style="position:absolute;left:0;top:960px;width:1080px;font-size:150px;color:#c99a06">≈ 29.500€</div>',
     lambda t0, d: f"""
      pop("#ende-sack", {t0});
      pop("#ende-num", {c('s6', 1)});"""),

    ("auszug", "s7", "s7",
     box("az-paper", 240, 360, 600, 720, AUSZUG),
     lambda t0, d: f"""
      pop("#az-paper", {t0});""" + "".join(f'\n      tl.fromTo("#az-h{i}", {{ opacity: 0 }}, {{ opacity: 0.5, duration: 0.25 }}, {c("s7", 1)} + {(i - 1) * 0.3:.2f});' for i in (1, 2, 3))),

    ("wirklich", "s8", "s8",
     box("wk-dog", 30, 520, 460, 460, BEAGLE) +
     '<div id="wk-grid" style="position:absolute;left:540px;top:470px">' + MINI + '</div>',
     lambda t0, d: f"""
      pop("#wk-dog", {t0});
      pop("#wk-grid", {t0} + 0.15);""" + "".join(f'\n      pop("#wk-m{i}", {t0} + {0.6 + i * 0.2:.2f});' for i in range(4))),

    ("outro", "s9", "s9", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
