#!/usr/bin/env python3
"""Ersetzt in bestehenden Karten den alten Button 'Jetzt anfragen' (-> handzettelverteiler.de/kontakt)
durch 'Jetzt beauftragen' (vorausgefuellte Auftrags-E-Mail) + 'Anfrage / Rueckfrage senden' (handzettelverteiler.com)
+ E-Mail-Adresse. Aufruf: python3 tools/fix_cta.py *.html   (Stefan, 09.11.2026)"""
import re, sys, html as H, os
sys.path.insert(0, os.path.dirname(__file__))
from build_karte import cta_block
CSS = """  .cta.cta2 { background: transparent; color: #fff; border: 1.5px solid #fff; margin-top: 8px; font-weight: 600; }
  .cta.cta2:hover { background: rgba(255,255,255,.12); }
  .ctamail { text-align: center; font-size: 12px; margin-top: 8px; opacity: .9; }
  .ctamail a { color: #fff; }
"""
n = 0
for f in sys.argv[1:]:
    s = open(f, encoding="utf-8").read()
    m = re.search(r'[ \t]*<a class="cta" href="https?://(www\.)?handzettelverteiler\.de/kontakt/?"[^>]*>Jetzt anfragen</a>', s)
    if not m: continue
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    title = H.unescape(t.group(1)).split(" – handzettelverteiler")[0].strip() if t else "Verteilgebiete"
    g = re.search(r'<div class="row total"><span>Gesamtsumme</span><span class="val">([^<]*)</span>', s)
    gesamt = H.unescape(g.group(1)).replace("\xa0", " ") if g else ""
    s = s[:m.start()] + cta_block(title, "", gesamt) + s[m.end():]
    if ".cta.cta2" not in s:
        s = s.replace("  .cta:hover { background: #eee; }\n", "  .cta:hover { background: #eee; }\n" + CSS, 1)
    open(f, "w", encoding="utf-8").write(s); n += 1
print(f"{n} Karte(n) umgestellt")
