"""Neue Standardfigur (blaues Strichmännchen, Basecap leicht schräg) in bestehende Stadtbilder einsetzen.
Basis ist immer Stadt_<Slug>.jpg (ohne Lupe); daraus entstehen Seite 3 (Einwurf 'Ihr Flyer') und Seite 4 (Lupe)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import figuren as f, basecap2 as bc, lupe2 as lp

W, H = 1600, 873
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "final")

def clean_base(path):
    im = Image.open(path).convert("RGB").resize((W, H))
    d = ImageDraw.Draw(im)
    d.rectangle([1058, 432, 1304, 866], fill="white")      # alter Briefkasten
    d.rectangle([1238, 196, W, H], fill="white")           # alte Figur + Arm
    # Fluss rechts neu (Verlauf wie im Original)
    def top(x): return 618 + (x - 1040) * 0.0145
    def bot(x): return 713 + (x - 1040) * 0.0545
    d.polygon([(1056, top(1056)), (W, top(W)), (W, bot(W)), (1056, bot(1056))], fill=(184, 219, 235))
    for x, y in ((1110, 664), (1340, 690), (1500, 704)):
        d.arc([x, y - 6, x + 16, y + 6], 200, 340, fill=(58, 111, 176), width=3)
        d.arc([x + 16, y - 6, x + 32, y + 6], 20, 160, fill=(58, 111, 176), width=3)
    return im

def compose(base, svg_body, name):
    fg = f.render(f.svgwrap(svg_body), os.path.join(OUT, "_tmp.png"))
    img = base.convert("RGBA"); img.alpha_composite(fg)
    img.convert("RGB").save(os.path.join(OUT, name), quality=90)

def build(slug, src):
    os.makedirs(OUT, exist_ok=True)
    base = clean_base(src)
    compose(base, bc.scene(bc.cap_schraeg), f"Stadt_{slug}.jpg")
    compose(base, lp.scene_lupe(), f"Stadt_{slug}_Lupe.jpg")
    print(slug)

if __name__ == "__main__":
    STAEDTE = os.environ.get("HZV_STAEDTE", "/home/claude/hzv-karten/staedte")
    for slug in sys.argv[1:]:
        src = os.path.join(STAEDTE, f"Stadt_{slug}.jpg")
        if not os.path.exists(src):
            src = os.path.join(os.path.dirname(OUT), f"Stadt_{slug}.jpg")
        build(slug, src)
