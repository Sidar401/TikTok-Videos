#!/usr/bin/env python3
"""HundeFinanzTv Longform 16:9 (Dark Glow): Das ändert sich 2027 für dein Geld – 7 Änderungen, Gewinner oder Verlierer (Kommentar-CTA Mitte).
Leitbild: Kalenderblatt 2027 mit Nummer je Änderung + Stempel GEWINNER/VERLIERER, am Ende Punktetafel."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import glow_short as g  # noqa: E402

g.querformat()
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, cta_szene, partikel, ring, t, zeiten  # noqa: E402
from glow_teile import BLAU, GL, beagle_ring, karte, svg  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
S = []


def sz(a, b, html, js):
    S.append((a, b, html, js))


def blatt(id_, nr, titel, monat="2027"):
    return (f'<div id="{id_}" style="position:absolute;left:760px;top:170px;width:400px;height:460px;border-radius:34px;background:#f4f1ea;overflow:hidden;z-index:2;'
            f'box-shadow:0 0 80px {OR}66;transform-origin:50% 0%">'
            f'<div style="height:110px;background:{OR};color:#111;font-weight:900;font-size:64px;text-align:center;line-height:110px">{monat}</div>'
            f'<div style="text-align:center;font-weight:900;font-size:260px;color:#111;line-height:340px">{nr}</div></div>'
            + t(f"{id_}-t", titel, 680, 96, "glow-o"))


def blatt_js(id_):
    return lambda a, d: (f'tl.fromTo("#{id_}", {{ rotationX: -100, transformPerspective: 1200 }}, {{ rotationX: 0, duration: 0.5, ease: "back.out(1.4)" }}, {a});'
                         f' pop("#{id_}-t", {a} + 0.35);')


def stempel(id_, txt, farbe, top=520, gr=150):
    return (f'<div id="{id_}" style="position:absolute;left:0;top:{top}px;width:1920px;display:flex;justify-content:center;z-index:5">'
            f'<span style="padding:10px 60px;border:14px solid {farbe};border-radius:28px;color:{farbe};font-weight:900;font-size:{gr}px;transform:rotate(-6deg);'
            f'box-shadow:0 0 70px {farbe}88;background:#0e1012dd">{txt}</span></div>')


def gw(id_, wer, gewinner=True):
    f = GRUEN if gewinner else ROT
    return stempel(id_, "GEWINNER" if gewinner else "VERLIERER", f, 300) + t(f"{id_}-w", wer, 620, 80)


def gw_js(id_, extra=0.0):
    return lambda a, d: f'slam("#{id_}", {a} + {extra}); shake("#{id_}", {a} + {extra} + 0.3); pop("#{id_}-w", {a} + {extra} + 0.5);'


def von_bis(id_, alt, neu, farbe=GRUEN, top=330):
    return (t(f"{id_}-a", alt, top, 140).replace('class="t "', 'class="t "') + svg(f"{id_}-p", f'<path d="M0 40 H220 M180 0 L230 40 L180 80" fill="none" stroke="{OR}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>', 845, top + 210, 240, 80, "0 0 240 80")
            + t(f"{id_}-n", neu, top + 320, 180, "glow-g" if farbe == GRUEN else "glow-r"))


def von_bis_js(id_, t1, t2):
    return f'pop("#{id_}-a", {t1}); pop("#{id_}-p", {t1} + 0.3); slam("#{id_}-n", {t2});'


# ---------- Szenen ----------
sz(0.0, st("s2"), blatt("k0", "1", "Neu ab Januar", "JAN 2027"),
   lambda a, d: f'tl.fromTo("#k0", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.4 }}, {a}); pop("#k0-t", {cap("s1", 1)});')
sz(st("s2"), st("s3"), stempel("w0", "GEWINNER", GRUEN, 240, 130) + stempel("v0", "VERLIERER", ROT, 560, 130),
   lambda a, d: f'slam("#w0", {a}); slam("#v0", {cap("s2", 1)}); shake("#v0", {cap("s2", 1)} + 0.3);')
BLAETTER = "".join(f'<div class="bl" style="position:absolute;left:{360 + i * 170}px;top:{300 + (i % 2) * 30}px;width:150px;height:180px;border-radius:18px;background:#f4f1ea;'
                   f'z-index:2;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:110px;color:#111;box-shadow:0 0 30px {OR}55;'
                   f'border-top:34px solid {OR}">{i + 1}</div>' for i in range(7))
sz(st("s3"), st("s4"), BLAETTER + t("sv-t", "7 Änderungen", 120, 100, "glow-o") + t("sv-u", "Gewinner oder Verlierer?", 620, 90),
   lambda a, d: f'pop("#sv-t", {a}); tl.fromTo(".bl", {{ y: 400, rotation: -20, opacity: 0 }}, {{ y: 0, rotation: 0, opacity: 1, duration: 0.35, stagger: 0.12, ease: "back.out(1.6)" }}, {a} + 0.3); pop("#sv-u", {cap("s3", 3)});')
sz(st("s4"), st("s5"), beagle_ring("fo-r", 790, 110, 340) + t("fo-t", "Folge HundeFinanzTv", 480, 96) + chip("fo-f", "+ Folgen", OR, 640, 70),
   lambda a, d: f'pop("#fo-r", {a}); pop("#fo-t", {a} + 0.3); slam("#fo-f", {a} + 0.6); tl.fromTo("#fo-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {a} + 1.0);')
sz(st("s5"), st("s6"), karte("hw", "Keine Anlage- oder Steuerberatung", ROT, 330, 90, 1500), lambda a, d: f'pop("#hw", {a} + 0.1);')
# 1 Mindestlohn
sz(st("s6"), st("s7"), blatt("k1", "1", "Mindestlohn"), blatt_js("k1"))
sz(st("s7"), st("s8"), von_bis("ml", "13,90 €", "14,60 €"),
   lambda a, d: von_bis_js("ml", a, cap("s7", 1)))
sz(st("s8"), st("s9"), chip("vz-c", "Vollzeit", OR, 240, 80) + t("vz-z", "+120 €", 400, 220, "glow-g") + t("vz-u", "pro Monat (brutto)", 680, 80),
   lambda a, d: f'pop("#vz-c", {a}); slam("#vz-z", {cap("s8", 1)}); pop("#vz-u", {cap("s8", 2)} + 0.4);')
sz(st("s9"), st("s10"), gw("g1", "alle mit Mindestlohn"), gw_js("g1"))
# 2 Minijob
sz(st("s10"), st("s11"), blatt("k2", "2", "Minijob"), blatt_js("k2"))
sz(st("s11"), st("s12"), von_bis("mj", "603 €", "633 €"), lambda a, d: von_bis_js("mj", a + 0.2, cap("s11", 3)))
sz(st("s12"), st("s13"), t("mj2-z", "+30 €", 300, 240, "glow-g") + t("mj2-u", "mehr dazuverdienen", 600, 90),
   lambda a, d: f'slam("#mj2-z", {a} + 0.2); pop("#mj2-u", {cap("s12", 1)});')
# 3 Deutschlandticket
sz(st("s13"), st("s14"), blatt("k3", "3", "Deutschlandticket"), blatt_js("k3"))
sz(st("s14"), st("s15"), von_bis("dt", "63 €", "66,80 €", ROT), lambda a, d: von_bis_js("dt", a + 0.2, cap("s14", 1)))
sz(st("s15"), st("s16"), t("dt2-z", "+45 €", 300, 240, "glow-r") + t("dt2-u", "pro Jahr", 600, 90),
   lambda a, d: f'slam("#dt2-z", {cap("s15", 1)}); pop("#dt2-u", {cap("s15", 1)} + 0.4);')
sz(st("s16"), st("s17"), gw("g3", "Pendler ohne Jobticket", False), gw_js("g3"))
# 4 Frühstart-Rente
sz(st("s17"), st("s18"), blatt("k4", "4", "Frühstart-Rente"), blatt_js("k4"))
KIND = svg("ki", f'<g {GL(GRUEN)} fill="{GRUEN}"><circle cx="100" cy="60" r="44"/><path d="M40 230 C40 140 160 140 160 230 Z"/></g>', 400, 300, 200, 240, "0 0 200 240")
sz(st("s18"), st("s19"), KIND + f'<div id="fs-z" class="t glow-g" style="left:700px;width:1000px;top:280px;font-size:170px;text-align:left">10 €</div>'
   + f'<div id="fs-u" class="t" style="left:700px;width:1000px;top:480px;font-size:70px;text-align:left">pro Monat · 6–18 Jahre</div>',
   lambda a, d: f'pop("#ki", {a}); slam("#fs-z", {a} + 0.6); pop("#fs-u", {cap("s18", 1)});')
sz(st("s19"), st("s20"), chip("jg-c", "Start: Jahrgang", OR, 260, 80) + t("jg-z", "2020", 420, 220, "glow-o"),
   lambda a, d: f'pop("#jg-c", {a}); slam("#jg-z", {a} + 0.8);')
sz(st("s20"), st("s21"), chip("fz-c", "12 Jahre × 120 €", OR, 230, 70) + t("fz-z", "0 €", 380, 220, "glow-g") + t("fz-u", "+ Rendite", 660, 90, "glow-o"),
   lambda a, d: f'pop("#fz-c", {a}); pop("#fz-z", {a} + 0.3); zaehl("#fz-z", 0, 1440, {cap("s20", 2)}, 1.0, " €"); pop("#fz-u", {cap("s20", 3)});')
sz(st("s21"), st("s22"), gw("g4", "Familien mit Kindern"), gw_js("g4"))
frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Welche Änderung trifft dich am meisten?")
frage_html = frage_html.replace("left:340px;top:380px;width:400px", "left:760px;top:130px;width:400px").replace('style="top:900px;font-size:66px"', 'style="top:600px;font-size:72px"')
sz(st("s22"), st("s23"), frage_html, frage_js)
# 5 Mütterrente
sz(st("s23"), st("s24"), blatt("k5", "5", "Mütterrente"), blatt_js("k5"))
sz(st("s24"), st("s25"), t("mr-a", "Alle Kinder zählen", 280, 120) + t("mr-b", '<span class="box">GLEICH</span>', 460, 160) + chip("mr-c", "auch vor 1992 geboren", BLAU, 700, 64),
   lambda a, d: f'pop("#mr-a", {cap("s24", 1)}); slam("#mr-b", {cap("s24", 2)}); pop("#mr-c", {cap("s24", 4)});')
sz(st("s25"), st("s26"), gw("g5", "viele Eltern in Rente"), gw_js("g5"))
# 6 Krankenkasse
sz(st("s26"), st("s27"), blatt("k6", "6", "Krankenkasse"), blatt_js("k6"))
sz(st("s27"), st("s28"), t("kk-k", "Ø Zusatzbeitrag", 280, 100, "glow-o") + t("kk-z", "2,9 %", 420, 240),
   lambda a, d: f'pop("#kk-k", {a}); slam("#kk-z", {cap("s27", 2)});')
KASSEN = "".join(f'<div id="kb{i}" style="position:absolute;left:{560 + i * 300}px;top:{760 - h}px;width:200px;height:{h}px;border-radius:18px 18px 0 0;background:{f};'
                 f'box-shadow:0 0 40px {f}77;transform-origin:50% 100%;z-index:2"></div><div class="t" style="left:{560 + i * 300 - 860}px;top:{700 - h}px;font-size:54px;color:{f}">{p}</div>'
                 f'<div class="t" style="left:{560 + i * 300 - 860}px;top:780px;font-size:40px">Kasse {chr(65 + i)}</div>'
                 for i, (h, p, f) in enumerate([(200, "niedrig", GRUEN), (290, "mittel", OR), (380, "hoch", ROT)]))
sz(st("s28"), st("s29"), KASSEN + t("kb-t", "Jede Kasse legt selbst fest", 170, 64, "glow-o"),
   lambda a, d: f'pop("#kb-t", {a});' + " ".join(f' tl.fromTo("#kb{i}", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "back.out(1.4)" }}, {a} + {0.3 + i * 0.3:.1f});' for i in range(3)))
sz(st("s29"), st("s30"), t("kw-t", "Wechsel", 280, 170, "glow-g") + chip("kw-c", "oft einfach online", GRUEN, 560, 80),
   lambda a, d: f'slam("#kw-t", {a}); pop("#kw-c", {cap("s29", 2)});')
# 7 Beitragsbemessungsgrenze
sz(st("s30"), st("s31"), blatt("k7", "7", "Gutverdiener zahlen mehr"), blatt_js("k7"))
sz(st("s31"), st("s32"), t("bb-k", "Beitragsbemessungsgrenze Rente", 280, 70, "glow-o") + t("bb-z", "≈ 8.850 €", 420, 220) + t("bb-u", "pro Monat", 680, 80),
   lambda a, d: f'pop("#bb-k", {a}); slam("#bb-z", {a} + 1.0); pop("#bb-u", {cap("s31", 3)} + 0.4);')
sz(st("s32"), st("s33"), f'<div id="gb" style="position:absolute;left:360px;top:400px;width:1200px;height:140px;border-radius:24px;background:#2a3036;z-index:1"></div>'
   + f'<div id="gb-a" style="position:absolute;left:360px;top:400px;width:1000px;height:140px;border-radius:24px;background:{OR};box-shadow:0 0 40px {OR}77;transform-origin:0 50%;z-index:2"></div>'
   + t("gb-t", "beitragspflichtiger Teil wird größer", 240, 70) + t("gb-u", "Gehalt", 580, 60),
   lambda a, d: f'pop("#gb-t", {a}); tl.fromTo("#gb-a", {{ scaleX: 0.7 }}, {{ scaleX: 1, duration: 1.2, ease: "power2.out" }}, {cap("s32", 2)}); pop("#gb-u", {a} + 0.2);')
sz(st("s33"), st("s34"), gw("g7", "Gutverdiener", False), gw_js("g7"))
sz(st("s34"), st("s35"), chip("ar-c", "BONUS: Aktivrente", GOLD, 220, 80) + t("ar-z", "2.000 €", 400, 220, "glow-g") + t("ar-u", "im Monat steuerfrei", 660, 80),
   lambda a, d: f'pop("#ar-c", {a}); slam("#ar-z", {cap("s34", 3)}); pop("#ar-u", {cap("s34", 4)} + 0.4);')


def spalte(id_, titel, items, x, f):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:200px;width:700px;border-radius:30px;background:#16191b;border:6px solid {f};box-shadow:0 0 60px {f}55;padding:30px 40px;z-index:2">'
            f'<div style="font-weight:900;font-size:70px;color:{f};margin-bottom:20px">{titel}</div>'
            + "".join(f'<div class="{id_}-i" style="font-weight:800;font-size:52px;color:#fff;margin:12px 0">✓ {i}</div>' for i in items) + '</div>')


TAFEL = (spalte("gs", "GEWINNER", ["Mindestlohn", "Minijob", "Familien", "Rentner"], 220, GRUEN)
         + spalte("vs", "VERLIERER", ["Pendler", "Gutverdiener"], 1000, ROT))
sz(st("s35"), st("s37"), TAFEL,
   lambda a, d: (f'pop("#gs", {a}); tl.fromTo(".gs-i", {{ x: -60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, stagger: 0.2 }}, {cap("s35", 2)});'
                 f' pop("#vs", {st("s36")}); tl.fromTo(".vs-i", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, stagger: 0.25 }}, {st("s36")} + 0.3);'))
sz(st("s37"), DAUER, t("fr-t", "Früh reagieren!", 220, 130, "glow-o") + chip("fr-1", "Kassenwechsel", GRUEN, 480, 90, 440) + chip("fr-2", "Jobticket", BLAU, 480, 90, 1080),
   lambda a, d: f'pop("#fr-t", {a} + 0.2); slam("#fr-1", {cap("s37", 5)}); slam("#fr-2", {cap("s37", 6)});')

SZENEN = S
SFX = ([(a, "whoosh") for a, *_ in S[1:]] + [(0.0, "boom"), (st("s2"), "boom"), (cap("s2", 1), "boom")]
       + [(st(f"s{k}") + 0.5, "pop") for k in (6, 10, 13, 17, 23, 26, 30)]
       + [(st(f"s{k}"), "boom") for k in (9, 16, 21, 25, 33)]
       + [(cap("s8", 2), "kasse"), (cap("s20", 2) + 1.0, "ding"), (cap("s34", 4), "kasse"), (cap("s37", 5), "pop"), (cap("s37", 6), "pop")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
