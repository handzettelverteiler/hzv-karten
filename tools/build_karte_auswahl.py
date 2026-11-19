#!/usr/bin/env python3
"""
Auswahl-Karte (Stefan, 19.11.2026): Kunde klickt Ortsteile/PLZ-Gebiete in der Karte an oder ab,
Haushalte und Preis rechnen live mit (An-/Abfahrt 35 EUR je PLZ mit mindestens einem gewaehlten Gebiet),
Button "Auswahl per E-Mail anfragen" oeffnet eine fertige Mail an HZV mit der Auswahl.

Aufruf:
  python3 tools/build_karte_auswahl.py --input auswahl.json --output <Projekt>_Auswahlkarte_v1_<Info>.html \
      --title "Bruns Medienlogistik GmbH - Verteilgebiete Minden &amp; Porta Westfalica" \
      --angebotsnr 2611-105 --kunde "Bruns Medienlogistik GmbH"

auswahl.json:
  { "areas": [ {"id": "32423-Dankersen", "plz": "32423", "gebiet": "Dankersen", "ort": "Minden",
                "hh": 1800, "preis": 216.0, "satz": 120, "polygons": [[[lon,lat],...]], "aus": false}, ... ],
    "plz":   { "32423": [[[lon,lat],...]], ... } }      # PLZ-Umrisse (nur Linien + Beschriftung)
  "aus": true = startet abgewaehlt (optional). Ohne Ortsteil-Polygone einfach je PLZ ein Eintrag mit dem PLZ-Polygon.

Parameter in der URL: ?shot=1 (ohne Sidebar, fuer Screenshots), ?sel=<id1>,<id2> (Vorauswahl).
"""
import argparse, json, os

TEMPLATE = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE_PLAIN__ &ndash; Gebiete auswählen &ndash; handzettelverteiler</title>
<style>
__LEAFLET_CSS__
</style>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: Arial, Helvetica, sans-serif; color: #222; background: #F7F6F3; }
  .layout { display: flex; height: 100vh; }
  aside { width: 340px; min-width: 340px; background: #fff; border-right: 1px solid #e5e2dd; padding: 18px; overflow-y: auto; }
  .logo { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .logo .mark { width: 30px; height: 30px; background: #C81E1E; border-radius: 6px; position: relative; flex-shrink: 0; }
  .logo .mark:before { content: "\2709"; position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:16px; color:#fff; }
  .logo .word { font-size: 18px; font-weight: 700; color: #222; }
  .logo .word b { color: #C81E1E; }
  .eyebrow { font-size: 12px; color: #888; margin: 10px 0 2px 0; }
  h1 { margin: 0 0 8px 0; font-size: 18px; line-height: 1.3; }
  .hint { font-size: 13px; color: #444; line-height: 1.45; background: #FFF6E5; border: 1px solid #F3D9A4; border-radius: 8px; padding: 9px 11px; margin-bottom: 12px; }
  .summary { background: #12463C; color: #fff; border-radius: 8px; padding: 14px 16px; margin-bottom: 12px; position: sticky; top: 0; z-index: 5; }
  .summary .cap { font-size: 11px; letter-spacing: .04em; text-transform: uppercase; opacity: .8; margin-bottom: 8px; }
  .summary .row { display: flex; justify-content: space-between; font-size: 13.5px; padding: 3px 0; }
  .summary .row.total { border-top: 1px solid rgba(255,255,255,.25); margin-top: 6px; padding-top: 8px; font-size: 16px; font-weight: 700; }
  .summary .val { font-weight: 700; }
  .summary .note { font-size: 11px; opacity: .75; margin-top: 4px; font-style: italic; }
  .cta { display: block; width: 100%; text-align: center; background: #fff; color: #12463C; font-weight: 700; padding: 10px; border-radius: 6px; text-decoration: none; margin-top: 10px; font-size: 14px; border: 0; cursor: pointer; font-family: inherit; }
  .cta:hover { background: #eee; }
  .cta[aria-disabled="true"] { opacity: .5; pointer-events: none; }
  .btns { display: flex; gap: 8px; margin-bottom: 10px; }
  .btns button { flex: 1; padding: 7px; border: 1px solid #ccc; background: #fff; border-radius: 6px; font-size: 12.5px; cursor: pointer; font-family: inherit; }
  .btns button:hover { background: #f3f3f3; }
  .grp { margin-bottom: 10px; border: 1px solid #eee; border-radius: 8px; overflow: hidden; }
  .grp-h { display: flex; align-items: center; gap: 8px; background: #F7F6F3; padding: 7px 10px; font-size: 13px; font-weight: 700; cursor: pointer; }
  .grp-h .sum { margin-left: auto; font-weight: 400; color: #666; font-size: 12px; }
  .it { display: flex; align-items: center; gap: 8px; padding: 6px 10px; font-size: 13px; border-top: 1px solid #f2f1ee; cursor: pointer; }
  .it:hover { background: #FBFAF8; }
  .it .nm { flex: 1; }
  .it .hh { color: #666; font-size: 12px; min-width: 56px; text-align: right; white-space: nowrap; }
  .it .pr { font-weight: 700; min-width: 66px; text-align: right; white-space: nowrap; }
  .it.off .nm, .it.off .pr { color: #aaa; font-weight: 400; }
  .it .tag { font-size: 10px; color: #12463C; background: #E3F1EC; border-radius: 4px; padding: 1px 5px; }
  input[type=checkbox] { width: 16px; height: 16px; accent-color: #C81E1E; cursor: pointer; flex-shrink: 0; }
  .footer-note { font-size: 11px; color: #999; margin-top: 14px; line-height: 1.5; }
  #map { flex: 1; height: 100%; }
  .ot-label { background: rgba(255,255,255,.85); border: 0; box-shadow: none; font-size: 11px; font-weight: 700; color: #7A1010; padding: 1px 4px; border-radius: 3px; }
  .ot-label.off { color: #888; font-weight: 400; }
  .ot-label:before { display: none; }
  #map.nolabels .ot-label { display: none; }
  .zoomhint { display: none; }
  @media (max-width: 760px) { .zoomhint { display: block; font-size: 12px; color: #666; margin: -6px 0 10px 0; } }
  .ot-label .pz { display: block; font-size: 9px; font-weight: 400; color: #555; text-align: center; line-height: 1.1; }
  .plz-label { background: #12463C; color: #fff; border: 0; font-size: 11px; font-weight: 700; padding: 2px 6px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,.3); }
  .plz-label:before { display: none; }
  .toast { position: fixed; bottom: 18px; left: 50%; transform: translateX(-50%); background: #222; color: #fff; padding: 9px 14px; border-radius: 6px; font-size: 13px; z-index: 9999; display: none; }
  body.shot aside { display: none; }
  body.shot .leaflet-control-zoom { display: none; }
  @media (max-width: 760px) {
    .layout { flex-direction: column; height: auto; }
    #map { height: 60vh; flex: none; }
    aside { width: 100%; min-width: 0; border-right: 0; border-top: 1px solid #e5e2dd; order: 2; }
    .summary { position: static; }
  }
</style>
</head>
<body>
<div class="layout">
<aside>
  <div class="logo"><div class="mark"></div><div class="word">handzettelverteiler<b>.de</b></div></div>
  <div class="eyebrow">Gebiete auswählen__ANGEBOTSNR__</div>
  <h1>__TITLE__</h1>
  <div class="hint">Klicken Sie in der Karte oder in der Liste auf die Ortsteile, die Sie bewerben möchten. Haushalte und Preis rechnen sich sofort mit. Mit dem Button unten senden Sie uns Ihre Auswahl.</div>
  <div class="zoomhint">Tipp: In die Karte hineinzoomen, dann erscheinen die Ortsteil-Namen.</div>
  <div class="summary">
    <div class="cap">Ihre Auswahl</div>
    <div class="row"><span>Gebiete</span><span class="val" id="sGeb">–</span></div>
    <div class="row"><span>Haushalte (bewerbbar)</span><span class="val" id="sHH">–</span></div>
    <div class="row"><span>Verteilung</span><span class="val" id="sVert">–</span></div>
    <div class="row"><span id="sAnfL">An-/Abfahrt</span><span class="val" id="sAnf">–</span></div>
    <div class="row total"><span>Gesamt netto</span><span class="val" id="sTot">–</span></div>
    <div class="note">Alle Preise zzgl. gesetzl. MwSt. An-/Abfahrt 35 € je PLZ-Region mit mindestens einem gewählten Ortsteil.</div>
    <a class="cta" id="mailBtn" href="#">Auswahl per E-Mail anfragen</a>
  </div>
  <div class="btns"><button type="button" id="bAll">Alle auswählen</button><button type="button" id="bNone">Alle abwählen</button></div>
  <div id="list"></div>
  <div class="footer-note">Haushaltszahlen: bewerbbare Haushalte laut Deutscher Post, auf 50 gerundet. Ortsteilgrenzen: © OpenStreetMap-Mitwirkende, vereinfacht dargestellt. Briefkästen mit „Keine Werbung“ werden nicht beliefert.<br>HZV handzettelverteiler GmbH · Bleichstraße 27 · 66111 Saarbrücken · __MAIL__</div>
</aside>
<div id="map"></div>
</div>
<div class="toast" id="toast"></div>
<script>
__LEAFLET_JS__
</script>
<script>
const DATA = __DATA__;
const CFG = __CFG__;
const QS = new URLSearchParams(location.search);
if (QS.get('shot')) document.body.classList.add('shot');
const fmtHH = n => n.toLocaleString('de-DE');
const fmtEur = n => n.toLocaleString('de-DE', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' €';
const sel = {};
const pre = QS.get('sel');
DATA.areas.forEach(a => sel[a.id] = pre ? pre.split(',').includes(a.id) : !a.aus);

const map = L.map('map', {zoomSnap: 0.25});
const B0 = L.latLngBounds([]); DATA.areas.forEach(a => a.polygons.forEach(r => r.forEach(([x, y]) => B0.extend([y, x]))));
map.fitBounds(B0, {padding: [20, 20]});  // View zuerst setzen, sonst scheitern permanente Tooltips
const Z0 = map.getZoom(), MOBIL = window.innerWidth < 760;
function labelCheck() { document.getElementById('map').classList.toggle('nolabels', MOBIL && map.getZoom() < Z0 + 1); }
map.on('zoomend', labelCheck);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '&copy; OpenStreetMap'}).addTo(map);
const ON = {color: '#7A1010', weight: 1.2, fillColor: '#C81E1E', fillOpacity: 0.32, dashArray: null};
const OFF = {color: '#888', weight: 1, fillColor: '#bbb', fillOpacity: 0.12, dashArray: '4 3'};
const layers = {};
const all = L.featureGroup().addTo(map);
DATA.areas.forEach(a => {
  const ll = a.polygons.map(r => r.map(([x, y]) => [y, x]));
  const lyr = L.polygon(ll, sel[a.id] ? ON : OFF).addTo(all);
  lyr.bindTooltip(a.gebiet + '<span class="pz">' + a.plz + '</span>', {permanent: true, direction: 'center', className: 'ot-label' + (sel[a.id] ? '' : ' off')});
  lyr.on('click', () => toggle(a.id));
  lyr.on('mouseover', () => lyr.setStyle({weight: 2.5}));
  lyr.on('mouseout', () => lyr.setStyle({weight: sel[a.id] ? ON.weight : OFF.weight}));
  layers[a.id] = lyr;
});
Object.entries(DATA.plz).forEach(([p, rings]) => {
  const l = L.polygon(rings.map(r => r.map(([x, y]) => [y, x])), {color: '#12463C', weight: 2.2, fill: false, interactive: false}).addTo(map);
  // PLZ-Schild: Position aus DATA.plz_label (vom Generator berechnet, moeglichst weit weg von den Ortsteil-Namen)
  if (DATA.plz_schilder) {  // optional: eigene PLZ-Schilder (Standard: PLZ steht klein unter jedem Ortsteil-Namen)
    const lp = (DATA.plz_label || {})[p] || [l.getBounds().getCenter().lng, l.getBounds().getCenter().lat];
    L.marker([lp[1], lp[0]], {opacity: 0, interactive: false}).addTo(map)
      .bindTooltip('PLZ ' + p, {permanent: true, direction: 'center', className: 'plz-label'});
  }
});

// Liste je PLZ
const groups = {};
DATA.areas.forEach(a => (groups[a.plz] = groups[a.plz] || []).push(a));
const list = document.getElementById('list');
Object.entries(groups).forEach(([p, arr]) => {
  const g = document.createElement('div'); g.className = 'grp';
  const h = document.createElement('div'); h.className = 'grp-h';
  h.innerHTML = '<input type="checkbox" data-plz="' + p + '"><span>PLZ ' + p + ' · ' + arr[0].ort + '</span><span class="sum" id="gs' + p + '"></span>';
  h.addEventListener('click', e => { const on = !arr.every(a => sel[a.id]); arr.forEach(a => sel[a.id] = on); refresh(); e.preventDefault(); });
  g.appendChild(h);
  arr.forEach(a => {
    const it = document.createElement('div'); it.className = 'it'; it.id = 'it-' + a.id;
    const tag = a.satz <= 98 ? '<br><span class="tag">Innenstadt-Preis</span>' : '';
    it.innerHTML = '<input type="checkbox"><span class="nm">' + a.gebiet + tag + '</span><span class="hh">' + fmtHH(a.hh) + ' HH</span><span class="pr">' + fmtEur(a.preis) + '</span>';
    it.addEventListener('click', e => { toggle(a.id); e.preventDefault(); });
    it.addEventListener('mouseenter', () => layers[a.id].setStyle({weight: 3}));
    it.addEventListener('mouseleave', () => layers[a.id].setStyle({weight: sel[a.id] ? ON.weight : OFF.weight}));
    g.appendChild(it);
  });
  list.appendChild(g);
});

let toastT;
function toast(t) { const el = document.getElementById('toast'); el.textContent = t; el.style.display = 'block'; clearTimeout(toastT); toastT = setTimeout(() => el.style.display = 'none', 1600); }
function toggle(id) { sel[id] = !sel[id]; refresh(); const a = DATA.areas.find(x => x.id === id); toast(a.gebiet + ' (' + a.plz + '): ' + (sel[id] ? 'ausgewählt' : 'abgewählt')); }
document.getElementById('bAll').onclick = () => { DATA.areas.forEach(a => sel[a.id] = true); refresh(); };
document.getElementById('bNone').onclick = () => { DATA.areas.forEach(a => sel[a.id] = false); refresh(); };

function refresh() {
  let hh = 0, vert = 0, n = 0; const plzSet = new Set();
  DATA.areas.forEach(a => {
    const on = sel[a.id];
    layers[a.id].setStyle(on ? ON : OFF);
    const tt = layers[a.id].getTooltip(); if (tt && tt.getElement()) tt.getElement().classList.toggle('off', !on);
    const it = document.getElementById('it-' + a.id); it.classList.toggle('off', !on); it.querySelector('input').checked = on;
    if (on) { hh += a.hh; vert += a.preis; n++; plzSet.add(a.plz); }
  });
  Object.entries(groups).forEach(([p, arr]) => {
    const k = arr.filter(a => sel[a.id]); const cb = document.querySelector('input[data-plz="' + p + '"]');
    cb.checked = k.length === arr.length; cb.indeterminate = k.length > 0 && k.length < arr.length;
    document.getElementById('gs' + p).textContent = k.length ? fmtHH(k.reduce((s, a) => s + a.hh, 0)) + ' HH' : '–';
  });
  const anf = 35 * plzSet.size, tot = Math.round((vert + anf) * 100) / 100;
  document.getElementById('sGeb').textContent = n + ' von ' + DATA.areas.length;
  document.getElementById('sHH').textContent = fmtHH(hh);
  document.getElementById('sVert').textContent = fmtEur(vert);
  document.getElementById('sAnfL').textContent = 'An-/Abfahrt (' + plzSet.size + ' × 35 €)';
  document.getElementById('sAnf').textContent = fmtEur(anf);
  document.getElementById('sTot').textContent = fmtEur(tot);
  const btn = document.getElementById('mailBtn');
  btn.setAttribute('aria-disabled', n ? 'false' : 'true');
  const lines = DATA.areas.filter(a => sel[a.id]).map(a => '- PLZ ' + a.plz + ' ' + a.gebiet + ': ' + fmtHH(a.hh) + ' HH, ' + fmtEur(a.preis));
  const body = 'Guten Tag,\n\nwir möchten folgende Gebiete' + (CFG.nr ? ' aus Angebot ' + CFG.nr : '') + ' beauftragen bzw. anfragen:\n\n' + lines.join('\n')
    + '\n\nHaushalte gesamt: ' + fmtHH(hh) + '\nVerteilung: ' + fmtEur(vert) + '\nAn-/Abfahrt (' + plzSet.size + ' PLZ-Regionen): ' + fmtEur(anf)
    + '\nGesamt netto: ' + fmtEur(tot) + ' zzgl. MwSt.\n\nWunschtermin: \nFlyerformat / Druck gewünscht: \n\nMit freundlichen Grüßen\n';
  const subj = 'Gebietsauswahl' + (CFG.nr ? ' zu Angebot ' + CFG.nr : '') + (CFG.kunde ? ' – ' + CFG.kunde : '');
  btn.href = 'mailto:' + CFG.mail + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
  const ids = DATA.areas.filter(a => sel[a.id]).map(a => a.id);
  try { history.replaceState(null, '', location.pathname + '?' + (QS.get('shot') ? 'shot=1&' : '') + 'sel=' + ids.join(',')); } catch (e) {}
}
refresh();
labelCheck();
</script>
</body>
</html>
"""


def plz_label_punkte(data):
    """Je PLZ einen Punkt im Inneren, moeglichst weit weg von den Ortsteil-Beschriftungen (Schwerpunkte) und vom Rand."""
    from shapely.geometry import Polygon, Point
    cents = []
    for ar in data["areas"]:
        polys = [Polygon(r) for r in ar["polygons"] if len(r) > 3]
        if polys:
            big = max(polys, key=lambda q: q.area)
            cents.append(big.centroid)  # Leaflet setzt Tooltips 'center' etwa auf den Schwerpunkt
    out = {}
    for plz, rings in data["plz"].items():
        P = Polygon(rings[0]).buffer(0)
        minx, miny, maxx, maxy = P.bounds
        best, bestd = None, -1
        n = 40
        for i in range(n + 1):
            for j in range(n + 1):
                pt = Point(minx + (maxx - minx) * i / n, miny + (maxy - miny) * j / n)
                if not P.contains(pt):
                    continue
                edge = P.exterior.distance(pt)
                if edge < 0.004:
                    continue
                d = min([((c.x - pt.x) / 2.6) ** 2 + (c.y - pt.y) ** 2 for c in cents] + [(edge * 0.8) ** 2])  # Schilder sind breit: x-Abstand weniger gewichten
                if d > bestd:
                    best, bestd = pt, d
        if best is None:
            best = P.representative_point()
        out[plz] = [round(best.x, 5), round(best.y, 5)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--title", required=True, help="HTML erlaubt (&amp;)")
    ap.add_argument("--angebotsnr", default="")
    ap.add_argument("--kunde", default="")
    ap.add_argument("--mail", default="info@handzettelverteiler.de")
    ap.add_argument("--leaflet-dir", default="/tmp/leaflet_pkg/node_modules/leaflet/dist")
    a = ap.parse_args()
    data = json.load(open(a.input, encoding="utf-8"))
    if "plz_label" not in data:
        data["plz_label"] = plz_label_punkte(data)
    css = open(os.path.join(a.leaflet_dir, "leaflet.css"), encoding="utf-8").read()
    js = open(os.path.join(a.leaflet_dir, "leaflet.js"), encoding="utf-8").read()
    import re
    plain = re.sub(r"<[^>]+>", "", a.title).replace("&amp;", "&").replace("&ndash;", "–")
    cfg = {"nr": a.angebotsnr, "kunde": a.kunde, "mail": a.mail}
    html = (TEMPLATE.replace("__LEAFLET_CSS__", css).replace("__LEAFLET_JS__", js)
            .replace("__TITLE_PLAIN__", plain).replace("__TITLE__", a.title)
            .replace("__ANGEBOTSNR__", f" · Angebot {a.angebotsnr}" if a.angebotsnr else "")
            .replace("__MAIL__", a.mail)
            .replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            .replace("__CFG__", json.dumps(cfg, ensure_ascii=False)))
    open(a.output, "w", encoding="utf-8").write(html)
    hh = sum(x["hh"] for x in data["areas"]); pr = sum(x["preis"] for x in data["areas"])
    anf = 35 * len({x["plz"] for x in data["areas"]})
    print(f"Geschrieben: {a.output} ({len(html)} bytes) – {len(data['areas'])} Gebiete, {hh:,} HH, Verteilung {pr:.2f} + Anfahrt {anf} = {pr+anf:.2f}".replace(",", "."))


if __name__ == "__main__":
    main()
