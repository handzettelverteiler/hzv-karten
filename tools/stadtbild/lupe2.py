"""Lupen-Variante (Seite 4): blaues Männchen hält die Lupe über einen 'Keine Werbung'-Briefkasten."""
import os
from PIL import Image
import figuren as f, strich as s, basecap2 as bc

L, RED = s.L, f.RED
BLUE, BLUE_D = s.FARBEN["Blau"]
CX = bc.CX

def lupe(cx, cy, r):
    g = f'<line x1="{cx+r*0.72}" y1="{cy+r*0.72}" x2="{cx+r*0.72+44}" y2="{cy+r*0.72+44}" stroke="{L}" stroke-width="22" stroke-linecap="round"/>'
    g += f'<line x1="{cx+r*0.72}" y1="{cy+r*0.72}" x2="{cx+r*0.72+44}" y2="{cy+r*0.72+44}" stroke="#3a3a3a" stroke-width="15" stroke-linecap="round"/>'
    g += f'<circle cx="{cx}" cy="{cy}" r="{r+11}" fill="#cfd4d9" stroke="{L}" stroke-width="4"/>'
    g += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fbd3d3" stroke="{L}" stroke-width="4"/>'
    g += f'<rect x="{cx-r*0.7}" y="{cy-r*0.62}" width="{r*1.4}" height="15" rx="4" fill="{L}"/>'
    g += f'<rect x="{cx-r*0.82}" y="{cy-r*0.22}" width="{r*1.64}" height="{r*0.78}" rx="8" fill="{RED}" stroke="{L}" stroke-width="3"/>'
    g += f'<text x="{cx}" y="{cy+r*0.12}" font-family="Arial" font-weight="bold" font-size="{r*0.25:.0f}" fill="#fff" text-anchor="middle">KEINE</text>'
    g += f'<text x="{cx}" y="{cy+r*0.44}" font-family="Arial" font-weight="bold" font-size="{r*0.25:.0f}" fill="#fff" text-anchor="middle">WERBUNG</text>'
    g += f'<path d="M{cx-r*0.55},{cy-r*0.85} Q{cx-r*0.88},{cy-r*0.6} {cx-r*0.9},{cy-r*0.22}" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".85"/>'
    return g

def scene_lupe():
    g = f.v4_briefkaesten()
    g = g[:g.index('<ellipse cx="1430" cy="852"')]
    cx, cy, r = 1194, 486, 74          # über dem Kasten oben rechts ("Keine Werbung")
    hx, hy = cx + r * 0.72 + 44, cy + r * 0.72 + 44
    fig = s.strich(CX, BLUE, BLUE_D, hand_to=(hx + 6, hy + 4), elbow=(1296, 516))
    i = fig.index(f'<path d="M{CX-30},246')
    fig = fig[:i] + fig[fig.index('/>', i) + 2:]
    g += fig + lupe(cx, cy, r)
    g += bc.hand_greift(hx + 8, hy + 2, -40, 0.8)
    g += bc.brauen(CX) + bc.cap_schraeg(CX)
    g += f.bubble(1180, 96, 300, "Wird respektiert!", 27)
    return g

if __name__ == "__main__":
    bg = f.scene_background()
    fg = f.render(f.svgwrap(scene_lupe()), os.path.join(f.OUT, "lupe2.png"))
    img = bg.convert("RGBA"); img.alpha_composite(fg); img = img.convert("RGB")
    img.save(os.path.join(f.OUT, "Basecap_B_Lupe.jpg"), quality=92)
    img.crop((820, 150, 1600, 873)).save("zl.png")
    print("ok")
