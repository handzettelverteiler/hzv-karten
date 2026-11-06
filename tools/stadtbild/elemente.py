"""Baukasten für Stadtsilhouetten (Stil v3). Alle Elemente stehen auf GROUND und geben SVG zurück."""
from stadtbild import rect, poly, line, circle, win, windows, spire, stepped_gable_house, gable_house, flat_front_house, tree, LINE, SW, GROUND

G = GROUND
BRICK, BRICK_D, SAND, WHITE, YELLOW, REDSAND, GREY_W = "#b9573b", "#a64b33", "#e9d9b4", "#f4ecdc", "#f3d27a", "#c97a5e", "#e6e2da"
SLATE, COPPER, ROOF_RED = "#6b7a8f", "#6fae8c", "#c9553d"

def path(d, fill, sw=SW):
    return f'<path d="{d}" fill="{fill}" stroke="{LINE}" stroke-width="{sw}" stroke-linejoin="round"/>'

def onion(cx, y, w, fill=COPPER):
    """Zwiebelhaube, Unterkante y."""
    h = w * 1.25
    return (path(f"M{cx-w/2},{y} Q{cx-w*0.75},{y-h*0.45} {cx},{y-h*0.8} Q{cx+w*0.75},{y-h*0.45} {cx+w/2},{y} Z", fill)
            + line(cx, y - h * 0.8, cx, y - h - 6, 2.5) + circle(cx, y - h - 8, 3.5, "#e2b23a", 2))

def helm(cx, y, w, fill=COPPER):
    """barocke Haube mit Laterne."""
    return (path(f"M{cx-w/2},{y} Q{cx},{y-w*0.9} {cx+w/2},{y} Z", fill)
            + rect(cx - w * 0.16, y - w * 0.95, w * 0.32, w * 0.42, fill, 2.5)
            + path(f"M{cx-w*0.22},{y-w*0.93} Q{cx},{y-w*1.35} {cx+w*0.22},{y-w*0.93} Z", fill, 2.5)
            + line(cx, y - w * 1.25, cx, y - w * 1.45, 2.5))

def dome(cx, y, w, fill=COPPER):
    return path(f"M{cx-w/2},{y} A{w/2},{w/2} 0 0 1 {cx+w/2},{y} Z", fill) + line(cx, y - w / 2, cx, y - w / 2 - 14, 2.5) + circle(cx, y - w / 2 - 16, 3.5, "#e2b23a", 2)

def battlement(x, y, w, fill):
    out, n = "", max(3, int(w // 14))
    step = w / n
    for i in range(0, n, 2):
        out += rect(x + i * step, y - 12, step, 12, fill, 2.5)
    return out

def top(kind, cx, y, w, fill=None):
    if kind == "spire":   return spire(cx, y - w * 2.4, y, w * 1.05, fill or SLATE)
    if kind == "spire_g": return spire(cx, y - w * 2.4, y, w * 1.05, fill or COPPER)
    if kind == "pyramid": return poly([(cx - w / 2 - 4, y), (cx, y - w * 0.9), (cx + w / 2 + 4, y)], fill or SLATE)
    if kind == "onion":   return onion(cx, y, w * 0.95, fill or COPPER)
    if kind == "helm":    return helm(cx, y, w, fill or COPPER)
    if kind == "dome":    return dome(cx, y, w, fill or COPPER)
    if kind == "flat":    return battlement(cx - w / 2, y, w, fill or GREY_W)
    if kind == "gable":   return poly([(cx - w / 2 - 3, y), (cx, y - w * 0.7), (cx + w / 2 + 3, y)], fill or ROOF_RED)
    return ""

def turm(x, w=56, h=230, wall=BRICK, kind="spire", topfill=None, clock=False, wins=3):
    out = rect(x, G - h, w, h, wall)
    out += windows(x + w / 2 - 11, G - h + 28, 1, wins, 0, 52, 22, 32, arch=True)
    if clock:
        out += circle(x + w / 2, G - h + 18 + wins * 52, 13, "#fff", 2.5)
    return out + top(kind, x + w / 2, G - h, w, topfill)

def kirche(x, w=190, h=140, wall=WHITE, roof=SLATE, tower="spire", tpos="left", tw=58, th=250, twall=None, topfill=None):
    tx = {"left": x - tw * 0.4, "right": x + w - tw * 0.6, "center": x + w / 2 - tw / 2}[tpos]
    out = rect(x, G - h, w, h, wall) + poly([(x - 5, G - h), (x + w / 2, G - h - w * 0.32), (x + w + 5, G - h)], roof)
    out += windows(x + 24, G - h + 30, max(2, int((w - 40) // 40)), 1, 40, 0, 18, 60, arch=True)
    return out + turm(tx, tw, th, twall or wall, tower, topfill)

def dom(x, w=220, h=170, wall=SAND, th=320, tw=60, kind="spire", topfill=None, vier=False):
    """Doppelturmfassade (optional zusätzliche Osttürme)."""
    out = ""
    if vier:
        out += turm(x + w + 40, tw * 0.8, th * 0.82, wall, kind, topfill, wins=3)
    out += rect(x + 20, G - h - 30, w + 40, h + 30, wall) + poly([(x + 14, G - h - 30), (x + w / 2 + 40, G - h - 100), (x + w + 66, G - h - 30)], SLATE)
    out += windows(x + 70, G - h + 10, 4, 1, 34, 0, 16, 70, arch=True)
    out += turm(x - tw / 2 + 20, tw, th, wall, kind, topfill, wins=4) + turm(x + w + 20 - tw / 2 + 20, tw, th, wall, kind, topfill, wins=4)
    out += circle(x + w / 2 + 40, G - h + 40, 22, "#cfe3f3", 2.5)
    out += f'<path d="M{x+w/2+28},{G} L{x+w/2+28},{G-34} A12,12 0 0 1 {x+w/2+52},{G-34} L{x+w/2+52},{G} Z" fill="#8a5a3a" stroke="{LINE}" stroke-width="2.5"/>'
    if vier:
        out += turm(x - 70, tw * 0.8, th * 0.82, wall, kind, topfill, wins=3)
    return out

def rathaus(x, w=150, h=130, wall=YELLOW, gable="stepped", clock=True, roof=ROOF_RED):
    if gable == "stepped":
        out = stepped_gable_house(x, w, h, wall, steps=5)
    elif gable == "baroque":
        y = G - h
        out = rect(x, y, w, h, wall) + path(f"M{x},{y} Q{x+w*0.2},{y-30} {x+w*0.3},{y-50} L{x+w*0.3},{y-80} Q{x+w/2},{y-120} {x+w*0.7},{y-80} L{x+w*0.7},{y-50} Q{x+w*0.8},{y-30} {x+w},{y} Z", wall)
        out += windows(x + 16, y + 18, max(2, int(w // 34)), max(1, int((h - 30) // 40)), (w - 30) / max(2, int(w // 34)), 40, 16, 24)
    else:
        out = gable_house(x, w, h, wall, roof)
    if clock:
        out += circle(x + w / 2, G - h - 20 if gable != "gable" else G - h + 22, 13, "#fff", 2.5)
    return out

def schloss(x, w=340, h=120, wall=YELLOW, roof=SLATE, towers=(("dome", 0.0), ("dome", 1.0)), mid="dome", tw=50, th=180, twall=None):
    y = G - h
    out = ""
    for kind, pos in towers:
        out += turm(x + pos * w - tw / 2, tw, th, twall or wall, kind, wins=2)
    out += rect(x, y, w, h, wall) + poly([(x - 6, y), (x + 20, y - 40), (x + w - 20, y - 40), (x + w + 6, y)], roof)
    out += windows(x + 20, y + 20, max(4, int(w // 34)), 2, (w - 34) / max(4, int(w // 34)), 46, 16, 26)
    if mid:
        out += rect(x + w / 2 - 40, y - 30, 80, 30 + h, wall) + top(mid, x + w / 2, y - 30, 70)
        out += f'<path d="M{x+w/2-14},{G} L{x+w/2-14},{G-36} A14,14 0 0 1 {x+w/2+14},{G-36} L{x+w/2+14},{G} Z" fill="#8a5a3a" stroke="{LINE}" stroke-width="2.5"/>'
    return out

def huegel(x, w, h, fill="#bfe0a8"):
    out = path(f"M{x},{G} Q{x+w*0.15},{G-h} {x+w/2},{G-h} Q{x+w*0.85},{G-h} {x+w},{G} Z", fill)
    for k in (0.18, 0.8):
        out += tree(x + w * k, 40).replace(f"{G}", f"{G}")
    return out

def burg(x, w=280, hh=120, wall="#d9cfb8", keep_h=130, ruine=False):
    """Burg auf Hügel."""
    out = huegel(x - 40, w + 80, hh)
    b = G - hh + 10
    out += rect(x + 20, b - 70, w - 40, 70, wall) + battlement(x + 20, b - 70, w - 40, wall)
    out += rect(x + w / 2 - 30, b - 70 - keep_h, 60, keep_h, wall) + windows(x + w / 2 - 8, b - 70 - keep_h + 24, 1, 2, 0, 40, 16, 24, arch=True)
    out += (battlement(x + w / 2 - 30, b - 70 - keep_h, 60, wall) if ruine else top("pyramid", x + w / 2, b - 70 - keep_h, 60, ROOF_RED))
    out += windows(x + 40, b - 50, max(3, int((w - 60) // 40)), 1, 40, 0, 14, 22, arch=True)
    return out

def tor(x, w=90, h=210, wall="#e0cba0", kind="stepped"):
    out = rect(x, G - h, w, h, wall)
    out += f'<path d="M{x+w*0.25},{G} L{x+w*0.25},{G-48} A{w*0.25},{w*0.25} 0 0 1 {x+w*0.75},{G-48} L{x+w*0.75},{G} Z" fill="#6b5a4a" stroke="{LINE}" stroke-width="{SW}"/>'
    out += windows(x + w / 2 - 22, G - h + 30, 2, 2, 30, 46, 14, 22, arch=True)
    if kind == "stepped":
        out = stepped_gable_house(x, w, h, wall, steps=3, wins=False) + out[len(rect(x, G - h, w, h, wall)):]
    else:
        out += top(kind, x + w / 2, G - h, w)
    return out

def wasserturm(x, w=90, h=230, wall=BRICK, kind="dome", kopf=True):
    out = rect(x + 10, G - h + 40, w - 20, h - 40, wall) + windows(x + w / 2 - 9, G - h + 70, 1, 3, 0, 46, 18, 26, arch=True)
    if kopf:
        out += rect(x - 6, G - h, w + 12, 42, wall) + windows(x + 4, G - h + 10, 4, 1, (w - 10) / 4, 0, 12, 18)
    return out + top(kind, x + w / 2, G - h, w + 14)

def hochhaus(x, w=70, h=280, fill="#cfe0ef", spitze=False):
    out = rect(x, G - h, w, h, fill)
    for k in range(1, int(h // 26)):
        out += line(x + 4, G - h + k * 26, x + w - 4, G - h + k * 26, 1.5, "#8fa9c2")
    out += line(x + w / 2, G - h, x + w / 2, G, 1.5, "#8fa9c2")
    if spitze:
        out += line(x + w / 2, G - h, x + w / 2, G - h - 40, 3)
    return out

def foerderturm(x, h=230):
    b, t = G, G - h
    out = rect(x - 20, G - 80, 140, 80, BRICK) + windows(x - 6, G - 64, 4, 1, 32, 0, 14, 22, arch=True)
    out += line(x + 10, b - 80, x + 40, t, 6, "#3e8e5a") + line(x + 90, b - 80, x + 60, t, 6, "#3e8e5a")
    for k in range(1, 5):
        yy = b - 80 - k * (h - 80) / 5
        out += line(x + 10 + 30 * k / 5, yy, x + 90 - 30 * k / 5, yy, 4, "#3e8e5a")
    out += line(x + 40, t, x + 60, t, 6, "#3e8e5a")
    out += circle(x + 38, t - 10, 14, "#fff", 4) + circle(x + 62, t - 10, 14, "#fff", 4)
    return out

def fachwerk(x, n=3, w=54):
    out, cols = "", ["#f4ecdc", "#f6e3b4", "#eef3f7", "#f2d9c4"]
    for i in range(n):
        out += gable_house(x + i * (w + 6), w, 96 + (i % 2) * 20, cols[i % 4], [ROOF_RED, "#b8483a", SLATE][i % 3], timber=True)
    return out

def kurhaus(x, w=300, h=110, wall=WHITE):
    y = G - h
    out = rect(x, y, w, h, wall) + rect(x - 8, y - 14, w + 16, 14, wall, 2.5)
    out += poly([(x + w / 2 - 80, y - 14), (x + w / 2, y - 60), (x + w / 2 + 80, y - 14)], wall)
    for k in range(9):
        cx = x + 20 + k * (w - 40) / 8
        out += rect(cx - 6, y + 6, 12, h - 6, "#fff", 2.5)
    return out

def denkmal(x, hh=150):
    """Statue mit erhobenem Schwert auf Rundsockel, auf bewaldetem Hügel (z. B. Hermannsdenkmal)."""
    out = huegel(x - 140, 300, hh, "#9fcf88")
    b = G - hh + 6
    out += rect(x - 26, b - 110, 52, 110, "#d8d2c4") + poly([(x - 34, b - 110), (x, b - 140), (x + 34, b - 110)], COPPER)
    out += rect(x - 9, b - 210, 18, 72, COPPER, 2.5) + circle(x, b - 218, 10, COPPER, 2.5)
    out += line(x + 6, b - 200, x + 30, b - 270, 5, "#7aa38f")
    return out

def muehle(x, h=150):
    out = poly([(x, G), (x + 20, G - h), (x + 60, G - h), (x + 80, G)], WHITE) + poly([(x + 14, G - h), (x + 40, G - h - 40), (x + 66, G - h)], SLATE)
    cx, cy = x + 40, G - h - 4
    for a, b in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        out += line(cx, cy, cx + a * 70, cy + b * 70, 9, "#8a6a4a")
    return out + circle(cx, cy, 8, "#555", 2)

def gradierwerk(x, w=360, h=90):
    out = rect(x, G - h, w, h, "#9b7a52")
    for k in range(1, int(w // 18)):
        out += line(x + k * 18, G - h, x + k * 18, G, 1.5, "#6f5536")
    return out + rect(x - 6, G - h - 12, w + 12, 12, "#7a5e3c", 2.5)

def kran(x, h=170, col="#e2a93b"):
    return (rect(x, G - h, 16, h, col, 2.5) + line(x + 8, G - h, x + 140, G - h + 10, 5, col)
            + line(x + 8, G - h, x - 40, G - h + 8, 5, col) + rect(x - 52, G - h + 6, 20, 22, "#888", 2) + line(x + 120, G - h + 10, x + 120, G - h + 70, 2))

def bruecke_haeuser(x, w=300):
    out = rect(x, G - 40, w, 40, "#c8b48f")
    for k in range(3):
        cx = x + 50 + k * 100
        out += f'<path d="M{cx-30},{G} A30,30 0 0 1 {cx+30},{G} Z" fill="#b8dbeb" stroke="{LINE}" stroke-width="2.5"/>'
    for k, (ww, hh) in enumerate(((70, 90), (80, 110), (66, 96))):
        out += '<g transform="translate(0,-40)">' + gable_house(x + 20 + k * 95, ww, hh, ["#f4ecdc", "#f6e3b4", "#f2d9c4"][k], ROOF_RED, timber=True) + '</g>'
    return out

def modern(x, w=150, h=120, fill="#e8edf2"):
    out = rect(x, G - h, w, h, fill) + windows(x + 12, G - h + 14, max(3, int(w // 30)), max(2, int((h - 20) // 30)), (w - 20) / max(3, int(w // 30)), 30, 18, 16)
    return out

def festspielhaus(x, w=240, h=130):
    y = G - h
    out = rect(x, y, w, h, "#c96a4a") + poly([(x - 4, y), (x + w / 2, y - 90), (x + w + 4, y)], "#c96a4a")
    out += rect(x + w / 2 - 50, y - 30, 100, 30, "#c96a4a", 2.5) + windows(x + 20, y + 30, 6, 1, (w - 40) / 6, 0, 16, 40, arch=True)
    return out

def windrad(x, h=240):
    cx, cy = x, G - h
    out = poly([(cx - 5, G), (cx - 2, cy), (cx + 2, cy), (cx + 5, G)], "#fff", 2.5)
    for a in (0, 120, 240):
        out += f'<path d="M{cx},{cy} L{cx+6},{cy-92} L{cx-2},{cy-94} Z" fill="#fff" stroke="{LINE}" stroke-width="2.5" transform="rotate({a} {cx} {cy})"/>'
    return out + circle(cx, cy, 6, "#ddd", 2)

def leuchtturm(x, h=230):
    out = poly([(x, G), (x + 12, G - h), (x + 58, G - h), (x + 70, G)], "#fff")
    for k in range(4):
        y = G - h + 30 + k * (h - 40) / 4
        out += rect(x + 10 - k * 1.5 + 2, y, 50 + k * 3 - 4, 22, "#d8262b", 2)
    out += rect(x + 14, G - h - 34, 42, 34, "#f6e3b4") + poly([(x + 8, G - h - 34), (x + 35, G - h - 60), (x + 62, G - h - 34)], "#d8262b")
    return out

def weinberg(x, w=320, h=150):
    """Hügel mit Rebzeilen."""
    out = path(f"M{x},{G} Q{x+w*0.2},{G-h} {x+w/2},{G-h} Q{x+w*0.8},{G-h} {x+w},{G} Z", "#cfe6a8")
    for k in range(1, 7):
        yy = G - h + k * h / 7
        out += f'<path d="M{x+w*0.12+k*6},{yy} L{x+w*0.88-k*6},{yy}" stroke="#6a9e3a" stroke-width="4" stroke-dasharray="10 6"/>'
    return out

def freitreppen_rathaus(x, w=170, h=120, wall=YELLOW):
    """Rathaus mit doppelter Freitreppe und Turmhaube (z. B. Deidesheim)."""
    y = G - h
    out = rect(x, y, w, h, wall) + poly([(x - 5, y), (x + w / 2, y - 60), (x + w + 5, y)], ROOF_RED)
    out += turm(x + w / 2 - 20, 40, h + 90, wall, "helm", wins=1)
    out += poly([(x - 40, G), (x + w / 2 - 20, G - 50), (x + w / 2 - 20, G - 40), (x - 26, G)], "#d9cfb8", 2.5)
    out += poly([(x + w + 40, G), (x + w / 2 + 20, G - 50), (x + w / 2 + 20, G - 40), (x + w + 26, G)], "#d9cfb8", 2.5)
    return out + windows(x + 14, y + 16, 4, 1, (w - 26) / 4, 0, 16, 26)

def zementwerk(x):
    out = rect(x, G - 170, 50, 170, "#d7d7d7") + rect(x + 56, G - 200, 50, 200, "#d7d7d7") + rect(x + 112, G - 150, 50, 150, "#d7d7d7")
    out += rect(x + 170, G - 260, 22, 260, "#c9c9c9") + rect(x - 30, G - 70, 230, 70, "#e6e2da")
    return out

def achterbahn(x, w=260, h=150):
    out = f'<path d="M{x},{G-20} Q{x+w*0.25},{G-h*1.2} {x+w*0.45},{G-h*0.5} Q{x+w*0.6},{G-h*0.1} {x+w*0.75},{G-h*0.8} Q{x+w*0.9},{G-h*1.1} {x+w},{G-30}" fill="none" stroke="#d8262b" stroke-width="7"/>'
    for k in range(1, 10):
        xx = x + k * w / 10
        out += line(xx, G, xx, G - h * (0.4 + 0.4 * ((k % 3) / 2)), 2.5, "#888")
    return out
