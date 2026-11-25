# TikTok-Videos

Videos werden mit HyperFrames (HTML + GSAP → MP4) gebaut. Skills: `.claude/skills/hyperframes*`.

- Setup (läuft automatisch per SessionStart-Hook): `scripts/setup.sh`
- Neues Video: `scripts/new-video.sh <name>` → kopiert `vorlage/` nach `videos/<name>/`
- **Videos immer mit dem Skill `/finanz-video` bauen** (Kanal-Daten: `kanal.json`)
- **Stil-Regeln: `STIL.md` immer einhalten**
- Prüfen: `cd videos/<name> && npx hyperframes lint && npx hyperframes check --json`
- Rendern: `npx hyperframes render --quality delivery --output ../../renders/<name>.mp4`
- CDNs (jsdelivr, unpkg) sind gesperrt: Libraries lokal einbinden (GSAP liegt in `node_modules/gsap`).
- Fertige MP4s in `renders/` committen, damit sie auf dem iPad abrufbar sind.

## Kanäle des Nutzers (TikTok)
1. **HundeWissenTv** (@hundewissentv): Hunde-Wissen als Slideshow-Bilder (macht der Nutzer selbst).
2. **HundeWissenTv 2.0**: ab Nov. 2026 **reiner TikTok-Shop-Kanal** (nur Hundesachen) → Skill `/shop-video`.
3. **HundeFinanzTV**: Geld & Finanzen (faceless, animierte Grafiken) → Skill `/finanz-video`, `kanal.json`, `STIL.md`.

## Kanal 3: HundeFinanzTV
- Nische: **Geld & Finanzen** (faceless, animierte Grafiken, Zahlen, Diagramme)
- Ziele: maximale Reichweite, Sympathie, später Monetarisierung
- Finanzvideos per Code (HyperFrames), **ohne Higgsfield**.

## Kanal 2: HundeWissenTv 2.0 (TikTok Shop)
- Videos **immer mit dem Skill `/shop-video`** bauen. Anleitung: `shop/ANLEITUNG.md`, Vorlage: `scripts/shop_video.py`.
- Immer **9:16**, **max. 20 s**, vorerst **ohne Stimme** (Trend-Sound legt der Nutzer in TikTok drunter).
- Name „HundeWissenTv 2.0“ und Beagle-Logo bleiben. Nur Hundeprodukte.
- **Higgsfield ist hier erlaubt:** Bilder (`gpt_image_2_5`) und kurze Clips (`kling3_0`, 5 s). Vor größeren
  Ausgaben Kosten mit `get_cost` prüfen und dem Nutzer nennen. Schnitt/Text/Endkarte immer per HyperFrames.
- Ziel: ab ca. Mitte Nov. 2026 **ca. 5 Videos pro Tag**.
- Freigegebenes Muster (Nutzer: „super“, 31.10.): `shop/spielball/` – 4 Videos, Links in `shop/spielball/videos.md`.

## Regeln vom Nutzer
- **Arbeitsweise (Nutzer 22.11., Limit-Ärger):** Nutzer nie dasselbe zweimal sagen lassen. Erst Regeln in CLAUDE.md/Skill lesen und anwenden. Bei unklarem Wunsch EINE kurze Frage stellen, statt etwas Falsches zu bauen. Nicht entschuldigen, sondern fixen und Regel speichern. Nichts bauen, was nicht gewünscht ist.
- **Referenz-Link vom Nutzer (22.11.):** Video laden, Text/Aufbau auswerten, das GLEICHE Thema im eigenen Look mit eigenen Worten und geprüften Zahlen bauen (nicht anderes Thema vorschlagen). Länge darf 2–3 Min. sein, wenn der Nutzer es sagt.
- **Erster Satz (Nutzer 24.11., Vorbild Novaro „Stern frisst Stern“):** spannender, packender Hook (ein Lebewesen/Akteur TUT etwas: fressen, verlieren, sparen, angreifen; „zum Ersten Mal“ nur wenn wahr) UND mit mehr BETONUNG gesprochen (Nutzer 24.11. klargestellt: NICHT lauter machen, NICHT höher/schneller per Effekt – das klingt nach Computer; Stimme bleibt gleich, die Betonung kommt aus der Sprachausgabe selbst, z. B. Satz 1 einzeln erzeugen mit Betonungs-Schreibweise; Lautstärke wie der Rest). `scripts/lauter_start.py` NICHT mehr benutzen. **Hook-Stil ABWECHSELN (Nutzer 24.11., Hörprobe: Variante 3 und 1 „sehr gut“; NICHT bei jedem Video dieselbe nehmen):** A) normal gesprochen, ohne Änderung; B) „Kurzsatz“: Hook in ZWEI kurze Ausrufe-Sätze teilen, z. B. „Dein Börsenverlust! Könnte Amerika Milliarden sparen!“ (im sprechtext; Stimme hebt sich von selbst, messbar höher, kein Effekt). B nur bei etwa jedem 2.–3. Video, wenn der Hook zwei klare Teile hat. Keine Lautstärke-/Pitch-/Tempo-Effekte.
- **Immer drin (Nutzer 22.11.):** Logo-Intro, Kommentar-Overlay (Button, KEIN gesprochener Kommentar-Satz), bei Serien „Teil X“ am Anfang + Teaser auf nächsten Teil, Cover 9:16, Folgen-CTA als letzter Satz.
- Setup-Skript enthält yt-dlp/ffmpeg/whisper; TikTok-Hosts sind freigegeben; Sprache→Text per ElevenLabs (Whisper-Modell gesperrt).
- **CTA-Position (Nutzer 25.11., bestätigt „Ja“):** Teilen-/Folgen-Aufruf steht als ZWEITER Satz direkt nach dem Hook (z. B. „Teile das Video mit deinen Freunden und folge uns, wir bringen jeden Tag neue Geld-Tipps!“), im Bild Beagle + „+ Folgen“ + „Video teilen“. Am Ende KEIN Folgen-Satz mehr; letzter Satz = Hinweis. (ersetzt die Regel vom 23.11.)
- **(überholt) Satz-Reihenfolge am Ende (Nutzer 23.11.):** vorletzter Satz = Folgen-CTA („Folge HundeFinanzTv …“), LETZTER Satz = „Kurzer Hinweis: Das ist keine Anlageberatung, nur eine Erklärung.“ (ersetzt die alte Regel „Folgen-CTA zuletzt“)
- Ab 19.11. ALLE Videos (auch Longform) nur 61–75 s, bis der Nutzer etwas anderes sagt (2–3 Min. liefen schlecht). Logo-Intro wie beim Short nach ca. 15 s
- **Covers (Nutzer 24.11.: „sehen schrecklich aus“):** Ursache war fehlende Schrift (Fallback Arial). `cover_hell.py` bindet jetzt Montserrat aus `brand/fonts/` ein. Neuer Stil: RIESIGE Überschrift (≈150 px, 2 Zeilen, Großbuchstaben), 2 große Kontrast-Karten (rot/grün) mit EINER fetten Zahl, dynamisches Element (Kurve/Pfeil), orange Pille unten, ganze Fläche nutzen (kein leeres Drittel). Vorbild: `videos/crash-usa-schulden/cover.py`.
- **Cover-Hintergrund SCHWARZ (Nutzer 24.11., „hochwertiger“):** Stil = Mischung aus „Dark Glow“ (leuchtende Kurve, Neon-Zahl) und „Gold-Münze“ (goldene Dollar-Münze, rote/grüne Schilder). Geteilter Bildschirm rot/grün und weiße Karten = abgelehnt. Baukasten: `scripts/cover_dark.py` (coin, zahnrad, kurve, schild, neon, kopf, pille); Vorbilder: `videos/crash-usa-schulden/covers_neu.py` (Variante D = gewählt) und `covers_serie.py`. Immer 3 Varianten anbieten.
- **Lieferung pro Video (Nutzer 24.11.), immer alles zusammen:** (1) MP4, (2) **3 verschiedene Cover** im schwarzen Stil (`scripts/cover_dark.py`, Dateien `<name>-A/B/C.jpg`, Favorit als `<name>-tiktok.jpg`), (3) **Beschreibung zum Kopieren** im Stil von @professorfinanzen: Hook-Zeile mit Emojis (🇺🇸📉), kurze Absätze mit den geprüften Zahlen, Gegenargument, Frage an die Community (💬 „Was glaubst du …?“), **📚 Quellen:** NUR die wirklich genutzten (Name + Link im Chat), Hashtags, dazu 10 Tags. Bei Referenz-Videos zusätzlich: Faktencheck der Original-Zahlen nennen.
- **Cover-SICHERE ZONE (Nutzer 24.11.):** Instagram/TikTok zeigen im Profil-Raster nur den mittleren 3:4-Ausschnitt (oben/unten je ≈ 240 px abgeschnitten). ALLES Wichtige (Überschrift, Zahl, Pille) nur zwischen y = 250 und y = 1670, Schrift groß (Schilder ≥ 50 px), keine Kleinsttexte. Vorlage: `videos/crash-usa-schulden/covers_safe.py`. Vor Abgabe 3:4-Ausschnitt prüfen (`crop=1080:1440:0:240`).
- Oranger Rahmen immer bei Video und Thumbnail
- Kein Thema/keine Firma innerhalb von 30 Tagen wiederholen (auch nicht mit „neuem Blickwinkel“); Bereiche abwechseln, Börse/KI selten
- Abend-Börsenrückblick startet immer mit „Alles, was heute an der Börse passiert ist – in 60 Sekunden.“
- Alles auf Deutsch, Antworten sehr kurz und iPad-tauglich, ohne Fachwörter
- Higgsfield nur für Kanal 2 (siehe oben), sonst nicht (kostet Credits)

- **Cover-Anzahl (Nutzer 25.11.):** ab sofort nur noch **2 Cover** pro Video (`<name>-A.jpg`, `<name>-B.jpg`, Favorit zusätzlich als `<name>-tiktok.jpg`), nicht mehr 3. Ersetzt „3 Varianten“.
