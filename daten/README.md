# Haushalts-Vorrat (POSTAKTUELL Manager)

`haushalte_plz_vorrat.csv` – bewerbbare Haushalte für alle PLZ der ~216 Städte (Top 200 + Kleinstädte), abgefragt am 2026-11-06.
Format wie `claude/haushalte_plz.csv` im Projekt: `plz;ort;hh_bewerbbar_post;hh_gerundet_50;abgefragt_am;quelle;hh_gesamt_post`.

Reihenfolge beim Nachschlagen: neueste Nachtragsdatei im Projekt > dieser Vorrat > `claude/haushalte_plz.csv`.
Werte älter als ~6 Monate vor Angebotsversand neu abfragen.

Lücken: 60306 Frankfurt (Portal hängt bei der Abfrage), Lahr/Schwarzwald 77933 (fehlt, im Lauf wurde das Eifeldorf 54675 erwischt).
