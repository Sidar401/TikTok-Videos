import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D = "#22c55e", "#ef3b3b", "#f28a1e", "#1d2330"
OUT = "/home/user/tiktok-videos/renders/thumbnails/crash-usa-schulden-"
BG = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 70%,#22080c 0%,#08090d 45%,#000 100%);z-index:0"></div>'
      '<div style="position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:90px 90px;z-index:0"></div>')


def coin(x, y, d, z=2, rot=0):
    f = d / 700
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;transform:rotate({rot}deg);'
            f'background:radial-gradient(circle at 35% 30%,#fff3b0 0%,#f7c948 28%,#c98a0b 70%,#8a5a00 100%);'
            f'box-shadow:0 {40*f:.0f}px {90*f:.0f}px #000c,inset 0 0 0 {26*f:.0f}px #e0a21a,inset 0 0 0 {40*f:.0f}px #8a5a00,inset 0 0 {90*f:.0f}px #fff6;z-index:{z}">'
            f'<div style="text-align:center;font-family:Arial,Helvetica,sans-serif;font-weight:900;font-size:{430*f:.0f}px;line-height:{d}px;color:#6b4200;text-shadow:0 {8*f:.0f}px 0 #fff6">$</div>'
            f'<div style="position:absolute;inset:0;border-radius:50%;background:linear-gradient(135deg,#ffffff66 0%,transparent 35%)"></div></div>')


def kurve(x, y, w, h, pts, z=3, dick=16):
    p = " L".join(f"{a*w:.0f} {b*h:.0f}" for a, b in pts)
    ex, ey = pts[-1][0] * w, pts[-1][1] * h
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};overflow:visible" viewBox="0 0 {w} {h}"><defs><filter id="g{y}"><feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<path d="M{p}" fill="none" stroke="{R}" stroke-width="{dick*2.4:.0f}" stroke-linejoin="round" stroke-linecap="round" filter="url(#g{y})" opacity=".9"/>'
            f'<path d="M{p}" fill="none" stroke="#ff6b6b" stroke-width="{dick}" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<polygon points="{ex+22:.0f},{ey+30:.0f} {ex-50:.0f},{ey-22:.0f} {ex-6:.0f},{ey+48:.0f}" fill="#ff6b6b"/></svg>')


def pille(y, text="NUR EIN GEDANKENSPIEL"):
    return (f'<div style="position:absolute;top:{y}px;width:1080px;display:flex;justify-content:center;z-index:6"><span style="padding:18px 56px;border-radius:80px;background:{O};'
            f'color:#fff;font-weight:900;font-size:54px;box-shadow:0 0 50px {O}88">{text}</span></div>')


FALL = [(0.0, 0.05), (0.18, 0.15), (0.3, 0.02), (0.5, 0.4), (0.62, 0.3), (0.82, 0.8), (0.9, 0.62), (1.0, 0.98)]

# ---------- D: Münze mit Absturz-Kurve davor ----------
D_ = (BG + f'<div style="position:absolute;top:110px;width:1080px;text-align:center;font-weight:900;font-size:104px;line-height:1.0;color:#fff;letter-spacing:-2px;z-index:5;text-shadow:0 8px 30px #000">BÖRSEN-<span style="color:{R};text-shadow:0 0 40px {R}">CRASH</span><br/>= AMERIKAS<br/><span style="color:{G};text-shadow:0 0 40px {G}">VORTEIL?</span></div>'
      + coin(215, 560, 650) + kurve(60, 560, 960, 640, FALL, z=4)
      + f'<div style="position:absolute;left:60px;top:1260px;width:960px;text-align:center;z-index:5"><div style="font-weight:900;font-size:166px;line-height:1.05;color:{G};white-space:nowrap;text-shadow:0 0 50px {G}99">100 Mrd. $</div>'
        f'<div style="font-weight:800;font-size:44px;color:#cbd5e1;letter-spacing:4px;margin-top:4px">WENIGER ZINSEN PRO JAHR?</div></div>' + pille(1650))
ch.speichern(D_, OUT + "D.jpg")

# ---------- E: Frage-Plakat mit Münze links, Schildern rechts ----------
E_ = (BG + f'<div style="position:absolute;top:120px;width:1080px;text-align:center;font-weight:900;font-size:150px;line-height:1.0;color:#fff;letter-spacing:-3px;z-index:5;text-shadow:0 8px 30px #000">WER<br/>VERDIENT<br/>AM <span style="color:{R};text-shadow:0 0 44px {R}">CRASH</span>?</div>'
      + coin(-130, 690, 640, z=2, rot=-10)
      + f'<div style="position:absolute;left:500px;top:800px;z-index:5;transform:rotate(5deg);white-space:nowrap;padding:18px 36px;background:{R};color:#fff;font-weight:900;font-size:62px;border-radius:16px;box-shadow:0 16px 40px #000a">DEIN DEPOT ▼</div>'
      + f'<div style="position:absolute;left:430px;top:980px;z-index:5;transform:rotate(-4deg);white-space:nowrap;padding:18px 36px;background:{G};color:#052e12;font-weight:900;font-size:62px;border-radius:16px;box-shadow:0 16px 40px #000a">USA ▲ 100 Mrd. $</div>'
      + f'<div style="position:absolute;top:1380px;width:1080px;text-align:center;z-index:5"><div style="font-weight:800;font-size:50px;color:#cbd5e1;letter-spacing:3px">US-SCHULDEN</div><div style="font-weight:900;font-size:104px;line-height:1.05;color:#fff;white-space:nowrap">40,71 <span style="color:{O}">Billionen $</span></div></div>' + pille(1700))
ch.speichern(E_, OUT + "E.jpg")

# ---------- F: Münzstapel + Kurve oben ----------
st = "".join(coin(230 + (i % 2) * 40, 1010 - i * 70, 600, z=2 + i) for i in range(0, 1)) 
F_ = (BG + kurve(40, 120, 1000, 420, [(0.0, 0.1), (0.2, 0.3), (0.32, 0.05), (0.52, 0.55), (0.66, 0.4), (0.84, 0.95), (1.0, 0.8)], z=2, dick=14)
      + f'<div style="position:absolute;top:470px;width:1080px;text-align:center;font-weight:900;font-size:112px;line-height:1.05;color:#fff;letter-spacing:-3px;z-index:5;text-shadow:0 8px 30px #000">DEIN VERLUST.<br/><span style="background:linear-gradient(180deg,#fff3b0,#f7c948 50%,#c98a0b);-webkit-background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 30px #f7c94888)">IHR GEWINN?</span></div>'
      + coin(215, 840, 650, z=3)
      + f'<div style="position:absolute;left:630px;top:880px;z-index:6;transform:rotate(8deg);white-space:nowrap;padding:14px 30px;background:{G};color:#052e12;font-weight:900;font-size:58px;border-radius:16px;box-shadow:0 16px 40px #000a">+100 Mrd. $</div>'
      + f'<div style="position:absolute;left:40px;top:1180px;z-index:6;transform:rotate(-7deg);padding:16px 36px;background:{R};color:#fff;font-weight:900;font-size:70px;border-radius:16px;box-shadow:0 16px 40px #000a">CRASH ▼</div>'
      + f'<div style="position:absolute;top:1560px;width:1080px;text-align:center;z-index:5;font-weight:800;font-size:56px;color:#cbd5e1;letter-spacing:3px">40,71 BILLIONEN $ SCHULDEN</div>' + pille(1680))
ch.speichern(F_, OUT + "F.jpg")
