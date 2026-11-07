#!/usr/bin/env python3
"""HundeFinanzTv Longform 16:9 (Dark Glow): Der Domino-Effekt – wie eine Wahl 2,5 Billionen vernichtet hat (Teilen-CTA in der Mitte).
Leitbild: 4 Dominosteine (Wahl → Rechenzentren → Chips → Depot), bei jedem „Dominostein Nummer …“ fällt der nächste."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import glow_short as g  # noqa: E402

g.querformat()
from glow_short import GOLD, GRUEN, OR, ROT, TEILEN_SVG, build, chip, partikel, ring, t, zeiten  # noqa: E402
from glow_teile import BLAU, GL, PFEIL_AB, beagle_ring, karte, plakette, regel, regel_js, svg  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
S = []


def sz(a, b, html, js):
    S.append((a, b, html, js))


# ---------- Leitbild: Dominosteine ----------
STEINE = [("WAHL", "🗳", BLAU), ("RECHEN-<br/>ZENTREN", "▤", OR), ("CHIPS", "▦", GRUEN), ("DEIN<br/>DEPOT", "€", ROT)]
ICON = {0: f'<svg viewBox="0 0 100 100" style="width:110px;height:110px"><rect x="15" y="40" width="70" height="50" rx="8" fill="none" stroke="#fff" stroke-width="8"/><rect x="38" y="10" width="24" height="40" rx="4" fill="#fff"/></svg>',
        1: '<svg viewBox="0 0 100 100" style="width:110px;height:110px">' + "".join(f'<rect x="15" y="{12 + i * 22}" width="70" height="16" rx="4" fill="none" stroke="#fff" stroke-width="6"/>' for i in range(4)) + '</svg>',
        2: '<svg viewBox="0 0 100 100" style="width:110px;height:110px"><rect x="25" y="25" width="50" height="50" rx="6" fill="none" stroke="#fff" stroke-width="8"/>' + "".join(f'<path d="M{30 + i * 14} 25 V10 M{30 + i * 14} 75 V90 M25 {30 + i * 14} H10 M75 {30 + i * 14} H90" stroke="#fff" stroke-width="6"/>' for i in range(4)) + '</svg>',
        3: '<div style="font-weight:900;font-size:110px;color:#fff;line-height:1">€</div>'}
X = [250, 560, 870, 1180]


def domino_html(p, gross=False):
    out = []
    for i, (txt, _, f) in enumerate(STEINE):
        out.append(f'<div id="{p}{i}" style="position:absolute;left:{X[i]}px;top:360px;width:240px;height:440px;border-radius:26px;background:#16191b;border:8px solid {f};'
                   f'box-shadow:0 0 50px {f}66;transform-origin:100% 100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;z-index:{2 + i}">'
                   f'{ICON[i]}<div style="font-weight:900;font-size:40px;line-height:1.05;color:#fff;text-align:center">{txt}</div></div>')
    return "".join(out)


def domino_szene(n, titel):
    """n = Index des Steins, der jetzt fällt (die davor liegen schon)."""
    html = domino_html(f"d{n}-") + t(f"dt{n}", titel, 170, 80, "glow-o")
    def js(a, d):
        x = [f'tl.fromTo("#d{n}-{i}", {{ rotation: 62 }}, {{ rotation: 62, duration: 0.01 }}, {a});' for i in range(n)]
        x.append(f'pop("#dt{n}", {a});')
        x.append(f'tl.fromTo("#d{n}-{n}", {{ rotation: 0 }}, {{ rotation: 62, duration: 0.5, ease: "power2.in" }}, {a} + 0.6);')
        x.append(f'tl.fromTo("#d{n}-{n}", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.2, yoyo: true, repeat: 1 }}, {a});')
        if n < 3:
            x.append(f'tl.fromTo("#d{n}-{n + 1}", {{ rotation: 0 }}, {{ rotation: 8, duration: 0.1, yoyo: true, repeat: 1, immediateRender: false }}, {a} + 1.1);')
        return " ".join(x)
    return html, js


def chart(id_, d, farbe, x=360, y=260, w=1200, h=520):
    return svg(id_, f'<path d="M0 {h - 10} L{w} {h - 10}" stroke="#ffffff33" stroke-width="4"/><path id="{id_}-l" d="{d}" fill="none" stroke="{farbe}" stroke-width="14" '
                    f'stroke-linejoin="round" stroke-linecap="round" {GL(farbe)}/>', x, y, w, h, f"0 0 {w} {h}")


SPACEX_PL = plakette("sx", "SpaceX", 960, 330)

# ---------- Szenen ----------
sz(0.0, st("s2"), t("h-z", "−2,5 Billionen $", 300, 170, "glow-r") + chip("h-c", "durch EINE Wahl", OR, 620, 80),
   lambda a, d: f'tl.fromTo("#h-z", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.4 }}, {a}); shake("#h-z", 0.5); pop("#h-c", {cap("s1", 1)});')
sz(st("s2"), st("s3"), t("t1", 'an <span class="box">EINEM</span> Tag', 380, 170),
   lambda a, d: f'slam("#t1", {a});')
sz(st("s3"), st("s4"), chip("r-1", "Rekordzahlen ▲", GRUEN, 280, 90) + t("r-2", "Aktie ▼", 520, 190, "glow-r"),
   lambda a, d: f'pop("#r-1", {a} + 0.2); slam("#r-2", {cap("s3", 2)}); shake("#r-2", {cap("s3", 2)} + 0.3);')
sz(st("s4"), st("s5"), domino_html("di") + t("di-t", "DER DOMINO-EFFEKT", 150, 110, "glow-o"),
   lambda a, d: (f'pop("#di-t", {a});' + " ".join(f' pop("#di{i}", {a} + {0.3 + i * 0.25:.2f});' for i in range(4))
                 + " ".join(f' tl.fromTo("#di{i}", {{ rotation: 0 }}, {{ rotation: 62, duration: 0.4, ease: "power2.in", immediateRender: false }}, {cap("s4", 3)} + {i * 0.3:.1f});' for i in range(4))))
sz(st("s5"), st("s6"), karte("lv", "Letztes Video: der KI-Geldkreis", BLAU, 220, 70) + t("lv-z", 'Heute: der <span class="box">AUSLÖSER</span>', 520, 120),
   lambda a, d: f'pop("#lv", {a}); slam("#lv-z", {cap("s5", 2)});')
sz(st("s6"), st("s7"), karte("hw", "Keine Anlageberatung", ROT, 330, 110),
   lambda a, d: f'pop("#hw", {a} + 0.2);')
sz(st("s7"), st("s8"), beagle_ring("fo-r", 790, 110, 340) + t("fo-t", "Folge HundeFinanzTv", 480, 96) + chip("fo-f", "+ Folgen", OR, 640, 70),
   lambda a, d: f'pop("#fo-r", {a}); pop("#fo-t", {cap("s7", 2)}); slam("#fo-f", {cap("s7", 2)} + 0.4); tl.fromTo("#fo-f", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 5 }}, {cap("s7", 3)});')
h, j = domino_szene(0, "Dominostein 1: die Wahl")
sz(st("s8"), st("s9"), h, j)
KAPITOL = svg("kp", f'<g {GL(BLAU)} fill="none" stroke="{BLAU}" stroke-width="10"><path d="M100 330 H500 M130 330 V230 M190 330 V230 M250 330 V230 M350 330 V230 M410 330 V230 M470 330 V230 M110 230 H490"/>'
                    f'<path d="M180 230 C180 120 420 120 420 230"/><path d="M300 125 V70 M285 70 H315"/></g>', 660, 230, 600, 360, "0 0 600 360")
sz(st("s9"), st("s10"), KAPITOL + t("ko-t", "US-Kongress", 600, 90) + chip("ko-c", "Demokraten: Mehrheit", BLAU, 740, 64),
   lambda a, d: f'pop("#kp", {a}); pop("#ko-t", {cap("s9", 1)}); slam("#ko-c", {cap("s9", 2)});')
RACK = svg("rk", f'<g {GL(OR)}>' + "".join(f'<rect x="0" y="{i * 60}" width="300" height="46" rx="10" fill="#23282c" stroke="{OR}" stroke-width="5"/><circle cx="30" cy="{i * 60 + 23}" r="9" fill="{GRUEN}"/>'
                                          f'<rect x="60" y="{i * 60 + 18}" width="190" height="10" rx="5" fill="#ffffff44"/>' for i in range(5)) + '</g>', 340, 260, 300, 290, "0 0 300 290")
sz(st("s10"), st("s11"), RACK + f'<div id="rz-t" class="t" style="left:700px;width:1000px;top:270px;font-size:84px;text-align:left">KI-Rechenzentren<br/><span class="box">bremsen?</span></div>'
   + f'<div id="rz-s" style="position:absolute;left:760px;top:560px;padding:12px 40px;border:10px solid {ROT};border-radius:20px;color:{ROT};font-weight:900;font-size:72px;transform:rotate(-6deg);z-index:4">Texas: BAUSTOPP?</div>',
   lambda a, d: f'pop("#rk", {a}); pop("#rz-t", {cap("s10", 2)}); slam("#rz-s", {cap("s10", 3)}); shake("#rz-s", {cap("s10", 4)});')
BLITZ = svg("bz", f'<path d="M120 10 L40 170 H110 L80 300 L190 120 H120 L160 10 Z" fill="{GOLD}" {GL(GOLD)}/>', 460, 230, 220, 310, "0 0 220 310")
TROPFEN = svg("tp", f'<path d="M110 10 C150 90 200 150 200 210 C200 270 160 300 110 300 C60 300 20 270 20 210 C20 150 70 90 110 10 Z" fill="{BLAU}" {GL(BLAU)}/>', 1240, 230, 220, 310, "0 0 220 310")
sz(st("s11"), st("s12"), BLITZ + TROPFEN + t("sw-a", "Strom", 560, 70) .replace('style="top:560px', 'style="left:-390px;top:560px') + t("sw-b", "Wasser", 560, 70).replace('style="top:560px', 'style="left:390px;top:560px')
   + chip("sw-c", "Strompreise ▲", ROT, 680, 80),
   lambda a, d: f'pop("#bz", {cap("s11", 1)}); pop("#sw-a", {cap("s11", 2)}); pop("#tp", {cap("s11", 2)} + 0.4); pop("#sw-b", {cap("s11", 2)} + 0.4); slam("#sw-c", {cap("s11", 5)});')
h, j = domino_szene(1, "Dominostein 2: die Rechenzentren")
sz(st("s12"), st("s13"), h, j)
CHIPS = "".join(f'<div class="ch" style="position:absolute;left:{360 + i * 150}px;top:380px;width:120px;height:120px;border-radius:16px;background:#16191b;border:6px solid {GRUEN};'
                f'box-shadow:0 0 30px {GRUEN}55;z-index:2"></div>' for i in range(8))
sz(st("s13"), st("s14"), t("wc-t", "weniger Rechenzentren =", 200, 80) + CHIPS + t("wc-z", "weniger Chips", 600, 130, "glow-r"),
   lambda a, d: (f'pop("#wc-t", {a}); tl.fromTo(".ch", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.05 }}, {a} + 0.2);'
                 f' tl.to(".ch", {{ opacity: 0.12, duration: 0.2, stagger: {{ each: 0.08, from: "end" }} }}, {cap("s13", 2)}); slam("#wc-z", {cap("s13", 2)} + 0.3);'))
sz(st("s14"), st("s15"), plakette("gv1", "Nvidia", 660, 360) + plakette("gv2", "AMD", 1260, 360) + t("gv-t", "verdienen gerade Milliarden", 560, 84, "glow-g"),
   lambda a, d: f'pop("#gv1", {cap("s14", 1)}); pop("#gv2", {cap("s14", 1)} + 0.3); pop("#gv-t", {cap("s14", 2)});')
h, j = domino_szene(2, "Dominostein 3: die Chip-Aktien")
sz(st("s15"), st("s16"), h, j)
sz(st("s16"), st("s17"), plakette("nv", "Nvidia", 960, 300, 1.3) + t("nv-z", "−9 %", 470, 230, "glow-r"),
   lambda a, d: f'pop("#nv", {a}); slam("#nv-z", {cap("s16", 3)}); shake("#nv-z", {cap("s16", 3)} + 0.3);')
sz(st("s17"), st("s18"), t("bw-z", "−400 Mrd $", 300, 200, "glow-r") + chip("bw-c", "Börsenwert an EINEM Tag", ROT, 640, 70),
   lambda a, d: f'slam("#bw-z", {a}); pop("#bw-c", {cap("s17", 1)});')
sz(st("s18"), st("s19"), plakette("amd", "AMD", 960, 330, 1.3) + t("amd-t", "noch verrückter …", 520, 110, "glow-o"),
   lambda a, d: f'pop("#amd", {a}); pop("#amd-t", {a} + 0.4);')
sz(st("s19"), st("s20"), chip("rq-c", "Rekordquartal", GRUEN, 230, 90) + t("rq-k", "Rechenzentren", 440, 80) + t("rq-z", "+97 %", 560, 200, "glow-g"),
   lambda a, d: f'pop("#rq-c", {a} + 0.2); pop("#rq-k", {cap("s19", 2)}); pop("#rq-z", {cap("s19", 3)}); zaehl("#rq-z", 0, 97, {cap("s19", 3)}, 0.9, " %");')
S[-1] = (S[-1][0], S[-1][1], S[-1][2].replace('>+97 %<', '>0 %<'), S[-1][3])
sz(st("s20"), st("s21"), chart("ad", "M10 120 L200 90 L380 110 L520 60 L600 80 L640 420 L760 380 L900 450", ROT, 360, 260, 1000, 520) + t("ad-t", "Aktie: zweistellig MINUS", 170, 80, "glow-r"),
   lambda a, d: f'draw("#ad-l", {a}, 1.4); pop("#ad-t", {cap("s20", 1)});')
sz(st("s21"), st("s22"), SPACEX_PL + chip("sx-c", "plant Riesen-Rechenzentrum in Texas", OR, 470, 64) + svg("sx-p", PFEIL_AB, 1600, 250, 120, 140, "-60 0 120 140"),
   lambda a, d: f'pop("#sx", {a}); tl.fromTo("#sx-p", {{ y: -40 }}, {{ y: 30, duration: 0.4, yoyo: true, repeat: 3 }}, {a} + 0.3); pop("#sx-c", {cap("s21", 3)});')
h, j = domino_szene(3, "Dominostein 4: dein Depot")
sz(st("s22"), st("s23"), h, j)
ETF_BOX = (f'<div id="eb" style="position:absolute;left:460px;top:190px;width:1000px;height:520px;border-radius:40px;border:8px dashed {OR};z-index:1"></div>'
           f'<div class="t glow-o" style="top:215px;font-size:60px">Dein ETF (z. B. MSCI World)</div>'
           + plakette("eb1", "Nvidia", 720, 420, 0.85) + plakette("eb2", "AMD", 1200, 420, 0.85) + plakette("eb3", "Microsoft", 960, 590, 0.85))
sz(st("s23"), st("s24"), ETF_BOX, lambda a, d: f'pop("#eb", {a}); pop("#eb1", {cap("s23", 1)}); pop("#eb2", {cap("s23", 1)} + 0.3); pop("#eb3", {cap("s23", 2)});')
sz(st("s24"), st("s25"), chip("sp-c", "Sparplan", OR, 240, 80) + t("sp-z", "auch DU hast verloren", 440, 120, "glow-r") + t("sp-u", "ob du wolltest oder nicht", 640, 70),
   lambda a, d: f'pop("#sp-c", {a}); slam("#sp-z", {cap("s24", 2)}); pop("#sp-u", {cap("s24", 3)});')
sz(st("s25"), st("s26"), ring("te-r", TEILEN_SVG, 760, 140, 400) + t("te-t", "Schick's jemandem, der nervös ist!", 620, 80),
   lambda a, d: f'pop("#te-r", {a}); tl.fromTo("#te-r", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {a} + 0.4); pop("#te-t", {cap("s25", 3)});')
sz(st("s26"), st("s27"), t("fr-a", 'Rekord <span style="color:#2fd27a">▲</span> &nbsp; Aktie <span style="color:#ff4d4d">▼</span>', 280, 150) + t("fr-b", "WIE GEHT DAS?", 560, 120, "glow-o"),
   lambda a, d: f'pop("#fr-a", {a}); slam("#fr-b", {cap("s26", 2)}); shake("#fr-b", {cap("s26", 2)} + 0.3);')
sz(st("s27"), st("s28"), chip("zk-1", "heute", "#555c60", 330, 90, 460) + svg("zk-p", f'<path d="M0 40 H300 M260 0 L310 40 L260 80" fill="none" stroke="{OR}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>', 760, 340, 320, 80, "0 0 320 80")
   + chip("zk-2", "ZUKUNFT", OR, 320, 110, 1140) + t("zk-t", "Die Börse handelt Erwartungen", 600, 80, "glow-o"),
   lambda a, d: f'pop("#zk-1", {cap("s27", 2)}); pop("#zk-p", {cap("s27", 3)}); slam("#zk-2", {cap("s27", 3)} + 0.3); pop("#zk-t", {cap("s27", 4)});')
sz(st("s28"), st("s29"), t("ep-t", "Rekordzahlen", 250, 110, "glow-g") + f'<div id="ep-s" style="position:absolute;left:540px;top:450px;padding:14px 50px;border:12px solid {OR};border-radius:24px;color:{OR};font-weight:900;font-size:120px;transform:rotate(-6deg);z-index:4">EINGEPREIST</div>',
   lambda a, d: f'pop("#ep-t", {a}); slam("#ep-s", {cap("s28", 1)});')
PFEILE = "".join(svg(f"ra{i}", PFEIL_AB, 200 + i * 220, 150 + (i % 3) * 30, 90, 120, "-60 0 120 140") for i in range(7))
sz(st("s29"), st("s30"), PFEILE + t("ar-t", "ALLE WOLLEN RAUS", 520, 130, "glow-r"),
   lambda a, d: " ".join(f'tl.fromTo("#ra{i}", {{ y: -300, opacity: 0 }}, {{ y: 40, opacity: 1, duration: 0.5, ease: "power2.in" }}, {cap("s29", 3)} + {i * 0.1:.1f});' for i in range(7)) + f' slam("#ar-t", {cap("s29", 4)});')
sz(st("s30"), st("s31"), chart("er", "M10 140 L160 160 L260 470 L380 420 L520 380 L700 300 L880 260 L1000 200", GRUEN, 460, 280, 1000, 500) + t("er-t", "am nächsten Tag: Erholung", 170, 84, "glow-g"),
   lambda a, d: f'pop("#er-t", {a}); draw("#er-l", {a} + 0.3, 2.4);')
sz(st("s31"), st("s32"), plakette("nv2", "Nvidia", 960, 300, 1.3) + t("nv2-z", "+6 %", 470, 230, "glow-g"),
   lambda a, d: f'pop("#nv2", {a}); slam("#nv2-z", {cap("s31", 1)});')
sz(st("s32"), st("s33"), chart("pv", "M10 100 L200 120 L320 440 L420 300 L560 240 L760 180 L1000 120", OR, 460, 260, 1000, 520)
   + f'<div id="pv-d" style="position:absolute;left:{460 + 320 - 30}px;top:{260 + 440 - 30}px;width:60px;height:60px;border-radius:50%;background:{ROT};box-shadow:0 0 40px {ROT};z-index:3"></div>'
   + chip("pv-c", "Panik-Verkauf = Tiefpunkt", ROT, 190, 70),
   lambda a, d: f'draw("#pv-l", {a}, 1.6); pop("#pv-d", {cap("s32", 3)}); pop("#pv-c", {cap("s32", 3)} + 0.2); tl.fromTo("#pv-d", {{ scale: 1 }}, {{ scale: 1.4, duration: 0.3, yoyo: true, repeat: 5 }}, {cap("s32", 3)} + 0.4);')
sz(st("s33"), st("s34"), t("dl-t", "3 LEHREN", 300, 200, "glow-o"), lambda a, d: f'slam("#dl-t", {cap("s33", 1)});')
sz(st("s34"), st("s35"), regel(1, "Politik bewegt<br/>die Börse", BLAU), regel_js(1))
sz(st("s35"), st("s36"), regel(2, "Gute Zahlen sind<br/>kein Schutz", OR), regel_js(2))
sz(st("s36"), st("s37"), regel(3, "Panik? Lieber<br/>aussitzen", GRUEN), regel_js(3))
sz(st("s37"), st("s38"), t("sa-t", 'Schreck <span style="color:#ffffff88">oder</span> Anfang?', 300, 130, "glow-o") + t("sa-z", "weiß niemand", 520, 100),
   lambda a, d: f'pop("#sa-t", {a}); pop("#sa-z", {cap("s37", 2)});')
sz(st("s38"), DAUER, domino_html("de") + t("de-t", "Wer die Dominosteine kennt, bleibt ruhiger", 150, 70, "glow-g"),
   lambda a, d: " ".join(f'tl.fromTo("#de{i}", {{ rotation: 62 }}, {{ rotation: 62, duration: 0.01 }}, {a});' for i in range(4))
   + f' pop("#de-t", {cap("s38", 1)}); tl.to("#de0, #de1, #de2, #de3", {{ rotation: 0, duration: 0.5, stagger: -0.15, ease: "back.out(1.6)" }}, {cap("s38", 2)});')

SZENEN = S
SFX = ([(a, "whoosh") for a, *_ in S[1:]] + [(0.0, "boom"), (st("s2"), "boom"), (cap("s3", 2), "boom")]
       + [(st(f"s{k}") + 1.1, "boom") for k in (8, 12, 15, 22)] + [(cap("s4", 3) + i * 0.3 + 0.4, "tick") for i in range(4)]
       + [(cap("s10", 3), "boom"), (cap("s16", 3), "boom"), (st("s17"), "kasse"), (cap("s19", 3) + 0.9, "ding"), (cap("s28", 1), "boom"),
          (cap("s31", 1), "ding"), (cap("s38", 2), "pop")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
