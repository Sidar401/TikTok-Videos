import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/gas-strom-2027-"
HOCH = [(0.0, 0.95), (0.2, 0.8), (0.32, 0.88), (0.52, 0.5), (0.66, 0.6), (0.84, 0.2), (1.0, 0.04)]


def m(d):
    return (1080 - d) // 2


# A: Flamme + Preis-Kurve
cd.speichern(cd.BG + cd.kopf([("GAS WIRD", None), ("14 % TEURER!", R)], y=270, gr=124)
  + cd.coin(m(470), 650, 470, zeichen="🔥") + cd.kurve(110, 640, 860, 520, HOCH, farbe=R, hell="#ff6b6b")
  + cd.neon(1200, "≈ +280 €", R, 160) + cd.pille(1520, "DU DARFST KÜNDIGEN"), OUT + "tiktok.jpg")
# B: Kündigen
cd.speichern(cd.BG_GRUEN + cd.kopf([("DU DARFST", None), ("KÜNDIGEN!", G)], y=270, gr=134)
  + cd.coin(m(470), 650, 470, zeichen="✂️") + cd.schild(40, 700, "GAS ▲ 14 %", R, -6, 60) + cd.schild(600, 1010, "STROM ▲ 8 %", R, 6, 56)
  + cd.neon(1200, "Frist beachten!", O, 100) + cd.pille(1520, "AB 1. JANUAR 2027"), OUT + "B.jpg")
# C: Zahlen-Duell
cd.speichern(cd.BG + cd.kopf([("ENERGIE", None), ("WIRD TEURER", R)], y=270, gr=124)
  + f'<div style="position:absolute;left:60px;top:600px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:230px;line-height:1;color:{R};text-shadow:0 0 60px {R}aa;white-space:nowrap">+14 %</div>'
    f'<div style="font-weight:900;font-size:70px;color:#fff;letter-spacing:3px">GAS</div></div>'
  + f'<div style="position:absolute;left:60px;top:1010px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:230px;line-height:1;color:{O};text-shadow:0 0 60px {O}aa;white-space:nowrap">+8 %</div>'
    f'<div style="font-weight:900;font-size:70px;color:#fff;letter-spacing:3px">STROM</div></div>'
  + cd.pille(1520, "SONDERKÜNDIGUNG MÖGLICH"), OUT + "C.jpg")
