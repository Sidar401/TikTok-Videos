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
GAPW = float(__import__("os").environ.get("GAPW", 3))


def envelope(path):
    """Silben-Spitzen und Lautstärke-Täler (Zeiten in s) aus der Hüllkurve."""
    import numpy as np
    from scipy.signal import find_peaks
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float)
    hop = 160
    e = np.sqrt(np.convolve(x ** 2, np.ones(400) / 400, "same")[::hop])
    e = np.convolve(e, np.ones(5) / 5, "same")
    pk, _ = find_peaks(e, distance=10, prominence=e.max() * 0.06)
    dp, _ = find_peaks(-e, distance=15, prominence=e.max() * 0.25)
    return list(pk * hop / 16000), list(dp * hop / 16000)


def piper_dauer(text, model="/root/tts/de-thorsten-low.onnx"):
    """Sprechdauer eines Satzes mit Piper messen (None, wenn Piper fehlt)."""
    import tempfile
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            subprocess.run([sys.executable, "-m", "piper", "-m", model, "--sentence-silence", "0", "--noise-w", "0", "--noise-scale", "0", "-f", f.name],
                           input=text.encode(), stderr=subprocess.DEVNULL, check=True)
            with wave.open(f.name) as w:
                return w.getnframes() / w.getframerate()
    except Exception:
        return None


def silben(text):
    """Grobe Silbenzahl (Vokalgruppen) – Maß für die Sprechdauer eines Satzes.
    Abkürzungen in Großbuchstaben (ETF, TV) werden buchstabiert, Ziffern grob mitgezählt."""
    n = 0
    for w in re.findall(r"[\wÄÖÜäöüß%€]+", text):
        if len(w) >= 2 and w.isupper() and w.isalpha():
            n += len(w)
        elif re.fullmatch(r"[A-ZÄÖÜ][a-zäöüß]+[A-Z]{2,}", w):  # z. B. HundeFinanzTV
            m = re.match(r"([A-ZÄÖÜ][a-zäöüß]+.*?)([A-Z]{2,})$", w)
            n += len(re.findall(r"[aeiouyäöü]+", m.group(1).lower())) + len(m.group(2))
        elif w.isdigit():
            n += 2 * len(w)
        elif w in ("%", "€"):
            n += 2
        else:
            n += max(1, len(re.findall(r"[aeiouyäöü]+", w.lower())))
    return max(1, n)


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

    # Kandidaten für Satzgrenzen: Pausen + kurze Lautstärke-Täler (ElevenLabs macht nicht immer Pausen)
    _, dips = envelope(orig)
    cands = {round((s + e) / 2, 3): e - s for s, e in silences(orig, -35, 0.06) if s > 0.05 and e < total - 0.05}
    for t in dips:
        if all(abs(t - m) > 0.15 for m in cands):
            cands[round(t, 3)] = 0.0
    mids = sorted(cands.items())

    # Erwartete Satzdauer: jeden Satz kurz mit Piper sprechen lassen (erfasst Zahlen, Abkürzungen, Satzlänge)
    est = [piper_dauer(s.get("sprechtext", s["text"])) for s in saetze]
    if None in est:
        est = [float(silben(s.get("sprechtext", s["text"]))) for s in saetze]
    e = [x * total / sum(est) for x in est]

    if need and len(mids) >= need:
        # DP über Satzdauern: jede Satzlänge nah an der Schätzung, Grenzen bevorzugt in echten Pausen
        pos = [0.0] + [m for m, _ in mids] + [total]
        gap = [0.0] + [g for _, g in mids] + [0.0]
        N, J, INF = len(pos), len(saetze), float("inf")
        cost = [[INF] * N for _ in range(J + 1)]
        prev = [[-1] * N for _ in range(J + 1)]
        cost[0][0] = 0.0
        for j in range(1, J + 1):
            for i in range(1, N):
                if (j == J) != (i == N - 1):
                    continue
                for q in range(i):
                    if cost[j - 1][q] == INF:
                        continue
                    c = cost[j - 1][q] + abs(pos[i] - pos[q] - e[j - 1]) - GAPW * min(gap[i], 0.6)
                    if c < cost[j][i]:
                        cost[j][i], prev[j][i] = c, q
        i, bounds = N - 1, []
        for j in range(J, 0, -1):
            i = prev[j][i]
            bounds.append(pos[i])
        bounds = list(reversed(bounds))[1:]
        mode = "Pausen + geschätzte Satzdauer"
    else:
        acc, bounds = 0.0, []
        for x in e[:-1]:
            acc += x
            bounds.append(acc)
        mode = "geschätzte Satzdauer (Fallback)"

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
