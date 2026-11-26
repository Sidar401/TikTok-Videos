#!/usr/bin/env python3
"""Slideshow-Baukasten DUNKEL (Nutzer 26.11.; Vorbild Bitcoin-Crash-Video 14.11.): abgedunkeltes Code-Foto, oranger Glow, Beagle oben, NEWS-Pille, Neon-Zahlen.
Nutzung: import slide_dark as sd; sd.speichern(sd.kopf("NEWS","26.11.2026") + ..., ziel)"""
import subprocess
import tempfile
from pathlib import Path

R_ = str(Path(__file__).resolve().parent.parent) + "/"
L = R_ + "brand/logos/"
BEAGLE = "file://" + R_ + "videos/boerse-25-11/assets/beagle.png"
G, ROT, O, W = "#22c55e", "#ff4d4d", "#f28a1e", "#ffffff"
FONT = f"file://{R_}brand/fonts/montserrat-900.woff2"
CSS = (f"<style>@font-face{{font-family:Montserrat;font-weight:100 900;src:url({FONT})}}*{{margin:0;box-sizing:border-box}}"
       "body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Montserrat,sans-serif;background:#0b0c0e;color:#fff}"
       ".glas{position:absolute;background:linear-gradient(180deg,#14171bdd,#0c0e11ee);border:2px solid #ffffff22;border-radius:22px;box-shadow:0 0 60px #000a,inset 0 0 40px #ffffff08;padding:34px 40px;z-index:4}</style>")


def bg(foto="frei-code-monitor.jpg"):
    return (f'<img src="file://{R_}brand/hintergruende/{foto}" style="position:absolute;left:-60px;top:-30px;width:1200px;height:1980px;object-fit:cover;filter:blur(2px) brightness(.5) saturate(.7);z-index:0"/>'
            '<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,#f28a1e22 0%,#0000 55%),linear-gradient(180deg,#000b 0%,#0008 40%,#000c 100%);z-index:1"></div>')


def kopf(datum="26.11.2026", marke="NEWS", nr=None):
    n = f'<div style="position:absolute;right:70px;top:60px;font-weight:800;font-size:36px;color:#fff;z-index:6">{nr}</div>' if nr else ""
    return (f'<div style="position:absolute;left:0;top:90px;width:1080px;text-align:center;z-index:6"><img src="{BEAGLE}" style="width:230px;height:230px;border-radius:50%;border:8px solid {O};box-shadow:0 0 40px {O}88;"/>'
            f'<div style="font-weight:800;font-size:46px;margin-top:10px;text-shadow:0 4px 12px #000">HundeFinanzTv</div></div>{n}'
            f'<div style="position:absolute;left:60px;top:430px;width:960px;display:flex;align-items:center;justify-content:space-between;z-index:6;border-bottom:3px solid {O}88;padding-bottom:16px">'
            f'<span style="background:{O};color:#111;font-weight:900;font-size:40px;padding:6px 24px;border-radius:10px;letter-spacing:2px">{marke}</span>'
            f'<span style="font-family:monospace;font-weight:700;font-size:40px;color:#fff">{datum}</span></div>')


def txt(t, y, gr, farbe=W, glow=True, extra=""):
    sh = f"text-shadow:0 0 40px {farbe}88,0 6px 20px #000;" if glow and farbe != W else "text-shadow:0 6px 20px #000;"
    return f'<div style="position:absolute;left:40px;top:{y}px;width:1000px;text-align:center;font-weight:900;font-size:{gr}px;line-height:1.08;color:{farbe};z-index:5;{sh}{extra}">{t}</div>'


def pille(t, y, farbe=O, gr=50, schrift="#fff"):
    return (f'<div style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:5"><span style="padding:16px 46px;border-radius:60px;'
            f'background:{farbe};color:{schrift};font-weight:900;font-size:{gr}px;box-shadow:0 0 40px {farbe}88;white-space:nowrap">{t}</span></div>')


def glas(inhalt, y, h, x=70, w=940):
    return f'<div class="glas" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;flex-direction:column;align-items:center;justify-content:center">{inhalt}</div>'


def von_nach(a, b, einheit, gr=118):
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:28px;font-weight:900;white-space:nowrap">'
            f'<span style="font-size:{gr}px;color:#8a919c;text-decoration:line-through;text-decoration-thickness:7px">{a}</span><span style="font-size:{gr*0.7:.0f}px;color:#fff">→</span>'
            f'<span style="font-size:{gr}px;color:{ROT};text-shadow:0 0 40px {ROT}aa">{b}</span></div>'
            f'<div style="font-weight:700;font-size:44px;color:#cbd5e1;margin-top:16px">{einheit}</div>')


def pfeil(y, d=150):
    """Oranger Pfeil nach rechts, OHNE Kreis, länglich (Nutzer 26.11.). d=150 → rechts unten (Breite 1,9·d); d>=240 → mittig groß (Thumbnail)."""
    w, h = int(d * 1.9), int(d * 0.8)
    x = (1080 - w) // 2 if d >= 240 else 1080 - w - 70
    return (f'<svg viewBox="0 0 190 80" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:6;filter:drop-shadow(0 0 22px {O}aa);overflow:visible">'
            f'<path d="M8 40 H168 M128 8 L174 40 L128 72" fill="none" stroke="{O}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def laufband(t, y=1600):
    return (f'<div style="position:absolute;left:0;top:{y}px;width:1080px;height:90px;background:#0b0d0ef2;border-top:4px solid {G}77;border-bottom:4px solid {G}77;z-index:6;'
            f'overflow:hidden;white-space:nowrap;font-family:monospace;font-weight:700;font-size:48px;line-height:82px;color:{ROT}">{t}</div>')


def quelle(t):
    return f'<div style="position:absolute;left:60px;width:960px;top:1710px;text-align:center;font-weight:600;font-size:32px;color:#aab2bd;z-index:6">{t}</div>'


def speichern(inhalt, ziel, foto="frei-code-monitor.jpg"):
    html = ("<html><body>" + CSS + bg(foto) + inhalt + f'<div style="position:absolute;inset:0;border:26px solid #DB8622;z-index:20"></div></body></html>')
    d = Path(tempfile.mkdtemp())
    (d / "c.html").write_text(html)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});"
          f"await p.goto('file://{d}/c.html');await p.waitForTimeout(600);await p.screenshot({{path:'{Path(ziel).resolve()}',type:'jpeg',quality:92}});await b.close();}})()")
    subprocess.run(["node", "-e", js], check=True)
    return ziel
