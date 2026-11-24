import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/"
B = "/home/user/tiktok-videos/brand/"
FALL = [(0.0, 0.05), (0.18, 0.15), (0.3, 0.02), (0.5, 0.4), (0.62, 0.3), (0.82, 0.8), (0.9, 0.62), (1.0, 0.98)]
STEIG = [(0.0, 0.95), (0.2, 0.75), (0.32, 0.85), (0.52, 0.45), (0.66, 0.55), (0.84, 0.15), (1.0, 0.02)]

# 1) Rente 2027
cd.speichern(cd.BG_GRUEN + cd.kopf([("RENTE STEIGT:", None), ("+4,09 %", G)], gr=124)
  + cd.coin(215, 520, 650, zeichen="€") + cd.kurve(60, 540, 960, 640, STEIG, farbe=G, hell="#6ee7a0")
  + cd.schild(540, 1150, "BEITRAG 19,8 % ▲", R, 4, 44) + cd.schild(40, 1150, "≈ +61 € bei 1.500 €", G, -4, 44)
  + cd.neon(1290, "DU ZAHLST MEHR?", R, 88, "RENTENBEITRAG AB 2028") + cd.pille(1650, "AB JULI 2027"), OUT + "rente-2027-plus-tiktok.jpg")

# 2) Top 1 %
punkte = "".join(f'<div style="width:50px;height:50px;border-radius:50%;background:{"radial-gradient(circle at 35% 30%,#fff3b0,#f7c948 40%,#8a5a00)" if i == 0 else "#222733"};'
                 f'{"box-shadow:0 0 50px #f7c948;transform:scale(1.35)" if i == 0 else "border:2px solid #343b4d"}"></div>' for i in range(100))
cd.speichern(cd.BG + cd.kopf([("AB WIE VIEL", None), ("GEHÖRST DU", None), ("ZU DEN TOP 1 %?", O)], gr=112)
  + f'<div style="position:absolute;left:100px;top:600px;width:880px;display:grid;grid-template-columns:repeat(10,1fr);gap:12px;justify-items:center;z-index:3">{punkte}</div>'
  + cd.neon(1290, "ab 2,3 Mio. €", G, 150, "VERMÖGEN PRO HAUSHALT") + cd.pille(1650, "REICH IN DEUTSCHLAND"), OUT + "top-ein-prozent-tiktok.jpg")

# 3) KI-Serie Teil 3 Roboter
cd.speichern(cd.BG + cd.kopf([("ROBOTER:", None), ("HYPE ODER", None), ("GELD?", O)], gr=124)
  + cd.zahnrad(215, 560, 650) + cd.schild(40, 640, "603.000 in Fabriken", G, -5, 54) + cd.schild(430, 1060, "≈ 7.000 Menschen-Roboter", R, 4, 40)
  + cd.neon(1290, "2,5 Mrd. $", G, 150, "BÖRSENGANG GEPLANT") + cd.pille(1650, "KI-SERIE · TEIL 3"), OUT + "ki-teil3-tiktok.jpg")

# 4) Nvidia: Huang zurück
foto = (f'<div style="position:absolute;left:230px;top:520px;width:620px;height:620px;border-radius:50%;overflow:hidden;border:14px solid {G};box-shadow:0 0 90px {G}88,0 40px 90px #000c;z-index:3">'
        f'<img src="file://{B}fotos/jensen-huang.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 18%"/></div>')
cd.speichern(cd.BG_GRUEN + cd.kopf([("HUANG IST", None), ("ZURÜCK!", G)], gr=140) + foto
  + f'<div style="position:absolute;left:40px;top:1020px;z-index:6;transform:rotate(-6deg);padding:14px 30px;background:#fff;border-radius:16px;box-shadow:0 16px 40px #000a"><img src="file://{B}logos/nvidia.svg" style="height:70px;display:block"/></div>'
  + cd.neon(1230, "+30 %", G, 230, "NVIDIA-AKTIE VORBÖRSLICH") + cd.pille(1650, "NACH 11 TAGEN"), OUT + "nvidia-huang-zurueck-tiktok.jpg")
