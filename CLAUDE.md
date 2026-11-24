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
- **Erster Satz (Nutzer 24.11., Vorbild Novaro „Stern frisst Stern“):** spannender, packender Hook (ein Lebewesen/Akteur TUT etwas: fressen, verlieren, sparen, angreifen; „zum Ersten Mal“ nur wenn wahr) UND LAUTER gesprochen: nach sync.py `python3 scripts/lauter_start.py videos/<name>` (+4,5 dB), vor dem Logo-Intro. Gilt ab sofort bei JEDEM Video.
- **Immer drin (Nutzer 22.11.):** Logo-Intro, Kommentar-Overlay (Button, KEIN gesprochener Kommentar-Satz), bei Serien „Teil X“ am Anfang + Teaser auf nächsten Teil, Cover 9:16, Folgen-CTA als letzter Satz.
- Setup-Skript enthält yt-dlp/ffmpeg/whisper; TikTok-Hosts sind freigegeben; Sprache→Text per ElevenLabs (Whisper-Modell gesperrt).
- **Satz-Reihenfolge am Ende (Nutzer 23.11.):** vorletzter Satz = Folgen-CTA („Folge HundeFinanzTv …“), LETZTER Satz = „Kurzer Hinweis: Das ist keine Anlageberatung, nur eine Erklärung.“ (ersetzt die alte Regel „Folgen-CTA zuletzt“)
- Ab 19.11. ALLE Videos (auch Longform) nur 61–75 s, bis der Nutzer etwas anderes sagt (2–3 Min. liefen schlecht). Logo-Intro wie beim Short nach ca. 15 s
- Oranger Rahmen immer bei Video und Thumbnail
- Kein Thema/keine Firma innerhalb von 30 Tagen wiederholen (auch nicht mit „neuem Blickwinkel“); Bereiche abwechseln, Börse/KI selten
- Abend-Börsenrückblick startet immer mit „Alles, was heute an der Börse passiert ist – in 60 Sekunden.“
- Alles auf Deutsch, Antworten sehr kurz und iPad-tauglich, ohne Fachwörter
- Higgsfield nur für Kanal 2 (siehe oben), sonst nicht (kostet Credits)
