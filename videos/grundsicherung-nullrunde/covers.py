import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
L = "file:///home/user/tiktok-videos/brand/logos/"
OUT = "/home/user/tiktok-videos/renders/thumbnails/grundsicherung-nullrunde-"
# A: NULLRUNDE + 563 €
cd.speichern(cd.BG + cd.kopf([("NULLRUNDE", R), ("BIS MITTE 2028", None)], y=270, gr=118)
  + f'<div style="position:absolute;left:0;top:700px;width:1080px;text-align:center;font-weight:900;font-size:300px;line-height:1;color:#fff;text-shadow:0 0 70px #ffffff66;z-index:5">563 €</div>'
  + cd.neon(1070, "kein Cent mehr", R, 110) + cd.pille(1520, "GRUNDSICHERUNG"), OUT + "tiktok.jpg")
# B: Flagge + eingefroren
cd.speichern(cd.BG + cd.kopf([("REGELSATZ", None), ("EINGEFROREN!", O)], y=270, gr=118)
  + f'<div style="position:absolute;left:290px;top:660px;width:500px;z-index:4;border-radius:14px;overflow:hidden;box-shadow:0 0 50px #000c,0 0 0 8px #fff;transform:rotate(-4deg)"><img src="{L}flagge-deutschland.svg" style="width:100%;display:block"/></div>'
  + cd.neon(1120, "bis Juli 2028", R, 120) + cd.pille(1520, "JETZT BESCHLOSSEN"), OUT + "B.jpg")
