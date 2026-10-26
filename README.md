# HZV Verteilgebiete-Karten

Interaktive PLZ-Karten der HZV handzettelverteiler GmbH für Kundenangebote.
Veröffentlicht über GitHub Pages: `https://handzettelverteiler.github.io/hzv-karten/<datei>.html`

Suchmaschinen sind per robots.txt und noindex ausgeschlossen. Die Karten sind nur über den direkten Link erreichbar.

## Werkzeuge (`tools/`)

- `build_karte.py`: maßgebliche Fassung des Kartengenerators (inkl. `--highlight-plz`, `--hide-sidebar`, Mehrteil-PLZ, `?shot=1&plz=` Screenshot-Modus). Immer diese Fassung nutzen, nicht die Kopie in der Skill.
- `publish.sh <datei.html>`: legt die Karte ins Repo, pusht und gibt den Live-Link aus.
- `build_angebot.js` + `fix_rid0.py`: maßgebliche Fassung des Angebots-Generators (v5: neue AGB Stand Oktober 2026 – 18 Paragraphen, 2 Seiten zweispaltig, Text direkt im Skript im Block `agbParas`; Angebot damit 9 Seiten, ohne Flyerdruck 8. Aus v4: Beispielseite, Stadtbild automatisch aus `staedte/` – Seite 3 normal, Seite 4 Lupen-Variante –, Ortsteile einer PLZ, Flyerdruck Option A/B, Footer-Fix für OpenOffice). Aufruf: `HZV_ASSETS=/mnt/skills/plugins/hzv-angebot/assets NODE_PATH=$(npm root -g) node tools/build_angebot.js --config config.json --output Angebot_<Kunde>_<Datum>_<Stadt>.docx`. Die Kopie in der Skill fällt regelmäßig auf v2 zurück – diese hier verwenden. Liefert der Kunde die Flyer selbst: `"flyerdruck": false` in der Config → keine Flyerdruck-Seite (7 Seiten), Materialien-Text ohne Druck-Hinweis.

## Stadtbilder (`staedte/`)

- `Stadt_<Slug>.jpg` (1600×873, weißer Hintergrund): Stadtbild über der Übersichtskarte (Angebot Seite 3).
- `Stadt_<Slug>_Lupe.jpg`: Lupen-Variante über der Beispiel-PLZ-Karte (Seite 4).
- 104 Städte (die 100 größten + Gießen, Konstanz, Worms, Villingen-Schwenningen) plus `Stadt_Allgemein` für Orte ohne eigenes Bild.
- `index.json`: Stadtname (klein, ohne Umlaute/Sonderzeichen) → Slug.
- `eigene/`: Stefans eigene Stadtbilder (z. B. Gemini), die nicht in den Skill-Assets liegen. Neue Uploads von Stefan hier als `Stadt_<Stadt>.jpg` ablegen.

`build_angebot.js` (v4) wählt die Bilder automatisch über `config.stadt`. Reihenfolge: `config.stadt_illustration` → neue Zeichnung (`staedte/`) → `staedte/eigene/` → Skill-Assets `staedte_logos/` → `Stadt_Allgemein`. Seite 4 nimmt automatisch die `_Lupe`-Variante, sonst dasselbe Bild. Aufruf mit `HZV_STAEDTE=/home/claude/hzv-karten/staedte` (Standard: `../staedte` relativ zum Skript).

## Dateinamen

`<Projekt>_Karte_v<Version>_<Info>.html`, ohne Umlaute und Leerzeichen.

## Angebots-Layout neu / alt (v6, ab 26.10.2026)

`tools/build_angebot.js` baut standardmäßig das **neue Layout** (von Stefan am 26.10.2026 freigegeben):
Seite 1 „Ihr Angebot auf einen Blick“ (Gebiet, Stückzahl, Gesamtpreis inkl. Anfahrt, Zeitraum, Nachweis, Beauftragung per E-Mail, gültig bis),
Seite 2 „So läuft Ihre Verteilung“ (4 Schritte, Vertrauenspunkte, Live-Kartenlink, „Gut zu wissen“),
Preistabelle mit An-/Abfahrt als eigener Zeile und Gesamtpreis, automatische Option „PLZ komplett beliefern“ bei einer teilbelieferten PLZ (Auffüllen),
Komplettpaket Druck + Verteilung, Abschlussseite „So einfach beauftragen Sie uns“ (E-Mail-Antwort genügt, Unterschrift optional).
Bewusst **nicht** enthalten: WhatsApp als Beauftragungsweg, „fester Ansprechpartner“, Preis pro Stück/Flyer (WhatsApp-QR nur für Rückfragen).

Neue Config-Felder (alle optional): `karten_link` (Live-Karte, erscheint auf Seite 2), `angebotsdatum`, `gueltig_bis` (Standard: heute + 3 Monate),
`absender.telefon` (Standard 0681 41098133), `option` (eigene Option als Objekt `{titel, text, plus_preis, plus_flyer}`, `false` = keine Option),
`teilmengen_text_neu`.

**Rückfall auf das alte Layout (v5):**
- nur für ein Angebot: `"layout": "alt"` in der Config
- für alle Angebote: `DEFAULT_LAYOUT = "alt"` im Skript setzen (oder `HZV_LAYOUT=alt` beim Aufruf)
- Branch `angebot-layout-alt-v5` = Repo-Stand direkt vor der Umstellung (Sicherung)
