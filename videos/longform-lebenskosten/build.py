#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): So viel Geld brauchst du wirklich zum Leben."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import (AUTO, AUTO_PFEIL, BANK, BLASE, DAUMEN, FLUG, GELDBEUTEL, HANDY, HAUS, HERZ, ICON, KIND, KURVE, PLAY,  # noqa: E402
                   RECHNER, SCHILD, SCHOCK, STAPEL, STERN, STROM, TASCHE, TEILEN, TICKET, TV, WAGEN, WARN, WASCH, ZETTEL,
                   doppel, folgen, gruppe, person)
from lf_szenen import Zeit, balken3, beleg, karte  # noqa: E402

Z = Zeit(HERE)
st = Z.st

KIND_P = person("#3d7be0", "#8a5a2b")
MAX = person("#3d7be0", "#353a3d")
LISA = person(ORANGE, "#8a5a2b")
TOM = person(GRUEN, "#353a3d")

SINGLE = gruppe((MAX, 1.3), w=260, h=360)
PAAR = gruppe((LISA, 1), (TOM, 1), w=260, h=360)
FAMILIE = gruppe((TOM, 1), (LISA, 1), (KIND_P, 0.62), (person(ORANGE, "#f2c418"), 0.62), w=200, h=300)


# ---------- Sonder-Szenen ----------
def intro():
    html = ('<div class="mitte" style="flex-direction:row;gap:70px">'
            f'<div id="in-b" style="width:460px;height:460px">{GELDBEUTEL}</div>'
            '<div style="text-align:left"><div id="in-t1" class="serif" style="font-size:118px;line-height:1.05;color:#111">Wie viel Geld<br />brauchst du</div>'
            '<div id="in-t2" style="display:inline-block;margin-top:26px;padding:12px 40px;border-radius:26px;background:var(--brand);color:#fff;font-weight:800;font-size:76px">wirklich zum Leben?</div></div></div>')

    def js(t0, d):
        return "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-b", "in-t1", "in-t2"))
    return dict(html=html, js=js)


def drei():
    teile = [("s9", SINGLE, "Single"), ("s10", PAAR, "Paar"), ("s11", FAMILIE, "Familie")]
    cols = "".join(f'<div id="dr-{i}" style="display:flex;flex-direction:column;align-items:center;gap:20px;width:520px">'
                   f'<div style="height:380px;display:flex;align-items:flex-end">{g}</div>'
                   f'<div style="padding:12px 40px;border-radius:40px;background:var(--brand);color:#fff;font-weight:800;font-size:58px">{n}</div></div>'
                   for i, (_, g, n) in enumerate(teile))
    html = f'<div class="mitte" style="flex-direction:row;gap:40px">{cols}</div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#dr-{i}", {st(s) if i else t0});' for i, (s, _, _) in enumerate(teile)))


def torte():
    """Miete ≈ Hälfte der Ausgaben (750 von 1.508 €)."""
    html = ('<div class="mitte" style="flex-direction:row;gap:100px">'
            '<div id="to-k" style="width:520px;height:520px">' + svg(
                '<circle cx="50" cy="50" r="46" fill="#e8e1d6" />'
                '<path d="M50 50 L50 4 A46 46 0 0 1 50.5 96 Z" fill="#DB8622" transform="rotate(0 50 50)" />'
                '<text x="72" y="56" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="12" fill="#fff">Miete</text>') + '</div>'
            '<div style="text-align:left"><div id="to-t" class="serif" style="font-size:110px;line-height:1.05;color:#111">Miete ≈<br /><span style="color:#DB8622">die Hälfte</span></div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#to-k", {t0}); pop("#to-t", {t0} + 0.3);')


def tipp(nr, titel):
    return karte(f"Tipp {nr}", titel, GRUEN, uid=f"tp{nr}")


KAPITEL = {"k1": "Einstieg", "k2": "1 · Single", "k3": "2 · Paar", "k4": "3 · Familie", "k5": "Fazit & Spartipps"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s1", "frei", intro()),
    ("s2", "s2", "split", dict(icon=ICON(TASCHE), text="Normal & entspannt leben")),
    ("s3", "s4", "split", dict(icon=ICON(GELDBEUTEL), text="Wo ist das Geld hin?", farbe=ROT)),
    ("s5", "s5", "split", dict(icon=ICON(WARN), text="Ohne Zahl kein Plan", farbe=ROT)),
    ("s6", "s7", "split", dict(icon=ICON(RECHNER), text="Wir rechnen alles durch", sub="ehrlich & mit echten Zahlen", sub_at=st("s7") - st("s6"))),
    ("s8", "s11", "frei", drei()),
    ("s12", "s12", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="Mehr übrig behalten", farbe=GRUEN)),
    ("s13", "s15", "split", dict(icon=ICON(HAUS), text="Mittelgroße Stadt", sub='München, Hamburg: <span style="color:#e24b4b">teurer</span><br />Land: <span style="color:#1f7a4d">günstiger</span>', sub_at=st("s14") - st("s13"))),
    ("s16", "s17", "split", dict(icon=ICON(SCHOCK), text="Überraschende Ergebnisse")),
    ("s18", "s20", "split", dict(icon=ICON(BLASE), text="Wie viel brauchst du im Monat?", sub="Schreib deine Zahl in die Kommentare!", sub_at=st("s20") - st("s18"))),
    ("s21", "s22", "frei", folgen()),
    ("s23", "s23", "kapitel", dict(titel='<span style="color:#DB8622">Los geht\'s!</span>')),
    # ---- Single ----
    ("s24", "s24", "frei", karte("Situation 1", "Single", uid="k1")),
    ("s25", "s48", "frei", beleg(Z, "mx", "Max · pro Monat", SINGLE, [
        ("s27", "s28", ICON(HAUS), "Warmmiete", 750),
        ("s29", "s30", doppel(STROM, HANDY), "Strom, Internet, Handy", 100),
        ("s31", "s32", ICON(WAGEN), "Essen", 300),
        ("s33", "s35", ICON(TICKET), "Deutschlandticket", 60),
        ("s37", "s39", ICON(SCHILD), "Versicherungen", 50),
        ("s40", "s40", ICON(TV), "Rundfunkbeitrag", 18),
        ("s41", "s42", ICON(PLAY), "Abos", 30),
        ("s44", "s46", ICON(TASCHE), "Freizeit & Kleidung", 200),
    ], "s48", "≈ 1.500 €")),
    ("s49", "s50", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="+ 10 % sparen", farbe=GRUEN)),
    ("s51", "s51", "zahl", dict(zahl="≈ 1.700 €", sub="netto im Monat", farbe=GRUEN)),
    ("s52", "s53", "split", dict(icon=ICON(ZETTEL), text="Netto ≈ 1.700 €", sub="Brutto: grob 2.500 €", sub_at=st("s53") - st("s52"), farbe=GRUEN)),
    ("s54", "s54", "split", dict(icon=ICON(CHECK), text="Ein ganz normales Gehalt", farbe=GRUEN)),
    ("s55", "s55", "frei", torte()),
    # ---- Paar ----
    ("s56", "s56", "frei", karte("Situation 2", "Paar", uid="k2")),
    ("s57", "s68", "frei", beleg(Z, "pa", "Lisa & Tom · pro Monat", PAAR, [
        ("s58", "s58", ICON(HAUS), "Warmmiete", 1100),
        ("s59", "s59", doppel(STROM, HANDY), "Strom, Internet, Handys", 150),
        ("s60", "s60", ICON(WAGEN), "Essen", 550),
        ("s61", "s62", doppel(AUTO, TICKET), "Auto & Ticket", 400),
        ("s63", "s63", ICON(SCHILD), "Versicherungen", 90),
        ("s64", "s65", ICON(TV), "Rundfunkbeitrag", 18),
        ("s66", "s66", ICON(PLAY), "Abos", 40),
        ("s67", "s67", ICON(TASCHE), "Freizeit & Kleidung", 350),
    ], "s68", "≈ 2.700 €")),
    ("s69", "s69", "split", dict(icon=ICON(SCHOCK), text="Jetzt wird's spannend …")),
    ("s70", "s71", "frei", balken3(Z, "pp", [("Max allein", "1.500 €", 420, ROT, None), ("pro Person", "1.350 €", 370, GRUEN, "s70")])),
    ("s72", "s73", "split", dict(icon=PAAR, text="Warum?", sub="Miete, Internet, Rundfunk & Auto teilen sich auf 2 Köpfe", sub_at=st("s73") - st("s72"))),
    ("s74", "s74", "split", dict(icon=ICON(HERZ), text="Romantisch & clever", farbe=GRUEN)),
    ("s75", "s75", "zahl", dict(zahl="≈ 3.000 €", sub="netto – mit 10 % Sparrate", farbe=GRUEN)),
    ("s76", "s76", "split", dict(icon=ICON(STAPEL), text="Hier bleibt was übrig", farbe=GOLD)),
    ("s77", "s77", "split", dict(icon=ICON(KURVE), text="Jetzt sparen & investieren", farbe=GRUEN)),
    ("s78", "s78", "split", dict(icon=ICON(WARN), text="Mit Kindern wird's enger", farbe=ROT)),
    # ---- Familie ----
    ("s79", "s79", "frei", karte("Situation 3", "Familie", uid="k3")),
    ("s80", "s95", "frei", beleg(Z, "fa", "Familie Becker · pro Monat", FAMILIE, [
        ("s81", "s82", ICON(HAUS), "Warmmiete", 1500),
        ("s83", "s83", doppel(STROM, WASCH), "Strom, Internet, Handys", 200),
        ("s84", "s85", ICON(WAGEN), "Essen", 900),
        ("s86", "s87", ICON(AUTO), "Auto & Bus", 450),
        ("s88", "s88", ICON(SCHILD), "Versicherungen", 130),
        ("s89", "s89", doppel(TV, PLAY), "Rundfunk & Abos", 60),
        ("s90", "s92", ICON(KIND), "Kinder", 400),
        ("s93", "s94", ICON(FLUG), "Freizeit & Urlaub", 300),
    ], "s95", "≈ 4.000 €")),
    ("s96", "s97", "zahl", dict(zahl="fast 4.000 €", sub="jeden Monat", farbe=ROT)),
    ("s98", "s99", "split", dict(icon=ICON(BANK), text="+ über 500 € Kindergeld", farbe=GRUEN)),
    ("s100", "s100", "zahl", dict(zahl="≈ 3.500 €", sub="netto selbst verdienen")),
    ("s101", "s101", "split", dict(icon=doppel(SPARSCHWEIN, CROSS), text="Noch kein Cent gespart", farbe=ROT)),
    ("s102", "s102", "split", dict(icon=ICON(GELDBEUTEL), text="Reicht gerade so …")),
    ("s103", "s104", "chips", dict(titel="Und dann …", chips=[("Waschmaschine kaputt", ROT, False), ("Autoreparatur", ROT, False), ("Nebenkosten-Nachzahlung", ROT, False)])),
    ("s105", "s105", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="Notgroschen!", farbe=GRUEN)),
    # ---- Fazit & Tipps ----
    ("s106", "s106", "kapitel", dict(titel="Zusammengefasst")),
    ("s107", "s110", "frei", balken3(Z, "zf", [("Single", "1.500 €", 220, "#3d7be0", "s107"), ("Paar", "2.700 €", 400, GRUEN, "s108"), ("Familie", "4.000 €", 590, ORANGE, "s109")], "ohne Sparen", "s110")),
    ("s111", "s112", "split", dict(icon=ICON(STERN), text="5 Tipps: mehr Geld übrig", farbe=GRUEN)),
    ("s113", "s113", "frei", tipp(1, "Miete")),
    ("s114", "s114", "zahl", dict(zahl="max. ⅓", sub="deines Nettos für die Warmmiete")),
    ("s115", "s115", "zahl", dict(zahl="12.000 €", sub="100 € weniger Miete × 10 Jahre", farbe=GOLD)),
    ("s116", "s116", "frei", tipp(2, "Verträge prüfen")),
    ("s117", "s117", "chips", dict(chips=[("Handy", "#3d7be0", False), ("Internet", "#9b59b6", False), ("Strom", "#c99a06", False), ("Versicherungen", GRUEN, False)])),
    ("s118", "s118", "zahl", dict(zahl="+50 €", sub="mehr im Monat", farbe=GRUEN)),
    ("s119", "s119", "frei", tipp(3, "Auto durchrechnen")),
    ("s120", "s121", "split", dict(icon=ICON(AUTO), text="Oft 300 €+ im Monat", farbe=ROT)),
    ("s122", "s122", "chips", dict(chips=[("Wertverlust", ROT, False), ("Versicherung", ROT, False), ("Steuer", ROT, False), ("Reparaturen", ROT, False)])),
    ("s123", "s123", "split", dict(icon=doppel(AUTO, TICKET), text="Auto oder D-Ticket?")),
    ("s124", "s124", "frei", tipp(4, "Wochenbudget Essen")),
    ("s125", "s125", "split", dict(icon=ICON(WAGEN), text="+100 € im Monat", farbe=GRUEN)),
    ("s126", "s126", "frei", tipp(5, "Zuerst sparen")),
    ("s127", "s127", "split", dict(icon=ICON(AUTO_PFEIL, 700, 700), text="Dauerauftrag am Gehaltstag")),
    ("s128", "s128", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="Aus den Augen, aus dem Sinn")),
    ("s129", "s129", "zahl", dict(zahl="+200–300 €", sub="mehr im Monat", farbe=GRUEN)),
    ("s130", "s130", "split", dict(icon=ICON(KURVE), text="Angelegt: große Summen", farbe=GRUEN)),
    ("s131", "s132", "split", dict(icon=ICON(BLASE), text="Und deine Zahl?", sub="Drüber oder drunter?", sub_at=st("s132") - st("s131"))),
    ("s133", "s133", "split", dict(icon=doppel(DAUMEN, TEILEN), text="Like & teilen!", farbe=ORANGE)),
    ("s134", "s134", "frei", folgen("Bis zum nächsten Video!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
