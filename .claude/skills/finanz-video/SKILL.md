---
name: finanz-video
description: Erstellt ein fertiges TikTok-Finanzvideo (Deutsch, 1080×1920, 30–60 s) für den Kanal aus kanal.json – Skript, Voiceover vom Nutzer (ElevenLabs) automatisch synchronisiert, animierte Szenen im Kanal-Stil (STIL.md) und MP4-Render. Nutzen, sobald der Nutzer ein Video, ein Thema oder eine Idee für den Finanzkanal nennt.
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
   - **40–50 s** (Nutzerwunsch: mind. 10 s länger als früher) ≈ 115–135 Wörter, 12–14 Sätze (ein Satz = ein Bild, 2–4 s).
   - Aufbau aus `STIL.md`: Hook (0–3 s) → Frage/Problem → Beispiel mit echten Zahlen → Visualisierung → Faustregel/Meinung → kurzer CTA.
   - **Zusatz-CTAs abwechselnd:** Video A → Kommentar-CTA („Schreib uns in die Kommentare …“), Video B → Teilen-CTA („Teile das Video mit jemandem, der …“), dann wieder A. Nie beide in einem Video. Im Chat beim Skript angeben, welcher CTA drin ist.
   - **CTA immer in Wir-Form**, nie „folg mir“: z. B. „Folge HundeFinanzTV, wir haben noch mehr Geld-Tipps für dich!“ (Outro-Button bleibt „+ Folgen“).
   - Skript: Zahlen im `sprechtext` ausschreiben (für ElevenLabs); den Untertitel-`text` mit `python3 scripts/zahlen.py videos/<name>/skript.json` erzeugen (Zahlwörter → Ziffern, „dreihundert Euro“ → „300 €“).
   - **Wir machen jeden Tag Videos** – im Skript nie „jede Woche“ sagen, sondern z. B. „wir bringen jeden Tag neue Videos“.
   - `text` = Untertitel (locker, kleingeschrieben wie gesprochen, Ziffern erlaubt). `sprechtext` = was die Stimme sagt: Zahlen und Zeichen ausschreiben („sechsunddreißigtausend Euro“, „sieben Prozent“), sonst liest Piper sie falsch.
   - Zahlen nachrechnen (Zinseszins etc.) und im Chat kurz nennen. Keine Anlageberatung versprechen.
4. **Voiceover (Standard: ElevenLabs vom Nutzer):**
   - Dem Nutzer das Skript zum Einsprechen schicken: nur die `sprechtext`-Sätze, **ein Satz pro Zeile**, in einem Codeblock (iPad: leicht zu kopieren). Hinweis: gleiche ElevenLabs-Stimme wie immer, Satzzeichen stehen lassen. Dann warten.
   - Lange Aufnahmen (Longform, > 5 Min.): DTW-Kosten um 0,70 sind normal (gröbere Auflösung). Dann mit `python3 scripts/stichprobe.py videos/<name>/ 5 20 50 80 110` prüfen – alle „OK“ = richtig.
   - **Mehrere Uploads auf einmal: nie nach Reihenfolge/Zeitstempel zuordnen**, sondern mit `python3 scripts/dtw_align.py <mp3> videos/<name>/skript.json` gegen jedes Skript prüfen (niedrigste Kosten = richtiges Skript; passend ≈ 0,55–0,60, falsch ≈ 0,70).
   - Lädt der Nutzer die Datei hoch: `python3 scripts/sync.py videos/<name> <upload.mp3>` (warnt bei DTW-Kosten > 0,65) → `assets/voice.wav` + `timings.json`. Standard: Pausen auf 0,25 s kürzen + Tempo 1,08 (Tonhöhe bleibt; 1,15 war dem Nutzer zu schnell); anpassbar mit `--tempo`/`--pause`. Satzgrenzen werden im Original erkannt und umgerechnet. Meldet es „Fallback“, Satzanzahl und Pausen prüfen und dem Nutzer sagen.
   - Nur wenn der Nutzer es ausdrücklich will: Computerstimme `python3 scripts/voice.py videos/<name>` (Piper, `stimme_fallback` aus `kanal.json`).
5. **Komposition bauen:** `build.py` aus dem letzten Video (Muster: `videos/100-euro-im-monat/build.py`) nach `videos/<name>/` kopieren, `SCENES` anpassen, `python3 build.py` → `index.html` (Kopf/CSS kommt aus der Vorlage). Es setzt automatisch:
   - Root-`data-duration` = `timings.json.dauer`.
   - Pro Satz eine `.scene clip` mit `data-start`/`data-duration` aus `timings.json` und einem SVG-Motiv nach `STIL.md` (flache Clipart-Optik, Serifen-Zahlen grün/gold, schlichte Charts). Motive selbst als Inline-SVG zeichnen; wiederverwendbare Motive aus früheren Videos kopieren.
   - Pro Untertitel-Box ein `.cap clip` aus `captions` in `timings.json`.
   - Marken-Badge oben (nur Name „HundeFinanzTV“), oranger Rahmen. **Kein Logo im Video**; Einstieg = Thema groß als Text + passende Szene (Logo-Regel in `STIL.md`). Maskottchen = Beagle (`assets/beagle.png`), sparsam (Tipp-Szene, Outro); der Aussie gehört nur zu HundeWissenTv.
   - Audio: `<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="<dauer>" data-track-index="3"></audio>` im Root.
   - Animation: Pop-in, langsamer Drift, Linien zeichnen (Helfer `pop`/`drift`/`draw` aus der Vorlage).
6. **Prüfen:** `cd videos/<name> && npx hyperframes lint && npx hyperframes check`. Fehler beheben. Warnungen „nested_structure“/„track_too_dense“ und der Kontrast der Untertitel-Box sind bekannt und ok.
7. **Ansehen:** `npx hyperframes snapshot --at <Mitte jeder Szene>` und das Kontaktblatt lesen: Text im Bild, nichts abgeschnitten, Motiv passt zum Satz.
8. **Rendern:** `npx hyperframes render --quality delivery --output ../../renders/<name>.mp4`; Dauer mit `ffprobe` gegen `dauer` prüfen.
9. **Abliefern:** committen + pushen (Branch laut Session), MP4 per `SendUserFile` schicken, dazu 1–2 Zeilen: Titel, Länge, Vorschlag für Caption + 3–5 Hashtags.

## Regeln

- **Erste 3 Sekunden:** Frame 0 ist nie leer, Thema/Hook und Hauptmotiv sind sofort sichtbar (nur leichtes Scale-Einrasten, kein Einblenden aus Opacity 0).

- Text nur im Bereich y = 168–1330, außer der Untertitel-Box (Oberkante 1360, wie in den Referenzen).
- Keine CDNs (gesperrt): nur lokale Dateien in `assets/`.
- Logos/Fotos echter Firmen nur, wenn der Nutzer sie liefert; sonst neutrale Grafik.
- Neue Kanal-Entscheidungen (Farbe, Name, Stimme) in `kanal.json` bzw. `STIL.md` festhalten.
