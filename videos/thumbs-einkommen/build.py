#!/usr/bin/env python3
"""Thumbnail (1920×1080, YouTube) + Cover (1080×1920, TikTok/Instagram) für longform-einkommen – Stil „Dark Glow“.
Aufruf: python3 build.py | python3 build.py tiktok"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
from thumbs import GRUEN, OR, ROT, seite, titel  # noqa: E402

STUFEN = [(6, "Top 1 %", "#b36bdb"), (5, "> 4.600 €", GRUEN), (4, "2.300 – 4.600 €", "#4d8ff0"),
          (3, "≈ 2.300 €", "#ffc533"), (2, "1.400 – 2.300 €", OR), (1, "< 1.400 €", ROT)]


def leiter(x, y, w, h=112, abstand=18, fs=54):
    out = []
    for i, (n, t, c) in enumerate(STUFEN):
        out.append(f'<div style="position:absolute;left:{x}px;top:{y + i * (h + abstand)}px;width:{w}px;height:{h}px;border-radius:24px;background:#16191b;'
                   f'border:4px solid {c};box-shadow:0 0 36px {c}77, inset 0 0 30px {c}22;display:flex;align-items:center;gap:30px;padding-right:30px;overflow:hidden;z-index:2">'
                   f'<div style="width:{h - 8}px;height:100%;background:{c};color:#111;font-weight:900;font-size:{fs + 14}px;display:flex;align-items:center;justify-content:center">{n}</div>'
                   f'<div style="font-weight:900;font-size:{fs}px;color:#fff;white-space:nowrap">{t}</div></div>')
    return "".join(out)


def pfeil(x, y, w=110):
    return (f'<svg viewBox="0 0 170 90" style="position:absolute;left:{x}px;top:{y - 45}px;width:{w}px;height:90px;overflow:visible;'
            f'filter:drop-shadow(0 0 16px {OR});z-index:3"><path d="M170 32 L70 32 L70 6 L4 45 L70 84 L70 58 L170 58 Z" fill="{OR}"/></svg>')


YT = (leiter(90, 90, 760)
      + titel([("Wo stehst", "w"), ("DU?", "box")], 990, 300, 160)
      + pfeil(870, 90 + 3 * 130 + 56))

TT = (titel([("Wo stehst", "w"), ("DU?", "box")], 0, 200, 160, w=1080, align="center")
      + leiter(140, 720, 800, 120, 26, 56))

if __name__ == "__main__":
    tiktok = sys.argv[1:2] == ["tiktok"]
    seite(HERE, [TT] if tiktok else [YT], tiktok=tiktok, glow=("70%", "45%"))
