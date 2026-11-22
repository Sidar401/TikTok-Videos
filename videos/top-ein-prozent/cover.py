import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = ch.G, ch.ROT, ch.O, ch.D
punkte = "".join(f'<div style="width:46px;height:46px;border-radius:50%;background:{"#f28a1e" if i == 0 else "#c9ced5"}"></div>' for i in range(100))
inhalt = (f'<div style="position:absolute;top:150px;width:1080px;text-align:center;font-weight:900;font-size:120px;color:{D};line-height:1.05">Du und die<br/>reichsten <span style="color:{O}">1 %</span></div>'
  f'<div style="position:absolute;left:150px;top:520px;width:780px;display:grid;grid-template-columns:repeat(10,1fr);gap:14px;justify-items:center">{punkte}</div>'
  f'<div class="karte" style="left:150px;top:1200px;width:780px;text-align:center"><div style="font-weight:800;font-size:44px;color:{D}">Ab etwa</div><div style="font-weight:900;font-size:120px;color:{R};line-height:1.1">2,3 Mio. €</div></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/top-ein-prozent-tiktok.jpg")
