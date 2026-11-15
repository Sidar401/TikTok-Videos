"""Gemeinsame Helfer für Longforms im News-Format v2 (ab 15.11.): Szenen pro Satz, freie Hintergründe, Original-Logos auf Karte,
keine Kapitel, keine Quellen im Bild. Nutzung:
    from lf_kit import Kit
    K = Kit(HERE, anzahl_saetze, quer=False)
    K.szene("s1", "frei-…", html, js, sfx)
"""
import shutil
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "scripts"))
from analyse_kit import hintergrund_foto, kit_hg, rahmen, wechsel_js, zoom_js  # noqa: E402
from glow_short import t, zeiten  # noqa: E402


class Kit:
    def __init__(self, here, n, hgs, quer=False, logos=(), fotos=()):
        self.here, self.quer = Path(here), quer
        self.cap, self.st, self.en, self.dauer = zeiten(here)
        self.reihe = [f"s{i}" for i in range(1, n + 1)]
        self.SZ, self.SFX = [], []
        kit_hg(here, hgs)
        (self.here / "assets/logos").mkdir(parents=True, exist_ok=True)
        (self.here / "assets/fotos").mkdir(parents=True, exist_ok=True)
        for f in logos:
            shutil.copy(WURZEL / "brand/logos" / f, self.here / "assets/logos" / f)
        for f in fotos:
            shutil.copy(WURZEL / "brand/fotos" / f, self.here / "assets/fotos" / f)

    def bg(self, id_, key):
        h = hintergrund_foto(id_, key)
        return h.replace("width:1080px;height:1920px", "width:1920px;height:1080px") if self.quer else h

    def szene(self, sid, hg, html, js, sfx=(), bis=None):
        i = len(self.SZ)
        a = self.st(sid)
        b = self.st(bis) if bis else (self.st(self.reihe[self.reihe.index(sid) + 1]) if sid != self.reihe[-1] else self.dauer)
        self.SZ.append((a, b, (self.bg(f"bg{i}", hg) if hg else "") + rahmen(html, self.quer),
                        lambda a_, d_, j=js, k=i, h=hg: j(a_, d_) + (wechsel_js(f"z{k}", a_, k) if k else "") + (zoom_js(f"#bg{k}", a_, d_, 1.12) if h else "")))
        self.SFX.extend(sfx)


def tz(*a, **k):
    return t(*a, **k).replace('style="top:', 'style="z-index:5;top:', 1)


def logo(id_, datei, y, w, x=None, karte=True, glow="#ff8a1f", pad=22):
    """Original-Logo (gemeinfrei, Wikimedia) – karte=True: auf weißer Karte."""
    pos = f"left:{x}px" if x is not None else f"left:{(1080 - w) // 2}px"
    stil = (f"padding:{pad}px;border-radius:24px;background:#fff;box-shadow:0 0 60px {glow}66, 0 30px 50px #000" if karte
            else f"filter:drop-shadow(0 0 30px {glow}aa) drop-shadow(0 20px 30px #000)")
    return (f'<div id="{id_}" style="position:absolute;{pos};top:{y}px;width:{w}px;{stil};z-index:4">'
            f'<img src="assets/logos/{datei}" alt="" style="width:100%;display:block"/></div>')


def balken2(id_, links, rechts, wl, wr, fl, fr, basis=1150, hmax=460, unten=("", "")):
    """Zwei Balken nebeneinander (Werte relativ). links/rechts = Beschriftung oben."""
    m = max(wl, wr)
    hl, hr = int(hmax * wl / m), int(hmax * wr / m)
    return (f'<div id="{id_}a" style="position:absolute;left:220px;top:{basis - hl}px;width:240px;height:{hl}px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{fl},{fl}88);box-shadow:0 0 40px {fl}77;transform-origin:50% 100%;z-index:3"></div>'
            f'<div id="{id_}b" style="position:absolute;left:620px;top:{basis - hr}px;width:240px;height:{hr}px;border-radius:16px 16px 4px 4px;background:linear-gradient(180deg,{fr},{fr}88);box-shadow:0 0 40px {fr}77;transform-origin:50% 100%;z-index:3"></div>'
            f'<div id="{id_}ta" class="mono" style="position:absolute;left:140px;width:400px;top:{basis - hl - 70}px;text-align:center;font-size:48px;color:{fl};z-index:5">{links}</div>'
            f'<div id="{id_}tb" class="mono" style="position:absolute;left:540px;width:400px;top:{basis - hr - 70}px;text-align:center;font-size:48px;color:{fr};z-index:5">{rechts}</div>'
            f'<div class="mono" style="position:absolute;left:140px;width:400px;top:{basis + 14}px;text-align:center;font-size:30px;color:#ffffffcc;z-index:4">{unten[0]}</div>'
            f'<div class="mono" style="position:absolute;left:540px;width:400px;top:{basis + 14}px;text-align:center;font-size:30px;color:#ffffffcc;z-index:4">{unten[1]}</div>')


def balken2_js(id_, ta, tb):
    return (f' tl.fromTo("#{id_}a", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5 }}, {ta}); pop("#{id_}ta", {ta} + 0.3);'
            f' tl.fromTo("#{id_}b", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6 }}, {tb}); pop("#{id_}tb", {tb} + 0.4);')
