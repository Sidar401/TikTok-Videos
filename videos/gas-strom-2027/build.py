#!/usr/bin/env python3
"""HundeFinanzTv (~64 s, Stimme Dan, Tempo 1.12) – Gas/Strom ab 1.1.2027 teurer, Sonderkündigungsrecht (für 25.11.2026). NEUES FORMAT.
Hook-Stil B (Kurzsatz, keine Effekte). Folgen-/Teilen-CTA als Satz 2 (Nutzer 25.11.), Hinweis letzter Satz.
58 Stromversorger Ø +8 %, 82 Gasversorger Ø +14 % (Grundversorger, Nov. 2026), Verivox Gas +10…20 %, Beispiel 14 % × 2.000 € = 280 € (eigene Rechnung),
Sonderkündigungsrecht in der Regel, N-ERGIE: Kündigung bis 31.12.2026 (Beispiel). Gegenstimme: Preise können auch sinken."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

_t = json.loads((HERE / "timings.json").read_text())
T0 = ls.einfuegen(HERE, next(s["end"] for s in _t["saetze"] if s["id"] == "s5") - 0.01)  # Logo-Intro nach s5

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 15, [])
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


def kk(id_, kopf, text, y):
    return nl.karte(id_, kopf, f'<div style="font-weight:800;font-size:52px;color:{D};text-align:center;padding:14px 0;line-height:1.25">{text}</div>', y=y)


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


def beagle(id_, y=330):
    return (f'<div id="{id_}" style="position:absolute;left:340px;top:{y}px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>')


# s1 Hook B
S("s1", None, nl.CSS + gross("f1", "🔥", 330, D, 200) + nl.karte("k1a", "Dein Gas", f'<div style="font-weight:900;font-size:110px;color:{R};text-align:center;line-height:1.1">bis +14 % ▲</div>', y=620)
  + nl.karte("k1b", "Aber", f'<div style="font-weight:900;font-size:96px;color:{G};text-align:center;line-height:1.1">Kündigen ✓</div>', y=960),
  lambda a, d: KIT_JS + f' pop("#f1", {a}); pop("#k1a", {a} + 0.1); pop("#k1b", {cap("s1", 3)});')

# s2 Teilen + Folgen (CTA)
S("s2", None, beagle("fl2", 340) + f'<div id="n2" class="nk-gross" style="top:770px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>'
  + pille("c2", "+ Folgen", 890, O, "#fff", 58) + pille("t2", "Video teilen ↗", 1040, D, "#fff", 52),
  lambda a, d: f'pop("#fl2", {a}); pop("#n2", {a} + 0.2); pop("#c2", {cap("s2", 1)}); pop("#t2", {cap("s2", 0)} + 0.4);')

# s3–s4 Januar + Kommentar-Overlay (stumm)
TXT = "Wie viel zahlst du für Gas?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.4)
S("s3", None, titel("t3", "Ab 1. Januar 2027", 380, D, 70) + gross("n3", "Preise ▲", 520, R, 180) + titel("t4", "Bis wann musst du handeln?", 400, O, 56) + gross("q4", "?", 520, R, 220) + CTA,
  lambda a, d: (f'pop("#t3", {a}); pop("#n3", {a} + 0.2); tl.set("#t4", {{ opacity: 0 }}, 0); tl.set("#q4", {{ opacity: 0 }}, 0);' + raus("t3", st("s4") - 0.05) + raus("n3", st("s4") - 0.05)
                + f' pop("#t4", {st("s4")}); pop("#q4", {st("s4")} + 0.2);' + cta_js), SFX_CTA, bis="s5")
S("s5", None, titel("t5", "Schauen wir genau hin", 640, D, 78) + pille("p5", "Strom · Gas · Kündigung", 900, O, "#fff", 50),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {a} + 0.3);')

# s6–s8 Zahlen
S("s6", None, titel("t6", "Strom · Grundversorger", 340, D, 58) + gross("n6", "58", 450, O, 240) + pille("p6", "Versorger erhöhen", 780, O, "#fff", 48) + pille("q6", "Ø +8 %", 920, R, "#fff", 64),
  lambda a, d: f'pop("#t6", {a}); pop("#n6", {a} + 0.15); pop("#p6", {cap("s6", 1)}); pop("#q6", {cap("s6", 2)});')
S("s7", None, titel("t7", "Gas · Grundversorger", 340, D, 58) + gross("n7", "82", 450, O, 240) + pille("p7", "Versorger erhöhen", 780, O, "#fff", 48) + pille("q7", "Ø +14 %", 920, R, "#fff", 64),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {a} + 0.15); pop("#p7", {cap("s7", 1)}); pop("#q7", {cap("s7", 2)});')
S("s8", None, titel("t8", "Verivox erwartet beim Gas", 340, D, 56) + gross("n8", "+10–20 %", 470, R, 190) + pille("p8", "je nach Tarif", 800, D, "#fff", 52),
  lambda a, d: f'pop("#t8", {a}); pop("#n8", {cap("s8", 1)}); pop("#p8", {cap("s8", 2)});')

# s9 Rechnung
S("s9", None, titel("t9", "Beispiel-Rechnung", 340, D, 64)
  + nl.karte("k9", "Gas pro Jahr", nl.zeile("r9a", "Gaskosten", "2.000 €", D) + nl.zeile("r9b", "Erhöhung", "+14 %", R, "▲")
             + f'<div id="r9c" class="nk-row" style="border-top:3px solid {D};margin-top:8px;font-weight:800;color:{D}">Mehrkosten<span class="v" style="color:{R};font-size:56px">≈ +280 €</span></div>', y=500),
  lambda a, d: f'pop("#t9", {a}); pop("#k9", {a} + 0.1); pop("#r9a", {cap("s9", 1)}); pop("#r9b", {cap("s9", 2)}); pop("#r9c", {cap("s9", 2)} + 0.6);')

# s10 Sonderkündigungsrecht
S("s10", None, titel("t10", "Bei Preiserhöhung", 340, D, 62) + gross("n10", "Sonder-<br/>kündigungs-<br/>recht", 470, G, 104) + pille("p10", "in der Regel ✓", 920, G, "#fff", 52),
  lambda a, d: f'pop("#t10", {a}); pop("#n10", {a} + 0.15); pop("#p10", {cap("s10", 2)});')

# s11 Frist
S("s11", None, titel("t11", "Wichtig: die Frist", 340, R, 66)
  + nl.karte("k11", "Beispiel N-ERGIE", f'<div style="font-weight:900;font-size:64px;color:{D};text-align:center;padding:14px 0;line-height:1.2">Kündigung bis<br/><span style="color:{R}">31. Dezember</span></div>', y=520)
  + pille("p11", "deine Frist steht im Brief", 900, O, "#fff", 44),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {cap("s11", 1)}); pop("#p11", {cap("s11", 3)});')

# s12 Brief lesen
S("s12", None, titel("t12", "Das solltest du tun", 340, D, 66)
  + nl.karte("k12", "Prüfen", nl.zeile("r12a", "Brief des Versorgers lesen", "✓", G) + nl.zeile("r12b", "Vertragsunterlagen ansehen", "✓", G), y=520),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.1); pop("#r12a", {cap("s12", 0)} + 0.4); pop("#r12b", {cap("s12", 1)});')

# s13 Gegenstimme / Vergleich
S("s13", None, titel("t13", "Je nach Anbieter", 340, D, 66)
  + nl.karte("k13", "Preise können auch", nl.zeile("r13a", "steigen", "▲", R) + nl.zeile("r13b", "sinken", "▼", G), y=520)
  + pille("p13", "Vergleich lohnt sich immer", 900, O, "#fff", 46),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.1); pop("#r13a", {cap("s13", 1)}); pop("#r13b", {cap("s13", 1)} + 0.5); pop("#p13", {cap("s13", 2)});')


def merk(sid, statisch=False):
    html = (titel(f"t{sid}", "Merk dir", 340, O, 70)
            + nl.karte(f"k{sid}", "Preiserhöhung", f'<div style="font-weight:900;font-size:72px;color:{G};text-align:center;padding:14px 0;line-height:1.15">= Kündigungsrecht ✓</div>', y=500))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#t{sid}", {a}); pop("#k{sid}", {a} + 0.15);'


h14, j14 = merk("s14")
S("s14", None, h14, j14)
h15, j15 = merk("s15", True)
S("s15", None, h15, j15)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s2", 1), "klick"), (cap("s7", 2), "kurve-hoch"), (cap("s9", 2) + 0.6, "kasse"), (cap("s10", 2), "richtig"), (cap("s11", 0), "alarm"), (cap("s14", 1), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "25.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
