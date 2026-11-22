import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
ch.R = ch.L.rsplit("brand", 1)[0]
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
L = "/home/user/tiktok-videos/brand/logos/"
def kachel(x, y, logo, wert, farbe, dreh):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:400px;padding:30px 0 24px;background:#fff;border:2px solid #e2e5ea;border-radius:14px;box-shadow:0 16px 34px #0002;text-align:center;transform:rotate({dreh}deg)">'
            f'<img src="file://{L}{logo}" style="max-width:260px;height:70px;object-fit:contain"/>'
            f'<div style="font-weight:900;font-size:92px;color:{farbe};margin-top:8px">{wert}</div></div>')
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:112px;color:{D};line-height:1.05">Wer verdient<br/>an <span style="color:{O}">KI</span>?</div>'
  + kachel(90, 520, "palantir.svg", "+96 %", G, -3) + kachel(590, 540, "meta.png", "+26 %", G, 3)
  + kachel(90, 900, "microsoft.svg", "30 Mio.", O, 2) + kachel(590, 920, "thomsonreuters.svg", "−16 %", R, -2)
  + f'<div style="position:absolute;top:1330px;width:1080px;display:flex;justify-content:center"><span style="padding:22px 64px;border-radius:70px;background:{O};color:#fff;font-weight:900;font-size:70px">KI-SERIE · TEIL 1</span></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/ki-teil1-tiktok.jpg")
