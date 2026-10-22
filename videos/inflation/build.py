#!/usr/bin/env python3
"""HundeFinanzTV: Dein Geld auf dem Konto schrumpft (Inflation)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, SPARSCHWEIN, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


SCHEIN = """<svg viewBox="0 0 400 220" style="width:100%;height:100%">
  <rect x="5" y="5" width="390" height="210" rx="18" fill="#8fc9a3" stroke="#1f7a4d" stroke-width="8" />
  <rect x="25" y="25" width="350" height="170" rx="10" fill="none" stroke="#1f7a4d" stroke-width="4" stroke-dasharray="10 8" />
  <circle cx="200" cy="110" r="58" fill="#e8f4ec" stroke="#1f7a4d" stroke-width="5" />
  <text x="200" y="135" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="70" fill="#1f7a4d">€</text>
  <text x="60" y="70" font-family="Montserrat" font-weight="800" font-size="40" fill="#1f7a4d">100</text>
  <text x="270" y="185" font-family="Montserrat" font-weight="800" font-size="40" fill="#1f7a4d">100</text>
</svg>"""

PHONE = """<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" />
  <rect x="22" y="40" width="256" height="480" rx="20" fill="#fff" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" />
  <text x="150" y="110" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="24" fill="#888">Girokonto</text>
  <text x="150" y="180" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#111">10.000,00 €</text>
  <rect x="50" y="230" width="200" height="14" rx="7" fill="#eee" /><rect x="50" y="265" width="160" height="14" rx="7" fill="#eee" />
  <rect x="50" y="300" width="180" height="14" rx="7" fill="#eee" />
</svg>"""

BALLON = """<svg viewBox="0 0 300 420" style="width:100%;height:100%">
  <path d="M150 330 Q140 370 160 410" fill="none" stroke="#353a3d" stroke-width="5" />
  <ellipse cx="150" cy="170" rx="130" ry="155" fill="#e24b4b" />
  <path d="M135 322 L165 322 L150 340 Z" fill="#c23b3b" />
  <ellipse cx="100" cy="100" rx="25" ry="45" fill="#fff" opacity="0.3" />
  <text x="150" y="215" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" fill="#fff">%</text>
</svg>"""

PUFF = """<svg viewBox="0 0 400 300" style="width:100%;height:100%">
  <g fill="#d9dde0"><circle cx="140" cy="160" r="70" /><circle cx="230" cy="130" r="85" /><circle cx="300" cy="180" r="60" /><circle cx="190" cy="210" r="60" /></g>
</svg>"""

COIN = '<div style="width:100%;height:100%;border-radius:50%;background:#f2c418;border:8px solid #c99a06;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:60px;color:#7a5a00">€</div>'

GEARS = """<svg viewBox="0 0 400 400" style="width:100%;height:100%">
  <g id="gear1"><circle cx="120" cy="130" r="58" fill="none" stroke="#353a3d" stroke-width="26" stroke-dasharray="22 14" /><circle cx="120" cy="130" r="30" fill="#353a3d" /></g>
  <g id="gear2"><circle cx="300" cy="120" r="42" fill="none" stroke="#9aa3a8" stroke-width="22" stroke-dasharray="18 12" /><circle cx="300" cy="120" r="20" fill="#9aa3a8" /></g>
  <circle cx="200" cy="260" r="100" fill="#f2c418" stroke="#c99a06" stroke-width="8" />
  <text x="200" y="300" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="120" fill="#c99a06">€</text>
</svg>"""

SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Dein Geld auf dem<br />Konto <span style="color:#e24b4b">schrumpft</span>') +
     box("intro-schein", 140, 620, 800, 440, SCHEIN),
     lambda t0, d: snap_in("#intro-title", t0) + f"""
      tl.fromTo("#intro-schein", {{ scale: 1 }}, {{ scale: 0.62, duration: {d}, ease: "power1.in" }}, {t0});"""),

    ("merkst", "s2", "s2",
     box("ms-phone", 390, 380, 300, 560, PHONE) +
     '<div id="ms-eq" class="big" style="position:absolute;left:0;top:980px;width:1080px;font-size:72px">sieht gleich aus …</div>',
     lambda t0, d: f"""
      pop("#ms-phone", {t0});
      pop("#ms-eq", {t0} + 0.6);"""),

    ("grund", "s3", "s3",
     '<div id="gr-word" class="big" style="position:absolute;left:0;top:340px;width:1080px;font-size:130px;color:#e24b4b">Inflation</div>' +
     box("gr-ballon", 340, 560, 400, 560, BALLON),
     lambda t0, d: f"""
      pop("#gr-word", {t0});
      tl.fromTo("#gr-ballon", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: {min(1.6, d)}, ease: "power1.out" }}, {t0} + 0.1);"""),

    ("rechnung", "s4", "s4",
     '<div class="big" style="position:absolute;left:0;top:340px;width:1080px">'
     '<div id="rc-a" style="font-size:130px;color:#1f7a4d">10.000€</div>'
     '<div id="rc-mid" style="height:250px;display:flex;justify-content:center;align-items:center;gap:30px"><svg viewBox="0 0 70 110" style="width:110px;height:190px"><path d="M35 6 L35 96 M14 76 L35 100 L56 76" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg>'
     '<div style="font-family:Montserrat;font-weight:800;font-size:48px;text-align:left;color:#353a3d">10 Jahre<br />2,5 % Inflation</div></div>'
     '<div id="rc-b" style="font-size:150px;color:#e24b4b">≈ 7.800€</div>'
     '<div id="rc-sub" style="font-family:Montserrat;font-weight:700;font-size:44px;color:#353a3d">Kaufkraft von heute</div></div>',
     lambda t0, d: f"""
      pop("#rc-a", {t0});
      pop("#rc-mid", {c('s4', 1)});
      pop("#rc-b", {c('s4', 3)} - 0.3);
      pop("#rc-sub", {c('s4', 3)});"""),

    ("verlust", "s5", "s5",
     '<div id="vl-num" class="big" style="position:absolute;left:0;top:420px;width:1080px;font-size:190px;color:#e24b4b">−2.200€</div>'
     '<svg id="vl-arrow" viewBox="0 0 100 160" style="position:absolute;left:470px;top:700px;width:140px;height:224px"><path d="M50 10 L50 140 M15 105 L50 145 L85 105" fill="none" stroke="#e24b4b" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" /></svg>'
     '<div id="vl-sub" style="position:absolute;left:0;top:960px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:64px;color:#111">Kaufkraft weg</div>',
     lambda t0, d: f"""
      pop("#vl-num", {t0});
      tl.fromTo("#vl-arrow", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power2.out" }}, {t0} + 0.3);
      pop("#vl-sub", {c('s5', 1)});"""),

    ("weg", "s6", "s6",
     box("weg-coin", 390, 520, 300, 300, COIN) + box("weg-puff", 240, 470, 600, 450, PUFF),
     lambda t0, d: f"""
      tl.fromTo("#weg-coin", {{ scale: 1, opacity: 1 }}, {{ scale: 0.3, opacity: 0, duration: 0.35, ease: "power2.in" }}, {t0} + 0.15);
      tl.fromTo("#weg-puff", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {t0} + 0.3);"""),

    ("notgroschen", "s7", "s7",
     '<div id="ng-head" class="big" style="position:absolute;left:0;top:330px;width:1080px;font-size:100px">Notgroschen</div>' +
     box("ng-pig", 270, 520, 540, 468, SPARSCHWEIN) +
     '<div id="ng-chip" style="position:absolute;left:0;top:1030px;width:1080px;display:flex;justify-content:center"><div class="chip" style="font-family:Montserrat;font-weight:800;font-size:56px;padding:14px 40px;border-radius:24px;background:var(--brand);color:#fff">3 × Monatsausgaben</div></div>',
     lambda t0, d: f"""
      pop("#ng-head", {t0});
      pop("#ng-pig", {t0} + 0.2);
      pop("#ng-chip", {c('s7', 2)});"""),

    ("arbeiten", "s8", "s8",
     box("ab-dog", 40, 520, 460, 460, BEAGLE) + box("ab-gears", 480, 440, 560, 560, GEARS),
     lambda t0, d: f"""
      pop("#ab-dog", {t0});
      pop("#ab-gears", {t0} + 0.2);
      tl.fromTo("#gear1", {{ rotation: 0 }}, {{ rotation: 120, duration: {d}, ease: "none", svgOrigin: "120 130" }}, {t0});
      tl.fromTo("#gear2", {{ rotation: 0 }}, {{ rotation: -160, duration: {d}, ease: "none", svgOrigin: "300 120" }}, {t0});"""),

    ("outro", "s9", "s9", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
