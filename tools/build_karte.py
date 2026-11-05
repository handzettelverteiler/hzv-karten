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
    --kunde-standort "lat,lon" [--kunde-name ".."] [--kunde-logo logo.png] [--kunde-stil logo|haus]
                           Kundenstandort als Marker (Logo-Kaertchen oder rotes Haeuschen)
URL-Parameter der fertigen Karte:
    ?shot=1          Sidebar + Zoom-Buttons ausblenden (Screenshot-Modus)
    ?shot=1&plz=XXX  zusaetzlich PLZ hervorheben
    --anfahrt-einmalig 35  An-/Abfahrt nur einmal fuer das ganze Gebiet (mehrere PLZ = ein Gebiet)
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
__AUFLAGE_ROW__    <div class="row"><span>__ANFAHRT_LABEL__</span><span class="val">__ANFAHRT__</span></div>
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
    ${p.auflage ? `<tr><td><b>Verteilmenge (Auflage)</b></td><td class="val"><b>${p.auflage}</b></td></tr>` : ''}
    <tr><td>An-/Abfahrt</td><td class="val">${p.anfahrt}</td></tr>
    <tr><td>Preis f&uuml;r Verteilung</td><td class="val">${p.preis_verteilung}</td></tr>
  </table>
  <div class="totals">${p.anfahrt.indexOf('gesamte Gebiet') > -1 ? 'Preis Teilgebiet' : p.anfahrt.indexOf('einmalig') > -1 ? 'Preis Ortsteil' : 'Gesamtpreis'}: <b>${p.gesamtpreis}</b></div>`;
}

const STYLE_NORMAL = { color: '#7A1010', weight: 1.5, opacity: 1, fillColor: '#C81E1E', fillOpacity: 0.25 };
const STYLE_TARGET = { color: '#0B3D91', weight: 3, opacity: 1, fillColor: '#1E6FD9', fillOpacity: 0.28 };
const STYLE_DIM    = { color: '#7A1010', weight: 1, opacity: 0.35, fillColor: '#C81E1E', fillOpacity: 0.08 };
// Feste Auflage: PLZ mit 0 Flyern grau gestrichelt (optional)
const STYLE_OPT    = { color: '#444444', weight: 2, opacity: 0.9, dashArray: '7 5', fillColor: '#777777', fillOpacity: 0.3 };

function baseStyle(p) {
  if (!HIGHLIGHT_PLZ) return p.optional ? STYLE_OPT : STYLE_NORMAL;
  return p.key === HIGHLIGHT_PLZ ? STYLE_TARGET : STYLE_DIM;
}

let targetLayer = null;
const geoLayer = L.geoJSON(geojson, {
  style: function(f) { return baseStyle(f.properties); },
  onEachFeature: function(feature, layer) {
    const p = feature.properties;
    const dim = HIGHLIGHT_PLZ && p.key !== HIGHLIGHT_PLZ;
    layer.bindPopup(popupHtml(p));
    layer.bindTooltip(p.optional && !HIGHLIGHT_PLZ ? p.label + ' (optional)' : p.label, { permanent: true, direction: 'center', className: dim ? 'plz-label plz-label-dim' : 'plz-label' });
    const s = baseStyle(p);
    layer.on('mouseover', function() { this.setStyle({ fillOpacity: Math.min(s.fillOpacity + 0.2, 0.6) }); });
    layer.on('mouseout', function() { this.setStyle({ fillOpacity: s.fillOpacity }); });
    if (HIGHLIGHT_PLZ && p.key === HIGHLIGHT_PLZ) targetLayer = layer;
  }
}).addTo(map);

// Kunden-Standort (optional): Logo-Kärtchen oder Häuschen mit Pin
const KUNDE = __KUNDE__;
if (KUNDE && KUNDE.lat) {
  let html, size, anchor;
  const nameTag = KUNDE.name ? '<div style="margin-top:3px;background:#C81E1E;color:#fff;font:bold 11px Arial;padding:2px 7px;border-radius:9px;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,.35)">' + KUNDE.name + '</div>' : '';
  if (KUNDE.stil === 'logo' && KUNDE.logo) {
    html = '<div style="display:flex;flex-direction:column;align-items:center">'
         + '<div style="background:#fff;border:2px solid #C81E1E;border-radius:8px;padding:4px 6px;box-shadow:0 2px 6px rgba(0,0,0,.4);line-height:0"><img src="' + KUNDE.logo + '" style="height:38px;width:auto;display:block"></div>'
         + '<div style="width:0;height:0;border-left:8px solid transparent;border-right:8px solid transparent;border-top:10px solid #C81E1E;margin-top:-1px"></div>'
         + '<div style="width:9px;height:9px;border-radius:50%;background:#C81E1E;border:2px solid #fff;box-shadow:0 0 3px rgba(0,0,0,.5);margin-top:1px"></div>'
         + nameTag + '</div>';
    size = [170, 110]; anchor = [85, 66];
  } else {
    html = '<div style="display:flex;flex-direction:column;align-items:center">'
         + '<svg width="46" height="52" viewBox="0 0 46 52" style="filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))">'
         + '<path d="M23 51 L15 40 H6 A4 4 0 0 1 2 36 V6 A4 4 0 0 1 6 2 H40 A4 4 0 0 1 44 6 V36 A4 4 0 0 1 40 40 H31 Z" fill="#C81E1E" stroke="#fff" stroke-width="2"/>'
         + '<path d="M23 8 L37 20 H33 V34 H13 V20 H9 Z" fill="#fff"/>'
         + '<rect x="20" y="25" width="6" height="9" fill="#C81E1E"/><rect x="14.5" y="22" width="4" height="4" fill="#C81E1E"/><rect x="27.5" y="22" width="4" height="4" fill="#C81E1E"/>'
         + '</svg>' + nameTag + '</div>';
    size = [170, 80]; anchor = [85, 51];
  }
  const icon = L.divIcon({ html: html, className: 'kunde-marker', iconSize: size, iconAnchor: anchor });
  L.marker([KUNDE.lat, KUNDE.lon], { icon: icon, zIndexOffset: 1000, interactive: !!KUNDE.popup })
    .addTo(map).bindPopup(KUNDE.popup || '');
}

if (targetLayer) {
  map.fitBounds(targetLayer.getBounds(), { padding: [40, 40] });
} else if (geojson.features.length) {
  map.fitBounds(geoLayer.getBounds(), { padding: [30, 30] });
}
setTimeout(function() { map.invalidateSize(); if (targetLayer) map.fitBounds(targetLayer.getBounds(), { padding: [40, 40] }); else map.fitBounds(geoLayer.getBounds(), { padding: [30, 30] }); }, 50);

if (!HIGHLIGHT_PLZ && geojson.features.some(function(f){ return f.properties.optional; })) {
  const lg = L.control({ position: 'bottomleft' });
  lg.onAdd = function() { const d = L.DomUtil.create('div'); d.style.cssText = 'background:#fff;padding:6px 10px;border-radius:6px;font:12px Arial;box-shadow:0 1px 4px rgba(0,0,0,.3);line-height:1.6'; d.innerHTML = '<span style="display:inline-block;width:14px;height:10px;background:rgba(200,30,30,.25);border:1.5px solid #7A1010;vertical-align:middle"></span> beliefert<br><span style="display:inline-block;width:14px;height:10px;background:rgba(158,158,158,.15);border:1.5px dashed #666;vertical-align:middle"></span> optional (0 Flyer)'; return d; };
  lg.addTo(map);
}

document.getElementById('layerToggle').addEventListener('change', function(e) {
  if (e.target.checked) { map.addLayer(geoLayer); } else { map.removeLayer(geoLayer); }
});

const listEl = document.getElementById('arealist');
geojson.features.forEach(function(f) {
  const p = f.properties;
  const div = document.createElement('div');
  div.className = 'item';
  div.innerHTML = `<span><b>PLZ ${p.plz}</b> &middot; ${p.gebiet}</span><span>${p.optional ? 'optional (0 Flyer)' : p.gesamtpreis}</span>`;
  listEl.appendChild(div);
});
</script>
</body>
</html>
"""


def build(areas, title, lede, cta_url, update_note, leaflet_dir, output_path,
          highlight_plz="", hide_sidebar=False, anfahrt_einmalig=None, hh_gesamt_total=None, kunde=None):
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
                "hh_gesamt": ("ca. " if a.get("hh_gesamt_ca") else "") + fmt_hh(a["hh_gesamt"]) if a.get("hh_gesamt") is not None else "&ndash;",
                "quote": f'{a["quote"]} %' if a.get("quote") is not None else "&ndash;",
                "auflage": fmt_hh(a["auflage"]) if a.get("auflage") is not None else "",
                "optional": a.get("auflage") == 0,
                "anfahrt": (fmt_eur(anfahrt_einmalig) + " einmalig f&uuml;r das gesamte Gebiet") if anfahrt_einmalig is not None
                           else fmt_eur(a["anfahrt"]) + (f' einmalig f&uuml;r PLZ {a["plz"]}' if plz_count[str(a["plz"])] > 1 else ""),
                "preis_verteilung": fmt_eur(a["preis_verteilung"]),
                "gesamtpreis": fmt_eur(a["preis_verteilung"] if (anfahrt_einmalig is not None or plz_count[str(a["plz"])] > 1) else a["gesamtpreis"]),
            },
            "geometry": geometry
        })
    geojson = {"type": "FeatureCollection", "features": features}

    if anfahrt_einmalig is not None:
        # Ganzes Verteilgebiet = ein Gebiet: An-/Abfahrt nur einmal, egal wie viele PLZ
        anfahrt_sum = anfahrt_einmalig
        gesamt_sum = sum(a["preis_verteilung"] for a in areas) + anfahrt_sum
    elif multi:
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
        "gesamt": fmt_hh(hh_gesamt_total) if hh_gesamt_total is not None else fmt_hh(sum(a.get("hh_gesamt") or 0 for a in areas)),
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
    # Teilauflage: Verteilmenge in der Kennzahlenbox zeigen, sobald ein Gebiet ein auflage-Feld hat
    auflage_row = ""
    if any(a.get("auflage") is not None for a in areas):
        auflage_sum = sum(a["auflage"] if a.get("auflage") is not None else a["hh_bewerbbar"] for a in areas)
        auflage_row = f'    <div class="row"><span><b>Verteilmenge (Auflage)</b></span><span class="val"><b>{fmt_hh(auflage_sum)}</b></span></div>\n'
    html = html.replace("__AUFLAGE_ROW__", auflage_row)
    html = html.replace("__GESAMT__", totals["gesamt"])
    # Summe ueber mehrere PLZ nicht als "je PLZ-Region" beschriften (sonst liest der Kunde 70 € je PLZ)
    n_plz_anf = len({str(a["plz"]) for a in areas if a.get("anfahrt")})
    anf_label = ("Anfahrt (einmalig)" if anfahrt_einmalig is not None
                 else f"An-/Abfahrt ({n_plz_anf} PLZ-Regionen)" if n_plz_anf > 1 else "Anfahrt je PLZ-Region")
    html = html.replace("__ANFAHRT_LABEL__", anf_label)
    html = html.replace("__ANFAHRT__", totals["anfahrt"])
    html = html.replace("__VERTEILUNG__", totals["verteilung"])
    html = html.replace("__GESAMTPREIS__", totals["gesamtpreis"])
    html = html.replace("__HIGHLIGHT_PLZ__", str(highlight_plz or ""))
    html = html.replace("__SIDEBAR_DISPLAY__", "none" if hide_sidebar else "block")
    html = html.replace("__GEOJSON__", json.dumps(geojson, ensure_ascii=False))
    html = html.replace("__KUNDE__", json.dumps(kunde or None, ensure_ascii=False))

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
    ap.add_argument("--hh-gesamt-total", type=float, default=None, help="HH gesamt fuer die Summenzeile, wenn je Ortsteil kein Wert bekannt ist (z. B. nur PLZ-Gesamtwert)")
    ap.add_argument("--anfahrt-einmalig", type=float, default=None, help="An-/Abfahrt nur einmal fuer das ganze Verteilgebiet (z. B. 35), unabhaengig von der Zahl der PLZ")
    ap.add_argument("--kunde-standort", default="", help="Kundenstandort 'lat,lon' als Marker auf der Karte")
    ap.add_argument("--kunde-name", default="", help="Beschriftung unter dem Kunden-Marker")
    ap.add_argument("--kunde-logo", default="", help="Logo-Datei (png/jpg) fuer den Marker; ohne Logo = Haeuschen")
    ap.add_argument("--kunde-stil", choices=["logo", "haus"], default=None, help="Marker-Stil (Standard: logo, wenn Logo angegeben, sonst haus)")
    ap.add_argument("--kunde-popup", default="", help="Popup-Text (HTML) beim Klick auf den Marker")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        areas = json.load(f)

    kunde = None
    if args.kunde_standort:
        import base64, mimetypes
        lat, lon = [float(x) for x in args.kunde_standort.split(",")]
        logo = ""
        if args.kunde_logo:
            mime = mimetypes.guess_type(args.kunde_logo)[0] or "image/png"
            logo = f"data:{mime};base64," + base64.b64encode(open(args.kunde_logo, "rb").read()).decode()
        kunde = {"lat": lat, "lon": lon, "name": args.kunde_name, "logo": logo,
                 "stil": args.kunde_stil or ("logo" if logo else "haus"), "popup": args.kunde_popup}

    if args.highlight_plz and args.highlight_plz not in [str(a.get("id") or a["plz"]) for a in areas]:
        raise SystemExit(f"--highlight-plz {args.highlight_plz} ist nicht in der Areas-Datei enthalten")
    build(areas, args.title, args.lede, args.cta_url, args.update_note, args.leaflet_dir, args.output,
          highlight_plz=args.highlight_plz, hide_sidebar=args.hide_sidebar, anfahrt_einmalig=args.anfahrt_einmalig, hh_gesamt_total=args.hh_gesamt_total, kunde=kunde)
