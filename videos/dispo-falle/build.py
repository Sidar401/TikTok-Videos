#!/usr/bin/env python3
"""HundeFinanzTV: Die Dispo-Falle (mit Kommentar-CTA)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import BEAGLE, SPARSCHWEIN, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


def big(id_, txt, top, size=120, col="#111", left=0, width=1080):
    return f'<div id="{id_}" class="big" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;font-size:{size}px;color:{col}">{txt}</div>'


def karte(betrag, col="#e24b4b"):
    return f"""<svg viewBox="0 0 400 250" style="width:100%;height:100%">
  <rect x="5" y="5" width="390" height="240" rx="26" fill="#353a3d" />
  <rect x="40" y="60" width="70" height="52" rx="10" fill="#f2c418" />
  <text x="360" y="200" text-anchor="end" font-family="Montserrat" font-weight="800" font-size="56" fill="{col}">{betrag}</text>
</svg>"""


def app(zeile1, wert, zeile2="", col="#111"):
    z2 = f'<text x="150" y="250" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="22" fill="#e24b4b">{zeile2}</text>' if zeile2 else ""
    return f"""<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" />
  <rect x="22" y="40" width="256" height="480" rx="20" fill="#fff" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" />
  <text x="150" y="120" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="26" fill="#888">{zeile1}</text>
  <text x="150" y="190" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="32" fill="{col}">{wert}</text>
  {z2}
  <rect x="50" y="300" width="200" height="14" rx="7" fill="#eee" /><rect x="50" y="335" width="160" height="14" rx="7" fill="#eee" />
</svg>"""


BANK = """<svg viewBox="0 0 400 360" style="width:100%;height:100%">
  <path d="M30 120 L200 30 L370 120 Z" fill="#353a3d" /><rect x="40" y="120" width="320" height="24" fill="#1a1a1a" />
  <g fill="#f6efe1" stroke="#353a3d" stroke-width="6"><rect x="70" y="150" width="40" height="150" /><rect x="150" y="150" width="40" height="150" /><rect x="230" y="150" width="40" height="150" /><rect x="300" y="150" width="40" height="150" /></g>
  <rect x="30" y="300" width="340" height="34" fill="#353a3d" />
</svg>"""
LEER = """<svg viewBox="0 0 300 320" style="width:100%;height:100%">
  <path d="M40 100 L260 100 L240 300 L60 300 Z" fill="#e8e1d6" stroke="#9aa3a8" stroke-width="8" />
  <path d="M100 100 Q100 30 150 30 Q200 30 200 100" fill="none" stroke="#9aa3a8" stroke-width="14" />
  <text x="150" y="235" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="90" fill="#9aa3a8">0</text>
</svg>"""
LEITER = """<svg viewBox="0 0 300 420" style="width:100%;height:100%">
  <rect x="0" y="300" width="300" height="120" rx="20" fill="#e24b4b" opacity="0.25" />
  <g stroke="#8a5a2b" stroke-width="16" stroke-linecap="round"><line x1="90" y1="20" x2="90" y2="400" /><line x1="210" y1="20" x2="210" y2="400" />
  <line x1="90" y1="80" x2="210" y2="80" /><line x1="90" y1="160" x2="210" y2="160" /><line x1="90" y1="240" x2="210" y2="240" /><line x1="90" y1="320" x2="210" y2="320" /></g>
</svg>"""
BLASE = """<svg viewBox="0 0 300 260" style="width:100%;height:100%">
  <path d="M30 20 L270 20 Q290 20 290 40 L290 170 Q290 190 270 190 L120 190 L60 245 L75 190 L30 190 Q10 190 10 170 L10 40 Q10 20 30 20 Z" fill="#fff" stroke="#111" stroke-width="10" stroke-linejoin="round" />
  <circle cx="95" cy="105" r="16" fill="#111" /><circle cx="150" cy="105" r="16" fill="#111" /><circle cx="205" cy="105" r="16" fill="#111" />
</svg>"""
KAL = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><rect x="8" y="16" width="84" height="76" rx="12" fill="#fff" stroke="#353a3d" stroke-width="7" /><rect x="8" y="16" width="84" height="24" rx="10" fill="#1f7a4d" /><path d="M30 64 L45 78 L72 50" fill="none" stroke="#1f7a4d" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" /></svg>'
TAG = '<svg viewBox="0 0 100 100" style="width:100%;height:100%"><path d="M8 30 L62 30 L92 50 L62 70 L8 70 Z" fill="#3d7be0" /><text x="38" y="60" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="28" fill="#fff">%</text></svg>'


def schritt(id_, nr, txt, icon, top):
    return (f'<div id="{id_}" style="position:absolute;left:70px;top:{top}px;width:940px;display:flex;align-items:center;gap:28px;'
            f'padding:24px 32px;border-radius:30px;background:#faf5ef">'
            f'<div style="width:96px;height:96px;flex:none;border-radius:50%;background:var(--brand);color:#fff;font-family:Montserrat;font-weight:800;font-size:58px;display:flex;align-items:center;justify-content:center">{nr}</div>'
            f'<div style="flex:1;font-family:Montserrat;font-weight:800;font-size:54px;line-height:1.1;color:#111">{txt}</div>'
            f'<div style="width:120px;height:120px;flex:none">{icon}</div></div>')


SCENES = [
    ("intro", "s1", "s1",
     title("intro-title", 'Dein Dispo ist eine<br /><span style="color:#e24b4b">Kostenfalle</span>') +
     box("intro-karte", 240, 620, 600, 375, karte("−2.000 €")),
     lambda t0, d: snap_in("#intro-title", t0) + snap_in("#intro-karte", t0)),

    ("zinsen", "s2", "s2",
     box("zs-bank", 290, 330, 500, 450, BANK) + big("zs-num", "10 %+", 840, 200, "#e24b4b") +
     '<div id="zs-sub" style="position:absolute;left:0;top:1090px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:60px;color:#111">Zinsen pro Jahr</div>',
     lambda t0, d: f"""
      pop("#zs-bank", {t0});
      pop("#zs-num", {c('s2', 1)});
      pop("#zs-sub", {c('s2', 1)} + 0.2);"""),

    ("ueberzogen", "s3", "s3",
     box("uz-app", 390, 340, 300, 560, app("Girokonto", "−2.000,00 €", col="#e24b4b")) +
     big("uz-jahr", "12 Monate", 960, 100),
     lambda t0, d: f"""
      pop("#uz-app", {t0});
      pop("#uz-jahr", {c('s3', 2)});"""),

    ("kosten", "s4", "s4",
     big("ks-num", "−200 €", 470, 220, "#e24b4b") +
     '<div id="ks-sub" style="position:absolute;left:0;top:790px;width:1080px;text-align:center;font-family:Montserrat;font-weight:800;font-size:76px;color:#111">nur Zinsen</div>',
     lambda t0, d: f"""
      pop("#ks-num", {c('s4', 1)} - 0.2);
      tl.fromTo("#ks-num", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 }}, {c('s4', 1)} + 0.3);
      pop("#ks-sub", {c('s4', 1)} + 0.2);"""),

    ("nichts", "s5", "s5",
     box("ni-tasche", 290, 430, 500, 533, LEER),
     lambda t0, d: f"""
      pop("#ni-tasche", {t0});
      tl.fromTo("#ni-tasche", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {c('s5', 2)});"""),

    ("gemein", "s6", "s6",
     box("gm-app", 390, 340, 300, 560, app("verfügbar", "2.000,00 €", "davon alles Dispo!", "#1f7a4d")) +
     big("gm-txt", "fühlt sich echt an", 960, 84, "#e24b4b"),
     lambda t0, d: f"""
      pop("#gm-app", {t0});
      pop("#gm-txt", {c('s6', 2)});"""),

    ("raus", "s7", "s7",
     big("rs-txt", "So kommst<br />du raus", 340, 120, "#1f7a4d") + box("rs-leiter", 390, 680, 300, 420, LEITER),
     lambda t0, d: f"""
      pop("#rs-txt", {t0});
      tl.fromTo("#rs-leiter", {{ y: 120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t0} + 0.2);"""),

    ("schritte", "s8", "s10",
     schritt("st-1", "1", "Jeden Monat fest zurückzahlen", KAL, 380) +
     schritt("st-2", "2", "Notgroschen aufbauen", SPARSCHWEIN, 640) +
     schritt("st-3", "3", "Notfalls günstiger Ratenkredit", TAG, 900),
     lambda t0, d: f"""
      pop("#st-1", {t0});
      pop("#st-2", {S['s9']['start']});
      pop("#st-3", {S['s10']['start']});"""),

    ("frage", "s11", "s11",
     box("fr-dog", 290, 330, 500, 500, BEAGLE) + big("fr-q", "Schon mal im<br />Dispo gewesen?", 880, 96),
     lambda t0, d: f"""
      pop("#fr-dog", {t0});
      pop("#fr-q", {t0} + 0.2);"""),

    ("kommentar", "s12", "s12",
     box("km-blase", 290, 400, 500, 433, BLASE) + big("km-txt", "Schreib's ehrlich<br />in die Kommentare!", 900, 80, "var(--brand)"),
     lambda t0, d: f"""
      pop("#km-blase", {t0});
      tl.fromTo("#km-blase", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.35);
      pop("#km-txt", {t0} + 0.2);"""),

    ("outro", "s13", "s13", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
