"""Berechnet die Stöße (echte Physik) + Zeitplan und erzeugt Klack-Ton.
Ausgabe: assets/data.js und assets/klacks.wav"""
import json, math, wave, sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Segmente: Masse, Startzeit, Zeiten (Video-Sekunden)
SEGS = [
    dict(M=1,     label="1 kg",      bw=0.9, T0=0.0,  intro=0.5, approach=1.1, span=1.5, exit=1.4, end=6.4),
    dict(M=100,   label="100 kg",    bw=1.35, T0=6.4, intro=0.4, approach=1.0, span=3.4, exit=1.3, end=13.8),
    dict(M=10000, label="10.000 kg", bw=2.3, T0=13.8, intro=0.4, approach=1.0, span=6.6, exit=1.2, end=23.4),
]
W1 = 0.9          # Breite kleiner Block (Einheiten)
X1 = 2.6          # Start kleiner Block (linke Kante)
X2 = 8.2          # Start grosser Block
V0 = 1.0

def simulate(M):
    m1 = 1.0
    x1, x2, v1, v2, s = X1, X2, 0.0, -V0, 0.0
    ev = [dict(s=0.0, x1=x1, x2=x2, v1=v1, v2=v2, kind="start")]
    while True:
        tb = (x2 - x1 - W1) / (v1 - v2) if v1 > v2 else math.inf
        tw = x1 / (-v1) if v1 < 0 else math.inf
        dt = min(tb, tw)
        if dt == math.inf:
            break
        s += dt; x1 += v1 * dt; x2 += v2 * dt
        if tb <= tw:
            x2 = x1 + W1
            n1 = ((m1 - M) * v1 + 2 * M * v2) / (m1 + M)
            n2 = ((M - m1) * v2 + 2 * m1 * v1) / (m1 + M)
            v1, v2, kind = n1, n2, "block"
        else:
            x1 = 0.0; v1 = -v1; kind = "wall"
        ev.append(dict(s=s, x1=x1, x2=x2, v1=v1, v2=v2, kind=kind))
    return ev

out = []
clack_times = []
for g in SEGS:
    ev = simulate(g["M"])
    n = len(ev) - 1
    t_first = g["T0"] + g["intro"] + g["approach"]
    dt = g["span"] / max(n - 1, 1)
    T = [g["T0"] + g["intro"]] + [t_first + k * dt for k in range(n)]
    # Ende: noch 6 Einheiten weiterlaufen
    last = ev[-1]
    exit_sim = 6.5
    T_end = T[-1] + g["exit"]
    print(g["M"], "Klacks:", n, file=sys.stderr)
    clack_times += [(t, e["kind"]) for t, e in zip(T[1:], ev[1:])]
    sq = math.sqrt(1.0 / g["M"])
    out.append(dict(
        M=g["M"], label=g["label"], bw=g["bw"], T0=g["T0"], end=g["end"], n=n,
        tStart=T[0], tEnd=T_end, exitSim=exit_sim,
        ev=[[round(e["s"], 9), round(e["x1"], 9), round(e["x2"], 9), round(e["v1"], 9), round(e["v2"], 9),
             1 if e["kind"] == "wall" else 0] for e in ev],
        T=[round(t, 5) for t in T],
        pts=[[round(e["v2"] / V0, 6), round(sq * e["v1"] / V0, 6)] for e in ev],
    ))

with open(os.path.join(ROOT, "assets", "data.js"), "w") as f:
    f.write("window.KLACK_DATA = " + json.dumps({"w1": W1, "segs": out}, separators=(",", ":")) + ";\n")

# --- Klack-Ton (kurzer Holz-Klack, je Stoss leicht variiert) ---
SR = 44100; DUR = 27.0
buf = np.zeros(int(SR * DUR) + SR)
rng = np.random.default_rng(7)

def clack(freq, amp):
    n = int(SR * 0.05)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n) * np.exp(-t * 420)
    tone = (np.sin(2 * np.pi * freq * t) * 0.9 + np.sin(2 * np.pi * freq * 2.37 * t) * 0.35) * np.exp(-t * 95)
    thump = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 60) * 0.4
    return amp * (0.45 * noise + tone + thump)

for i, (t, kind) in enumerate(clack_times):
    base = 1500 if kind == "block" else 1150
    c = clack(base * (1 + rng.uniform(-0.06, 0.06)), rng.uniform(0.75, 1.0))
    i0 = int((t + 1 / 30) * SR)  # Ton 1 Frame nach dem Bild
    buf[i0:i0 + len(c)] += c
buf = buf[: int(SR * DUR)]
buf = buf / np.max(np.abs(buf)) * 0.85
pcm = (buf * 32767).astype(np.int16)
with wave.open(os.path.join(ROOT, "assets", "klacks.wav"), "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", len(clack_times), file=sys.stderr)
