# Zustellbezirke der Deutschen Post (POSTAKTUELL)

Echte Zustellbezirks-Grenzen + Haushalte je Bezirk, damit Karten und Preistabellen in Angeboten exakt statt angenähert sind.
Quelle: POSTAKTUELL Manager, Reiter „Zustellbezirke“ (Umkreisselektion), per Claude in Chrome aus `map.getFeatures()`
(EPSG:3857 → lon/lat, Douglas-Peucker 0,0002°, Polyline 1e-4). Nichts abgesendet, keine Kundennummer.

Format je Datei: GeoJSON-FeatureCollection, ein Feature (MultiPolygon) je Bezirk; properties `bezirk`, `plz`,
`hh_bewerbbar`, `hh_ohne_werbung`, `hh_gesamt`, `strassen` (Liste wie bei der Post; „*“ = Straße nur teilweise im Bezirk),
`abgefragt_am`. Nur Außenringe gespeichert (Löcher weggelassen).

## Städte

| Stadt (Teil) | PLZ | Bezirke | Summe HH bewerbbar | Summe HH gesamt | Datum | Datei |
|---|---|---|---|---|---|---|
| Berlin (Mitte) | 10115, 10117, 10119, 10178, 10179 | 41 | 23.765 | 79.463 | 2026-11-24 | `berlin.geojson` |
| Hamburg (Altstadt/Neustadt/St. Georg/HafenCity/Hammerbrook) | 20095, 20097, 20099, 20354, 20355, 20457, 20459 | 33 | 10.991 | 38.844 | 2026-11-24 | `hamburg.geojson` |
| München (Altstadt/Maxvorstadt/Isarvorstadt/Lehel) | 80331, 80333, 80335, 80469, 80538, 80539 | 39 | 14.463 | 57.242 | 2026-11-24 | `muenchen.geojson` |

**Stand:** Rangfolge nach Häufigkeit in `angebote_register.csv` + `anfragen_log.csv`: Berlin, Hamburg, München, Potsdam, Köln, Augsburg, …
Berlin/Hamburg/München sind zu groß für einen Lauf (Berlin ≈ 190 PLZ). Lauf 24.11.2026: jeweils die innerste Kernstadt (PLZ oben) vollständig.
Nächste Läufe: weitere Kernstadt-PLZ dieser drei Städte ringweise ergänzen (an die Datei anhängen), danach Potsdam, Köln, Augsburg.

## Abgleich mit Haushalts-Vorrat (`daten/haushalte_plz_vorrat.csv`, Stand 06.11.2026)

Eine PLZ gilt als vollständig, wenn zusätzliche Abfragepunkte am Rand keine neuen Bezirke dieser PLZ mehr liefern.
⚠ = Abweichung HH gesamt ≥ 5 % (Vorrat-Werte sind PLZ-Summen der Post vom 06.11., Bezirkswerte vom 24.11.; Grenzbezirke an PLZ-Rändern können der Nachbar-PLZ zugeordnet sein).

| PLZ | Stadt | Bezirke | HH bew. Bezirke | HH bew. Vorrat | Abw. | HH ges. Bezirke | HH ges. Vorrat | Abw. |
|---|---|---|---|---|---|---|---|---|
| 10115 | Berlin | 9 | 5644 | 5501 | +2.6 % | 19560 | 19157 | +2.1 % |
| 10117 | Berlin | 10 | 3937 | 4190 | -6.0 % | 14704 | 15499 | -5.1 % ⚠ |
| 10119 | Berlin | 7 | 4156 | 4233 | -1.8 % | 14440 | 14456 | -0.1 % |
| 10178 | Berlin | 6 | 3878 | 4031 | -3.8 % | 11119 | 11277 | -1.4 % |
| 10179 | Berlin | 9 | 6150 | 5810 | +5.9 % | 19640 | 19074 | +3.0 % |
| 20095 | Hamburg | 4 | 1196 | 1208 | -1.0 % | 2631 | 2650 | -0.7 % |
| 20097 | Hamburg | 6 | 1547 | 1517 | +2.0 % | 6700 | 6604 | +1.5 % |
| 20099 | Hamburg | 5 | 2146 | 2146 | +0.0 % | 7992 | 7992 | +0.0 % |
| 20354 | Hamburg | 4 | 1204 | 1244 | -3.2 % | 2850 | 2964 | -3.8 % |
| 20355 | Hamburg | 3 | 954 | 1073 | -11.1 % | 3268 | 3638 | -10.2 % ⚠ |
| 20457 | Hamburg | 7 | 2037 | 2068 | -1.5 % | 9041 | 9768 | -7.4 % ⚠ |
| 20459 | Hamburg | 4 | 1907 | 1742 | +9.5 % | 6362 | 5851 | +8.7 % ⚠ |
| 80331 | München | 7 | 2352 | 2069 | +13.7 % | 7284 | 6783 | +7.4 % ⚠ |
| 80333 | München | 8 | 3067 | 3431 | -10.6 % | 10252 | 11191 | -8.4 % ⚠ |
| 80335 | München | 6 | 2815 | 2998 | -6.1 % | 8666 | 8778 | -1.3 % |
| 80469 | München | 10 | 3793 | 3708 | +2.3 % | 19496 | 19404 | +0.5 % |
| 80538 | München | 6 | 2053 | 2152 | -4.6 % | 8852 | 8846 | +0.1 % |
| 80539 | München | 2 | 383 | 404 | -5.2 % | 2692 | 3048 | -11.7 % ⚠ |

## Hinweise zur Abfrage (Lauf 24.11.2026)

- Radius-Schieber geht bis 10 km, aber in Großstädten hängt die Abfrage ab 3 km (Spinner > 2 min, keine Daten). 2 km dauert ~30 s
  (~50–65 Bezirke), 1 km ~5–10 s. Vorgehen: 2 km um den Mittelpunkt, dann 1-km-Abfragen an den Rändern unvollständiger PLZ.
- Radius per JS setzen: `$('#sliderRadius').slider('value',km)` + `#amountRadius` = „<km> km“; Abfragen-Link klicken.
- Engpass ist nicht die Post, sondern die Übertragung per Seitentext (~250–300 Zeichen je Bezirk inkl. Straßenliste) –
  daher pro Lauf ca. 100–120 Bezirke.
