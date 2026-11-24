"""Covers mit SICHERER ZONE (Nutzer 24.11.: Instagram/TikTok schneiden im Profil-Raster oben/unten ab, 3:4-Ausschnitt).
Alles Wichtige zwischen y = 250 und y = 1670; Schrift groß, keine Kleinsttexte."""
import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_dark as cd
G, R, O = cd.G, cd.R, cd.O
OUT = "/home/user/tiktok-videos/renders/thumbnails/"
B = "/home/user/tiktok-videos/brand/"
FALL = [(0.0, 0.05), (0.18, 0.15), (0.3, 0.02), (0.5, 0.4), (0.62, 0.3), (0.82, 0.8), (0.9, 0.62), (1.0, 0.98)]
STEIG = [(0.0, 0.95), (0.2, 0.75), (0.32, 0.85), (0.52, 0.45), (0.66, 0.55), (0.84, 0.15), (1.0, 0.02)]
PILLE_Y = 1520


def mitte(d):
    return (1080 - d) // 2


# ===== Crash: D (Favorit), E, F =====
cd.speichern(cd.BG + cd.kopf([("BÖRSEN-CRASH", None), ("= AMERIKAS", None), ("VORTEIL?", G)], y=270, gr=112)
  + cd.coin(mitte(470), 650, 470) + cd.kurve(110, 640, 860, 520, FALL)
  + cd.neon(1190, "100 Mrd. $", G, 156) + cd.pille(PILLE_Y, "NUR EIN GEDANKENSPIEL"), OUT + "crash-usa-schulden-tiktok.jpg")
cd.speichern(cd.BG + cd.kopf([("WER", None), ("VERDIENT AM", None), ("CRASH?", R)], y=270, gr=124)
  + cd.coin(-110, 700, 520, rot=-10) + cd.schild(440, 760, "DEIN DEPOT ▼", R, 5, 62) + cd.schild(400, 960, "USA ▲ 100 Mrd. $", G, -4, 58)
  + cd.neon(1250, "40,71 Bio. $", "#fff", 130) + cd.pille(PILLE_Y, "NUR EIN GEDANKENSPIEL"), OUT + "crash-usa-schulden-E.jpg")
cd.speichern(cd.BG + cd.kurve(40, 250, 1000, 300, [(0.0, 0.1), (0.2, 0.3), (0.32, 0.05), (0.52, 0.55), (0.66, 0.4), (0.84, 0.95), (1.0, 0.8)], z=2, dick=14)
  + cd.kopf([("DEIN VERLUST.", None), ("IHR GEWINN?", "#f7c948")], y=440, gr=104)
  + cd.coin(mitte(470), 730, 470) + cd.schild(600, 780, "+100 Mrd. $", G, 8, 58) + cd.schild(60, 1090, "CRASH ▼", R, -7, 62)
  + cd.neon(1250, "40,71 Bio. $", "#fff", 120) + cd.pille(PILLE_Y, "NUR EIN GEDANKENSPIEL"), OUT + "crash-usa-schulden-F.jpg")

# ===== Rente =====
cd.speichern(cd.BG_GRUEN + cd.kopf([("RENTE STEIGT:", None), ("+4,09 %", G)], y=270, gr=132)
  + cd.coin(mitte(440), 620, 440, zeichen="€") + cd.kurve(120, 600, 840, 480, STEIG, farbe=G, hell="#6ee7a0")
  + cd.schild(40, 1090, "+61 € bei 1.500 €", G, -4, 50) + cd.schild(520, 1100, "BEITRAG ▲", R, 4, 50)
  + cd.neon(1230, "DU ZAHLST MEHR?", R, 96) + cd.pille(PILLE_Y, "AB JULI 2027"), OUT + "rente-2027-plus-tiktok.jpg")

# ===== Top 1 % =====
punkte = "".join(f'<div style="width:46px;height:46px;border-radius:50%;background:{"radial-gradient(circle at 35% 30%,#fff3b0,#f7c948 40%,#8a5a00)" if i == 0 else "#222733"};'
                 f'{"box-shadow:0 0 50px #f7c948;transform:scale(1.4)" if i == 0 else "border:2px solid #343b4d"}"></div>' for i in range(100))
cd.speichern(cd.BG + cd.kopf([("DU UND DIE", None), ("REICHSTEN", None), ("1 %?", O)], y=270, gr=116)
  + f'<div style="position:absolute;left:150px;top:660px;width:780px;display:grid;grid-template-columns:repeat(10,1fr);gap:10px;justify-items:center;z-index:3">{punkte}</div>'
  + cd.neon(1230, "ab 2,3 Mio. €", G, 140) + cd.pille(PILLE_Y, "REICH IN DEUTSCHLAND"), OUT + "top-ein-prozent-tiktok.jpg")

# ===== KI Teil 3 Roboter =====
cd.speichern(cd.BG + cd.kopf([("ROBOTER:", None), ("HYPE ODER GELD?", O)], y=270, gr=112)
  + cd.zahnrad(mitte(470), 640, 470) + cd.schild(40, 700, "603.000 in Fabriken", G, -5, 50) + cd.schild(380, 1060, "≈ 7.000 Humanoide", R, 4, 50)
  + cd.neon(1230, "2,5 Mrd. $", G, 150) + cd.pille(PILLE_Y, "KI-SERIE · TEIL 3"), OUT + "ki-teil3-tiktok.jpg")

# ===== Nvidia =====
foto = (f'<div style="position:absolute;left:{mitte(480)}px;top:600px;width:480px;height:480px;border-radius:50%;overflow:hidden;border:14px solid {G};box-shadow:0 0 90px {G}88,0 40px 90px #000c;z-index:3">'
        f'<img src="file://{B}fotos/jensen-huang.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 18%"/></div>')
cd.speichern(cd.BG_GRUEN + cd.kopf([("HUANG IST", None), ("ZURÜCK!", G)], y=270, gr=132) + foto
  + f'<div style="position:absolute;left:30px;top:940px;z-index:6;transform:rotate(-6deg);padding:12px 26px;background:#fff;border-radius:16px;box-shadow:0 16px 40px #000a"><img src="file://{B}logos/nvidia.svg" style="height:64px;display:block"/></div>'
  + cd.neon(1110, "+30 %", G, 210) + cd.pille(PILLE_Y, "NACH 11 TAGEN"), OUT + "nvidia-huang-zurueck-tiktok.jpg")
