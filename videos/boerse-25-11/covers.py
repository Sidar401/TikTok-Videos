import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/boerse-25-11-"
FALL = [(0.0, 0.05), (0.15, 0.2), (0.3, 0.1), (0.5, 0.45), (0.65, 0.35), (0.82, 0.8), (0.9, 0.65), (1.0, 0.98)]
# A: Dax -1,3 % + Kurve
cd.speichern(cd.BG + cd.kopf([("DAX STÜRZT", None), ("AB!", R)], y=270, gr=118)
  + cd.kurve(110, 560, 860, 420, FALL)
  + f'<div style="position:absolute;left:0;top:1050px;width:1080px;text-align:center;font-weight:900;font-size:300px;line-height:1;color:{R};text-shadow:0 0 80px {R}bb;z-index:5">−1,3 %</div>'
  + cd.pille(1520, "TIEFSTER STAND SEIT JULI"), OUT + "tiktok.jpg")
# B: KI-Flucht, Infineon / VW
cd.speichern(cd.BG + cd.kopf([("FLUCHT AUS", None), ("KI-AKTIEN!", O)], y=270, gr=118)
  + cd.neon(640, "Infineon −6,5 %", R, 100) + cd.neon(790, "Nvidia −8 %", R, 100)
  + cd.neon(1030, "VW +4,5 %", G, 100) + cd.neon(1180, "BMW +3,5 %", G, 100)
  + cd.pille(1520, "BÖRSE 25.11."), OUT + "B.jpg")
