#!/usr/bin/env python3
"""Macht aus den Kaestchen (U+2610) der Preistabelle im Angebots-PDF klickbare Formular-Checkboxen.
Aufruf: python3 tools/pdf_ankreuzfelder.py <angebot.pdf>   (ueberschreibt die Datei)
Kunde kann dann in Acrobat/Browser/Vorschau ankreuzen, speichern und zuruecksenden. (Stefan, 19.11.2026)
"""
import sys, pdfplumber, pikepdf
from pikepdf import Name, Dictionary, Array

def boxes(path):
    out = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages):
            h = page.height
            for ch in page.chars:
                if ch["text"] == "☐":
                    out.append((pno, ch["x0"], h - ch["bottom"], ch["x1"], h - ch["top"], ch["size"]))
    return out

def ap(pdf, w, h, checked):
    s = f"1 1 1 rg 0.5 0.5 {w-1:.2f} {h-1:.2f} re f 0.27 0.27 0.27 RG 0.8 w 0.5 0.5 {w-1:.2f} {h-1:.2f} re S"
    if checked:
        s += f" 0.78 0.12 0.12 RG 1.6 w {w*0.2:.2f} {h*0.52:.2f} m {w*0.42:.2f} {h*0.25:.2f} l {w*0.82:.2f} {h*0.8:.2f} l S"
    st = pikepdf.Stream(pdf, s.encode())
    st.Type = Name.XObject; st.Subtype = Name.Form; st.BBox = Array([0, 0, w, h])
    return st

def main(path):
    found = boxes(path)
    if not found:
        print("Keine Kaestchen gefunden."); return
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    fields = []
    for i, (pno, x0, y0, x1, y1, fs) in enumerate(found):
        # Glyph-Box etwas einruecken, quadratisch
        # Lage des Kaestchens im Glyph (DejaVu/Segoe, gemessen): Mitte ~0,39 em rechts von x0 und unter Oberkante, Kantenlaenge ~0,64 em
        size = 0.74 * fs                 # etwas groesser, damit das gedruckte Kaestchen verdeckt wird
        cx, cy = x0 + 0.39 * fs, y1 - 0.39 * fs
        rect = [cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2]
        w = h = size
        page = pdf.pages[pno]
        widget = pdf.make_indirect(Dictionary(
            Type=Name.Annot, Subtype=Name.Widget, FT=Name.Btn, T=pikepdf.String(f"auswahl_{i+1}"),
            Rect=Array(rect), F=4, V=Name.Off, AS=Name.Off, P=page.obj,
            MK=Dictionary(CA=pikepdf.String("4")),
            AP=Dictionary(N=Dictionary(Yes=ap(pdf, w, h, True), Off=ap(pdf, w, h, False)),
                          D=Dictionary(Yes=ap(pdf, w, h, True), Off=ap(pdf, w, h, False)))))
        if "/Annots" not in page.obj:
            page.obj.Annots = Array()
        page.obj.Annots.append(widget)
        fields.append(widget)
    pdf.Root.AcroForm = Dictionary(Fields=Array(fields), NeedAppearances=False)
    pdf.save(path)
    print(f"{len(fields)} Ankreuzfelder eingefuegt.")

if __name__ == "__main__":
    main(sys.argv[1])
