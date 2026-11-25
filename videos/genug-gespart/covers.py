import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/genug-gespart-"


def m(d):
    return (1080 - d) // 2


# A: Münze + 120.000 €
cd.speichern(cd.BG + cd.kopf([("MIT 40 SOLLTEST", None), ("DU SO VIEL", None), ("GESPART HABEN?", O)], y=270, gr=104)
  + cd.coin(m(450), 640, 450, zeichen="€") + cd.schild(30, 700, "3 JAHRESGEHÄLTER", G, -5, 50)
  + cd.neon(1150, "≈ 120.000 €", G, 150) + cd.pille(1520, "FAUSTREGEL NACH ALTER"), OUT + "tiktok.jpg")
# B: Treppe
stufen = ""
for i, (alter, mal) in enumerate((("30", "1×"), ("40", "3×"), ("50", "6×"), ("60", "8×"), ("67", "10×"))):
    h = [90, 170, 280, 360, 450][i]
    farbe = [("#8a93a1"), G, G, O, R][i]
    stufen += (f'<div style="position:absolute;left:{70 + i * 190}px;top:{1100 - h}px;width:170px;height:{h}px;background:linear-gradient(180deg,{farbe},{farbe}99);border-radius:14px 14px 0 0;z-index:4;'
               f'box-shadow:0 0 40px {farbe}88;text-align:center"><div style="font-weight:900;font-size:56px;color:#fff;padding-top:12px">{mal}</div></div>'
               f'<div style="position:absolute;left:{70 + i * 190}px;top:1115px;width:170px;text-align:center;font-weight:900;font-size:58px;color:#cbd5e1;z-index:4">{alter}</div>')
cd.speichern(cd.BG_GRUEN + cd.kopf([("HAST DU", None), ("GENUG", None), ("GESPART?", G)], y=270, gr=118) + stufen
  + cd.neon(1230, "Jahresgehälter", "#fff", 80) + cd.pille(1520, "ALTER · FAUSTREGEL"), OUT + "B.jpg")
# C: Riesige 3×
cd.speichern(cd.BG + cd.kopf([("MIT 40", None), ("HABEN?", None)], y=270, gr=130)
  + f'<div style="position:absolute;left:0;top:560px;width:1080px;text-align:center;font-weight:900;font-size:420px;line-height:1;color:{G};text-shadow:0 0 90px {G}bb;z-index:5">3×</div>'
  + cd.neon(1060, "JAHRESGEHALT", "#fff", 100) + cd.schild(330, 1230, "GESPART?", O, 0, 74) + cd.pille(1520, "HAST DU DAS?"), OUT + "C.jpg")
