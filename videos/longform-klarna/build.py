#!/usr/bin/env python3
"""HundeFinanzTv Longform 9:16 (Dark Glow, für TikTok/Instagram): Jetzt kaufen, später zahlen – die Klarna-Falle + neue Regeln ab 20.11.2026 (Teilen-CTA Mitte).
Leitbild: Rechnungsstapel „später“, der wächst und kippt; danach Schutzschild der neuen Regel und 3 Regel-Karten."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from glow_short import GOLD, GRUEN, OR, ROT, TEILEN_SVG, build, chip, cta_szene, handy, partikel, t, zeiten  # noqa: E402

cap, st, en, DAUER = zeiten(HERE)
BLAU = "#4d8ff0"
S = []


def sz(a, b, html, js):
    S.append((a, b, html, js))


def rechnung(id_, x, y, betrag, faellig, farbe=OR, rot=0, z=2):
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:300px;padding:22px 26px;border-radius:20px;background:#f4f1ea;transform:rotate({rot}deg);'
            f'border-top:16px solid {farbe};box-shadow:0 20px 40px #000a, 0 0 40px {farbe}44;z-index:{z}">'
            f'<div style="font-weight:800;font-size:26px;color:#555">Rechnung</div><div style="font-weight:900;font-size:56px;color:#111">{betrag}</div>'
            f'<div style="font-weight:800;font-size:24px;color:{farbe}">fällig: {faellig}</div></div>')


def regel(n, txt, farbe):
    return (f'<div id="rg{n}" style="position:absolute;left:90px;top:520px;width:900px;border-radius:40px;background:#16191b;border:8px solid {farbe};'
            f'box-shadow:0 0 80px {farbe}55;padding:50px 50px;z-index:2;text-align:center">'
            f'<div style="width:180px;height:180px;margin:0 auto 30px;border-radius:50%;background:{farbe};color:#111;font-weight:900;font-size:120px;display:flex;align-items:center;justify-content:center">{n}</div>'
            f'<div style="font-weight:900;font-size:76px;line-height:1.08;color:#fff">{txt}</div></div>')


def regel_js(n):
    return lambda a, d: f'tl.fromTo("#rg{n}", {{ x: -1100, rotation: -6 }}, {{ x: 0, rotation: 0, duration: 0.45, ease: "back.out(1.4)" }}, {a});'


SCHUH = (f'<svg id="sh" viewBox="0 0 300 160" style="position:absolute;left:340px;top:470px;width:400px;height:213px;z-index:2">'
         f'<g filter="drop-shadow(0 0 22px {OR})"><path d="M20 120 L30 50 Q80 60 120 30 L170 40 Q190 90 270 100 Q290 104 290 130 L20 130 Z" fill="{OR}"/>'
         f'<rect x="20" y="128" width="270" height="18" rx="6" fill="#fff"/><path d="M100 50 L120 80 M125 45 L145 75" stroke="#fff" stroke-width="6"/></g></svg>')
RATEN = "".join(f'<div id="ra{i}" style="position:absolute;left:{110 + i * 225}px;top:960px;width:200px;padding:20px 0;border-radius:20px;background:#16191b;'
                f'border:5px solid {OR};text-align:center;font-weight:900;font-size:50px;color:#fff;z-index:2">25 €<div style="font-size:26px;color:#ffffffaa">Rate {i + 1}</div></div>'
                for i in range(4))
GEHIRN = (f'<svg id="gh" viewBox="0 0 300 240" style="position:absolute;left:340px;top:440px;width:400px;height:320px;z-index:2">'
          f'<g fill="none" stroke="#ff9ab0" stroke-width="14" stroke-linecap="round" filter="drop-shadow(0 0 22px #ff9ab0)">'
          f'<path d="M150 30 C90 10 30 50 40 110 C10 140 40 210 100 200 C120 230 180 230 200 200 C260 210 290 140 260 110 C270 50 210 10 150 30 Z"/>'
          f'<path d="M150 30 V210 M90 80 C110 100 110 120 90 140 M210 80 C190 100 190 120 210 140"/></g></svg>')
SCHUFA = (f'<div id="sf" style="position:absolute;left:0;top:1080px;width:1080px;display:flex;justify-content:center;z-index:5">'
          f'<span style="padding:10px 44px;border:12px solid {ROT};border-radius:24px;color:{ROT};font-weight:900;font-size:96px;transform:rotate(-6deg);'
          f'background:#0e1012dd;box-shadow:0 0 60px {ROT}88">SCHUFA ✕</span></div>')
SCHILD = (f'<svg id="sd" viewBox="0 0 300 340" style="position:absolute;left:330px;top:420px;width:420px;height:476px;z-index:2">'
          f'<path d="M150 10 L280 60 L280 170 C280 250 220 300 150 330 C80 300 20 250 20 170 L20 60 Z" fill="#16191b" stroke="{BLAU}" stroke-width="16" filter="drop-shadow(0 0 30px {BLAU})"/>'
          f'<text x="150" y="160" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="64" fill="{BLAU}">EU</text>'
          f'<text x="150" y="225" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="36" fill="#fff">20.11.</text></svg>')
LUPE = (f'<svg id="lp" viewBox="0 0 200 200" style="position:absolute;left:600px;top:560px;width:300px;height:300px;z-index:4">'
        f'<g filter="drop-shadow(0 0 20px {GOLD})"><circle cx="80" cy="80" r="60" fill="#ffffff18" stroke="{GOLD}" stroke-width="14"/>'
        f'<path d="M125 125 L185 185" stroke="{GOLD}" stroke-width="22" stroke-linecap="round"/></g></svg>')

teilen_html, teilen_js = cta_szene("te", TEILEN_SVG, "Schick das jemandem,<br/>der ständig mit<br/>Klarna zahlt!")

# Hook
sz(0.0, st("s2"), t("h-a", "Jetzt kaufen,", 440, 120) + t("h-b", '<span class="box">später zahlen</span>', 600, 120) + t("h-c", "Klingt super?", 880, 90, "glow-o"),
   lambda a, d: f'tl.fromTo("#h-a", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.35 }}, {a}); slam("#h-b", {a} + 0.6); pop("#h-c", {cap("s1", 2)});')
sz(st("s2"), st("s3"), chip("pv-1", "Klarna", "#ffb3c7", 460, 90) + chip("pv-2", "PayPal", BLAU, 620, 90) + chip("pv-3", "& Co.", OR, 780, 90) + t("pv-z", "Milliarden-Geschäft", 980, 84, "glow-g"),
   lambda a, d: f'pop("#pv-1", {cap("s2", 1)}); pop("#pv-2", {cap("s2", 1)} + 0.3); pop("#pv-3", {cap("s2", 2)}); slam("#pv-z", {cap("s2", 2)} + 0.4);')
sz(st("s3"), st("s4"), f'<div id="kl" style="position:absolute;left:340px;top:420px;width:400px;height:420px;border-radius:34px;background:#f4f1ea;overflow:hidden;z-index:2;box-shadow:0 0 80px {ROT}55">'
   f'<div style="height:110px;background:{ROT};color:#fff;font-weight:900;font-size:60px;text-align:center;line-height:110px">NOV</div>'
   f'<div style="text-align:center;font-weight:900;font-size:230px;color:#111;line-height:300px">20</div></div>' + t("kl-t", "Neue Regeln für alle Online-Shopper", 920, 64, "glow-o"),
   lambda a, d: f'tl.fromTo("#kl", {{ rotation: -20, scale: 0.5, opacity: 0 }}, {{ rotation: 0, scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }}, {a}); pop("#kl-t", {cap("s3", 3)});')
sz(st("s4"), st("s5"), t("fo-t", "Folge", 520, 110) + t("fo-n", "HundeFinanzTv", 660, 110, "glow-o") + chip("fo-f", "+ Folgen", OR, 880, 90),
   lambda a, d: f'pop("#fo-t", {a}); pop("#fo-n", {a} + 0.2); slam("#fo-f", {a} + 0.5);')
sz(st("s5"), st("s6"), f'<div id="hw" style="position:absolute;left:140px;top:600px;width:800px;padding:40px 0;border-radius:30px;background:#16191b;border:6px solid {ROT};'
   f'text-align:center;font-weight:900;font-size:70px;color:#fff;z-index:2">Keine Anlage-<br/>oder Rechtsberatung</div>', lambda a, d: f'pop("#hw", {a} + 0.1);')
sz(st("s6"), st("s7"), t("wf-t", 'Wie funktioniert<br/><span class="box">das eigentlich?</span>', 560, 110), lambda a, d: f'slam("#wf-t", {a} + 0.2);')
sz(st("s7"), st("s8"), SCHUH + t("sh-z", "100 €", 720, 150) + RATEN,
   lambda a, d: (f'pop("#sh", {a}); pop("#sh-z", {a} + 0.3);' + " ".join(f' pop("#ra{i}", {cap("s7", 2)} + {i * 0.2:.1f});' for i in range(4))))
FLUSS = (chip("fl-1", "Anbieter", BLAU, 450, 80) + t("fl-p", "→ zahlt sofort →", 640, 70, "glow-g") + chip("fl-2", "Shop", OR, 800, 80)
         + t("fl-u", "Für dich: wirkt kostenlos", 1000, 64))
sz(st("s8"), st("s9"), FLUSS, lambda a, d: f'pop("#fl-u", {a}); pop("#fl-1", {cap("s8", 2)}); pop("#fl-p", {cap("s8", 3)}); pop("#fl-2", {cap("s8", 3)} + 0.3);')
sz(st("s9"), st("s10"), t("gb-a", "Der Shop zahlt", 480, 100) + t("gb-z", "mehrere %", 640, 200, "glow-o") + t("gb-u", "Gebühr pro Kauf", 900, 80),
   lambda a, d: f'pop("#gb-a", {a}); slam("#gb-z", {cap("s9", 2)}); pop("#gb-u", {cap("s9", 3)});')
WAGEN = "".join(f'<div class="wk" style="position:absolute;left:{170 + (i % 4) * 190}px;top:{560 + (i // 4) * 170}px;width:150px;height:140px;border-radius:20px;background:#16191b;'
                f'border:5px solid {OR};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:60px;color:#ff8a1f;z-index:2">+1</div>' for i in range(8))
sz(st("s10"), st("s11"), t("wk-t", "Leute kaufen MEHR", 400, 80, "glow-o") + WAGEN,
   lambda a, d: f'pop("#wk-t", {a}); tl.fromTo(".wk", {{ scale: 0 }}, {{ scale: 1, duration: 0.2, stagger: 0.15, ease: "back.out(2)" }}, {cap("s10", 1)});')
sz(st("s11"), st("s12"), GEHIRN + t("gh-t", 'kein<br/><span class="box">Bezahl-Schmerz</span>', 820, 84),
   lambda a, d: f'pop("#gh", {a}); slam("#gh-t", {cap("s11", 1)});')
sz(st("s12"), st("s13"), t("fa-t", "DIE FALLE", 620, 150, "glow-r"), lambda a, d: f'slam("#fa-t", {a} + 0.2); shake("#fa-t", {a} + 0.5);')
sz(st("s13"), st("s14"), rechnung("mr", 390, 430, "100 €", "überfällig", ROT, -4) + chip("mr-1", "+ Mahngebühr", ROT, 860, 70) + chip("mr-2", "+ Zinsen", ROT, 1000, 70),
   lambda a, d: f'pop("#mr", {a}); slam("#mr-1", {cap("s13", 1)}); slam("#mr-2", {cap("s13", 3)});')
STAPEL = "".join(rechnung(f"st{i}", 130 + (i % 3) * 270 + (i // 3) * 40, 420 + (i // 3) * 180, b, f, c, r, 2 + i)
                 for i, (b, f, c, r) in enumerate([("49 €", "3.12.", OR, -6), ("89 €", "8.12.", "#ffb3c7", 4), ("25 €", "10.12.", BLAU, -3),
                                                   ("120 €", "15.12.", OR, 5), ("35 €", "18.12.", "#ffb3c7", -5), ("60 €", "20.12.", BLAU, 3)]))
sz(st("s14"), st("s15"), STAPEL + t("ub-t", "Überblick? WEG.", 1180, 80, "glow-r"),
   lambda a, d: " ".join(f'tl.fromTo("#st{i}", {{ y: -500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }}, {a} + {i * 0.4:.1f});' for i in range(6))
   + f' pop("#ub-t", {cap("s14", 4)}); shake("#ub-t", {cap("s14", 4)} + 0.3);')
sz(st("s15"), st("s16"), t("ju-t", "Junge Leute", 460, 100) + t("ju-z", "SCHULDEN", 620, 150, "glow-r") + SCHUFA,
   lambda a, d: f'pop("#ju-t", {a}); slam("#ju-z", {cap("s15", 1)}); slam("#sf", {cap("s15", 3)}); shake("#sf", {cap("s15", 3)} + 0.3);')
sz(st("s16"), st("s17"), teilen_html, teilen_js)
sz(st("s17"), st("s18"), t("nr-t", 'Die <span class="box">NEUE REGEL</span>', 620, 120), lambda a, d: f'slam("#nr-t", {a} + 0.1);')
sz(st("s18"), st("s19"), SCHILD + t("eu-t", "EU-Verbraucherkredit-Regel", 960, 64, "glow-o"),
   lambda a, d: f'tl.fromTo("#sd", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }}, {a}); pop("#eu-t", {cap("s18", 2)});')
sz(st("s19"), st("s20"), t("kr-a", "Später zahlen", 440, 100) + t("kr-b", "+ Kredite < 200 €", 600, 90, "glow-o") + t("kr-z", "= echter KREDIT", 800, 120, "glow-r"),
   lambda a, d: f'pop("#kr-a", {a}); pop("#kr-b", {cap("s19", 2)}); slam("#kr-z", {cap("s19", 3)});')
sz(st("s20"), st("s21"), handy("bp", 260, 450, 320, '<div style="font-weight:900;font-size:34px;color:#fff;text-align:center">Kannst du<br/>das zahlen?</div>') + LUPE
   + t("bp-t", "Prüfung VOR dem Kauf", 1120, 70, "glow-o"),
   lambda a, d: f'pop("#bp", {a}); tl.fromTo("#lp", {{ x: 200, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4 }}, {a} + 0.4); tl.fromTo("#lp", {{ rotation: -10 }}, {{ rotation: 10, duration: 0.4, yoyo: true, repeat: 5 }}, {a} + 0.8); pop("#bp-t", {cap("s20", 2)});')
sz(st("s21"), st("s22"), chip("ko-1", "Kosten klarer", GRUEN, 520, 80) + chip("ko-2", "mehr Rechte", GRUEN, 680, 80) + chip("ko-3", "z. B. Widerruf", BLAU, 840, 70),
   lambda a, d: f'pop("#ko-1", {cap("s21", 1)}); pop("#ko-2", {cap("s21", 2)}); pop("#ko-3", {cap("s21", 3)});')
sz(st("s22"), st("s23"), t("sz-a", "mehr Schutz", 520, 110, "glow-g") + t("sz-b", "aber manchmal:", 720, 70) + t("sz-z", "NEIN", 820, 200, "glow-r"),
   lambda a, d: f'pop("#sz-a", {cap("s22", 1)}); pop("#sz-b", {cap("s22", 2)}); slam("#sz-z", {cap("s22", 2)} + 0.3);')
sz(st("s23"), st("s24"), t("bf-t", "BLACK FRIDAY", 560, 150) + chip("bf-c", "27.11. – Achtung!", ROT, 800, 80),
   lambda a, d: f'tl.fromTo("#bf-t", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.in" }}, {cap("s23", 1)}); pop("#bf-c", {cap("s23", 2)});')
sz(st("s24"), st("s25"), t("dr-t", "3 REGELN", 560, 200, "glow-o"), lambda a, d: f'slam("#dr-t", {cap("s24", 2)});')
sz(st("s25"), st("s26"), regel(1, "Nur kaufen, wenn das<br/>Geld schon da ist", GRUEN), regel_js(1))
sz(st("s26"), st("s27"), regel(2, "Max. 1 offene Rechnung<br/>+ Datum in den Kalender", OR), regel_js(2))
sz(st("s27"), st("s28"), regel(3, "Eine Nacht<br/>drüber schlafen", BLAU), regel_js(3))
sz(st("s28"), DAUER, t("fz-a", "Später zahlen ist", 520, 90) + t("fz-b", '<span class="box">ein KREDIT</span>', 680, 150) + t("fz-c", "– behandle es so.", 920, 80, "glow-o"),
   lambda a, d: f'pop("#fz-a", {cap("s28", 1)}); slam("#fz-b", {cap("s28", 2)}); pop("#fz-c", {cap("s28", 4)});')

SZENEN = S
SFX = ([(a, "whoosh") for a, *_ in S[1:]] + [(0.0, "boom"), (st("s1") + 0.6, "pop"), (cap("s2", 2) + 0.4, "kasse"), (cap("s7", 2), "pop"),
                                             (cap("s9", 2), "kasse"), (st("s12") + 0.2, "boom"), (cap("s13", 1), "boom"), (cap("s15", 3), "boom"),
                                             (cap("s19", 3), "boom"), (cap("s22", 2) + 0.3, "boom"), (cap("s23", 1), "boom")]
       + [(st("s14") + i * 0.4, "pop") for i in range(6)] + [(cap("s28", 2), "ding")])

if __name__ == "__main__":
    build(HERE, SZENEN, SFX)
