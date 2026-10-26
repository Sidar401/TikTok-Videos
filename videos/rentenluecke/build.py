#!/usr/bin/env python3
"""HundeFinanzTV: Wie viel Rente bekommst du wirklich? (Kommentar-CTA). Leitmotiv: die Rentenlücke als Balken, die am Ende gefüllt wird."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402
from icons import BLASE, UHR, person  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}
GRUEN, ROT, OR, GRAU = "#1f7a4d", "#e24b4b", "#DB8622", "#9aa3a8"


def c(sid, i):
    return cap(t, sid, i)


def big(id_, txt, top, size=120, col="#111"):
    return f'<div id="{id_}" class="big" style="position:absolute;left:0;top:{top}px;width:1080px;font-size:{size}px;line-height:1.05;color:{col}">{txt}</div>'


def sub(id_, txt, top, size=58, col="#111"):
    return f'<div id="{id_}" style="position:absolute;left:60px;top:{top}px;width:960px;text-align:center;font-family:Montserrat;font-weight:800;font-size:{size}px;line-height:1.15;color:{col}">{txt}</div>'


RENTNERIN = f"""<svg viewBox="0 0 100 100" style="width:100%;height:100%">
  <path d="M30 32 Q30 8 50 8 Q70 8 70 32 L72 46 L28 46 Z" fill="#d6d9db" />
  <circle cx="50" cy="30" r="17" fill="#f1c9a5" /><circle cx="43" cy="30" r="5" fill="none" stroke="#353a3d" stroke-width="2" /><circle cx="57" cy="30" r="5" fill="none" stroke="#353a3d" stroke-width="2" />
  <path d="M20 98 Q20 54 50 52 Q80 54 80 98 Z" fill="#9b59b6" />
  <path d="M84 60 L84 98 M84 60 Q84 52 76 54" fill="none" stroke="#8a5a2b" stroke-width="4" stroke-linecap="round" /></svg>"""

TACHO = f"""<svg viewBox="0 0 400 230" style="width:100%;height:100%">
  <path d="M30 210 A170 170 0 0 1 370 210" fill="none" stroke="#eee" stroke-width="40" stroke-linecap="round" />
  <path id="ta-b" d="M30 210 A170 170 0 0 1 370 210" fill="none" stroke="{OR}" stroke-width="40" stroke-linecap="round" pathLength="100" stroke-dasharray="48 100" />
</svg>"""


def luecke(uid, gefuellt=False):
    """Gehalt (grün) vs. Rente (grau) mit roter Lücke; optional grüner ETF-Block in der Lücke."""
    fill = (f'<rect id="{uid}-etf" x="560" y="90" width="200" height="270" rx="10" fill="{GRUEN}" />'
            f'<text id="{uid}-etft" x="660" y="240" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="#fff">ETF</text>') if gefuellt else ""
    return f"""<svg viewBox="0 0 900 620" style="width:100%;height:100%">
  <line x1="40" y1="600" x2="860" y2="600" stroke="#111" stroke-width="6" />
  <rect id="{uid}-g" x="140" y="90" width="200" height="510" rx="10" fill="{GRUEN}" />
  <text x="240" y="70" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="{GRUEN}">2.500 €</text>
  <rect id="{uid}-r" x="560" y="360" width="200" height="240" rx="10" fill="{GRAU}" />
  <text id="{uid}-rt" x="660" y="430" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="#fff">1.400 €</text>
  {"" if gefuellt else f'''<g id="{uid}-l"><rect x="560" y="90" width="200" height="270" rx="10" fill="none" stroke="{ROT}" stroke-width="8" stroke-dasharray="18 12" />
  <text x="660" y="240" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="{ROT}">−1.100 €</text></g>'''}
  {fill}
  <text x="240" y="560" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">heute</text>
  <text x="660" y="560" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">Rente</text>
</svg>"""


KURVE = f"""<svg viewBox="0 0 900 460" style="width:100%;height:100%">
  <path d="M20 20 L20 440 L880 440" fill="none" stroke="#111" stroke-width="6" />
  <path id="ku-l" d="M30 432 C300 420 560 360 870 40" fill="none" stroke="{GRUEN}" stroke-width="12" stroke-linecap="round" />
  <text x="40" y="420" font-family="Montserrat" font-weight="800" font-size="34" fill="#555c60">30</text>
  <text x="870" y="420" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="34" fill="#555c60">67</text>
</svg>"""


def chip(id_, txt, col, x, y):
    return f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:16px 34px;border-radius:24px;background:{col};color:#fff;font-family:Montserrat;font-weight:800;font-size:50px">{txt}</div>'


SCENES = [
    ("hook", "s1", "s2",
     title("hk-t", 'Wie viel Rente<br />bekommst <span style="color:#DB8622">du</span>?', 290, 104) +
     box("hk-p", 330, 560, 420, 420, RENTNERIN) +
     sub("hk-s", "viel weniger, als du denkst!", 1050, 64, ROT),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-p", t0) + f'\n      pop("#hk-s", {c("s2", 1)});'),

    ("niveau", "s3", "s3",
     box("ni-ta", 190, 380, 700, 403, TACHO) +
     big("ni-z", "48 %", 640, 150, OR) +
     sub("ni-s", "des Durchschnittslohns", 860, 60) +
     sub("ni-v", "– und zwar vor Steuern!", 950, 56, ROT),
     lambda t0, d: f"""
      pop("#ni-ta", {t0});
      tl.fromTo("#ta-b", {{ strokeDasharray: "0 100" }}, {{ strokeDasharray: "48 100", duration: 1.2, ease: "power2.out" }}, {c('s3', 1)});
      pop("#ni-z", {c('s3', 1)});
      pop("#ni-s", {c('s3', 2)});
      pop("#ni-v", {c('s3', 3)});"""),

    ("lena", "s4", "s4",
     box("le-p", 340, 330, 400, 520, person(OR, "#8a5a2b")) +
     chip("le-n", "Lena", OR, 445, 880) +
     chip("le-g", "2.500 € netto", GRUEN, 330, 1010),
     lambda t0, d: f"""
      pop("#le-p", {t0});
      pop("#le-n", {t0} + 0.3);
      pop("#le-g", {c('s4', 1)});"""),

    ("luecke", "s5", "s7",
     box("lu-c", 90, 330, 900, 620, luecke("lu")) +
     big("lu-t", "Rentenlücke", 1010, 110, ROT),
     lambda t0, d: f"""
      pop("#lu-c", {t0});
      tl.fromTo("#lu-r", {{ attr: {{ y: 600, height: 0 }} }}, {{ attr: {{ y: 360, height: 240 }}, duration: 0.8, ease: "power2.out" }}, {c('s5', 2)});
      pop("#lu-rt", {c('s5', 2)} + 0.6);
      tl.fromTo("#lu-l", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {S['s6']['start']});
      tl.fromTo("#lu-l", {{ x: 0 }}, {{ x: 8, duration: 0.08, yoyo: true, repeat: 5 }}, {c('s6', 1)});
      pop("#lu-t", {S['s7']['start']});"""),

    ("gute", "s8", "s8",
     sub("gu-t", "Die gute Nachricht:", 330, 70, GRUEN) +
     box("gu-u", 390, 470, 300, 300, UHR) +
     big("gu-z", "Zeit schließt<br />die Lücke", 840, 110),
     lambda t0, d: f"""
      pop("#gu-t", {t0});
      pop("#gu-u", {t0} + 0.2);
      tl.fromTo("#gu-u", {{ rotation: 0 }}, {{ rotation: 180, duration: 0.6, ease: "power2.inOut" }}, {t0} + 0.8);
      pop("#gu-z", {c('s8', 1)});"""),

    ("etf", "s9", "s9",
     chip("et-a", "ab 30", OR, 90, 330) + chip("et-b", "200 € / Monat", GRUEN, 330, 330) + chip("et-c", "6 %", "#3d7be0", 820, 330) +
     box("et-k", 90, 470, 900, 460, KURVE) +
     big("et-n", "0 €", 990, 150, GRUEN),
     lambda t0, d: f"""
      pop("#et-a", {c('s9', 0)});
      pop("#et-b", {c('s9', 1)});
      pop("#et-c", {c('s9', 3)});
      pop("#et-k", {c('s9', 0)} + 0.2);
      draw("#ku-l", {c('s9', 1)}, {round(c('s9', 4) - c('s9', 1), 2)});
      pop("#et-n", {c('s9', 3)});
      zaehl("#et-n", 0, 320000, {c('s9', 3)}, {round(c('s9', 4) - c('s9', 3) + 0.8, 2)}, " €");"""),

    ("gefuellt", "s10", "s10",
     box("gf-c", 90, 330, 900, 620, luecke("gf", True)) +
     big("gf-t", "Lücke geschlossen!", 1010, 96, GRUEN),
     lambda t0, d: f"""
      pop("#gf-c", {t0});
      tl.fromTo("#gf-etf", {{ attr: {{ y: 360, height: 0 }} }}, {{ attr: {{ y: 90, height: 270 }}, duration: 0.9, ease: "power2.out" }}, {t0} + 0.3);
      pop("#gf-etft", {t0} + 1.0);
      pop("#gf-t", {c('s10', 1)});"""),

    ("frage", "s11", "s11",
     box("fr-b", 290, 360, 500, 433, BLASE) +
     big("fr-t", "Wie viel Rente<br />bekommst du?", 860, 92, OR),
     lambda t0, d: f"""
      pop("#fr-b", {t0});
      tl.fromTo("#fr-b", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#fr-t", {t0} + 0.2);"""),

    ("outro", "s12", "s12", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
