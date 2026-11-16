# TikTok-Shop-Videos (HundeWissenTv 2.0)

Ziel: ca. 5 Videos pro Tag, 9:16, max. 20 s.
**Stimme (ab 16.11.): immer Novaro-Stimme** (ElevenLabs „Dan – Engaging Science Instructor“, `BHr135B5EUBtaWheVj8S`, `eleven_v4`):
`python3 scripts/shop_stimme.py videos/<name> sprechtext.txt` (ein Satz pro Zeile, Zahlen ausgeschrieben).

## Ablauf pro Produkt (1 Produkt → 4 Videos)
1. Nutzer schickt Screenshots der Shop-Seite (Bild, Preis, Sterne, „verkauft“).
2. Produktbild freistellen → `shop/<produkt>/produkt.png`.
3. Higgsfield (`gpt_image_2_5`, high, 9:16, ca. 1,5 Credits/Bild): 8 Startbilder **mit dem Produktfoto als Referenz**,
   immer derselbe Hund (Papillon aus `shop/spielball`), damit der Kanal wiedererkennbar ist.
4. Higgsfield (`kling3_0`, std, 5 s, sound off, ca. 7,5 Credits/Clip): 10 Clips aus den Startbildern.
   URLs in `shop/<produkt>/clips.txt` eintragen.
5. 4 Konfigs `shop/<produkt>/*.json` schreiben (Vorbild: `shop/spielball/`), je 4–6 Schnitte à 2–3 s.
6. `python3 scripts/shop_video.py shop/<produkt>/<x>.json` → `videos/<name>/index.html`.
7. Clips holen + rendern: `scripts/hole_clips.sh shop/<produkt>`, dann in jedem Video
   `npx hyperframes render --quality delivery --output ../../renders/<name>.mp4`.
   Diese Sitzung erreicht Higgsfield nicht → Schritt 7 in der Higgsfield-Sandbox (`sandbox_exec`):
   Repo klonen, rendern, MP4 per `media_upload` zurück zu Higgsfield.

**Kosten pro Produkt: ca. 90 Credits → 4 Videos.** Für 5 Videos/Tag: Clips über mehrere Produkte
wiederverwenden (z. B. „Hund langweilt sich“, „Besitzer geht“, „Hund schläft“ sind produktunabhängig).

## Story-Formate (je Produkt alle 4)
- **A – POV:** „POV: Du musst zur Arbeit“ → Problem → Produkt → Reaktion → Ergebnis
- **B – Demo:** „Dieser … ist gerade überall 🔥“ → Funktionen im Schnelldurchlauf
- **C – Problem/Geld:** „Wenn dein Hund sich langweilt … wird's teuer“ → Lösung für X €
- **D – 3 Gründe:** „3 Gründe, warum 12.500 Hundehalter …“

## Untertitel
`|` = neue Zeile, `*Wort*` oder `*zwei Wörter*` = orange. Max. 2–3 Zeilen, kurze Wörter.

## Beim Posten
- Schalter **„KI-generiert“** an (KI-Clips!)
- Trend-Sound drunter, Produkt im Warenkorb verlinken
- Preis im Video vor dem Posten prüfen (Deals ändern sich)

## Demo-Videos ohne KI und ohne Stimme (kostenlos, ab 16.11.)
`python3 scripts/shop_demo.py shop/<produkt>/demo-<x>.json` – nur Produktfoto + Grafik (Emojis, Preis-Stempel, Merkmale).
Muster: `shop/spielball/demo-*.json` → `renders/demo-ball-*.mp4` (je 15 s).
Nutzer-Feedback 16.11.: **C (Problem/Geld) und D (3 Gründe) gut**, A (POV) und B (gerade überall) gefallen nicht → bei Demo-Videos A/B nicht mehr nutzen.

## Studio-Stil (ab 16.11., Nutzer: Emojis wirken unprofessionell)
`python3 scripts/shop_studio.py shop/<produkt>/studio-<x>.json` – Linien-Icons, Karten, Vergleichstabelle, Hinweise am Produkt, Zähler.
Formate: Vergleich, Fehler, Frage, Geld (Muster: `shop/spielball/studio-*.json` → `renders/studio-ball-*.mp4`). **Keine Emojis mehr.**
