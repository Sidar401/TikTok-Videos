---
name: novaro-ideen
description: Liefert jeden Abend (ab 19 Uhr) 3 neue, aktuelle Video-Ideen für den Weltraum-Kanal Novaro (für die 2 Shorts am nächsten Tag). Nutzen, wenn der Nutzer "3 Ideen", "Ideen für morgen" sagt oder die tägliche 19-Uhr-Erinnerung kommt.
---

# Novaro: 3 Ideen für morgen

Der Nutzer will **jeden Abend ab 19 Uhr 3 Ideen**, wählt dann 2 aus („eins und drei“, „los“) → danach
direkt durchproduzieren (Skript, ElevenLabs-Stimme, 3D-Szenen, Prüfen, Rendern, Thumbnail, Push, Senden).
Regeln: `wissen/REGELN.md` IMMER einhalten.

## Ablauf
1. **Aktuelle Weltraum-News suchen** (WebSearch, letzte 1–3 Tage, auch Termine für morgen:
   Starts, Livestreams, Himmelsereignisse). Mehrere Suchen parallel.
2. **Doppelte vermeiden:** `ls wissen/texte/` und grob reingrepen – kein Thema der letzten ~2 Wochen nochmal
   (außer es gibt wirklich Neues, dann sagen).
3. **3 Ideen auswählen** – bevorzugt was gut lief:
   - Drama mit „Lebewesen-Verben“: fressen, sterben, angreifen, explodieren, abstürzen („Stern frisst Stern“ lief super)
   - „zum ersten Mal“ / „noch nie gesehen“ (nur wenn wahr)
   - große Namen/Logos (NASA, ESA, SpaceX, Amazon, Google …), aktuelle Starts
   - gut als 3D-Szene darstellbar (Modelle in `wissen/kit/modelle.js`)
4. **Antwort an den Nutzer** (Deutsch, sehr kurz, iPad, keine Fachwörter):
   - je Idee: **Titel** (wie die Hook) + 1–2 Sätze, worum es geht + warum es zieht
   - Hinweis, falls ein Video zeitgebunden ist (z. B. „morgen Vormittag posten“)
   - am Ende Frage: „Welche 2?“ + Quellen als Links
