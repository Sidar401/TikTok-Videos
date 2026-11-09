#!/usr/bin/env python3
"""Pausen kürzen + auf Ziel-Länge bringen, Wort-Zeiten aus ElevenLabs-Alignment.

Aufruf: python3 wissen/kit/schnitt.py videos/<name> [ziel=29.4] [gap=0.18] [maxtempo=1.12]
liest:   assets/voice-orig.mp3, alignment.json (von stimme.py)
schreibt: assets/voice.wav, words.json ({"words":[{w,s,e}], "chunks":[[s,e],...]}  – ein Chunk pro Zeile)

Wichtig (Fehler vom 09.11.): Geschnitten wird NUR in echter Stille. Spricht der Sprecher ohne Pause
weiter, bleibt die Stelle ungeschnitten. Jeder Schnitt bekommt eine kurze Blende (kein Knacken).
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

proj = Path(sys.argv[1])
ZIEL = float(sys.argv[2]) if len(sys.argv) > 2 else 29.4
GAP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.18
MAXT = float(sys.argv[4]) if len(sys.argv) > 4 else 1.12
src = str(proj / "assets/voice-orig.mp3")
a = json.load(open(proj / "alignment.json"))["alignment"]
ch, cs, ce = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]

# Zeilen und Wörter aus den Zeichen
lines, cur, line = [], None, []
for c, s, e in zip(ch, cs, ce):
    if c in " \n":
        if cur: line.append(cur); cur = None
        if c == "\n" and line: lines.append(line); line = []
        continue
    if cur is None: cur = {"w": "", "s": s, "e": e}
    cur["w"] += c; cur["e"] = e
if cur: line.append(cur)
if line: lines.append(line)

SR = 44100
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(float) / 32768
dur = len(x) / SR
hop = int(SR * 0.005); w = int(SR * 0.02)
env = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, "same"))[::hop]
th = max(env.max() * 0.02, 1e-4)  # "Stille" = unter 2 % der lautesten Stelle

segs, start = [], 0.0
for i in range(len(lines) - 1):
    e_i, s_n = lines[i][-1]["e"], lines[i + 1][0]["s"]
    ia, ib = int((min(e_i, s_n) - 0.05) * SR / hop), int((max(e_i, s_n) + 0.05) * SR / hop)
    ia, ib = max(0, ia), min(len(env) - 1, max(ib, ia + 1))
    im = ia + int(np.argmin(env[ia:ib + 1]))
    if env[im] >= th: continue  # keine echte Pause -> nicht schneiden
    a_, b_ = im, im
    while a_ > 0 and env[a_ - 1] < th: a_ -= 1
    while b_ < len(env) - 1 and env[b_ + 1] < th: b_ += 1
    sa, sb = a_ * hop / SR, b_ * hop / SR
    if sb - sa > GAP + 0.02:
        segs.append((start, sa + GAP / 2)); start = sb - GAP / 2
segs.append((start, min(dur, lines[-1][-1]["e"] + 0.35)))

speech = sum(b - a for a, b in segs)
tempo = max(1.0, min(MAXT, speech / ZIEL))
F = 0.012
f = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d={F},afade=t=out:st={max(0.0, b - a - F):.4f}:d={F}[s{i}];" for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1,atempo={tempo}[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", f, "-map", "[o]", "-ar", "44100", "-ac", "1", str(proj / "assets/voice.wav")], check=True)

def mapt(t):
    off = 0.0
    for a_, b_ in segs:
        if t <= b_: return round((off + max(0.0, t - a_)) / tempo, 3)
        off += b_ - a_
    return round(off / tempo, 3)

out, chunks = [], []
for ln in lines:
    for wd in ln: out.append({"w": wd["w"], "s": mapt(wd["s"]), "e": mapt(wd["e"])})
    chunks.append([mapt(ln[0]["s"]), mapt(ln[-1]["e"])])
json.dump({"words": out, "chunks": chunks, "tempo": tempo}, open(proj / "words.json", "w"), ensure_ascii=False)
neu = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice.wav")], capture_output=True, text=True).stdout)
print(f"Tempo {tempo:.3f} · neue Länge {neu:.2f} s · {len(lines)} Zeilen · {len(out)} Wörter · {len(segs) - 1} Schnitte (nur in Stille)")
