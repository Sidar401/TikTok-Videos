#!/usr/bin/env python3
"""HundeFinanzTV Short (9:16) aus longform-lotto: Marcos Jahr 1 – Cliffhanger aufs Hauptvideo.
Voice = Ausschnitte der Longform-Voice (scripts/kurz.py), keine neuen Credits."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from shorts import DUNKEL, GRUEN, ORANGE, ROT, build, endkarte  # noqa: E402
from icons import TV, person  # noqa: E402
from lf_szenen import Zeit  # noqa: E402

Z = Zeit(HERE)
st = Z.st
BLAU, LILA = "#3d7be0", "#9b59b6"
KUGEL_F = [ROT, BLAU, GRUEN, ORANGE, LILA, "#c99a06"]


def eur(v):
    return f"{v:,.0f} €".replace(",", ".")


def kugeln(gr=120):
    return "".join(f'<div id="ku-{i}" style="width:{gr}px;height:{gr}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 12%,{c} 13%);'
                   f'display:flex;align-items:center;justify-content:center"><div style="width:{gr * 0.55:.0f}px;height:{gr * 0.55:.0f}px;border-radius:50%;background:#fff;'
                   f'color:#111;font-weight:900;font-size:{gr * 0.28:.0f}px;display:flex;align-items:center;justify-content:center">{z}</div></div>'
                   for i, (z, c) in enumerate(zip([7, 13, 21, 29, 36, 42], KUGEL_F)))


def hook():
    html = (f'<div class="mitte" style="gap:56px"><div style="display:flex;gap:18px">{kugeln()}</div>'
            '<div id="hk-t" class="serif" style="font-size:150px;line-height:1;color:#c99a06">1.000.000 €</div>'
            '<div id="hk-s" style="font-weight:800;font-size:66px;line-height:1.2;color:#111">im Lotto gewonnen …</div>'
            '<div id="hk-r" style="padding:16px 40px;border-radius:24px;background:#e24b4b;color:#fff;font-weight:900;font-size:62px">… und nach 1 Jahr?</div></div>')

    def js(t0, d):
        return ("".join(f' tl.fromTo("#ku-{i}", {{ y: -30 }}, {{ y: 0, duration: 0.5, ease: "bounce.out" }}, {t0} + {i * 0.06:.2f});' for i in range(6))
                + f' tl.fromTo("#hk-t", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.5 }}, {t0}); tl.fromTo("#hk-s", {{ scale: 1.04 }}, {{ scale: 1, duration: 0.4 }}, {t0});'
                f' pop("#hk-r", {t0} + 1.6);')
    return dict(html=html, js=js)


def jackpot():
    jp = Z.S["s14"]["captions"][-1]["start"]
    html = ('<div class="mitte" style="gap:40px"><div style="display:flex;align-items:flex-end;gap:50px">'
            f'<div id="jp-p" style="width:280px;height:380px">{person(ORANGE, "#353a3d")}</div><div id="jp-tv" style="width:380px;height:380px">{TV}</div></div>'
            '<div id="jp-c" class="chip" style="background:#353a3d">Marco · 32 · Lagerist</div>'
            '<div id="jp-j" style="padding:18px 56px;border-radius:30px;background:#f2c418;color:#111;font-weight:900;font-size:120px;transform:rotate(-4deg)">JACKPOT!</div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#jp-p", {t0}); pop("#jp-tv", {t0} + 0.2); pop("#jp-c", {t0} + 0.5); pop("#jp-j", {jp});'
                f' tl.fromTo("#jp-j", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3 }}, {st("s15")});'
                f' tl.fromTo("#jp-p", {{ x: 0 }}, {{ x: -8, duration: 0.08, yoyo: true, repeat: 9 }}, {st("s15")} + 0.5);')


def konto(uid, start, schritte, zeilen, titel="Marcos Konto", farbe=GRUEN):
    """Kontostand oben (zählt live), darunter Zeilen, die nacheinander erscheinen."""
    stil = {"h": "font-family:'Abril Fatface',serif;font-size:76px;line-height:1.05;color:#111",
            "s": "font-weight:800;font-size:52px;line-height:1.2;color:#353a3d",
            "k": "font-weight:700;font-size:44px;line-height:1.2;color:#555c60",
            "r": "font-weight:800;font-size:52px;line-height:1.2;color:#e24b4b",
            "g": "font-weight:800;font-size:52px;line-height:1.2;color:#1f7a4d"}
    rechts = "".join(f'<div id="{uid}-z{k}" style="{stil[a]}">{t}</div>' for k, (t, _, a) in enumerate(zeilen))
    html = (f'<div style="position:absolute;left:110px;top:330px;width:860px;padding:40px 50px;border-radius:40px;background:{DUNKEL};box-shadow:0 16px 0 #000">'
            f'<div style="font-weight:800;font-size:40px;color:#9aa3a8;letter-spacing:2px">{titel.upper()}</div>'
            f'<div id="{uid}-n" style="font-family:\'Abril Fatface\',serif;font-size:124px;color:{farbe};margin:16px 0 26px;white-space:nowrap">{eur(start)}</div>'
            f'<div style="height:44px;border-radius:22px;background:#3a4045;overflow:hidden"><div id="{uid}-b" style="height:100%;width:100%;border-radius:22px;background:{farbe};'
            f'transform-origin:left center;transform:scaleX({min(start, 1e6) / 1e6:.3f})"></div></div>'
            f'<div style="display:flex;justify-content:space-between;font-weight:700;font-size:28px;color:#9aa3a8;margin-top:10px"><span>0 €</span><span>1 Mio. €</span></div></div>'
            f'<div style="position:absolute;left:70px;top:820px;width:940px;height:500px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:20px;text-align:center">{rechts}</div>')

    def js(t0, d):
        out = [f'const {uid}o = {{ v: {start} }};']
        alt = start
        for sid, neu in schritte:
            a = Z.euro_zeit(sid) + 0.2
            out.append(f'tl.fromTo({uid}o, {{ v: {alt} }}, {{ v: {neu}, duration: 1.4, ease: "power1.inOut", onUpdate: () => {{ '
                       f'document.querySelector("#{uid}-n").textContent = Math.round({uid}o.v).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " €"; }} }}, {a});')
            out.append(f'tl.fromTo("#{uid}-b", {{ scaleX: {min(alt, 1e6) / 1e6:.3f} }}, {{ scaleX: {min(neu, 1e6) / 1e6:.3f}, duration: 1.4, ease: "power1.inOut" }}, {a});')
            alt = neu
        for k, (_, sid, _) in enumerate(zeilen):
            a = st(sid) if sid else t0
            out.append(f'tl.fromTo("#{uid}-z{k}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {max(a, t0 + 0.1)});')
        return " ".join(out)
    return dict(html=html, js=js)


SZENEN = [
    ("s1", "s1", "frei", hook()),
    ("s14", "s15", "frei", jackpot()),
    ("s35", "s40", "frei", konto("k1", 1_000_000, [("s36", 500_000), ("s37", 420_000), ("s38", 370_000), ("s39", 300_000)],
                                 [("Job gekündigt", "s35", "r"), ("Haus: 500.000 € bar", "s36", "s"), ("Sportwagen: 80.000 €", "s37", "s"),
                                  ("Reise mit Freunden", "s38", "s"), ("Uhren · Technik · Shopping", "s39", "k")])),
    ("s41", "s47", "frei", konto("k2", 300_000, [("s43", 200_000)],
                                 [("Plötzlich melden sich alle", None, "h"), ("Geschäft · Hochzeit · …", "s42", "k"), ("100.000 € verliehen", "s43", "r"),
                                  ("nach 1 Jahr: noch 200.000 €", "s45", "s"), ("„Ist doch noch genug da“", "s47", "r")])),
    ("s22", "s22", "frei", endkarte("Und dann wird's richtig bitter …", "Jahr 2 – 4: der Absturz")),
]

if __name__ == "__main__":
    build(HERE, SZENEN, "Ausschnitt · ganzes Video auf YouTube")
