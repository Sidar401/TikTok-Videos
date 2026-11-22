import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
L = "/home/user/tiktok-videos/brand/logos/"
def kachel(x, y, logo, wert, farbe, dreh, w=400):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:30px 0 24px;background:#fff;border:2px solid #e2e5ea;border-radius:14px;box-shadow:0 16px 34px #0002;text-align:center;transform:rotate({dreh}deg)">'
            f'<img src="file://{L}{logo}" style="max-width:280px;height:70px;object-fit:contain"/>'
            f'<div style="font-weight:900;font-size:80px;color:{farbe};margin-top:8px">{wert}</div></div>')
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:108px;color:{D};line-height:1.05">Wer liefert<br/>der <span style="color:{O}">KI</span> alles?</div>'
  + kachel(90, 520, "asml.svg", "+55 %", G, -3) + kachel(590, 540, "micron.svg", "−46 %", R, 3)
  + f'<div class="karte" style="left:190px;top:900px;width:700px;text-align:center;transform:rotate(1deg)"><div style="font-weight:800;font-size:44px;color:{D}">Strom für Rechenzentren</div><div style="font-weight:900;font-size:100px;color:{O}">23 Mrd. kWh</div></div>'
  + f'<div style="position:absolute;top:1290px;width:1080px;display:flex;justify-content:center"><span style="padding:22px 64px;border-radius:70px;background:{O};color:#fff;font-weight:900;font-size:70px">KI-SERIE · TEIL 2</span></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/ki-teil2-tiktok.jpg")
