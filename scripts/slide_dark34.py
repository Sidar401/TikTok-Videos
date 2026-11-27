#!/usr/bin/env python3
"""Slideshow-Baukasten DUNKEL im Format 3:4 (1080×1440) – Nutzer 26.11.: Instagram schneidet 9:16 ab. Nutzt slide_dark (Helfer: txt, pille, glas, von_nach, pfeil, quelle-Stil).
Layout: kompakter Kopf (Beagle links, NEWS+Datum+Zähler rechts), Inhalt y≈260–1300, Pfeil rechts unten y≈1190, Quelle y≈1350."""
import subprocess
import tempfile
from pathlib import Path

import slide_dark as sd

H = 1440
G, ROT, O, W = sd.G, sd.ROT, sd.O, sd.W
txt, pille, glas, von_nach, pfeil = sd.txt, sd.pille, sd.glas, sd.von_nach, sd.pfeil
L = sd.L
BEAGLE = sd.BEAGLE


def bg(foto="frei-code-monitor.jpg"):
    return (f'<img src="file://{sd.R_}brand/hintergruende/{foto}" style="position:absolute;left:-60px;top:-30px;width:1200px;height:1500px;object-fit:cover;filter:blur(2px) brightness(.5) saturate(.7);z-index:0"/>'
            '<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,#f28a1e22 0%,#0000 55%),linear-gradient(180deg,#000b 0%,#0008 40%,#000c 100%);z-index:1"></div>')


def kopf(datum="27.11.2026", nr=None, marke="NEWS"):
    z = f'<div style="font-family:monospace;font-weight:800;font-size:34px;color:#fff;margin-top:8px;text-align:right">{nr}</div>' if nr else ""
    return (f'<div style="position:absolute;left:64px;top:58px;display:flex;align-items:center;gap:22px;z-index:6"><img src="{BEAGLE}" style="width:128px;height:128px;border-radius:50%;border:6px solid {O};box-shadow:0 0 30px {O}88"/>'
            f'<div style="font-weight:800;font-size:40px;text-shadow:0 4px 12px #000">HundeFinanzTv</div></div>'
            f'<div style="position:absolute;right:64px;top:70px;z-index:6;text-align:right"><span style="background:{O};color:#111;font-weight:900;font-size:32px;padding:4px 20px;border-radius:10px;letter-spacing:2px">{marke}</span>'
            f'<div style="font-family:monospace;font-weight:700;font-size:32px;margin-top:8px">{datum}</div>{z}</div>'
            f'<div style="position:absolute;left:60px;top:214px;width:960px;height:3px;background:linear-gradient(90deg,{O},{O}22);z-index:6"></div>')


def quelle(t):
    return f'<div style="position:absolute;left:60px;width:960px;top:1340px;text-align:center;font-weight:600;font-size:28px;color:#aab2bd;z-index:6">{t}</div>'


def logo_chip(datei, y, w=560, h=200):
    return (f'<div style="position:absolute;left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:22px;box-shadow:0 0 60px #000a;z-index:5;'
            f'display:flex;align-items:center;justify-content:center"><img src="file://{L}{datei}" style="max-width:86%;max-height:78%"/></div>')


def speichern(inhalt, ziel, foto="frei-code-monitor.jpg"):
    css = sd.CSS.replace("height:1920px", f"height:{H}px")
    html = ("<html><body>" + css + bg(foto) + inhalt + '<div style="position:absolute;inset:0;border:26px solid #DB8622;z-index:20"></div></body></html>')
    d = Path(tempfile.mkdtemp())
    (d / "c.html").write_text(html)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:" + str(H) + "}});"
          f"await p.goto('file://{d}/c.html');await p.waitForTimeout(600);await p.screenshot({{path:'{Path(ziel).resolve()}',type:'jpeg',quality:92}});await b.close();}})()")
    subprocess.run(["node", "-e", js], check=True)
    return ziel
