# Ortsteil-Grenzen für die Auswahlkarte (Stefan, 19.11.2026)

Die Sandbox erreicht Nominatim/Overpass nicht – die Ortsteil-Polygone kommen über Claude in Chrome.

## 1. In Chrome holen (Tab auf https://nominatim.openstreetmap.org/ui/about.html, dann javascript_tool)

```js
const L=[["Dankersen","Minden"],["Hausberge","Porta Westfalica"] /* … alle Ortsteile [Name, Stadt] … */];
window.__geo={}; let rep=[];
for (const [n,c] of L){ const r=await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(n+', '+c)}&format=jsonv2&polygon_geojson=1&polygon_threshold=0.0002&limit=5&countrycodes=de`).then(r=>r.json());
 const hit=r.find(x=>x.geojson&&/Polygon/.test(x.geojson.type));
 if(hit){window.__geo[c+'|'+n]={g:hit.geojson}; rep.push(n+': '+hit.addresstype);} else rep.push(n+': NONE');
 await new Promise(r=>setTimeout(r,1200)); }
rep.join('\n')
```
Nur Treffer mit addresstype suburb/village/quarter verwenden (z. B. „amenity“ = falsch → weglassen).

## 2. Kompakt kodieren und als Seitentext ausgeben (javascript_tool), dann get_page_text

```js
function dp(pts,eps){if(pts.length<3)return pts;let dmax=0,idx=0;const [x1,y1]=pts[0],[x2,y2]=pts[pts.length-1];for(let i=1;i<pts.length-1;i++){const [x,y]=pts[i];const den=Math.hypot(y2-y1,x2-x1);const d=den<1e-12?Math.hypot(x-x1,y-y1):Math.abs((y2-y1)*x-(x2-x1)*y+x2*y1-y2*x1)/den;if(d>dmax){dmax=d;idx=i;}}if(dmax>eps){const a=dp(pts.slice(0,idx+1),eps),b=dp(pts.slice(idx),eps);return a.slice(0,-1).concat(b);}return [pts[0],pts[pts.length-1]];}
function enc(pts){let s='',px=0,py=0;for(const [x,y] of pts){const X=Math.round(x*1e4),Y=Math.round(y*1e4);for(let v of [Y-py,X-px]){v=v<0?~(v<<1):(v<<1);while(v>=0x20){s+=String.fromCharCode((0x20|(v&0x1f))+63);v>>=5;}s+=String.fromCharCode(v+63);}px=X;py=Y;}return s;}
const out=[];for(const k in window.__geo){const g=window.__geo[k].g;const polys=g.type==='Polygon'?[g.coordinates]:g.coordinates;out.push(k+'='+polys.map(p=>enc(dp(p[0],0.00025))).join('~'));}
document.body.innerHTML='<pre></pre>'; document.querySelector('pre').textContent=out.join('\n'); out.length
```
(`javascript_tool` kürzt lange Rückgaben – deshalb über den Seitentext. ~30 Ortsteile ≈ 5 KB.)

## 3. In der Sandbox

Text exakt in eine Datei schreiben (quoted heredoc), dann
`python3 tools/ortsteile/decode.py ortsteile_enc.txt ortsteile.json` (prüft, dass jeder Ring geschlossen ist; Mehrteil-Ortsteile werden am richtigen `~` getrennt),
dann `python3 tools/ortsteile/auswahl_daten.py --rows rows.json --ortsteile ortsteile.json --plz-geojson postleitzahlen.geojson.br --out auswahl.json`
und `python3 tools/build_karte_auswahl.py --input auswahl.json …`.

„Innenstadt“-Zeilen (Post fasst die Kernstadt so zusammen) = PLZ-Fläche minus alle benannten Ortsteile.

## Test 24.11.2026: Grenzen direkt aus POSTAKTUELL (Stefan: „gerne testen“)

- Tab **Ortsteile**: liefert nur eine Tabelle (PLZ, Gemeinde, Ortsteil, Haushalte) – **keine Polygone**. Nützlich, weil jede
  Ortschaft ihrer Gemeinde zugeordnet ist (z. B. 04838: Mörtitz → Doberschütz) – besser als der Tooltip im PLZ-Tab.
- Tab **Zustellbezirke** (Umkreisselektion um eine Adresse, Radius-Schieber oder Auflage): liefert echte
  **MultiPolygone je Zustellbezirk** (z. B. 04838-05 … 04838-08) in `map.getFeatures()` (EPSG:3857), Eigenschaft `name` =
  Bezirk, `description` = Bewerbbare HH, HH ohne Werbung, INSGESAMT und Straßenliste. Test Torgauer Str. 1, Eilenburg, 1 km:
  4 Bezirke, 3.355 bew. HH.
- Folgerung: Für Kernstädte/Umkreis-Angebote können Karte und Haushalte exakt aus den Post-Zustellbezirken kommen
  (Koordinaten per `ol.proj.toLonLat` umrechnen, kodieren wie oben, per get_page_text übernehmen). Für Dörfer bleibt
  Nominatim/Voronoi die Näherung, bis die Bezirke ganzer PLZ abgefragt werden (Radius groß genug wählen).
