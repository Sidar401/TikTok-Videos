#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): So viel Geld brauchst du wirklich zum Leben."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402
from icons import (AUTO_PFEIL, BANK, BLASE, DAUMEN, FLUG, GELDBEUTEL, HANDY, ICON, KURVE, RECHNER, SCHOCK,  # noqa: E402
                   STAPEL, STERN, TASCHE, TEILEN, WARN, WASCH, ZETTEL, big, doppel, folgen, person)

T = json.loads((HERE / "timings.json").read_text())
S = {s["id"]: s for s in T["saetze"]}


def st(sid):
    return S[sid]["start"]


def euro_zeit(sid):
    """Zeitpunkt, an dem im Satz der Euro-Betrag gesprochen wird (erste Caption mit €)."""
    for c in S[sid]["captions"]:
        if "€" in c["text"]:
            return c["start"]
    return st(sid)


def eur(v):
    return f"{v:,} €".replace(",", ".")


# ---------- Icons ----------
HAUS = svg('<path d="M8 48 L50 10 L92 48" fill="none" stroke="#353a3d" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /><path d="M18 44 L18 92 L82 92 L82 44 L50 16 Z" fill="#DB8622" /><rect x="40" y="62" width="20" height="30" rx="3" fill="#fff" /><rect x="24" y="52" width="14" height="14" rx="2" fill="#fff8d6" /><rect x="62" y="52" width="14" height="14" rx="2" fill="#fff8d6" />')
STROM = svg('<circle cx="50" cy="50" r="44" fill="#fff8d6" stroke="#353a3d" stroke-width="5" /><path d="M56 12 L28 56 L48 56 L42 88 L72 42 L52 42 Z" fill="#f2c418" stroke="#c99a06" stroke-width="3" stroke-linejoin="round" />')
WAGEN = svg('<path d="M6 14 L20 14 L30 64 L80 64 L90 30 L24 30" fill="none" stroke="#353a3d" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" /><rect x="34" y="20" width="14" height="16" rx="2" fill="#2c9a63" /><rect x="52" y="14" width="12" height="22" rx="2" fill="#e24b4b" /><rect x="68" y="22" width="12" height="14" rx="2" fill="#f2c418" /><circle cx="36" cy="80" r="8" fill="#353a3d" /><circle cx="72" cy="80" r="8" fill="#353a3d" />')
TICKET = svg('<path d="M6 26 L94 26 L94 42 Q86 50 94 58 L94 74 L6 74 L6 58 Q14 50 6 42 Z" fill="#e24b4b" /><text x="50" y="58" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="17" fill="#fff">D-Ticket</text>')
AUTO = svg('<path d="M10 62 L16 40 Q20 30 32 30 L68 30 Q80 30 84 40 L90 62 Z" fill="#3d7be0" /><rect x="6" y="56" width="88" height="22" rx="8" fill="#3d7be0" /><path d="M26 40 L32 34 L68 34 L74 40 Z" fill="#cfe6f5" /><circle cx="28" cy="78" r="10" fill="#353a3d" /><circle cx="72" cy="78" r="10" fill="#353a3d" />')
SCHILD = svg('<path d="M50 6 L88 20 L88 48 Q88 78 50 94 Q12 78 12 48 L12 20 Z" fill="#1f7a4d" /><path d="M32 50 L46 64 L70 38" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" />')
TV = svg('<rect x="6" y="18" width="88" height="60" rx="8" fill="#353a3d" /><rect x="14" y="26" width="72" height="44" rx="4" fill="#cfe6f5" /><path d="M38 6 L50 18 L62 6" fill="none" stroke="#353a3d" stroke-width="5" stroke-linecap="round" /><rect x="30" y="82" width="40" height="8" rx="4" fill="#353a3d" />')
PLAY = svg('<rect x="6" y="14" width="88" height="66" rx="14" fill="#9b59b6" /><path d="M40 32 L66 47 L40 62 Z" fill="#fff" />')
KIND = svg('<rect x="22" y="22" width="56" height="70" rx="14" fill="#e24b4b" /><path d="M36 22 Q36 6 50 6 Q64 6 64 22" fill="none" stroke="#a8321f" stroke-width="6" /><rect x="32" y="52" width="36" height="24" rx="6" fill="#f2c418" /><rect x="46" y="58" width="8" height="8" rx="2" fill="#a8321f" />')
HERZ = svg('<path d="M50 88 Q10 60 10 34 Q10 12 30 12 Q44 12 50 26 Q56 12 70 12 Q90 12 90 34 Q90 60 50 88 Z" fill="#e24b4b" />')
KIND_P = person("#3d7be0", "#8a5a2b")
MAX = person("#3d7be0", "#353a3d")
LISA = person(ORANGE, "#8a5a2b")
TOM = person(GRUEN, "#353a3d")


def gruppe(*leute, w=220, h=300):
    return '<div style="display:flex;align-items:flex-end;gap:10px">' + "".join(
        f'<div style="width:{w * f:.0f}px;height:{h * f:.0f}px">{p}</div>' for p, f in leute) + "</div>"


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


def karte(nr_text, titel, farbe=ORANGE, uid="ka"):
    html = (f'<div class="mitte"><div class="kap"><div class="nr" id="{uid}-n" style="background:{farbe}">{nr_text}</div>'
            f'<div class="t" id="{uid}-t">{titel}</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#{uid}-n", {t0}); tl.fromTo("#{uid}-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t0} + 0.15);')


def drei():
    teile = [("s9", SINGLE, "Single"), ("s10", PAAR, "Paar"), ("s11", FAMILIE, "Familie")]
    cols = "".join(f'<div id="dr-{i}" style="display:flex;flex-direction:column;align-items:center;gap:20px;width:520px">'
                   f'<div style="height:380px;display:flex;align-items:flex-end">{g}</div>'
                   f'<div style="padding:12px 40px;border-radius:40px;background:var(--brand);color:#fff;font-weight:800;font-size:58px">{n}</div></div>'
                   for i, (_, g, n) in enumerate(teile))
    html = f'<div class="mitte" style="flex-direction:row;gap:40px">{cols}</div>'
    return dict(html=html, js=lambda t0, d: " ".join(f'pop("#dr-{i}", {st(s) if i else t0});' for i, (s, _, _) in enumerate(teile)))


def beleg(uid, titel, intro_icon, posten, ende_sid, summe_text):
    """Kassenzettel: links wechselnde Icons, rechts füllt sich die Liste mit laufender Summe.
    posten = [(icon_ab_sid, betrag_sid, icon, label, betrag)]"""
    icons = [(None, intro_icon)] + [(p[0], p[2]) for p in posten]
    bild = "".join(f'<div id="{uid}-i{k}" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0">{ic}</div>'
                   for k, (_, ic) in enumerate(icons))
    zeilen = "".join(f'<div id="{uid}-r{k}" style="display:flex;justify-content:space-between;font-weight:700;font-size:38px;color:#353a3d;padding:7px 0;opacity:0">'
                     f'<span>{p[3]}</span><span style="font-weight:800;color:#111">{eur(p[4])}</span></div>'
                     for k, p in enumerate(posten))
    summen, s = [], 0
    for p in posten:
        s += p[4]
        summen.append(s)
    tot = "".join(f'<div id="{uid}-s{k}" class="serif" style="position:absolute;right:0;top:0;font-size:60px;color:{ROT};opacity:0">{eur(v)}</div>'
                  for k, v in enumerate(summen))
    tot += f'<div id="{uid}-sf" class="serif" style="position:absolute;right:0;top:0;font-size:60px;color:{ROT};opacity:0">{summe_text}</div>'
    html = (f'<div class="bild" style="position:absolute">{bild}</div>'
            f'<div style="position:absolute;left:960px;top:120px;width:840px;height:740px;background:#faf5ef;border-radius:34px;padding:34px 50px;display:flex;flex-direction:column">'
            f'<div style="font-weight:800;font-size:46px;color:var(--brand);border-bottom:4px dashed #d9cbb8;padding-bottom:14px;margin-bottom:10px">{titel}</div>'
            f'<div style="flex:1">{zeilen}</div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center;border-top:4px solid #353a3d;padding-top:18px">'
            f'<span style="font-weight:800;font-size:46px;color:#111">Summe</span><div id="{uid}-sb" style="position:relative;width:420px;height:72px">{tot}</div></div></div>')

    def js(t0, d):
        out = []
        zeiten = [t0] + [st(p[0]) for p in posten]
        for k, a in enumerate(zeiten):
            out.append(f'tl.fromTo("#{uid}-i{k}", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, {a});')
            if k + 1 < len(zeiten):
                out.append(f'tl.to("#{uid}-i{k}", {{ opacity: 0, duration: 0.2 }}, {zeiten[k + 1] - 0.2});')
        for k, p in enumerate(posten):
            a = euro_zeit(p[1])
            out.append(f'tl.fromTo("#{uid}-r{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {a});')
            out.append(f'tl.fromTo("#{uid}-s{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {a});')
            if k:
                out.append(f'tl.to("#{uid}-s{k - 1}", {{ opacity: 0, duration: 0.2 }}, {a});')
        e = euro_zeit(ende_sid)
        out.append(f'tl.to("#{uid}-s{len(posten) - 1}", {{ opacity: 0, duration: 0.2 }}, {e});')
        out.append(f'tl.fromTo("#{uid}-sf", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {e});')
        return " ".join(out)
    return dict(html=html, js=js)


def balken3(uid, daten, sub=None, sub_sid=None):
    """Balkenvergleich: daten = [(label, wert_text, höhe, farbe, sid)]"""
    cols = "".join(
        f'<div id="{uid}-{i}" style="display:flex;flex-direction:column;align-items:center;gap:14px">'
        f'<div class="serif" style="font-size:64px;color:{c}">{v}</div>'
        f'<div style="width:260px;height:{h}px;border-radius:14px 14px 0 0;background:{c}"></div>'
        f'<div style="font-weight:800;font-size:46px;color:#353a3d">{lab}</div></div>' for i, (lab, v, h, c, _) in enumerate(daten))
    sub_html = f'<div id="{uid}-sub" style="position:absolute;right:150px;top:150px;padding:12px 34px;border-radius:30px;background:#353a3d;color:#fff;font-weight:800;font-size:46px">{sub}</div>' if sub else ""
    html = f'<div class="mitte" style="flex-direction:row;align-items:flex-end;gap:90px;top:110px">{cols}</div>{sub_html}'

    def js(t0, d):
        out = [f'pop("#{uid}-{i}", {euro_zeit(s) if s else t0});' for i, (_, _, _, _, s) in enumerate(daten)]
        if sub:
            out.append(f'pop("#{uid}-sub", {st(sub_sid)});')
        return " ".join(out)
    return dict(html=html, js=js)


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
    ("s25", "s48", "frei", beleg("mx", "Max · pro Monat", SINGLE, [
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
    ("s57", "s68", "frei", beleg("pa", "Lisa & Tom · pro Monat", PAAR, [
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
    ("s70", "s71", "frei", balken3("pp", [("Max allein", "1.500 €", 420, ROT, None), ("pro Person", "1.350 €", 370, GRUEN, "s70")])),
    ("s72", "s73", "split", dict(icon=PAAR, text="Warum?", sub="Miete, Internet, Rundfunk & Auto teilen sich auf 2 Köpfe", sub_at=st("s73") - st("s72"))),
    ("s74", "s74", "split", dict(icon=ICON(HERZ), text="Romantisch & clever", farbe=GRUEN)),
    ("s75", "s75", "zahl", dict(zahl="≈ 3.000 €", sub="netto – mit 10 % Sparrate", farbe=GRUEN)),
    ("s76", "s76", "split", dict(icon=ICON(STAPEL), text="Hier bleibt was übrig", farbe=GOLD)),
    ("s77", "s77", "split", dict(icon=ICON(KURVE), text="Jetzt sparen & investieren", farbe=GRUEN)),
    ("s78", "s78", "split", dict(icon=ICON(WARN), text="Mit Kindern wird's enger", farbe=ROT)),
    # ---- Familie ----
    ("s79", "s79", "frei", karte("Situation 3", "Familie", uid="k3")),
    ("s80", "s95", "frei", beleg("fa", "Familie Becker · pro Monat", FAMILIE, [
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
    ("s107", "s110", "frei", balken3("zf", [("Single", "1.500 €", 220, "#3d7be0", "s107"), ("Paar", "2.700 €", 400, GRUEN, "s108"), ("Familie", "4.000 €", 590, ORANGE, "s109")], "ohne Sparen", "s110")),
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
