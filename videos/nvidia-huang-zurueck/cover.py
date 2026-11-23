import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
B = "/home/user/tiktok-videos/brand/"
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:116px;color:{D};line-height:1.05">Huang ist<br/><span style="color:{G}">ZURÜCK!</span></div>'
  f'<div style="position:absolute;left:290px;top:520px;width:500px;height:560px;border:10px solid #fff;border-radius:14px;overflow:hidden;box-shadow:0 20px 44px #0003"><img src="file://{B}fotos/jensen-huang.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 15%"/></div>'
  f'<div class="karte" style="left:90px;top:1130px;width:900px;display:flex;align-items:center;justify-content:space-around;padding:26px 30px"><img src="file://{B}logos/nvidia.svg" style="height:80px"/><span style="font-weight:900;font-size:130px;color:{G}">+30 %</span></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/nvidia-huang-zurueck-tiktok.jpg")
