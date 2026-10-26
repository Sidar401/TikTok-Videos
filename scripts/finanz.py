"""Gemeinsame Bausteine für HundeFinanzTV-Videos.

Ein Video-`build.py` definiert nur noch SCENES und ruft `build(HERE, SCENES)` auf:
  SCENES = [(id, von_satz, bis_satz, html, lambda t0, d: js), ...]
Hilfen: `T(here)` lädt timings.json, `cap(T, satz, i)` = Start der i-ten Untertitel-Box.
"""
import json
from pathlib import Path

BEAGLE = '<img src="assets/beagle.png" alt="" style="width:100%;height:100%;object-fit:contain" />'


def T(here):
    return json.loads((Path(here) / "timings.json").read_text())


def cap(t, sid, i):
    s = next(x for x in t["saetze"] if x["id"] == sid)
    return s["captions"][min(i, len(s["captions"]) - 1)]["start"]


def title(id_, html, top=290, size=92):
    """Großer Hook-Titel (ab Frame 0 sichtbar)."""
    return (f'<div id="{id_}" style="position:absolute;top:{top}px;left:40px;width:1000px;text-align:center;'
            f'font-family:Montserrat;font-weight:800;font-size:{size}px;line-height:1.05;color:#111">{html}</div>')


def snap_in(sel, t0, s=1.05):
    """Einrasten ohne Einblenden (für Frame 0)."""
    return f'\n      tl.fromTo("{sel}", {{ scale: {s} }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});'


def box(id_, left, top, w, h, inner, extra=""):
    return f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;{extra}">{inner}</div>'


GELDSACK = """<svg viewBox="0 0 400 400" style="width:100%;height:100%">
  <g fill="#f2c418" stroke="#c99a06" stroke-width="3">
    <rect x="250" y="300" width="110" height="22" rx="8" /><rect x="250" y="276" width="110" height="22" rx="8" />
    <rect x="250" y="252" width="110" height="22" rx="8" /><rect x="250" y="228" width="110" height="22" rx="8" />
    <rect x="250" y="204" width="110" height="22" rx="8" /><rect x="265" y="180" width="110" height="22" rx="8" />
  </g>
  <path d="M150 110 C120 70 140 50 160 70 C175 50 205 50 220 70 C240 50 260 70 230 110 Z" fill="#1f7a4d" />
  <rect x="145" y="104" width="90" height="18" rx="9" fill="#f2c418" />
  <path d="M150 120 C60 170 40 330 120 340 L260 340 C340 330 320 170 230 120 Z" fill="#1f7a4d" />
  <path d="M155 135 C90 180 75 300 125 325" fill="none" stroke="#2c9a63" stroke-width="10" stroke-linecap="round" />
  <circle cx="190" cy="245" r="62" fill="#f2c418" />
  <text x="190" y="272" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="80" fill="#1f7a4d">€</text>
</svg>"""

SPARSCHWEIN = """<svg viewBox="0 0 300 260" style="width:100%;height:100%">
  <ellipse cx="150" cy="150" rx="120" ry="90" fill="#f4a6b5" />
  <circle cx="250" cy="140" r="38" fill="#f4a6b5" /><ellipse cx="265" cy="140" rx="20" ry="16" fill="#e98a9c" />
  <circle cx="258" cy="136" r="4" fill="#8a3a4a" /><circle cx="272" cy="136" r="4" fill="#8a3a4a" />
  <circle cx="215" cy="110" r="7" fill="#111" /><path d="M200 70 L225 40 L235 80 Z" fill="#e98a9c" />
  <rect x="85" y="225" width="30" height="34" rx="10" fill="#e98a9c" /><rect x="180" y="225" width="30" height="34" rx="10" fill="#e98a9c" />
  <rect x="120" y="62" width="70" height="12" rx="6" fill="#8a3a4a" />
</svg>"""

CHECK = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><circle cx="50" cy="50" r="46" fill="#1f7a4d" /><path d="M28 52 L44 68 L74 36" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>'
CROSS = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><circle cx="50" cy="50" r="46" fill="#e24b4b" /><path d="M32 32 L68 68 M68 32 L32 68" stroke="#fff" stroke-width="11" stroke-linecap="round" /></svg>'


def balken(p, a_val, a_lab, b_val, b_lab, ratio, a_col="#1f7a4d", b_col="#f2c418", b_txt="#c99a06", top=""):
    """Zwei Balken (Vergleich). ratio = Höhe A / Höhe B. Liefert (html, js(t0, t_b))."""
    hb, ha = 232, max(30, round(232 * ratio))
    ya, yb = 350 - ha, 350 - hb
    html = f'''<svg viewBox="0 0 400 400" style="width:100%;height:100%">
          <line x1="30" y1="350" x2="370" y2="350" stroke="#111" stroke-width="6" />
          <rect id="{p}-b1" x="70" y="{ya}" width="110" height="{ha}" fill="{a_col}" />
          <rect id="{p}-b2" x="220" y="{yb}" width="110" height="{hb}" fill="{b_col}" />
          <text id="{p}-l1" x="125" y="{ya - 15}" text-anchor="middle" class="serif" font-size="32" fill="{a_col}">{a_val}</text>
          <text id="{p}-l2" x="275" y="{yb - 15}" text-anchor="middle" class="serif" font-size="32" fill="{b_txt}">{b_val}</text>
          <text x="125" y="385" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="22" fill="#353a3d">{a_lab}</text>
          <text x="275" y="385" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="22" fill="#353a3d">{b_lab}</text>
          {top}
        </svg>'''

    def js(t0, tb):
        return f'''
      tl.fromTo("#{p}-b1", {{ attr: {{ y: 350, height: 0 }} }}, {{ attr: {{ y: {ya}, height: {ha} }}, duration: 0.5, ease: "power2.out" }}, {t0});
      pop("#{p}-l1", {t0} + 0.4);
      tl.fromTo("#{p}-b2", {{ attr: {{ y: 350, height: 0 }} }}, {{ attr: {{ y: {yb}, height: {hb} }}, duration: 0.8, ease: "power2.out" }}, {tb});
      pop("#{p}-l2", {tb} + 0.7);'''
    return html, js


def outro(t0):
    html = """
        <div style="position:absolute;left:0;top:330px;width:1080px;display:flex;flex-direction:column;align-items:center;gap:30px">
          <div id="outro-dog" style="width:520px;height:520px">""" + BEAGLE + """</div>
          <div id="outro-name" style="font-family:Montserrat;font-weight:800;font-size:92px;color:#111">HundeFinanzTV</div>
          <div id="outro-btn" style="padding:18px 64px;border-radius:60px;background:var(--brand);color:#fff;font-family:Montserrat;font-weight:700;font-size:56px">+ Folgen</div>
        </div>"""
    return html


def outro_js(t0, d):
    return f"""
      pop("#outro-dog", {t0});
      pop("#outro-name", {t0} + 0.25);
      pop("#outro-btn", {t0} + 0.5);
      tl.fromTo("#outro-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {t0} + 1.1);"""


EXTRA_CSS = """
      .scene { position: absolute; inset: 0; top: 0; height: 1920px; display: block; }
      .tile { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 30px 10px; border-radius: 30px; background: #faf5ef; }
      .tile svg { width: 230px; height: 230px; }
      .tile span { font-family: Montserrat; font-weight: 800; font-size: 54px; color: #111; }
      .big { font-family: var(--font-display); text-align: center; color: #111; }
      .cap span { max-width: 990px; font-size: 50px; }
    </style>"""


def build(here, scenes):
    here = Path(here)
    t = T(here)
    S = {s["id"]: s for s in t["saetze"]}
    dauer = t["dauer"]
    tpl = (here / "index.html").read_text()
    head = tpl[: tpl.index("<body>")]
    if ".tile {" not in head:
        head = head.replace("    </style>", EXTRA_CSS, 1)
    last = t["saetze"][-1]["id"]
    out_scenes, js, caps = [], [], []
    for sid, a, b, html, code in scenes:
        t0 = S[a]["start"]
        t1 = dauer if b == last else S[b]["end"]
        d = round(t1 - t0, 3)
        out_scenes.append(f'      <div id="{sid}" class="scene clip" data-start="{t0}" data-duration="{d}" data-track-index="1">{html}\n      </div>')
        js.append(f"      // {sid}\n      (() => {{{code(t0, d)}\n      }})();")
    n = 0
    for s in t["saetze"]:
        for cp in s["captions"]:
            n += 1
            caps.append(f'        <div id="c{n}" class="cap clip" data-start="{cp["start"]}" data-duration="{round(cp["end"] - cp["start"], 3)}" data-track-index="2"><span>{cp["text"]}</span></div>')
    body = f"""<body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dauer}" data-width="1080" data-height="1920">
{chr(10).join(out_scenes)}

      <div id="brand"><span>HundeFinanzTV</span></div>
      <div id="frame"></div>

      <div id="captions" data-track-kind="captions">
{chr(10).join(caps)}
      </div>

      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{dauer}" data-track-index="3"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      const pop = (sel, at) =>
        tl.fromTo(sel, {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, at);
      const zaehl = (sel, von, bis, at, dur, nach) => {{
        const o = {{ v: von }};
        tl.fromTo(o, {{ v: von }}, {{ v: bis, duration: dur, ease: "power1.out", onUpdate: () => {{
          document.querySelector(sel).textContent = Math.round(o.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + (nach || ""); }} }}, at);
      }};
      const draw = (sel, at, dur) => {{
        const len = document.querySelector(sel).getTotalLength();
        tl.fromTo(sel, {{ strokeDasharray: len, strokeDashoffset: len }}, {{ strokeDashoffset: 0, duration: dur, ease: "power2.out" }}, at);
      }};

{chr(10).join(js)}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (here / "index.html").write_text(head + body)
    print("index.html gebaut,", dauer, "s")
