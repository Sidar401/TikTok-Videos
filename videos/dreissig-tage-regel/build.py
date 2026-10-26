#!/usr/bin/env python3
"""HundeFinanzTV: Die 30-Tage-Regel (Kommentar-CTA als Text, da nicht eingesprochen). Leitmotiv: Wunschzettel + Kalender, der 30 Tage abhakt."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import T, box, build, cap, snap_in, title  # noqa: E402
from icons import TASCHE  # noqa: E402
from kurz_szenen import GRUEN, OR, ROT, big, chip, outro_cta, outro_cta_js, sub  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


SHOP = f"""<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" />
  <rect x="22" y="40" width="256" height="480" rx="20" fill="#fff" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" />
  <rect x="50" y="80" width="200" height="180" rx="16" fill="#faf5ef" />
  <path d="M90 210 Q90 140 150 140 Q210 140 210 210 Z" fill="{OR}" /><rect x="80" y="205" width="140" height="22" rx="8" fill="#353a3d" />
  <text x="150" y="310" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="34" fill="#111">Sneaker</text>
  <text x="150" y="360" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="{ROT}">120 €</text>
  <rect id="sh-btn" x="50" y="400" width="200" height="70" rx="35" fill="{OR}" />
  <text x="150" y="447" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="24" fill="#fff">JETZT KAUFEN</text>
</svg>"""

TAGE = "".join(f'<div class="tg" style="position:relative;width:110px;height:110px;border-radius:18px;background:#faf5ef;border:4px solid #353a3d;'
               f'font-family:Montserrat;font-weight:800;font-size:40px;color:#353a3d;display:flex;align-items:center;justify-content:center">{i + 1}'
               f'<svg class="tx" viewBox="0 0 100 100" style="position:absolute;inset:8px;width:auto;height:auto"><path d="M15 15 L85 85 M85 15 L15 85" stroke="{ROT}" '
               f'stroke-width="12" stroke-linecap="round" /></svg></div>' for i in range(30))

ZETTEL = f"""<div id="ze" style="position:absolute;left:150px;top:380px;width:780px;padding:40px 50px;border-radius:24px;background:#fff8d6;
  border:5px solid #c99a06;font-family:Montserrat;font-weight:800;color:#111">
  <div style="font-size:58px;color:{OR};margin-bottom:24px">Meine Wunschliste</div>
  <div id="ze-1" style="display:flex;justify-content:space-between;font-size:50px;border-bottom:3px dashed #c99a06;padding:14px 0"><span>Sneaker</span><span>120 €</span><span style="color:#888">3.11.</span></div>
  <div id="ze-2" style="display:flex;justify-content:space-between;font-size:50px;border-bottom:3px dashed #c99a06;padding:14px 0"><span>Kopfhörer</span><span>89 €</span><span style="color:#888">5.11.</span></div>
</div>"""

BLASE_WUNSCH = f"""<svg viewBox="0 0 400 320" style="width:100%;height:100%">
  <path d="M60 20 L340 20 Q380 20 380 60 L380 200 Q380 240 340 240 L170 240 L100 300 L115 240 L60 240 Q20 240 20 200 L20 60 Q20 20 60 20 Z" fill="#faf5ef" stroke="#353a3d" stroke-width="10" />
  <path d="M150 170 Q150 90 200 90 Q250 90 250 170 Z" fill="{OR}" /><rect x="140" y="165" width="120" height="20" rx="8" fill="#353a3d" /></svg>"""

MOND = """<svg viewBox="0 0 300 300" style="width:100%;height:100%"><circle cx="150" cy="150" r="140" fill="#353a3d" />
  <path d="M170 60 A95 95 0 1 0 230 220 A75 75 0 1 1 170 60 Z" fill="#f2c418" />
  <text x="190" y="110" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">Zzz</text></svg>"""

SCENES = [
    ("hook", "s1", "s1",
     title("hk-t", 'Sofort haben<br /><span style="color:#DB8622">wollen?</span>', 290, 104) +
     box("hk-h", 390, 560, 300, 560, SHOP),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-h", t0) +
     f'\n      tl.fromTo("#sh-btn", {{ scale: 1, svgOrigin: "150 435" }}, {{ scale: 1.1, svgOrigin: "150 435", duration: 0.25, yoyo: true, repeat: 5 }}, {t0} + 0.6);'),

    ("regel", "s2", "s2",
     big("rg-t", '30-Tage-<br /><span style="color:#DB8622">Regel</span>', 320, 150) +
     box("rg-b", 390, 720, 300, 300, TASCHE),
     lambda t0, d: f"""
      pop("#rg-t", {c('s2', 1)} - 0.2);
      pop("#rg-b", {c('s2', 1)});"""),

    ("liste", "s3", "s3",
     ZETTEL + sub("ze-s", "mit Datum und Preis", 950, 62, GRUEN),
     lambda t0, d: f"""
      pop("#ze", {t0});
      pop("#ze-1", {c('s3', 1)});
      pop("#ze-2", {c('s3', 1)} + 0.6);
      pop("#ze-s", {c('s3', 2)});"""),

    ("warten", "s4", "s4",
     f'<div id="wa-k" style="position:absolute;left:105px;top:330px;width:870px;display:grid;grid-template-columns:repeat(6,130px);gap:18px">{TAGE}</div>',
     lambda t0, d: f"""
      pop("#wa-k", {t0});
      tl.fromTo(".tx", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.12, stagger: {round((d - 0.6) / 30, 3)} }}, {t0} + 0.3);"""),

    ("danach", "s5", "s5",
     big("da-t", "Immer noch?", 360, 130) +
     chip("da-k", "✓ Dann kauf's ohne schlechtes Gewissen", GRUEN, 0, 640, 50, center=True),
     lambda t0, d: f"""
      pop("#da-t", {t0});
      pop("#da-k", {c('s5', 2)});"""),

    ("weg", "s6", "s7",
     box("we-b", 290, 330, 500, 400, BLASE_WUNSCH) +
     big("we-t", "Wunsch weg!", 800, 130, GRUEN) +
     sub("we-s", "Viele Käufe = nur der Moment", 1000, 58, OR),
     lambda t0, d: f"""
      pop("#we-b", {t0});
      tl.to("#we-b", {{ opacity: 0.12, scale: 0.85, duration: 0.8, ease: "power2.in" }}, {c('s6', 2)});
      pop("#we-t", {c('s6', 2)} + 0.3);
      pop("#we-s", {S['s7']['start']});"""),

    ("rechnung", "s8", "s9",
     big("re-a", "3 × 50 € × 12", 360, 110) +
     big("re-b", "0 €", 540, 180, ROT) +
     big("re-c", "nur die Hälfte verhindert:", 830, 70, "#555c60") +
     big("re-d", "+900 € / Jahr", 940, 130, GRUEN),
     lambda t0, d: f"""
      pop("#re-a", {c('s8', 1)});
      pop("#re-b", {c('s8', 3)} - 0.2);
      zaehl("#re-b", 0, 1800, {c('s8', 3)} - 0.2, 1.2, " €");
      pop("#re-c", {S['s9']['start']});
      pop("#re-d", {c('s9', 2)});"""),

    ("nacht", "s10", "s10",
     sub("na-k", "Kleine Beträge?", 340, 70, OR) +
     box("na-m", 340, 470, 400, 400, MOND) +
     big("na-t", "1 Nacht drüber<br />schlafen", 940, 100),
     lambda t0, d: f"""
      pop("#na-k", {t0});
      pop("#na-m", {t0} + 0.2);
      pop("#na-t", {c('s10', 1)});"""),

    ("outro", "sF", "sF", outro_cta("Dein letzter Fehlkauf?<br />Schreib's in die Kommentare!"), outro_cta_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
