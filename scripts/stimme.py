#!/usr/bin/env python3
"""Stimme direkt per ElevenLabs-API erzeugen (Nutzer 8.11.: statt MP3-Upload).

  python3 scripts/stimme.py videos/<name>        → videos/<name>/assets/voice-original.mp3
  danach wie immer: python3 scripts/sync.py videos/<name> videos/<name>/assets/voice-original.mp3 --tempo 1.12

Stimme „HundeTV“, Modell eleven_v4. Der Schlüssel wird vom Proxy eingesetzt (Header-Wert ist nur ein Platzhalter).
Kosten ≈ 1 Credit pro Zeichen – vorher Kontostand zeigen (`--stand`), Limit 100.000 geteilt mit Kanal Novaro.
"""
import json
import sys
import urllib.request
from pathlib import Path

VOICE = "BwioUoriWcYELLG6prCr"  # HundeTV
MODELL = "eleven_v4"
API = "https://api.elevenlabs.io/v1"
H = {"xi-api-key": "proxy-injected", "Content-Type": "application/json"}


def stand():
    r = urllib.request.Request(f"{API}/user/subscription", headers=H)
    d = json.load(urllib.request.urlopen(r))
    return d["character_count"], d["character_limit"]


if __name__ == "__main__":
    if sys.argv[1] == "--stand":
        v, g = stand()
        print(f"verbraucht {v} / {g} Credits, frei {g - v}")
        sys.exit()
    ordner = Path(sys.argv[1])
    saetze = json.loads((ordner / "skript.json").read_text())["saetze"]
    text = "\n".join(s["sprechtext"] for s in saetze)
    v, g = stand()
    print(f"{len(text)} Zeichen, frei vorher {g - v}")
    body = json.dumps({"text": text, "model_id": MODELL}).encode()
    r = urllib.request.Request(f"{API}/text-to-speech/{VOICE}?output_format=mp3_44100_128", data=body, headers=H, method="POST")
    ziel = ordner / "assets/voice-original.mp3"
    ziel.write_bytes(urllib.request.urlopen(r, timeout=300).read())
    print("gespeichert:", ziel)
