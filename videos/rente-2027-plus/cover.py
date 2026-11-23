import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:112px;color:{D};line-height:1.05">Rente 2027:<br/><span style="color:{G}">+4,09 %</span></div>'
  f'<div class="karte" style="left:110px;top:560px;width:860px;text-align:center;transform:rotate(-2deg)"><div style="font-weight:800;font-size:44px;color:{D}">1.500 € Rente</div><div style="font-weight:900;font-size:130px;color:{G};line-height:1.1">≈ +61 €</div></div>'
  f'<div style="position:absolute;top:960px;width:1080px;display:flex;justify-content:center"><span style="padding:22px 56px;border-radius:70px;background:{R};color:#fff;font-weight:900;font-size:64px">Aber: dein Beitrag steigt!</span></div>'
  f'<div style="position:absolute;top:1130px;width:1080px;text-align:center;font-weight:900;font-size:140px;color:{R}">19,8 % ▲</div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/rente-2027-plus-tiktok.jpg")
