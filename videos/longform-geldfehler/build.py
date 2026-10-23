#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): 10 Geldfehler, die dich arm halten (Countdown). Beagle nur im CTA."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import (AUTO, BANK, BLASE, GELDBEUTEL, HANDY, ICON, KAL3, KURVE, NOTIZ, PLAY, RECHNER, SCHILD, STAPEL,  # noqa: E402
                   STERN, TEILEN, UHR, WARN, ZETTEL, folgen)
from lf_szenen import Zeit, balken3, beleg, chips_zeit  # noqa: E402

Z = Zeit(HERE)
st = Z.st

# ---------- Icons ----------
KAFFEE = svg('<path d="M24 30 L76 30 L70 92 L30 92 Z" fill="#fff" stroke="#353a3d" stroke-width="4" stroke-linejoin="round" /><rect x="20" y="20" width="60" height="12" rx="4" fill="#8a5a2b" />'
             '<rect x="28" y="50" width="44" height="22" fill="#DB8622" /><path d="M42 14 Q38 6 44 2 M56 14 Q52 6 58 2" fill="none" stroke="#9aa3a8" stroke-width="3" stroke-linecap="round" />')
THERMOS = svg('<rect x="32" y="16" width="36" height="78" rx="12" fill="#1f7a4d" /><rect x="36" y="6" width="28" height="14" rx="4" fill="#353a3d" /><rect x="32" y="44" width="36" height="12" fill="#2c9a63" />'
              '<path d="M68 30 Q86 34 84 52 Q82 64 68 62" fill="none" stroke="#353a3d" stroke-width="5" />')
KARTE = svg('<rect x="6" y="22" width="88" height="56" rx="8" fill="#353a3d" /><rect x="6" y="34" width="88" height="10" fill="#111" /><rect x="16" y="52" width="16" height="12" rx="2" fill="#f2c418" />'
            '<text x="84" y="70" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="13" fill="#e24b4b">−2.000 €</text>')
PIZZA = svg('<circle cx="50" cy="50" r="44" fill="#f2c418" stroke="#c99a06" stroke-width="6" /><circle cx="50" cy="50" r="36" fill="#e24b4b" opacity="0.85" />' + "".join(
    f'<circle cx="{x}" cy="{y}" r="6" fill="#a8321f" />' for x, y in [(38, 36), (62, 40), (46, 62), (66, 62), (30, 56)]) +
    '<path d="M50 50 L50 6" stroke="#c99a06" stroke-width="3" /><path d="M50 50 L88 70" stroke="#c99a06" stroke-width="3" />')
TOPF = svg('<rect x="14" y="40" width="72" height="46" rx="10" fill="#9aa3a8" /><rect x="8" y="34" width="84" height="10" rx="5" fill="#555c60" /><rect x="42" y="26" width="16" height="8" rx="3" fill="#555c60" />'
           '<rect x="2" y="50" width="12" height="8" rx="3" fill="#555c60" /><rect x="86" y="50" width="12" height="8" rx="3" fill="#555c60" /><text x="50" y="72" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="16" fill="#fff">×2</text>')


def intro():
    html = ('<div class="mitte" style="flex-direction:row;gap:70px">'
            f'<div id="in-b" style="width:440px;height:440px">{GELDBEUTEL}</div>'
            '<div style="text-align:left"><div id="in-t1" class="serif" style="font-size:170px;line-height:1;color:#e24b4b">10 Geldfehler</div>'
            '<div id="in-t2" style="font-weight:800;font-size:76px;color:#111;margin-top:24px">die dich arm halten</div></div></div>')

    def js(t0, d):
        return "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-b", "in-t1", "in-t2"))
    return dict(html=html, js=js)


def platz(nr, titel):
    """Countdown-Karte: große Platz-Nummer im Kreis + Fehler."""
    farbe = GOLD if nr == 1 else ROT
    html = (f'<div class="mitte" style="flex-direction:row;gap:80px">'
            f'<div id="pl{nr}-n" style="width:380px;height:380px;border-radius:50%;background:{farbe};display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
            f'<div style="font-weight:800;font-size:54px;margin-bottom:-20px">Platz</div><div class="serif" style="font-size:200px;line-height:1">{nr}</div></div>'
            f'<div id="pl{nr}-t" class="serif" style="font-size:120px;line-height:1.05;color:#111;max-width:1000px">{titel}</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#pl{nr}-n", {t0}); tl.fromTo("#pl{nr}-t", {{ x: 60, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {t0} + 0.2);')


def kosten(betrag, sub="pro Jahr", farbe=ROT):
    return dict(zahl=betrag, sub=sub, farbe=farbe)


KAPITEL = {"k1": "Einstieg", "k2": "Platz 10 – 8", "k3": "Platz 7 – 5", "k4": "Platz 4 – 2", "k5": "Platz 1 & Fazit"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s1", "frei", intro()),
    ("s2", "s2", "split", dict(icon=KAL3, text="Leise. Automatisch. Jeden Monat.")),
    ("s3", "s3", "zahl", dict(zahl="3 von 10", sub="macht fast jeder", farbe=ROT)),
    ("s4", "s6", "split", dict(icon=ICON(ZETTEL), text="Nicht dein Gehalt entscheidet …", sub="… sondern deine Fehler", sub_at=st("s5") - st("s4"))),
    ("s7", "s8", "zahl", dict(zahl="10 → 1", sub="vom kleinsten zum teuersten Fehler")),
    ("s9", "s10", "split", dict(icon=ICON(RECHNER), text="Was kostet das pro Jahr?", sub="+ die große Summe am Ende", sub_at=st("s10") - st("s9"))),
    ("s11", "s11", "split", dict(icon=ICON(WARN), text="Fehler Nr. 7 macht fast jeder", farbe=ROT)),
    ("s12", "s12", "split", dict(icon=ICON(STERN), text="Platz 1: sechsstellig!", farbe=GOLD)),
    ("s13", "s15", "split", dict(icon=ICON(BLASE), text="Welcher Fehler ist der teuerste?", sub="Dein Tipp in die Kommentare!", sub_at=st("s15") - st("s13"))),
    ("s16", "s17", "frei", folgen("+ Folgen")),
    ("s18", "s18", "kapitel", dict(titel='<span style="color:#DB8622">Los geht\'s!</span>')),
    # ---- Platz 10 – 8 ----
    ("s19", "s19", "frei", platz(10, "Ungenutzte Abos")),
    ("s20", "s21", "chips", dict(chips=[("Streaming", "#9b59b6", False), ("Musik", GRUEN, False), ("Fitnessstudio", "#3d7be0", False), ("Apps", ORANGE, False)])),
    ("s22", "s22", "zahl", kosten("30 €", "pro Monat")),
    ("s23", "s23", "zahl", kosten("360 €", "pro Jahr – einfach weg")),
    ("s24", "s24", "split", dict(icon=ICON(NOTIZ), text="Kontoauszüge checken & kündigen", farbe=GRUEN)),
    ("s25", "s25", "frei", platz(9, "Teures Girokonto")),
    ("s26", "s26", "split", dict(icon=ICON(BANK), text="Gebühren für Konto, Karte & Abheben", farbe=ROT)),
    ("s27", "s27", "zahl", kosten("120 €")),
    ("s28", "s30", "split", dict(icon=ICON(BANK), text="Kostenlose Konten gibt's noch", farbe=GRUEN, sub="Wechsel in Minuten – Bedingungen prüfen!", sub_at=st("s29") - st("s28"))),
    ("s31", "s31", "frei", platz(8, "Coffee to go")),
    ("s32", "s33", "split", dict(icon=ICON(KAFFEE), text="3 € pro Arbeitstag")),
    ("s34", "s34", "zahl", kosten("720 €")),
    ("s35", "s35", "zahl", kosten("7.000 €+", "in 10 Jahren")),
    ("s36", "s37", "split", dict(icon=ICON(THERMOS), text="Thermoskanne von zu Hause", farbe=GRUEN)),
    # ---- Platz 7 – 5 ----
    ("s38", "s38", "frei", platz(7, "Verträge nie vergleichen")),
    ("s39", "s40", "chips", dict(chips=[("Strom", "#c99a06", False), ("Gas", "#3d7be0", False), ("Handy", "#353a3d", False), ("Internet", "#9b59b6", False), ("Versicherungen", GRUEN, False)])),
    ("s41", "s42", "frei", chips_zeit(Z, "nk", "Der Trick der Anbieter", [("Neukunden: günstig", GRUEN, None), ("Treue Kunden: teuer", ROT, "s42")])),
    ("s43", "s43", "zahl", kosten("400 €", "pro Jahr zu viel")),
    ("s44", "s45", "split", dict(icon=ICON(UHR), text="1 Stunde pro Jahr", sub="vergleichen, wechseln, verhandeln", sub_at=st("s45") - st("s44"))),
    ("s46", "s46", "zahl", kosten("400 €/Std.", "dein bester Stundenlohn", GRUEN)),
    ("s47", "s47", "frei", platz(6, "Leben im Dispo")),
    ("s48", "s48", "split", dict(icon=ICON(KARTE), text="Fühlt sich an wie eigenes Geld …", sub='<span style="color:#e24b4b">… ist aber ein teurer Kredit</span>', sub_at=1.4)),
    ("s49", "s49", "zahl", kosten("11 %+", "Dispozinsen")),
    ("s50", "s51", "zahl", kosten("220 €", "pro Jahr – nur Zinsen")),
    ("s52", "s53", "split", dict(icon=KAL3, text="Fester Betrag zurück – jeden Monat", farbe=GRUEN)),
    ("s54", "s54", "frei", platz(5, "Kaufen auf Raten")),
    ("s55", "s55", "chips", dict(chips=[("Handy", "#353a3d", False), ("Fernseher", "#3d7be0", False), ("Sofa", ORANGE, False)])),
    ("s56", "s58", "split", dict(icon=ICON(WARN), text="Geld, das du noch nicht hast", farbe=ROT, sub="versteckte Zinsen & Gebühren", sub_at=st("s57") - st("s56"))),
    ("s59", "s59", "zahl", kosten("250 €")),
    ("s60", "s60", "split", dict(icon=ICON(STAPEL), text="Nicht bar leistbar? Nicht leisten!", farbe=GRUEN)),
    # ---- Platz 4 – 2 ----
    ("s61", "s61", "kapitel", dict(titel='Die <span style="color:#e24b4b">Top 4</span>')),
    ("s62", "s62", "frei", platz(4, "Lieferdienst")),
    ("s63", "s63", "split", dict(icon=ICON(PIZZA), text="So bequem …")),
    ("s64", "s66", "frei", balken3(Z, "lf", [("bestellt", "25 €", 460, ROT, "s64"), ("selbst gekocht", "8 €", 150, GRUEN, "s65")])),
    ("s67", "s67", "zahl", kosten("1.700 €", "pro Jahr mehr")),
    ("s68", "s68", "split", dict(icon=ICON(TOPF), text="Sonntags doppelt kochen", farbe=GRUEN)),
    ("s69", "s69", "frei", platz(3, "Geld auf dem Girokonto")),
    ("s70", "s70", "split", dict(icon=ICON(BANK), text="10.000 € → 0 % Zinsen", farbe=ROT)),
    ("s71", "s72", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="Tagesgeld: rund 2 %", farbe=GRUEN, sub="= 200 € pro Jahr geschenkt", sub_at=st("s72") - st("s71"))),
    ("s73", "s74", "split", dict(icon=ICON(SCHILD), text="Sicher & täglich verfügbar", sub="perfekt für den Notgroschen", sub_at=st("s74") - st("s73"))),
    ("s75", "s75", "frei", platz(2, "Zu viel Auto")),
    ("s76", "s77", "frei", balken3(Z, "au", [("Neuwagen", "30.000 €", 500, "#3d7be0", None), ("nach 3 Jahren", "15.000 €", 250, ROT, "s77")])),
    ("s78", "s78", "split", dict(icon=ICON(AUTO), text="Passt nicht zum Gehalt", farbe=ROT)),
    ("s79", "s79", "zahl", kosten("150 €", "pro Monat weniger mit einem Gebrauchten", GRUEN)),
    ("s80", "s80", "zahl", kosten("1.800 €", "pro Jahr", GRUEN)),
    ("s81", "s81", "split", dict(icon=ICON(STERN), text="Mehr Freiheit", farbe=GRUEN)),
    # ---- Platz 1 & Fazit ----
    ("s82", "s82", "frei", platz(1, "Nicht investieren")),
    ("s83", "s84", "split", dict(icon=ICON(KURVE), text="… oder zu spät anfangen", sub="„zu kompliziert, zu riskant …“", sub_at=st("s84") - st("s83"))),
    ("s85", "s85", "split", dict(icon=ICON(RECHNER), text="Die Rechnung")),
    ("s86", "s88", "frei", balken3(Z, "et", [("eingezahlt", "72.000 €", 170, GRUEN, "s86"), ("nach 30 Jahren", "≈ 250.000 €", 600, GOLD, "s87")], "keine Garantie", "s88")),
    ("s89", "s91", "frei", balken3(Z, "wa", [("10 Jahre später", "104.000 €", 250, ROT, "s90"), ("heute starten", "250.000 €", 600, GOLD, None)], "−140.000 € fürs Warten", "s91")),
    ("s92", "s92", "split", dict(icon=ICON(UHR), text="Zeit ist dein wichtigster Faktor", farbe=GRUEN)),
    ("s93", "s103", "frei", beleg(Z, "su", "Fehler 10 – 2 · pro Jahr", ICON(RECHNER), [
        ("s94", "s94", ICON(PLAY), "Abos", 360),
        ("s95", "s95", ICON(BANK), "Girokonto", 120),
        ("s96", "s96", ICON(KAFFEE), "Coffee to go", 720),
        ("s97", "s97", ICON(ZETTEL), "Verträge", 400),
        ("s98", "s98", ICON(KARTE), "Dispo", 220),
        ("s99", "s99", ICON(HANDY), "Ratenkäufe", 250),
        ("s100", "s100", ICON(PIZZA), "Lieferdienst", 1700),
        ("s101", "s101", ICON(SPARSCHWEIN, 640, 555), "Tagesgeld verschenkt", 200),
        ("s102", "s102", ICON(AUTO), "Zu viel Auto", 1800),
    ], "s103", "≈ 5.800 €", fs=32)),
    ("s104", "s104", "zahl", kosten("58.000 €", "in 10 Jahren")),
    ("s105", "s105", "split", dict(icon=ICON(GELDBEUTEL), text="Nicht mehr verdienen – weniger verschwenden", farbe=GRUEN)),
    ("s106", "s107", "split", dict(icon=ICON(WARN), text="Schon 3–4 Fehler kosten Tausende", farbe=ROT)),
    ("s108", "s110", "frei", chips_zeit(Z, "pl", "Dein Plan", [("1 Fehler aussuchen", ORANGE, "s108"), ("Verträge & Abos zuerst", ORANGE, "s109"), ("Ersparnis → Sparplan", GRUEN, "s110")])),
    ("s111", "s112", "split", dict(icon=ICON(BLASE), text="Lagst du richtig?", sub="Welchen Fehler gehst du zuerst an?", sub_at=st("s112") - st("s111"))),
    ("s113", "s113", "split", dict(icon=ICON(TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s114", "s114", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
