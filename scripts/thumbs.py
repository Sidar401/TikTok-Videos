"""Thumbnail-Stil „Dark Glow“ (ab 25.10., Nutzer-Wunsch nach Vorbild Finanzbär, aber in Orange).

Dunkler Hintergrund mit Raster + orangem Leuchten, riesige fette Schrift (weiß + orange Akzente,
oranger Kasten), leuchtende Chart-Linien mit Wert-Pillen, plastische Objekte (Geldbündel, Münzen, Kugeln),
Kein Pfoten-Badge (Nutzer: weglassen), kein Rahmen, kein Beagle.

  from thumbs import *            # in videos/thumbs-<name>/build.py
  seite(HERE, [V1, V2, V3])       # 1920×1080, je 1 s
  seite(HERE, [TT], tiktok=True)  # 1080×1920
Export: python3 scripts/thumbs.py export videos/thumbs-<name> <name>  (→ renders/thumbnails/<name>-1..3.jpg / -tiktok.jpg)
"""
import subprocess
import sys
from pathlib import Path

OR, OR_HELL, OR_DUNKEL = "#ff8a1f", "#ffb35c", "#c25f00"
ROT, GRUEN, BG = "#ff4d4d", "#2fd27a", "#0e1012"
_n = [0]


def _uid(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


def titel(zeilen, x, y, gr=150, w=None, align="left"):
    """zeilen = [(text, art)]; art: 'w' weiß, 'o' orange, 'box' orange Kasten, 'rot' rote Box."""
    out = []
    for t, a in zeilen:
        if a == "box":
            out.append(f'<div><span style="display:inline-block;padding:4px 30px 10px;border-radius:22px;background:{OR};color:#111;box-shadow:0 0 60px {OR}88">{t}</span></div>')
        elif a == "rot":
            out.append(f'<div><span style="display:inline-block;padding:4px 30px 10px;border-radius:22px;background:{ROT};color:#fff;box-shadow:0 0 60px {ROT}88">{t}</span></div>')
        else:
            col = {"w": "#fff", "o": OR, "r": ROT, "g": GRUEN}[a]
            glow = f";text-shadow:0 0 40px {col}66" if a != "w" else ";text-shadow:0 6px 0 #000"
            out.append(f'<div style="color:{col}{glow}">{t}</div>')
    ww = f"width:{w}px;" if w else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{ww}font-weight:900;font-size:{gr}px;line-height:1.02;'
            f'letter-spacing:-2px;text-align:{align};display:flex;flex-direction:column;gap:14px;z-index:3">{"".join(out)}</div>')


def chart(pts, x, y, w, h, farbe=OR, pills=(), achse=None, fill=True):
    """Leuchtende Linie. pts = [(0..1, 0..1)] (y=0 unten). pills = [(index, text)]. achse = Beschriftungen unten."""
    u = _uid("c")
    P = [(px * w, h - py * h) for px, py in pts]
    d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in P)
    area = d + f" L{P[-1][0]:.0f} {h} L{P[0][0]:.0f} {h} Z"
    s = [f'<defs><linearGradient id="{u}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{farbe}" stop-opacity="0.35"/>'
         f'<stop offset="1" stop-color="{farbe}" stop-opacity="0"/></linearGradient>'
         f'<filter id="{u}f" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter></defs>']
    if fill:
        s.append(f'<path d="{area}" fill="url(#{u}g)"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="22" stroke-linejoin="round" opacity="0.7" filter="url(#{u}f)"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>')
    s.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="2.5" stroke-linejoin="round" opacity="0.6"/>')
    html = [f'<svg viewBox="0 0 {w} {h}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:1">{"".join(s)}</svg>']
    for i, t in pills:
        px, py = P[i]
        html.append(f'<div style="position:absolute;left:{x + px}px;top:{y + py - 150}px;transform:translateX(-50%);z-index:2;display:flex;flex-direction:column;align-items:center">'
                    f'<div style="padding:6px 22px 8px;border-radius:14px;background:{farbe};color:#111;font-weight:900;font-size:50px;white-space:nowrap;'
                    f'box-shadow:0 0 30px {farbe}aa;border:3px solid #fff3">{t}</div>'
                    f'<div style="width:0;height:{80}px;border-left:5px dashed {farbe};opacity:0.8"></div></div>')
    if achse:
        n = len(achse)
        html.append(f'<div style="position:absolute;left:{x}px;top:{y + h + 20}px;width:{w}px;display:flex;justify-content:space-around;'
                    f'font-weight:800;font-size:40px;color:#ffffffaa;z-index:2">{"".join(f"<span>{a}</span>" for a in achse)}</div>')
    return "".join(html)


def muenzen(x, y, n=6, gr=150):
    """Goldmünz-Stapel (plastisch)."""
    u = _uid("m")
    h = gr * 0.16
    defs = (f'<defs><linearGradient id="{u}s" x1="0" x2="1"><stop offset="0" stop-color="#a86a00"/><stop offset="0.45" stop-color="#ffd25e"/>'
            f'<stop offset="1" stop-color="#9a5c00"/></linearGradient><radialGradient id="{u}t" cx="0.4" cy="0.35"><stop offset="0" stop-color="#fff2b0"/>'
            f'<stop offset="0.6" stop-color="#ffc533"/><stop offset="1" stop-color="#d48a00"/></radialGradient></defs>')
    rx, ry = gr / 2, gr * 0.22
    H = n * h + ry * 2 + 10
    coins = []
    for i in range(n):
        cy = H - ry - 5 - i * h
        coins.append(f'<path d="M0 {cy - h} L0 {cy} A{rx} {ry} 0 0 0 {gr} {cy} L{gr} {cy - h} Z" fill="url(#{u}s)" stroke="#8a5200" stroke-width="1.5"/>')
        coins.append(f'<ellipse cx="{rx}" cy="{cy - h}" rx="{rx}" ry="{ry}" fill="url(#{u}t)" stroke="#b87800" stroke-width="2"/>')
    top = H - ry - 5 - (n - 1) * h - h
    coins.append(f'<text x="{rx}" y="{top + gr * 0.09}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="{gr * 0.26}" fill="#b87800">€</text>')
    return (f'<svg viewBox="0 0 {gr} {H}" style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{H}px;overflow:visible;'
            f'filter:drop-shadow(0 20px 20px #000a);z-index:2">{defs}{"".join(coins)}</svg>')


def buendel(x, y, s=1.0, lagen=4):
    """Stapel Geldbündel (isometrisch)."""
    u = _uid("b")
    w, d, hh = 260, 120, 26
    parts = [f'<defs><linearGradient id="{u}t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9f2d0"/><stop offset="1" stop-color="#9fcf8f"/></linearGradient></defs>']
    for i in range(lagen):
        oy = 200 - i * hh
        top = f"0,{oy} {w / 2},{oy - d / 2} {w},{oy} {w / 2},{oy + d / 2}"
        parts.append(f'<polygon points="0,{oy} {w / 2},{oy + d / 2} {w / 2},{oy + d / 2 + hh} 0,{oy + hh}" fill="#6fa862"/>')
        parts.append(f'<polygon points="{w},{oy} {w / 2},{oy + d / 2} {w / 2},{oy + d / 2 + hh} {w},{oy + hh}" fill="#558a4a"/>')
        for k in range(1, 5):
            parts.append(f'<path d="M0 {oy + k * hh / 5} L{w / 2} {oy + d / 2 + k * hh / 5} L{w} {oy + k * hh / 5}" fill="none" stroke="#e8f5e2" stroke-width="1.2" opacity="0.7"/>')
        parts.append(f'<polygon points="{top}" fill="url(#{u}t)" stroke="#4d7d43" stroke-width="2"/>')
    oy = 200 - (lagen - 1) * hh
    parts.append(f'<polygon points="{w * 0.42},{oy - d * 0.29} {w * 0.58},{oy - d * 0.37} {w * 0.58},{oy + d * 0.37} {w * 0.42},{oy + d * 0.29}" fill="{OR}" opacity="0.95"/>')
    parts.append(f'<text x="{w * 0.25}" y="{oy + 8}" font-family="Montserrat" font-weight="900" font-size="30" fill="#3f6b36" transform="rotate(-24 {w * 0.25} {oy})">100</text>')
    return (f'<svg viewBox="0 {-60} {w} {300}" style="position:absolute;left:{x}px;top:{y}px;width:{w * s}px;height:{300 * s}px;overflow:visible;'
            f'filter:drop-shadow(0 24px 22px #000b);z-index:2">{"".join(parts)}</svg>')


def kugel(x, y, zahl, farbe, gr=200):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{gr}px;border-radius:50%;z-index:2;'
            f'background:radial-gradient(circle at 32% 28%,#ffffffcc 0 8%,{farbe} 30%,#000 115%);box-shadow:0 30px 40px #000b, 0 0 50px {farbe}55;'
            f'display:flex;align-items:center;justify-content:center"><div style="width:{gr * 0.5:.0f}px;height:{gr * 0.5:.0f}px;border-radius:50%;'
            f'background:radial-gradient(circle at 40% 35%,#fff,#ddd);color:#111;font-weight:900;font-size:{gr * 0.25:.0f}px;display:flex;align-items:center;justify-content:center">{zahl}</div></div>')


def pill(x, y, text, farbe=OR, gr=56, dreh=0):
    tc = "#111" if farbe in (OR, OR_HELL, GRUEN, "#ffc533") else "#fff"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;padding:8px 30px 12px;border-radius:20px;background:{farbe};color:{tc};font-weight:900;'
            f'font-size:{gr}px;white-space:nowrap;box-shadow:0 0 40px {farbe}99;transform:rotate({dreh}deg);z-index:3">{text}</div>')


PFOTE = ('<svg viewBox="0 0 100 100" style="width:62%;height:62%"><ellipse cx="50" cy="66" rx="22" ry="18" fill="#fff"/>'
         '<ellipse cx="26" cy="42" rx="9" ry="12" fill="#fff"/><ellipse cx="42" cy="28" rx="9" ry="12" fill="#fff"/>'
         '<ellipse cx="58" cy="28" rx="9" ry="12" fill="#fff"/><ellipse cx="74" cy="42" rx="9" ry="12" fill="#fff"/></svg>')


def badge(x, y, gr=150):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{gr}px;border-radius:50%;background:{OR};'
            f'box-shadow:0 0 0 8px #0e1012, 0 0 40px {OR}aa;display:flex;align-items:center;justify-content:center;z-index:4">{PFOTE}</div>')


def seite(here, inhalte, tiktok=False, glow=("78%", "55%")):
    W, H = (1080, 1920) if tiktok else (1920, 1080)
    szenen = "\n".join(f'<div id="v{i}" class="scene clip" data-start="{i}" data-duration="1" data-track-index="1">{h}</div>' for i, h in enumerate(inhalte))
    (Path(here) / "index.html").write_text(f"""<!doctype html>
<html lang="de" data-resolution="{"portrait" if tiktok else "landscape"}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: {BG}; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: Montserrat, sans-serif; overflow: hidden;
        background: radial-gradient(ellipse at {glow[0]} {glow[1]}, #ff8a1f40 0%, #ff8a1f10 35%, transparent 60%),
                    radial-gradient(ellipse at 50% 50%, #1b1f22 0%, {BG} 75%); }}
      #raster {{ position: absolute; inset: 0; background-image: linear-gradient(#ffffff0d 2px, transparent 2px), linear-gradient(90deg, #ffffff0d 2px, transparent 2px);
        background-size: 96px 96px; }}
      .scene {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{len(inhalte)}" data-width="{W}" data-height="{H}">
      <div id="raster"></div>
{szenen}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#root", {{ opacity: 1 }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")


def export(proj, name):
    """Baut beide Varianten, macht Snapshots und speichert JPGs in renders/thumbnails/."""
    proj = Path(proj).resolve()
    ziel = proj.parent.parent / "renders" / "thumbnails"
    for modus, zeiten, namen in (("", "0.5,1.5,2.5", [f"{name}-1", f"{name}-2", f"{name}-3"]), ("tiktok", "0.5", [f"{name}-tiktok"])):
        subprocess.run([sys.executable, "build.py"] + ([modus] if modus else []), cwd=proj, check=True)
        out = subprocess.run(["npx", "hyperframes", "snapshot", f"--at={zeiten}", "--no-end"], cwd=proj, capture_output=True, text=True).stdout
        pngs = sorted(l.strip() for l in out.splitlines() if l.strip().endswith(".png"))
        for p, n in zip(pngs, namen):
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(proj / p), "-q:v", "2", str(ziel / f"{n}.jpg")], check=True)
            print("→", ziel / f"{n}.jpg")


if __name__ == "__main__" and sys.argv[1:2] == ["export"]:
    export(sys.argv[2], sys.argv[3])
