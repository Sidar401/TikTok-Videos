#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (Analyse-Look + Börsen-Laufband): Jensen Huang ist raus – was jetzt mit Nvidia und deinem ETF passiert."""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
WURZEL = HERE.parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
from analyse_kit import (GELB, GRAU, GRUEN, KIT_CSS, KIT_JS, OR, ROT, flagge, hand, kalender, karte, kasten, kit_assets, kreis,  # noqa: E402
                         laufband_szene, linie, logo_karte, person, pfeil, raster, stempel, unterstrich, zettel)
from glow_short import BLASE_SVG, build, chip, cta_szene, partikel, t, zeiten  # noqa: E402

NV = "#76b900"
kit_assets(HERE, ["nvidia", "amd", "broadcom", "apple", "msci", "flagge-usa"])
cap, st, en, DAUER = zeiten(HERE)

# Fotos (nur freie Fotos öffentlicher Personen, mit Lizenzzeile)
FQ = json.loads((WURZEL / "brand/fotos/quellen.json").read_text())
(HERE / "assets/fotos").mkdir(parents=True, exist_ok=True)


def foto(key):
    f = WURZEL / "brand/fotos" / f"{key}.jpg"
    if not f.exists() or f"{key}.jpg" not in FQ:
        return {}
    shutil.copy(f, HERE / "assets/fotos" / f.name)
    return {"foto": f"assets/fotos/{f.name}", "credit": FQ[f"{key}.jpg"]["einblenden"][:48]}


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def wort(id_, text, x, y, w, h, farbe, f="#fff"):
    return logo_karte(id_, "", x, y, w, h, text=text, farbe=farbe, pad=0.22).replace(f"font-size:{h * 0.5:.0f}px", f"font-size:{h * 0.36:.0f}px")


def kapitel(n, titel, gr=110):
    return (tz(f"k{n}-a", f"TEIL {n}", 560, 96, "glow-o") + tz(f"k{n}-b", f'<span class="box">{titel}</span>', 710, gr)
            + unterstrich(f"k{n}-u", 290, 880, 500, GELB))


def kj(n):
    return lambda a, d: f'slam("#k{n}-a", {a}); pop("#k{n}-b", {a} + 0.25); draw("#k{n}-u-p", {a} + 0.6, 0.4); flash({a}, 0.4);'


SZ, SFX = [], []


def szene(t0, t1, html, js):
    SZ.append((t0, t1, html, js))


# ---------------- Intro ----------------
TISCH = (f'<div id="i-t" style="position:absolute;left:90px;top:520px;width:380px;height:300px;border-radius:30px;background:#14181b;border:5px solid {OR};'
         f'box-shadow:0 0 40px {OR}55;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:3">'
         f'<div style="font-size:130px">🍽️</div><div class="mono" style="font-size:34px;color:#fff">1993</div></div>')
szene(0.0, st("s2"), KIT_CSS + TISCH + hand("i-h", "ein Tisch im Schnellrestaurant", 330, 860, 40, GELB, -3, True) + pfeil("i-p", 480, 670, 600, 670, 0.0, "#fff", 9)
      + logo_karte("i-nv", "nvidia", 610, 600, 400, 130, glow=NV) + stempel("i-s", "WERTVOLLSTE FIRMA DER WELT", 110, 1010, NV, 40, -4),
      lambda a, d: (KIT_JS + f' pop("#i-t", {a}); pop("#i-h", {cap("s1", 1)}); draw("#i-p-p", {cap("s1", 2)}, 0.3); pop("#i-p-k", {cap("s1", 2)} + 0.25);'
                    f' pop("#i-nv", {cap("s1", 2)} + 0.3); stempeln("#i-s", {cap("s1", 3)});'))
SFX += [(0.0, "nv-boom-tief"), (cap("s1", 2), "whoosh-schnell"), (cap("s1", 3), "stempel")]

szene(st("s2"), st("s3"), person("j-p", "Jensen Huang", "Chef seit 1993", 330, 450, 420, NV, **foto("jensen-huang")) + stempel("j-s", "RAUS!", 380, 980, ROT, 120, -8),
      lambda a, d: f'pop("#j-p", {a}); stempeln("#j-s", {cap("s2", 1)}); flash({cap("s2", 1)}, 0.5);')
SFX += [(st("s2"), "whoosh-weich"), (cap("s2", 1), "nv-film-horn")]

AG = [("① Der Rücktritt", "s3", 1, OR), ("② Wer übernimmt?", "s3", 2, "#4d8ff0"), ("③ Trump + Tim Cook", "s3", 3, ROT), ("④ Dein ETF", "s3", 5, GRUEN)]
szene(st("s3"), st("s4"), karte("ag-k", 90, 440, 900, 740, "Heute im Video", "6 Teile · ca. 3 Minuten")
      + "".join(kasten(f"ag-{i}", txt, 150, 580 + i * 145, 780, 120, f, 46) for i, (txt, _, _, f) in enumerate(AG)),
      lambda a, d: f'pop("#ag-k", {a});' + "".join(f' pop("#ag-{i}", {cap(s, c)});' for i, (_, s, c, _) in enumerate(AG)))
SFX += [(st("s3"), "whoosh-weich")] + [(cap(s, c), "klick") for _, s, c, _ in AG]

szene(st("s4"), st("s5"), zettel("hw", "Keine Anlage&shy;beratung –<br/>nur Nachrichten erklärt", 200, 560, 680, 74, GELB, -3),
      lambda a, d: f'tl.fromTo("#hw", {{ y: -400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {a});')
SFX += [(st("s4"), "swipe")]

# ---------------- Teil 1: der Rücktritt ----------------
szene(st("s5"), st("s6"), kapitel(1, "Der Rücktritt"), kj(1))
SFX += [(st("s5"), "nv-dun-dun-dun")]

ZL = f'<div id="zl" style="position:absolute;left:230px;top:760px;width:620px;height:12px;border-radius:6px;background:linear-gradient(90deg,{NV},{ROT});transform-origin:0 50%;z-index:2"></div>'
szene(st("s6"), st("s7"), kalender("zl-a", "GRÜNDUNG", "1993", 80, 600, 260, NV) + ZL + kalender("zl-b", "ENDE", "2026", 740, 600, 260, ROT)
      + tz("zl-z", "33 Jahre", 840, 130, "glow-o") + hand("zl-h", "ein Chef – eine Ära", 540, 1020, 60, GELB, -3, True),
      lambda a, d: (f'pop("#zl-a", {a}); tl.fromTo("#zl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2 }}, {a} + 0.3); pop("#zl-b", {cap("s6", 1)});'
                    f' slam("#zl-z", {cap("s6", 0)} + 0.5); pop("#zl-h", {cap("s6", 2)});'))
SFX += [(st("s6"), "uhr-tickt"), (cap("s6", 0) + 0.5, "bass-schlag")]

szene(st("s7"), st("s8"), stempel("af-1", "SPIONAGE-VERDACHT", 130, 560, ROT, 58, -6) + chip("af-c", "laut Berichten", GRAU, 760, 46)
      + stempel("af-2", "+ 2. AFFÄRE", 280, 880, OR, 74, 5),
      lambda a, d: f'stempeln("#af-1", {a}); pop("#af-c", {cap("s7", 1)}); stempeln("#af-2", {cap("s7", 3)});')
SFX += [(st("s7"), "stempel"), (cap("s7", 3), "nv-platte-kratzer")]

MOND = f'<div id="na-m" style="position:absolute;left:120px;top:450px;font-size:150px;z-index:3;filter:drop-shadow(0 0 30px {GELB})">🌙</div>'
szene(st("s8"), st("s9"), MOND + kasten("na-k", "Verwaltungsrat<br/>berät die Nacht durch", 320, 470, 660, 220, "#4d8ff0", 48) + flagge("na-f", "flagge-usa", 120, 760, 220, -4)
      + hand("na-h", "kurz vor Börsenstart …", 640, 800, 52, GELB, -3, True) + stempel("na-s", "RÜCKTRITT – SOFORT", 170, 980, ROT, 62, -5),
      lambda a, d: (f'pop("#na-m", {a}); pop("#na-k", {cap("s8", 1)}); pop("#na-f", {cap("s8", 3)}); pop("#na-h", {cap("s8", 3)} + 0.2);'
                    f' stempeln("#na-s", {cap("s8", 4)}); flash({cap("s8", 4)}, 0.5);'))
SFX += [(st("s8"), "nv-sog"), (cap("s8", 3), "uhr-tickt"), (cap("s8", 4), "nv-gong")]

szene(st("s9"), st("s10"), kasten("of-a", "Offiziell:<br/>freiwillig", 80, 560, 420, 260, GRUEN, 56) + kasten("of-b", "Laut Berichten:<br/>gedrängt", 580, 560, 420, 260, ROT, 56)
      + tz("of-v", "vs.", 640, 70) + hand("of-h", "was stimmt?", 540, 900, 70, GELB, -3, True),
      lambda a, d: f'pop("#of-a", {a}); pop("#of-v", {cap("s9", 1)} - 0.2); slam("#of-b", {cap("s9", 2)}); pop("#of-h", {cap("s9", 2)} + 0.5);')
SFX += [(st("s9"), "swipe"), (cap("s9", 2), "nv-falsch-buzzer")]

# ---------------- Teil 2: Wer übernimmt? ----------------
szene(st("s10"), st("s11"), kapitel(2, "Wer übernimmt?", 90), kj(2))
SFX += [(st("s10"), "nv-boom-kurz")]

szene(st("s11"), st("s12"), person("kr-p", "Colette Kress", "Übergangschefin", 330, 450, 420, "#4d8ff0", **foto("colette-kress"))
      + chip("kr-c", "+ bleibt Finanzchefin", OR, 1060, 52),
      lambda a, d: f'pop("#kr-p", {cap("s11", 1)}); slam("#kr-c", {cap("s11", 4)});')
SFX += [(st("s11"), "whoosh-weich"), (cap("s11", 1), "pop"), (cap("s11", 4), "klick")]

szene(st("s12"), st("s13"), person("hj-p", "Harvey Jones", "Vorsitzender", 90, 470, 380, GELB, **foto("harvey-jones"))
      + wort("hj-s", "SYNOPSYS", 540, 560, 450, 130, "#5a2d82") + hand("hj-h", "früher Chef", 760, 720, 56, GELB, -3, True)
      + stempel("hj-st", "ZUM 1. MAL", 500, 880, OR, 62, 6),
      lambda a, d: f'stempeln("#hj-st", {cap("s12", 1)}); pop("#hj-p", {cap("s12", 4)}); pop("#hj-s", {cap("s12", 6)}); pop("#hj-h", {cap("s12", 6)} + 0.2);')
SFX += [(st("s12"), "swipe"), (cap("s12", 1), "stempel"), (cap("s12", 4), "pop")]

LUPE = (f'<svg id="nf-l" viewBox="0 0 200 200" style="position:absolute;left:390px;top:440px;width:300px;height:300px;z-index:5;filter:drop-shadow(0 0 20px {GELB})">'
        f'<circle cx="80" cy="80" r="56" fill="#ffffff10" stroke="{GELB}" stroke-width="14"/><path d="M122 122 L180 180" stroke="{GELB}" stroke-width="20" stroke-linecap="round"/></svg>')
szene(st("s13"), st("s14"), LUPE + kasten("nf-a", "intern?", 120, 800, 380, 160, OR, 60) + kasten("nf-b", "von außen?", 580, 800, 380, 160, "#4d8ff0", 60)
      + tz("nf-q", "Nachfolger gesucht", 1010, 64, "glow-o"),
      lambda a, d: (f'tl.fromTo("#nf-l", {{ x: -200, rotation: -20, opacity: 0 }}, {{ x: 0, rotation: 0, opacity: 1, duration: 0.5 }}, {a}); pop("#nf-q", {cap("s13", 1)});'
                    f' pop("#nf-a", {cap("s13", 2)}); pop("#nf-b", {cap("s13", 2)} + 0.4);'))
SFX += [(st("s13"), "whoosh-schnell"), (cap("s13", 2), "pop")]

# ---------------- Teil 3: die Aktie ----------------
szene(st("s14"), st("s15"), kapitel(3, "Die Aktie"), kj(3))
SFX += [(st("s14"), "nv-boom-kurz")]

szene(st("s15"), st("s16"), logo_karte("dr-nv", "nvidia", 290, 460, 500, 140, glow=NV) + tz("dr-z", "−13 %", 660, 260, "glow-r")
      + hand("dr-h", "vor Börsenstart", 540, 960, 60, GELB, -3, True) + partikel("dr-p", 540, 800, 26, (ROT, "#fff", OR), 520),
      lambda a, d: f'pop("#dr-nv", {a}); slam("#dr-z", {cap("s15", 2)}); burst("#dr-p", {cap("s15", 2)} + 0.2); pop("#dr-h", {cap("s15", 2)} + 0.4); flash({cap("s15", 2)}, 0.4);')
SFX += [(st("s15"), "whoosh-weich"), (cap("s15", 2), "glas-bricht")]

KURS = linie("ku", [0.55, 0.75, 0.97, 0.9, 0.78, 0.7, 0.6, 0.45, 0.28, 0.1], 150, 640, 780, 400, ROT, punkte=[(2, "239 $"), (9, "< 155 $")])
szene(st("s16"), st("s18"), karte("ku-k", 70, 440, 940, 740, "Nvidia-Aktie", "Rekord Okt. → heute") + KURS + kreis("ku-kr", 880, 1000, 120, 80, GELB, 6)
      + tz("ku-a", "über 1/3 weniger", 1080, 54, "glow-r").replace("top:1080px", "top:1075px") + stempel("ku-s", "≈ −2 BILLIONEN $", 180, 540, ROT, 50, -4),
      lambda a, d: (f'pop("#ku-k", {a}); draw("#ku-p", {cap("s16", 0)}, 1.6); pop("#ku-w0", {cap("s16", 1)}); pop("#ku-w1", {cap("s16", 2)}); tl.fromTo("#ku-f", {{ opacity: 0 }}, {{ opacity: 0.14, duration: 0.5 }}, {cap("s16", 2)});'
                    f' draw("#ku-kr-p", {cap("s17", 0)}, 0.5); pop("#ku-a", {cap("s17", 1)}); stempeln("#ku-s", {cap("s17", 3)});'))
SFX += [(st("s16"), "kurve-runter"), (cap("s17", 3), "stempel")]

BASIS = 1120
KZ = (f'<div id="kz-a" style="position:absolute;left:220px;top:{BASIS - 520}px;width:240px;height:520px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{NV},{NV}88);box-shadow:0 0 40px {NV}77;transform-origin:50% 100%;z-index:3"></div>'
      f'<div id="kz-b" style="position:absolute;left:620px;top:{BASIS - 260}px;width:240px;height:260px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{ROT},{ROT}88);box-shadow:0 0 40px {ROT}77;transform-origin:50% 100%;z-index:3"></div>'
      f'<div class="mono" style="position:absolute;left:140px;width:400px;top:{BASIS - 590}px;text-align:center;font-size:56px;color:{NV};z-index:5">400 $</div>'
      f'<div class="mono" style="position:absolute;left:540px;width:400px;top:{BASIS - 330}px;text-align:center;font-size:56px;color:{ROT};z-index:5">200 $</div>')
szene(st("s18"), st("s19"), wort("kz-bn", "BERNSTEIN", 330, 440, 420, 110, "#003a70") + KZ + stempel("kz-s", "HALBIERT", 560, 600, ROT, 60, 8),
      lambda a, d: (f'pop("#kz-bn", {a}); tl.fromTo("#kz-a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s18", 1)}); tl.fromTo("#kz-b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {cap("s18", 2)});'
                    f' stempeln("#kz-s", {cap("s18", 2)} + 0.5);'))
SFX += [(st("s18"), "swipe"), (cap("s18", 2), "kurve-runter"), (cap("s18", 2) + 0.5, "stempel")]

szene(st("s19"), st("s20"), tz("gw-t", "Die Gewinner", 450, 80, "glow-g") + logo_karte("gw-a", "amd", 90, 600, 420, 140) + logo_karte("gw-b", "broadcom", 570, 600, 420, 140)
      + tz("gw-pa", "▲", 760, 140, "glow-g").replace('style="z-index:5;top:760px', 'style="z-index:5;left:-240px;top:760px')
      + tz("gw-pb", "▲", 760, 140, "glow-g").replace('style="z-index:5;top:760px', 'style="z-index:5;left:240px;top:760px'),
      lambda a, d: f'pop("#gw-t", {a}); pop("#gw-a", {cap("s19", 1)}); pop("#gw-b", {cap("s19", 1)} + 0.3); slam("#gw-pa", {cap("s19", 1)} + 0.5); slam("#gw-pb", {cap("s19", 1)} + 0.7);')
SFX += [(st("s19"), "whoosh-weich"), (cap("s19", 1) + 0.5, "kurve-hoch")]

fr_html, fr_js = cta_szene("fr", BLASE_SVG, "Jetzt günstig kaufen –<br/>oder wegbleiben?")
szene(st("s20"), st("s21"), fr_html + chip("fr-a", "🛒 kaufen", GRUEN, 1060, 50, 200) + chip("fr-b", "🙅 weg", ROT, 1060, 50, 640),
      lambda a, d: fr_js(a, d) + f' pop("#fr-a", {cap("s20", 2)}); pop("#fr-b", {cap("s20", 3)});')
SFX += [(st("s20"), "handy-benachrichtigung"), (cap("s20", 2), "pop"), (cap("s20", 3), "pop")]

# ---------------- Teil 4: Donald Trump ----------------
szene(st("s21"), st("s22"), kapitel(4, "Donald Trump"), kj(4))
SFX += [(st("s21"), "nv-boom-kurz")]

BL = (f'<div id="tr-b" style="position:absolute;left:470px;top:500px;width:540px;padding:34px 36px;border-radius:30px 30px 30px 6px;background:#fff;color:#111;'
      f'font-weight:900;font-size:50px;line-height:1.1;box-shadow:0 20px 50px #000;z-index:4">„Nur ein Mann kann ihn ersetzen …“'
      f'<div class="mono" style="font-size:26px;color:#666;margin-top:12px">Truth Social</div></div>')
szene(st("s22"), st("s24"), person("tr-p", "Donald Trump", "Präsident", 90, 470, 340, ROT, **foto("donald-trump")) + BL
      + tz("tr-c", "TIM COOK?!", 880, 120, "glow-o") + zettel("tr-z", "„Eine Legende ersetzt eine Legende!“", 200, 1010, 680, 46, GELB, -2),
      lambda a, d: (f'pop("#tr-p", {cap("s22", 2)}); pop("#tr-b", {cap("s22", 3)}); slam("#tr-c", {cap("s22", 4)} + 0.5); flash({cap("s22", 4)} + 0.5, 0.4);'
                    f' tl.fromTo("#tr-z", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }}, {st("s23")});'))
SFX += [(st("s22"), "whoosh-weich"), (cap("s22", 3), "handy-benachrichtigung"), (cap("s22", 4) + 0.5, "nv-tusch"), (st("s23"), "nv-staunen-wow")]

szene(st("s24"), st("s25"), person("tc-p", "Tim Cook", "Apple", 90, 470, 380, "#aaa", **foto("tim-cook")) + logo_karte("tc-a", "apple", 610, 500, 300, 200)
      + kalender("tc-k", "CHEF", "15 J.", 620, 760, 280, "#555") + hand("tc-h", "heute Verwaltungsrats-Chef", 540, 1100, 50, GELB, -3, True),
      lambda a, d: f'pop("#tc-p", {a}); pop("#tc-a", {a} + 0.2); pop("#tc-k", {cap("s24", 0)} + 0.5); pop("#tc-h", {cap("s24", 2)});')
SFX += [(st("s24"), "swipe"), (cap("s24", 0) + 0.5, "pop")]

KX = ('<svg id="vr-x" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:5">'
      f'<path id="vr-x1" d="M600 520 L980 760" stroke="{ROT}" stroke-width="14" stroke-linecap="round"/><path id="vr-x2" d="M980 520 L600 760" stroke="{ROT}" stroke-width="14" stroke-linecap="round"/></svg>')
szene(st("s25"), st("s26"), kasten("vr-a", "Verwaltungsrat<br/>entscheidet", 80, 520, 460, 240, GRUEN, 52) + kasten("vr-b", "Präsident", 600, 520, 380, 240, GRAU, 56) + KX
      + stempel("vr-s", "SEHR UNWAHRSCHEINLICH", 130, 900, OR, 46, -5),
      lambda a, d: (f'pop("#vr-a", {cap("s25", 2)}); pop("#vr-b", {cap("s25", 3)}); draw("#vr-x1", {cap("s25", 3)} + 0.3, 0.2); draw("#vr-x2", {cap("s25", 3)} + 0.5, 0.2);'
                    f' stempeln("#vr-s", {cap("s25", 5)});'))
SFX += [(st("s25"), "whoosh-weich"), (cap("s25", 3) + 0.3, "falsch"), (cap("s25", 5), "stempel")]

# ---------------- Teil 5: dein Geld ----------------
szene(st("s26"), st("s27"), kapitel(5, "Dein Geld"), kj(5))
SFX += [(st("s26"), "nv-boom-kurz")]

szene(st("s27"), st("s28"), wort("ms", "MSCI", 360, 440, 360, 110, "#002f6c") + raster("ms-r", 270, 590, 10, 10, 46, 8, "#3a4248") + hand("ms-h", "≈ 6 € von 100 €", 800, 560, 54, NV, -6, True),
      lambda a, d: (f'pop("#ms", {cap("s27", 1)}); tl.fromTo("#ms-r .q", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.005 }}, {a});'
                    f' tl.to("#ms-r .q:nth-child(-n+6)", {{ background: "{NV}", boxShadow: "0 0 20px {NV}", duration: 0.2, stagger: 0.1 }}, {cap("s27", 2)}); pop("#ms-h", {cap("s27", 2)} + 0.6);'))
SFX += [(st("s27"), "zaehler"), (cap("s27", 2), "muenzen-klimpern")]

ZEILE = 'style="display:flex;justify-content:space-between;font-size:58px;margin:18px 0"'
szene(st("s28"), st("s29"), f'<div id="rc" class="mono" style="position:absolute;left:120px;top:470px;width:840px;padding:50px 56px;border-radius:30px;background:#14181bee;border:3px solid #ffffff22;box-shadow:0 30px 60px #000;z-index:2;color:#fff">'
      f'<div style="font-family:Montserrat;font-weight:900;font-size:44px;color:{GRAU};margin-bottom:16px">Rechnung</div>'
      f'<div id="rc-1" {ZEILE}><span>Nvidia</span><span style="color:{ROT}">− 13 %</span></div>'
      f'<div id="rc-2" {ZEILE}><span>Anteil</span><span>× 6 %</span></div>'
      f'<div id="rc-l" style="height:6px;background:#fff;margin:24px 0;transform-origin:0 50%"></div>'
      f'<div id="rc-3" {ZEILE}><span>dein ETF</span><span style="color:{ROT};text-shadow:0 0 30px {ROT}">≈ − 0,8 %</span></div></div>',
      lambda a, d: (f'pop("#rc", {a}); pop("#rc-1", {a} + 0.2); pop("#rc-2", {cap("s28", 1)}); tl.fromTo("#rc-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4 }}, {cap("s28", 2)});'
                    f' slam("#rc-3", {cap("s28", 2)} + 0.3);'))
SFX += [(st("s28"), "taschenrechner"), (cap("s28", 2) + 0.3, "klick")]

WIP = (f'<div id="wp" style="position:absolute;left:140px;top:860px;width:800px;height:16px;border-radius:8px;background:#fff;box-shadow:0 0 30px #fff8;transform-origin:50% 50%;z-index:3"></div>'
       f'<div style="position:absolute;left:500px;top:876px;width:0;height:0;border-left:40px solid transparent;border-right:40px solid transparent;border-bottom:80px solid {GRAU};z-index:2"></div>')
szene(st("s29"), st("s30"), WIP + logo_karte("wp-n", "nvidia", 150, 700, 300, 100, glow=ROT) + logo_karte("wp-a", "amd", 630, 700, 300, 100, glow=GRUEN)
      + hand("wp-h", "gleicht einen Teil aus", 540, 1010, 60, GELB, -3, True),
      lambda a, d: (f'pop("#wp-n", {a}); pop("#wp-a", {cap("s29", 1)}); tl.fromTo("#wp", {{ rotation: 8 }}, {{ rotation: 2, duration: 0.8, ease: "back.out(2)" }}, {cap("s29", 2)});'
                    f' tl.fromTo("#wp-n", {{ y: 40 }}, {{ y: 10, duration: 0.8 }}, {cap("s29", 2)}); tl.fromTo("#wp-a", {{ y: -40 }}, {{ y: -10, duration: 0.8 }}, {cap("s29", 2)}); pop("#wp-h", {cap("s29", 3)});'))
SFX += [(st("s29"), "swipe"), (cap("s29", 2), "richtig")]

# ---------------- Teil 6: Wie geht es weiter? ----------------
szene(st("s30"), st("s31"), kapitel(6, "Wie geht es weiter?", 80), kj(6))
SFX += [(st("s30"), "nv-boom-kurz")]

szene(st("s31"), st("s32"), kalender("qz-k", "NOV", "17", 110, 470, 320, ROT) + person("qz-p", "Colette Kress", "1. großer Auftritt", 600, 470, 360, "#4d8ff0", **foto("colette-kress"))
      + kasten("qz-q", "Quartals&shy;zahlen", 200, 940, 680, 170, OR, 64),
      lambda a, d: f'pop("#qz-k", {a}); pop("#qz-q", {cap("s31", 2)}); pop("#qz-p", {cap("s31", 4)});')
SFX += [(st("s31"), "whoosh-weich"), (cap("s31", 2), "spannung")]

ZL2 = f'<div id="jb-l" style="position:absolute;left:250px;top:930px;width:580px;height:10px;border-radius:5px;background:linear-gradient(90deg,{OR},{ROT});transform-origin:0 50%;z-index:2"></div>'
szene(st("s32"), st("s33"), person("jb-p", "Steve Jobs", "Apple-Gründer", 90, 450, 320, "#aaa", **foto("steve-jobs")) + logo_karte("jb-a", "apple", 650, 470, 260, 180)
      + kalender("jb-1", "JOBS GEHT", "1985", 90, 830, 230, OR) + ZL2 + kalender("jb-2", "FAST PLEITE", "1997", 760, 830, 230, ROT),
      lambda a, d: (f'pop("#jb-p", {cap("s32", 1)}); pop("#jb-a", {cap("s32", 1)} + 0.2); pop("#jb-1", {cap("s32", 2)}); tl.fromTo("#jb-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8 }}, {cap("s32", 3)});'
                    f' pop("#jb-2", {cap("s32", 4)});'))
SFX += [(st("s32"), "nv-sog"), (cap("s32", 4), "kurve-runter")]

CHIP = (f'<svg id="ch" viewBox="0 0 200 200" style="position:absolute;left:390px;top:450px;width:300px;height:300px;z-index:4;filter:drop-shadow(0 0 30px {NV})">'
        f'<rect x="45" y="45" width="110" height="110" rx="14" fill="#1b1f22" stroke="{NV}" stroke-width="8"/><rect x="75" y="75" width="50" height="50" rx="6" fill="{NV}"/>'
        + "".join(f'<rect x="{60 + k * 30}" y="15" width="10" height="28" rx="4" fill="{NV}"/><rect x="{60 + k * 30}" y="157" width="10" height="28" rx="4" fill="{NV}"/>'
                  f'<rect x="15" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{NV}"/><rect x="157" y="{60 + k * 30}" width="28" height="10" rx="4" fill="{NV}"/>' for k in range(3)) + '</svg>')
szene(st("s33"), st("s34"), CHIP + tz("gk-t", "wichtigste KI-Chips der Welt", 800, 60) + stempel("gk-s", "GESCHÄFT LÄUFT WEITER", 160, 940, GRUEN, 54, -4),
      lambda a, d: f'tl.fromTo("#ch", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.8)" }}, {a}); pop("#gk-t", {cap("s33", 2)}); stempeln("#gk-s", {cap("s33", 3)});')
SFX += [(st("s33"), "whoosh-weich"), (cap("s33", 3), "stempel")]

szene(st("s34"), DAUER, logo_karte("en-nv", "nvidia", 290, 480, 500, 140, glow=NV) + hand("en-h", "ohne Jensen?", 540, 680, 90, GELB, -4, True)
      + stempel("en-s", "VOR 1 WOCHE UNDENKBAR", 140, 900, OR, 44, -5),
      lambda a, d: f'pop("#en-nv", {a}); pop("#en-h", {cap("s34", 0)} + 0.5); stempeln("#en-s", {cap("s34", 1)});')
SFX += [(st("s34"), "whoosh-weich"), (cap("s34", 1), "nv-tusch")]

SZ.append(laufband_szene([("NVIDIA ▼ −13 %", ROT), ("HUANG TRITT ZURÜCK", None), ("AMD ▲", GRUEN), ("BROADCOM ▲", GRUEN), ("KURSZIEL 400 → 200 $", ROT),
                          ("DAX ▲ 27.000", GRUEN), ("ZAHLEN 17.11.", GELB)], DAUER))

if __name__ == "__main__":
    build(HERE, SZ, SFX)
