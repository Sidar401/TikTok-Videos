"""NEUES FORMAT ab 19.11. (Nutzer): heller Nachrichten-Look nach Vorbild Eulen-Kanal.
Nutzung im build.py (nach glow_short.build):
    import news_look as nl
    K.SZ.append((0.0, K.dauer, nl.kopf("BÖRSENNEWS", "19.11.2026"), lambda a, d: "", 8))
    build(HERE, K.SZ, K.SFX); nl.hell(HERE)
Bausteine: nl.CSS (einmal in der ersten Szene), karte(), zeile(), kachel_raster(), logo_frei(), kurve_karte().
"""
import random
from pathlib import Path

G, R, DUNKEL, ORANGE = "#22a35a", "#d23c3c", "#1d2330", "#f28a1e"


def _netz():
    rnd = random.Random(3)
    pts = [(rnd.randint(0, 1080), rnd.randint(200, 1900)) for _ in range(70)]
    s = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="none" stroke="#b9bec6" stroke-width="2"/>' for x, y in pts)
    for i, (x, y) in enumerate(pts):
        for a, b in pts[i + 1:i + 4]:
            if abs(a - x) + abs(b - y) < 420:
                s += f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="#c9ced5" stroke-width="1.5"/>'
    return f'<svg style="position:absolute;inset:0;width:1080px;height:1920px;opacity:.75" viewBox="0 0 1080 1920">{s}</svg>'


CSS = f"""<style>
.nk-karte {{ position:absolute; background:#ffffff; border:2px solid #e2e5ea; border-radius:12px; box-shadow:0 18px 40px #0000001a; padding:34px 40px; z-index:4; }}
.nk-kt {{ font-weight:700; font-size:42px; color:{DUNKEL}; padding-bottom:20px; border-bottom:2px solid #e8eaee; margin-bottom:12px; }}
.nk-row {{ display:flex; align-items:center; font-size:40px; color:#3a414c; padding:20px 0; white-space:nowrap; }}
.nk-row .v {{ margin-left:auto; font-weight:800; }}
.nk-ok {{ color:{G}; font-size:46px; margin-left:26px; }}
.nk-kachel {{ display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; border-radius:8px; height:200px; }}
.nk-kachel img {{ max-width:200px; max-height:84px; }}
.nk-kachel .nk-p {{ font-weight:800; font-size:44px; }}
.nk-gross {{ position:absolute; left:0; width:1080px; text-align:center; font-weight:900; color:{DUNKEL}; z-index:4; }}
</style>"""


def kopf(rechts="BÖRSENNEWS", datum=""):
    return (f'<div id="kopf" style="position:absolute;left:0;top:150px;width:1080px;height:120px;background:linear-gradient(90deg,#fbe9e9,#fdf6e3);'
            f'border-bottom:2px solid #e4e6ea;display:flex;align-items:center;padding:0 50px;gap:18px;z-index:8">'
            f'<img src="assets/beagle.png" style="width:86px;height:86px;border-radius:50%;border:3px solid #fff;box-shadow:0 4px 10px #0002"/>'
            f'<div style="font-weight:700;font-size:40px;color:{DUNKEL}">HundeFinanzTv</div>'
            f'<div style="margin-left:auto;font-size:34px;color:{DUNKEL};font-weight:800;letter-spacing:1px;white-space:nowrap">{rechts}'
            f'<span style="font-weight:500;color:#555c66;margin-left:12px">{datum}</span></div></div>')


def karte(id_, titel, inhalt, x=110, y=640, w=860):
    return f'<div id="{id_}" class="nk-karte" style="left:{x}px;top:{y}px;width:{w}px"><div class="nk-kt">{titel}</div>{inhalt}</div>'


def zeile(id_, links, wert, farbe=DUNKEL, haken=""):
    h = f'<span class="nk-ok">{haken}</span>' if haken else ""
    return f'<div id="{id_}" class="nk-row">{links}<span class="v" style="color:{farbe}">{wert}</span>{h}</div>'


def logo_frei(id_, datei, x, y, w):
    return f'<img id="{id_}" src="assets/logos/{datei}" alt="" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:4"/>'


def kachel(id_, datei, text, gut):
    f = G if gut else R
    img = f'<img src="assets/logos/{datei}"/>' if datei else ""
    return f'<div id="{id_}" class="nk-kachel" style="background:{"#e3f5e9" if gut else "#fbe6e6"}">{img}<div class="nk-p" style="color:{f}">{text}</div></div>'


def hell(here):
    """Nach glow_short.build: dunklen Glow-Look in index.html auf hellen Nachrichten-Look umstellen."""
    p = Path(here) / "index.html"
    s = p.read_text()
    ersatz = [
        ("background: radial-gradient(ellipse at 50% 42%, #ff8a1f33 0%, #ff8a1f0d 38%, transparent 62%), radial-gradient(ellipse at 50% 50%, #1b1f22 0%, #0e1012 75%);",
         "background: linear-gradient(180deg,#f7f8fa,#eceef2);"),
        ("background: #0e1012; }", "background: #eef0f3; }"),
        ('<div id="raster"></div>', f'<div id="raster">{_netz()}</div>'),
        ("#logo {", "#logo { display:none; "),
        ("#brand {", "#brand { display:none; "),
        ("color: #fff; text-shadow: 0 6px 0 #000, 0 0 30px #000; }\n",
         f"color: {ORANGE}; -webkit-text-stroke: 3px #ffffff; paint-order: stroke fill; text-shadow: 0 6px 14px #0000002e; }}\n"),
        ('{ color: "#ffffff", scale: 1 }', f'{{ color: "{ORANGE}", scale: 1 }}'),
        ('{ color: "#ff8a1f", scale: 1.06, duration: 0.08 }', f'{{ color: "{DUNKEL}", scale: 1.06, duration: 0.08 }}'),
        ('tl.to("#w', 'tl.to("#w'),
    ]
    for a, b in ersatz:
        s = s.replace(a, b)
    s = s.replace('{ color: "#ffffff", scale: 1, duration: 0.08 }', f'{{ color: "{ORANGE}", scale: 1, duration: 0.08 }}')
    p.write_text(s)


def ohne_untertitel(here, bis):
    """Untertitel-Boxen, die vor `bis` Sekunden starten, entfernen (z. B. erster Satz mit großem Logo, Nutzer 19.11.)."""
    import re
    p = Path(here) / "index.html"
    s = p.read_text()
    weg = [m.group(1) for m in re.finditer(r'<div id="c(\d+)" class="cap clip" data-start="([\d.]+)"', s) if float(m.group(2)) < bis]
    zeilen = []
    for z in s.split("\n"):
        if any(f'id="c{n}" class="cap clip"' in z or f'"#w{n}-' in z for n in weg):
            continue
        zeilen.append(z)
    p.write_text("\n".join(zeilen))


def foto(id_, key, deckkraft=0.72):
    """Echtes Foto hell und weich als Szenen-Hintergrund (wie Eulen-Kanal). Datei per Kit(hgs=[key]) nach assets/hg/ kopieren."""
    return (f'<img id="{id_}" src="assets/hg/{key}.jpg" alt="" style="position:absolute;left:-30px;top:-30px;width:1140px;height:1980px;object-fit:cover;'
            f'filter:blur(3px) grayscale(.25);z-index:0"/>'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(247,248,250,{deckkraft + 0.12:.2f}),rgba(236,238,242,{deckkraft:.2f}));z-index:1"></div>')


def kurve_hinten(id_):
    """Orange Börsen-Kurve hinter dem Logo im Einstieg. JS: draw("#<id>-p", t, 1.2)."""
    pts = [(0, .5), (1, .62), (2, .55), (3, .8), (4, .72), (5, .92), (6, .6), (7, .45), (8, .3), (9, .35), (10, .2)]
    d = "M" + " L".join(f"{i * 108} {560 + 360 * (1 - v)}" for i, v in pts)
    return (f'<svg id="{id_}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:2"><defs><linearGradient id="{id_}-g" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{ORANGE}" stop-opacity=".22"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient></defs>'
            f'<path id="{id_}-f" d="{d} L1080 1100 L0 1100 Z" fill="url(#{id_}-g)"/><path id="{id_}-p" d="{d}" fill="none" stroke="{ORANGE}" stroke-width="9" stroke-linejoin="round"/></svg>')


def mini_kachel(id_, x, y, oben, wert, farbe, dreh):
    """Kleine Zahlen-Kachel im Einstieg. oben = Logo-Datei (assets/logos) oder Text."""
    o = f'<img src="assets/logos/{oben}" style="max-width:200px;max-height:54px"/>' if "." in oben else f'<div style="font-weight:900;font-size:44px;color:{DUNKEL}">{oben}</div>'
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:280px;padding:22px 0;background:#fff;border:2px solid #e2e5ea;border-radius:12px;'
            f'box-shadow:0 14px 30px #0002;text-align:center;transform:rotate({dreh}deg);z-index:5">{o}<div style="font-weight:800;font-size:50px;color:{farbe};margin-top:8px">{wert}</div></div>')
