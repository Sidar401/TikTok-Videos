#!/usr/bin/env python3
"""HundeFinanzTV: Die 52-Wochen-Challenge (Teilen-CTA). Leitmotiv: Sparglas, das sich füllt + Wochen-Treppe."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from finanz import CHECK, T, box, build, cap, outro, outro_js, snap_in, title  # noqa: E402
from icons import TEILEN  # noqa: E402

t = T(HERE)
S = {s["id"]: s for s in t["saetze"]}
GRUEN, ROT, OR, GOLD = "#1f7a4d", "#e24b4b", "#DB8622", "#f2c418"


def c(sid, i):
    return cap(t, sid, i)


def big(id_, txt, top, size=120, col="#111"):
    return f'<div id="{id_}" class="big" style="position:absolute;left:0;top:{top}px;width:1080px;font-size:{size}px;line-height:1.05;color:{col}">{txt}</div>'


def glas(uid, fuell=None):
    """Sparglas; #uid-f ist die Füllung (scaleY), #uid-m Münzen-Glanz."""
    return f"""<svg viewBox="0 0 300 380" style="width:100%;height:100%">
  <defs><clipPath id="{uid}-k"><path d="M50 90 L250 90 L250 330 Q250 360 220 360 L80 360 Q50 360 50 330 Z" /></clipPath></defs>
  <rect x="70" y="40" width="160" height="40" rx="10" fill="#8a5a2b" />
  <g clip-path="url(#{uid}-k)"><g id="{uid}-f"{"" if fuell is None else f' transform="translate(0 {360 * (1 - fuell):.1f}) scale(1 {fuell})"'}>
    <rect x="40" y="90" width="220" height="280" fill="{GOLD}" />
    {''.join(f'<ellipse cx="{70 + (i % 4) * 52}" cy="{110 + (i // 4) * 40}" rx="22" ry="9" fill="#c99a06" opacity="0.6" />' for i in range(24))}
  </g></g>
  <path d="M50 90 L250 90 L250 330 Q250 360 220 360 L80 360 Q50 360 50 330 Z" fill="none" stroke="#353a3d" stroke-width="10" />
  <rect x="70" y="120" width="18" height="180" rx="9" fill="#fff" opacity="0.6" />
</svg>"""


def treppe(uid, n=52, rueck=False, w=900, h=420):
    bw = w / n
    bars = "".join(
        f'<rect class="{uid}-b" x="{i * bw + 1:.1f}" y="{h - h * ((n - i) if rueck else (i + 1)) / n:.1f}" width="{bw - 2:.1f}" '
        f'height="{h * ((n - i) if rueck else (i + 1)) / n:.1f}" fill="{OR if (i + 1) % 13 else GRUEN}" />' for i in range(n))
    return f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:100%"><line x1="0" y1="{h}" x2="{w}" y2="{h}" stroke="#111" stroke-width="6" />{bars}</svg>'


def woche(id_, nr, betrag, top):
    return (f'<div id="{id_}" style="position:absolute;left:150px;top:{top}px;width:780px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:26px 44px;border-radius:30px;background:#faf5ef;font-family:Montserrat;font-weight:800;font-size:62px;color:#111">'
            f'<span>Woche {nr}</span><span style="color:{GRUEN}">+ {betrag}</span></div>')


KAL = "".join(f'<div class="kz" style="width:56px;height:56px;border-radius:12px;background:{GRUEN if (i + 1) % 13 == 0 else OR}"></div>' for i in range(52))
PFEIL = f'<svg viewBox="0 0 200 120" style="width:100%;height:100%"><path d="M180 60 L40 60 M80 20 L36 60 L80 100" fill="none" stroke="{OR}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" /></svg>'

SCENES = [
    ("hook", "s1", "s1",
     title("hk-t", 'Am Monatsende<br /><span style="color:#e24b4b">nie was übrig?</span>', 300, 104) +
     box("hk-g", 340, 620, 400, 507, glas("g0", 0.04)),
     lambda t0, d: snap_in("#hk-t", t0) + snap_in("#hk-g", t0) +
     f'\n      tl.fromTo("#hk-g", {{ rotation: -4 }}, {{ rotation: 4, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {c("s1", 2)});'),

    ("challenge", "s2", "s3",
     big("ch-t", '52-Wochen-<br /><span style="color:#DB8622">Challenge</span>', 300, 130) +
     f'<div id="ch-k" style="position:absolute;left:115px;top:660px;width:850px;display:grid;grid-template-columns:repeat(13,56px);gap:10px">{KAL}</div>' +
     big("ch-r", "Die Regel:", 1000, 90, GRUEN),
     lambda t0, d: f"""
      pop("#ch-t", {c('s2', 1)});
      tl.fromTo(".kz", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.2, stagger: 0.025, ease: "back.out(2)" }}, {c('s2', 1)} + 0.3);
      pop("#ch-r", {S['s3']['start']});"""),

    ("wochen", "s4", "s6",
     woche("wo-1", 1, "1 €", 360) + woche("wo-2", 2, "2 €", 560) + woche("wo-3", 3, "3 €", 760) +
     big("wo-m", "jede Woche <span style='color:#1f7a4d'>+1 €</span>", 1010, 92),
     lambda t0, d: f"""
      pop("#wo-1", {t0});
      pop("#wo-2", {c('s5', 0)});
      pop("#wo-3", {c('s5', 1)});
      pop("#wo-m", {c('s6', 1)});"""),

    ("treppe", "s7", "s8",
     box("tr-c", 90, 560, 900, 420, treppe("tr")) +
     big("tr-k", "kaum spürbar …", 330, 90, "#9aa3a8") +
     big("tr-e", "Woche 52: <span style='color:#e24b4b'>52 €</span>", 330, 96),
     lambda t0, d: f"""
      tl.fromTo(".tr-b", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.25, stagger: {round((d - 1.2) / 52, 3)}, ease: "power2.out" }}, {t0});
      pop("#tr-k", {t0} + 0.2);
      tl.to("#tr-k", {{ opacity: 0, duration: 0.2 }}, {c('s8', 1)} - 0.2);
      pop("#tr-e", {c('s8', 2)});"""),

    ("summe", "s9", "s11",
     box("su-g", 340, 300, 400, 507, glas("g1")) +
     big("su-n", "0 €", 850, 190, GRUEN) +
     f'<div id="su-c" style="position:absolute;left:0;top:1080px;width:1080px;display:flex;justify-content:center;align-items:center;gap:24px">'
     f'<div style="width:100px;height:100px">{CHECK}</div><span style="font-family:Montserrat;font-weight:800;font-size:60px;color:#111">fast ohne Verzicht</span></div>',
     lambda t0, d: f"""
      pop("#su-g", {t0});
      tl.fromTo("#g1-f", {{ scaleY: 0.02, svgOrigin: "150 360" }}, {{ scaleY: 0.95, svgOrigin: "150 360", duration: 2.2, ease: "power1.inOut" }}, {t0} + 0.4);
      pop("#su-n", {S['s10']['start']} - 0.3);
      zaehl("#su-n", 0, 1378, {S['s10']['start']} - 0.3, 1.6, " €");
      tl.fromTo("#su-n", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }}, {S['s10']['start']} + 1.4);
      pop("#su-c", {S['s11']['start']});"""),

    ("rueckwaerts", "s12", "s13",
     big("rw-t", 'Unser Tipp:<br /><span style="color:#DB8622">rückwärts!</span>', 300, 110) +
     box("rw-p", 440, 560, 200, 120, PFEIL) +
     box("rw-c", 90, 720, 900, 300, treppe("rw", rueck=True, h=300)) +
     '<div id="rw-a" style="position:absolute;left:90px;top:1060px;font-family:Montserrat;font-weight:800;font-size:54px;color:#1f7a4d">Januar: 52 €</div>' +
     '<div id="rw-b" style="position:absolute;right:90px;top:1060px;font-family:Montserrat;font-weight:800;font-size:54px;color:#DB8622">Dezember: 1 €</div>',
     lambda t0, d: f"""
      pop("#rw-t", {t0});
      pop("#rw-p", {c('s12', 1)});
      tl.fromTo(".rw-b", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.2, stagger: 0.03, ease: "power2.out" }}, {S['s13']['start']});
      pop("#rw-a", {c('s13', 0)} + 0.4);
      pop("#rw-b", {c('s13', 3)});"""),

    ("teilen", "s14", "s15",
     box("te-i", 340, 380, 400, 400, TEILEN) +
     big("te-t", "Teile das Video<br />mit deinem Spar-Buddy!", 880, 76, OR),
     lambda t0, d: f"""
      pop("#te-i", {t0});
      tl.fromTo("#te-i", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {t0} + 0.4);
      pop("#te-t", {S['s15']['start']});"""),

    ("outro", "s16", "s16", outro(0), outro_js),
]

if __name__ == "__main__":
    build(HERE, SCENES)
