import json, os, shutil, subprocess
ROOT = "/home/user/TikTok-Videos"; S = "/tmp/claude-0/-home-user-TikTok-Videos/d5d88d44-fe09-517d-b753-eb81a1931e07/scratchpad"
BASE_CSS = """
@font-face { font-family: "Inter Display"; font-weight: 900; src: url("assets/fonts/InterDisplay-Black.otf"); }
@font-face { font-family: "Inter Display"; font-weight: 800; src: url("assets/fonts/InterDisplay-ExtraBold.otf"); }
@font-face { font-family: "Inter"; font-weight: 600; src: url("assets/fonts/Inter-SemiBold.otf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: "Inter Display", "Inter", sans-serif; color: #fff; }
#bg { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }
.glass { background: rgba(14,17,26,.62); border: 2px solid rgba(255,255,255,.14); backdrop-filter: blur(22px); -webkit-backdrop-filter: blur(22px); box-shadow: 0 30px 80px rgba(0,0,0,.55); }
.av { border-radius: 50%; background: url(assets/avatar.png) center/cover; box-shadow: 0 0 0 5px rgba(255,255,255,.9), 0 0 40px rgba(255,214,140,.35); }
.btn { position: relative; display: flex; align-items: center; justify-content: center; font-weight: 800; overflow: hidden; }
.btn .a, .btn .b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; border-radius: inherit; }
.btn .b { opacity: 0; }
#finger { position: absolute; font-size: 130px; line-height: 1; opacity: 0; filter: drop-shadow(0 10px 20px rgba(0,0,0,.6)); z-index: 20; transform-origin: 30% 10%; }
#ripple { position: absolute; width: 60px; height: 60px; margin: -30px 0 0 -30px; border-radius: 50%; border: 6px solid rgba(255,255,255,.9); opacity: 0; z-index: 19; }
.spark { position: absolute; width: 16px; height: 16px; margin: -8px 0 0 -8px; border-radius: 50%; background: #ffd23f; opacity: 0; z-index: 18; box-shadow: 0 0 16px #ffd23f; }
"""
DEMOS = {
 "cta-demo-1": dict(bg="bg1.png", tap=(540, 1552), css="""
#card { position: absolute; left: 150px; top: 1010px; width: 780px; padding: 56px 60px 60px; border-radius: 48px; text-align: center; opacity: 0; }
#card .av { width: 170px; height: 170px; margin: 0 auto 26px; }
#card .n { font-size: 66px; font-weight: 900; letter-spacing: -1px; }
#card .h { font: 600 36px Inter, sans-serif; color: rgba(255,255,255,.6); margin-top: 6px; }
#card .d { font: 600 36px Inter, sans-serif; color: rgba(255,255,255,.85); margin: 22px 0 36px; }
#card .btn { height: 112px; border-radius: 56px; font-size: 52px; }
#card .btn .a { background: #fff; color: #0b0d14; }
#card .btn .b { background: rgba(255,255,255,.12); border: 2px solid rgba(255,255,255,.35); color: #fff; }
""", html="""<div id="card" class="glass"><div class="av"></div><div class="n">Novaro</div><div class="h">@novaro040</div><div class="d">Weltraum, einfach erklärt 🔭</div>
<div class="btn" id="btn"><span class="a">Folgen</span><span class="b">✓ Gefolgt</span></div></div>""", enter="#card"),
 "cta-demo-2": dict(bg="bg2.png", tap=(540, 1205), css="""
#box { position: absolute; left: 0; right: 0; top: 760px; text-align: center; opacity: 0; }
#box .t { font-size: 96px; font-weight: 900; letter-spacing: -2px; text-shadow: 0 6px 40px rgba(0,0,0,.9); margin-bottom: 50px; }
#box .av { width: 280px; height: 280px; margin: 0 auto; position: relative; box-shadow: 0 0 0 7px #fff, 0 0 60px rgba(255,214,140,.4); }
#plus { position: absolute; left: 50%; top: 100%; width: 104px; height: 104px; margin: -52px 0 0 -52px; border-radius: 50%; background: #ffd23f; color: #111; font: 900 76px "Inter Display"; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 7px #000, 0 10px 30px rgba(0,0,0,.6); }
#plus .a, #plus .b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; line-height: 1; }
#plus .b { opacity: 0; }
#box .h { font: 600 44px Inter, sans-serif; color: rgba(255,255,255,.85); margin-top: 90px; text-shadow: 0 4px 20px rgba(0,0,0,.9); }
""", html="""<div id="box"><div class="t">Folg uns! 🚀</div><div class="av"><div id="plus"><span class="a"><svg width="54" height="54" viewBox="0 0 54 54"><path d="M27 6v42M6 27h42" stroke="#111" stroke-width="9" stroke-linecap="round"/></svg></span><span class="b"><svg width="54" height="54" viewBox="0 0 54 54"><path d="M9 28l12 12 24-26" fill="none" stroke="#111" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div></div><div class="h">@novaro040</div></div>""", enter="#box"),
 "cta-demo-3": dict(bg="bg3.png", tap=(868, 1455), css="""
#bar { position: absolute; left: 50px; right: 50px; top: 1370px; height: 170px; border-radius: 85px; display: flex; align-items: center; padding: 0 22px; opacity: 0; }
#bar .av { width: 126px; height: 126px; flex: none; box-shadow: 0 0 0 4px rgba(255,255,255,.9); }
#bar .tx { flex: 1; padding-left: 26px; }
#bar .n { font-size: 54px; font-weight: 900; letter-spacing: -1px; }
#bar .d { font: 600 30px Inter, sans-serif; color: rgba(255,255,255,.7); margin-top: 2px; }
#bar .btn { width: 250px; height: 104px; border-radius: 52px; font-size: 44px; flex: none; }
#bar .btn .a { background: #ffd23f; color: #111; }
#bar .btn .b { background: rgba(255,255,255,.12); border: 2px solid rgba(255,255,255,.4); color: #fff; }
""", html="""<div id="bar" class="glass"><div class="av"></div><div class="tx"><div class="n">Novaro</div><div class="d">Neue Videos jeden Tag</div></div><div class="btn" id="btn"><span class="a">Folgen</span><span class="b">Gefolgt ✓</span></div></div>""", enter="#bar"),
}
for name, d in DEMOS.items():
    P = f"{ROOT}/videos/{name}"; os.makedirs(P + "/assets", exist_ok=True)
    shutil.copytree(f"{ROOT}/videos/leoniden/assets/fonts", P + "/assets/fonts", dirs_exist_ok=True)
    shutil.copy(f"{ROOT}/videos/leoniden/assets/gsap.min.js", P + "/assets/"); shutil.copy(f"{S}/avatar.png", P + "/assets/"); shutil.copy(f"{S}/{d['bg']}", P + "/assets/bg.png")
    for f in ["hyperframes.json", "package.json"]:
        open(f"{P}/{f}", "w").write(open(f"{ROOT}/videos/leoniden/{f}").read().replace("leoniden", name))
    json.dump({"id": name, "name": name}, open(f"{P}/meta.json", "w"))
    tx, ty = d["tap"]; T = 3.6
    cues = [{"s": "whoosh-schnell", "t": 1.15, "v": 0.35}, {"s": "kamera-klick", "t": T, "v": 0.5}, {"s": "pling-idee", "t": T + 0.15, "v": 0.3}, {"s": "whoosh-tief", "t": 8.9, "v": 0.25}]
    json.dump(cues, open(f"{P}/cues.json", "w"))
    subprocess.run(["python3", "-I", f"{ROOT}/wissen/kit/mix.py", f"{P}/cues.json", f"{P}/assets/sfx.wav", "10"], check=True)
    swap = (f'tl.to("#plus", {{ rotation: 360, backgroundColor: "#ffffff", duration: 0.45, ease: "back.out(2)" }}, {T});'
            f'tl.to("#plus .a", {{ opacity: 0, duration: 0.15 }}, {T}); tl.to("#plus .b", {{ opacity: 1, duration: 0.2 }}, {T + 0.15});'
            f'tl.fromTo("#box .av", {{ boxShadow: "0 0 0 7px #fff, 0 0 60px rgba(255,214,140,.4)" }}, {{ boxShadow: "0 0 0 7px #ffd23f, 0 0 110px rgba(255,210,63,.8)", duration: 0.4, yoyo: true, repeat: 1, immediateRender: false }}, {T});'
            ) if name == "cta-demo-2" else (
            f'tl.to("#btn", {{ scale: 0.93, duration: 0.12 }}, {T - 0.12}); tl.to("#btn", {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, {T});'
            f'tl.to("#btn .a", {{ opacity: 0, duration: 0.2 }}, {T}); tl.to("#btn .b", {{ opacity: 1, duration: 0.25 }}, {T + 0.05});')
    if name == "cta-demo-2": swap += f'tl.to("#plus", {{ scale: 0.88, duration: 0.12 }}, {T - 0.12}); tl.to("#plus", {{ scale: 1, duration: 0.3 }}, {T});'
    sparks = "".join(f'<div class="spark" id="sp{i}" style="left:{tx}px;top:{ty}px"></div>' for i in range(10))
    sp_js = "".join(f'tl.fromTo("#sp{i}", {{ x: 0, y: 0, opacity: 1, scale: 1 }}, {{ x: {int(150*__import__("math").cos(i*0.628))}, y: {int(150*__import__("math").sin(i*0.628))}, opacity: 0, scale: 0.3, duration: 0.7, ease: "power2.out", immediateRender: false }}, {T});' for i in range(10))
    html = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>{BASE_CSS}{d['css']}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="10" data-width="1080" data-height="1920">
      <img id="bg" class="clip" src="assets/bg.png" data-start="0" data-duration="10" data-track-index="0" alt="" />
      <div id="ui" class="clip" data-start="0" data-duration="10" data-track-index="1">{d['html']}
        <div id="ripple" style="left:{tx}px;top:{ty}px"></div>{sparks}
        <div id="finger" style="left:{tx - 38}px;top:{ty - 12}px">👆</div>
      </div>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="10" data-track-index="2" data-volume="0.6"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#bg", {{ scale: 1.0 }}, {{ scale: 1.08, duration: 10, ease: "none" }}, 0);
      tl.fromTo("{d['enter']}", {{ opacity: 0, y: 90, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.65, ease: "back.out(1.6)" }}, 1.2);
      tl.fromTo("#finger", {{ opacity: 0, x: 260, y: 320 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.9, ease: "power3.out" }}, 2.4);
      tl.to("#finger", {{ scale: 0.86, duration: 0.12 }}, {T - 0.12}); tl.to("#finger", {{ scale: 1, duration: 0.2 }}, {T});
      tl.fromTo("#ripple", {{ opacity: 0.9, scale: 0.4 }}, {{ opacity: 0, scale: 4, duration: 0.6, ease: "power2.out", immediateRender: false }}, {T});
      {swap}{sp_js}
      tl.to("#finger", {{ opacity: 0, x: 200, y: 300, duration: 0.7, ease: "power2.in" }}, {T + 0.8});
      tl.to("{d['enter']}", {{ opacity: 0, y: 60, duration: 0.5, ease: "power2.in" }}, 9.0);
      window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
    </script>
  </body>
</html>"""
    open(f"{P}/index.html", "w").write(html)
    print("ok", name)
