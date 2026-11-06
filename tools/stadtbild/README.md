# HZV Stadtbilder (Stil v3, ab 06.11.2026)

Jedes Stadtbild: Stadtsilhouette mit typischen Wahrzeichen + blaues Strichmännchen (Basecap leicht schräg) an einer
Briefkastenanlage mit 2 „Keine Werbung“-Kästen.
- `staedte/Stadt_<Slug>.jpg` = Angebot Seite 3 (Einwurf „Ihr Flyer“, Sprechblase „Keine Werbung? Kein Einwurf.“)
- `staedte/Stadt_<Slug>_Lupe.jpg` = Angebot Seite 4 (Lupe über „Keine Werbung“, Sprechblase „Wird respektiert!“)
- `staedte/index.json` ordnet normalisierte Ortsnamen (klein, ä→ae, nur a–z/0–9) dem Slug zu.

## Neuen Ort anlegen (dauert ca. 2 Minuten)
1. Wahrzeichen des Orts kurz recherchieren (Kirche, Rathaus, Burg, Tor, Weinberg, Förderturm, Hafen …).
2. In `orte_klein.py` eine Zeile ergänzen, z. B.
   `reg("Deidesheim", ["Deidesheim"], lambda: basis(201) + weinberg(0, 380, 150) + freitreppen_rathaus(420) + kirche(680, 180, 130, SAND, SLATE, "spire"))`
   Bausteine stehen in `elemente.py` (kirche, dom, rathaus, schloss, burg, tor, turm, wasserturm, hochhaus, foerderturm,
   fachwerk, kurhaus, denkmal, muehle, gradierwerk, kran, bruecke_haeuser, weinberg, leuchtturm, windrad, kuehlturm …).
   Landmarken zwischen x=20 und x≈930 platzieren (rechts davon stehen Briefkastenanlage und Figur).
3. `cd tools/stadtbild && python3 orte_klein.py <Slug>` → Bilder unter `out/final/`, nach `staedte/` kopieren,
   Namen in `staedte/index.json` eintragen, committen, pushen.

Vorlage `base_alt/Stadt_Allgemein*.jpg` = alter Stand (Stil v2) – wird nur für Fluss/Wiese unten links genutzt.
Bestehende Städte mit neuer Figur versehen: `python3 final.py <Slug> ...` (Basis = `staedte/Stadt_<Slug>.jpg` im alten Stil v2).
