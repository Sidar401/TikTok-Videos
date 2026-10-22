#!/usr/bin/env python3
"""HundeFinanzTV: Dein Coffee to go kostet dich 170.000 €."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, GELDSACK, T, balken, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


CUP = """<svg viewBox="0 0 300 380" style="width:100%;height:100%">
  <path d="M60 110 L240 110 L215 350 Q150 368 85 350 Z" fill="#f6efe1" stroke="#353a3d" stroke-width="8" stroke-linejoin="round" />
  <path d="M70 190 L230 190 L220 290 L80 290 Z" fill="#DB8622" />
  <circle cx="150" cy="240" r="26" fill="#fff" opacity="0.9" />
  <rect x="45" y="78" width="210" height="40" rx="14" fill="#6b3f1f" />
  <rect x="80" y="58" width="140" height="28" rx="10" fill="#8a5a2b" />
  <g id="{p}-steam" fill="none" stroke="#b9c0c4" stroke-width="10" stroke-linecap="round">
    <path d="M110 40 Q95 20 110 0" /><path d="M150 40 Q135 20 150 0" /><path d="M190 40 Q175 20 190 0" />
  </g>
</svg>"""


def cup(p):
    return CUP.replace("{p}", p)


chart_html = """<svg viewBox="0 0 400 400" style="width:100%;height:100%">
  <path d="M40 40 L40 340 L370 340" fill="none" stroke="#111" stroke-width="8" stroke-linecap="square" />
  <path id="zins-solid" d="M60 300 C140 290 220 285 300 270" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" />
  <path id="zins-dots" d="M60 295 C170 270 240 200 300 95" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 16" />
  <text id="zins-label" class="serif" x="70" y="100" font-size="70" fill="#1f7a4d">~7%</text>
  <text id="zins-years" x="205" y="385" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#353a3d">30 Jahre</text>
  <g id="zins-check"><circle cx="320" cy="80" r="42" fill="#111" />
    <path d="M300 82 L315 97 L342 66" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></g>
</svg>"""

bars_html, bars_js = balken("vgl", "54.000€", "eingezahlt", "170.000€", "am Ende", 54 / 170,
                            top='<text id="vgl-x" x="200" y="50" text-anchor="middle" class="serif" font-size="56" fill="var(--brand)">x3</text>')

DAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
WEEK = '<div style="display:flex;gap:12px;justify-content:center">' + "".join(
    f'<div class="day"><span>{d}</span><div id="wk-{i}" style="width:120px;height:120px">{CHECK if i in (2, 5) else CROSS}</div></div>'
    for i, d in enumerate(DAYS)) + "</div>"

SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Dein Coffee to go<br />kostet dich') +
     '<div id="intro-num" class="big" style="position:absolute;left:0;top:520px;width:1080px;font-size:170px;color:#c99a06">170.000€</div>' +
     box("intro-cup", 390, 760, 300, 380, cup("ic")),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-num", t0, 1.1) + snap_in("#intro-cup", t0)),

    ("verrueckt", "s2", "s2",
     box("vr-cup", 330, 470, 420, 532, cup("vc")) +
     '<div id="vr-q" class="big" style="position:absolute;left:720px;top:380px;font-size:260px;color:#e24b4b">?!</div>',
     lambda t0, d: f"""
      pop("#vr-cup", {t0});
      tl.fromTo("#vr-cup", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.1, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {t0} + 0.3);
      pop("#vr-q", {t0} + 0.2);"""),

    ("tag", "s3", "s3",
     '<div class="big" style="position:absolute;left:0;top:360px;width:1080px">'
     '<div id="tag-a" style="font-size:140px">5€ <span style="font-size:80px">/ Tag</span></div>'
     '<div id="tag-arrow" style="height:230px;display:flex;justify-content:center;align-items:center"><svg viewBox="0 0 70 110" style="width:120px;height:200px"><path d="M35 6 L35 96 M14 76 L35 100 L56 76" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /></svg></div>'
     '<div id="tag-b" style="font-size:150px;color:#e24b4b">150€ <span style="font-size:80px;color:#111">/ Monat</span></div></div>',
     lambda t0, d: f"""
      pop("#tag-a", {t0});
      pop("#tag-arrow", {t0} + 0.4);
      pop("#tag-b", {c('s3', 1)});"""),

    ("kaum", "s4", "s4",
     """<svg viewBox="0 0 400 400" style="position:absolute;left:190px;top:400px;width:700px;height:700px">
          <circle id="kaum-coin" cx="170" cy="170" r="34" fill="#f2c418" stroke="#c99a06" stroke-width="6" />
          <text x="170" y="182" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#7a5a00">5€</text>
          <g id="kaum-lupe"><circle cx="170" cy="170" r="90" fill="none" stroke="#353a3d" stroke-width="20" />
            <line x1="235" y1="235" x2="340" y2="340" stroke="#353a3d" stroke-width="30" stroke-linecap="round" /></g>
        </svg>""",
     lambda t0, d: f"""
      pop("#kaum-coin", {t0});
      tl.fromTo("#kaum-lupe", {{ x: 120, y: 120, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t0} + 0.2);"""),

    ("zins", "s5", "s5",
     box("zins-art", 130, 330, 820, 820, chart_html),
     lambda t0, d: f"""
      draw("#zins-solid", {t0}, 0.6);
      tl.fromTo("#zins-dots", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {t0} + 0.4);
      pop("#zins-years", {t0} + 0.5);
      pop("#zins-label", {c('s5', 1)});
      pop("#zins-check", {c('s5', 1)} + 0.4);"""),

    ("ende", "s6", "s6",
     box("ende-sack", 240, 330, 600, 600, GELDSACK) +
     '<div id="ende-num" class="big" style="position:absolute;left:0;top:960px;width:1080px;font-size:160px;color:#c99a06">170.000€</div>',
     lambda t0, d: f"""
      pop("#ende-sack", {t0});
      pop("#ende-num", {c('s6', 1)});
      tl.fromTo("#ende-num", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 }}, {c('s6', 1)} + 0.45);"""),

    ("vergleich", "s7", "s7",
     box("vgl-art", 130, 330, 820, 820, bars_html),
     lambda t0, d: bars_js(t0, t0 + 0.6) + f'\n      pop("#vgl-x", {t0} + 1.4);'),

    ("kaffee-ok", "s8", "s8",
     box("ok-dog", 60, 450, 480, 480, BEAGLE) + box("ok-cup", 600, 470, 340, 430, cup("oc")) +
     box("ok-check", 820, 380, 160, 160, CHECK),
     lambda t0, d: f"""
      pop("#ok-dog", {t0});
      pop("#ok-cup", {t0} + 0.2);
      pop("#ok-check", {c('s8', 1)});"""),

    ("woche", "s9", "s9",
     '<div id="wk-title" class="big" style="position:absolute;left:0;top:400px;width:1080px;font-size:96px">nicht jeden Tag</div>'
     '<div style="position:absolute;left:0;top:640px;width:1080px">' + WEEK + '</div>',
     lambda t0, d: f'\n      pop("#wk-title", {t0});' + "".join(f'\n      pop("#wk-{i}", {t0} + {0.25 + i * 0.12:.2f});' for i in range(7))),

    ("outro", "s10", "s10", outro(0), outro_js),
]

EXTRA = """
      .day { display: flex; flex-direction: column; align-items: center; gap: 12px; font-family: Montserrat; font-weight: 800; font-size: 46px; color: #353a3d; }
    </style>"""

if __name__ == "__main__":
    build(HERE, SCENES)
    p = HERE / "index.html"
    s = p.read_text()
    if ".day {" not in s:
        p.write_text(s.replace("    </style>", EXTRA, 1))
