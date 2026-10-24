#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): Bist du arm oder reich? Die Einkommens-Leiter. Beagle nur im CTA, kein Geldbeutel/Kassenzettel."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import BLASE, HANDY, HAUS, ICON, TEILEN, folgen, gruppe, person  # noqa: E402
from lf_szenen import Zeit, balken3, chips_zeit, duell, karte  # noqa: E402

Z = Zeit(HERE)
st = Z.st
BLAU, LILA, GRAU = "#3d7be0", "#9b59b6", "#d9d2c7"

# ---------- Icons ----------
WAAGE = svg('<rect x="47" y="14" width="6" height="70" fill="#353a3d" /><rect x="26" y="84" width="48" height="8" rx="4" fill="#353a3d" /><rect x="12" y="20" width="76" height="5" rx="2" fill="#353a3d" />'
            '<path d="M18 24 L6 52 L30 52 Z M82 24 L70 52 L94 52 Z" fill="none" stroke="#353a3d" stroke-width="3" /><path d="M4 52 Q18 64 32 52 Z" fill="#1f7a4d" /><path d="M68 52 Q82 64 96 52 Z" fill="#e24b4b" />')
LUPE = svg('<circle cx="42" cy="42" r="28" fill="#cfe6f5" stroke="#353a3d" stroke-width="8" /><path d="M62 62 L90 90" stroke="#353a3d" stroke-width="12" stroke-linecap="round" />'
           '<text x="42" y="52" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="26" fill="#1f7a4d">%</text>')
PSST = svg('<path d="M10 14 L90 14 Q96 14 96 20 L96 62 Q96 68 90 68 L40 68 L22 86 L26 68 L10 68 Q4 68 4 62 L4 20 Q4 14 10 14 Z" fill="#fff" stroke="#353a3d" stroke-width="4" />'
           '<rect x="36" y="38" width="28" height="22" rx="4" fill="#DB8622" /><path d="M42 38 L42 30 Q50 20 58 30 L58 38" fill="none" stroke="#353a3d" stroke-width="4" />')
FRAGE = svg('<circle cx="50" cy="50" r="44" fill="#DB8622" /><text x="50" y="72" text-anchor="middle" font-family="Abril Fatface" font-size="64" fill="#fff">?</text>')
LEITER = svg('<rect x="22" y="4" width="8" height="92" rx="3" fill="#8a5a2b" /><rect x="70" y="4" width="8" height="92" rx="3" fill="#8a5a2b" />' + "".join(
    f'<rect x="26" y="{14 + i * 16}" width="48" height="6" rx="3" fill="{c}" />' for i, c in enumerate(["#9b59b6", "#1f7a4d", "#3d7be0", "#c99a06", "#DB8622", "#e24b4b"])) +
    '<path d="M84 60 L84 20 M76 30 L84 18 L92 30" fill="none" stroke="#1f7a4d" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />')
HOCHHAUS = svg('<rect x="20" y="8" width="34" height="88" fill="#555c60" /><rect x="56" y="30" width="26" height="66" fill="#353a3d" />' + "".join(
    f'<rect x="{25 + (i % 3) * 9}" y="{14 + (i // 3) * 12}" width="6" height="7" fill="#f2c418" />' for i in range(18)) + '<rect x="4" y="94" width="92" height="4" fill="#353a3d" />')
KRONE_P = svg('<path d="M30 26 L26 6 L38 16 L50 2 L62 16 L74 6 L70 26 Z" fill="#f2c418" stroke="#c99a06" stroke-width="2" />'
              '<circle cx="50" cy="44" r="16" fill="#f1c9a5" /><path d="M18 98 Q18 62 50 60 Q82 62 82 98 Z" fill="#c99a06" />')

STUFEN = [("1", "< 1.400 €", ROT), ("2", "1.400 – 2.300 €", ORANGE), ("3", "≈ 2.300 €", GOLD),
          ("4", "2.300 – 4.600 €", BLAU), ("5", "> 4.600 €", GRUEN), ("6", "Top 1 %", LILA)]


def leiter(uid, aktiv, zeilen):
    """Einkommens-Leiter links (Stufe 1 unten), aktive Stufe hervorgehoben; rechts Textzeilen [(text, sid, art)].
    aktiv=0: Übersicht, alle Stufen bunt und nacheinander eingeblendet. art: 'h' groß, 's' normal, 'k' klein, 'g' grün."""
    sprossen = []
    for i, (nr, label, farbe) in enumerate(reversed(STUFEN)):
        n = int(nr)
        an = aktiv == 0 or n == aktiv
        bg = farbe if an else GRAU
        sprossen.append(f'<div id="{uid}-p{n}" style="display:flex;align-items:center;gap:18px;height:84px;padding:0 26px;border-radius:18px;background:{bg};'
                        f'color:#fff;font-weight:800;font-size:{40 if an else 34}px;{"transform:scale(1.06);" if n == aktiv else ""}'
                        f'{"opacity:0.55;" if not an else ""}"><span class="serif" style="font-size:52px;width:44px">{nr}</span>{label}</div>')
    stil = {"h": "font-family:'Abril Fatface',serif;font-size:96px;line-height:1.05;color:#111",
            "s": "font-weight:800;font-size:50px;line-height:1.2;color:#353a3d",
            "k": "font-weight:700;font-size:40px;line-height:1.25;color:#555c60",
            "g": "font-weight:800;font-size:50px;line-height:1.2;color:#1f7a4d"}
    rechts = "".join(f'<div id="{uid}-z{k}" style="{stil[a]}">{t}</div>' for k, (t, _, a) in enumerate(zeilen))
    html = (f'<div style="position:absolute;left:130px;top:130px;width:620px;height:720px;display:flex;flex-direction:column;justify-content:space-between;'
            f'border-left:12px solid #8a5a2b;border-right:12px solid #8a5a2b;padding:0 18px">{"".join(sprossen)}</div>'
            f'<div style="position:absolute;left:850px;top:150px;width:950px;height:700px;display:flex;flex-direction:column;justify-content:center;gap:26px">{rechts}</div>')

    def js(t0, d):
        out = []
        if aktiv == 0:
            step = min(0.35, max(0.15, (d - 1) / 8))
            out += [f'pop("#{uid}-p{n}", {t0} + {(n - 1) * step:.2f});' for n in range(1, 7)]
        else:
            out.append(f'tl.fromTo("#{uid}-p{aktiv}", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.25, yoyo: true, repeat: 1 }}, {t0} + 0.2);')
        for k, (_, sid, _) in enumerate(zeilen):
            a = st(sid) if sid else t0
            out.append(f'tl.fromTo("#{uid}-z{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {max(a, t0 + 0.1)});')
        return " ".join(out)
    return dict(html=html, js=js)


def intro():
    pills = "".join(f'<div id="in-{i}" style="padding:20px 60px;border-radius:60px;background:{c};color:#fff;font-weight:900;font-size:110px">{w}</div>'
                    for i, (w, c) in enumerate([("arm?", ROT), ("normal?", BLAU), ("reich?", GRUEN)]))
    html = (f'<div class="mitte" style="gap:60px"><div id="in-t" class="serif" style="font-size:120px;color:#111">Bist du …</div>'
            f'<div style="display:flex;gap:40px">{pills}</div></div>')

    def js(t0, d):
        return "".join(f' tl.fromTo("#{i}", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {t0});' for i in ("in-t", "in-0", "in-1", "in-2"))
    return dict(html=html, js=js)


def durchschnitt():
    """9 Leute à 3.000 € + 1 Millionär: Durchschnitt springt, Median bleibt."""
    leute = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px"><div style="width:150px;height:200px">{person(BLAU, "#353a3d")}</div>'
                    f'<div style="font-weight:800;font-size:30px;color:#353a3d">3.000&nbsp;€</div></div>' for _ in range(9))
    mill = (f'<div id="du-m" style="display:flex;flex-direction:column;align-items:center;gap:8px"><div style="width:190px;height:250px">{KRONE_P}</div>'
            f'<div style="font-weight:800;font-size:28px;color:#c99a06">Millionär</div></div>')
    html = (f'<div class="mitte" style="gap:50px"><div style="display:flex;align-items:flex-end;gap:14px">{leute}{mill}</div>'
            f'<div style="display:flex;gap:40px"><div id="du-d" class="chip" style="background:{ROT}">Durchschnitt: explodiert ↑</div>'
            f'<div id="du-n" class="chip" style="background:{GRUEN}">Median: bleibt 3.000 €</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#du-m", {Z.euro_zeit("s69") + 1.2}); pop("#du-d", {st("s70")}); pop("#du-n", {st("s70")} + 1.2);')


def weg(nr, titel):
    return karte(f"Weg {nr}", titel, BLAU, uid=f"weg{nr}")


FAMILIE = gruppe((person(GRUEN, "#353a3d"), 1), (person(ORANGE, "#8a5a2b"), 1), (person(BLAU, "#8a5a2b"), 0.62), (person(ROT, "#f2c418"), 0.62), w=190, h=280)

KAPITEL = {"k1": "Einstieg", "k2": "Stufe 1 – 3", "k3": "Stufe 4 – 6", "k4": "Warum wir uns ärmer fühlen", "k5": "5 Wege nach oben"}

SZENEN = [
    # ---- Einstieg ----
    ("s1", "s1", "frei", intro()),
    ("s2", "s4", "split", dict(icon=ICON(WAAGE), text="Die meisten schätzen sich falsch ein", sub="Gefühl ≠ Wirklichkeit", sub_at=st("s3") - st("s2"))),
    ("s5", "s6", "split", dict(icon=ICON(PSST), text="Über Geld spricht keiner", sub="wir vergleichen uns mit Freunden & Internet", sub_at=st("s6") - st("s5"))),
    ("s7", "s7", "split", dict(icon=ICON(LUPE), text="Heute: echte Zahlen", farbe=GRUEN)),
    ("s8", "s10", "frei", leiter("ue", 0, [("Die Einkommens-Leiter", None, "h"), ("Auf welcher Stufe stehst du?", "s10", "s")])),
    ("s11", "s12", "frei", chips_zeit(Z, "pl", "Danach", [("Warum wir uns ärmer fühlen", ORANGE, "s11"), ("5 Wege nach oben", GRUEN, "s12")])),
    ("s13", "s15", "split", dict(icon=ICON(person(BLAU, "#353a3d"), 420, 520), text="Single · netto · pro Monat", sub="Paare & Familien: später · Zahlen gerundet", sub_at=st("s14") - st("s13"))),
    ("s16", "s18", "split", dict(icon=ICON(BLASE), text="Auf welcher Stufe stehst du?", sub="Nur die Nummer in die Kommentare!", sub_at=st("s18") - st("s16"))),
    ("s19", "s20", "frei", folgen("+ Folgen")),
    ("s21", "s21", "kapitel", dict(titel='Ab auf die <span style="color:#DB8622">Leiter!</span>')),
    # ---- Stufe 1 – 3 ----
    ("s22", "s28", "frei", leiter("l1", 1, [("Stufe 1", "s22", "h"), ("unter 1.400 € netto", "s22", "s"), ("offiziell armutsgefährdet", "s23", "s"),
                                            ("≈ jeder 7. Mensch", "s24", "s"), ("Studierende · Alleinerziehende · Teilzeit · kleine Rente", "s25", "k"),
                                            ("Tipp: Wohngeld prüfen!", "s28", "g")])),
    ("s29", "s34", "frei", leiter("l2", 2, [("Stufe 2", "s29", "h"), ("1.400 – 2.300 € netto", "s29", "s"), ("die untere Mitte", "s30", "s"),
                                            ("Berufseinsteiger · Handel · Gastro · Pflege", "s31", "k"),
                                            ("Mindestlohn Vollzeit: ≈ 2.400 € brutto → ≈ 1.700 € netto", "s32", "k"), ("über die Runden – große Sprünge schwer", "s33", "s")])),
    ("s35", "s35", "split", dict(icon=ICON(FRAGE), text="Diese Zahl überrascht viele …")),
    ("s36", "s42", "frei", leiter("l3", 3, [("Stufe 3", "s36", "h"), ("≈ 2.300 € netto", "s36", "s"), ("genau die Mitte Deutschlands", "s37", "s"),
                                            ("50 % haben weniger · 50 % mehr", "s38", "s"), ("= der Median", "s39", "g"),
                                            ("Rentner, Studierende & Teilzeit ziehen ihn nach unten", "s42", "k")])),
    # ---- Stufe 4 – 6 ----
    ("s43", "s43", "kapitel", dict(titel="Weiter nach oben ↑")),
    ("s44", "s49", "frei", leiter("l4", 4, [("Stufe 4", "s44", "h"), ("2.300 – 4.600 € netto", "s44", "s"), ("die obere Mitte", "s45", "s"),
                                            ("Facharbeiter · Meister · erfahrene Angestellte", "s46", "k"), ("Wohnung · Urlaub · sparen ✓", "s48", "g"),
                                            ("„Ich bin doch ganz normal …“", "s49", "s")])),
    ("s50", "s56", "frei", leiter("l5", 5, [("Stufe 5", "s50", "h"), ("über 4.600 € netto", "s50", "s"), ("offiziell einkommensreich", "s51", "g"),
                                            ("doppelte Mitte · nicht mal jeder 10.", "s52", "s"), ("≈ 8.000 € brutto im Monat", "s54", "s"),
                                            ("Ingenieure · Ärzte · IT · Führungskräfte", "s55", "k")])),
    ("s57", "s60", "frei", leiter("l6", 6, [("Stufe 6", "s57", "h"), ("das reichste 1 %", "s58", "s"), ("> 20.000 € brutto im Monat", "s59", "s"),
                                            ("Unternehmer · Top-Manager · Chefärzte", "s60", "k")])),
    ("s61", "s62", "frei", balken3(Z, "ve", [("reichstes Zehntel", "über 50 %", 420, LILA, None), ("alle anderen 90 %", "unter 50 %", 380, "#555c60", "s62")], "Anteil am Vermögen", "s62")),
    ("s63", "s64", "frei", leiter("ub", 0, [("Welten dazwischen", None, "h"), ("Und du? Welche Stufe?", "s64", "s")])),
    # ---- Warum wir uns ärmer fühlen ----
    ("s65", "s65", "split", dict(icon=ICON(FRAGE), text="Ein Trick der Statistik")),
    ("s66", "s68", "zahl", dict(zahl="4.600 €+", sub="„Durchschnittsgehalt“ brutto – wirklich?", farbe=ROT)),
    ("s69", "s70", "frei", durchschnitt()),
    ("s71", "s72", "split", dict(icon=ICON(WAAGE), text="Der Median ist ehrlicher", farbe=GRUEN, sub="darum fühlen sich viele unterdurchschnittlich", sub_at=st("s72") - st("s71"))),
    ("s73", "s74", "frei", balken3(Z, "md", [("Durchschnitt", "≈ 4.600 €", 470, ROT, None), ("Median Vollzeit", "≈ 4.000 €", 400, GRUEN, "s73")], "≈ 2.550 € netto", "s74")),
    ("s75", "s75", "split", dict(icon=ICON(FRAGE), text="3 Gründe, warum wir uns ärmer fühlen")),
    ("s76", "s78", "frei", duell(Z, "wo", dict(name="Land", farbe=GRUEN, icon=ICON(HAUS, 380, 380), wert="3.000 € = viel", ab_sid="s77"),
                                 dict(name="München", farbe=ROT, icon=ICON(HOCHHAUS, 380, 380), wert="3.000 € = knapp", ab_sid="s77"))),
    ("s79", "s82", "split", dict(icon=ICON(HANDY), text="Social Media: nur Highlights", sub="den Kontoauszug postet keiner", sub_at=st("s82") - st("s79"))),
    ("s83", "s84", "split", dict(icon=FAMILIE, text="Familie: ganz andere Grenzen")),
    ("s85", "s87", "frei", balken3(Z, "fa", [("armutsgefährdet", "< 2.900 €", 200, ROT, None), ("einkommensreich", "> 9.700 €", 560, GRUEN, "s86")], "Paar + 2 Kinder, netto", "s87")),
    # ---- 5 Wege nach oben ----
    ("s88", "s89", "split", dict(icon=ICON(LEITER), text="5 Wege eine Stufe höher", farbe=GRUEN)),
    ("s90", "s90", "frei", weg(1, "Gehalt verhandeln")),
    ("s91", "s93", "zahl", dict(zahl="+5 – 10 %", sub="„Wer nie fragt, bekommt nichts“", farbe=GRUEN)),
    ("s94", "s94", "frei", weg(2, "Job wechseln")),
    ("s95", "s96", "zahl", dict(zahl="+10 – 20 %", sub="beim Jobwechsel", farbe=GRUEN)),
    ("s97", "s97", "frei", weg(3, "Weiterbildung")),
    ("s98", "s99", "frei", chips_zeit(Z, "wb", None, [("Meister", BLAU, "s98"), ("Fachwirt", BLAU, None), ("IT-Zertifikat", BLAU, None), ("Aufstiegs-BAföG", GRUEN, "s99")])),
    ("s100", "s100", "frei", weg(4, "Steuererklärung")),
    ("s101", "s103", "zahl", dict(zahl="1.000 €+", sub="im Schnitt zurück – geschenktes Geld", farbe=GRUEN)),
    ("s104", "s104", "frei", weg(5, "Zweites Standbein")),
    ("s105", "s106", "chips", dict(chips=[("Nebenjob", BLAU, False), ("Nachhilfe", ORANGE, False), ("Fotografie", LILA, False), ("Handwerk", GRUEN, False)])),
    ("s107", "s107", "zahl", dict(zahl="3.600 €", sub="pro Jahr mit 300 € im Monat extra", farbe=GRUEN)),
    ("s108", "s110", "frei", leiter("zf", 0, [("Fassen wir zusammen", None, "h"), ("Mitte: ≈ 2.300 € netto", "s109", "s"), ("einkommensreich ab 4.600 €", "s110", "g")])),
    ("s111", "s113", "split", dict(icon=ICON(LEITER), text="Du stehst höher, als du denkst", farbe=GRUEN, sub="… und kannst weiter klettern", sub_at=st("s113") - st("s111"))),
    ("s114", "s115", "split", dict(icon=ICON(BLASE), text="Welche Stufe bist du?", sub="Schreib's in die Kommentare!", sub_at=st("s115") - st("s114"))),
    ("s116", "s116", "split", dict(icon=ICON(TEILEN), text="Teile das Video!", farbe=ORANGE)),
    ("s117", "s117", "frei", folgen("Bis morgen!", uid="fo2")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, KAPITEL)
