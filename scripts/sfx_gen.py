#!/usr/bin/env python3
"""Erzeugt die HundeFinanzTv-Soundeffekte per ElevenLabs (Sound Effects API) → brand/sfx/<name>.mp3.
Aufruf: python3 scripts/sfx_gen.py [name ...]   (ohne Namen: alle fehlenden). Vorhandene Dateien werden übersprungen.
Kosten ca. 40 Credits pro Sekunde. In glow_short: SFX-Art = Dateiname (z. B. "muenzen-glas")."""
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128"
H = {"xi-api-key": "proxy-injected", "Content-Type": "application/json"}
ZIEL = Path(__file__).resolve().parent.parent / "brand" / "sfx"

# name: (prompt, sekunden)
SOUNDS = {
    "muenzen-glas": ("A handful of coins dropping into a glass jar, crisp metallic clinks, close-up, no music", 1.5),
    "muenzen-klimpern": ("Short jingle of a few coins in a hand, bright metallic, close-up, no music", 0.8),
    "kasse": ("Classic cash register cha-ching with drawer opening, clean, satisfying, no music", 1.2),
    "karte-piep": ("Contactless card payment terminal beep, single short confirmation beep, clean", 0.6),
    "handy-benachrichtigung": ("Modern smartphone notification sound, short soft two-tone chime, clean UI sound", 0.7),
    "geld-erhalten": ("Banking app money received sound, bright positive sparkle chime, short UI sound", 0.9),
    "kurve-hoch": ("Rising synth sweep tone going up in pitch, positive, clean, for a stock chart going up", 1.2),
    "kurve-runter": ("Falling synth sweep tone going down in pitch, negative, clean, for a stock chart crashing", 1.2),
    "zaehler": ("Fast digital number counter ticking up, rapid soft clicks like a slot counter, clean", 1.5),
    "level-up": ("Short triumphant success level up sound, bright ascending arpeggio, game UI, clean", 1.0),
    "bass-schlag": ("Deep cinematic bass hit impact, short boom with sub bass, trailer style, clean", 1.0),
    "whoosh-schnell": ("Very fast clean whoosh swoosh transition, short air movement, no music", 0.5),
    "whoosh-weich": ("Soft smooth airy whoosh transition, gentle, modern, no music", 0.8),
    "swipe": ("Quick smartphone swipe UI sound, short soft swish, clean", 0.5),
    "pop": ("Short satisfying bubble pop sound, clean, cartoonish, UI", 0.5),
    "klick": ("Single crisp button click, modern UI click, clean, dry", 0.5),
    "taschenrechner": ("Typing numbers on a calculator, several quick plastic button presses, close-up", 1.2),
    "geldschein": ("Banknotes rustling and being counted, crisp paper money flipping, close-up", 1.2),
    "geldbuendel": ("A thick bundle of cash landing on a wooden table, heavy thud with paper slap", 0.7),
    "tresor": ("Heavy bank vault door unlocking and opening, metallic clunk and creak, cinematic", 2.0),
    "stempel": ("Loud rubber stamp slammed hard on paper on a wooden desk, strong punchy thump, close-up", 0.8),
    "papier-reissen": ("Tearing a sheet of paper in half, quick rip, close-up", 0.8),
    "glas-bricht": ("Glass shattering crash, short dramatic break, cinematic", 1.2),
    "alarm": ("Short warning alarm beep-beep, urgent but not harsh, two quick electronic beeps", 0.9),
    "falsch": ("Wrong answer buzzer, short low buzz, game show style", 0.6),
    "richtig": ("Correct answer ding, bright short pleasant chime, game show style", 0.6),
    "spannung": ("Short tension riser building up, cinematic suspense swell ending abruptly, no melody", 2.0),
    "uhr-tickt": ("Clock ticking steadily, clear mechanical tick tock, close-up", 2.0),
    "herzschlag": ("Deep heartbeat thump thump, suspense, two beats, cinematic", 1.5),
    "tippen": ("Fast typing on a modern keyboard, short burst of keystrokes, close-up", 1.2),
    "blase-platzt": ("Bubble bursting with a loud pop, cartoon balloon explosion sound effect, punchy and loud", 1.0),
    "glitch": ("Short digital glitch stutter sound, electronic distortion burst, modern", 0.6),
}


def mach(name):
    ziel = ZIEL / f"{name}.mp3"
    if ziel.exists():
        return print("✓ schon da", name)
    prompt, sek = SOUNDS[name]
    daten = json.dumps({"text": prompt, "duration_seconds": sek, "prompt_influence": 0.5}).encode()
    for versuch in range(4):
        try:
            r = urllib.request.Request(API, data=daten, headers=H, method="POST")
            ziel.write_bytes(urllib.request.urlopen(r, timeout=180).read())
            return print("→", name, sek, "s")
        except Exception as e:  # noqa: BLE001
            print("Fehler", name, e)
            time.sleep(3 * (versuch + 1))
    raise SystemExit(f"{name} fehlgeschlagen")


if __name__ == "__main__":
    ZIEL.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[1:] or SOUNDS:
        mach(n)
