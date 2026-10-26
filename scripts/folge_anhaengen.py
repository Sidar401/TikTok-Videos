"""Fehlenden Schluss-Satz „Folge HundeFinanzTV, wir bringen jeden Tag neue Videos rund ums Geld!“ anhängen,
wenn er in der Nutzer-Aufnahme fehlt (gleiche ElevenLabs-Stimme aus videos/wochen-challenge).

  python3 scripts/folge_anhaengen.py videos/<name>
Hängt Audio an assets/voice.wav, Satz 'sF' an timings.json und skript.json.
"""
import json
import subprocess
import sys
from pathlib import Path

v = Path(sys.argv[1])
q = Path(__file__).parent.parent / "videos/wochen-challenge"
qt = json.loads((q / "timings.json").read_text())
qs = next(s for s in qt["saetze"] if s["id"] == "s16")
a, b = qs["start"], qt["dauer"]

T = json.loads((v / "timings.json").read_text())
base = round(T["saetze"][-1]["end"] + 0.15, 3)
tmp = v / "assets/voice-neu.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v / "assets/voice.wav"), "-i", str(q / "assets/voice.wav"), "-filter_complex",
                f"[0:a]atrim=0:{base},apad=whole_dur={base}[x];[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[y];[x][y]concat=n=2:v=0:a=1[o]",
                "-map", "[o]", str(tmp)], check=True)
tmp.replace(v / "assets/voice.wav")
off = base - a
T["saetze"][-1]["end"] = base
T["saetze"].append({"id": "sF", "start": base, "end": round(qs["end"] + off, 3),
                    "captions": [{"text": c["text"], "start": round(c["start"] + off, 3), "end": round(c["end"] + off, 3)} for c in qs["captions"]]})
T["dauer"] = round(base + (b - a), 3)
(v / "timings.json").write_text(json.dumps(T, ensure_ascii=False, indent=1))
sk = json.loads((v / "skript.json").read_text())
if sk["saetze"][-1]["id"] != "sF":
    sk["saetze"].append({"id": "sF", "text": "Folge HundeFinanzTV, wir bringen jeden Tag neue Videos rund ums Geld!",
                         "sprechtext": "Folge HundeFinanzTV, wir bringen jeden Tag neue Videos rund ums Geld!"})
    (v / "skript.json").write_text(json.dumps(sk, ensure_ascii=False, indent=1))
print(v.name, "dauer", T["dauer"])
