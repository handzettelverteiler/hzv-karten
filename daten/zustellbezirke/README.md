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
| Düsseldorf (Altstadt/Stadtmitte/Friedrichstadt/Unterbilk/Pempelfort/Derendorf-Süd) | 40210, 40211, 40212, 40213, 40215, 40217, 40219, 40477, 40479 | 32 | 38.134 | 72.880 | 2026-11-25 | `duesseldorf.geojson` |
| Burgstädt + Umkreis 6 km (Mühlau, Hartmannsdorf, Taura, Claußnitz, Penig u. a., Nachbar-PLZ nur teilweise) | 09217 (+ 09228, 09232, 09236, 09241, 09247, 09249, 09306, 09322, 09328) | 22 | 13.380 | 16.942 | 2026-11-25 | `burgstaedt.geojson` |
| Ispringen + Umkreis 3 km (Pforzheim-West/Nord, Ersingen, Nachbar-PLZ nur teilweise) | 75228 (+ 75172, 75177, 75179, 75236) | 18 | 11.759 | 22.294 | 2026-11-25 | `ispringen.geojson` |
| Waren (Müritz) + Penzlin + Möllenhagen (ganze PLZ inkl. Ortsteile) | 17192, 17217, 17219 | 25 | 18.011 | 21.006 | 2026-11-26 | `moellenhagen_penzlin_waren.geojson` |
| Aying + Brunnthal + Egmating + Höhenkirchen-Siegertsbrunn (ganze PLZ) | 85635, 85649, 85653, 85658 | 18 | 7.248 | 12.814 | 2026-11-26 | `aying.geojson` |
| Wiesbaden (Innenstadt-Ring: Mitte, Nordost, Rheingauviertel, Südost, Westend, Klarenthal, Dichterviertel) | 65183, 65185, 65187, 65189, 65193, 65195, 65197 | 50 | 35.421 | 84.965 | 2026-11-26/27 | `wiesbaden.geojson` (27.11.: +65197-25) |
| Neckarsulm (ganze PLZ inkl. Amorbach, Obereisesheim, Dahenfeld) + Untereisesheim | 74172, 74257 | 20 | 11.663 | 16.210 | 2026-11-26 | `neckarsulm.geojson` |
| Leipzig (Zentrum, Zentrum-Ost/-Nord/-Süd/-West, Südvorstadt) | 04103, 04105, 04107, 04109, 04275 | 34 | 21.068 | 67.758 | 2026-11-26 | `leipzig.geojson` |
| Mönchengladbach (Gladbach-Mitte, Eicken/Westend, Ost/Lürrip) | 41061, 41063, 41065 | 23 | 32.313 | 44.186 | 2026-11-26 | `moenchengladbach.geojson` |
| Wuppertal (Elberfeld: Mitte, Nordstadt, Ostersbaum, Arrenberg/Zoo, Südstadt; Barmen: Mitte, Unterbarmen, Rott, Heckinghausen-West; Ränder 42109/42113/42277 nur teilweise) | 42103, 42105, 42107, 42115, 42117, 42119, 42275, 42281, 42283, 42285, 42287, 42289 (+ 42109, 42113, 42277 teilweise) | 69 | 81.936 | 115.324 | 2026-11-27 | `wuppertal.geojson` |
| Kassel (Mitte, Vorderer Westen, Wehlheiden/Südstadt, Nord-Holland, Wesertor/Fasanenhof; Ränder 34123/34128/34130 nur teilweise) | 34117, 34119, 34121, 34125, 34127 (+ 34123, 34128, 34130 teilweise) | 42 | 33.019 | 65.607 | 2026-11-27 | `kassel.geojson` |
| Paderborn (Innenstadt komplett; 33100/33102 nur Kernstadt ohne Ortsteile wie Dahl, Benhausen, Neuenbeken) + Hövelhof (ganze PLZ) | 33098, 33161 (+ 33100, 33102 teilweise) | 53 | 32.123 | 55.593 | 2026-11-27 | `paderborn_hoevelhof.geojson` |
| Höchberg + Randersacker (Hauptorte; Randbezirke/Lindelbach evtl. unter Würzburger Präfix) | 97204, 97236 | 9 | 3.311 | 5.889 | 2026-11-27 | `hoechberg_randersacker.geojson` |
| Salzgitter-Bad (inkl. Ortsteile Gitter, Hohenrode, Bad-Ost/-West, Ringelheim-Teile) | 38259 | 16 | 11.538 | 14.810 | 2026-11-27 | `salzgitter.geojson` |

**Stand:** Rangfolge nach Häufigkeit in `angebote_register.csv` + `anfragen_log.csv`: Berlin, Hamburg, München, Potsdam, Köln, Augsburg, …
Berlin/Hamburg/München sind zu groß für einen Lauf (Berlin ≈ 190 PLZ). Lauf 24.11.2026: jeweils die innerste Kernstadt (PLZ oben) vollständig.
Lauf 25.11.2026 abends: Potsdam, Köln (Innenstadt), Augsburg (Innenstadt). Lauf 25.11. (2): Düsseldorf, Burgstädt, Ispringen. Lauf 26.11.: Möllenhagen/Penzlin/Waren, Aying/Brunnthal/Egmating/Höhenkirchen, Wiesbaden (Kernstadt ohne 65191 Bierstadt/65199 Dotzheim). Lauf 26.11. (2): Neckarsulm, Leipzig (Innenstadt), Mönchengladbach (Gladbach-Mitte). Lauf 27.11.: Wiesbaden-Lücke (+65197-25), Wuppertal (Elberfeld + Barmen), Kassel (Kernstadt). Lauf 27.11. (2): Paderborn/Hövelhof, Höchberg/Randersacker, Salzgitter-Bad. Nächste Läufe: Höchberg/Randersacker, Salzgitter … sowie ringweise Ergänzung von Berlin/Hamburg/München/Köln/Augsburg.

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
| 40210 | Düsseldorf | 1 | 1195 | 3075 | -61.1 % | 2029 | 5286 | -61.6 % ⚠ |
| 40211 | Düsseldorf | 5 | 5117 | 4201 | +21.8 % | 11253 | 9883 | +13.9 % ⚠ |
| 40212 | Düsseldorf | 2 | 924 | 1035 | -10.7 % | 1740 | 1923 | -9.5 % ⚠ |
| 40213 | Düsseldorf | 4 | 2927 | 2133 | +37.2 % | 6708 | 5354 | +25.3 % ⚠ |
| 40215 | Düsseldorf | 5 | 7783 | 7504 | +3.7 % | 12704 | 11990 | +6.0 % ⚠ |
| 40217 | Düsseldorf | 2 | 2702 | 4113 | -34.3 % | 5117 | 7764 | -34.1 % ⚠ |
| 40219 | Düsseldorf | 5 | 6070 | 3929 | +54.5 % | 13378 | 8974 | +49.1 % ⚠ |
| 40477 | Düsseldorf | 4 | 6471 | 7651 | -15.4 % | 10729 | 13096 | -18.1 % ⚠ |
| 40479 | Düsseldorf | 4 | 4945 | 4357 | +13.5 % | 9222 | 7996 | +15.3 % ⚠ |
| 09217 | Burgstädt | 8 | 5502 | 5118 | +7.5 % | 7003 | 6506 | +7.6 % ⚠ |
| 75228 | Ispringen | 5 | 2654 | 2036 | +30.4 % | 4383 | 3276 | +33.8 % ⚠ |
| 17192 | Waren (Müritz) | 19 | 14290 | 14304 | -0.1 % | 16869 | 16876 | -0.0 % |
| 17217 | Penzlin | 4 | 2579 | 2493 | +3.4 % | 2887 | 2797 | +3.2 % |
| 17219 | Möllenhagen | 2 | 1142 | 1118 | +2.1 % | 1250 | 1224 | +2.1 % |
| 85635 | Höhenkirchen-Siegertsbrunn | 5 | 2544 | 2937 | -13.4 % | 4728 | 5573 | -15.2 % ⚠ |
| 85649 | Brunnthal | 6 | 2207 | 1814 | +21.7 % | 3696 | 2851 | +29.6 % ⚠ |
| 85653 | Aying | 5 | 1659 | 1742 | -4.8 % | 3119 | 3241 | -3.8 % |
| 85658 | Egmating | 2 | 838 | 827 | +1.3 % | 1271 | 1259 | +1.0 % |
| 65183 | Wiesbaden | 7 | 5529 | 5529 | +0.0 % | 11444 | 11444 | +0.0 % |
| 65185 | Wiesbaden | 6 | 4512 | 4205 | +7.3 % | 12392 | 11480 | +7.9 % ⚠ |
| 65187 | Wiesbaden | 5 | 3398 | 5975 | -43.1 % | 9193 | 13792 | -33.3 % ⚠ |
| 65189 | Wiesbaden | 7 | 4046 | 3147 | +28.6 % | 11829 | 10037 | +17.9 % ⚠ |
| 65193 | Wiesbaden | 11 | 3526 | 3526 | +0.0 % | 10188 | 10188 | +0.0 % |
| 65195 | Wiesbaden | 6 | 5215 | 5065 | +3.0 % | 11673 | 11383 | +2.5 % |
| 65197 | Wiesbaden | 8 | 9195 | 9447 | -2.7 % | 18246 | 18936 | -3.6 % |
| 74172 | Neckarsulm | 17 | 10036 | 10163 | -1.2 % | 14143 | 14389 | -1.7 % |
| 74257 | Untereisesheim | 3 | 1627 | 1627 | +0.0 % | 2067 | 2067 | +0.0 % |
| 04103 | Leipzig | 6 | 5129 | 5037 | +1.8 % | 15788 | 15705 | +0.5 % |
| 04105 | Leipzig | 6 | 4211 | 4259 | -1.1 % | 13317 | 13190 | +1.0 % |
| 04107 | Leipzig | 4 | 3804 | 3975 | -4.3 % | 10392 | 10960 | -5.2 % ⚠ |
| 04109 | Leipzig | 10 | 3160 | 3014 | +4.8 % | 11946 | 11504 | +3.8 % |
| 04275 | Leipzig | 8 | 4764 | 4383 | +8.7 % | 16315 | 15538 | +5.0 % ⚠ |
| 41061 | Mönchengladbach | 6 | 8823 | 11753 | -24.9 % | 12775 | 16937 | -24.6 % ⚠ |
| 41063 | Mönchengladbach | 8 | 10078 | 9018 | +11.8 % | 14110 | 12375 | +14.0 % ⚠ |
| 41065 | Mönchengladbach | 9 | 13412 | 12816 | +4.7 % | 17301 | 16364 | +5.7 % ⚠ |
| 42103 | Wuppertal | 3 | 3468 | 3649 | -5.0 % | 6214 | 6271 | -0.9 % |
| 42105 | Wuppertal | 5 | 6352 | 7057 | -10.0 % | 10363 | 11492 | -9.8 % ⚠ |
| 42107 | Wuppertal | 4 | 5626 | 4740 | +18.7 % | 9940 | 8754 | +13.5 % ⚠ |
| 42109 | Wuppertal (teilw.) | 3 | 2386 | 6297 | -62.1 % | 3239 | 8220 | -60.6 % ⚠ |
| 42113 | Wuppertal (teilw.) | 1 | 734 | 4385 | -83.3 % | 943 | 6310 | -85.1 % ⚠ |
| 42115 | Wuppertal | 8 | 5984 | 6769 | -11.6 % | 7826 | 8640 | -9.4 % ⚠ |
| 42117 | Wuppertal | 7 | 5816 | 5716 | +1.7 % | 8348 | 8329 | +0.2 % |
| 42119 | Wuppertal | 6 | 8168 | 8962 | -8.9 % | 11933 | 13216 | -9.7 % ⚠ |
| 42275 | Wuppertal | 4 | 6758 | 6359 | +6.3 % | 8397 | 8006 | +4.9 % |
| 42277 | Wuppertal (teilw.) | 4 | 6365 | 11688 | -45.5 % | 7515 | 13608 | -44.8 % ⚠ |
| 42281 | Wuppertal | 5 | 6460 | 6543 | -1.3 % | 7940 | 8068 | -1.6 % |
| 42283 | Wuppertal | 4 | 6056 | 7602 | -20.3 % | 8329 | 10296 | -19.1 % ⚠ |
| 42285 | Wuppertal | 6 | 6710 | 5176 | +29.6 % | 10044 | 8142 | +23.4 % ⚠ |
| 42287 | Wuppertal | 3 | 3660 | 4930 | -25.8 % | 5232 | 7054 | -25.8 % ⚠ |
| 42289 | Wuppertal | 6 | 7393 | 9457 | -21.8 % | 9061 | 11642 | -22.2 % ⚠ |
| 34117 | Kassel | 6 | 3327 | 3694 | -9.9 % | 9341 | 9800 | -4.7 % |
| 34119 | Kassel | 6 | 4511 | 4725 | -4.5 % | 10113 | 10693 | -5.4 % ⚠ |
| 34121 | Kassel | 13 | 6263 | 6263 | +0.0 % | 13538 | 13538 | +0.0 % |
| 34123 | Kassel (teilw.) | 1 | 1113 | 8708 | -87.2 % | 2033 | 13838 | -85.3 % ⚠ |
| 34125 | Kassel | 7 | 7790 | 9742 | -20.0 % | 13875 | 16189 | -14.3 % ⚠ |
| 34127 | Kassel | 6 | 7218 | 8543 | -15.5 % | 11713 | 13823 | -15.3 % ⚠ |
| 34128 | Kassel (teilw.) | 1 | 1152 | 6619 | -82.6 % | 1671 | 10451 | -84.0 % ⚠ |
| 34130 | Kassel (teilw.) | 2 | 1645 | 2749 | -40.2 % | 3323 | 5614 | -40.8 % ⚠ |
| 33098 | Paderborn | 12 | 8824 | 8898 | -0.8 % | 18418 | 18436 | -0.1 % |
| 33100 | Paderborn (Kernstadt-Teil) | 14 | 7402 | 11843 | -37.5 % | 12030 | 18195 | -33.9 % ⚠ |
| 33102 | Paderborn (Kernstadt-Teil) | 15 | 9743 | 13894 | -29.9 % | 16845 | 23070 | -27.0 % ⚠ |
| 33161 | Hövelhof | 12 | 6154 | 6139 | +0.2 % | 8300 | 8351 | -0.6 % |
| 97204 | Höchberg | 7 | 2379 | 3112 | -23.6 % | 4128 | 5361 | -23.0 % ⚠ |
| 97236 | Randersacker | 2 | 932 | 1215 | -23.3 % | 1761 | 2134 | -17.5 % ⚠ |
| 38259 | Salzgitter-Bad | 16 | 11538 | 11995 | -3.8 % | 14810 | 15442 | -4.1 % |

Lauf 25.11. (2): Düsseldorf (9 PLZ) summiert 72.880 HH ges. vs. Vorrat 72.266 (+0,8 %) – PLZ-Abweichungen wieder durch die
Stützpunkt-Nummerierung. Vorratswerte 09217/75228 aus den Projekt-Nachträgen (19.11./23.11.); 75228-Bezirke reichen in
Pforzheimer Randlagen hinein (+34 %), 09217 enthält Ortsteile (+8 %). 09247-46 hat 0 bewerbbare HH. Beim Dekodieren wurden
degenerierte Mini-Ringe (3 Punkte) verworfen (40215-32, 40217-15).

Lauf 26.11.: Vorratswerte 17192/17217/17219 aus dem Projekt-Nachtrag 25.11., 85635/85649/85653/85658 aus dem Nachtrag 17.11.
Waren/Penzlin/Möllenhagen passt über die 3 PLZ auf +0,5 % (HH ges.), Aying-Gruppe über die 4 PLZ auf -0,9 % – Einzel-PLZ-Abweichungen
(85635 vs. 85649) wieder durch die Stützpunkt-Nummerierung. Nicht gespeichert: Nachbar-Bezirke anderer PLZ (u. a. 17194-19, 83626-22,
85625-35, Ottobrunn 85521, Biebrich 65203, 65191, 65199). **Wiesbaden ist noch nicht vollständig:** über die 7 PLZ -4,8 % (83.058 vs. 87.260
HH ges.); vermutlich fehlen Bezirke am Rand von 65187 (Nummern 65187-41…45?) und 65197 (65197-32…36?). Weitere Abfragen scheiterten an
nicht gefundenen Adressen (Dotzheimer Str. 150, Hollerbornstr. 10, Graf-von-Galen-Str. 30, Akazienstr. 1) bzw. lieferten keine neuen Bezirke
(Schiersteiner Str. 50) – im nächsten Lauf mit anderen Mittelpunkten ergänzen. Straßenlisten in diesen drei Dateien als JSON-Liste.

Lauf 26.11. (2): Neckarsulm über beide PLZ -1,5 % (vermutlich fehlt nur Bezirk 74172-01), Leipzig über die 5 PLZ +1,3 %,
Mönchengladbach über die 3 PLZ -3,3 % (41061 hat nur 6 Bezirke mit eigenem Präfix; Teile von 41061 laufen vermutlich unter 41068/41069,
die nicht gespeichert sind). Vorratswerte 74172 aus dem Nachtrag 02.11., 74257 aus dem Nachtrag 11.11.

Lauf 27.11.: **Wiesbaden** um 65197-25 (Schelmengraben-Rand, 1.907 HH ges.) ergänzt → 65197 jetzt -3,6 %, die 7 PLZ zusammen 84.965 vs. 87.260
(-2,6 %). Bezirke 65187-41…45 gibt es nicht: Um Gabelsbornstr. liefert das Portal nur 65187-46…50. Die 65187-Lücke (-4.600 HH ges.) liegt vermutlich in
den Grenzbezirken 65199-62 (Gräselberg: Am Gräselberg, Kärntner Str., Klagenfurter Ring) und 65203-45 (Waldstr./Erich-Ollenhauer-Str./Biebricher Allee),
die nach Stützpunkt-Präfix zu Dotzheim/Biebrich zählen – nicht gespeichert (Präfix-Regel wie bisher); bei Bedarf in einem Lauf ergänzen.
**Wuppertal:** Elberfeld (42103/05/07/15/17/19) zusammen 54.624 vs. Vorrat 56.702 HH ges. (-3,7 %), Barmen (42275/81/83/85/87/89) 49.003 vs. 53.208
(-7,9 %; Ränder Richtung Heckinghausen/Lichtscheid fehlen noch, 42285 enthält Stützpunkt-Bezirke von 42287). 42103+42105+42107 zusammen exakt wie Vorrat
(26.517). Abfragepunkte: Herzogstr. 10, Johannes-Rau-Platz 1, Friedrich-Ebert-Str. 150 (42117), Hünefeldstr. 20 (je 2 km); „Kothener Straße 50“ wurde
nicht gefunden. **Kassel:** 34117+34119+34121 zusammen 32.992 vs. 34.031 (-3,1 %; 34121 exakt), 34125/34127 zu ~85 %. Abfragepunkte: Obere Königsstr. 8,
Friedrich-Ebert-Str. 100 (34119), Holländische Str. 50 (je 2 km, je ~20 s). Vorratswerte vom 06.11.

Lauf 27.11. (2): **Paderborn** 33098 (Innenstadt) vollständig (-0,1 %), Hövelhof 33161 vollständig (-0,6 %, 5 km um Schloßstr. 14). 33100/33102 nur die
Kernstadt-Bezirke (Abfragen Marienplatz 1, Driburger Str. 50, Riemekestr. 100, je 2 km); es fehlen die äußeren Ortsteile (33100: Dahl, Benhausen,
Neuenbeken u. a.; 33102: Rand Richtung Elsen/Wewer) – daher -27 bis -34 %. Nicht gespeichert: 33129 Delbrück (2 Bezirke). **Höchberg** 97204 -23 %
(7 Bezirke, 3 km um Hauptstr. 58) und **Randersacker** 97236 -17,5 % (2 Bezirke, 3 km um Maingasse 9; Lindelbach fehlt vermutlich): die fehlenden
Haushalte liegen wohl in Bezirken mit Würzburger Präfix (97082/97084/97074, nicht gespeichert). **Salzgitter-Bad** 38259 -4,1 % (16 Bezirke, 3 km + 6 km um
Kniestedter Str.). Nicht gespeichert: 38229, 38275, 38704, 97218, 97297. Vorratswerte 06.11. bzw. 97204/97236 aus dem Nachtrag 16.11.

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

## Hinweise zur Abfrage (Lauf 26.11.2026)

- Radius 10 km liefert „Für Ihre Suche wurden keine Ergebnisse gefunden“; 8 km geht auf dem Land (~10 s). Die Fehlermeldung kommt auch, wenn die
  Adresse nicht gefunden wird (z. B. „Markt 1, 17217 Penzlin“ statt „Am Markt“, „Schlossplatz“ statt „Schloßplatz“ in Wiesbaden).
  Zuverlässig: eine Straße aus der Straßenliste eines schon geholten Bezirks als Mittelpunkt nehmen (so Möllenhagen über „Rumpshagener Weg“/„Kraaser Str.“).
- `get_page_text` macht aus Tabs Leerzeichen → Felder im `<pre>` mit „ ¦ “ trennen, Ringe mit Leerzeichen (kommt in Polylines nicht vor).
- **Portal-Sperre nach einigen Abfragen je Seitensitzung** (Lauf 26.11. (2) bestätigt): Nach ca. 5–10 Abfragen kommt auch für bekannte
  Adressen nur noch „keine Ergebnisse“. Seite neu laden und Zustellbezirke-Reiter wieder öffnen, dann geht es weiter (vermutlich auch der Grund
  für die Wiesbaden-Lücke). Die Hilfsfunktionen liegen als Code in `localStorage.__hzv` der Portal-Seite → nach dem Neuladen `eval(localStorage.__hzv)`.
- Hausnummer muss es geben: Übernimmt das Portal die Adresse ohne Nummer ins Feld (z. B. „Lürriper Straße“), wurde sie nicht gefunden → andere Nummer.

## Hinweise zur Abfrage (Lauf 27.11.2026)

- Hilfsfunktionen aus `localStorage.__hzv` (`__Q(street, plz, km)`, `__col()`, `__show(text)`) funktionierten unverändert; `__B` nach dem Neuladen aus
  `localStorage.__hzvB` wiederherstellen (Duplikate werden übersprungen). Vorbeugend nach 3–4 Abfragen gespeichert und neu geladen – keine Sperre aufgetreten.
- In Wuppertal sind Bezirke groß (~2.000 HH): 2 km liefert nur ~25–30 Bezirke, deshalb mehrere Mittelpunkte.
