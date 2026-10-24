#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): Warum Lottogewinner pleite gehen – Marcos Million.
Leitmotiv: Kontostand-Anzeige, die live hoch- und runterzählt. Beagle nur im CTA."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import BLASE, ICON, TEILEN, folgen, gruppe, person  # noqa: E402
from lf_szenen import Zeit, balken3, chips_zeit, karte  # noqa: E402

Z = Zeit(HERE)
st = Z.st
BLAU, LILA, DUNKEL = "#3d7be0", "#9b59b6", "#1d2125"
MARCO = person(ORANGE, "#353a3d")
KUGEL_F = [ROT, BLAU, GRUEN, ORANGE, LILA, "#c99a06"]

SCHEIN = svg('<rect x="8" y="10" width="84" height="80" rx="6" fill="#fff8d6" stroke="#c99a06" stroke-width="4" /><rect x="8" y="10" width="84" height="16" rx="6" fill="#e24b4b" />'
             '<text x="50" y="22" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="10" fill="#fff">LOTTO 6 aus 49</text>' + "".join(
                 f'<rect x="{16 + (i % 7) * 10}" y="{32 + (i // 7) * 10}" width="7" height="7" fill="none" stroke="#e24b4b" stroke-width="1.2" />' for i in range(35))
             + "".join(f'<path d="M{17 + (i % 7) * 10} {33 + (i // 7) * 10} l5 5 m0 -5 l-5 5" stroke="#111" stroke-width="1.6" />' for i in (3, 9, 15, 20, 26, 33)))
KOPF = svg('<path d="M30 92 L30 72 Q14 64 14 44 Q14 10 50 10 Q86 10 86 42 L94 58 L84 60 L84 74 Q84 82 74 82 L62 82 L62 92 Z" fill="#cfd6db" stroke="#353a3d" stroke-width="4" />'
           '<text x="50" y="56" text-anchor="middle" font-family="Abril Fatface" font-size="34" fill="#1f7a4d">€?</text>')
ANZUG = svg('<circle cx="50" cy="26" r="16" fill="#f1c9a5" /><path d="M16 98 Q16 52 50 50 Q84 52 84 98 Z" fill="#353a3d" /><path d="M42 50 L50 74 L58 50 Z" fill="#fff" /><path d="M48 54 L52 54 L54 76 L50 82 L46 76 Z" fill="#e24b4b" />'
            '<rect x="62" y="4" width="36" height="22" rx="6" fill="#f2c418" /><text x="80" y="20" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="12" fill="#111">20 %!</text>')
STUDIE = svg('<rect x="14" y="6" width="72" height="88" rx="5" fill="#fff" stroke="#353a3d" stroke-width="4" /><text x="50" y="24" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="11" fill="#111">STUDIE</text>'
             '<path d="M24 76 L24 40 M24 76 L76 76" stroke="#353a3d" stroke-width="3" /><path d="M28 48 L42 60 L54 52 L72 72" fill="none" stroke="#e24b4b" stroke-width="4" />')


def kugeln(gr=150):
    zahlen = [7, 13, 21, 29, 36, 42]
    return "".join(f'<div id="ku-{i}" style="width:{gr}px;height:{gr}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 12%,{c} 13%);'
                   f'display:flex;align-items:center;justify-content:center"><div style="width:{gr * 0.55:.0f}px;height:{gr * 0.55:.0f}px;border-radius:50%;background:#fff;'
                   f'color:#111;font-weight:900;font-size:{gr * 0.28:.0f}px;display:flex;align-items:center;justify-content:center">{z}</div></div>'
                   for i, (z, c) in enumerate(zip(zahlen, KUGEL_F)))


def eur(v):
    return f"{v:,.0f} €".replace(",", ".")


def konto(uid, start, schritte, zeilen, titel="Marcos Konto", farbe=GRUEN):
    """Kontostand-Anzeige links, zählt bei jedem Schritt [(sid, neuer_wert)] live; Balken zeigt Anteil an 1 Mio.; rechts Zeilen."""
    stil = {"h": "font-family:'Abril Fatface',serif;font-size:86px;line-height:1.05;color:#111",
            "s": "font-weight:800;font-size:48px;line-height:1.2;color:#353a3d",
            "k": "font-weight:700;font-size:40px;line-height:1.25;color:#555c60",
            "r": "font-weight:800;font-size:48px;line-height:1.2;color:#e24b4b",
            "g": "font-weight:800;font-size:48px;line-height:1.2;color:#1f7a4d"}
    rechts = "".join(f'<div id="{uid}-z{k}" style="{stil[a]}">{t}</div>' for k, (t, _, a) in enumerate(zeilen))
    breite = 100 * min(start, 1_000_000) / 1_000_000
    html = (f'<div style="position:absolute;left:110px;top:200px;width:820px;padding:44px 50px;border-radius:40px;background:{DUNKEL};box-shadow:0 18px 0 #000">'
            f'<div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:2px">{titel.upper()}</div>'
            f'<div id="{uid}-n" style="font-family:\'Abril Fatface\',serif;font-size:118px;color:{farbe};margin:20px 0 30px;white-space:nowrap">{eur(start)}</div>'
            f'<div style="height:44px;border-radius:22px;background:#3a4045;overflow:hidden"><div id="{uid}-b" style="height:100%;width:100%;border-radius:22px;background:{farbe};'
            f'transform-origin:left center;transform:scaleX({breite / 100:.3f})"></div></div>'
            f'<div style="display:flex;justify-content:space-between;font-weight:700;font-size:28px;color:#9aa3a8;margin-top:10px"><span>0 €</span><span>1 Mio. €</span></div></div>'
            f'<div style="position:absolute;left:1000px;top:150px;width:820px;height:680px;display:flex;flex-direction:column;justify-content:center;gap:22px">{rechts}</div>')

    def js(t0, d):
        out = [f'const {uid}o = {{ v: {start} }};']
        alt = start
        for sid, neu in schritte:
            a = Z.euro_zeit(sid) + 0.2
            out.append(f'tl.fromTo({uid}o, {{ v: {alt} }}, {{ v: {neu}, duration: 1.4, ease: "power1.inOut", onUpdate: () => {{ '
                       f'document.querySelector("#{uid}-n").textContent = Math.round({uid}o.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " €"; }} }}, {a});')
            out.append(f'tl.fromTo("#{uid}-b", {{ scaleX: {min(alt, 1e6) / 1e6:.3f} }}, {{ scaleX: {min(neu, 1e6) / 1e6:.3f}, duration: 1.4, ease: "power1.inOut" }}, {a});')
            alt = neu
        for k, (_, sid, _) in enumerate(zeilen):
            a = st(sid) if sid else t0
            out.append(f'tl.fromTo("#{uid}-z{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {max(a, t0 + 0.1)});')
        return " ".join(out)
    return dict(html=html, js=js)


def intro():
    html = (f'<div class="mitte" style="gap:50px"><div style="display:flex;gap:26px">{kugeln(150)}</div>'
            '<div id="in-t" class="serif" style="font-size:150px;line-height:1;color:#c99a06">1.000.000 €</div>'
            '<div id="in-s" style="font-weight:800;font-size:64px;color:#353a3d">… und dann pleite?</div></div>')

    def js(t0, d):
        return ("".join(f' tl.fromTo("#ku-{i}", {{ y: -30 }}, {{ y: 0, duration: 0.5, ease: "bounce.out" }}, {t0} + {i * 0.08:.2f});' for i in range(6))
                + f' tl.fromTo("#in-t", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5 }}, {t0}); pop("#in-s", {st("s6")});')
    return dict(html=html, js=js)


def marco_intro():
    fakten = [("32 Jahre", "s11"), ("Lagerist", "s11"), ("Zahlen = Geburtstage", "s12"), ("Miete · altes Auto", "s13")]
    chips = "".join(f'<div id="mi-c{i}" class="chip" style="background:#353a3d">{t}</div>' for i, (t, _) in enumerate(fakten))
    html = (f'<div class="mitte" style="flex-direction:row;gap:90px"><div id="mi-p" style="display:flex;flex-direction:column;align-items:center;gap:16px">'
            f'<div style="width:320px;height:420px">{MARCO}</div><div class="chip" style="background:{ORANGE}">Marco</div></div>'
            f'<div style="display:flex;flex-direction:column;align-items:flex-start;gap:22px">{chips}'
            f'<div id="mi-j" style="margin-top:20px;padding:18px 56px;border-radius:30px;background:#f2c418;color:#111;font-weight:900;font-size:110px;transform:rotate(-4deg)">JACKPOT!</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#mi-p", {t0});' + "".join(f' pop("#mi-c{i}", {st(s)} + {i % 2 * 0.4});' for i, (_, s) in enumerate(fakten))
                + f' pop("#mi-j", {st("s14")} + 1.2); tl.fromTo("#mi-j", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3 }}, {st("s15")});')


def stadien():
    stadion = '<div style="width:110px;height:70px;border-radius:50%;border:8px solid #9aa3a8;background:#bfe3c8"></div>'
    grid = "".join(f'<div class="sd" style="opacity:0">{stadion}</div>' for _ in range(32))
    html = (f'<div class="mitte" style="gap:40px"><div style="display:grid;grid-template-columns:repeat(8,130px);gap:22px">{grid}</div>'
            f'<div style="display:flex;gap:30px"><div id="sd-a" class="chip" style="background:#353a3d">× über 1.000 Stadien voller Scheine</div>'
            f'<div id="sd-b" class="chip" style="background:#c99a06">1 Gewinner</div></div>'
            f'<div id="sd-c" style="font-weight:800;font-size:46px;color:#e24b4b">jede Woche spielen: im Schnitt über 1 Mio. Jahre warten</div></div>')
    return dict(html=html, js=lambda t0, d: f'tl.to(".sd", {{ opacity: 1, duration: 0.2, stagger: 0.06 }}, {t0} + 0.2); pop("#sd-a", {st("s27")}); pop("#sd-b", {st("s28")}); pop("#sd-c", {st("s29")});')


def mythos():
    html = ('<div class="mitte" style="gap:40px"><div id="my-t" class="serif" style="font-size:150px;color:#111">„70 % pleite“?</div>'
            '<div id="my-s" style="padding:16px 60px;border:12px solid #e24b4b;border-radius:20px;color:#e24b4b;font-weight:900;font-size:110px;transform:rotate(-8deg)">NICHT BELEGT</div>'
            '<div id="my-u" style="font-weight:800;font-size:50px;color:#353a3d">… aber es passiert oft genug</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#my-t", {t0}); tl.fromTo("#my-s", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "power4.in" }}, {t0} + 1.6); pop("#my-u", {st("s71")});')


def gruende():
    karten = [("1", "Eine Million ist endlich", "100.000 €/Jahr → nach 10 Jahren leer", "s73"), ("2", "Gewöhnung an Luxus", "fühlt sich schnell normal an", "s75"),
              ("3", "Laufende Kosten", "Sportwagen: jedes Jahr Tausende", "s77"), ("4", "Falsche Freunde", "alle wollen etwas von dir", "s79")]
    k = "".join(f'<div id="gr-{i}" style="width:780px;padding:30px 40px;border-radius:30px;background:#faf5ef;border-left:16px solid #e24b4b">'
                f'<div style="font-family:\'Abril Fatface\',serif;font-size:58px;color:#111">{n} · {t}</div><div style="font-weight:700;font-size:38px;color:#555c60;margin-top:8px">{u}</div></div>'
                for i, (n, t, u, _) in enumerate(karten))
    html = f'<div class="mitte"><div style="display:grid;grid-template-columns:repeat(2,780px);gap:34px">{k}</div></div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#gr-{i}", {st(s) if i else t0});' for i, (_, _, _, s) in enumerate(karten)))


def regeln():
    items = [("Erst mal nichts tun", "s85"), ("Niemandem erzählen", "s88"), ("Unabhängiger Berater", "s90"), ("Haus mit bezahlbaren Kosten", "s92"), ("Breit gestreut anlegen", "s93")]
    rows = "".join(f'<div id="rg-{i}" style="display:flex;align-items:center;gap:28px"><div style="width:90px;height:90px;border-radius:50%;background:#1f7a4d;color:#fff;'
                   f'font-family:\'Abril Fatface\',serif;font-size:56px;display:flex;align-items:center;justify-content:center">{i + 1}</div>'
                   f'<div style="font-weight:800;font-size:62px;color:#111">{t}</div></div>' for i, (t, _) in enumerate(items))
    html = f'<div class="mitte"><div style="display:flex;flex-direction:column;gap:26px">{rows}</div></div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#rg-{i}", {st(s) if i else t0});' for i, (_, s) in enumerate(items)))


def plan_torte():
    teile = [(300, "Haus", BLAU), (50, "Reserve", "#9aa3a8"), (50, "Traum", LILA), (600, "Anlage", GRUEN)]
    import math
    a, segs = -90.0, []
    for v, _, c in teile:
        w = 360 * v / 1000
        x1, y1 = 50 + 45 * math.cos(math.radians(a)), 50 + 45 * math.sin(math.radians(a))
        x2, y2 = 50 + 45 * math.cos(math.radians(a + w)), 50 + 45 * math.sin(math.radians(a + w))
        segs.append(f'<path d="M50 50 L{x1:.2f} {y1:.2f} A45 45 0 {1 if w > 180 else 0} 1 {x2:.2f} {y2:.2f} Z" fill="{c}" stroke="#fff" stroke-width="1.5" />')
        a += w
    leg = "".join(f'<div id="pt-{i}" style="display:flex;align-items:center;gap:20px"><div style="width:50px;height:50px;border-radius:12px;background:{c}"></div>'
                  f'<div style="font-weight:800;font-size:52px;color:#111">{eur(v * 1000)} · {t}</div></div>' for i, (v, t, c) in enumerate(teile))
    html = (f'<div class="mitte" style="flex-direction:row;gap:100px"><div id="pt-k" style="width:560px;height:560px">{svg("".join(segs))}</div>'
            f'<div style="display:flex;flex-direction:column;gap:26px">{leg}</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#pt-k", {t0});' + "".join(f' pop("#pt-{i}", {t0} + {0.5 + i * 0.6:.1f});' for i in range(3)) + f' pop("#pt-3", {st("s95")});')


KAPITEL = {"k1": "Einstieg", "k2": "Der Gewinn & Jahr 1", "k3": "Der Absturz", "k4": "Warum das passiert", "k5": "Der bessere Weg"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s5", "frei", intro()),
    ("s6", "s9", "split", dict(icon=ICON(KOPF), text="Nicht Pech – Psychologie", sub="Viele haben nach Jahren weniger als vorher", sub_at=0.6)),
    ("s10", "s15", "frei", marco_intro()),
    ("s16", "s17", "frei", konto("k0", 0, [], [("Wir verfolgen sein Konto", None, "h"), ("Jahr für Jahr", None, "s"), ("… und zeigen den besseren Weg", "s17", "g")])),
    ("s18", "s20", "split", dict(icon=ICON(BLASE), text="Was würdest du mit 1 Mio. kaufen?", sub="Schreib's in die Kommentare!", sub_at=st("s20") - st("s18"))),
    ("s21", "s22", "frei", folgen("+ Folgen")),
    ("s23", "s23", "kapitel", dict(titel="Wie wahrscheinlich ist das?")),
    # ---- Gewinn & Jahr 1 ----
    ("s24", "s25", "zahl", dict(zahl="1 : 140 Mio.", sub="Chance auf den Jackpot bei 6 aus 49", farbe=ROT)),
    ("s26", "s29", "frei", stadien()),
    ("s30", "s33", "frei", konto("k1", 0, [("s31", 1_000_000)], [("Marco hat ihn!", None, "h"), ("in Deutschland steuerfrei", "s31", "g"), ("2 Wochen später auf dem Konto", "s32", "s")])),
    ("s34", "s34", "kapitel", dict(titel='Jahr 1: <span style="color:#DB8622">Die Party</span>')),
    ("s35", "s40", "frei", konto("k2", 1_000_000, [("s36", 500_000), ("s37", 420_000), ("s39", 300_000)],
                                 [("Job gekündigt", "s35", "r"), ("Haus: 500.000 € bar", "s36", "s"), ("Sportwagen: 80.000 €", "s37", "s"), ("Reisen · Uhren · Technik", "s39", "s")])),
    ("s41", "s47", "frei", konto("k3", 300_000, [("s43", 200_000)],
                                 [("Plötzlich melden sich alle", None, "h"), ("Geschäft · Hochzeit · …", "s42", "k"), ("100.000 € verliehen", "s43", "r"),
                                  ("nach 1 Jahr: noch 200.000 €", "s45", "s"), ("„Ist doch noch genug da“", "s47", "s")])),
    # ---- Absturz ----
    ("s48", "s48", "kapitel", dict(titel='Jahr 2 – 4: <span style="color:#e24b4b">Der Absturz</span>')),
    ("s49", "s54", "frei", chips_zeit(Z, "lk", "Laufende Kosten", [("Grundsteuer", "#555c60", "s50"), ("Versicherungen", "#555c60", None), ("Reparaturen", "#555c60", None),
                                                                     ("neuer Lebensstil", ORANGE, "s51"), ("= 5.000 € / Monat", ROT, "s52"), ("= 60.000 € / Jahr", ROT, "s53")])),
    ("s55", "s57", "split", dict(icon=gruppe((person(GRUEN, "#353a3d"), 1), (person(BLAU, "#8a5a2b"), 1), (person(LILA, "#353a3d"), 1), w=170, h=240),
                                 text="Neue „Freunde“", farbe=ROT, sub="vor allem da, wenn er bezahlt", sub_at=st("s57") - st("s55"))),
    ("s58", "s61", "split", dict(icon=ICON(ANZUG), text="Der „Finanzexperte“", sub='<span style="color:#e24b4b">Betrug: 50.000 € weg</span>', sub_at=Z.euro_zeit("s60") - st("s58"))),
    ("s62", "s65", "frei", konto("k4", 200_000, [("s62", 0)], [("Nach 4 Jahren: leer", None, "r"), ("Auto verkauft · Kredit aufs Haus", "s63", "s"),
                                                             ("Jobsuche nach Jahren Pause", "s64", "k"), ("mehr Stress als vorher", "s65", "r")], farbe=ROT)),
    # ---- Warum ----
    ("s66", "s69", "split", dict(icon=ICON(STUDIE), text="Studie: Großer Gewinn schützt nicht", sub="plötzlicher Reichtum → riskante Entscheidungen", sub_at=st("s69") - st("s66"))),
    ("s70", "s71", "frei", mythos()),
    ("s72", "s72", "frei", karte("4 Gründe", "Warum passiert das?", ROT, uid="wa")),
    ("s73", "s80", "frei", gruende()),
    ("s81", "s83", "frei", chips_zeit(Z, "au", "Passiert auch bei …", [("Erbschaft", BLAU, "s82"), ("Abfindung", BLAU, None), ("großem Bonus", BLAU, None)])),
    # ---- Der bessere Weg ----
    ("s84", "s84", "kapitel", dict(titel='Spulen wir <span style="color:#1f7a4d">zurück</span>')),
    ("s85", "s93", "frei", regeln()),
    ("s94", "s95", "frei", plan_torte()),
    ("s96", "s101", "frei", konto("k5", 0, [("s96", 24_000)], [("Marco 2.0", None, "h"), ("= 2.000 € im Monat extra", "s97", "g"), ("dauerhaft", "s98", "s"),
                                                             ("+ sein Gehalt", "s99", "s"), ("reich werden ≠ reich bleiben", "s101", "g")], titel="Entnahme pro Jahr")),
    ("s102", "s104", "zahl", dict(zahl="≈ 50 %", sub="der Einsätze fließen als Gewinne zurück", farbe=ROT)),
    ("s105", "s107", "frei", balken3(Z, "ei", [("eingesetzt (40 Jahre)", "20.000 €+", 480, ROT, None), ("im Schnitt zurück", "≈ 10.000 €", 240, ORANGE, "s105")], "Sparen gewinnt immer", "s107")),
    ("s108", "s109", "split", dict(icon=ICON(SCHEIN), text="Zum Spaß: ja. Als Plan: nie.", sub='<span style="color:#1f7a4d">Wohlstand = guter Umgang mit Geld</span>', sub_at=st("s109") - st("s108"))),
    ("s110", "s110", "split", dict(icon=ICON(BLASE), text="Was würdest du mit 1 Mio. machen?", sub="Schreib's in die Kommentare!", sub_at=1.5)),
    ("s111", "s111", "split", dict(icon=ICON(TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s112", "s112", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
