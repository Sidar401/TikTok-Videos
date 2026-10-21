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

## Kanal
- Nische: **Geld & Finanzen** (faceless, animierte Grafiken, Zahlen, Diagramme)
- Ziele: maximale Reichweite, Sympathie, später Monetarisierung

## Regeln vom Nutzer
- Alles auf Deutsch
- Videos immer per Code (HyperFrames) bauen – **kein Higgsfield** (kostet Credits)
