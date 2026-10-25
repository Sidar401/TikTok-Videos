# Kanal-Stil (aus Referenzen 2–4, @finanzbaer_ TikToks)

Referenzvideos: `refs/tiktok/ref2.mp4` (Abo-Wirtschaft/Zuora), `ref3.mp4` (Einmalanlage vs. Sparplan), `ref4.mp4` (Batteriespeicher). Analyse von YouTube-Referenz 1: `refs/ref1.md`.
Code-Vorlage: `vorlage/` (Demo: `renders/stil-demo.mp4`).

## Grundregeln
- Format 1080×1920, 30 fps, **Länge 45–60 s**, alles auf **Deutsch**
- **Reinweißer Hintergrund**, keine Verläufe, keine Rahmen
- **Ein Motiv pro Bild**, zentriert im oberen/mittleren Bereich (y ≈ 230–1310)
- **Bildwechsel alle 2–4 s** (harter Schnitt), jedes Bild illustriert genau den gesprochenen Halbsatz
- Voiceover (männlich, locker, schnell) + durchgehende Untertitel

## Branding HundeFinanzTV
- **Maskottchen HundeFinanzTV = der Beagle** (vom Nutzer so gewollt). **Nur in CTA-Szenen** (Folgen-CTA, Outro) – sonst nirgends im Video, auch nicht als Bild für Hund/Beispiele (Nutzer: „Logo zu oft“). Der Aussie gehört nur zu HundeWissenTv.
- Orange `#DB8622` aus HundeWissenTv: Untertitel-Box + **26 px oranger Rahmen** ums ganze Video (wie auf HundeWissenTv)
- Maskottchen: Beagle aus `brand/hundewissentv-logo.jpg` (dunkler Kreis `#353A3D`, Creme `#FAF5EF`)

## Untertitel-Box (Markenzeichen)
- Kanalfarbe aus `kanal.json` (Orange; Referenz nutzte Türkis `#19C4A0`), abgerundet (Radius 28 px), weiße Schrift
- Montserrat 600, 54 px, max. 2 Zeilen, kleingeschrieben wie gesprochen
- Position: horizontal zentriert, Oberkante y = 1360
- Wechselt pro Halbsatz (ca. 1,5–3 s), ohne Animation

## Motive
- **Flache Clipart-Illustrationen** (Geldsack, Zielscheibe, Kalender, Waage, Figuren mit Emotion)
- **Zahlen-Vergleiche** in fetter Serifenschrift (Abril Fatface): schwarz für Überschriften, **Grün `#1F7A4D`** für eingezahltes Geld, **Gold `#F2C418`** für Gewinn, schwarze Trennlinie + geschwungene Pfeile
- **Diagramme** minimalistisch: schwarze Achsen, Linien schwarz/grün, Markierungen mit ★ oder schwarzem ✓-Kreis, Rot `#E24B4B` für Verluste (rote Fläche unter Kurve)
- Echte Logos/Screenshots/Fotos, wenn es um konkrete Firmen geht (z. B. Netflix, Volvo, Tesla)
- Animation dezent: Pop-in (scale 0.82→1, back.out), langsamer Zoom, Linien zeichnen sich

## Aufbau (Story)
1. **Hook (0–3 s):** Alltagssituation oder Behauptung („du hast ein bisschen Geld gespart…“)
2. **Problem/Frage** („die Frage aller Fragen“)
3. **Erklärung mit Beispiel** und konkreten Zahlen
4. **Visualisierung** per Vergleich oder Chart
5. **Fazit/Faustregel** + persönliche Meinung („ich halte mich an…“)
6. Kein extra Outro-Bild in den Referenzen; optional kurzer CTA

## Logo-Regel (vom Nutzer)
- **Kein Logo im Video**, auch nicht am Anfang. Marken-Badge oben = nur Kanalname als Text. Auf Covern eine Pfote.
- Einstieg: das **Thema groß als Text** + passende Szene (z. B. „Warum **bellt** dein Hund ständig?“ mit bellendem Hund).

## Hauptfigur Hundekanäle: der Aussie
- Immer derselbe Australian Shepherd (blue merle), Cartoon-Posen in `brand/aussie/`: `sitzend`, `bellend`, `liegend`, `aengstlich`, `neugierig`, `springend` (freigestellte PNGs, Original: `posen-original.webp`).
- Passende Pose pro Szene wählen, per GSAP animieren (Pop-in, Hüpfen, Zittern); Spiegeln mit `pose(name, flip=True)`.
- Nicht selbst als SVG nachzeichnen. Fehlt eine Pose, den Nutzer bitten, sie im gleichen Stil zu erstellen.
- Vorlage für Hunde-Shorts: `videos/hunde-bellen-animiert/build.py`.

## Thumbnails & Cover (ab 25.10., Nutzer-Wunsch)
- Stil „Dark Glow“ (`scripts/thumbs.py`): dunkler Raster-Hintergrund, leuchtende Linien, fette Montserrat, plastische Objekte – nach Vorbild Finanzbär, aber in **Orange**.
- **Orange muss dominieren:** Hervorhebungs-Kasten im Titel immer orange; Rot/Grün nur als kleine Akzente (Zahlen, Kurven).
- **Kein Pfoten-Badge**, kein Beagle, kein Rahmen.
