#!/usr/bin/env python3
"""HundeFinanzTV: Die 50-30-20-Regel."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, SPARSCHWEIN, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


R = 150
U = 2 * 3.14159265 * R
SEG = [("fix", 0.5, 0.0, "#353a3d", "1.000€", "Fixkosten"),
       ("spass", 0.3, 0.5, "#DB8622", "600€", "Spaß"),
       ("spar", 0.2, 0.8, "#1f7a4d", "400€", "Sparen")]

DONUT = f"""<svg viewBox="0 0 400 400" style="width:100%;height:100%">
  <circle cx="200" cy="200" r="{R}" fill="none" stroke="#eee" stroke-width="70" />
  <g transform="rotate(-90 200 200)">""" + "".join(
    f'<circle id="dn-{k}" cx="200" cy="200" r="{R}" fill="none" stroke="{col}" stroke-width="70" '
    f'stroke-dasharray="0 {U:.1f}" stroke-dashoffset="{-start * U:.1f}" />' for k, frac, start, col, _, _ in SEG) + """</g>
  <text x="200" y="195" text-anchor="middle" class="serif" font-size="48" fill="#111">2.000€</text>
  <text x="200" y="240" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="26" fill="#353a3d">netto</text>
</svg>"""

LEGENDE = "".join(
    f'<div id="lg-{k}" style="display:flex;align-items:center;gap:24px;margin:14px 0">'
    f'<div style="width:56px;height:56px;border-radius:14px;background:{col}"></div>'
    f'<div class="serif" style="font-size:76px;color:{col};width:300px">{val}</div>'
    f'<div style="font-family:Montserrat;font-weight:800;font-size:58px;color:#111">{lab}</div></div>'
    for k, _, _, col, val, lab in SEG)

WALLET = """<svg viewBox="0 0 400 300" style="width:100%;height:100%">
  <rect x="30" y="70" width="340" height="210" rx="28" fill="#8a5a2b" />
  <rect x="30" y="70" width="340" height="60" rx="28" fill="#a8743f" />
  <rect x="270" y="145" width="110" height="70" rx="16" fill="#6b3f1f" /><circle cx="305" cy="180" r="12" fill="#f2c418" />
  <g id="wl-moth" fill="#9aa3a8"><ellipse cx="200" cy="40" rx="10" ry="16" /><ellipse cx="180" cy="34" rx="20" ry="12" /><ellipse cx="220" cy="34" rx="20" ry="12" /></g>
</svg>"""


def karte(id_, txt, icon, top, col):
    return (f'<div id="{id_}" style="position:absolute;left:140px;top:{top}px;width:800px;display:flex;align-items:center;gap:30px;'
            f'padding:30px 40px;border-radius:30px;background:#faf5ef;border:6px solid {col}">'
            f'<div style="flex:1;font-family:Montserrat;font-weight:800;font-size:58px;color:#111;white-space:nowrap">{txt}</div>'
            f'<div style="width:120px;height:120px">{icon}</div></div>')


TASCHE = """<svg viewBox="0 0 300 320" style="width:100%;height:100%">
  <path d="M40 100 L260 100 L240 300 L60 300 Z" fill="#DB8622" />
  <path d="M100 100 Q100 30 150 30 Q200 30 200 100" fill="none" stroke="#a8621a" stroke-width="14" />
  <path d="M150 230 Q110 200 120 175 Q130 155 150 175 Q170 155 180 175 Q190 200 150 230 Z" fill="#fff" />
</svg>"""


def stapel(i, n, x):
    return "".join(
        f'<div class="st-{i}" style="position:absolute;left:{x}px;top:{1100 - k * 46}px;width:170px;height:40px;border-radius:12px;background:#f2c418;border:5px solid #c99a06"></div>'
        for k in range(n))


SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Am Ende vom Geld ist<br />noch so viel <span style="color:var(--brand)">Monat</span> übrig?', size=74) +
     box("intro-wallet", 240, 620, 600, 450, WALLET),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-wallet", t0) + f"""
      tl.fromTo("#wl-moth", {{ y: 0 }}, {{ y: -60, duration: {d}, ease: "sine.inOut" }}, {t0});"""),

    ("regel", "s2", "s2",
     '<div id="rg-num" class="big" style="position:absolute;left:0;top:480px;width:1080px;font-size:200px">'
     '<span style="color:#353a3d">50</span><span style="color:#ccc">·</span><span style="color:#DB8622">30</span><span style="color:#ccc">·</span><span style="color:#1f7a4d">20</span></div>'
     '<div id="rg-sub" style="position:absolute;left:0;top:760px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:80px;color:#111">Regel</div>',
     lambda t0, d: f"""
      pop("#rg-num", {t0});
      pop("#rg-sub", {t0} + 0.3);"""),

    ("donut", "s3", "s5",
     box("dn-art", 260, 320, 560, 560, DONUT) +
     '<div style="position:absolute;left:150px;top:900px">' + LEGENDE + '</div>',
     lambda t0, d: f"""
      pop("#dn-art", {t0});""" + "".join(
         f"""
      tl.fromTo("#dn-{k}", {{ strokeDasharray: "0 {U:.1f}" }}, {{ strokeDasharray: "{frac * U:.1f} {U:.1f}", duration: 0.7, ease: "power2.out" }}, {at});
      pop("#lg-{k}", {at} + 0.2);"""
         for (k, frac, *_), at in zip(SEG, [c('s3', 1), t['saetze'][3]['start'], t['saetze'][4]['start']]))),

    ("anfang", "s6", "s6",
     karte("an-1", "am Monatsanfang", CHECK, 470, "#1f7a4d") + karte("an-2", "am Monatsende", CROSS, 760, "#e24b4b"),
     lambda t0, d: f"""
      pop("#an-1", {t0});
      pop("#an-2", {c('s6', 1)});"""),

    ("wachstum", "s7", "s7",
     box("wa-pig", 40, 520, 380, 329, SPARSCHWEIN) + stapel(0, 3, 470) + stapel(1, 6, 670) + stapel(2, 10, 870),
     lambda t0, d: f'\n      pop("#wa-pig", {t0});' + "".join(
         f'\n      tl.fromTo(".st-{i}", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.25, stagger: 0.05, ease: "power2.out" }}, {t0} + {0.3 + i * 0.4:.2f});' for i in range(3))),

    ("shoppen", "s8", "s8",
     box("sh-dog", 40, 500, 480, 480, BEAGLE) + box("sh-bag", 580, 480, 380, 405, TASCHE),
     lambda t0, d: f"""
      pop("#sh-dog", {t0});
      pop("#sh-bag", {t0} + 0.25);
      tl.fromTo("#sh-bag", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {c('s8', 1)});"""),

    ("outro", "s9", "s9", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
