"""Kleinere Orte – bei Bedarf hier eine Zeile ergänzen und `python3 orte_klein.py <Slug>` ausführen."""
import sys
import stadtbild as sb, final
from elemente import *
import staedte_101_200 as gross

C = {}
def reg(slug, namen, fn): C[slug] = (namen, fn)
basis = gross.basis

reg("Deidesheim", ["Deidesheim"], lambda: basis(201) + weinberg(0, 380, 150) + freitreppen_rathaus(420, 170, 120) + kirche(680, 180, 130, SAND, SLATE, "spire"))
reg("Hassloch", ["Haßloch", "Hassloch"], lambda: basis(202) + fachwerk(40, 3) + kirche(260, 200, 140, WHITE, SLATE, "spire", "center", 56, 270) + achterbahn(540, 280, 150) + weinberg(830, 200, 90))
reg("Wiesloch", ["Wiesloch"], lambda: basis(203) + weinberg(0, 340, 140) + kirche(380, 200, 140, WHITE, SLATE, "spire", "center", 56, 270) + rathaus(650, 150, 120, YELLOW, "baroque"))
reg("Eschborn", ["Eschborn", "Niederhöchstadt", "Niederhoechstadt"], lambda: basis(205) + fachwerk(30, 3) + kirche(220, 190, 140, WHITE, SLATE, "spire", "center", 56, 260) + turm(450, 46, 190, "#c9b27c", "flat") + hochhaus(560, 70, 270) + modern(640, 150, 150, "#d6e6f2") + hochhaus(800, 60, 220, "#bcd3e6", True))
reg("Leimen", ["Leimen"], lambda: basis(204) + weinberg(0, 300, 130) + kirche(330, 190, 140, WHITE, SLATE, "helm", "left") + zementwerk(620))

if __name__ == "__main__":
    for slug in sys.argv[1:] or list(C):
        sb.STAEDTE[slug] = C[slug][1]
        sb.build(slug)
        final.build(slug, f"{sb.OUT}/Stadt_{slug}.jpg")
