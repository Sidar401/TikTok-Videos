import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:116px;color:{D};line-height:1.05">Roboter:<br/><span style="color:{O}">Hype</span> oder <span style="color:{G}">Geld</span>?</div>'
  f'<div class="karte" style="left:110px;top:560px;width:860px;text-align:center;transform:rotate(-2deg)"><div style="font-weight:800;font-size:44px;color:{D}">Neu in Fabriken</div><div style="font-weight:900;font-size:130px;color:{G};line-height:1.1">603.000</div></div>'
  f'<div class="karte" style="left:110px;top:900px;width:860px;text-align:center;transform:rotate(2deg)"><div style="font-weight:800;font-size:44px;color:{D}">Menschen-Roboter verkauft</div><div style="font-weight:900;font-size:130px;color:{R};line-height:1.1">≈ 7.000</div></div>'
  f'<div style="position:absolute;top:1290px;width:1080px;display:flex;justify-content:center"><span style="padding:22px 64px;border-radius:70px;background:{O};color:#fff;font-weight:900;font-size:70px">KI-SERIE · TEIL 3</span></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/ki-teil3-tiktok.jpg")
