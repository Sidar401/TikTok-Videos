#!/usr/bin/env python3
"""Slideshow „2027 wird teurer“ (Test, 26.11.2026, 9:16, heller News-Look). Zahlen: Deutsche Post (Pressemitteilung 2026), BMG 30.10.2026,
Bundesregierung/DRV Kabinettsbeschluss 7.10.2026 (SV-Rechengrößen 2027)."""
import os
import sys
sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch  # noqa: E402

G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
OUT = "/home/user/tiktok-videos/renders/slides/2027-teurer/"
BEAGLE = "file:///home/user/tiktok-videos/videos/boerse-25-11/assets/beagle.png"
POST = ch.L + "deutsche-post.svg"
HAS_POST = os.path.exists(ch.L + "deutsche-post.svg") and b"<svg" in open(ch.L + "deutsche-post.svg", "rb").read(400)


def kopf(nr, n=7):
    return (f'<div style="position:absolute;left:0;top:150px;width:1080px;height:120px;background:linear-gradient(90deg,#fbe9e9,#fdf6e3);border-bottom:2px solid #e4e6ea;'
            f'display:flex;align-items:center;padding:0 64px 0 50px;gap:18px;z-index:8"><img src="{BEAGLE}" style="width:86px;height:86px;border-radius:50%;border:3px solid #fff;box-shadow:0 4px 10px #0002"/>'
            f'<div style="font-weight:700;font-size:40px;color:{D}">HundeFinanzTv</div>'
            f'<div style="margin-left:auto;font-size:34px;color:{D};font-weight:800;white-space:nowrap">{nr}<span style="font-weight:500;color:#555c66"> / {n}</span></div></div>')


def txt(t, y, gr, farbe=D, w=1080, extra=""):
    return f'<div style="position:absolute;left:0;top:{y}px;width:{w}px;text-align:center;font-weight:900;font-size:{gr}px;line-height:1.08;color:{farbe};z-index:5;{extra}">{t}</div>'


def pille(t, y, farbe=O, gr=50, schrift="#fff"):
    return (f'<div style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5"><span style="padding:16px 46px;border-radius:60px;'
            f'background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 12px 26px #0000002a;white-space:nowrap">{t}</span></div>')


def karte(inhalt, y, h, x=70, w=940):
    return f'<div class="karte" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:center">{inhalt}</div>'


def von_nach(a, b, einheit, gr=120):
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:30px;font-weight:900;white-space:nowrap">'
            f'<span style="font-size:{gr}px;color:#8a919c;text-decoration:line-through;text-decoration-thickness:8px">{a}</span><span style="font-size:{gr * 0.7:.0f}px;color:{D}">→</span>'
            f'<span style="font-size:{gr}px;color:{R}">{b}</span></div><div style="font-weight:700;font-size:44px;color:#3a414c;margin-top:14px">{einheit}</div>')


def quelle(t):
    return f'<div style="position:absolute;left:60px;width:960px;top:1700px;text-align:center;font-weight:600;font-size:32px;color:#555c66;z-index:5">{t}</div>'


def wisch():
    return pille("Weiter wischen →", 1560, D, 46)


# 1 Hook
s1 = (kopf(1) + txt("Ab Januar 2027", 330, 84, D) + txt("wird vieles", 430, 120, D) + txt("TEURER", 570, 250, R, extra="text-shadow:0 10px 30px #d23c3c33")
      + karte("".join(f'<div style="display:flex;width:100%;align-items:center;gap:22px;font-weight:800;font-size:46px;color:{D};padding:15px 0"><span style="color:{O}">{i}</span>{t}</div>'
                      for i, t in [("1", "Briefporto"), ("2", "Krankenkasse"), ("3", "Beitragsgrenze Kranken"), ("4", "Beitragsgrenze Rente")]), 900, 560)
      + wisch() + quelle("Stand 26.11.2026 · geprüfte Zahlen"))
# 2 Porto
s2 = (kopf(2) + txt("1 · Briefporto", 330, 100, O)
      + karte((f'<img src="file://{POST}" style="height:120px;margin-bottom:34px"/>' if HAS_POST else "") + von_nach("0,95 €", "1,15 €", "Standardbrief", 118), 560, 620)
      + pille("+ 21 %", 1240, R, 80) + txt("geplant ab 1. Januar 2027<br>Bundesnetzagentur muss noch zustimmen", 1380, 44, "#3a414c")
      + wisch() + quelle("Quelle: Deutsche Post, Bundesnetzagentur · +21 % = eigene Rechnung"))
# 3 Zusatzbeitrag
s3 = (kopf(3) + txt("2 · Krankenkasse", 330, 100, O)
      + karte(f'<div style="font-weight:700;font-size:46px;color:#3a414c">Ø Zusatzbeitrag 2027</div><div style="font-weight:900;font-size:230px;color:{D};line-height:1.1">2,9 %</div>'
              f'<div style="font-weight:800;font-size:54px;color:{G}">bleibt wie 2026</div>', 560, 560)
      + txt("Aber: Deine Kasse kann<br>trotzdem mehr verlangen.", 1190, 56, D)
      + pille("Dann darfst du wechseln", 1420, O, 52) + wisch() + quelle("Quelle: Bundesgesundheitsministerium, 30.10.2026"))
# 4 Beitragsgrenze KV
s4 = (kopf(4) + txt("3 · Krankenversicherung", 330, 66, O)
      + karte(von_nach("5.812,50 €", "6.375 €", "Beitragsgrenze pro Monat", 72), 540, 520)
      + txt("Bis zu diesem Gehalt zahlst du<br>Beiträge. Alles darüber ist frei.", 1130, 50, D)
      + pille("Trifft Gutverdiener", 1390, R, 54) + wisch() + quelle("Quelle: Bundesregierung, Kabinett 7.10.2026 · Bundesrat steht noch aus"))
# 5 Beispiel
s5 = (kopf(5) + txt("Was heißt das?", 330, 110, O)
      + karte(f'<div style="font-weight:700;font-size:46px;color:#3a414c">Bei 6.375 € brutto und mehr</div><div style="font-weight:900;font-size:200px;color:{R};line-height:1.1">+ 49 €</div>'
              f'<div style="font-weight:800;font-size:54px;color:{D}">im Monat für dich</div>', 520, 600)
      + txt("nur Krankenversicherung,<br>Anteil Arbeitnehmer", 1190, 50, "#3a414c") + wisch()
      + quelle("Eigene Rechnung: 562,50 € × 8,75 % (14,6 % + 2,9 % Zusatz, geteilt)"))
# 6 Rente
s6 = (kopf(6) + txt("4 · Rentenversicherung", 330, 70, O)
      + karte(von_nach("8.450 €", "8.850 €", "Beitragsgrenze pro Monat", 92), 540, 520)
      + txt("Wer mehr verdient,<br>zahlt auf mehr Gehalt Beiträge.", 1130, 52, D)
      + pille("+ 400 € mehr Grenze", 1390, R, 54) + wisch() + quelle("Quelle: Deutsche Rentenversicherung, Kabinett 7.10.2026"))
# 7 CTA
s7 = (kopf(7) + f'<img src="{BEAGLE}" style="position:absolute;left:290px;top:340px;width:500px;height:500px;border-radius:50%;border:12px solid {O};box-shadow:0 20px 50px #0003;z-index:5"/>'
      + txt('HundeFinanz<span style="color:#f28a1e">Tv</span>', 900, 100, D) + pille("+ Folgen", 1090, O, 70) + pille("Speichern · Teilen", 1250, D, 60)
      + txt("Jeden Tag neue Geld-Tipps", 1430, 56, D) + quelle("Keine Anlageberatung, nur eine Erklärung."))

for i, s in enumerate([s1, s2, s3, s4, s5, s6, s7], 1):
    ch.speichern(s, f"{OUT}{i:02d}.jpg")
print("fertig", HAS_POST)
