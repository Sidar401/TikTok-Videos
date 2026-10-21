#!/usr/bin/env python3
"""Fremdes Voiceover (z. B. ElevenLabs) an skript.json anlegen.

Aufruf: python3 scripts/sync.py videos/<name> <audio.mp3>
Findet die Pausen zwischen den Sätzen (ffmpeg silencedetect) und schreibt
assets/voice.wav + timings.json im gleichen Format wie voice.py.
"""
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voice import chunks  # noqa: E402

TAIL = 0.6


def silences(path, noise_db, min_dur):
    err = subprocess.run(
        ["ffmpeg", "-i", str(path), "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(starts, ends))


def duration(path):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout)


def main(video_dir, audio):
    vdir = Path(video_dir).resolve()
    saetze = json.loads((vdir / "skript.json").read_text())["saetze"]
    (vdir / "assets").mkdir(exist_ok=True)
    out = vdir / "assets" / "voice.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=44100", str(out)], check=True)
    total = duration(out)
    need = len(saetze) - 1

    # Pausen innerhalb der Sprache (nicht Anfang/Ende), längste zuerst
    gaps = []
    for noise in (-35, -30, -40, -25):
        for d in (0.18, 0.12, 0.25, 0.08):
            g = [(s, e) for s, e in silences(out, noise, d) if s > 0.05 and e < total - 0.05]
            if len(g) >= need:
                gaps = g
                break
        if gaps:
            break

    lens = [len(s["text"]) for s in saetze]
    expect, acc = [], 0
    for l in lens[:-1]:
        acc += l
        expect.append(total * acc / sum(lens))

    if need and len(gaps) >= need:
        # DP: Satzgrenzen = Pausen, die lang sind UND nahe an der erwarteten Stelle
        # (erwartet = Anteil der Textlänge an der Gesamtdauer)
        mids = [((s + e) / 2, e - s) for s, e in gaps]
        INF = float("inf")
        K, J = len(mids), need
        cost = [[INF] * K for _ in range(J)]
        prev = [[-1] * K for _ in range(J)]
        for j in range(J):
            for k in range(j, K - (J - 1 - j)):
                c = abs(mids[k][0] - expect[j]) - 6 * mids[k][1]
                if j == 0:
                    cost[j][k] = c
                else:
                    best = min(range(j - 1, k), key=lambda q: cost[j - 1][q])
                    cost[j][k] = cost[j - 1][best] + c
                    prev[j][k] = best
        k = min(range(K), key=lambda q: cost[J - 1][q])
        picks = []
        for j in range(J - 1, -1, -1):
            picks.append(k)
            k = prev[j][k]
        bounds = [mids[q][0] for q in reversed(picks)]
        mode = "Pausen + Textlänge"
    else:
        bounds = expect
        mode = "Textlänge (Fallback)"

    edges = [0.0] + bounds + [total]
    timings = []
    for s, a, b in zip(saetze, edges, edges[1:]):
        parts = chunks(s["text"])
        n = sum(len(p) for p in parts)
        caps, ct = [], a
        for p in parts:
            d = (b - a) * len(p) / n
            caps.append({"text": p, "start": round(ct, 3), "end": round(ct + d, 3)})
            ct += d
        timings.append({"id": s["id"], "start": round(a, 3), "end": round(b, 3), "captions": caps})
    dauer = round(total + TAIL, 2)
    (vdir / "timings.json").write_text(json.dumps({"dauer": dauer, "saetze": timings}, ensure_ascii=False, indent=2))
    print(f"{len(saetze)} Sätze an {mode} ausgerichtet, Dauer {dauer}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
