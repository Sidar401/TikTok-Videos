#!/usr/bin/env python3
"""HundeFinanzTv (~122 s, Stimme Dan, Tempo 1.12) – KI-Serie Teil 2: Wer liefert (Strom, Chipmaschinen, Speicher). NEUES FORMAT.
Zahlen: Bitkom Rechenzentren DE 2026 ≈ 23 Mrd. kWh (= 6,5 Mio. Haushalte), 2030 bis 38, 2035 bis 70 Mrd. kWh, KI-Anteil 20 % → 55 %;
ASML Q3 11,66 Mrd. € (Vorjahr 7,5 → +55 %), Q4 14,2–15,2, Jahr 44–45 Mrd. €; Micron Schluss ≈ 656 $ vs. Rekord 1.213 $ (25.6.) ≈ −46 %, 5.11. −13…−17 %.
Kommentar-Overlay (stumm) bei s3–s4, Logo-Intro nach s5."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
WURZEL = HERE.parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 23)  # Logo-Intro nach s5

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 24, [], logos=["asml.svg", "micron.svg"])
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


def logo(id_, datei, y, w=560, h=170):
    return (f'<div id="{id_}" class="nk-karte" style="left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;padding:22px">'
            f'<img src="assets/logos/{datei}" style="width:100%;height:{h - 44}px;object-fit:contain"/></div>')


def balken(id_, y, breite, farbe, text, h=96, gr=38):
    return (f'<div id="{id_}" style="position:absolute;left:110px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def bar(id_, a, ziel=None):
    """Balken zeichnet sich von links."""
    return f'tl.fromTo("#{id_}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, {a});'


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


# s1 Hook
S("s1", None, nl.CSS + titel("t1", "Diese Firma baut keine KI", 330, D, 56) + logo("l1", "asml.svg", 450) + gross("n1", "11,66 Mrd. €", 680, O, 150)
  + pille("p1", "Umsatz in nur 3 Monaten", 900, D, "#fff", 46),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1", {a} + 0.1); pop("#n1", {cap("s1", 0)} + 0.3); pop("#p1", {cap("s1", 1)});')

# s2 Serie
S("s2", None, pille("p2a", "KI-SERIE", 400, O, "#fff", 54) + gross("n2", "TEIL 2", 520, D, 230)
  + nl.karte("k2a", "Teil 1", f'<div style="font-weight:800;font-size:48px;color:{D};text-align:center;padding:10px 0">Wer <span style="color:{O}">nutzt</span> KI?</div>', y=790)
  + nl.karte("k2b", "Teil 2 · heute", f'<div style="font-weight:800;font-size:48px;color:{D};text-align:center;padding:10px 0">Wer <span style="color:{O}">liefert</span> alles dafür?</div>', y=990),
  lambda a, d: f'pop("#p2a", {a}); pop("#n2", {a} + 0.15); pop("#k2a", {cap("s2", 1)}); pop("#k2b", {cap("s2", 2)});')

# s3–s4 Überblick + Kommentar-Overlay
TXT = "Kennst du ASML schon?"
CTA = nl.cta_overlay("co", "Kommentare", TXT, "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len(TXT), SFX_CTA, 1.6)
LISTE = nl.karte("k3", "Heute: 3 Bereiche", nl.zeile("r3a", "1 · Strom", "", D) + nl.zeile("r3b", "2 · Chipmaschinen", "", D) + nl.zeile("r3c", "3 · Speicher", "", D), y=360)
S("s3", None, LISTE + gross("q4", "−46 % ?", 400, R, 200) + pille("pq", "Selbst Gewinner stürzen ab", 680, D, "#fff", 46) + CTA,
  lambda a, d: (f'pop("#k3", {a}); pop("#r3a", {a} + 0.4); pop("#r3b", {a} + 0.8); pop("#r3c", {a} + 1.2); tl.set("#q4", {{ opacity: 0 }}, 0); tl.set("#pq", {{ opacity: 0 }}, 0);'
                + raus("k3", st("s4") - 0.05) + f' pop("#q4", {st("s4")}); pop("#pq", {cap("s4", 1)});' + cta_js),
  SFX_CTA, bis="s5")

# s5
S("s5", None, titel("t5", "Schauen wir genau hin", 640, D, 78) + pille("p5", "3 Bereiche · 3 Zahlen", 900, O, "#fff", 50),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {a} + 0.3);')

# ---- Bereich 1 Strom s6–s11 ----
S("s6", None, titel("t6", "Bereich 1: Strom", 340, O, 58) + gross("n6", "23 Mrd. kWh", 520, D, 150) + pille("p6", "Rechenzentren in Deutschland · 2026", 800, O, "#fff", 40),
  lambda a, d: f'pop("#t6", {a}); pop("#n6", {cap("s6", 1)}); pop("#p6", {cap("s6", 2)});')
S("s7", None, titel("t7", "Das entspricht", 340, D, 60) + gross("n7", "6,5 Mio.", 480, G, 230) + pille("p7", "Haushalten im Jahr", 800, G, "#fff", 50),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {a} + 0.15); pop("#p7", {cap("s7", 1)});')
S("s8", None, gross("n8", "6,5 Mio.?", 420, D, 170) + pille("p8", "Ja – und es wird mehr ▲", 760, R, "#fff", 52),
  lambda a, d: f'pop("#n8", {a}); pop("#p8", {cap("s8", 1)});')
S("s9", None, titel("t9", "Strombedarf Rechenzentren", 340, D, 54) + balken("b9a", 520, 330, "#8a93a1", "2026 · 23 Mrd.") + balken("b9b", 650, 560, O, "2030 · bis 38 Mrd.")
  + pille("p9", "Prognose Bitkom", 800, D, "#fff", 44),
  lambda a, d: f'pop("#t9", {a}); {bar("b9a", a + 0.3)} {bar("b9b", cap("s9", 2))} pop("#p9", {cap("s9", 3)});')
S("s10", None, titel("t10", "Strombedarf Rechenzentren", 340, D, 54) + balken("b10a", 520, 330, "#8a93a1", "2026 · 23 Mrd.") + balken("b10b", 650, 560, O, "2030 · bis 38 Mrd.")
  + balken("b10c", 780, 860, R, "2035 · bis 70 Mrd. kWh"),
  lambda a, d: f'pop("#t10", {a}); tl.set("#b10a", {{ opacity: 1 }}, 0); tl.set("#b10b", {{ opacity: 1 }}, 0); {bar("b10c", a + 0.2)}')
S("s11", None, titel("t11", "Anteil für KI", 340, D, 62) + balken("b11a", 520, 330, "#8a93a1", "2026 · 20 %") + balken("b11b", 650, 860, G, "2035 · 55 %")
  + pille("p11", "der Rechenzentren-Kapazität", 820, D, "#fff", 42),
  lambda a, d: f'pop("#t11", {a}); {bar("b11a", a + 0.3)} {bar("b11b", cap("s11", 1))} pop("#p11", {cap("s11", 2)});')

# ---- Bereich 2 ASML s12–s15 ----
S("s12", None, titel("t12", "Bereich 2: Chipmaschinen", 340, O, 58) + logo("l12", "asml.svg", 470) + pille("p12", "Niederlande · baut die Maschinen", 760, D, "#fff", 44)
  + pille("p12b", "ohne ASML kaum ein KI-Chip", 880, O, "#fff", 44),
  lambda a, d: f'pop("#t12", {a}); pop("#l12", {a} + 0.1); pop("#p12", {cap("s12", 1)}); pop("#p12b", {cap("s12", 2)});')
S("s13", None, titel("t13", "ASML · Umsatz pro Quartal", 340, D, 54) + balken("b13a", 520, 500, "#8a93a1", "Vor 1 Jahr · 7,5 Mrd. €") + balken("b13b", 650, 780, G, "Jetzt · 11,66 Mrd. €"),
  lambda a, d: f'pop("#t13", {a}); {bar("b13a", cap("s13", 1))} {bar("b13b", cap("s13", 2))}')
S("s14", None, titel("t14", "In nur einem Jahr", 340, D, 62) + gross("n14", "+55 %", 480, G, 260) + pille("p14", "mehr Umsatz", 860, G, "#fff", 50),
  lambda a, d: f'pop("#t14", {a}); pop("#n14", {a} + 0.15); pop("#p14", {cap("s14", 1)});')
S("s15", None, titel("t15", "ASML erwartet", 340, D, 62)
  + nl.karte("k15", "Umsatz-Prognose", nl.zeile("r15a", "4. Quartal", "14,2 – 15,2 Mrd. €", G) + nl.zeile("r15b", "Ganzes Jahr", "44 – 45 Mrd. €", G), y=520),
  lambda a, d: f'pop("#t15", {a}); pop("#k15", {a} + 0.1); pop("#r15a", {cap("s15", 1)}); pop("#r15b", {cap("s15", 3)});')

# ---- Bereich 3 Micron s16–s19 ----
S("s16", None, titel("t16", "Bereich 3: Speicher", 340, O, 58) + logo("l16", "micron.svg", 470) + pille("p16", "liefert den KI-Speicher", 760, D, "#fff", 46)
  + pille("p16b", "zuletzt Rekordzahlen ✓", 880, G, "#fff", 46),
  lambda a, d: f'pop("#t16", {a}); pop("#l16", {a} + 0.1); pop("#p16", {cap("s16", 1)}); pop("#p16b", {cap("s16", 3)});')
S("s17", None, titel("t17", "Micron-Aktie", 340, D, 62) + balken("b17a", 520, 860, G, "Rekord im Juni · ≈ 1.213 $") + balken("b17b", 650, 465, R, "Jetzt · ≈ 656 $")
  + gross("n17", "≈ −46 %", 820, R, 170),
  lambda a, d: f'pop("#t17", {a}); {bar("b17a", a + 0.2)} {bar("b17b", cap("s17", 1))} pop("#n17", {cap("s17", 2)});')
S("s18", None, titel("t18", "5. November", 340, D, 66) + gross("n18", "−10 %+", 480, R, 240) + pille("p18", "an einem einzigen Tag", 860, R, "#fff", 50),
  lambda a, d: f'pop("#t18", {a}); pop("#n18", {cap("s18", 1)}); pop("#p18", {cap("s18", 2)});')
S("s19", None, gross("n19", "Warum?", 380, D, 170)
  + nl.karte("k19", "Die Sorge der Anleger", f'<div style="font-weight:800;font-size:48px;color:{D};text-align:center;padding:14px 0;line-height:1.25">Wie lange geben Firmen<br/>noch so viel für <span style="color:{O}">KI</span> aus?</div>', y=640),
  lambda a, d: f'pop("#n19", {a}); pop("#k19", {cap("s19", 1)});')

# ---- Depot s20–s21 ----
S("s20", None, titel("t20", "Und dein Depot?", 340, D, 66)
  + nl.karte("k20", "Globale ETFs", nl.zeile("r20a", "ASML", "drin", D, "✓") + nl.zeile("r20b", "Micron", "drin", D, "✓") + nl.zeile("r20c", "Dein Depot", "schwankt mit", R, "▲▼"), y=520),
  lambda a, d: f'pop("#t20", {a}); pop("#k20", {a} + 0.1); pop("#r20a", {cap("s20", 1)}); pop("#r20b", {cap("s20", 1)} + 0.4); pop("#r20c", {cap("s20", 2)});')
S("s21", None, titel("t21", "Merk dir", 340, O, 70)
  + nl.karte("k21", "Lieferanten", nl.zeile("r21a", "Auch sie schwanken stark", "", D) + nl.zeile("r21b", "Alles hängt an den KI-Ausgaben", "", D), y=500),
  lambda a, d: f'pop("#t21", {a}); pop("#k21", {a} + 0.1); pop("#r21a", {cap("s21", 1)}); pop("#r21b", {cap("s21", 2)});')

# ---- Teaser s22 / Hinweis s23 / Folgen s24 ----
S("s22", None, pille("p22", "TEIL 3", 440, O, "#fff", 54)
  + nl.karte("k22", "Als Nächstes", f'<div style="font-weight:900;font-size:80px;color:{D};text-align:center;padding:18px 0">Roboter</div>', y=600),
  lambda a, d: f'pop("#p22", {a}); pop("#k22", {a} + 0.2);')
S("s23", None, pille("p23", "TEIL 3", 440, O, "#fff", 54)
  + nl.karte("k23", "Als Nächstes", f'<div style="font-weight:900;font-size:80px;color:{D};text-align:center;padding:18px 0">Roboter</div>', y=600),
  lambda a, d: 'tl.set("#p23", { opacity: 1 }, 0);')
S("s24", None, f'<div id="fl24" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n24" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c24", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl24", {a}); pop("#n24", {a} + 0.2); pop("#c24", {cap("s24", 0)} + 0.4);')

K.SFX.extend([(0.05, "bass-schlag"), (cap("s9", 2), "kurve-hoch"), (cap("s14", 1), "richtig"), (cap("s17", 2), "kurve-runter"),
              (cap("s18", 1), "mm-bumm"), (cap("s21", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("KI-SERIE · TEIL 2", "23.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
