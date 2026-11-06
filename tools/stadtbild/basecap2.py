"""Blaues Strichmännchen: Basecap erwachsener getragen + Einwurf 'Ihr Flyer'."""
import os
from PIL import Image, ImageDraw, ImageFont
import figuren as f, strich as s

L, RED = s.L, f.RED
BLUE, BLUE_D = s.FARBEN["Blau"]
CX = 1330

def brauen(cx):
    return (f'<path d="M{cx-25},290 Q{cx-16},285 {cx-7},290" fill="none" stroke="{L}" stroke-width="3.5" stroke-linecap="round"/>'
            f'<path d="M{cx+10},290 Q{cx+19},285 {cx+28},290" fill="none" stroke="{L}" stroke-width="3.5" stroke-linecap="round"/>')

def cap_frontal(cx):
    return (f'<path d="M{cx-62},266 Q{cx-60},206 {cx},202 Q{cx+60},206 {cx+62},266 Z" fill="{BLUE}" stroke="{L}" stroke-width="4"/>'
            f'<path d="M{cx},204 L{cx},264" stroke="{BLUE_D}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="202" r="5" fill="{BLUE_D}" stroke="{L}" stroke-width="3"/>'
            f'<path d="M{cx-70},266 Q{cx},252 {cx+70},266 Q{cx+60},284 {cx},286 Q{cx-60},284 {cx-70},266 Z" fill="{BLUE_D}" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>'
            + f.red_hand(cx, 236, 0.85))

def cap_schraeg(cx):
    return (f'<path d="M{cx-62},268 Q{cx-58},206 {cx+4},202 Q{cx+64},208 {cx+62},266 Z" fill="{BLUE}" stroke="{L}" stroke-width="4"/>'
            f'<path d="M{cx+6},204 L{cx+12},264" stroke="{BLUE_D}" stroke-width="3"/>'
            f'<circle cx="{cx+4}" cy="202" r="5" fill="{BLUE_D}" stroke="{L}" stroke-width="3"/>'
            f'<path d="M{cx-64},268 Q{cx-30},254 {cx+30},262 Q{cx+8},284 {cx-40},288 Q{cx-80},286 {cx-92},278 Q{cx-84},270 {cx-64},268 Z" fill="{BLUE_D}" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>'
            + f.red_hand(cx + 22, 236, 0.85))

def cap_struktur(cx):
    return (f'<path d="M{cx-60},266 L{cx-56},214 Q{cx},192 {cx+56},214 L{cx+60},266 Z" fill="{BLUE}" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="{cx-62}" y="252" width="124" height="14" fill="#fff" stroke="{L}" stroke-width="3"/>'
            f'<line x1="{cx-62}" y1="259" x2="{cx+62}" y2="259" stroke="{RED}" stroke-width="5"/>'
            f'<path d="M{cx-64},266 Q{cx},256 {cx+64},266 Q{cx+50},282 {cx},284 Q{cx-50},282 {cx-64},266 Z" fill="{BLUE_D}" stroke="{L}" stroke-width="4" stroke-linejoin="round"/>'
            + f.red_hand(cx, 228, 0.85))

CAPS = [("B_Leicht_schraeg", cap_schraeg)]
_ALT = [("A_Frontal", cap_frontal), ("B_Leicht_schraeg", cap_schraeg), ("C_Strukturiert", cap_struktur)]

def hand_greift(x, y, rot=0, s=1.0):
    """Cartoon-Hand, greift von rechts um die Flyerkante (Finger vorne auf dem Flyer)."""
    st = f'stroke="{L}" stroke-width="3.2" stroke-linejoin="round"'
    g = f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
    g += f'<path d="M-2,-16 Q16,-20 20,-4 Q22,14 6,20 Q-6,22 -8,10 Z" fill="#fff" {st}/>'   # Handballen
    for i, dy in enumerate((-12, -2, 8)):
        g += f'<rect x="-24" y="{dy}" width="26" height="10" rx="5" fill="#fff" {st}/>'       # Finger
    g += f'<rect x="-6" y="-30" width="10" height="22" rx="5" fill="#fff" {st} transform="rotate(-28 -1 -19)"/>'  # Daumen
    return g + '</g>'

def hand_haengt(x, y, s=1.0):
    st = f'stroke="{L}" stroke-width="3.2" stroke-linejoin="round"'
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-10,-6 Q-12,14 0,18 Q12,16 11,-4 Q2,-12 -10,-6 Z" fill="#fff" {st}/>'
            f'<path d="M-9,4 Q-16,8 -13,14" fill="none" {st}/></g>')

def ihr_flyer(x, y, rot=-6):
    w, h = 58, 78
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="{-w/2}" y="0" width="{w}" height="{h}" fill="#ffe27a" stroke="{L}" stroke-width="3.5"/>'
            f'<rect x="{-w/2}" y="0" width="{w}" height="14" fill="{RED}" stroke="{L}" stroke-width="3"/>'
            f'<text x="0" y="38" font-family="Arial" font-weight="bold" font-size="17" text-anchor="middle" fill="{L}">Ihr</text>'
            f'<text x="0" y="58" font-family="Arial" font-weight="bold" font-size="17" text-anchor="middle" fill="{L}">Flyer</text>'
            f'<line x1="{-w/2+10}" y1="68" x2="{w/2-10}" y2="68" stroke="{L}" stroke-width="2"/></g>')

def scene(capfn):
    g = f.v4_briefkaesten()
    g = g[:g.index('<ellipse cx="1430" cy="852"')]
    import re
    g = re.sub(r'<circle cx="1234" cy="552"[^>]*/><path[^>]*/>', '', g)
    # Kasten unten rechts leeren (Flyer + Haken entfernen): neu übermalen
    bx, by = 940 + 8 + 2 * 100, 440 + 8 + 100
    g += f'<rect x="{bx}" y="{by}" width="92" height="92" rx="5" fill="#f7f8f9" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{bx+14}" y="{by+16}" width="64" height="10" rx="2" fill="{L}"/>'
    g += f'<rect x="{bx+30}" y="{by+50}" width="32" height="14" fill="#fff" stroke="{L}" stroke-width="2"/>'
    fig = s.strich(CX, BLUE, BLUE_D, hand_to=(1232, 606), elbow=(1252, 530))
    i = fig.index(f'<path d="M{CX-30},246')
    fig = fig[:i] + fig[fig.index('/>', i) + 2:]
    g += ihr_flyer(1194, 566, 0)                 # steckt im Schlitz
    g += fig
    g += hand_greift(1236, 606, 0, 0.8)
    g += brauen(CX) + capfn(CX)
    g += f.bubble(1150, 96, 400, "Keine Werbung? Kein Einwurf.", 25)
    return g

if __name__ == "__main__":
    bg = f.scene_background()
    tiles = []
    for name, fn in CAPS:
        fg = f.render(f.svgwrap(scene(fn)), os.path.join(f.OUT, f"bc_{name}.png"))
        img = bg.convert("RGBA"); img.alpha_composite(fg); img = img.convert("RGB")
        img.save(os.path.join(f.OUT, f"Basecap_{name}.jpg"), quality=92)
        tiles.append((name.replace("_", " ").replace("ae", "ä"), img.crop((900, 150, 1600, 873))))
    TW, TH = 700, 723
    sheet = Image.new("RGB", (3 * TW + 20, TH + 60), "white")
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    for k, (n, t) in enumerate(tiles):
        x = k * (TW + 10)
        d.text((x + 10, 10), n, fill="#c81e1e", font=font)
        sheet.paste(t, (x, 55))
    sheet.save(os.path.join(f.OUT, "Vorschau_Basecap.jpg"), quality=88)
    print("ok")
