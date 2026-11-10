# Regeln für den Wissens-Kanal (vom Nutzer, 01.11.2026) – IMMER einhalten
1. **Riesige Hook am Anfang (0–2,5 s):** Die Frage/Hook steht GROSS mitten im Bild (ca. 110–130 px, 2–3 Zeilen, Glow),
   nicht nur als kleine Titelzeile. Der normale Titel oben ist in dieser Zeit ausgeblendet.
2. **Call to Action zum Folgen:** In jedem Video am Ende ein großer „Folg uns für mehr!“-Hinweis mit Folgen-Knopf
   (rote Pille „+ Folgen“). Zusätzlich gern die Kommentar-Frage.
3. 30 Sekunden, Hochformat 1080×1920, keine Hintergrund-Musik (nur Effekte), Deutsch.
4. Fakten vorher prüfen; Annahmen im Video nennen.
Vorlage/Baukasten: `wissen/kit/` (neu.sh, kit.js, kit.css, mix.py, fertig.sh, snap.sh).
5. Vom Nutzer freigegeben (01.11.2026): Look der Probebilder in `wissen/probe/` (Hook 150 px + dunkle Fläche, Folgen-Kasten mit roter Pille). Text immer „Folg uns für mehr! 👆“.

## Ablauf ab 08.11.2026 (Kanal heißt jetzt **Novaro**)
- Stil: **3D-Kino** (three.js, echte Erde aus NASA-Texturen, große Wort-für-Wort-Untertitel mit gelbem Wort, Fortschrittsbalken oben). Vorlagen: `videos/mond-weg/`, `videos/erde-stopp/`.
- Ablauf: 3–4 Themen vorschlagen → Nutzer wählt → Sprechtext (Zahlen ausgeschrieben) → Nutzer sagt „passt“ → **Stimme selbst erzeugen** mit `python3 wissen/kit/stimme.py videos/<name> sprechtext.txt` (ElevenLabs, Stimme „Dan – Engaging Science Instructor“, Modell eleven_v4; Schlüssel liegt sicher in der Umgebung) → Pausen kürzen, auf 30 s bringen → Video bauen → rendern → schicken.
- API-Schlüssel hat ein Limit von 20.000 Credits/Monat (ca. 35–40 Videos). Vor dem Limit dem Nutzer Bescheid sagen.
- **Ton (Nutzer-Feedback 09.11.):** Effekte waren lauter als die Stimme („Zischen“). Ab jetzt: wenige kurze Effekte, kein Riser/Glitzern/Glitch während der Stimme, `data-volume` 0.3 und nach `mix.py` immer `python3 -I wissen/kit/duck.py videos/<name>` (Effekte beim Sprechen auf 25 %).
- Nach dem ersten Satz ein Teilen-Aufruf („Teile das Video mit jemandem, der das nicht weiß!“) + rote „Teilen ➜“-Pille rechts (Nutzer-Wunsch 09.11.).
- **Oben im Bild (Zeile über dem Fortschrittsbalken) immer das aktuelle Datum**, z. B. „9. NOVEMBER 2026“ – kein „NEU“, kein „WAS WÄRE, WENN …“ (Nutzer-Wunsch 09.11.).
- **Zu jedem Video ein Thumbnail** (Nutzer-Wunsch 09.11.): `node wissen/kit/thumb.js videos/<name> <sekunde> 'Titel mit <y>Schlagwort</y>'` → `renders/<name>-thumbnail.png` (1080×1920, sauberes 3D-Bild ohne Untertitel, großer Titel, NOVARO unten). Zu langer Titel: `SIZE=128` davor.
- **Stimm-Kontrolle:** `stimme.py` wandelt die Aufnahme automatisch zurück in Text (ElevenLabs Sprache-zu-Text) und schreibt Abweichungen in `kontrolle.json`. Bei Abweichungen neu aufnehmen. Stimme/Einstellungen NICHT ändern (Nutzer-Wunsch).
- **Schnitt-Regel (Fehler vom 09.11., Nutzer: „ab sofort immer darauf achten“):** Stimme nur in echter Stille schneiden (`schnitt.py` macht das automatisch). Wenn die ElevenLabs-Aufnahme schon ≤ 30 s ist, **gar nicht schneiden**. Nach dem Schnitt die geschnittene `voice.wav` noch einmal per Sprache-zu-Text prüfen und die Übergänge zwischen den Sätzen kontrollieren (keine doppelten Wortstücke).
- **Neuer Kino-Look (ab 10.11.):** Baukasten `wissen/kit/kino.js` (Bloom, Farbstimmung, Körnung, Stadt, Wasser, Mond, Erde mit Wolken/Eis/Überflutung) + Vorlage `kino_vorlage.html`. Pro Video nur `szene.json` + `szene.js` schreiben und `python3 wissen/kit/kino_bau.py videos/<name>` ausführen. Beispiele: `videos/supermond/`, `videos/eis-schmilzt/`. Mischung aus Szenen vom Boden (Stadt, Wasser, Mensch) und aus dem All; starker Start in der 1. Sekunde.
- **Kino-Look macht riesige Dateien** (Filmkörnung): nach dem Rendern immer verkleinern: `ffmpeg -i roh.mp4 -vf hqdn3d=3:3:10:10 -c:v libx264 -preset slow -b:v 9M -maxrate 12M -bufsize 18M -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k renders/<name>.mp4` (≈ 35 MB).
