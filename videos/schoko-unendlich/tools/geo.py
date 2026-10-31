"""Berechnet Teile (8x8 -> 5x13), Zahlen und Ton. Schreibt assets/data.js + assets/sfx.wav"""
import json, math, os, subprocess
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Teile ---
src = {
 "A": [(0,0),(5,0),(3,5),(0,5)],
 "B": [(5,0),(8,0),(8,5),(3,5)],
 "T1": [(0,5),(8,5),(8,8)],
 "T2": [(0,5),(8,8),(0,8)],
}
horiz = [
 [(0,0),(5,2),(5,5),(0,5)],          # Trapez unten links
 [(5,2),(13,5),(5,5)],               # Dreieck unten
 [(0,0),(8,0),(8,3)],                # Dreieck oben
 [(8,0),(13,0),(13,5),(8,3)],        # Trapez oben rechts
]
dest = [[(5 - y, x) for (x, y) in p] for p in horiz]  # 90° gedreht -> Turm 5 breit, 13 hoch

def centroid(p):
    return (sum(x for x, _ in p) / len(p), sum(y for _, y in p) / len(p))

def fit(sp, dp):
    n = len(sp)
    if len(dp) != n: return None
    cs, cd = centroid(sp), centroid(dp)
    for order in (dp, dp[::-1]):
        for sh in range(n):
            d = order[sh:] + order[:sh]
            ax, ay = sp[0][0]-cs[0], sp[0][1]-cs[1]
            bx, by = d[0][0]-cd[0], d[0][1]-cd[1]
            th = math.atan2(by, bx) - math.atan2(ay, ax)
            c, s = math.cos(th), math.sin(th)
            ok = all(abs(cd[0] + c*(x-cs[0]) - s*(y-cs[1]) - X) < 1e-6 and abs(cd[1] + s*(x-cs[0]) + c*(y-cs[1]) - Y) < 1e-6
                     for (x, y), (X, Y) in zip(sp, d))
            if ok:
                th = (th + math.pi) % (2*math.pi) - math.pi
                return th, cd
    return None

pieces, used = [], set()
for name, sp in src.items():
    for i, dp in enumerate(dest):
        if i in used: continue
        r = fit(sp, dp)
        if r:
            used.add(i); th, cd = r
            pieces.append(dict(name=name, poly=sp, c0=centroid(sp), c1=cd, th=th))
            break
    else:
        raise SystemExit("kein Partner für " + name)
gap = [(5 - y, x) for (x, y) in [(0,0),(5,2),(13,5),(8,3)]]

# --- Zahlen ---
def fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
S = 0.025  # Kantenlänge eines Stücks in m
def de(n): return f"{n:,}".replace(",", ".")
def dec(x, d):
    s = f"{x:.{d}f}".replace(".", ",")
    return s
def length(m):
    if m >= 1000: return (dec(m/1000, 0 if m >= 100000 else 1) if m < 1e6 else de(round(m/1000))) + " km"
    if m >= 1: return dec(m, 0 if m >= 100 else 1) + " m"
    return dec(m*100, 0) + " cm"
def gapfmt(m):
    if m >= 1e-3: return dec(m*1e3, 2) + " mm"
    if m >= 1e-6: return dec(m*1e6, 1 if m < 1e-5 else 0) + " µm"
    return dec(m*1e9, 2 if m < 1e-8 else 0) + " nm"

compare = {
 8: ("Tisch", 0.75, "table", ""),
 21: ("Tisch", 0.75, "table", ""),
}
steps_def = [
 (8,  "table",   "Tisch", 0.75, ""),
 (12, "giraffe", "Giraffe", 5.5, ""),
 (16, "house",   "Haus", 10, "dünner als ein Haar!"),
 (20, "dom",     "Kölner Dom", 157, ""),
 (24, "burj",    "Burj Khalifa", 828, "dünner als eine Bakterie!"),
 (28, "everest", "Mount Everest", 8849, ""),
 (32, "plane",   "Flugzeug", 10000, ""),
 (36, "iss",     "Raumstation", 420000, "so dünn wie DNA!"),
 (40, "moon",    "Mond", 3474000, "etwa 1 ATOM!"),
]
steps = []
for n, kind, cname, ch, note in steps_def:
    F, a, b = fib(n), fib(n-1), fib(n+1)
    assert a*b == F*F + 1
    tower = b * S
    g = 2*S/math.hypot(a, b)
    steps.append(dict(F=F, a=a, b=b, sq=de(F*F), sq1=de(a*b), tower=length(tower), towerM=tower,
                      gap=gapfmt(g), kind=kind, cname=cname, cname_h=length(ch) if kind!="moon" else "3.474 km breit",
                      cH=ch, note=note))
g0 = 2*S/math.hypot(5, 13)
first = dict(tower=length(13*S), gap=gapfmt(g0))
for s in steps: print(s["sq"], "->", s["sq1"], s["tower"], s["gap"], s["note"])
print("8x8:", first)

with open(os.path.join(ROOT, "assets", "data.js"), "w") as f:
    f.write("window.SCHOKO = " + json.dumps(dict(pieces=pieces, gap=gap, steps=steps, first=first), ensure_ascii=False) + ";\n")
