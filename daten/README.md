# Haushalts-Vorrat (POSTAKTUELL Manager)

`haushalte_plz_vorrat.csv` – bewerbbare Haushalte für alle PLZ der ~216 Städte (Top 200 + Kleinstädte), abgefragt am 2026-11-06.
Format wie `claude/haushalte_plz.csv` im Projekt: `plz;ort;hh_bewerbbar_post;hh_gerundet_50;abgefragt_am;quelle;hh_gesamt_post`.

Reihenfolge beim Nachschlagen: neueste Nachtragsdatei im Projekt > dieser Vorrat > `claude/haushalte_plz.csv`.
Werte älter als ~6 Monate vor Angebotsversand neu abfragen.

Lücken: 60306 Frankfurt (Portal hängt bei der Abfrage), Lahr/Schwarzwald 77933 (fehlt, im Lauf wurde das Eifeldorf 54675 erwischt).

## angebote_register.csv – Angebotsnummern (ab 09.11.2026)

Jedes Angebot bekommt eine Nummer **JJMM-NN** (z. B. `2611-03` = drittes Angebot im November 2026, ab Dezember `2612-01` …).
Neue Fassung desselben Angebots: Versionssuffix `-2`, `-3` (z. B. `2611-09-2`). November 2026 wurde rückwirkend nach Erstellzeit nummeriert.
Spalten: nr;datum;kunde;gebiet;flyer;netto;kartenlink;ordner;datei;status;notiz – Status: offen | beauftragt | verloren | storniert.
Vergabe/Pflege nur über `tools/angebotsnummer.py` (zieht/pusht selbst, damit parallele Sitzungen keine Nummer doppelt vergeben):
- neu: `python3 tools/angebotsnummer.py neu --kunde "<Kunde>" --gebiet "<Stadt>"` → gibt die Nummer aus
- Version: `python3 tools/angebotsnummer.py version --nr 2611-09`
- Werte nachtragen: `python3 tools/angebotsnummer.py setze --nr 2611-41 --netto 1.635,00 --flyer 15000 --kartenlink <URL> --datei <docx> --ordner "November\<Kunde>"`
- Nachfassen: `python3 tools/angebotsnummer.py offen --tage 5`
Einbau: `build_angebot.js` Config `"angebotsnummer": "2611-41"` (Deckblatt + Abschlussseite), `build_karte.py --angebotsnr 2611-41` (Sidebar + Betreff der Auftrags-E-Mail).
Dateiname ab 2611-42: `Angebot_<Nr>_<Kunde>_<Datum>_<Stadt>.docx`.
