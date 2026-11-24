#!/usr/bin/env python3
"""Stimme direkt bei ElevenLabs erzeugen (Shop-Kanal, gleiche Stimme wie Novaro).

Aufruf: python3 scripts/shop_stimme.py videos/<name> sprechtext.txt
  - sprechtext.txt: ein Satz pro Zeile, Zahlen ausgeschrieben
  - schreibt: assets/voice-orig.mp3 + alignment.json (Zeichen-Zeiten von ElevenLabs)
Der API-Schlüssel wird vom Netzwerk-Proxy eingesetzt (Umgebung „Standard“), nie im Code.
"""
import base64, json, sys, urllib.request
from pathlib import Path

VOICE = "BHr135B5EUBtaWheVj8S"  # Dan - Engaging Science Instructor
MODEL = "eleven_v4"

proj, txt = Path(sys.argv[1]), Path(sys.argv[2])
text = "\n".join(l.strip() for l in txt.read_text().splitlines() if l.strip())
body = json.dumps({"text": text, "model_id": MODEL, "output_format": "mp3_44100_192"}).encode()
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
    data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
d = json.load(urllib.request.urlopen(req, timeout=180))
(proj / "assets").mkdir(parents=True, exist_ok=True)
(proj / "assets" / "voice-orig.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
json.dump({"text": text, "alignment": d.get("alignment")}, open(proj / "alignment.json", "w"), ensure_ascii=False)
print("Stimme ok:", len(text), "Zeichen")

# Kontrolle: Aufnahme zurück in Text und mit dem Skript vergleichen
import difflib, re, uuid
def norm(s): return re.sub(r"[^a-zäöüß0-9 ]", " ", s.lower()).split()
bnd = uuid.uuid4().hex; mp3 = (proj / "assets" / "voice-orig.mp3").read_bytes()
body = (f"--{bnd}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n--{bnd}\r\nContent-Disposition: form-data; name=\"language_code\"\r\n\r\ndeu\r\n"
        f"--{bnd}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"v.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + mp3 + f"\r\n--{bnd}--\r\n".encode()
req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body, headers={"Content-Type": f"multipart/form-data; boundary={bnd}", "xi-api-key": "proxy-injected"})
heard = json.load(urllib.request.urlopen(req, timeout=180))["text"]
a, b = norm(text), norm(heard)
diff = [(op, " ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes() if op != "equal"]
json.dump({"gehoert": heard, "abweichungen": diff}, open(proj / "kontrolle.json", "w"), ensure_ascii=False, indent=1)
print("Gehört:", heard)
print("Abweichungen:", diff if diff else "keine")

# Nutzer 24.11.: erster Satz LAUTER (ca. +5 dB, wie bei Novaro „Stern frisst Stern“), danach normal.
# Ergebnis: assets/voice.wav (fertig für das Video). Erster Satz im Sprechtext immer mit „!“.
import subprocess  # noqa: E402
al = d.get("alignment") or {}
chars, ends = al.get("characters") or [], al.get("character_end_times_seconds") or []
first_len = len(text.split("\n")[0])
hook = (ends[min(first_len, len(ends)) - 1] + 0.05) if ends else 0
src, dst = proj / "assets" / "voice-orig.mp3", proj / "assets" / "voice.wav"
af = f"volume=1.75:enable='lt(t,{hook:.3f})',alimiter=limit=0.95" if hook else "anull"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "44100", "-ac", "1", str(dst)], check=True)
print(f"Erster Satz lauter bis {hook:.2f} s → {dst}")
