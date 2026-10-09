# HZV Verteilgebiete-Karten

Interaktive PLZ-Karten der HZV handzettelverteiler GmbH für Kundenangebote.
Veröffentlicht über GitHub Pages: `https://handzettelverteiler.github.io/hzv-karten/<datei>.html`

Suchmaschinen sind per robots.txt und noindex ausgeschlossen. Die Karten sind nur über den direkten Link erreichbar.

## Werkzeuge (`tools/`)

- `build_karte.py`: maßgebliche Fassung des Kartengenerators (inkl. `--highlight-plz`, `--hide-sidebar`, Mehrteil-PLZ, `?shot=1&plz=` Screenshot-Modus). Immer diese Fassung nutzen, nicht die Kopie in der Skill.
- `publish.sh <datei.html>`: legt die Karte ins Repo, pusht und gibt den Live-Link aus.
- `build_angebot.js` + `fix_rid0.py`: maßgebliche 8-Seiten-Fassung des Angebots-Generators (v4: Beispielseite, Stadtbild automatisch aus `staedte/` – Seite 3 normal, Seite 4 Lupen-Variante –, Ortsteile einer PLZ, Flyerdruck Option A/B, Footer-Fix für OpenOffice). Aufruf: `HZV_ASSETS=/mnt/skills/plugins/hzv-angebot/assets NODE_PATH=$(npm root -g) node tools/build_angebot.js --config config.json --output Angebot_<Kunde>_<Datum>_<Stadt>.docx`. Die Kopie in der Skill fällt regelmäßig auf v2 zurück – diese hier verwenden. Liefert der Kunde die Flyer selbst: `"flyerdruck": false` in der Config → keine Flyerdruck-Seite (7 Seiten), Materialien-Text ohne Druck-Hinweis.

## Stadtbilder (`staedte/`)

- `Stadt_<Slug>.jpg` (1600×873, weißer Hintergrund): Stadtbild über der Übersichtskarte (Angebot Seite 3).
- `Stadt_<Slug>_Lupe.jpg`: Lupen-Variante über der Beispiel-PLZ-Karte (Seite 4).
- 104 Städte (die 100 größten + Gießen, Konstanz, Worms, Villingen-Schwenningen) plus `Stadt_Allgemein` für Orte ohne eigenes Bild.
- `index.json`: Stadtname (klein, ohne Umlaute/Sonderzeichen) → Slug.
- `eigene/`: Stefans eigene Stadtbilder (z. B. Gemini), die nicht in den Skill-Assets liegen. Neue Uploads von Stefan hier als `Stadt_<Stadt>.jpg` ablegen.

`build_angebot.js` (v4) wählt die Bilder automatisch über `config.stadt`. Reihenfolge: `config.stadt_illustration` → neue Zeichnung (`staedte/`) → `staedte/eigene/` → Skill-Assets `staedte_logos/` → `Stadt_Allgemein`. Seite 4 nimmt automatisch die `_Lupe`-Variante, sonst dasselbe Bild. Aufruf mit `HZV_STAEDTE=/home/claude/hzv-karten/staedte` (Standard: `../staedte` relativ zum Skript).

## Dateinamen

`<Projekt>_Karte_v<Version>_<Info>.html`, ohne Umlaute und Leerzeichen.
