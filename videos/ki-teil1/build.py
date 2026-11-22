#!/usr/bin/env python3
"""HundeFinanzTv (~134 s, Stimme Dan, Tempo 1.12) – KI-Serie Teil 1: Wer verdient an KI (Anwendungen). NEUES FORMAT.
Struktur-Vorbild (nur Aufbau, nicht Inhalt): Bereiche mit je einer fetten Zahl + Zwischenfragen + Serien-Teaser.
Zahlen: Copilot >30 Mio. bezahlte Lizenzen (+10 Mio./Quartal, ~450 Mio. M365-Nutzer → ~6,7 %); Meta Q3 Werbung 63,1 Mrd. $ (+26 %, Preis/Anzeige +14 %);
Gartner KI-Sicherheit 51,3 → ~86 Mrd. $ (2026→2027); CrowdStrike ~+26 %; Palantir Q3 +96 % (2,313 Mrd. $), US-Kommerz 984 Mio. > US-Staat 953 Mio., TCV US-Kommerz +11 % (Vorquartal +153 %);
Thomson Reuters −16 % am 3.2.2026 (Claude-Legal-Plugin). Kommentar-Overlay (silent) bei s3–s4, Logo-Intro nach s5."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
WURZEL = HERE.parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 21)  # Logo-Intro nach s5 (Satzende ≈ 22,2 s)

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
LOGOS = ["microsoft.svg", "meta.png", "crowdstrike.svg", "palantir.svg", "thomsonreuters.svg", "anthropic.svg"]
K = Kit(HERE, 26, [], logos=LOGOS)
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


def logo(id_, datei, y, w=420, h=150):
    return (f'<div id="{id_}" class="nk-karte" style="left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;padding:22px">'
            f'<img src="assets/logos/{datei}" style="width:100%;height:{h - 44}px;object-fit:contain"/></div>')


def balken(id_, y, breite, farbe, text, h=96, gr=40):
    return (f'<div id="{id_}" style="position:absolute;left:110px;top:{y}px;width:{breite}px;height:{h}px;background:{farbe};border-radius:14px;color:#fff;font-weight:900;'
            f'font-size:{gr}px;display:flex;align-items:center;padding:0 26px;white-space:nowrap;box-shadow:0 12px 26px #0002;z-index:4;transform-origin:0 50%">{text}</div>')


def raus(id_, t):
    return f' tl.to("#{id_}", {{ opacity: 0, duration: 0.2 }}, {t});'


# ---------- s1 Hook ----------
S("s1", None, nl.CSS + titel("t1", "Microsoft verkauft KI-Lizenzen", 330, D, 56) + logo("l1", "microsoft.svg", 450) + gross("n1", "30 Mio.", 660, O, 220)
  + pille("p1", "bezahlt – und erst der Anfang", 960, D, "#fff", 46),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1", {a} + 0.1); pop("#n1", {cap("s1", 0)} + 0.3); pop("#p1", {cap("s1", 3)});')

# ---------- s2 Serie ----------
S("s2", None, pille("p2a", "KI-SERIE", 440, O, "#fff", 54) + gross("n2", "TEIL 1", 560, D, 230)
  + nl.karte("k2", "Teil 2 (bald)", f'<div style="font-weight:800;font-size:50px;color:{D};text-align:center;padding:18px 0">Wer liefert<br/><span style="color:{O}">Strom und Chips?</span></div>', y=950),
  lambda a, d: f'pop("#p2a", {a}); pop("#n2", {a} + 0.15); pop("#k2", {cap("s2", 2)});')

# ---------- s3–s4: Überblick + Kommentar-Overlay (ohne gesprochenen Satz) ----------
CTA = nl.cta_overlay("co", "Kommentare", "Welche KI nutzt du am meisten?", "Kommentieren", "DEINE MEINUNG", "IN DIE KOMMENTARE", 930)
cta_js = nl.cta_overlay_js("co", st("s3"), len("Welche KI nutzt du am meisten?"), SFX_CTA, 1.6)
LISTE = nl.karte("k3", "Heute: 5 Bereiche",
                 nl.zeile("r3a", "1 · Büro-Software", "", D) + nl.zeile("r3b", "2 · Werbung", "", D) + nl.zeile("r3c", "3 · Sicherheit", "", D)
                 + nl.zeile("r3d", "4 · Daten", "", D) + nl.zeile("r3e", "5 · Die Verlierer", "", R), y=340)
S("s3", None, LISTE + gross("q4", "−16 % ?", 420, R, 200) + pille("pq", "Wer verliert an einem Tag?", 700, D, "#fff", 46) + CTA,
  lambda a, d: (f'pop("#k3", {a}); pop("#r3a", {a} + 0.4); pop("#r3b", {a} + 0.7); pop("#r3c", {a} + 1.0); pop("#r3d", {a} + 1.3); pop("#r3e", {a} + 1.6);'
                f' tl.set("#q4", {{ opacity: 0 }}, 0); tl.set("#pq", {{ opacity: 0 }}, 0);' + raus("k3", st("s4") - 0.05) + f' pop("#q4", {st("s4")}); pop("#pq", {cap("s4", 1)});' + cta_js),
  SFX_CTA, bis="s5")

# ---------- s5 Überleitung ----------
S("s5", None, titel("t5", "Schauen wir genau hin", 640, D, 78) + pille("p5", "5 Bereiche · 5 Zahlen", 900, O, "#fff", 50),
  lambda a, d: f'pop("#t5", {a}); pop("#p5", {a} + 0.3);')

# ---------- Bereich 1: Büro-Software (s6–s8) ----------
S("s6", None, titel("t6", "Bereich 1: Büro-Software", 340, O, 58) + logo("l6", "microsoft.svg", 470) + gross("n6", "30 Mio.+", 680, D, 200)
  + pille("p6", "bezahlte Copilot-Lizenzen", 960, O, "#fff", 46),
  lambda a, d: f'pop("#t6", {a}); pop("#l6", {a} + 0.1); pop("#n6", {cap("s6", 1)}); pop("#p6", {cap("s6", 2)});')
S("s7", None, titel("t7", "In nur 3 Monaten", 340, D, 64) + gross("n7", "+10 Mio.", 520, G, 220) + pille("p7", "neue bezahlte Lizenzen", 820, G, "#fff", 48),
  lambda a, d: f'pop("#t7", {a}); pop("#n7", {a} + 0.15); pop("#p7", {cap("s7", 1)});')
BAL = ('<div id="b8" style="position:absolute;left:110px;top:620px;width:860px;height:110px;background:#e4e7ec;border-radius:14px;overflow:hidden;z-index:4;box-shadow:0 12px 26px #0002">'
       f'<div id="b8g" style="position:absolute;left:0;top:0;height:110px;width:58px;background:{G};transform-origin:0 50%"></div></div>')
S("s8", None, titel("t8", "450 Mio. Büro-Nutzer", 340, D, 60) + BAL + gross("n8", "≈ 1 von 15", 800, R, 150)
  + pille("p8", "hat erst KI dazugebucht", 1010, D, "#fff", 44),
  lambda a, d: (f'pop("#t8", {a}); pop("#b8", {a} + 0.2); tl.fromTo("#b8g", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power2.out" }}, {cap("s8", 1)});'
                f' pop("#n8", {cap("s8", 2)}); pop("#p8", {cap("s8", 2)} + 0.5);'))

# ---------- Bereich 2: Werbung (s9–s12) ----------
S("s9", None, titel("t9", "Bereich 2: Werbung", 340, O, 58) + logo("l9", "meta.png", 470) + gross("n9", "63 Mrd. $", 690, D, 190)
  + pille("p9", "Werbeumsatz in 3 Monaten", 960, O, "#fff", 46),
  lambda a, d: f'pop("#t9", {a}); pop("#l9", {a} + 0.1); pop("#n9", {cap("s9", 1)}); pop("#p9", {cap("s9", 3)});')
S("s10", None, titel("t10", "Verglichen mit dem Vorjahr", 340, D, 56) + gross("n10", "+26 %", 480, G, 260) + pille("p10", "mehr Werbeumsatz", 860, G, "#fff", 50),
  lambda a, d: f'pop("#t10", {a}); pop("#n10", {a} + 0.15); pop("#p10", {cap("s10", 1)});')
S("s11", None, titel("t11", "KI wählt deine Anzeige", 340, D, 60)
  + nl.karte("k11", "Meta · Werbung", nl.zeile("r11a", "KI wählt aus, was du siehst", "✓", G) + nl.zeile("r11b", "Preis pro Anzeige", "+14 %", R, "▲"), y=520),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {a} + 0.1); pop("#r11a", {cap("s11", 1)}); pop("#r11b", {cap("s11", 2)});')
S("s12", None, titel("t12", "Vierzehn Prozent teurer?", 340, R, 60) + pille("p12", "Ja – weil sie besser trifft", 640, G, "#fff", 52)
  + nl.karte("k12", "Mehr Geld pro Anzeige", f'<div style="font-weight:900;font-size:110px;color:{R};text-align:center;line-height:1.1">+14 %</div>', y=800),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {a} + 0.15); pop("#p12", {cap("s12", 1)});')

# ---------- Bereich 3: Sicherheit (s13–s15) ----------
S("s13", None, titel("t13", "Bereich 3: Sicherheit", 340, O, 58)
  + nl.karte("k13", "Mehr KI im Netz", nl.zeile("r13a", "Mehr Programme", "▲", O) + nl.zeile("r13b", "Mehr Angriffsfläche", "▲", R) + nl.zeile("r13c", "Mehr Arbeit für Hacker", "▲", R), y=520),
  lambda a, d: f'pop("#t13", {a}); pop("#k13", {a} + 0.1); pop("#r13a", {a} + 0.6); pop("#r13b", {cap("s13", 1)}); pop("#r13c", {cap("s13", 2)});')
S("s14", None, titel("t14", "Ausgaben für KI-Sicherheit", 340, D, 56) + balken("b14a", 560, 400, "#8a93a1", "2026 · 51 Mrd. $") + balken("b14b", 700, 780, G, "2027 · ≈ 86 Mrd. $")
  + pille("p14", "laut Gartner", 900, D, "#fff", 44),
  lambda a, d: (f'pop("#t14", {a}); tl.fromTo("#b14a", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5 }}, {cap("s14", 1)}); tl.fromTo("#b14b", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8 }}, {cap("s14", 2)} + 0.3);'
                f' pop("#p14", {cap("s14", 0)} + 0.4);'))
S("s15", None, titel("t15", "Eine der größten Sicherheitsfirmen", 340, D, 44) + logo("l15", "crowdstrike.svg", 470) + gross("n15", "+26 %", 690, G, 240)
  + pille("p15", "Umsatzwachstum", 1000, G, "#fff", 48),
  lambda a, d: f'pop("#t15", {a}); pop("#l15", {a} + 0.1); pop("#n15", {cap("s15", 1)}); pop("#p15", {cap("s15", 2)});')

# ---------- Bereich 4: Daten / Palantir (s16–s20) ----------
S("s16", None, titel("t16", "Bereich 4: Daten", 340, O, 58) + logo("l16", "palantir.svg", 470, 640, 150) + gross("n16", "+96 %", 680, G, 260)
  + pille("p16", "Umsatz fast verdoppelt", 1000, G, "#fff", 48),
  lambda a, d: f'pop("#t16", {a}); pop("#l16", {a} + 0.1); pop("#n16", {cap("s16", 1)}); pop("#p16", {cap("s16", 2)});')
S("s17", None, titel("t17", "Erstmals: Firmen vor Staat", 340, D, 58) + balken("b17a", 520, 780, G, "Unternehmen USA · 984 Mio. $") + balken("b17b", 660, 750, "#8a93a1", "US-Staat · 953 Mio. $")
  + pille("p17", "pro Quartal", 830, D, "#fff", 44),
  lambda a, d: f'pop("#t17", {a}); tl.fromTo("#b17a", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7 }}, {cap("s17", 1)}); tl.fromTo("#b17b", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7 }}, {cap("s17", 1)} + 0.5); pop("#p17", {cap("s17", 1)} + 1.2);')
S("s18", None, titel("t18", "Und trotzdem:", 400, D, 70) + gross("n18", "Aktie ▼", 560, R, 220),
  lambda a, d: f'pop("#t18", {a}); pop("#n18", {a} + 0.3);')
S("s19", None, titel("t19", "Warum? Neue Aufträge", 340, D, 58)
  + nl.karte("k19", "Palantir · US-Firmen", nl.zeile("r19a", "Vorher", "+153 %", G) + nl.zeile("r19b", "Jetzt", "+11 %", R, "▼"), y=520),
  lambda a, d: f'pop("#t19", {a}); pop("#k19", {a} + 0.1); pop("#r19a", {cap("s19", 1)}); pop("#r19b", {cap("s19", 2)});')
S("s20", None, titel("t20", "Gute Zahlen reichen nicht", 380, D, 62) + pille("p20", "Anleger wollen mehr Tempo", 640, O, "#fff", 50)
  + nl.karte("k20", "Merke", f'<div style="font-weight:900;font-size:64px;color:{D};text-align:center;padding:14px 0">Tempo <span style="color:{O}">&gt;</span> Zahl</div>', y=820),
  lambda a, d: f'pop("#t20", {a}); pop("#p20", {cap("s20", 1)}); pop("#k20", {cap("s20", 2)});')

# ---------- Bereich 5: Die Verlierer (s21–s24) ----------
S("s21", None, titel("t21", "Bereich 5: Die Verlierer", 340, R, 58) + logo("l21", "anthropic.svg", 470) + pille("p21", "zeigt KI-Werkzeug für Juristen", 760, D, "#fff", 46)
  + titel("n21", "Februar 2026", 900, D, 60),
  lambda a, d: f'pop("#t21", {a}); pop("#l21", {a} + 0.1); pop("#p21", {cap("s21", 1)}); pop("#n21", {cap("s21", 2)});')
S("s22", None, titel("t22", "An einem Tag", 340, D, 64) + logo("l22", "thomsonreuters.svg", 450, 640, 150) + gross("n22", "−16 %", 660, R, 260)
  + pille("p22", "Infos für Anwälte", 980, D, "#fff", 46),
  lambda a, d: f'pop("#t22", {a}); pop("#l22", {a} + 0.1); pop("#n22", {cap("s22", 0)} + 0.4); pop("#p22", {cap("s22", 2)});')
S("s23", None, gross("n23", "Autsch.", 420, R, 150)
  + nl.karte("k23", "Aber:", f'<div style="font-weight:800;font-size:50px;color:{D};text-align:center;padding:14px 0">Manche Fachleute sagen:<br/><span style="color:{O}">Angst übertrieben</span></div>', y=700),
  lambda a, d: f'pop("#n23", {a}); pop("#k23", {cap("s23", 1)});')
S("s24", None, titel("t24", "Merk dir", 340, O, 70)
  + nl.karte("k24", "KI-Regeln", nl.zeile("r24a", "Nicht jede Firma mit KI gewinnt", "", D) + nl.zeile("r24b", "Gute Zahlen ≠ steigender Kurs", "", D), y=500),
  lambda a, d: f'pop("#t24", {a}); pop("#k24", {a} + 0.1); pop("#r24a", {cap("s24", 1)}); pop("#r24b", {cap("s24", 2)});')

# ---------- s25 Teaser Teil 2 / s26 Folgen ----------
S("s25", None, pille("p25", "TEIL 2", 440, O, "#fff", 54)
  + nl.karte("k25", "Als Nächstes", f'<div style="font-weight:900;font-size:60px;color:{D};text-align:center;padding:18px 0;line-height:1.2">Wer liefert<br/><span style="color:{O}">Strom und Chips?</span></div>', y=600),
  lambda a, d: f'pop("#p25", {a}); pop("#k25", {a} + 0.2);')
S("s26", None, f'<div id="fl26" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n26" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c26", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl26", {a}); pop("#n26", {a} + 0.2); pop("#c26", {cap("s26", 0)} + 0.4);')

K.SFX.extend([(0.05, "bass-schlag"), (cap("s7", 1), "richtig"), (cap("s10", 1), "kurve-hoch"), (cap("s18", 0), "kurve-runter"),
              (cap("s22", 0) + 0.4, "mm-bumm"), (cap("s24", 2), "richtig")])

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("KI-SERIE · TEIL 1", "22.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
