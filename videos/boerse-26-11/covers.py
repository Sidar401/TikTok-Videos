import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/boerse-26-11-"
UP = [(0.0, 0.95), (0.2, 0.8), (0.35, 0.86), (0.55, 0.55), (0.7, 0.62), (0.85, 0.3), (1.0, 0.06)]
# A: Dax erholt sich
cd.speichern(cd.BG_GRUEN + cd.kopf([("DAX ERHOLT", None), ("SICH!", G)], y=270, gr=124)
  + cd.kurve(110, 560, 860, 420, UP, farbe=G, hell="#6ee7a0")
  + f'<div style="position:absolute;left:0;top:1060px;width:1080px;text-align:center;font-weight:900;font-size:300px;line-height:1;color:{G};text-shadow:0 0 80px {G}bb;z-index:5">+2,1 %</div>'
  + cd.pille(1520, "GESTERN: TIEFSTSTAND SEIT JULI"), OUT + "tiktok.jpg")
# B: Gewinner
cd.speichern(cd.BG_GRUEN + cd.kopf([("DIE GEWINNER", None), ("DES TAGES", G)], y=270, gr=118)
  + cd.neon(640, "Rheinmetall ≈ +4 %", G, 84) + cd.neon(790, "Siemens Energy +4 %", G, 84) + cd.neon(940, "Infineon +3,6 %", G, 84)
  + cd.coin(340, 1120, 400, zeichen="▲") + cd.pille(1520, "BÖRSE 26.11."), OUT + "B.jpg")
