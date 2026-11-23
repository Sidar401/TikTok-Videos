#!/usr/bin/env python3
"""HundeFinanzTv (~110 s, Stimme Dan, Tempo 1.12) – KI-Serie Teil 3: Roboter (für 24.11.). NEUES FORMAT.
IFR World Robotics 2026: 603.000 neue Industrieroboter 2025 (+11 %), 354.000 China (59 %), DE 24.800, 5 Mio. im Einsatz, ≈ 7.000 Humanoide verkauft;
Tesla-Optimus-Plan 1 Mio./Jahr (Wikipedia, Plan), Hyundai 80 % Boston Dynamics, Morgan Stanley: verzögerte Skalierung;
Agility Robotics SPAC-Börsengang (Nov. geplant) 620 Mio. $, Bewertung 2,5 Mrd. $ (Motley Fool 1.11.). Ende: Folgen-CTA vorletzter, Hinweis letzter Satz."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 27)  # Logo-Intro nach s5

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 20, [], logos=["tesla-symbol.png", "flagge-china.svg", "flagge-deutschland.svg"])
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


def logo(id_, datei, y, w=300, h=170):
    return (f'<div id="{id_}" class="nk-karte" style="left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;padding:22px">'
            f'<img src="assets/logos/{datei}" style="width:100%;height:{h - 44}px;object-fit:contain"/></div>')


def balken(id_, y, breite, farbe, text, h=96, gr=38, x=110):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def bar(id_, a):
    return f'tl.fromTo("#{id_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, {a});'


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


def kk(id_, kopf, text, y):
    return nl.karte(id_, kopf, f'<div style="font-weight:800;font-size:52px;color:{D};text-align:center;padding:14px 0;line-height:1.25">{text}</div>', y=y)


# s1 Hook
S("s1", None, nl.CSS + titel("t1", "Roboter 2025", 330, D, 58)
  + nl.karte("k1a", "Neu in Fabriken", f'<div style="font-weight:900;font-size:120px;color:{G};text-align:center;line-height:1.1">603.000</div>', y=450)
  + nl.karte("k1b", "In Menschenform verkauft", f'<div style="font-weight:900;font-size:120px;color:{R};text-align:center;line-height:1.1">≈ 7.000</div>', y=800),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#k1a", {a} + 0.1); pop("#k1b", {cap("s1", 2)});')

# s2 Serie
S("s2", None, pille("p2a", "KI-SERIE", 380, O, "#fff", 54) + gross("n2", "TEIL 3", 490, D, 230)
  + nl.karte("k2a", "Teil 1 · Teil 2", f'<div style="font-weight:800;font-size:44px;color:{D};text-align:center;padding:6px 0">Wer <span style="color:{O}">nutzt</span> KI · Wer <span style="color:{O}">liefert</span></div>', y=820)
  + nl.karte("k2b", "Teil 3 · heute", f'<div style="font-weight:900;font-size:72px;color:{O};text-align:center;padding:6px 0">Roboter</div>', y=1010),
  lambda a, d: f'pop("#p2a", {a}); pop("#n2", {a} + 0.15); pop("#k2a", {cap("s2", 1)}); pop("#k2b", {cap("s2", 3)});')

# s3–s4 Überblick + Kommentar-Overlay (stumm)
TXT = "Würdest du einen Roboter kaufen?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.6)
LISTE = nl.karte("k3", "Heute: 3 Bereiche", nl.zeile("r3a", "1 · Fabrik-Roboter", "", D) + nl.zeile("r3b", "2 · Menschen-Roboter", "", D) + nl.zeile("r3c", "3 · Die Börse", "", D), y=360)
S("s3", None, LISTE + gross("q4", "2,5 Mrd. $ ?", 420, R, 150) + pille("pq", "Welche Firma geht an die Börse?", 680, D, "#fff", 44) + CTA,
  lambda a, d: (f'pop("#k3", {a}); pop("#r3a", {cap("s3", 1)}); pop("#r3b", {cap("s3", 2)}); pop("#r3c", {cap("s3", 3)}); tl.set("#q4", {{ opacity: 0 }}, 0); tl.set("#pq", {{ opacity: 0 }}, 0);'
                + raus("k3", st("s4") - 0.05) + f' pop("#q4", {st("s4")}); pop("#pq", {cap("s4", 1)});' + cta_js),
  SFX_CTA, bis="s5")
S("s5", None, titel("t5", "Schauen wir genau hin", 640, D, 78) + pille("p5", "3 Bereiche · 3 Zahlen", 900, O, "#fff", 50),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {a} + 0.3);')

# ---- Bereich 1 ----
S("s6", None, titel("t6", "Bereich 1: Fabrik-Roboter", 340, O, 56) + gross("n6", "5 Mio.", 480, D, 240) + pille("p6", "arbeiten weltweit in Fabriken", 820, O, "#fff", 44),
  lambda a, d: f'pop("#t6", {a}); pop("#n6", {cap("s6", 1)}); pop("#p6", {cap("s6", 2)});')
S("s7", None, titel("t7", "Allein letztes Jahr neu", 340, D, 60) + gross("n7", "603.000", 480, G, 200) + pille("p7", "+11 % zum Vorjahr", 780, G, "#fff", 54),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {a} + 0.15); pop("#p7", {cap("s7", 2)});')
S("s8", None, titel("t8", "Neue Roboter 2025", 340, D, 60) + balken("b8a", 520, 760, G, "China · 354.000") + balken("b8b", 650, 535, "#8a93a1", "Rest · 249.000")
  + gross("n8", "59 %", 820, R, 190),
  lambda a, d: f'pop("#t8", {a}); {bar("b8a", cap("s8", 1))} {bar("b8b", cap("s8", 1) + 0.4)} pop("#n8", {cap("s8", 2)});')
S("s9", None, titel("t9", "Neue Roboter 2025", 340, D, 60)
  + nl.karte("k9", "Vergleich", nl.zeile("r9a", "China", "354.000", G, "▲") + nl.zeile("r9b", "Deutschland", "24.800", R), y=520),
  lambda a, d: f'pop("#t9", {a}); pop("#k9", {a} + 0.1); pop("#r9a", {cap("s9", 0)} + 0.6); pop("#r9b", {cap("s9", 2)});')

# ---- Bereich 2 ----
S("s10", None, titel("t10", "Bereich 2: Menschen-Roboter", 340, O, 54) + gross("n10", "≈ 7.000", 480, R, 220) + pille("p10", "verkauft im ganzen Jahr", 800, R, "#fff", 46),
  lambda a, d: f'pop("#t10", {a}); pop("#n10", {cap("s10", 1)}); pop("#p10", {cap("s10", 3)});')
S("s11", None, titel("t11", "Tesla · Optimus", 340, D, 62) + logo("l11", "tesla-symbol.png", 460, 260, 200) + gross("n11", "1 Mio. / Jahr", 700, O, 120) + pille("p11", "Plan, keine Produktion", 900, D, "#fff", 46),
  lambda a, d: f'pop("#t11", {a}); pop("#l11", {a} + 0.1); pop("#n11", {cap("s11", 1)}); pop("#p11", {cap("s11", 2)});')
S("s12", None, titel("t12", "Hyundai", 340, D, 66) + gross("n12", "80 %", 440, O, 230) + kk("k12", "von Boston Dynamics", "Roboter <span style=\"color:#f28a1e\">Atlas</span><br/>in Hyundai-Fabriken", 740),
  lambda a, d: f'pop("#t12", {a}); pop("#n12", {a} + 0.15); pop("#k12", {cap("s12", 1)});')
S("s13", None, titel("t13", "Aber: Morgan Stanley", 340, D, 62) + kk("k13", "Einschätzung", "Es dauert <span style=\"color:#d23c3c\">länger</span>,<br/>bis es viele davon gibt", 520),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.15);')

# ---- Bereich 3 ----
S("s14", None, titel("t14", "Bereich 3: Die Börse", 340, O, 58) + kk("k14", "Agility Robotics", "Börsengang <span style=\"color:#f28a1e\">geplant</span><br/>im November", 520),
  lambda a, d: f'pop("#t14", {a}); pop("#k14", {a} + 0.15);')
S("s15", None, titel("t15", "Agility Robotics", 340, D, 62)
  + nl.karte("k15", "Börsengang (geplant)", nl.zeile("r15a", "Bewertung", "2,5 Mrd. $", O) + nl.zeile("r15b", "Neues Geld", "620 Mio. $", G), y=520),
  lambda a, d: f'pop("#t15", {a}); pop("#k15", {a} + 0.1); pop("#r15a", {cap("s15", 1)}); pop("#r15b", {cap("s15", 2)});')
S("s16", None, gross("n16", "Viel Geld?", 420, D, 150) + pille("p16", "Roboter stehen erst am Anfang", 700, R, "#fff", 46),
  lambda a, d: f'pop("#n16", {a}); pop("#p16", {cap("s16", 1)});')
S("s17", None, titel("t17", "Chinesische Roboter-Aktien", 340, D, 56) + logo("l17", "flagge-china.svg", 470, 300, 200) + gross("n17", "▲ stark gestiegen", 740, G, 80),
  lambda a, d: f'pop("#t17", {a}); pop("#l17", {a} + 0.1); pop("#n17", {cap("s17", 1)});')
S("s18", None, titel("t18", "Merk dir", 340, O, 70)
  + nl.karte("k18", "Roboter", nl.zeile("r18a", "Heute: Fabrik-Roboter", "€", G) + nl.zeile("r18b", "Menschen-Roboter", "Zukunft", O), y=500),
  lambda a, d: f'pop("#t18", {a}); pop("#k18", {a} + 0.1); pop("#r18a", {cap("s18", 1)}); pop("#r18b", {cap("s18", 2)});')


def folgen(sid, statisch=False):
    html = (f'<div id="fl{sid}" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
            f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
            f'<div id="n{sid}" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille(f"c{sid}", "+ Folgen", 1040, O, "#fff", 58))
    if statisch:
        return html, lambda a, d: ""
    return html, lambda a, d: f'pop("#fl{sid}", {a}); pop("#n{sid}", {a} + 0.2); pop("#c{sid}", {cap(sid, 0)} + 0.4);'


h19, j19 = folgen("s19")
S("s19", None, h19, j19)
h20, j20 = folgen("s20", True)
S("s20", None, h20, j20)

K.SFX.extend([(0.05, "bass-schlag"), (cap("s8", 2), "mm-bumm"), (cap("s10", 1), "falsch"), (cap("s13", 1), "alarm"), (cap("s15", 2), "kasse"), (cap("s18", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("KI-SERIE · TEIL 3", "24.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
