import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
L = "/home/user/tiktok-videos/brand/logos/"
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:108px;color:{D};line-height:1.05">Dein Verlust =<br/><span style="color:{G}">ihr Gewinn?</span></div>'
  f'<div class="karte" style="left:110px;top:560px;width:860px;text-align:center;transform:rotate(-2deg)"><img src="file://{L}flagge-usa.svg" style="height:110px"/><div style="font-weight:800;font-size:44px;color:{D};margin-top:10px">US-Schulden</div><div style="font-weight:900;font-size:120px;color:{R};line-height:1.1">40,71 Bio. $</div></div>'
  f'<div class="karte" style="left:110px;top:1010px;width:860px;text-align:center;transform:rotate(2deg)"><div style="font-weight:800;font-size:44px;color:{D}">1 % weniger Zinsen =</div><div style="font-weight:900;font-size:110px;color:{G};line-height:1.1">≈ 100 Mrd. $</div></div>'
  f'<div style="position:absolute;top:1390px;width:1080px;display:flex;justify-content:center"><span style="padding:20px 56px;border-radius:70px;background:{O};color:#fff;font-weight:900;font-size:60px">Nur ein Gedankenspiel</span></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/crash-usa-schulden-tiktok.jpg")
