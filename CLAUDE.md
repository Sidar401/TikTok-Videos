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
   Ab ca. Ende Nov. 2026 zusätzlich **animierte Videos wie HundeFinanzTV**. Stimme = gleiche wie Kanal Novaro:
   ElevenLabs **„Dan“** (`BHr135B5EUBtaWheVj8S`, Modell `eleven_v4`), automatisch per `hundewissen/stimme.py`
   (mit Sprache-zu-Text-Kontrolle). Probe: `renders/hundewissen-stimmprobe.m4a`.
   - **Formate:** normale Videos (Shorts) immer **9:16**, Länge **60–80 s** (wird vom Algorithmus gepusht);
     gepostet auf TikTok, Instagram **und YouTube** (als Shorts).
   - **Ca. 1× pro Woche Longform:** in **16:9** (für YouTube) **und am selben Tag dasselbe Video zusätzlich in 9:16**
     (für TikTok/Instagram).
   - **Thumbnails:** für **jedes** erstellte Video immer passende Thumbnails mitliefern (16:9-Video → 16:9-Thumbnail,
     9:16-Video → 9:16-Thumbnail).
   - **Stil: „Magazin“** (vom Nutzer gewählt 13.11.): cremefarbenes Papier, Fraunces-Serif-Überschriften (Kursiv-Akzent orange),
     Aussie-Posen als sympathische Figur, saubere Schaubilder, kleine Quellenzeile. Kit: `hundewissen/magazin/`
     (CSS/JS, in `videos/<name>/assets/` kopieren). Beispiele: `videos/hw-mag-farben`, `hw-mag-hundejahre`, `hw-mag-gaehnen`.
   - **Kopf immer:** Beagle-Logo `beagle.png` (Kreis, oranger Rand) + darunter „HundeWissenTv“ – wie bei HundeFinanzTv.
     **Keine** „Nr. 01 – Thema“-Zeile oben rechts.
   - Demos ohne Stimme (spart ElevenLabs-Credits).
   - **Aktueller Stand (Nutzer 16.11.):** nur **ruhige Bilder** der Posen (kein Wackeln/Verformen – „sieht schrecklich aus“;
     vorerst keine Bewegung). **Kein Fortschrittsbalken** oben. **Ruhiges Tempo** (3 Szenen à ~4 s
     pro 15 s). **Schluss immer mit großem Logo** + oranger „+ Folgen“-Knopf.
     Bauen: `python3 hundewissen/bau_einfach.py <name>` (Inhalte dort in `VIDEOS`). Beispiele: `videos/hw-e-*`.
     (Altes Bewegungs-Werkzeug `hundewissen/rig/` nur zur Info, nicht benutzen.)
   - **Nutzer 16.11. (2):** **keine Lautwörter** („*kratz*“, „Zzz“ o. ä.), **keine kleine Überschrift (Kicker)** über dem
     großen Text. Schluss: nur Logo + „HundeWissenTv“ + **oranger „+ Folgen“-Knopf** (kein „Folg uns…“-Satz).
     Info-Kärtchen (z. B. „Flöhe?“) und Quellenzeile sind ok. Beispiele: `videos/hw-f-*`.
   - **Nutzer 17.11.:** **oranger Rahmen** (26 px, `#DB8622`) in **allen Videos und Thumbnails**. Demo-Stil `videos/hw-g-*`
     ist freigegeben („damit können wir anfangen“).
   - **Themen-Bilder:** Vor jedem Video passende Bilder zum Thema erzeugen (z. B. Lachsöl, Banane) – im gleichen
     Zeichenstil. **Kein Higgsfield** für diesen Kanal (Nutzer 17.11.: zu teuer) – immer ChatGPT-Texte für den Nutzer schreiben
     (Vorlage `renders/aussie-stil-neu.png`, Nutzer schafft ca. 3 Bilder pro Tag kostenlos).
   - **Posen fertig (20.11.):** 90 Posen in `brand/aussie/` (Liste in `STIL.md`). Keine weiteren Posen-Bögen nötig.
   - **Ablauf pro Video (Nutzer 20.11.):** Nutzer nennt das Thema → ich schreibe sofort die passenden **ChatGPT-Texte
     für Themen-Bilder** (Gegenstände/Futter/Szenen, gleicher Zeichenstil, weißer Hintergrund, ohne Text; max. 3 pro Tag)
     → Nutzer schickt Bilder → ausschneiden (`hundewissen/posen_schneiden.py` o. ä.) → Video bauen.
     Bögen mit Hund (2×3): `posen_schneiden.py` → `brand/aussie/`; Gegenstände in einer Reihe: `reihe_schneiden.py`
     → `brand/themen/` (im Builder als `pose="themen/<name>"`, Zusatzbilder über `bilder=[...]`).
     Mehr als 3 Szenen → automatisch 4,5 s je Szene + 3 s Schluss (6 Szenen = 30 s). Beispiel: `videos/hw-s*` (Schnellfresser).
   - **3-Teile-Serie pro Thema (Nutzer 23.11.):** am Posting-Tag aus einem Thema 3 Videos: **Teil 1 Problem & Gefahr**,
     **Teil 2 Tipps**, **Teil 3 Selbsttest** (Muster `videos/hw-s1-problem`, `hw-s2-tipps`, `hw-s3-test`).
   - **Kommentar-Aufruf (wie HundeFinanzTv-CTA, Nutzer 23.11.):** am Ende der letzten Szene dunkles Kommentar-Fenster,
     Text tippt mit Tasten-Klick, Zeiger klickt orangen „Kommentieren“-Knopf, Banner darunter. Im Builder `KOMMENTAR`
     (getippter Text + Banner) – danach Logo-Schluss.
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
- Alles auf Deutsch, Antworten sehr kurz und iPad-tauglich, ohne Fachwörter
- Higgsfield nur für Kanal 2 (siehe oben), sonst nicht (kostet Credits)
