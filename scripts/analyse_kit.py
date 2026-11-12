"""Analyse-Baukasten (Nutzer 10.11.: „Skizzen, Analysen … professionell, nicht immer das Gleiche“).

Ergänzt glow_short (Dark Glow) um: echte Logo-Karten, Logo-Netz, handgezeichnete Pfeile/Kreise (zeichnen sich selbst),
Handschrift-Notizen (Caveat), Analyse-Karten mit Millimeterpapier, Balken mit Notizen, Donut, Preis-Spanne, Kurs-Laufband,
Aktien-Raster, Server-Racks, Ablauf-Kästen, Stempel.

  from analyse_kit import *
  KIT_CSS in die ERSTE Szene packen (Schrift + Klassen). Vorher kit_assets(HERE, ["anthropic", "nvidia", …]) aufrufen
  (kopiert Logos aus brand/logos + Caveat-Schrift nach assets/).
  JS: draw("#id-p", t, dauer) zeichnet Pfeile/Kreise; pop/slam wie gewohnt; kit-eigene JS-Helfer stehen bei der Funktion.
Koordinaten: 1080×1920. Freie Bildfläche (9:16) ca. y 420–1300 (darüber Logo/Name, darunter Untertitel).
"""
import math
import shutil
from pathlib import Path

from glow_short import GOLD, GRUEN, OR, ROT

GELB = "#ffd54a"
GRAU = "#8a949c"
WURZEL = Path(__file__).resolve().parent.parent

KIT_CSS = ('<style>@font-face { font-family: Caveat; src: url(assets/caveat.woff2); font-weight: 700; }'
           ' .hand { font-family: Caveat, cursive; font-weight: 700; line-height: 1; white-space: nowrap; }'
           ' .mono { font-family: "JetBrains Mono", monospace; font-weight: 800; }</style>')


def kit_assets(here, logos):
    a = Path(here) / "assets"
    (a / "logos").mkdir(parents=True, exist_ok=True)
    shutil.copy(WURZEL / "brand/fonts/caveat-700.woff2", a / "caveat.woff2")
    for l in logos:
        q = WURZEL / "brand/logos" / f"{l}.svg"
        if q.exists():
            shutil.copy(q, a / "logos" / f"{l}.svg")


def logo_karte(id_, name, x, y, w, h, pad=0.14, glow=OR, text=None, farbe="#111"):
    """Weiße Karte mit Original-Logo (assets/logos/<name>.svg). text= Wortmarke, falls kein Logo vorhanden."""
    inhalt = (f'<img src="assets/logos/{name}.svg" alt="" style="max-width:100%;max-height:100%;display:block"/>' if text is None else
              f'<div style="font-weight:900;font-size:{h * 0.5:.0f}px;color:{farbe};letter-spacing:-2px">{text}</div>')
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;padding:{h * pad:.0f}px {w * 0.08:.0f}px;'
            f'border-radius:{min(w, h) * 0.18:.0f}px;background:#fff;box-shadow:0 0 50px {glow}66, 0 20px 40px #000a;display:flex;align-items:center;'
            f'justify-content:center;z-index:3">{inhalt}</div>')


def _svg(id_, inhalt, z=4):
    return f'<svg id="{id_}" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible;z-index:{z};pointer-events:none">{inhalt}</svg>'


def pfeil(id_, x1, y1, x2, y2, bogen=0.25, farbe=OR, breite=9):
    """Handgezeichneter Bogen-Pfeil. JS: draw("#id-p", t, 0.5); pop("#id-k", t + 0.45)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bogen, my + dx * bogen
    w = math.atan2(y2 - cy, x2 - cx)
    k = 34
    a1 = (x2 - k * math.cos(w - 0.5), y2 - k * math.sin(w - 0.5))
    a2 = (x2 - k * math.cos(w + 0.5), y2 - k * math.sin(w + 0.5))
    st = f'fill="none" stroke="{farbe}" stroke-width="{breite}" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 10px {farbe})"'
    return _svg(id_, f'<path id="{id_}-p" d="M{x1} {y1} Q{cx:.0f} {cy:.0f} {x2} {y2}" {st}/>'
                     f'<path id="{id_}-k" d="M{a1[0]:.0f} {a1[1]:.0f} L{x2} {y2} L{a2[0]:.0f} {a2[1]:.0f}" {st}/>')


def kreis(id_, cx, cy, rx, ry, farbe=OR, breite=8):
    """Handgezeichneter Kreis (leicht unrund, überlappt). JS: draw("#id-p", t, 0.5)."""
    pts = []
    for i in range(0, 61):
        a = -2.2 + i / 60 * (2 * math.pi + 0.5)
        r = 1 + 0.04 * math.sin(a * 3 + 1) + 0.02 * math.cos(a * 5)
        pts.append(f"{cx + rx * r * math.cos(a):.0f} {cy + ry * r * math.sin(a) * (1 + 0.03 * math.cos(a)):.0f}")
    return _svg(id_, f'<path id="{id_}-p" d="M{" L".join(pts)}" fill="none" stroke="{farbe}" stroke-width="{breite}" stroke-linecap="round" '
                     f'stroke-linejoin="round" style="filter:drop-shadow(0 0 10px {farbe})"/>', 5)


def unterstrich(id_, x, y, w, farbe=OR, breite=9):
    d = f"M{x} {y} Q{x + w * 0.3} {y + 10} {x + w * 0.55} {y + 2} T{x + w} {y + 6}"
    return _svg(id_, f'<path id="{id_}-p" d="{d}" fill="none" stroke="{farbe}" stroke-width="{breite}" stroke-linecap="round" style="filter:drop-shadow(0 0 8px {farbe})"/>', 5)


def hand(id_, text, x, y, size=70, farbe=GELB, dreh=-4, mitte=False):
    """Handschrift-Notiz. mitte=True: x ist die Mitte."""
    tf = f"translateX(-50%) rotate({dreh}deg)" if mitte else f"rotate({dreh}deg)"
    return (f'<div id="{id_}" class="hand" style="position:absolute;left:{x}px;top:{y}px;font-size:{size}px;color:{farbe};'
            f'transform:{tf};text-shadow:0 0 24px {farbe}88, 0 4px 0 #000;z-index:6">{text}</div>')


def zettel(id_, text, x, y, w, size=64, farbe=GELB, dreh=-3):
    """Klebezettel mit Handschrift."""
    return (f'<div id="{id_}" class="hand" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:34px 30px 40px;background:{farbe};color:#1a1a1a;'
            f'font-size:{size}px;line-height:1.05;white-space:normal;text-align:center;transform:rotate({dreh}deg);box-shadow:0 24px 40px #000b, 0 0 60px {farbe}44;'
            f'border-radius:6px 6px 26px 6px;z-index:4">'
            f'<div style="position:absolute;left:50%;top:-18px;width:140px;height:38px;margin-left:-70px;background:#ffffff55;transform:rotate(2deg)"></div>{text}</div>')


def karte(id_, x, y, w, h, titel="", untertitel="", farbe=OR):
    """Analyse-Karte: dunkel, Millimeterpapier, Titelzeile. Inhalt separat absolut darüber legen."""
    kopf = (f'<div style="position:absolute;left:36px;top:26px;font-weight:900;font-size:40px;color:#fff">{titel}</div>'
            f'<div class="mono" style="position:absolute;left:36px;top:80px;font-size:26px;color:{GRAU}">{untertitel}</div>') if titel else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;background-color:#14181bee;'
            f'background-image:linear-gradient(#ffffff10 1px, transparent 1px),linear-gradient(90deg,#ffffff10 1px,transparent 1px),'
            f'linear-gradient(#ffffff06 1px, transparent 1px),linear-gradient(90deg,#ffffff06 1px,transparent 1px);'
            f'background-size:60px 60px,60px 60px,12px 12px,12px 12px;border:3px solid {farbe}66;box-shadow:0 0 60px {farbe}33, 0 30px 60px #000;z-index:2">{kopf}</div>')


def balken(id_, x, basis, w, h, farbe, oben="", unten="", oben_gr=56):
    """Balken wächst von unten. JS: wachs("#id", t)."""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{basis - h}px;width:{w}px;height:{h}px;border-radius:16px 16px 4px 4px;'
            f'background:linear-gradient(180deg,{farbe},{farbe}99);box-shadow:0 0 40px {farbe}77;transform-origin:50% 100%;z-index:3"></div>'
            f'<div id="{id_}-o" style="position:absolute;left:{x - 150}px;width:{w + 300}px;top:{basis - h - oben_gr - 26}px;text-align:center;font-weight:900;'
            f'font-size:{oben_gr}px;color:{farbe};text-shadow:0 0 30px {farbe}99;z-index:4">{oben}</div>'
            f'<div class="mono" style="position:absolute;left:{x - 100}px;width:{w + 200}px;top:{basis + 14}px;text-align:center;font-size:32px;color:#ffffffcc;z-index:4">{unten}</div>')


WACHS_JS = 'const wachs = (sel, at, dur) => tl.fromTo(sel, { scaleY: 0 }, { scaleY: 1, duration: dur || 0.6, ease: "power3.out" }, at);'


def _bogen(cx, cy, r, a0, a1):
    p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
    gross = 1 if a1 - a0 > math.pi else 0
    return f"M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 {gross} 1 {p1[0]:.1f} {p1[1]:.1f}"


def donut(id_, cx, cy, r, teile, dicke=70):
    """teile = [(anteil 0..1, farbe)]. JS: draw("#id-0", t, 0.6); draw("#id-1", t+0.6, 0.4) …"""
    s, a = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ffffff14" stroke-width="{dicke}"/>'], -math.pi / 2
    for i, (anteil, f) in enumerate(teile):
        b = a + anteil * 2 * math.pi - 0.03
        s.append(f'<path id="{id_}-{i}" d="{_bogen(cx, cy, r, a, b)}" fill="none" stroke="{f}" stroke-width="{dicke}" style="filter:drop-shadow(0 0 14px {f}88)"/>')
        a = b + 0.03
    return _svg(id_, "".join(s), 3)


def spanne(id_, x, y, w, von, bis, links, rechts, farbe=GRUEN):
    """Preis-Spanne als Regler: grauer Strahl, leuchtender Bereich. JS: spann("#id", t)."""
    a, b = w * von, w * bis
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:30px;border-radius:15px;background:#ffffff1a;z-index:3">'
            f'<div id="{id_}-f" style="position:absolute;left:{a}px;width:{b - a}px;top:0;height:30px;border-radius:15px;background:{farbe};box-shadow:0 0 40px {farbe};transform-origin:0 50%"></div>'
            f'<div id="{id_}-a" style="position:absolute;left:{a - 26}px;top:-11px;width:52px;height:52px;border-radius:50%;background:#fff;border:7px solid {farbe}"></div>'
            f'<div id="{id_}-b" style="position:absolute;left:{b - 26}px;top:-11px;width:52px;height:52px;border-radius:50%;background:#fff;border:7px solid {farbe}"></div>'
            f'<div class="mono" style="position:absolute;left:{a - 150}px;width:300px;top:60px;text-align:center;font-size:56px;color:#fff">{links}</div>'
            f'<div class="mono" style="position:absolute;left:{b - 150}px;width:300px;top:60px;text-align:center;font-size:56px;color:#fff">{rechts}</div></div>')


SPANN_JS = ('const spann = (sel, at) => { tl.fromTo(sel + "-f", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, at);'
            ' tl.fromTo(sel + "-a", { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(2)" }, at);'
            ' tl.fromTo(sel + "-b", { x: -200, scale: 0 }, { x: 0, scale: 1, duration: 0.6, ease: "power3.out" }, at); };')


def ticker(id_, eintraege, top, farbe=GRUEN):
    """Kurs-Laufband. eintraege = [(text, farbe|None)]. JS: lauf("#id", t, dauer)."""
    teil = "".join(f'<span style="margin:0 34px;color:{f or "#fff"}">{tx}</span><span style="color:{OR}">●</span>' for tx, f in eintraege)
    return (f'<div id="{id_}" style="position:absolute;left:0;top:{top}px;width:1080px;height:86px;background:#0b0d0ef0;border-top:3px solid {farbe}66;'
            f'border-bottom:3px solid {farbe}66;overflow:hidden;z-index:4"><div id="{id_}-s" class="mono" style="position:absolute;left:0;top:14px;white-space:nowrap;font-size:44px">'
            f'{teil * 4}</div></div>')


LAUF_JS = 'const lauf = (sel, at, dur) => tl.fromTo(sel + "-s", { x: 0 }, { x: -1400, duration: dur, ease: "none" }, at);'


def raster(id_, x, y, spalten, zeilen, gr, abstand, farbe=OR, hell=None):
    """Aktien-Raster aus kleinen Quadraten (Klasse id-q). JS: tl.fromTo("#id .q", {scale:0}, {scale:1, stagger:0.004 …})."""
    q = []
    for r in range(zeilen):
        for c in range(spalten):
            f = hell if hell and (r * spalten + c) % 7 == 3 else farbe
            q.append(f'<div class="q" style="position:absolute;left:{c * (gr + abstand)}px;top:{r * (gr + abstand)}px;width:{gr}px;height:{gr}px;border-radius:{gr * 0.22:.0f}px;background:{f};box-shadow:0 0 10px {f}88"></div>')
    return f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;z-index:3">{"".join(q)}</div>'


def racks(id_, x, y, n=4, w=180, h=420, abstand=40):
    """Server-Racks mit LEDs (Klasse led). JS: blink("#id", t)."""
    out = []
    for i in range(n):
        leds = "".join(f'<div class="led" style="position:absolute;left:{24 + (k % 3) * 46}px;top:{30 + (k // 3) * 56}px;width:30px;height:12px;border-radius:6px;'
                       f'background:{(GRUEN, OR, "#4d8ff0")[(i + k) % 3]};box-shadow:0 0 12px {(GRUEN, OR, "#4d8ff0")[(i + k) % 3]}"></div>' for k in range(21))
        out.append(f'<div class="rk" style="position:absolute;left:{i * (w + abstand)}px;top:0;width:{w}px;height:{h}px;border-radius:18px;background:linear-gradient(180deg,#22282c,#15191b);'
                   f'border:4px solid #3a4248;box-shadow:0 30px 50px #000">{leds}</div>')
    return f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;z-index:2">{"".join(out)}</div>'


BLINK_JS = ('const blink = (sel, at) => { tl.fromTo(sel + " .rk", { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, stagger: 0.08, ease: "back.out(1.6)" }, at);'
            ' tl.fromTo(sel + " .led", { opacity: 0.2 }, { opacity: 1, duration: 0.18, stagger: { each: 0.02, repeat: 7, yoyo: true }, ease: "none" }, at + 0.4); };')


def kasten(id_, text, x, y, w, h, farbe=OR, size=50, unter=""):
    """Ablauf-Kasten (Umriss, leuchtend)."""
    u = f'<div class="mono" style="font-size:26px;color:{GRAU};margin-top:8px">{unter}</div>' if unter else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:26px;border:6px solid {farbe};background:#14181b;'
            f'box-shadow:0 0 50px {farbe}55;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;z-index:3">'
            f'<div style="font-weight:900;font-size:{size}px;color:#fff;line-height:1.05">{text}</div>{u}</div>')


def stempel(id_, text, x, y, farbe=ROT, size=78, dreh=-10):
    """Stempel. JS: stempeln("#id", t)."""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:12px 34px;border:9px solid {farbe};border-radius:18px;color:{farbe};'
            f'font-weight:900;font-size:{size}px;letter-spacing:4px;white-space:nowrap;transform:rotate({dreh}deg);text-shadow:0 0 20px {farbe}88;box-shadow:0 0 30px {farbe}55, inset 0 0 30px {farbe}33;'
            f'background:#0e1012cc;z-index:6">{text}</div>')


STEMPEL_JS = 'const stempeln = (sel, at) => tl.fromTo(sel, { scale: 3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, at);'


def linie(id_, werte, x, y, w, h, farbe=ROT, fuellung=True, punkte=()):
    """Kurs-Linie (werte 0..1, oben=1). punkte=[(index, text)] Wert-Pillen. JS: draw("#id-p", t, 1.0)."""
    n = len(werte) - 1
    P = [(x + w * i / n, y + h * (1 - v)) for i, v in enumerate(werte)]
    d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in P)
    s = []
    if fuellung:
        s.append(f'<path id="{id_}-f" d="{d} L{P[-1][0]:.0f} {y + h} L{P[0][0]:.0f} {y + h} Z" fill="{farbe}" opacity="0.14"/>')
    s.append(f'<path id="{id_}-p" d="{d}" fill="none" stroke="{farbe}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round" style="filter:drop-shadow(0 0 14px {farbe})"/>')
    html = _svg(id_, "".join(s), 3)
    for k, (i, txt) in enumerate(punkte):
        px, py = P[i]
        html += (f'<div id="{id_}-w{k}" class="mono" style="position:absolute;left:{px - 130:.0f}px;width:260px;top:{py - 80:.0f}px;text-align:center;z-index:5">'
                 f'<span style="display:inline-block;padding:6px 16px;border-radius:12px;background:{farbe};color:#111;font-size:34px">{txt}</span></div>')
    return html


def person(id_, name, rolle, x, y, w=300, farbe=OR, foto=None, credit=""):
    """Personen-Karte. foto= Pfad (nur freie Fotos öffentlicher Personen, credit = Lizenzzeile), sonst Silhouette."""
    bild = (f'<div style="width:{w * 0.62:.0f}px;height:{w * 0.62:.0f}px;margin:0 auto;border-radius:50%;overflow:hidden;border:5px solid {farbe};box-shadow:0 0 30px {farbe}88">'
            f'<img src="{foto}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 18%"/></div>') if foto else (
            f'<svg viewBox="0 0 100 100" style="width:{w * 0.5:.0f}px;height:{w * 0.5:.0f}px"><circle cx="50" cy="36" r="20" fill="{farbe}"/>'
            f'<path d="M14 96 Q16 62 50 62 Q84 62 86 96 Z" fill="{farbe}"/></svg>')
    cr = f'<div class="mono" style="font-size:{max(14, w * 0.045):.0f}px;color:#ffffff88;margin-top:10px">{credit}</div>' if credit else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:26px 16px 22px;border-radius:28px;background:#14181b;border:5px solid {farbe};'
            f'box-shadow:0 0 50px {farbe}55;text-align:center;z-index:3">' + bild +
            f'<div style="font-weight:900;font-size:{w * 0.13:.0f}px;color:#fff;margin-top:8px;line-height:1.05">{name}</div>'
            f'<div class="mono" style="font-size:{w * 0.075:.0f}px;color:{GRAU};margin-top:8px">{rolle}</div>{cr}</div>')


def flagge(id_, name, x, y, w, dreh=0):
    return (f'<img id="{id_}" src="assets/logos/{name}.svg" alt="" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:10px;'
            f'outline:4px solid #ffffff55;box-shadow:0 20px 40px #000c;transform:rotate({dreh}deg);z-index:3"/>')


def kalender(id_, monat, tag, x, y, w=260, farbe=ROT, unter=""):
    u = f'<div class="mono" style="font-size:{w * 0.09:.0f}px;color:#555;margin-top:4px">{unter}</div>' if unter else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 0 60px {farbe}66, 0 30px 50px #000;z-index:3;text-align:center">'
            f'<div style="background:{farbe};color:#fff;font-weight:900;font-size:{w * 0.17:.0f}px;padding:12px 0">{monat}</div>'
            f'<div style="font-weight:900;font-size:{w * (0.5 if len(str(tag)) <= 2 else 0.3):.0f}px;color:#111;line-height:1.1;padding:{0 if len(str(tag)) <= 2 else w * 0.08:.0f}px 0 14px">{tag}{u}</div></div>')


def rahmen(html, quer):
    """Für 16:9: Szene (1080×1920-Koordinaten, Inhalt y 420–1300) skaliert in die Bildmitte legen."""
    if not quer:
        return html
    return f'<div class="qbox" style="position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;transform:translate(528px,-186px) scale(0.8)">{html}</div>'


QUER_CSS = '<style>.qbox .t { width: 1080px !important; }</style>'

KIT_JS = " ".join([WACHS_JS, SPANN_JS, LAUF_JS, BLINK_JS, STEMPEL_JS])
__all__ = ["GELB", "GRAU", "KIT_CSS", "KIT_JS", "kit_assets", "logo_karte", "pfeil", "kreis", "unterstrich", "hand", "zettel", "karte",
           "balken", "donut", "linie", "person", "flagge", "kalender", "rahmen", "QUER_CSS", "spanne", "ticker", "raster", "racks", "kasten", "stempel", "GOLD", "GRUEN", "OR", "ROT"]


def laufband_szene(eintraege, dauer, top=388, farbe=None):
    """Dauerhaftes Börsen-Laufband über das GANZE Video (Nutzer 12.11.: Videos mit Laufband gingen viral).
    eintraege = [(text, farbe|None)], echte, geprüfte Werte (z. B. ("NVDA ▼ −13 %", ROT)). In SZENEN als letzten Eintrag anhängen:
    SZENEN.append(laufband_szene([...], DAUER))"""
    farbe = farbe or GRUEN
    teil = "".join(f'<span style="margin:0 30px;color:{f or "#fff"}">{tx}</span><span style="color:{OR}">●</span>' for tx, f in eintraege)
    html = (f'<div id="lb" style="position:absolute;left:0;top:{top}px;width:1080px;height:64px;background:#0b0d0ef2;border-top:3px solid {farbe}55;'
            f'border-bottom:3px solid {farbe}55;overflow:hidden;z-index:8"><div id="lb-s" class="mono" style="position:absolute;left:0;top:9px;white-space:nowrap;font-size:36px">'
            f'{teil * 12}</div></div>')
    return (0.0, dauer, html, lambda a, d: f'tl.fromTo("#lb-s", {{ x: 0 }}, {{ x: {-int(d * 90)}, duration: {d}, ease: "none" }}, 0);', 9)
