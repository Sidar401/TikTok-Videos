#!/usr/bin/env python3
"""HundeFinanzTV: Der Aufrunden-Trick (Teilen-CTA). Leitmotiv: Bon wird aufgerundet, Münze fliegt ins Sparschwein."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import SPARSCHWEIN, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402
from icons import TEILEN  # noqa: E402
from kurz_szenen import GRUEN, OR, ROT, big, chip, sub  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


APP = f"""<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" /><rect x="22" y="40" width="256" height="480" rx="20" fill="#fff" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" />
  <text x="150" y="110" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#111">Banking-App</text>
  <rect x="45" y="170" width="210" height="70" rx="16" fill="#faf5ef" />
  <text x="62" y="215" font-family="Montserrat" font-weight="800" font-size="24" fill="#111">Aufrunden</text>
  <rect x="190" y="188" width="56" height="34" rx="17" fill="{GRUEN}" /><circle id="ap-k" cx="229" cy="205" r="13" fill="#fff" />
  <rect x="45" y="270" width="210" height="14" rx="7" fill="#eee" /><rect x="45" y="305" width="160" height="14" rx="7" fill="#eee" /></svg>"""

MUENZE = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><circle cx="50" cy="50" r="46" fill="#f2c418" stroke="#c99a06" stroke-width="6" /><text x="50" y="62" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="30" fill="#8a5a00">0,70</text></svg>'

SCENES = [
    ("hook", "s1", "s1",
     title("hk-t", 'Sparen, ohne es<br /><span style="color:#DB8622">zu merken?</span>', 300, 100) +
     box("hk-s", 290, 620, 500, 433, SPARSCHWEIN),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-s", t0) +
     f'\n      tl.fromTo("#hk-s", {{ rotation: -4 }}, {{ rotation: 4, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {c("s1", 2)});'),

    ("app", "s2", "s2",
     box("ap-h", 390, 330, 300, 560, APP) +
     big("ap-t", "Aufrunden: AN", 960, 100, GRUEN),
     lambda t0, d: f"""
      pop("#ap-h", {t0});
      pop("#ap-t", {c('s2', 2)});"""),

    ("bon", "s3", "s4",
     '<div id="bo-b" style="position:absolute;left:150px;top:340px;width:460px;padding:36px 40px;background:#fff;border:6px solid #353a3d;border-radius:16px;'
     'font-family:Montserrat;font-weight:800;color:#111">'
     '<div style="font-size:40px;color:#888">Einkauf</div>'
     '<div id="bo-a" style="font-size:96px">12,30 €</div>'
     '<div id="bo-n" style="font-size:96px;color:#DB8622">13,00 €</div></div>' +
     box("bo-s", 640, 560, 380, 329, SPARSCHWEIN) +
     box("bo-m", 760, 360, 130, 130, MUENZE) +
     sub("bo-t", "+0,70 € aufs Sparkonto", 1010, 66, GRUEN),
     lambda t0, d: f"""
      pop("#bo-b", {t0});
      tl.fromTo("#bo-n", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {c('s3', 1)});
      pop("#bo-s", {S['s4']['start']});
      tl.fromTo("#bo-m", {{ x: 0, y: 0, opacity: 1, scale: 1 }}, {{ x: 0, y: 240, scale: 0.6, duration: 0.9, ease: "power2.in" }}, {S['s4']['start']} + 0.2);
      tl.to("#bo-m", {{ opacity: 0, duration: 0.15 }}, {S['s4']['start']} + 1.1);
      pop("#bo-t", {c('s4', 1)});"""),

    ("jahr", "s5", "s5",
     sub("ja-a", "1 Kartenkauf pro Tag", 400, 70, "#555c60") +
     big("ja-z", "0 €", 560, 200, GRUEN) +
     sub("ja-s", "pro Jahr – nebenbei", 840, 70),
     lambda t0, d: f"""
      pop("#ja-a", {t0});
      pop("#ja-z", {c('s5', 1)});
      zaehl("#ja-z", 0, 180, {c('s5', 1)}, {round(c('s5', 2) - c('s5', 1) + 0.8, 2)}, " €");
      pop("#ja-s", {c('s5', 2)});"""),

    ("stufen", "s6", "s6",
     big("st-t", "Noch mehr?", 330, 120, OR) +
     chip("st-a", "auf 1 €", GRUEN, 0, 600, 70, center=True) +
     chip("st-b", "auf 5 €", GRUEN, 0, 760, 80, center=True) +
     chip("st-c", "auf 10 €", GRUEN, 0, 940, 90, center=True),
     lambda t0, d: f"""
      pop("#st-t", {t0});
      pop("#st-a", {t0} + 0.4);
      pop("#st-b", {c('s6', 1)});
      pop("#st-c", {c('s6', 1)} + 0.5);"""),

    ("check", "s7", "s7",
     box("ch-h", 390, 330, 300, 560, APP) +
     big("ch-t", "Check deine App!", 960, 100, OR),
     lambda t0, d: f"""
      pop("#ch-h", {t0});
      tl.fromTo("#ch-h", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3 }}, {t0} + 0.4);
      pop("#ch-t", {c('s7', 1)});"""),

    ("teilen", "s8", "s8",
     box("te-i", 340, 380, 400, 400, TEILEN) +
     big("te-t", "Schick's deinem<br />Spar-Muffel!", 880, 90, OR),
     lambda t0, d: f"""
      pop("#te-i", {t0});
      tl.fromTo("#te-i", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#te-t", {c('s8', 3)});"""),

    ("outro", "s9", "s9", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
