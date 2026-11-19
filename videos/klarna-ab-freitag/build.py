#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (~66 s, alte Stimme wiederverwendet) – Klarna/PayPal: ab 20.11. Bonitätsprüfung auch < 200 € und zinslos (EU-Verbraucherkreditrichtlinie),
14 Tage Widerruf, Begründungspflicht, Black Friday 27.11. → longform-klarna. NEUES FORMAT (heller News-Look, Nutzer 19.11.), Folgen-CTA ans Ende verschoben.
Alte dunkle Version: alt/build.py (+ alt/timings.json, alt/voice.wav)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 9.5)  # Logo nach s2 (Datum)

import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from glow_short import build  # noqa: E402
from lf_kit import Kit  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
PINK = "#ffb3c7"
K = Kit(HERE, 16, ["frei-laptop", "frei-sitzung"], logos=["klarna.png", "paypal.png", "flagge-eu.svg"])
cap, st = K.cap, K.st
S = K.szene


def titel(id_, text, y=360, farbe=D, gr=72):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=56):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a">{text}</span></div>')


def logo_karte(id_, datei, x, y, w, bg="#fff", dreh=0):
    return (f'<div id="{id_}" class="nk-karte" style="left:{x}px;top:{y}px;width:{w}px;padding:34px;background:{bg};text-align:center;transform:rotate({dreh}deg)">'
            f'<img src="assets/logos/{datei}" style="max-width:100%;max-height:110px"/></div>')


def kalender(id_, tag, monat, oben, x, y, farbe=R, w=300):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:20px;overflow:hidden;background:#fff;box-shadow:0 16px 36px #0003;text-align:center;z-index:5">'
            f'<div style="background:{farbe};color:#fff;font-weight:800;font-size:{w * 0.11:.0f}px;padding:12px 0">{oben}</div>'
            f'<div style="font-weight:900;font-size:{w * 0.5:.0f}px;color:{D};line-height:1.05">{tag}</div>'
            f'<div style="font-weight:700;font-size:{w * 0.12:.0f}px;color:#555;padding-bottom:16px">{monat}</div></div>')


# s1 Hook
S("s1", None, nl.CSS + nl.foto("f1", "frei-laptop") + titel("t1", "Ab Freitag:<br/>„Nein“ beim Bezahlen?", 340, D, 70)
  + logo_karte("l1a", "klarna.png", 110, 600, 400, PINK, -3) + logo_karte("l1b", "paypal.png", 570, 620, 400, "#fff", 3)
  + pille("p1", "Später bezahlen", 900, PINK, D, 60) + pille("x1", "✗ abgelehnt", 1050, R, "#fff", 60),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1a", {a}); pop("#l1b", {cap("s1", 1)}); pop("#p1", {cap("s1", 2)}); pop("#x1", {cap("s1", 3)});',
  [], bis="s2")

# s2 Datum
S("s2", None, titel("t2", "Neue Regeln", 340, D, 76) + kalender("k2", "20", "NOVEMBER", "FREITAG", 390, 480)
  + nl.karte("c2", "Gilt für", nl.zeile("r2a", "Ratenkauf", "✓", O) + nl.zeile("r2b", "Kauf auf Rechnung", "✓", O), y=930),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 0)}); pop("#c2", {cap("s2", 2)}); pop("#r2a", {cap("s2", 2)} + 0.2); pop("#r2b", {cap("s2", 3)});')

# s3 Bisher
S("s3", None, titel("t3", "Bisher", 340) + nl.karte("c3", "Später bezahlen", nl.zeile("r3a", "1 Klick", "✓", G) + nl.zeile("r3b", "Prüfung", "keine", "#8a909a"), y=520),
  lambda a, d: f'pop("#t3", {a}); pop("#c3", {a} + 0.1); pop("#r3a", {cap("s3", 0)} + 0.4); pop("#r3b", {cap("s3", 1)});')

# s4–s5 Jetzt
S("s4", None, nl.foto("f4", "frei-sitzung") + titel("t4", "Ab 20.11.", 340, R) + nl.karte("c4", "Der Anbieter muss prüfen",
  nl.zeile("r4a", "Kannst du es dir leisten?", "?", O) + nl.zeile("r5a", "auch unter 200 €", "✓", R) + nl.zeile("r5b", "auch zinslos", "✓", R), y=520),
  lambda a, d: (f'pop("#t4", {a}); pop("#c4", {a} + 0.1); pop("#r4a", {cap("s4", 2)});'
                f' pop("#r5a", {cap("s5", 1)}); pop("#r5b", {cap("s5", 2)});'), [], bis="s6")

# s6 EU-Regel
S("s6", None, f'<img id="e6" src="assets/logos/flagge-eu.svg" style="position:absolute;left:390px;top:360px;width:300px;border-radius:10px;box-shadow:0 12px 26px #0003;z-index:4"/>'
  + nl.karte("c6", "Der Grund", f'<div style="font-weight:800;font-size:50px;color:{D};text-align:center;padding:16px 0">Neue EU-Regel für<br/>Verbraucherkredite</div>', y=640),
  lambda a, d: f'pop("#e6", {a}); pop("#c6", {cap("s6", 1)});')

# s7 Später zahlen = Kredit
S("s7", None, titel("t7", "Später zahlen", 420, D, 90) + titel("eq7", "=", 560, O, 120) + titel("k7", "ein Kredit", 720, R, 110),
  lambda a, d: f'pop("#t7", {cap("s7", 0)}); pop("#eq7", {cap("s7", 1)}); pop("#k7", {cap("s7", 2)});')

# s8 Mahngebühren
S("s8", None, titel("t8", "Die Gefahr", 340, R) + nl.karte("c8", "Was oft passiert",
  nl.zeile("r8a", "Überblick verloren", "✗", R) + nl.zeile("r8b", "Mahngebühren", "€ €", R), y=520),
  lambda a, d: f'pop("#t8", {a}); pop("#c8", {a} + 0.1); pop("#r8a", {cap("s8", 1)}); pop("#r8b", {cap("s8", 2)});')

# s9–s11 Rechte
S("s9", None, titel("t9", "Die gute Nachricht", 340, G, 68) + nl.karte("c9", "Deine neuen Rechte",
  nl.zeile("r10", "Widerruf", "14 Tage", G, "✓") + nl.zeile("r11", "Ablehnung", "mit Begründung", G, "✓"), y=520)
  + titel("n10", "14 Tage", 900, G, 140),
  lambda a, d: (f'pop("#t9", {a}); pop("#c9", {cap("s9", 1)}); pop("#r10", {cap("s10", 1)}); pop("#n10", {cap("s10", 2)});'
                f' tl.to("#n10", {{ opacity: 0, duration: 0.2 }}, {st("s11")}); pop("#r11", {cap("s11", 2)});'), [], bis="s12")

# s12–s13 Black Friday
S("s12", None, titel("t12", "Wichtig", 340, R) + kalender("k12", "27", "NOVEMBER", "BLACK FRIDAY", 390, 480, D)
  + pille("p13", "Rechnung? ✗ abgelehnt", 960, R, "#fff", 50),
  lambda a, d: f'pop("#t12", {a}); pop("#k12", {cap("s12", 0)} + 0.3); pop("#p13", {cap("s13", 2)});', [], bis="s14")

# s14 Tipp
S("s14", None, titel("t14", "Unser Tipp", 340, G) + nl.karte("c14", "Bevor du klickst",
  f'<div style="font-weight:800;font-size:54px;color:{D};text-align:center;padding:20px 0">Kauf nur, was du<br/><span style="color:{G}">heute schon</span> bezahlen könntest</div>', y=520),
  lambda a, d: f'pop("#t14", {a}); pop("#c14", {cap("s14", 0)} + 0.3);')

# s15 Hinweis Longform
S("s15", None, titel("t15", "Ganzes Video", 340)
  + f'<div id="b15" style="position:absolute;left:371px;top:480px;width:338px;height:600px;border-radius:24px;overflow:hidden;border:8px solid {O};box-shadow:0 20px 40px #0003;z-index:4">'
    f'<img src="assets/lf.jpg" style="width:100%;height:100%;object-fit:cover"/></div>' + pille("c15", "Auf unserem Kanal", 1120, O, "#fff", 50),
  lambda a, d: f'pop("#t15", {a}); pop("#b15", {a} + 0.2); pop("#c15", {a} + 0.6);')

# s16 Folgen (letzter Satz)
S("s16", None, f'<div id="fl16" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n16" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c16", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl16", {a}); pop("#n16", {a} + 0.2); pop("#c16", {cap("s16", 0)} + 0.4);')

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "19.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
