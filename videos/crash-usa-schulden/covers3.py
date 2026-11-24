import sys; sys.path.insert(0, "/home/user/tiktok-videos/scripts")
import cover_hell as ch
G, R, O, D, L = "#22c55e", "#ef3b3b", "#f28a1e", "#1d2330", ch.L
OUT = "/home/user/tiktok-videos/renders/thumbnails/crash-usa-schulden-"

# ---------- A: DARK GLOW (Kino-Look) ----------
bgA = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,#3a1218 0%,#12141d 45%,#07080c 100%);z-index:0"></div>'
       '<div style="position:absolute;inset:0;background-image:linear-gradient(#ffffff0d 1px,transparent 1px),linear-gradient(90deg,#ffffff0d 1px,transparent 1px);background-size:90px 90px;z-index:0"></div>')
chartA = (f'<svg style="position:absolute;left:0;top:700px;width:1080px;height:520px;z-index:1" viewBox="0 0 1080 640"><defs><filter id="g"><feGaussianBlur stdDeviation="14"/></filter></defs>'
          f'<path d="M30 60 L190 130 L300 40 L470 250 L570 190 L760 470 L850 380 L1030 600" fill="none" stroke="{R}" stroke-width="40" stroke-linejoin="round" stroke-linecap="round" filter="url(#g)" opacity=".9"/>'
          f'<path d="M30 60 L190 130 L300 40 L470 250 L570 190 L760 470 L850 380 L1030 600" fill="none" stroke="#ff6b6b" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>'
          f'<polygon points="1050,620 985,560 1010,630" fill="#ff6b6b"/></svg>')
htmlA = (bgA + chartA
  + f'<div style="position:absolute;top:120px;width:1080px;text-align:center;font-weight:900;font-size:128px;line-height:1.0;color:#fff;letter-spacing:-2px;text-shadow:0 8px 30px #000">BÖRSEN-<span style="color:{R};text-shadow:0 0 40px {R}">CRASH</span><br/>= AMERIKAS<br/><span style="color:{G};text-shadow:0 0 40px {G}">VORTEIL?</span></div>'
  f'<div style="position:absolute;left:40px;top:1290px;width:1000px;text-align:center;z-index:3"><div style="font-weight:800;font-size:44px;color:#cbd5e1;letter-spacing:4px">ZINSERSPARNIS PRO JAHR</div>'
  f'<div style="font-weight:900;font-size:160px;line-height:1.05;color:{G};white-space:nowrap;text-shadow:0 0 50px {G}99">100 Mrd. $</div></div>'
  f'<div style="position:absolute;top:1665px;width:1080px;display:flex;justify-content:center;z-index:3"><span style="padding:18px 56px;border-radius:80px;background:{O};color:#fff;font-weight:900;font-size:54px;box-shadow:0 0 50px {O}88">NUR EIN GEDANKENSPIEL</span></div>')
ch.speichern(htmlA, OUT + "A.jpg")

# ---------- B: GETEILTER BILDSCHIRM (Plakat) ----------
htmlB = (f'<div style="position:absolute;inset:0;background:linear-gradient(115deg,#b91c1c 0%,#ef3b3b 49.6%,#16a34a 50.4%,#22c55e 100%);z-index:0"></div>'
  f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,#ffffff22,transparent 60%);z-index:0"></div>'
  f'<div style="position:absolute;left:60px;top:130px;width:460px;text-align:center;color:#fff;z-index:2"><div style="font-weight:900;font-size:62px;letter-spacing:2px;opacity:.9">DU</div><div style="font-weight:900;font-size:120px;line-height:1;text-shadow:0 10px 30px #0006">VER-<br/>LIERST</div></div>'
  f'<div style="position:absolute;left:560px;top:130px;width:460px;text-align:center;color:#fff;z-index:2"><div style="font-weight:900;font-size:62px;letter-spacing:2px;opacity:.9">DIE USA</div><div style="font-weight:900;font-size:104px;line-height:1;text-shadow:0 10px 30px #0006">SPAREN</div></div>'
  f'<div style="position:absolute;left:40px;top:560px;width:480px;text-align:center;z-index:2"><div style="font-weight:900;font-size:260px;line-height:1;color:#fff;text-shadow:0 14px 40px #0007">▼</div><div style="font-weight:900;font-size:70px;color:#fff;text-shadow:0 8px 24px #0006">DEIN DEPOT</div></div>'
  f'<div style="position:absolute;left:560px;top:560px;width:480px;text-align:center;z-index:2"><div style="font-weight:900;font-size:230px;line-height:1;color:#fff;text-shadow:0 14px 40px #0007">100</div><div style="font-weight:900;font-size:60px;color:#fff;text-shadow:0 8px 24px #0006">MRD. $ PRO JAHR</div></div>'
  f'<div style="position:absolute;left:400px;top:1090px;width:280px;height:280px;border-radius:50%;background:#fff;color:{D};font-weight:900;font-size:240px;line-height:280px;text-align:center;box-shadow:0 20px 60px #0008;z-index:4;border:12px solid {O}">?</div>'
  f'<div style="position:absolute;top:1560px;width:1080px;text-align:center;z-index:3"><div style="display:inline-block;padding:24px 50px;background:{D};color:#fff;font-weight:900;font-size:50px;border-radius:20px;box-shadow:0 16px 40px #0007">GEDANKENSPIEL: <span style="color:{O}">40,71 BIO. $</span> SCHULDEN</div></div>')
ch.speichern(htmlB, OUT + "B.jpg")

# ---------- C: GOLD-MÜNZE / GELD (Premium-Look) ----------
coin = (f'<div style="position:absolute;left:190px;top:470px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff3b0 0%,#f7c948 28%,#c98a0b 70%,#8a5a00 100%);box-shadow:0 40px 90px #000a,inset 0 0 0 26px #e0a21a,inset 0 0 0 40px #8a5a00,inset 0 0 90px #fff6;z-index:2">'
        f'<div style="text-align:center;font-weight:900;font-family:Arial,Helvetica,sans-serif;font-size:430px;line-height:700px;color:#6b4200;text-shadow:0 8px 0 #fff6,0 -4px 0 #4a2c00">$</div></div>'
        f'<div style="position:absolute;left:190px;top:470px;width:700px;height:700px;border-radius:50%;background:linear-gradient(135deg,#ffffff66 0%,transparent 35%);z-index:3"></div>')
htmlC = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,#1f2a44 0%,#0b1020 60%,#05070d 100%);z-index:0"></div>'
  + f'<div style="position:absolute;top:120px;width:1080px;text-align:center;font-weight:900;font-size:102px;line-height:1.04;color:#fff;letter-spacing:-2px;z-index:3;text-shadow:0 8px 30px #000">WER PROFITIERT<br/>WIRKLICH VOM<br/><span style="color:{R};text-shadow:0 0 36px {R}aa">CRASH</span>?</div>'
  + coin
  + f'<div style="position:absolute;left:70px;top:1010px;z-index:4;transform:rotate(-8deg);padding:18px 40px;background:{R};color:#fff;font-weight:900;font-size:78px;border-radius:16px;box-shadow:0 16px 40px #0009">−40 % DEPOT</div>'
  + f'<div style="position:absolute;right:50px;top:560px;z-index:4;transform:rotate(7deg);padding:18px 40px;background:{G};color:#06240f;font-weight:900;font-size:78px;border-radius:16px;box-shadow:0 16px 40px #0009">+100 Mrd. $</div>'
  + f'<div style="position:absolute;top:1290px;width:1080px;text-align:center;z-index:3"><div style="font-weight:800;font-size:50px;color:#cbd5e1;letter-spacing:3px">US-SCHULDEN</div><div style="font-weight:900;font-size:128px;line-height:1.05;color:#fff">40,71 <span style="color:{O}">Billionen</span></div></div>'
  + f'<div style="position:absolute;top:1685px;width:1080px;display:flex;justify-content:center;z-index:3"><span style="padding:18px 56px;border-radius:80px;background:{O};color:#fff;font-weight:900;font-size:52px;box-shadow:0 0 50px {O}88">NUR EIN GEDANKENSPIEL</span></div>')
ch.speichern(htmlC, OUT + "C.jpg")
