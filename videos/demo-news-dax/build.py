#!/usr/bin/env python3
"""DEMO (ohne Stimme, 30 s): News-Format – DAX erstmals über 27.000 (12.11.2026)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = HERE.parent.parent
sys.path.insert(0, str(W / "scripts"))
from analyse_kit import (hintergrund, quelle, vergleich, wechsel_js, zoom_js, GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, NEWS_JS, OR, ROT, hand, icon_gross, kit_assets, kreis,  # noqa: E402
                         laufband_szene, linie, marke, news_kopf, raster, stempel, titel_zeile, zettel)
from glow_short import build, chip, partikel, t  # noqa: E402
from musik import beat  # noqa: E402

kit_assets(HERE, ["nvidia", "flagge-usa"])
D = 2.5
SZ, SFX = [], []


def text(id_, s):
    return t(id_, s, 1330, 72).replace('style="top:', 'style="z-index:6;top:', 1)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


HG = ['boerse', 'boerse', 'skyline', 'skyline', 'skyline', 'boerse', 'boerse', 'skyline', 'boerse', 'buero', 'buero', 'skyline']


def szene(i, html, js, sfx=()):
    a = round(i * D, 2)
    SZ.append((a, round(a + D, 2), hintergrund(HG[i]) + html, (lambda j, k: lambda a, d: j(a, d) + (wechsel_js(f"z{k}", a, k) if k else ""))(js, i)))
    SFX.extend((a + dt, s) for dt, s in sfx)


szene(0, KIT_CSS + titel_zeile("t0", "⚡ Eilmeldung", farbe=ROT) + tz("n0", "26.000", 650, 210, "glow-g") + tz("u0", "Punkte – DAX", 900, 70)
      + partikel("p0", 540, 760, 30, (GRUEN, GELB, "#fff"), 600) + quelle("q0", "Frankfurt · 12.11.2026", 1000) + text("x0", "DAX erstmals über 27.000"),
      lambda a, d: (KIT_JS + " " + NEWS_JS + f' pop("#t0", {a}); pop("#n0", {a} + 0.2); zaehl("#n0", 26000, 27000, {a} + 0.3, 1.4); burst("#p0", {a} + 1.7);'
                    f' pop("#u0", {a} + 0.4); flash({a} + 1.7, 0.5); pop("#x0", {a} + 0.3); pop("#q0", {a} + 0.6);' + zoom_js("#n0", a + 1.7, 0.8, 1.06)), [(0, "eilmeldung"), (0.3, "zaehler"), (1.7, "boersenglocke")])
KURS = linie("ku", [0.15, 0.25, 0.2, 0.4, 0.35, 0.55, 0.62, 0.8, 0.97], 150, 700, 780, 400, GRUEN, punkte=[(8, "27.000")])
szene(1, titel_zeile("t1", "Neues Allzeithoch") + KURS + kreis("k1", 930, 720, 110, 80, GELB, 6) + stempel("s1", "REKORD", 200, 640, GRUEN, 60, -6) + text("x1", "so hoch wie noch nie"),
      lambda a, d: f'pop("#t1", {a}); draw("#ku-p", {a} + 0.2, 1.2); pop("#ku-w0", {a} + 1.3); draw("#k1-p", {a} + 1.4, 0.4); stempeln("#s1", {a} + 1.5); pop("#x1", {a} + 0.3);',
      [(0, "ticker-rauschen"), (0.2, "kurve-hoch"), (1.5, "stempel")])
szene(2, titel_zeile("t2", "Grund 1: Ölpreis fällt") + icon_gross("i2", "🛢️", 230, 640, 260) + tz("a2", "▼", 660, 280, "glow-r").replace('style="z-index:5;top:660px', 'style="z-index:5;left:200px;top:660px')
      + text("x2", "Energie wird billiger"),
      lambda a, d: f'pop("#t2", {a}); pop("#i2", {a} + 0.2); tl.fromTo("#a2", {{ y: -120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "bounce.out" }}, {a} + 0.6); pop("#x2", {a} + 0.3);',
      [(0, "whoosh-schnell"), (0.6, "kurve-runter")])
szene(3, titel_zeile("t3", "Grund 2: Friedenshoffnung", gr=50) + icon_gross("i3", "🕊️", 0, 620, 280, "#ffffff", True) + chip("c3", "Amerika ↔ Iran", GRAU, 960, 56) + text("x3", "Hoffnung auf Frieden"),
      lambda a, d: f'pop("#t3", {a}); tl.fromTo("#i3", {{ x: -300, y: 80, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.7, ease: "power2.out" }}, {a} + 0.2); pop("#c3", {a} + 0.9); pop("#x3", {a} + 0.3);',
      [(0, "whoosh-weich"), (0.9, "pop")])
szene(4, titel_zeile("t4", "Grund 3: Tech erholt sich", gr=54) + icon_gross("i4", "💻", 0, 620, 260, "#4d8ff0", True) + stempel("s4", "ERHOLUNG", 300, 960, GRUEN, 66, -5) + text("x4", "Technik-Aktien ziehen an"),
      lambda a, d: f'pop("#t4", {a}); pop("#i4", {a} + 0.2); stempeln("#s4", {a} + 0.9); pop("#x4", {a} + 0.3);', [(0, "swipe"), (0.9, "stempel")])
szene(5, titel_zeile("t5", "Top & Flop im DAX") + vergleich("v5", "TOP", "Siemens<br/>+5 %", "FLOP", "Infineon<br/>−2,8 %") + quelle("q5", "Tagesverlauf · 12.11.", 970)
      + text("x5", "Gewinner und Verlierer"),
      lambda a, d: f'pop("#t5", {a}); pop("#v5-l", {a} + 0.2); pop("#v5-r", {a} + 0.8); pop("#q5", {a} + 1.1); pop("#x5", {a} + 0.3);', [(0.2, "kasse"), (0.8, "nv-falsch-buzzer")])
szene(6, titel_zeile("t6", "Frankfurter Börse") + icon_gross("i6", "🏛️", 0, 600, 200, OR, True) + tz("n6", "27.001", 840, 150, "glow-g") + quelle("q6", "DAX · Xetra · 12.11. · vormittags", 1020)
      + text("x6", "die Marke ist geknackt"),
      lambda a, d: f'pop("#t6", {a}); pop("#i6", {a} + 0.2); slam("#n6", {a} + 0.6); pop("#q6", {a} + 1.0); pop("#x6", {a} + 0.3);' + zoom_js("#n6", a + 0.9, 1.5), [(0.2, "boersenglocke")])
szene(7, titel_zeile("t7", "Aber in Amerika:") + marke("m7", "nvidia", 0, 680, 150, wortmarke="nvidia", mitte=True) + tz("n7", "−13 %", 880, 200, "glow-r") + text("x7", "Nvidia stürzt ab"),
      lambda a, d: f'pop("#t7", {a}); pop("#m7", {a} + 0.2); slam("#n7", {a} + 0.7); shake("#m7", {a} + 0.7); pop("#x7", {a} + 0.3);', [(0, "swipe"), (0.7, "crash-bass")])
szene(8, titel_zeile("t8", "40 Firmen im DAX") + raster("r8", 230, 620, 8, 5, 70, 14, "#4d8ff0", GRUEN) + text("x8", "die größten aus Deutschland"),
      lambda a, d: f'pop("#t8", {a}); tl.fromTo("#r8 .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.03, ease: "back.out(2)" }}, {a} + 0.2); pop("#x8", {a} + 0.3);', [(0, "zaehler")])
szene(9, titel_zeile("t9", "Rekord = zu spät?") + icon_gross("i9", "🤔", 0, 620, 280, GELB, True) + hand("h9", "Rekorde gab es schon oft", 540, 980, 62, GELB, -3, True) + text("x9", "die große Frage"),
      lambda a, d: f'pop("#t9", {a}); pop("#i9", {a} + 0.2); pop("#h9", {a} + 0.9); pop("#x9", {a} + 0.3);', [(0, "whoosh-weich"), (0.9, "nv-pling-idee")])
szene(10, titel_zeile("t10", "Wichtig") + zettel("z10", "Keine Anlage&shy;beratung –<br/>nur Nachrichten", 200, 640, 680, 76, GELB, -3) + text("x10", "informier dich selbst"),
      lambda a, d: f'pop("#t10", {a}); tl.fromTo("#z10", {{ y: -300, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, {a} + 0.2); pop("#x10", {a} + 0.3);',
      [(0, "zeitung")])
szene(11, titel_zeile("t11", "Morgen: neue News") + icon_gross("i11", "📰", 0, 640, 280, OR, True) + text("x11", "HundeFinanzTv NEWS"),
      lambda a, d: f'pop("#t11", {a}); slam("#i11", {a} + 0.2); pop("#x11", {a} + 0.3);', [(0, "whoosh-schnell"), (0.2, "nv-tusch")])

SZ.append((0.0, 30.0, news_kopf("12.11.2026"), lambda a, d: "", 8))
SZ.append(laufband_szene([("DAX ▲ 27.000 REKORD", GRUEN), ("SIEMENS ▲ +5 %", GRUEN), ("INFINEON ▼ −2,8 %", ROT), ("ÖL ▼", ROT), ("NVIDIA ▼ −13 %", ROT)], 30.0))

if __name__ == "__main__":
    build(HERE, SZ, SFX, dauer=30.0, musik=beat(30.0) * 0.35)
