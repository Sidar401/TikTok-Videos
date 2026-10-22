#!/usr/bin/env python3
"""HundeFinanzTV: Die 72er-Regel – wann verdoppelt sich dein Geld?"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CROSS, GELDSACK, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


def coin(txt="€", size=60):
    return (f'<div style="width:100%;height:100%;border-radius:50%;background:#f2c418;border:10px solid #c99a06;'
            f'display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:{size}px;color:#7a5a00">{txt}</div>')


SNAIL = """<svg viewBox="0 0 400 260" style="width:100%;height:100%">
  <path d="M30 230 Q60 200 120 205 L330 205 Q370 205 370 230 Z" fill="#9bc27a" />
  <circle cx="200" cy="140" r="85" fill="#DB8622" />
  <circle cx="200" cy="140" r="58" fill="none" stroke="#a8621a" stroke-width="12" /><circle cx="200" cy="140" r="30" fill="none" stroke="#a8621a" stroke-width="12" />
  <path d="M300 205 Q330 150 320 110" fill="none" stroke="#9bc27a" stroke-width="24" stroke-linecap="round" />
  <line x1="318" y1="112" x2="300" y2="70" stroke="#6f9a52" stroke-width="7" /><line x1="326" y1="112" x2="345" y2="72" stroke="#6f9a52" stroke-width="7" />
  <circle cx="300" cy="68" r="9" fill="#353a3d" /><circle cx="346" cy="70" r="9" fill="#353a3d" />
</svg>"""

STEPS = [("0", "10.000€", 80), ("10", "20.000€", 160), ("20", "40.000€", 320)]
TREPPE = '<div style="display:flex;align-items:flex-end;justify-content:center;gap:50px;height:640px">' + "".join(
    f'<div id="tr-{i}" style="display:flex;flex-direction:column;align-items:center;gap:14px">'
    f'<div class="serif" style="font-size:52px;color:{"#1f7a4d" if i == 0 else "#c99a06"}">{v}</div>'
    f'<div style="width:200px;height:{h * 1.4:.0f}px;background:{"#1f7a4d" if i == 0 else "#f2c418"};border-radius:12px 12px 0 0"></div>'
    f'<div style="font-family:Montserrat;font-weight:800;font-size:40px;color:#353a3d">{y} Jahre</div></div>'
    for i, (y, v, h) in enumerate(STEPS)) + "</div>"

SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Wann <span style="color:var(--brand)">verdoppelt</span><br />sich dein Geld?') +
     box("intro-c1", 230, 640, 260, 260, coin()) + box("intro-c2", 590, 640, 260, 260, coin()) +
     '<div id="intro-x2" class="big" style="position:absolute;left:0;top:950px;width:1080px;font-size:150px;color:#1f7a4d">×2</div>',
     lambda t0, d: snap_in("#intro-title", t0) + f"""
      tl.fromTo("#intro-c1", {{ x: 180, scale: 1.05 }}, {{ x: 180, scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});
      tl.to("#intro-c1", {{ x: 0, duration: 0.35, ease: "power2.out" }}, {c('s1', 2)} - 0.2);
      pop("#intro-c2", {c('s1', 2)});
      pop("#intro-x2", {c('s1', 2)} + 0.3);"""),

    ("regel", "s2", "s2",
     '<div id="rg-badge" style="position:absolute;left:290px;top:420px;width:500px;height:500px;border-radius:50%;background:var(--brand);display:flex;flex-direction:column;align-items:center;justify-content:center">'
     '<div class="serif" style="font-size:230px;line-height:1;color:#fff">72</div>'
     '<div style="font-family:Montserrat;font-weight:800;font-size:64px;color:#fff">Regel</div></div>',
     lambda t0, d: f"""
      pop("#rg-badge", {t0});
      tl.fromTo("#rg-badge", {{ rotation: -8 }}, {{ rotation: 0, duration: 0.6, ease: "back.out(3)" }}, {t0});"""),

    ("formel", "s3", "s3",
     '<div id="fm-text" class="big" style="position:absolute;left:0;top:360px;width:1080px;font-size:118px;line-height:1.25">72 ÷ Zins<br /><span style="color:var(--brand)">= Jahre</span></div>' +
     box("fm-dog", 300, 760, 480, 480, BEAGLE),
     lambda t0, d: f"""
      pop("#fm-text", {t0});
      pop("#fm-dog", {c('s3', 1)});"""),

    ("sieben", "s4", "s4",
     '<div class="big" style="position:absolute;left:0;top:400px;width:1080px">'
     '<div id="sv-a" style="font-size:150px">72 ÷ 7</div>'
     '<div id="sv-b" style="font-size:190px;color:#1f7a4d">≈ 10</div>'
     '<div id="sv-c" style="font-family:Montserrat;font-weight:800;font-size:72px;color:#111">Jahre</div></div>',
     lambda t0, d: f"""
      pop("#sv-a", {t0});
      pop("#sv-b", {c('s4', 1)});
      pop("#sv-c", {c('s4', 1)} + 0.2);"""),

    ("doppelt", "s5", "s5",
     box("dp-s1", 90, 560, 320, 320, GELDSACK) +
     '<div id="dp-l1" class="big" style="position:absolute;left:60px;top:900px;width:380px;font-size:72px;color:#1f7a4d">10.000€</div>'
     '<svg id="dp-arrow" viewBox="0 0 120 60" style="position:absolute;left:440px;top:680px;width:180px;height:90px"><path d="M8 30 L100 30 M76 8 L104 30 L76 52" fill="none" stroke="#111" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></svg>' +
     box("dp-s2", 590, 450, 400, 400, GELDSACK) +
     '<div id="dp-l2" class="big" style="position:absolute;left:560px;top:880px;width:460px;font-size:86px;color:#c99a06">20.000€</div>',
     lambda t0, d: f"""
      pop("#dp-s1", {t0});
      pop("#dp-l1", {t0} + 0.2);
      pop("#dp-arrow", {c('s5', 1)} - 0.3);
      pop("#dp-s2", {c('s5', 1)});
      pop("#dp-l2", {c('s5', 1)} + 0.2);"""),

    ("treppe", "s6", "s6",
     '<div style="position:absolute;left:0;top:420px;width:1080px">' + TREPPE + '</div>',
     lambda t0, d: "".join(f'\n      pop("#tr-{i}", {t0} + {i * 0.45:.2f});' for i in range(3))),

    ("schnecke", "s7", "s7",
     '<div id="sn-head" class="big" style="position:absolute;left:0;top:340px;width:1080px;font-size:96px">Tagesgeld <span style="color:#1f7a4d">2 %</span></div>' +
     box("sn-snail", 190, 560, 700, 455, SNAIL) +
     '<div id="sn-years" class="big" style="position:absolute;left:0;top:1060px;width:1080px;font-size:110px;color:#e24b4b">36 Jahre</div>',
     lambda t0, d: f"""
      pop("#sn-head", {t0});
      tl.fromTo("#sn-snail", {{ x: -120, opacity: 0 }}, {{ x: 40, opacity: 1, duration: {d}, ease: "none" }}, {t0} + 0.1);
      pop("#sn-years", {c('s7', 1)});"""),

    ("nie", "s8", "s8",
     '<div id="ni-head" class="big" style="position:absolute;left:0;top:360px;width:1080px;font-size:96px">Girokonto <span style="color:#9aa3a8">0 %</span></div>' +
     box("ni-c", 390, 560, 300, 300, coin()) + box("ni-x", 600, 520, 160, 160, CROSS) +
     '<div id="ni-nie" class="big" style="position:absolute;left:0;top:930px;width:1080px;font-size:170px;color:#e24b4b">nie ×2</div>',
     lambda t0, d: f"""
      pop("#ni-head", {t0});
      pop("#ni-c", {t0} + 0.2);
      pop("#ni-x", {c('s8', 2)} - 0.3);
      pop("#ni-nie", {c('s8', 2)});"""),

    ("outro", "s9", "s9", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
