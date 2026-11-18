#!/usr/bin/env python3
"""HundeFinanzTv Motor-Short (~73 s, Stimme Dan, → longform-bargeld-grenze): Geldautomaten verschwinden (≈48.000 Ende 2025),
fremde Automaten 4–6 € → bis 144 €/Jahr; 3 Wege gratis: Supermarktkasse (Rewe/Penny/Netto ab 1 Cent, Lidl ab 99 Cent, bis 200 €),
eigener Automaten-Verbund + Bank-App, seltener aber mehr abheben (Gebühr pauschal). Leitmotiv: gezeichneter Geldautomat mit Display."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import logo_sting as ls  # noqa: E402

T0 = ls.einfuegen(HERE, 18)  # Logo nach dem Open Loop (s4)

from analyse_kit import (GELB, GRUEN, KIT_CSS, KIT_JS, OR, ROT, hand, icon_gross, kasten, kreis, news_kopf,  # noqa: E402
                         pfeil, stempel, titel_zeile, vergleich)
from glow_short import build, chip, handy  # noqa: E402
from lf_kit import Kit, folg_js, folg_logo, logo  # noqa: E402

K = Kit(HERE, 15, ["commerzbank-turm", "hvb-turm", "frei-gold", "unicredit-turm", "frankfurt-westhafen", "frei-commerzbank-turm", "frei-mailand-porta-nuova"],
        logos=["rewe.svg", "penny.svg", "netto.svg", "lidl.svg", "bundesbank.png"])
cap, st = K.cap, K.st
S = K.szene
BLAU = "#3aa0ff"


def automat(id_, x, y, w=420, display="", farbe=OR, dreh=0):
    """Leitmotiv: Geldautomat (Gehäuse, Display, Tastenfeld, Geldschlitz)."""
    h = int(w * 1.45)
    tasten = "".join(f'<div style="width:{w * 0.13:.0f}px;height:{w * 0.09:.0f}px;border-radius:6px;background:#3a4147;box-shadow:inset 0 -3px 0 #0006"></div>' for _ in range(12))
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:26px;transform:rotate({dreh}deg);'
            f'background:linear-gradient(180deg,#2d3338,#1a1e21);border:6px solid {farbe};box-shadow:0 0 80px {farbe}77, 0 40px 60px #000;z-index:3">'
            f'<div class="mono" style="position:absolute;left:8%;top:5%;width:84%;font-size:{w * 0.07:.0f}px;color:{farbe};text-align:center;letter-spacing:3px">GELDAUTOMAT</div>'
            f'<div id="{id_}-d" style="position:absolute;left:10%;top:15%;width:80%;height:34%;border-radius:14px;background:radial-gradient(#13324a,#0a1a26);'
            f'border:4px solid #0008;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:{w * 0.12:.0f}px;line-height:1.1;color:#fff;'
            f'box-shadow:inset 0 0 30px {BLAU}55">{display}</div>'
            f'<div style="position:absolute;left:22%;top:55%;width:56%;display:grid;grid-template-columns:repeat(3,1fr);gap:{w * 0.025:.0f}px">{tasten}</div>'
            f'<div style="position:absolute;left:18%;bottom:7%;width:64%;height:{w * 0.05:.0f}px;border-radius:6px;background:#050607;box-shadow:0 0 18px {GRUEN}88"></div></div>')


def plakette(id_, text, x, y, farbe, w=380, size=56, schrift="#fff"):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:20px 0;border-radius:22px;background:{farbe};color:{schrift};'
            f'font-weight:900;font-size:{size}px;text-align:center;box-shadow:0 0 40px {farbe}88, 0 20px 30px #000;z-index:4">{text}</div>')


def karte_logo(id_, datei, x, y, w, unter, farbe=GRUEN):
    return (logo(id_, datei, y, w, x=x, pad=18)
            + f'<div id="{id_}-u" class="mono" style="position:absolute;left:{x - 40}px;width:{w + 80}px;top:{y + w + 54}px;text-align:center;font-size:40px;color:{farbe};'
              f'text-shadow:0 0 20px {farbe};z-index:5">{unter}</div>')


def girocard(id_, x, y, w=520, dreh=-6):
    h = int(w * 0.63)
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:28px;transform:rotate({dreh}deg);'
            f'background:linear-gradient(135deg,#1f5fae,#0d2f5c);box-shadow:0 0 70px {BLAU}88, 0 30px 50px #000;z-index:3;overflow:hidden">'
            f'<div style="position:absolute;left:40px;top:{h * 0.36:.0f}px;width:{w * 0.16:.0f}px;height:{w * 0.12:.0f}px;border-radius:10px;background:linear-gradient(135deg,#f3d27a,#b8902e)"></div>'
            f'<div class="mono" style="position:absolute;left:40px;bottom:30px;font-size:{w * 0.06:.0f}px;color:#ffffffcc;letter-spacing:4px">•••• •••• •••• 2026</div>'
            f'<div style="position:absolute;right:36px;top:28px;font-weight:900;font-style:italic;font-size:{w * 0.09:.0f}px;color:#fff">girocard</div></div>')


# s1 Hook: Automat + Gebühr knallt rein
S("s1", "commerzbank-turm", KIT_CSS + titel_zeile("t1", "⚡ Geldautomaten", farbe=ROT) + automat("a1", 330, 620, 420, "Gebühr<br/>6,00 €", ROT)
  + stempel("s1x", "BIS ZU 6 €", 230, 1060, ROT, 90, -8),
  lambda a, d: KIT_JS + f' pop("#t1", {a}); pop("#a1", {a}); shake("#a1", {cap("s1", 1)}); stempeln("#s1x", {cap("s1", 2)});',
  [(0.0, "bass-schlag")])

# s2 48.000 zählt hoch
S("s2", "hvb-turm", titel_zeile("t2", "Ende 2025 nur noch") + logo("l2", "bundesbank.png", 600, 260, karte=True)
  + f'<div id="n2" style="position:absolute;left:0;width:1080px;top:820px;text-align:center;font-weight:900;font-size:190px;color:{GELB};text-shadow:0 0 50px {GELB}88;z-index:4">48.000</div>'
  + hand("h2", "Geldautomaten in ganz Deutschland", 150, 1050, 56, "#fff", -3),
  lambda a, d: f'pop("#t2", {a}); pop("#l2", {a} + 0.1); zaehl("#n2", 60000, 48000, {cap("s2", 2)} - 0.6, 1.2, ""); pop("#h2", {cap("s2", 2)});',
  [])

# s3 Dein Automat ist weg → nächster fremder
S("s3", "frei-gold", titel_zeile("t3", "Heißt für dich", farbe=GELB) + automat("a3", 90, 640, 340, "defekt", "#9aa4ab", -4)
  + stempel("s3x", "WEG", 110, 820, ROT, 96, -14) + automat("a3b", 650, 640, 340, "5,00 €", ROT, 3)
  + pfeil("p3", 430, 1000, 650, 950, 0.3, GELB) + hand("h3", "der nächste: fremd", 560, 1150, 52, GELB, -3),
  lambda a, d: (f'pop("#t3", {a}); pop("#a3", {a} + 0.1); stempeln("#s3x", {cap("s3", 1)}); draw("#p3-p", {cap("s3", 2)} - 0.3, 0.4); pop("#p3-k", {cap("s3", 2)});'
                f' pop("#a3b", {cap("s3", 2)}); pop("#h3", {cap("s3", 2)} + 0.4);'),
  [(cap("s3", 1), "stempel")])

# s4 3 Wege, der dritte = ?
W4 = "".join(kasten(f"k4{i}", txt, 80 + i * 320, 680, 280, 300, f, 110, u) for i, (txt, f, u) in enumerate(
    [("1", GRUEN, "Weg"), ("2", GRUEN, "Weg"), ("?", GELB, "überrascht")]))
S("s4", "unicredit-turm", titel_zeile("t4", "3 Wege gratis") + W4 + kreis("kr4", 860, 830, 190, 200, GELB),
  lambda a, d: (f'pop("#t4", {a}); pop("#k40", {cap("s4", 0)} + 0.3); pop("#k41", {cap("s4", 0)} + 0.6); pop("#k42", {cap("s4", 1)});'
                f' draw("#kr4-p", {cap("s4", 3)}, 0.6); shake("#k42", {cap("s4", 4)});'),
  [(cap("s4", 3), "spannung")])

# s5 Fremde Automaten 4–6 €
S("s5", "frankfurt-westhafen", titel_zeile("t5", "Fremder Automat", farbe=ROT) + automat("a5", 330, 600, 420, "4–6 €", ROT)
  + hand("h5", "jedes Mal!", 720, 1060, 70, GELB, -8),
  lambda a, d: f'pop("#t5", {a}); pop("#a5", {a} + 0.1); slam("#a5-d", {cap("s5", 1)}); pop("#h5", {cap("s5", 1)} + 0.5);',
  [])

# s6 Rechnung 144 €
S("s6", "frei-commerzbank-turm", titel_zeile("t6", "Pro Jahr")
  + kasten("k6", "2 × 6 € × 12", 140, 620, 800, 200, OR, 90, "zweimal im Monat")
  + f'<div id="n6" style="position:absolute;left:0;width:1080px;top:880px;text-align:center;font-weight:900;font-size:180px;color:{ROT};text-shadow:0 0 50px {ROT}aa;z-index:4">144 €</div>',
  lambda a, d: f'pop("#t6", {a}); pop("#k6", {cap("s6", 0)} + 0.2); slam("#n6", {cap("s6", 3)}); zaehl("#n6", 0, 144, {cap("s6", 3)}, 0.8, " €");',
  [(cap("s6", 3), "kasse")])

# s7 Weg 1 Supermarktkasse
S("s7", "frei-mailand-porta-nuova", titel_zeile("t7", "Weg 1", farbe=GRUEN) + icon_gross("i7", "🛒", 0, 620, 300, GRUEN, True)
  + chip("c7", "Supermarktkasse", GRUEN, 1020, 70),
  lambda a, d: f'pop("#t7", {a}); pop("#i7", {a} + 0.1); slam("#c7", {cap("s7", 0)} + 0.6);',
  [])

# s8 Logos + Mindesteinkauf
L8 = (karte_logo("l8a", "rewe.svg", 90, 610, 170, "ab 1 ct") + karte_logo("l8b", "penny.svg", 335, 590, 170, "ab 1 ct")
      + karte_logo("l8c", "netto.svg", 580, 610, 170, "ab 1 ct") + karte_logo("l8d", "lidl.svg", 825, 590, 170, "ab 99 ct", GELB))
S("s8", "commerzbank-turm", titel_zeile("t8", "Geld an der Kasse") + L8 + hand("h8", "an der Kasse: „Bitte 50 € abheben!“", 150, 1000, 50, "#fff", -2),
  lambda a, d: (f'pop("#t8", {a}); pop("#l8a", {cap("s8", 0)}); pop("#l8b", {cap("s8", 1)}); pop("#l8c", {cap("s8", 1)} + 0.4);'
                f' pop("#l8a-u", {cap("s8", 2)}); pop("#l8b-u", {cap("s8", 2)} + 0.1); pop("#l8c-u", {cap("s8", 2)} + 0.2);'
                f' pop("#l8d", {cap("s8", 3)}); pop("#l8d-u", {cap("s8", 3)} + 0.3); pop("#h8", {cap("s8", 3)} + 0.6);'),
  [])

# s9 Girocard, 200 €, 0 € Gebühr
S("s9", "hvb-turm", titel_zeile("t9", "Bis 200 € auf einmal") + girocard("g9", 280, 620, 520, -6)
  + stempel("s9x", "0 € GEBÜHR", 210, 1010, GRUEN, 90, -6),
  lambda a, d: f'pop("#t9", {a}); pop("#g9", {cap("s9", 1)}); stempeln("#s9x", {cap("s9", 2)});',
  [(cap("s9", 1), "karte-piep")])

# s10 Weg 2 Verbund
NETZ = (icon_gross("i10", "🏦", 0, 690, 200, BLAU, True)
        + pfeil("p10a", 450, 860, 230, 1000, 0.2, BLAU) + pfeil("p10b", 630, 860, 850, 1000, -0.2, BLAU)
        + automat("a10a", 120, 1000, 150, "0 €", GRUEN) + automat("a10b", 810, 1000, 150, "0 €", GRUEN))
S("s10", "frei-gold", titel_zeile("t10", "Weg 2", farbe=GRUEN) + chip("c10", "dein Automaten-Verbund", BLAU, 590, 56) + NETZ,
  lambda a, d: (f'pop("#t10", {a}); pop("#c10", {cap("s10", 0)} + 0.5); pop("#i10", {a} + 0.3); draw("#p10a-p", {cap("s10", 1)}, 0.4); draw("#p10b-p", {cap("s10", 1)}, 0.4);'
                f' pop("#p10a-k", {cap("s10", 1)} + 0.4); pop("#p10b-k", {cap("s10", 1)} + 0.4); pop("#a10a", {cap("s10", 1)} + 0.4); pop("#a10b", {cap("s10", 1)} + 0.5);'),
  [])

# s11 Verbünde + Bank-App
PIN = lambda i, x, y: f'<div id="pin{i}" style="position:absolute;left:{x}px;top:{y}px;font-size:52px;z-index:5">📍</div>'
HANDY11 = ('<div style="font-weight:900;font-size:36px;color:#fff;margin-top:40px">Bank-App</div>'
           f'<div style="position:relative;width:86%;height:330px;border-radius:18px;background:repeating-linear-gradient(0deg,#22313a 0 2px,transparent 2px 40px),'
           f'repeating-linear-gradient(90deg,#22313a 0 2px,transparent 2px 40px),#152027">{PIN(1, 40, 60)}{PIN(2, 160, 170)}{PIN(3, 90, 240)}</div>'
           f'<div class="mono" style="font-size:26px;color:{GRUEN}">nächster: 350 m</div>')
S("s11", "unicredit-turm", titel_zeile("t11", "Gratis im Verbund")
  + plakette("v11a", "Sparkasse", 60, 600, "#e30613", 420, 54) + plakette("v11b", "Volksbank", 60, 730, "#0066b3", 420, 54)
  + plakette("v11c", "Cash Group", 60, 860, "#2b2f33", 420, 54) + plakette("v11d", "Cashpool", 60, 990, "#2b2f33", 420, 54)
  + handy("hd11", 600, 580, 300, HANDY11, GRUEN),
  lambda a, d: (f'pop("#t11", {a}); pop("#v11a", {cap("s11", 0)}); pop("#v11b", {cap("s11", 0)} + 0.5); pop("#v11c", {cap("s11", 1)}); pop("#v11d", {cap("s11", 1)} + 0.4);'
                f' pop("#hd11", {cap("s11", 4)}); pop("#pin1", {cap("s11", 5)}); pop("#pin2", {cap("s11", 5)} + 0.2); pop("#pin3", {cap("s11", 5)} + 0.4);'),
  [])

# s12 Weg 3: einmal viel statt viermal wenig
S("s12", "frankfurt-westhafen", titel_zeile("t12", "Weg 3", farbe=GELB)
  + vergleich("v12", "4 × 50 €", "4 × Gebühr", "1 × 200 €", "1 × Gebühr", ROT, GRUEN, y=640, h=320),
  lambda a, d: f'pop("#t12", {a}); pop("#v12-l", {cap("s12", 4)}); pop("#v12-r", {cap("s12", 3)});',
  [(cap("s12", 3), "level-up")])

# s13 Gebühr gleich – 20 € oder 200 €
S("s13", "frei-commerzbank-turm", titel_zeile("t13", "Gleiche Gebühr")
  + automat("a13a", 110, 620, 330, "20 €", ROT, -3)
  + automat("a13b", 640, 620, 330, "200 €", GRUEN, 3)
  + chip("g13a", "Gebühr 5 €", ROT, 1110, 40, x=130) + chip("g13b", "Gebühr 5 €", ROT, 1110, 40, x=660),
  lambda a, d: f'pop("#t13", {a}); pop("#a13a", {cap("s13", 1)}); pop("#a13b", {cap("s13", 2)} + 0.5); pop("#g13a", {cap("s13", 1)} + 0.4); pop("#g13b", {cap("s13", 2)} + 0.9);',
  [])

# s14 Endkarte Longform
MK = (titel_zeile("mk-t", "Ganzes Video") + f'<div id="mk-b" style="position:absolute;left:371px;top:690px;width:338px;height:600px;border-radius:30px;overflow:hidden;'
      f'border:8px solid {OR};box-shadow:0 0 80px {OR}88;z-index:3"><img src="assets/lf.jpg" style="width:100%;height:100%;object-fit:cover" alt=""/></div>'
      + chip("mk-c", "Jetzt auf unserem Kanal", OR, 580, 50))
S("s14", None, MK,
  lambda a, d: (f'pop("#mk-t", {a}); tl.fromTo("#mk-b", {{ scale: 0.6, rotation: -6, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {a} + 0.2);'
                f' pop("#mk-c", {a} + 0.6);'),
  [])

# s15 Folgen (letzter Satz)
S("s15", "frei-mailand-porta-nuova", titel_zeile("t15", "Folg uns") + folg_logo("fl15", 600, 360) + chip("c15", "+ Folgen", OR, 1020, 70),
  lambda a, d: f'pop("#t15", {a}); {folg_js("fl15", a)} slam("#c15", {cap("s15", 0)} + 0.4);')

html, code = ls.szene()
K.SZ.append((T0, T0 + ls.DAUER, html, code, 7))
K.SFX.extend(ls.sounds(T0))
K.SZ.append((0.0, K.dauer, news_kopf("19.11.2026"), lambda a, d: "", 8))

if __name__ == "__main__":
    build(HERE, K.SZ, K.SFX)
