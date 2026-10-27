/**
 * HZV Angebot Generator (v6 – Layout „neu“ ab 26.10.2026 mit Rückfall auf „alt“; AGB Stand Okt 2026 auf 2 Seiten zweispaltig; Stadtbild + Lupen-Variante automatisch, Config-basiert)
 *
 * LAYOUT-SCHALTER (Stefan, 26.10.2026):
 *   neu (Standard): Seite 1 "Ihr Angebot auf einen Blick", Seite 2 "So läuft Ihre Verteilung", Anfahrt als Tabellenzeile + Gesamtpreis,
 *                   Option (Rest-PLZ komplett), Komplettpaket Druck + Verteilung, Beauftragung per E-Mail, gültig-bis-Datum.
 *                   Bewusst NICHT: WhatsApp als Beauftragungsweg, "fester Ansprechpartner", Preis pro Stück/Flyer.
 *   alt:            exakt das Layout v5 (bis 26.10.2026).
 *   Umschalten je Angebot: "layout": "alt" in der Config. Global: Umgebungsvariable HZV_LAYOUT=alt
 *   oder unten DEFAULT_LAYOUT auf "alt" setzen. Branch angebot-layout-alt-v5 = Stand vor der Umstellung.
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
  Header, Footer, VerticalAlign, UnderlineType, SectionType, ExternalHyperlink,
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
// "werbemittel": z. B. "Briefe" statt "Flyer" in Verteilungsdetails/Teilmengen-Hinweis; "materialien_text": eigener Materialien-Absatz (z. B. kuvertierte Briefe)
const werbemittel = config.werbemittel || "Flyer";
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
const einStadt = !einePLZ && (config.ein_stadt ?? (new Set(areas.map((a) => a.gebiet)).size === 1 && areas.length > 1)); // config.ein_stadt: alle PLZ in einer Stadt, gebiet = Stadtteil
function listeUnd(arr) { return arr.length <= 1 ? arr.join("") : arr.slice(0, -1).join(", ") + " und " + arr[arr.length - 1]; }
const stadtteile = listeUnd([...new Set(areas.map((a) => a.gebiet))]);
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

// ==================== LAYOUT-SCHALTER (v6) ====================
const DEFAULT_LAYOUT = "neu"; // Rückfall für ALLE Angebote: hier "alt" eintragen
const LAYOUT = String(config.layout || process.env.HZV_LAYOUT || DEFAULT_LAYOUT).toLowerCase() === "alt" ? "alt" : "neu";
console.log(`Layout: ${LAYOUT}`);

// ---- gemeinsame Werte für Layout "neu" ----
const telefon = config.absender?.telefon || config.kontakt?.telefon || "0681 41098133";
const kartenLink = config.karten_link || "";
function datumDE(d) { return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" }); }
const angebotsDatum = config.angebotsdatum || datumDE(new Date());
const gueltigBis = config.gueltig_bis || (() => { const d = new Date(); d.setMonth(d.getMonth() + 3); return datumDE(d); })();
const anfahrtSumme = einePLZ ? anfahrtGesamt : (config.anfahrt_gesamt ?? areas.reduce((s, a) => s + (a.anfahrt ?? 35), 0));
const endpreis = Math.round((gesamt.preis + anfahrtSumme) * 100) / 100;
const flyerGesamt = areas.reduce((s, a) => s + (a.auflage ?? a.hh_bewerbbar), 0);
function euroText(n) { return Number.isInteger(n) ? `${fmtHH(n)},- Euro` : `${n.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} Euro`; }
// Option: explizit per config.option, abschaltbar mit "option": false; sonst automatisch, wenn genau EINE PLZ nur teilweise beliefert wird (Auffüllen)
const opt = (() => {
  if (config.option === false) return null;
  if (config.option) return config.option;
  const teil = areas.filter((a) => a.auflage != null && a.auflage > 0 && a.auflage < a.hh_bewerbbar);
  if (teil.length !== 1) return null;
  const a = teil[0], diff = a.hh_bewerbbar - a.auflage;
  const plus = Math.round(diff * a.preis_verteilung / a.auflage * 100) / 100;
  return {
    titel: `Option: PLZ ${a.plz} komplett beliefern`,
    text: `Die PLZ ${a.plz} (${a.gebiet}) vollständig abdecken: ${fmtHH(a.hh_bewerbbar)} statt ${fmtHH(a.auflage)} ${werbemittel} – also ${fmtHH(diff)} ${werbemittel} mehr für nur ${euroText(plus)} netto zusätzlich.`,
    plus_preis: plus, plus_flyer: diff,
  };
})();
const LIGHT = "F7F7F7";
const NOB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const NO_BORDERS = { top: NOB, bottom: NOB, left: NOB, right: NOB };
function run(text, o = {}) { return new TextRun({ text, bold: !!o.bold, italics: !!o.italics, color: o.color, size: o.size || SIZE, font: FONT }); }
function para(runs, o = {}) {
  return new Paragraph({ alignment: o.align || AlignmentType.LEFT, spacing: { after: o.after ?? 0, before: o.before ?? 0 }, children: runs });
}
function linkPara(url, o = {}) {
  return new Paragraph({ spacing: { after: o.after ?? 0, before: o.before ?? 0 }, alignment: o.align || AlignmentType.LEFT,
    children: [new ExternalHyperlink({ link: url, children: [new TextRun({ text: o.text || url, style: "Hyperlink", color: "1F4E9E", underline: { type: UnderlineType.SINGLE }, size: o.size || 20, font: FONT })] })] });
}
function smallBullet(text, o = {}) {
  return new Paragraph({ spacing: { after: 80 }, bullet: { level: 0 }, children: [run(text, { size: o.size || 21, color: o.color || "333333" })] });
}

// ==================== SEITE 1 (Layout alt, v5): DECKBLATT + KUNDENDATEN/INTRO/MATERIALIEN ====================
const page1Alt = [
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
      : einStadt
      ? `vielen Dank für Ihr Interesse an einer Handzettelverteilung für ${kundeName}. Wir haben für Sie ein Verteilgebiet in ${stadt} zusammengestellt, das gezielt Haushalte in den Stadtteilen ${stadtteile} erreicht. Auf den folgenden Seiten finden Sie alle Details zu Gebieten, Ablauf und Preisen.`
      : `vielen Dank für Ihr Interesse an einer Handzettelverteilung für ${kundeName}. Wir haben für Sie ein Verteilgebiet rund um ${stadt} zusammengestellt, das gezielt Haushalte in den angrenzenden Ortschaften erreicht. Auf den folgenden Seiten finden Sie alle Details zu Gebieten, Ablauf und Preisen.`),
    { after: 280 }
  ),
  heading("Ihr Verteilgebiet"),
  p(
    config.gebiet_text || (einePLZ
      ? `Das Verteilgebiet umfasst ${areas.length} Ortsteile in PLZ ${plzListe} mit insgesamt ${fmtHH(gesamt.hh_bewerbbar)} bewerbbaren Haushalten. Verteilt wird in: ${ortsteile}. Den genauen Zeitraum stimmen wir gerne direkt mit Ihnen ab.`
      : einStadt
      ? `Das Verteilgebiet umfasst ${areas.length} PLZ-Bereiche in ${stadt} (${plzListe}) mit insgesamt ${fmtHH(gesamt.hh_bewerbbar)} bewerbbaren Haushalten. Verteilt wird in den Stadtteilen ${stadtteile}. Den genauen Zeitraum stimmen wir gerne direkt mit Ihnen ab.`
      : `Das Verteilgebiet umfasst ${areas.length} PLZ-Bereiche (${plzListe}) mit insgesamt ${fmtHH(gesamt.hh_bewerbbar)} bewerbbaren Haushalten. Verteilt wird in: ${ortsteile}. Den genauen Zeitraum stimmen wir gerne direkt mit Ihnen ab.`),
    { after: 280 }
  ),
  heading("Materialien"),
  p(
    config.materialien_text || `Ihre Flyer können im Format DIN A6 bis DIN A4 sein, einlagig oder gefaltet. Am einfachsten senden Sie uns die Materialien direkt zu – die Lieferanschrift teilen wir Ihnen nach Auftragsbestätigung mit.` +
      (ohneDruck ? "" : ` Möchten Sie die Flyer bequem über uns drucken, sehen Sie weiter unten ein Angebotsbeispiel, das wir gerne individuell anpassen können.`),
    { after: 0 }
  ),
];

// ==================== SEITE 2 (Layout alt, v5): VERTEILUNGSDETAILS ====================
const page2Alt = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 560 }, pageBreakBefore: true,
    children: [new ImageRun({ data: logo, type: "png", transformation: { width: 460, height: 92 } })],
  }),
  heading("Verteilungsdetails", { before: 0 }),
  bullet(`In Mehrfamilienhäusern werden die ${werbemittel} in die Briefkästen eingeworfen, nicht in das Treppenhaus, außer es sind spezielle Werbekörbe vorhanden.`),
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

// ==================== SEITE 1 (Layout neu): DECKBLATT mit "Ihr Angebot auf einen Blick" ====================
const gebietKurz = config.gebiet_kurz || (einePLZ ? `${stadt}, PLZ ${plzListe} (${areas.length} Ortsteile)` : einStadt ? `${stadtteile} (${plzSet.length} PLZ-Bereiche: ${plzListe})` : `${ortsteile} (${plzListe})`); // config.gebiet_kurz: eigener Text für "Verteilgebiet" auf Seite 1
const blickRows = [
  ["Verteilgebiet", [run(gebietKurz, { size: 21 })]],
  [`Verteilte ${werbemittel}`, [run(`${fmtHH(flyerGesamt)} Stück an Privathaushalte`, { size: 21 })]],
  ["Gesamtpreis", [run(`${fmtEur(endpreis)} netto`, { bold: true, color: RED, size: 30 }), run("  inkl. An-/Abfahrt", { size: 20, color: "555555" })]],
  ["Zeitraum", [run("nach Ihrem Wunschtermin – wir stimmen ihn direkt mit Ihnen ab", { size: 21 })]],
  ["Nachweis", [run("Stichprobendokumentation und/oder Fotos nach der Verteilung", { size: 21 })]],
  ["Beauftragung", [run("Kurze Antwort per E-Mail genügt", { size: 21, bold: true })]],
];
function blickTable() {
  const W1 = 2300, W2 = 7800;
  const head = new TableRow({ children: [new TableCell({
    columnSpan: 2, width: { size: W1 + W2, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: RED },
    margins: { top: 90, bottom: 90, left: 180, right: 180 }, borders: NO_BORDERS,
    children: [para([run("Ihr Angebot auf einen Blick", { bold: true, color: "FFFFFF", size: 24 })])],
  })] });
  const rows = blickRows.map(([l, runs], i) => new TableRow({ children: [
    new TableCell({ width: { size: W1, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: i === 2 ? "FDECEC" : LIGHT }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 70, bottom: 70, left: 180, right: 100 }, borders: { ...NO_BORDERS, bottom: { style: BorderStyle.SINGLE, size: 2, color: "E3E3E3" } },
      children: [para([run(l, { size: 20, color: "555555" })])] }),
    new TableCell({ width: { size: W2, type: WidthType.DXA }, shading: i === 2 ? { type: ShadingType.CLEAR, fill: "FDECEC" } : undefined, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 70, bottom: 70, left: 140, right: 140 }, borders: { ...NO_BORDERS, bottom: { style: BorderStyle.SINGLE, size: 2, color: "E3E3E3" } },
      children: [para(runs)] }),
  ] }));
  return new Table({ width: { size: W1 + W2, type: WidthType.DXA }, columnWidths: [W1, W2], rows: [head, ...rows] });
}
const page1Neu = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 180 },
    children: [new ImageRun({ data: headerBanner, type: "png", transformation: { width: 647, height: 132 } })],
  }),
  p(absenderName, { bold: true, after: 20 }),
  p(`${absenderStrasse} · ${absenderOrt}`, { after: 20 }),
  p(`Tel. ${telefon} · ${email}`, { after: 220 }),
  new Paragraph({
    spacing: { after: 0 },
    border: { left: { color: RED, space: 8, style: BorderStyle.SINGLE, size: 36 } },
    children: [new TextRun({ text: "Angebot", bold: true, color: RED, size: 56, font: FONT })],
  }),
  new Paragraph({
    spacing: { after: 200 },
    border: { left: { color: RED, space: 8, style: BorderStyle.SINGLE, size: 36 } },
    children: [run(`vom ${angebotsDatum} · gültig bis ${gueltigBis}`, { size: 20, color: "555555" })],
  }),
  new Table({
    width: { size: 10100, type: WidthType.DXA },
    columnWidths: [10100],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: 10100, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: "F7F7F7" },
        margins: { top: 150, bottom: 150, left: 220, right: 220 }, borders: NO_BORDERS,
        children: [
          p("Angebot für", { color: GREY, size: 18, after: 40 }),
          p(kunde.name, { bold: true, size: 26, after: 20 }),
          ...(kunde.zusatz || []).map((z) => p(z, { after: 10 })),
          p([kunde.strasse, kunde.ort].filter(Boolean).join(" · "), { after: 0 }),
        ],
      })],
    })],
  }),
  new Paragraph({ spacing: { before: 220, after: 0 }, children: [] }),
  p(
    config.intro || `vielen Dank für Ihr Interesse an einer Handzettelverteilung für ${kundeName}. Wir haben für Sie ein passendes Verteilgebiet ${einStadt || einePLZ ? "in" : "rund um"} ${stadt} zusammengestellt. Das Wichtigste sehen Sie hier, alle Details zu Gebiet, Ablauf und Preisen auf den folgenden Seiten.`,
    { after: 220 }
  ),
  blickTable(),
  heading("Materialien", { before: 260 }),
  p(
    config.materialien_text || `Ihre Flyer können im Format DIN A6 bis DIN A4 sein, einlagig oder gefaltet. Am einfachsten senden Sie uns die Materialien direkt zu – die Lieferanschrift teilen wir Ihnen nach Auftragsbestätigung mit.` +
      (ohneDruck ? "" : ` Oder Sie lassen die Flyer bequem über uns drucken – das Angebot dazu finden Sie weiter hinten.`),
    { after: 0 }
  ),
];

// ==================== SEITE 2 (Layout neu): SO LÄUFT IHRE VERTEILUNG ====================
const schritte = [
  ["Beauftragen", "Eine kurze Antwort per E-Mail genügt. Wir bestätigen Ihnen Auftrag und Verteilzeitraum schriftlich."],
  [`${werbemittel} anliefern`, ohneDruck ? `Sie senden uns die ${werbemittel} an die Lieferanschrift aus der Auftragsbestätigung – spätestens 3 Werktage vor Verteilbeginn.` : `Sie senden uns die ${werbemittel} an die Lieferanschrift aus der Auftragsbestätigung – oder wir drucken sie für Sie.`],
  ["Verteilung", `Unsere Verteiler werfen Ihre ${werbemittel} im vereinbarten Zeitraum in die Briefkästen der Privathaushalte ein – in Mehrfamilienhäusern in jeden Briefkasten, nicht ins Treppenhaus.`],
  ["Nachweis", "Nach Abschluss erhalten Sie eine Stichprobendokumentation und/oder Fotos Ihrer Verteilung."],
];
function schritteTable() {
  const W1 = 900, W2 = 9200;
  return new Table({ width: { size: W1 + W2, type: WidthType.DXA }, columnWidths: [W1, W2], rows: schritte.map(([t, txt], i) => new TableRow({ children: [
    new TableCell({ width: { size: W1, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: RED }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 80, bottom: 80, left: 60, right: 60 }, borders: { ...NO_BORDERS, bottom: { style: BorderStyle.SINGLE, size: 12, color: "FFFFFF" } },
      children: [para([run(String(i + 1), { bold: true, color: "FFFFFF", size: 34 })], { align: AlignmentType.CENTER })] }),
    new TableCell({ width: { size: W2, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: LIGHT }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 100, bottom: 100, left: 200, right: 200 }, borders: { ...NO_BORDERS, bottom: { style: BorderStyle.SINGLE, size: 12, color: "FFFFFF" } },
      children: [para([run(t, { bold: true, size: 23 })], { after: 30 }), para([run(txt, { size: 21, color: "333333" })])] }),
  ] })) });
}
const page2Neu = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 320 }, pageBreakBefore: true,
    children: [new ImageRun({ data: logo, type: "png", transformation: { width: 400, height: 80 } })],
  }),
  para([run("So läuft Ihre Verteilung", { bold: true, color: RED, size: 30 })], { after: 180 }),
  schritteTable(),
  para([run("Darauf können Sie sich verlassen", { bold: true, size: 24 })], { before: 300, after: 120 }),
  bullet("Seit über 20 Jahren zuverlässig im Einsatz."),
  bullet("Ausschließlich erwachsene Verteiler, bezahlt nach dem gesetzlichen Mindestlohn."),
  bullet("Stichprobendokumentation und/oder Fotos nach jeder Verteilung."),
  ...(kartenLink ? [bullet("Ihr Verteilgebiet als interaktive Karte zum Zoomen:"), linkPara(kartenLink, { after: 60, size: 19 })] : []),
  para([run("Gut zu wissen", { bold: true, size: 22, color: "555555" })], { before: 280, after: 100 }),
  smallBullet("Briefkästen mit „Keine Werbung“ respektieren wir. Diese Haushalte sind aus den bewerbbaren Haushalten bereits herausgerechnet – Sie bezahlen sie nicht."),
  smallBullet("Wo kein Zugang besteht, erfolgt kein Einwurf – etwa bei verschlossenen Häusern, wenn nach Klingeln niemand öffnet, bei unzugänglichen Briefkästen oder Grundstücken mit „Vorsicht Hund“."),
  smallBullet("Gewerbe- und Industriegebiete, Kleingartenanlagen und Kleinstsiedlungen unter 150 Haushalten werden nicht beliefert; eine Auswahl nach Haustypen ist nicht möglich."),
  smallBullet("Wir beliefern in jedem Verteilbezirk mindestens 90 % der erreichbaren Haushalte. Alle Einzelheiten regeln unsere AGB am Ende dieses Angebots."),
];
const page1Children = LAYOUT === "alt" ? page1Alt : page1Neu;
const page2Children = LAYOUT === "alt" ? page2Alt : page2Neu;

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
  p(config.karten_text || (einePLZ ? `Sie sehen hier die einzelnen Ortsteile der PLZ ${plzListe}. Die Haushaltszahlen sind weiter unten in der Tabelle aufgeführt.` : `Sie sehen hier die einzelnen Verteilbereiche. Die Haushaltszahlen sind weiter unten in der Tabelle aufgeführt.`), { align: AlignmentType.CENTER, after: 240 }),
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
  const hasAuflage = areas.some((a) => a.auflage != null);
  const headerCells = ["PLZ", "Gebiet", "HH bewerbbar", "HH gesamt", "Quote", ...(hasAuflage ? ["Verteilte Flyer"] : []), "Preis"];
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
    const vals = [a.plz, a.gebiet, fmtHH(a.hh_bewerbbar), fmtHH(a.hh_gesamt), `${a.quote} %`, ...(hasAuflage ? [fmtHH(a.auflage ?? a.hh_bewerbbar)] : []), fmtEur(a.preis_verteilung)];
    const leer = a.auflage === 0; // feste Auflage: PLZ mit 0 Flyern grau (optional)
    const zebra = rowIdx % 2 === 1;
    return new TableRow({
      children: vals.map((v, i) => {
        const isKeyCol = keyCols.includes(i); // HH bewerbbar & Preis: hellgrün (Kunde soll NICHT HH gesamt mit dem Preis verwechseln)
        let fill;
        if (isKeyCol && !leer) fill = GREEN_BG; else if (zebra || leer) fill = LIGHT_ROW;
        return new TableCell({
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: fill ? { type: ShadingType.CLEAR, fill } : undefined,
          verticalAlign: VerticalAlign.CENTER,
          margins: { top: ROW_PAD, bottom: ROW_PAD, left: 100, right: 100 },
          borders: { bottom: BORDER_LIGHT },
          children: [new Paragraph({
            alignment: i >= 2 ? AlignmentType.RIGHT : AlignmentType.LEFT,
            children: [new TextRun({ text: String(v), size: 19, font: FONT, bold: isKeyCol && !leer, color: leer ? "999999" : "222222" })],
          })],
        });
      }),
    });
  });

  const gesamtAuflage = areas.reduce((s, a) => s + (a.auflage ?? a.hh_bewerbbar), 0);
  if (LAYOUT === "neu") return priceTableNeu({ headerRow, dataRows, colWidths, keyCols, hasAuflage, ROW_PAD, BORDER_LIGHT, gesamtAuflage });
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

// Layout neu: An-/Abfahrt als eigene Zeile, Summe = Gesamtpreis inkl. Anfahrt (Anfahrt bleibt separat ausgewiesen)
function priceTableNeu({ headerRow, dataRows, colWidths, keyCols, hasAuflage, ROW_PAD, BORDER_LIGHT, gesamtAuflage }) {
  const anfahrtLabel = (einePLZ || plzSet.length === 1) ? "An-/Abfahrt (einmalig)" : (config.anfahrt_gesamt != null ? "An-/Abfahrt (pauschal)" : `An-/Abfahrt (${plzSet.length} PLZ-Regionen × 35 €)`);
  const nLast = colWidths.length - 1;
  const spanW = colWidths.slice(0, nLast).reduce((s, w) => s + w, 0);
  const anfahrtRow = new TableRow({
    children: [
      new TableCell({ columnSpan: nLast, width: { size: spanW, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        margins: { top: ROW_PAD, bottom: ROW_PAD, left: 100, right: 100 }, borders: { bottom: BORDER_LIGHT },
        children: [new Paragraph({ children: [new TextRun({ text: anfahrtLabel, size: 19, font: FONT, italics: true, color: "222222" })] })] }),
      new TableCell({ width: { size: colWidths[nLast], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        margins: { top: ROW_PAD, bottom: ROW_PAD, left: 100, right: 100 }, borders: { bottom: BORDER_LIGHT },
        shading: { type: ShadingType.CLEAR, fill: GREEN_BG },
        children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: fmtEur(anfahrtSumme), size: 19, font: FONT, bold: true, color: "222222" })] })] }),
    ],
  });
  const totalVals = ["Gesamtpreis netto", fmtHH(gesamt.hh_bewerbbar), fmtHH(gesamt.hh_gesamt), "", ...(hasAuflage ? [fmtHH(gesamtAuflage)] : []), fmtEur(endpreis)];
  const totalWidths = [colWidths[0] + colWidths[1], ...colWidths.slice(2)];
  const totalKey = keyCols.map((k) => k - 1);
  const totalRow = new TableRow({
    children: totalVals.map((v, i) => {
      const isKeyCol = totalKey.includes(i);
      const isPreis = i === totalVals.length - 1;
      return new TableCell({
        columnSpan: i === 0 ? 2 : undefined,
        width: { size: totalWidths[i], type: WidthType.DXA },
        shading: isPreis ? { type: ShadingType.CLEAR, fill: RED } : isKeyCol ? { type: ShadingType.CLEAR, fill: GREEN_BG } : undefined,
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 120, bottom: 120, left: 100, right: 100 },
        borders: { top: { style: BorderStyle.SINGLE, size: 14, color: "222222" } },
        children: [new Paragraph({
          alignment: i >= 1 ? AlignmentType.RIGHT : AlignmentType.LEFT,
          children: [new TextRun({ text: String(v), bold: true, size: isPreis ? 22 : 20, font: FONT, color: isPreis ? "FFFFFF" : "222222" })],
        })],
      });
    }),
  });
  return new Table({ width: { size: 10100, type: WidthType.DXA }, columnWidths: colWidths, rows: [headerRow, ...dataRows, anfahrtRow, totalRow] });
}

const page4Alt = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 120 }, pageBreakBefore: true,
    children: [new ImageRun({ data: iconPreis, type: "png", transformation: { width: 170, height: 170 } })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: "Preisübersicht", bold: true, color: RED, size: 32, font: FONT })],
  }),
  p(config.preis_intro || `Für die Verteilung wie oben aufgeführt berechnen wir folgende Preise:`, { after: 200 }),
  priceTable(),
  p("Haushaltszahlen sind auf volle 50 gerundet.", { italics: true, color: GREY, size: 18, after: 200, before: 120 }),
  ...(config.rabatt_text ? [p(config.rabatt_text, { bold: true, color: RED, after: 200 })] : []),
  p(einePLZ ? `Für die An-/Abfahrt berechnen wir einmalig ${anfahrtGesamt},- Euro (alle Ortsteile liegen in PLZ ${plzListe}).` : (config.anfahrt_text || `Für die An-/Abfahrt berechnen wir je Verteil-PLZ insgesamt 35,- Euro (bei ${areas.length} PLZ-Regionen zusammen ${fmtHH(areas.reduce((s, a) => s + (a.anfahrt ?? 35), 0))},- Euro).`), { after: 200 }),
  p(config.teilmengen_text || `Möchten Sie weniger ${werbemittel} verteilen lassen, wird der Preis dem Anteil nach berechnet.`, { after: 0 }),
];

// ==================== SEITE 5 (Layout neu): PREISÜBERSICHT ====================
function optionBox() {
  if (!opt) return [];
  const mitFlyer = flyerGesamt + (opt.plus_flyer || 0), mitPreis = Math.round((endpreis + (opt.plus_preis || 0)) * 100) / 100;
  return [new Table({ width: { size: 10100, type: WidthType.DXA }, columnWidths: [10100], rows: [new TableRow({ children: [new TableCell({
    width: { size: 10100, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: LIGHT },
    margins: { top: 140, bottom: 140, left: 220, right: 220 },
    borders: { ...NO_BORDERS, left: { style: BorderStyle.SINGLE, size: 36, color: RED } },
    children: [
      para([run(opt.titel, { bold: true, color: RED, size: 23 })], { after: 60 }),
      para([run(opt.text, { size: 21 })], { after: 60 }),
      para([run(`Gesamt mit Option: ${fmtHH(mitFlyer)} ${werbemittel} für ${fmtEur(mitPreis)} netto.`, { size: 21, bold: true })]),
    ],
  })] })] })];
}
const page4Neu = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 120 }, pageBreakBefore: true,
    children: [new ImageRun({ data: iconPreis, type: "png", transformation: { width: 150, height: 150 } })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: "Preisübersicht", bold: true, color: RED, size: 32, font: FONT })],
  }),
  p(config.preis_intro || `Für die Verteilung wie oben aufgeführt berechnen wir folgende Preise – An-/Abfahrt bereits eingerechnet:`, { after: 200 }),
  priceTable(),
  p("Haushaltszahlen sind auf volle 50 gerundet.", { italics: true, color: GREY, size: 18, after: 280, before: 120 }),
  ...(config.rabatt_text ? [p(config.rabatt_text, { bold: true, color: RED, after: 200 })] : []),
  ...optionBox(),
  p(opt ? (config.teilmengen_text_neu || `Möchten Sie weniger ${werbemittel} verteilen lassen, wird der Preis dem Anteil nach berechnet.`)
        : (config.teilmengen_text || `Möchten Sie weniger ${werbemittel} verteilen lassen, wird der Preis dem Anteil nach berechnet.`),
    { before: opt ? 240 : 0, after: 0, size: 21, color: "444444" }),
];
const page4Children = LAYOUT === "alt" ? page4Alt : page4Neu;

// ==================== SEITE 6: FLYERDRUCK (optional) – Option A / Option B ====================
// Standard (Stefan, 02.10.2026): Option A = DIN A5, Option B = DIN A4, je beidseitig 4/4, 135g matt.
// Preise: live von wir-machen-druck.de (netto) x 1,30, auf volle Euro aufgerundet. Auflage = Summe HH bewerbbar,
// aufgerundet auf die nächste WMD-Auflagenstufe. Per config.flyerdruck komplett überschreibbar (Sonderwunsch Kunde).
// Config: "flyerdruck": { "auflage": 20000, "preise": [260, 479] }
const FD_DEFAULT = {
  intro: LAYOUT === "alt" ? "Auf Wunsch übernehmen wir auch den Druck Ihrer Flyer." : "Auf Wunsch übernehmen wir auch den Druck Ihrer Flyer – Sie bekommen dann alles aus einer Hand.",
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
const fdAuflage = FD.auflage || areas.reduce((s, a) => s + (a.auflage ?? a.hh_bewerbbar ?? 0), 0);
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
  // Mehrere Preiszeilen je Option (z. B. 135g und 170g): o.preis_zeilen = ["...", "..."]
  if (Array.isArray(o.preis_zeilen) && o.preis_zeilen.length) {
    o.preis_zeilen.forEach((z, zi) => optionBlocks.push(p(z, { bold: true, after: zi === o.preis_zeilen.length - 1 ? 0 : 40 })));
  } else {
    const preisTxt = o.preis_text || `Gesamtauflage ${fmtHH(o.auflage || fdAuflage)} Stück: ${fdPreisTxt} zzgl. MwSt.`;
    optionBlocks.push(p(preisTxt, { bold: true, after: 0 }));
    // Layout neu: Komplettpaket Druck + Verteilung (Gesamtpreis inkl. Anfahrt)
    if (LAYOUT === "neu" && typeof fdPreis === "number") optionBlocks.push(para([run("Komplettpaket Druck + Verteilung: ", { size: 22 }), run(`${euroText(fdPreis + endpreis)} zzgl. MwSt.`, { bold: true, color: RED, size: 22 })], { before: 40 }));
  }
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
const page6Alt = [
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

// ==================== SEITE 7 (Layout neu): ABSCHLUSS – Beauftragung per E-Mail ====================
function kontaktBox() {
  const W1 = 6600, W2 = 3500;
  return new Table({ width: { size: W1 + W2, type: WidthType.DXA }, columnWidths: [W1, W2], rows: [new TableRow({ children: [
    new TableCell({ width: { size: W1, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: LIGHT }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 180, bottom: 180, left: 260, right: 200 }, borders: { ...NO_BORDERS, left: { style: BorderStyle.SINGLE, size: 36, color: RED } },
      children: [
        para([run("So erreichen Sie uns", { size: 19, color: GREY })], { after: 40 }),
        para([run(absenderName, { bold: true, size: 26 })], { after: 20 }),
        para([run(`${absenderStrasse} · ${absenderOrt}`, { size: 20, color: "444444" })], { after: 120 }),
        para([run(`Tel. ${telefon}`, { bold: true, size: 24 })], { after: 30 }),
        para([run(email, { size: 22 })]),
      ] }),
    new TableCell({ width: { size: W2, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: LIGHT }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 140, bottom: 140, left: 100, right: 100 }, borders: NO_BORDERS,
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ data: whatsappQr, type: "png", transformation: { width: 105, height: 105 } })] }),
        para([run("Kurze Frage über WhatsApp? Einfach scannen.", { size: 17, color: "444444" })], { align: AlignmentType.CENTER, before: 40 }),
      ] }),
  ] })] });
}
const page6Neu = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 180 }, pageBreakBefore: true,
    children: [new ImageRun({ data: iconBuchen, type: "png", transformation: { width: 150, height: 150 } })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 240 },
    children: [new TextRun({ text: "So einfach beauftragen Sie uns", bold: true, color: RED, size: 32, font: FONT })],
  }),
  p(`Antworten Sie einfach auf unsere E-Mail mit „Ja, wir beauftragen das Angebot“ und Ihrem Wunschzeitraum. Eine Unterschrift ist nicht nötig: Wir bestätigen Ihnen Auftrag und Verteilzeitraum anschließend schriftlich.`, { after: 200 }),
  p(`Damit wir alles rechtzeitig einplanen können, beauftragen Sie uns bitte spätestens 10 Werktage vor dem gewünschten Verteilzeitraum. Soll es schneller gehen? Nennen Sie uns Ihren Wunschtermin – wir versuchen, ihn möglich zu machen.`, { after: 280 }),
  kontaktBox(),
  p(`Die Rechnung stellen wir nach der Auftragserteilung aus, die Zahlung ist vor Beginn der Verteilung fällig. Alle Preise verstehen sich zuzüglich der gesetzlichen Mehrwertsteuer.`, { before: 280, after: 160 }),
  p(`Dieses Angebot ist gültig bis ${gueltigBis}.`, { bold: true, after: 380 }),
  p("Lieber klassisch? Sie können diese Seite auch unterschrieben zurücksenden.", { size: 19, color: GREY, after: 420 }),
  new Paragraph({
    spacing: { after: 60 },
    border: { top: { color: "BBBBBB", space: 4, style: BorderStyle.SINGLE, size: 6 } },
    children: [new TextRun({ text: "" })],
  }),
  p("Datum, Kunde, Unterschrift, Stempel", { size: 19, color: GREY, after: 0 }),
];
const page6Children = LAYOUT === "alt" ? page6Alt : page6Neu;

// ==================== AGB (Stand Oktober 2026, 18 Paragraphen, 2 Seiten zweispaltig) ====================
// Quelle: Doc "HZV AGB – Prüfung & Neuentwurf 2026" (Stefan, 21.10.2026). Text nur hier ändern.
const AGB_STAND = "Oktober 2026";
const agbParas = [
  ["§ 1 Geltungsbereich", [
    "(1) Diese AGB gelten für alle Verträge der HZV handzettelverteiler GmbH (nachfolgend „HZV“) über die Verteilung von Werbemitteln und damit verbundene Leistungen wie Gestaltung, Druck und Lagerung.",
    "(2) HZV schließt Verträge ausschließlich mit Unternehmern im Sinne von § 14 BGB, juristischen Personen des öffentlichen Rechts und öffentlich-rechtlichen Sondervermögen. Der Auftraggeber erteilt den Auftrag in Ausübung seiner gewerblichen oder selbständigen beruflichen Tätigkeit.",
    "(3) Abweichende Bedingungen des Auftraggebers gelten nicht, auch wenn HZV ihnen nicht ausdrücklich widerspricht. Diese AGB gelten auch für Folgeaufträge.",
    "(4) Individuelle Vereinbarungen haben Vorrang vor diesen AGB. Sie sind zu Beweiszwecken in Textform (z. B. E-Mail) festzuhalten.",
  ]],
  ["§ 2 Angebot und Vertragsschluss", [
    "(1) Angebote von HZV sind freibleibend und 3 Monate gültig. Der Vertrag kommt mit der Auftragsbestätigung von HZV in Textform zustande. Den Leistungsumfang bestimmen Auftragsbestätigung, Verteilplan bzw. Gebietskarte und diese AGB.",
    "(2) Alle Preise verstehen sich in Euro zuzüglich der gesetzlichen Umsatzsteuer. Sie gelten je Verteilgebiet für die im Angebot genannte Stückzahl sowie das genannte Format und Gewicht der Werbemittel. Weichen die angelieferten Werbemittel davon ab, teilt HZV den Mehrpreis vor Beginn der Verteilung in Textform mit.",
  ]],
  ["§ 3 Leistungsumfang", [
    "(1) HZV verteilt die Werbemittel durch Einwurf in die Briefkästen von Privathaushalten im vereinbarten Verteilgebiet und Verteilzeitraum. Geschuldet ist die Verteilung an die erreichbaren Haushalte nach Absatz 3, nicht ein bestimmter Werbeerfolg, Umsatz oder Rücklauf.",
    "(2) Die im Angebot genannten Haushaltszahlen sind Planzahlen. Sie umfassen auch Haushalte, die nach Absatz 3 nicht beliefert werden dürfen oder können. Abweichungen der tatsächlich erreichbaren Haushalte von den Planzahlen sind kein Mangel.",
    "(3) Nicht erreichbar sind und nicht beliefert werden insbesondere:",
    "a) Briefkästen mit einem Hinweis, dass keine Werbung gewünscht ist (§ 4);",
    "b) Häuser mit verschlossenen Innenbriefkästen oder Briefkästen an Wohnungstüren, wenn nach einmaligem Klingeln kein Zugang gewährt wird;",
    "c) Gewerbe- und Industriegebiete, Kleingartenanlagen, Einzelgehöfte sowie Häuser außerhalb zusammenhängender Wohngebiete;",
    "d) Grundstücke, deren Betreten verboten oder unzumutbar ist (z. B. wegen frei laufender Hunde oder fehlender sicherer Zuwegung).",
    "Briefkästen von Büros, Praxen und Geschäften innerhalb von Wohngebieten werden mitbeliefert. Sieht eine Hausverwaltung eine Ablagestelle für Werbemittel vor, kann die Abgabe dort erfolgen.",
    "(4) Die Leistung ist ordnungsgemäß erbracht, wenn in jedem Verteilbezirk mindestens 90 % der erreichbaren Haushalte beliefert wurden. Verteilbezirk ist die kleinste in Auftragsbestätigung oder Verteilplan ausgewiesene Gebietseinheit (z. B. Postleitzahl oder Teilgebiet).",
    "(5) Einzelne nicht belieferte Adressen, die sich nicht in einem zusammenhängenden Straßenabschnitt häufen, sind übliche Streuverluste und kein Mangel.",
    "(6) Ist die bestellte oder angelieferte Stückzahl geringer als die Zahl der erreichbaren Haushalte, bestimmt HZV die ausgelassenen Teilflächen; dies ist kein Mangel.",
    "(7) HZV darf Subunternehmer einsetzen und haftet für sie wie für eigene Mitarbeiter. In der Regel verteilt HZV jeden Auftrag einzeln. In einzelnen Teilgebieten darf HZV Werbemittel mehrerer Auftraggeber gemeinsam verteilen; ein Ausschluss von Wettbewerbern derselben Branche gilt nur, wenn er in Textform vereinbart ist.",
  ]],
  ["§ 4 Werbeverbote", [
    "(1) HZV beachtet Hinweise an Briefkästen, die den Einwurf von Werbung untersagen (z. B. „Keine Werbung“). Ein Einwurf trotz solcher Hinweise ist rechtswidrig; für Verstöße kann auch das werbende Unternehmen in Anspruch genommen werden.",
    "(2) Haushalte mit Werbeverbot zählen nicht zu den erreichbaren Haushalten. Weisungen, Werbeverbote zu missachten, führt HZV nicht aus.",
  ]],
  ["§ 5 Verteilnachweis", [
    "(1) HZV dokumentiert jede Verteilung stichprobenartig durch Kontrolllisten und/oder Fotos von bestückten Briefkästen oder Briefkastenanlagen.",
    "(2) Nach Abschluss der Verteilung erhält der Auftraggeber eine Auswahl dieser Nachweise in Textform.",
    "(3) Die Nachweise sind Stichproben. Sie zeigen weder jeden Briefkasten noch jede Straße. Ein lückenloser Einzelnachweis ist bei der Haushaltsverteilung weder technisch noch wirtschaftlich möglich und branchenüblich nicht geschuldet. Fehlt für eine Straße ein Nachweis, belegt das keine Nichtverteilung.",
  ]],
  ["§ 6 Werbemittel, Anlieferung und Mengen", [
    "(1) Werbemittel müssen briefkastengerecht sein, gebündelt angeliefert werden und mit einem Lieferschein versehen sein, der Auftraggeber, Auftragsnummer und Stückzahl nennt. Maximales Format und Gewicht ergeben sich aus dem Angebot.",
    "(2) Die Anlieferung erfolgt frei Haus an die vereinbarte Lieferadresse, spätestens 3 Werktage vor Beginn des Verteilzeitraums. Verspätete oder unvollständige Anlieferung verschiebt den Verteilzeitraum; dadurch entstehende Mehrkosten trägt der Auftraggeber.",
    "(3) HZV stellt die angelieferte Menge durch Zählen oder Wiegen fest und teilt Abweichungen vom Lieferschein unverzüglich in Textform mit. Für Verlust oder Beschädigung beim Transport durch Dritte haftet HZV nicht.",
    "(4) Liefert der Auftraggeber mehr Werbemittel an als beauftragt, ist HZV zur Verteilung dieser Mehrmengen nicht verpflichtet. Mehrmengen und nach der Verteilung verbliebene Restmengen überlässt der Auftraggeber HZV nach deren Wahl zur Verteilung im Verteilgebiet oder zur Entsorgung. Ein Anspruch auf Rückgabe, Abrechnung oder Auskunft über ihren Verbleib besteht nicht. Eine Rücknahme ist nur möglich, wenn sie vor der Anlieferung in Textform vereinbart wurde; der Auftraggeber holt die Werbemittel dann binnen 7 Tagen nach Ende des Verteilzeitraums auf eigene Kosten ab.",
    "(5) Werbemittel können durch Feuchtigkeit, statische Aufladung oder ihre Papier- und Druckqualität aneinanderhaften. Dadurch können vereinzelt mehrere Exemplare in einen Briefkasten gelangen. Der daraus entstehende Mehrverbrauch und daraus folgende Fehlmengen sind kein Mangel. Haften die Werbemittel in erheblichem Umfang aneinander, informiert HZV den Auftraggeber.",
  ]],
  ["§ 7 Inhalt der Werbemittel", [
    "(1) Der Auftraggeber ist allein verantwortlich für Inhalt, Gestaltung und Rechtmäßigkeit der Werbemittel, insbesondere nach Wettbewerbs-, Marken-, Urheber- und Datenschutzrecht. Er stellt HZV von Ansprüchen Dritter frei, die auf dem Inhalt der Werbemittel beruhen, einschließlich angemessener Kosten der Rechtsverteidigung.",
    "(2) Übernimmt HZV Gestaltung oder Druck, ist die Druckfreigabe des Auftraggebers maßgeblich. Für Fehler, die in der freigegebenen Vorlage enthalten sind, haftet HZV nicht.",
    "(3) HZV darf die Verteilung von Werbemitteln ablehnen, die gegen Gesetze oder die guten Sitten verstoßen, politische oder religiöse Inhalte haben oder von Format und Gewicht laut Angebot abweichen. Der Auftraggeber holt sie dann binnen 5 Werktagen auf eigene Kosten ab; für die Vergütung gilt § 13 entsprechend.",
  ]],
  ["§ 8 Verteilzeitraum, Verschiebungen, höhere Gewalt", [
    "(1) HZV verteilt innerhalb des vereinbarten Verteilzeitraums. Ein fester Verteiltag gilt nur, wenn er in der Auftragsbestätigung ausdrücklich als Fixtermin bezeichnet ist.",
    "(2) Unwetter, Streik, behördliche Maßnahmen, Verkehrssperren und vergleichbare Ereignisse, die HZV nicht zu vertreten hat, verlängern den Verteilzeitraum um die Dauer der Behinderung. HZV informiert den Auftraggeber unverzüglich. Ist ihm die spätere Verteilung nicht mehr zumutbar, kann er insoweit vom Vertrag zurücktreten; bereits erbrachte Leistungen werden vergütet.",
    "(3) Eine Nachverteilung in einzelnen Verteilbezirken innerhalb von 3 Werktagen nach Ende des Verteilzeitraums gilt als fristgerecht, soweit der Werbezweck (z. B. ein Veranstaltungsdatum) nicht entgegensteht.",
  ]],
  ["§ 9 Beanstandungen", [
    "(1) Beanstandungen sind in Textform an info@handzettelverteiler.de innerhalb von 2 Werktagen nach Ende des Verteilzeitraums zu erheben. Den Verteilzeitraum teilt HZV vor Beginn der Verteilung in Textform mit. Mängel, die der Auftraggeber schon während des Verteilzeitraums feststellt, meldet er unverzüglich. Die kurze Frist ist notwendig, weil Briefkästen in der Regel täglich geleert werden und eine spätere Überprüfung nicht mehr zuverlässig möglich ist.",
    "(2) Die Beanstandung muss enthalten:",
    "a) Verteilbezirk (Postleitzahl und Ort);",
    "b) betroffene Straße(n) mit Hausnummernbereich;",
    "c) Datum, Uhrzeit und Art der eigenen Kontrolle;",
    "d) vorhandene Belege, etwa eigene Fotos.",
    "Namen von Bewohnern werden nicht benötigt und sollen nicht übermittelt werden.",
    "(3) Eine Beanstandung ohne die Angaben nach Absatz 2 kann HZV nicht prüfen; sie wahrt die Frist nach Absatz 1 nicht.",
    "(4) Befragungen von Haushaltsmitgliedern, Telefonkontrollen und die Aussage, kein Werbemittel gesehen zu haben, belegen für sich genommen keine Nichtverteilung. Werbemittel werden häufig von einem Haushaltsmitglied zusammen mit anderer Werbung entnommen und ungelesen entsorgt, ohne dass andere Haushaltsmitglieder sie sehen. Bei geschlossenen Briefkästen ist ein eingeworfenes Werbemittel von außen nicht erkennbar; auch ein leer wirkender Briefkasten belegt daher keine Nichtverteilung.",
    "(5) HZV prüft jede fristgerechte Beanstandung anhand der Nachweise nach § 5 und einer Stellungnahme des eingesetzten Verteilers. Das Ergebnis teilt HZV dem Auftraggeber in der Regel innerhalb von 5 Werktagen in Textform mit.",
    "(6) Nicht fristgerecht oder nicht nach Absatz 2 erhobene Beanstandungen begründen keine Mängelrechte. Das gilt nicht, wenn HZV einen Mangel kannte und dem Auftraggeber verschwiegen hat, und nicht für Ansprüche nach § 11 Abs. 1.",
  ]],
  ["§ 10 Rechte bei berechtigter Beanstandung", [
    "(1) Ergibt die Prüfung nach § 9 Abs. 5, dass in den beanstandeten Straßenabschnitten nicht verteilt wurde und die Quote nach § 3 Abs. 4 dadurch unterschritten ist, verteilt HZV dort nach, soweit der Werbezweck dies zulässt und Werbemittel vorhanden sind.",
    "(2) Ist eine Nachverteilung nicht möglich, für den Auftraggeber nicht zumutbar oder schlägt sie fehl, erhält er eine Gutschrift für genau diese Straßenabschnitte: die Zahl der dortigen Haushalte multipliziert mit dem Preis je Haushalt. Der Preis je Haushalt ist der Preis des Verteilgebiets geteilt durch die im Angebot genannte Haushaltszahl dieses Gebiets.",
    "(3) Mängel in einzelnen Verteilbezirken lassen die Vergütung für die übrigen Bezirke unberührt. Ein Rücktritt vom gesamten Vertrag ist nur möglich, wenn der Auftraggeber an den mangelfreien Teilleistungen kein Interesse hat.",
    "(4) Schadensersatz richtet sich nach § 11.",
  ]],
  ["§ 11 Haftung", [
    "(1) HZV haftet unbeschränkt bei Vorsatz und grober Fahrlässigkeit, für Schäden aus der Verletzung von Leben, Körper oder Gesundheit, nach dem Produkthaftungsgesetz und im Umfang einer übernommenen Garantie.",
    "(2) Bei leicht fahrlässiger Verletzung einer wesentlichen Vertragspflicht ist die Haftung auf den vertragstypischen, vorhersehbaren Schaden begrenzt. Wesentlich sind Pflichten, deren Erfüllung die ordnungsgemäße Durchführung des Vertrags erst ermöglicht und auf deren Einhaltung der Auftraggeber regelmäßig vertrauen darf.",
    "(3) Im Übrigen ist die Haftung für leichte Fahrlässigkeit ausgeschlossen.",
    "(4) Diese Regeln gelten auch für die persönliche Haftung von Mitarbeitern, Verteilern und Subunternehmern von HZV.",
  ]],
  ["§ 12 Zahlung", [
    "(1) Rechnungen sind, soweit nicht anders vereinbart, vor Beginn des Verteilzeitraums ohne Abzug zu zahlen (Vorkasse). HZV beginnt die Verteilung nach Zahlungseingang; verzögert sich die Zahlung, verschiebt sich der Verteilzeitraum.",
    "(2) Bei Zahlungsverzug schuldet der Auftraggeber Verzugszinsen in gesetzlicher Höhe von 9 Prozentpunkten über dem Basiszinssatz sowie die Pauschale von 40 € nach § 288 Abs. 5 BGB. Solange der Auftraggeber in Verzug ist, darf HZV weitere Aufträge zurückstellen.",
    "(3) Der Auftraggeber kann nur mit unbestrittenen, rechtskräftig festgestellten oder entscheidungsreifen Gegenforderungen aufrechnen oder ein Zurückbehaltungsrecht ausüben. Gegenansprüche wegen Mängeln aus demselben Auftrag bleiben hiervon unberührt. Eine Beanstandung berechtigt nicht zur Kürzung von Rechnungen anderer Aufträge.",
  ]],
  ["§ 13 Stornierung durch den Auftraggeber", [
    "(1) Kündigt der Auftraggeber den Auftrag vor Abschluss der Verteilung, kann HZV statt einer konkreten Abrechnung nach § 648 BGB eine Pauschale auf die Netto-Verteilvergütung der nicht erbrachten Leistung verlangen: bis 10 Werktage vor Beginn des Verteilzeitraums 10 %, bis 3 Werktage vorher 25 %, danach 40 %. Bereits erbrachte Leistungen und bei Dritten beauftragte Leistungen, etwa der Druck, sind voll zu vergüten.",
    "(2) Der Auftraggeber kann nachweisen, dass HZV kein oder ein geringerer Schaden entstanden ist; dann schuldet er nur diesen. HZV kann umgekehrt einen höheren Anspruch nachweisen.",
  ]],
  ["§ 14 Mindestlohn", [
    "HZV beauftragt nur Subunternehmer, die sich zur Zahlung des gesetzlichen Mindestlohns verpflichtet haben, und überprüft dies. HZV stellt den Auftraggeber von Ansprüchen nach dem Mindestlohngesetz frei, die auf Pflichtverletzungen von HZV oder seinen Subunternehmern beruhen.",
  ]],
  ["§ 15 Verjährung", [
    "Mängel, die nicht fristgerecht nach § 9 beanstandet wurden, begründen von vornherein keine Ansprüche (§ 9 Abs. 6). Ansprüche aus fristgerecht beanstandeten Mängeln verjähren in 12 Monaten ab Ende des Verteilzeitraums. Das gilt nicht, wenn HZV einen Mangel kannte und verschwiegen hat, und nicht für Ansprüche nach § 11 Abs. 1.",
  ]],
  ["§ 16 Datenschutz", [
    "HZV verarbeitet personenbezogene Daten zur Vertragsdurchführung (Art. 6 Abs. 1 lit. b DSGVO) sowie zur Dokumentation der Verteilung und zur Abwehr von Ansprüchen (Art. 6 Abs. 1 lit. f DSGVO). Einzelheiten enthält die Datenschutzerklärung unter www.handzettelverteiler.de.",
  ]],
  ["§ 17 Rahmenverträge", [
    "Verträge über regelmäßig wiederkehrende Verteilungen können beide Seiten mit einer Frist von drei Monaten zum Monatsende kündigen.",
  ]],
  ["§ 18 Schlussbestimmungen", [
    "(1) Es gilt deutsches Recht.",
    "(2) Erfüllungsort und ausschließlicher Gerichtsstand ist Saarbrücken. HZV darf den Auftraggeber auch an dessen allgemeinem Gerichtsstand verklagen.",
    "(3) Ist eine Bestimmung dieser AGB unwirksam, bleiben die übrigen Bestimmungen wirksam.",
  ]],
];
const AGB_SIZE = 14, AGB_TITLE_SIZE = 15;
const agbTitleChildren = [
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: "Allgemeine Geschäftsbedingungen – HZV handzettelverteiler GmbH", bold: true, size: 22, font: FONT })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [new TextRun({ text: `Stand: ${AGB_STAND}`, size: AGB_SIZE, font: FONT, color: "555555" })],
  }),
];
const agbChildren = [];
agbParas.forEach(([t, absaetze], idx) => {
  agbChildren.push(new Paragraph({
    keepNext: true,
    spacing: { before: idx === 0 ? 0 : 100, after: 30 },
    children: [new TextRun({ text: t, bold: true, size: AGB_TITLE_SIZE, font: FONT })],
  }));
  absaetze.forEach((txt) => {
    const sub = /^[a-d]\) /.test(txt);
    agbChildren.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      indent: sub ? { left: 220 } : undefined,
      spacing: { after: 30, line: 228 },
      children: [new TextRun({ text: txt, size: AGB_SIZE, font: FONT })],
    }));
  });
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
    { properties: { page: { size: A4, margin: { top: 700, bottom: 700, left: 900, right: 900 } } }, headers: { default: emptyHeader() }, footers: { default: emptyFooter() }, children: agbTitleChildren },
    { properties: { type: SectionType.CONTINUOUS, column: { count: 2, space: 360 }, page: { size: A4, margin: { top: 700, bottom: 700, left: 900, right: 900 } } }, headers: { default: emptyHeader() }, footers: { default: emptyFooter() }, children: agbChildren },
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
