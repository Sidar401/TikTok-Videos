#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (~64 s, Stimme Dan): Deutschlandticket – DB-Kunden müssen bis 30.11. zustimmen, sonst Abo weg;
ab 2027 Preis per Index (Personal 55 / Energie 20 / Sonstiges 25 %), künftig keine Zustimmung mehr; Kündigung bis 10.12. → longform-2027."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, balken, donut, hand, icon_gross, kalender, kasten,  # noqa: E402
                         news_kopf, stempel, titel_zeile, vergleich, zettel)
from glow_short import build, chip, handy  # noqa: E402
from lf_kit import Kit, folg_js, folg_logo, logo  # noqa: E402

DB = "#f01414"
K = Kit(HERE, 16, ["frei-frankfurt-nacht", "frei-euro", "frei-sitzung", "frei-frankfurt-staedel", "frei-miami-nacht", "frei-code-monitor", "frei-50euro", "frei-ocean-drive"],
        logos=["db.svg"])
cap, st = K.cap, K.st
S = K.szene


def ticket(id_, preis, y, x=230, w=620, dreh=-4):
    """Leitmotiv: das Deutschlandticket als Karte."""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{int(w * 0.58)}px;border-radius:30px;transform:rotate({dreh}deg);'
            f'background:linear-gradient(135deg,#e8eef2,#c9d3da);box-shadow:0 0 70px {OR}88, 0 30px 50px #000;z-index:3;overflow:hidden">'
            f'<div style="position:absolute;left:0;top:0;width:100%;height:28%;background:{DB}"></div>'
            f'<div style="position:absolute;left:36px;top:18px;font-weight:900;font-size:{int(w * 0.075)}px;color:#fff">DEUTSCHLAND-TICKET</div>'
            f'<div class="mono" style="position:absolute;left:36px;top:40%;font-size:{int(w * 0.05)}px;color:#333">ABO · MONATLICH</div>'
            f'<div style="position:absolute;left:36px;bottom:26px;font-weight:900;font-size:{int(w * 0.15)}px;color:#111">{preis}</div>'
            f'<div style="position:absolute;right:36px;bottom:36px;width:{int(w * 0.2)}px;height:{int(w * 0.2)}px;'
            f'background:repeating-linear-gradient(90deg,#111 0 10px,#fff 10px 16px),#111;opacity:.85;border-radius:6px"></div></div>')


S("s1", "frei-frankfurt-nacht", KIT_CSS + titel_zeile("t1", "⚡ Bahn-Kunden", farbe=ROT) + logo("l1", "db.svg", 600, 240, x=110, karte=False, glow=DB)
  + ticket("tk1", "63 €", 640, x=400, w=560, dreh=5) + stempel("s1x", "ABO WEG?", 250, 900, ROT, 96, -8),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#l1", {a}); pop("#tk1", {a} + 0.1); stempeln("#s1x", {cap("s1", 3)});',
  [(0.0, "eilmeldung")])

S("s2", "frei-sitzung", titel_zeile("t2", "Die Frist") + kalender("k2", "NOV", "30", 390, 620, 300, ROT) + chip("c2", "bis dahin zustimmen", ROT, 1020, 60),
  lambda a, d: f'pop("#t2", {a}); pop("#k2", {cap("s2", 1)}); slam("#c2", {cap("s2", 2)});')

S("s3", "frei-frankfurt-staedel", titel_zeile("t3", "Teilen") + icon_gross("i3", "👥", 0, 620, 300, OR, True) + chip("c3", "Teile das Video mit deinen Freunden", OR, 1020, 48),
  lambda a, d: f'pop("#t3", {a}); pop("#i3", {a} + 0.1); pop("#c3", {cap("s3", 1)});')

S("s4", "frei-euro", titel_zeile("t4", "Ab Januar") + vergleich("v4", "BISHER", "63 €", "AB 2027", "66,80 €", "#9aa4ab", ROT, y=620, h=300)
  + chip("c4", "+3,80 € im Monat", ROT, 1010, 64),
  lambda a, d: f'pop("#t4", {a}); pop("#v4-l", {a} + 0.1); pop("#v4-r", {cap("s4", 1)}); slam("#c4", {cap("s4", 1)} + 0.6);',
  [(cap("s4", 1), "mm-tippen")])

S("s5", "frei-code-monitor", titel_zeile("t5", "Neue Bedingungen") + zettel("z5", "Neue Tarif-<br/>bedingungen", 200, 640, 680, 76, GELB, -3)
  + icon_gross("i5", "✍️", 720, 900, 200, GELB),
  lambda a, d: f'pop("#t5", {a}); pop("#z5", {cap("s5", 1)}); pop("#i5", {cap("s5", 2)});')

S("s6", "frei-miami-nacht", titel_zeile("t6", "Sagst du nichts …", farbe=ROT) + ticket("tk6", "66,80 €", 650, x=240, w=600, dreh=-3)
  + stempel("s6x", "ABO ENDET", 220, 1040, ROT, 104, -8),
  lambda a, d: f'pop("#t6", {a}); pop("#tk6", {a} + 0.1); stempeln("#s6x", {cap("s6", 1)});',
  [(cap("s6", 1), "stempel")])

HANDY7 = ('<div style="font-weight:900;font-size:46px;color:#fff;margin-top:30px">DB Navigator</div>'
          '<div class="mono" style="font-size:26px;color:#ffffffaa;text-align:center">Ticket öffnen<br/>⋮ Menü</div>'
          f'<div id="b7" style="margin-top:30px;padding:20px 34px;border-radius:50px;background:{GRUEN};color:#111;font-weight:900;font-size:40px;white-space:nowrap;box-shadow:0 0 50px {GRUEN}">Zustimmen ✓</div>')
S("s7", "frei-code-monitor", titel_zeile("t7", "So geht's") + handy("h7", 330, 600, 360, HANDY7, OR) + hand("n7", "oder<br/>Abo-Portal", 735, 760, 58, GELB, -6),
  lambda a, d: (f'pop("#t7", {a}); pop("#h7", {a} + 0.1); pop("#b7", {cap("s7", 1)}); tl.fromTo("#b7", {{ scale: 1 }}, {{ scale: 0.9, duration: 0.12, yoyo: true, repeat: 1 }}, {cap("s7", 1)} + 0.5);'
                f' pop("#n7", {cap("s7", 2)});'),
  [(cap("s7", 1) + 0.5, "klick")])

S("s8", "frei-sitzung", titel_zeile("t8", "Anderer Anbieter?", farbe=GELB) + icon_gross("i8", "📩", 0, 620, 280, GELB, True)
  + chip("c8", "Dessen Nachricht zählt", GELB, 1000, 60),
  lambda a, d: f'pop("#t8", {a}); pop("#i8", {cap("s8", 1)}); slam("#c8", {cap("s8", 2)});')

S("s9", "frei-frankfurt-staedel", titel_zeile("t9", "Folg uns") + folg_logo("fl9", 600, 360) + chip("c9", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t9", {a}); {folg_js("fl9", a)} slam("#c9", {cap("s9", 0)} + 0.4);')

S("s10", "frei-ocean-drive", titel_zeile("t10", "Der Haken", farbe=ROT) + icon_gross("i10", "🪝", 0, 600, 340, ROT, True),
  lambda a, d: f'pop("#t10", {a}); slam("#i10", {cap("s10", 0)} + 0.3);',
  [(cap("s10", 0) + 0.3, "mm-bumm")])

S("s11", "frei-euro", titel_zeile("t11", "Ab 2027") + kasten("k11", "PREIS = INDEX", 140, 640, 800, 240, OR, 84, "fest berechnet")
  + hand("n11", "statt Politik-Streit", 160, 960, 66, GELB, -4),
  lambda a, d: f'pop("#t11", {a}); slam("#k11", {cap("s11", 1)}); pop("#n11", {cap("s11", 1)} + 0.6);')

LBL = lambda id_, t, x, y, f: f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;font-weight:900;font-size:50px;color:{f};text-shadow:0 0 24px {f};z-index:4">{t}</div>'
S("s12", "frei-50euro", titel_zeile("t12", "Was drinsteckt") + donut("d12", 300, 830, 190, [(0.55, OR), (0.20, GELB), (0.25, GRUEN)], 80)
  + LBL("l12a", "Löhne 55 %", 560, 660, OR) + LBL("l12b", "Energie 20 %", 560, 800, GELB) + LBL("l12c", "Sonstiges 25 %", 560, 940, GRUEN),
  lambda a, d: (f'pop("#t12", {a}); draw("#d12-0", {cap("s12", 0)}, 0.6); pop("#l12a", {cap("s12", 0)} + 0.3);'
                f' draw("#d12-1", {cap("s12", 1)}, 0.4); pop("#l12b", {cap("s12", 1)}); draw("#d12-2", {cap("s12", 1)} + 0.5, 0.4); pop("#l12c", {cap("s12", 1)} + 0.6);'))

B13 = "".join(balken(f"b13{i}", 110 + i * 175, 1130, 130, h, f, o, u, 44) for i, (h, f, o, u) in enumerate(
    [(290, "#9aa4ab", "49 €", "2023"), (340, "#9aa4ab", "58 €", "2025"), (370, OR, "63 €", "2026"), (395, ROT, "66,80", "2027"), (430, "#ffffff33", "?", "2028")]))
S("s13", "frei-frankfurt-nacht", titel_zeile("t13", "Jedes Jahr automatisch") + B13,
  lambda a, d: f'pop("#t13", {a}); ' + " ".join(f'wachs("#b13{i}", {a} + 0.15 + {i} * 0.35); pop("#b13{i}-o", {a} + 0.45 + {i} * 0.35);' for i in range(5)),
  [(st("s13") + 1.2, "kurve-hoch")])

S("s14", "frei-miami-nacht", titel_zeile("t14", "Ohne dein Ja") + icon_gross("i14", "🔄", 0, 620, 280, OR, True)
  + stempel("s14x", "AUTOMATISCH", 190, 960, ROT, 90, -6),
  lambda a, d: f'pop("#t14", {a}); pop("#i14", {a} + 0.1); tl.fromTo("#i14", {{ rotation: 0 }}, {{ rotation: 360, duration: 1.4, ease: "power2.inOut" }}, {a} + 0.4); stempeln("#s14x", {cap("s14", 2)});')

S("s15", "frei-sitzung", titel_zeile("t15", "Willst du raus?", farbe=GELB) + kalender("k15", "DEZ", "10", 390, 620, 300, GELB) + chip("c15", "bis dahin kündigen", GELB, 1020, 60),
  lambda a, d: f'pop("#t15", {a}); pop("#k15", {cap("s15", 1)}); slam("#c15", {cap("s15", 2)});')

MK = (titel_zeile("mk-t", "Ganzes Video") + f'<div id="mk-b" style="position:absolute;left:371px;top:690px;width:338px;height:600px;border-radius:30px;overflow:hidden;'
      f'border:8px solid {OR};box-shadow:0 0 80px {OR}88;z-index:3"><img src="assets/lf.jpg" style="width:100%;height:100%;object-fit:cover" alt=""/></div>'
      + chip("mk-c", "Jetzt auf unserem Kanal", OR, 580, 50))
S("s16", None, MK,
  lambda a, d: (f'pop("#mk-t", {a}); tl.fromTo("#mk-b", {{ scale: 0.6, rotation: -6, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {a} + 0.2);'
                f' pop("#mk-c", {a} + 0.6); tl.fromTo("#mk-c", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {a} + 1.0);'),
  [(st("s16"), "mm-wusch")])

K.SZ.append((0.0, K.dauer, news_kopf("18.11."), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
