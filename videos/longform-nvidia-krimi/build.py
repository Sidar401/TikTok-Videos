#!/usr/bin/env python3
"""HundeFinanzTv Longform (Analyse-Look): Spionage-Krimi bei Nvidia – und was er mit deinem ETF zu tun hat.
python3 build.py        → 9:16 (TikTok/Instagram)
python3 build.py quer   → 16:9 (YouTube): gleiche Szenen mittig skaliert + Kapitel-Leiste links + Nvidia-Kurs rechts."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import glow_short  # noqa: E402
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, QUER_CSS, ROT, donut, flagge, hand, kalender, karte, kasten, kit_assets,  # noqa: E402
                         kreis, linie, logo_karte, person, pfeil, rahmen, raster, stempel, unterstrich, zettel)
from glow_short import BLASE_SVG, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402

QUER = "quer" in sys.argv
NV = "#76b900"
kit_assets(HERE, ["nvidia", "apple", "microsoft", "amazon", "google", "amd", "doj", "flagge-usa", "flagge-china", "flagge-singapur", "msci"])
cap, st, en, DAUER = zeiten(HERE)
import shutil  # noqa: E402
FOTO = HERE.parent.parent / "brand/fotos/jensen-huang.jpg"
JH = {}
if FOTO.exists():
    (HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)
    shutil.copy(FOTO, HERE / "assets/fotos/jensen-huang.jpg")
    JH = {"foto": "assets/fotos/jensen-huang.jpg", "credit": "Foto: Peter Dasilva · CC BY 4.0"}


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def megaspeed(id_, x, y, w=420, h=130):
    return logo_karte(id_, "", x, y, w, h, text="MEGASPEED", farbe="#1c3f8f", glow="#4d8ff0", pad=0.22).replace(f"font-size:{h * 0.5:.0f}px", f"font-size:{h * 0.34:.0f}px")


def msci(id_, x, y, w=360, h=120):
    if (HERE / "assets/logos/msci.svg").exists():
        return logo_karte(id_, "msci", x, y, w, h, pad=0.2)
    return logo_karte(id_, "", x, y, w, h, text="MSCI", farbe="#002f6c", pad=0.2)


def kapitel(n, titel):
    return (tz(f"k{n}-a", f"TEIL {n}", 560, 96, "glow-o") + tz(f"k{n}-b", f'<span class="box">{titel}</span>', 710, 110)
            + unterstrich(f"k{n}-u", 290, 880, 500, GELB))


def kj(n):
    return lambda a, d: f'slam("#k{n}-a", {a}); pop("#k{n}-b", {a} + 0.25); draw("#k{n}-u-p", {a} + 0.6, 0.4); flash({a}, 0.4);'


SZ, SFX = [], []


def szene(t0, t1, html, js):
    SZ.append((t0, t1, rahmen(html, QUER), js))


# ---------------- Intro ----------------
CRASH = linie("i-l", [0.95, 0.9, 0.93, 0.85, 0.88, 0.7, 0.62, 0.66, 0.35, 0.12], 120, 720, 840, 420, ROT, punkte=[(9, "−10 %")])
szene(0.0, st("s2"), KIT_CSS + (QUER_CSS if QUER else "") + logo_karte("i-nv", "nvidia", 290, 450, 500, 140, glow=NV) + CRASH
      + tz("i-z", "hunderte Mrd. $", 1180, 76, "glow-r") + stempel("i-s", "SPIONAGE-VERDACHT", 140, 610, ROT, 54, -8),
      lambda a, d: (KIT_JS + f' pop("#i-nv", {a}); draw("#i-l-p", {cap("s1", 1)}, 1.2); tl.fromTo("#i-l-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s1", 1)} + 0.8);'
                    f' pop("#i-l-w0", {cap("s1", 2)} + 0.3); slam("#i-z", {cap("s1", 2)}); stempeln("#i-s", {a} + 0.2); flash({a} + 0.2, 0.5);'))
SFX += [(0.0, "nv-boom-tief"), (0.2, "stempel"), (cap("s1", 1), "kurve-runter"), (cap("s1", 2), "bass-schlag")]

szene(st("s2"), st("s3"), person("j-p", "Jensen Huang", "Chef von Nvidia", 90, 450, 380, NV, **JH) + logo_karte("j-nv", "nvidia", 560, 520, 430, 130, glow=NV)
      + hand("j-h", "wertvollste<br/>Chipfirma der Welt", 770, 680, 46, GELB, -4, True) + pfeil("j-pf", 760, 780, 520, 900, -0.3, GELB, 7)
      + kreis("j-k", 280, 735, 210, 60, GELB, 6),
      lambda a, d: (f'pop("#j-nv", {a}); pop("#j-h", {cap("s2", 2)}); draw("#j-pf-p", {cap("s2", 3)}, 0.4); pop("#j-pf-k", {cap("s2", 3)} + 0.35);'
                    f' pop("#j-p", {cap("s2", 4)}); draw("#j-k-p", {cap("s2", 4)} + 0.4, 0.5);'))
SFX += [(st("s2"), "whoosh-weich"), (cap("s2", 2), "klick"), (cap("s2", 4), "pop")]

GRID = raster("g3", 270, 470, 10, 10, 46, 8, "#3a4248")
szene(st("s3"), st("s4"), GRID + tz("g3-t", "dein ETF", 1050, 70) + hand("g3-h", "steckt Nvidia drin?", 540, 1150, 58, GELB, -3, True)
      + logo_karte("g3-nv", "nvidia", 650, 430, 300, 90, glow=NV),
      lambda a, d: (f'tl.fromTo("#g3 .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.006 }}, {a}); pop("#g3-t", {cap("s3", 1)});'
                    f' tl.to("#g3 .q:nth-child(-n+6)", {{ background: "{NV}", boxShadow: "0 0 20px {NV}", duration: 0.2, stagger: 0.08 }}, {cap("s3", 3)});'
                    f' pop("#g3-nv", {cap("s3", 3)}); pop("#g3-h", {cap("s3", 4)});'))
SFX += [(st("s3"), "swipe"), (cap("s3", 3), "pop"), (cap("s3", 4), "nv-pling-idee")]

AG = [("① Was ist passiert?", "s4", 1), ("② Warum fällt die Aktie?", "s4", 2), ("③ Was heißt das für deinen ETF?", "s4", 3)]
szene(st("s4"), st("s5"), karte("ag-k", 90, 440, 900, 820, "Heute im Video", "3 Teile · ca. 3 Minuten")
      + "".join(kasten(f"ag-{i}", txt, 150, 620 + i * 200, 780, 150, (OR, ROT, GRUEN)[i], 48) for i, (txt, *_) in enumerate(AG)),
      lambda a, d: f'pop("#ag-k", {a});' + "".join(f' pop("#ag-{i}", {cap(s, c)});' for i, (_, s, c) in enumerate(AG)))
SFX += [(st("s4"), "whoosh-weich")] + [(cap(s, c), "klick") for _, s, c in AG]

szene(st("s5"), st("s6"), zettel("hw-z", "Keine Anlage&shy;beratung", 220, 480, 640, 84, GELB, -3) + stempel("hw-s", "NUR BERICHTE", 150, 860, OR, 66, -6)
      + stempel("hw-s2", "NICHTS BEWIESEN", 190, 1050, ROT, 60, 5),
      lambda a, d: (f'tl.fromTo("#hw-z", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {cap("s5", 1)});'
                    f' stempeln("#hw-s", {cap("s5", 3)}); stempeln("#hw-s2", {cap("s5", 4)});'))
SFX += [(st("s5"), "swipe"), (cap("s5", 3), "stempel"), (cap("s5", 4), "stempel")]

# ---------------- Teil 1: der Verdacht ----------------
szene(st("s6"), st("s7"), kapitel(1, "Der Verdacht"), kj(1))
SFX += [(st("s6"), "nv-dun-dun-dun")]

VERB = ('<svg id="vb" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:2">'
        f'<path id="vb-p" d="M400 760 Q540 690 680 760" fill="none" stroke="{GELB}" stroke-width="8" stroke-dasharray="18 16" stroke-linecap="round"/></svg>')
szene(st("s7"), st("s9"), person("p1", "Jensen Huang", "Nvidia", 70, 560, 330, NV, **JH) + person("p2", "Alice Huang", "Megaspeed", 680, 560, 330, "#4d8ff0") + VERB
      + hand("vb-h", "enge private Beziehung", 540, 620, 50, GELB, -3, True) + chip("vb-c", "laut Berichten", GRAU, 460, 46)
      + stempel("vb-s", "NICHT VERWANDT", 200, 1080, OR, 66, -5) + hand("vb-h2", "nur gleicher Nachname", 540, 1210, 52, GELB, 2, True),
      lambda a, d: (f'pop("#vb-c", {a}); pop("#p1", {cap("s7", 1)}); pop("#p2", {cap("s7", 4)}); tl.fromTo("#vb-p", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {cap("s7", 3)});'
                    f' pop("#vb-h", {cap("s7", 3)}); stempeln("#vb-s", {cap("s8", 1)}); pop("#vb-h2", {cap("s8", 3)});'))
SFX += [(st("s7"), "whoosh-weich"), (cap("s7", 1), "pop"), (cap("s7", 4), "pop"), (cap("s7", 3), "nv-sog"), (cap("s8", 1), "stempel")]

szene(st("s9"), st("s10"), person("ms-p", "Alice Huang", "Managerin", 90, 450, 300, "#4d8ff0") + megaspeed("ms-m", 500, 470, 480, 140)
      + flagge("ms-f", "flagge-singapur", 620, 650, 240, 4) + hand("ms-fh", "Singapur", 740, 830, 52, "#fff", -2, True)
      + logo_karte("ms-nv", "nvidia", 120, 1020, 380, 110, glow=NV) + pfeil("ms-pf", 520, 1075, 760, 1000, -0.3, NV, 8) + hand("ms-h", "kauft KI-Chips", 780, 1080, 56, GELB, -4, True),
      lambda a, d: (f'pop("#ms-p", {a}); pop("#ms-m", {cap("s9", 1)}); tl.fromTo("#ms-f", {{ y: -200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {cap("s9", 2)});'
                    f' pop("#ms-fh", {cap("s9", 2)} + 0.2); pop("#ms-nv", {cap("s9", 3)}); draw("#ms-pf-p", {cap("s9", 3)} + 0.2, 0.4); pop("#ms-pf-k", {cap("s9", 3)} + 0.55); pop("#ms-h", {cap("s9", 3)} + 0.6);'))
SFX += [(st("s9"), "swipe"), (cap("s9", 1), "klick"), (cap("s9", 2), "pop"), (cap("s9", 3), "kasse")]

szene(st("s10"), st("s11"), flagge("gd-us", "flagge-usa", 110, 480, 320, -4) + hand("gd-h", "US-Geheimdienste vermuten …", 340, 700, 42, GELB, -3, True)
      + flagge("gd-cn", "flagge-china", 640, 600, 330, 5) + tz("gd-q", "?", 380, 380, "glow-r") + person("gd-p", "Alice Huang", "Spionin?", 380, 840, 320, ROT)
      + stempel("gd-s", "VERDACHT", 520, 1150, ROT, 64, -8),
      lambda a, d: (f'pop("#gd-us", {a}); pop("#gd-h", {cap("s10", 1)}); tl.fromTo("#gd-cn", {{ x: 300, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4 }}, {cap("s10", 2)});'
                    f' slam("#gd-q", {cap("s10", 2)} + 0.2); pop("#gd-p", {cap("s10", 3)}); stempeln("#gd-s", {cap("s10", 3)} + 0.5);'))
SFX += [(st("s10"), "nv-whoosh-tief"), (cap("s10", 2), "herzschlag"), (cap("s10", 3) + 0.5, "stempel")]

BL = lambda id_, txt, x, y, f, dreh: (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:440px;padding:30px 34px;border-radius:30px 30px 30px 6px;background:#14181b;'  # noqa: E731
                                     f'border:5px solid {f};box-shadow:0 0 40px {f}55;font-weight:900;font-size:46px;color:#fff;line-height:1.1;transform:rotate({dreh}deg);z-index:3">{txt}</div>')
szene(st("s11"), st("s12"), flagge("de-cn", "flagge-china", 110, 450, 220, -3) + BL("de-b1", "„Das stimmt nicht.“", 80, 640, ROT, -2)
      + logo_karte("de-nv", "nvidia", 620, 790, 360, 110, glow=NV) + BL("de-b2", "„Keine Geheimnisse weitergegeben.“", 560, 950, NV, 2),
      lambda a, d: f'pop("#de-cn", {a}); pop("#de-b1", {a} + 0.3); pop("#de-nv", {cap("s11", 1)}); pop("#de-b2", {cap("s11", 2)});')
SFX += [(st("s11"), "swipe"), (st("s11") + 0.3, "pop"), (cap("s11", 2), "pop")]

# ---------------- Teil 2: die Chips ----------------
szene(st("s12"), st("s13"), kapitel(2, "Die Chips"), kj(2))
SFX += [(st("s12"), "nv-boom-kurz")]

CHIP = (f'<svg id="ch" viewBox="0 0 200 200" style="position:absolute;left:440px;top:560px;width:200px;height:200px;z-index:4;filter:drop-shadow(0 0 20px {NV})">'
        f'<rect x="45" y="45" width="110" height="110" rx="14" fill="#1b1f22" stroke="{NV}" stroke-width="8"/><rect x="75" y="75" width="50" height="50" rx="6" fill="{NV}"/>'
        + "".join(f'<rect x="{60 + k * 30}" y="15" width="10" height="28" rx="4" fill="{NV}"/><rect x="{60 + k * 30}" y="157" width="10" height="28" rx="4" fill="{NV}"/>'
                  f'<rect x="15" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{NV}"/><rect x="157" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{NV}"/>' for k in range(3))
        + '</svg>')
KREUZ = (f'<svg id="kz" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:5">'
         f'<path id="kz-a" d="M470 560 L610 760" stroke="{ROT}" stroke-width="16" stroke-linecap="round"/><path id="kz-b" d="M610 560 L470 760" stroke="{ROT}" stroke-width="16" stroke-linecap="round"/></svg>')
szene(st("s13"), st("s14"), flagge("ex-us", "flagge-usa", 70, 600, 300, -3) + CHIP + flagge("ex-cn", "flagge-china", 720, 600, 290, 3) + KREUZ
      + stempel("ex-s", "EXPORT-VERBOT", 230, 960, ROT, 74, -6) + hand("ex-h", "moderne KI-Chips", 540, 470, 56, NV, -3, True),
      lambda a, d: (f'pop("#ch", {a}); pop("#ex-h", {a} + 0.2); pop("#ex-us", {cap("s13", 1)}); pop("#ex-cn", {cap("s13", 2)});'
                    f' draw("#kz-a", {cap("s13", 2)} + 0.4, 0.2); draw("#kz-b", {cap("s13", 2)} + 0.6, 0.2); stempeln("#ex-s", {cap("s13", 2)} + 0.9);'))
SFX += [(st("s13"), "whoosh-weich"), (cap("s13", 2) + 0.4, "falsch"), (cap("s13", 2) + 0.9, "stempel")]

szene(st("s14"), st("s15"), flagge("wg-us", "flagge-usa", 60, 470, 230, -3) + megaspeed("wg-m", 330, 640, 420, 120) + flagge("wg-sg", "flagge-singapur", 440, 780, 200, 3)
      + flagge("wg-cn", "flagge-china", 790, 470, 230, 3) + pfeil("wg-p1", 200, 640, 380, 700, 0.25, NV, 8) + pfeil("wg-p2", 700, 690, 880, 640, 0.25, ROT, 8)
      + hand("wg-h", "Umweg?", 870, 760, 60, GELB, -6, True) + tz("wg-z", "7,5", 940, 200, "glow-r") + tz("wg-u", "Mrd. $ (laut Bericht)", 1170, 52),
      lambda a, d: (f'pop("#wg-us", {cap("s14", 1)} - 0.3); pop("#wg-m", {cap("s14", 1)}); pop("#wg-sg", {cap("s14", 1)} + 0.2); draw("#wg-p1-p", {cap("s14", 1)} + 0.3, 0.4); pop("#wg-p1-k", {cap("s14", 1)} + 0.7);'
                    f' pop("#wg-cn", {cap("s14", 2)}); draw("#wg-p2-p", {cap("s14", 2)} + 0.2, 0.4); pop("#wg-p2-k", {cap("s14", 2)} + 0.55); pop("#wg-h", {cap("s14", 3)});'
                    f' slam("#wg-z", {cap("s14", 5)}); pop("#wg-u", {cap("s14", 5)} + 0.3);'))
SFX += [(st("s14"), "swipe"), (cap("s14", 1) + 0.3, "whoosh-schnell"), (cap("s14", 2) + 0.2, "whoosh-schnell"), (cap("s14", 5), "kasse")]

ZL = (f'<div id="zl-l" style="position:absolute;left:150px;top:820px;width:780px;height:10px;border-radius:5px;background:linear-gradient(90deg,{OR},{ROT});transform-origin:0 50%;z-index:2"></div>')
szene(st("s15"), st("s16"), karte("zl-k", 70, 440, 940, 820, "Ermittlungen", "gegen Megaspeed") + ZL
      + kalender("zl-a", "SEIT", "2024", 110, 560, 240, OR) + kalender("zl-b", "HEUTE", "2026", 730, 560, 240, ROT)
      + logo_karte("zl-doj", "doj", 640, 900, 340, 240, pad=0.08) + hand("zl-h", "Justizministerium der USA", 370, 960, 48, GELB, -3, True),
      lambda a, d: (f'pop("#zl-k", {a}); pop("#zl-a", {a} + 0.2); tl.fromTo("#zl-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8 }}, {cap("s15", 1)}); pop("#zl-b", {cap("s15", 2)});'
                    f' pop("#zl-doj", {cap("s15", 3)}); pop("#zl-h", {cap("s15", 3)} + 0.3);'))
SFX += [(st("s15"), "whoosh-weich"), (cap("s15", 1), "uhr-tickt"), (cap("s15", 3), "bass-schlag")]

LUPE = (f'<svg id="lu" viewBox="0 0 200 200" style="position:absolute;left:620px;top:700px;width:300px;height:300px;z-index:5;filter:drop-shadow(0 0 20px {GELB})">'
        f'<circle cx="80" cy="80" r="56" fill="#ffffff10" stroke="{GELB}" stroke-width="14"/><path d="M122 122 L180 180" stroke="{GELB}" stroke-width="20" stroke-linecap="round"/></svg>')
szene(st("s16"), st("s17"), logo_karte("uv-nv", "nvidia", 140, 480, 460, 130, glow=NV) + hand("uv-h", "Vorstand", 370, 650, 60, GELB, -3, True)
      + kasten("uv-k", "unabhängige<br/>Untersuchung", 120, 780, 520, 260, OR, 58) + LUPE + stempel("uv-s", "LÄUFT", 640, 1080, OR, 70, 8),
      lambda a, d: (f'pop("#uv-nv", {a}); pop("#uv-h", {a} + 0.3); pop("#uv-k", {cap("s16", 2)});'
                    f' tl.fromTo("#lu", {{ x: 200, y: -200, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.5 }}, {cap("s16", 3)}); stempeln("#uv-s", {cap("s16", 3)} + 0.6);'))
SFX += [(st("s16"), "swipe"), (cap("s16", 2), "klick"), (cap("s16", 3) + 0.6, "stempel")]

fr_html, fr_js = cta_szene("fr", BLASE_SVG, "Sturm im Wasserglas –<br/>oder echtes Problem?")
szene(st("s17"), st("s18"), fr_html + chip("fr-a", "🌊 Wasserglas", GRUEN, 1100, 52, 130) + chip("fr-b", "⚠️ Problem", ROT, 1100, 52, 600),
      lambda a, d: fr_js(a, d) + f' pop("#fr-a", {cap("s17", 3)}); pop("#fr-b", {cap("s17", 4)});')
SFX += [(st("s17"), "handy-benachrichtigung"), (cap("s17", 3), "pop"), (cap("s17", 4), "pop")]

# ---------------- Teil 3: die Aktie ----------------
szene(st("s18"), st("s19"), kapitel(3, "Die Aktie"), kj(3))
SFX += [(st("s18"), "nv-boom-kurz")]

ZW = linie("zw", [0.9, 0.86, 0.88, 0.5, 0.53, 0.47, 0.1], 150, 680, 780, 440, ROT, punkte=[(3, "Mo −4 %"), (6, "Di −6 %")])
szene(st("s19"), st("s20"), karte("zw-k", 70, 440, 940, 820, "Nvidia-Aktie", "Montag + Dienstag") + ZW
      + logo_karte("zw-nv", "nvidia", 650, 470, 320, 90, glow=NV),
      lambda a, d: (f'pop("#zw-k", {a}); pop("#zw-nv", {a} + 0.2); draw("#zw-p", {cap("s19", 0)}, 1.0); pop("#zw-w0", {cap("s19", 1)} + 0.3);'
                    f' tl.fromTo("#zw-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s19", 3)}); pop("#zw-w1", {cap("s19", 3)} + 0.3);'))
SFX += [(st("s19"), "whoosh-weich"), (cap("s19", 1), "kurve-runter"), (cap("s19", 3), "kurve-runter")]

szene(st("s20"), st("s21"), tz("ew-a", "an EINEM Tag", 470, 70) + tz("ew-z", "250", 600, 300, "glow-r") + tz("ew-u", "Mrd. $ weg", 930, 100)
      + kreis("ew-k", 540, 760, 330, 200, GELB) + partikel("ew-p", 540, 760, 30, (ROT, GELB, "#fff"), 600) + hand("ew-h", "≈ Wert von SAP + Siemens", 540, 1110, 52, GELB, -3, True),
      lambda a, d: (f'pop("#ew-a", {a}); pop("#ew-z", {cap("s20", 1)}); zaehl("#ew-z", 0, 250, {cap("s20", 1)}, 1.0); burst("#ew-p", {cap("s20", 1)} + 0.9);'
                    f' pop("#ew-u", {cap("s20", 2)}); draw("#ew-k-p", {cap("s20", 2)} + 0.3, 0.5);'))
SFX += [(st("s20"), "zaehler"), (cap("s20", 1) + 0.9, "glas-bricht")]

OKT = linie("ok", [0.55, 0.7, 0.85, 0.97, 0.9, 0.8, 0.72, 0.78, 0.6, 0.45, 0.3], 140, 650, 800, 480, ROT, punkte=[(3, "Rekord"), (10, "−30 %")])
szene(st("s21"), st("s22"), karte("ok-k", 70, 440, 940, 820, "Seit dem Rekord", "Oktober → heute") + OKT + kreis("ok-kr", 870, 1000, 120, 90, GELB, 6)
      + tz("ok-z", "1,7 Billionen $", 1150, 80, "glow-r"),
      lambda a, d: (f'pop("#ok-k", {a}); draw("#ok-p", {a} + 0.2, 1.3); pop("#ok-w0", {a} + 0.8); pop("#ok-w1", {cap("s21", 1)} + 0.3); draw("#ok-kr-p", {cap("s21", 1)} + 0.6, 0.5);'
                    f' slam("#ok-z", {cap("s21", 3)});'))
SFX += [(st("s21"), "kurve-runter"), (cap("s21", 3), "bass-schlag")]

szene(st("s22"), st("s23"), flagge("in-us", "flagge-usa", 380, 450, 320, -3) + kasten("in-a", "Inflation ↑", 100, 720, 400, 170, ROT, 64)
      + pfeil("in-p", 510, 805, 600, 805, 0.0, "#fff", 8) + kasten("in-b", "Zinsen ↑ ?", 600, 720, 380, 170, OR, 64) + stempel("in-s", "SCHLECHTE NACHRICHT", 150, 990, ROT, 56, -5),
      lambda a, d: (f'pop("#in-us", {cap("s22", 1)}); pop("#in-a", {cap("s22", 2)}); draw("#in-p-p", {cap("s22", 3)}, 0.3); pop("#in-p-k", {cap("s22", 3)} + 0.25);'
                    f' pop("#in-b", {cap("s22", 4)}); stempeln("#in-s", {cap("s22", 4)} + 0.6);'))
SFX += [(st("s22"), "swipe"), (cap("s22", 2), "kurve-hoch"), (cap("s22", 4), "alarm")]

# ---------------- Teil 4: dein Geld ----------------
szene(st("s23"), st("s24"), kapitel(4, "Dein Geld"), kj(4))
SFX += [(st("s23"), "nv-boom-kurz")]

RANG = [("nvidia", "1", NV), ("apple", "2", "#aaa"), ("microsoft", "3", "#4d8ff0")]
szene(st("s24"), st("s25"), msci("ms-k", 360, 450, 360, 120) + hand("ms-w", "World · beliebtester ETF", 540, 590, 50, GELB, -2, True)
      + "".join(f'<div id="rg-n{i}" style="position:absolute;left:140px;top:{700 + i * 170}px;width:110px;height:110px;border-radius:50%;background:{f};color:#111;font-weight:900;font-size:64px;'
                f'display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px {f};z-index:3">{r}</div>' + logo_karte(f"rg-{i}", n, 290, 690 + i * 170, 420, 130)
                for i, (n, r, f) in enumerate(RANG)) + stempel("rg-s", "PLATZ 1", 700, 700, NV, 56, 8),
      lambda a, d: (f'pop("#ms-k", {cap("s24", 2)}); pop("#ms-w", {cap("s24", 3)});' + "".join(f' pop("#rg-n{i}", {cap("s24", 1)} + {0.2 * i}); pop("#rg-{i}", {cap("s24", 1)} + {0.2 * i});' for i in range(3))
                    + f' stempeln("#rg-s", {cap("s24", 4)});'))
SFX += [(st("s24"), "whoosh-weich"), (cap("s24", 1), "pop"), (cap("s24", 2), "klick"), (cap("s24", 4), "stempel")]

szene(st("s25"), st("s26"), raster("g25", 270, 460, 10, 10, 46, 8, "#3a4248") + tz("g25-t", "100 € im ETF", 1010, 64)
      + hand("g25-h", "≈ 6 € Nvidia", 770, 430, 60, NV, -6, True) + pfeil("g25-p", 800, 540, 560, 500, 0.3, NV, 7),
      lambda a, d: (f'tl.fromTo("#g25 .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.005 }}, {a}); pop("#g25-t", {a} + 0.3);'
                    f' tl.to("#g25 .q:nth-child(-n+6)", {{ background: "{NV}", boxShadow: "0 0 20px {NV}", duration: 0.2, stagger: 0.1 }}, {cap("s25", 2)});'
                    f' pop("#g25-h", {cap("s25", 2)} + 0.6); draw("#g25-p-p", {cap("s25", 2)} + 0.8, 0.4); pop("#g25-p-k", {cap("s25", 2)} + 1.15);'))
SFX += [(st("s25"), "zaehler"), (cap("s25", 2), "muenzen-klimpern")]

ZEILE = 'style="display:flex;justify-content:space-between;font-size:58px;margin:18px 0"'
szene(st("s26"), st("s27"), f'<div id="rc-k" class="mono" style="position:absolute;left:120px;top:470px;width:840px;padding:50px 56px;border-radius:30px;background:#14181bee;border:3px solid #ffffff22;box-shadow:0 30px 60px #000;z-index:2;color:#fff">'
      f'<div style="font-family:Montserrat;font-weight:900;font-size:44px;color:{GRAU};margin-bottom:16px">Rechnung</div>'
      f'<div id="rc-1" {ZEILE}><span>Nvidia</span><span style="color:{ROT}">− 10 %</span></div>'
      f'<div id="rc-2" {ZEILE}><span>Anteil</span><span>× 6 %</span></div>'
      f'<div id="rc-l" style="height:6px;background:#fff;margin:24px 0;transform-origin:0 50%"></div>'
      f'<div id="rc-3" {ZEILE}><span>dein ETF</span><span style="color:{ROT};text-shadow:0 0 30px {ROT}">≈ − 0,6 %</span></div></div>'
      + stempel("rc-s", "≈ HALBES PROZENT", 200, 1060, OR, 60, -5),
      lambda a, d: (f'pop("#rc-k", {a}); pop("#rc-1", {a} + 0.2); pop("#rc-2", {cap("s26", 1)}); tl.fromTo("#rc-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4 }}, {cap("s26", 2)});'
                    f' slam("#rc-3", {cap("s26", 2)} + 0.3); stempeln("#rc-s", {cap("s26", 3)});'))
SFX += [(st("s26"), "taschenrechner"), (cap("s26", 2) + 0.3, "klick"), (cap("s26", 3), "stempel")]

DOM = [("nvidia", 80, 470), ("microsoft", 560, 470), ("apple", 80, 690), ("amazon", 560, 690), ("google", 80, 910), ("amd", 560, 910)]
szene(st("s27"), st("s28"), "".join(logo_karte(f"dm-{n}", n, x, y, 440, 150) for n, x, y in DOM) + hand("dm-h", "alles KI – alles verbunden", 540, 1110, 54, GELB, -3, True),
      lambda a, d: ("".join(f' pop("#dm-{n}", {cap("s27", 1)} + {0.12 * i});' for i, (n, *_) in enumerate(DOM)) + f' pop("#dm-h", {cap("s27", 2)});'
                    + "".join(f' tl.fromTo("#dm-{n}", {{ rotation: -4 }}, {{ rotation: 4, duration: 0.09, yoyo: true, repeat: 7, ease: "none" }}, {cap("s27", 3)} + {0.1 * i});' for i, (n, *_) in enumerate(DOM))
))
SFX += [(st("s27"), "swipe"), (cap("s27", 3), "nv-erdbeben")]

# ---------------- Teil 5: was jetzt kommt ----------------
szene(st("s28"), st("s29"), kapitel(5, "Was jetzt kommt").replace("font-size:110px", "font-size:84px"), kj(5))
SFX += [(st("s28"), "nv-boom-kurz")]

szene(st("s29"), st("s30"), kalender("wa-k", "NOV", "18", 110, 470, 330, ROT) + person("wa-p", "Jensen Huang", "Aussage", 620, 470, 330, NV, **JH)
      + flagge("wa-f", "flagge-usa", 250, 950, 260, -4) + hand("wa-h", "Washington", 720, 1010, 70, GELB, -3, True),
      lambda a, d: f'pop("#wa-k", {a}); pop("#wa-p", {cap("s29", 1)}); pop("#wa-f", {cap("s29", 2)}); pop("#wa-h", {cap("s29", 2)} + 0.2);')
SFX += [(st("s29"), "whoosh-weich"), (st("s29"), "stempel"), (cap("s29", 2), "pop")]

szene(st("s30"), st("s31"), logo_karte("qz-nv", "nvidia", 290, 460, 500, 140, glow=NV) + kasten("qz-k", "Quartals&shy;zahlen", 190, 700, 700, 220, OR, 80, "in den nächsten Tagen")
      + tz("qz-q", "?", 980, 200, "glow-o"),
      lambda a, d: f'pop("#qz-nv", {a}); pop("#qz-k", {cap("s30", 1)}); slam("#qz-q", {cap("s30", 2)});')
SFX += [(st("s30"), "swipe"), (cap("s30", 2), "spannung")]

szene(st("s31"), st("s32"), logo_karte("sz-nv", "nvidia", 370, 450, 340, 100, glow=NV) + pfeil("sz-p1", 480, 600, 230, 820, 0.2, GRUEN, 12) + pfeil("sz-p2", 600, 600, 850, 820, -0.2, ROT, 12)
      + kasten("sz-a", "stark<br/>→ Erholung", 70, 860, 420, 220, GRUEN, 54) + kasten("sz-b", "enttäuschend<br/>→ weiter runter", 590, 860, 420, 220, ROT, 50),
      lambda a, d: (f'pop("#sz-nv", {a}); draw("#sz-p1-p", {a} + 0.2, 0.4); pop("#sz-p1-k", {a} + 0.55); pop("#sz-a", {cap("s31", 2)});'
                    f' draw("#sz-p2-p", {cap("s31", 3)}, 0.4); pop("#sz-p2-k", {cap("s31", 3)} + 0.35); pop("#sz-b", {cap("s31", 4)});'))
SFX += [(st("s31"), "whoosh-weich"), (cap("s31", 2), "kurve-hoch"), (cap("s31", 4), "kurve-runter")]

# ---------------- Teil 6: Was heißt das für dich? ----------------
szene(st("s32"), st("s33"), kapitel(6, "Was heißt das für dich?").replace("font-size:110px", "font-size:64px"), kj(6))
SFX += [(st("s32"), "nv-boom-kurz")]

ERH = linie("t1", [0.8, 0.7, 0.45, 0.25, 0.3, 0.5, 0.65, 0.85, 0.95], 150, 680, 780, 420, GRUEN, punkte=[(3, "Panik-Verkauf?"), (8, "Erholung")])
szene(st("s33"), st("s34"), karte("t1-k", 70, 440, 940, 820, "Tipp 1: Keine Panik", "Krisen gab es immer") + ERH
      + kreis("t1-kr", 400, 950, 120, 80, ROT, 6),
      lambda a, d: (f'pop("#t1-k", {a}); draw("#t1-p", {a} + 0.3, 1.6); pop("#t1-w0", {cap("s33", 2)}); draw("#t1-kr-p", {cap("s33", 2)} + 0.2, 0.4);'
                    f' pop("#t1-w1", {cap("s33", 3)});'))
SFX += [(st("s33"), "whoosh-weich"), (cap("s33", 2), "falsch"), (cap("s33", 3), "kurve-hoch")]

szene(st("s34"), st("s35"), karte("t2-k", 70, 440, 940, 820, "Tipp 2: Hinschauen", "Wie viel hängt an KI?") + donut("t2-d", 540, 860, 230, [(0.28, OR), (0.72, "#3a4248")], 80)
      + tz("t2-z", "≈ 28 %", 800, 84, "glow-o") + hand("t2-h", "Top 10 im MSCI World", 540, 1150, 52, GELB, -3, True),
      lambda a, d: f'pop("#t2-k", {a}); draw("#t2-d-1", {a} + 0.2, 0.5); draw("#t2-d-0", {cap("s34", 1)}, 0.6); pop("#t2-z", {cap("s34", 2)}); pop("#t2-h", {cap("s34", 2)} + 0.3);')
SFX += [(st("s34"), "swipe"), (cap("s34", 2), "nv-pling-idee")]

SP = ("".join(f'<div class="sp1" style="position:absolute;left:{170 + k * 70}px;top:880px;width:56px;height:56px;border-radius:12px;background:{OR};box-shadow:0 0 14px {OR};z-index:3"></div>' for k in range(4))
      + "".join(f'<div class="sp2" style="position:absolute;left:{170 + k * 70}px;top:1060px;width:56px;height:56px;border-radius:12px;background:{GRUEN};box-shadow:0 0 14px {GRUEN};z-index:3"></div>' for k in range(10)))
szene(st("s35"), st("s36"), karte("t3-k", 70, 440, 940, 820, "Tipp 3: Sparplan läuft weiter", "gleicher Betrag, z. B. 100 €") + SP
      + f'<div class="mono" style="position:absolute;left:150px;top:800px;font-size:36px;color:#fff;z-index:3">Kurs hoch → 4 Anteile</div>'
      + f'<div class="mono" style="position:absolute;left:150px;top:980px;font-size:36px;color:{GRUEN};z-index:3">Kurs runter → mehr Anteile</div>'
      + stempel("t3-s", "MEHR FÜRS GELD", 380, 1150, GRUEN, 52, -5),
      lambda a, d: (f'pop("#t3-k", {a}); tl.fromTo(".sp1", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.08 }}, {cap("s35", 1)});'
                    f' tl.fromTo(".sp2", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.08 }}, {cap("s35", 3)}); stempeln("#t3-s", {cap("s35", 4)} + 0.4);'))
SFX += [(st("s35"), "whoosh-weich"), (cap("s35", 3), "muenzen-glas"), (cap("s35", 4) + 0.4, "stempel")]

szene(st("s36"), DAUER, logo_karte("en-nv", "nvidia", 290, 480, 500, 140, glow=NV) + stempel("en-s", "FORTSETZUNG FOLGT", 150, 720, OR, 54, -6)
      + hand("en-h", "ruhig bleiben + genau hinschauen", 540, 940, 56, GELB, -3, True) + kreis("en-k", 540, 980, 420, 80, GELB, 6),
      lambda a, d: f'pop("#en-nv", {a}); stempeln("#en-s", {cap("s36", 1)}); pop("#en-h", {cap("s36", 2)}); draw("#en-k-p", {cap("s36", 3)}, 0.6);')
SFX += [(st("s36"), "whoosh-weich"), (cap("s36", 1), "nv-tusch")]

# ---------------- 16:9: Kapitel-Leiste links + Nvidia-Kurs rechts ----------------
if QUER:
    KAP = [(0.0, st("s6"), "Intro"), (st("s6"), st("s12"), "1 · Der Verdacht"), (st("s12"), st("s18"), "2 · Die Chips"), (st("s18"), st("s23"), "3 · Die Aktie"),
           (st("s23"), st("s28"), "4 · Dein Geld"), (st("s28"), st("s32"), "5 · Was jetzt kommt"), (st("s32"), DAUER, "6 · Für dich")]
    for i, (a0, a1, txt) in enumerate(KAP):
        html = (f'<div id="kl{i}" style="position:absolute;left:100px;top:330px;width:400px;z-index:4">'
                f'<div class="mono" style="font-size:30px;color:{GRAU}">KAPITEL</div><div style="font-weight:900;font-size:50px;color:#fff;line-height:1.1;margin-top:8px">{txt}</div>'
                f'<div style="margin-top:22px;height:8px;width:{60 + 50 * i}px;border-radius:4px;background:{OR};box-shadow:0 0 20px {OR}"></div></div>')
        SZ.append((a0, a1, html, (lambda j: lambda a, d: f'tl.fromTo("#kl{j}", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4 }}, {a});')(i), 4))
    RECHTS = (f'<div id="re" style="position:absolute;left:1440px;top:300px;width:410px;padding:28px;border-radius:26px;background:#14181bee;border:3px solid {NV}66;z-index:4">'
              f'<img src="assets/logos/nvidia.svg" style="width:220px;background:#fff;padding:14px 20px;border-radius:14px"/>'
              f'<div class="mono" style="font-size:28px;color:{GRAU};margin-top:20px">seit Okt.-Rekord</div>'
              f'<div style="font-weight:900;font-size:86px;color:{ROT};text-shadow:0 0 30px {ROT}">−30 %</div>'
              f'<div class="mono" style="font-size:28px;color:{GRAU}">2 Tage: ≈ −10 %</div></div>')
    SZ.append((st("s2"), DAUER, RECHTS, lambda a, d: f'tl.fromTo("#re", {{ x: 80, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5 }}, {a});', 5))
    glow_short.querformat()

if __name__ == "__main__":
    build(HERE, SZ, SFX)
