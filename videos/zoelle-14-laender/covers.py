import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
L = "file:///home/user/tiktok-videos/brand/logos/"
OUT = "/home/user/tiktok-videos/renders/thumbnails/zoelle-14-laender-"


def flag(datei, x, y, w, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:4;border-radius:14px;overflow:hidden;box-shadow:0 0 50px #000c,0 0 0 8px #ffffff">'
            f'<img src="{L}{datei}" style="width:100%;display:block"/></div>')


# A: NEUE ZÖLLE – 14 LÄNDER
cd.speichern(cd.BG + cd.kopf([("NEUE ZÖLLE", R), ("AUF 14 LÄNDER!", None)], y=270, gr=112)
  + flag("flagge-usa.svg", 90, 700, 380, -6) + flag("flagge-china.svg", 610, 700, 380, 6)
  + cd.neon(1000, "China: 20 %", R, 110) + cd.neon(1160, "EU: 15 %", R, 110) + cd.pille(1520, "AUCH EUROPA IM VISIER"), OUT + "tiktok.jpg")
# B: EU 15 %
cd.speichern(cd.BG + cd.kopf([("TRUMP-ZÖLLE", None), ("AUF EUROPA?", O)], y=270, gr=116)
  + flag("flagge-eu.svg", 290, 650, 500, 0)
  + f'<div style="position:absolute;left:0;top:1030px;width:1080px;text-align:center;font-weight:900;font-size:300px;line-height:1;color:{R};text-shadow:0 0 80px {R}bb;z-index:5">15 %</div>'
  + cd.pille(1520, "NOCH NICHT IN KRAFT"), OUT + "B.jpg")
