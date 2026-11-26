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
            f'border-bottom:2px solid #e4e6ea;display:flex;align-items:center;padding:0 64px 0 50px;gap:18px;z-index:8">'
            f'<img src="assets/beagle.png" style="width:86px;height:86px;border-radius:50%;border:3px solid #fff;box-shadow:0 4px 10px #0002"/>'
            f'<div style="font-weight:700;font-size:40px;color:{DUNKEL}">HundeFinanzTv</div>'
            f'<div style="margin-left:auto;font-size:31px;color:{DUNKEL};font-weight:800;letter-spacing:1px;white-space:nowrap">{rechts}'
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


def kopf_quer(rechts="BÖRSENNEWS", datum=""):
    """Kopfzeile für 16:9 (1920×1080)."""
    return (f'<div id="kopf" style="position:absolute;left:0;top:26px;width:1920px;height:110px;background:linear-gradient(90deg,#fbe9e9,#fdf6e3);'
            f'border-bottom:2px solid #e4e6ea;display:flex;align-items:center;padding:0 70px;gap:22px;z-index:8">'
            f'<img src="assets/beagle.png" style="width:80px;height:80px;border-radius:50%;border:3px solid #fff;box-shadow:0 4px 10px #0002"/>'
            f'<div style="font-weight:700;font-size:42px;color:{DUNKEL}">HundeFinanzTv</div>'
            f'<div style="margin-left:auto;font-size:38px;color:{DUNKEL};font-weight:800;letter-spacing:1px;white-space:nowrap">{rechts}'
            f'<span style="font-weight:500;color:#555c66;margin-left:12px">{datum}</span></div></div>')


# ---------------- Animierte CTAs (Nutzer 22.11., Vorbild: Kommentar-Feld mit Tipp-Text + Mauszeiger) ----------------
ZEIGER = ('<svg viewBox="0 0 24 24" style="width:100%;height:100%;filter:drop-shadow(0 4px 6px #0006)">'
          '<path d="M4 2 L4 20 L9 15.5 L12.5 23 L15.5 21.6 L12 14.3 L19 14 Z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def _zeiger(id_, x, y):
    return f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:70px;height:70px;z-index:30;opacity:0">{ZEIGER}</div>'


def _banner(id_, teil1, teil2, y):
    return (f'<div id="{id_}" style="position:absolute;left:0;width:1080px;top:{y}px;display:flex;justify-content:center;z-index:29">'
            f'<span style="padding:20px 44px;border-radius:60px;background:{DUNKEL};color:#fff;font-weight:900;font-size:46px;letter-spacing:2px;white-space:nowrap;'
            f'box-shadow:0 14px 30px #0004">{teil1} <span style="color:{ORANGE}">{teil2}</span></span></div>')


def cta_kommentar(id_, text="Meine Meinung dazu", antwort="", y=700):
    """Kommentar-Feld: Text tippt sich ein, Zeiger klickt „Kommentieren“. JS: cta_kommentar_js(id_, t). Dauer ≈ 4,5 s."""
    buchst = "".join(f'<span class="tz" style="opacity:0">{"&nbsp;" if c == " " else c}</span>' for c in text)
    ant = (f'<div id="{id_}-ant" style="display:flex;gap:18px;align-items:flex-start;margin-top:26px;opacity:0">'
           f'<div style="width:62px;height:62px;border-radius:50%;background:#3b82f6;flex:none"></div><div><div style="font-weight:800;font-size:32px;color:{DUNKEL}">Du · gerade eben</div>'
           f'<div style="font-size:38px;color:#3a414c;margin-top:4px">{antwort}</div><div style="font-size:30px;color:#8a909a;margin-top:6px">♡ 1 · Antworten</div></div></div>') if antwort else ""
    return (f'<div id="{id_}" style="position:absolute;left:70px;width:940px;top:{y}px;background:#fff;border:2px solid #e2e5ea;border-radius:26px;padding:34px 40px;'
            f'box-shadow:0 26px 60px #0000002e;z-index:28;opacity:0">'
            f'<div style="font-weight:800;font-size:40px;color:{DUNKEL}">Kommentare</div>'
            f'<div style="display:flex;align-items:center;gap:20px;margin-top:26px"><div style="width:62px;height:62px;border-radius:50%;background:#3b82f6;flex:none;'
            f'display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px">●</div>'
            f'<div style="flex:1;border-bottom:4px solid {DUNKEL};padding-bottom:10px;font-size:44px;color:{DUNKEL};white-space:nowrap">{buchst}'
            f'<span id="{id_}-cur" style="display:inline-block;width:4px;height:46px;background:{DUNKEL};vertical-align:middle;margin-left:2px"></span></div></div>'
            f'<div style="display:flex;justify-content:flex-end;gap:30px;margin-top:26px;align-items:center"><span style="font-size:36px;color:#8a909a;font-weight:700">Abbrechen</span>'
            f'<span id="{id_}-btn" style="padding:16px 40px;border-radius:40px;background:{ORANGE};color:#fff;font-weight:900;font-size:38px">Kommentieren</span></div>{ant}</div>'
            + _zeiger(f"{id_}-z", 520, y + 520) + _banner(f"{id_}-bn", "DEINE MEINUNG", "IN DIE KOMMENTARE", y - 140))


def cta_kommentar_js(id_, t, n_zeichen=18, tipp=1.6, sfx=None):
    """sfx: Liste, an die (zeit, sound) angehängt wird."""
    s = (f' tl.fromTo("#{id_}", {{ y: 260, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {t});'
         f' tl.fromTo("#{id_}-bn", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {t} + 0.2);'
         f' tl.to("#{id_} .tz", {{ opacity: 1, duration: 0.01, stagger: {tipp / max(n_zeichen, 1):.3f} }}, {t} + 0.6);'
         f' tl.fromTo("#{id_}-cur", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.25, repeat: 9, yoyo: true, ease: "steps(1)" }}, {t} + 0.4);'
         f' tl.fromTo("#{id_}-z", {{ x: 260, y: 320, opacity: 0 }}, {{ x: 150, y: -290, opacity: 1, duration: 0.7, ease: "power2.inOut" }}, {t} + 0.6 + {tipp});'
         f' tl.to("#{id_}-z", {{ scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }}, {t} + 1.4 + {tipp});'
         f' tl.to("#{id_}-btn", {{ scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }}, {t} + 1.4 + {tipp});'
         f' tl.to("#{id_}-btn", {{ backgroundColor: "#22a35a", duration: 0.2 }}, {t} + 1.5 + {tipp});'
         f' tl.fromTo("#{id_}-ant", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35 }}, {t} + 1.7 + {tipp});')
    if sfx is not None:
        sfx += [(t, "whoosh-weich"), (t + 0.6, "tippen"), (t + 1.4 + tipp, "klick"), (t + 1.75 + tipp, "pop")]
    return s


def cta_folgen(id_, y=620, follower="12.480"):
    """Profil-Karte: Zeiger klickt „+ Folgen“ → „Gefolgt ✓“. JS: cta_folgen_js."""
    return (f'<div id="{id_}" style="position:absolute;left:110px;width:860px;top:{y}px;background:#fff;border:2px solid #e2e5ea;border-radius:30px;padding:46px 40px;'
            f'box-shadow:0 26px 60px #0000002e;z-index:28;opacity:0;text-align:center">'
            f'<div style="width:220px;height:220px;margin:0 auto;border-radius:50%;overflow:hidden;border:8px solid {ORANGE};background:#1b1f22">'
            f'<img src="assets/beagle.png" style="width:100%;height:100%;object-fit:cover"/></div>'
            f'<div style="font-weight:900;font-size:60px;color:{DUNKEL};margin-top:20px">HundeFinanz<span style="color:{ORANGE}">Tv</span></div>'
            f'<div style="font-size:34px;color:#8a909a">@hundefinanztv</div>'
            f'<div style="font-size:36px;color:{DUNKEL};margin-top:16px"><b id="{id_}-zahl">{follower}</b> Follower</div>'
            f'<div style="position:relative;height:110px;margin-top:30px">'
            f'<span id="{id_}-btn" style="position:absolute;left:50%;top:0;transform:translateX(-50%);padding:22px 90px;border-radius:50px;background:{ORANGE};color:#fff;font-weight:900;font-size:50px;white-space:nowrap">+ Folgen</span>'
            f'<span id="{id_}-ok" style="position:absolute;left:50%;top:0;transform:translateX(-50%);padding:22px 70px;border-radius:50px;background:#e8eaee;color:{DUNKEL};font-weight:900;font-size:50px;white-space:nowrap;opacity:0">Gefolgt ✓</span></div></div>'
            + _zeiger(f"{id_}-z", 520, y + 760) + _banner(f"{id_}-bn", "FOLGE", "HUNDEFINANZTV", y - 140))


def cta_folgen_js(id_, t, sfx=None, follower_neu="12.481"):
    s = (f' tl.fromTo("#{id_}", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.7)" }}, {t});'
         f' tl.fromTo("#{id_}-bn", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {t} + 0.25);'
         f' tl.fromTo("#{id_}-z", {{ x: 280, y: 300, opacity: 0 }}, {{ x: 0, y: -235, opacity: 1, duration: 0.8, ease: "power2.inOut" }}, {t} + 0.9);'
         f' tl.to("#{id_}-z", {{ scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }}, {t} + 1.75);'
         f' tl.to("#{id_}-btn", {{ scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }}, {t} + 1.75);'
         f' tl.to("#{id_}-btn", {{ opacity: 0, duration: 0.15 }}, {t} + 1.9); tl.fromTo("#{id_}-ok", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {t} + 1.9);'
         f' tl.set("#{id_}-zahl", {{ textContent: "{follower_neu}" }}, {t} + 2.0); tl.fromTo("#{id_}-zahl", {{ scale: 1.4 }}, {{ scale: 1, duration: 0.3 }}, {t} + 2.0);')
    if sfx is not None:
        sfx += [(t, "whoosh-weich"), (t + 1.75, "klick"), (t + 1.95, "level-up")]
    return s


def cta_teilen(id_, text="mit jemandem, der das wissen muss", y=860):
    """Teilen-Menü: Zeiger klickt „Senden“, Papierflieger fliegt weg. JS: cta_teilen_js."""
    kreise = "".join(f'<div style="text-align:center"><div style="width:120px;height:120px;border-radius:50%;background:{f};margin:0 auto;display:flex;align-items:center;'
                     f'justify-content:center;color:#fff;font-size:56px;font-weight:900">{i}</div><div style="font-size:28px;color:#3a414c;margin-top:10px">{n}</div></div>'
                     for i, n, f in (("✉", "Nachricht", "#3b82f6"), ("🔗", "Link", "#8a909a"), ("➤", "Senden", ORANGE), ("★", "Story", "#a855f7")))
    return (f'<div id="{id_}" style="position:absolute;left:40px;width:1000px;top:{y}px;background:#fff;border-radius:34px 34px 26px 26px;padding:30px 40px 40px;'
            f'box-shadow:0 -10px 60px #0000003a;z-index:28;opacity:0">'
            f'<div style="width:120px;height:10px;border-radius:6px;background:#d9dde3;margin:0 auto 26px"></div>'
            f'<div style="font-weight:800;font-size:40px;color:{DUNKEL};text-align:center;margin-bottom:30px">Teilen</div>'
            f'<div style="display:flex;justify-content:space-around">{kreise}</div></div>'
            f'<div id="{id_}-fl" style="position:absolute;left:600px;top:{y + 140}px;font-size:90px;color:{ORANGE};z-index:31;opacity:0">➤</div>'
            + _zeiger(f"{id_}-z", 640, y + 250) + _banner(f"{id_}-bn", "TEILE DAS", text.upper(), y - 140).replace("font-size:46px", "font-size:34px"))


def cta_teilen_js(id_, t, sfx=None):
    s = (f' tl.fromTo("#{id_}", {{ y: 500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t});'
         f' tl.fromTo("#{id_}-bn", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {t} + 0.3);'
         f' tl.fromTo("#{id_}-z", {{ x: 200, y: 300, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.8, ease: "power2.inOut" }}, {t} + 0.9);'
         f' tl.to("#{id_}-z", {{ scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }}, {t} + 1.75);'
         f' tl.fromTo("#{id_}-fl", {{ x: 0, y: 0, opacity: 1, rotation: 0 }}, {{ x: 380, y: -700, opacity: 0, rotation: -25, duration: 0.9, ease: "power2.in" }}, {t} + 1.85);')
    if sfx is not None:
        sfx += [(t, "swipe"), (t + 1.75, "klick"), (t + 1.85, "whoosh-schnell"), (t + 2.6, "handy-benachrichtigung")]
    return s


# ---------- CTA-Overlay „wie im Vorbild“ (Nutzer 22.11.): dunkles Feld unten, Text tippt, Zeiger klickt orangen Button, Banner darunter ----------
def cta_overlay(id_, titel, text, knopf, banner1, banner2, y=1430, knopf2=""):
    """Dunkles, halbtransparentes Overlay-Feld (wie YouTube-Kommentarfeld) + Banner. knopf2 = Text nach dem Klick (optional).
    JS: cta_overlay_js(id_, t, len(text), sfx)."""
    buchst = "".join(f'<span class="tz" style="opacity:0">{"&nbsp;" if c == " " else c}</span>' for c in text)
    k2 = (f'<span id="{id_}-k2" style="position:absolute;right:0;top:0;padding:12px 34px;border-radius:30px;background:#22a35a;color:#fff;font-weight:800;'
          f'font-size:32px;white-space:nowrap;opacity:0">{knopf2}</span>') if knopf2 else ""
    return (f'<div id="{id_}" style="position:absolute;left:90px;width:900px;top:{y}px;background:#101722e8;border:1px solid #ffffff22;border-radius:22px;'
            f'padding:26px 34px 24px;box-shadow:0 18px 40px #0006;z-index:28;opacity:0;font-family:Montserrat,sans-serif">'
            f'<div style="font-weight:700;font-size:34px;color:#fff">{titel}</div>'
            f'<div style="display:flex;align-items:center;gap:18px;margin-top:20px"><div style="width:50px;height:50px;border-radius:50%;background:#3b82f6;flex:none;'
            f'display:flex;align-items:flex-end;justify-content:center;overflow:hidden"><div style="width:22px;height:22px;border-radius:50%;background:#fff;margin-bottom:-2px;'
            f'box-shadow:0 26px 0 6px #fff"></div></div>'
            f'<div style="flex:1;border-bottom:3px solid #ffffffcc;padding-bottom:8px;font-size:36px;color:#fff;white-space:nowrap">{buchst}'
            f'<span id="{id_}-cur" style="display:inline-block;width:3px;height:38px;background:#fff;vertical-align:middle;margin-left:2px"></span></div></div>'
            f'<div style="display:flex;justify-content:flex-end;align-items:center;gap:30px;margin-top:20px"><span style="font-size:30px;color:#ffffffaa;font-weight:600">Abbrechen</span>'
            f'<span style="position:relative;display:inline-block"><span id="{id_}-btn" style="display:inline-block;padding:12px 34px;border-radius:30px;background:{ORANGE};'
            f'color:#111;font-weight:800;font-size:32px;white-space:nowrap">{knopf}</span>{k2}</span></div></div>'
            + f'<div id="{id_}-z" style="position:absolute;left:560px;top:{y + 330}px;width:58px;height:58px;z-index:30;opacity:0">{ZEIGER}</div>'
            + f'<div id="{id_}-bn" style="position:absolute;left:0;width:1080px;top:{y + 300}px;display:flex;justify-content:center;z-index:27;opacity:0">'
              f'<span style="padding:18px 40px;border-radius:40px;background:#101722e8;border:1px solid #ffffff22;color:#fff;font-weight:900;font-size:40px;letter-spacing:3px;'
              f'white-space:nowrap">{banner1} <span style="color:{ORANGE}">{banner2}</span></span></div>')


def cta_overlay_js(id_, t, n_zeichen, sfx=None, tipp=1.5):
    """Ablauf: Feld + Banner rein, Text tippt (Tastatur-Sound), Zeiger fährt zum Button, Klick (Sound), Button wird grün/zweiter Text."""
    klick = t + 0.5 + tipp + 0.9
    s = (f' tl.fromTo("#{id_}", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {t});'
         f' tl.fromTo("#{id_}-bn", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {t} + 0.15);'
         f' tl.to("#{id_} .tz", {{ opacity: 1, duration: 0.01, stagger: {tipp / max(n_zeichen, 1):.3f} }}, {t} + 0.5);'
         f' tl.fromTo("#{id_}-cur", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.3, repeat: 13, yoyo: true, ease: "steps(1)" }}, {t} + 0.3);'
         f' tl.fromTo("#{id_}-z", {{ x: -200, y: 120, opacity: 0 }}, {{ x: 230, y: -160, opacity: 1, duration: 0.8, ease: "power2.inOut" }}, {t} + 0.5 + {tipp});'
         f' tl.to("#{id_}-z", {{ scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }}, {klick});'
         f' tl.to("#{id_}-btn", {{ scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }}, {klick});'
         f' tl.to("#{id_}-k2", {{ opacity: 1, duration: 0.15 }}, {klick} + 0.15);')
    if sfx is not None:
        sfx += [(t, "whoosh-weich"), (t + 0.5, "tippen"), (klick, "klick")]
    return s


def ohne_untertitel_zwischen(here, von, bis):
    """Untertitel entfernen, die zwischen `von` und `bis` Sekunden starten (Nutzer 26.11.: kein Untertitel beim Kommentar-Bild).
    Nach glow_short.build aufrufen. Gleiche Logik wie ohne_untertitel()."""
    import re
    p = Path(here) / "index.html"
    s = p.read_text()
    weg = [m.group(1) for m in re.finditer(r'<div id="c(\d+)" class="cap clip" data-start="([\d.]+)"', s) if von - 0.01 <= float(m.group(2)) < bis]
    zeilen = []
    for z in s.split("\n"):
        if any(f'id="c{n}" class="cap clip"' in z or f'"#w{n}-' in z for n in weg):
            continue
        zeilen.append(z)
    p.write_text("\n".join(zeilen))
