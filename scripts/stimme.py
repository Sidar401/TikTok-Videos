#!/usr/bin/env python3
"""Stimme direkt per ElevenLabs-API erzeugen (Nutzer 8.11.: statt MP3-Upload).

  python3 scripts/stimme.py videos/<name>        → videos/<name>/assets/voice-original.mp3
  python3 scripts/stimme.py videos/<name> --stimme <voice_id>   (andere Stimme, z. B. für den Shop-Kanal)
  python3 scripts/stimme.py --stimmen                            (alle Stimmen im Konto auflisten)
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
_ap = Path(__file__).resolve().parent.parent / "brand/aussprache.json"
AUSSPRACHE = json.loads(_ap.read_text()) if _ap.exists() else None
H = {"xi-api-key": "proxy-injected", "Content-Type": "application/json"}


def stand():
    r = urllib.request.Request(f"{API}/user/subscription", headers=H)
    d = json.load(urllib.request.urlopen(r))
    return d["character_count"], d["character_limit"]


if __name__ == "__main__":
    if "--stimme" in sys.argv:
        i = sys.argv.index("--stimme"); VOICE = sys.argv[i + 1]; del sys.argv[i:i + 2]
    if sys.argv[1] == "--stimmen":
        r = urllib.request.Request(f"{API}/voices", headers=H)
        for v in json.load(urllib.request.urlopen(r))["voices"]:
            print(v["voice_id"], "|", v["name"], "|", v.get("category"))
        sys.exit()
    if sys.argv[1] == "--stand":
        v, g = stand()
        print(f"verbraucht {v} / {g} Credits, frei {g - v}")
        sys.exit()
    ordner = Path(sys.argv[1])
    saetze = json.loads((ordner / "skript.json").read_text())["saetze"]
    text = "\n".join(s["sprechtext"] for s in saetze)
    v, g = stand()
    print(f"{len(text)} Zeichen, frei vorher {g - v}")
    # In Abschnitte (≤ ~900 Zeichen) teilen – lange Texte brechen sonst mit 502 ab; mit previous_text für gleichmäßigen Klang
    teile, cur = [], []
    for satz in (s["sprechtext"] for s in saetze):
        if cur and sum(len(x) + 1 for x in cur) + len(satz) > 900:
            teile.append("\n".join(cur)); cur = []
        cur.append(satz)
    teile.append("\n".join(cur))
    ziel = ordner / "assets/voice-original.mp3"
    roh = []
    for i, teil in enumerate(teile):
        daten = {"text": teil, "model_id": MODELL}
        if AUSSPRACHE:  # Aussprache-Wörterbuch (ETF, MSCI, USA, AMD – Nutzer 12.11.)
            daten["pronunciation_dictionary_locators"] = [AUSSPRACHE]
        if i:
            daten["previous_text"] = teile[i - 1][-300:]
        if i < len(teile) - 1:
            daten["next_text"] = teile[i + 1][:300]
        r = urllib.request.Request(f"{API}/text-to-speech/{VOICE}?output_format=mp3_44100_128", data=json.dumps(daten).encode(), headers=H, method="POST")
        for versuch in range(3):
            try:
                roh.append(urllib.request.urlopen(r, timeout=300).read()); break
            except Exception as e:  # noqa: BLE001
                if versuch == 2:
                    raise
                print("Fehler, neuer Versuch:", e)
        print(f"Teil {i + 1}/{len(teile)} ok")
    if len(roh) == 1:
        ziel.write_bytes(roh[0])
    else:
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as tmp:
            liste = []
            for i, b in enumerate(roh):
                f = Path(tmp) / f"t{i}.mp3"; f.write_bytes(b); liste.append(f"file '{f}'")
            (Path(tmp) / "l.txt").write_text("\n".join(liste))
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(Path(tmp) / "l.txt"), "-c", "copy", str(ziel)], check=True)
    print("gespeichert:", ziel)
