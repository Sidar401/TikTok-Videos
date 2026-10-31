# TikTok-Shop-Videos (HundeWissenTv 2.0)

Ziel: ca. 5 Videos pro Tag, 9:16, max. 20 s, ohne Stimme (Trend-Sound in TikTok drunterlegen).

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
