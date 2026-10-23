#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): Reich mit 40 oder pleite mit 40? Zwei Leben, gleiches Gehalt. Beagle nur im CTA."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import (AUTO, AUTO_PFEIL, BLASE, DENKEN, GELDBEUTEL, GLOBUS, HERZ, ICON, KAL3, KURVE, NACHKAUF, NOTIZ,  # noqa: E402
                   PFEILE, PLAY, SCHOCK, STAPEL, STERN, TEILEN, TREPPE, UHR, WARN, doppel, folgen, person)
from lf_szenen import Zeit, balken3, beleg, chips_zeit, duell, karte  # noqa: E402

Z = Zeit(HERE)
st = Z.st

LEON = person(GRUEN, "#353a3d")
FELIX = person(ROT, "#8a5a2b")
NEUBAU = svg('<rect x="14" y="10" width="72" height="84" rx="4" fill="#cfe6f5" stroke="#353a3d" stroke-width="4" />' + "".join(
    f'<rect x="{22 + (i % 3) * 20}" y="{18 + (i // 3) * 18}" width="16" height="12" fill="#3d7be0" />' for i in range(12)) +
    '<rect x="10" y="44" width="20" height="4" fill="#353a3d" /><rect x="40" y="78" width="20" height="16" fill="#353a3d" />')
ALTBAU = svg('<path d="M10 34 L50 8 L90 34 Z" fill="#a8621a" /><rect x="16" y="34" width="68" height="60" fill="#f6efe1" stroke="#353a3d" stroke-width="4" />' + "".join(
    f'<rect x="{26 + (i % 3) * 18}" y="{44 + (i // 3) * 22}" width="12" height="14" rx="6" fill="#9ed0f0" stroke="#353a3d" stroke-width="2" />' for i in range(3)) +
    '<rect x="42" y="68" width="16" height="26" rx="8" fill="#8a5a2b" />')
PIZZA = svg('<circle cx="50" cy="50" r="44" fill="#f2c418" stroke="#c99a06" stroke-width="6" /><circle cx="50" cy="50" r="36" fill="#e24b4b" opacity="0.85" />' + "".join(
    f'<circle cx="{x}" cy="{y}" r="6" fill="#a8321f" />' for x, y in [(38, 36), (62, 40), (46, 62), (66, 62), (30, 56)]))
TOPF = svg('<rect x="14" y="40" width="72" height="46" rx="10" fill="#9aa3a8" /><rect x="8" y="34" width="84" height="10" rx="5" fill="#555c60" /><rect x="42" y="26" width="16" height="8" rx="3" fill="#555c60" />'
           '<rect x="2" y="50" width="12" height="8" rx="3" fill="#555c60" /><rect x="86" y="50" width="12" height="8" rx="3" fill="#555c60" />')
KARTE = svg('<rect x="6" y="22" width="88" height="56" rx="8" fill="#353a3d" /><rect x="6" y="34" width="88" height="10" fill="#111" /><rect x="16" y="52" width="16" height="12" rx="2" fill="#f2c418" />'
            '<text x="84" y="70" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="13" fill="#e24b4b">Dispo</text>')
NEUWAGEN = svg('<path d="M10 62 L16 40 Q20 30 32 30 L68 30 Q80 30 84 40 L90 62 Z" fill="#e24b4b" /><rect x="6" y="56" width="88" height="22" rx="8" fill="#e24b4b" />'
               '<path d="M26 40 L32 34 L68 34 L74 40 Z" fill="#cfe6f5" /><circle cx="28" cy="78" r="10" fill="#353a3d" /><circle cx="72" cy="78" r="10" fill="#353a3d" />'
               '<path d="M78 14 L82 22 L90 24 L82 26 L78 34 L74 26 L66 24 L74 22 Z" fill="#f2c418" />')


def fig(p, w=300):
    return f'<div style="width:{w}px;height:{w * 1.3:.0f}px">{p}</div>'


def intro():
    html = ('<div class="mitte" style="gap:30px">'
            f'<div style="display:flex;align-items:flex-end;gap:50px"><div id="in-l">{fig(LEON, 240)}</div>'
            '<div id="in-g" class="serif" style="font-size:150px;color:#DB8622;margin-bottom:80px">=</div>'
            f'<div id="in-r">{fig(FELIX, 240)}</div></div>'
            '<div id="in-t" class="serif" style="font-size:96px;line-height:1.05;color:#111;text-align:center">'
            '<span style="color:#1f7a4d">Reich</span> mit 40 oder <span style="color:#e24b4b">pleite</span> mit 40?</div></div>')

    def js(t0, d):
        return "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-l", "in-g", "in-r", "in-t"))
    return dict(html=html, js=js)


def vorstellung():
    def seite(k, p, name, farbe):
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:20px">{fig(p, 280)}'
                f'<div style="padding:10px 44px;border-radius:40px;background:{farbe};color:#fff;font-weight:800;font-size:58px">{name}</div></div>')
    html = (f'<div class="mitte" style="flex-direction:row;gap:120px;top:90px"><div id="vo-l">{seite("l", LEON, "Leon", GRUEN)}</div>'
            '<div style="display:flex;flex-direction:column;align-items:center;gap:26px">'
            '<div id="vo-a" class="chip" style="background:#353a3d">25 Jahre</div>'
            '<div id="vo-g" class="chip" style="background:#DB8622">2.500&nbsp;€ netto</div></div>'
            f'<div id="vo-r">{seite("r", FELIX, "Felix", ROT)}</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#vo-l", {t0}); pop("#vo-r", {t0} + 0.4); pop("#vo-a", {st("s22")}); pop("#vo-g", {Z.euro_zeit("s23")});')


def L(icon, wert, ab=None, wert_sid=None):
    return dict(name="Leon", farbe=GRUEN, icon=icon, wert=wert, ab_sid=ab, wert_sid=wert_sid)


def F(icon, wert, ab=None, wert_sid=None):
    return dict(name="Felix", farbe=ROT, icon=icon, wert=wert, ab_sid=ab, wert_sid=wert_sid)


def entscheidung(nr, titel):
    return karte(f"Entscheidung {nr}", titel, uid=f"en{nr}")


KAPITEL = {"k1": "Einstieg", "k2": "Mit 25 · Der Start", "k3": "Der Alltag", "k4": "Die Jahre vergehen", "k5": "Mit 40 · Die Bilanz"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s1", "frei", intro()),
    ("s2", "s2", "zahl", dict(zahl="+130.000 €", sub="der eine – mit 40", farbe=GRUEN)),
    ("s3", "s3", "zahl", dict(zahl="−8.000 €", sub="der andere – Schulden", farbe=ROT)),
    ("s4", "s7", "split", dict(icon=ICON(SCHOCK), text="Wie kann das sein?", sub="Nicht dumm, nicht faul – ganz normal", sub_at=st("s5") - st("s4"))),
    ("s8", "s8", "chips", dict(chips=[("Lotto", ROT, True), ("Erbe", ROT, True), ("großer Fehler", ROT, True)])),
    ("s9", "s9", "split", dict(icon=ICON(TREPPE), text="Viele kleine Entscheidungen")),
    ("s10", "s11", "zahl", dict(zahl="25 → 40", sub="15 Jahre – alles durchgerechnet")),
    ("s12", "s12", "split", dict(icon=ICON(STERN), text="Am Ende: 5 Lehren", farbe=GRUEN)),
    ("s13", "s14", "split", dict(icon=ICON(DENKEN), text="Erkennst du dich wieder?")),
    ("s15", "s17", "split", dict(icon=ICON(BLASE), text="Sparer oder Genießer?", sub="Schreib's in die Kommentare!", sub_at=st("s17") - st("s15"))),
    ("s18", "s19", "frei", folgen("+ Folgen")),
    ("s20", "s20", "kapitel", dict(titel='<span style="color:#DB8622">Lernen wir sie kennen</span>')),
    # ---- Mit 25 ----
    ("s21", "s25", "frei", vorstellung()),
    ("s26", "s26", "frei", entscheidung(1, "Das Auto")),
    ("s27", "s30", "frei", duell(Z, "au", L(ICON(AUTO, 380, 380), "150 € / Monat", "s29", "s30"), F(ICON(NEUWAGEN, 380, 380), "300 € / Monat", "s27", "s28"))),
    ("s31", "s32", "zahl", dict(zahl="150 €", sub="Unterschied – jeden Monat")),
    ("s33", "s33", "zahl", dict(zahl="27.000 €", sub="in 15 Jahren – nur beim Auto", farbe=ROT)),
    ("s34", "s34", "frei", entscheidung(2, "Die Wohnung")),
    ("s35", "s40", "frei", duell(Z, "wo", L(ICON(ALTBAU, 380, 380), "800 € warm", "s38", "s40"), F(ICON(NEUBAU, 380, 380), "950 € warm", "s35", "s37"))),
    ("s41", "s42", "zahl", dict(zahl="150 €", sub="wieder Unterschied – völlig normal")),
    ("s43", "s43", "zahl", dict(zahl="300 €", sub="pro Monat – Auto + Wohnung", farbe=ROT)),
    # ---- Alltag ----
    ("s44", "s44", "frei", entscheidung(3, "Der Alltag")),
    ("s45", "s47", "frei", duell(Z, "al", L(ICON(TOPF, 380, 380), "kocht selbst, 1 Abo", "s46"), F(doppel(PIZZA, PLAY), "+100 € / Monat", "s45", "s47"))),
    ("s48", "s48", "split", dict(icon=ICON(NOTIZ), text="Kleinigkeiten, die keiner merkt")),
    ("s49", "s49", "frei", karte("Entscheidung 4", "Sparen", GRUEN, uid="en4")),
    ("s50", "s51", "split", dict(icon=ICON(GELDBEUTEL), text="Felix: am Monatsende 0 €", farbe=ROT, sub="„Sparen kann ich später noch“", sub_at=st("s51") - st("s50"))),
    ("s52", "s54", "split", dict(icon=ICON(AUTO_PFEIL, 700, 700), text="Leon: 400 € per Dauerauftrag", farbe=GRUEN, sub="= genau die Differenz", sub_at=st("s54") - st("s52"))),
    ("s55", "s57", "split", dict(icon=ICON(GLOBUS), text="ETF-Sparplan auf die Welt", sub="breit gestreut, günstig, automatisch", sub_at=st("s56") - st("s55"))),
    ("s58", "s60", "split", dict(icon=fig(LEON, 380), text="Leon lebt nicht schlechter", farbe=GRUEN, sub="nur ein bisschen günstiger", sub_at=st("s60") - st("s58"))),
    ("s61", "s61", "chips", dict(chips=[("Vorjahres-Handy", GRUEN, False), ("Ostsee statt Fernreise", GRUEN, False)])),
    ("s62", "s63", "split", dict(icon=doppel(LEON, FELIX), text="Von außen gleich …", sub="… auf dem Konto riesig verschieden", sub_at=st("s63") - st("s62"))),
    # ---- Die Jahre vergehen ----
    ("s64", "s64", "kapitel", dict(titel="Die Jahre vergehen …")),
    ("s65", "s65", "split", dict(icon=ICON(STAPEL), text="Mit 28: Gehaltserhöhung!", farbe=GOLD)),
    ("s66", "s68", "split", dict(icon=ICON(PFEILE), text="Felix: Lifestyle-Inflation", farbe=ROT, sub="mehr verdienen = mehr ausgeben", sub_at=st("s67") - st("s66"))),
    ("s69", "s70", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="Leon: ½ jeder Erhöhung zur Seite", farbe=GRUEN, sub="→ 10.000 € Notgroschen", sub_at=st("s70") - st("s69"))),
    ("s71", "s72", "split", dict(icon=doppel(AUTO, WARN), text="Mit 31: Auto kaputt!", farbe=ROT, sub="Reparatur: 2.000 €", sub_at=Z.euro_zeit("s72") - st("s71"))),
    ("s73", "s75", "frei", duell(Z, "nf", L(ICON(SPARSCHWEIN, 380, 330), "zahlt aus dem Notgroschen", "s73"), F(ICON(KARTE, 380, 380), "Dispo: 11 %+ Zinsen", "s74", "s75"))),
    ("s76", "s76", "zahl", dict(zahl="200 €+", sub="Dispozinsen pro Jahr – für nichts", farbe=ROT)),
    ("s77", "s80", "frei", chips_zeit(Z, "pu", "Felix auf Pump", [("Urlaub auf Raten", ROT, "s77"), ("Handy auf Raten", ROT, "s80"), ("Fernseher 0 %", ROT, None), ("wieder Dispo", ROT, None)])),
    ("s81", "s83", "split", dict(icon=ICON(DENKEN), text="Ständig Geldstress", farbe=ROT, sub="„Wie macht Leon das nur?“", sub_at=st("s83") - st("s81"))),
    ("s84", "s88", "split", dict(icon=ICON(NACHKAUF), text="Leon bleibt ruhig", farbe=GRUEN, sub="Kurse fallen = günstig nachkaufen", sub_at=st("s87") - st("s84"))),
    ("s89", "s90", "frei", duell(Z, "35", L(ICON(KURVE, 380, 380), "≈ 70.000 € Depot", None, "s89"), F(ICON(KARTE, 380, 380), "neuer Kredit", "s90"))),
    # ---- Mit 40 ----
    ("s91", "s93", "frei", karte("15 Jahre später", "Der 40. Geburtstag", GOLD, uid="g40")),
    ("s94", "s98", "frei", beleg(Z, "le", "Leon mit 40", fig(LEON, 380), [
        ("s95", "s95", KAL3, "Selbst eingezahlt", 72000),
        ("s96", "s96", ICON(KURVE), "Gewinn durch Zinseszins", 55000),
        ("s97", "s97", ICON(SPARSCHWEIN, 640, 555), "Notgroschen", 10000),
    ], "s98", "≈ 137.000 €")),
    ("s99", "s101", "zahl", dict(zahl="−8.000 €", sub="Felix mit 40: nichts gespart, nur Schulden", farbe=ROT)),
    ("s102", "s103", "zahl", dict(zahl="145.000 €", sub="Unterschied – bei gleichem Gehalt", farbe=GOLD)),
    ("s104", "s104", "split", dict(icon=ICON(HERZ), text="Mehr Spaß, weniger Geldsorgen", farbe=GRUEN)),
    ("s105", "s107", "frei", balken3(Z, "fr", [("Leon mit 40", "137.000 €", 160, GRUEN, None), ("Leon mit 65", "≈ 700.000 €", 540, GOLD, "s107")], "ohne einen weiteren Euro", "s106")),
    ("s108", "s110", "split", dict(icon=ICON(STERN), text="Finanzielle Freiheit", farbe=GRUEN, sub="Er hat die Wahl", sub_at=st("s110") - st("s108"))),
    ("s111", "s114", "frei", chips_zeit(Z, "ns", "Zu spät für Felix?", [("Nein!", GRUEN, "s112"), ("1 · Schulden abbauen", ORANGE, "s113"), ("2 · Notgroschen", ORANGE, "s114")])),
    ("s115", "s116", "frei", balken3(Z, "vg", [("Felix ab 40", "≈ 320.000 €", 250, ORANGE, "s115"), ("Leon ab 25", "≈ 700.000 €", 540, GOLD, None)], "15 Jahre Vorsprung", "s116")),
    ("s117", "s117", "kapitel", dict(titel='Die <span style="color:#1f7a4d">5 Lehren</span>')),
    ("s118", "s118", "split", dict(icon=ICON(GELDBEUTEL), text="1 · Was du behältst, zählt")),
    ("s119", "s120", "split", dict(icon=ICON(TREPPE), text="2 · Kleine Beträge, riesige Summen", sub="150 + 150 + 100 € im Monat", sub_at=st("s120") - st("s119"))),
    ("s121", "s121", "split", dict(icon=ICON(AUTO_PFEIL, 700, 700), text="3 · Zahl dich zuerst")),
    ("s122", "s123", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="4 · Notgroschen schützt", sub="sonst wird die Waschmaschine zum Kredit", sub_at=st("s123") - st("s122"))),
    ("s124", "s126", "split", dict(icon=ICON(UHR), text="5 · Zeit ist dein Verbündeter", farbe=GRUEN, sub="schon 50–100 € im Monat zählen", sub_at=st("s126") - st("s124"))),
    ("s127", "s128", "split", dict(icon=doppel(LEON, FELIX), text="Leon oder Felix?", sub="Schreib's in die Kommentare!", sub_at=st("s128") - st("s127"))),
    ("s129", "s129", "split", dict(icon=ICON(TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s130", "s130", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
