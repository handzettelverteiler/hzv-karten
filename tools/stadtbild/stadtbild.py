"""HZV Stadtbild-Generator (Stil v2): setzt eine neu gezeichnete Stadtsilhouette hinter
Figur, Briefkasten, Lupe, Fluss und Wiese aus Stadt_Allgemein(.jpg|_Lupe.jpg).

Aufruf: python3 stadtbild.py <Slug> [<Slug> ...]   (Slug = Funktionsname in STAEDTE)
Ausgabe: out/Stadt_<Slug>.jpg und out/Stadt_<Slug>_Lupe.jpg (1600x873)
"""
import math, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw

BASE = os.environ.get("HZV_STAEDTE", "/home/claude/hzv-karten/staedte")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
W, H, GROUND = 1600, 873, 578
LINE = "#2b2b2b"
SW = 3

# ---------------- Zeichen-Bausteine (SVG-Strings) ----------------
def rect(x, y, w, h, fill, sw=SW):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{LINE}" stroke-width="{sw}" stroke-linejoin="round"/>'

def poly(pts, fill, sw=SW):
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{LINE}" stroke-width="{sw}" stroke-linejoin="round"/>'

def line(x1, y1, x2, y2, sw=SW, color=LINE):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'

def circle(cx, cy, r, fill, sw=SW):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{LINE}" stroke-width="{sw}"/>'

def win(x, y, w=14, h=20, arch=False, fill="#cfe3f3"):
    if arch:
        r = w / 2
        return f'<path d="M{x},{y+h} L{x},{y+r} A{r},{r} 0 0 1 {x+w},{y+r} L{x+w},{y+h} Z" fill="{fill}" stroke="{LINE}" stroke-width="2.5"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{LINE}" stroke-width="2.5"/>'

def windows(x, y, cols, rows, dx, dy, w=14, h=20, arch=False, fill="#cfe3f3"):
    return "".join(win(x + c * dx, y + r * dy, w, h, arch, fill) for c in range(cols) for r in range(rows))

def small_house(x, w=46, h=34, roof="#c9553d", wall="#f4ecdc"):
    y = GROUND - h
    return (rect(x, y, w, h, wall, 2.5) + poly([(x - 3, y), (x + w / 2, y - 22), (x + w + 3, y)], roof, 2.5)
            + win(x + w / 2 - 6, y + 10, 12, 12))

def tree(x, h=44):
    y = GROUND
    return (rect(x - 3, y - 12, 6, 12, "#7a5230", 2) + circle(x, y - h * 0.62, h * 0.36, "#6dbb63", 2.5))

def stepped_gable_house(x, w, h, wall, steps=4, wins=True):
    """Backsteingiebelhaus mit Treppengiebel (Hanse-Stil)."""
    y = GROUND - h
    gh = w * 0.75
    pts = [(x, y)]
    sw_, sh_ = (w / 2) / steps, gh / steps
    for i in range(steps):
        pts += [(x + i * sw_, y - (i + 1) * sh_), (x + (i + 1) * sw_, y - (i + 1) * sh_)]
    for i in range(steps):
        pts += [(x + w / 2 + i * sw_, y - (steps - i) * sh_), (x + w / 2 + (i + 1) * sw_, y - (steps - i) * sh_)]
    pts += [(x + w, y)]
    out = poly(pts + [(x + w, GROUND), (x, GROUND)], wall)
    if wins:
        cols = max(2, int(w // 26))
        dx = (w - 16) / cols
        out += windows(x + 10, y + 14, cols, max(1, int((h - 30) // 34)), dx, 34, 14, 20)
        out += win(x + w / 2 - 7, y - gh * 0.45, 14, 18, arch=True)
        out += win(x + w / 2 - 8, GROUND - 26, 16, 26, arch=True, fill="#8a5a3a")
    return out

def gable_house(x, w, h, wall, roof="#c9553d", timber=False):
    y = GROUND - h
    out = rect(x, y, w, h, wall) + poly([(x - 4, y), (x + w / 2, y - w * 0.7), (x + w + 4, y)], roof)
    if timber:
        for k in range(1, 3):
            out += line(x, y + k * h / 3, x + w, y + k * h / 3, 2.5, "#7a4a2a")
        out += line(x, y, x + w / 3, y + h / 3, 2.5, "#7a4a2a") + line(x + w, y, x + 2 * w / 3, y + h / 3, 2.5, "#7a4a2a")
    out += windows(x + w * 0.2, y + 10, 2, max(1, int((h - 20) // 32)), w * 0.4, 32, 13, 17)
    return out

def flat_front_house(x, w, h, wall):
    """Inn-Salzach-Haus: Fassade mit waagrechtem Abschluss (Grabendach verdeckt)."""
    y = GROUND - h
    out = rect(x, y, w, h, wall) + rect(x - 3, y - 8, w + 6, 8, "#e9e1cf", 2.5)
    cols = max(2, int(w // 28))
    out += windows(x + 9, y + 14, cols, max(1, int((h - 30) // 32)), (w - 14) / cols, 32, 13, 19)
    return out

def spire(cx, top_y, base_y, base_w, fill="#6b7a8f"):
    return poly([(cx - base_w / 2, base_y), (cx, top_y), (cx + base_w / 2, base_y)], fill) + \
        line(cx, top_y, cx, top_y - 14, 2.5) + circle(cx, top_y - 16, 4, "#e2b23a", 2)

def arcs():
    """Gestrichelte Funkwellen wie im Original, Zentrum hinter der Stadt."""
    cx, cy = 640, 640
    out = []
    for r in (300, 390, 480, 570, 660):
        a0, a1 = math.radians(196), math.radians(338)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="#8c8c8c" '
                   f'stroke-width="2.5" stroke-dasharray="14 11"/>')
    return "".join(out)

def house_row(x0, x1, seed=1):
    import random
    rnd = random.Random(seed)
    out, x = "", x0
    while x < x1 - 40:
        w = rnd.choice([40, 44, 48])
        out += small_house(x, w, rnd.choice([28, 32, 36]), rnd.choice(["#c9553d", "#d4673f", "#b8483a"]),
                           rnd.choice(["#f4ecdc", "#f6e3b4", "#efe7da"]))
        x += w + rnd.choice([4, 8, 14])
        if rnd.random() < 0.3 and not (900 < x < 1340):
            out += tree(x + 8, 40); x += 22
    return out

# ---------------- Städte ----------------
def Lueneburg():
    s = house_row(10, 1330, seed=3)
    # Wasserturm (Backstein, Turmhelm grün)
    s += rect(110, 300, 90, 278, "#c0603f") + windows(130, 330, 2, 6, 34, 40, 14, 22, arch=True)
    s += rect(98, 268, 114, 34, "#c0603f") + windows(108, 276, 4, 1, 26, 0, 12, 16)
    s += poly([(96, 268), (155, 205), (214, 268)], "#6fae8c") + rect(144, 186, 22, 22, "#6fae8c", 2.5)
    s += poly([(141, 186), (155, 168), (169, 186)], "#6fae8c", 2.5)
    # Giebelhäuser "Am Sande"
    s += stepped_gable_house(230, 70, 120, "#b8553a") + stepped_gable_house(305, 62, 130, "#a84a34")
    s += stepped_gable_house(372, 74, 112, "#c46a46")
    # St. Johannis: Backsteinkirche mit sehr hoher Turmspitze
    s += rect(455, 380, 230, 198, "#b9573b") + poly([(450, 380), (570, 318), (690, 380)], "#7a8796")
    s += windows(510, 420, 4, 1, 40, 0, 18, 70, arch=True)
    s += rect(560, 230, 64, 348, "#a64b33") + windows(578, 260, 1, 4, 0, 60, 26, 36, arch=True)
    s += spire(592, 70, 232, 70, "#51606f")
    # Alter Kran am Stintmarkt (Holzkran am Wasser)
    s += rect(760, 470, 76, 108, "#e9d3a8") + poly([(752, 470), (798, 430), (844, 470)], "#7a8796")
    s += line(798, 448, 900, 404, 5, "#6a4426") + line(900, 404, 900, 470, 2.5)
    s += windows(772, 490, 2, 2, 30, 38, 14, 20)
    s += stepped_gable_house(880, 60, 98, "#c46a46") + stepped_gable_house(945, 66, 108, "#b8553a")
    return s

def Stade():
    s = house_row(10, 1330, seed=5)
    # Schwedenspeicher: großer Backsteinspeicher mit Walmdach
    s += rect(60, 400, 250, 178, "#b9573b") + poly([(50, 400), (110, 330), (260, 330), (320, 400)], "#c9553d")
    s += windows(80, 425, 7, 3, 33, 46, 15, 22)
    s += poly([(160, 330), (185, 300), (210, 330)], "#c9553d", 2.5) + win(178, 310, 14, 14)
    # Fachwerk-Giebelhäuser am Hansehafen
    s += gable_house(335, 56, 110, "#f4ecdc", "#b8483a", timber=True)
    s += gable_house(395, 50, 124, "#f6e3b4", "#c9553d", timber=True)
    s += gable_house(449, 56, 104, "#eef3f7", "#7a8796", timber=True)
    # St. Cosmae et Damiani: Turm mit barocker Haube
    s += rect(530, 420, 160, 158, "#c0603f") + poly([(524, 420), (610, 370), (696, 420)], "#7a8796")
    s += windows(552, 450, 3, 1, 44, 0, 16, 60, arch=True)
    s += rect(580, 250, 60, 328, "#b0523a") + windows(596, 280, 1, 3, 0, 56, 28, 34, arch=True)
    s += f'<path d="M574,252 Q610,190 646,252 Z" fill="#6fae8c" stroke="{LINE}" stroke-width="{SW}"/>'
    s += rect(597, 178, 26, 40, "#6fae8c", 2.5) + f'<path d="M592,180 Q610,140 628,180 Z" fill="#6fae8c" stroke="{LINE}" stroke-width="{SW}"/>'
    s += spire(610, 104, 150, 16, "#6fae8c")
    # Holzkran am Hafen
    s += rect(740, 480, 64, 98, "#e9d3a8") + poly([(732, 480), (772, 446), (812, 480)], "#7a8796")
    s += line(772, 460, 860, 420, 5, "#6a4426") + line(860, 420, 860, 488, 2.5)
    s += gable_house(880, 52, 100, "#f6e3b4", "#c9553d", timber=True) + gable_house(938, 56, 116, "#f4ecdc", "#b8483a", timber=True)
    # kleiner Ewer (Segelschiff) im Hafen – sitzt auf dem Wasser vor der Uferkante
    return s

def Wasserburg():
    s = house_row(10, 1330, seed=9)
    # Pastellfarbene Inn-Salzach-Häuser
    cols = ["#f3d27a", "#f2b8b0", "#bfe0c4", "#f6e3b4", "#c9dcef", "#f3d27a"]
    x = 30
    for i, (w, h) in enumerate([(70, 130), (60, 150), (72, 120), (64, 140)]):
        s += flat_front_house(x, w, h, cols[i]); x += w + 6
    # Brucktor: Stadttor mit Staffelgiebel und Durchfahrt
    s += rect(330, 320, 110, 258, "#f0e2c4") + stepped_gable_house(330, 110, 258, "#f0e2c4", steps=4, wins=False)
    s += f'<path d="M360,578 L360,520 A25,25 0 0 1 410,520 L410,578 Z" fill="#6b5a4a" stroke="{LINE}" stroke-width="{SW}"/>'
    s += circle(385, 400, 18, "#ffffff", 2.5) + line(385, 400, 385, 388, 2.5) + line(385, 400, 394, 404, 2.5)
    s += windows(350, 440, 3, 1, 28, 0, 14, 22)
    # St. Jakob: hoher Kirchturm
    s += rect(470, 420, 210, 158, "#f4ecdc") + poly([(464, 420), (575, 360), (686, 420)], "#c9553d")
    s += windows(500, 450, 4, 1, 44, 0, 18, 64, arch=True)
    s += rect(610, 220, 64, 358, "#efe3c8") + windows(628, 250, 1, 4, 0, 62, 28, 36, arch=True)
    s += spire(642, 80, 222, 76, "#6b7a8f")
    # Rathaus mit Staffelgiebel
    s += stepped_gable_house(720, 120, 150, "#f3d27a", steps=5)
    x = 850
    for i, (w, h) in enumerate([(66, 128), (70, 112), (64, 138)]):
        s += flat_front_house(x, w, h, cols[(i + 3) % 6]); x += w + 6
    return s

STAEDTE = {"Lueneburg": Lueneburg, "Stade": Stade, "Wasserburg": Wasserburg}

# ---------------- Komposition ----------------
def keep_mask(lupe):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    # alles unterhalb der Uferkante bleibt original; links bleibt die Brücke stehen
    d.polygon([(0, 546), (487, 546), (487, 590), (W, 590), (W, H), (0, H)], fill=255)
    d.rectangle([1330, 0, W, H], fill=255)          # Figur
    if lupe:
        d.ellipse([1140 - 156, 368 - 156, 1140 + 156, 368 + 156], fill=255)  # Lupe
        d.polygon([(1230, 470), (1262, 452), (1300, 520), (1268, 540)], fill=255)  # Griff
        d.ellipse([1236, 474, 1300, 548], fill=255)     # Hand
        d.rectangle([1292, 420, W, H], fill=255)
    else:
        d.rectangle([1066, 438, W, H], fill=255)    # Briefkasten + Arm
    return m

def build(slug):
    os.makedirs(OUT, exist_ok=True)
    body = STAEDTE[slug]()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>{arcs()}'
           f'<g>{body}</g><line x1="0" y1="{GROUND}" x2="{W}" y2="{GROUND}" stroke="{LINE}" stroke-width="2"/></svg>')
    svg_path = os.path.join(OUT, f"{slug}.svg")
    open(svg_path, "w").write(svg)
    png = os.path.join(OUT, f"{slug}_bg.png")
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", png, svg_path], check=True)
    bg = Image.open(png).convert("RGB")
    for lupe in (False, True):
        src = Image.open(os.path.join(BASE, "Stadt_Allgemein_Lupe.jpg" if lupe else "Stadt_Allgemein.jpg")).convert("RGB")
        res = bg.copy()
        m = np.array(keep_mask(lupe))
        a = np.array(src).astype(int)
        # Hügel-Grün (185,220,162) und Hügelkontur aus behaltenen Bereichen oberhalb des Ufers entfernen
        hill = (np.abs(a[..., 0] - 185) < 26) & (np.abs(a[..., 1] - 220) < 22) & (np.abs(a[..., 2] - 162) < 26)
        yy, xx = np.mgrid[0:H, 0:W]
        lens = ((xx - 1140) ** 2 + (yy - 368) ** 2) < 128 ** 2 if lupe else np.zeros_like(hill)
        m[(hill) & (yy < 590) & (~lens)] = 0
        res.paste(src, (0, 0), Image.fromarray(m.astype(np.uint8)))
        name = f"Stadt_{slug}{'_Lupe' if lupe else ''}.jpg"
        res.save(os.path.join(OUT, name), quality=90)
        print(name)

if __name__ == "__main__":
    for s in sys.argv[1:] or STAEDTE:
        build(s)
