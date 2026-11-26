#!/usr/bin/env python3
"""Slideshow „2027 wird teurer“ DUNKEL (26.11.2026, 9:16). thumbnail.jpg = Titelbild mit Pfeil, zählt NICHT mit; Bilder 01–06 = 1/6–6/6."""
import os
import sys
sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import slide_dark as sd  # noqa: E402

R, O, G = sd.ROT, sd.O, sd.G
OUT = "/home/user/tiktok-videos/renders/slides/2027-teurer-dunkel/"
POSTF = sd.L + "deutsche-post.svg"
HAS_POST = os.path.exists(POSTF) and b"<svg" in open(POSTF, "rb").read(400)
D = "26.11.2026"
W = lambda: sd.pfeil(1540)  # noqa: E731


def liste(zeilen):
    return "".join(f'<div style="display:flex;width:100%;align-items:center;gap:22px;font-weight:800;font-size:46px;padding:14px 0"><span style="color:{O}">{i}</span>{t}</div>' for i, t in zeilen)


s1 = (sd.kopf(D) + sd.txt("Ab Januar 2027", 600, 90) + sd.txt("wird vieles", 710, 130) + sd.txt("TEURER", 860, 230, R) + sd.pfeil(1250, 260))
s2 = (sd.kopf(D, nr="1 / 6") + sd.txt("1 · Briefporto", 540, 100, O)
      + sd.glas((f'<img src="file://{POSTF}" style="height:110px;margin-bottom:26px"/>' if HAS_POST else "") + sd.von_nach("0,95 €", "1,15 €", "Standardbrief", 118), 700, 420)
      + sd.pille("+ 21 %", 1190, R, 80) + sd.txt("geplant ab 1. Januar 2027<br>Bundesnetzagentur muss noch zustimmen", 1330, 44, "#e5e7eb")
      + W() + sd.quelle("Quelle: Deutsche Post, Bundesnetzagentur · +21 % = eigene Rechnung"))
s3 = (sd.kopf(D, nr="2 / 6") + sd.txt("2 · Krankenkasse", 540, 100, O)
      + sd.glas('<div style="font-weight:700;font-size:46px;color:#cbd5e1">Ø Zusatzbeitrag 2027</div>'
                f'<div style="font-weight:900;font-size:220px;line-height:1.1;text-shadow:0 0 40px #fff4">2,9 %</div><div style="font-weight:800;font-size:54px;color:{G}">bleibt wie 2026</div>', 700, 520)
      + sd.txt("Aber: Deine Kasse kann<br>trotzdem mehr verlangen.", 1260, 54) + sd.pille("Dann darfst du wechseln", 1440, O, 50)
      + W() + sd.quelle("Quelle: Bundesgesundheitsministerium, 30.10.2026"))
s4 = (sd.kopf(D, nr="3 / 6") + sd.txt("3 · Krankenversicherung", 540, 70, O)
      + sd.glas(sd.von_nach("5.812,50 €", "6.375 €", "Beitragsgrenze pro Monat", 72), 680, 400)
      + sd.txt("Bis zu diesem Gehalt zahlst du<br>Beiträge. Alles darüber ist frei.", 1150, 48) + sd.pille("Trifft Gutverdiener", 1370, R, 54)
      + W() + sd.quelle("Quelle: Bundesregierung, Kabinett 7.10.2026 · Bundesrat steht noch aus"))
s5 = (sd.kopf(D, nr="4 / 6") + sd.txt("Was heißt das?", 540, 110, O)
      + sd.glas('<div style="font-weight:700;font-size:46px;color:#cbd5e1">Bei 6.375 € brutto und mehr</div>'
                f'<div style="font-weight:900;font-size:190px;line-height:1.1;color:{R};text-shadow:0 0 50px {R}aa">+ 49 €</div><div style="font-weight:800;font-size:54px">im Monat für dich</div>', 700, 520)
      + sd.txt("nur Krankenversicherung,<br>Anteil Arbeitnehmer", 1260, 50, "#e5e7eb") + W()
      + sd.quelle("Eigene Rechnung: 562,50 € × 8,75 % (14,6 % + 2,9 % Zusatz, geteilt)"))
s6 = (sd.kopf(D, nr="5 / 6") + sd.txt("4 · Rentenversicherung", 540, 70, O)
      + sd.glas(sd.von_nach("8.450 €", "8.850 €", "Beitragsgrenze pro Monat", 92), 680, 400)
      + sd.txt("Wer mehr verdient, zahlt auf<br>mehr Gehalt Rentenbeiträge.", 1150, 48) + sd.pille("+ 400 € mehr Grenze", 1370, R, 54)
      + W() + sd.quelle("Quelle: Deutsche Rentenversicherung, Kabinett 7.10.2026"))
s7 = (sd.kopf(D, nr="6 / 6") + sd.txt('HundeFinanz<span style="color:#f28a1e">Tv</span>', 600, 100)
      + sd.pille("+ Folgen", 800, O, 70) + sd.pille("Speichern · Teilen", 960, "#1d2330", 60) + sd.txt("Jeden Tag neue Geld-Tipps", 1150, 56)
      + sd.glas('<div style="font-weight:700;font-size:40px;text-align:center;line-height:1.3">Merk dir:<br>Mehr Beiträge, weniger Netto.</div>', 1300, 220)
      + sd.quelle("Keine Anlageberatung, nur eine Erklärung."))
sd.speichern(s1, OUT + "thumbnail.jpg")
for i, s in enumerate([s2, s3, s4, s5, s6, s7], 1):
    sd.speichern(s, f"{OUT}{i:02d}.jpg")
print("fertig, Post-Logo:", HAS_POST)
