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
| Saarbrücken (Mitte) | 66111, 66113, 66121 | 22 | 21.182 | 38.327 | 2026-11-25 | `saarbruecken.geojson` (Zeile am 25.11. abends nachgetragen) |
| Potsdam (ganze Stadt ohne Nordortsteile 14476) | 14467, 14469, 14471, 14473, 14478, 14480, 14482 | 58 | 58.759 | 105.415 | 2026-11-25 | `potsdam.geojson` |
| Köln (Innenstadt + Deutz) | 50667, 50668, 50670, 50672, 50674, 50676, 50677, 50678, 50679 | 45 | 47.340 | 105.199 | 2026-11-25 | `koeln.geojson` |
| Augsburg (Innenstadt) | 86150, 86152, 86153 | 20 | 11.564 | 38.948 | 2026-11-25 | `augsburg.geojson` |

**Stand:** Rangfolge nach Häufigkeit in `angebote_register.csv` + `anfragen_log.csv`: Berlin, Hamburg, München, Potsdam, Köln, Augsburg, …
Berlin/Hamburg/München sind zu groß für einen Lauf (Berlin ≈ 190 PLZ). Lauf 24.11.2026: jeweils die innerste Kernstadt (PLZ oben) vollständig.
Lauf 25.11.2026 abends: Potsdam, Köln (Innenstadt), Augsburg (Innenstadt). Nächste Läufe: Düsseldorf, Burgstädt, Ispringen, Möllenhagen/Penzlin/Waren, Aying … sowie ringweise Ergänzung von Berlin/Hamburg/München/Köln/Augsburg.

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
| 14467 | Potsdam | 5 | 4013 | 5110 | -21.5 % | 9521 | 12487 | -23.8 % ⚠ |
| 14469 | Potsdam | 17 | 13219 | 11433 | +15.6 % | 24410 | 20522 | +18.9 % ⚠ |
| 14471 | Potsdam | 4 | 4912 | 6539 | -24.9 % | 9006 | 11557 | -22.1 % ⚠ |
| 14473 | Potsdam | 5 | 6397 | 5421 | +18.0 % | 11677 | 10005 | +16.7 % ⚠ |
| 14478 | Potsdam | 8 | 11075 | 11075 | +0.0 % | 16874 | 16874 | +0.0 % |
| 14480 | Potsdam | 9 | 10991 | 11293 | -2.7 % | 16764 | 17275 | -3.0 % |
| 14482 | Potsdam | 10 | 8152 | 7850 | +3.8 % | 17163 | 16652 | +3.1 % |
| 50667 | Köln | 5 | 3347 | 2265 | +47.8 % | 7762 | 5521 | +40.6 % ⚠ |
| 50668 | Köln | 4 | 3686 | 4743 | -22.3 % | 8278 | 10388 | -20.3 % ⚠ |
| 50670 | Köln | 7 | 6863 | 5894 | +16.4 % | 16303 | 14427 | +13.0 % ⚠ |
| 50672 | Köln | 4 | 3048 | 2971 | +2.6 % | 9616 | 9224 | +4.2 % |
| 50674 | Köln | 6 | 8724 | 8801 | -0.9 % | 15724 | 16116 | -2.4 % |
| 50676 | Köln | 4 | 4687 | 5769 | -18.8 % | 11262 | 13503 | -16.6 % ⚠ |
| 50677 | Köln | 6 | 7207 | 4626 | +55.8 % | 15067 | 9658 | +56.0 % ⚠ |
| 50678 | Köln | 4 | 5127 | 7015 | -26.9 % | 9771 | 13164 | -25.8 % ⚠ |
| 50679 | Köln | 5 | 4651 | 4563 | +1.9 % | 11416 | 11181 | +2.1 % |
| 86150 | Augsburg | 7 | 3724 | 3537 | +5.3 % | 13159 | 12708 | +3.5 % |
| 86152 | Augsburg | 5 | 2984 | 3846 | -22.4 % | 10204 | 12532 | -18.6 % ⚠ |
| 86153 | Augsburg | 8 | 4856 | 4298 | +13.0 % | 15585 | 13623 | +14.4 % ⚠ |

**Wichtig (Lauf 25.11.):** Das PLZ-Präfix im Bezirksnamen (z. B. 50677-05) ist die Nummerierung des Zustellstützpunkts und deckt sich
nicht immer mit der PLZ der Straßen im Bezirk (50677-05 enthält z. B. Severinstr./Chlodwigplatz = 50678). Deshalb die großen Abweichungen
je PLZ – über die ganze Stadt summiert passt es: Potsdam (7 PLZ) 105.415 HH ges. vs. Vorrat 105.372 (+0,04 %), Köln Innenstadt (9 PLZ)
105.199 vs. 103.182 (+2,0 %), Augsburg (3 PLZ) 38.948 vs. 38.863 (+0,2 %). Für Angebote je PLZ weiter den Vorrat nutzen; die Bezirke
für Karten, Teilgebiete und Umkreis-Angebote. 86153-99 (Willy-Brandt-Platz) hat 0 bewerbbare HH.

## Hinweise zur Abfrage (Lauf 24.11.2026)

- Radius-Schieber geht bis 10 km, aber in Großstädten hängt die Abfrage ab 3 km (Spinner > 2 min, keine Daten). 2 km dauert ~30 s
  (~50–65 Bezirke), 1 km ~5–10 s. Vorgehen: 2 km um den Mittelpunkt, dann 1-km-Abfragen an den Rändern unvollständiger PLZ.
- Radius per JS setzen: `$('#sliderRadius').slider('value',km)` + `#amountRadius` = „<km> km“; Abfragen-Link klicken.
- Engpass ist nicht die Post, sondern die Übertragung per Seitentext (~250–300 Zeichen je Bezirk inkl. Straßenliste) –
  daher pro Lauf ca. 100–120 Bezirke.

## Hinweise zur Abfrage (Lauf 25.11.2026)

- Felder per JS setzbar: `#searchStreet`, `#searchPlz` (= „<PLZ> <Ort>“), `#spnGewicht` 20, `$('#submissionDate').datepicker('setDate','09.12.2026')`,
  Radius über `$('#sliderRadius').slider('value',km)`; `#btnQuery` per `setTimeout` klicken und mit `computer wait` warten
  (ein `await` im javascript_tool friert ein). `ol` ist nicht global → EPSG:3857 per Formel umrechnen.
- Potsdam: 4 km um Rathaus bzw. Konrad-Wolf-Allee liefen ohne Hänger (je ~35 s). Köln/Augsburg: 2 km ~30 s, danach 1-km-Randabfragen ohne neue Bezirke.
- Seitentext: Body-Kinder vorübergehend aus dem DOM nehmen und nur ein `<pre>` zeigen, sonst liest get_page_text ein verstecktes Formular.
