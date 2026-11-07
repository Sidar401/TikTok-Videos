"""Bausteine für Longform 16:9 im Dark-Glow-Stil (aus longform-ki-blase): Plaketten in Firmenfarben (keine echten Logos),
Karten, Regel-Karten, Geldsäcke, Pfeile. Vorher `glow_short.querformat()` aufrufen."""
from finanz import BEAGLE
from glow_short import GOLD, GRUEN, OR, ROT, ring

BLAU, NV = "#4d8ff0", "#76b900"
GL = lambda f: f'filter="drop-shadow(0 0 18px {f})"'  # noqa: E731


def svg(id_, inhalt, x, y, w, h, vb, z=2):
    return f'<svg id="{id_}" viewBox="{vb}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;z-index:{z}">{inhalt}</svg>'


# ---------- Firmen-Plaketten (keine echten Logos) ----------
def _icon(firma):
    if firma == "Microsoft":
        return ('<svg viewBox="0 0 22 22" style="width:46px;height:46px"><rect width="10" height="10" fill="#f25022"/><rect x="12" width="10" height="10" fill="#7fba00"/>'
                '<rect y="12" width="10" height="10" fill="#00a4ef"/><rect x="12" y="12" width="10" height="10" fill="#ffb900"/></svg>')
    if firma == "OpenAI":
        return ('<svg viewBox="0 0 40 40" style="width:48px;height:48px"><g fill="none" stroke="#fff" stroke-width="3.2">'
                + "".join(f'<ellipse cx="20" cy="20" rx="16" ry="7" transform="rotate({a} 20 20)"/>' for a in (0, 60, 120)) + '</g></svg>')
    if firma == "Nvidia":
        return (f'<svg viewBox="0 0 40 30" style="width:54px;height:40px"><path d="M2 15 C10 3 30 3 38 15 C30 27 10 27 2 15 Z" fill="none" stroke="{NV}" stroke-width="4"/>'
                f'<circle cx="20" cy="15" r="6" fill="{NV}"/></svg>')
    if firma == "AMD":
        return '<svg viewBox="0 0 30 30" style="width:40px;height:40px"><path d="M4 4 H26 V26 L18 18 V12 H12 Z" fill="#fff"/><path d="M4 12 L12 20 H4 Z" fill="#fff"/></svg>'
    if firma == "Apple":
        return '<svg viewBox="0 0 30 34" style="width:36px;height:42px"><path d="M15 9 C10 6 3 8 3 18 C3 26 9 33 12 33 C14 33 15 32 15 32 C15 32 16 33 18 33 C21 33 27 26 27 18 C27 8 20 6 15 9 Z" fill="#ddd"/><path d="M15 9 C15 5 17 2 21 1" stroke="#ddd" stroke-width="2.5" fill="none"/></svg>'
    return ""


FARBEN = {"SpaceX": ("#ffffff", "#ffffff"), "Microsoft": ("#ffffff", "#00a4ef"), "OpenAI": ("#ffffff", "#ffffff"), "Nvidia": (NV, NV), "Oracle": ("#ffffff", "#c74634"),
          "AMD": ("#ffffff", "#e5e5e5"), "Apple": ("#ffffff", "#bbbbbb")}


def plakette(id_, firma, cx, cy, s=1.0, z=3):
    tf, rand = FARBEN[firma]
    name = {"Oracle": "ORACLE", "Nvidia": "NVIDIA", "AMD": "AMD", "SpaceX": "SPACEX"}.get(firma, firma)
    bg = "#c74634" if firma == "Oracle" else "#111417"
    w, h = 330 * s, 116 * s
    return (f'<div id="{id_}" style="position:absolute;left:{cx - w / 2:.0f}px;top:{cy - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;border-radius:{22 * s:.0f}px;'
            f'background:{bg};border:{5 * s:.0f}px solid {rand};box-shadow:0 0 {40 * s:.0f}px {rand}66;display:flex;align-items:center;justify-content:center;gap:{14 * s:.0f}px;'
            f'z-index:{z}"><div style="transform:scale({s})">{_icon(firma)}</div>'
            f'<span style="font-weight:900;font-size:{50 * s:.0f}px;color:{tf};letter-spacing:{1 if firma in ("Oracle", "Nvidia") else -1}px">{name}</span></div>')


def geldsack(id_, txt, cx, cy, farbe=GOLD, gr=40):
    return (f'<div id="{id_}" style="position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);padding:8px 22px 10px;border-radius:16px;background:{farbe};'
            f'color:#111;font-weight:900;font-size:{gr}px;white-space:nowrap;box-shadow:0 0 30px {farbe}99;z-index:4">{txt}</div>')


def karte(id_, txt, farbe, top, gr=86, w=1300):
    return (f'<div id="{id_}" style="position:absolute;left:{960 - w / 2:.0f}px;top:{top}px;width:{w}px;padding:30px 0 36px;border-radius:30px;background:#16191b;'
            f'border:6px solid {farbe};box-shadow:0 0 60px {farbe}55;text-align:center;font-weight:900;font-size:{gr}px;color:#fff;z-index:2">{txt}</div>')


def regel(n, txt, farbe=OR):
    return (f'<div id="rg{n}" style="position:absolute;left:260px;top:300px;width:1400px;height:380px;border-radius:40px;background:#16191b;border:8px solid {farbe};'
            f'box-shadow:0 0 80px {farbe}55;display:flex;align-items:center;gap:60px;padding:0 70px;z-index:2">'
            f'<div style="flex:none;width:220px;height:220px;border-radius:50%;background:{farbe};color:#111;font-weight:900;font-size:150px;display:flex;align-items:center;justify-content:center">{n}</div>'
            f'<div style="font-weight:900;font-size:92px;line-height:1.05;color:#fff">{txt}</div></div>')


def regel_js(n):
    return lambda a, d: f'tl.fromTo("#rg{n}", {{ x: -1600, rotation: -4 }}, {{ x: 0, rotation: 0, duration: 0.45, ease: "back.out(1.4)" }}, {a});'


PFEIL_AB = (f'<path d="M0 0 L0 120 M-40 80 L0 125 L40 80" fill="none" stroke="{ROT}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')



def beagle_ring(id_, x, y, gr):
    return ring(id_, f'<div style="width:100%;height:100%;border-radius:50%;overflow:hidden">{BEAGLE}</div>', x, y, gr)
