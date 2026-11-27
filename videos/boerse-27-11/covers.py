import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
L = "file:///home/user/tiktok-videos/brand/logos/"
OUT = "/home/user/tiktok-videos/renders/thumbnails/boerse-27-11-"
UP = [(0.0, 0.95), (0.2, 0.8), (0.35, 0.86), (0.55, 0.55), (0.7, 0.62), (0.85, 0.3), (1.0, 0.06)]


def chip(datei, x, y, w=420, h=150):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:22px;box-shadow:0 0 50px #000c;z-index:4;'
            f'display:flex;align-items:center;justify-content:center"><img src="{L}{datei}" style="max-width:80%;max-height:68%"/></div>')


def wert(text, x, y, w=420):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:150px;display:flex;align-items:center;font-weight:900;font-size:86px;color:{G};'
            f'text-shadow:0 0 50px {G}99;z-index:5;white-space:nowrap">{text}</div>')


# A: starke Woche
cd.speichern(cd.BG_GRUEN + cd.kopf([("DAX BEENDET", None), ("STARKE WOCHE", G)], y=270, gr=112)
  + cd.kurve(110, 560, 860, 420, UP, farbe=G, hell="#6ee7a0")
  + f'<div style="position:absolute;left:0;top:1060px;width:1080px;text-align:center;font-weight:900;font-size:280px;line-height:1;color:{G};text-shadow:0 0 80px {G}bb;z-index:5">+2,6 %</div>'
  + cd.pille(1520, "BÖRSENRÜCKBLICK 27.11."), OUT + "tiktok.jpg")
# B: Gewinner mit Logos
cd.speichern(cd.BG_GRUEN + cd.kopf([("DIE GEWINNER", None), ("DES TAGES", G)], y=270, gr=118)
  + chip("rheinmetall.svg", 90, 640) + wert("+3,3 %", 560, 640)
  + chip("siemens-energy.svg", 90, 840) + wert("bis +2,7 %", 560, 840)
  + chip("infineon.svg", 90, 1040) + wert("bis +2,7 %", 560, 1040)
  + cd.pille(1520, "BÖRSE 27.11."), OUT + "B.jpg")
