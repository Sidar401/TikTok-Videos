#!/usr/bin/env python3
"""HundeFinanzTV: Wie lange musst du dafür arbeiten? (Teilen-CTA). Leitmotiv: Preis → Arbeitsstunden-Uhr."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402
from icons import DENKEN, RECHNER, TEILEN, UHR, person  # noqa: E402
from kurz_szenen import GRUEN, OR, ROT, big, chip, sub  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}


def c(sid, i):
    return cap(t, sid, i)


HANDY = f"""<svg viewBox="0 0 300 560" style="width:100%;height:100%">
  <rect x="5" y="5" width="290" height="550" rx="44" fill="#353a3d" /><rect x="22" y="40" width="256" height="480" rx="20" fill="#cfe6f5" />
  <rect x="110" y="18" width="80" height="12" rx="6" fill="#1a1a1a" /></svg>"""

WOCHEN = "".join(f'<div class="wt" style="width:150px;height:150px;border-radius:24px;background:{OR};display:flex;align-items:center;justify-content:center;'
                 f'font-family:Montserrat;font-weight:800;font-size:44px;color:#fff">{d}</div>' for d in ["Mo", "Di", "Mi", "Do", "Fr"] * 2)

SCENES = [
    ("hook", "s1", "s2",
     title("hk-t", 'Wie lange musst du<br />dafür <span style="color:#DB8622">arbeiten?</span>', 300, 92) +
     box("hk-u", 340, 600, 400, 400, UHR),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-u", t0) +
     f'\n      tl.fromTo("#hk-u", {{ rotation: 0 }}, {{ rotation: 180, duration: 0.7, ease: "power2.inOut" }}, {S["s2"]["start"]});'),

    ("gehalt", "s3", "s3",
     box("ge-p", 340, 330, 400, 520, person(OR, "#353a3d")) +
     chip("ge-a", "2.000 € netto", GRUEN, 0, 900, 62, center=True) +
     chip("ge-b", "160 Stunden / Monat", "#3d7be0", 0, 1040, 62, center=True),
     lambda t0, d: f"""
      pop("#ge-p", {t0});
      pop("#ge-a", {c('s3', 1)});
      pop("#ge-b", {c('s3', 2)});"""),

    ("lohn", "s4", "s4",
     sub("lo-r", "2.000 € ÷ 160 Std.", 420, 72, "#555c60") +
     big("lo-z", "12,50 €", 560, 210, GRUEN) +
     sub("lo-s", "pro Stunde", 830, 72),
     lambda t0, d: f"""
      pop("#lo-r", {t0});
      pop("#lo-z", {c('s4', 1)});
      pop("#lo-s", {c('s4', 1)} + 0.2);"""),

    ("handy", "s5", "s6",
     box("ha-h", 110, 360, 260, 485, HANDY) +
     chip("ha-p", "1.000 €", ROT, 120, 880, 64) +
     '<svg id="ha-a" viewBox="0 0 200 100" style="position:absolute;left:420px;top:540px;width:180px;height:90px"><path d="M10 50 L170 50 M130 15 L175 50 L130 85" fill="none" stroke="#DB8622" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" /></svg>' +
     big("ha-z", "80 Std.", 540, 120, OR).replace("left:0;", "left:600px;").replace("width:1080px", "width:440px;white-space:nowrap") +
     f'<div id="ha-w" style="position:absolute;left:60px;top:1010px;width:960px;display:grid;grid-template-columns:repeat(5,150px);gap:20px 52px;justify-content:center">{WOCHEN}</div>',
     lambda t0, d: f"""
      pop("#ha-h", {t0});
      pop("#ha-p", {c('s5', 1)});
      pop("#ha-a", {c('s5', 2)});
      pop("#ha-z", {c('s5', 2)} + 0.2);
      zaehl("#ha-z", 0, 80, {c('s5', 2)} + 0.2, 1.0, " Std.");
      tl.fromTo(".wt", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.18, stagger: 0.08, ease: "back.out(2)" }}, {S['s6']['start']});"""),

    ("anders", "s7", "s7",
     box("an-d", 340, 360, 400, 400, DENKEN) +
     big("an-t", "Plötzlich teuer?!", 840, 110, ROT),
     lambda t0, d: f"""
      pop("#an-d", {t0});
      pop("#an-t", {c('s7', 1)});"""),

    ("rechnen", "s8", "s8",
     box("re-r", 390, 340, 300, 400, RECHNER) +
     big("re-t", "Deinen Stundenlohn<br />ausrechnen", 800, 92, GRUEN) +
     sub("re-s", "bei jedem größeren Kauf", 1040, 58, OR),
     lambda t0, d: f"""
      pop("#re-r", {t0});
      pop("#re-t", {c('s8', 1)} - 0.3);
      pop("#re-s", {c('s8', 2)});"""),

    ("teilen", "s9", "s9",
     box("te-i", 340, 380, 400, 400, TEILEN) +
     big("te-t", "Teile das Video!", 880, 100, OR),
     lambda t0, d: f"""
      pop("#te-i", {t0});
      tl.fromTo("#te-i", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#te-t", {c('s9', 2)});"""),

    ("outro", "s10", "s10", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
