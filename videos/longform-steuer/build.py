#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): 7 legale Steuertricks – der Steuer-Tresor mit Tim.
Leitmotiv: Tresor mit 7 Schlössern, die nacheinander aufspringen. Beagle nur im CTA."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import BLASE, HANDY, ICON, TEILEN, folgen, person  # noqa: E402
from lf_szenen import Zeit, balken3, chips_zeit  # noqa: E402

Z = Zeit(HERE)
st = Z.st
BLAU, GRAU, DUNKEL = "#3d7be0", "#555c60", "#353a3d"
TIM = person(BLAU, "#8a5a2b")

PARAGRAF = svg('<circle cx="50" cy="50" r="44" fill="#faf5ef" stroke="#353a3d" stroke-width="5" /><text x="50" y="70" text-anchor="middle" font-family="Abril Fatface" font-size="60" fill="#353a3d">§</text>')
PROZENT = svg('<rect x="10" y="10" width="80" height="80" rx="18" fill="#1f7a4d" /><text x="50" y="68" text-anchor="middle" font-family="Abril Fatface" font-size="52" fill="#fff">%</text>')
ABRECHNUNG = svg('<rect x="16" y="4" width="68" height="92" rx="5" fill="#fff" stroke="#353a3d" stroke-width="4" /><text x="50" y="22" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="9" fill="#111">Nebenkosten</text>'
                 + "".join(f'<rect x="24" y="{32 + i * 11}" width="{38 - (i % 2) * 10}" height="4" rx="2" fill="#ccc" /><rect x="68" y="{32 + i * 11}" width="8" height="4" rx="2" fill="#999" />' for i in range(4))
                 + '<rect x="22" y="76" width="56" height="12" rx="3" fill="#1f7a4d" /><text x="50" y="85" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="8" fill="#fff">absetzbar!</text>')
KOFFER = svg('<rect x="12" y="30" width="76" height="56" rx="10" fill="#DB8622" /><path d="M36 30 L36 18 Q36 12 42 12 L58 12 Q64 12 64 18 L64 30" fill="none" stroke="#a8621a" stroke-width="6" />'
             '<rect x="12" y="52" width="76" height="6" fill="#a8621a" /><circle cx="28" cy="40" r="5" fill="#f2c418" /><path d="M60 40 L70 44 L60 48 Z" fill="#fff" />')
RING = svg('<circle cx="50" cy="50" r="42" fill="none" stroke="#e24b4b" stroke-width="16" stroke-dasharray="33 33" /><circle cx="50" cy="50" r="42" fill="none" stroke="#fff" stroke-width="16" stroke-dasharray="33 33" stroke-dashoffset="33" />'
           '<circle cx="50" cy="50" r="50" fill="none" stroke="#353a3d" stroke-width="2" /><circle cx="50" cy="50" r="34" fill="none" stroke="#353a3d" stroke-width="2" />')

NAMEN = ["Arbeitsweg", "Homeoffice", "Arbeitsmittel", "Fortbildung", "Kleinkram", "Handwerker", "Spenden"]


def schloss_pos(n):
    """Schloss 1–6 im Kreis, 7 in der Mitte (Tresor 640×640)."""
    if n == 7:
        return 320, 320
    w = math.radians(-90 + (n - 1) * 60)
    return 320 + 205 * math.cos(w), 320 + 205 * math.sin(w)


def tresor(uid, aktiv, zeilen, offen_bis=None, alle_auf_sid=None):
    """Tresortür links, Schlösser < aktiv sind offen (grün), aktiv pulsiert und springt auf; rechts Zeilen [(text, sid, art)]."""
    offen_bis = aktiv - 1 if offen_bis is None else offen_bis
    s = []
    for n in range(1, 8):
        x, y = schloss_pos(n)
        gr = 150 if n == 7 else 120
        if n <= offen_bis:
            bg, inhalt = GRUEN, "✓"
        elif n == aktiv:
            bg, inhalt = ORANGE, str(n)
        else:
            bg, inhalt = GRAU, str(n)
        s.append(f'<div id="{uid}-s{n}" style="position:absolute;left:{x - gr / 2:.0f}px;top:{y - gr / 2:.0f}px;width:{gr}px;height:{gr}px;border-radius:50%;'
                 f'background:{bg};border:8px solid #f2c418;color:#fff;font-family:\'Abril Fatface\',serif;font-size:{gr * 0.5:.0f}px;display:flex;align-items:center;justify-content:center">'
                 f'<span id="{uid}-t{n}">{inhalt}</span></div>')
    tuer = (f'<div style="position:absolute;left:120px;top:150px;width:640px;height:640px;border-radius:44px;background:{DUNKEL};box-shadow:inset 0 0 0 18px #555c60, 0 18px 0 #222">'
            f'{"".join(s)}<div style="position:absolute;left:-18px;top:200px;width:28px;height:240px;border-radius:8px;background:#8a8f93"></div></div>')
    stil = {"h": "font-family:'Abril Fatface',serif;font-size:92px;line-height:1.05;color:#111",
            "s": "font-weight:800;font-size:50px;line-height:1.2;color:#353a3d",
            "k": "font-weight:700;font-size:40px;line-height:1.25;color:#555c60",
            "r": "font-weight:800;font-size:46px;line-height:1.2;color:#e24b4b",
            "g": "font-weight:800;font-size:50px;line-height:1.2;color:#1f7a4d"}
    rechts = "".join(f'<div id="{uid}-z{k}" style="{stil[a]}">{t}</div>' for k, (t, _, a) in enumerate(zeilen))
    html = tuer + f'<div style="position:absolute;left:860px;top:140px;width:960px;height:680px;display:flex;flex-direction:column;justify-content:center;gap:22px">{rechts}</div>'

    def js(t0, d):
        out = []
        if 1 <= aktiv <= 7:
            out.append(f'tl.fromTo("#{uid}-s{aktiv}", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.2);')
            auf = t0 + 1.6
            out.append(f'tl.to("#{uid}-s{aktiv}", {{ backgroundColor: "{GRUEN}", duration: 0.3 }}, {auf});')
            out.append(f'tl.to("#{uid}-t{aktiv}", {{ opacity: 0, duration: 0.15 }}, {auf}); tl.set("#{uid}-t{aktiv}", {{ textContent: "✓" }}, {auf + 0.15}); tl.to("#{uid}-t{aktiv}", {{ opacity: 1, duration: 0.2 }}, {auf + 0.16});')
        if alle_auf_sid:
            out.append(f'tl.fromTo("#{uid}-s1, #{uid}-s2, #{uid}-s3, #{uid}-s4, #{uid}-s5, #{uid}-s6, #{uid}-s7", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 1, stagger: 0.08 }}, {st(alle_auf_sid)});')
        for k, (_, sid, _) in enumerate(zeilen):
            a = st(sid) if sid else t0
            out.append(f'tl.fromTo("#{uid}-z{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {max(a, t0 + 0.1)});')
        return " ".join(out)
    return dict(html=html, js=js)


def intro():
    html = ('<div class="mitte" style="gap:40px"><div id="in-t1" class="serif" style="font-size:130px;line-height:1.05;color:#111;text-align:center">'
            'Du verschenkst Geld<br />ans <span style="color:#e24b4b">Finanzamt</span>!</div>'
            '<div id="in-t2" style="padding:16px 50px;border-radius:40px;background:#1f7a4d;color:#fff;font-weight:900;font-size:66px">7 legale Steuertricks</div></div>')
    return dict(html=html, js=lambda t0, d: "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-t1", "in-t2")))


def tim_intro():
    blase = ('<div id="ti-b" style="position:relative;padding:34px 46px;background:#fff;border:6px solid #111;border-radius:40px;font-weight:800;font-size:56px;color:#111;max-width:760px">'
             '„Zu kompliziert – und am Ende kommt eh nichts raus.“</div>')
    html = (f'<div class="mitte" style="flex-direction:row;gap:80px"><div id="ti-p" style="display:flex;flex-direction:column;align-items:center;gap:16px">'
            f'<div style="width:330px;height:430px">{TIM}</div><div class="chip" style="background:{BLAU}">Tim, 35</div></div>'
            f'<div style="display:flex;flex-direction:column;gap:30px">{blase}<div id="ti-m" class="serif" style="font-size:80px;color:#1f7a4d">Mal sehen …</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#ti-p", {t0}); pop("#ti-b", {st("s12")}); pop("#ti-m", {st("s13")});')


def schwelle():
    """Pauschbetrag als Schwelle: bis 1.230 € automatisch, darüber zählt jeder Euro."""
    html = ('<div class="mitte" style="gap:50px"><div id="sw-t" class="serif" style="font-size:96px;color:#111">Der Pauschbetrag</div>'
            '<div style="position:relative;width:1500px;height:150px;border-radius:30px;overflow:hidden;display:flex">'
            '<div id="sw-a" style="width:820px;background:#9aa3a8;color:#fff;font-weight:900;font-size:52px;display:flex;align-items:center;justify-content:center">bis 1.230 €: automatisch</div>'
            '<div id="sw-b" style="flex:1;background:#1f7a4d;color:#fff;font-weight:900;font-size:52px;display:flex;align-items:center;justify-content:center">darüber: jeder Euro zählt!</div></div>'
            '<div id="sw-n" style="font-weight:800;font-size:46px;color:#555c60">Werbungskosten pro Jahr →</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#sw-t", {t0}); tl.fromTo("#sw-a", {{ scaleX: 0, transformOrigin: "left center" }}, {{ scaleX: 1, duration: 0.6 }}, {st("s22")} + 0.4); '
                                           f'tl.fromTo("#sw-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {st("s24")}); pop("#sw-n", {st("s23")});')


def tresor_auf():
    stapel = [("Arbeitskosten", "≈ 300 €", 260, "s88"), ("Handwerker", "300 €", 260, "s89"), ("Spenden", "≈ 60 €", 70, "s90")]
    sp = "".join(f'<div id="ta-{i}" style="display:flex;flex-direction:column;align-items:center;gap:12px"><div class="serif" style="font-size:58px;color:#7a5a00">{v}</div>'
                 f'<div style="width:200px;height:{h}px;background:repeating-linear-gradient(0deg,#f2c418 0 22px,#c99a06 22px 26px);border-radius:12px"></div>'
                 f'<div style="font-weight:800;font-size:38px;color:#353a3d">{t}</div></div>' for i, (t, v, h, _) in enumerate(stapel))
    html = (f'<div style="position:absolute;left:260px;top:150px;width:1400px;height:700px;border-radius:44px;background:#fff8d6;box-shadow:inset 0 0 0 18px #555c60">'
            f'<div style="position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:center;gap:90px;padding-bottom:70px">{sp}</div>'
            f'<div id="ta-s" style="position:absolute;right:60px;top:50px;padding:16px 40px;border-radius:30px;background:#1f7a4d;color:#fff;font-family:\'Abril Fatface\',serif;font-size:80px">≈ 650 € zurück</div>'
            f'<div id="ta-d" style="position:absolute;inset:0;border-radius:44px;background:{DUNKEL};transform-origin:left center;display:flex;align-items:center;justify-content:center">'
            f'<div style="width:300px;height:300px">{RING}</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'tl.to("#ta-d", {{ rotationY: -100, opacity: 0, duration: 1.2, ease: "power2.in" }}, {t0} + 0.5); '
                                           + " ".join(f'pop("#ta-{i}", {Z.euro_zeit(s)});' for i, (_, _, _, s) in enumerate(stapel)) + f' pop("#ta-s", {Z.euro_zeit("s91")});')


def vier_jahre():
    jahre = "".join(f'<div id="vj-{i}" style="display:flex;flex-direction:column;align-items:center;width:300px;border-radius:24px;overflow:hidden;border:6px solid #353a3d">'
                    f'<div style="width:100%;padding:14px 0;background:{BLAU};color:#fff;text-align:center;font-weight:900;font-size:56px">{j}</div>'
                    f'<div class="serif" style="padding:40px 0;font-size:72px;color:#1f7a4d">≈ 650 €</div></div>' for i, j in enumerate([2022, 2023, 2024, 2025]))
    html = (f'<div class="mitte" style="gap:50px"><div id="vj-t" class="serif" style="font-size:90px;color:#111">Bis zu 4 Jahre rückwirkend</div>'
            f'<div style="display:flex;gap:40px">{jahre}</div><div id="vj-s" class="chip" style="background:#1f7a4d">zusammen über 2.500 €</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#vj-t", {st("s93")});' + "".join(f' pop("#vj-{i}", {st("s94")} + {i * 0.4});' for i in range(4)) + f' pop("#vj-s", {Z.euro_zeit("s95")});')


KAPITEL = {"k1": "Einstieg", "k2": "Schloss 1 – 3", "k3": "Schloss 4 – 5", "k4": "Schloss 6 – 7", "k5": "Der Tresor geht auf"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s3", "frei", intro()),
    ("s4", "s6", "frei", chips_zeit(Z, "pr", "Das Problem", [("keine Steuererklärung", ROT, "s4"), ("die Hälfte vergessen", ROT, "s5"), ("Finanzamt erinnert dich nicht", ROT, "s6")])),
    ("s7", "s9", "frei", tresor("t0", 0, [("Der Steuer-Tresor", None, "h"), ("7 Schlösser · 7 legale Tricks", "s8", "s"), ("durchgerechnet an einem Beispiel", "s9", "k")])),
    ("s10", "s14", "frei", tim_intro()),
    ("s15", "s15", "split", dict(icon=ICON(PARAGRAF), text="Keine Steuerberatung", sub="Beträge können sich jedes Jahr ändern", sub_at=0.8)),
    ("s16", "s18", "split", dict(icon=ICON(BLASE), text="Machst du eine Steuererklärung?", sub="Ja oder Nein in die Kommentare!", sub_at=st("s18") - st("s16"))),
    ("s19", "s20", "frei", folgen("+ Folgen")),
    ("s21", "s24", "frei", schwelle()),
    ("s25", "s27", "split", dict(icon=ICON(PARAGRAF), text="Der größte Irrtum …", farbe=ROT, sub="2 Schlösser zählen gar nicht zum Pauschbetrag!", sub_at=st("s27") - st("s25"))),
    # ---- Schloss 1 – 3 ----
    ("s28", "s34", "frei", tresor("t1", 1, [("Schloss 1", None, "h"), ("Der Weg zur Arbeit", None, "s"), ("egal ob Auto, Rad, Bus oder zu Fuß", "s30", "k"),
                                          ("Tim: 20 km · 3 Tage pro Woche", "s33", "s"), ("≈ 800 € im Jahr ansetzbar", "s34", "g")])),
    ("s35", "s41", "frei", tresor("t2", 2, [("Schloss 2", None, "h"), ("Homeoffice: 6 € pro Tag", "s36", "s"), ("max. 210 Tage = 1.260 €", "s37", "k"),
                                          ("Küchentisch reicht!", "s38", "g"), ("Tim: ≈ 500 €", "s40", "s"), ("pro Tag: Fahrt ODER Homeoffice", "s41", "r")])),
    ("s42", "s49", "frei", tresor("t3", 3, [("Schloss 3", None, "h"), ("Arbeitsmittel", None, "s"), ("Laptop · Stuhl · Bücher · Software", "s44", "k"),
                                          ("Computer: sofort im 1. Jahr", "s46", "g"), ("Tim: Laptop für 600 €", "s49", "s")])),
    # ---- Schloss 4 – 5 ----
    ("s50", "s54", "frei", tresor("t4", 4, [("Schloss 4", None, "h"), ("Fortbildung", None, "s"), ("Kurse · Seminare · Sprachkurs", "s51", "k"),
                                          ("sogar ein Studium nach der Ausbildung", "s53", "g"), ("Tim: Excel-Kurs 300 €", "s54", "s")])),
    ("s55", "s59", "frei", tresor("t5", 5, [("Schloss 5", None, "h"), ("Der Kleinkram", None, "s"), ("Kontoführung: 16 € pauschal", "s56", "g"),
                                          ("Bewerbung · Gewerkschaft · Handy", "s57", "k"), ("Umzug für den neuen Job", "s58", "k")])),
    ("s60", "s64", "frei", balken3(Z, "ti", [("Tims Kosten", "≈ 2.200 €", 460, BLAU, None), ("Pauschbetrag", "1.230 €", 260, "#9aa3a8", "s62")], "≈ 1.000 € extra → ≈ 300 € zurück", "s63")),
    ("s65", "s67", "split", dict(icon=ICON(PROZENT), text="Höherer Steuersatz = mehr zurück", farbe=GRUEN, sub="… und das ist erst der Anfang", sub_at=st("s67") - st("s65"))),
    ("s68", "s68", "kapitel", dict(titel='Die 2 <span style="color:#1f7a4d">Geld-Schlösser</span>')),
    # ---- Schloss 6 – 7 ----
    ("s69", "s74", "frei", tresor("t6", 6, [("Schloss 6", None, "h"), ("Handwerker & Haushaltshilfe", None, "s"), ("20 % direkt von der Steuer!", "s70", "g"),
                                          ("Schornsteinfeger · Gärtner · Putzhilfe", "s72", "k"), ("auch als Mieter!", "s74", "s")])),
    ("s75", "s78", "split", dict(icon=ICON(ABRECHNUNG), text="Nebenkostenabrechnung checken!", sub="nur per Überweisung zahlen – nicht bar", sub_at=st("s77") - st("s75"))),
    ("s79", "s80", "zahl", dict(zahl="+300 €", sub="Tims Bad: 20 % von 1.500 € Arbeitskosten", farbe=GRUEN)),
    ("s81", "s86", "frei", tresor("t7", 7, [("Schloss 7", None, "h"), ("Spenden", None, "s"), ("bis 300 €: Kontoauszug reicht", "s83", "g"),
                                          ("Tim: 200 € ans Tierheim → ≈ 60 €", "s85", "s"), ("Alle 7 geknackt ✓", "s86", "g")], alle_auf_sid="s86")),
    # ---- Der Tresor geht auf ----
    ("s87", "s91", "frei", tresor_auf()),
    ("s92", "s92", "kapitel", dict(titel='Der eigentliche <span style="color:#e24b4b">Knaller</span>')),
    ("s93", "s96", "frei", vier_jahre()),
    ("s97", "s98", "split", dict(icon=ICON(KOFFER), text="Jedes Jahr einen Kurzurlaub verschenkt", farbe=ROT)),
    ("s99", "s103", "frei", chips_zeit(Z, "so", "So einfach geht's", [("Elster – kostenlos", BLAU, "s100"), ("oder Steuer-App", BLAU, None),
                                                                      ("Daten oft schon drin", GRUEN, "s101"), ("nächstes Jahr übernehmen", GRUEN, "s102"), ("Geld in wenigen Wochen", ORANGE, "s103")])),
    ("s104", "s105", "split", dict(icon=ICON(HANDY), text="Belege als Foto sammeln", sub="→ in 1 Stunde fertig", sub_at=st("s105") - st("s104"))),
    ("s106", "s107", "split", dict(icon=ICON(RING), text="Hilfe: Lohnsteuerhilfeverein", sub="oder Steuerberater – Kosten teils absetzbar", sub_at=st("s107") - st("s106"))),
    ("s108", "s110", "frei", tresor("ta", 8, [("Die 7 Schlösser", None, "h"), (" · ".join(NAMEN), "s109", "k"), ("schon 2 – 3 lohnen sich!", "s110", "g")], offen_bis=7)),
    ("s111", "s111", "split", dict(icon=ICON(KOFFER), text="Tim: 4 Jahre nachgeholt → Kurzurlaub!", farbe=GRUEN)),
    ("s112", "s112", "split", dict(icon=ICON(BLASE), text="Steuererklärung: Ja oder Nein?", sub="Schreib's in die Kommentare!", sub_at=1.2)),
    ("s113", "s113", "split", dict(icon=ICON(TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s114", "s114", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
