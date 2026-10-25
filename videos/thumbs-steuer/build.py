#!/usr/bin/env python3
"""Thumbnail (1920×1080, YouTube) + Cover (1080×1920, TikTok/Instagram) für longform-steuer – Stil „Dark Glow“.
Aufruf: python3 build.py | python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import OR, ROT, buendel, muenzen, seite, titel  # noqa: E402

HAKEN = '<svg viewBox="0 0 100 100" style="width:55%;height:55%"><path d="M22 52 L42 72 L80 30" fill="none" stroke="#111" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def kreis(n, offen, gr):
    if offen:
        return (f'<div style="width:{gr}px;height:{gr}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffb35c,{OR} 55%,#c25f00);'
                f'box-shadow:0 0 40px {OR}aa;display:flex;align-items:center;justify-content:center">{HAKEN}</div>')
    return (f'<div style="width:{gr}px;height:{gr}px;border-radius:50%;background:#16191b;border:6px solid {OR};box-shadow:0 0 30px {OR}55;'
            f'display:flex;align-items:center;justify-content:center;color:{OR};font-weight:900;font-size:{gr * 0.48:.0f}px">{n}</div>')


def schloesser(gr):
    return "".join(kreis(i + 1, i < 5, gr) for i in range(7))


def tresor(x, y, s):
    pos = [(50, 15), (79, 32), (79, 68), (50, 85), (21, 68), (21, 32)]
    zu = {4, 5}
    kreise = "".join(f'<div style="position:absolute;left:{px - 9}%;top:{py - 9}%;width:18%;height:18%">{kreis({4: 6, 5: 7}.get(i, i + 1), i not in zu, s * 0.18)}</div>' for i, (px, py) in enumerate(pos))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:{s * 0.08}px;background:linear-gradient(145deg,#2a2f33,#121517);'
            f'border:8px solid {OR};box-shadow:0 0 80px {OR}66, 0 40px 60px #000, inset 0 0 40px #000;z-index:2">'
            f'<div style="position:absolute;inset:4%;border-radius:{s * 0.06}px;border:3px solid #ffffff14"></div>{kreise}'
            f'<div style="position:absolute;left:35%;top:35%;width:30%;height:30%;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff2b0,#ffc533 50%,#b87800);'
            f'box-shadow:0 0 60px #ffc533aa;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:{s * 0.14:.0f}px;color:#8a5200">€</div></div>')


YT = (titel([('7 legale <span style="color:#ff8a1f;text-shadow:0 0 40px #ff8a1f66">Steuertricks</span>', "w")], 0, 150, 160, w=1920, align="center")
      + f'<div style="position:absolute;left:0;top:450px;width:1920px;display:flex;justify-content:center;gap:34px;z-index:2">{schloesser(196)}</div>'
      + titel([("die fast keiner nutzt", "rot")], 0, 770, 100, w=1920, align="center")
      + buendel(60, 820, 0.85, 4) + muenzen(1690, 800, 6, 150))

TT = (titel([("Das Finanzamt", "w"), ("schuldet dir", "w"), ("GELD!", "box")], 0, 220, 118, w=1080, align="center")
      + tresor(200, 860, 680) + muenzen(780, 1360, 6, 170) + buendel(80, 1400, 0.9, 4))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [YT], tiktok=tiktok, glow=("50%", "50%"))
