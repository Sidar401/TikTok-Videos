---
name: finanz-video
description: Erstellt ein fertiges TikTok-Finanzvideo (Deutsch, 1080×1920, 45–60 s) für den Kanal aus kanal.json – Skript, Voiceover mit der festen Kanalstimme (Piper, offline), animierte Szenen im Kanal-Stil (STIL.md) und MP4-Render. Nutzen, sobald der Nutzer ein Video, ein Thema oder eine Idee für den Finanzkanal nennt.
---

# Finanz-Video erstellen

Immer Deutsch. Immer per Code (HyperFrames). **Kein Higgsfield** und keine anderen kostenpflichtigen Dienste.
Vor dem Start lesen: `STIL.md` (Look), `kanal.json` (Name, Farbe, Stimme, Tempo), `/hyperframes` (Render-Vertrag).
Der Nutzer arbeitet am iPad: Antworten kurz, Ergebnisse per `SendUserFile` schicken.

## Ablauf

1. **Setup prüfen:** `ls /root/tts/*.onnx` – fehlt etwas: `bash scripts/setup.sh`.
2. **Projekt anlegen:** `scripts/new-video.sh <kurzer-name>` → `videos/<name>/`.
3. **Skript schreiben** → `videos/<name>/skript.json`:
   ```json
   { "titel": "…", "saetze": [
     { "id": "s1", "text": "du hast 100 € im Monat übrig", "sprechtext": "Du hast hundert Euro im Monat übrig.", "bild": "Geldsack mit Münzen" }
   ] }
   ```
   - 45–60 s gesprochen ≈ 110–150 Wörter, 12–20 Sätze (ein Satz = ein Bild, 2–4 s).
   - Aufbau aus `STIL.md`: Hook (0–3 s) → Frage/Problem → Beispiel mit echten Zahlen → Visualisierung → Faustregel/Meinung → kurzer CTA.
   - `text` = Untertitel (locker, kleingeschrieben wie gesprochen, Ziffern erlaubt). `sprechtext` = was die Stimme sagt: Zahlen und Zeichen ausschreiben („sechsunddreißigtausend Euro“, „sieben Prozent“), sonst liest Piper sie falsch.
   - Zahlen nachrechnen (Zinseszins etc.) und im Chat kurz nennen. Keine Anlageberatung versprechen.
4. **Voiceover:** `python3 scripts/voice.py videos/<name>` → `assets/voice.wav` + `timings.json` (Start/Ende pro Satz und pro Untertitel-Box). Stimme kommt fest aus `kanal.json`, nie wechseln, außer der Nutzer sagt es.
5. **Komposition bauen** in `videos/<name>/index.html` (Vorlage ist schon drin, Beispielszenen ersetzen):
   - Root-`data-duration` = `timings.json.dauer`.
   - Pro Satz eine `.scene clip` mit `data-start`/`data-duration` aus `timings.json` und einem SVG-Motiv nach `STIL.md` (flache Clipart-Optik, Serifen-Zahlen grün/gold, schlichte Charts). Motive selbst als Inline-SVG zeichnen; wiederverwendbare Motive aus früheren Videos kopieren.
   - Pro Untertitel-Box ein `.cap clip` aus `captions` in `timings.json`.
   - Audio: `<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="<dauer>" data-track-index="3"></audio>` im Root.
   - Animation: Pop-in, langsamer Drift, Linien zeichnen (Helfer `pop`/`drift`/`draw` aus der Vorlage).
6. **Prüfen:** `cd videos/<name> && npx hyperframes lint && npx hyperframes check`. Fehler beheben. Warnungen „nested_structure“/„track_too_dense“ und der Kontrast der Untertitel-Box sind bekannt und ok.
7. **Ansehen:** `npx hyperframes snapshot --at <Mitte jeder Szene>` und das Kontaktblatt lesen: Text im Bild, nichts abgeschnitten, Motiv passt zum Satz.
8. **Rendern:** `npx hyperframes render --quality delivery --output ../../renders/<name>.mp4`; Dauer mit `ffprobe` gegen `dauer` prüfen.
9. **Abliefern:** committen + pushen (Branch laut Session), MP4 per `SendUserFile` schicken, dazu 1–2 Zeilen: Titel, Länge, Vorschlag für Caption + 3–5 Hashtags.

## Regeln

- Text nur im Bereich y = 168–1330, außer der Untertitel-Box (Oberkante 1360, wie in den Referenzen).
- Keine CDNs (gesperrt): nur lokale Dateien in `assets/`.
- Logos/Fotos echter Firmen nur, wenn der Nutzer sie liefert; sonst neutrale Grafik.
- Neue Kanal-Entscheidungen (Farbe, Name, Stimme) in `kanal.json` bzw. `STIL.md` festhalten.
