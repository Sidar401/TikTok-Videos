#!/usr/bin/env python3
"""HundeFinanzTV: Kfz-Versicherung bis 30. November wechseln (Kommentar-CTA). Leitmotiv: Kalenderblatt 30. NOV + Preisschilder."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402
from icons import AUTO, BLASE, SCHILD, UHR, person  # noqa: E402
from kurz_szenen import GRUEN, OR, ROT, big, chip, kalender, liste, sub  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


def preis(id_, txt, col, x, y, strich=False):
    st = f'<div id="{id_}-x" style="position:absolute;left:-4%;right:-4%;top:46%;height:14px;border-radius:7px;background:{ROT}"></div>' if strich else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:18px 40px 18px 70px;background:{col};color:#fff;font-family:Montserrat;'
            f'font-weight:800;font-size:76px;clip-path:polygon(40px 0,100% 0,100% 100%,40px 100%,0 50%)"><span style="position:relative">{txt}{st}</span></div>')


SCENES = [
    ("hook", "s1", "s1",
     title("hk-t", 'Autoversicherung<br /><span style="color:#DB8622">schon verglichen?</span>', 290, 92) +
     box("hk-a", 240, 560, 600, 600, AUTO),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-a", t0) +
     f'\n      tl.fromTo("#hk-a", {{ x: -12 }}, {{ x: 12, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.8);'),

    ("stichtag", "s2", "s3",
     box("st-k", 290, 330, 500, 500, kalender("NOV", "30")) +
     chip("st-c", "Stichtag zum Kündigen", ROT, 0, 920, 58, center=True),
     lambda t0, d: f"""
      pop("#st-k", {c('s2', 1)} - 0.2);
      tl.fromTo("#st-k", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.18, yoyo: true, repeat: 3 }}, {c('s2', 2)});
      pop("#st-c", {S['s3']['start']} + 0.4);"""),

    ("wechsel", "s4", "s5",
     box("we-a", 80, 380, 380, 380, kalender("NOV", "30")) +
     '<svg id="we-p" viewBox="0 0 200 100" style="position:absolute;left:440px;top:500px;width:200px;height:100px"><path d="M10 50 L170 50 M130 15 L175 50 L130 85" fill="none" stroke="#DB8622" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" /></svg>' +
     box("we-b", 620, 380, 380, 380, kalender("JAN", "1", GRUEN)) +
     sub("we-t1", "kündigen", 800, 54, ROT).replace("left:60px;", "left:80px;").replace("width:960px", "width:380px") +
     sub("we-t2", "neuer Tarif", 800, 54, GRUEN).replace("left:60px;", "left:620px;").replace("width:960px", "width:380px") +
     big("we-l", "lohnt sich!", 960, 120, GRUEN),
     lambda t0, d: f"""
      pop("#we-a", {t0});
      pop("#we-t1", {t0} + 0.3);
      pop("#we-p", {c('s4', 1)});
      pop("#we-b", {c('s4', 1)} + 0.2);
      pop("#we-t2", {c('s4', 2)});
      pop("#we-l", {S['s5']['start']});"""),

    ("tom", "s6", "s8",
     box("to-p", 60, 380, 300, 400, person(OR, "#353a3d")) +
     chip("to-n", "Tom", OR, 140, 800) +
     preis("to-a", "780 €", ROT, 430, 420, strich=True) +
     preis("to-b", "520 €", GRUEN, 430, 620) +
     big("to-g", "+260 €", 920, 170, GRUEN) +
     f'<div id="to-u" style="position:absolute;left:0;top:1120px;width:1080px;display:flex;justify-content:center;align-items:center;gap:20px">'
     f'<div style="width:110px;height:110px">{UHR}</div><span style="font-family:Montserrat;font-weight:800;font-size:56px;color:#111">½ Stunde Arbeit</span></div>',
     lambda t0, d: f"""
      pop("#to-p", {t0});
      pop("#to-n", {t0} + 0.3);
      pop("#to-a", {c('s6', 2)});
      tl.fromTo("#to-a-x", {{ scaleX: 0, rotation: -10 }}, {{ scaleX: 1, rotation: -10, duration: 0.35, ease: "power2.out" }}, {c('s7', 1)});
      pop("#to-b", {c('s7', 1)});
      pop("#to-g", {S['s8']['start']});
      zaehl("#to-g", 0, 260, {S['s8']['start']}, 1.0, " €");
      pop("#to-u", {c('s8', 1)});"""),

    ("sf", "s9", "s9",
     box("sf-s", 340, 340, 400, 400, SCHILD) +
     big("sf-t", "Schadenfreiheits-<br />rabatt", 800, 96) +
     sub("sf-u", "nimmst du einfach mit ✓", 1030, 62, GRUEN),
     lambda t0, d: f"""
      pop("#sf-s", {t0});
      pop("#sf-t", {c('s9', 1)});
      pop("#sf-u", {c('s9', 2)});"""),

    ("check", "s10", "s10",
     big("ck-t", "Beim Vergleich:", 330, 100, OR) +
     liste("ck-l", ["gleiche Leistung", "Kilometer ehrlich angeben"], 560),
     lambda t0, d: f"""
      pop("#ck-t", {t0});
      pop("#ck-l-0", {c('s10', 1)});
      pop("#ck-l-1", {c('s10', 2)});"""),

    ("frage", "s12", "s12",
     box("fr-b", 290, 360, 500, 433, BLASE) +
     big("fr-t", "Wie viel zahlst du<br />für dein Auto?", 860, 92, OR),
     lambda t0, d: f"""
      pop("#fr-b", {t0});
      tl.fromTo("#fr-b", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#fr-t", {t0} + 0.2);"""),

    ("outro", "sF", "sF", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
