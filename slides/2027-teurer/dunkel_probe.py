import sys
sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import slide_dark as sd
import cover_dark as cd
OUT = "/home/user/tiktok-videos/renders/slides/2027-teurer-dunkel/"
R, O, G = sd.ROT, sd.O, sd.G
# Slide 1: Hook
s1 = (sd.kopf("26.11.2026", nr="1 / 7") + sd.txt("Ab Januar 2027", 560, 84) + sd.txt("wird vieles", 660, 120)
      + sd.txt("TEURER", 800, 215, R)
      + sd.glas("".join(f'<div style="display:flex;width:100%;align-items:center;gap:22px;font-weight:800;font-size:46px;padding:14px 0"><span style="color:{O}">{i}</span>{t}</div>'
                        for i, t in [("1", "Briefporto"), ("2", "Krankenkasse"), ("3", "Beitragsgrenze Kranken"), ("4", "Beitragsgrenze Rente")]), 1120, 400)
      + sd.pille("Weiter wischen →", 1560, O, 46) + sd.quelle("Stand 26.11.2026 · geprüfte Zahlen"))
sd.speichern(s1, OUT + "01.jpg")
# Slide 2: Porto
s2 = (sd.kopf("26.11.2026", nr="2 / 7") + sd.txt("1 · Briefporto", 540, 100, O)
      + sd.glas(sd.von_nach("0,95 €", "1,15 €", "Standardbrief", 118), 700, 420)
      + sd.pille("+ 21 %", 1190, R, 80) + sd.txt("geplant ab 1. Januar 2027<br>Bundesnetzagentur muss noch zustimmen", 1330, 44, "#e5e7eb")
      + sd.pille("Weiter wischen →", 1560, "#1d2330", 46) + sd.quelle("Quelle: Deutsche Post, Bundesnetzagentur · +21 % = eigene Rechnung"))
sd.speichern(s2, OUT + "02.jpg")
# Cover (Profil-Raster, schwarzer Stil, sichere Zone)
FALL = [(0.0, 0.9), (0.2, 0.75), (0.4, 0.7), (0.6, 0.45), (0.8, 0.3), (1.0, 0.05)]
cd.speichern(cd.BG + cd.kopf([("2027 WIRD", None), ("TEURER!", R)], y=270, gr=124)
             + cd.schild(60, 650, "Porto +21 %", R, -5, 64) + cd.schild(330, 880, "Krankenkasse ▲", R, 4, 64) + cd.schild(80, 1110, "Rente-Grenze ▲", R, -4, 64)
             + cd.coin(590, 1090, 400, zeichen="€") + cd.pille(1520, "4 DINGE ZUM JAHRESSTART"), OUT + "cover.jpg")
