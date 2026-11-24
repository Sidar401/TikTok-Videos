import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D, L = ch.G, ch.ROT, ch.O, ch.D, ch.L
chart = (f'<svg style="position:absolute;left:60px;top:1350px;width:960px;height:300px;z-index:3" viewBox="0 0 960 380"><path d="M0 40 L180 70 L300 20 L460 150 L560 110 L700 300 L780 230 L960 340" fill="none" stroke="{R}" stroke-width="22" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>'
         f'<polygon points="960,340 905,290 925,355" fill="{R}"/></svg>')
inhalt = (chart
  + f'<div style="position:absolute;top:130px;width:1080px;text-align:center;font-weight:900;font-size:150px;line-height:1.0;color:{D};letter-spacing:-3px">DEIN<br/>VERLUST</div>'
  f'<div style="position:absolute;top:470px;width:1080px;text-align:center;font-weight:900;font-size:150px;line-height:1.0;color:{G};letter-spacing:-3px">= IHR<br/>GEWINN?</div>'
  f'<div style="position:absolute;left:60px;top:880px;width:450px;height:400px;background:#fff;border:6px solid {R};border-radius:22px;box-shadow:0 22px 50px #0003;text-align:center;padding-top:40px;transform:rotate(-3deg);z-index:4">'
  f'<div style="font-weight:800;font-size:44px;color:{D}">DEIN DEPOT</div><div style="font-weight:900;font-size:150px;color:{R};line-height:1.1">▼</div><div style="font-weight:900;font-size:60px;color:{R}">Verlust</div></div>'
  f'<div style="position:absolute;left:570px;top:900px;width:450px;height:400px;background:#fff;border:6px solid {G};border-radius:22px;box-shadow:0 22px 50px #0003;text-align:center;padding-top:30px;transform:rotate(3deg);z-index:4">'
  f'<img src="file://{L}flagge-usa.svg" style="height:80px"/><div style="font-weight:900;font-size:110px;color:{G};line-height:1.05;margin-top:6px">100</div><div style="font-weight:900;font-size:46px;color:{G}">Mrd. $ gespart?</div></div>'
  f'<div style="position:absolute;top:1620px;width:1080px;display:flex;justify-content:center;z-index:5"><span style="padding:22px 62px;border-radius:80px;background:{O};color:#fff;font-weight:900;font-size:62px;box-shadow:0 16px 36px #0004">NUR EIN GEDANKENSPIEL</span></div>')
ch.speichern(inhalt, "/home/user/tiktok-videos/renders/thumbnails/crash-usa-schulden-tiktok.jpg")
