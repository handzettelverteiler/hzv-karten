"""Illustrationen für die Zusatzseiten der Auslagenverteilungs-Angebote (Stefan, 24.11.2026):
Strategie (Hotspot-Belegung), Posteraushang, Nachweise – im Stil der Stadtbilder (blaues Strichmännchen, Basecap).
Ortsunabhängig, für alle Auslage-Angebote nutzbar.
Aufruf: python3 auslage_seiten.py  -> staedte/auslage/Auslage_Strategie.jpg, Auslage_Poster.jpg, Auslage_Nachweis.jpg
"""
import os
from PIL import Image
import figuren as f, strich as s, basecap2 as bc
import stadtbild as sb

W, H = 1600, 873
L, RED = s.L, f.RED
BLUE, BLUE_D = s.FARBEN["Blau"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "staedte", "auslage")
GY = 770          # Gehweg-Kante (Fassaden stehen hier)
ST = f'stroke="{L}" stroke-width="4" stroke-linejoin="round"'


def txt(x, y, t, size=24, col=L, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="Arial" font-weight="bold" font-size="{size}" text-anchor="{anchor}" fill="{col}">{t}</text>'


def markise(x, y, w, c1=RED, c2="#ffffff", n=6):
    g = ""
    sw = w / n
    for i in range(n):
        g += f'<path d="M{x+i*sw},{y} L{x+(i+1)*sw},{y} L{x+(i+1)*sw+4},{y+44} L{x+i*sw+4},{y+44} Z" fill="{c1 if i % 2 == 0 else c2}" stroke="{L}" stroke-width="3"/>'
    for i in range(n):
        g += f'<path d="M{x+i*sw+4},{y+44} Q{x+i*sw+sw/2+4},{y+62} {x+(i+1)*sw+4},{y+44}" fill="{c1 if i % 2 == 0 else c2}" stroke="{L}" stroke-width="3"/>'
    return g


def laden(x, w, name, wall="#f3e3c3", c1=RED, top=330, schild="#ffffff", fenster=True, tuer="rechts"):
    """Ladenfassade mit Obergeschoss-Fenstern, Schild, Markise, Schaufenster und Tür."""
    g = f'<rect x="{x}" y="{top}" width="{w}" height="{GY-top}" fill="{wall}" {ST}/>'
    g += f'<rect x="{x-8}" y="{top-16}" width="{w+16}" height="18" fill="#d9cbb0" {ST}/>'
    if fenster:
        n = max(2, int(w // 90))
        fw = 46
        gap = (w - n * fw) / (n + 1)
        for i in range(n):
            fx = x + gap + i * (fw + gap)
            g += f'<rect x="{fx}" y="{top+30}" width="{fw}" height="62" fill="#cfe6f3" stroke="{L}" stroke-width="3"/>'
            g += f'<line x1="{fx+fw/2}" y1="{top+30}" x2="{fx+fw/2}" y2="{top+92}" stroke="{L}" stroke-width="2"/>'
    sy = top + 118
    g += f'<rect x="{x+16}" y="{sy}" width="{w-32}" height="44" rx="6" fill="{schild}" {ST}/>'
    g += txt(x + w / 2, sy + 31, name, 24)
    g += markise(x + 6, sy + 56, w - 12, c1)
    # Schaufenster + Tür
    ty = sy + 124
    dw = 64
    dx = x + w - dw - 18 if tuer == "rechts" else x + 18
    wx0 = x + 18 if tuer == "rechts" else x + dw + 34
    ww = w - dw - 52
    g += f'<rect x="{wx0}" y="{ty}" width="{ww}" height="{GY-ty-40}" fill="#dff1fb" {ST}/>'
    g += f'<path d="M{wx0+14},{ty+16} L{wx0+44},{ty+16} M{wx0+14},{ty+28} L{wx0+30},{ty+28}" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>'
    g += f'<rect x="{dx}" y="{ty}" width="{dw}" height="{GY-ty}" fill="#b97a42" {ST}/>'
    g += f'<rect x="{dx+12}" y="{ty+14}" width="{dw-24}" height="70" fill="#dff1fb" stroke="{L}" stroke-width="3"/>'
    g += f'<circle cx="{dx+dw-14}" cy="{ty+110}" r="5" fill="{L}"/>'
    return g


def boden():
    return (f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#ffffff"/>'
            f'<line x1="0" y1="{GY}" x2="{W}" y2="{GY}" stroke="{L}" stroke-width="3"/>'
            + "".join(f'<line x1="{x}" y1="{GY+40}" x2="{x+34}" y2="{GY+40}" stroke="{L}" stroke-width="3"/>' for x in range(30, 1000, 140)))


def pin(x, y, n=None, s=1.0):
    g = (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,0 C-26,-34 -26,-70 0,-74 C26,-70 26,-34 0,0 Z" fill="{RED}" stroke="{L}" stroke-width="3.5"/>'
         f'<circle cx="0" cy="-48" r="11" fill="#fff" stroke="{L}" stroke-width="3"/>')
    if n is not None:
        g += txt(0, -41, str(n), 18)
    return g + '</g>'


def figur(cx, hand_to, elbow, flyer=True, cap=True):
    fig = s.strich(cx, BLUE, BLUE_D, hand_to=hand_to, elbow=elbow)
    i = fig.index(f'<path d="M{cx-30},246')
    fig = fig[:i] + fig[fig.index('/>', i) + 2:]
    g = fig + bc.brauen(cx) + (bc.cap_schraeg(cx) if cap else "")
    return g


def render(body, name):
    os.makedirs(OUT, exist_ok=True)
    svg = f.svgwrap(sb.arcs() + body, bg=True)
    img = f.render(svg, os.path.join(OUT, "_tmp.png")).convert("RGB")
    p = os.path.join(OUT, name)
    img.save(p, quality=90)
    for t in ("_tmp.png", "_tmp.png.svg"):
        try:
            os.remove(os.path.join(OUT, t))
        except OSError:
            pass
    print(p)
    return p


# ---------------- 1) Strategie: viele Lokationen auf engem Raum ----------------
def strategie():
    g = laden(20, 220, "Café", "#f6e6c8", RED)
    g += laden(240, 200, "Bäckerei", "#fbe8d6", "#e8a33a", top=360)
    g += laden(440, 210, "Bar", "#e3e8ee", "#2f6dbf", top=320)
    g += laden(650, 210, "Apotheke", "#eef5ea", "#34a853", top=350)
    g += laden(860, 200, "Yoga", "#f4e9f3", "#9b59b6", top=340)
    g += boden()
    # Route der Verteiler (gestrichelt) + Pins über den Läden
    pts = [(130, 300), (340, 330), (545, 290), (755, 320), (960, 310)]
    d = "M" + " L".join(f"{x},{y-90}" for x, y in pts)
    g += f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="5" stroke-dasharray="14 12" stroke-linecap="round"/>'
    for k, (x, y) in enumerate(pts, 1):
        g += pin(x, y - 50, k, 0.95)
    g += f.check(1000, 236, 24)
    # Figur mit Flyerstapel
    cx = 1330
    g += figur(cx, (1228, 560), (1240, 500))
    g += bc.ihr_flyer(1204, 512, -6) + bc.ihr_flyer(1214, 518, 4) + bc.hand_greift(1232, 560, 0, 0.8)
    g += f.bubble(1060, 96, 500, "Viele Lokationen auf engem Raum!", 25)
    return render(g, "Auslage_Strategie.jpg")


# ---------------- 2) Posteraushang: Poster mit Tesafilm ins Schaufenster ----------------
def poster_motiv(x, y, w=150, h=210, rot=-2):
    g = f'<g transform="translate({x},{y}) rotate({rot})">'
    g += f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffe27a" stroke="{L}" stroke-width="4"/>'
    g += f'<rect x="0" y="0" width="{w}" height="34" fill="{RED}" stroke="{L}" stroke-width="3.5"/>'
    g += txt(w / 2, 92, "Ihr", 30) + txt(w / 2, 128, "Poster", 30)
    g += f'<line x1="22" y1="152" x2="{w-22}" y2="152" stroke="{L}" stroke-width="3"/>'
    g += f'<line x1="22" y1="168" x2="{w-44}" y2="168" stroke="{L}" stroke-width="3"/>'
    g += f'<line x1="22" y1="184" x2="{w-60}" y2="184" stroke="{L}" stroke-width="3"/>'
    # Tesafilm-Streifen an den Ecken
    for (tx, ty, a) in ((0, 0, -40), (w, 0, 40), (0, h, 40), (w, h, -40)):
        g += f'<rect x="{tx-20}" y="{ty-8}" width="40" height="16" fill="#eaf6ff" fill-opacity="0.85" stroke="#8fb3c9" stroke-width="2" transform="rotate({a} {tx} {ty})"/>'
    return g + '</g>'


def poster():
    g = laden(20, 250, "Bistro", "#f6e6c8", "#2f6dbf", top=340)
    g += laden(270, 230, "Buchladen", "#eef0e4", "#34a853", top=310)
    # großes Café-Schaufenster rechts, an dem der Verteiler das Poster anbringt
    x, w, top = 500, 640, 300
    g += f'<rect x="{x}" y="{top}" width="{w}" height="{GY-top}" fill="#f3e3c3" {ST}/>'
    g += f'<rect x="{x-8}" y="{top-16}" width="{w+16}" height="18" fill="#d9cbb0" {ST}/>'
    g += f'<rect x="{x+20}" y="{top+22}" width="{w-40}" height="48" rx="6" fill="#ffffff" {ST}/>' + txt(x + w / 2, top + 56, "Café am Markt", 28)
    g += markise(x + 6, top + 82, w - 12, RED, "#ffffff", 10)
    g += f'<rect x="{x+30}" y="{top+160}" width="{w-150}" height="{GY-top-200}" fill="#dff1fb" {ST}/>'
    g += f'<path d="M{x+50},{top+180} L{x+100},{top+180} M{x+50},{top+194} L{x+76},{top+194}" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'
    g += f'<rect x="{x+w-104}" y="{top+160}" width="74" height="{GY-top-160}" fill="#b97a42" {ST}/>'
    g += f'<rect x="{x+w-92}" y="{top+174}" width="50" height="70" fill="#dff1fb" stroke="{L}" stroke-width="3"/>'
    # bereits ausgelegte Flyer im Fenster (Ständer)
    g += f'<rect x="{x+60}" y="{GY-120}" width="80" height="80" fill="#e3b47c" {ST}/>'
    g += bc.ihr_flyer(x + 82, GY - 196, -4) + bc.ihr_flyer(x + 118, GY - 192, 5)
    g += boden()
    # Poster im Fenster
    g += poster_motiv(x + 340, top + 190, 150, 210, -2)
    g += f.check(x + 300, top + 200, 26)
    # Figur mit Tesafilm-Rolle, Hand am Poster
    cx = 1330
    g += figur(cx, (1012, 548), (1180, 590))
    g += f'<circle cx="1004" cy="540" r="22" fill="#eaf6ff" stroke="{L}" stroke-width="4"/><circle cx="1004" cy="540" r="10" fill="#fff" stroke="{L}" stroke-width="3"/>'
    g += f.bubble(1000, 96, 560, "Mit Erlaubnis – direkt angebracht!", 25)
    return render(g, "Auslage_Poster.jpg")


# ---------------- 3) Nachweise: Stempel & Visitenkarten auf dem Nachweisbogen ----------------
def nachweis():
    g = laden(20, 240, "Friseur", "#eef0e4", "#2f6dbf", top=330)
    g += laden(260, 230, "Kiosk", "#fbe8d6", "#e8a33a", top=360)
    g += laden(490, 240, "Galerie", "#e3e8ee", RED, top=320)
    g += boden()
    # Theke mit Stempel
    tx = 760
    g += f'<rect x="{tx}" y="600" width="300" height="{GY-600}" fill="#e3b47c" {ST}/>'
    g += f'<rect x="{tx+20}" y="626" width="120" height="{GY-646}" rx="6" fill="#f0cf9f" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{tx+160}" y="626" width="120" height="{GY-646}" rx="6" fill="#f0cf9f" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{tx-20}" y="578" width="340" height="26" rx="5" fill="#b97a42" {ST}/>'
    # Stempel + Stempelkissen
    g += f'<rect x="{tx+30}" y="560" width="80" height="20" rx="4" fill="#5b6770" {ST}/><rect x="{tx+38}" y="564" width="64" height="10" fill="{RED}"/>'
    g += f'<rect x="{tx+150}" y="548" width="46" height="18" fill="#7a4a2a" {ST}/><rect x="{tx+163}" y="500" width="20" height="48" fill="#b97a42" {ST}/><circle cx="{tx+173}" cy="494" r="16" fill="{RED}" {ST}/>'
    # Visitenkarte
    g += f'<rect x="{tx+222}" y="552" width="70" height="40" fill="#fff" stroke="{L}" stroke-width="3" transform="rotate(-8 {tx+257} 572)"/>'
    g += f'<line x1="{tx+232}" y1="566" x2="{tx+272}" y2="562" stroke="{L}" stroke-width="2.5"/><line x1="{tx+232}" y1="578" x2="{tx+262}" y2="574" stroke="{L}" stroke-width="2.5"/>'
    # Nachweisbogen (Klemmbrett) in der Hand der Figur
    bx, by = 1080, 440
    g += f'<g transform="rotate(-6 {bx+70} {by+90})">'
    g += f'<rect x="{bx}" y="{by}" width="150" height="190" rx="8" fill="#b97a42" {ST}/>'
    g += f'<rect x="{bx+12}" y="{by+16}" width="126" height="164" fill="#fff" stroke="{L}" stroke-width="3"/>'
    g += f'<rect x="{bx+50}" y="{by-8}" width="50" height="22" rx="4" fill="#9aa4ad" stroke="{L}" stroke-width="3"/>'
    for r in range(3):
        for c in range(2):
            gx, gy = bx + 20 + c * 60, by + 26 + r * 50
            g += f'<rect x="{gx}" y="{gy}" width="54" height="44" fill="none" stroke="#bbb" stroke-width="2"/>'
    stamps = [(bx + 47, by + 48, RED), (bx + 107, by + 48, "#2f6dbf"), (bx + 47, by + 98, "#34a853"), (bx + 107, by + 98, RED), (bx + 47, by + 148, "#2f6dbf")]
    for (sx, sy, col) in stamps:
        g += f'<ellipse cx="{sx}" cy="{sy}" rx="20" ry="13" fill="none" stroke="{col}" stroke-width="3" transform="rotate(-12 {sx} {sy})"/>'
        g += f'<line x1="{sx-11}" y1="{sy}" x2="{sx+11}" y2="{sy-3}" stroke="{col}" stroke-width="2.5"/>'
    g += '</g>'
    g += f.check(1240, 450, 26)
    cx = 1330
    g += figur(cx, (1214, 560), (1250, 520))
    g += bc.hand_greift(1216, 560, 0, 0.8)
    g += f.bubble(1000, 96, 560, "Gestempelt &amp; dokumentiert!", 25)
    return render(g, "Auslage_Nachweis.jpg")


if __name__ == "__main__":
    strategie()
    poster()
    nachweis()
