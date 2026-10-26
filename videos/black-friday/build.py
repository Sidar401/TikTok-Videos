#!/usr/bin/env python3
"""HundeFinanzTV: Black Friday – 3 Tricks der Händler (Teilen-CTA als Text, da nicht eingesprochen). Leitmotiv: Preisschild mit Fake-Rabatt."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import T, box, build, cap, snap_in  # noqa: E402
from icons import SCHILD, TASCHE  # noqa: E402
from kurz_szenen import GRUEN, OR, ROT, big, chip, liste, outro_cta, outro_cta_js, sub  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


def nr(id_, n, x, y, col=OR):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:220px;height:220px;border-radius:50%;background:{col};color:#fff;'
            f'font-family:\'Abril Fatface\',serif;font-size:140px;display:flex;align-items:center;justify-content:center">{n}</div>')


def trick(id_, n):
    return f'<div id="{id_}" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:64px;color:{OR}">Trick {n}</div>'


KURVE = f"""<svg viewBox="0 0 900 420" style="width:100%;height:100%">
  <path d="M20 20 L20 400 L880 400" fill="none" stroke="#111" stroke-width="6" />
  <path id="ku-l" d="M30 300 L300 300 L360 120 L600 120 L640 260 L870 260" fill="none" stroke="{ROT}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" />
  <text x="160" y="280" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#555c60">79 €</text>
  <text x="480" y="100" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="{ROT}">99 €</text>
  <text x="755" y="235" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="36" fill="{GRUEN}">−20 % = 79 €</text>
</svg>"""


def schild(id_, alt, neu, x, y):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:640px;padding:40px 60px;border-radius:36px;background:#faf5ef;border:8px solid #111;'
            f'font-family:Montserrat;font-weight:800">'
            f'<div style="position:relative;display:inline-block;font-size:56px;color:#9aa3a8">UVP {alt}<div id="{id_}-x" style="position:absolute;left:-4%;right:-4%;top:45%;height:10px;background:{ROT}"></div></div>'
            f'<div style="font-size:110px;color:#111">{neu}</div></div>')


SCENES = [
    ("hook", "s1", "s1",
     '<div id="hk-t" style="position:absolute;left:0;top:300px;width:1080px;display:flex;justify-content:center"><span style="padding:20px 50px;border-radius:24px;'
     'background:#111;color:#fff;font-family:Montserrat;font-weight:800;font-size:104px;white-space:nowrap">BLACK FRIDAY</span></div>' +
     box("hk-b", 365, 560, 350, 350, TASCHE) +
     sub("hk-s", "… aber nicht für dich?", 1030, 66, ROT),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-b", t0) + f'\n      pop("#hk-s", {c("s1", 3)});'),

    ("drei", "s2", "s2",
     big("dr-t", "3 Tricks", 320, 150) +
     nr("dr-1", 1, 90, 620) + nr("dr-2", 2, 430, 620) + nr("dr-3", 3, 770, 620) +
     sub("dr-s", "nicht reinfallen!", 920, 66, ROT),
     lambda t0, d: f"""
      pop("#dr-t", {t0});
      pop("#dr-1", {t0} + 0.4); pop("#dr-2", {t0} + 0.6); pop("#dr-3", {t0} + 0.8);
      pop("#dr-s", {c('s2', 1)});"""),

    ("trick1", "s3", "s3",
     trick("t1-n", 1) + big("t1-t", "Preis vorher<br />erhöht", 400, 100) +
     box("t1-k", 90, 680, 900, 420, KURVE),
     lambda t0, d: f"""
      pop("#t1-n", {t0}); pop("#t1-t", {t0} + 0.2);
      pop("#t1-k", {c('s3', 1)} - 0.3);
      draw("#ku-l", {c('s3', 1)}, {round(c('s3', 3) - c('s3', 1) + 0.3, 2)});"""),

    ("trick2", "s4", "s5",
     trick("t2-n", 2) + big("t2-t", "Fake-Streichpreis", 400, 96) +
     schild("t2-s", "199 €", "99 €", 220, 600) +
     chip("t2-a", "−50 %", ROT, 700, 540, 70) +
     sub("t2-r", "Marktpreis: 110 € → nur −10 %", 1060, 56, GRUEN),
     lambda t0, d: f"""
      pop("#t2-n", {t0}); pop("#t2-t", {t0} + 0.2);
      pop("#t2-s", {c('s4', 1)});
      tl.fromTo("#t2-s-x", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.35 }}, {c('s4', 2)});
      pop("#t2-a", {c('s4', 2)} + 0.3);
      pop("#t2-r", {S['s5']['start']} + 0.6);
      tl.to("#t2-a", {{ opacity: 0.3, duration: 0.3 }}, {c('s5', 1)});"""),

    ("trick3", "s6", "s7",
     trick("t3-n", 3) + big("t3-t", "Fake-Druck", 400, 110) +
     '<div id="t3-c" style="position:absolute;left:190px;top:600px;width:700px;padding:24px 0;border-radius:30px;background:#111;text-align:center;'
     'font-family:Montserrat;font-weight:800;font-size:120px;color:#e24b4b">00:09:<span id="t3-s">59</span></div>' +
     chip("t3-l", "Nur noch 2 auf Lager!", ROT, 0, 820, 60, center=True) +
     big("t3-k", "Kaufen ohne Nachdenken", 1000, 76, ROT),
     lambda t0, d: f"""
      pop("#t3-n", {t0}); pop("#t3-t", {t0} + 0.2);
      pop("#t3-c", {c('s6', 0)} + 0.6);
      zaehl("#t3-s", 59, 52, {c('s6', 0)} + 0.6, 7, "");
      pop("#t3-l", {c('s6', 2)});
      tl.fromTo("#t3-l", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.2, yoyo: true, repeat: 5 }}, {c('s6', 2)} + 0.4);
      pop("#t3-k", {S['s7']['start']});"""),

    ("schutz", "s8", "s9",
     box("sc-s", 390, 300, 300, 300, SCHILD) +
     big("sc-t", "So schützt du dich", 640, 90, GRUEN) +
     liste("sc-l", ["Wunschliste schreiben", "Preisverlauf prüfen"], 830),
     lambda t0, d: f"""
      pop("#sc-s", {t0});
      pop("#sc-t", {t0} + 0.2);
      pop("#sc-l-0", {S['s9']['start']});
      pop("#sc-l-1", {c('s9', 2)} + 0.5);"""),

    ("outro", "sF", "sF", outro_cta("Schick's deinen Shopping-Freunden!"), outro_cta_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
