#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (Dark Glow): Inflation 4 % – erhöht die EZB jetzt die Zinsen? (Kommentar-CTA Mitte, echtes EZB-Logo).
Leitbild: Preis-Thermometer + Leitzins-Regler mit EZB-Logo; 4 Bereiche als Kacheln, 3 Tipps."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import BLASE_SVG, GOLD, GRUEN, OR, ROT, build, chip, cta_szene, handy, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
BLAU = "#4d8ff0"
S = []


def sz(a, b, html, js):
    S.append((a, b, html, js))


def ezb(id_, x, y, w):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:{w * 0.06:.0f}px;border-radius:{w * 0.08:.0f}px;background:#fff;'
            f'box-shadow:0 0 80px {BLAU}88;z-index:3"><img src="assets/logos/ezb.svg" alt="" style="width:100%;display:block"/></div>')


THERMO = (f'<svg viewBox="0 0 200 500" style="position:absolute;left:420px;top:420px;width:240px;height:600px;overflow:visible;z-index:2">'
          f'<rect x="70" y="20" width="60" height="380" rx="30" fill="#16191b" stroke="#fff" stroke-width="8"/>'
          f'<circle cx="100" cy="430" r="55" fill="{ROT}" stroke="#fff" stroke-width="8" filter="drop-shadow(0 0 24px {ROT})"/>'
          f'<rect id="th-f" x="84" y="60" width="32" height="340" rx="16" fill="{ROT}" style="transform-origin:100px 400px" filter="drop-shadow(0 0 14px {ROT})"/>'
          + "".join(f'<rect x="140" y="{60 + i * 68}" width="26" height="6" fill="#fff"/>' for i in range(5)) + '</svg>')
KORB = (f'<svg id="kb" viewBox="0 0 300 220" style="position:absolute;left:330px;top:440px;width:420px;height:308px;z-index:2">'
        f'<g filter="drop-shadow(0 0 20px {OR})"><path d="M20 70 H280 L250 200 H50 Z" fill="none" stroke="{OR}" stroke-width="14" stroke-linejoin="round"/>'
        f'<path d="M80 70 L120 15 M220 70 L180 15" stroke="{OR}" stroke-width="12" stroke-linecap="round"/>'
        f'<circle cx="110" cy="60" r="26" fill="{ROT}"/><rect x="150" y="30" width="50" height="40" rx="8" fill="{GOLD}"/><circle cx="215" cy="58" r="18" fill="{GRUEN}"/></g></svg>')
REGLER = (f'<div style="position:absolute;left:140px;top:860px;width:800px;height:40px;border-radius:20px;background:#2a3036;z-index:2"></div>'
          f'<div id="rg-f" style="position:absolute;left:140px;top:860px;width:800px;height:40px;border-radius:20px;background:linear-gradient(90deg,{GRUEN},{OR},{ROT});'
          f'transform-origin:0 50%;z-index:2"></div>'
          f'<div id="rg-k" style="position:absolute;left:{140 + 800 * 0.5 - 40}px;top:840px;width:80px;height:80px;border-radius:50%;background:#fff;box-shadow:0 0 30px #fff;z-index:3"></div>'
          f'<div class="t" style="top:940px;font-size:44px;color:#ffffffaa">Leitzins</div>')


def kachel(n, titel, farbe, symbol):
    return (f'<div id="kc{n}" style="position:absolute;left:140px;top:460px;width:800px;padding:50px 0;border-radius:40px;background:#16191b;border:8px solid {farbe};'
            f'box-shadow:0 0 80px {farbe}55;text-align:center;z-index:2"><div style="font-size:150px;font-weight:900;color:{farbe};line-height:1">{symbol}</div>'
            f'<div style="font-weight:900;font-size:90px;color:#fff;margin-top:20px">{n}. {titel}</div></div>')


def kachel_js(n):
    return lambda a, d: f'tl.fromTo("#kc{n}", {{ x: 1100, rotation: 6 }}, {{ x: 0, rotation: 0, duration: 0.45, ease: "back.out(1.4)" }}, {a});'


def tipp(n, txt, farbe):
    return (f'<div id="tp{n}" style="position:absolute;left:90px;top:520px;width:900px;border-radius:40px;background:#16191b;border:8px solid {farbe};'
            f'box-shadow:0 0 80px {farbe}55;padding:50px;z-index:2;text-align:center">'
            f'<div style="font-weight:900;font-size:60px;color:{farbe}">TIPP {n}</div>'
            f'<div style="font-weight:900;font-size:76px;line-height:1.08;color:#fff;margin-top:20px">{txt}</div></div>')


def tipp_js(n):
    return lambda a, d: f'tl.fromTo("#tp{n}", {{ x: -1100, rotation: -6 }}, {{ x: 0, rotation: 0, duration: 0.45, ease: "back.out(1.4)" }}, {a});'


def pfeil(id_, hoch, farbe, x, y, gr=200):
    d = "M50 90 L50 10 M15 45 L50 8 L85 45" if hoch else "M50 10 L50 90 M15 55 L50 92 L85 55"
    return (f'<svg id="{id_}" viewBox="0 0 100 100" style="position:absolute;left:{x}px;top:{y}px;width:{gr}px;height:{gr}px;z-index:3">'
            f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" filter="drop-shadow(0 0 14px {farbe})"/></svg>')


frage_html, frage_js = cta_szene("fr", BLASE_SVG, "Sparer oder Kredit?<br/>Schreib's uns!")

# Hook
sz(0.0, st("s2"), THERMO + t("h-z", "4 %", 1100, 220, "glow-r") + t("h-u", "Inflation Eurozone", 1360, 70),
   lambda a, d: (f'tl.fromTo("#th-f", {{ scaleY: 0.2 }}, {{ scaleY: 1, duration: 1.4, ease: "power2.out" }}, {a}); slam("#h-z", {cap("s1", 2)});'
                 f' pop("#h-u", {cap("s1", 2)} + 0.3);'))
sz(st("s2"), st("s3"), ezb("ez", 290, 420, 500) + t("ez-q", 'Zinsen <span class="box">RAUF?</span>', 1000, 130),
   lambda a, d: f'pop("#ez", {a}); slam("#ez-q", {cap("s2", 3)}); shake("#ez-q", {cap("s2", 4)});')
sz(st("s3"), st("s4"), chip("b-1", "Tagesgeld", GRUEN, 460, 84) + chip("b-2", "Kredit", ROT, 620, 84) + chip("b-3", "ETFs", BLAU, 780, 84) + t("b-t", "Was heißt das für dich?", 990, 70, "glow-o"),
   lambda a, d: f'pop("#b-1", {cap("s3", 0)} + 0.4); pop("#b-2", {cap("s3", 1)}); pop("#b-3", {cap("s3", 2)}); pop("#b-t", {cap("s3", 3)});')
sz(st("s4"), st("s5"), t("fo-t", "Folge", 520, 110) + t("fo-n", "HundeFinanzTv", 660, 110, "glow-o") + chip("fo-f", "+ Folgen", OR, 880, 90),
   lambda a, d: f'pop("#fo-t", {a}); pop("#fo-n", {a} + 0.2); slam("#fo-f", {a} + 0.5);')
sz(st("s5"), st("s6"), f'<div id="hw" style="position:absolute;left:140px;top:620px;width:800px;padding:50px 0;border-radius:30px;background:#16191b;border:6px solid {ROT};'
   f'text-align:center;font-weight:900;font-size:80px;color:#fff;z-index:2">Keine<br/>Anlageberatung</div>', lambda a, d: f'pop("#hw", {a} + 0.1);')
sz(st("s6"), st("s7"), t("wi-t", 'Was heißt<br/><span class="box">4 % Inflation?</span>', 580, 110), lambda a, d: f'slam("#wi-t", {a} + 0.2);')
sz(st("s7"), st("s8"), KORB + t("ko-a", "100 €", 820, 120) + t("ko-p", "→", 960, 100, "glow-o") + t("ko-b", "104 €", 1070, 170, "glow-r"),
   lambda a, d: f'pop("#kb", {a}); pop("#ko-a", {cap("s7", 2)}); pop("#ko-p", {cap("s7", 3)}); slam("#ko-b", {cap("s7", 3)} + 0.3);')
sz(st("s8"), st("s9"), chip("de-c", "Deutschland", OR, 470, 80) + t("de-z", "2,8 %", 640, 240, "glow-o") + t("de-u", "etwas niedriger", 920, 80),
   lambda a, d: f'pop("#de-c", {a}); slam("#de-z", {cap("s8", 2)}); pop("#de-u", {cap("s8", 1)});')
sz(st("s9"), st("s10"), ezb("ez2", 240, 440, 600) + t("ez2-t", "Europäische Zentralbank", 940, 70, "glow-o"),
   lambda a, d: f'tl.fromTo("#ez2", {{ scale: 0.4, rotation: -10 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.7)" }}, {cap("s9", 1)}); pop("#ez2-t", {cap("s9", 2)});')
sz(st("s10"), st("s11"), chip("zi-c", "Ziel", GRUEN, 480, 90) + t("zi-z", "2 %", 640, 260, "glow-g") + t("zi-u", "stabile Preise", 950, 80),
   lambda a, d: f'pop("#zi-u", {cap("s10", 1)}); pop("#zi-c", {cap("s10", 2)}); slam("#zi-z", {cap("s10", 2)} + 0.3);')
sz(st("s11"), st("s12"), t("lz-k", "Leitzins", 450, 110, "glow-o") + t("lz-z", "≈ 2,5 %", 600, 220) + REGLER,
   lambda a, d: (f'pop("#lz-k", {cap("s11", 1)}); slam("#lz-z", {cap("s11", 3)}); tl.fromTo("#rg-f", {{ scaleX: 0 }}, {{ scaleX: 0.5, duration: 0.8 }}, {a} + 0.4);'))
sz(st("s12"), st("s13"), t("mc-a", "Preise zu schnell?", 440, 90, "glow-r") + pfeil("mc-p", True, ROT, 440, 560) + t("mc-b", "Zinsen rauf", 800, 110, "glow-o")
   + t("mc-c", "→ Geld wird teurer", 960, 70),
   lambda a, d: f'pop("#mc-a", {a}); pop("#mc-p", {cap("s12", 1)}); slam("#mc-b", {cap("s12", 1)} + 0.2); pop("#mc-c", {cap("s12", 2)});')
KAL = (f'<div id="kl" style="position:absolute;left:340px;top:440px;width:400px;height:420px;border-radius:34px;background:#f4f1ea;overflow:hidden;z-index:2;box-shadow:0 0 80px {BLAU}66">'
       f'<div style="height:110px;background:{BLAU};color:#fff;font-weight:900;font-size:60px;text-align:center;line-height:110px">DEZ</div>'
       f'<div style="text-align:center;font-weight:900;font-size:230px;color:#111;line-height:300px">17</div></div>')
sz(st("s13"), st("s14"), KAL + t("kl-t", "nächste EZB-Sitzung", 920, 70, "glow-o") + chip("kl-c", "Erhöhung erwartet", ROT, 1060, 64),
   lambda a, d: (f'tl.fromTo("#kl", {{ rotation: -20, scale: 0.5, opacity: 0 }}, {{ rotation: 0, scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }}, {a});'
                 f' pop("#kl-t", {cap("s13", 1)}); slam("#kl-c", {cap("s13", 3)});'))
sz(st("s14"), st("s15"), t("vb-t", "4 BEREICHE", 560, 190, "glow-o"), lambda a, d: f'slam("#vb-t", {cap("s14", 2)});')
sz(st("s15"), st("s16"), kachel(1, "Tagesgeld", GRUEN, "€"), kachel_js(1))
sz(st("s16"), st("s17"), pfeil("tg-p", True, GRUEN, 440, 440) + t("tg-z", "Zinsen steigen", 720, 110, "glow-g") + chip("tg-c", "gut für Sparer", GRUEN, 900, 80),
   lambda a, d: f'pop("#tg-p", {a}); slam("#tg-z", {cap("s16", 2)}); pop("#tg-c", {cap("s16", 3)});')
sz(st("s17"), st("s18"), kachel(2, "Kredit", ROT, "%"), kachel_js(2))
sz(st("s18"), st("s19"), pfeil("kr-p", True, ROT, 440, 440) + t("kr-z", "teurer", 720, 160, "glow-r") + chip("kr-c", "Kredit & Dispo", ROT, 960, 80),
   lambda a, d: f'pop("#kr-p", {a}); slam("#kr-z", {cap("s18", 1)}); pop("#kr-c", {cap("s18", 2)});')
sz(st("s19"), st("s20"), kachel(3, "Immobilien", OR, "⌂"), kachel_js(3))
sz(st("s20"), st("s21"), t("im-a", "Baukredit teurer", 480, 96, "glow-r") + pfeil("im-p", False, OR, 440, 620) + t("im-b", "Hauspreise gebremst", 880, 90, "glow-o"),
   lambda a, d: f'pop("#im-a", {cap("s20", 1)}); pop("#im-p", {cap("s20", 2)}); pop("#im-b", {cap("s20", 2)} + 0.3);')
sz(st("s21"), st("s22"), kachel(4, "ETFs", BLAU, "↗"), kachel_js(4))
WACKEL = (f'<svg viewBox="0 0 800 400" style="position:absolute;left:140px;top:460px;width:800px;height:400px;overflow:visible;z-index:2">'
          f'<path d="M0 390 L800 390" stroke="#ffffff33" stroke-width="4"/>'
          f'<path id="wk-l" d="M10 300 L90 250 L150 320 L230 200 L290 280 L370 170 L430 250 L520 140 L590 200 L680 90 L790 40" fill="none" stroke="{BLAU}" stroke-width="14" '
          f'stroke-linejoin="round" stroke-linecap="round" filter="drop-shadow(0 0 14px {BLAU})"/></svg>')
sz(st("s22"), st("s23"), WACKEL + t("et-t", "kurzfristig nervös", 920, 90, "glow-o"),
   lambda a, d: f'draw("#wk-l", {a}, 2.2); pop("#et-t", {cap("s22", 1)});')
sz(st("s23"), st("s24"), t("lf-a", "langfristig zählen", 480, 90) + t("lf-z", "GEWINNE", 640, 190, "glow-g"),
   lambda a, d: f'pop("#lf-a", {a}); slam("#lf-z", {cap("s23", 1)});')
sz(st("s24"), st("s25"), frage_html, frage_js)
sz(st("s25"), st("s26"), t("dt-t", "3 TIPPS", 580, 200, "glow-o"), lambda a, d: f'slam("#dt-t", {cap("s25", 1)});')
sz(st("s26"), st("s27"), tipp(1, "Notgeld aufs<br/>Tagesgeld", GRUEN), tipp_js(1))
sz(st("s27"), st("s28"), tipp(2, "Kredit jetzt<br/>vergleichen", OR), tipp_js(2))
sz(st("s28"), st("s29"), tipp(3, "Sparplan<br/>weiterlaufen lassen", BLAU), tipp_js(3))
sz(st("s29"), DAUER, THERMO.replace('id="th-f"', 'id="th-g"') + t("en-a", "Inflation verstehen", 1100, 90, "glow-o") + t("en-b", "= gegensteuern", 1240, 100, "glow-g"),
   lambda a, d: (f'tl.fromTo("#th-g", {{ scaleY: 1 }}, {{ scaleY: 0.45, duration: 2.0, ease: "power2.inOut" }}, {a} + 0.3); pop("#en-a", {cap("s29", 1)}); slam("#en-b", {cap("s29", 3)});'))

SZENEN = S
SFX = ([(a, "whoosh") for a, *_ in S[1:]] + [(0.0, "boom"), (cap("s1", 2), "boom"), (cap("s2", 3), "boom"), (cap("s7", 3) + 0.3, "kasse"),
                                             (cap("s10", 2) + 0.3, "ding"), (cap("s13", 3), "boom"), (cap("s16", 2), "ding"), (cap("s18", 1), "boom"),
                                             (cap("s23", 1), "ding"), (cap("s29", 3), "ding")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
