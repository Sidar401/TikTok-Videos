#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): So viel kostet ein Hund wirklich – vom Welpen bis ins Alter."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import (AUTO, HUND_NEUTRAL, BLASE, DAUMEN, FLUG, HERZ, ICON, KAL3, RECHNER, SCHILD, SCHOCK, STERN, TEILEN, WARN,  # noqa: E402
                   doppel, folgen)
from lf_szenen import Zeit, balken3, beleg, chips_zeit, karte  # noqa: E402

Z = Zeit(HERE)
st = Z.st

# ---------- Hunde-Icons (viewBox 0 0 100 100) ----------
EISBERG = svg('<rect x="0" y="40" width="100" height="60" fill="#cfe6f5" /><path d="M38 40 L50 14 L62 40 Z" fill="#fff" stroke="#353a3d" stroke-width="3" stroke-linejoin="round" />'
              '<path d="M38 40 L62 40 L84 92 L14 92 Z" fill="#9ed0f0" stroke="#3d7be0" stroke-width="3" stroke-linejoin="round" /><line x1="0" y1="40" x2="100" y2="40" stroke="#3d7be0" stroke-width="3" />'
              '<text x="50" y="72" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="13" fill="#e24b4b">€€€</text>')
TIERHEIM = svg('<path d="M8 48 L50 10 L92 48" fill="none" stroke="#353a3d" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /><path d="M18 44 L18 92 L82 92 L82 44 L50 16 Z" fill="#1f7a4d" />'
               '<path d="M50 80 Q32 66 36 56 Q40 48 50 56 Q60 48 64 56 Q68 66 50 80 Z" fill="#fff" />')
INTERNET = svg('<rect x="6" y="10" width="88" height="62" rx="8" fill="#353a3d" /><rect x="12" y="16" width="76" height="50" rx="3" fill="#fff" /><text x="50" y="48" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="16" fill="#e24b4b">99 €!?</text>'
               '<rect x="36" y="76" width="28" height="8" fill="#353a3d" /><rect x="24" y="84" width="52" height="6" rx="3" fill="#353a3d" />')
LEINE = svg('<circle cx="30" cy="30" r="20" fill="none" stroke="#e24b4b" stroke-width="9" /><path d="M46 42 Q70 60 60 90" fill="none" stroke="#DB8622" stroke-width="7" stroke-linecap="round" /><circle cx="60" cy="90" r="6" fill="#353a3d" />'
            '<rect x="56" y="10" width="34" height="22" rx="6" fill="#3d7be0" /><circle cx="73" cy="21" r="5" fill="#f2c418" />')
SPRITZE = svg('<g transform="rotate(-40 50 50)"><rect x="40" y="18" width="20" height="54" rx="4" fill="#cfe6f5" stroke="#353a3d" stroke-width="4" /><rect x="40" y="44" width="20" height="28" fill="#3d7be0" opacity="0.6" />'
              '<rect x="46" y="6" width="8" height="14" fill="#353a3d" /><rect x="36" y="4" width="28" height="6" rx="3" fill="#353a3d" /><line x1="50" y1="72" x2="50" y2="96" stroke="#353a3d" stroke-width="3" /></g>')
TIERARZT = svg('<circle cx="50" cy="50" r="44" fill="#fff" stroke="#e24b4b" stroke-width="6" /><rect x="40" y="20" width="20" height="60" rx="4" fill="#e24b4b" /><rect x="20" y="40" width="60" height="20" rx="4" fill="#e24b4b" />')
SCHULE = svg('<path d="M4 38 L50 18 L96 38 L50 58 Z" fill="#353a3d" /><path d="M24 48 L24 70 Q50 84 76 70 L76 48 L50 58 Z" fill="#555c60" /><line x1="88" y1="42" x2="88" y2="72" stroke="#f2c418" stroke-width="4" /><circle cx="88" cy="74" r="5" fill="#f2c418" />')
NAPF = svg('<path d="M10 56 L90 56 L80 88 L20 88 Z" fill="#DB8622" /><ellipse cx="50" cy="56" rx="40" ry="10" fill="#a8621a" />' + "".join(
    f'<circle cx="{x}" cy="{y}" r="7" fill="#8a5a2b" />' for x, y in [(34, 50), (46, 46), (58, 48), (68, 52), (40, 54), (54, 54)]) +
    '<path d="M44 76 Q50 70 56 76 Q50 82 44 76 Z" fill="#fff" opacity="0.6" />')
KNOCHEN = svg('<g transform="rotate(-30 50 50)"><rect x="24" y="42" width="52" height="16" rx="6" fill="#f6efe1" stroke="#353a3d" stroke-width="3" />' + "".join(
    f'<circle cx="{x}" cy="{y}" r="11" fill="#f6efe1" stroke="#353a3d" stroke-width="3" />' for x, y in [(20, 40), (20, 60), (80, 40), (80, 60)]) + '</g>')
STEUER = svg('<rect x="16" y="6" width="68" height="88" rx="6" fill="#fff" stroke="#353a3d" stroke-width="4" /><text x="50" y="34" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="13" fill="#111">Steuer</text>'
             '<rect x="28" y="44" width="44" height="5" rx="2" fill="#ccc" /><rect x="28" y="54" width="34" height="5" rx="2" fill="#ccc" /><text x="50" y="84" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="16" fill="#e24b4b">Hund</text>')
SCHERE = svg('<circle cx="28" cy="74" r="12" fill="none" stroke="#353a3d" stroke-width="6" /><circle cx="72" cy="74" r="12" fill="none" stroke="#353a3d" stroke-width="6" />'
             '<path d="M36 64 L70 8 M64 64 L30 8" stroke="#9aa3a8" stroke-width="7" stroke-linecap="round" />')
PFLASTER = svg('<g transform="rotate(-35 50 50)"><rect x="8" y="34" width="84" height="32" rx="16" fill="#f1c9a5" stroke="#a8743f" stroke-width="3" /><rect x="36" y="34" width="28" height="32" fill="#f6efe1" />'
               '<circle cx="44" cy="44" r="2" fill="#a8743f" /><circle cx="56" cy="44" r="2" fill="#a8743f" /><circle cx="44" cy="56" r="2" fill="#a8743f" /><circle cx="56" cy="56" r="2" fill="#a8743f" /></g>')
HUNDEHAUS = svg('<path d="M10 46 L50 12 L90 46" fill="#e24b4b" /><rect x="18" y="44" width="64" height="48" fill="#DB8622" /><path d="M36 92 L36 66 Q50 52 64 66 L64 92 Z" fill="#353a3d" />'
                '<text x="50" y="40" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="10" fill="#fff">PENSION</text>')
PILLE = svg('<g transform="rotate(-35 50 50)"><rect x="14" y="36" width="72" height="28" rx="14" fill="#fff" stroke="#353a3d" stroke-width="4" /><path d="M50 36 L36 36 Q14 36 14 50 Q14 64 36 64 L50 64 Z" fill="#3d7be0" /></g>')
HUND = ICON(HUND_NEUTRAL, 560, 560)


def intro():
    html = ('<div class="mitte" style="gap:40px">'
            f'<div style="display:flex;align-items:center;gap:60px"><div id="in-h" style="width:340px;height:340px">{HUND_NEUTRAL}</div>'
            '<div id="in-g" class="serif" style="font-size:200px;color:#DB8622">=</div>'
            f'<div id="in-a" style="width:360px;height:360px">{AUTO}</div></div>'
            '<div id="in-t" class="serif" style="font-size:84px;line-height:1.1;color:#111;text-align:center">Ein Hund kostet so viel<br />wie ein <span style="color:#e24b4b">Kleinwagen?</span></div></div>')

    def js(t0, d):
        return "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-h", "in-g", "in-a", "in-t"))
    return dict(html=html, js=js)


def ueber(nr, titel):
    return karte(f"Überraschung {nr}", titel, ROT, uid=f"ub{nr}")


def tipp(nr, titel):
    return karte(f"Tipp {nr}", titel, GRUEN, uid=f"tp{nr}")


KAPITEL = {"k1": "Einstieg", "k2": "1 · Anschaffung", "k3": "2 · Laufende Kosten", "k4": "3 · Überraschungen", "k5": "Gesamtrechnung & Tipps"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s1", "frei", intro()),
    ("s2", "s2", "split", dict(icon=ICON(SCHOCK), text="Klingt übertrieben?")),
    ("s3", "s3", "split", dict(icon=ICON(RECHNER), text="Wir rechnen ehrlich nach")),
    ("s4", "s5", "split", dict(icon=ICON(EISBERG), text="Kaufpreis + Futter?", sub="Nur die Spitze des Eisbergs!", sub_at=st("s5") - st("s4"))),
    ("s6", "s7", "chips", dict(chips=[("Hundesteuer", "#353a3d", False), ("Versicherungen", GRUEN, False), ("Tierarzt", ROT, False), ("Urlaub", "#3d7be0", False), ("Notfälle", ORANGE, False)])),
    ("s8", "s11", "frei", chips_zeit(Z, "ch", "Das ganze Hundeleben", [("1 Anschaffung", ORANGE, "s9"), ("2 Laufende Kosten", ORANGE, "s10"), ("3 Überraschungen", ROT, "s11")])),
    ("s12", "s12", "split", dict(icon=ICON(STERN), text="Komplette Rechnung + Spartipps", farbe=GRUEN)),
    ("s13", "s14", "split", dict(icon=HUND, text="Mittelgroß, 13 Jahre", sub='klein: <span style="color:#1f7a4d">günstiger</span> · groß: <span style="color:#e24b4b">teurer</span>', sub_at=st("s14") - st("s13"))),
    ("s15", "s16", "split", dict(icon=ICON(TIERARZT), text="Überraschende Zahlen", sub="Dieses Video spart dir bares Geld", sub_at=st("s16") - st("s15"))),
    ("s17", "s18", "split", dict(icon=HUND, text="Hast du einen Hund?")),
    ("s19", "s20", "split", dict(icon=ICON(BLASE), text="Was kostet ein Hund im Leben?", sub="Schreib deine Schätzung in die Kommentare!", sub_at=st("s20") - st("s19"))),
    ("s21", "s22", "frei", folgen("+ Folgen")),
    ("s23", "s23", "kapitel", dict(titel='<span style="color:#DB8622">Los geht\'s!</span>')),
    # ---- Anschaffung ----
    ("s24", "s24", "frei", karte("Teil 1", "Anschaffung", uid="t1")),
    ("s25", "s42", "frei", beleg(Z, "an", "Start & erstes Jahr", HUND, [
        ("s25", "s26", HUND, "Welpe vom Züchter", 1500),
        ("s27", None, ICON(TIERHEIM), None, None),
        ("s29", None, doppel(INTERNET, WARN), None, None),
        ("s31", "s33", ICON(LEINE), "Erstausstattung", 300),
        ("s34", "s36", ICON(SPRITZE), "Impfungen & Chip", 200),
        ("s37", None, ICON(TIERARZT), None, None),
        ("s40", "s41", ICON(SCHULE), "Welpenschule", 200),
    ], "s42", "≈ 2.200 €")),
    ("s43", "s43", "split", dict(icon=KAL3, text="Und jetzt: jeden Monat")),
    # ---- Laufende Kosten ----
    ("s44", "s44", "frei", karte("Teil 2", "Laufende Kosten", uid="t2")),
    ("s45", "s68", "frei", beleg(Z, "lk", "Pro Monat", ICON(NAPF), [
        ("s45", "s45", ICON(NAPF), "Futter", 60),
        ("s46", "s48", ICON(KNOCHEN), "Leckerlis & Spielzeug", 20),
        ("s49", "s51", ICON(STEUER), "Hundesteuer", 10),
        ("s54", "s56", ICON(SCHILD), "Haftpflicht", 6),
        ("s57", "s59", ICON(SPRITZE), "Tierarzt (Routine)", 25),
        ("s60", None, ICON(SCHERE), None, None),
        ("s63", "s64", ICON(PFLASTER), "OP-Versicherung", 25),
    ], "s68", "≈ 150 €")),
    ("s69", "s69", "zahl", dict(zahl="1.800 €", sub="pro Jahr", farbe=ROT)),
    ("s70", "s71", "zahl", dict(zahl="23.400 €", sub="in 13 Jahren", farbe=ROT)),
    # ---- Überraschungen ----
    ("s72", "s72", "split", dict(icon=ICON(WARN), text="Was viele unterschätzen", farbe=ROT)),
    ("s73", "s73", "frei", ueber(1, "Notfall-Tierarzt")),
    ("s74", "s74", "split", dict(icon=ICON(TIERARZT), text="Tierarzt: deutlich teurer", farbe=ROT)),
    ("s75", "s75", "split", dict(icon=ICON(TIERARZT), text="Notdienst: über 100 €", farbe=ROT)),
    ("s76", "s77", "split", dict(icon=ICON(PFLASTER), text="Kreuzband, Magendrehung", sub='<span style="color:#e24b4b">2.000 – 4.000 €</span>', sub_at=Z.euro_zeit("s77") - st("s76"))),
    ("s78", "s78", "zahl", dict(zahl="≈ 3.000 €", sub="eine große OP", farbe=ROT)),
    ("s79", "s80", "split", dict(icon=ICON(SCHILD), text="Mit OP-Versicherung: kleiner Eigenanteil", farbe=GRUEN, sub='<span style="color:#e24b4b">Ohne: alles selbst zahlen</span>', sub_at=st("s80") - st("s79"))),
    ("s81", "s82", "chips", dict(titel="Kleinigkeiten", chips=[("Ohrenentzündung", ORANGE, False), ("verschluckte Socke", ORANGE, False), ("Allergie", ORANGE, False)])),
    ("s83", "s83", "zahl", dict(zahl="80 – 200 €", sub="pro Besuch", farbe=ROT)),
    ("s84", "s84", "frei", ueber(2, "Urlaub")),
    ("s85", "s86", "split", dict(icon=ICON(HUNDEHAUS), text="Hundepension", sub="20 – 40 € pro Tag", sub_at=Z.euro_zeit("s86") - st("s85"))),
    ("s87", "s87", "zahl", dict(zahl="300 €", sub="pro Jahr (2 Wochen)", farbe=ROT)),
    ("s88", "s88", "zahl", dict(zahl="≈ 4.000 €", sub="in 13 Jahren", farbe=ROT)),
    ("s89", "s90", "split", dict(icon=ICON(LEINE), text="Gassi-Service", sub="10 – 20 € pro Runde", sub_at=Z.euro_zeit("s90") - st("s89"))),
    ("s91", "s91", "frei", ueber(3, "Seniorenjahre")),
    ("s92", "s92", "chips", dict(chips=[("Spezialfutter", ORANGE, False), ("Medikamente", ROT, False), ("mehr Tierarzt", ROT, False)])),
    ("s93", "s93", "zahl", dict(zahl="+50 €", sub="pro Monat im Alter", farbe=ROT)),
    ("s94", "s94", "zahl", dict(zahl="≈ 1.800 €", sub="extra in 3 Jahren", farbe=ROT)),
    ("s95", "s96", "split", dict(icon=ICON(HERZ), text="Im Alter braucht er dich am meisten")),
    # ---- Gesamtrechnung & Tipps ----
    ("s97", "s103", "frei", beleg(Z, "gs", "Ein ganzes Hundeleben", ICON(RECHNER), [
        ("s98", "s98", HUND, "Anschaffung & 1. Jahr", 2200),
        ("s99", "s99", ICON(NAPF), "Laufend (13 Jahre)", 23400),
        ("s100", "s100", ICON(FLUG), "Urlaub & Pension", 3900),
        ("s101", "s101", ICON(PFLASTER), "Große OP", 3000),
        ("s102", "s102", ICON(PILLE), "Seniorenjahre", 1800),
    ], "s103", "≈ 34.000 €")),
    ("s104", "s104", "split", dict(icon=doppel(HUND_NEUTRAL, AUTO), text="= ein Kleinwagen!", farbe=ROT)),
    ("s105", "s105", "zahl", dict(zahl="≈ 220 €", sub="pro Monat – 13 Jahre lang")),
    ("s106", "s107", "frei", balken3(Z, "gr", [("kleiner Hund", "20.000 €", 240, GRUEN, "s106"), ("mittel", "34.000 €", 410, ORANGE, None),
                                                ("großer Hund", "40.000 €+", 500, ROT, "s107")])),
    ("s108", "s108", "split", dict(icon=ICON(BLASE), text="Wie lag deine Schätzung?")),
    ("s109", "s110", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="5 Spartipps", farbe=GRUEN)),
    ("s111", "s111", "frei", tipp(1, "Hundekonto")),
    ("s112", "s112", "zahl", dict(zahl="50 €", sub="jeden Monat zurücklegen", farbe=GRUEN)),
    ("s113", "s113", "zahl", dict(zahl="1.800 €", sub="nach 3 Jahren für Notfälle", farbe=GOLD)),
    ("s114", "s114", "frei", tipp(2, "OP-Versicherung früh")),
    ("s115", "s115", "split", dict(icon=HUND, text="Jung = günstiger Beitrag", farbe=GRUEN)),
    ("s116", "s116", "frei", tipp(3, "Futter in Großpackung")),
    ("s117", "s117", "zahl", dict(zahl="−10 – 20 %", sub="beim Futter", farbe=GRUEN)),
    ("s118", "s118", "frei", tipp(4, "Haftpflicht vergleichen")),
    ("s119", "s120", "split", dict(icon=ICON(SCHILD), text="Gleiche Leistung, andere Preise", sub="+ günstige Kurse im Hundeverein", sub_at=st("s120") - st("s119"))),
    ("s121", "s121", "frei", tipp(5, "Vorsorge")),
    ("s122", "s122", "chips", dict(chips=[("Bewegung", GRUEN, False), ("richtiges Gewicht", GRUEN, False), ("gepflegte Zähne", GRUEN, False)])),
    ("s123", "s124", "split", dict(icon=HUND, text="Kein günstiges Hobby …", sub="… aber ein Familienmitglied", sub_at=st("s124") - st("s123"))),
    ("s125", "s125", "split", dict(icon=ICON(HERZ), text="Jeder Euro ist es wert", farbe=ORANGE)),
    ("s126", "s126", "split", dict(icon=doppel(DAUMEN, TEILEN), text="Like & teilen!", farbe=ORANGE)),
    ("s127", "s127", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
