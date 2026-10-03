#!/usr/bin/env python3
"""Patcht rId0 -> rId1 in Footer-Relationen (sonst verschwinden Footer-Bilder in Apache OpenOffice)."""
import sys, zipfile, shutil, re, os, tempfile
src = sys.argv[1]
tmp = tempfile.mktemp(suffix=".docx")
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    n = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if re.match(r"word/_rels/footer\d+\.xml\.rels$", item.filename):
            new = data.replace(b'Id="rId0"', b'Id="rId1"'); n += new != data; data = new
        elif re.match(r"word/footer\d+\.xml$", item.filename):
            new = data.replace(b'r:embed="rId0"', b'r:embed="rId1"'); n += new != data; data = new
        zout.writestr(item, data)
shutil.move(tmp, src)
print(f"fix_rid0: {n} Datei(en) gepatcht")
