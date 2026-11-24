import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/"
STEIG = [(0.0, 0.95), (0.2, 0.75), (0.32, 0.85), (0.52, 0.45), (0.66, 0.55), (0.84, 0.15), (1.0, 0.02)]

# ---------- B: Zahlen-Duell ----------
cd.speichern(cd.BG + cd.kopf([("ROBOTER 2025", None)], y=270, gr=124)
  + f'<div style="position:absolute;left:60px;top:470px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:190px;line-height:1;color:{G};text-shadow:0 0 60px {G}aa;white-space:nowrap">603.000</div>'
    f'<div style="font-weight:900;font-size:66px;color:#fff;letter-spacing:3px">IN FABRIKEN</div></div>'
  + f'<div style="position:absolute;left:{(1080-200)//2}px;top:830px;width:200px;height:200px;border-radius:50%;background:{O};color:#fff;font-weight:900;font-size:90px;line-height:200px;text-align:center;z-index:6;box-shadow:0 0 60px {O}99">VS</div>'
  + f'<div style="position:absolute;left:60px;top:1010px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:190px;line-height:1;color:{R};text-shadow:0 0 60px {R}aa;white-space:nowrap">7.000</div>'
    f'<div style="font-weight:900;font-size:66px;color:#fff;letter-spacing:3px">MENSCHEN-ROBOTER</div></div>'
  + cd.pille(1520, "KI-SERIE · TEIL 3"), OUT + "ki-teil3-B.jpg")

# ---------- C: Börsengang / Münze mit Roboter ----------
cd.speichern(cd.BG_GRUEN + cd.kopf([("2,5 MRD. $", G), ("FÜR EINE", None), ("ROBOTER-FIRMA?", None)], y=270, gr=92)
  + cd.coin(190, 660, 700 - 220, zeichen="🤖", farbe="#6b4200") + cd.kurve(100, 640, 880, 520, STEIG, farbe=G, hell="#6ee7a0")
  + cd.schild(480, 1110, "BÖRSENGANG ▲", G, 5, 50) + cd.schild(40, 1150, "GEPLANT", O, -5, 50)
  + cd.pille(1520, "KI-SERIE · TEIL 3"), OUT + "ki-teil3-C.jpg")
