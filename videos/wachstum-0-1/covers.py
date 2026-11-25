import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/wachstum-0-1-"
FALL = [(0.0, 0.05), (0.18, 0.15), (0.3, 0.02), (0.5, 0.4), (0.62, 0.3), (0.82, 0.8), (0.9, 0.62), (1.0, 0.98)]


def m(d):
    return (1080 - d) // 2


# A: riesige 0,1 % + Absturzkurve
cd.speichern(cd.BG + cd.kopf([("DEUTSCHLAND", None), ("WÄCHST NUR NOCH", None)], y=270, gr=84)
  + cd.kurve(110, 560, 860, 520, FALL)
  + f'<div style="position:absolute;left:0;top:1100px;width:1080px;text-align:center;font-weight:900;font-size:300px;line-height:1;color:{R};text-shadow:0 0 80px {R}bb;z-index:5">0,1 %</div>'
  + cd.pille(1520, "3. QUARTAL 2026"), OUT + "tiktok.jpg")
# B: Einkaufswagen
cd.speichern(cd.BG + cd.kopf([("WIR SPAREN", None), ("BEIM ESSEN!", O)], y=270, gr=124)
  + cd.coin(m(470), 640, 470, zeichen="🛒") + cd.schild(30, 700, "Essen ▼", R, -6, 60) + cd.schild(640, 1010, "Sprit ▼", R, 6, 60)
  + cd.neon(1200, "Wirtschaft: +0,1 %", R, 96) + cd.pille(1520, "NEUE ZAHLEN"), OUT + "B.jpg")
# C: Zahlen
cd.speichern(cd.BG + cd.kopf([("WARUM SO", None), ("SCHWACH?", R)], y=270, gr=124)
  + f'<div style="position:absolute;left:60px;top:600px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:220px;line-height:1;color:{R};text-shadow:0 0 60px {R}aa;white-space:nowrap">−3,5 %</div>'
    f'<div style="font-weight:900;font-size:64px;color:#fff;letter-spacing:3px">INVESTITIONEN</div></div>'
  + f'<div style="position:absolute;left:60px;top:1010px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:220px;line-height:1;color:{O};text-shadow:0 0 60px {O}aa;white-space:nowrap">−1 %</div>'
    f'<div style="font-weight:900;font-size:64px;color:#fff;letter-spacing:3px">EXPORTE</div></div>'
  + cd.pille(1520, "DEUTSCHLAND · 3. QUARTAL"), OUT + "C.jpg")
