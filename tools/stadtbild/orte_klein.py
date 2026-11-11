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

reg("Ansbach", ["Ansbach"], lambda: basis(206) + schloss(30, 380, 120, SAND, ROOF_RED, (), None) + turm(470, 40, 215, SAND, "spire") + turm(700, 40, 215, SAND, "spire") + kirche(480, 250, 140, SAND, SLATE, "spire", "center", 58, 310) + fachwerk(800, 2))
reg("Reiskirchen", ["Reiskirchen"], lambda: basis(207) + fachwerk(40, 3) + kirche(260, 190, 140, WHITE, SLATE, "helm", "left", 58, 260) + fachwerk(520, 2) + windrad(700, 230) + windrad(840, 190))
reg("Breitscheid", ["Breitscheid", "Breitscheid (Hessen)", "Driedorf"], lambda: basis(208) + huegel(0, 420, 90) + modern(30, 190, 95, "#c9d3dc") + fachwerk(250, 2) + kirche(380, 190, 140, WHITE, SLATE, "spire", "left", 58, 260) + fachwerk(620, 2) + windrad(760, 240) + windrad(870, 200))

reg("Enger", ["Enger", "Spenge"], lambda: basis(209) + huegel(0, 300, 80) + burg(20, 240, 100, "#d9cfb8", 120) + fachwerk(290, 2) + kirche(420, 210, 150, SAND, SLATE, "spire", "center", 62, 300) + denkmal(690, 140) + muehle(810, 150))
reg("Gotha", ["Gotha"], lambda: basis(210) + huegel(0, 520, 80) + schloss(30, 420, 120, WHITE, SLATE, (("helm", 0.0), ("helm", 1.0)), None, 56, 200) + rathaus(520, 150, 130, "#e08a5a", "stepped") + kirche(700, 200, 140, SAND, SLATE, "helm", "left", 58, 270))

reg("Neckarsulm", ["Neckarsulm", "Amorbach", "Dahenfeld", "Obereisesheim", "Untereisesheim"], lambda: basis(211) + weinberg(0, 300, 140) + burg(300, 240, 110, SAND, 140) + kirche(570, 200, 140, WHITE, SLATE, "helm", "left", 58, 280) + modern(800, 130, 110, "#d6e0e8"))

if __name__ == "__main__":
    for slug in sys.argv[1:] or list(C):
        sb.STAEDTE[slug] = C[slug][1]
        sb.build(slug)
        final.build(slug, f"{sb.OUT}/Stadt_{slug}.jpg")
