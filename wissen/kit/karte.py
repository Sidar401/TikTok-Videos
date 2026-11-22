"""Folgen-Karte (freigegeben 17.11., Variante cta-pro-3) für sauber_bau.py.
szene.json: "karte": [start, dauer]  -> ersetzt roten "+ Folgen"-Pill und Folg-Box."""
CHECK = '<svg class="ck" width="44" height="44" viewBox="0 0 44 44"><path d="M8 23l9 9 19-20" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="48" stroke-dashoffset="48"/></svg>'
CSS = """
#fk-box { transform-origin: 540px 995px; transform: translateY(330px) scale(.68); }
#fk-wrap { position: absolute; left: 170px; top: 760px; width: 740px; z-index: 30; }
#fk { position: relative; width: 740px; padding: 130px 56px 54px; border-radius: 52px; text-align: center; overflow: hidden; font-family: "Inter Display", Inter, sans-serif; color: #fff;
  background: linear-gradient(180deg, rgba(30,34,48,.74), rgba(10,12,20,.82)); border: 1.5px solid rgba(255,255,255,.16); backdrop-filter: blur(26px) saturate(1.2); -webkit-backdrop-filter: blur(26px) saturate(1.2);
  box-shadow: 0 40px 100px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.18); }
#fk-wrap > .fk-av { position: absolute; left: 50%; top: -105px; width: 210px; height: 210px; margin-left: -105px; z-index: 3; border-radius: 50%; background: url(assets/avatar.png) center/cover; box-shadow: 0 0 0 8px rgba(12,14,22,.9), 0 20px 50px rgba(0,0,0,.6); }
.fk-ring { position: absolute; inset: -9px; border-radius: 50%; background: conic-gradient(from 0deg, #ffe7a8, rgba(255,231,168,.1), #ffd06a, rgba(255,231,168,.1), #ffe7a8);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 5px), #000 calc(100% - 4px)); mask: radial-gradient(farthest-side, transparent calc(100% - 5px), #000 calc(100% - 4px)); }
#fk .n { font-size: 70px; font-weight: 900; letter-spacing: -1.5px; } #fk .d { font: 600 36px Inter, sans-serif; color: rgba(255,255,255,.66); margin: 10px 0 40px; }
#fk .btn { position: relative; height: 116px; border-radius: 58px; font-size: 50px; font-weight: 800; }
#fk .btn .a, #fk .btn .b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 14px; border-radius: inherit; }
#fk .btn .a { background: #fff; color: #0b0d14; } #fk .btn .b { opacity: 0; background: linear-gradient(180deg, #ffe39a, #f6c04a); color: #1a1406; }
#fk-shine { position: absolute; top: -20%; bottom: -20%; width: 220px; left: -300px; background: linear-gradient(100deg, transparent, rgba(255,255,255,.22), transparent); transform: skewX(-18deg); }
#fk-touch, #fk-rip { position: absolute; left: 540px; top: 1127px; width: 92px; height: 92px; margin: -46px 0 0 -46px; border-radius: 50%; z-index: 31; opacity: 0; }
#fk-touch { background: rgba(255,255,255,.32); border: 3px solid rgba(255,255,255,.9); box-shadow: 0 8px 30px rgba(0,0,0,.45); } #fk-rip { border: 3px solid rgba(255,255,255,.8); }
"""
def html(s, d):
    return (f'<div id="fk-box" class="clip" data-start="{s}" data-duration="{d}" data-track-index="5"><div id="fk-wrap"><div class="fk-av"><div class="fk-ring"></div></div>'
            f'<div id="fk"><div class="n">Novaro</div><div class="d">Weltraum, einfach erklärt</div><div class="btn" id="fk-btn"><span class="a">Folgen</span><span class="b">{CHECK}Gefolgt</span></div><div id="fk-shine"></div></div></div>'
            f'<div id="fk-rip"></div><div id="fk-touch"></div></div>')
def js(s, d):
    T = s + 1.9
    return f"""
      tl.fromTo("#fk-wrap", {{ opacity: 0, y: 120, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "expo.out" }}, {s});
      tl.fromTo(".fk-ring", {{ rotation: 0 }}, {{ rotation: 200, duration: {d}, ease: "none" }}, {s});
      tl.fromTo("#fk .n, #fk .d, #fk-btn", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, stagger: 0.07, ease: "power3.out" }}, {s + 0.2});
      tl.fromTo("#fk-touch", {{ opacity: 0, x: 240, y: 260, scale: 1.3 }}, {{ opacity: 1, x: 0, y: 0, scale: 1, duration: 0.8, ease: "power3.out" }}, {s + 0.9});
      tl.to("#fk-touch", {{ scale: 0.72, duration: 0.14 }}, {T - 0.14}); tl.to("#fk-touch", {{ scale: 1, duration: 0.25 }}, {T});
      tl.to("#fk-btn", {{ scale: 0.95, duration: 0.14 }}, {T - 0.14}); tl.to("#fk-btn", {{ scale: 1, duration: 0.45, ease: "back.out(3)" }}, {T});
      tl.fromTo("#fk-rip", {{ opacity: 0.9, scale: 0.6 }}, {{ opacity: 0, scale: 3.2, duration: 0.7, ease: "power2.out", immediateRender: false }}, {T});
      tl.to("#fk-btn .a", {{ opacity: 0, duration: 0.18 }}, {T}); tl.to("#fk-btn .b", {{ opacity: 1, duration: 0.22 }}, {T + 0.05});
      tl.to("#fk-btn .ck path", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.45, ease: "power2.out" }}, {T + 0.15});
      tl.fromTo("#fk-shine", {{ x: 0 }}, {{ x: 1400, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, {T + 0.35});
      tl.to("#fk-touch", {{ opacity: 0, scale: 0.6, duration: 0.4, ease: "power2.in" }}, {T + 0.7});
      tl.to("#fk-wrap", {{ opacity: 0, y: 40, scale: 0.96, duration: 0.45, ease: "power2.in" }}, {s + d - 0.5});
"""
def apply(h, s, d):
    lines = [l for l in h.split("\n") if not any(k in l for k in ('id="share"', 'id="follow"', '"#share-in"', '"#follow-in', '#follow-in .pill'))]
    h = "\n".join(lines)
    h = h.replace("</style>", CSS + "</style>", 1)
    h = h.replace('<audio id="voice"', html(s, d) + '\n      <audio id="voice"', 1)
    h = h.replace("      tl.to({}, { duration: 0.01 }", js(s, d) + "      tl.to({}, { duration: 0.01 }", 1)
    return h
