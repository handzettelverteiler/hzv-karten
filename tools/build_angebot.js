/**
 * HZV Angebot Generator (v4 – 8 Seiten, Stadtbild + Lupen-Variante automatisch, Config-basiert)
 * Baut das Angebots-docx nach den festen HZV-Standards für einen beliebigen Kunden.
 *
 * Aufruf:
 *   node build_angebot.js --config config.json --output Angebot_Kunde.docx
 *
 * Config-Format: siehe references/config-beispiel.json
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, PageOrientation,
  Header, Footer, VerticalAlign, UnderlineType,
} = require("docx");
const { execFileSync } = require("child_process");

// ---- CLI-Argumente ----
const args = process.argv.slice(2);
function getArg(name, fallback) {
  const i = args.indexOf(`--${name}`);
  return i !== -1 ? args[i + 1] : fallback;
}
const configPath = getArg("config");
if (!configPath) {
  console.error("Nutzung: node build_angebot.js --config config.json --output Angebot_Kunde.docx");
  process.exit(1);
}
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
const configDir = path.dirname(path.resolve(configPath));
const ASSETS = process.env.HZV_ASSETS || path.join(__dirname, "..", "assets");

function resolvePath(p) {
  if (!p) return null;
  return path.isAbsolute(p) ? p : path.join(configDir, p);
}

const RED = "C81E1E";
const GREEN_BG = "C6EFCE";
const GREY = "888888";
const FONT = "Arial";
const SIZE = 24; // 12pt

// ---- Bilddaten laden ----
const img = (p) => fs.readFileSync(p);
const logo = img(path.join(ASSETS, "logo_wortmarke.png"));
const headerBanner = img(path.join(ASSETS, "header_banner.png"));
const footerImg = img(path.join(ASSETS, "footer_4figuren.png"));
const iconPreis = img(path.join(ASSETS, "icon_preisuebersicht.png"));
const iconBuchen = img(path.join(ASSETS, "icon_jetzt_buchen.png"));
const whatsappQr = img(path.join(ASSETS, "whatsapp_qr.png"));
const flyerdruckIllustration = img(path.join(ASSETS, "flyerdruck_illustration.png"));

// Bildtyp + Abmessungen aus PNG/JPEG-Header (imgType / fit)
function imgType(p) { return /\.jpe?g$/i.test(p) ? "jpg" : "png"; }
function imgSize(buf) {
  if (buf[0] === 0x89 && buf[1] === 0x50) return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  let i = 2;
  while (i < buf.length) {
    if (buf[i] !== 0xFF) { i++; continue; }
    const m = buf[i + 1], len = buf.readUInt16BE(i + 2);
    if (m >= 0xC0 && m <= 0xCF && m !== 0xC4 && m !== 0xC8 && m !== 0xCC) return { w: buf.readUInt16BE(i + 7), h: buf.readUInt16BE(i + 5) };
    i += 2 + len;
  }
  return { w: 4, h: 3 };
}
function fit(buf, maxW, maxH) {
  const { w, h } = imgSize(buf); const sc = Math.min(maxW / w, maxH / h);
  return { width: Math.round(w * sc), height: Math.round(h * sc) };
}

// Kundenspezifisch, aus Config
const mapImagePath = resolvePath(config.map_image);
if (!mapImagePath || !fs.existsSync(mapImagePath)) {
  console.error(
    "FEHLER: config.map_image fehlt oder Datei nicht gefunden.\n" +
    "Der Karten-Screenshot kann NICHT automatisch erzeugt werden (bewusste Sicherheitssperre\n" +
    "im Browser-Tool verhindert das Zurückholen von Bilddaten). Stefan muss die Karte live\n" +
    "öffnen (nach Upload auf auslagenverteiler.de) und EINEN Screenshot davon liefern."
  );
  process.exit(1);
}
const mapImage = img(mapImagePath);
const beispielPath = resolvePath(config.beispiel_plz_map_image);
if (!beispielPath || !fs.existsSync(beispielPath)) {
  console.error("FEHLER: config.beispiel_plz_map_image fehlt oder Datei nicht gefunden (blauer Einzel-PLZ-Screenshot ist Pflicht).");
  process.exit(1);
}
const beispielImage = img(beispielPath);

// ---- Stadtbilder (v4): Seite 3 = Stadtbild, Seite 4 = Lupen-Variante ----
// Reihenfolge (Stefan, 04.10.2026: neue Zeichnung zuerst): config.stadt_illustration > staedte/index.json (neue Zeichnungen) >
// staedte/eigene/Stadt_<Stadt>.jpg (Stefans Bilder im Repo) > Skill-Assets staedte_logos/Stadt_<Stadt>.jpg >
// staedte/Stadt_Allgemein.jpg > Stadt_Ormesheim_Mandelbachtal.jpg
const STAEDTE = process.env.HZV_STAEDTE || path.join(__dirname, "..", "staedte");
function normName(s) {
  return String(s || "").toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9]/g, "");
}
function asciiFile(s) {
  return String(s || "").replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/Ä/g, "Ae").replace(/Ö/g, "Oe").replace(/Ü/g, "Ue").replace(/ß/g, "ss").replace(/[^A-Za-z0-9]+/g, "_");
}
function findStadtbild(name) {
  const idxPath = path.join(STAEDTE, "index.json");
  if (fs.existsSync(idxPath)) {
    const idx = JSON.parse(fs.readFileSync(idxPath, "utf8"));
    const n = normName(name);
    const slug = idx.staedte[n] || idx.staedte[normName(String(name).split(/ am | an der | im | \(|-/)[0])];
    if (slug && fs.existsSync(path.join(STAEDTE, `Stadt_${slug}.jpg`))) return path.join(STAEDTE, `Stadt_${slug}.jpg`);
  }
  // Stefans eigene Bilder: zuerst im Repo (staedte/eigene/, dauerhaft nachgeliefert), dann in den Skill-Assets
  for (const dir of [path.join(STAEDTE, "eigene"), path.join(ASSETS, "staedte_logos")]) {
    for (const ext of ["jpg", "png"]) {
      const cand = path.join(dir, `Stadt_${asciiFile(name)}.${ext}`);
      if (fs.existsSync(cand)) return cand;
    }
  }
  const allg = path.join(STAEDTE, "Stadt_Allgemein.jpg");
  if (fs.existsSync(allg)) return allg;
  const orm = path.join(ASSETS, "staedte_logos", "Stadt_Ormesheim_Mandelbachtal.jpg");
  return fs.existsSync(orm) ? orm : null;
}
let stadtIllustrationPath = resolvePath(config.stadt_illustration);
if (!stadtIllustrationPath || !fs.existsSync(stadtIllustrationPath)) stadtIllustrationPath = findStadtbild(config.stadt);
const stadtIllustration = stadtIllustrationPath ? img(stadtIllustrationPath) : null;
// Lupen-Variante für die Beispiel-PLZ-Seite: explizit, sonst <Stadtbild>_Lupe.<ext>, sonst dasselbe Bild
let stadtLupePath = resolvePath(config.stadt_illustration_lupe);
if ((!stadtLupePath || !fs.existsSync(stadtLupePath)) && stadtIllustrationPath) {
  const cand = stadtIllustrationPath.replace(/(\.[a-z]+)$/i, "_Lupe$1");
  stadtLupePath = fs.existsSync(cand) ? cand : stadtIllustrationPath;
}
const stadtLupe = stadtLupePath ? img(stadtLupePath) : null;
console.log(`Stadtbild Seite 3: ${stadtIllustrationPath || "-"}\nStadtbild Seite 4: ${stadtLupePath || "-"}`);

// ---- Kundendaten ----
const kunde = config.kunde; // { name, strasse, ort }
const stadt = config.stadt; // z.B. "Neuötting" - für Textbausteine
// "flyerdruck": false -> Kunde liefert die Flyer selbst: keine Flyerdruck-Seite, Materialien-Text ohne Druck-Hinweis (Stefan, 09.10.2026)
const ohneDruck = config.flyerdruck === false;
const areas = config.areas; // Array wie in references/config-beispiel.json
const email = config.absender?.email || "info@handzettelverteiler.de";
const absenderName = config.absender?.name || "HZV handzettelverteiler GmbH";
const absenderStrasse = config.absender?.strasse || "Bleichstraße 27";
const absenderOrt = config.absender?.ort || "66111 Saarbrücken";

const gesamt = {
  hh_bewerbbar: areas.reduce((s, a) => s + a.hh_bewerbbar, 0),
  hh_gesamt: areas.reduce((s, a) => s + a.hh_gesamt, 0),
  preis: areas.reduce((s, a) => s + a.preis_verteilung, 0),
};
const ortsteile = [...new Set(areas.map((a) => a.gebiet))].join(", ");
const plzSet = [...new Set(areas.map((a) => a.plz))];
const plzListe = plzSet.join(", ");
const einePLZ = plzSet.length === 1 && areas.length > 1;          // Ortsteile einer PLZ
const einStadt = !einePLZ && new Set(areas.map((a) => a.gebiet)).size === 1 && areas.length > 1;
const anfahrtGesamt = config.anfahrt_gesamt ?? (35 * plzSet.length);
const kundeName = kunde.name.replace(/\.$/, "");                   // kein doppelter Punkt ("e. V..")
const hatCent = areas.some((a) => Math.abs(a.preis_verteilung - Math.round(a.preis_verteilung)) > 0.001);
function fmtEur(n) {
  return n.toLocaleString("de-DE", hatCent ? { minimumFractionDigits: 2, maximumFractionDigits: 2 } : {}) + " €";
}
function fmtHH(n) { return n.toLocaleString("de-DE"); }

// ---- Bausteine ----
function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { after: opts.after ?? 160, before: opts.before ?? 0 },
    children: [
      new TextRun({
        text, bold: !!opts.bold, italics: !!opts.italics, color: opts.color,
        size: opts.size || SIZE, font: FONT,
        underline: opts.underline ? { type: UnderlineType.SINGLE } : undefined,
      }),
    ],
    pageBreakBefore: !!opts.pageBreakBefore,
  });
}
function heading(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 140, before: opts.before ?? 200 },
    pageBreakBefore: !!opts.pageBreakBefore,
    children: [new TextRun({ text, bold: true, size: opts.size || SIZE, font: FONT, color: opts.color })],
  });
}
function bullet(text) {
  return new Paragraph({
    spacing: { after: 100 },
    bullet: { level: 0 },
    children: [new TextRun({ text, size: SIZE, font: FONT })],
  });
}
function emptyFooter() { return new Footer({ children: [new Paragraph({ children: [] })] }); }
function emptyHeader() { return new Header({ children: [new Paragraph({ children: [] })] }); }
function footerWithFigures() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new ImageRun({ data: footerImg, type: "png", transformation: { width: 380, height: 86 } })],
    })],
  });
}

// ==================== SEITE 1: DECKBLATT + KUNDENDATEN/INTRO/MATERIALIEN ====================
const page1Children = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 220 },
    children: [new ImageRun({ data: headerBanner, type: "png", transformation: { width: 647, height: 132 } })],
  }),
  p(absenderName, { bold: true, after: 20 }),
  p(`${absenderStrasse} · ${absenderOrt}`, { after: 20 }),
  p(email, { after: 280 }),
  new Paragraph({
    spacing: { after: 260 },
    border: { left: { color: RED, space: 8, style: BorderStyle.SINGLE, size: 36 } },
    children: [new TextRun({ text: "Angebot", bold: true, color: RED, size: 56, font: FONT })],
  }),
  new Table({
    width: { size: 10100, type: WidthType.DXA },
    columnWidths: [10100],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: 10100, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: "F7F7F7" },
        margins: { top: 200, bottom: 200, left: 220, right: 220 },
        children: [
          p("Angebot für", { color: GREY, size: 18, after: 60 }),
          p(kunde.name, { bold: true, size: 26, after: 30 }),
          // optionale Zusatzzeilen (z. B. Behörde/Eigenbetrieb) zwischen Name und Straße
          ...(kunde.zusatz || []).map((z) => p(z, { after: 10 })),
          p(kunde.strasse, { after: 10 }),
          p(kunde.ort, { after: 0 }),
        ],
      })],
    })],
  }),
  new Paragraph({ spacing: { before: 320, after: 0 }, children: [] }),
  p(
    config.intro || (einePLZ
      ? `vielen Dank für Ihr Interesse an einer Handzettelverteilung für ${kundeName}. Wir haben für Sie ein Verteilgebiet in ${stadt} (PLZ ${plzListe}) zusammengestellt, das gezielt die Haushalte in den einzelnen Ortsteilen erreicht. Auf den folgenden Seiten finden Sie alle Details zu Gebieten, Ablauf und Preisen.`
      : `vielen Dank für Ihr Interesse an einer Handzettelverteilung für ${kundeName}. Wir haben für Sie ein Verteilgebiet rund um ${stadt} zusammengestellt, das gezielt Haushalte in den angrenzenden Ortschaften erreicht. Auf den folgenden Seiten finden Sie alle Details zu Gebieten, Ablauf und Preisen.`),
    { after: 280 }
  ),
  heading("Ihr Verteilgebiet"),
  p(
    config.gebiet_text || (einePLZ
      ? `Das Verteilgebiet umfasst ${areas.length} Ortsteile in PLZ ${plzListe} mit insgesamt ${fmtHH(gesamt.hh_bewerbbar)} bewerbbaren Haushalten. Verteilt wird in: ${ortsteile}. Den genauen Zeitraum stimmen wir gerne direkt mit Ihnen ab.`
      : einStadt
      ? `Das Verteilgebiet umfasst ${areas.length} PLZ-Bereiche in ${stadt} (${plzListe}) mit insgesamt ${fmtHH(gesamt.hh_bewerbbar)} bewerbbaren Haushalten. Den genauen Zeitraum stimmen wir gerne direkt mit Ihnen ab.`
      : `Das Verteilgebiet umfasst ${areas.length} PLZ-Bereiche (${plzListe}) mit insgesamt ${fmtHH(gesamt.hh_bewerbbar)} bewerbbaren Haushalten. Verteilt wird in: ${ortsteile}. Den genauen Zeitraum stimmen wir gerne direkt mit Ihnen ab.`),
    { after: 280 }
  ),
  heading("Materialien"),
  p(
    `Ihre Flyer können im Format DIN A6 bis DIN A4 sein, einlagig oder gefaltet. Am einfachsten senden Sie uns die Materialien direkt zu – die Lieferanschrift teilen wir Ihnen nach Auftragsbestätigung mit.` +
      (ohneDruck ? "" : ` Möchten Sie die Flyer bequem über uns drucken, sehen Sie weiter unten ein Angebotsbeispiel, das wir gerne individuell anpassen können.`),
    { after: 0 }
  ),
];

// ==================== SEITE 2: VERTEILUNGSDETAILS ====================
const page2Children = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 560 }, pageBreakBefore: true,
    children: [new ImageRun({ data: logo, type: "png", transformation: { width: 460, height: 92 } })],
  }),
  heading("Verteilungsdetails", { before: 0 }),
  bullet("In Mehrfamilienhäusern werden die Flyer in die Briefkästen eingeworfen, nicht in das Treppenhaus, außer es sind spezielle Werbekörbe vorhanden."),
  bullet("Bei Briefkästen mit dem Hinweis „Keine Werbung“ erfolgt kein Einwurf."),
  bullet("Bei verschlossenen Türen in Mehrparteienhäusern versuchen wir zu klingeln. Wenn niemand öffnet, erfolgt keine Verteilung."),
  bullet("Bei Einfamilienhäusern ohne zugängliche Briefkästen kann kein Einwurf erfolgen."),
  bullet("Falls ein Grundstück den Hinweis „Vorsicht Hund“ aufweist, werfen wir nicht ein, sofern wir dieses Grundstück betreten müssen, um den Briefkasten zu erreichen."),
  bullet("Wir führen keine Selektion nach Haustypen durch."),
  bullet("In Kleinstsiedlungen unter 150 bewerbbaren Haushalten, Gewerbegebieten, Industriegebieten und Kleingartenanlagen erfolgt keine Verteilung."),
  bullet("Insgesamt erreichen wir ca. 90 % der Haushalte im Verteilgebiet."),
  heading("Hinweis zur Verteilung", { before: 340 }),
  p(
    `Trotz größter Sorgfalt bei der Verteilung können wir keine Garantie für eine 100-prozentige Erreichung aller Briefkästen geben. Faktoren wie Zugänglichkeit, individuelle Gegebenheiten oder das Verhalten der Empfänger (z. B. Wegwerfen ohne Lesen, Nichtlesen, Nichtleerung des Briefkastens) können die Verteilung beeinflussen.`,
    { after: 320 }
  ),
  p(`Wir akzeptieren keine Telefonkontrollen oder Abfragen über soziale Medien (z. B. Facebook, WhatsApp).`, { after: 320 }),
  p(
    `Wir können nicht für das Verhalten der Empfänger haften, z. B. ungelesene oder weggeworfene Flyer, Desinteresse oder dass im Haushalt mehrere Bewohner leben, aber nicht miteinander kommunizieren.`,
    { after: 0 }
  ),
];

// ==================== SEITE 3: ÜBERSICHTSKARTE (Hochformat) ====================
// Dauerregel: Stadtbild IMMER über der Karte – Seite 3 UND Seite 4
// Altbilder (ca. quadratisch) bleiben wie bisher max. 240x200; neue Breitbilder (1600x873) werden 440x240.
function stadtIllustrationPara(lupe = false) {
  const data = lupe ? stadtLupe : stadtIllustration;
  const p_ = lupe ? stadtLupePath : stadtIllustrationPath;
  if (!data) return new Paragraph({ pageBreakBefore: true, children: [] });
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 200 }, pageBreakBefore: true,
    children: [new ImageRun({ data, type: imgType(p_), transformation: (() => { const d = imgSize(data); return d.w / d.h > 1.4 ? fit(data, 440, 240) : fit(data, 240, 200); })() })],
  });
}
const page3Children = [
  stadtIllustrationPara(),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: `Verteilgebiete ${stadt}`, bold: true, color: RED, size: 32, font: FONT })],
  }),
  p(einePLZ ? `Sie sehen hier die einzelnen Ortsteile der PLZ ${plzListe}. Die Haushaltszahlen sind weiter unten in der Tabelle aufgeführt.` : `Sie sehen hier die einzelnen Verteilbereiche. Die Haushaltszahlen sind weiter unten in der Tabelle aufgeführt.`, { align: AlignmentType.CENTER, after: 240 }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({ data: mapImage, type: imgType(mapImagePath), transformation: fit(mapImage, 600, 470) })],
  }),
];

// ==================== SEITE 4: BEISPIEL PLZ-REGION (Hochformat) ====================
const bKey = String(config.beispiel_area || areas[0].plz);
const bArea = areas.find((a) => a.id === bKey || a.gebiet === bKey) || areas.find((a) => String(a.plz) === bKey) || areas[0];
const bDiff = bArea.hh_gesamt - bArea.hh_bewerbbar;
const page3bChildren = [
  stadtIllustrationPara(true),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: `Beispiel: PLZ-Region ${bArea.plz} – ${bArea.gebiet}`, bold: true, color: RED, size: 32, font: FONT })],
  }),
  p(
    config.beispiel_text ||
    `${einePLZ ? "Im Ortsteil " + bArea.gebiet : "In der PLZ-Region " + bArea.plz + " (" + bArea.gebiet + ")"} gibt es insgesamt rund ${fmtHH(bArea.hh_gesamt)} Haushalte. Davon sind ${fmtHH(bArea.hh_bewerbbar)} Haushalte bewerbbar – nur diese werden verteilt und berechnet. Die Differenz von rund ${fmtHH(bDiff)} Haushalten entsteht vor allem durch Briefkästen mit dem Hinweis „Keine Werbung“: Dort erfolgt kein Einwurf.`,
    { align: AlignmentType.CENTER, after: 240 }
  ),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({ data: beispielImage, type: imgType(beispielPath), transformation: fit(beispielImage, 600, 440) })],
  }),
];

// ==================== SEITE 4: PREISÜBERSICHT ====================
function priceTable() {
  // Teilauflage (config areas[].auflage) -> zusätzliche grüne Auflage-Spalte, Preis bezieht sich auf die Auflage
  const hasAuflage = areas.some((a) => a.auflage);
  const headerCells = ["PLZ", "Gebiet", "HH bewerbbar", "HH gesamt", "Quote", ...(hasAuflage ? ["Auflage"] : []), "Preis"];
  const colWidths = hasAuflage ? [1000, 2300, 1550, 1400, 1000, 1250, 1600] : [1200, 2600, 1700, 1500, 1100, 2000];
  const keyCols = hasAuflage ? [2, 5, 6] : [2, 5];
  const ROW_PAD = areas.length > 15 ? 40 : 80; // viele PLZ -> engere Zeilen, damit Seite 5 nicht umbricht
  const LIGHT_ROW = "F7F7F7";
  const BORDER_LIGHT = { style: BorderStyle.SINGLE, size: 2, color: "E0E0E0" };

  const headerRow = new TableRow({
    tableHeader: true,
    children: headerCells.map((t, i) => new TableCell({
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: RED },
      verticalAlign: VerticalAlign.CENTER,
      margins: { top: 100, bottom: 100, left: 100, right: 100 },
      children: [new Paragraph({
        alignment: i >= 2 ? AlignmentType.RIGHT : AlignmentType.LEFT,
        children: [new TextRun({ text: t, bold: true, color: "FFFFFF", size: 19, font: FONT })],
      })],
    })),
  });

  const dataRows = areas.map((a, rowIdx) => {
    const vals = [a.plz, a.gebiet, fmtHH(a.hh_bewerbbar), fmtHH(a.hh_gesamt), `${a.quote} %`, ...(hasAuflage ? [fmtHH(a.auflage || a.hh_bewerbbar)] : []), fmtEur(a.preis_verteilung)];
    const zebra = rowIdx % 2 === 1;
    return new TableRow({
      children: vals.map((v, i) => {
        const isKeyCol = keyCols.includes(i); // HH bewerbbar & Preis: hellgrün (Kunde soll NICHT HH gesamt mit dem Preis verwechseln)
        let fill;
        if (isKeyCol) fill = GREEN_BG; else if (zebra) fill = LIGHT_ROW;
        return new TableCell({
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: fill ? { type: ShadingType.CLEAR, fill } : undefined,
          verticalAlign: VerticalAlign.CENTER,
          margins: { top: ROW_PAD, bottom: ROW_PAD, left: 100, right: 100 },
          borders: { bottom: BORDER_LIGHT },
          children: [new Paragraph({
            alignment: i >= 2 ? AlignmentType.RIGHT : AlignmentType.LEFT,
            children: [new TextRun({ text: String(v), size: 19, font: FONT, bold: isKeyCol, color: "222222" })],
          })],
        });
      }),
    });
  });

  const gesamtAuflage = areas.reduce((s, a) => s + (a.auflage || a.hh_bewerbbar), 0);
  const totalVals = ["Gesamt", "", fmtHH(gesamt.hh_bewerbbar), fmtHH(gesamt.hh_gesamt), "", ...(hasAuflage ? [fmtHH(gesamtAuflage)] : []), fmtEur(gesamt.preis)];
  const totalRow = new TableRow({
    children: totalVals.map((v, i) => {
      const isKeyCol = keyCols.includes(i);
      return new TableCell({
        width: { size: colWidths[i], type: WidthType.DXA },
        shading: isKeyCol ? { type: ShadingType.CLEAR, fill: GREEN_BG } : undefined,
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 120, bottom: 120, left: 100, right: 100 },
        borders: { top: { style: BorderStyle.SINGLE, size: 14, color: "222222" } },
        children: [new Paragraph({
          alignment: i >= 2 ? AlignmentType.RIGHT : AlignmentType.LEFT,
          children: [new TextRun({ text: String(v), bold: true, size: 20, font: FONT, color: "222222" })],
        })],
      });
    }),
  });

  return new Table({ width: { size: 10100, type: WidthType.DXA }, columnWidths: colWidths, rows: [headerRow, ...dataRows, totalRow] });
}

const page4Children = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 120 }, pageBreakBefore: true,
    children: [new ImageRun({ data: iconPreis, type: "png", transformation: { width: 170, height: 170 } })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: "Preisübersicht", bold: true, color: RED, size: 32, font: FONT })],
  }),
  p(`Für die Verteilung wie oben aufgeführt berechnen wir folgende Preise:`, { after: 200 }),
  priceTable(),
  p("Haushaltszahlen sind auf volle 50 gerundet.", { italics: true, color: GREY, size: 18, after: 200, before: 120 }),
  p(einePLZ ? `Für die An-/Abfahrt berechnen wir einmalig ${anfahrtGesamt},- Euro (alle Ortsteile liegen in PLZ ${plzListe}).` : (config.anfahrt_text || `Für die An-/Abfahrt berechnen wir je Verteil-PLZ insgesamt 35,- Euro (bei ${areas.length} PLZ-Regionen zusammen ${fmtHH(areas.reduce((s, a) => s + (a.anfahrt ?? 35), 0))},- Euro).`), { after: 200 }),
  p(`Möchten Sie weniger Flyer verteilen lassen, wird der Preis dem Anteil nach berechnet.`, { after: 0 }),
];

// ==================== SEITE 6: FLYERDRUCK (optional) – Option A / Option B ====================
// Standard (Stefan, 02.10.2026): Option A = DIN A5, Option B = DIN A4, je beidseitig 4/4, 135g matt.
// Preise: live von wir-machen-druck.de (netto) x 1,30, auf volle Euro aufgerundet. Auflage = Summe HH bewerbbar,
// aufgerundet auf die nächste WMD-Auflagenstufe. Per config.flyerdruck komplett überschreibbar (Sonderwunsch Kunde).
// Config: "flyerdruck": { "auflage": 20000, "preise": [260, 479] }
const FD_DEFAULT = {
  intro: "Auf Wunsch übernehmen wir auch den Druck Ihrer Flyer.",
  auflage: null,
  optionen: [
    { titel: "Flyer DIN A5 (14,8 cm x 21,0 cm), beidseitig bedruckt",
      specs: ["135g hochwertiger Qualitätsdruck matt", "4/4 farbig (beidseitiger Druck)",
              "Endformat: 14,8 cm x 21,0 cm", "Datenformat: 15,4 cm x 21,6 cm"],
      druckverfahren: "Diese Auflage wird im hochwertigen Offsetdruck hergestellt.", preis: null },
    { titel: "Flyer DIN A4 (21,0 cm x 29,7 cm), beidseitig bedruckt",
      specs: ["135g hochwertiger Qualitätsdruck matt", "4/4 farbig (beidseitiger Druck)",
              "Endformat: 21,0 cm x 29,7 cm", "Datenformat: 21,6 cm x 30,3 cm"],
      druckverfahren: "Diese Auflage wird im hochwertigen Offsetdruck hergestellt.", preis: null },
  ],
  hinweis: "Auflage, Flyerformat und Papierstärke passen wir selbstverständlich individuell an Ihre Wünsche an – sprechen Sie uns gerne an.",
};
const FD = Object.assign({}, FD_DEFAULT, config.flyerdruck || {});
const fdAuflage = FD.auflage || areas.reduce((s, a) => s + (a.auflage || a.hh_bewerbbar || 0), 0);
function specLine(text, opts = {}) {
  return new Paragraph({ spacing: { after: 0, before: 0 },
    children: [new TextRun({ text, bold: !!opts.bold, size: SIZE, font: FONT, color: opts.color })] });
}
const optionBlocks = [];
FD.optionen.forEach((o, i) => {
  const label = "Option " + String.fromCharCode(65 + i);
  // Nur eine Druckvariante (Kundenwunsch) -> kein "Option A"-Label
  if (FD.optionen.length > 1) optionBlocks.push(new Paragraph({ spacing: { before: i === 0 ? 120 : 280, after: 60 },
    children: [new TextRun({ text: label, bold: true, color: RED, size: SIZE + 4, font: FONT })] }));
  else optionBlocks.push(new Paragraph({ spacing: { before: 200, after: 0 }, children: [] }));
  optionBlocks.push(specLine(o.titel, { bold: true }));
  (o.specs || []).forEach(sp => optionBlocks.push(specLine(sp)));
  optionBlocks.push(p(o.druckverfahren || "", { before: 120, after: 120 }));
  const fdPreis = o.preis ?? (FD.preise || [])[i];
  // Tausenderpunkt + ",- Euro" wie bei der Anfahrt (sonst "1066.- Euro")
  const fdPreisTxt = typeof fdPreis === "number" ? `${fmtHH(fdPreis)},- Euro` : `${fdPreis}.- Euro`;
  const preisTxt = o.preis_text || `Gesamtauflage ${fmtHH(o.auflage || fdAuflage)} Stück: ${fdPreisTxt} zzgl. MwSt.`;
  optionBlocks.push(p(preisTxt, { bold: true, after: 0 }));
});
const page5Children = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 }, pageBreakBefore: true,
    children: [new ImageRun({ data: flyerdruckIllustration, type: "png", transformation: { width: 647, height: 162 } })],
  }),
  heading("Flyerdruck (optional)", { before: 0 }),
  p(FD.intro, { after: 0 }),
  ...optionBlocks,
  p(FD.hinweis, { italics: true, color: GREY, before: 320, after: 0 }),
];


// ==================== SEITE 6: ABSCHLUSS ====================
const heuteStr = new Date().toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
const page6Children = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 260 }, pageBreakBefore: true,
    children: [new ImageRun({ data: iconBuchen, type: "png", transformation: { width: 180, height: 180 } })],
  }),
  p(
    `Bitte senden Sie uns den Auftrag spätestens 10 Werktage vor dem gewünschten Verteilzeitraum unterzeichnet zu, damit wir alles rechtzeitig einplanen können. Soll früher verteilt werden? Teilen Sie uns Ihren Wunschtermin mit. Wir versuchen es dann schnell zu integrieren.`,
    { after: 200 }
  ),
  p(`Wir sind mittlerweile seit über 20 Jahren zuverlässig im Einsatz. Wir arbeiten ausschließlich mit erwachsenen Personen und halten uns an den gesetzlichen Mindestlohn.`, { after: 200 }),
  p(`Die Rechnung stellen wir nach der Auftragserteilung aus, die Zahlung ist vor Beginn der Verteilung fällig.`, { after: 200 }),
  p(`Alle Preise verstehen sich zuzüglich der gesetzlichen Mehrwertsteuer.`, { after: 360 }),
  p(heuteStr, { after: 500 }),
  new Paragraph({
    spacing: { after: 60 },
    border: { top: { color: "999999", space: 4, style: BorderStyle.SINGLE, size: 6 } },
    children: [new TextRun({ text: "" })],
  }),
  p("Kunde, Unterschrift, Stempel", { after: 400 }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new ImageRun({ data: whatsappQr, type: "png", transformation: { width: 110, height: 110 } })],
  }),
  p("Kurze Frage über WhatsApp? Einfach scannen.", { align: AlignmentType.CENTER, after: 60, size: 20 }),
  p("Preise haben Gültigkeit von 3 Monaten.", { align: AlignmentType.CENTER, size: 20, after: 0 }),
];

// ==================== SEITE 7: AGB (komprimiert auf 1 Seite) ====================
const agbParas = [
  ["1. Leistungen und Abweichungen", "Unsere Leistungen richten sich ausschließlich nach unseren schriftlich bestätigten Leistungs- und Zahlungsbedingungen. Abweichende Bedingungen des Auftraggebers gelten nur, wenn diese ausdrücklich und schriftlich anerkannt werden. Diese Bedingungen gelten auch für künftige Verträge mit dem Auftraggeber. Änderungen und Ergänzungen bedürfen der Schriftform."],
  ["2. Angebote", "Unsere Angebote sind freibleibend. Verbindlich werden Preise und Leistungen erst mit unserer schriftlichen Auftragsbestätigung. Sämtliche Preise verstehen sich in EUR zuzüglich der jeweils gültigen gesetzlichen Mehrwertsteuer. Besondere Anforderungen (z. B. für Proben, sperrige Sendungen, besondere Verteilgebiete) können gesondert berechnet werden."],
  ["3. Vertragliche Änderungen", "Ergeben sich gesetzlich bedingte Kostenänderungen, verhandeln die Parteien neu. Kommt keine Einigung zustande, steht beiden Seiten ein Sonderkündigungsrecht zu."],
  ["4. Anlieferung", "Das Verteilgut ist, sofern nicht anders vereinbart, spätestens drei Werktage vor Verteiltermin frei Haus an die vereinbarte Lieferadresse anzuliefern. Eine Haftung für Beschädigungen oder Verlust beim Transport durch Dritte übernehmen wir nicht. Verzögerungen, die durch den Auftraggeber verursacht werden, gehen zu dessen Lasten."],
  ["5. Durchführung", "Die Verteilung erfolgt standardmäßig durch Einwurf in Briefkästen von Privathaushalten. Kein Anspruch besteht auf Belieferung von Gewerbebetrieben, Büros, öffentlichen Einrichtungen, Heimen oder ähnlichen Adressen. Bei Hochhäusern mit verschlossenen Briefkästen erfolgt die Abgabe am vorgesehenen Sammelplatz. Nicht verteilbare Mengen werden nach Wahl entweder makuliert oder gegen Kostenübernahme zur Abholung bereitgestellt. Wir behalten uns vor, Aufträge mit gesetzes- oder sittenwidrigen Inhalten abzulehnen."],
  ["6. Unternehmerische Pflichten", "Die Verantwortung für die Einhaltung des Mindestlohngesetzes durch eingesetzte Subunternehmer liegt ausschließlich bei uns. Eine Haftung des Auftraggebers hierfür ist ausgeschlossen."],
  ["7. Gewährleistung, Nachweise und Haftung", "Es wird ausdrücklich kein bestimmter Werbeerfolg geschuldet. Der Auftraggeber haftet allein für Inhalt, Rechtmäßigkeit und Gestaltung der Werbemittel. Eine ordnungsgemäße Leistung liegt vor, wenn mindestens 90 % der vorgesehenen Haushalte beliefert wurden. Minder- oder Restmengen stellen keinen Mangel dar, sofern nichts Abweichendes schriftlich vereinbart ist. Nach jeder Verteilung werden stichprobenartige Nachweise in Form von Kontrolllisten und/oder Fotos erstellt und dem Auftraggeber zur Verfügung gestellt. Der Auftraggeber erhält den genauen Verteilzeitraum vor Beginn der Verteilung schriftlich mitgeteilt. Diese Nachweise gelten als verbindlicher Leistungsnachweis. Beanstandungen müssen innerhalb von 3 Werktagen nach Verteilerende schriftlich und konkretisiert erfolgen. Nach Ablauf dieser Frist gilt die Leistung als mängelfrei angenommen. Eine Haftung unsererseits besteht ausschließlich bei vorsätzlichem oder grob fahrlässigem Verhalten."],
  ["8. Beanstandungen (DSGVO)", "Beanstandungen sind ausschließlich anonymisiert und ohne personenbezogene Daten einzureichen. Nur konkrete, nachvollziehbare Angaben (Straße/Hausnummer) können berücksichtigt werden. Eine pauschale Reklamation berechtigt nicht zur Kürzung oder Verweigerung der Zahlung."],
  ["9. Haftungsausschluss", "Jegliche Schadensersatzansprüche sind ausgeschlossen, soweit sie nicht auf Vorsatz, grober Fahrlässigkeit oder der Verletzung wesentlicher Vertragspflichten beruhen. Eine Haftung für entgangenen Gewinn, mittelbare Schäden oder Mangelfolgeschäden ist ausgeschlossen. Unberührt bleibt die gesetzliche Haftung für Schäden an Leben, Körper oder Gesundheit."],
  ["10. Zahlung", "Die Zahlung erfolgt grundsätzlich im Voraus und ohne Abzug. Bei Zahlungsverzug sind wir berechtigt, Verzugszinsen in Höhe von 8 % über dem jeweiligen Basiszinssatz zu verlangen. Weitergehende Schadensersatzansprüche bleiben unberührt."],
  ["11. Erfüllungsort und Gerichtsstand", "Erfüllungsort und Gerichtsstand ist der Sitz der HZV handzettelverteiler GmbH."],
  ["12. Kündigungsfristen", "Verträge über regelmäßig wiederkehrende Leistungen können von beiden Parteien mit einer Frist von drei Monaten zum Monatsende gekündigt werden."],
  ["13. Schlussbestimmungen", "Sollten einzelne Bestimmungen dieser AGB unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt. Unwirksame Regelungen werden durch solche ersetzt, die dem wirtschaftlichen Zweck am nächsten kommen."],
];
const agbChildren = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 200 }, pageBreakBefore: true,
    children: [new TextRun({ text: "Allgemeine Geschäftsbedingungen – HZV handzettelverteiler GmbH", bold: true, size: 22, font: FONT })],
  }),
];
agbParas.forEach(([t, body], idx) => {
  agbChildren.push(new Paragraph({
    spacing: { before: idx === 0 ? 0 : 110, after: 40 },
    children: [new TextRun({ text: t, bold: true, size: 16, font: FONT })],
  }));
  agbChildren.push(p(body, { size: 14, after: 0 }));
});

// ==================== DOCUMENT ASSEMBLY ====================
const A4 = { width: 11906, height: 16838 };
const doc = new Document({
  sections: [
    { properties: { page: { size: A4, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, headers: { default: emptyHeader() }, footers: { default: footerWithFigures() }, children: page1Children },
    { properties: { page: { size: A4, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, headers: { default: emptyHeader() }, footers: { default: footerWithFigures() }, children: page2Children },
    { properties: { page: { size: A4, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, headers: { default: emptyHeader() }, footers: { default: footerWithFigures() }, children: page3Children },
    { properties: { page: { size: A4, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, headers: { default: emptyHeader() }, footers: { default: footerWithFigures() }, children: page3bChildren },
    { properties: { page: { size: A4, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, headers: { default: emptyHeader() }, footers: { default: footerWithFigures() }, children: [...page4Children, ...(ohneDruck ? [] : page5Children), ...page6Children] },
    { properties: { page: { size: A4, margin: { top: 700, bottom: 700, left: 900, right: 900 } } }, headers: { default: emptyHeader() }, footers: { default: emptyFooter() }, children: agbChildren },
  ],
});

const outPath = getArg("output", config.output || "Angebot.docx");
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  const fixScript = path.join(__dirname, "fix_rid0.py");
  console.log(execFileSync("python3", [fixScript, outPath]).toString().trim());
  console.log("Geschrieben:", outPath, buf.length, "bytes");
  console.log(`Summen -> HH bewerbbar: ${fmtHH(gesamt.hh_bewerbbar)}, HH gesamt: ${fmtHH(gesamt.hh_gesamt)}, Preis: ${fmtEur(gesamt.preis)}`);
});
