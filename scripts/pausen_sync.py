"""Satzgrenzen an echten Sprechpausen ausrichten (wenn DTW ungenau ist).

  python3 scripts/pausen_sync.py videos/<name>/

Erwartete Satzlängen kommen von Piper (Verhältnisse), die Grenzen werden per DP auf die
Pausen in assets/voice.wav gelegt. Untertitel werden proportional neu verteilt; timings.json wird überschrieben.
"""
import json
import re
import subprocess
import sys

import librosa

sys.path.insert(0, __import__("os").path.dirname(__file__))
from dtw_align import SR, piper_wav  # noqa: E402

v = sys.argv[1]
T = json.load(open(v + "timings.json"))
sk = {s["id"]: s["sprechtext"] for s in json.load(open(v + "skript.json"))["saetze"]}
ids = [s["id"] for s in T["saetze"]]
n = len(ids)

out = subprocess.run(["ffmpeg", "-v", "info", "-i", v + "assets/voice.wav", "-af", "silencedetect=n=-35dB:d=0.08", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
pausen = list(zip(st, en))
sprech_start = pausen[0][1] if pausen and pausen[0][0] < 0.05 else 0.0
sprech_ende = pausen[-1][0] if pausen and en[-1] >= librosa.get_duration(path=v + "assets/voice.wav") - 0.05 else librosa.get_duration(path=v + "assets/voice.wav")
kand = [((a + b) / 2, b - a) for a, b in pausen if sprech_start + 0.3 < (a + b) / 2 < sprech_ende - 0.3]

laengen = [len(librosa.effects.trim(piper_wav(sk[i]), top_db=35)[0]) / SR for i in ids]
ges = sum(laengen)
erwartet = []
acc = 0.0
for L in laengen[:-1]:
    acc += L
    erwartet.append(sprech_start + (sprech_ende - sprech_start) * acc / ges)

# DP: n-1 Grenzen aus Kandidaten (aufsteigend), Kosten = Abweichung² − Pausenbonus
INF = 1e18
m = len(kand)
dp = [[INF] * m for _ in range(n - 1)]
bp = [[-1] * m for _ in range(n - 1)]
for j in range(m):
    dp[0][j] = (kand[j][0] - erwartet[0]) ** 2 - 2.0 * kand[j][1]
for k in range(1, n - 1):
    best, bi = INF, -1
    for j in range(m):
        if j - 1 >= 0 and dp[k - 1][j - 1] < best:
            best, bi = dp[k - 1][j - 1], j - 1
        if best < INF:
            dp[k][j] = best + (kand[j][0] - erwartet[k]) ** 2 - 2.0 * kand[j][1]
            bp[k][j] = bi
j = min(range(m), key=lambda x: dp[n - 2][x])
wahl = []
for k in range(n - 2, -1, -1):
    wahl.append(kand[j][0])
    j = bp[k][j]
wahl = wahl[::-1]

grenzen = [0.0] + wahl + [T["dauer"]]
for i, s in enumerate(T["saetze"]):
    a, b = grenzen[i], grenzen[i + 1]
    texts = [c["text"] for c in s["captions"]]
    L = sum(map(len, texts))
    cur, caps = a, []
    for x in texts:
        e = cur + (b - a) * len(x) / L
        caps.append({"text": x, "start": round(cur, 3), "end": round(e, 3)})
        cur = e
    s["start"], s["end"], s["captions"] = round(a, 3), round(b, 3), caps
json.dump(T, open(v + "timings.json", "w"), ensure_ascii=False, indent=1)
for s, e in zip(T["saetze"], erwartet + [None]):
    print(s["id"], s["start"], round(s["end"] - s["start"], 2))
