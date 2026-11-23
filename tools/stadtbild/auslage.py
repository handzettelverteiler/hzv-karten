"""Stadtbild-Variante für Auslagenverteilung: Figur legt Flyer auf einer Ladentheke aus (statt Briefkastenanlage).
Aufruf: python3 auslage.py <Slug>  -> out/final/Stadt_<Slug>_Auslage.jpg"""
import os, sys, re
from PIL import ImageDraw
import figuren as f, strich as s, basecap2 as bc, final as fn

L, RED = s.L, f.RED
BLUE, BLUE_D = s.FARBEN["Blau"]
CX = bc.CX
WOOD, WOOD_D, PANEL = "#e3b47c", "#b97a42", "#f0cf9f"

def base(src):
    im = fn.clean_base(src)
    d = ImageDraw.Draw(im)
    d.rectangle([930, 425, 1060, 866], fill="white")
    d.rectangle([1150, 80, 1600, 190], fill="white")
    def top(x): return 618 + (x - 1040) * 0.0145
    def bot(x): return 713 + (x - 1040) * 0.0545
    d.polygon([(930, top(930)), (1060, top(1060)), (1060, bot(1060)), (930, bot(930))], fill=(184, 219, 235))
    return im

def theke():
    st = f'stroke="{L}" stroke-width="4" stroke-linejoin="round"'
    g = f'<path d="M987,418 L979,600 L1028,600 L1019,418" fill="#dddcd8" stroke="{L}" stroke-width="3.5"/>'           # Fernsehturm-Schaft hinter der Theke
    g += f'<rect x="925" y="618" width="300" height="232" fill="{WOOD}" {st}/>'
    for x in (945, 1080):
        g += f'<rect x="{x}" y="645" width="120" height="180" rx="6" fill="{PANEL}" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="905" y="596" width="340" height="26" rx="5" fill="{WOOD_D}" {st}/>'   # Thekenplatte
    # Kasse
    g += f'<path d="M940,596 L948,540 L1010,540 L1018,596 Z" fill="#cfd6dd" {st}/>'
    g += f'<rect x="952" y="518" width="54" height="26" rx="4" fill="#5b6770" {st}/>'
    g += f'<rect x="958" y="524" width="42" height="12" fill="#9fe0a8"/>'
    # Kaffeetasse
    g += f'<path d="M1030,566 L1034,596 L1062,596 L1066,566 Z" fill="#fff" {st}/>'
    g += f'<path d="M1066,572 Q1080,578 1066,590" fill="none" stroke="{L}" stroke-width="4"/>'
    for x in (1040, 1054):
        g += f'<path d="M{x},556 Q{x+6},546 {x},536" fill="none" stroke="#999" stroke-width="3" stroke-linecap="round"/>'
    # vorhandene Prospektauslage (Acrylhalter) mit Ihren Flyern
    g += f'<rect x="1084" y="560" width="92" height="36" rx="3" fill="#dff1fb" {st}/>'
    g += bc.ihr_flyer(1112, 486, -5) + bc.ihr_flyer(1146, 490, 5)
    g += f'<rect x="1084" y="574" width="92" height="22" rx="3" fill="#dff1fb" fill-opacity="0.8" {st}/>'
    g += f.check(1180, 478, 24)
    return g

def scene():
    g = theke()
    fig = s.strich(CX, BLUE, BLUE_D, hand_to=(1232, 606), elbow=(1252, 530))
    i = fig.index(f'<path d="M{CX-30},246')
    fig = fig[:i] + fig[fig.index('/>', i) + 2:]
    g += bc.ihr_flyer(1206, 548, 8)
    g += fig + bc.hand_greift(1236, 606, 0, 0.8) + bc.brauen(CX) + bc.cap_schraeg(CX)
    g += f.bubble(1060, 96, 500, "Ausgelegt – zur freien Mitnahme!", 25)
    return g

if __name__ == "__main__":
    os.makedirs(fn.OUT, exist_ok=True)
    for slug in sys.argv[1:]:
        src = os.path.join("/home/claude/hzv-karten/staedte", f"Stadt_{slug}.jpg")
        fn.compose(base(src), scene(), f"Stadt_{slug}_Auslage.jpg"); print(slug)
