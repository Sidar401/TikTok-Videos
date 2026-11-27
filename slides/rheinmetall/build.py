#!/usr/bin/env python3
"""Slideshow „Rheinmetall kappt sein Ziel“ (27.11.2026, 3:4, dunkel). Zahlen: Kapitalmarkttag Hamburg 27.11.2026 (investing.com, cash-online, aktiencheck, Dr. Web)."""
import sys
sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import slide_dark34 as s34  # noqa: E402
from slide_dark34 import G, ROT, O, W, glas, kopf, logo_chip, pfeil, pille, quelle, txt, von_nach  # noqa: E402

OUT = "/home/user/tiktok-videos/renders/slides/rheinmetall/"
D = "27.11.2026"
N = 5

# Thumbnail (zählt nicht mit): Logo, Überschrift, +3 %, Pfeil
th = (kopf(D) + logo_chip("rheinmetall.svg", 270, 620, 200) + txt("KAPPT SEIN ZIEL", 520, 110, ROT)
      + pille("Aktie steigt trotzdem", 680, "#1d2330", 54) + txt("+ 3 %", 790, 210, G) + pfeil(1150, 260))
s34.speichern(th, OUT + "thumbnail.jpg")

s1 = (kopf(D, f"1 / {N}") + txt("Umsatzziel 2030", 260, 80, O)
      + glas(von_nach("45 Mrd. €", "33–37 Mrd. €", "Umsatz im Jahr 2030", 58), 380, 360) + pille("gesenkt", 800, ROT, 64)
      + txt("Das hat Rheinmetall heute<br>auf dem Kapitalmarkttag verkündet.", 930, 44, "#e5e7eb") + pfeil(1180, 150) + quelle("Altes Ziel: rund 45 Mrd. € (Quellen nennen 45–50) · Kapitalmarkttag Hamburg"))
s2 = (kopf(D, f"2 / {N}") + txt("Wie viel weniger?", 260, 80, O)
      + glas('<div style="font-weight:700;font-size:44px;color:#cbd5e1">beim Umsatzziel</div>'
             f'<div style="font-weight:900;font-size:210px;line-height:1.1;color:{ROT};text-shadow:0 0 50px {ROT}aa">−22 %</div>'
             '<div style="font-weight:700;font-size:40px;color:#e5e7eb">Mitte 35 gegen 45 Mrd. €</div>', 380, 560)
      + pille("eigene Rechnung", 990, "#1d2330", 46) + pfeil(1180, 150) + quelle("Eigene Rechnung aus den Zielen des Konzerns"))
s3 = (kopf(D, f"3 / {N}") + txt("Marge und 2026", 260, 80, O)
      + glas("".join(f'<div style="display:flex;width:100%;align-items:center;justify-content:space-between;font-weight:800;font-size:42px;padding:18px 0;border-bottom:2px solid #ffffff14"><span style="color:#e5e7eb;font-weight:600">{a}</span><span style="color:{c}">{b}</span></div>'
                     for a, b, c in [("Marge 2030", "≈ 20 %", W), ("Umsatz 2026", "13,2 Mrd. €", W), ("Marge 2026", "≈ 18,5 %", W)]), 380, 470)
      + pille("2026-Prognose unverändert", 900, G, 50) + pfeil(1180, 150) + quelle("Quelle: Rheinmetall-Kapitalmarkttag, laut cash-online / aktiencheck"))
s4 = (kopf(D, f"4 / {N}") + txt("Und die Aktie?", 260, 80, O)
      + glas(f'<div style="font-weight:900;font-size:210px;line-height:1.1;color:{G};text-shadow:0 0 50px {G}aa">+ 3 %</div><div style="font-weight:700;font-size:44px;color:#e5e7eb">rund 790–800 €</div>', 380, 420)
      + txt("Analysten hatten die Kürzung schon erwartet<br>(Schätzung vorher: rund 36,8 Mrd. €)", 850, 42, "#e5e7eb") + pfeil(1180, 150)
      + quelle("Quelle: investing.com, cash-online · Kurs schwankt im Tagesverlauf"))
s5 = (kopf(D, f"5 / {N}") + f'<img src="{s34.BEAGLE}" style="position:absolute;left:340px;top:270px;width:400px;height:400px;border-radius:50%;border:10px solid {O};box-shadow:0 0 50px {O}88;z-index:5"/>'
      + txt('HundeFinanz<span style="color:#f28a1e">Tv</span>', 700, 84) + pille("+ Folgen", 850, O, 64) + pille("Speichern · Teilen", 990, "#1d2330", 54)
      + txt("Jeden Tag neue Geld-News", 1110, 48, "#e5e7eb") + quelle("Keine Anlageberatung, nur eine Erklärung."))
for i, s in enumerate([s1, s2, s3, s4, s5], 1):
    s34.speichern(s, f"{OUT}{i:02d}.jpg")
print("fertig")
