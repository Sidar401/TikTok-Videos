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
   - **Höchstens 40 s** (Nutzerwunsch ab 26.10.) ≈ 90–100 Wörter, 9–11 Sätze (ein Satz = ein Bild, 2–4 s).
   - Aufbau aus `STIL.md`: Hook (0–3 s) → Frage/Problem → Beispiel mit echten Zahlen → Visualisierung → Faustregel/Meinung → kurzer CTA.
   - **Zusatz-CTAs abwechselnd:** Video A → Kommentar-CTA („Schreib uns in die Kommentare …“), Video B → Teilen-CTA („Teile das Video mit jemandem, der …“), dann wieder A. Nie beide in einem Video. Im Chat beim Skript angeben, welcher CTA drin ist.
   - **CTA immer in Wir-Form**, nie „folg mir“: z. B. „Folge HundeFinanzTV, wir haben noch mehr Geld-Tipps für dich!“ (Outro-Button bleibt „+ Folgen“).
   - Skript: Zahlen im `sprechtext` ausschreiben (für ElevenLabs); den Untertitel-`text` mit `python3 scripts/zahlen.py videos/<name>/skript.json` erzeugen (Zahlwörter → Ziffern, „dreihundert Euro“ → „300 €“).
   - **Keine Wiederholungen:** Vor Ideen/Skript `THEMEN.md` lesen (Archiv aller Videos), nach jedem Video dort eintragen. Andere Beispiele, Namen, Zahlen und Bildideen als bisher. **Auch Thumbnails:** Thumbnail-Archiv in `THEMEN.md` prüfen, jedes Mal neue Motive/Layouts (Geldbeutel gesperrt).
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
   - Marken-Badge oben (nur Name „HundeFinanzTV“), oranger Rahmen. **Kein Logo im Video**; Einstieg = Thema groß als Text + passende Szene (Logo-Regel in `STIL.md`). Maskottchen/Logo = Beagle (`assets/beagle.png`) **nur in CTA-Szenen** (Folgen-CTA, Outro), sonst nie; der Aussie gehört nur zu HundeWissenTv.
   - Audio: `<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="<dauer>" data-track-index="3"></audio>` im Root.
   - Animation: Pop-in, langsamer Drift, Linien zeichnen (Helfer `pop`/`drift`/`draw` aus der Vorlage).
6. **Prüfen:** `cd videos/<name> && npx hyperframes lint && npx hyperframes check`. Fehler beheben. Warnungen „nested_structure“/„track_too_dense“ und der Kontrast der Untertitel-Box sind bekannt und ok.
7. **Ansehen:** `npx hyperframes snapshot --at <Mitte jeder Szene>` und das Kontaktblatt lesen: Text im Bild, nichts abgeschnitten, Motiv passt zum Satz.
8. **Rendern:** `npx hyperframes render --quality delivery --output ../../renders/<name>.mp4`; Dauer mit `ffprobe` gegen `dauer` prüfen.
9. **Abliefern:** committen + pushen (Branch laut Session), MP4 per `SendUserFile` schicken, dazu Titel, Länge, Caption **und Hashtags nur für EINE Plattform** (Nutzer, 27.10.: nicht mehr TikTok/YouTube/Instagram getrennt):
   - **Hashtags:** 5–8 Stück, Mix aus 2 großen (#geld #finanzen), 3–4 Nischen-Tags zum Thema, 1–2 Reichweiten-Tags (#fyp #fürdich) + #hundefinanztv.
   - **Dazu immer 10 passende Tags** (ohne #, kommagetrennt, z. B. fürs YouTube-Tag-Feld).

## Regeln

- **Erste 3 Sekunden:** Frame 0 ist nie leer, Thema/Hook und Hauptmotiv sind sofort sichtbar (nur leichtes Scale-Einrasten, kein Einblenden aus Opacity 0).

- Text nur im Bereich y = 168–1330, außer der Untertitel-Box (Oberkante 1360, wie in den Referenzen).
- Keine CDNs (gesperrt): nur lokale Dateien in `assets/`.
- Logos/Fotos echter Firmen nur, wenn der Nutzer sie liefert; sonst neutrale Grafik.
- Neue Kanal-Entscheidungen (Farbe, Name, Stimme) in `kanal.json` bzw. `STIL.md` festhalten.

## Unsere Vorgehensweise (Nutzer, nach „Bist du arm oder reich?“ – so ab sofort IMMER)
Das Einkommen-Video (`videos/longform-einkommen`) ist der Qualitäts-Maßstab: „viel professioneller, viel Spaß, Entertainment, immer schön verbessern“.
- **Eigenes Leitmotiv pro Video:** ein neues, durchgehendes Bild-Konzept, das es so noch nicht gab (dort: Einkommens-Leiter, die Stufe für Stufe aufleuchtet).
- **Abwechslung:** viele verschiedene Szenentypen (Leitmotiv, kleine Erklär-Szenen wie „9 Leute + Millionär“, Duell, Balken, Chips, farbige Karten) – nie dieselbe Szenenart mehrmals hintereinander.
- **Entertainment:** Neugier-Fragen, Überraschungs-Zahlen, Mitmach-Element („merk dir deine Stufe“), lockere Sprache.
- **Nichts wiederholen:** `THEMEN.md` (Themen + Thumbnails) prüfen und ergänzen; Geldbeutel/Kassenzettel nur noch, wenn wirklich neu.
- **Jedes Video ein Stück besser** als das letzte: nach dem Rendern kurz notieren, was beim nächsten Mal besser geht.

## Shorts aus Longform (Nutzer-Wunsch, merken!)
- Aus jedem Longform-Video 4–8 Shorts (9:16) schneiden – **ohne neue Voice** (Original-Voice-Ausschnitte wiederverwenden).
- Jeder Short endet mit Verweis aufs Hauptvideo („Das ganze Video findest du auf YouTube/in unserem Profil“).
- Starke Einzelszenen wählen (Hook, Aha-Zahl, Twist), Grafiken für 9:16 neu anordnen.

## NEUER STANDARD für Shorts (ab 27.10., Nutzer: „viel besser“)
- Stil „Dark Glow“ mit `scripts/glow_short.py` (Vorlage: `videos/arbeitsstunden-v2/build.py`): dunkler Raster-Hintergrund, oranges Leuchten, oranger Rahmen.
- **20–30 s**, Hook im ersten Bild (stärkste Aussage + Motiv sofort sichtbar, keine Einleitung).
- Bildwechsel alle 1–2 s, Zoom-Drift je Szene, slam/pop/shake, Zahlen zählen hoch.
- Wort-für-Wort-Untertitel (aktives Wort orange), Soundeffekte (whoosh bei Szenenwechsel, pop, ding, boom, tick, kasse).
- Musik wählt der Nutzer in TikTok (Trend-Sound leise).
- Alte Aufnahmen lassen sich ohne Credits umbauen: `scripts/kurz.py` (Sätze auswählen/kürzen) → neues build.py.
- **Gilt ab 27.10. auch für Longform (16:9)**: gleicher Dark-Glow-Look (dunkel, Glow, oranger Rahmen, Wort-Untertitel, Soundeffekte, schnellere Bildwechsel). `scripts/longform.py` dafür beim nächsten Longform auf den Glow-Stil umstellen (Vorbild `scripts/glow_short.py`).
- Alte, schon fertige Videos postet der Nutzer unverändert – nicht neu bauen.

- **Logo in Shorts (Nutzer, 27.10.):** Beagle-Logo oben über „HundeFinanzTv“ (Name normal geschrieben, **nicht in Großbuchstaben** – Nutzer, 27.10.), im ganzen Video durchgehend sichtbar (ersetzt für Shorts die alte Regel „Beagle nur im CTA“). Ist in `glow_short.py` eingebaut.

- **Videos ohne Stimme** (z. B. Kanal-Trailer, Nutzer 29.10.): `build(HERE, SZENEN, SFX, dauer=30.0, musik=beat(30.0, pausen=[(a, drop)]))` – Beat aus `scripts/musik.py` (120 BPM, Breakdown + Drop) plus Soundeffekte; Helfer `partikel`/`burst`, `buchstaben`/`letters`, `flash`, `glitch`. Vorlagen: `videos/willkommen-*/build.py`.

- **Abgelehnt (Nutzer 6.11.):** Stil „wachsendes Leitbild“ mit Beagle unten + Ein-Wort-Untertiteln („zu viele Hundelogos“) → beim Dark-Glow-Stil wie `videos/freistellungsauftrag` bleiben. Alte Probe: `videos/gehalt-fluss/build-probe-leitbild.py`.

- **Longform 16:9 im Dark-Glow-Stil (ab 6.11.):** `import glow_short as g; g.querformat()` vor dem Szenenbau, dann wie Shorts mit `build(...)` (Logo klein oben links, Untertitel unten bei y=900). Vorlage: `videos/longform-ki-blase/build.py` (Firmen-Plaketten statt echter Logos, Nutzer wählte „Weg 2“).

- **Thumbnails bei Longform (Nutzer 6.11.):** IMMER zwei Versionen liefern: 16:9 für YouTube (`<name>-1.jpg`) **und zusätzlich 9:16** (`<name>-tiktok.jpg`), gleiches Motiv, für Hochformat neu angeordnet.

- **CTA-Regel (Nutzer 8.11.):** Nicht jedes Video braucht „Folge HundeFinanzTv, wir posten jeden Tag“. Ein CTA reicht oft – z. B. Teilen-CTA („Schick das jemandem, der …“) schon als **3. Satz**. Der Nutzer bearbeitet Skripte manchmal selbst → Aufnahme immer per DTW gegen Varianten (ohne s3, CTA verschoben) prüfen.
- **CTAs nicht ans Ende (Nutzer 7.11.):** Folgen-CTA früh (nach dem Hook), Teilen-/Kommentar-CTA in der Mitte. Kein Schluss-CTA wie „Wir sind HundeFinanzTv, wir sehen uns morgen“ – das Video endet mit dem letzten Inhalts-Satz (Nutzer schneidet späte CTAs raus).

- **Aussprache (Nutzer 7.11., „sehr gute Idee“):** Abkürzungen im `sprechtext` lautschriftlich: ETF → „E-Te-Eff“, USA → „U-Es-A“ (oder „Amerika“), KI → „Ka-I“, MSCI World → „Em-Es-Ze-I World“, DAX bleibt. Im Untertitel-`text` normal schreiben.
- **Tempo ab 7.11.: `--tempo 1.12`** bei sync.py (1,08 zu langsam, 1,15 zu schnell).
- **Satz-Reihenfolge der Aufnahme prüfen:** Liegt ein Satz an anderer Stelle (z. B. Folgen-CTA am Ende), Skript in Aufnahme-Reihenfolge syncen und Audio-Blöcke danach umschneiden (Muster: `videos/deutschlandticket-2027`, `skript-plan.json`).

## Tagesablauf (Nutzer 7.11.)
- Täglich **1 Longform + 2 Shorts** (Nutzer 8.11.). Longform **täglich im Hochformat 9:16** (für TikTok/Instagram, Thumbnail 9:16). **Jeden 3. Tag (8.11., 11.11., 14.11., …) zusätzlich 16:9** für YouTube (gleiche Stimme, Szenen neu angeordnet, Thumbnail 16:9). Shorts täglich überall.
- Geplante Aufgabe „HundeFinanzTv Tagesideen“ jeden Tag 11:40 Uhr (Berlin): aktuelle Trends recherchieren, `THEMEN.md` prüfen, je 3 Ideen für Longform, Short 1, Short 2 + Empfehlung. Skripte erst nach Auswahl des Nutzers.

## Stimme per API (Nutzer 8.11.)
- Ablauf: Skript schreiben → Nutzer gibt frei („passt“) → `python3 scripts/stimme.py videos/<name>` (Stimme „HundeTV“, eleven_v4) → `sync.py … --tempo 1.12` → bauen/rendern. Kein MP3-Upload mehr nötig.
- Credits: Schlüssel-Limit 100.000/Monat, **geteilt mit Kanal Novaro**; Abo ~121.000. Vor jeder Erzeugung `python3 scripts/stimme.py --stand`; bei < 15.000 frei den Nutzer warnen.
- **Motor-Short (Nutzer 8.11.):** Täglich bei **einem der 2 Shorts** auf ein YouTube-Longform hinweisen – Thema passend zum letzten YouTube-Longform. Letzter Satz NUR Hinweis, dass es das Video bei uns auf dem Kanal gibt (Nutzer 10.11.), z. B. „Ein ganzes Video dazu findest du bei uns auf dem Kanal.“ – NIE „unten verlinkt“/„unter dem Video“, kein Pfeil nach unten. Endkarte: Longform-Thumbnail + „Auf unserem Kanal“. Ausnahme von der Regel „kein Schluss-CTA“. Nutzer verlinkt NICHTS (kein „Verwandtes Video“ mehr nennen).
- **Longform-Länge ab 9.11.: 2–3 Minuten** (≈ 300–450 Wörter, ≈ 2.500–3.500 Credits) – Nutzer: „erstmal“ so.
- **Echte Logos (Nutzer 10.11.: „immer die echten Logos holen, professioneller“):** `python3 scripts/logos.py <name> …` lädt von Wikimedia Commons nach `brand/logos/` (Cache). Ins Video nach `assets/logos/` kopieren und auf weißer/heller Plakette zeigen. Nur redaktionell, nie wie Partner/Werbung. Fehlt ein Logo: `--datei <name> <Commons-Dateiname>`; geht gar nicht → Namens-Plakette (glow_teile.plakette).

## Soundeffekte (ab 10.11.)
32 echte ElevenLabs-Sounds in `brand/sfx/` (Liste + Hörprobe: `brand/sfx/LISTE.md`, `renders/sfx-hoerprobe.mp3`).
In `SFX` einfach den Dateinamen als Art nutzen, z. B. `(cap("s4", 2), "muenzen-glas")`, `"kurve-hoch"`, `"tresor"`, `"falsch"`/`"richtig"`.
`kasse` und `pop` nutzen jetzt automatisch die echten Sounds; `whoosh`, `boom`, `ding`, `tick` bleiben synthetisch (Alternativen: `whoosh-schnell`, `whoosh-weich`, `bass-schlag`, `richtig`, `klick`).
Pro Video passende Sounds abwechseln, nicht immer dieselben. Neue Sounds: Eintrag in `scripts/sfx_gen.py` (min. 0,5 s), dann `python3 scripts/sfx_gen.py <name>` (~10 Credits/Sound).

### Novaro-Sounds (ab 10.11., Nutzer-Wunsch)
32 weitere Sounds aus dem Novaro-Kanal liegen als `brand/sfx/nv-<name>.mp3` (Liste in `brand/sfx/LISTE.md`), Nutzung gleich: `"nv-gong"`.

### Wann welcher Sound (MUSS zum Bild passen, sparsam: 1 Sound pro Moment, nicht jede Zeile)
| Moment im Video | Sound |
|---|---|
| Hook / große Zahl knallt rein | `bass-schlag`, `nv-boom-tief`, `nv-film-horn` (selten) |
| Geld kommt dazu, Ersparnis, Gewinn | `kasse`, `muenzen-glas`, `geld-erhalten`, `geldschein` |
| Kurve/Kurs steigt bzw. fällt | `kurve-hoch` / `kurve-runter` |
| Zahl zählt hoch | `zaehler` |
| Fehler, Falle, „das ist falsch“ | `falsch`, `nv-falsch-buzzer`, `nv-platte-kratzer` (lustig) |
| Richtig, Tipp, Lösung | `richtig`, `nv-pling-idee`, `level-up` |
| Warnung, Achtung, Frist | `alarm`, `uhr-tickt`, `nv-countdown` |
| Spannung vor Auflösung | `spannung`, `nv-sog`, `herzschlag`, `nv-dun-dun-dun` |
| Auflösung / Enthüllung | `nv-tusch`, `nv-gong` |
| Crash, Blase platzt, Schock | `glas-bricht`, `blase-platzt`, `nv-explosion-fern`, `nv-erdbeben` |
| Handy/App/Bank-App | `handy-benachrichtigung`, `swipe`, `klick`, `karte-piep` |
| Rechnen, Formular, Steuer | `taschenrechner`, `tippen`, `stempel`, `papier-reissen` |
| Tresor, Sparen, Sicherheit | `tresor` |
| Szenenwechsel | `whoosh-schnell`, `whoosh-weich`, `nv-whoosh-tief` |
| Überraschung beim Zuschauer | `nv-staunen-wow` |
Nicht für Finanz: `nv-laser`, `nv-raumschiff`, `nv-rakete` (nur bei „Aktie geht zum Mond“-Witz), `nv-sturm`, `nv-donner`, `nv-wasser-platsch`, `nv-publikum-lachen` (nur selten als Gag).
Abwechseln: nicht in jedem Video dieselben; pro Video ca. 3–6 verschiedene echte Sounds + Whooshes.

## Shorts-Länge NEU (Nutzer 10.11.): alle Shorts 61–75 s
Ab sofort jeder Short **61–75 Sekunden** (TikTok/IG/YouTube pushen > 1 Min.). Ca. 15–17 Sätze / ~200 Wörter bei Tempo 1.12.
Ist die Stimme zu lang: Satz streichen (Audio-Schnitt wie bei anthropic-boersengang: Satz aus voice.wav schneiden, skript.json anpassen, `sync.py … --tempo 1.07`).
Longform bleibt 2–3 Min.; YouTube-16:9 alle 3 Tage.

## Analyse-Look (Nutzer 10.11.: „Skizzen, Analysen … professionell, nicht immer das Gleiche“)
Baukasten `scripts/analyse_kit.py` (Vorbild: `videos/anthropic-boersengang/build.py`): echte Logo-Karten + Logo-Netz mit Pfeilen,
handgezeichnete Pfeile/Kreise/Unterstriche (zeichnen sich selbst), Handschrift-Notizen (Caveat) und Klebezettel, Analyse-Karten mit
Millimeterpapier, Balken mit Notizen, Donut, Preis-Spanne, Kurs-Laufband, Aktien-Raster, Server-Racks, Ablauf-Kästen, Stempel.
Pro Video Mischung wechseln, nicht jede Szene gleich. Text über Karten mit z-index (siehe `tz()` in anthropic-boersengang).
Fehlt ein Original-Logo (z. B. TSMC nicht auf Commons): Wortmarke per `logo_karte(..., text="tsmc", farbe=…)`.

## ⭐ QUALITÄTS-STANDARD (Nutzer 10.11.: „genau so professionell ab sofort immer … geil gemacht, wirklich super“)
Referenz = `videos/anthropic-boersengang/` (Render `renders/anthropic-boersengang.mp4`). JEDES Video (Short + Longform) mindestens auf diesem Niveau:
- Echte Original-Logos aller genannten Firmen/Institutionen (scripts/logos.py), als weiße Logo-Karten, gern als Netz mit Pfeilen.
- Jede Szene „Analyse“-Charakter: Karte mit Millimeterpapier, Diagramm/Balken/Donut/Spanne/Raster, dazu Handschrift-Notizen,
  selbst zeichnende Pfeile/Kreise/Unterstriche, Stempel, Klebezettel (scripts/analyse_kit.py). Keine Szene nur mit Text.
- Pro Satz 1 neues Bild-Element genau auf dem gesprochenen Wort (cap(sid, i)); Zahlen zählen hoch, wichtige Zahl wird eingekreist.
- Passende echte Sounds pro Moment (Tabelle oben), ca. 2–3 pro Satz-Gruppe, plus Whoosh bei Szenenwechsel.
- Zahlen aus Primärquellen prüfen; Quellen im Chat nennen.
- Vor dem Render alle Szenen als Snapshot-Bogen prüfen (Überlappungen, Text hinter Karten → tz(), Ränder).

## Aussprache-Update (Nutzer 11.11., per Hörprobe bestätigt) – gilt VOR der alten Liste
- ETF → „Eh-Teh-Eff“ (deutsches E, NICHT „E-Te-Eff“, das klingt wie „Itf“)
- MSCI World → „Em-Es-Si-Ai World“ (C wie „Si“)
- USA → „Amerika“ / „amerikanisch“ (NICHT „U-Es-A“, das klingt wie „You SA“)
- Dezimalzahlen mit eins: „eins Komma sieben“ (NICHT „ein Komma sieben“)
- Fotos echter Personen: nur Personen des öffentlichen Lebens mit freiem Foto (Wikimedia Commons, Lizenz + Quelle klein einblenden); Privatpersonen/Verdächtige nie, nur Silhouette.

## 📈 Börsen-Laufband IMMER (Nutzer 12.11.: Anthropic-Video 8.509 Aufrufe + Bitcoin-Video – beide hatten das Laufband)
NICHT bei jedem Video (Nutzer 12.11.: „sonst nicht professionell“) – NUR bei Börsen-/Aktien-/Krypto-Themen mit echten Kursbewegungen (z. B. Nvidia, Bitcoin, DAX, Börsengang). Dann ein dauerhaftes Börsen-Laufband über die ganze Länge – GROSS wie im Bitcoin-Video (Nutzer-Screenshot 12.11.): direkt über den Untertiteln (top 1200, 90 px hoch, Schrift 48 px, Mono). Szenen-Inhalte deshalb nur bis y ≈ 1180 planen:
`SZENEN.append(laufband_szene([("NVDA ▼ −13 %", ROT), ("DAX ▲ 27.000", GRUEN), ...], DAUER))` (scripts/analyse_kit.py).
Nur echte, geprüfte Werte zum Thema des Videos (Kürzel + Pfeil + Zahl), grün/rot. Bei Verbraucher-Themen (Schufa, Weihnachtsgeld, Krankenkasse …) KEIN Laufband.

## Logos + Fotos wie Eulen-Kanal (Nutzer 12.11.: „Logos immer noch falsch“, „Bilder der Personen sollen da sein“)
- Logos IMMER komplett mit Symbol (z. B. Nvidia = grünes Auge + Schriftzug, Broadcom = rotes Symbol), GROSS, frei auf dem Hintergrund
  (bei dunklen Logos heller Glow statt weißer Karte), daneben ein Kurs-Schild (z. B. „−13 %“ rot / „+5 %“ grün). Nur Schriftzug = falsch.
- Fotos echter Personen GROSS und rechteckig wie Nachrichtenbild, mit kleiner Quellenzeile. Nur freie Lizenzen (Wikimedia Commons CC/PD,
  offizielle Regierungsporträts); keine Pressefotos (Reuters/Getty/AP). Commons-API sparsam (Rate-Limit) – Fotos früh im Ablauf holen.
- ETF/MSCI: ElevenLabs-Aussprache-Wörterbuch nutzen (Schreibweise allein reicht nicht, v4 variiert); ETF-Sätze vom Nutzer gegenhören lassen.
