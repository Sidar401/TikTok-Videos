#!/usr/bin/env python3
"""HundeFinanzTV: Karte oder Bargeld? (Kommentar-CTA). Leitmotiv: Karte vs. Geldscheine im Duell, Bargeld-Umschlag."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import T, box, build, cap, outro, outro_js, snap_in  # noqa: E402
from icons import BLASE  # noqa: E402
from kurz_szenen import GRUEN, OR, ROT, big, chip, sub  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


KARTE = f"""<svg viewBox="0 0 400 250" style="width:100%;height:100%">
  <rect x="5" y="5" width="390" height="240" rx="26" fill="#3d7be0" /><rect x="40" y="60" width="70" height="52" rx="10" fill="#f2c418" />
  <rect x="40" y="170" width="200" height="16" rx="8" fill="#ffffff88" /></svg>"""


def scheine(uid, n=5):
    s = "".join(f'<g class="{uid}-s" transform="translate({i * 6} {80 - i * 16})"><rect x="10" y="40" width="300" height="150" rx="14" fill="#7fbf74" stroke="#4d7d43" stroke-width="5" />'
                f'<circle cx="160" cy="115" r="38" fill="#a8d69c" />{"" if i < n - 1 else '<text x="160" y="130" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#2f5a28">50</text>'}</g>'
                for i in range(n))
    return f'<svg viewBox="0 0 340 290" style="width:100%;height:100%">{s}</svg>'


UMSCHLAG = f"""<svg viewBox="0 0 400 300" style="width:100%;height:100%">
  <rect x="10" y="40" width="380" height="250" rx="20" fill="#f6efe1" stroke="#c99a06" stroke-width="8" />
  <path d="M10 60 L200 180 L390 60" fill="none" stroke="#c99a06" stroke-width="8" />
  <text x="200" y="265" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="{OR}">Freizeit &amp; Shopping</text></svg>"""

STOPP = f"""<svg viewBox="0 0 300 300" style="width:100%;height:100%">
  <path d="M90 10 L210 10 L290 90 L290 210 L210 290 L90 290 L10 210 L10 90 Z" fill="{ROT}" />
  <text x="150" y="175" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="80" fill="#fff">STOPP</text></svg>"""

SCENES = [
    ("hook", "s1", "s2",
     '<div id="hk-t" style="position:absolute;left:0;top:290px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:104px;line-height:1.05;color:#111">'
     'Karte <span style="color:#DB8622">oder</span><br />Bargeld?</div>' +
     box("hk-k", 70, 640, 420, 263, KARTE) + box("hk-s", 590, 600, 420, 358, scheine("hk")) +
     sub("hk-u", "Der Unterschied ist größer, als du denkst", 1040, 54, ROT),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-k", t0) + snap_in("#hk-s", t0) + f'\n      pop("#hk-u", {S["s2"]["start"]} + 0.3);'),

    ("studie", "s3", "s3",
     sub("su-t", "Studien zeigen:", 330, 70, OR) +
     f'<div style="position:absolute;left:190px;top:520px;width:700px;height:520px;display:flex;align-items:flex-end;justify-content:space-around;border-bottom:8px solid #111">'
     f'<div id="su-b1" style="width:220px;height:300px;border-radius:20px 20px 0 0;background:{GRUEN};transform-origin:50% 100%"></div>'
     f'<div id="su-b2" style="width:220px;height:500px;border-radius:20px 20px 0 0;background:{ROT};transform-origin:50% 100%"></div></div>'
     '<div style="position:absolute;left:190px;top:1060px;width:700px;display:flex;justify-content:space-around;font-family:Montserrat;font-weight:800;font-size:52px">'
     f'<span style="color:{GRUEN}">Bargeld</span><span style="color:{ROT}">Karte</span></div>',
     lambda t0, d: f"""
      pop("#su-t", {t0});
      tl.fromTo("#su-b1", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power2.out" }}, {c('s3', 1)});
      tl.fromTo("#su-b2", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.7, ease: "power2.out" }}, {c('s3', 2)});"""),

    ("weh", "s4", "s4",
     box("we-s", 270, 360, 540, 461, scheine("we")) +
     big("we-t", "Bargeld tut weh", 900, 110, ROT),
     lambda t0, d: f"""
      pop("#we-s", {t0});
      pop("#we-t", {t0} + 0.3);
      tl.to(".we-s", {{ opacity: 0, y: -60, duration: 0.3, stagger: -0.3 }}, {c('s4', 2)});"""),

    ("piep", "s5", "s5",
     box("pi-k", 240, 420, 600, 375, KARTE) +
     chip("pi-p", "PIEP ✓", GRUEN, 600, 330, 70) +
     big("pi-t", "… und du spürst nichts", 900, 92),
     lambda t0, d: f"""
      pop("#pi-k", {t0});
      pop("#pi-p", {c('s5', 2)});
      tl.fromTo("#pi-p", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }}, {c('s5', 2)} + 0.35);
      pop("#pi-t", {c('s5', 1)});"""),

    ("monat", "s6", "s8",
     big("mo-t", "Bargeld-Monat", 300, 120, OR) +
     box("mo-u", 240, 500, 600, 450, UMSCHLAG) +
     chip("mo-b", "fester Betrag", GRUEN, 0, 1010, 60, center=True) +
     box("mo-x", 760, 640, 230, 230, STOPP),
     lambda t0, d: f"""
      pop("#mo-t", {t0});
      pop("#mo-u", {c('s6', 1)});
      pop("#mo-b", {S['s7']['start']} + 0.4);
      pop("#mo-x", {S['s8']['start']});
      tl.fromTo("#mo-x", {{ rotation: -10 }}, {{ rotation: 0, duration: 0.3, ease: "back.out(3)" }}, {S['s8']['start']});"""),

    ("wohin", "s9", "s9",
     big("wo-t", "Wohin fließt<br />dein Geld?", 360, 120) +
     chip("wo-a", "Essen", OR, 120, 760, 60) + chip("wo-b", "Freizeit", "#3d7be0", 440, 760, 60) + chip("wo-c", "Shopping", ROT, 300, 900, 60),
     lambda t0, d: f"""
      pop("#wo-t", {t0});
      pop("#wo-a", {c('s9', 1)}); pop("#wo-b", {c('s9', 1)} + 0.3); pop("#wo-c", {c('s9', 2)});"""),

    ("frage", "s10", "s10",
     box("fr-b", 290, 360, 500, 433, BLASE) +
     big("fr-t", "Karte oder Bargeld?", 860, 96, OR),
     lambda t0, d: f"""
      pop("#fr-b", {t0});
      tl.fromTo("#fr-b", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#fr-t", {t0} + 0.2);"""),

    ("outro", "s11", "s11", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
