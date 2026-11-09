---
name: shop-video
description: Erstellt TikTok-Shop-Verkaufsvideos (9:16, max. 20 s, ohne Stimme) für den Kanal HundeWissenTv 2.0 aus Produkt-Screenshots – KI-Startbilder und KI-Clips von Higgsfield, Schnitt, Untertitel und Endkarte per HyperFrames. Nutzen, sobald der Nutzer ein Produkt (Screenshot, Link, Name) für den Shop-Kanal schickt oder Shop-Videos will.
---

# Shop-Video (HundeWissenTv 2.0)

Erst `shop/ANLEITUNG.md` lesen – dort steht der ganze Ablauf. Muster, das der Nutzer abgenommen hat: `shop/spielball/`.

Kurz:
1. Screenshots → Preis, Sterne, „verkauft“, Besonderheiten notieren; Produkt freistellen → `shop/<produkt>/produkt.png`.
2. Kosten mit `get_cost` prüfen und dem Nutzer kurz nennen (Bild ca. 1,5, Clip 5 s ca. 7,5 Credits).
3. Startbilder (`gpt_image_2_5`, high, 9:16) mit Produktfoto + Kanal-Hund (IDs in `shop/spielball/videos.md`) als Referenz.
4. Clips (`kling3_0`, std, 5 s, sound off, 9:16) aus den Startbildern → `shop/<produkt>/clips.txt`.
5. 4 Konfigs (POV / Demo / Problem-Geld / 3 Gründe) → `python3 scripts/shop_video.py shop/<produkt>/<x>.json`.
6. `scripts/hole_clips.sh shop/<produkt>`, prüfen (`npx hyperframes lint`, Snapshot ansehen), rendern nach `renders/<name>.mp4`, committen.
   Erreicht die Sitzung Higgsfield nicht: Schritt 6 per `sandbox_exec` in der Higgsfield-Sandbox (Repo ist öffentlich klonbar)
   und MP4 per `media_upload` hochladen; Links dem Nutzer geben.

Regeln: Deutsch, sehr kurze Antworten fürs iPad. Erster Untertitel steht ab Frame 0. Text nie über Hundegesichtern.
Beim Posten erinnern: Schalter „KI-generiert“ an, Trend-Sound drunter, Preis prüfen.

## Stimme (vorbereitet 9.11., ab ca. 19.11. geplant)
- ElevenLabs ist über die Umgebung „Standard“ freigeschaltet (Schlüssel setzt der Proxy ein, nie selbst eintragen).
- Sprechtext pro Video in `skript.json` (`saetze[].sprechtext`, max. ~20 s ≈ 50 Wörter), dann `python3 scripts/stimme.py <ordner>` → `assets/voice-original.mp3`, danach `python3 scripts/sync.py <ordner> <ordner>/assets/voice-original.mp3 --tempo 1.12` für Untertitel-Zeiten.
- Shop-Stimme = **„HundeTV“** (gleiche Stimme wie HundeFinanzTv, Nutzer 9.11.) – Standard in `stimme.py`, kein `--stimme` nötig. Credits geteilt mit HundeFinanzTv, Novaro, HundeWissenTv – Stand mit `--stand` prüfen.
