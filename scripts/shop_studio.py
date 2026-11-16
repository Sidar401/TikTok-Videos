#!/usr/bin/env python3
"""Shop-Demo im „Studio-Stil“ (ohne Emojis, ohne KI-Clips, ohne Stimme).

    python3 scripts/shop_studio.py shop/<produkt>/studio-<x>.json

Konfig (JSON):
  name, produkt {bild, preis, sterne, verkauft, cta, badge}, ende (s)
  szenen: Liste, jede mit
    typ     "titel" | "produkt" | "vergleich" | "liste" | "zahl" | "frage"
    dur     Länge in s
    bg      "hell" | "dunkel"
    kicker  kleines Etikett oben (z. B. "FEHLER #1")
    titel   Überschrift (*Wort* = orange markiert, | = neue Zeile)
  je Typ:
    titel:     icon (siehe ICONS), unter (kleiner Text)
    produkt:   punkte [{t, x, y}]  Hinweise mit Linie zu Punkt (x, y) am Produkt
    vergleich: links, rechts (Spaltennamen), zeilen [[text, links_ok, rechts_ok], ...]
    liste:     punkte [[icon, text], ...]
    zahl:      wert (Zahl), format ("de" = 12.500), nach (z. B. "×"), unter
    frage:     antworten ["Ja", "Nein"], unter
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from shop_video import TEMPLATE as SHOP_TEMPLATE  # noqa: E402

END_CSS = SHOP_TEMPLATE.split("/* Endkarte */")[1].split("</style>")[0]
END_HTML = SHOP_TEMPLATE.split("<div id=\"end\"")[1].split("<div id=\"flash\"")[0]
END_JS = SHOP_TEMPLATE.split("// Endkarte")[1].split("window.__timelines[\"main\"]")[0]

# Linien-Icons (24er Raster, Strich)
ICONS = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    "warn": '<path d="M12 3.5L21.5 20h-19z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.3" r=".6" fill="currentColor"/>',
    "uhr": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "blitz": '<path d="M13 2.5L5 13.5h6l-1 8 8-11h-6z"/>',
    "musik": '<path d="M9 17.5V6l10-2v11.5"/><circle cx="6.5" cy="17.5" r="2.5"/><circle cx="16.5" cy="15.5" r="2.5"/>',
    "akku": '<rect x="2.5" y="7" width="17" height="10" rx="2"/><path d="M22 10.5v3M6 10v4M9.5 10v4"/>',
    "sofa": '<path d="M4 11V8a2 2 0 012-2h12a2 2 0 012 2v3"/><path d="M2.5 11.5a1.5 1.5 0 013 0V14h13v-2.5a1.5 1.5 0 013 0V17h-19z"/><path d="M5 17v2M19 17v2"/>',
    "schuh": '<path d="M3 16.5V9l4 1 3-3 3.5 4.5 5 1.5a3 3 0 012.5 3v1.5z"/><path d="M3 19.5h18"/>',
    "kabel": '<path d="M7 3v5M11 3v5M5 8h8v3a4 4 0 01-8 0z"/><path d="M9 15v2a4 4 0 004 4h2a4 4 0 004-4V5"/>',
    "herz": '<path d="M12 20s-7.5-4.6-7.5-10A4.2 4.2 0 0112 7.3 4.2 4.2 0 0119.5 10c0 5.4-7.5 10-7.5 10z"/>',
    "pfote": '<circle cx="7" cy="10" r="1.8"/><circle cx="10.5" cy="6.5" r="1.8"/><circle cx="14.5" cy="6.5" r="1.8"/><circle cx="18" cy="10" r="1.8"/><path d="M8 17c0-2.8 1.8-5 4-5s4 2.2 4 5c0 1.7-1.3 2.5-2.7 2-.9-.3-1.7-.3-2.6 0-1.4.5-2.7-.3-2.7-2z"/>',
    "frage": '<circle cx="12" cy="12" r="8.5"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1.2-1.5 2.3"/><circle cx="12" cy="16.8" r=".6" fill="currentColor"/>',
    "stern": '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>',
    "pfeil": '<path d="M12 4v15M6 13l6 6 6-6"/>',
    "wagen": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h3l2.4 11.5h11l2-8H6.6"/>',
    "euro": '<path d="M17.5 6.5A7 7 0 007 12a7 7 0 0010.5 5.5"/><path d="M4.5 10.5h8M4.5 13.5h8"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def title_html(text):
    """Zeilen als Masken (für Hereinschieben); *x* = orange Markierung."""
    lines = []
    for line in text.split("|"):
        line = html.escape(line)
        line = re.sub(r"\*(.+?)\*", r'<em>\1</em>', line)
        lines.append(f'<span class="ln"><span class="lni">{line}</span></span>')
    return "".join(lines)


def scene(i, s, t):
    typ, d = s["typ"], s["dur"]
    h, js = [], []
    A = lambda code: js.append(code)  # noqa: E731
    sid = f"#s{i}"
    h.append('<div class="bgfill"></div><div class="grain"></div>')
    if s.get("kicker"):
        h.append(f'<div class="kicker"><span>{html.escape(s["kicker"])}</span></div>')
    if s.get("titel"):
        h.append(f'<div class="title">{title_html(s["titel"])}</div>')
    A(f'tl.fromTo("{sid} .bgfill", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.6, ease: "power3.out" }}, {t:.2f});')
    if i > 1:
        A(f'tl.fromTo("{sid}", {{ clipPath: "inset(0 0 0 100%)" }}, {{ clipPath: "inset(0 0 0 0%)", duration: 0.35, ease: "power3.inOut" }}, {t - 0.0:.2f});')
    if s.get("kicker"):
        A(f'tl.fromTo("{sid} .kicker span", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {t + 0.1:.2f});')
    if s.get("titel"):
        if i > 1:
            A(f'tl.fromTo("{sid} .lni", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.45, ease: "power4.out", stagger: 0.08 }}, {t + 0.15:.2f});')
        A(f'tl.fromTo("{sid} .title em", {{ backgroundSize: "0% 38%" }}, {{ backgroundSize: "100% 38%", duration: 0.4, ease: "power2.out" }}, {t + 0.5:.2f});')

    if typ == "titel":
        if s.get("icon"):
            h.append(f'<div class="bigico">{icon(s["icon"])}</div>')
            A(f'tl.fromTo("{sid} .bigico", {{ scale: 0.3, opacity: 0, rotation: -15 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }}, {t + 0.3:.2f});')
            A(f'tl.to("{sid} .bigico", {{ scale: 1.05, duration: {max(d - 0.8, 0.3):.2f}, ease: "sine.inOut" }}, {t + 0.8:.2f});')
            A(f'tl.fromTo("{sid} .bigico path, {sid} .bigico circle, {sid} .bigico rect", {{ strokeDasharray: 80, strokeDashoffset: 80 }}, {{ strokeDashoffset: 0, duration: 0.7, ease: "power2.out", stagger: 0.08 }}, {t + 0.35:.2f});')
        if s.get("unter"):
            h.append(f'<div class="unter">{html.escape(s["unter"])}</div>')
            A(f'tl.fromTo("{sid} .unter", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {t + 0.7:.2f});')

    elif typ == "produkt":
        h.append('<div class="podium"></div><img class="prod" src="assets/produkt.png" alt="" />')
        A(f'tl.fromTo("{sid} .podium", {{ scaleX: 0.2, opacity: 0 }}, {{ scaleX: 1, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t + 0.1:.2f});')
        A(f'tl.fromTo("{sid} .prod", {{ y: 120, opacity: 0, scale: 0.85 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }}, {t + 0.15:.2f});')
        A(f'tl.to("{sid} .prod", {{ y: -14, rotation: 1.5, duration: {max(d - 0.8, 0.3):.2f}, ease: "sine.inOut" }}, {t + 0.75:.2f});')
        for k, p in enumerate(s.get("punkte", [])):
            x, y = p["x"], p["y"]
            right = x > 540
            lx = 1020 if right else 60
            h.append(
                f'<svg class="cline cl{k}" viewBox="0 0 1080 1920"><path d="M{x} {y} L{(x + lx) / 2:.0f} {p.get("ly", y)} L{lx + (-40 if right else 40)} {p.get("ly", y)}"/>'
                f'<circle cx="{x}" cy="{y}" r="11"/></svg>'
                f'<div class="callout co{k} {"r" if right else "l"}" style="top:{p.get("ly", y) - 46}px">{html.escape(p["t"])}</div>')
            tt = t + 0.75 + k * 0.45
            A(f'tl.fromTo("{sid} .cl{k} circle", {{ scale: 0, transformOrigin: "{x}px {y}px" }}, {{ scale: 1, duration: 0.25, ease: "back.out(3)" }}, {tt:.2f});')
            A(f'tl.fromTo("{sid} .cl{k} path", {{ strokeDasharray: 900, strokeDashoffset: 900 }}, {{ strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }}, {tt + 0.05:.2f});')
            A(f'tl.fromTo("{sid} .co{k}", {{ opacity: 0, x: {30 if right else -30} }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {tt + 0.3:.2f});')

    elif typ == "vergleich":
        rows = "".join(
            f'<div class="vrow"><div class="vl">{html.escape(z[0])}</div>'
            f'<div class="vc a {"ok" if z[1] else "no"}">{icon("check" if z[1] else "x")}</div>'
            f'<div class="vc b {"ok" if z[2] else "no"}">{icon("check" if z[2] else "x")}</div></div>'
            for z in s["zeilen"])
        h.append(
            f'<div class="vtab"><div class="vhead"><div></div><div class="vh a">{html.escape(s["links"])}</div>'
            f'<div class="vh b"><img src="assets/produkt.png" alt="" />{html.escape(s["rechts"])}</div></div>{rows}</div>')
        A(f'tl.fromTo("{sid} .vhead", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t + 0.3:.2f});')
        A(f'tl.fromTo("{sid} .vrow", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out", stagger: 0.35 }}, {t + 0.55:.2f});')
        A(f'tl.fromTo("{sid} .vc", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, ease: "back.out(3)", stagger: 0.175 }}, {t + 0.7:.2f});')

    elif typ == "liste":
        items = "".join(
            f'<div class="li {p[0]}"><div class="lic">{icon(p[0])}</div><div class="lit">{html.escape(p[1])}</div></div>'
            for p in s["punkte"])
        h.append(f'<div class="list">{items}</div>')
        step = min(0.45, (d - 1.0) / max(len(s["punkte"]), 1))
        A(f'tl.fromTo("{sid} .li", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out", stagger: {step:.2f} }}, {t + 0.45:.2f});')
        A(f'tl.fromTo("{sid} .lic", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2.5)", stagger: {step:.2f} }}, {t + 0.55:.2f});')

    elif typ == "zahl":
        h.append(f'<div class="zahl"><span id="z{i}">0</span><small>{html.escape(s.get("nach", ""))}</small></div>'
                 f'<div class="sterne">{"".join(icon("stern", "st") for _ in range(5))}</div>'
                 f'<div class="unter">{html.escape(s.get("unter", ""))}</div>'
                 '<img class="prod klein" src="assets/produkt.png" alt="" />')
        A(f'(() => {{ const o = {{ v: 0 }}; const el = document.getElementById("z{i}");'
          f' tl.to(o, {{ v: {s["wert"]}, duration: 1.2, ease: "power2.out", onUpdate: () => {{ el.textContent = Math.round(o.v).toLocaleString("de-DE"); }} }}, {t + 0.3:.2f}); }})();')
        A(f'tl.fromTo("{sid} .zahl", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {t + 0.25:.2f});')
        A(f'tl.fromTo("{sid} .st", {{ scale: 0, rotation: -60 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "back.out(3)", stagger: 0.1 }}, {t + 1.0:.2f});')
        A(f'tl.fromTo("{sid} .unter", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {t + 1.3:.2f});')
        A(f'tl.fromTo("{sid} .prod.klein", {{ y: 200, opacity: 0, rotation: 12 }}, {{ y: 0, opacity: 1, rotation: -4, duration: 0.6, ease: "back.out(1.5)" }}, {t + 0.6:.2f});')

    elif typ == "frage":
        btns = "".join(f'<div class="btn b{k}">{html.escape(a)}</div>' for k, a in enumerate(s["antworten"]))
        h.append(f'<div class="bigico frage">{icon("frage")}</div><div class="btns">{btns}</div>'
                 f'<div class="tap"></div><div class="unter">{html.escape(s.get("unter", ""))} {icon("pfeil", "pf")}</div>')
        A(f'tl.fromTo("{sid} .bigico", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, {t + 0.2:.2f});')
        A(f'tl.fromTo("{sid} .btn", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.15 }}, {t + 0.5:.2f});')
        A(f'tl.fromTo("{sid} .tap", {{ scale: 0, opacity: 0.8 }}, {{ scale: 2.4, opacity: 0, duration: 0.6, ease: "power2.out" }}, {t + 1.3:.2f});')
        A(f'tl.to("{sid} .b0", {{ backgroundColor: "#DB8622", color: "#fff", scale: 1.06, duration: 0.2 }}, {t + 1.3:.2f});')
        A(f'tl.fromTo("{sid} .unter", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {t + 1.6:.2f});')
        A(f'tl.to("{sid} .pf", {{ y: 12, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t + 1.9:.2f});')

    cls = f'scene bg-{s.get("bg", "hell")} typ-{typ}'
    return (f'<div id="s{i}" class="clip {cls}" data-start="{t:.2f}" data-duration="{d:.2f}" data-track-index="1">\n          '
            + "\n          ".join(h) + "\n        </div>", "\n      ".join([f"// Szene {i}: {typ}"] + js))


def build(cfg_path):
    cfg = json.loads(Path(cfg_path).read_text())
    name = cfg["name"]
    vdir = ROOT / "videos" / name
    if not vdir.exists():
        shutil.copytree(ROOT / "vorlage", vdir)
        shutil.rmtree(vdir / ".hyperframes", ignore_errors=True)
        pj = vdir / "package.json"
        pj.write_text(re.sub(r'"name":\s*"[^"]*"', f'"name": "{name}"', pj.read_text()))
    p = cfg["produkt"]
    shutil.copy(ROOT / p["bild"], vdir / "assets" / "produkt.png")

    t, scenes, js = 0.0, [], []
    for i, s in enumerate(cfg["szenen"], 1):
        hh, jj = scene(i, s, t)
        scenes.append(hh)
        js.append(jj)
        t += s["dur"]
    ende = cfg.get("ende", 3.0)
    total = t + ende
    end_html = END_HTML.replace("{{CTA}} 🛒", "{{CTA}} " + icon("wagen", "wg"))
    for k, v in {
        "{{T_END}}": f"{t:.2f}", "{{ENDE}}": f"{ende:.2f}",
        "{{PREIS}}": html.escape(p["preis"]), "{{STERNE}}": html.escape(p["sterne"]),
        "{{VERKAUFT}}": html.escape(p["verkauft"]), "{{CTA}}": html.escape(p.get("cta", "Unten im Warenkorb")),
        "{{BADGE}}": html.escape(p.get("badge", "Bestseller")),
    }.items():
        end_html = end_html.replace(k, v)
    doc = (STUDIO.replace("{{END_CSS}}", END_CSS)
           .replace("{{TOTAL}}", f"{total:.2f}")
           .replace("{{SCENES}}", "\n        ".join(scenes))
           .replace("{{END}}", '<div id="end"' + end_html)
           .replace("{{JS}}", "\n\n      ".join(js))
           .replace("{{END_JS}}", END_JS.replace("tEnd", f"{t:.2f}")))
    (vdir / "index.html").write_text(doc)
    print(f"{vdir}/index.html · {total:.1f} s")


STUDIO = """<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      /* Studio-Stil HundeWissenTv 2.0 – erzeugt von scripts/shop_studio.py */
      :root { --brand: #DB8622; --dark: #16181A; --ink: #1B1D1F; --soft: #F4EFE8; --ok: #2E9E62; --no: #D9534F;
        --font: "Montserrat", sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      #root { position: relative; width: 100%; height: 100%; background: #000; font-family: var(--font); }
      .scene { position: absolute; inset: 0; overflow: hidden; color: var(--ink); }
      .bgfill { position: absolute; inset: -60px;
        background: radial-gradient(circle at 50% 55%, #FFFFFF 0%, var(--soft) 55%, #E9E1D6 100%); }
      .bg-dunkel { color: #fff; }
      .bg-dunkel .bgfill { background: radial-gradient(circle at 50% 55%, #2A2622 0%, var(--dark) 60%, #0E0F10 100%); }
      .grain { position: absolute; inset: 0; opacity: 0.05;
        background-image: repeating-linear-gradient(45deg, #000 0 1px, transparent 1px 6px); }

      .kicker { position: absolute; top: 210px; left: 0; width: 1080px; text-align: center; }
      .kicker span { display: inline-block; font-weight: 800; font-size: 34px; letter-spacing: 6px; color: var(--brand);
        border: 3px solid var(--brand); border-radius: 999px; padding: 10px 28px; }
      .title { position: absolute; top: 300px; left: 70px; width: 940px; text-align: center; font-weight: 900;
        font-size: 92px; line-height: 1.08; letter-spacing: -2px; }
      .ln { display: block; overflow: hidden; padding: 4px 0; }
      .lni { display: inline-block; }
      .title em { font-style: normal; background-image: linear-gradient(var(--brand), var(--brand));
        background-repeat: no-repeat; background-position: 0 88%; background-size: 100% 38%; padding: 0 6px; }
      .bg-dunkel .title em { color: #fff; }

      .bigico { position: absolute; left: 340px; top: 760px; width: 400px; height: 400px; border-radius: 50%;
        background: #fff; box-shadow: 0 30px 80px rgba(0,0,0,0.12); color: var(--brand); display: flex;
        align-items: center; justify-content: center; }
      .bg-dunkel .bigico { background: #23201C; box-shadow: 0 0 0 3px rgba(219,134,34,0.35), 0 30px 80px rgba(0,0,0,0.5); }
      .bigico .ico { width: 220px; height: 220px; }
      .bigico.frage { top: 640px; width: 300px; height: 300px; left: 390px; }
      .bigico.frage .ico { width: 170px; height: 170px; }
      .unter { position: absolute; top: 1250px; left: 90px; width: 900px; text-align: center; font-weight: 700;
        font-size: 46px; line-height: 1.3; opacity: 0.8; }
      .unter .pf { width: 46px; height: 46px; vertical-align: -10px; color: var(--brand); }

      .podium { position: absolute; left: 190px; top: 1290px; width: 700px; height: 120px; border-radius: 50%;
        background: radial-gradient(ellipse, rgba(0,0,0,0.22) 0%, rgba(0,0,0,0) 70%); }
      .prod { position: absolute; left: 215px; top: 660px; width: 650px; filter: drop-shadow(0 30px 40px rgba(0,0,0,0.25)); }
      .prod.klein { left: 340px; top: 1130px; width: 400px; }
      .cline { position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: visible; }
      .cline path { fill: none; stroke: var(--ink); stroke-width: 4; }
      .bg-dunkel .cline path { stroke: #fff; }
      .cline circle { fill: var(--brand); stroke: #fff; stroke-width: 5; }
      .callout { position: absolute; font-weight: 800; font-size: 40px; background: var(--ink); color: #fff;
        padding: 18px 28px; border-radius: 18px; white-space: nowrap; }
      .bg-dunkel .callout { background: #fff; color: var(--ink); }
      .callout.l { left: 50px; } .callout.r { right: 50px; }

      .vtab { position: absolute; left: 60px; width: 960px; top: 640px; background: #fff; border-radius: 40px;
        padding: 30px 30px 20px; box-shadow: 0 30px 80px rgba(0,0,0,0.12); color: var(--ink); }
      .vhead, .vrow { display: grid; grid-template-columns: 1fr 220px 220px; align-items: center; }
      .vhead { padding-bottom: 20px; border-bottom: 3px solid #EEE7DD; }
      .vh { text-align: center; font-weight: 800; font-size: 34px; line-height: 1.15; }
      .vh.a { color: #8A8580; }
      .vh.b { color: var(--brand); }
      .vh.b img { display: block; width: 130px; margin: 0 auto 6px; }
      .vrow { height: 150px; border-bottom: 3px solid #F3EEE7; }
      .vrow:last-child { border-bottom: 0; }
      .vl { font-weight: 800; font-size: 44px; line-height: 1.1; }
      .vc { justify-self: center; width: 92px; height: 92px; border-radius: 50%; display: flex; align-items: center;
        justify-content: center; color: #fff; }
      .vc.ok { background: var(--ok); } .vc.no { background: #D8D2CA; }
      .vc .ico { width: 56px; height: 56px; stroke-width: 3; }

      .list { position: absolute; left: 80px; width: 920px; top: 700px; display: flex; flex-direction: column; gap: 34px; }
      .li { display: flex; align-items: center; gap: 34px; background: #fff; border-radius: 30px; padding: 30px 36px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.10); color: var(--ink); }
      .bg-dunkel .li { background: #24211D; color: #fff; box-shadow: none; border: 2px solid #3A342D; }
      .lic { flex: none; width: 104px; height: 104px; border-radius: 50%; display: flex; align-items: center;
        justify-content: center; color: #fff; background: var(--brand); }
      .li.check .lic { background: var(--ok); } .li.x .lic, .li.warn .lic { background: var(--no); }
      .lic .ico { width: 60px; height: 60px; stroke-width: 2.6; }
      .lit { font-weight: 800; font-size: 50px; line-height: 1.15; }

      .zahl { position: absolute; top: 580px; left: 0; width: 1080px; text-align: center; font-weight: 900;
        font-size: 250px; letter-spacing: -8px; line-height: 1; color: var(--brand); }
      .zahl small { font-size: 150px; }
      .sterne { position: absolute; top: 860px; left: 0; width: 1080px; display: flex; justify-content: center; gap: 18px; }
      .st { width: 90px; height: 90px; color: #F2B418; fill: #F2B418; }
      .typ-zahl .unter { top: 990px; opacity: 0.9; }

      .btns { position: absolute; top: 1010px; left: 120px; width: 840px; display: flex; gap: 40px; }
      .btn { flex: 1; text-align: center; font-weight: 900; font-size: 64px; padding: 34px 0; border-radius: 30px;
        background: #fff; color: var(--ink); box-shadow: 0 20px 50px rgba(0,0,0,0.12); border: 4px solid #E6DED3; }
      .tap { position: absolute; left: 270px; top: 1060px; width: 120px; height: 120px; border-radius: 50%;
        background: rgba(219,134,34,0.5); }
      .typ-frage .unter { top: 1260px; }

      #e-cta .wg { width: 58px; height: 58px; vertical-align: -10px; stroke-width: 2.6; }
      /* Endkarte */{{END_CSS}}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
      <div id="scenes">
        {{SCENES}}
      </div>

      {{END}}
      <div id="flash" class="clip" data-start="0" data-duration="{{TOTAL}}" data-track-index="3"></div>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });

      {{JS}}

      // Endkarte{{END_JS}}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    build(sys.argv[1])
