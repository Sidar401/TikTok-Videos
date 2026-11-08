#!/usr/bin/env python3
"""Pausen kürzen + auf Ziel-Länge bringen, Wort-Zeiten aus ElevenLabs-Alignment.

Aufruf: python3 wissen/kit/schnitt.py videos/<name> [ziel=29.4] [gap=0.18] [maxtempo=1.12]
liest:   assets/voice-orig.mp3, alignment.json (von stimme.py)
schreibt: assets/voice.wav, words.json ({"words":[{w,s,e}], "chunks":[[s,e],...]}  – ein Chunk pro Zeile)
"""
import json, subprocess, sys
from pathlib import Path

proj = Path(sys.argv[1])
ZIEL = float(sys.argv[2]) if len(sys.argv) > 2 else 29.4
GAP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.18
MAXT = float(sys.argv[4]) if len(sys.argv) > 4 else 1.12
d = json.load(open(proj / "alignment.json"))
a = d["alignment"]; ch, cs, ce = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]

# Zeilen und Wörter aus den Zeichen bauen
lines, words, cur, line = [], [], None, []
for c, s, e in zip(ch, cs, ce):
    if c in " \n":
        if cur: line.append(cur); cur = None
        if c == "\n" and line: lines.append(line); line = []
        continue
    if cur is None: cur = {"w": "", "s": s, "e": e}
    cur["w"] += c; cur["e"] = e
if cur: line.append(cur)
if line: lines.append(line)

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice-orig.mp3")], capture_output=True, text=True).stdout)
segs = []
for i, ln in enumerate(lines):
    s0 = max(0.0, ln[0]["s"] - 0.05); s1 = min(dur, ln[-1]["e"] + (0.25 if i == len(lines) - 1 else 0.08))
    segs.append((s0, s1))
speech = sum(b - a for a, b in segs) + GAP * (len(segs) - 1)
tempo = max(1.0, min(MAXT, speech / ZIEL))
f = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[s{i}];" for i, (a, b) in enumerate(segs))
# Lücken als Stille einfügen
parts = []
for i in range(len(segs)):
    parts.append(f"[s{i}]")
    if i < len(segs) - 1:
        f += f"aevalsrc=0:d={GAP}:s=44100[z{i}];"; parts.append(f"[z{i}]")
f += "".join(f"[s{i}]aresample=44100,aformat=channel_layouts=mono[m{i}];" for i in range(len(segs)))
parts = [p.replace("[s", "[m") for p in parts]
f += "".join(parts) + f"concat=n={len(parts)}:v=0:a=1,atempo={tempo}[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(proj / "assets/voice-orig.mp3"), "-filter_complex", f, "-map", "[o]", "-ar", "44100", "-ac", "1", str(proj / "assets/voice.wav")], check=True)

out, chunks, off = [], [], 0.0
for (a0, a1), ln in zip(segs, lines):
    m = lambda t: round((off + t - a0) / tempo, 3)
    for w in ln: out.append({"w": w["w"], "s": m(w["s"]), "e": m(w["e"])})
    chunks.append([m(ln[0]["s"]), m(ln[-1]["e"])])
    off += (a1 - a0) + GAP
json.dump({"words": out, "chunks": chunks, "tempo": tempo}, open(proj / "words.json", "w"), ensure_ascii=False)
neu = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(proj / "assets/voice.wav")], capture_output=True, text=True).stdout)
print(f"Tempo {tempo:.3f} · neue Länge {neu:.2f} s · {len(lines)} Zeilen · {len(out)} Wörter")
