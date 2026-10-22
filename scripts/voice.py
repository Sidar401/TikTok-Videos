#!/usr/bin/env python3
"""Voiceover + Untertitel-Timings aus skript.json erzeugen (Piper, offline).

Aufruf: python3 scripts/voice.py videos/<name>
Liest  videos/<name>/skript.json  -> {"saetze": [{"id": "s1", "text": "...", "sprechtext": "..."?}]}
Schreibt videos/<name>/assets/voice.wav und videos/<name>/timings.json
"""
import json, re, subprocess, sys, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICES = Path("/root/tts")
GAP = 0.12          # Pause zwischen Sätzen (s)
TAIL = 0.6          # Stille am Ende (s)
MAX_WORDS, MAX_CHARS = 6, 32  # pro Untertitel-Box
# Nach diesen Wörtern nie eine Untertitel-Box beenden (gehören zum nächsten Wort)
KLEBEWOERTER = {"der", "die", "das", "dem", "den", "des", "ein", "eine", "einen", "einem", "einer", "im", "in", "am", "an",
                "zum", "zur", "mit", "von", "vom", "für", "auf", "aus", "bei", "nach", "und", "oder", "aber", "zu", "dein",
                "deine", "deinen", "deinem", "mein", "meine", "unser", "unsere", "wenn", "dass", "weil", "als", "wie", "so"}


def _even(words):
    """Wortliste in möglichst wenige, gleich lange Teile (nach Zeichen) teilen; nie direkt nach einer Zahl trennen."""
    from itertools import combinations
    n = 1
    while n <= len(words):
        best = None
        for cuts in combinations(range(1, len(words)), n - 1):
            if any(re.fullmatch(r"[\d.,]+(\x01[€%])?", words[c - 1]) or words[c - 1].lower() in KLEBEWOERTER for c in cuts):
                continue
            idx = (0,) + cuts + (len(words),)
            parts = [" ".join(words[a:b]) for a, b in zip(idx, idx[1:])]
            if all(len(p.split()) <= MAX_WORDS and len(p) <= MAX_CHARS for p in parts):
                score = max(len(p) for p in parts)
                if best is None or score < best[0]:
                    best = (score, parts)
        if best:
            return best[1]
        n += 1
    return words


def chunks(text):
    """Text in Untertitel-Boxen teilen: zuerst an Kommas, dann gleichmäßig (max. MAX_WORDS / MAX_CHARS)."""
    text = re.sub(r"(\d) ([€%])", "\\1\x01\\2", text)  # Zahl und Einheit nie trennen
    clauses, cur = [], []
    for w in text.split():
        cur.append(w)
        if w.endswith(","):
            clauses.append(cur); cur = []
    if cur:
        clauses.append(cur)
    # sehr kurze Teilsätze mit dem nächsten zusammenlegen
    merged = []
    for c in clauses:
        if merged and len(merged[-1]) < 3 and len(" ".join(merged[-1] + c)) <= MAX_CHARS:
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    parts = [p for c in merged for p in _even(c)]
    return [p.replace("\x01", "\u00a0").replace("-", "\u2011") for p in parts]


def main(video_dir):
    vdir = Path(video_dir).resolve()
    kanal = json.loads((ROOT / "kanal.json").read_text())
    model = VOICES / f"de-{kanal['stimme']}-low.onnx"
    saetze = json.loads((vdir / "skript.json").read_text())["saetze"]
    tmp = vdir / ".voice"; tmp.mkdir(exist_ok=True)
    (vdir / "assets").mkdir(exist_ok=True)

    timings, frames, t, rate = [], [], 0.0, None
    for i, s in enumerate(saetze):
        raw = tmp / f"{i:03d}.wav"
        subprocess.run(
            [sys.executable, "-m", "piper", "-m", str(model), "--length-scale", str(kanal["tempo"]), "-f", str(raw)],
            input=s.get("sprechtext", s["text"]).encode(), check=True, stderr=subprocess.DEVNULL,
        )
        with wave.open(str(raw)) as w:
            rate = w.getframerate()
            data = w.readframes(w.getnframes())
            dur = w.getnframes() / rate
        frames.append(data + b"\x00\x00" * int(GAP * rate))
        parts = chunks(s["text"])
        total = sum(len(p) for p in parts)
        caps, ct = [], t
        for p in parts:
            d = dur * len(p) / total
            caps.append({"text": p, "start": round(ct, 3), "end": round(ct + d, 3)})
            ct += d
        timings.append({"id": s["id"], "start": round(t, 3), "end": round(t + dur + GAP, 3), "captions": caps})
        t += dur + GAP

    raw_all = tmp / "all.wav"
    with wave.open(str(raw_all), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b"".join(frames) + b"\x00\x00" * int(TAIL * rate))
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(raw_all), "-af",
         "highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,"
         "loudnorm=I=-14:TP=-1.5:LRA=7,aresample=44100", str(vdir / "assets" / "voice.wav")],
        check=True,
    )
    total = round(t + TAIL, 2)
    (vdir / "timings.json").write_text(json.dumps({"dauer": total, "saetze": timings}, ensure_ascii=False, indent=2))
    print(f"voice.wav + timings.json: {total}s, {len(saetze)} Sätze")


if __name__ == "__main__":
    main(sys.argv[1])
