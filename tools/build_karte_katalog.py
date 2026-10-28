#!/usr/bin/env python3
"""
HZV Katalog-Karte: viele PLZ-Regionen zur freien Auswahl durch den Kunden (z. B. Möbel Jobst, 4 Landkreise).
Anders als build_karte.py gibt es hier KEINE feste Gesamtsumme: der Kunde klickt Gebiete an (oder ganze
Landkreise) und sieht live Haushalte, Verteilpreis je Gewichtsklasse und An-/Abfahrt seiner Auswahl.
"Auswahl per E-Mail senden" öffnet eine Mail an info@handzettelverteiler.de mit der PLZ-Liste.

Input-JSON (Liste): {plz, gebiet, kreis, hh_bewerbbar, hh_gesamt, quote, preise:[p1,p2,p3], anfahrt, geometry:{GeoJSON}}

Aufruf:
  python3 build_karte_katalog.py --input areas.json --output Kunde_Karte_v1_Info.html \
     --title "Möbel Jobst &ndash; Verteilgebiete zur Auswahl" --klassen "20–30 g" "31–40 g" "41–50 g" \
     --leaflet-dir /home/claude/leaflet_pkg/node_modules/leaflet/dist [--highlight-plz 83301 --hide-sidebar]
URL-Parameter: ?shot=1 (Sidebar aus), ?shot=1&plz=83301 (eine PLZ blau, Zoom)
"""
import argparse, json

FARBEN = ["#C81E1E", "#1F6FB2", "#2E8B57", "#D17A00", "#7B3FA0", "#00838F", "#8D6E63"]

TEMPLATE = r"""<!DOCTYPE html>
<html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE_PLAIN__ &ndash; handzettelverteiler Kartentool</title>
<style>__LEAFLET_CSS__</style>
<style>
*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#222;background:#F7F6F3}
.layout{display:flex;height:100vh}aside{width:340px;min-width:340px;background:#fff;border-right:1px solid #e5e2dd;padding:18px;overflow-y:auto;display:__SIDEBAR_DISPLAY__}
#map{flex:1}.logo{display:flex;align-items:center;gap:8px}.logo .mark{width:30px;height:30px;background:#C81E1E;border-radius:6px;color:#fff;display:flex;align-items:center;justify-content:center}
.logo .word{font-size:18px;font-weight:700}.logo .word b{color:#C81E1E}.eyebrow{font-size:12px;color:#888;margin:10px 0 2px}
h1{margin:0 0 8px;font-size:18px;line-height:1.3}.lede{font-size:13px;color:#555;line-height:1.5;margin-bottom:12px}
.sum{background:#12463C;color:#fff;border-radius:8px;padding:14px;margin-bottom:12px}.sum .cap{font-size:12px;opacity:.8;margin-bottom:6px}
.sum .row{display:flex;justify-content:space-between;font-size:13px;padding:3px 0}.sum .row.big{font-size:15px;font-weight:700;border-top:1px solid rgba(255,255,255,.3);margin-top:4px;padding-top:6px}
.sum .note{font-size:11px;opacity:.75;margin-top:6px;line-height:1.4}
.btn{display:block;width:100%;text-align:center;border:0;border-radius:6px;padding:9px;font-size:13px;font-weight:700;cursor:pointer;margin-top:8px;text-decoration:none}
.btn.w{background:#fff;color:#12463C}.btn.g{background:#eee;color:#333}
.kreis{border:1px solid #e5e2dd;border-radius:8px;margin-bottom:8px;overflow:hidden}
.kreis .head{display:flex;align-items:center;gap:8px;padding:8px 10px;background:#FAFAF8;cursor:pointer;font-size:13px}
.kreis .sw{width:14px;height:14px;border-radius:3px;flex-shrink:0}.kreis .head .n{margin-left:auto;color:#777;font-size:12px}
.kreis .list{display:none;padding:4px 10px 8px}.kreis.open .list{display:block}
.item{display:flex;gap:6px;align-items:center;font-size:12px;padding:3px 0;border-bottom:1px solid #f1efeb}
.item span.hh{margin-left:auto;color:#555}.kbtn{font-size:11px;border:1px solid #ccc;background:#fff;border-radius:4px;padding:2px 6px;cursor:pointer}
.plz-label{background:transparent;border:0;box-shadow:none;font-size:10px;font-weight:700;color:#222;text-shadow:0 0 3px #fff,0 0 3px #fff}
.plz-label:before{display:none}.leaflet-popup-content{font-size:13px}.leaflet-popup-content b{color:#C81E1E}
table.info{border-collapse:collapse;margin-top:6px}table.info td{padding:2px 6px 2px 0}table.info td.v{text-align:right;font-weight:700}
.legend{background:#fff;padding:6px 10px;border-radius:6px;font:12px Arial;box-shadow:0 1px 4px rgba(0,0,0,.3);line-height:1.7}
.legend i{display:inline-block;width:14px;height:10px;margin-right:6px;vertical-align:middle;border-radius:2px}
body.shot aside{display:none}body.shot .leaflet-control-zoom{display:none}
.footer-note{font-size:11px;color:#999;margin-top:14px;line-height:1.5}
@media (max-width:760px){.layout{flex-direction:column-reverse;height:auto}#map{height:62vh;flex:none}aside{width:100%;min-width:0}}
</style></head><body>
<div class="layout"><aside>
<div class="logo"><div class="mark">&#9993;</div><div class="word">handzettelverteiler<b>.de</b></div></div>
<div class="eyebrow">Ihre Verteilgebiete zur Auswahl</div><h1>__TITLE__</h1><div class="lede">__LEDE__</div>
<div class="sum"><div class="cap">Ihre Auswahl</div>
<div class="row"><span>PLZ-Regionen</span><span id="sN">0</span></div>
<div class="row"><span>Haushalte bewerbbar</span><span id="sHH">0</span></div>
<div id="sPreise"></div>
<div class="row"><span>An-/Abfahrt (35 € je PLZ)</span><span id="sAnf">0 €</span></div>
<div class="note">Verteilpreise je Prospektgewicht, An-/Abfahrt kommt einmal je gebuchter PLZ-Region hinzu. Alle Preise netto zzgl. MwSt.</div>
<a class="btn w" id="mail" href="#">Auswahl per E-Mail senden</a>
<button class="btn g" id="clear">Auswahl leeren</button></div>
<div id="kreise"></div>
<div class="footer-note">Gebiet anklicken = auswählen / abwählen. Haushaltszahlen auf volle 50 gerundet (Quelle: Deutsche Post, Stand __STAND__).</div>
</aside><div id="map"></div></div>
<script>__LEAFLET_JS__</script>
<script>
const DATA=__DATA__, KLASSEN=__KLASSEN__, FARBEN=__FARBEN__, MAIL='__MAIL__', KUNDE='__KUNDE__';
const QS=new URLSearchParams(location.search), SHOT=QS.get('shot')==='1';
let HL=QS.get('plz')||'__HIGHLIGHT_PLZ__'; if(HL.indexOf('__')===0) HL='';
if(SHOT) document.body.classList.add('shot');
const fmtHH=n=>n.toLocaleString('de-DE'), fmtE=n=>n.toLocaleString('de-DE',{minimumFractionDigits:2,maximumFractionDigits:2})+' €';
const kreise=[...new Set(DATA.map(a=>a.kreis))], farbe=k=>FARBEN[kreise.indexOf(k)%FARBEN.length];
const sel=new Set(), layers={};
const map=L.map('map',{zoomControl:true,zoomSnap:SHOT?0.1:1}).setView([48,12.5],9);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
function style(a){const c=farbe(a.kreis);
 if(HL) return a.plz===HL?{color:'#0B3D91',weight:3,fillColor:'#1E6FD9',fillOpacity:.35,opacity:1}:{color:c,weight:1,opacity:.35,fillColor:c,fillOpacity:.08};
 return sel.has(a.plz)?{color:'#111',weight:2.5,fillColor:c,fillOpacity:.6,opacity:1}:{color:c,weight:1.2,opacity:.9,fillColor:c,fillOpacity:.22};}
function popup(a){return `<b>PLZ ${a.plz} &ndash; ${a.gebiet}</b><br><span style="color:#666">${a.kreis}</span><table class="info">
 <tr><td>Haushalte bewerbbar</td><td class="v">${fmtHH(a.hh_bewerbbar)}</td></tr><tr><td>Haushalte gesamt</td><td class="v">${fmtHH(a.hh_gesamt)}</td></tr>
 <tr><td>Bewerbungsquote</td><td class="v">${a.quote} %</td></tr>${KLASSEN.map((k,i)=>`<tr><td>Verteilung ${k}</td><td class="v">${fmtE(a.preise[i])}</td></tr>`).join('')}
 <tr><td>An-/Abfahrt</td><td class="v">${fmtE(a.anfahrt)}</td></tr></table>`;}
let target=null; const group=L.featureGroup().addTo(map);
DATA.forEach(a=>{const l=L.geoJSON({type:'Feature',geometry:a.geometry},{style:()=>style(a)});
 l.bindPopup(popup(a)); l.bindTooltip(a.plz,{permanent:true,direction:'center',className:'plz-label'});
 if(!HL) l.on('click',e=>{toggle(a.plz);});
 l.addTo(group); layers[a.plz]=l; if(HL&&a.plz===HL) target=l;});
function fit(){ if(target) map.fitBounds(target.getBounds(),{padding:[40,40]}); else map.fitBounds(group.getBounds(),{padding:[20,20]}); }
fit(); setTimeout(()=>{map.invalidateSize();fit();},60);
function labels(){const z=map.getZoom(); document.querySelectorAll('.plz-label').forEach(el=>el.style.display=(z>=9.6||HL)?'':'none');}
map.on('zoomend',labels); setTimeout(labels,100);
const lg=L.control({position:'bottomleft'}); lg.onAdd=()=>{const d=L.DomUtil.create('div','legend'); d.innerHTML=kreise.map(k=>`<i style="background:${farbe(k)}"></i>${k}`).join('<br>'); return d;}; if(!HL) lg.addTo(map);
function toggle(p,force){ if(force===true) sel.add(p); else if(force===false) sel.delete(p); else sel.has(p)?sel.delete(p):sel.add(p);
 const a=DATA.find(x=>x.plz===p); layers[p].setStyle(style(a)); const cb=document.getElementById('cb'+p); if(cb) cb.checked=sel.has(p); upd(); }
function upd(){const A=DATA.filter(a=>sel.has(a.plz));
 document.getElementById('sN').textContent=A.length; document.getElementById('sHH').textContent=fmtHH(A.reduce((s,a)=>s+a.hh_bewerbbar,0));
 document.getElementById('sPreise').innerHTML=KLASSEN.map((k,i)=>`<div class="row big"><span>Verteilung ${k}</span><span>${fmtE(A.reduce((s,a)=>s+a.preise[i],0))}</span></div>`).join('');
 document.getElementById('sAnf').textContent=fmtE(A.reduce((s,a)=>s+a.anfahrt,0));
 const body='Guten Tag,\n\nfür unsere nächste Prospektverteilung wählen wir folgende PLZ-Regionen ('+A.length+' PLZ, '+fmtHH(A.reduce((s,a)=>s+a.hh_bewerbbar,0))+' Haushalte):\n\n'+A.map(a=>a.plz+' '+a.gebiet).join('\n')+'\n\nProspektgewicht: ___ g\nWunschzeitraum: ___\n\nViele Grüße\n'+KUNDE;
 document.getElementById('mail').href='mailto:'+MAIL+'?subject='+encodeURIComponent('Gebietsauswahl Prospektverteilung '+KUNDE)+'&body='+encodeURIComponent(body);}
const kEl=document.getElementById('kreise');
kreise.forEach(k=>{const A=DATA.filter(a=>a.kreis===k); const d=document.createElement('div'); d.className='kreis';
 d.innerHTML=`<div class="head"><span class="sw" style="background:${farbe(k)}"></span><b>${k}</b><span class="n">${A.length} PLZ · ${fmtHH(A.reduce((s,a)=>s+a.hh_bewerbbar,0))} HH</span></div>
 <div class="list"><div style="margin:4px 0 6px"><button class="kbtn" data-a="1">alle wählen</button> <button class="kbtn" data-a="0">keine</button></div>
 ${A.map(a=>`<label class="item"><input type="checkbox" id="cb${a.plz}"> <b>${a.plz}</b> ${a.gebiet}<span class="hh">${fmtHH(a.hh_bewerbbar)}</span></label>`).join('')}</div>`;
 d.querySelector('.head').onclick=()=>d.classList.toggle('open');
 d.querySelectorAll('.kbtn').forEach(b=>b.onclick=()=>A.forEach(a=>toggle(a.plz,b.dataset.a==='1')));
 A.forEach(a=>d.querySelector('#cb'+a.plz).onchange=e=>toggle(a.plz,e.target.checked));
 kEl.appendChild(d);});
document.getElementById('clear').onclick=()=>[...sel].forEach(p=>toggle(p,false));
upd();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True); ap.add_argument("--output", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--lede", default="Wählen Sie für jede Aktion die gewünschten PLZ-Regionen per Klick in der Karte oder ganze Landkreise in der Liste – Haushalte und Preise Ihrer Auswahl sehen Sie sofort.")
    ap.add_argument("--klassen", nargs="+", default=["20–30 g", "31–40 g", "41–50 g"])
    ap.add_argument("--kunde", default=""); ap.add_argument("--mail", default="info@handzettelverteiler.de")
    ap.add_argument("--stand", default="")
    ap.add_argument("--leaflet-dir", default="/tmp/leaflet_pkg/node_modules/leaflet/dist")
    ap.add_argument("--highlight-plz", default=""); ap.add_argument("--hide-sidebar", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.input, encoding="utf-8"))
    keep = ["plz", "gebiet", "kreis", "hh_bewerbbar", "hh_gesamt", "quote", "preise", "anfahrt", "geometry"]
    data = [{k: d[k] for k in keep} for d in data]
    html = TEMPLATE
    rep = {
        "__LEAFLET_CSS__": open(f"{a.leaflet_dir}/leaflet.css").read(),
        "__LEAFLET_JS__": open(f"{a.leaflet_dir}/leaflet.js").read(),
        "__TITLE_PLAIN__": a.title.replace("&ndash;", "-"), "__TITLE__": a.title, "__LEDE__": a.lede,
        "__SIDEBAR_DISPLAY__": "none" if a.hide_sidebar else "block", "__STAND__": a.stand,
        "__KLASSEN__": json.dumps(a.klassen, ensure_ascii=False), "__FARBEN__": json.dumps(FARBEN),
        "__MAIL__": a.mail, "__KUNDE__": a.kunde.replace("'", "\\'"), "__HIGHLIGHT_PLZ__": a.highlight_plz,
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    open(a.output, "w", encoding="utf-8").write(html)
    print(f"Geschrieben: {a.output} ({len(html)} bytes), {len(data)} Gebiete, HH {sum(d['hh_bewerbbar'] for d in data):,}")


if __name__ == "__main__":
    main()
