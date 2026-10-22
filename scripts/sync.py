#!/usr/bin/env python3
"""Fremdes Voiceover (z. B. ElevenLabs) an skript.json anlegen.

Aufruf: python3 scripts/sync.py videos/<name> <audio.mp3> [--tempo 1.08] [--pause 0.25]
  --tempo  schneller sprechen (Tonhöhe bleibt), Standard 1.08
  --pause  Pausen länger als dieser Wert (s) werden darauf gekürzt, Standard 0.25
Findet die Pausen zwischen den Sätzen (ffmpeg silencedetect) und schreibt
assets/voice.wav + timings.json im gleichen Format wie voice.py.
"""
import json, re, subprocess, sys, wave
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


def tighten(src, dst, tempo, max_pause):
    """Pausen auf max_pause kürzen, dann Tempo erhöhen (atempo, Tonhöhe bleibt)."""
    raw = dst.with_suffix(".raw.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", "44100", str(raw)], check=True)
    with wave.open(str(raw)) as w:
        rate = w.getframerate()
        pcm = w.readframes(w.getnframes())
    keep, pos, segs, new = [], 0, [], 0
    for s, e in silences(raw, -35, max_pause):
        a, b = int(s * rate) * 2, int(e * rate) * 2
        half = int(max_pause / 2 * rate) * 2
        keep.append(pcm[pos:a + half])
        segs.append((pos / 2 / rate, (a + half) / 2 / rate, new / 2 / rate))
        new += a + half - pos
        pos = max(a + half, b - half)
    keep.append(pcm[pos:])
    segs.append((pos / 2 / rate, len(pcm) / 2 / rate, new / 2 / rate))
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b"".join(keep))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                    f"atempo={tempo},loudnorm=I=-14:TP=-1.5:LRA=7,aresample=44100", str(dst)], check=True)
    raw.unlink()

    def fmap(t):
        """Zeit im Original -> Zeit in der gekürzten, schnelleren Fassung."""
        for oa, ob, na in segs:
            if t <= ob:
                return (na + max(0.0, t - oa)) / tempo
        oa, ob, na = segs[-1]
        return (na + ob - oa) / tempo
    return fmap


def main(video_dir, audio, tempo=1.08, max_pause=0.25):
    vdir = Path(video_dir).resolve()
    saetze = json.loads((vdir / "skript.json").read_text())["saetze"]
    (vdir / "assets").mkdir(exist_ok=True)
    out = vdir / "assets" / "voice.wav"
    before = duration(audio)
    fmap = tighten(Path(audio), out, tempo, max_pause)
    # Satzgrenzen im Original suchen (dort sind die Pausen noch aussagekräftig)
    orig = vdir / ".voice-orig.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-ac", "1", "-ar", "44100", str(orig)], check=True)
    total = duration(orig)
    need = len(saetze) - 1

    # Pausen innerhalb der Sprache (nicht Anfang/Ende), längste zuerst
    gaps = []
    for noise in (-35, -30, -40, -25):
        for d in (0.18, 0.12, 0.25, 0.08):
            g = [(s, e) for s, e in silences(orig, noise, d) if s > 0.05 and e < total - 0.05]
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

    orig.unlink()
    edges = [0.0] + bounds + [total]
    timings = []
    for s, a, b in zip(saetze, edges, edges[1:]):
        parts = chunks(s["text"])
        n = sum(len(p) for p in parts)
        caps, ct = [], a
        for p in parts:
            d = (b - a) * len(p) / n
            caps.append({"text": p, "start": round(fmap(ct), 3), "end": round(fmap(ct + d), 3)})
            ct += d
        timings.append({"id": s["id"], "start": round(fmap(a), 3), "end": round(fmap(b), 3), "captions": caps})
    dauer = round(duration(out) + TAIL, 2)
    (vdir / "timings.json").write_text(json.dumps({"dauer": dauer, "saetze": timings}, ensure_ascii=False, indent=2))
    print(f"{len(saetze)} Sätze an {mode} ausgerichtet, {before:.1f}s -> {dauer}s (Tempo {tempo}, Pausen max {max_pause}s)")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("video_dir"); ap.add_argument("audio")
    ap.add_argument("--tempo", type=float, default=1.08)
    ap.add_argument("--pause", type=float, default=0.25)
    a = ap.parse_args()
    main(a.video_dir, a.audio, a.tempo, a.pause)
