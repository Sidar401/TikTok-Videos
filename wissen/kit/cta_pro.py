"""Profi-Folgen-Karten (3 Varianten). Aufruf: python3 wissen/kit/cta_pro.py  -> videos/cta-pro-1..3"""
import json, math, os, shutil, subprocess
ROOT = "/home/user/TikTok-Videos"; KIT = f"{ROOT}/wissen/kit"
S = "/tmp/claude-0/-home-user-TikTok-Videos/d5d88d44-fe09-517d-b753-eb81a1931e07/scratchpad"
CHECK = '<svg class="ck" width="44" height="44" viewBox="0 0 44 44"><path d="M8 23l9 9 19-20" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="48" stroke-dashoffset="48"/></svg>'
BASE = """
@font-face { font-family: "Inter Display"; font-weight: 900; src: url("assets/fonts/InterDisplay-Black.otf"); }
@font-face { font-family: "Inter Display"; font-weight: 800; src: url("assets/fonts/InterDisplay-ExtraBold.otf"); }
@font-face { font-family: "Inter"; font-weight: 600; src: url("assets/fonts/Inter-SemiBold.otf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: "Inter Display", "Inter", sans-serif; color: #fff; }
#bg { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }
#card { position: absolute; opacity: 0; overflow: hidden; }
.glass { background: linear-gradient(180deg, rgba(30,34,48,.72), rgba(10,12,20,.78)); border: 1.5px solid rgba(255,255,255,.16); backdrop-filter: blur(26px) saturate(1.2); -webkit-backdrop-filter: blur(26px) saturate(1.2);
  box-shadow: 0 40px 100px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.18); }
.av { position: relative; border-radius: 50%; background: url(assets/avatar.png) center/cover; }
.ring { position: absolute; inset: -9px; border-radius: 50%; background: conic-gradient(from 0deg, #ffe7a8, rgba(255,231,168,.1), #ffd06a, rgba(255,231,168,.1), #ffe7a8);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 5px), #000 calc(100% - 4px)); mask: radial-gradient(farthest-side, transparent calc(100% - 5px), #000 calc(100% - 4px)); }
.n { font-weight: 900; letter-spacing: -1.5px; }
.d { font-family: Inter, sans-serif; font-weight: 600; color: rgba(255,255,255,.66); letter-spacing: .2px; }
.btn { position: relative; font-weight: 800; letter-spacing: -.3px; }
.btn .a, .btn .b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 14px; border-radius: inherit; }
.btn .b { opacity: 0; }
#shine { position: absolute; top: -20%; bottom: -20%; width: 220px; left: -300px; background: linear-gradient(100deg, transparent, rgba(255,255,255,.22), transparent); transform: skewX(-18deg); pointer-events: none; }
#touch { position: absolute; width: 92px; height: 92px; margin: -46px 0 0 -46px; border-radius: 50%; background: rgba(255,255,255,.32); border: 3px solid rgba(255,255,255,.9); box-shadow: 0 8px 30px rgba(0,0,0,.45); opacity: 0; z-index: 20; }
#ripple { position: absolute; width: 92px; height: 92px; margin: -46px 0 0 -46px; border-radius: 50%; border: 3px solid rgba(255,255,255,.8); opacity: 0; z-index: 19; }
"""
V = {
 "cta-pro-1": dict(bg="bg1.png", tap=(540, 1566), css="""
#card { left: 160px; top: 1060px; width: 760px; padding: 64px 60px 58px; border-radius: 52px; text-align: center; }
#card .av { width: 180px; height: 180px; margin: 0 auto 30px; }
#card .n { font-size: 70px; } #card .d { font-size: 36px; margin: 10px 0 40px; }
#card .btn { height: 116px; border-radius: 58px; font-size: 50px; }
#card .btn .a { background: #fff; color: #0b0d14; }
#card .btn .b { background: rgba(255,255,255,.1); border: 2px solid rgba(255,255,255,.3); color: #fff; }
""", html=f"""<div class="av"><div class="ring"></div></div><div class="n">Novaro</div><div class="d">Weltraum, einfach erklärt</div>
<div class="btn" id="btn"><span class="a">Folgen</span><span class="b">{CHECK}Gefolgt</span></div>"""),
 "cta-pro-2": dict(bg="bg3.png", tap=(540, 1470), css="""
#card { left: 90px; top: 1180px; width: 900px; padding: 44px 46px 46px; border-radius: 48px;
  border: 2px solid transparent; background: linear-gradient(180deg, rgba(26,30,44,.8), rgba(10,12,20,.86)) padding-box, linear-gradient(135deg, #ffe2a0, rgba(255,255,255,.08) 40%, rgba(255,255,255,.08) 60%, #ffd06a) border-box; }
#card .row { display: flex; align-items: center; gap: 34px; margin-bottom: 38px; }
#card .av { width: 150px; height: 150px; flex: none; }
#card .n { font-size: 66px; } #card .d { font-size: 34px; margin-top: 6px; }
#card .btn { height: 108px; border-radius: 54px; font-size: 48px; }
#card .btn .a { background: linear-gradient(180deg, #ffe39a, #f6c04a); color: #1a1406; box-shadow: 0 10px 30px rgba(246,192,74,.3); }
#card .btn .b { background: rgba(255,255,255,.08); border: 2px solid rgba(255,226,160,.5); color: #ffe7a8; }
""", html=f"""<div class="row"><div class="av"><div class="ring"></div></div><div><div class="n">Novaro</div><div class="d">Weltraum, einfach erklärt</div></div></div>
<div class="btn" id="btn"><span class="a">Folgen</span><span class="b">{CHECK}Gefolgt</span></div>"""),
 "cta-pro-3": dict(bg="bg2.png", tap=(540, 1507), css="""
#wrap { position: absolute; left: 170px; top: 1140px; width: 740px; opacity: 0; }
#card { position: relative; opacity: 1; width: 740px; padding: 130px 56px 54px; border-radius: 52px; text-align: center; }
#wrap > .av { position: absolute; left: 50%; top: -105px; width: 210px; height: 210px; margin-left: -105px; z-index: 3; box-shadow: 0 0 0 8px rgba(12,14,22,.9), 0 20px 50px rgba(0,0,0,.6); }
#card .n { font-size: 70px; } #card .d { font-size: 36px; margin: 10px 0 40px; }
#card .btn { height: 116px; border-radius: 58px; font-size: 50px; }
#card .btn .a { background: #fff; color: #0b0d14; }
#card .btn .b { background: linear-gradient(180deg, #ffe39a, #f6c04a); color: #1a1406; }
""", html=f"""<div class="n">Novaro</div><div class="d">Weltraum, einfach erklärt</div>
<div class="btn" id="btn"><span class="a">Folgen</span><span class="b">{CHECK}Gefolgt</span></div>""", wrap=True),
}
for name, d in V.items():
    P = f"{ROOT}/videos/{name}"; os.makedirs(P + "/assets", exist_ok=True)
    shutil.copytree(f"{ROOT}/videos/leoniden/assets/fonts", P + "/assets/fonts", dirs_exist_ok=True)
    shutil.copy(f"{ROOT}/videos/leoniden/assets/gsap.min.js", P + "/assets/"); shutil.copy(f"{KIT}/avatar.png", P + "/assets/")
    shutil.copy(f"{ROOT}/videos/cta-demo-1/assets/bg.png" if d["bg"] == "bg1.png" else f"{ROOT}/videos/cta-demo-{3 if d['bg']=='bg3.png' else 2}/assets/bg.png", P + "/assets/bg.png")
    for f in ["hyperframes.json", "package.json"]:
        open(f"{P}/{f}", "w").write(open(f"{ROOT}/videos/leoniden/{f}").read().replace("leoniden", name))
    json.dump({"id": name, "name": name}, open(f"{P}/meta.json", "w"))
    tx, ty = d["tap"]; T = 3.7
    json.dump([{"s": "whoosh-schnell", "t": 1.1, "v": 0.3}, {"s": "kamera-klick", "t": T, "v": 0.45}, {"s": "pling-idee", "t": T + 0.2, "v": 0.25}, {"s": "whoosh-tief", "t": 8.9, "v": 0.22}], open(f"{P}/cues.json", "w"))
    subprocess.run(["python3", "-I", f"{KIT}/mix.py", f"{P}/cues.json", f"{P}/assets/sfx.wav", "10"], check=True)
    card = f'<div id="card" class="glass">{d["html"]}<div id="shine"></div></div>'
    if d.get("wrap"): card = f'<div id="wrap"><div class="av"><div class="ring"></div></div>{card}</div>'
    enter = "#wrap" if d.get("wrap") else "#card"
    html = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script><style>{BASE}{d['css']}</style></head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="10" data-width="1080" data-height="1920">
      <img id="bg" class="clip" src="assets/bg.png" data-start="0" data-duration="10" data-track-index="0" alt="" />
      <div id="ui" class="clip" data-start="0" data-duration="10" data-track-index="1">{card}
        <div id="ripple" style="left:{tx}px;top:{ty}px"></div><div id="touch" style="left:{tx}px;top:{ty}px"></div></div>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="10" data-track-index="2" data-volume="0.6"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#bg", {{ scale: 1.0 }}, {{ scale: 1.07, duration: 10, ease: "none" }}, 0);
      tl.fromTo("{enter}", {{ opacity: 0, y: 120, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "expo.out" }}, 1.1);
      tl.fromTo(".ring", {{ rotation: 0 }}, {{ rotation: 360, duration: 10, ease: "none" }}, 0);
      tl.fromTo("#card .n, #card .d, #btn", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.5, stagger: 0.08, ease: "power3.out" }}, 1.35);
      tl.fromTo("#touch", {{ opacity: 0, x: 240, y: 260, scale: 1.3 }}, {{ opacity: 1, x: 0, y: 0, scale: 1, duration: 0.9, ease: "power3.out" }}, 2.5);
      tl.to("#touch", {{ scale: 0.72, duration: 0.14 }}, {T - 0.14}); tl.to("#touch", {{ scale: 1, duration: 0.25 }}, {T});
      tl.to("#btn", {{ scale: 0.95, duration: 0.14 }}, {T - 0.14}); tl.to("#btn", {{ scale: 1, duration: 0.45, ease: "back.out(3)" }}, {T});
      tl.fromTo("#ripple", {{ opacity: 0.9, scale: 0.6 }}, {{ opacity: 0, scale: 3.2, duration: 0.7, ease: "power2.out", immediateRender: false }}, {T});
      tl.to("#btn .a", {{ opacity: 0, duration: 0.18 }}, {T}); tl.to("#btn .b", {{ opacity: 1, duration: 0.22 }}, {T + 0.05});
      tl.to("#btn .ck path", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.45, ease: "power2.out" }}, {T + 0.15});
      tl.fromTo("#shine", {{ x: 0 }}, {{ x: 1400, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, {T + 0.35});
      tl.to("#touch", {{ opacity: 0, scale: 0.6, duration: 0.4, ease: "power2.in" }}, {T + 0.7});
      tl.to("{enter}", {{ opacity: 0, y: 40, scale: 0.96, duration: 0.55, ease: "power2.in" }}, 9.0);
      window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
    </script>
  </body>
</html>"""
    open(f"{P}/index.html", "w").write(html); print("ok", name)
