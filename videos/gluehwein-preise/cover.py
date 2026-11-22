import sys; sys.path.insert(0, "/home/user/TikTok-Videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
inhalt = (f'<div style="position:absolute;top:170px;width:1080px;text-align:center;font-weight:900;font-size:104px;color:{D};line-height:1.05">Glühwein-<br/>Abzocke?</div>'
  f'<div class="karte" style="left:110px;top:520px;width:860px;text-align:center"><div style="font-weight:800;font-size:46px;color:{D}">1 Liter Glühwein</div>'
  f'<div style="display:flex;justify-content:space-around;margin-top:30px"><div><div style="font-size:40px;color:#555">Markt</div><div style="font-weight:900;font-size:150px;color:{R}">25 €</div></div>'
  f'<div><div style="font-size:40px;color:#555">Supermarkt</div><div style="font-weight:900;font-size:150px;color:{G}">3 €</div></div></div></div>'
  f'<div style="position:absolute;top:1020px;width:1080px;display:flex;justify-content:center"><span style="padding:22px 56px;border-radius:70px;background:{R};color:#fff;font-weight:900;font-size:64px">So viel kassiert der Staat</span></div>'
  f'<div style="position:absolute;top:1220px;width:1080px;text-align:center;font-size:190px">🍷</div>')
ch.speichern(inhalt, "/home/user/TikTok-Videos/renders/thumbnails/gluehwein-preise-tiktok.jpg")
