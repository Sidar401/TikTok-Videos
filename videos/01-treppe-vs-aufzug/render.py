"""Treppe vs. Aufzug – Simulations-Video (1080x1920, 30 fps).

Aufruf:  python3 render.py   ->  treppe_vs_aufzug.mp4
"""
import math
import os
import subprocess
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "treppe_vs_aufzug.mp4")

W, H, FPS, S = 1080, 1920, 30, 2  # S = Supersampling

# ---------- Modell (Durchschnittswerte) ----------
STAIR_S_PER_FLOOR = 12.0   # zu Fuß pro Stockwerk
LIFT_WAIT = 30.0           # bis der Aufzug unten ist
LIFT_DOORS = 8.0           # Türen auf, einsteigen, Türen zu
LIFT_S_PER_FLOOR = 3.0     # Fahrt pro Stockwerk
FLOORS = 8
LIFT_START = LIFT_WAIT + LIFT_DOORS                                   # 38 s
T_LIFT_GOAL = LIFT_START + FLOORS * LIFT_S_PER_FLOOR                  # 62 s
T_STAIR_GOAL = FLOORS * STAIR_S_PER_FLOOR                             # 96 s
T_CROSS = LIFT_START * STAIR_S_PER_FLOOR / (STAIR_S_PER_FLOOR - LIFT_S_PER_FLOOR)  # 50,67 s
F_CROSS = T_CROSS / STAIR_S_PER_FLOOR                                 # 4,22


def stair_pos(T):
    return min(T / STAIR_S_PER_FLOOR, FLOORS)


def lift_pos(T):
    """Position der Kabine (Stockwerk)."""
    if T < 9:
        return 7.0
    if T < LIFT_WAIT:
        return 7.0 - (T - 9) / LIFT_S_PER_FLOOR
    if T < LIFT_START:
        return 0.0
    return min((T - LIFT_START) / LIFT_S_PER_FLOOR, FLOORS)


def lift_status(T):
    if T < LIFT_WAIT:
        return "WARTET", AMBER
    if T < LIFT_START:
        return "TÜREN", AMBER
    if T < T_LIFT_GOAL:
        return "FÄHRT", BLUE
    return "IM ZIEL", GREEN


def stair_status(T):
    if T <= 0:
        return "BEREIT", GREY
    if T < T_STAIR_GOAL:
        return "LÄUFT", BLUE
    return "IM ZIEL", GREEN


# ---------- Timeline (Videozeit -> Simulationszeit) ----------
SEG = [  # (typ, start, ende, sim_von, sim_bis)
    ("hold", 0.0, 7.0, 0, 0),
    ("run", 7.0, 16.0, 0, 36),
    ("pause", 16.0, 19.5, 36, 36),
    ("run", 19.5, 27.0, 36, T_CROSS),
    ("pause", 27.0, 30.0, T_CROSS, T_CROSS),
    ("run", 30.0, 35.5, T_CROSS, T_LIFT_GOAL),
    ("pause", 35.5, 37.5, T_LIFT_GOAL, T_LIFT_GOAL),
    ("run", 37.5, 43.0, T_LIFT_GOAL, T_STAIR_GOAL),
    ("hold", 43.0, 47.0, T_STAIR_GOAL, T_STAIR_GOAL),
]
T_CHART, T_SUMMARY, T_OUTRO, DURATION = 47.0, 53.0, 58.0, 61.0

CAPTIONS = [  # (start, ende, text, hervorgehoben)
    (0.0, 3.5, "Treppe oder Aufzug – was ist schneller?", "schneller?"),
    (3.5, 7.0, "Beide wollen in den 8. Stock", "8. Stock"),
    (7.0, 10.0, "Die Treppe läuft sofort los", "sofort"),
    (10.0, 13.0, "Der Aufzug muss erst runterkommen", "erst"),
    (13.0, 16.0, "12 Sekunden pro Stockwerk", "12 Sekunden"),
    (16.0, 19.5, "Treppe schon im 3. Stock?", "3. Stock?"),
    (19.5, 23.0, "Jetzt fährt der Aufzug endlich", "endlich"),
    (23.0, 27.0, "Nur 3 Sekunden pro Stockwerk", "3 Sekunden"),
    (27.0, 30.0, "Kurz nach Stock 4 wird überholt", "überholt"),
    (30.0, 35.5, "Ab hier keine Chance mehr", "keine Chance"),
    (35.5, 37.5, "Aufzug nach 62 Sekunden oben", "62 Sekunden"),
    (37.5, 43.0, "Die Treppe braucht noch eine halbe Minute", "halbe Minute"),
    (43.0, 47.0, "Am Ende 34 Sekunden Unterschied", "34 Sekunden"),
    (47.0, 53.0, "Entscheidend ist die Wartezeit", "Wartezeit"),
    (53.0, 58.0, "Bis zum 4. Stock: nimm die Treppe", "Treppe"),
    (58.0, 61.0, "Was soll ich als Nächstes simulieren?", "Nächstes"),
]


def sim_time(tv):
    for kind, a, b, s0, s1 in SEG:
        if a <= tv < b:
            return kind, s0 + (s1 - s0) * (tv - a) / (b - a), tv - a
    return "hold", T_STAIR_GOAL, 0.0


# ---------- Farben ----------
BG = (12, 19, 32)
PANEL = (20, 30, 47)
LINE = (40, 55, 80)
STAIR_C = (232, 96, 76)
LIFT_C = (43, 181, 168)
AMBER = (245, 177, 61)
BLUE = (88, 140, 220)
GREEN = (90, 200, 120)
GREY = (120, 135, 160)
WHITE = (240, 244, 250)
DIM = (130, 145, 170)

# ---------- Zeichenhelfer (Koordinaten in 1080er-Raum) ----------
_fonts = {}


def F(size, w="Bold"):
    key = (size, w)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(
            f"/usr/share/fonts/opentype/inter/Inter-{w}.otf", int(size * S))
    return _fonts[key]


def sc(v):
    return [int(round(x * S)) for x in v]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


class Pen:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def rect(self, box, fill=None, outline=None, width=0):
        self.d.rectangle(sc(box), fill=fill, outline=outline, width=int(width * S))

    def rrect(self, box, r, fill=None, outline=None, width=0):
        self.d.rounded_rectangle(sc(box), int(r * S), fill=fill, outline=outline,
                                 width=int(width * S))

    def line(self, pts, fill, width):
        self.d.line(sc([c for p in pts for c in p]), fill=fill, width=int(width * S),
                    joint="curve")

    def circle(self, x, y, r, fill):
        self.d.ellipse(sc((x - r, y - r, x + r, y + r)), fill=fill)

    def text(self, x, y, s, font, fill, anchor="mm"):
        self.d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)

    def tlen(self, s, font):
        return self.d.textlength(s, font=font) / S


def layer():
    return Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))


def blend(base, top, alpha):
    if alpha <= 0:
        return base
    if alpha < 1:
        a = top.getchannel("A").point(lambda v: int(v * alpha))
        top.putalpha(a)
    base.alpha_composite(top)
    return base


# ---------- Szene: Gebäude ----------
GROUND = 1470
FH = 115
LB = (60, 515)    # Treppenhaus x
RB = (565, 1020)  # Aufzug x
SHAFT = (880, 1000)
STAIR_X = (150, 480)


def fy(pos):
    return GROUND - pos * FH


def static_scene():
    img = Image.new("RGBA", (W * S, H * S), BG + (255,))
    p = Pen(img)
    top = fy(FLOORS) - 30
    for (x0, x1), col, name in ((LB, STAIR_C, "TREPPE"), (RB, LIFT_C, "AUFZUG")):
        p.rrect((x0, top, x1, GROUND), 18, fill=PANEL, outline=LINE, width=2)
        for i in range(FLOORS + 1):
            y = fy(i)
            p.line([(x0 + 2, y), (x1 - 2, y)], LINE, 2)
            lbl = "EG" if i == 0 else str(i)
            p.text(x0 + 16, y - 16, lbl, F(20, "SemiBold"), DIM, "lm")
        p.text((x0 + x1) / 2, top - 32, name, F(30, "ExtraBold"), col)
        # Ziel-Linie
        y8 = fy(FLOORS)
        for xx in range(x0 + 60, x1 - 10, 28):
            p.line([(xx, y8), (xx + 14, y8)], col, 4)
    # Treppenläufe
    for i in range(FLOORS):
        xa, xb = (STAIR_X if i % 2 == 0 else STAIR_X[::-1])
        y0, y1 = fy(i), fy(i + 1)
        pts = []
        n = 9
        for k in range(n):
            xs = xa + (xb - xa) * k / n
            xe = xa + (xb - xa) * (k + 1) / n
            ys = y0 + (y1 - y0) * k / n
            ye = y0 + (y1 - y0) * (k + 1) / n
            pts += [(xs, ys), (xs, ye), (xe, ye)]
        p.line(pts, (55, 72, 100), 4)
    # Schacht
    p.rect((SHAFT[0], fy(FLOORS) - 10, SHAFT[1], GROUND), fill=(15, 23, 37),
           outline=LINE, width=2)
    p.circle(SHAFT[0] - 22, GROUND - 60, 8, (60, 75, 100))  # Rufknopf
    # Boden
    p.rect((0, GROUND, W, GROUND + 6), fill=LINE)
    return img


def figure(p, x, yf, col, phase, moving, face=1):
    leg = 30
    sw = math.sin(phase) * 0.45 if moving else 0.0
    hip = (x, yf - leg)
    for a in (sw, -sw):
        p.line([hip, (x + math.sin(a) * leg * face, yf - (1 - math.cos(a)) * 6)], col, 9)
    bob = abs(math.sin(phase)) * 3 if moving else 0
    p.rrect((x - 10, yf - leg - 46 - bob, x + 10, yf - leg + 4 - bob), 10, fill=col)
    p.circle(x, yf - leg - 64 - bob, 15, WHITE)


def stair_xy(pos):
    i = min(int(pos), FLOORS - 1)
    fr = pos - i
    xa, xb = (STAIR_X if i % 2 == 0 else STAIR_X[::-1])
    return xa + (xb - xa) * fr, fy(i) + (fy(i + 1) - fy(i)) * fr, (1 if xb > xa else -1)


def draw_race(img, tv, T, moving):
    p = Pen(img)
    # Treppe
    sp = stair_pos(T)
    x, y, face = stair_xy(sp)
    figure(p, x, y, STAIR_C, tv * 2 * math.pi * 2.2, moving and T < T_STAIR_GOAL, face)
    # Aufzug
    cp = lift_pos(T)
    cy = fy(cp)
    if LIFT_WAIT <= T < LIFT_START:
        rel = T - LIFT_WAIT
        door = ease(rel / 2) if rel < 5 else 1 - ease((rel - 5) / 2)
    else:
        door = 0.0
    cx0, cx1 = SHAFT[0] + 6, SHAFT[1] - 6
    p.rect((cx0, cy - 112, cx1, cy - 2), fill=(30, 46, 70), outline=LIFT_C, width=3)
    # Person
    if T < LIFT_WAIT + 2:
        px, pm = 780, False
    elif T < LIFT_WAIT + 5:
        px, pm = 780 + (940 - 780) * ease((T - LIFT_WAIT - 2) / 3), moving
    else:
        px, pm = 940, False
    figure(p, px, cy - 4 if T >= LIFT_WAIT + 5 else GROUND, LIFT_C,
           tv * 2 * math.pi * 2.2, pm)
    # Türen (über der Person)
    half = (cx1 - cx0) / 2
    dw = half * (1 - door)
    if dw > 1:
        p.rect((cx0, cy - 110, cx0 + dw, cy - 4), fill=(48, 68, 98))
        p.rect((cx1 - dw, cy - 110, cx1, cy - 4), fill=(48, 68, 98))
    if T < LIFT_WAIT:  # Rufknopf leuchtet
        glow = 0.6 + 0.4 * math.sin(tv * 6)
        p.circle(SHAFT[0] - 22, GROUND - 60, 8, tuple(int(c * glow) for c in AMBER))


def fmt(T):
    T = int(T)
    return f"{T // 60}:{T % 60:02d}"


def pill(p, x, y, s, col, size=20):
    f = F(size, "ExtraBold")
    w = p.tlen(s, f) + 28
    p.rrect((x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.85), size, fill=col)
    p.text(x, y, s, f, BG)


def floor_label(pos):
    n = int(pos + 1e-6)
    return ("EG", "") if n == 0 else (f"{n}.", "STOCK")


def draw_header(img, T, paused):
    p = Pen(img)
    p.text(540, 120, fmt(T), F(96, "Bold"), WHITE)
    if paused:
        pill(p, 540, 190, "PAUSE", WHITE, 18)
    for (x0, x1), col, name, pos, (st, stc) in (
        (LB, STAIR_C, "TREPPE", stair_pos(T), stair_status(T)),
        (RB, LIFT_C, "AUFZUG", lift_pos(T) if T >= LIFT_START else 0, lift_status(T)),
    ):
        p.rrect((x0, 225, x1, 345), 18, fill=PANEL, outline=LINE, width=2)
        p.text(x0 + 24, 255, name, F(24, "ExtraBold"), col, "lm")
        p.text(x1 - 24, 255, "STOCKWERK", F(18, "SemiBold"), DIM, "rm")
        big, small = floor_label(pos)
        p.text(x0 + 24, 312, big, F(54, "Bold"), WHITE, "lm")
        bw = p.tlen(big, F(54, "Bold"))
        p.text(x0 + 32 + bw, 322, small, F(20, "SemiBold"), DIM, "lm")
        f = F(18, "ExtraBold")
        w = p.tlen(st, f) + 26
        p.rrect((x1 - 24 - w, 296, x1 - 24, 328), 16, fill=stc)
        p.text(x1 - 24 - w / 2, 312, st, f, BG)


def card(p, box):
    p.rrect(box, 26, fill=(17, 26, 42), outline=LINE, width=3)


def draw_overlays(base, tv, T):
    """Pausen-Karten, Intro, Regeln, Endstand."""
    def show(a, b, fade=0.3):
        if not (a <= tv < b):
            return 0.0
        return min(1.0, (tv - a) / fade, (b - tv) / fade)

    # Intro
    al = show(0.0, 3.5)
    if al:
        L = layer(); p = Pen(L)
        dy = (1 - ease((tv) / 0.5)) * 30
        card(p, (110, 610 + dy, 970, 900 + dy))
        p.text(540, 700 + dy, "TREPPE", F(84, "Black"), STAIR_C, "rm")
        p.text(540, 700 + dy, "  vs  ", F(40, "Bold"), DIM, "lm")
        p.text(540 + p.tlen("  vs  ", F(40, "Bold")), 700 + dy, "AUFZUG",
               F(84, "Black"), LIFT_C, "lm")
        p.text(540, 815, "Was ist schneller?", F(58, "ExtraBold"), AMBER)
        base = blend(base, L, al)
    # Regeln
    al = show(3.5, 7.0)
    if al:
        L = layer(); p = Pen(L)
        rules = [("ZIEL: 8. STOCK", WHITE), ("ZU FUSS: 12 s / STOCK", STAIR_C),
                 ("AUFZUG: 30 s WARTEN", LIFT_C), ("FAHRT: 3 s / STOCK", LIFT_C)]
        for k, (s, c) in enumerate(rules):
            if tv - 3.5 > k * 0.45:
                pill(p, 540, 620 + k * 95, s, c, 34)
        base = blend(base, L, al)
    # Pause 1
    al = show(16.0, 19.5)
    if al:
        L = layer(); p = Pen(L)
        card(p, (130, 640, 950, 900))
        p.text(540, 700, "NACH 36 SEKUNDEN", F(30, "ExtraBold"), DIM)
        p.text(330, 775, "3. Stock", F(56, "Bold"), STAIR_C)
        p.text(540, 775, "vs", F(34, "Bold"), DIM)
        p.text(750, 775, "noch EG", F(56, "Bold"), LIFT_C)
        p.text(540, 850, "TREPPE GEWINNT?", F(34, "ExtraBold"), AMBER)
        base = blend(base, L, al)
    # Pause 2
    al = show(27.0, 30.0)
    if al:
        L = layer(); p = Pen(L)
        card(p, (180, 640, 900, 860))
        p.text(540, 720, "ÜBERHOLT!", F(80, "Black"), AMBER)
        p.text(540, 805, f"bei Stock {F_CROSS:.1f}".replace(".", ","),
               F(38, "SemiBold"), WHITE)
        base = blend(base, L, al)
    # Pause 3
    al = show(35.5, 37.5)
    if al:
        L = layer(); p = Pen(L)
        card(p, (160, 640, 920, 860))
        p.text(540, 715, "AUFZUG IM ZIEL", F(56, "Black"), LIFT_C)
        p.text(540, 800, "Treppe erst im 5. Stock", F(38, "SemiBold"), WHITE)
        base = blend(base, L, al)
    # Endstand
    al = show(43.0, T_CHART + 0.3)
    if al:
        L = layer(); p = Pen(L)
        p.rect((0, 0, W, H), fill=BG + (200,))
        card(p, (130, 560, 950, 1060))
        p.text(540, 620, "ENDSTAND", F(30, "ExtraBold"), DIM)
        rows = [("AUFZUG", LIFT_C, fmt(T_LIFT_GOAL)), ("TREPPE", STAIR_C, fmt(T_STAIR_GOAL))]
        for k, (n, c, v) in enumerate(rows):
            if tv - 43 > 0.3 + k * 0.5:
                y = 710 + k * 95
                p.text(190, y, n, F(48, "ExtraBold"), c, "lm")
                p.text(890, y, v, F(60, "Bold"), WHITE, "rm")
        if tv - 43 > 1.6:
            p.line([(190, 880), (890, 880)], LINE, 2)
            p.text(190, 945, "DIFFERENZ", F(28, "SemiBold"), DIM, "lm")
            diff = T_STAIR_GOAL - T_LIFT_GOAL
            p.text(890, 930, f"{diff:.0f} s", F(56, "Bold"), AMBER, "rm")
            p.text(890, 990, f"≈ {diff / T_STAIR_GOAL * 100:.0f} % SCHNELLER",
                   F(24, "ExtraBold"), AMBER, "rm")
        base = blend(base, L, al)
    return base


# ---------- Szene: Diagramm ----------
def draw_chart(img, tv):
    p = Pen(img)
    t = tv - T_CHART
    p.text(540, 330, "WANN LOHNT SICH WAS?", F(58, "Black"), AMBER)
    p.text(540, 400, "Zeit bis zum Ziel je Stockwerk", F(30, "SemiBold"), DIM)
    X0, X1, Y0, Y1 = 170, 960, 1380, 560
    NMAX, TMAX = 10, 130

    def P(n, s):
        return X0 + (X1 - X0) * n / NMAX, Y0 - (Y0 - Y1) * s / TMAX

    # Bereiche
    cx = P(F_CROSS, 0)[0]
    if t > 2.6:
        a = int(40 * ease((t - 2.6) / 0.6))
        L = layer(); q = Pen(L)
        q.rect((X0, Y1, cx, Y0), fill=STAIR_C + (a,))
        q.rect((cx, Y1, X1, Y0), fill=LIFT_C + (a,))
        img.alpha_composite(L)
        p = Pen(img)
        p.text((X0 + cx) / 2, Y1 + 50, "TREPPE", F(32, "ExtraBold"), STAIR_C)
        p.text((X0 + cx) / 2, Y1 + 88, "schneller", F(24, "SemiBold"), STAIR_C)
        p.text((cx + X1) / 2, Y1 + 50, "AUFZUG", F(32, "ExtraBold"), LIFT_C)
        p.text((cx + X1) / 2, Y1 + 88, "schneller", F(24, "SemiBold"), LIFT_C)
    # Achsen
    p.line([(X0, Y1), (X0, Y0), (X1, Y0)], DIM, 3)
    for n in range(0, NMAX + 1, 2):
        x, _ = P(n, 0)
        p.text(x, Y0 + 32, "EG" if n == 0 else str(n), F(24, "SemiBold"), DIM)
    for s in range(0, TMAX + 1, 30):
        _, y = P(0, s)
        p.text(X0 - 18, y, f"{s} s", F(22, "SemiBold"), DIM, "rm")
        if s:
            p.line([(X0, y), (X1, y)], LINE, 1)
    p.text((X0 + X1) / 2, Y0 + 80, "Stockwerk", F(26, "SemiBold"), DIM)
    # Linien
    k = ease(t / 2.2)
    nm = NMAX * k
    if nm > 0:
        p.line([P(n / 20, n / 20 * STAIR_S_PER_FLOOR) for n in range(int(nm * 20) + 1)]
               + [P(nm, nm * STAIR_S_PER_FLOOR)], STAIR_C, 8)
        p.line([P(0, LIFT_START), P(nm, LIFT_START + nm * LIFT_S_PER_FLOOR)], LIFT_C, 8)
    if t > 2.4:
        x, y = P(F_CROSS, T_CROSS)
        r = 16 * ease((t - 2.4) / 0.4)
        p.circle(x, y, r, WHITE)
        if t > 2.8:
            pill(p, x, y - 60, "GLEICHSTAND ≈ 4. STOCK", AMBER, 26)
    return img


# ---------- Szene: Fazit + Outro ----------
def draw_summary(img, tv):
    p = Pen(img)
    t = tv - T_SUMMARY
    p.text(540, 520, "UNTERM STRICH", F(34, "ExtraBold"), DIM)
    rows = [("EG – 4. STOCK", "TREPPE", STAIR_C), ("AB 5. STOCK", "AUFZUG", LIFT_C)]
    for k, (a, b, c) in enumerate(rows):
        if t > 0.3 + k * 0.6:
            y = 650 + k * 170
            p.rrect((110, y - 65, 970, y + 65), 22, fill=PANEL, outline=c, width=3)
            p.text(160, y, a, F(44, "Bold"), WHITE, "lm")
            p.text(920, y, b, F(52, "Black"), c, "rm")
    if t > 1.8:
        p.text(540, 1030, "Bonus: Die Treppe ist ein gratis Workout.",
               F(32, "SemiBold"), AMBER)
    p.text(540, 1300, "Annahmen (Durchschnitt): 12 s pro Stockwerk zu Fuß,",
           F(24, "Medium"), DIM)
    p.text(540, 1340, "30 s Wartezeit, 8 s Türen, 3 s pro Stockwerk Fahrt",
           F(24, "Medium"), DIM)
    return img


def draw_outro(img, tv):
    p = Pen(img)
    t = tv - T_OUTRO
    p.text(540, 760, "Was soll ich als", F(66, "Black"), WHITE)
    p.text(540, 850, "Nächstes simulieren?", F(66, "Black"), AMBER)
    if t > 0.6:
        pill(p, 540, 990, "SCHREIB'S IN DIE KOMMENTARE", WHITE, 30)
    return img


# ---------- Untertitel ----------
def draw_caption(img, tv):
    for a, b, text, hl in CAPTIONS:
        if a <= tv < b:
            break
    else:
        return
    p = Pen(img)
    f = F(50, "ExtraBold")
    hlw = set(hl.split())
    words = text.split()
    lines, cur = [], []
    for w in words:
        if cur and p.tlen(" ".join(cur + [w]), f) > 900:
            lines.append(cur); cur = []
        cur.append(w)
    lines.append(cur)
    y0 = 1700 - (len(lines) - 1) * 32
    for li, ln in enumerate(lines):
        total = p.tlen(" ".join(ln), f)
        x = 540 - total / 2
        for w in ln:
            p.text(x, y0 + li * 64, w, f, AMBER if w in hlw else WHITE, "lm")
            x += p.tlen(w + " ", f)


# ---------- Frame ----------
_static = None


def frame(i):
    global _static
    if _static is None:
        _static = static_scene()
    tv = i / FPS
    if tv < T_CHART:
        kind, T, _ = sim_time(tv)
        img = _static.copy()
        draw_race(img, tv, T, kind == "run")
        draw_header(img, T, kind == "pause")
        img = draw_overlays(img, tv, T)
    else:
        img = Image.new("RGBA", (W * S, H * S), BG + (255,))
        if tv < T_SUMMARY:
            draw_chart(img, tv)
        elif tv < T_OUTRO:
            draw_summary(img, tv)
        else:
            draw_outro(img, tv)
    draw_caption(img, tv)
    # kurze Überblendung bei Szenenwechsel
    for cut in (T_CHART, T_SUMMARY, T_OUTRO):
        d = abs(tv - cut)
        if d < 0.25:
            L = Image.new("RGBA", img.size, BG + (int(255 * (1 - d / 0.25)),))
            img.alpha_composite(L)
    return img.convert("RGB").reduce(S).tobytes()


# ---------- Ton ----------
def make_audio(path):
    sr = 44100
    n = int(DURATION * sr)
    a = np.zeros(n)

    def add(t, sig):
        i = int(t * sr)
        sig = sig[: max(0, n - i)]
        a[i:i + len(sig)] += sig

    def tone(freq, dur, vol, decay):
        tt = np.arange(int(dur * sr)) / sr
        return vol * np.sin(2 * np.pi * freq * tt) * np.exp(-tt * decay)

    tick = tone(1800, 0.03, 0.18, 120)
    for kind, s, e, *_ in SEG:
        if kind == "run":
            t = s
            while t < e:
                add(t, tick)
                t += 0.25
        if kind == "pause":
            add(s, tone(520, 0.25, 0.35, 12) + tone(780, 0.25, 0.2, 12))
    ding = tone(1320, 1.2, 0.35, 3) + tone(1760, 1.2, 0.2, 3.5)
    add(35.5, ding)
    add(43.0, tone(990, 1.2, 0.35, 3) + tone(1320, 1.2, 0.2, 3.5))
    for t in (0.0, T_CHART, T_SUMMARY, T_OUTRO):
        noise = np.random.default_rng(1).normal(0, 1, int(0.35 * sr))
        env = np.sin(np.linspace(0, np.pi, len(noise))) * 0.06
        add(t, np.convolve(noise, np.ones(30) / 30, "same") * env * 8)
    a = np.clip(a, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


def main():
    wav = os.path.join(HERE, "_audio.wav")
    make_audio(wav)
    total = int(DURATION * FPS)
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT],
        stdin=subprocess.PIPE)
    with Pool() as pool:
        for k, buf in enumerate(pool.imap(frame, range(total), chunksize=8)):
            ff.stdin.write(buf)
            if k % 150 == 0:
                print(f"{k}/{total}", flush=True)
    ff.stdin.close()
    ff.wait()
    os.remove(wav)
    print("fertig:", OUT)


if __name__ == "__main__":
    main()
