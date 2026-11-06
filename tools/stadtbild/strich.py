"""Strichmännchen im Stil des HZV-Briefkopfs/Footers in der Szene 'Keine Werbung? Kein Einwurf.'"""
import os
from PIL import Image, ImageDraw, ImageFont
import figuren as f

L = "#262626"
HAIR, HAIR_D = "#ffd92e", "#e3b400"
FARBEN = {
    "Blau": ("#2079c7", "#165c9c"),
    "Gruen": ("#8cc63f", "#6c9f2a"),
    "Gelb": ("#ffcc00", "#c9a000"),
    "Rot": ("#ef2b2b", "#bb1d1d"),
}
CX = 1440

def strich(cx, col, dark, hand_to=(1220, 576), walk=False, elbow=None):
    g = f'<ellipse cx="{cx}" cy="850" rx="95" ry="10" fill="#ececec"/>'
    sw = 5
    # Beine (Strich) + Füße
    if walk:
        g += f'<path d="M{cx-26},640 L{cx-70},760 L{cx-96},820 M{cx-96},820 L{cx-128},810" fill="none" stroke="{L}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
        g += f'<path d="M{cx+26},640 L{cx+34},835 M{cx+34},835 L{cx+72},835" fill="none" stroke="{L}" stroke-width="{sw}" stroke-linecap="round"/>'
    else:
        g += f'<path d="M{cx-28},640 L{cx-32},836 L{cx-70},836 M{cx+28},640 L{cx+32},836 L{cx+70},836" fill="none" stroke="{L}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    # Hemd (Trapez) + Shorts
    g += f'<path d="M{cx-44},398 L{cx+44},398 L{cx+70},560 L{cx-70},560 Z" fill="{col}" stroke="{L}" stroke-width="3"/>'
    g += f'<path d="M{cx-44},398 L{cx-72},440 L{cx-56},452 L{cx-40},420 Z" fill="{col}" stroke="{L}" stroke-width="3"/>'
    g += f'<path d="M{cx+44},398 L{cx+72},440 L{cx+56},452 L{cx+40},420 Z" fill="{col}" stroke="{L}" stroke-width="3"/>'
    g += f'<path d="M{cx-60},560 L{cx+60},560 L{cx+62},648 L{cx+6},648 L{cx},600 L{cx-6},648 L{cx-62},648 Z" fill="{col}" stroke="{L}" stroke-width="3"/>'
    g += f'<path d="M{cx-60},560 L{cx+60},560" stroke="{dark}" stroke-width="5"/>'
    # roter Punkt / rote Hand auf der Brust
    g += f'<circle cx="{cx-18}" cy="450" r="17" fill="#fff" stroke="{L}" stroke-width="2.5"/>' + f.red_hand(cx - 18, 450, 0.62)
    # Tasche (dunklere Farbe) + Gurt
    g += f'<path d="M{cx+58},440 L{cx+96},520 L{cx+120},560" fill="none" stroke="{L}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    g += f'<path d="M{cx-38},400 L{cx+86},530" stroke="{dark}" stroke-width="9" stroke-linecap="round"/>'
    g += f'<rect x="{cx+50}" y="516" width="86" height="100" rx="12" fill="{dark}" stroke="{L}" stroke-width="3"/>'
    g += f'<path d="M{cx+50},540 Q{cx+93},560 {cx+136},540" fill="none" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{cx+64}" y="494" width="44" height="30" fill="#ffe27a" stroke="{L}" stroke-width="2.5" transform="rotate(-8 {cx+84} 513)"/>'
    # Arme (Strich)
    hx, hy = hand_to
    g += f'<path d="M{cx-58},440 L{(elbow or (cx-112,590))[0]},{(elbow or (cx-112,590))[1]} L{hx},{hy}" fill="none" stroke="{L}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    # Hals + Kopf
    g += f'<line x1="{cx}" y1="352" x2="{cx}" y2="400" stroke="{L}" stroke-width="{sw}"/>'
    g += f'<circle cx="{cx}" cy="300" r="60" fill="#fff" stroke="{L}" stroke-width="4"/>'
    # Haare: Topfschnitt mit Pony
    g += (f'<path d="M{cx-60},298 Q{cx-66},236 {cx-4},230 Q{cx+60},228 {cx+62},292 '
          f'L{cx+48},270 L{cx+40},286 L{cx+30},266 L{cx+18},284 L{cx+6},264 L{cx-8},282 L{cx-20},262 L{cx-32},280 L{cx-44},262 L{cx-52},286 Z" '
          f'fill="{HAIR}" stroke="{L}" stroke-width="3.5" stroke-linejoin="round"/>')
    g += f'<path d="M{cx-30},246 Q{cx-6},236 {cx+22},244" fill="none" stroke="{HAIR_D}" stroke-width="3"/>'
    # Gesicht: Kulleraugen mit Lichtpunkt, kleines Lächeln
    for ex in (cx - 16, cx + 18):
        g += f'<ellipse cx="{ex}" cy="304" rx="7" ry="9" fill="{L}"/><circle cx="{ex+2}" cy="300" r="2.5" fill="#fff"/>'
    g += f'<path d="M{cx-18},328 Q{cx+2},346 {cx+22},326" fill="none" stroke="{L}" stroke-width="4" stroke-linecap="round"/>'
    return g

def scene(farbe):
    col, dark = FARBEN[farbe]
    g = f.v4_briefkaesten()
    g = g[:g.index('<ellipse cx="1430" cy="852"')]
    g += strich(CX, col, dark)
    g += f.flyer(1206, 562, -8, 40, 54)
    g += f.bubble(930, 320, 400, "Keine Werbung? Kein Einwurf.", 26)
    return g

if __name__ == "__main__":
    bg = f.scene_background()
    tiles = []
    for farbe in FARBEN:
        fg = f.render(f.svgwrap(scene(farbe)), os.path.join(f.OUT, f"s_{farbe}.png"))
        img = bg.convert("RGBA"); img.alpha_composite(fg); img = img.convert("RGB")
        img.save(os.path.join(f.OUT, f"Strichmann_{farbe}.jpg"), quality=92)
        tiles.append((farbe.replace("ue", "ü"), img.crop((860, 160, 1600, 873))))
    tw, th = 740, 713
    sheet = Image.new("RGB", (2 * tw + 10, 2 * (th + 50) + 10), "white")
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    for k, (n, t) in enumerate(tiles):
        x, y = (k % 2) * (tw + 10), (k // 2) * (th + 60)
        d.text((x + 10, y + 8), n, fill="#c81e1e", font=font)
        sheet.paste(t, (x, y + 50))
    sheet.save(os.path.join(f.OUT, "Vorschau_Strichmann.jpg"), quality=88)
    print("ok")
