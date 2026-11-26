#!/usr/bin/env python3
"""HundeWissenTv-Cover (1080×1920 JPEG). Wichtiges nur in der Mitte (y 285–1635 = Instagram-4:5-Ausschnitt,
TikTok-Profil schneidet ähnlich). Aufruf: import cover; cover.speichern(html, "renders/thumbnails/<name>.jpg")"""
import subprocess, tempfile
from pathlib import Path
R = Path(__file__).resolve().parent.parent
F = R / "videos/hw-mag-farben/assets/fonts"
CSS = f"""<style>
@font-face{{font-family:FR;font-weight:900;src:url(file://{F}/fraunces-latin-900-normal.woff2)}}
@font-face{{font-family:FR;font-weight:900;font-style:italic;src:url(file://{F}/fraunces-latin-900-italic.woff2)}}
@font-face{{font-family:IN;font-weight:900;src:url(file://{F}/InterDisplay-Black.otf)}}
@font-face{{font-family:IN;font-weight:800;src:url(file://{F}/InterDisplay-ExtraBold.otf)}}
*{{margin:0;box-sizing:border-box}} body{{width:1080px;height:1920px;position:relative;overflow:hidden;color:#1d1b19;
background:radial-gradient(ellipse at 50% 45%,#faf6ef 0%,#f3ede3 55%,#e6dccb 100%)}}
.h{{position:absolute;left:60px;right:60px;text-align:center;font-family:FR;font-weight:900;line-height:.95;letter-spacing:-3px}}
.h i{{color:#db8622;font-style:italic}} .r{{color:#d23c3c}}
.badge{{position:absolute;left:0;width:1080px;text-align:center}}
.badge span{{display:inline-block;background:#db8622;color:#fff;font-family:IN;font-weight:900;font-size:50px;padding:10px 40px 14px;border-radius:50px;letter-spacing:2px}}
.sub{{position:absolute;left:0;width:1080px;text-align:center;font-family:IN;font-weight:800;font-size:56px}}
.sub b{{color:#d23c3c}} img{{position:absolute;filter:drop-shadow(0 26px 30px #0003)}}
.logo{{position:absolute;left:470px;top:120px;width:140px;height:140px;border-radius:50%;border:6px solid #db8622;overflow:hidden;filter:none}}
.logo img{{position:static;width:100%;height:100%;filter:none}}
</style>"""
def bild(n): return f"file://{R}/brand/{n}.png"
def speichern(inhalt, ziel):
    html = ("<html><body>" + CSS + f'<div class="logo"><img src="{bild("aussie/../../videos/hw-mag-farben/assets/beagle")}"></div>' + inhalt +
            '<div style="position:absolute;inset:0;border:26px solid #DB8622;z-index:20"></div></body></html>')
    d = Path(tempfile.mkdtemp()); (d / "c.html").write_text(html)
    js = (f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});"
          f"await p.goto('file://{d}/c.html');await p.waitForTimeout(700);await p.screenshot({{path:'{Path(ziel).resolve()}',type:'jpeg',quality:88}});await b.close();}})()")
    subprocess.run(["node", "-e", js], check=True)
