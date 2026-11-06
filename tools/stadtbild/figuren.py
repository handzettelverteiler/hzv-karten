"""4 Figuren-Varianten (verkaufsfördernd) auf dem Lüneburg-Hintergrund."""
import os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stadtbild as sb

W, H = 1600, 873
L = "#2b2b2b"
BLUE, BLUE_D, NAVY = "#2f6dbf", "#2559a3", "#1f2d4d"
HAIR, RED, SKIN = "#f2c230", "#d8262b", "#ffffff"
OUT = sb.OUT

def svgwrap(body, bg=False):
    b = f'<rect width="{W}" height="{H}" fill="#ffffff"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{b}{body}</svg>'

def render(svg, path):
    open(path + ".svg", "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", path, path + ".svg"], check=True)
    return Image.open(path).convert("RGBA")

def red_hand(x, y, s=1.0):
    p = f'<g transform="translate({x},{y}) scale({s})" fill="{RED}">'
    p += '<ellipse cx="0" cy="8" rx="12" ry="13"/>'
    for ang, ln in ((-52, 20), (-24, 24), (2, 25), (28, 22), (-95, 18)):
        p += f'<rect x="-3.6" y="{-ln}" width="7.2" height="{ln}" rx="3.6" transform="translate(0,4) rotate({ang}) translate(0,-6)"/>'
    return p + "</g>"

def arm(points, sleeve=True):
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    return (f'<path d="{d}" fill="none" stroke="{L}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="37" stroke-linecap="round" stroke-linejoin="round"/>')

def hand(x, y):
    return f'<circle cx="{x}" cy="{y}" r="15" fill="#fff" stroke="{L}" stroke-width="4"/>'

def figure(cx, arm_l, arm_r, bag=True, smile_big=False, front_l=False, front_r=False):
    """Briefträger frontal. arm_l / arm_r: Punktlisten von der Schulter zur Hand (Hand = letzter Punkt)."""
    g = ""
    # Schatten
    g += f'<ellipse cx="{cx}" cy="852" rx="120" ry="12" fill="#e6e6e6"/>'
    # Arme hinter dem Körper
    if not front_l: g += arm(arm_l)
    if not front_r: g += arm(arm_r)
    # Beine + Schuhe
    for lx in (cx - 52, cx + 10):
        g += f'<rect x="{lx}" y="600" width="42" height="232" fill="{BLUE}" stroke="{L}" stroke-width="4"/>'
    g += f'<line x1="{cx-31}" y1="630" x2="{cx-31}" y2="820" stroke="{BLUE_D}" stroke-width="2"/>'
    g += f'<line x1="{cx+31}" y1="630" x2="{cx+31}" y2="820" stroke="{BLUE_D}" stroke-width="2"/>'
    for sx in (cx - 60, cx + 4):
        g += f'<path d="M{sx},826 L{sx+56},826 Q{sx+72},836 {sx+66},848 L{sx-6},848 Q{sx-10},834 {sx},826 Z" fill="#fff" stroke="{L}" stroke-width="4"/>'
    # Jacke
    g += (f'<path d="M{cx-78},430 Q{cx-80},402 {cx-50},398 L{cx+50},398 Q{cx+80},402 {cx+78},430 '
          f'L{cx+68},612 L{cx-68},612 Z" fill="{BLUE}" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>')
    g += f'<line x1="{cx}" y1="440" x2="{cx}" y2="612" stroke="{BLUE_D}" stroke-width="3"/>'
    for by in (470, 515, 560):
        g += f'<circle cx="{cx+10}" cy="{by}" r="4" fill="{NAVY}"/>'
    g += f'<line x1="{cx-60}" y1="560" x2="{cx-28}" y2="560" stroke="{BLUE_D}" stroke-width="3"/>'
    # Kragen, Hemd, Krawatte
    g += f'<path d="M{cx-26},398 L{cx},440 L{cx+26},398 Z" fill="#fff" stroke="{L}" stroke-width="3.5"/>'
    g += f'<path d="M{cx-6},406 L{cx+6},406 L{cx+8},446 L{cx},458 L{cx-8},446 Z" fill="{NAVY}"/>'
    # Arme vor dem Körper
    if front_l: g += arm(arm_l)
    if front_r: g += arm(arm_r)
    g += hand(*arm_l[-1]) + hand(*arm_r[-1])
    # Tasche + Gurt
    if bag:
        g += f'<line x1="{cx-48}" y1="402" x2="{cx+92}" y2="540" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
        g += f'<rect x="{cx+62}" y="530" width="100" height="96" rx="8" fill="#3d77b8" stroke="{L}" stroke-width="4"/>'
        g += f'<path d="M{cx+62},556 L{cx+162},556" stroke="{L}" stroke-width="3"/>'
        g += red_hand(cx + 112, 594, 1.2)
        g += f'<path d="M{cx+80},530 Q{cx+100},500 {cx+128},508 Q{cx+150},500 {cx+152},530 Z" fill="#6dbb63" stroke="{L}" stroke-width="3"/>'
    # Hals + Kopf
    g += f'<line x1="{cx}" y1="372" x2="{cx}" y2="400" stroke="{L}" stroke-width="5"/>'
    g += f'<circle cx="{cx}" cy="318" r="58" fill="#fff" stroke="{L}" stroke-width="4.5"/>'
    # Haare rechts
    g += f'<path d="M{cx+38},284 L{cx+66},282 L{cx+70},318 L{cx+60},306 L{cx+56},328 L{cx+46},304 Z" fill="{HAIR}" stroke="{L}" stroke-width="3"/>'
    # Mütze
    g += (f'<path d="M{cx-58},292 Q{cx-56},228 {cx+6},224 Q{cx+70},224 {cx+72},292 Z" fill="{BLUE}" stroke="{L}" stroke-width="4.5"/>'
          f'<rect x="{cx-60}" y="276" width="134" height="20" fill="{BLUE_D}" stroke="{L}" stroke-width="4"/>'
          f'<path d="M{cx-58},294 Q{cx-120},292 {cx-112},314 Q{cx-80},308 {cx-40},300 Z" fill="{NAVY}" stroke="{L}" stroke-width="4"/>')
    g += red_hand(cx + 8, 252, 0.9)
    # Gesicht
    g += f'<ellipse cx="{cx-14}" cy="318" rx="6" ry="9" fill="{L}"/><ellipse cx="{cx+22}" cy="318" rx="6" ry="9" fill="{L}"/>'
    if smile_big:
        g += f'<path d="M{cx-26},340 Q{cx+4},378 {cx+34},340 Q{cx+4},356 {cx-26},340 Z" fill="#fff" stroke="{L}" stroke-width="4"/>'
    else:
        g += f'<path d="M{cx-24},342 Q{cx+2},368 {cx+30},342" fill="none" stroke="{L}" stroke-width="4.5" stroke-linecap="round"/>'
    return g

def flyer(x, y, rot=0, w=46, h=62, col="#ffe27a"):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="{col}" stroke="{L}" stroke-width="3"/>'
            f'<line x1="{-w/2+8}" y1="{-h/2+12}" x2="{w/2-8}" y2="{-h/2+12}" stroke="{RED}" stroke-width="4"/>'
            f'<line x1="{-w/2+8}" y1="{-h/2+24}" x2="{w/2-12}" y2="{-h/2+24}" stroke="{L}" stroke-width="2"/>'
            f'<line x1="{-w/2+8}" y1="{-h/2+32}" x2="{w/2-16}" y2="{-h/2+32}" stroke="{L}" stroke-width="2"/></g>')

def check(x, y, r=26):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#34a853" stroke="{L}" stroke-width="3.5"/>'
            f'<path d="M{x-r*0.45},{y} L{x-r*0.1},{y+r*0.35} L{x+r*0.5},{y-r*0.35}" fill="none" stroke="#fff" stroke-width="{r*0.22}" stroke-linecap="round" stroke-linejoin="round"/>')

def bubble(x, y, w, text, size=30):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="16" fill="#fff" stroke="{L}" stroke-width="3.5"/>'
            f'<path d="M{x+40},{y+56} L{x+30},{y+80} L{x+64},{y+56}" fill="#fff" stroke="{L}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<rect x="{x+28}" y="{y+52}" width="40" height="6" fill="#fff"/>'
            f'<text x="{x+w/2}" y="{y+39}" font-family="Arial" font-weight="bold" font-size="{size}" text-anchor="middle" fill="{L}">{text}</text>')

# ---------------- Varianten ----------------
CX = 1430
SH_L, SH_R = (CX - 70, 425), (CX + 70, 425)

def v1_foto():
    """Fotonachweis: fotografiert eingeworfene Flyer am Briefkasten mit dem Smartphone."""
    g = ""
    # Hausbriefkasten an Pfosten
    g += f'<rect x="1150" y="560" width="14" height="290" fill="#8a8f96" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="1090" y="470" width="134" height="104" rx="10" fill="#e8ecef" stroke="{L}" stroke-width="4"/>'
    g += f'<rect x="1112" y="492" width="90" height="12" rx="3" fill="{L}"/>'
    g += flyer(1157, 486, -6, 40, 44)
    g += f'<rect x="1140" y="526" width="34" height="22" rx="3" fill="#fff" stroke="{L}" stroke-width="2.5"/>'
    g += figure(CX, [SH_L, (CX - 140, 470), (CX - 175, 420)], [SH_R, (CX + 112, 520), (CX + 92, 600)])
    # Smartphone in linker Hand, Bildschirm zum Betrachter geneigt
    g += f'<rect x="-34" y="-62" width="68" height="118" rx="10" fill="{NAVY}" stroke="{L}" stroke-width="4" transform="translate({CX-180},392) rotate(-12)"/>'
    g += f'<rect x="-27" y="-52" width="54" height="92" rx="5" fill="#cfe3f3" transform="translate({CX-180},392) rotate(-12)"/>'
    g += f'<g transform="translate({CX-180},386) rotate(-12)">{check(0, 0, 18)}</g>'
    # Blitz-Strahlen Richtung Briefkasten
    for dx, dy in ((-60, 30), (-74, 60), (-66, 0)):
        g += f'<line x1="{CX-222}" y1="{410}" x2="{CX-222+dx}" y2="{410+dy}" stroke="#f2b01e" stroke-width="5" stroke-linecap="round"/>'
    g += bubble(1000, 290, 270, "Foto-Nachweis ✓", 30)
    return g

def v2_daumen():
    """Zuverlässigkeit: Daumen hoch + Klemmbrett mit abgehakter Liste."""
    g = figure(CX, [SH_L, (CX - 110, 500), (CX - 34, 560)], [SH_R, (CX + 130, 380), (CX + 132, 300)], smile_big=True, front_l=True)
    # Daumen über rechter Hand
    g += f'<rect x="{CX+124}" y="262" width="16" height="34" rx="8" fill="#fff" stroke="{L}" stroke-width="4"/>'
    # Klemmbrett in linker Hand vor dem Körper
    x, y = CX - 150, 470
    g += f'<rect x="{x}" y="{y}" width="120" height="160" rx="8" fill="#c99a63" stroke="{L}" stroke-width="4"/>'
    g += f'<rect x="{x+10}" y="{y+16}" width="100" height="136" fill="#fff" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{x+38}" y="{y-8}" width="44" height="18" rx="4" fill="#8a8f96" stroke="{L}" stroke-width="3"/>'
    for i in range(4):
        yy = y + 40 + i * 30
        g += f'<path d="M{x+18},{yy} L{x+25},{yy+7} L{x+38},{yy-8}" fill="none" stroke="#34a853" stroke-width="5" stroke-linecap="round"/>'
        g += f'<line x1="{x+48}" y1="{yy}" x2="{x+100}" y2="{yy}" stroke="{L}" stroke-width="3"/>'
    g += hand(CX - 34, 560)
    g += bubble(1030, 380, 300, "Alles verteilt!", 32)
    return g

def v3_rad():
    """Lokal & schnell: Lastenrad voller Flyer."""
    g = ""
    def wheel(x, y, r):
        s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{L}" stroke-width="9"/><circle cx="{x}" cy="{y}" r="{r-9}" fill="none" stroke="#9aa3ad" stroke-width="3"/>'
        for a in range(0, 180, 30):
            import math
            dx, dy = (r - 10) * math.cos(math.radians(a)), (r - 10) * math.sin(math.radians(a))
            s += f'<line x1="{x-dx}" y1="{y-dy}" x2="{x+dx}" y2="{y+dy}" stroke="#9aa3ad" stroke-width="2"/>'
        return s + f'<circle cx="{x}" cy="{y}" r="7" fill="{L}"/>'
    # Lastenrad links, Figur hält den Lenker
    g += wheel(1010, 800, 48) + wheel(1250, 800, 48)
    g += f'<path d="M1010,800 L1080,800 L1135,700 L1250,800 M1135,700 L1195,700 L1250,800" fill="none" stroke="{RED}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    g += f'<path d="M1195,700 L1214,630 L1262,624" fill="none" stroke="{L}" stroke-width="9" stroke-linecap="round"/>'
    g += f'<path d="M1120,700 L1150,690" stroke="{L}" stroke-width="12" stroke-linecap="round"/>'
    g += f'<rect x="958" y="650" width="140" height="110" rx="8" fill="{BLUE}" stroke="{L}" stroke-width="4"/>'
    g += red_hand(1028, 708, 1.6)
    for i, (fx, rot) in enumerate(((980, -12), (1008, -4), (1036, 6), (1066, 14))):
        g += flyer(fx + 10, 632 - (i % 2) * 8, rot, 40, 54)
    g += figure(CX, [SH_L, (CX - 120, 540), (CX - 168, 624)], [SH_R, (CX + 112, 520), (CX + 92, 600)])
    g += bubble(1000, 470, 300, "Schnell vor Ort", 32)
    return g

def xmark(x, y, r=22):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED}" stroke="{L}" stroke-width="3.5"/>'
            f'<path d="M{x-r*0.4},{y-r*0.4} L{x+r*0.4},{y+r*0.4} M{x+r*0.4},{y-r*0.4} L{x-r*0.4},{y+r*0.4}" stroke="#fff" stroke-width="{r*0.24}" stroke-linecap="round"/>')

def v4_briefkaesten():
    """Briefkastenanlage: Flyer in jeden Briefkasten – außer bei 'Keine Werbung' (rot)."""
    g = ""
    x0, y0, bw, gap = 940, 440, 92, 8
    pw = 3 * bw + 4 * gap
    g += f'<rect x="{x0+pw/2-10}" y="{y0+2*bw+3*gap}" width="20" height="{850-(y0+2*bw+3*gap)}" fill="#8a8f96" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{x0}" y="{y0}" width="{pw}" height="{2*bw+3*gap}" rx="6" fill="#dfe4e8" stroke="{L}" stroke-width="4"/>'
    keine = {(0, 2), (1, 0)}
    for r in range(2):
        for c in range(3):
            bx, by = x0 + gap + c * (bw + gap), y0 + gap + r * (bw + gap)
            nein = (r, c) in keine
            g += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bw}" rx="5" fill="{"#fbd3d3" if nein else "#f7f8f9"}" stroke="{RED if nein else L}" stroke-width="{4.5 if nein else 3}"/>'
            g += f'<rect x="{bx+14}" y="{by+16}" width="{bw-28}" height="10" rx="2" fill="{L}"/>'
            if nein:
                # Aufkleber "Keine Werbung"
                g += f'<rect x="{bx+10}" y="{by+40}" width="{bw-20}" height="34" rx="4" fill="{RED}" stroke="{L}" stroke-width="2"/>'
                g += f'<text x="{bx+bw/2}" y="{by+54}" font-family="Arial" font-weight="bold" font-size="11.5" fill="#fff" text-anchor="middle">KEINE</text>'
                g += f'<text x="{bx+bw/2}" y="{by+68}" font-family="Arial" font-weight="bold" font-size="11.5" fill="#fff" text-anchor="middle">WERBUNG</text>'
                g += xmark(bx + bw - 6, by + 4, 17)
            else:
                g += f'<rect x="{bx+24}" y="{by+2}" width="{bw-48}" height="22" fill="#ffe27a" stroke="{L}" stroke-width="2.5" transform="rotate(-4 {bx+bw/2} {by+12})"/>'
                g += f'<rect x="{bx+30}" y="{by+50}" width="{bw-60}" height="14" fill="#fff" stroke="{L}" stroke-width="2"/>'
                g += check(bx + bw - 6, by + 4, 17)
    g += figure(CX, [SH_L, (CX - 100, 520), (CX - 210, 585)], [SH_R, (CX + 112, 520), (CX + 92, 600)], front_l=True)
    g += flyer(CX - 236, 572, -8, 40, 54)
    g += bubble(930, 320, 400, "Keine Werbung? Kein Einwurf.", 26)
    return g

VARIANTEN = [("1_Foto-Nachweis", v1_foto), ("2_Zuverlaessig", v2_daumen), ("3_Lastenrad", v3_rad), ("4_Jeder_Briefkasten", v4_briefkaesten)]

def scene_background():
    """Lüneburg-Silhouette + Original-Landschaft links, Fluss/Wiese rechts neu, ohne Briefkasten/Figur."""
    body = sb.STAEDTE["Lueneburg"]()
    river = (f'<polygon points="1000,617 1600,626 1600,743 1000,710" fill="#b8dbeb"/>'
             + "".join(f'<path d="M{x},{y} q8,-6 16,0 q8,6 16,0" fill="none" stroke="#3a6fb0" stroke-width="2.5"/>'
                       for x, y in ((1110, 660), (1330, 690), (1480, 700))))
    svg = svgwrap(sb.arcs() + body + f'<line x1="0" y1="{sb.GROUND}" x2="{W}" y2="{sb.GROUND}" stroke="{L}" stroke-width="2"/>'
                  + f'<rect x="0" y="590" width="{W}" height="{H-590}" fill="#fff"/>' + river, bg=True)
    bg = render(svg, os.path.join(OUT, "fig_bg.png")).convert("RGB")
    src = Image.open(os.path.join(sb.BASE, "Stadt_Allgemein.jpg")).convert("RGB")
    m = Image.new("L", (W, H), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(m)
    d.polygon([(0, 546), (487, 546), (487, 590), (1000, 590), (1000, H), (0, H)], fill=255)
    bg.paste(src, (0, 0), m)
    return bg

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    bg = scene_background()
    tiles = []
    for name, fn in VARIANTEN:
        fg = render(svgwrap(fn()), os.path.join(OUT, f"fig_{name}.png"))
        img = bg.copy().convert("RGBA")
        img.alpha_composite(fg)
        p = os.path.join(OUT, f"Figur_{name}.jpg")
        img.convert("RGB").save(p, quality=90)
        tiles.append(img.convert("RGB"))
        print(p)
    sheet = Image.new("RGB", (1600, 2 * 437 + 10), "white")
    for k, t in enumerate(tiles):
        sheet.paste(t.resize((800, 437)), ((k % 2) * 800, (k // 2) * 447))
    sheet.save(os.path.join(OUT, "Vorschau_Figuren.jpg"), quality=88)
