#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): Von 0 auf 100.000 € mit normalem Gehalt."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, GELDSACK, SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build  # noqa: E402
from icons import *  # noqa: E402,F401,F403

T = json.loads((HERE / "timings.json").read_text())
S = {s["id"]: s for s in T["saetze"]}


def st(i):
    return S[f"s{i}"]["start"]



# ---------- Sonder-Szenen ----------
def intro():
    html = ('<div class="mitte" style="flex-direction:row;gap:80px">'
            f'<div id="in-sack" style="width:520px;height:520px">{GELDSACK}</div>'
            '<div style="text-align:left"><div id="in-t1" class="serif" style="font-size:150px;line-height:1;color:#111">0 → <span style="color:#c99a06">100.000 €</span></div>'
            '<div id="in-t2" style="font-weight:800;font-size:72px;color:#353a3d;margin-top:30px">mit normalem Gehalt</div></div></div>')

    def js(t0, d):
        return (f'tl.fromTo("#in-sack", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});'
                f' tl.fromTo("#in-t1", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});'
                f' tl.fromTo("#in-t2", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});')
    return dict(html=html, js=js)


def wachstum():
    data = [("5 Jahre", "21.000 €", 150, "s50"), ("10 Jahre", "50.000 €", 330, "s51"), ("16 Jahre", "100.000 €", 600, "s52")]
    cols = "".join(
        f'<div id="wa-{i}" style="display:flex;flex-direction:column;align-items:center;gap:16px">'
        f'<div class="serif" style="font-size:64px;color:{GOLD if i else GRUEN}">{v}</div>'
        f'<div style="width:260px;height:{h}px;border-radius:14px 14px 0 0;background:{"#f2c418" if i else GRUEN}"></div>'
        f'<div style="font-weight:800;font-size:46px;color:#353a3d">{j}</div></div>' for i, (j, v, h, _) in enumerate(data))
    html = f'<div class="mitte" style="flex-direction:row;align-items:flex-end;gap:90px;top:110px">{cols}</div>'

    def js(t0, d):
        return " ".join(f'pop("#wa-{i}", {st(int(s[1:]))});' for i, (_, _, _, s) in enumerate(data))
    return dict(html=html, js=js)


def vergleich():
    html = ('<div class="mitte" style="flex-direction:row;align-items:flex-end;gap:120px">'
            '<div id="vg-a" style="display:flex;flex-direction:column;align-items:center;gap:16px"><div class="serif" style="font-size:72px;color:#1f7a4d">58.000 €</div>'
            '<div style="width:300px;height:330px;background:#1f7a4d;border-radius:14px 14px 0 0"></div><div style="font-weight:800;font-size:46px">eingezahlt</div></div>'
            '<div id="vg-b" style="display:flex;flex-direction:column;align-items:center;gap:16px"><div class="serif" style="font-size:72px;color:#c99a06">100.000 €</div>'
            '<div style="width:300px;height:570px;background:#f2c418;border-radius:14px 14px 0 0"></div><div style="font-weight:800;font-size:46px">nach 16 Jahren</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#vg-a", {t0}); pop("#vg-b", {t0} + 0.6);')


def checkliste():
    items = ["Kassensturz", "Notgroschen", "Automatisch sparen", "Investieren", "Dranbleiben"]
    rows = "".join(f'<div id="cl-{i}" style="display:flex;align-items:center;gap:30px"><div style="width:84px;height:84px">{CHECK}</div>'
                   f'<div style="font-weight:800;font-size:64px;color:#111">{t}</div></div>' for i, t in enumerate(items))
    html = f'<div class="mitte" style="align-items:center"><div style="display:flex;flex-direction:column;gap:22px">{rows}</div></div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#cl-{i}", {t0} + {0.2 + i * min(0.8, (d - 0.5) / 5):.2f});' for i in range(5)))



KAPITEL = {"k1": "Einstieg", "k2": "Schritt 1 · Kassensturz", "k3": "Schritte 2 & 3 · Notgroschen & Sparen", "k4": "Schritt 4 · Investieren", "k5": "Stolperfallen"}

SZENEN = [
    # ---- Kapitel 1 ----
    ("s1", "s1", "frei", intro()),
    ("s2", "s3", "split", dict(icon=ICON(KRONE), text="Nur was für Reiche?", sub='<span style="color:#e24b4b">Stimmt nicht!</span>', sub_at=S["s3"]["start"] - S["s2"]["start"])),
    ("s4", "s4", "split", dict(icon=doppel(ZETTEL, PLAN), text="Normales Gehalt + klarer Plan", farbe=GRUEN)),
    ("s5", "s5", "chips", dict(chips=[("Lotto", ROT, True), ("Erbschaft", ROT, True), ("Zocker-Aktien", ROT, True)])),
    ("s6", "s6", "split", dict(icon=ICON(DENKEN), text="„Mit meinem Gehalt geht das nie …“")),
    ("s7", "s7", "split", dict(icon=ICON(KURVE), text="Die Mathematik ist auf deiner Seite", farbe=GRUEN)),
    ("s8", "s8", "chips", dict(titel="Der Plan", chips=[("1 Kassensturz", ORANGE, False), ("2 Notgroschen", ORANGE, False), ("3 Zuerst sparen", ORANGE, False), ("4 Investieren", ORANGE, False)])),
    ("s9", "s9", "split", dict(icon=ICON(UHR), text="Wie lange dauert es?")),
    ("s10", "s10", "split", dict(icon=ICON(WARN), text="3 Stolperfallen", farbe=ROT)),
    ("s11", "s11", "split", dict(icon=ICON(BEAGLE), text="Bleib bis zum Schluss dran!")),
    ("s12", "s12", "kapitel", dict(titel='<span style="color:#DB8622">Los geht\'s!</span>')),
    # ---- Kapitel 2 ----
    ("s13", "s13", "kapitel", dict(nr=1, titel="Kassensturz")),
    ("s14", "s14", "split", dict(icon=ICON(GELDBEUTEL), text="Wohin fließt dein Geld?")),
    ("s15", "s15", "split", dict(icon=ICON(NOTIZ), text="1 Monat lang alles aufschreiben")),
    ("s16", "s16", "chips", dict(chips=[(x, c, False) for x, c in [("Miete", "#353a3d"), ("Strom", "#f2c418"), ("Handy", "#3d7be0"), ("Versicherungen", GRUEN), ("Essen", ORANGE), ("Abos", "#9b59b6"), ("Kaffee", "#8a5a2b")]])),
    ("s17", "s17", "split", dict(icon=ICON(HANDY), text="App oder Tabelle")),
    ("s18", "s18", "split", dict(icon=ICON(SCHOCK), text="Ehrlich schockiert …")),
    ("s19", "s19", "zahl", dict(zahl="−200 bis −300 €", sub="verschwinden jeden Monat", farbe=ROT)),
    ("s20", "s20", "split", dict(icon=ICON(STAPEL), text="Dein Startkapital", farbe=GOLD)),
    ("s21", "s21", "split", dict(icon=ICON(LISA), text="Das ist Lisa")),
    ("s22", "s22", "split", dict(icon=ICON(LISA), text="2.000 € netto", farbe=GRUEN)),
    ("s23", "s23", "chips", dict(chips=[("2 Abos", ROT, True), ("öfter selbst kochen", GRUEN, False)])),
    ("s24", "s24", "zahl", dict(zahl="+300 €", sub="jeden Monat übrig", farbe=GRUEN)),
    ("s25", "s26", "split", dict(icon=ICON(BLASE), text="Wie viel bleibt bei dir übrig?", sub="Schreib's in die Kommentare!", sub_at=S["s26"]["start"] - S["s25"]["start"])),
    ("s27", "s27", "frei", folgen()),
    # ---- Kapitel 3 ----
    ("s28", "s28", "kapitel", dict(nr=2, titel="Notgroschen")),
    ("s29", "s29", "split", dict(icon=ICON(SPARSCHWEIN, 640, 555), text="Dein Sicherheitspolster")),
    ("s30", "s30", "split", dict(icon=KAL3, text="3 Monatsausgaben", farbe=GRUEN)),
    ("s31", "s31", "split", dict(icon=ICON(LISA), text="≈ 4.500 €", farbe=GRUEN)),
    ("s32", "s32", "split", dict(icon=ICON(BANK), text="Tagesgeldkonto")),
    ("s33", "s33", "chips", dict(chips=[("kostenlos ✓", GRUEN, False), ("Zinsen ✓", GRUEN, False)])),
    ("s34", "s34", "split", dict(icon=ICON(WASCH), text="Für echte Notfälle")),
    ("s35", "s35", "split", dict(icon=doppel(FLUG, CROSS), text="Nicht für den Urlaub!", farbe=ROT)),
    ("s36", "s36", "kapitel", dict(nr=3, titel="Zuerst sparen")),
    ("s37", "s37", "split", dict(icon=ICON(AUTO_PFEIL, 700, 700), text="Dauerauftrag am Gehaltstag")),
    ("s38", "s38", "split", dict(icon=doppel(coin("300 €", 300, 80), SPARSCHWEIN), text="Automatisch weg", farbe=GRUEN)),
    ("s39", "s39", "split", dict(icon=ICON(TASCHE), text="Der Rest: entspannt ausgeben")),
    ("s40", "s40", "split", dict(icon=ICON(WARN), text="Simpel – aber die meisten scheitern", farbe=ROT)),
    ("s41", "s41", "split", dict(icon=ICON(GELDBEUTEL), text="Monatsende = 0 €", farbe=ROT)),
    # ---- Kapitel 4 ----
    ("s42", "s42", "kapitel", dict(nr=4, titel="Investieren")),
    ("s43", "s43", "split", dict(icon=doppel(coin("300 €", 300, 80), GLOBUS), text="ETF auf die ganze Welt")),
    ("s44", "s44", "split", dict(icon=ICON(KORB), text="1.000+ Unternehmen", farbe=GRUEN)),
    ("s45", "s45", "split", dict(icon=ICON(RASTER), text="Breit gestreut")),
    ("s46", "s46", "split", dict(icon=ICON(PREIS, 640, 640), text="Kosten: Zehntel Prozent", farbe=GRUEN)),
    ("s47", "s47", "split", dict(icon=ICON(CHART7), text="Historisch ~7 % pro Jahr", farbe=GRUEN)),
    ("s48", "s48", "split", dict(icon=ICON(WARN), text="Keine Garantie!", farbe=ROT)),
    ("s49", "s49", "split", dict(icon=ICON(RECHNER), text="Rechnen wir mal …")),
    ("s50", "s52", "frei", wachstum()),
    ("s53", "s53", "frei", vergleich()),
    ("s54", "s54", "split", dict(icon=ICON(SCHNEEBALL), text="Der Zinseszins", farbe=GRUEN)),
    ("s55", "s55", "split", dict(icon=ICON(RAKETE), text="500 €/Monat → gut 11 Jahre", farbe=GRUEN)),
    # ---- Kapitel 5 ----
    ("s56", "s56", "split", dict(icon=ICON(WARN), text="Die 3 Stolperfallen", farbe=ROT)),
    ("s57", "s57", "kapitel", dict(nr=1, titel="Panik").copy()),
    ("s58", "s58", "split", dict(icon=ICON(CRASH), text="−20 bis −30 %", farbe=ROT)),
    ("s59", "s59", "split", dict(icon=doppel(VERKAUF, CROSS), text="Verluste werden echt", farbe=ROT)),
    ("s60", "s60", "split", dict(icon=ICON(NACHKAUF), text="Weiter sparen = günstig kaufen", farbe=GRUEN)),
    ("s61", "s61", "kapitel", dict(nr=2, titel="Lifestyle-Inflation")),
    ("s62", "s62", "split", dict(icon=ICON(PFEILE), text="Erst Sparrate, dann Ausgaben")),
    ("s63", "s63", "kapitel", dict(nr=3, titel="Ungeduld")),
    ("s64", "s64", "split", dict(icon=ICON(FUNDAMENT), text="Erst das Fundament")),
    ("s65", "s65", "split", dict(icon=ICON(STERN), text="Bonus-Tipp", farbe=GOLD)),
    ("s66", "s66", "split", dict(icon=ICON(TREPPE), text="+20 € Sparrate pro Jahr", farbe=GRUEN)),
    ("s67", "s67", "split", dict(icon=ICON(ZIEL), text="Schneller ans Ziel")),
    ("s68", "s68", "zahl", dict(zahl="100.000 €", sub="kein Traum – ein Plan", farbe=GOLD)),
    ("s69", "s69", "frei", checkliste()),
    ("s70", "s70", "split", dict(icon=doppel(DAUMEN, TEILEN), text="Like & teilen!", farbe=ORANGE)),
    ("s71", "s71", "frei", folgen("Bis zum nächsten Video!")),
]

# Stolperfallen-Karten zeigen "Falle 1/2/3" statt "Schritt"
for i, z in enumerate(SZENEN):
    if z[0] in ("s57", "s61", "s63"):
        SZENEN[i] = (z[0], z[1], "frei", dict(
            html=f'<div class="mitte"><div class="kap"><div class="nr" id="fa-{z[0]}" style="background:#e24b4b">Stolperfalle {z[3]["nr"]}</div><div class="t" id="fa-{z[0]}-t">{z[3]["titel"]}</div></div></div>',
            js=(lambda s: lambda t0, d: f'pop("#fa-{s}", {t0}); pop("#fa-{s}-t", {t0} + 0.15);')(z[0])))

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
