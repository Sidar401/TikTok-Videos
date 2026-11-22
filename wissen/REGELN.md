# Regeln für den Wissens-Kanal (vom Nutzer, 01.11.2026) – IMMER einhalten
1. **Riesige Hook am Anfang (0–2,5 s):** Die Frage/Hook steht GROSS mitten im Bild (ca. 110–130 px, 2–3 Zeilen, Glow),
   nicht nur als kleine Titelzeile. Der normale Titel oben ist in dieser Zeit ausgeblendet.
2. **Call to Action zum Folgen:** ⚠️ NEU ab 17.11. → siehe „Folgen-Aufruf NEU“ unten (nach dem 3. Satz, nur „Folg uns“,
   KEINE Kommentar-Frage, cta-pro-3-Karte).
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
- **Zu jedem Video ein Thumbnail** (Nutzer-Wunsch 09.11.): `node wissen/kit/thumb.js videos/<name> <sekunde> 'Titel mit <y>Schlagwort</y>'` → `renders/<name>-thumbnail.png` (1080×1920, sauberes 3D-Bild ohne Untertitel, großer Titel – **ohne „NOVARO“**, Nutzer-Wunsch 14.11.). Zu langer Titel: `SIZE=128` davor.
- **Stimm-Kontrolle:** `stimme.py` wandelt die Aufnahme automatisch zurück in Text (ElevenLabs Sprache-zu-Text) und schreibt Abweichungen in `kontrolle.json`. Bei Abweichungen neu aufnehmen. Stimme/Einstellungen NICHT ändern (Nutzer-Wunsch).
- **Schnitt-Regel (Fehler vom 09.11., Nutzer: „ab sofort immer darauf achten“):** Stimme nur in echter Stille schneiden (`schnitt.py` macht das automatisch). Wenn die ElevenLabs-Aufnahme schon ≤ 30 s ist, **gar nicht schneiden**. Nach dem Schnitt die geschnittene `voice.wav` noch einmal per Sprache-zu-Text prüfen und die Übergänge zwischen den Sätzen kontrollieren (keine doppelten Wortstücke).
- **Neuer Kino-Look (ab 10.11.):** Baukasten `wissen/kit/kino.js` (Bloom, Farbstimmung, Körnung, Stadt, Wasser, Mond, Erde mit Wolken/Eis/Überflutung) + Vorlage `kino_vorlage.html`. Pro Video nur `szene.json` + `szene.js` schreiben und `python3 wissen/kit/kino_bau.py videos/<name>` ausführen. Beispiele: `videos/supermond/`, `videos/eis-schmilzt/`. Mischung aus Szenen vom Boden (Stadt, Wasser, Mensch) und aus dem All; starker Start in der 1. Sekunde.
- **Kino-Look macht riesige Dateien** (Filmkörnung): nach dem Rendern immer verkleinern: `ffmpeg -i roh.mp4 -vf hqdn3d=3:3:10:10 -c:v libx264 -preset slow -b:v 9M -maxrate 12M -bufsize 18M -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k renders/<name>.mp4` (≈ 35 MB bei 30 s). Bei Videos über 45 s `-b:v 6M -maxrate 8M` nehmen, damit die Datei unter 50 MB bleibt (GitHub-Grenze 100 MB).
- **Eigene Soundeffekte (ab 10.11.):** `wissen/kit/sounds/` – 32 Sounds (Liste mit Beschreibung: `liste.json`; dazu u. a. `alarm`, `countdown`, `gong`, `laser`, `raumschiff`, `rakete`, `explosion-fern`, `donner`, `wasser-platsch`, `eis-knacken`, `sturm`, `erdbeben`, `kamera-klick`, `tippen`, `sog`, `publikum-lachen`), mit ElevenLabs erzeugt (Rechte beim Nutzer, keine Sperren). Namen direkt in `cues.json` verwenden (z. B. `boom-tief`, `platte-kratzer`, `dun-dun-dun`, `film-horn`, `herzschlag`, `whoosh-schnell`, `whoosh-tief`, `ding`, `pling-idee`, `falsch-buzzer`, `tusch`, `spannung`, `pop-blase`, `kasse`, `staunen-wow`, `boom-kurz`). Keine fremden/berühmten Original-Sounds einbauen (Rechte!). Trend-Sounds legt der Nutzer selbst in TikTok leise drunter.
- **Ab 11.11.: Videos 60–70 s** (YouTube Shorts bis 3 Min. möglich, TikTok Creator-Programm ab 1 Min.).
- **⭐ Immer echte Original-Logos** (Nutzer-Wunsch 12.11., wie HundeFinanzTV): Jede genannte Firma/Behörde/Organisation (NASA, SpaceX, ESA, FAA, Rubin, …) bekommt ihr Original-Logo als weiße Logo-Karte. Logos liegen in `wissen/kit/logos/` (Quelle: Wikimedia Commons `Special:FilePath/<Datei>`, in `quellen.json` eintragen). Nur wenn es auf Commons nicht existiert: Wortmarke nachbauen und dem Nutzer sagen. Logos nur redaktionell zeigen (nie so, als wären die Firmen Partner).
- **⭐ Immer so gut wie möglich produzieren** (Nutzer 12.11.): Wo es erlaubt ist, echte Originale einbauen (Original-Logos, gemeinfreie NASA/ESA-Bilder, echte Daten/Grafiken mit Quelle). Wenn etwas fehlt, später nachholen und ggf. neu rendern.

## ⭐ Neuer Ziel-Look ab 14.11.2026 (Nutzer-Vorbild: YouTube-Short @erklärwürdig „Reihenfolge der Planeten nach Größe“)
- Nutzer: „Siehst du, wie gut diese Bilder aussehen?“ → so sollen die nächsten Videos aussehen. Alte Videos NICHT neu machen.
- **Fotorealistische Himmelskörper:** Kugeln immer mit echten Karten/Texturen (NASA, gemeinfrei/freie Lizenz, Quelle notieren) – keine selbst gebastelten Geräte/Formen mehr.
- **Sauberer schwarzer Hintergrund**, Objekte groß und mittig, viel freier Raum, ruhige, weiche Kamerafahrten.
- **Ganz wenig Text:** ein großes, klares Wort / Name in weißer, schlichter Schrift (z. B. „Mars“, „Planet“). Keine Zettel, Stempel, Karopapier-Karten, Handschrift-Pfeile mehr (Analyse-Ebene nur noch sparsam: eine Zahl oder ein Wort).
- Edle Effekte erlaubt: glühende Sonne, leuchtendes Raumzeit-Gitter, Ringe, Umlaufbahnen.
- Thumbnails ohne „NOVARO“.

## ✅ FREIGEGEBEN (Nutzer 14.11.2026): „Genau das will ich – ab sofort IMMER so“
- Muster: `videos/demo-groesse/` (Größenvergleich) und `videos/demo-raumzeit/` (Sonne im Raumzeit-Gitter), Renders in `renders/demo-*.mp4`.
- Bauen mit `wissen/kit/sauber_vorlage.html` + `python3 wissen/kit/sauber_bau.py videos/<name>` (Hilfen im Szenen-Code: `tex("mars.jpg")`, `label(name, obj, radius, {t0,t1,size})`, `word(html, sichtbarkeit)`).
- Echte Planeten-Texturen in `assets/tex/` (Solar System Scope, CC BY 4.0 → in JEDE Beschreibung: „Planeten-Texturen: Solar System Scope (CC BY 4.0)“), Erde über `K.earth` (Leuchtrand mit `scale 0.93` dünner).
- Schwarzer Hintergrund, große echte Kugeln, weiße schlichte Namen über den Objekten, unten höchstens ein großes Wort/eine Zahl. Bloom niedrig halten (Planeten nicht überstrahlen), Füll-Licht, damit keine schwarzen Scheiben entstehen.
- Für lange Videos mit Stimme: diesen Look mit Untertiteln/Stimme kombinieren (Vorlage noch erweitern).

## Longform rendern (gelernt 15.11.)
- Formate nacheinander rendern (je ein Hintergrund-Job, < 2 h), nie parallel.
- Vorher alte `*-roh.mp4` im Scratchpad löschen (Roh-Datei ~4 GB, sonst Speicher voll).
- Thumbnail 16:9: `VW=1920 VH=1080 TOP=730 SIZE=125 HIDE=".tag,.capw" node wissen/kit/thumb.js ...`

## Thumbnails: sichtbarer Bereich (Nutzer, 16.11.) – AB SOFORT IMMER
- Instagram/TikTok-Raster zeigt nur die Mitte (3:4): y = 240 … 1680 von 1920.
- Titel komplett zwischen **y ≈ 400 und 1500** – nicht zu hoch, nicht zu tief.
- Standard in thumb.js jetzt TOP=420. Titel unten nur, wenn er vor 1500 endet.
- Vor dem Abschicken prüfen: 3:4-Ausschnitt ansehen, Text darf nicht angeschnitten oder an den Rand gedrückt sein.

## Folgen-Aufruf NEU (Nutzer, 17.11.) – AB SOFORT
- Der alte rote „+ Folgen“-Pill und die alte Folg-Box werden NICHT mehr benutzt (Farbe rot gefällt nicht).
- Stattdessen ein Profil-Button wie bei Creatorn: Profilbild (wissen/kit/avatar.png), Novaro, @novaro040, Folgen-Button, Finger tippt → „Gefolgt ✓“.
- 3 Muster: videos/cta-demo-1 (Karte), cta-demo-2 (Profilbild mit Plus), cta-demo-3 (Leiste unten). Baukasten: wissen/kit/cta_demos.py.
- Nutzer (17.11.): Variante 1 (Karte) gewählt, OHNE @novaro040, professioneller. Neue Proben: videos/cta-pro-1..3 (wissen/kit/cta_pro.py) – Tipp-Punkt statt Emoji-Finger, Haken wird gezeichnet, Lichtschimmer. 
- ✅ ENTSCHIEDEN (17.11.): **cta-pro-3 IMMER** (Profilbild ragt oben aus der Karte, Novaro + „Weltraum, einfach erklärt“, weißer Folgen-Knopf → goldenes „✓ Gefolgt“). Ersetzt den alten roten Pill UND die alte Folg-Box am Ende.
- ✅ ENTSCHIEDEN (17.11., Nutzer: „ab sofort immer bei jedem“): **Aufruf NACH DEM DRITTEN SATZ**, nicht am Ende.
  Im Sprechtext NUR „Folg uns für mehr!“ (o. ä.) – **KEINE Kommentar-Frage** („Schreib's in die Kommentare“, „Was denkst du?“) – erstmal nicht.
  Karte (szene.json "karte": [start, dauer]) genau dann einblenden, wenn „Folg uns“ gesprochen wird. Am Ende kein Aufruf mehr.

## KEIN Intro (Nutzer 19.11. abends: „schrecklich“, ab sofort rauslassen)
- Das Intro „Umlaufbahn“ (`wissen/kit/intro.py`) NICHT mehr verwenden. Kein `"intro"` in szene.json, keine Pause in der Stimme.
- Ton (Nutzer 19.11.): Soundeffekte haben die Stimme übertönt → ab jetzt nur 2–3 Effekte pro Video, sehr leise (0.1), NUR in Sprechpausen, nie über der Stimme.
- Bilder (Nutzer 19.11.): selbstgebaute 3D-Raketen/Roboter sahen „billig“ aus. KEINE echten Fotos verwenden (Nutzer: „du sollst keine echten Bilder nehmen“). Stattdessen detaillierte 3D-Modelle aus `wissen/kit/modelle.js` (in szene.js Zeile `// @modelle`: MO.vulcan, MO.ariane6, MO.falcon9, MO.exhaust, MO.smoke, MO.mliM, MO.cellM).

## Longform-Titelbilder (Nutzer 20.11.): nicht wie das alte aussehen
- Jedes Titelbild muss sich klar von den bisherigen unterscheiden (nicht wieder „Kugeln in einer Reihe + Titel“).
- Muss zum Inhalt passen. „Findest du die SONNE?“ mit Kreis + „hier!“-Knopf fand der Nutzer SCHRECKLICH. Gut: Sterne-Treppe klein → riesig mit Namen, Titel „Vom kleinsten zum GRÖSSTEN Stern“. Code: `videos/sterne-groesse/thumb-szene.js` (eigene Szene bei t < 1).

## Longform (Nutzer 20.11.)
- Lange Videos (16:9 und 9:16) KOMPLETT OHNE Untertitel: in szene.json `.capw, #cap-in { display: none !important; }` (bei 16:9 in `css_land`).
- Auch im Longform NUR die neue Folgen-Karte (`"karte": [start, dauer]`), NIE mehr `share`/`follow` (roter Knopf). 16:9: Karte per css_land mittig setzen (siehe `videos/sterne-groesse/szene.json`).

## Folgen-Aufruf NICHT aussprechen (Nutzer 21.11.) – AB SOFORT
- „Folg uns für mehr!“ NICHT mehr in sprechtext.txt. Die Folgen-Karte (`"karte"`) kommt stumm nach dem 3. Satz.
- Jedes Mal, wenn die Karte erscheint: Soundeffekt `stern-funkeln` (in cues.json, Zeit = Karten-Start, v ≈ 0.12).

## Nutzer 22.11. – AB SOFORT
- **KEINE Untertitel** mehr (sauber_bau.py blendet `.capw` immer aus).
- **Einblendungen (word/seg) nur ab und zu** – nicht jeden gesprochenen Satz nochmal hinschreiben. Max. ca. 4–5 starke Zahlen/Fakten pro Video.
- **Folgen-Karte kleiner und tiefer** (karte.py: `#fk-box` scale .68, nach unten verschoben), nicht mitten über dem Bild.
