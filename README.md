# HZV Verteilgebiete-Karten

Interaktive PLZ-Karten der HZV handzettelverteiler GmbH für Kundenangebote.
Veröffentlicht über GitHub Pages: `https://handzettelverteiler.github.io/hzv-karten/<datei>.html`

Suchmaschinen sind per robots.txt und noindex ausgeschlossen. Die Karten sind nur über den direkten Link erreichbar.

## Werkzeuge (`tools/`)

- `build_karte.py`: maßgebliche Fassung des Kartengenerators (inkl. `--highlight-plz`, `--hide-sidebar`, Mehrteil-PLZ, `?shot=1&plz=` Screenshot-Modus). Immer diese Fassung nutzen, nicht die Kopie in der Skill.
- `publish.sh <datei.html>`: legt die Karte ins Repo, pusht und gibt den Live-Link aus.
- `build_angebot.js` + `fix_rid0.py`: maßgebliche 8-Seiten-Fassung des Angebots-Generators (v3: Beispielseite, Stadtbild auf beiden Kartenseiten, Ortsteile einer PLZ, Flyerdruck Option A/B, Footer-Fix für OpenOffice). Aufruf: `HZV_ASSETS=/mnt/skills/plugins/hzv-angebot/assets NODE_PATH=$(npm root -g) node tools/build_angebot.js --config config.json --output Angebot_<Kunde>_<Datum>_<Stadt>.docx`. Die Kopie in der Skill fällt regelmäßig auf v2 zurück – diese hier verwenden.

## Dateinamen

`<Projekt>_Karte_v<Version>_<Info>.html`, ohne Umlaute und Leerzeichen.
