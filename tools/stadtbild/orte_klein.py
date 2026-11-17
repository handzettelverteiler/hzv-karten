"""Kleinere Orte – bei Bedarf hier eine Zeile ergänzen und `python3 orte_klein.py <Slug>` ausführen."""
import sys
import stadtbild as sb, final
from elemente import *
from stadtbild import gable_house
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

reg("Sulingen", ["Sulingen", "Bassum", "Twistringen", "Barnstorf", "Ehrenburg", "Scholen", "Schwaförden", "Schwafoerden", "Diepholz"], lambda: basis(212) + huegel(0, 520, 60) + dom(20, 230, 150, BRICK, 290, 64, "helm") + fachwerk(340, 1) + kirche(430, 190, 130, BRICK, SLATE, "spire", "left", 56, 270) + fachwerk(660, 1) + muehle(790, 150))

reg("Karben", ["Karben", "Nidderau", "Niddatal", "Wöllstadt", "Woellstadt"], lambda: basis(214) + huegel(0, 380, 70) + fachwerk(30, 3) + kirche(240, 190, 140, WHITE, SLATE, "helm", "left", 58, 260) + rathaus(500, 150, 120, YELLOW, "baroque") + fachwerk(680, 2) + windrad(860, 200))

reg("Bischofsheim", ["Bischofsheim", "Ginsheim-Gustavsburg", "Ginsheim", "Gustavsburg", "Mainspitze"], lambda: basis(216) + huegel(0, 400, 60) + dom(20, 200, 150, REDSAND, 280, 60, "helm") + burg(250, 200, 100, SAND, 120) + kirche(480, 170, 130, WHITE, SLATE, "spire", "left", 56, 250) + fachwerk(690, 2) + modern(810, 120, 110, "#d6e0e8"))

reg("Wartenberg", ["Wartenberg", "Thenn", "Pesenlern", "Manhartsdorf", "Auerbach"], lambda: basis(217) + huegel(0, 420, 80) + kirche(40, 200, 140, WHITE, ROOF_RED, "onion", "left", 58, 270) + rathaus(330, 150, 120, YELLOW, "baroque") + kirche(560, 160, 110, WHITE, ROOF_RED, "helm", "left", 50, 210))
reg("Greussen", ["Greußen", "Greussen", "Clingen", "Großenehrich", "Grossenehrich", "Westgreußen", "Westgreussen"], lambda: basis(218) + huegel(0, 520, 70) + fachwerk(30, 2) + kirche(200, 190, 140, WHITE, SLATE, "helm", "left", 60, 290) + rathaus(500, 150, 125, YELLOW, "stepped") + fachwerk(680, 2) + muehle(820, 150))
reg("Kierspe", ["Kierspe", "Meinerzhagen", "Halver", "Marienheide"], lambda: basis(219) + huegel(0, 560, 110) + fachwerk(30, 2) + kirche(170, 180, 130, WHITE, SLATE, "spire", "left", 56, 260) + fachwerk(410, 2) + kirche(540, 170, 125, SAND, SLATE, "helm", "left", 54, 240) + windrad(780, 230) + windrad(890, 190))

def _sendemast(x, h=300):
    """Funkerberg-Sendemast (Gittermast mit Abspannung) – Königs Wusterhausen."""
    top_y = G - h
    out = line(x - 22, G, x, top_y, 3, "#c0392b") + line(x + 22, G, x, top_y, 3, "#c0392b")
    for i in range(1, 9):
        yy = G - h * i / 9
        dx = 22 * (1 - i / 9)
        out += line(x - dx, yy, x + dx, yy, 2, "#c0392b")
    out += line(x, top_y, x - 90, G, 1.2, "#777") + line(x, top_y, x + 90, G, 1.2, "#777")
    return out


reg("KoenigsWusterhausen", ["Königs Wusterhausen", "Koenigs Wusterhausen", "Königs-Wusterhausen", "Zeesen", "Zernsdorf", "Deutsch Wusterhausen", "Wildau"], lambda: basis(220) + huegel(0, 420, 90) + _sendemast(130, 300) + schloss(260, 260, 120, "#f3e3b5", ROOF_RED, (), "helm", 54, 190) + kirche(600, 190, 135, BRICK, SLATE, "spire", "left", 58, 270) + fachwerk(830, 1))

reg("IdarOberstein", ["Idar-Oberstein", "Idar Oberstein", "Idaroberstein", "Oberstein", "Idar", "Baumholder", "Rammelsbach", "Kusel", "Glantal"], lambda: basis(221) + burg(30, 260, 150, "#d9cfb8", 120, True) + huegel(320, 260, 120, "#c9c2b4") + kirche(370, 150, 105, WHITE, SLATE, "spire", "left", 46, 210) + fachwerk(620, 2) + modern(760, 150, 110, "#d6e0e8"))


def _maibaum(x, h=340):
    """Bayerischer Maibaum (weiß-blau gestreift, Zunftschilder, Kranz) – Aying."""
    top_y = G - h
    w = 12
    out = rect(x - w / 2, top_y, w, h, "#ffffff", 2.5)
    k = 0
    yy = top_y + 10
    while yy < G - 10:
        out += poly([(x - w / 2, yy), (x + w / 2, yy - 10), (x + w / 2, yy - 2), (x - w / 2, yy + 8)], "#2f6db5", 0.8)
        yy += 22
        k += 1
    for i, side in enumerate((-1, 1, -1, 1, -1, 1)):
        sy = top_y + 70 + i * 38
        out += line(x, sy, x + side * 34, sy, 2.5)
        bx = x + side * 34 - (24 if side < 0 else 0)
        out += rect(bx, sy + 2, 24, 18, "#f4ecdc", 2) + rect(bx + 6, sy + 6, 12, 10, ["#c9553d", "#6fae8c", "#e2b23a"][i % 3], 1.5)
    out += f'<ellipse cx="{x}" cy="{top_y + 40}" rx="30" ry="9" fill="none" stroke="#3f8f3a" stroke-width="7"/>'
    out += circle(x, top_y - 10, 15, "#6dbb63", 2.5)
    return out


def _brauerei(x):
    """Brauerei mit Sudhaus und Schlot – Ayinger Brauerei."""
    out = rect(x, G - 120, 160, 120, "#f4ecdc") + poly([(x - 5, G - 120), (x + 80, G - 175), (x + 165, G - 120)], ROOF_RED)
    out += windows(x + 18, G - 100, 4, 2, 34, 42, 16, 24, arch=True)
    out += rect(x + 175, G - 250, 26, 250, BRICK) + rect(x + 171, G - 258, 34, 10, BRICK_D, 2.5)
    out += path(f"M{x+12},{G-60} q-6,-30 10,-36", "none", 0)
    out += circle(x + 238, G - 34, 30, "#d08a45", 2.5) + rect(x + 208, G - 34, 60, 34, "#d08a45", 2.5)
    return out


reg("Aying", ["Aying", "Großhelfendorf", "Grosshelfendorf", "Dürrnhaar", "Duerrnhaar", "Brunnthal", "Hofolding", "Faistenhaar", "Otterloh", "Egmating"], lambda: basis(222) + huegel(0, 560, 80) + kirche(40, 190, 135, YELLOW, ROOF_RED, "helm", "right", 58, 270) + _maibaum(330, 340) + gable_house(410, 120, 110, WHITE, ROOF_RED) + _brauerei(560) + kirche(840, 110, 100, WHITE, ROOF_RED, "onion", "left", 44, 200))

if __name__ == "__main__":
    for slug in sys.argv[1:] or list(C):
        sb.STAEDTE[slug] = C[slug][1]
        sb.build(slug)
        final.build(slug, f"{sb.OUT}/Stadt_{slug}.jpg")

