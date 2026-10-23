"""Wiederverwendbare Szenen-Bausteine für 16:9-Longform-Videos (Kassenzettel, Balken, Kapitelkarten)."""
import json
from pathlib import Path

from longform import ORANGE, ROT


class Zeit:
    """Satz-Zeiten aus timings.json eines Videos."""

    def __init__(self, here):
        t = json.loads((Path(here) / "timings.json").read_text())
        self.S = {s["id"]: s for s in t["saetze"]}

    def st(self, sid):
        return self.S[sid]["start"]

    def euro_zeit(self, sid):
        """Zeitpunkt, an dem im Satz der Euro-Betrag gesprochen wird (erste Caption mit €)."""
        for c in self.S[sid]["captions"]:
            if "€" in c["text"]:
                return c["start"]
        return self.st(sid)


def eur(v):
    return f"{v:,} €".replace(",", ".")


def karte(nr_text, titel, farbe=ORANGE, uid="ka"):
    html = (f'<div class="mitte"><div class="kap"><div class="nr" id="{uid}-n" style="background:{farbe}">{nr_text}</div>'
            f'<div class="t" id="{uid}-t">{titel}</div></div></div>')
    return dict(html=html, js=lambda t0, d: f'pop("#{uid}-n", {t0}); tl.fromTo("#{uid}-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {t0} + 0.15);')


def beleg(z, uid, titel, intro_icon, posten, ende_sid, summe_text, fs=38):
    """Kassenzettel: links wechselnde Icons, rechts füllt sich die Liste mit laufender Summe.
    posten = [(icon_ab_sid, betrag_sid, icon, label, betrag)]; betrag None = nur Bildwechsel, keine Zeile."""
    zeilen_p = [p for p in posten if p[4] is not None]
    icons = [(None, intro_icon)] + [(p[0], p[2]) for p in posten]
    bild = "".join(f'<div id="{uid}-i{k}" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0">{ic}</div>'
                   for k, (_, ic) in enumerate(icons))
    zeilen = "".join(f'<div id="{uid}-r{k}" style="display:flex;justify-content:space-between;font-weight:700;font-size:{fs}px;color:#353a3d;padding:{round(fs * 0.18)}px 0;opacity:0">'
                     f'<span>{p[3]}</span><span style="font-weight:800;color:#111">{eur(p[4])}</span></div>'
                     for k, p in enumerate(zeilen_p))
    summen, s = [], 0
    for p in zeilen_p:
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
        zeiten = [t0] + [z.st(p[0]) for p in posten]
        for k, a in enumerate(zeiten):
            if k == 0 and len(zeiten) > 1 and zeiten[1] <= t0 + 0.05:
                continue  # erster Posten startet sofort: Start-Bild gar nicht zeigen
            out.append(f'tl.fromTo("#{uid}-i{k}", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, {a});')
            if k + 1 < len(zeiten):
                out.append(f'tl.to("#{uid}-i{k}", {{ opacity: 0, duration: 0.2 }}, {zeiten[k + 1] - 0.2});')
        for k, p in enumerate(zeilen_p):
            a = z.euro_zeit(p[1])
            out.append(f'tl.fromTo("#{uid}-r{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {a});')
            out.append(f'tl.fromTo("#{uid}-s{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {a});')
            if k:
                out.append(f'tl.to("#{uid}-s{k - 1}", {{ opacity: 0, duration: 0.2 }}, {a});')
        e = z.euro_zeit(ende_sid)
        out.append(f'tl.to("#{uid}-s{len(zeilen_p) - 1}", {{ opacity: 0, duration: 0.2 }}, {e});')
        out.append(f'tl.fromTo("#{uid}-sf", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {e});')
        return " ".join(out)
    return dict(html=html, js=js)


def balken3(z, uid, daten, sub=None, sub_sid=None):
    """Balkenvergleich: daten = [(label, wert_text, höhe, farbe, sid)]"""
    cols = "".join(
        f'<div id="{uid}-{i}" style="display:flex;flex-direction:column;align-items:center;gap:14px">'
        f'<div class="serif" style="font-size:64px;color:{c}">{v}</div>'
        f'<div style="width:260px;height:{h}px;border-radius:14px 14px 0 0;background:{c}"></div>'
        f'<div style="font-weight:800;font-size:46px;color:#353a3d">{lab}</div></div>' for i, (lab, v, h, c, _) in enumerate(daten))
    sub_html = f'<div id="{uid}-sub" style="position:absolute;right:150px;top:150px;padding:12px 34px;border-radius:30px;background:#353a3d;color:#fff;font-weight:800;font-size:46px">{sub}</div>' if sub else ""
    html = f'<div class="mitte" style="flex-direction:row;align-items:flex-end;gap:90px;top:110px">{cols}</div>{sub_html}'

    def js(t0, d):
        out = [f'pop("#{uid}-{i}", {z.euro_zeit(s) if s else t0});' for i, (_, _, _, _, s) in enumerate(daten)]
        if sub:
            out.append(f'pop("#{uid}-sub", {z.st(sub_sid)});')
        return " ".join(out)
    return dict(html=html, js=js)


def chips_zeit(z, uid, titel, items):
    """Schilder, die genau zum jeweiligen Satz erscheinen: items = [(text, farbe, sid)]"""
    chips = "".join(f'<div class="chip" id="{uid}-c{i}" style="background:{c}">{t}</div>' for i, (t, c, _) in enumerate(items))
    kopf = f'<div class="ctitel" id="{uid}-t">{titel}</div>' if titel else ""
    html = f'<div class="mitte">{kopf}<div class="chips">{chips}</div></div>'

    def js(t0, d):
        return (f'pop("#{uid}-t", {t0});' if titel else "") + "".join(
            f' pop("#{uid}-c{i}", {z.st(s) if s else t0 + 0.3 + i * 0.4});' for i, (_, _, s) in enumerate(items))
    return dict(html=html, js=js)
