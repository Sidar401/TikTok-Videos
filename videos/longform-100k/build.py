#!/usr/bin/env python3
"""HundeFinanzTV Longform (16:9): Von 0 auf 100.000 € mit normalem Gehalt."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, CHECK, CROSS, GELDSACK, SPARSCHWEIN  # noqa: E402
from longform import GOLD, GRUEN, ORANGE, ROT, build, svg  # noqa: E402

T = json.loads((HERE / "timings.json").read_text())
S = {s["id"]: s for s in T["saetze"]}


def st(i):
    return S[f"s{i}"]["start"]


# ---------- Icons (viewBox 0 0 100 100) ----------
def person(col="#353a3d", haar=None):
    h = f'<path d="M30 30 Q30 8 50 8 Q70 8 70 30 L74 52 L26 52 Z" fill="{haar}" />' if haar else ""
    return svg(f'{h}<circle cx="50" cy="30" r="18" fill="#f1c9a5" /><path d="M18 98 Q18 56 50 54 Q82 56 82 98 Z" fill="{col}" />')


LISA = person(ORANGE, "#8a5a2b")
KRONE = svg('<path d="M10 80 L5 25 L30 45 L50 12 L70 45 L95 25 L90 80 Z" fill="#f2c418" stroke="#c99a06" stroke-width="4" stroke-linejoin="round" /><circle cx="50" cy="62" r="7" fill="#e24b4b" />')
ZETTEL = svg('<rect x="15" y="5" width="70" height="90" rx="6" fill="#fff" stroke="#353a3d" stroke-width="4" /><text x="25" y="25" font-family="Montserrat" font-weight="800" font-size="11" fill="#111">Gehalt</text><rect x="25" y="34" width="50" height="5" rx="2" fill="#eee" /><rect x="25" y="45" width="40" height="5" rx="2" fill="#eee" /><text x="50" y="80" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="16" fill="#1f7a4d">2.000 €</text>')
PLAN = svg('<rect x="15" y="5" width="70" height="90" rx="6" fill="#faf5ef" stroke="#353a3d" stroke-width="4" />' + "".join(
    f'<path d="M24 {24 + i * 18} l6 6 l10 -12" fill="none" stroke="#1f7a4d" stroke-width="5" stroke-linecap="round" /><rect x="46" y="{22 + i * 18}" width="30" height="6" rx="3" fill="#ccc" />' for i in range(4)))
DENKEN = svg('<circle cx="40" cy="62" r="16" fill="#f1c9a5" /><path d="M14 100 Q14 82 40 80 Q66 82 66 100 Z" fill="#353a3d" /><circle cx="62" cy="38" r="4" fill="#ccc" /><circle cx="70" cy="28" r="6" fill="#ccc" /><ellipse cx="80" cy="12" rx="16" ry="10" fill="#ccc" /><text x="80" y="16" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="10" fill="#e24b4b">?!</text>')
KURVE = svg('<path d="M8 8 L8 92 L95 92" fill="none" stroke="#111" stroke-width="4" /><path d="M12 85 C40 82 60 70 90 15" fill="none" stroke="#1f7a4d" stroke-width="6" stroke-linecap="round" /><circle cx="90" cy="15" r="6" fill="#1f7a4d" />')
UHR = svg('<path d="M25 8 L75 8 L75 14 Q75 38 55 50 Q75 62 75 86 L75 92 L25 92 L25 86 Q25 62 45 50 Q25 38 25 14 Z" fill="#faf5ef" stroke="#353a3d" stroke-width="5" /><path d="M35 82 Q50 66 65 82 Z" fill="#f2c418" /><path d="M35 22 L65 22 Q60 36 50 42 Q40 36 35 22 Z" fill="#f2c418" />')
WARN = svg('<path d="M50 6 L96 90 L4 90 Z" fill="#f2c418" stroke="#111" stroke-width="5" stroke-linejoin="round" /><rect x="45" y="32" width="10" height="34" rx="5" fill="#111" /><circle cx="50" cy="78" r="6" fill="#111" />')
NOTIZ = svg('<rect x="18" y="6" width="64" height="88" rx="6" fill="#fff8d6" stroke="#353a3d" stroke-width="4" />' + "".join(f'<rect x="28" y="{20 + i * 14}" width="{44 - (i % 3) * 8}" height="5" rx="2" fill="#999" />' for i in range(5)) + '<path d="M78 70 L92 56 L96 60 L82 74 Z" fill="#DB8622" />')
GELDBEUTEL = svg('<rect x="8" y="26" width="84" height="56" rx="10" fill="#8a5a2b" /><rect x="8" y="26" width="84" height="16" rx="8" fill="#a8743f" /><rect x="66" y="46" width="28" height="18" rx="5" fill="#6b3f1f" /><path d="M30 20 L20 4 M50 18 L50 2 M70 20 L80 4" stroke="#e24b4b" stroke-width="5" stroke-linecap="round" />')
HANDY = svg('<rect x="28" y="4" width="44" height="92" rx="8" fill="#353a3d" /><rect x="33" y="14" width="34" height="70" rx="3" fill="#fff" /><rect x="38" y="22" width="24" height="5" rx="2" fill="#DB8622" />' + "".join(f'<rect x="38" y="{34 + i * 10}" width="24" height="4" rx="2" fill="#ccc" />' for i in range(4)))
SCHOCK = svg('<circle cx="50" cy="50" r="44" fill="#f2c418" /><circle cx="35" cy="40" r="8" fill="#fff" /><circle cx="65" cy="40" r="8" fill="#fff" /><circle cx="35" cy="40" r="4" fill="#111" /><circle cx="65" cy="40" r="4" fill="#111" /><ellipse cx="50" cy="70" rx="10" ry="13" fill="#5a1f1f" />')
STAPEL = svg("".join(f'<rect x="{20 + (i % 2) * 4}" y="{82 - i * 11}" width="60" height="10" rx="4" fill="#f2c418" stroke="#c99a06" stroke-width="2" />' for i in range(7)))
BANK = svg('<path d="M8 32 L50 8 L92 32 Z" fill="#DB8622" /><rect x="10" y="32" width="80" height="6" fill="#a8621a" /><g fill="#f6efe1" stroke="#353a3d" stroke-width="3"><rect x="17" y="40" width="10" height="40" /><rect x="37" y="40" width="10" height="40" /><rect x="55" y="40" width="10" height="40" /><rect x="73" y="40" width="10" height="40" /></g><rect x="8" y="80" width="84" height="9" fill="#353a3d" /><text x="50" y="27" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="13" fill="#fff">%</text>')
KAL3 = '<div style="display:flex;gap:28px">' + "".join(f'<div style="width:200px;height:200px">{svg(chr(10).join(["<rect x=\"8\" y=\"16\" width=\"84\" height=\"76\" rx=\"12\" fill=\"#fff\" stroke=\"#353a3d\" stroke-width=\"7\" />", "<rect x=\"8\" y=\"16\" width=\"84\" height=\"24\" rx=\"10\" fill=\"#1f7a4d\" />", f"<text x=\"50\" y=\"78\" text-anchor=\"middle\" font-family=\"Montserrat\" font-weight=\"800\" font-size=\"30\" fill=\"#353a3d\">{i + 1}</text>"]))}</div>' for i in range(3)) + "</div>"
WASCH = svg('<rect x="12" y="6" width="76" height="88" rx="8" fill="#f6efe1" stroke="#353a3d" stroke-width="4" /><line x1="12" y1="24" x2="88" y2="24" stroke="#353a3d" stroke-width="3" /><circle cx="50" cy="58" r="24" fill="#cfe6f5" stroke="#353a3d" stroke-width="4" /><path d="M70 4 Q80 -6 92 4" fill="none" stroke="#9aa3a8" stroke-width="5" /><path d="M14 24 L28 2" stroke="#e24b4b" stroke-width="5" />')
FLUG = svg('<path d="M10 55 L90 30 Q98 28 96 36 L60 52 L50 85 L42 85 L44 56 L22 62 L16 74 L10 74 L12 60 Z" fill="#3d7be0" />')
TASCHE = svg('<path d="M14 34 L86 34 L80 94 L20 94 Z" fill="#DB8622" /><path d="M34 34 Q34 10 50 10 Q66 10 66 34" fill="none" stroke="#a8621a" stroke-width="6" /><path d="M50 78 Q34 66 38 56 Q42 48 50 56 Q58 48 62 56 Q66 66 50 78 Z" fill="#fff" />')
GLOBUS = svg('<circle cx="50" cy="50" r="45" fill="#9ed0f0" /><path d="M24 28 Q34 20 44 28 Q46 38 36 40 Q30 46 24 40 Z M54 24 Q70 20 76 34 Q72 44 62 42 Q56 36 54 24 Z M40 58 Q54 54 58 66 Q54 80 44 84 Q38 74 40 58 Z M70 58 Q80 56 84 64 Q78 72 72 68 Z" fill="#2c9a63" /><circle cx="50" cy="50" r="45" fill="none" stroke="#353a3d" stroke-width="4" />')
FARBEN = ["#3d7be0", "#1f7a4d", "#DB8622", "#e24b4b", "#8a5a2b", "#9b59b6", "#f2c418", "#353a3d", "#2c9a63"]
KORB = svg("".join(f'<rect x="{24 + (i % 5) * 11}" y="{30 - (i // 5) * 10}" width="9" height="9" rx="2" fill="{FARBEN[i % 9]}" />' for i in range(10)) +
           '<path d="M10 42 L90 42 L80 88 L20 88 Z" fill="#DB8622" /><path d="M24 42 Q50 4 76 42" fill="none" stroke="#353a3d" stroke-width="5" />')
RASTER = svg("".join(f'<rect x="{6 + (i % 5) * 18}" y="{14 + (i // 5) * 24}" width="15" height="20" rx="3" fill="{"#e24b4b" if i == 7 else FARBEN[i % 9]}" />' for i in range(15)))
PREIS = svg('<path d="M4 25 L66 25 L96 50 L66 75 L4 75 Z" fill="#1f7a4d" /><circle cx="72" cy="50" r="5" fill="#fff" /><text x="34" y="58" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#fff">0,2 %</text>')
CHART7 = svg('<path d="M8 8 L8 92 L95 92" fill="none" stroke="#111" stroke-width="4" /><path d="M12 82 L24 74 L32 78 L44 62 L52 66 L64 48 L72 52 L88 24" fill="none" stroke="#1f7a4d" stroke-width="5" stroke-linejoin="round" /><text x="16" y="30" font-family="Abril Fatface" font-size="22" fill="#1f7a4d">~7 %</text>')
RECHNER = svg('<rect x="18" y="4" width="64" height="92" rx="10" fill="#353a3d" /><rect x="26" y="12" width="48" height="20" rx="4" fill="#cfe6f5" /><text x="70" y="28" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="14" fill="#111">7 %</text>' + "".join(
    f'<rect x="{26 + (i % 3) * 17}" y="{40 + (i // 3) * 17}" width="13" height="13" rx="3" fill="{"#DB8622" if i == 11 else "#fff"}" />' for i in range(12)))
SCHNEEBALL = svg('<circle cx="58" cy="58" r="34" fill="#eef4f8" stroke="#9aa3a8" stroke-width="3" /><circle cx="22" cy="80" r="8" fill="#eef4f8" stroke="#9aa3a8" stroke-width="2" /><path d="M6 92 L96 92" stroke="#9aa3a8" stroke-width="3" /><text x="58" y="66" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#1f7a4d">€€€</text>')
RAKETE = svg('<path d="M50 4 Q72 24 70 62 L30 62 Q28 24 50 4 Z" fill="#e24b4b" /><circle cx="50" cy="34" r="9" fill="#cfe6f5" stroke="#fff" stroke-width="3" /><path d="M30 50 L16 70 L30 66 Z M70 50 L84 70 L70 66 Z" fill="#a8321f" /><path d="M38 64 Q50 98 62 64 Z" fill="#f2c418" />')
CRASH = svg('<path d="M8 8 L8 92 L95 92" fill="none" stroke="#111" stroke-width="4" /><path d="M12 30 L30 24 L44 34 L56 28 L70 66 L80 58 L92 80" fill="none" stroke="#e24b4b" stroke-width="6" stroke-linejoin="round" />')
VERKAUF = svg('<rect x="10" y="30" width="80" height="40" rx="12" fill="#e24b4b" /><text x="50" y="58" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="20" fill="#fff">VERKAUFEN</text>')
NACHKAUF = svg('<path d="M8 8 L8 92 L95 92" fill="none" stroke="#111" stroke-width="4" /><path d="M12 30 L34 70 L50 62 L68 40 L90 18" fill="none" stroke="#1f7a4d" stroke-width="6" stroke-linejoin="round" /><circle cx="34" cy="70" r="8" fill="#f2c418" stroke="#c99a06" stroke-width="2" /><circle cx="50" cy="62" r="6" fill="#f2c418" stroke="#c99a06" stroke-width="2" />')
PFEILE = svg('<path d="M28 90 L28 22 M12 40 L28 20 L44 40" fill="none" stroke="#1f7a4d" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /><path d="M72 90 L72 58 M58 70 L72 54 L86 70" fill="none" stroke="#e24b4b" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" /><text x="28" y="14" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="10" fill="#1f7a4d">SPAREN</text><text x="72" y="50" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="9" fill="#e24b4b">AUSGABEN</text>')
FUNDAMENT = svg('<rect x="10" y="78" width="80" height="14" fill="#9aa3a8" /><rect x="18" y="64" width="20" height="12" fill="#DB8622" /><rect x="40" y="64" width="20" height="12" fill="#DB8622" /><rect x="62" y="64" width="20" height="12" fill="#DB8622" /><rect x="28" y="50" width="20" height="12" fill="#DB8622" /><rect x="52" y="50" width="20" height="12" fill="#e9a35a" opacity="0.5" />')
STERN = svg('<path d="M50 4 L62 36 L96 38 L70 60 L80 94 L50 74 L20 94 L30 60 L4 38 L38 36 Z" fill="#f2c418" stroke="#c99a06" stroke-width="4" stroke-linejoin="round" />')
TREPPE = svg("".join(f'<rect x="{6 + i * 18}" y="{78 - i * 15}" width="18" height="{14 + i * 15}" fill="{"#1f7a4d" if i % 2 else "#2c9a63"}" /><text x="{15 + i * 18}" y="{73 - i * 15}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="7" fill="#1f7a4d">+20</text>' for i in range(5)))
ZIEL = svg('<line x1="22" y1="8" x2="22" y2="96" stroke="#353a3d" stroke-width="5" /><path d="M24 10 L84 10 L84 50 L24 50 Z" fill="#fff" stroke="#353a3d" stroke-width="3" />' + "".join(
    f'<rect x="{24 + (i % 6) * 10}" y="{10 + (i // 6) * 10}" width="10" height="10" fill="#111" />' for i in range(24) if (i % 6 + i // 6) % 2 == 0))
DAUMEN = svg('<path d="M30 46 L46 12 Q56 10 56 22 L52 40 L84 40 Q94 42 90 54 L82 86 Q80 92 72 92 L30 92 Z" fill="#3d7be0" /><rect x="8" y="44" width="18" height="48" rx="4" fill="#3d7be0" />', w="100%")
TEILEN = svg('<circle cx="50" cy="50" r="46" fill="#DB8622" /><path d="M28 70 Q31 42 56 40 L56 26 L78 49 L56 72 L56 57 Q38 56 28 70 Z" fill="#fff" />')
BLASE = svg('<path d="M10 8 L90 8 Q96 8 96 14 L96 62 Q96 68 90 68 L40 68 L20 88 L24 68 L10 68 Q4 68 4 62 L4 14 Q4 8 10 8 Z" fill="#fff" stroke="#111" stroke-width="4" stroke-linejoin="round" /><circle cx="30" cy="38" r="6" fill="#111" /><circle cx="50" cy="38" r="6" fill="#111" /><circle cx="70" cy="38" r="6" fill="#111" />')
AUTO_PFEIL = svg('<rect x="4" y="30" width="22" height="40" rx="6" fill="#DB8622" /><text x="15" y="56" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="10" fill="#fff">1.</text><path d="M30 50 L58 50 M48 40 L60 50 L48 60" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />' + BANK.replace('<svg viewBox="0 0 100 100" style="width:100%;height:100%">', '<svg x="62" y="28" width="38" height="44" viewBox="0 0 100 100">'))


def coin(t, s=200, fs=70):
    return (f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:#f2c418;border:10px solid #c99a06;display:flex;align-items:center;'
            f'justify-content:center;font-family:\'Abril Fatface\';font-size:{fs}px;color:#7a5a00">{t}</div>')


def big(w, h, inner):
    return f'<div style="width:{w}px;height:{h}px">{inner}</div>'


def ICON(inner, w=620, h=620):
    return big(w, h, inner)


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


def folgen(text="+ Folgen"):
    html = ('<div class="mitte" style="flex-direction:row;gap:90px">'
            f'<div id="fo-dog" style="width:520px;height:520px">{BEAGLE}</div>'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;gap:36px">'
            '<div id="fo-name" style="font-weight:800;font-size:110px;color:#111">HundeFinanzTV</div>'
            f'<div id="fo-btn" style="padding:22px 70px;border-radius:70px;background:var(--brand);color:#fff;font-weight:800;font-size:68px">{text}</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#fo-dog", {t0}); pop("#fo-name", {t0} + 0.25); pop("#fo-btn", {t0} + 0.5); tl.fromTo("#fo-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 3 }}, {t0} + 1.0);')


def doppel(a, b):
    """Zwei Icons nebeneinander (links im Bildbereich)."""
    return f'<div style="display:flex;gap:40px;align-items:center">{big(340, 340, a)}{big(340, 340, b)}</div>'


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
