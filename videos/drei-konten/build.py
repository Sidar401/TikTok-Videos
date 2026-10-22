#!/usr/bin/env python3
"""HundeFinanzTV: Das Drei-Konten-Modell."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, SPARSCHWEIN, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)


def c(sid, i):
    return cap(t, sid, i)


FARBEN = {1: "#3d7be0", 2: "#1f7a4d", 3: "#DB8622"}
NAMEN = {1: "Girokonto", 2: "Tagesgeld", 3: "Depot"}


def karte(nr, label=None, nummer=True):
    label = label or NAMEN.get(nr, "")
    col = FARBEN.get(nr, "#353a3d")
    num = f'<circle cx="345" cy="55" r="34" fill="#fff" /><text x="345" y="70" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="{col}">{nr}</text>' if nummer else ""
    return f"""<svg viewBox="0 0 400 250" style="width:100%;height:100%">
  <rect x="5" y="5" width="390" height="240" rx="26" fill="{col}" />
  <rect x="40" y="70" width="70" height="52" rx="10" fill="#f2c418" />
  <line x1="40" y1="96" x2="110" y2="96" stroke="#c99a06" stroke-width="4" />
  {num}
  <text x="40" y="200" font-family="Montserrat" font-weight="800" font-size="44" fill="#fff">{label}</text>
</svg>"""


def icon_tile(id_, svg, label):
    return (f'<div id="{id_}" style="display:flex;flex-direction:column;align-items:center;gap:8px">'
            f'<div style="width:170px;height:170px;border-radius:30px;background:#faf5ef;padding:24px"><svg viewBox="0 0 100 100" style="width:100%;height:100%">{svg}</svg></div>'
            f'<span style="font-family:Montserrat;font-weight:800;font-size:44px;color:#111">{label}</span></div>')


HAUS = '<path d="M10 50 L50 15 L90 50 L80 50 L80 88 L20 88 L20 50 Z" fill="#DB8622" /><rect x="42" y="60" width="16" height="28" fill="#fff" />'
KORB = '<path d="M12 30 L88 30 L78 75 L22 75 Z" fill="#1f7a4d" /><circle cx="32" cy="86" r="7" fill="#353a3d" /><circle cx="68" cy="86" r="7" fill="#353a3d" /><path d="M12 30 L5 15" stroke="#353a3d" stroke-width="6" stroke-linecap="round" />'
BLITZ = '<path d="M58 6 L22 56 L46 56 L38 94 L78 40 L52 40 Z" fill="#f2c418" stroke="#c99a06" stroke-width="4" stroke-linejoin="round" />'
EURO = '<div style="width:100%;height:100%;border-radius:50%;background:#f2c418;border:10px solid #c99a06;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:{s}px;color:#7a5a00">€</div>'
CHART = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M10 85 L40 55 L60 68 L90 25" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /><path d="M70 22 L92 22 L92 44" fill="none" stroke="#1f7a4d" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" /></svg>'
PFEIL = '<svg viewBox="0 0 120 60" style="width:100%;height:100%"><path d="M8 30 L100 30 M76 8 L104 30 L76 52" fill="none" stroke="#111" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></svg>'
BLASE = """<svg viewBox="0 0 300 260" style="width:100%;height:100%">
  <path d="M30 20 L270 20 Q290 20 290 40 L290 170 Q290 190 270 190 L120 190 L60 245 L75 190 L30 190 Q10 190 10 170 L10 40 Q10 20 30 20 Z" fill="#fff" stroke="#111" stroke-width="10" stroke-linejoin="round" />
  <circle cx="95" cy="105" r="16" fill="#111" /><circle cx="150" cy="105" r="16" fill="#111" /><circle cx="205" cy="105" r="16" fill="#111" />
</svg>"""


def big(id_, txt, top, size=120, col="#111"):
    return f'<div id="{id_}" class="big" style="position:absolute;left:0;top:{top}px;width:1080px;font-size:{size}px;color:{col}">{txt}</div>'


SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Warum <span style="color:#e24b4b">ein</span> Konto<br />nicht reicht') +
     box("intro-card", 290, 600, 500, 312, karte(0, "Mein Konto", nummer=False)) + big("intro-q", "?", 930, 220, "#e24b4b"),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-card", t0) + f'\n      pop("#intro-q", {t0} + 0.4);'),

    ("chaos", "s2", "s2",
     box("ch-card", 290, 520, 500, 312, karte(0, "Mein Konto", nummer=False)) +
     big("ch-q1", "?", 380, 160, "#e24b4b").replace("left:0;", "left:-300px;") + big("ch-q2", "?", 440, 140, "#e24b4b").replace("left:0;", "left:330px;") +
     big("ch-txt", "Wie viel darf ich ausgeben?", 900, 64),
     lambda t0, d: f"""
      pop("#ch-card", {t0});
      pop("#ch-q1", {t0} + 0.3);
      pop("#ch-q2", {t0} + 0.5);
      pop("#ch-txt", {c('s2', 1)});"""),

    ("modell", "s3", "s3",
     big("md-title", "3-Konten-Modell", 350, 104) +
     box("md-1", 60, 620, 300, 188, karte(1)) + box("md-2", 390, 620, 300, 188, karte(2)) + box("md-3", 720, 620, 300, 188, karte(3)),
     lambda t0, d: f'\n      pop("#md-title", {t0});' + "".join(f'\n      pop("#md-{i}", {t0} + {0.3 + i * 0.25:.2f});' for i in (1, 2, 3))),

    ("giro", "s4", "s4", box("gi-card", 190, 480, 700, 437, karte(1)),
     lambda t0, d: f'\n      pop("#gi-card", {t0});'),

    ("fluss", "s5", "s5",
     box("fl-card", 290, 330, 500, 312, karte(1)) + box("fl-euro", 100, 400, 150, 150, EURO.format(s=70)) +
     '<div id="fl-out" style="position:absolute;left:0;top:760px;width:1080px;display:flex;justify-content:center;gap:40px">' +
     icon_tile("fl-i1", HAUS, "Miete") + icon_tile("fl-i2", KORB, "Essen") + icon_tile("fl-i3", BLITZ, "Strom") + '</div>',
     lambda t0, d: f"""
      pop("#fl-card", {t0});
      tl.fromTo("#fl-euro", {{ x: -200, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "power2.out" }}, {t0} + 0.2);""" + "".join(
         f'\n      pop("#fl-i{i}", {c("s5", 1)} + {(i - 1) * 0.3:.2f});' for i in (1, 2, 3))),

    ("tagesgeld", "s6", "s6", box("tg-card", 190, 480, 700, 437, karte(2)),
     lambda t0, d: f'\n      pop("#tg-card", {t0});'),

    ("notgroschen", "s7", "s7",
     box("ng-pig", 270, 360, 540, 468, SPARSCHWEIN) +
     big("ng-txt", "3 × Monatsausgaben", 880, 76) + big("ng-zins", "+ Zinsen", 1000, 90, "#1f7a4d"),
     lambda t0, d: f"""
      pop("#ng-pig", {t0});
      pop("#ng-txt", {c('s7', 1)});
      pop("#ng-zins", {c('s7', 2)});"""),

    ("depot", "s8", "s8", box("dp-card", 190, 480, 700, 437, karte(3)),
     lambda t0, d: f'\n      pop("#dp-card", {t0});'),

    ("sparplan", "s9", "s9",
     box("sp-euro", 90, 520, 220, 220, EURO.format(s=100)) + box("sp-p1", 330, 590, 160, 80, PFEIL) +
     box("sp-card", 510, 480, 480, 300, karte(3)) + box("sp-chart", 640, 820, 220, 220, CHART) +
     big("sp-auto", "automatisch", 360, 90, "var(--brand)"),
     lambda t0, d: f"""
      pop("#sp-euro", {t0});
      pop("#sp-p1", {t0} + 0.3);
      pop("#sp-card", {t0} + 0.5);
      pop("#sp-auto", {c('s9', 1)});
      pop("#sp-chart", {c('s9', 2)});"""),

    ("sortiert", "s10", "s10",
     box("so-euro", 440, 330, 200, 200, EURO.format(s=90)) +
     """<svg id="so-lines" viewBox="0 0 1080 300" style="position:absolute;left:0;top:540px;width:1080px;height:300px">
        <path d="M540 0 L210 240 M540 0 L540 240 M540 0 L870 240" stroke="#111" stroke-width="8" stroke-linecap="round" fill="none" />
      </svg>""" +
     box("so-1", 60, 820, 300, 188, karte(1)) + box("so-2", 390, 820, 300, 188, karte(2)) + box("so-3", 720, 820, 300, 188, karte(3)),
     lambda t0, d: f"""
      pop("#so-euro", {t0});
      tl.fromTo("#so-lines", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {t0} + 0.3);""" + "".join(
         f'\n      pop("#so-{i}", {t0} + {0.5 + i * 0.2:.2f});' for i in (1, 2, 3))),

    ("blick", "s11", "s11",
     box("bl-dog", 40, 500, 460, 460, BEAGLE) + box("bl-card", 530, 560, 480, 300, karte(1)) + box("bl-check", 470, 470, 150, 150, CHECK) +
     big("bl-txt", "= dein Budget", 920, 76).replace("left:0;width:1080px", "left:500px;width:540px"),
     lambda t0, d: f"""
      pop("#bl-dog", {t0});
      pop("#bl-card", {t0} + 0.2);
      pop("#bl-check", {c('s11', 1)});
      pop("#bl-txt", {c('s11', 1)} + 0.2);"""),

    ("frage", "s12", "s12",
     big("fr-q", "Wie viele Konten<br />hast du?", 360, 100) +
     '<div style="position:absolute;left:0;top:720px;width:1080px;display:flex;justify-content:center;gap:50px">' + "".join(
         f'<div id="fr-{i}" style="width:200px;height:200px;border-radius:50%;background:{FARBEN[i]};display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:800;font-size:110px;color:#fff">{i}</div>'
         for i in (1, 2, 3)) + '</div>',
     lambda t0, d: f'\n      pop("#fr-q", {t0});' + "".join(f'\n      pop("#fr-{i}", {t0} + {0.2 + i * 0.15:.2f});' for i in (1, 2, 3))),

    ("kommentar", "s13", "s13",
     box("km-blase", 290, 400, 500, 433, BLASE) + big("km-txt", "Schreib's in<br />die Kommentare!", 900, 84, "var(--brand)"),
     lambda t0, d: f"""
      pop("#km-blase", {t0});
      tl.fromTo("#km-blase", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.35);
      pop("#km-txt", {t0} + 0.2);"""),

    ("outro", "s14", "s14", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
