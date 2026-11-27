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
reg("Ebstorf", ["Ebstorf", "Bienenbüttel", "Bienenbuettel", "Wriedel", "Gerdau", "Hanstedt (Uelzen)", "Eimke", "Barum (Uelzen)", "Landkreis Uelzen"], lambda: basis(223) + huegel(0, 520, 80, "#c9b6d6") + kirche(30, 240, 140, BRICK, SLATE, "spire", "left", 60, 300) + fachwerk(330, 2) + kirche(470, 200, 120, BRICK, ROOF_RED, "helm", "right", 54, 240) + fachwerk(720, 2) + windrad(880, 200))

reg("Fellbach", ["Fellbach", "Schmiden", "Oeffingen", "Fellbach-Schmiden", "Fellbach-Oeffingen"], lambda: basis(224) + weinberg(0, 330, 150) + turm(250, 44, 200, SAND, "flat") + kirche(330, 210, 140, SAND, SLATE, "spire", "left", 62, 310) + modern(590, 160, 115, "#d6e0e8") + hochhaus(800, 84, 360, "#cfe0ef", True))

reg("Kaltenkirchen", ["Kaltenkirchen", "Henstedt-Ulzburg", "Henstedt Ulzburg", "Henstedtulzburg", "Henstedt", "Ulzburg", "Götzberg", "Goetzberg", "Rhen", "Kattendorf", "Nützen", "Nuetzen", "Oersdorf", "Winsen (Holstein)", "Wakendorf II"], lambda: basis(225) + huegel(0, 520, 70) + kirche(30, 210, 140, BRICK, SLATE, "spire", "left", 60, 310) + modern(300, 170, 110, "#d6e0e8") + fachwerk(500, 2) + kirche(630, 160, 120, BRICK, ROOF_RED, "helm", "left", 52, 230) + muehle(830, 160))
reg("HofheimTaunus", ["Hofheim am Taunus", "Hofheim", "Hofheim (Taunus)", "Hofheim a. Ts.", "Wallau", "Diedenbergen", "Marxheim", "Lorsbach", "Langenhain", "Wildsachsen"], lambda: basis(226) + huegel(0, 380, 140) + turm(150, 50, 230, "#b98a5a", "flat") + fachwerk(330, 2) + kirche(450, 200, 140, WHITE, SLATE, "helm", "left", 60, 290) + rathaus(700, 140, 120, YELLOW, "stepped") + fachwerk(850, 1))
reg("Westerwald", ["Westerwald", "Selters (Westerwald)", "Selters", "Hachenburg", "Wirges", "Dierdorf", "Puderbach", "Altenkirchen", "Altenkirchen (Westerwald)", "Flammersfeld", "Ransbach-Baumbach", "Ransbach Baumbach"], lambda: basis(227) + huegel(0, 560, 120) + schloss(30, 300, 110, YELLOW, SLATE, (("helm", 0.0), ("helm", 1.0)), "helm", 48, 170) + fachwerk(370, 2) + kirche(500, 190, 135, WHITE, SLATE, "spire", "left", 58, 270) + windrad(770, 240) + windrad(890, 190))

reg("Bad_Vilbel", ["Bad Vilbel", "Dortelweil", "Massenheim", "Gronau (Bad Vilbel)", "Bad Vilbel-Dortelweil", "Bad Vilbel-Massenheim", "Bad Vilbel-Heilsberg"], lambda: basis(228) + huegel(0, 420, 90) + burg(30, 260, 110, "#d9cfb8", 140, True) + kurhaus(330, 230, 100, WHITE) + kirche(600, 190, 135, SAND, SLATE, "spire", "left", 58, 270) + fachwerk(830, 2))
reg("Oebisfelde", ["Oebisfelde", "Oebisfelde-Weferlingen", "Weferlingen", "Velpke", "Bahrdorf", "Danndorf", "Grafhorst", "Rühen", "Ruehen", "Grasleben", "Mariental", "Querenhorst", "Groß Twülpstedt", "Gross Twuelpstedt"], lambda: basis(229) + huegel(0, 560, 70) + burg(20, 280, 110, "#d9cfb8", 150, False) + fachwerk(330, 2) + kirche(460, 200, 135, BRICK, SLATE, "spire", "left", 60, 280) + muehle(720, 160) + windrad(880, 200))

reg("Burgstaedt", ["Burgstädt", "Burgstaedt", "Taura", "Mohsdorf", "Köthensdorf-Reitzenhain", "Koethensdorf-Reitzenhain"], lambda: basis(230) + huegel(0, 380, 120) + wasserturm(120, 70, 330, "#cfc6b2", "pyramid") + rathaus(330, 160, 125, YELLOW, "baroque") + kirche(540, 190, 140, WHITE, SLATE, "spire", "left", 58, 280) + burg(770, 170, 100, "#d9cfb8", 130))

reg("LaufPegnitz", ["Lauf an der Pegnitz", "Lauf a.d. Pegnitz", "Lauf a. d. Pegnitz", "Heuchling", "Kotzenhof", "Rudolfshof"], lambda: basis(231) + huegel(0, 420, 90) + burg(20, 300, 110, "#d9cfb8", 150, False) + tor(360, 90, 210, "#e0cba0", "stepped") + rathaus(480, 150, 125, YELLOW, "stepped") + fachwerk(650, 2) + kirche(770, 160, 130, WHITE, SLATE, "spire", "left", 54, 260))
reg("Altomuenster", ["Altomünster", "Altomuenster", "Wollomoos", "Pipinsried", "Unterzeitlbach", "Hohenzell", "Erdweg", "Kleinberghofen", "Großberghofen", "Grossberghofen", "Eisenhofen", "Unterweikertshofen", "Markt Indersdorf", "Karpfhofen", "Niederroth"], lambda: basis(232) + huegel(0, 560, 90) + kirche(40, 230, 150, WHITE, ROOF_RED, "onion", "right", 64, 330) + _maibaum(380, 330) + gable_house(450, 120, 110, YELLOW, ROOF_RED) + gable_house(590, 110, 100, WHITE, ROOF_RED) + _brauerei(720))
reg("Stockach", ["Stockach", "Stockach (Kernstadt)", "Wahlwies", "Zizenhausen", "Hindelwangen", "Winterspüren", "Winterspueren", "Espasingen", "Hoppetenzell", "Mahlspüren im Hegau", "Seelfingen", "Raithaslach", "Eigeltingen", "Heudorf im Hegau", "Münchhöf", "Honstetten", "Orsingen-Nenzingen", "Orsingen", "Nenzingen", "Aach", "Aach (Hegau)", "Hegau"], lambda: basis(233) + huegel(0, 300, 170) + burg(20, 240, 110, "#d9cfb8", 140, True) + rathaus(330, 150, 125, YELLOW, "baroque") + kirche(510, 190, 140, WHITE, SLATE, "helm", "left", 60, 300) + fachwerk(760, 3))
reg("Osterode", ["Osterode am Harz", "Osterode", "Osterode (Kernstadt)", "Freiheit", "Lasfelde", "Katzenstein", "Petershütte", "Förste", "Foerste", "Dorste", "Schwiegershausen", "Lerbach", "Nienstedt", "Bad Grund", "Bad Grund (Harz)", "Badenhausen", "Gittelde", "Eisdorf", "Windhausen"], lambda: basis(234) + huegel(0, 600, 160) + burg(20, 220, 110, "#d9cfb8", 150, True) + fachwerk(270, 2) + kirche(400, 190, 140, WHITE, SLATE, "helm", "left", 60, 300) + kurhaus(630, 190, 100, YELLOW) + foerderturm(850, 200))
reg("Ispringen", ["Ispringen", "Eisingen"], lambda: basis(235) + huegel(0, 520, 110) + fachwerk(30, 2) + kirche(200, 190, 140, WHITE, SLATE, "spire", "left", 58, 280) + rathaus(450, 150, 125, YELLOW, "baroque") + gable_house(640, 110, 100, WHITE, ROOF_RED) + windrad(860, 220))
reg("Chiemgau", ["Chiemgau", "Waging am See", "Waging a. See", "Waging", "Traunstein", "Chiemsee", "Prien am Chiemsee", "Prien a. Chiemsee", "Bad Reichenhall", "Laufen", "Trostberg", "Siegsdorf", "Teisendorf", "Tittmoning", "Grassau", "Bernau a. Chiemsee", "Bad Endorf", "Chieming"], lambda: basis(236) + huegel(0, 930, 260, "#c9d8e6") + huegel(0, 520, 120) + kirche(40, 200, 140, WHITE, ROOF_RED, "onion", "left", 62, 320) + _maibaum(330, 330) + gable_house(400, 130, 110, WHITE, ROOF_RED) + kirche(580, 160, 120, SAND, SLATE, "onion", "right", 54, 260) + gable_house(790, 120, 100, YELLOW, ROOF_RED))
reg("Nettetal", ["Nettetal", "Lobberich", "Kaldenkirchen", "Breyell", "Hinsbeck", "Leuth", "Schaag"], lambda: basis(237) + huegel(0, 930, 50, "#c9d8e6") + burg(20, 230, 100, BRICK, 120) + kirche(290, 210, 145, BRICK, SLATE, "spire", "center", 62, 330) + fachwerk(560, 2) + kirche(680, 160, 120, BRICK, SLATE, "spire", "left", 54, 260) + muehle(860, 150))
reg("Ottobrunn", ["Ottobrunn", "Riemerling", "Hohenbrunn", "Neubiberg", "Putzbrunn", "Unterhaching"], lambda: basis(238) + huegel(0, 930, 40, "#c9d8e6") + modern(30, 200, 120, "#e8edf2") + kirche(270, 200, 140, WHITE, SLATE, "pyramid", "left", 60, 300) + turm(540, 34, 230, "#d8d2c4", "dome", COPPER, False, 2) + rathaus(620, 160, 125, YELLOW, "baroque") + gable_house(810, 110, 100, WHITE, ROOF_RED))
reg("Nordsachsen", ["Delitzsch", "Eilenburg", "Wurzen", "Bad Düben", "Bad Dueben", "Mockrehna", "Dommitzsch", "Doberschütz", "Doberschuetz", "Mörtitz", "Moertitz", "Krostitz", "Löbnitz", "Loebnitz", "Laußig", "Laussig", "Zschepplin", "Thallwitz", "Nordsachsen"], lambda: basis(239) + huegel(0, 600, 80) + schloss(20, 300, 110, WHITE, ROOF_RED, (("helm", 0.0),), None, 52, 190) + turm(350, 60, 200, BRICK, "flat") + rathaus(440, 150, 125, YELLOW, "stepped") + dom(620, 210, 150, SAND, 290, 56, "spire", None, True) + burg(860, 70, 90, "#d9cfb8", 160))
reg("HoehenkirchenSiegertsbrunn", ["Höhenkirchen-Siegertsbrunn", "Hoehenkirchen-Siegertsbrunn", "Höhenkirchen", "Hoehenkirchen", "Siegertsbrunn", "Wächterhof", "Waechterhof", "Kleinkarolinenfeld", "Großkarolinenfeld (Höhenkirchen)"], lambda: basis(240) + huegel(0, 930, 50, "#c9d8e6") + kirche(30, 200, 140, WHITE, ROOF_RED, "helm", "left", 60, 300) + _maibaum(330, 330) + gable_house(400, 130, 110, WHITE, ROOF_RED) + kirche(580, 170, 120, YELLOW, ROOF_RED, "onion", "right", 54, 250) + gable_house(800, 110, 100, YELLOW, ROOF_RED))
reg("Hoechberg", ["Höchberg", "Hoechberg", "Hexenbruch", "Waldbrunn", "Eisingen (Unterfranken)", "Kist", "Waldbüttelbrunn", "Waldbuettelbrunn"], lambda: basis(241) + huegel(0, 560, 120) + kirche(30, 220, 150, SAND, SLATE, "onion", "left", 64, 330) + rathaus(330, 150, 125, YELLOW, "baroque") + fachwerk(510, 2) + weinberg(640, 290, 120))
reg("Randersacker", ["Randersacker", "Lindelbach", "Theilheim", "Eibelstadt", "Gerbrunn"], lambda: basis(242) + weinberg(0, 520, 170) + kirche(40, 190, 130, SAND, SLATE, "pyramid", "left", 60, 270) + rathaus(560, 120, 110, YELLOW, "baroque", False) + fachwerk(720, 2) + gable_house(850, 80, 100, WHITE, ROOF_RED))
reg("Germering", ["Germering", "Unterpfaffenhofen", "Germering-Unterpfaffenhofen", "Harthaus", "Nebel", "Puchheim", "Gilching", "Gauting"], lambda: basis(243) + huegel(0, 930, 40, "#c9d8e6") + kirche(30, 200, 140, WHITE, ROOF_RED, "onion", "left", 58, 290) + modern(300, 240, 120, "#e8edf2") + kirche(580, 170, 120, WHITE, SLATE, "spire", "right", 54, 260) + hochhaus(820, 70, 230, "#cfe0ef"))
reg("Hoevelhof", ["Hövelhof", "Hoevelhof", "Hövelriege", "Hoevelriege", "Riege", "Espeln", "Staumühle", "Staumuehle", "Senne"], lambda: basis(244) + huegel(0, 930, 60, "#d8c3d6") + schloss(20, 280, 110, WHITE, SLATE, (("helm", 0.5),), None, 50, 190) + fachwerk(350, 2) + kirche(480, 210, 145, BRICK, SLATE, "spire", "left", 62, 330) + windrad(750, 230) + windrad(850, 180))

reg("Pattensen", ["Pattensen", "Schulenburg (Leine)", "Schulenburg Leine", "Jeinsen", "Hüpede", "Huepede", "Koldingen", "Hemmingen", "Arnum", "Hemmingen-Westerfeld", "Hiddestorf", "Devese", "Harkenbleck", "Wilkenburg"], lambda: basis(245) + huegel(0, 420, 110) + burg(20, 300, 110, "#d9cfb8", 160) + kirche(400, 200, 140, BRICK, SLATE, "spire", "left", 60, 310) + rathaus(660, 140, 120, WHITE, "stepped") + fachwerk(830, 2))

reg("Seenplatte", ["Penzlin", "Möllenhagen", "Moellenhagen", "Waren (Müritz)", "Waren Müritz", "Waren", "Penzlin Möllenhagen Waren", "Mecklenburgische Seenplatte", "Seenplatte"], lambda: basis(246) + huegel(0, 930, 70, "#c9d8e6") + huegel(0, 380, 120) + burg(20, 300, 110, "#e6dcc4", 150) + kirche(380, 210, 145, BRICK, SLATE, "spire", "left", 64, 340) + fachwerk(650, 2) + kirche(780, 150, 120, BRICK, ROOF_RED, "pyramid", "right", 54, 250))

reg("Prenzlau", ["Prenzlau", "Gramzow", "Nordwestuckermark", "Uckermark", "Röpersdorf", "Roepersdorf", "Dedelow", "Warnitz", "Schenkenberg", "Fürstenwerder", "Fuerstenwerder"], lambda: basis(247) + huegel(0, 930, 60, "#c9d8e6") + tor(20, 90, 230, BRICK, "spire") + dom(170, 260, 170, BRICK, 330, 62, "spire") + fachwerk(520, 2) + kirche(660, 170, 125, BRICK, SLATE, "pyramid", "left", 56, 260) + windrad(870, 210))

def _hebewerk(x, w=300, h=230):
    """Schiffshebewerk Henrichenburg (Waltrop): zwei Backsteintürme mit Stahlfachwerk-Brücke, Trog darunter."""
    tw = 50
    out = rect(x, G - h, tw, h, BRICK) + rect(x + w - tw, G - h, tw, h, BRICK)
    out += poly([(x - 6, G - h), (x + tw / 2, G - h - 34), (x + tw + 6, G - h)], SLATE)
    out += poly([(x + w - tw - 6, G - h), (x + w - tw / 2, G - h - 34), (x + w + 6, G - h)], SLATE)
    by = G - h + 20
    out += rect(x + tw, by, w - 2 * tw, 34, "#7f9bb3")
    n = 6
    for k in range(n):
        x1 = x + tw + k * (w - 2 * tw) / n
        x2 = x + tw + (k + 1) * (w - 2 * tw) / n
        out += line(x1, by + 34, x2, by, 2.5)
    out += rect(x + tw, G - 70, w - 2 * tw, 40, "#9fc3df")
    for k in range(1, 4):
        xx = x + tw + k * (w - 2 * tw) / 4
        out += line(xx, by + 34, xx, G - 70, 2.5)
    return out

reg("Waltrop", ["Waltrop", "Oberwiese", "Leveringhausen", "Lippe", "Brockenscheidt"], lambda: basis(248) + huegel(0, 930, 50, "#c9d8e6") + foerderturm(30, 240) + kirche(230, 200, 140, BRICK, SLATE, "spire", "left", 60, 320) + _hebewerk(500, 300, 230) + gable_house(840, 90, 100, BRICK, ROOF_RED))

reg("Mayen", ["Mayen", "Mayen-Koblenz", "Hausen", "Kürrenberg", "Kuerrenberg", "Alzheim", "Betzing", "Saffig"], lambda: basis(249) + huegel(0, 930, 50, "#c9d8e6") + burg(20, 320, 120, "#d9cfb8", 170) + kirche(410, 200, 140, SAND, SLATE, "spire", "left", 60, 340) + tor(660, 90, 210, "#d9cfb8", "pyramid") + fachwerk(790, 2))
reg("Werder", ["Werder (Havel)", "Werder Havel", "Werder", "Glindow", "Petzow", "Plötzin", "Ploetzin", "Töplitz", "Toeplitz", "Derwitz", "Kemnitz", "Phöben", "Phoeben", "Groß Kreutz", "Gross Kreutz"], lambda: basis(250) + huegel(0, 930, 40, "#c9d8e6") + muehle(75, 160) + kirche(290, 220, 145, BRICK, SLATE, "spire", "center", 64, 340) + gable_house(560, 90, 100, WHITE, ROOF_RED) + tree(700, 70) + tree(760, 80) + tree(840, 70) + tree(905, 60))
reg("Landau", ["Landau", "Landau in der Pfalz", "Landau Pfalz", "Landau (Pfalz)", "Godramstein", "Arzheim", "Nußdorf", "Nussdorf", "Queichheim", "Mörlheim", "Moerlheim", "Mörzheim", "Moerzheim", "Wollmesheim", "Dammheim", "Offenbach an der Queich"], lambda: basis(251) + weinberg(0, 300, 130) + kirche(340, 210, 150, SAND, SLATE, "spire", "left", 62, 340) + tor(600, 110, 190, SAND, "flat") + kirche(770, 140, 125, REDSAND, SLATE, "helm", "left", 58, 300))
reg("Aindling", ["Aindling", "Affing", "Rehling", "Affing Aindling Rehling", "Todtenweis", "Petersdorf", "Gebenhofen", "Mühlhausen (Affing)", "Muehlhausen", "Bergen (Affing)", "Stotzard", "Pichl"], lambda: basis(252) + huegel(0, 930, 60) + kirche(50, 200, 140, WHITE, ROOF_RED, "onion", "left", 60, 300) + schloss(330, 300, 110, WHITE, ROOF_RED, (("onion", 0.0), ("onion", 1.0)), None, 46, 170) + kirche(720, 150, 120, WHITE, ROOF_RED, "spire", "left", 50, 240) + tree(905, 60))
reg("Neufahrn", ["Neufahrn", "Neufahrn bei Freising", "Neufahrn b. Freising", "Eching", "Mintraching", "Massenhausen", "Fürholzen", "Fuerholzen", "Hetzenhausen", "Giggenhausen", "Dietersheim", "Unterschleißheim", "Unterschleissheim"], lambda: basis(253) + huegel(0, 930, 40, "#c9d8e6") + kirche(50, 210, 145, WHITE, ROOF_RED, "onion", "left", 60, 300) + modern(330, 200, 110, "#e8edf2") + kirche(580, 170, 120, WHITE, SLATE, "spire", "left", 54, 260) + tree(800, 70) + tree(870, 60))

def _schaufelradbagger(x, w=330, h=170):
    """Tagebau-Schaufelradbagger (generisch): Schaufelrad am Ausleger, Raupenunterwagen, Gegenausleger."""
    out = huegel(x - 20, w + 40, 40, "#d8c49a")
    out += rect(x + 90, G - 34, 160, 26, "#6b6b6b") + rect(x + 120, G - 80, 100, 46, "#e2a93b")
    out += line(x + 170, G - 80, x + 170, G - h, 5) + line(x + 170, G - h, x + 40, G - 110, 4) + line(x + 170, G - h, x + w - 10, G - 90, 4)
    out += line(x + 120, G - 70, x + 40, G - 110, 6, "#e2a93b") + line(x + 220, G - 70, x + w - 10, G - 90, 6, "#e2a93b")
    out += circle(x + 40, G - 110, 48, "#e2a93b", 4)
    for k in range(8):
        import math
        a = k * math.pi / 4
        out += line(x + 40, G - 110, x + 40 + 48 * math.cos(a), G - 110 + 48 * math.sin(a), 2.5)
    out += rect(x + w - 30, G - 100, 40, 30, "#8a8a8a")
    return out

def _giesshalle(x, w=260, h=130):
    """Sayner Hütte: Gießhalle mit Glas-Giebelfront (Basilika-Form aus Gusseisen)."""
    out = rect(x, G - h + 30, w, h - 30, "#e6e2da") + poly([(x - 4, G - h + 30), (x + w / 2, G - h - 30), (x + w + 4, G - h + 30)], "#6b7a8f")
    out += rect(x + w * 0.3, G - h - 10, w * 0.4, h + 10, "#cfe3f3") + poly([(x + w * 0.3 - 4, G - h - 10), (x + w / 2, G - h - 50), (x + w * 0.7 + 4, G - h - 10)], "#6b7a8f")
    for k in range(1, 5):
        xx = x + w * 0.3 + k * w * 0.4 / 5
        out += line(xx, G - h - 10, xx, G, 2)
    out += windows(x + 14, G - h + 50, 2, 1, 26, 0, 14, 40, arch=True) + windows(x + w * 0.72 + 6, G - h + 50, 2, 1, 26, 0, 14, 40, arch=True)
    return out

reg("Niederzier", ["Niederzier", "Huchem-Stammeln", "Huchem Stammeln", "Oberzier", "Ellen", "Hambach", "Krauthausen", "Selhausen", "Selgersdorf", "Merzenich", "Morschenich"], lambda: basis(254) + huegel(0, 930, 40, "#c9d8e6") + burg(30, 240, 40, "#e6dcc4", 110) + kirche(360, 190, 140, WHITE, SLATE, "spire", "left", 58, 280) + _schaufelradbagger(600, 320, 170))
reg("Andernach", ["Andernach", "Namedy", "Eich", "Kell", "Miesenheim", "Kretz", "Plaidt", "Saffig", "Weißenthurm", "Weissenthurm", "Kruft", "Nickenich", "Urmitz", "Kettig"], lambda: basis(255) + turm(30, 74, 260, "#d9cfb8", "flat") + dom(210, 200, 160, "#e6dcc4", 290, 56, "helm", SLATE, True) + tor(560, 100, 200, "#d9cfb8", "stepped") + fachwerk(720, 2) + tree(880, 60))
reg("Hueckelhoven", ["Hückelhoven", "Hueckelhoven", "Ratheim", "Baal", "Doveren", "Hilfarth", "Brachelen", "Millich", "Kleingladbach", "Rurich", "Altmyhl", "Wassenberg", "Erkelenz"], lambda: basis(256) + huegel(0, 330, 120, "#a9c79a") + foerderturm(380, 250) + kirche(620, 190, 140, BRICK, SLATE, "spire", "left", 60, 320) + fachwerk(840, 1))
reg("Lahnstein", ["Lahnstein", "Oberlahnstein", "Niederlahnstein", "Friedland", "Braubach", "Fachbach"], lambda: basis(257) + burg(30, 280, 140, "#e6dcc4", 140) + schloss(390, 200, 110, "#efe6d2", SLATE, (("spire", 0.0),), None, 50, 200) + turm(650, 56, 210, "#d9cfb8", "spire") + fachwerk(760, 3))
reg("Bendorf", ["Bendorf", "Sayn", "Bendorf-Sayn", "Mülhofen", "Muelhofen", "Stromberg", "Vallendar", "Weitersburg", "Höhr-Grenzhausen", "Hoehr-Grenzhausen"], lambda: basis(258) + burg(30, 240, 150, "#d9cfb8", 120, True) + schloss(330, 260, 110, "#efe6d2", SLATE, (("spire", 0.0), ("flat", 1.0)), None, 46, 190) + _giesshalle(660, 260, 130))

reg("Poessneck", ["Pößneck", "Poessneck", "Neustadt an der Orla", "Neustadt (Orla)", "Neustadt Orla", "Krölpa", "Kroelpa", "Ranis", "Oppurg", "Schweinitz", "Jüdewein", "Juedewein", "Köstitz", "Koestitz", "Öpitz", "Oepitz"], lambda: basis(259) + huegel(0, 560, 90) + kirche(40, 210, 150, WHITE, SLATE, "helm", "left", 62, 300) + rathaus(330, 170, 150, "#efe6d2", "stepped") + fachwerk(560, 2) + turm(720, 52, 210, "#d9cfb8", "spire") + tree(860, 60))
reg("Kroepelin", ["Kröpelin", "Kroepelin", "Bad Doberan", "Kühlungsborn", "Kuehlungsborn", "Rerik", "Satow", "Kirch Mulsow", "Jennewitz", "Schmadebeck", "Wichmannsdorf", "Detershagen", "Kühlung", "Kuehlung"], lambda: basis(260) + huegel(0, 620, 70) + kirche(40, 220, 150, BRICK, SLATE, "spire", "left", 64, 300) + rathaus(330, 150, 125, BRICK, "stepped") + fachwerk(520, 2) + muehle(730, 170))
reg("Neuenkirchen", ["Neuenkirchen", "Neuenkirchen (Rheine)", "Neuenkirchen Kreis Steinfurt", "Neuenkirchen (Kreis Steinfurt)", "St. Arnold", "Sankt Arnold", "St Arnold", "Landersum", "Offlum", "Sutrum-Harum", "Wettringen"], lambda: basis(261) + huegel(0, 520, 60) + fachwerk(30, 2) + kirche(220, 240, 160, BRICK, SLATE, "spire", "center", 70, 360) + fachwerk(500, 1) + kirche(610, 170, 120, BRICK, SLATE, "spire", "left", 54, 240) + muehle(810, 140))
reg("Rottweil", ["Rottweil", "Zimmern ob Rottweil", "Deißlingen", "Deisslingen", "Dietingen", "Villingendorf", "Wellendingen", "Göllsdorf", "Goellsdorf", "Bühlingen", "Buehlingen", "Altstadt Rottweil", "Hausen ob Rottweil", "Feckenhausen", "Zepfenhan"], lambda: basis(262) + huegel(0, 520, 100) + tor(20, 100, 230, "#7d746a", "pyramid") + dom(170, 200, 160, SAND, 300, 58, "spire") + turm(570, 66, 310, SAND, "spire") + fachwerk(670, 2) + hochhaus(820, 52, 330, "#e6eaee", True))
reg("Voerde", ["Voerde", "Voerde (Niederrhein)", "Voerde Niederrhein", "Friedrichsfeld", "Spellen", "Götterswickerhamm", "Goetterswickerhamm", "Löhnen", "Loehnen", "Mehrum", "Emmelsum", "Hünxe", "Huenxe"], lambda: basis(263) + huegel(0, 420, 50) + schloss(40, 300, 110, BRICK, SLATE, (("helm", 0.0), ("helm", 1.0)), None, 50, 180) + kirche(430, 190, 140, BRICK, SLATE, "spire", "left", 58, 280) + rathaus(650, 150, 115, WHITE, "baroque") + windrad(850, 200))

if __name__ == "__main__":
    for slug in sys.argv[1:] or list(C):
        sb.STAEDTE[slug] = C[slug][1]
        sb.build(slug)
        final.build(slug, f"{sb.OUT}/Stadt_{slug}.jpg")

