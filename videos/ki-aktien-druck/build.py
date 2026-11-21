#!/usr/bin/env python3
"""HundeFinanzTv (~71 s, Stimme Dan) – KI-Aktien unter Druck, 20.11.2026. NEUES FORMAT.
Nvidia: Reuters – SEC prüft mögliche Buchhaltungsprobleme (kein Urteil), Aktie Fr. ≈ −14 % (schlimmster Tag seit Jan. 2025);
Anthropic: IPO 83 $, Tag 1 Schluss 97,17 $, Tag 2 88,30 $ (−9 %), Tief 83,05 $; Facebook Tag 2 −10 % unter IPO-Preis.
Quellen: Reuters/Investing.com, Bloomberg, 24/7 Wall St."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 15)  # Logo nach dem Open Loop (s3)

import glow_short as gs  # noqa: E402
import news_look as nl  # noqa: E402
from analyse_kit import KIT_JS  # noqa: E402
from lf_kit import Kit  # noqa: E402
from analyse_kit import symbol  # noqa: E402

G, R, D, O = nl.G, nl.R, nl.DUNKEL, nl.ORANGE
K = Kit(HERE, 13, ["chips"], logos=["nvidia.svg", "sec.svg", "anthropic.svg", "claude.svg", "meta.png"])
cap, st = K.cap, K.st
S = K.szene


def nvidia(id_, y, h=150):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;align-items:center;gap:26px;z-index:4">'
            + symbol("nvidia", h, "#76b900").replace("filter:drop-shadow(0 0 18px #76b90099)", "")
            + f'<img src="assets/logos/nvidia.svg" style="height:{int(h * 0.62)}px"/></div>')


def titel(id_, text, y=340, farbe=D, gr=70):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe};line-height:1.1">{text}</div>'


def pille(id_, text, y, farbe, schrift="#fff", gr=52):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:16px 46px;border-radius:60px;background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{text}</span></div>')


def gross(id_, text, y, farbe, gr=170):
    return f'<div id="{id_}" class="nk-gross" style="top:{y}px;font-size:{gr}px;color:{farbe}">{text}</div>'


# s1–s2 Hook
S("s1", None, nl.CSS + nl.foto("f1", "chips") + nvidia("l1", 330) + gross("n1", "−14 %", 640, R, 190)
  + nl.logo_frei("sec1", "sec.svg", 120, 900, 170) + pille("p1", "Börsenaufsicht prüft", 930, D, "#fff", 46).replace("justify-content:center", "justify-content:flex-end;padding-right:110px")
  + pille("p2", "Anthropic: fast am Ausgabepreis", 1170, O, "#fff", 46),
  lambda a, d: (KIT_JS + f' pop("#l1", {a}); pop("#n1", {cap("s1", 2)}); pop("#sec1", {cap("s1", 3)}); pop("#p1", {cap("s1", 4)});'
                f' pop("#p2", {cap("s2", 1)});'), [], bis="s3")

# s3 Open Loop
S("s3", None, titel("t3", "Am Ende: der Fehler,<br/>den gerade viele machen", 360, R, 60)
  + nl.karte("k3", "Achtung", f'<div style="font-weight:900;font-size:180px;color:{R};text-align:center;line-height:1.1">!</div>', y=620),
  lambda a, d: f'pop("#t3", {a}); pop("#k3", {cap("s3", 2)});')

# s4–s5 SEC-Prüfung
S("s4", None, nl.logo_frei("l4", "sec.svg", 400, 340, 280) + nl.karte("k4", "Bericht von Reuters",
  nl.zeile("r4", "SEC prüft Nvidias Buchhaltung", "?", O) + nl.zeile("r5a", "Kein Urteil", "✓", G) + nl.zeile("r5b", "Unschuldsvermutung", "✓", G), y=680),
  lambda a, d: (f'pop("#l4", {a}); pop("#k4", {cap("s4", 1)}); pop("#r4", {cap("s4", 2)}); pop("#r5a", {cap("s5", 1)}); pop("#r5b", {cap("s5", 2)});'),
  [], bis="s6")

# s6 Nvidia −14 %
S("s6", None, nvidia("l6", 330) + gross("n6", "−14 %", 620, R, 200)
  + pille("p6", "schlimmster Tag seit Januar 2025", 920, R, "#fff", 46),
  lambda a, d: f'pop("#l6", {a}); pop("#n6", {cap("s6", 1)}); pop("#p6", {cap("s6", 3)});')

# s7–s9 Anthropic: Kurs-Karte mit Ausgabepreis-Linie
ANT = (nl.zeile("r7a", "Ausgabepreis", "83,00 $", D) + nl.zeile("r7b", "Tag 1 (Schluss)", "97,17 $", G, "▲")
       + nl.zeile("r8", "Tag 2 (Schluss)", "88,30 $ · −9 %", R) + nl.zeile("r9", "Tief am Tag 2", "83,05 $", O))
S("s7", None, nl.logo_frei("l7", "anthropic.svg", 230, 340, 620) + nl.logo_frei("l7b", "claude.svg", 400, 460, 280)
  + nl.karte("k7", "Anthropic-Aktie", ANT, y=600) + pille("p9", "nur 5 Cent über dem Ausgabepreis!", 1140, O, "#fff", 44),
  lambda a, d: (f'pop("#l7", {a}); pop("#l7b", {a} + 0.2); pop("#k7", {cap("s7", 0)} + 0.4); pop("#r7a", {cap("s7", 1)}); pop("#r7b", {cap("s7", 3)});'
                f' pop("#r8", {cap("s8", 1)}); pop("#r9", {cap("s9", 1)}); pop("#p9", {cap("s9", 2)});'), [], bis="s10")

# s10 Facebook-Vergleich
S("s10", None, titel("t10", "Zum Vergleich", 340) + nl.logo_frei("l10", "meta.png", 340, 460, 400)
  + nl.karte("k10", "Facebook-Börsengang 2012", nl.zeile("r10a", "Tag 2", "−10 % unter Ausgabepreis", R) + nl.zeile("r10b", "Später", "ein Riese", G, "✓"), y=680),
  lambda a, d: f'pop("#t10", {a}); pop("#l10", {cap("s10", 1)}); pop("#k10", {cap("s10", 1)} + 0.3); pop("#r10a", {cap("s10", 2)}); pop("#r10b", {cap("s10", 4)});')

# s11 Der Fehler
S("s11", None, titel("t11", "Der Fehler", 340, R) + nl.karte("k11", "Was viele gerade tun",
  nl.zeile("r11a", "Zu teuer eingestiegen", "✗", R) + nl.zeile("r11b", "Aus Panik verkauft", "✗", R), y=520)
  + pille("p11", "Verlust gesichert – Erholung verpasst", 900, R, "#fff", 42),
  lambda a, d: f'pop("#t11", {a}); pop("#k11", {cap("s11", 1)}); pop("#r11a", {cap("s11", 3)}); pop("#r11b", {cap("s11", 2)}); pop("#p11", {cap("s11", 4)});')

# s12 Hinweis
S("s12", None, nl.karte("k12", "Kurzer Hinweis", f'<div style="font-size:52px;font-weight:800;color:{D};text-align:center;padding:30px 0">Keine Anlageberatung –<br/>nur erklärt.</div>', y=620),
  lambda a, d: f'pop("#k12", {a});')

# s13 Folgen
S("s13", None, f'<div id="fl13" style="position:absolute;left:340px;top:480px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:10px solid {O};'
  f'box-shadow:0 20px 50px #0003;background:#1b1f22;z-index:4"><img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
  + f'<div id="n13" class="nk-gross" style="top:920px;font-size:64px">HundeFinanz<span style="color:{O}">Tv</span></div>' + pille("c13", "+ Folgen", 1040, O, "#fff", 58),
  lambda a, d: f'pop("#fl13", {a}); pop("#n13", {a} + 0.2); pop("#c13", {cap("s13", 0)} + 0.4);')

html, code = ls.szene(hell=True)
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, nl.kopf("NEWS", "21.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    gs.build(HERE, K.SZ, K.SFX)
    nl.hell(HERE)
