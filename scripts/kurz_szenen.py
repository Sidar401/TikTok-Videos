"""Kleine Bausteine für 9:16-Shorts (zusammen mit finanz.build)."""
from finanz import BEAGLE

GRUEN, ROT, OR, GOLD, INK = "#1f7a4d", "#e24b4b", "#DB8622", "#f2c418", "#111"


def big(id_, txt, top, size=120, col=INK):
    return f'<div id="{id_}" class="big" style="position:absolute;left:0;top:{top}px;width:1080px;font-size:{size}px;line-height:1.05;color:{col}">{txt}</div>'


def sub(id_, txt, top, size=58, col=INK):
    return (f'<div id="{id_}" style="position:absolute;left:60px;top:{top}px;width:960px;text-align:center;font-family:Montserrat;'
            f'font-weight:800;font-size:{size}px;line-height:1.15;color:{col}">{txt}</div>')


def chip(id_, txt, col, x, y, size=50, center=False):
    pos = f"left:0;width:1080px;display:flex;justify-content:center" if center else f"left:{x}px"
    inner = f'<span style="padding:16px 34px;border-radius:24px;background:{col};color:#fff;font-family:Montserrat;font-weight:800;font-size:{size}px">{txt}</span>'
    return f'<div id="{id_}" style="position:absolute;{pos};top:{y}px">{inner}</div>' if center else \
        f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;padding:16px 34px;border-radius:24px;background:{col};color:#fff;font-family:Montserrat;font-weight:800;font-size:{size}px">{txt}</div>'


def kalender(monat, tag, farbe=ROT):
    return f"""<svg viewBox="0 0 300 300" style="width:100%;height:100%">
  <rect x="10" y="30" width="280" height="260" rx="30" fill="#fff" stroke="#353a3d" stroke-width="10" />
  <path d="M10 60 Q10 30 40 30 L260 30 Q290 30 290 60 L290 100 L10 100 Z" fill="{farbe}" />
  <rect x="70" y="8" width="20" height="50" rx="10" fill="#353a3d" /><rect x="210" y="8" width="20" height="50" rx="10" fill="#353a3d" />
  <text x="150" y="85" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="40" fill="#fff">{monat}</text>
  <text x="150" y="240" text-anchor="middle" font-family="Abril Fatface" font-size="130" fill="#111">{tag}</text></svg>"""


def liste(id_, zeilen, top, x=120, w=840, size=56):
    """Abhak-Liste: zeilen = [(text, id-suffix)]; Haken grün."""
    z = "".join(f'<div id="{id_}-{k}" style="display:flex;align-items:center;gap:26px"><div style="width:84px;height:84px;flex:none;border-radius:50%;background:{GRUEN};'
                f'display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 100 100" style="width:60%;height:60%"><path d="M22 52 L42 72 L80 30" fill="none" '
                f'stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" /></svg></div>'
                f'<span style="font-family:Montserrat;font-weight:800;font-size:{size}px;line-height:1.1;color:#111">{t}</span></div>' for k, t in enumerate(zeilen))
    return f'<div id="{id_}" style="position:absolute;left:{x}px;top:{top}px;width:{w}px;display:flex;flex-direction:column;gap:34px">{z}</div>'


def outro_cta(text):
    """Outro mit Beagle (CTA-Szene) + zusätzlicher Text-CTA (wenn er in der Aufnahme fehlt)."""
    return f"""
        <div style="position:absolute;left:0;top:300px;width:1080px;display:flex;flex-direction:column;align-items:center;gap:26px">
          <div id="outro-dog" style="width:460px;height:460px">{BEAGLE}</div>
          <div id="outro-name" style="font-family:Montserrat;font-weight:800;font-size:92px;color:#111">HundeFinanzTV</div>
          <div id="outro-btn" style="padding:18px 64px;border-radius:60px;background:var(--brand);color:#fff;font-family:Montserrat;font-weight:700;font-size:56px">+ Folgen</div>
          <div id="outro-cta" style="margin-top:20px;font-family:Montserrat;font-weight:800;font-size:46px;line-height:1.15;color:{OR};text-align:center;padding:0 60px">{text}</div>
        </div>"""


def outro_cta_js(t0, d):
    return f"""
      pop("#outro-dog", {t0});
      pop("#outro-name", {t0} + 0.25);
      pop("#outro-btn", {t0} + 0.5);
      pop("#outro-cta", {t0} + 0.9);
      tl.fromTo("#outro-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {t0} + 1.3);"""
