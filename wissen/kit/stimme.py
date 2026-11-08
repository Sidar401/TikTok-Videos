#!/usr/bin/env python3
"""Stimme direkt bei ElevenLabs erzeugen (Kanal Novaro).

Aufruf: python3 wissen/kit/stimme.py videos/<name> sprechtext.txt
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
