#!/usr/bin/env python3
"""Cover-Stil SCHWARZ (Nutzer 24.11.: „hochwertiger“): schwarzer Hintergrund, Neon-Zahlen, Gold-Münze, leuchtende Kurve, rote/grüne Schilder, orange Pille.
Nutzung: import cover_dark as cd; cd.speichern(cd.BG + ..., ziel). Vorbild: videos/crash-usa-schulden/covers_neu.py (Variante D)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cover_hell as ch  # noqa: E402

G, R, O, D = "#22c55e", "#ef3b3b", "#f28a1e", "#1d2330"
BG = ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 70%,#22080c 0%,#08090d 45%,#000 100%);z-index:0"></div>'
      '<div style="position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:90px 90px;z-index:0"></div>')
BG_GRUEN = BG.replace("#22080c", "#06210f")


def coin(x, y, d, z=2, rot=0, zeichen="$", farbe="#6b4200"):
    f = d / 700
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;transform:rotate({rot}deg);'
            f'background:radial-gradient(circle at 35% 30%,#fff3b0 0%,#f7c948 28%,#c98a0b 70%,#8a5a00 100%);'
            f'box-shadow:0 {40*f:.0f}px {90*f:.0f}px #000c,inset 0 0 0 {26*f:.0f}px #e0a21a,inset 0 0 0 {40*f:.0f}px #8a5a00,inset 0 0 {90*f:.0f}px #fff6;z-index:{z}">'
            f'<div style="text-align:center;font-family:Arial,Helvetica,sans-serif;font-weight:900;font-size:{430*f:.0f}px;line-height:{d}px;color:{farbe};text-shadow:0 {8*f:.0f}px 0 #fff6">{zeichen}</div>'
            f'<div style="position:absolute;inset:0;border-radius:50%;background:linear-gradient(135deg,#ffffff66 0%,transparent 35%)"></div></div>')


def zahnrad(x, y, d, z=2):
    """Goldenes Zahnrad (Roboter/Technik)."""
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;z-index:{z};filter:drop-shadow(0 30px 50px #000c)" viewBox="0 0 700 700"><defs>'
            f'<radialGradient id="gg" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#fff3b0"/><stop offset=".3" stop-color="#f7c948"/><stop offset=".7" stop-color="#c98a0b"/><stop offset="1" stop-color="#8a5a00"/></radialGradient></defs>'
            f'<circle cx="350" cy="350" r="285" fill="none" stroke="url(#gg)" stroke-width="95" stroke-dasharray="58 58.5"/>'
            f'<circle cx="350" cy="350" r="235" fill="url(#gg)"/><circle cx="350" cy="350" r="120" fill="#0a0a0f" stroke="#8a5a00" stroke-width="22"/>'
            f'<circle cx="350" cy="350" r="235" fill="none" stroke="#ffffff55" stroke-width="6"/></svg>')


def kurve(x, y, w, h, pts, z=3, dick=16, farbe=R, hell="#ff6b6b", pfeil=True):
    p = " L".join(f"{a*w:.0f} {b*h:.0f}" for a, b in pts)
    ex, ey = pts[-1][0] * w, pts[-1][1] * h
    pf = f'<polygon points="{ex+22:.0f},{ey+30:.0f} {ex-50:.0f},{ey-22:.0f} {ex-6:.0f},{ey+48:.0f}" fill="{hell}"/>' if pfeil else ""
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};overflow:visible" viewBox="0 0 {w} {h}"><defs><filter id="g{y}"><feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<path d="M{p}" fill="none" stroke="{farbe}" stroke-width="{dick*2.4:.0f}" stroke-linejoin="round" stroke-linecap="round" filter="url(#g{y})" opacity=".9"/>'
            f'<path d="M{p}" fill="none" stroke="{hell}" stroke-width="{dick}" stroke-linejoin="round" stroke-linecap="round"/>{pf}</svg>')


def pille(y, text):
    return (f'<div style="position:absolute;top:{y}px;width:1080px;display:flex;justify-content:center;z-index:6"><span style="padding:18px 56px;border-radius:80px;background:{O};'
            f'color:#fff;font-weight:900;font-size:54px;box-shadow:0 0 50px {O}88;white-space:nowrap">{text}</span></div>')


def kopf(zeilen, y=110, gr=104):
    """zeilen = [(text, farbe|None)] – große weiße Überschrift mit Neon-Akzent."""
    t = "<br/>".join(f'<span style="color:{f};text-shadow:0 0 40px {f}">{tx}</span>' if f else tx for tx, f in zeilen)
    return (f'<div style="position:absolute;top:{y}px;width:1080px;text-align:center;font-weight:900;font-size:{gr}px;line-height:1.02;color:#fff;letter-spacing:-2px;z-index:5;'
            f'text-shadow:0 8px 30px #000">{t}</div>')


def neon(y, text, farbe=G, gr=166, unter=None):
    u = f'<div style="font-weight:800;font-size:44px;color:#cbd5e1;letter-spacing:4px;margin-top:4px">{unter}</div>' if unter else ""
    return (f'<div style="position:absolute;left:40px;top:{y}px;width:1000px;text-align:center;z-index:5"><div style="font-weight:900;font-size:{gr}px;line-height:1.05;color:{farbe};'
            f'white-space:nowrap;text-shadow:0 0 50px {farbe}99">{text}</div>{u}</div>')


def schild(x, y, text, farbe=G, rot=0, gr=62):
    schrift = "#fff" if farbe == R else "#052e12"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:6;transform:rotate({rot}deg);white-space:nowrap;padding:16px 34px;background:{farbe};color:{schrift};'
            f'font-weight:900;font-size:{gr}px;border-radius:16px;box-shadow:0 16px 40px #000a">{text}</div>')


def speichern(inhalt, ziel):
    ch.speichern(inhalt, ziel)
