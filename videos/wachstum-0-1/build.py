#!/usr/bin/env python3
"""HundeFinanzTv (~36 s, Stimme Dan, Tempo 1.12) – Deutschland wächst nur 0,1 % (TEST-KURZVIDEO 35–40 s, Nutzer 25.11.; für 26.11.). NEUES FORMAT.
Destatis Q3 2026: +0,1 % (erst +0,2 %), Verbraucher sparen bei Essen/Sprit, Exporte −1 %, Ausrüstungsinvestitionen −3,5 % zum Vorquartal,
Wachstum v. a. vom Staat (Commerzbank-Analyst Solveen). Quelle: dpa-AFX/ARIVA, finanzen.ch 25.11.2026. Hook-Stil B, CTA Satz 2, Hinweis letzter Satz."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

_t = json.loads((HERE / "timings.json").read_text())
T0 = ls.einfuegen(HERE, next(s["end"] for s in _t["saetze"] if s["id"] == "s4") - 0.01)  # Logo-Intro nach s4

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 9, [])
cap, st = K.cap, K.st
S = K.szene
SFX_CTA = []


def titel(id_, text, y=340, farbe=D, gr=64):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=50):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.05">{text}</div>'


def beagle(id_, y=330):
    return (f'<div id="{id_}" style="position:absolute;left:340px;top:{y}px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>')


# s1: HOOK – stärkste Aussage SOFORT im ersten Bild (Test-Regel: kein Titel-Vorlauf)
S("s1", None, nl.CSS + gross("n1", "+0,1 %", 360, R, 250) + pille("p1", "Wirtschaftswachstum", 700, D, "#fff", 54)
  + nl.karte("k1", "Wir sparen beim", f'<div style="font-weight:900;font-size:110px;color:{O};text-align:center;line-height:1.1">Essen ▼</div>', y=860),
  lambda a, d: KIT_JS + f' tl.set("#n1", {{ opacity: 1 }}, 0); pop("#n1", {a}); pop("#p1", {a} + 0.15); pop("#k1", {cap("s1", 1)});')

# s2: CTA Teilen + Folgen
S("s2", None, beagle("fl2", 340) + f'<div id="n2" class="nk-gross" style="top:770px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + pille("c2", "+ Folgen", 890, O, "#fff", 58) + pille("t2", "Video teilen ↗", 1040, D, "#fff", 52),
  lambda a, d: f'pop("#fl2", {a}); pop("#n2", {a} + 0.2); pop("#c2", {cap("s2", 1)}); pop("#t2", {cap("s2", 0)} + 0.4);')

# s3–s4: Q3 + Kommentar-Overlay (stumm)
TXT = "Sparst du auch beim Essen?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.2)
S("s3", None, titel("t3", "3. Quartal 2026", 380, D, 66) + gross("n3", "+0,1 %", 500, R, 210) + titel("t3b", "Deutschland", 760, O, 60) + CTA,
  lambda a, d: f'pop("#t3", {a}); pop("#n3", {a} + 0.15); pop("#t3b", {cap("s3", 1)});' + cta_js, SFX_CTA, bis="s5")
S("s5", None, titel("t5", "Schauen wir genau hin", 640, D, 78) + pille("p5", "Konjunktur · Konsum · Export", 900, O, "#fff", 46),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {a} + 0.3);') if False else None
S("s5", None, nl.karte("k5", "Verbraucher sparen bei", nl.zeile("r5a", "Essen", "▼", R) + nl.zeile("r5b", "Sprit", "▼", R), y=420)
  + pille("p5", "kaum mehr Konsum", 800, O, "#fff", 52),
  lambda a, d: f'pop("#k5", {a}); pop("#r5a", {cap("s5", 1)} - 0.2); pop("#r5b", {cap("s5", 1)} + 0.3); pop("#p5", {cap("s5", 1)} + 0.6);')

# s6: Exporte / Investitionen
S("s6", None, titel("t6", "Warum so schwach?", 340, D, 64)
  + nl.karte("k6", "Gegenüber dem Vorquartal", nl.zeile("r6a", "Exporte", "−1 %", R, "▼") + nl.zeile("r6b", "Investitionen in Maschinen", "−3,5 %", R, "▼"), y=500),
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {a} + 0.1); pop("#r6a", {cap("s6", 0)} + 0.4); pop("#r6b", {cap("s6", 2)});')

# s7: Staat
S("s7", None, titel("t7", "Wer trägt das Wachstum?", 340, D, 60) + gross("n7", "Der Staat", 480, O, 180) + pille("p7", "höhere Staatsausgaben", 800, O, "#fff", 52),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {a} + 0.15); pop("#p7", {cap("s7", 1)});')


def merk(sid, statisch=False):
    html = (titel(f"t{sid}", "Merk dir", 340, O, 70)
            + nl.karte(f"k{sid}", "Wenn alle sparen", f'<div style="font-weight:900;font-size:68px;color:{R};text-align:center;padding:14px 0;line-height:1.15">wächst die Wirtschaft kaum ▼</div>', y=500))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.15);'


h8, j8 = merk("s8")
S("s8", None, h8, j8)
h9, j9 = merk("s9", True)
S("s9", None, h9, j9)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "klick"), (cap("s5", 1), "kurve-runter"), (cap("s6", 2), "falsch"), (cap("s8", 1), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "26.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
