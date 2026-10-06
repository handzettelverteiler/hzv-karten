#!/usr/bin/env python3
"""
Baut eine eigenstaendige HZV-Verteilgebiete-Karte (Leaflet, HZV-Branding) aus einer
Areas-JSON-Datei. Leaflet wird lokal aus node_modules eingebettet (kein CDN noetig).

Vorbereitung (einmalig pro Session):
    mkdir -p /tmp/leaflet_pkg && cd /tmp/leaflet_pkg && npm install leaflet --no-save

Input-JSON-Format (Liste von Gebieten):
[
  {
    "plz": "45899",
    "gebiet": "GE-Horst/Karnap",
    "hh_bewerbbar": 13900,
    "hh_gesamt": 15500,
    "quote": 90,
    "anfahrt": 35,
    "preis_verteilung": 1362,
    "gesamtpreis": 1397,
    "coords": [[7.0095781, 51.532666], [7.0099264, 51.5326553], ...]
  },
  ...
]

"coords" sind [lon, lat]-Paare des Aussenrings. Mehrteilige PLZ: zusaetzlich
"polygons": [[ring1], [ring2], ...] angeben (alle Teilflaechen werden gezeichnet).

Zusatzoptionen:
    --highlight-plz <PLZ>  Ziel-PLZ blau, Rest abgedimmt, Zoom auf die PLZ
    --hide-sidebar         Sidebar ausblenden (fuer die Beispielseite im Angebot)
URL-Parameter der fertigen Karte:
    ?shot=1          Sidebar + Zoom-Buttons ausblenden (Screenshot-Modus)
    ?shot=1&plz=XXX  zusaetzlich PLZ hervorheben
Ortsteile einer PLZ (mehrere Gebiete mit gleicher PLZ): je Gebiet optional
    "id": "eutingen"     eindeutiger Schluessel fuer --highlight-plz / ?plz= (Standard: plz)
    "label": "Eutingen"  Beschriftung auf der Karte (Standard: "PLZ <plz>")

Aufruf:
    python3 build_karte.py --input areas.json --output IGA2027_Karte.html \
        --title "IGA 2027 &ndash; Angebot Handzettelverteilung (6 PLZ-Gebiete)" \
        --lede "Vorrangig in 'guten Lagen' innerhalb des Gebiets verteilen: ..." \
        --leaflet-dir /tmp/leaflet_pkg/node_modules/leaflet/dist \
        --update-note "PLZ 47166 wurde gegen PLZ 47057 (Duisburg/Neudorf) getauscht."
"""
import argparse
import json


def fmt_eur(n):
    if abs(n - round(n)) > 0.001:  # Cent-Betraege (z. B. 310,50 €) nicht verschlucken
        return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"
    return f"{round(n):,.0f}".replace(",", ".") + " €"


def fmt_hh(n):
    return f"{n:,.0f}".replace(",", ".")


TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE_PLAIN__ &ndash; handzettelverteiler Kartentool</title>
<style>
__LEAFLET_CSS__
</style>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: Arial, Helvetica, sans-serif; color: #222; background: #F7F6F3; }
  .layout { display: flex; height: 100vh; }
  aside { width: 300px; min-width: 300px; background: #fff; border-right: 1px solid #e5e2dd; padding: 20px; overflow-y: auto; }
  .logo { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .logo .mark { width: 30px; height: 30px; background: #C81E1E; border-radius: 6px; position: relative; flex-shrink: 0; }
  .logo .mark:before { content: "\\2709"; position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:16px; color:#fff; }
  .logo .word { font-size: 18px; font-weight: 700; color: #222; }
  .logo .word b { color: #C81E1E; }
  .eyebrow { font-size: 12px; color: #888; margin: 10px 0 2px 0; }
  h1 { margin: 0 0 10px 0; font-size: 19px; line-height: 1.3; color: #222; }
  .lede { font-size: 13px; color: #555; line-height: 1.5; margin-bottom: 16px; }
  .summary { background: #12463C; color: #fff; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
  .summary .cap { font-size: 11px; letter-spacing: .04em; text-transform: uppercase; opacity: .8; margin-bottom: 10px; }
  .summary .row { display: flex; justify-content: space-between; font-size: 13.5px; padding: 4px 0; }
  .summary .row.total { border-top: 1px solid rgba(255,255,255,.25); margin-top: 8px; padding-top: 10px; font-size: 15px; font-weight: 700; }
  .summary .val { font-weight: 700; }
  .summary .note { font-size: 11px; opacity: .7; margin-top: 6px; font-style: italic; }
  .cta { display: block; text-align: center; background: #fff; color: #12463C; font-weight: 700; padding: 10px; border-radius: 6px; text-decoration: none; margin-top: 12px; font-size: 14px; }
  .cta:hover { background: #eee; }
  .toggle-box { border: 1px solid #e5e2dd; border-radius: 8px; padding: 12px 14px; display: flex; align-items: center; justify-content: space-between; }
  .toggle-box .lbl { font-size: 13px; font-weight: 600; }
  .toggle-box .sub { font-size: 11px; color: #888; }
  .switch { position: relative; width: 38px; height: 20px; }
  .switch input { opacity: 0; width: 0; height: 0; }
  .slider { position: absolute; cursor: pointer; inset: 0; background-color: #C81E1E; border-radius: 20px; transition: .2s; }
  .slider:before { content: ""; position: absolute; height: 16px; width: 16px; left: 20px; bottom: 2px; background-color: white; border-radius: 50%; transition: .2s; }
  input:not(:checked) + .slider { background-color: #ccc; }
  input:not(:checked) + .slider:before { transform: translateX(-18px); }
  .arealist { margin-top: 16px; font-size: 12.5px; }
  .arealist .item { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #f0efec; }
  .arealist .item b { color: #C81E1E; }
  #map { flex: 1; height: 100%; }
  .leaflet-popup-content b { color: #C81E1E; }
  table.info { border-collapse: collapse; margin-top: 6px; }
  table.info td { padding: 1px 8px 1px 0; font-size: 13px; }
  table.info td.val { font-weight: bold; text-align: right; }
  .totals { margin-top: 8px; padding-top: 6px; border-top: 1px solid #ddd; font-size: 13px; }
  .footer-note { font-size: 11px; color: #999; margin-top: 18px; line-height: 1.5; }
  .plz-label-dim { opacity: 0.45; }
  aside { display: __SIDEBAR_DISPLAY__; }
  body.shot aside { display: none; }
  body.shot .leaflet-control-zoom { display: none; }
  @media (max-width: 760px) {
    .layout { flex-direction: column-reverse; height: auto; }
    #map { height: 65vh; flex: none; }
    aside { width: 100%; min-width: 0; border-right: 0; border-top: 1px solid #e5e2dd; }
  }
</style>
</head>
<body>
<div class="layout">
<aside>
  <div class="logo"><div class="mark"></div><div class="word">handzettelverteiler<b>.de</b></div></div>
  <div class="eyebrow">Ihre Verteilgebiete</div>
  <h1>__TITLE__</h1>
  <div class="lede">__LEDE__</div>

  <div class="summary">
    <div class="cap">Ihr Angebot &ndash; Gesamt</div>
    <div class="row"><span>Haushalte bewerbbar</span><span class="val">__BEWERBBAR__</span></div>
    <div class="row"><span>Haushalte gesamt</span><span class="val">__GESAMT__</span></div>
    <div class="row"><span>Anfahrt je PLZ-Region</span><span class="val">__ANFAHRT__</span></div>
    <div class="row"><span>Preis f&uuml;r Verteilung</span><span class="val">__VERTEILUNG__</span></div>
    <div class="row total"><span>Gesamtsumme</span><span class="val">__GESAMTPREIS__</span></div>
    <div class="note">Alle Preise zzgl. gesetzl. MwSt.</div>
    <a class="cta" href="__CTA_URL__" target="_blank" rel="noopener">Jetzt anfragen</a>
  </div>

  <div class="toggle-box">
    <div><div class="lbl">Verteilgebiete</div><div class="sub">__AREA_COUNT__ Objekte</div></div>
    <label class="switch"><input type="checkbox" id="layerToggle" checked><span class="slider"></span></label>
  </div>

  <div class="arealist" id="arealist"></div>

  <div class="footer-note">Klicke auf ein Gebiet auf der Karte f&uuml;r Details.__UPDATE_NOTE__</div>
</aside>
<div id="map"></div>
</div>
<script>
__LEAFLET_JS__
</script>
<script>
const geojson = __GEOJSON__;
const QS = new URLSearchParams(window.location.search);
const SHOT = QS.get('shot') === '1';
let HIGHLIGHT_PLZ = QS.get('plz') || '__HIGHLIGHT_PLZ__';
if (HIGHLIGHT_PLZ.indexOf('__') === 0) HIGHLIGHT_PLZ = '';
if (SHOT) document.body.classList.add('shot');

// Screenshot-Modus: Bruchteil-Zoom, damit die Gebiete den Ausschnitt fuellen (z. B. Rostock, hohe Nord-Sued-Ausdehnung)
const map = L.map('map', { zoomControl: true, zoomSnap: SHOT ? 0.1 : 1 }).setView([51.0, 10.0], 6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function popupHtml(p) {
  return `<b>PLZ ${p.plz} &ndash; ${p.gebiet}</b>
  <table class="info">
    <tr><td>Haushalte bewerbbar</td><td class="val">${p.hh_bewerbbar}</td></tr>
    <tr><td>Haushalte gesamt</td><td class="val">${p.hh_gesamt}</td></tr>
    <tr><td>Bewerbungsquote</td><td class="val">${p.quote}</td></tr>
    <tr><td>An-/Abfahrt</td><td class="val">${p.anfahrt}</td></tr>
    <tr><td>Preis f&uuml;r Verteilung</td><td class="val">${p.preis_verteilung}</td></tr>
  </table>
  <div class="totals">${p.anfahrt.indexOf('einmalig') > -1 ? 'Preis Ortsteil' : 'Gesamtpreis'}: <b>${p.gesamtpreis}</b></div>`;
}

const STYLE_NORMAL = { color: '#7A1010', weight: 1.5, opacity: 1, fillColor: '#C81E1E', fillOpacity: 0.25 };
const STYLE_TARGET = { color: '#0B3D91', weight: 3, opacity: 1, fillColor: '#1E6FD9', fillOpacity: 0.28 };
const STYLE_DIM    = { color: '#7A1010', weight: 1, opacity: 0.35, fillColor: '#C81E1E', fillOpacity: 0.08 };

function baseStyle(p) {
  if (!HIGHLIGHT_PLZ) return STYLE_NORMAL;
  return p.key === HIGHLIGHT_PLZ ? STYLE_TARGET : STYLE_DIM;
}

let targetLayer = null;
const geoLayer = L.geoJSON(geojson, {
  style: function(f) { return baseStyle(f.properties); },
  onEachFeature: function(feature, layer) {
    const p = feature.properties;
    const dim = HIGHLIGHT_PLZ && p.key !== HIGHLIGHT_PLZ;
    layer.bindPopup(popupHtml(p));
    layer.bindTooltip(p.label, { permanent: true, direction: 'center', className: dim ? 'plz-label plz-label-dim' : 'plz-label' });
    const s = baseStyle(p);
    layer.on('mouseover', function() { this.setStyle({ fillOpacity: Math.min(s.fillOpacity + 0.2, 0.6) }); });
    layer.on('mouseout', function() { this.setStyle({ fillOpacity: s.fillOpacity }); });
    if (HIGHLIGHT_PLZ && p.key === HIGHLIGHT_PLZ) targetLayer = layer;
  }
}).addTo(map);

if (targetLayer) {
  map.fitBounds(targetLayer.getBounds(), { padding: [40, 40] });
} else if (geojson.features.length) {
  map.fitBounds(geoLayer.getBounds(), { padding: [30, 30] });
}
setTimeout(function() { map.invalidateSize(); if (targetLayer) map.fitBounds(targetLayer.getBounds(), { padding: [40, 40] }); else map.fitBounds(geoLayer.getBounds(), { padding: [30, 30] }); }, 50);

document.getElementById('layerToggle').addEventListener('change', function(e) {
  if (e.target.checked) { map.addLayer(geoLayer); } else { map.removeLayer(geoLayer); }
});

const listEl = document.getElementById('arealist');
geojson.features.forEach(function(f) {
  const p = f.properties;
  const div = document.createElement('div');
  div.className = 'item';
  div.innerHTML = `<span><b>PLZ ${p.plz}</b> &middot; ${p.gebiet}</span><span>${p.gesamtpreis}</span>`;
  listEl.appendChild(div);
});
</script>
</body>
</html>
"""


def build(areas, title, lede, cta_url, update_note, leaflet_dir, output_path,
          highlight_plz="", hide_sidebar=False):
    with open(f"{leaflet_dir}/leaflet.js") as f:
        leaflet_js = f.read()
    with open(f"{leaflet_dir}/leaflet.css") as f:
        leaflet_css = f.read()

    # Ortsteile einer PLZ: An-/Abfahrt nur einmal je PLZ zaehlen (wie build_angebot.js)
    plz_count = {}
    for a in areas:
        plz_count[str(a["plz"])] = plz_count.get(str(a["plz"]), 0) + 1
    multi = any(c > 1 for c in plz_count.values())

    features = []
    for a in areas:
        polys = a.get("polygons") or [a["coords"]]
        polys = [[[float(lon), float(lat)] for lon, lat in ring] for ring in polys]
        if len(polys) == 1:
            geometry = {"type": "Polygon", "coordinates": [polys[0]]}
        else:
            geometry = {"type": "MultiPolygon", "coordinates": [[r] for r in polys]}
        features.append({
            "type": "Feature",
            "properties": {
                "plz": str(a["plz"]),
                "key": str(a.get("id") or a["plz"]),
                "label": a.get("label") or f'PLZ {a["plz"]}',
                "gebiet": a["gebiet"],
                "hh_bewerbbar": fmt_hh(a["hh_bewerbbar"]),
                "hh_gesamt": fmt_hh(a["hh_gesamt"]),
                "quote": f'{a["quote"]} %',
                "anfahrt": fmt_eur(a["anfahrt"]) + (f' einmalig f&uuml;r PLZ {a["plz"]}' if plz_count[str(a["plz"])] > 1 else ""),
                "preis_verteilung": fmt_eur(a["preis_verteilung"]),
                "gesamtpreis": fmt_eur(a["preis_verteilung"] if plz_count[str(a["plz"])] > 1 else a["gesamtpreis"]),
            },
            "geometry": geometry
        })
    geojson = {"type": "FeatureCollection", "features": features}

    if multi:
        anfahrt_je_plz = {}
        for a in areas:
            anfahrt_je_plz[str(a["plz"])] = max(anfahrt_je_plz.get(str(a["plz"]), 0), a["anfahrt"])
        anfahrt_sum = sum(anfahrt_je_plz.values())
        gesamt_sum = sum(a["preis_verteilung"] for a in areas) + anfahrt_sum
    else:
        anfahrt_sum = sum(a["anfahrt"] for a in areas)
        gesamt_sum = sum(a["gesamtpreis"] for a in areas)
    totals = {
        "bewerbbar": fmt_hh(sum(a["hh_bewerbbar"] for a in areas)),
        "gesamt": fmt_hh(sum(a["hh_gesamt"] for a in areas)),
        "anfahrt": fmt_eur(anfahrt_sum),
        "verteilung": fmt_eur(sum(a["preis_verteilung"] for a in areas)),
        "gesamtpreis": fmt_eur(gesamt_sum),
    }

    html = TEMPLATE
    html = html.replace("__LEAFLET_CSS__", leaflet_css)
    html = html.replace("__LEAFLET_JS__", leaflet_js)
    html = html.replace("__TITLE_PLAIN__", title.replace("&ndash;", "-"))
    html = html.replace("__TITLE__", title)
    html = html.replace("__LEDE__", lede)
    html = html.replace("__CTA_URL__", cta_url)
    html = html.replace("__AREA_COUNT__", str(len(areas)))
    html = html.replace("__UPDATE_NOTE__", f" {update_note}" if update_note else "")
    html = html.replace("__BEWERBBAR__", totals["bewerbbar"])
    html = html.replace("__GESAMT__", totals["gesamt"])
    html = html.replace("__ANFAHRT__", totals["anfahrt"])
    html = html.replace("__VERTEILUNG__", totals["verteilung"])
    html = html.replace("__GESAMTPREIS__", totals["gesamtpreis"])
    html = html.replace("__HIGHLIGHT_PLZ__", str(highlight_plz or ""))
    html = html.replace("__SIDEBAR_DISPLAY__", "none" if hide_sidebar else "block")
    html = html.replace("__GEOJSON__", json.dumps(geojson, ensure_ascii=False))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Geschrieben: {output_path} ({len(html)} bytes)")
    print(f"Summen -> HH bewerbbar: {totals['bewerbbar']}, HH gesamt: {totals['gesamt']}, "
          f"Anfahrt: {totals['anfahrt']}, Verteilung: {totals['verteilung']}, Gesamt: {totals['gesamtpreis']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Pfad zur Areas-JSON-Datei")
    ap.add_argument("--output", required=True, help="Pfad zur Ausgabe-HTML-Datei")
    ap.add_argument("--title", required=True, help="Projekttitel (HTML erlaubt, z.B. &ndash;)")
    ap.add_argument("--lede", default="Vorrangig in „guten Lagen“ innerhalb des Gebiets verteilen: hohe Eigentümerquote, Familien mit Kindern, mittlere Kaufkraft.")
    ap.add_argument("--cta-url", default="https://handzettelverteiler.de/kontakt/")
    ap.add_argument("--update-note", default="")
    ap.add_argument("--leaflet-dir", default="/tmp/leaflet_pkg/node_modules/leaflet/dist")
    ap.add_argument("--highlight-plz", default="", help="Ziel-PLZ (bzw. Gebiets-id bei Ortsteilen) blau hervorheben, Rest abdimmen, Zoom darauf")
    ap.add_argument("--hide-sidebar", action="store_true", help="Sidebar ausblenden")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        areas = json.load(f)

    if args.highlight_plz and args.highlight_plz not in [str(a.get("id") or a["plz"]) for a in areas]:
        raise SystemExit(f"--highlight-plz {args.highlight_plz} ist nicht in der Areas-Datei enthalten")
    build(areas, args.title, args.lede, args.cta_url, args.update_note, args.leaflet_dir, args.output,
          highlight_plz=args.highlight_plz, hide_sidebar=args.hide_sidebar)
