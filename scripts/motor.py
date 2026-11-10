"""Endkarte für Motor-Shorts (Nutzer 8.11.): Thumbnail des Longforms + „Auf unserem Kanal“ (Nutzer 10.11.: nicht „unten verlinkt“, kein Pfeil nach unten).

  from motor import endkarte
  html, js = endkarte("assets/lf.jpg")   # Thumbnail vorher nach assets/ kopieren
"""
from glow_short import OR, chip, t


def endkarte(bild, titel="Das ganze Video"):
    html = (t("mk-t", titel, 420, 84, "glow-o")
            + f'<div id="mk-b" style="position:absolute;left:150px;top:540px;width:780px;height:439px;border-radius:30px;overflow:hidden;'
              f'border:8px solid {OR};box-shadow:0 0 80px {OR}88;z-index:3"><img src="{bild}" style="width:100%;height:100%;object-fit:cover" alt=""/></div>'
            + chip("mk-c", "Jetzt auf unserem Kanal", OR, 1060, 60))
    js = lambda a, d: (f'pop("#mk-t", {a}); tl.fromTo("#mk-b", {{ scale: 0.6, rotation: -6, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {a} + 0.2);'  # noqa: E731
                       f' pop("#mk-c", {a} + 0.6); tl.fromTo("#mk-c", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {a} + 1.0);')
    return html, js
