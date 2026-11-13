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
   - **Formate:** normale Videos immer **9:16** (TikTok/Instagram).
   - **Ca. 1× pro Woche Longform:** in **16:9** (für YouTube) **und am selben Tag dasselbe Video zusätzlich in 9:16**
     (für TikTok/Instagram).
   - **Thumbnails:** für **jedes** erstellte Video immer passende Thumbnails mitliefern (16:9-Video → 16:9-Thumbnail,
     9:16-Video → 9:16-Thumbnail).
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
