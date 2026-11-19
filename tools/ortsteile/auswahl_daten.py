#!/usr/bin/env python3
"""Baut auswahl.json fuer tools/build_karte_auswahl.py.
--rows: Angebots-areas (je Ortsteil: plz, id, gebiet, hh_bewerbbar, preis_verteilung); gebiet "…Innenstadt…" = PLZ minus benannte Ortsteile
--ortsteile: Ausgabe von decode.py ({"Stadt|Ortsteil": [ring,...]})
--stadt-je-plz: JSON {"32457": "Porta Westfalica"} fuer PLZ, deren Ortsteile unter einer anderen Stadt stehen (Standard: erste Stadt im Ortsteil-Schluessel, der passt)
"""
import argparse, json, brotli
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union

ap = argparse.ArgumentParser()
ap.add_argument("--rows", required=True); ap.add_argument("--ortsteile", required=True)
ap.add_argument("--plz-geojson", required=True); ap.add_argument("--out", required=True)
a = ap.parse_args()
ot = {k: MultiPolygon([Polygon(r) for r in v]).buffer(0) for k, v in json.load(open(a.ortsteile)).items()}
rows = json.load(open(a.rows))
plzs = sorted({r["plz"] for r in rows})
d = json.loads(brotli.decompress(open(a.plz_geojson, "rb").read()))
P = {f["properties"]["postcode"]: shape(f["geometry"]).buffer(0) for f in d["features"] if f["properties"].get("postcode") in plzs}
allOT = unary_union(list(ot.values()))
by_name = {}
for k in ot:
    by_name.setdefault(k.split("|", 1)[1], []).append(k)
out = []
for r in rows:
    name = r["gebiet"]
    if "Innenstadt" in name:
        g = P[r["plz"]].difference(allOT); ort = name.split("-")[0]
    else:
        keys = by_name.get(name, [])
        # Ortsteil mit groesster Ueberlappung zur PLZ nehmen (gleichnamige Orte in Nachbarstaedten)
        k = max(keys, key=lambda kk: ot[kk].intersection(P[r["plz"]]).area)
        g = ot[k].intersection(P[r["plz"]]); ort = k.split("|")[0]
    g = g.buffer(0)
    parts = [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
    mx = max(p.area for p in parts)
    parts = [p.simplify(0.0001) for p in parts if p.area > 0.03 * mx]
    satz = round(r["preis_verteilung"] / r["hh_bewerbbar"] * 1000)
    out.append(dict(id=r.get("id") or r["plz"], plz=r["plz"], gebiet=name, ort=ort, hh=r["hh_bewerbbar"], preis=r["preis_verteilung"], satz=satz,
                    polygons=[[[round(x, 5), round(y, 5)] for x, y in p.exterior.coords] for p in parts]))
outl = {p: [[[round(x, 5), round(y, 5)] for x, y in (g if g.geom_type == "Polygon" else max(g.geoms, key=lambda q: q.area)).simplify(0.00015).exterior.coords]] for p, g in P.items()}
json.dump(dict(areas=out, plz=outl), open(a.out, "w"), ensure_ascii=False)
print(f"{len(out)} Gebiete -> {a.out}")
