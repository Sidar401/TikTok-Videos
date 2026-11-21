#!/usr/bin/env python3
"""Covers im neuen hellen Look (ohne Kopfzeile, oranger Rahmen). Nutzung:
    import cover_hell as ch; ch.speichern(html_inhalt, "renders/thumbnails/<name>-tiktok.jpg", quer=False)
Pfade zu Logos: ch.L + datei. Rendert per Playwright (Chromium)."""
import random
import subprocess
import tempfile
from pathlib import Path

R = "/home/user/TikTok-Videos/"
L = R + "brand/logos/"
G, ROT, O, D = "#22a35a", "#d23c3c", "#f28a1e", "#1d2330"


def netz(w=1080, h=1920):
    rnd = random.Random(3)
    pts = [(rnd.randint(0, w), rnd.randint(0, h)) for _ in range(70)]
    s = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="none" stroke="#b9bec6" stroke-width="2"/>' for x, y in pts)
    for i, (x, y) in enumerate(pts):
        for a, b in pts[i + 1:i + 4]:
            if abs(a - x) + abs(b - y) < 420:
                s += f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="#c9ced5" stroke-width="1.5"/>'
    return f'<svg style="position:absolute;inset:0;width:{w}px;height:{h}px;opacity:.75" viewBox="0 0 {w} {h}">{s}</svg>'


def css(w=1080, h=1920):
    return (f"<style>*{{margin:0;box-sizing:border-box}}body{{width:{w}px;height:{h}px;position:relative;overflow:hidden;font-family:Montserrat,sans-serif;"
            "background:linear-gradient(180deg,#f7f8fa,#eceef2)}"
            ".karte{position:absolute;background:#fff;border:2px solid #e2e5ea;border-radius:12px;box-shadow:0 18px 40px #0000001a;padding:34px 40px}</style>")


def speichern(inhalt, ziel, quer=False):
    w, h = (1920, 1080) if quer else (1080, 1920)
    html = ("<html><body>" + css(w, h) + netz(w, h) + inhalt +
            '<div style="position:absolute;inset:0;border:26px solid #DB8622;z-index:20"></div></body></html>')
    d = Path(tempfile.mkdtemp())
    (d / "c.html").write_text(html)
    js = (f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{w},height:{h}}}}});"
          f"await p.goto('file://{d}/c.html');await p.waitForTimeout(500);await p.screenshot({{path:'{Path(ziel).resolve()}',type:'jpeg',quality:90}});await b.close();}})()")
    subprocess.run(["node", "-e", js], check=True)
    return ziel
