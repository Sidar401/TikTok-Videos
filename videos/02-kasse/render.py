"""Kasse: kürzeste Schlange vs. wenigste Artikel – Simulation mit Sprecher.

Aufruf:  FONT_DIR=... AUDIO_DIR=... python3 render.py [out.mp4]
Ohne AUDIO_DIR: nur Untertitel und Effekte, ohne Sprecher.
"""
import math
import os
import subprocess
import sys
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("FONT_DIR", "/usr/share/fonts/opentype/inter")
AUDIO_DIR = os.environ.get("AUDIO_DIR")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "kasse.mp4")

W, H, FPS, S = 1080, 1920, 30, 2

# ---------- Modell (Durchschnittswerte) ----------
S_ITEM = 3.0     # Sekunden pro Artikel
S_PAY = 40.0     # Begrüßen, Bezahlen, Einpacken
LANES = {"A": [45, 50], "B": [6, 9, 4, 8, 7]}


def schedule(items):
    t, out = 0.0, []
    for n in items:
        out.append((t, t + n * S_ITEM, t + n * S_ITEM + S_PAY, n))
        t += n * S_ITEM + S_PAY
    return out


SCHED = {k: schedule(v) for k, v in LANES.items()}
T_A = SCHED["A"][-1][2]   # 365
T_B = SCHED["B"][-1][2]   # 302
T_P1 = SCHED["B"][2][2]   # 177

# ---------- Sprecher ----------
TEMPO = 1.1
GAP = 0.5
NARR = {
    1: (15.57, "Supermarkt, zwei Kassen. Links stehen nur zwei Leute vor dir – aber mit "
               "randvollen Wagen. Rechts sind es fünf Leute, dafür nur mit kleinen Körben. "
               "Wo stellst du dich an?", {"zwei", "fünf", "an?"}),
    2: (13.71, "Wir rechnen mit Durchschnittswerten: drei Sekunden pro Artikel. Und vierzig "
               "Sekunden pro Kunde – fürs Begrüßen, Bezahlen und Einpacken. Also: Los geht's.",
        {"drei", "vierzig", "Sekunden"}),
    3: (8.59, "Links wird gescannt und gescannt. Rechts ist der erste Kunde schon wieder weg. "
              "Kleine Körbe gehen schnell durch.", {"schnell", "weg."}),
    4: (9.25, "Knapp drei Minuten sind vorbei. Links ist gerade mal der erste Kunde fertig. "
              "Rechts sind schon drei von fünf durch.", {"drei", "erste", "fünf"}),
    5: (7.00, "Und der zweite Wagen links ist sogar noch voller als der erste. Fünfzig Artikel.",
        {"Fünfzig", "voller"}),
    6: (6.43, "Rechts heißt es: Du bist dran! Nach fünf Minuten und zwei Sekunden.",
        {"dran!", "fünf", "zwei"}),
    7: (3.55, "Links musst du noch über eine Minute länger warten.", {"Minute"}),
    8: (8.12, "Am Ende ist die lange Schlange dreiundsechzig Sekunden schneller. Obwohl dort "
              "mehr als doppelt so viele Leute standen.", {"dreiundsechzig", "doppelt"}),
    9: (12.83, "Der Grund: Jeder Kunde kostet Zeit, egal wie wenig er kauft. Links steckt fast "
               "die ganze Zeit im Scannen. Rechts frisst das Bezahlen zwei Drittel.",
        {"Jeder", "Scannen.", "Drittel."}),
    10: (14.37, "Daraus folgt eine einfache Faustregel: Ein Kunde zählt so viel wie dreizehn "
                "Artikel. Also: Leute mal dreizehn, plus alle Artikel. Die kleinere Zahl gewinnt.",
         {"Faustregel:", "dreizehn", "kleinere"}),
    11: (16.04, "Links: zwei mal dreizehn plus fünfundneunzig – macht hunderteinundzwanzig. "
                "Rechts: fünf mal dreizehn plus vierunddreißig – nur neunundneunzig. "
                "Rechts gewinnt.", {"hunderteinundzwanzig.", "neunundneunzig.", "gewinnt."}),
    12: (10.11, "Zähl also nicht nur die Leute, sondern auch die Wagen. Welche Alltagsfrage "
                "soll ich als Nächstes simulieren? Schreib's in die Kommentare.",
         {"Wagen.", "Nächstes"}),
}

# (Sprecher-Nr, Typ, Sim von, Sim bis, Overlay)
PLAN = [
    (1, "hold", 0, 0, "intro"),
    (2, "hold", 0, 0, "rules"),
    (3, "run", 0, T_P1, None),
    (4, "pause", T_P1, T_P1, "p1"),
    (5, "run", T_P1, T_B, None),
    (6, "pause", T_B, T_B, "p2"),
    (7, "run", T_B, T_A, None),
    (8, "hold", T_A, T_A, "end"),
    (9, "chart", 0, 0, None),
    (10, "rule", 0, 0, None),
    (11, "calc", 0, 0, None),
    (12, "outro", 0, 0, None),
]
MIN_LEN = {7: 4.5}

SCENES = []  # (start, end, n, kind, s0, s1, overlay)
_t = 0.0
for n, kind, s0, s1, ov in PLAN:
    L = max(NARR[n][0] / TEMPO + GAP, MIN_LEN.get(n, 0))
    SCENES.append((_t, _t + L, n, kind, s0, s1, ov))
    _t += L
DURATION = _t + 0.8
NARR_OFFSET = 0.15


def scene_at(tv):
    for sc_ in SCENES:
        if sc_[0] <= tv < sc_[1]:
            return sc_
    return SCENES[-1]


def sim_time(tv):
    a, b, n, kind, s0, s1, ov = scene_at(tv)
    if kind == "run":
        return kind, s0 + (s1 - s0) * min(1, (tv - a) / (b - a))
    return kind, s1


def captions():
    out = []
    for a, b, n, *_ in SCENES:
        dur, text, hl = NARR[n]
        dur /= TEMPO
        words = text.split()
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 26 or w[-1] in ".?!:":
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
        total = sum(len(" ".join(c)) for c in chunks)
        t = a + NARR_OFFSET
        for c in chunks:
            d = dur * len(" ".join(c)) / total
            out.append((t, t + d, c, hl))
            t += d
    return out


CAPS = captions()

# ---------- Farben ----------
BG = (12, 19, 32)
PANEL = (20, 30, 47)
LINE = (40, 55, 80)
A_C = (232, 96, 76)
B_C = (43, 181, 168)
AMBER = (245, 177, 61)
BLUE = (88, 140, 220)
GREEN = (90, 200, 120)
GREY = (120, 135, 160)
WHITE = (240, 244, 250)
DIM = (130, 145, 170)

# ---------- Zeichenhelfer ----------
_fonts = {}


def F(size, w="Bold"):
    key = (size, w)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, f"Inter-{w}.otf"), int(size * S))
    return _fonts[key]


def sc(v):
    return [int(round(x * S)) for x in v]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


class Pen:
    def __init__(self, img):
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
        top.putalpha(top.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(top)
    return base


def pill(p, x, y, s, col, size=20, fg=BG):
    f = F(size, "ExtraBold")
    w = p.tlen(s, f) + size * 1.4
    p.rrect((x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.85), size, fill=col)
    p.text(x, y, s, f, fg)


def card(p, box):
    p.rrect(box, 26, fill=(17, 26, 42), outline=LINE, width=3)


def fmt(T):
    T = int(T)
    return f"{T // 60}:{T % 60:02d}"


# ---------- Szene: Kassen ----------
COLS = {"A": (60, 515), "B": (565, 1020)}
DESK_Y = 470
SLOT0 = 690     # Fußhöhe des Kunden an der Kasse
SLOT_H = 140


def lane_state(lane, T):
    """Fertige Kunden, (Index, Phase, Rest-Artikel) des aktuellen Kunden."""
    done = 0
    for k, (s, e_scan, e_pay, n) in enumerate(SCHED[lane]):
        if T >= e_pay:
            done += 1
            continue
        if T < e_scan:
            left = n - int((T - s) / S_ITEM)
            return done, (k, "scan", left)
        return done, (k, "pay", 0)
    return done, None


def queue_offset(lane, T):
    """Fließende Position der Schlange (wie viele Plätze schon aufgerückt)."""
    off = 0.0
    for s, e_scan, e_pay, n in SCHED[lane]:
        off += ease((T - e_pay) / 6.0) if T > e_pay else 0
    return off


def figure(p, x, yf, body, head=WHITE, phase=0.0, moving=False):
    leg = 28
    sw = math.sin(phase) * 0.45 if moving else 0.0
    for a in (sw, -sw):
        p.line([(x, yf - leg), (x + math.sin(a) * leg, yf - (1 - math.cos(a)) * 6)], body, 9)
    p.rrect((x - 10, yf - leg - 44, x + 10, yf - leg + 4), 10, fill=body)
    p.circle(x, yf - leg - 62, 15, head)


def cart(p, x, yf, n, col, big, label=None):
    w, h = (120, 74) if big else (84, 50)
    x0, y0 = x - w / 2, yf - 26 - h
    p.rrect((x0, y0, x0 + w, y0 + h), 10, fill=(32, 46, 70), outline=col, width=3)
    if big:
        p.circle(x0 + 20, yf - 12, 9, (70, 88, 118))
        p.circle(x0 + w - 20, yf - 12, 9, (70, 88, 118))
    else:
        p.line([(x0 + 14, y0), (x + 0, y0 - 22), (x0 + w - 14, y0)], col, 4)
    p.text(x, y0 + h / 2, label if label else str(n), F(34 if big else 28, "ExtraBold"), WHITE)


def static_scene():
    img = Image.new("RGBA", (W * S, H * S), BG + (255,))
    p = Pen(img)
    for lane, (x0, x1) in COLS.items():
        col = A_C if lane == "A" else B_C
        name = "KASSE 1" if lane == "A" else "KASSE 2"
        p.rrect((x0, 405, x1, 1560), 18, fill=PANEL, outline=LINE, width=2)
        p.text((x0 + x1) / 2, 380, name, F(30, "ExtraBold"), col)
        # Kassentisch + Band
        p.rrect((x0 + 30, DESK_Y - 40, x1 - 30, DESK_Y + 40), 12, fill=(36, 50, 74))
        for xx in range(int(x0 + 50), int(x1 - 120), 26):
            p.line([(xx, DESK_Y - 10), (xx + 12, DESK_Y - 10)], (60, 78, 108), 4)
        p.rrect((x1 - 110, DESK_Y - 30, x1 - 45, DESK_Y + 20), 8, fill=(24, 34, 52))
    p.rect((0, 1560, W, 1566), fill=LINE)
    return img


def draw_lanes(img, tv, T, moving):
    p = Pen(img)
    for lane, (x0, x1) in COLS.items():
        col = A_C if lane == "A" else B_C
        cx = (x0 + x1) / 2
        big = lane == "A"
        done, cur = lane_state(lane, T)
        off = queue_offset(lane, T)
        sched = SCHED[lane]
        # Scanner-Licht
        if cur and cur[1] == "scan" and moving:
            on = (tv * 8) % 1 < 0.5
            p.circle(x1 - 78, DESK_Y - 5, 9, (255, 80, 80) if on else (90, 40, 40))
        # Kunden (inkl. DU am Ende)
        for k in range(len(sched) + 1):
            is_you = k == len(sched)
            if k < len(sched) and T >= sched[k][2] + 6:
                continue  # schon gegangen
            slot = k - off
            yf = SLOT0 + max(slot, 0) * SLOT_H
            xf = cx - 70
            walking = moving and abs(slot - round(slot)) > 0.02
            if k < len(sched) and T >= sched[k][2]:  # verlässt die Kasse
                f = ease((T - sched[k][2]) / 6.0)
                figure(p, xf + 190 * f, SLOT0 - 50 * f, col, WHITE, tv * 14, moving)
                continue
            if is_you:
                figure(p, xf, yf, AMBER, WHITE, tv * 14, walking)
                pill(p, xf + 95, yf - 50, "DU", AMBER, 24)
                continue
            figure(p, xf, yf, col, WHITE, tv * 14, walking)
            n = sched[k][3]
            label = None
            if cur and cur[0] == k:
                if cur[1] == "scan":
                    n = cur[2]
                else:
                    label = "€"
            elif k < done:
                label = "€"
            cart(p, xf + 110, yf, n, col, big, label)


def lane_card(p, lane, T):
    x0, x1 = COLS[lane]
    col = A_C if lane == "A" else B_C
    done, cur = lane_state(lane, T)
    sched = SCHED[lane]
    people = len(sched) - done
    items = 0
    for k, (s, e_scan, e_pay, n) in enumerate(sched):
        if k > done - 1 and T < e_pay:
            items += cur[2] if cur and cur[0] == k else n
    if cur is None:
        st, stc = "DU BIST DRAN", GREEN
    elif cur[1] == "scan":
        st, stc = "SCANNT", BLUE
    else:
        st, stc = "BEZAHLT", AMBER
    p.rrect((x0, 205, x1, 335), 18, fill=PANEL, outline=LINE, width=2)
    p.text(x0 + 22, 235, "VOR DIR", F(20, "ExtraBold"), col, "lm")
    f = F(16, "ExtraBold")
    w = p.tlen(st, f) + 24
    p.rrect((x1 - 22 - w, 220, x1 - 22, 250), 15, fill=stc)
    p.text(x1 - 22 - w / 2, 235, st, f, BG)
    p.text(x0 + 22, 295, str(people), F(52, "Bold"), WHITE, "lm")
    bw = p.tlen(str(people), F(52, "Bold"))
    p.text(x0 + 30 + bw, 305, "Pers.", F(20, "SemiBold"), DIM, "lm")
    p.text(x1 - 22, 295, f"{items}", F(52, "Bold"), WHITE, "rm")
    p.text(x1 - 22 - p.tlen(f"{items}", F(52, "Bold")) - 8, 305, "Artikel",
           F(20, "SemiBold"), DIM, "rm")


def draw_header(img, T, paused):
    p = Pen(img)
    p.text(540, 105, fmt(T), F(92, "Bold"), WHITE)
    if paused:
        pill(p, 540, 168, "PAUSE", WHITE, 16)
    lane_card(p, "A", T)
    lane_card(p, "B", T)


def overlay(base, tv):
    a, b, n, kind, s0, s1, ov = scene_at(tv)
    if not ov:
        return base
    al = min(1.0, (tv - a) / 0.3, (b - tv) / 0.3)
    if ov == "end":
        al = min(1.0, (tv - a) / 0.3)
    L = layer()
    p = Pen(L)
    t = tv - a
    dy = (1 - ease(t / 0.5)) * 30
    if ov == "intro":
        card(p, (90, 700 + dy, 990, 1010 + dy))
        p.text(540, 780 + dy, "KÜRZESTE SCHLANGE", F(54, "Black"), A_C)
        p.text(540, 845 + dy, "vs", F(34, "Bold"), DIM)
        p.text(540, 910 + dy, "WENIGSTE ARTIKEL", F(54, "Black"), B_C)
        p.text(540, 975 + dy, "Wo bist du schneller dran?", F(30, "SemiBold"), AMBER)
    elif ov == "rules":
        rules = [("3 s PRO ARTIKEL", WHITE), ("40 s PRO KUNDE", AMBER),
                 ("(Begrüßen, Bezahlen, Einpacken)", None)]
        for k, (s, c) in enumerate(rules):
            if t > k * 0.6:
                if c:
                    pill(p, 540, 800 + k * 100, s, c, 40)
                else:
                    p.rrect((200, 975, 880, 1025), 25, fill=(17, 26, 42))
                    p.text(540, 1000, s, F(28, "SemiBold"), WHITE)
    elif ov == "p1":
        card(p, (110, 760, 970, 1060))
        p.text(540, 815, f"NACH {fmt(T_P1)} MIN", F(30, "ExtraBold"), DIM)
        p.text(310, 900, "1 von 2", F(58, "Bold"), A_C)
        p.text(770, 900, "3 von 5", F(58, "Bold"), B_C)
        p.text(310, 955, "fertig", F(26, "SemiBold"), DIM)
        p.text(770, 955, "fertig", F(26, "SemiBold"), DIM)
        p.text(540, 1015, "LANGE SCHLANGE VORNE?", F(30, "ExtraBold"), AMBER)
    elif ov == "p2":
        card(p, (130, 780, 950, 1000))
        p.text(540, 850, "KASSE 2:", F(40, "ExtraBold"), B_C)
        p.text(540, 925, "DU BIST DRAN!", F(68, "Black"), AMBER)
        p.text(540, 975, f"nach {fmt(T_B)} min", F(28, "SemiBold"), WHITE)
    elif ov == "end":
        p.rect((0, 0, W, H), fill=BG + (205,))
        card(p, (110, 640, 970, 1160))
        p.text(540, 700, "ENDSTAND", F(30, "ExtraBold"), DIM)
        rows = [("KASSE 2", "5 Pers. · 34 Art.", B_C, fmt(T_B)),
                ("KASSE 1", "2 Pers. · 95 Art.", A_C, fmt(T_A))]
        for k, (nm, sub, c, v) in enumerate(rows):
            if t > 0.3 + k * 0.5:
                y = 790 + k * 110
                p.text(170, y - 10, nm, F(46, "ExtraBold"), c, "lm")
                p.text(170, y + 32, sub, F(22, "SemiBold"), DIM, "lm")
                p.text(910, y, v, F(60, "Bold"), WHITE, "rm")
        if t > 1.6:
            p.line([(170, 980), (910, 980)], LINE, 2)
            p.text(170, 1050, "DIFFERENZ", F(28, "SemiBold"), DIM, "lm")
            p.text(910, 1035, f"{T_A - T_B:.0f} s", F(56, "Bold"), AMBER, "rm")
            p.text(910, 1095, "LANGE SCHLANGE GEWINNT", F(22, "ExtraBold"), AMBER, "rm")
    return blend(base, L, al)


# ---------- Erklär-Szenen ----------
def draw_chart(img, t):
    p = Pen(img)
    p.text(540, 420, "WOHIN GEHT DIE ZEIT?", F(56, "Black"), AMBER)
    rows = [("KASSE 1", A_C, LANES["A"]), ("KASSE 2", B_C, LANES["B"])]
    X0, X1 = 110, 970
    scale = (X1 - X0) / 380
    k_all = ease(t / 1.6)
    for r, (nm, c, items) in enumerate(rows):
        y = 640 + r * 330
        scan = sum(items) * S_ITEM
        pay = len(items) * S_PAY
        p.text(X0, y - 70, nm, F(40, "ExtraBold"), c, "lm")
        p.text(X1, y - 70, fmt(scan + pay), F(40, "Bold"), WHITE, "rm")
        ws = scan * scale * k_all
        wp = pay * scale * k_all
        p.rrect((X0, y - 40, X0 + max(ws, 1), y + 40), 10, fill=BLUE)
        p.rrect((X0 + ws + 6, y - 40, X0 + ws + 6 + max(wp, 1), y + 40), 10, fill=AMBER)
        if t > 1.7:
            tot = scan + pay
            p.text(X0 + ws / 2, y, f"{scan / tot * 100:.0f} %", F(32, "ExtraBold"), WHITE)
            p.text(X0 + ws + 6 + wp / 2, y, f"{pay / tot * 100:.0f} %", F(32, "ExtraBold"), BG)
            p.text(X0, y + 75, f"{sum(items)} Artikel × 3 s", F(24, "SemiBold"), BLUE, "lm")
            p.text(X1, y + 75, f"{len(items)} Kunden × 40 s", F(24, "SemiBold"), AMBER, "rm")
    # Legende
    p.rrect((250, 1240, 280, 1270), 6, fill=BLUE)
    p.text(295, 1255, "Scannen", F(28, "SemiBold"), WHITE, "lm")
    p.rrect((560, 1240, 590, 1270), 6, fill=AMBER)
    p.text(605, 1255, "Bezahlen & Co.", F(28, "SemiBold"), WHITE, "lm")


def draw_rule(img, t):
    p = Pen(img)
    p.text(540, 520, "FAUSTREGEL", F(40, "ExtraBold"), DIM)
    if t > 0.3:
        card(p, (110, 600, 970, 860))
        p.text(540, 690, "1 KUNDE", F(76, "Black"), AMBER)
        p.text(540, 790, "= 13 ARTIKEL", F(76, "Black"), WHITE)
    if t > 4.5:
        p.text(540, 960, "40 s ÷ 3 s ≈ 13", F(30, "SemiBold"), DIM)
    if t > 6.5:
        pill(p, 540, 1080, "LEUTE × 13  +  ARTIKEL", WHITE, 40)
    if t > 10.0:
        p.text(540, 1200, "Die kleinere Zahl gewinnt.", F(44, "ExtraBold"), GREEN)


def draw_calc(img, t):
    p = Pen(img)
    p.text(540, 470, "NACHGERECHNET", F(40, "ExtraBold"), DIM)
    rows = [("KASSE 1", A_C, "2 × 13 + 95", "121", 0.2),
            ("KASSE 2", B_C, "5 × 13 + 34", "99", 6.5)]
    for r, (nm, c, f, v, t0) in enumerate(rows):
        if t > t0:
            y = 640 + r * 240
            win = r == 1 and t > 12.5
            p.rrect((90, y - 95, 990, y + 95), 24, fill=PANEL, outline=GREEN if win else c,
                    width=5 if win else 3)
            p.text(140, y - 40, nm, F(32, "ExtraBold"), c, "lm")
            p.text(140, y + 25, f, F(52, "Bold"), WHITE, "lm")
            p.text(940, y, v, F(96, "Black"), GREEN if win else WHITE, "rm")
    if t > 12.5:
        pill(p, 540, 1180, "KASSE 2 GEWINNT", GREEN, 44)
    p.text(540, 1370, "Annahmen (Durchschnitt): 3 s pro Artikel, 40 s pro Kunde",
           F(24, "Medium"), DIM)


def draw_outro(img, t):
    p = Pen(img)
    p.text(540, 640, "Zähl nicht nur die Leute –", F(50, "ExtraBold"), WHITE)
    p.text(540, 710, "zähl die Wagen!", F(50, "ExtraBold"), AMBER)
    if t > 4.0:
        p.text(540, 900, "Was soll ich als", F(62, "Black"), WHITE)
        p.text(540, 980, "Nächstes simulieren?", F(62, "Black"), AMBER)
    if t > 7.5:
        pill(p, 540, 1110, "SCHREIB'S IN DIE KOMMENTARE", WHITE, 30)


def draw_caption(img, tv):
    for a, b, words, hl in CAPS:
        if a <= tv < b:
            break
    else:
        return
    p = Pen(img)
    f = F(54, "ExtraBold")
    lines, cur = [], []
    for w in words:
        if cur and p.tlen(" ".join(cur + [w]), f) > 920:
            lines.append(cur)
            cur = []
        cur.append(w)
    lines.append(cur)
    y0 = 1720 - (len(lines) - 1) * 34
    for li, ln in enumerate(lines):
        x = 540 - p.tlen(" ".join(ln), f) / 2
        for w in ln:
            c = AMBER if (w in hl or any(ch.isdigit() for ch in w)) else WHITE
            p.text(x, y0 + li * 68, w, f, c, "lm")
            x += p.tlen(w + " ", f)


# ---------- Frame ----------
_static = None


def frame(i):
    global _static
    if _static is None:
        _static = static_scene()
    tv = i / FPS
    a, b, n, kind, *_ = scene_at(tv)
    if kind in ("hold", "run", "pause"):
        k, T = sim_time(tv)
        img = _static.copy()
        draw_lanes(img, tv, T, k == "run")
        draw_header(img, T, k == "pause")
        img = overlay(img, tv)
    else:
        img = Image.new("RGBA", (W * S, H * S), BG + (255,))
        {"chart": draw_chart, "rule": draw_rule, "calc": draw_calc,
         "outro": draw_outro}[kind](img, tv - a)
    draw_caption(img, tv)
    for a2, *_r in SCENES[8:]:
        d = abs(tv - a2)
        if d < 0.25:
            img.alpha_composite(Image.new("RGBA", img.size, BG + (int(255 * (1 - d / 0.25)),)))
    return img.convert("RGB").reduce(S).tobytes()


# ---------- Ton ----------
def make_sfx(path):
    sr = 44100
    a = np.zeros(int(DURATION * sr))

    def add(t, sig):
        i = int(t * sr)
        sig = sig[: max(0, len(a) - i)]
        a[i:i + len(sig)] += sig

    def tone(freq, dur, vol, decay):
        tt = np.arange(int(dur * sr)) / sr
        return vol * np.sin(2 * np.pi * freq * tt) * np.exp(-tt * decay)

    beep = tone(2400, 0.04, 0.05, 60)
    for st, en, n, kind, s0, s1, ov in SCENES:
        if kind == "run":
            t = st
            while t < en:
                add(t, beep)
                t += 0.3
        if kind == "pause":
            add(st, tone(880, 1.0, 0.12, 4) + tone(1320, 1.0, 0.08, 4))
    add(SCENES[7][0], tone(660, 1.2, 0.12, 3) + tone(990, 1.2, 0.08, 3))
    a = np.clip(a, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


def audio_args(sfx):
    """ffmpeg-Eingänge + Filter: Sprecher (beschleunigt) an Szenenstart + SFX."""
    args, filt, labels = ["-i", sfx], [], ["[1:a]"]
    for k, (st, en, n, *_r) in enumerate(SCENES):
        args += ["-i", os.path.join(AUDIO_DIR, f"n{n:02d}.mp3")]
        ms = int((st + NARR_OFFSET) * 1000)
        filt.append(f"[{k + 2}:a]atempo={TEMPO},aresample=44100,adelay={ms}|{ms},"
                    f"volume=1.6[v{k}]")
        labels.append(f"[v{k}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,"
                f"alimiter=limit=0.95[aout]")
    return args, ";".join(filt)


def main():
    total = int(DURATION * FPS)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    sfx = os.path.join(os.path.dirname(OUT) or ".", "_sfx.wav")
    make_sfx(sfx)
    if AUDIO_DIR:
        a_in, filt = audio_args(sfx)
        cmd += a_in + ["-filter_complex", filt, "-map", "0:v", "-map", "[aout]"]
    else:
        cmd += ["-i", sfx, "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-t", f"{DURATION:.2f}", "-movflags", "+faststart", OUT]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool() as pool:
        for k, buf in enumerate(pool.imap(frame, range(total), chunksize=8)):
            ff.stdin.write(buf)
            if k % 300 == 0:
                print(f"{k}/{total}", flush=True)
    ff.stdin.close()
    ff.wait()
    os.remove(sfx)
    print("fertig:", OUT, f"{DURATION:.1f}s")


if __name__ == "__main__":
    main()
