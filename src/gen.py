"""IEC sticker set: ~100 original stickers drawn as SVG in the club palette.

Every sticker is a simple white-bordered shape (circle, rounded rectangle, pill, hexagon, ...), so it can be cut
by hand with scissors. Writes stickers.json: [{id, cat, name, w, h, mm, svg}], where w/h is the viewBox and mm
the default printed width.
"""
import json
import math
import sys
from html import escape

NAVY, NAVY9, NAVY4, SKY = "#154a7f", "#0f2f52", "#6b90bc", "#dbe7f4"
HONEY, HONEYL, SAGE, SAGEL = "#d4962a", "#f6dfae", "#4f8f6e", "#d3e8db"
INK, PAPER, BRICK, CREAM, PEACH, W = "#1c2633", "#f4f7fb", "#c4583e", "#fff6e3", "#f4b183", "#ffffff"
CUT = "#c3cedb"
F, M, G = "Fredoka, Nunito, sans-serif", "'IBM Plex Mono', monospace", "'Space Grotesk', sans-serif"

S = []


def add(sid, cat, name, w, h, mm, body):
    S.append({"id": sid, "cat": cat, "name": name, "w": w, "h": h, "mm": mm,
              "svg": f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'})


def t(x, y, s, size, fill=INK, font=F, weight=600, anchor="middle", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{escape(s)}</text>')


# ---------------------------------------------------------------- cut shapes (white border + inner panel)

def circle(c, r, fill, ring=None):
    out = f'<circle cx="{c}" cy="{c}" r="{r}" fill="{W}" stroke="{CUT}" stroke-width="1.4"/>'
    out += f'<circle cx="{c}" cy="{c}" r="{r - 10}" fill="{fill}"/>'
    if ring:
        out += f'<circle cx="{c}" cy="{c}" r="{r - 17}" fill="none" stroke="{ring}" stroke-width="2.5" stroke-dasharray="1 6" stroke-linecap="round"/>'
    return out


def rrect(w, h, rad, fill, inset=10, stroke=None):
    out = f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rad}" fill="{W}" stroke="{CUT}" stroke-width="1.4"/>'
    out += f'<rect x="{inset}" y="{inset}" width="{w - 2 * inset}" height="{h - 2 * inset}" rx="{max(rad - inset + 2, 2)}" fill="{fill}"'
    out += (f' stroke="{stroke}" stroke-width="3"/>' if stroke else "/>")
    return out


def hexagon(c, r, fill):
    def pts(rr):
        return " ".join(f"{c + rr * math.cos(math.radians(60 * i - 90)):.1f},{c + rr * math.sin(math.radians(60 * i - 90)):.1f}"
                        for i in range(6))
    return (f'<polygon points="{pts(r)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<polygon points="{pts(r - 11)}" fill="{fill}" stroke-linejoin="round"/>')


def burst(c, r, n, fill):
    def pts(r1, r2):
        return " ".join(f"{c + (r1 if i % 2 == 0 else r2) * math.cos(math.pi * i / n):.1f},"
                        f"{c + (r1 if i % 2 == 0 else r2) * math.sin(math.pi * i / n):.1f}" for i in range(2 * n))
    return (f'<polygon points="{pts(r, r - 9)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<polygon points="{pts(r - 10, r - 19)}" fill="{fill}" stroke-linejoin="round"/>')


def shield(w, h, fill):
    def p(i):
        return (f"M{w / 2} {i} L{w - i} {i + 14} L{w - i} {h * 0.5} Q{w - i} {h * 0.82} {w / 2} {h - i} "
                f"Q{i} {h * 0.82} {i} {h * 0.5} L{i} {i + 14} Z")
    return (f'<path d="{p(2)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{p(12)}" fill="{fill}"/>')


def bubble(w, h, fill, tail_x=None):
    tx = tail_x or w * 0.28

    def p(i, r):
        b = h - 34
        return (f"M{i + r} {i} H{w - i - r} Q{w - i} {i} {w - i} {i + r} V{b - r} Q{w - i} {b} {w - i - r} {b} "
                f"H{tx + 22} L{tx - 6} {h - i - 4} L{tx + 2} {b} H{i + r} Q{i} {b} {i} {b - r} V{i + r} Q{i} {i} {i + r} {i} Z")
    return (f'<path d="{p(2, 26)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{p(11, 18)}" fill="{fill}" stroke-linejoin="round"/>')


def tag(w, h, fill):
    def p(i):
        return f"M{h / 2 + i * 0.4} {i} H{w - i - 14} Q{w - i} {i} {w - i} {i + 14} V{h - i - 14} Q{w - i} {h - i} {w - i - 14} {h - i} H{h / 2 + i * 0.4} L{i} {h / 2} Z"
    return (f'<path d="{p(2)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{p(11)}" fill="{fill}" stroke-linejoin="round"/>'
            f'<circle cx="{h / 2 + 4}" cy="{h / 2}" r="7" fill="{W}"/>')


def ticket(w, h, fill):
    def p(i, notch):
        return (f"M{i} {i} H{w - i} V{h / 2 - notch} A{notch} {notch} 0 0 0 {w - i} {h / 2 + notch} V{h - i} H{i} "
                f"V{h / 2 + notch} A{notch} {notch} 0 0 0 {i} {h / 2 - notch} Z")
    return (f'<path d="{p(2, 16)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="{p(11, 9)}" fill="{fill}"/>')


# ---------------------------------------------------------------- drawing parts

def gear(cx, cy, ro, ri, teeth, fill, hole=None, hole_fill=None, rot=0):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4) + rot
        r = ro if i % 4 in (1, 2) else ri
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    out = f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke-linejoin="round"/>'
    if hole:
        out += f'<circle cx="{cx}" cy="{cy}" r="{hole}" fill="{hole_fill or W}"/>'
    return out


def face(cx, cy, s, kind="happy", ink=INK):
    ex, ey, er = s * 0.3, cy - s * 0.08, s * 0.085
    o = ""
    if kind in ("happy", "wave", "love_text", "coffee", "proud"):
        o += f'<circle cx="{cx - ex}" cy="{ey}" r="{er}" fill="{ink}"/><circle cx="{cx + ex}" cy="{ey}" r="{er}" fill="{ink}"/>'
        o += f'<circle cx="{cx - ex + er * 0.35}" cy="{ey - er * 0.35}" r="{er * 0.32}" fill="{W}"/><circle cx="{cx + ex + er * 0.35}" cy="{ey - er * 0.35}" r="{er * 0.32}" fill="{W}"/>'
    if kind == "sleepy":
        o += (f'<path d="M{cx - ex - er} {ey} q{er} {er * 0.9} {er * 2} 0 M{cx + ex - er} {ey} q{er} {er * 0.9} {er * 2} 0" '
              f'fill="none" stroke="{ink}" stroke-width="{s * 0.045}" stroke-linecap="round"/>')
    if kind == "wink":
        o += f'<circle cx="{cx - ex}" cy="{ey}" r="{er}" fill="{ink}"/>'
        o += f'<path d="M{cx + ex - er} {ey} q{er} -{er} {er * 2} 0" fill="none" stroke="{ink}" stroke-width="{s * 0.045}" stroke-linecap="round"/>'
    if kind == "cool":
        o += (f'<rect x="{cx - ex - er * 2}" y="{ey - er * 1.3}" width="{er * 4}" height="{er * 2.4}" rx="{er}" fill="{ink}"/>'
              f'<rect x="{cx + ex - er * 2}" y="{ey - er * 1.3}" width="{er * 4}" height="{er * 2.4}" rx="{er}" fill="{ink}"/>'
              f'<path d="M{cx - ex + er * 2} {ey - er * 0.4} H{cx + ex - er * 2}" stroke="{ink}" stroke-width="{s * 0.035}"/>')
    if kind == "love":
        for dx in (-ex, ex):
            x0, y0, k = cx + dx, ey, er * 1.25
            o += (f'<path d="M{x0} {y0 + k} C{x0 - k * 1.8} {y0 - k * 0.2} {x0 - k * 0.8} {y0 - k * 1.6} {x0} {y0 - k * 0.5} '
                  f'C{x0 + k * 0.8} {y0 - k * 1.6} {x0 + k * 1.8} {y0 - k * 0.2} {x0} {y0 + k} Z" fill="{BRICK}"/>')
    if kind in ("shock", "confused"):
        o += f'<circle cx="{cx - ex}" cy="{ey}" r="{er * 1.15}" fill="{W}" stroke="{ink}" stroke-width="{s * 0.03}"/><circle cx="{cx - ex}" cy="{ey}" r="{er * 0.5}" fill="{ink}"/>'
        o += f'<circle cx="{cx + ex}" cy="{ey}" r="{er * (0.8 if kind == "confused" else 1.15)}" fill="{W}" stroke="{ink}" stroke-width="{s * 0.03}"/><circle cx="{cx + ex}" cy="{ey}" r="{er * 0.45}" fill="{ink}"/>'
    if kind == "tired":
        o += (f'<path d="M{cx - ex - er} {ey - er * 0.3} h{er * 2} M{cx + ex - er} {ey - er * 0.3} h{er * 2}" stroke="{ink}" '
              f'stroke-width="{s * 0.045}" stroke-linecap="round"/>'
              f'<path d="M{cx - ex - er} {ey + er * 0.6} q{er} {er * 0.6} {er * 2} 0 M{cx + ex - er} {ey + er * 0.6} q{er} {er * 0.6} {er * 2} 0" '
              f'fill="none" stroke="{NAVY4}" stroke-width="{s * 0.025}" stroke-linecap="round"/>')
    my = cy + s * 0.16
    if kind in ("happy", "wave", "wink", "cool", "love", "love_text", "coffee", "proud"):
        o += (f'<path d="M{cx - s * 0.16} {my - s * 0.03} Q{cx} {my + s * 0.16} {cx + s * 0.16} {my - s * 0.03}" fill="none" '
              f'stroke="{ink}" stroke-width="{s * 0.05}" stroke-linecap="round"/>')
    elif kind == "sleepy":
        o += f'<ellipse cx="{cx}" cy="{my + s * 0.02}" rx="{s * 0.06}" ry="{s * 0.045}" fill="{ink}"/>'
    elif kind == "shock":
        o += f'<ellipse cx="{cx}" cy="{my + s * 0.03}" rx="{s * 0.075}" ry="{s * 0.095}" fill="{ink}"/>'
    elif kind == "confused":
        o += (f'<path d="M{cx - s * 0.13} {my + s * 0.04} q{s * 0.065} -{s * 0.07} {s * 0.13} 0 t{s * 0.13} 0" fill="none" '
              f'stroke="{ink}" stroke-width="{s * 0.045}" stroke-linecap="round"/>')
    elif kind == "tired":
        o += f'<path d="M{cx - s * 0.12} {my + s * 0.05} H{cx + s * 0.12}" stroke="{ink}" stroke-width="{s * 0.045}" stroke-linecap="round"/>'
    if kind not in ("cool", "tired"):
        o += (f'<ellipse cx="{cx - ex - er * 0.6}" cy="{my}" rx="{s * 0.075}" ry="{s * 0.045}" fill="{PEACH}" opacity="0.85"/>'
              f'<ellipse cx="{cx + ex + er * 0.6}" cy="{my}" rx="{s * 0.075}" ry="{s * 0.045}" fill="{PEACH}" opacity="0.85"/>')
    return o


def bolt(x, y, s, fill=HONEY):
    return (f'<path d="M{x + s * 0.55} {y} L{x} {y + s * 0.58} H{x + s * 0.42} L{x + s * 0.3} {y + s} L{x + s * 0.95} '
            f'{y + s * 0.38} H{x + s * 0.52} Z" fill="{fill}" stroke-linejoin="round"/>')


def resistor(cx, cy, s, bands=(BRICK, INK, HONEY)):
    w, h = s, s * 0.42
    o = f'<path d="M{cx - s * 0.95} {cy} H{cx + s * 0.95}" stroke="{NAVY4}" stroke-width="{s * 0.07}" stroke-linecap="round"/>'
    o += f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h * 0.45}" fill="{HONEYL}" stroke="{INK}" stroke-width="{s * 0.035}"/>'
    for i, b in enumerate(bands):
        o += f'<rect x="{cx - w * 0.3 + i * w * 0.2}" y="{cy - h / 2 + 1}" width="{w * 0.09}" height="{h - 2}" fill="{b}"/>'
    return o


def chip(cx, cy, s, fill=NAVY9):
    o = ""
    for i in range(4):
        d = -s * 0.3 + i * s * 0.2
        o += (f'<rect x="{cx + d - s * 0.04}" y="{cy - s * 0.62}" width="{s * 0.08}" height="{s * 1.24}" rx="{s * 0.03}" fill="{NAVY4}"/>'
              f'<rect x="{cx - s * 0.62}" y="{cy + d - s * 0.04}" width="{s * 1.24}" height="{s * 0.08}" rx="{s * 0.03}" fill="{NAVY4}"/>')
    o += f'<rect x="{cx - s * 0.45}" y="{cy - s * 0.45}" width="{s * 0.9}" height="{s * 0.9}" rx="{s * 0.12}" fill="{fill}"/>'
    return o


def bulb(cx, cy, s, fill=HONEY):
    return (f'<circle cx="{cx}" cy="{cy}" r="{s * 0.5}" fill="{fill}"/>'
            f'<rect x="{cx - s * 0.22}" y="{cy + s * 0.38}" width="{s * 0.44}" height="{s * 0.3}" rx="{s * 0.06}" fill="{NAVY4}"/>'
            f'<path d="M{cx - s * 0.22} {cy + s * 0.5} H{cx + s * 0.22} M{cx - s * 0.22} {cy + s * 0.6} H{cx + s * 0.22}" stroke="{W}" stroke-width="{s * 0.03}"/>')


def cup(cx, cy, s, fill=W, drink=HONEY):
    return (f'<path d="M{cx - s * 0.42} {cy - s * 0.3} H{cx + s * 0.42} L{cx + s * 0.34} {cy + s * 0.42} Q{cx + s * 0.32} {cy + s * 0.52} {cx + s * 0.22} {cy + s * 0.52} '
            f'H{cx - s * 0.22} Q{cx - s * 0.32} {cy + s * 0.52} {cx - s * 0.34} {cy + s * 0.42} Z" fill="{fill}" stroke="{INK}" stroke-width="{s * 0.06}" stroke-linejoin="round"/>'
            f'<path d="M{cx + s * 0.4} {cy - s * 0.12} q{s * 0.32} 0 {s * 0.28} {s * 0.24} q-{s * 0.04} {s * 0.2} -{s * 0.33} {s * 0.18}" fill="none" stroke="{INK}" stroke-width="{s * 0.06}" stroke-linecap="round"/>'
            f'<rect x="{cx - s * 0.36}" y="{cy - s * 0.22}" width="{s * 0.72}" height="{s * 0.1}" fill="{drink}"/>'
            f'<path d="M{cx - s * 0.15} {cy - s * 0.42} q-{s * 0.1} -{s * 0.12} 0 -{s * 0.24} M{cx + s * 0.08} {cy - s * 0.42} q-{s * 0.1} -{s * 0.12} 0 -{s * 0.24}" '
            f'fill="none" stroke="{NAVY4}" stroke-width="{s * 0.05}" stroke-linecap="round"/>')


def duck(cx, cy, s, body=HONEY):
    return (f'<ellipse cx="{cx + s * 0.08}" cy="{cy + s * 0.22}" rx="{s * 0.55}" ry="{s * 0.34}" fill="{body}"/>'
            f'<path d="M{cx + s * 0.5} {cy + s * 0.05} q{s * 0.25} -{s * 0.05} {s * 0.2} {s * 0.12}" fill="{body}"/>'
            f'<circle cx="{cx - s * 0.22}" cy="{cy - s * 0.2}" r="{s * 0.3}" fill="{body}"/>'
            f'<path d="M{cx - s * 0.52} {cy - s * 0.16} q-{s * 0.2} {s * 0.02} -{s * 0.24} {s * 0.12} q{s * 0.14} {s * 0.08} {s * 0.28} -{s * 0.02} Z" fill="{BRICK}"/>'
            f'<circle cx="{cx - s * 0.26}" cy="{cy - s * 0.26}" r="{s * 0.055}" fill="{INK}"/>'
            f'<path d="M{cx - s * 0.05} {cy + s * 0.12} q{s * 0.25} {s * 0.2} {s * 0.45} -{s * 0.02}" fill="none" stroke="{W}" stroke-width="{s * 0.05}" stroke-linecap="round" opacity="0.7"/>')


def laptop(cx, cy, s, screen=NAVY9, body=NAVY4):
    return (f'<rect x="{cx - s * 0.5}" y="{cy - s * 0.36}" width="{s}" height="{s * 0.62}" rx="{s * 0.05}" fill="{body}"/>'
            f'<rect x="{cx - s * 0.44}" y="{cy - s * 0.3}" width="{s * 0.88}" height="{s * 0.5}" rx="{s * 0.02}" fill="{screen}"/>'
            f'<path d="M{cx - s * 0.62} {cy + s * 0.28} H{cx + s * 0.62} L{cx + s * 0.56} {cy + s * 0.38} H{cx - s * 0.56} Z" fill="{body}"/>')


def bug(cx, cy, s, fill=BRICK):
    o = ""
    for dy in (-0.15, 0.1, 0.35):
        o += (f'<path d="M{cx - s * 0.28} {cy + s * dy} l-{s * 0.25} -{s * 0.05} M{cx + s * 0.28} {cy + s * dy} l{s * 0.25} -{s * 0.05}" '
              f'stroke="{INK}" stroke-width="{s * 0.06}" stroke-linecap="round"/>')
    o += (f'<path d="M{cx - s * 0.1} {cy - s * 0.42} l-{s * 0.12} -{s * 0.18} M{cx + s * 0.1} {cy - s * 0.42} l{s * 0.12} -{s * 0.18}" '
          f'stroke="{INK}" stroke-width="{s * 0.05}" stroke-linecap="round"/>')
    o += f'<circle cx="{cx}" cy="{cy - s * 0.32}" r="{s * 0.17}" fill="{INK}"/>'
    o += f'<ellipse cx="{cx}" cy="{cy + s * 0.12}" rx="{s * 0.32}" ry="{s * 0.4}" fill="{fill}"/>'
    o += f'<path d="M{cx} {cy - s * 0.26} V{cy + s * 0.52}" stroke="{INK}" stroke-width="{s * 0.04}"/>'
    o += f'<circle cx="{cx - s * 0.14}" cy="{cy}" r="{s * 0.06}" fill="{INK}"/><circle cx="{cx + s * 0.15}" cy="{cy + s * 0.22}" r="{s * 0.06}" fill="{INK}"/>'
    return o


def robot(cx, cy, s, fill=SKY):
    return (f'<path d="M{cx} {cy - s * 0.48} V{cy - s * 0.66}" stroke="{INK}" stroke-width="{s * 0.05}"/>'
            f'<circle cx="{cx}" cy="{cy - s * 0.7}" r="{s * 0.07}" fill="{BRICK}"/>'
            f'<rect x="{cx - s * 0.62}" y="{cy - s * 0.15}" width="{s * 0.1}" height="{s * 0.28}" rx="{s * 0.04}" fill="{NAVY4}"/>'
            f'<rect x="{cx + s * 0.52}" y="{cy - s * 0.15}" width="{s * 0.1}" height="{s * 0.28}" rx="{s * 0.04}" fill="{NAVY4}"/>'
            f'<rect x="{cx - s * 0.52}" y="{cy - s * 0.48}" width="{s * 1.04}" height="{s * 0.86}" rx="{s * 0.22}" fill="{fill}" stroke="{INK}" stroke-width="{s * 0.045}"/>'
            f'<rect x="{cx - s * 0.38}" y="{cy - s * 0.3}" width="{s * 0.76}" height="{s * 0.42}" rx="{s * 0.14}" fill="{NAVY9}"/>'
            f'<circle cx="{cx - s * 0.17}" cy="{cy - s * 0.1}" r="{s * 0.075}" fill="{HONEY}"/><circle cx="{cx + s * 0.17}" cy="{cy - s * 0.1}" r="{s * 0.075}" fill="{HONEY}"/>'
            f'<path d="M{cx - s * 0.16} {cy + s * 0.24} h{s * 0.32}" stroke="{INK}" stroke-width="{s * 0.05}" stroke-linecap="round" stroke-dasharray="{s * 0.04} {s * 0.06}"/>')


def wizard_hat(cx, cy, s, fill=NAVY):
    return (f'<path d="M{cx - s * 0.1} {cy - s * 0.62} L{cx + s * 0.38} {cy + s * 0.32} H{cx - s * 0.42} Z" fill="{fill}" stroke-linejoin="round"/>'
            f'<path d="M{cx - s * 0.1} {cy - s * 0.62} q-{s * 0.25} {s * 0.05} -{s * 0.3} {s * 0.2}" fill="none" stroke="{fill}" stroke-width="{s * 0.08}" stroke-linecap="round"/>'
            f'<ellipse cx="{cx}" cy="{cy + s * 0.34}" rx="{s * 0.6}" ry="{s * 0.13}" fill="{NAVY9}"/>'
            f'<rect x="{cx - s * 0.36}" y="{cy + s * 0.12}" width="{s * 0.7}" height="{s * 0.1}" fill="{HONEY}"/>'
            + star(cx + s * 0.02, cy - s * 0.12, s * 0.12, HONEY) + star(cx - s * 0.15, cy + s * 0.02, s * 0.07, W))


def star(cx, cy, r, fill):
    pts = " ".join(f"{cx + (r if i % 2 == 0 else r * 0.45) * math.cos(math.pi * i / 5 - math.pi / 2):.1f},"
                   f"{cy + (r if i % 2 == 0 else r * 0.45) * math.sin(math.pi * i / 5 - math.pi / 2):.1f}" for i in range(10))
    return f'<polygon points="{pts}" fill="{fill}" stroke-linejoin="round"/>'


def heart(cx, cy, k, fill=BRICK):
    return (f'<path d="M{cx} {cy + k} C{cx - k * 1.8} {cy - k * 0.2} {cx - k * 0.8} {cy - k * 1.6} {cx} {cy - k * 0.5} '
            f'C{cx + k * 0.8} {cy - k * 1.6} {cx + k * 1.8} {cy - k * 0.2} {cx} {cy + k} Z" fill="{fill}"/>')


def check(cx, cy, s, color=W, width=None):
    return (f'<path d="M{cx - s * 0.4} {cy} L{cx - s * 0.1} {cy + s * 0.3} L{cx + s * 0.45} {cy - s * 0.32}" fill="none" '
            f'stroke="{color}" stroke-width="{width or s * 0.16}" stroke-linecap="round" stroke-linejoin="round"/>')


def marshmallow(cx, cy, s, kind="happy"):
    return (f'<rect x="{cx - s * 0.45}" y="{cy - s * 0.4}" width="{s * 0.9}" height="{s * 0.85}" rx="{s * 0.3}" fill="{W}" stroke="{INK}" stroke-width="{s * 0.04}"/>'
            f'<ellipse cx="{cx}" cy="{cy - s * 0.32}" rx="{s * 0.38}" ry="{s * 0.1}" fill="{CREAM}"/>' + face(cx, cy + s * 0.05, s * 0.7, kind))


def battery(cx, cy, s, level, fill):
    w, h = s * 1.1, s * 0.6
    o = (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h * 0.22}" fill="{W}" stroke="{INK}" stroke-width="{s * 0.05}"/>'
         f'<rect x="{cx + w / 2}" y="{cy - h * 0.2}" width="{s * 0.08}" height="{h * 0.4}" rx="{s * 0.02}" fill="{INK}"/>')
    o += f'<rect x="{cx - w / 2 + s * 0.06}" y="{cy - h / 2 + s * 0.06}" width="{(w - s * 0.12) * level}" height="{h - s * 0.12}" rx="{h * 0.12}" fill="{fill}"/>'
    return o


def terminal(x, y, w, h, lines, title_fill=NAVY4):
    o = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{NAVY9}"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="10" fill="{title_fill}"/><rect x="{x}" y="{y + 12}" width="{w}" height="10" fill="{title_fill}"/>'
         f'<circle cx="{x + 16}" cy="{y + 11}" r="4.5" fill="{BRICK}"/><circle cx="{x + 30}" cy="{y + 11}" r="4.5" fill="{HONEY}"/><circle cx="{x + 44}" cy="{y + 11}" r="4.5" fill="{SAGE}"/>')
    for i, (txt, col) in enumerate(lines):
        o += t(x + 14, y + 46 + i * 22, txt, 15, col, M, 600, "start")
    return o


def dzezva(cx, cy, s, fill=HONEY):
    return (f'<path d="M{cx - s * 0.28} {cy - s * 0.35} H{cx + s * 0.28} L{cx + s * 0.42} {cy + s * 0.45} Q{cx + s * 0.42} {cy + s * 0.52} {cx + s * 0.34} {cy + s * 0.52} '
            f'H{cx - s * 0.34} Q{cx - s * 0.42} {cy + s * 0.52} {cx - s * 0.42} {cy + s * 0.45} Z" fill="{fill}" stroke="{INK}" stroke-width="{s * 0.05}" stroke-linejoin="round"/>'
            f'<path d="M{cx - s * 0.3} {cy - s * 0.35} q-{s * 0.12} -{s * 0.12} -{s * 0.22} -{s * 0.08}" fill="none" stroke="{INK}" stroke-width="{s * 0.05}" stroke-linecap="round"/>'
            f'<path d="M{cx + s * 0.36} {cy + s * 0.05} L{cx + s * 0.9} {cy - s * 0.3}" stroke="{INK}" stroke-width="{s * 0.09}" stroke-linecap="round"/>'
            f'<path d="M{cx - s * 0.05} {cy - s * 0.5} q-{s * 0.08} -{s * 0.1} 0 -{s * 0.2} M{cx + s * 0.13} {cy - s * 0.5} q-{s * 0.08} -{s * 0.1} 0 -{s * 0.2}" fill="none" stroke="{NAVY4}" stroke-width="{s * 0.045}" stroke-linecap="round"/>')


def tea_glass(cx, cy, s):
    return (f'<path d="M{cx - s * 0.26} {cy - s * 0.42} Q{cx - s * 0.12} {cy} {cx - s * 0.24} {cy + s * 0.38} H{cx + s * 0.24} Q{cx + s * 0.12} {cy} {cx + s * 0.26} {cy - s * 0.42} Z" '
            f'fill="{BRICK}" opacity="0.9" stroke="{INK}" stroke-width="{s * 0.04}" stroke-linejoin="round"/>'
            f'<path d="M{cx - s * 0.26} {cy - s * 0.42} H{cx + s * 0.26}" stroke="{INK}" stroke-width="{s * 0.04}"/>'
            f'<ellipse cx="{cx}" cy="{cy + s * 0.46}" rx="{s * 0.42}" ry="{s * 0.09}" fill="{W}" stroke="{INK}" stroke-width="{s * 0.04}"/>'
            f'<path d="M{cx - s * 0.06} {cy - s * 0.55} q-{s * 0.08} -{s * 0.1} 0 -{s * 0.2}" fill="none" stroke="{NAVY4}" stroke-width="{s * 0.04}" stroke-linecap="round"/>')


def sebilj(cx, cy, s, fill=NAVY):
    return (f'<rect x="{cx - s * 0.5}" y="{cy + s * 0.3}" width="{s}" height="{s * 0.1}" fill="{fill}"/>'
            f'<rect x="{cx - s * 0.38}" y="{cy - s * 0.12}" width="{s * 0.76}" height="{s * 0.42}" fill="{fill}"/>'
            + "".join(f'<rect x="{cx - s * 0.3 + i * s * 0.17}" y="{cy - s * 0.05}" width="{s * 0.09}" height="{s * 0.3}" rx="{s * 0.045}" fill="{SKY}"/>' for i in range(4))
            + f'<path d="M{cx - s * 0.45} {cy - s * 0.12} H{cx + s * 0.45} L{cx + s * 0.3} {cy - s * 0.2} H{cx - s * 0.3} Z" fill="{fill}"/>'
            f'<path d="M{cx - s * 0.3} {cy - s * 0.2} Q{cx - s * 0.3} {cy - s * 0.62} {cx} {cy - s * 0.66} Q{cx + s * 0.3} {cy - s * 0.62} {cx + s * 0.3} {cy - s * 0.2} Z" fill="{SAGE}"/>'
            f'<path d="M{cx} {cy - s * 0.66} V{cy - s * 0.8}" stroke="{HONEY}" stroke-width="{s * 0.04}"/>'
            f'<circle cx="{cx}" cy="{cy - s * 0.82}" r="{s * 0.04}" fill="{HONEY}"/>')


def rocket(cx, cy, s):
    return (f'<path d="M{cx} {cy - s * 0.6} C{cx + s * 0.3} {cy - s * 0.35} {cx + s * 0.25} {cy + s * 0.15} {cx + s * 0.18} {cy + s * 0.3} H{cx - s * 0.18} '
            f'C{cx - s * 0.25} {cy + s * 0.15} {cx - s * 0.3} {cy - s * 0.35} {cx} {cy - s * 0.6} Z" fill="{W}" stroke="{INK}" stroke-width="{s * 0.04}"/>'
            f'<circle cx="{cx}" cy="{cy - s * 0.15}" r="{s * 0.11}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.035}"/>'
            f'<path d="M{cx - s * 0.18} {cy + s * 0.05} L{cx - s * 0.36} {cy + s * 0.36} H{cx - s * 0.16} Z M{cx + s * 0.18} {cy + s * 0.05} L{cx + s * 0.36} {cy + s * 0.36} H{cx + s * 0.16} Z" fill="{BRICK}"/>'
            f'<path d="M{cx - s * 0.12} {cy + s * 0.32} Q{cx} {cy + s * 0.75} {cx + s * 0.12} {cy + s * 0.32} Z" fill="{HONEY}"/>')


def trophy(cx, cy, s):
    return (f'<path d="M{cx - s * 0.32} {cy - s * 0.45} H{cx + s * 0.32} V{cy - s * 0.15} Q{cx + s * 0.32} {cy + s * 0.15} {cx} {cy + s * 0.18} Q{cx - s * 0.32} {cy + s * 0.15} {cx - s * 0.32} {cy - s * 0.15} Z" fill="{HONEY}"/>'
            f'<path d="M{cx - s * 0.32} {cy - s * 0.35} q-{s * 0.25} 0 -{s * 0.2} {s * 0.18} q{s * 0.05} {s * 0.12} {s * 0.22} {s * 0.12} M{cx + s * 0.32} {cy - s * 0.35} q{s * 0.25} 0 {s * 0.2} {s * 0.18} q-{s * 0.05} {s * 0.12} -{s * 0.22} {s * 0.12}" fill="none" stroke="{HONEY}" stroke-width="{s * 0.07}"/>'
            f'<rect x="{cx - s * 0.06}" y="{cy + s * 0.16}" width="{s * 0.12}" height="{s * 0.16}" fill="{HONEY}"/>'
            f'<rect x="{cx - s * 0.26}" y="{cy + s * 0.32}" width="{s * 0.52}" height="{s * 0.13}" rx="{s * 0.03}" fill="{NAVY9}"/>')


def mic(cx, cy, s):
    return (f'<rect x="{cx - s * 0.17}" y="{cy - s * 0.5}" width="{s * 0.34}" height="{s * 0.6}" rx="{s * 0.17}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.04}"/>'
            f'<path d="M{cx - s * 0.3} {cy - s * 0.05} Q{cx - s * 0.3} {cy + s * 0.3} {cx} {cy + s * 0.3} Q{cx + s * 0.3} {cy + s * 0.3} {cx + s * 0.3} {cy - s * 0.05}" fill="none" stroke="{INK}" stroke-width="{s * 0.05}"/>'
            f'<path d="M{cx} {cy + s * 0.3} V{cy + s * 0.48} M{cx - s * 0.18} {cy + s * 0.48} H{cx + s * 0.18}" stroke="{INK}" stroke-width="{s * 0.05}" stroke-linecap="round"/>')


def cat(cx, cy, s, fill=NAVY4):
    return (f'<path d="M{cx - s * 0.45} {cy - s * 0.1} L{cx - s * 0.4} {cy - s * 0.55} L{cx - s * 0.12} {cy - s * 0.32} Z M{cx + s * 0.45} {cy - s * 0.1} '
            f'L{cx + s * 0.4} {cy - s * 0.55} L{cx + s * 0.12} {cy - s * 0.32} Z" fill="{fill}" stroke-linejoin="round"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.48}" ry="{s * 0.4}" fill="{fill}"/>' + face(cx, cy + s * 0.02, s * 0.8, "happy")
            + f'<path d="M{cx - s * 0.5} {cy + s * 0.05} h-{s * 0.18} M{cx - s * 0.5} {cy + s * 0.13} l-{s * 0.16} {s * 0.05} M{cx + s * 0.5} {cy + s * 0.05} h{s * 0.18} M{cx + s * 0.5} {cy + s * 0.13} l{s * 0.16} {s * 0.05}" stroke="{INK}" stroke-width="{s * 0.025}" stroke-linecap="round"/>')


def cloud(cx, cy, s, fill=W):
    return (f'<path d="M{cx - s * 0.5} {cy + s * 0.25} Q{cx - s * 0.75} {cy + s * 0.25} {cx - s * 0.72} {cy} Q{cx - s * 0.7} {cy - s * 0.25} {cx - s * 0.42} {cy - s * 0.2} '
            f'Q{cx - s * 0.35} {cy - s * 0.52} {cx} {cy - s * 0.5} Q{cx + s * 0.32} {cy - s * 0.5} {cx + s * 0.38} {cy - s * 0.2} Q{cx + s * 0.72} {cy - s * 0.22} {cx + s * 0.72} {cy + s * 0.05} '
            f'Q{cx + s * 0.72} {cy + s * 0.25} {cx + s * 0.48} {cy + s * 0.25} Z" fill="{fill}" stroke="{INK}" stroke-width="{s * 0.04}" stroke-linejoin="round"/>')


def keycap(x, y, w, label, fill=W):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="10" fill="{NAVY9}"/>'
            f'<rect x="{x + 3}" y="{y + 2}" width="{w - 6}" height="42" rx="8" fill="{fill}"/>' + t(x + w / 2, y + 31, label, 20, INK, M, 700))


def wrench(cx, cy, s, fill=NAVY4):
    return (f'<g transform="rotate(-45 {cx} {cy})"><rect x="{cx - s * 0.09}" y="{cy - s * 0.25}" width="{s * 0.18}" height="{s * 0.8}" rx="{s * 0.09}" fill="{fill}"/>'
            f'<path d="M{cx - s * 0.24} {cy - s * 0.42} a{s * 0.26} {s * 0.26} 0 1 0 {s * 0.48} 0 l-{s * 0.12} {s * 0.06} v-{s * 0.2} z" fill="{fill}"/></g>')


def ruler(x, y, w, h, fill=HONEYL):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
    for i in range(1, int(w // 10)):
        o += f'<path d="M{x + i * 10} {y} v{h * (0.45 if i % 5 == 0 else 0.25)}" stroke="{INK}" stroke-width="1.6"/>'
    return o


# ---------------------------------------------------------------- A · IEC identity

def wordmark_gear(cx, cy, s):
    return gear(cx, cy, s * 0.62, s * 0.5, 14, NAVY, s * 0.36, W) + t(cx, cy + s * 0.13, "IEC", s * 0.36, NAVY9, G, 700)


add("A01", "kimlik", "IEC dişli rozet", 200, 200, 50, hexagon(100, 98, NAVY9) + wordmark_gear(100, 92, 120)
    + t(100, 158, "ENGINEERING", 11, W, M, 700, ls=1.5) + t(100, 172, "CLUB", 11, HONEY, M, 700, ls=2))
add("A02", "kimlik", "IEC · Sarajevo · 2026", 200, 200, 50, circle(100, 98, SKY, NAVY4)
    + f'<path id="arcA02" d="M30 104 A70 70 0 0 1 170 104" fill="none"/>'
    + f'<text font-family="{M}" font-size="11.5" font-weight="700" fill="{NAVY}" letter-spacing="1.6"><textPath href="#arcA02" startOffset="50%" text-anchor="middle">IUS ENGINEERING CLUB</textPath></text>'
    + gear(100, 112, 34, 27, 10, NAVY, 14, SKY) + t(100, 172, "SARAJEVO · 2026", 12, NAVY9, M, 700, ls=1.5))
add("A03", "kimlik", "IEC est. 2026", 300, 120, 70, rrect(300, 120, 58, NAVY) + gear(68, 60, 28, 22, 10, HONEY, 10, NAVY)
    + t(178, 70, "IEC", 46, W, G, 700) + t(178, 94, "EST. 2026", 13, HONEYL, M, 700, ls=3))
add("A04", "kimlik", "Kulüp sloganı", 300, 170, 75, rrect(300, 170, 26, PAPER, stroke=NAVY)
    + t(150, 62, "We turn what we", 23, NAVY9, F, 600) + t(150, 92, "learn in class into", 23, NAVY9, F, 600)
    + t(150, 124, "real projects.", 27, HONEY, F, 700) + bolt(250, 120, 26))
add("A05", "kimlik", "Kurucu üye 2026", 200, 200, 52, burst(100, 98, 16, HONEY) + star(100, 62, 16, W)
    + t(100, 104, "FOUNDING", 20, NAVY9, F, 700) + t(100, 128, "MEMBER", 20, NAVY9, F, 700) + t(100, 150, "2026", 15, W, M, 700))
add("A06", "kimlik", "Yönetim kurulu", 180, 210, 45, shield(180, 210, NAVY) + gear(90, 78, 30, 24, 10, HONEY, 12, NAVY)
    + t(90, 140, "BOARD", 26, W, F, 700) + t(90, 164, "MEMBER", 16, HONEYL, M, 700, ls=2))
add("A07", "kimlik", "Mentor", 200, 200, 48, circle(100, 98, SAGE) + bulb(100, 78, 54, HONEY)
    + t(100, 150, "MENTOR", 26, W, F, 700))
add("A08", "kimlik", "Gönüllü", 200, 200, 48, circle(100, 98, HONEY) + heart(100, 82, 22, W)
    + t(100, 148, "VOLUNTEER", 22, NAVY9, F, 700))
add("A09", "kimlik", "IEC Pass damgası", 200, 200, 45, circle(100, 98, W) +
    f'<circle cx="100" cy="98" r="72" fill="none" stroke="{BRICK}" stroke-width="5"/><circle cx="100" cy="98" r="62" fill="none" stroke="{BRICK}" stroke-width="1.6"/>'
    + t(100, 92, "IEC", 30, BRICK, G, 700) + t(100, 118, "PASS", 22, BRICK, G, 700) + check(100, 140, 18, BRICK, 5)
    + t(100, 50, "★ ★ ★", 10, BRICK, M, 700))
add("A10", "kimlik", "Teknik resim IEC", 300, 170, 75, rrect(300, 170, 18, NAVY9)
    + "".join(f'<path d="M{20 + i * 20} 18 V152" stroke="{NAVY}" stroke-width="1"/>' for i in range(14))
    + t(150, 102, "IEC", 70, "none", G, 700, extra=f'stroke="{W}" stroke-width="2.4"')
    + f'<path d="M58 124 H242 M58 118 V130 M242 118 V130" stroke="{HONEY}" stroke-width="2"/>'
    + t(150, 146, "ENGINEERING CLUB", 12, HONEYL, M, 700, ls=3))
add("A11", "kimlik", "Sarajevo × Engineers", 300, 110, 70, tag(300, 110, SAGE) + t(178, 52, "SARAJEVO", 26, W, F, 700)
    + t(178, 78, "× ENGINEERS", 16, SAGEL, M, 700, ls=2))
add("A12", "kimlik", "Made at IEC", 200, 200, 45, burst(100, 98, 12, NAVY) + t(100, 92, "MADE", 22, W, F, 700)
    + t(100, 116, "AT IEC", 22, HONEY, F, 700) + gear(100, 140, 10, 8, 8, W, 3, NAVY))
add("A13", "kimlik", "IEC üye kartı", 300, 190, 70, rrect(300, 190, 20, PAPER, stroke=NAVY)
    + f'<rect x="10" y="10" width="280" height="40" rx="10" fill="{NAVY}"/>' + t(150, 37, "IEC · MEMBER", 18, W, M, 700, ls=2)
    + f'<rect x="30" y="66" width="80" height="96" rx="10" fill="{SKY}"/>' + face(70, 116, 60, "happy")
    + f'<path d="M128 82 H262 M128 108 H262 M128 134 H220" stroke="{NAVY4}" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 9"/>'
    + t(128, 160, "since 2026", 13, NAVY, M, 600, "start"))
add("A14", "kimlik", "Bana IEC'yi sor", 260, 180, 62, bubble(260, 180, HONEY) + t(130, 66, "Ask me", 30, NAVY9, F, 700)
    + t(130, 102, "about IEC!", 30, W, F, 700))

# ---------------------------------------------------------------- B · engineering jokes

add("B01", "espri", "It works on my machine", 240, 200, 55, rrect(240, 200, 28, SKY) + laptop(120, 82, 100)
    + check(120, 72, 30, SAGE, 8) + t(120, 158, "It works on", 19, NAVY9, F, 600) + t(120, 180, "my machine", 19, NAVY9, F, 700))
add("B02", "espri", "Bug değil, özellik", 220, 220, 52, circle(110, 108, HONEYL) + bug(110, 86, 70)
    + t(110, 154, "not a bug,", 18, NAVY9, F, 600) + t(110, 176, "a feature", 20, BRICK, F, 700))
add("B03", "espri", "Ohm my God", 300, 120, 70, rrect(300, 120, 58, NAVY9) + resistor(76, 60, 44)
    + t(196, 66, "Ohm my God", 24, W, F, 700) + t(196, 90, "Ω", 18, HONEY, F, 700))
add("B04", "espri", "Resistance is futile", 220, 220, 52, circle(110, 108, SKY) + resistor(110, 82, 70)
    + t(110, 140, "RESISTANCE", 18, NAVY9, F, 700) + t(110, 162, "IS FUTILE", 18, NAVY9, F, 700) + t(110, 182, "(if < 1 Ω)", 13, NAVY, M, 600))
add("B05", "espri", "Trust me, I'm an engineer", 300, 130, 72, rrect(300, 130, 24, HONEY) + gear(52, 65, 30, 24, 10, NAVY9, 11, HONEY)
    + t(178, 58, "Trust me,", 26, NAVY9, F, 700) + t(178, 90, "I'm an engineer", 21, W, F, 700))
add("B06", "espri", "I void warranties", 200, 200, 48, burst(100, 98, 14, BRICK) + wrench(100, 78, 70, W)
    + t(100, 138, "I VOID", 20, W, F, 700) + t(100, 160, "WARRANTIES", 15, CREAM, M, 700))
add("B07", "espri", "Ctrl + Z", 300, 120, 70, rrect(300, 120, 26, SKY) + keycap(28, 30, 96, "Ctrl") + t(150, 66, "+", 28, NAVY9, F, 700)
    + keycap(176, 30, 96, "Z"))
add("B08", "espri", "404: sleep not found", 220, 200, 52, rrect(220, 200, 30, NAVY9) + t(110, 92, "404", 58, HONEY, M, 700)
    + t(110, 128, "sleep", 22, W, F, 600) + t(110, 154, "not found", 22, W, F, 600) + t(160, 66, "z", 18, SKY, F, 700) + t(176, 52, "z", 13, SKY, F, 700))
add("B09", "espri", "Coffee → Code", 300, 120, 70, rrect(300, 120, 58, CREAM, stroke=HONEY) + cup(58, 62, 52)
    + t(170, 72, "coffee", 22, NAVY9, F, 600) + t(216, 72, "→", 22, HONEY, F, 700) + t(254, 72, "</>", 20, NAVY, M, 700))
add("B10", "espri", "Hello, World!", 260, 180, 60, rrect(260, 180, 20, PAPER)
    + terminal(22, 22, 216, 136, [("$ ./hello", SAGEL), ("Hello, World!", HONEY), ("$ _", W)]))
add("B11", "espri", "There's no place like 127.0.0.1", 220, 220, 52, circle(110, 108, SAGEL)
    + f'<path d="M70 104 L110 66 L150 104 V140 H70 Z" fill="{W}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    + f'<rect x="100" y="114" width="20" height="26" fill="{HONEY}"/>' + t(110, 162, "no place like", 15, NAVY9, F, 600)
    + t(110, 182, "127.0.0.1", 18, NAVY, M, 700))
add("B12", "espri", "git push --force", 220, 200, 52,
    f'<path d="M110 6 L214 190 H6 Z" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
    f'<path d="M110 26 L196 180 H24 Z" fill="{HONEY}" stroke-linejoin="round"/>'
    + t(110, 108, "!", 44, NAVY9, F, 700) + t(110, 140, "git push", 15, NAVY9, M, 700) + t(110, 158, "--force", 15, NAVY9, M, 700)
    + t(110, 174, "(please don't)", 10, NAVY9, F, 600))
add("B13", "espri", "Measure twice, cut once", 300, 130, 72, rrect(300, 130, 22, PAPER, stroke=SAGE) + ruler(26, 26, 248, 30)
    + t(150, 88, "Measure twice,", 21, NAVY9, F, 600) + t(150, 112, "cut once ✂", 21, SAGE, F, 700))
add("B14", "espri", "Keep calm and debug on", 180, 220, 45, rrect(180, 220, 18, NAVY) + t(90, 48, "♛", 22, HONEY, F, 600)
    + t(90, 84, "KEEP", 26, W, F, 700) + t(90, 112, "CALM", 26, W, F, 700) + t(90, 136, "AND", 14, HONEYL, M, 700)
    + t(90, 166, "DEBUG", 26, W, F, 700) + t(90, 194, "ON", 26, W, F, 700))
add("B15", "espri", "Runs on caffeine", 260, 150, 60, rrect(260, 150, 30, SAGEL) + battery(82, 64, 80, 0.82, SAGE) + cup(196, 68, 44)
    + t(130, 128, "runs on caffeine", 20, NAVY9, F, 700))
add("B16", "espri", "It compiled!", 200, 200, 48, burst(100, 98, 18, SAGE) + t(100, 88, "IT", 22, W, F, 700)
    + t(100, 116, "COMPILED!", 22, W, F, 700) + star(56, 140, 9, HONEY) + star(146, 64, 7, HONEY) + star(140, 142, 6, W))
add("B17", "espri", "Unutulan noktalı virgül", 200, 200, 45, circle(100, 98, SKY)
    + f'<circle cx="100" cy="62" r="22" fill="{NAVY}"/><circle cx="100" cy="114" r="22" fill="{NAVY}"/>'
    + f'<path d="M116 128 Q114 152 92 164" fill="none" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>'
    + face(100, 64, 34, "confused", W) + face(100, 116, 34, "sleepy", W) + t(100, 182, "forgot me again?", 12, NAVY9, F, 600))
add("B18", "espri", "418 I'm a teapot", 220, 200, 52, rrect(220, 200, 30, CREAM, stroke=HONEY) + dzezva(96, 84, 62)
    + t(110, 154, "ERROR 418", 18, BRICK, M, 700) + t(110, 176, "I'm a teapot", 17, NAVY9, F, 600))
add("B19", "espri", "while(alive) learn()", 300, 120, 70, rrect(300, 120, 20, NAVY9)
    + t(150, 52, "while (alive) {", 20, SKY, M, 600) + t(150, 78, "  learn();", 20, HONEY, M, 700) + t(150, 102, "}", 20, SKY, M, 600))
add("B20", "espri", "Rubber duck debugging", 220, 220, 52, circle(110, 108, SKY) + duck(112, 92, 80)
    + t(110, 162, "explain it", 17, NAVY9, F, 600) + t(110, 182, "to the duck", 17, NAVY9, F, 700))
add("B21", "espri", "F = ma(gic)", 200, 200, 45, hexagon(100, 98, NAVY) + t(100, 108, "F = ma", 30, W, F, 700)
    + t(100, 136, "(gic)", 20, HONEY, F, 700) + star(60, 66, 8, HONEY) + star(142, 72, 6, W))
add("B22", "espri", "Problem? Solved. (sonunda)", 300, 130, 72, rrect(300, 130, 22, HONEYL) + t(150, 56, "Problem?", 24, NAVY9, F, 600)
    + t(150, 88, "Solved.", 30, NAVY, F, 700) + t(150, 110, "(eventually)", 13, NAVY9, M, 600))
add("B23", "espri", "Deadline: yesterday", 200, 200, 48, rrect(200, 200, 26, W, stroke=NAVY)
    + f'<rect x="10" y="10" width="180" height="46" rx="18" fill="{BRICK}"/><rect x="10" y="38" width="180" height="18" fill="{BRICK}"/>'
    + t(100, 42, "DEADLINE", 18, W, M, 700, ls=2) + t(100, 112, "yester-", 30, NAVY9, F, 700) + t(100, 146, "day", 30, NAVY9, F, 700)
    + face(100, 172, 30, "shock"))
add("B24", "espri", "brain.exe yanıt vermiyor", 300, 150, 72, rrect(300, 150, 16, PAPER)
    + f'<rect x="20" y="20" width="260" height="110" rx="8" fill="{W}" stroke="{NAVY}" stroke-width="2.5"/>'
    + f'<rect x="20" y="20" width="260" height="26" rx="8" fill="{NAVY}"/><rect x="20" y="34" width="260" height="12" fill="{NAVY}"/>'
    + t(34, 39, "brain.exe", 13, W, M, 700, "start") + t(264, 39, "×", 16, W, F, 700)
    + t(150, 80, "has stopped", 20, NAVY9, F, 600) + t(150, 106, "responding", 20, BRICK, F, 700))
add("B25", "espri", "0 bugs*", 200, 200, 45, circle(100, 98, SAGE) + t(100, 108, "0 bugs*", 34, W, F, 700)
    + t(100, 136, "*that we know of", 11, SAGEL, M, 600))

# ---------------------------------------------------------------- C · mascots

def gear_mascot(sid, name, kind, extra="", label=None, fill=HONEY, bg=SKY):
    body = circle(100, 98, bg) + gear(100, 92, 64, 54, 12, fill) + f'<circle cx="100" cy="92" r="46" fill="{fill}"/>' + face(100, 94, 70, kind) + extra
    if label:
        body += t(100, 176, label, 16, NAVY9, F, 700)
    add(sid, "maskot", name, 200, 200, 48, body)


gear_mascot("C01", "Dişli · mutlu", "happy", label="hi!")
gear_mascot("C02", "Dişli · uykulu", "sleepy", t(156, 46, "z", 22, NAVY, F, 700) + t(170, 30, "z", 15, NAVY, F, 700), "5 more min", NAVY4, SKY)
gear_mascot("C03", "Dişli · kahveli", "coffee", cup(150, 128, 36), "fuelled", HONEY, CREAM)
gear_mascot("C04", "Dişli · havalı", "cool", "", "cool gear", SAGE, SAGEL)
gear_mascot("C05", "Dişli · aşık", "love", "", "I ♥ eng", BRICK, CREAM)
gear_mascot("C06", "Dişli · şaşkın", "confused", t(158, 50, "?!", 28, BRICK, F, 700), "debugging", NAVY4, SKY)
add("C07", "maskot", "Direnç dostu", 220, 200, 52, rrect(220, 200, 34, CREAM)
    + f'<path d="M20 92 H200" stroke="{NAVY4}" stroke-width="7" stroke-linecap="round"/>'
    + f'<rect x="56" y="54" width="108" height="76" rx="34" fill="{HONEYL}" stroke="{INK}" stroke-width="3"/>'
    + f'<rect x="72" y="56" width="10" height="72" fill="{BRICK}"/><rect x="140" y="56" width="10" height="72" fill="{SAGE}"/>'
    + face(110, 92, 50, "wink") + t(110, 168, "I resist!", 20, NAVY9, F, 700))
add("C08", "maskot", "Pil · dolu", 220, 200, 52, rrect(220, 200, 34, SAGEL) + battery(104, 86, 120, 1.0, SAGE) + face(100, 86, 54, "proud")
    + t(110, 170, "100% ready", 20, NAVY9, F, 700))
add("C09", "maskot", "Sosyal pil %3", 220, 200, 52, rrect(220, 200, 34, CREAM) + battery(104, 86, 120, 0.08, BRICK) + face(96, 86, 54, "tired")
    + t(110, 162, "social battery", 15, NAVY9, F, 600) + t(110, 182, "3%", 18, BRICK, F, 700))
add("C10", "maskot", "Fikir ampulü", 200, 200, 48, circle(100, 98, NAVY) + bulb(100, 84, 86, HONEY) + face(100, 82, 56, "happy")
    + f'<path d="M100 22 V34 M44 44 l9 9 M156 44 l-9 9 M30 90 h12 M158 90 h12" stroke="{HONEYL}" stroke-width="4" stroke-linecap="round"/>'
    + t(100, 168, "idea!", 18, W, F, 700))
add("C11", "maskot", "Çip dostu", 200, 200, 48, circle(100, 98, SKY) + chip(100, 92, 90, NAVY9) + face(100, 94, 50, "happy", W)
    + t(100, 176, "smart chip", 15, NAVY9, F, 700))
add("C12", "maskot", "Robot · beep boop", 200, 200, 48, circle(100, 98, SAGEL) + robot(100, 100, 92, W)
    + t(100, 176, "beep boop", 16, NAVY9, F, 700))
add("C13", "maskot", "Lastik ördek", 200, 200, 48, circle(100, 98, NAVY) + duck(104, 90, 90, HONEY)
    + t(100, 168, "quack.", 18, W, F, 700))
add("C14", "maskot", "Marshmallow", 200, 200, 48, circle(100, 98, HONEYL) + marshmallow(100, 90, 96)
    + t(100, 172, "squishy but stable", 13, NAVY9, F, 700))
add("C15", "maskot", "Kod kedisi", 220, 200, 52, rrect(220, 200, 34, SKY) + laptop(110, 132, 104, NAVY9, NAVY4) + cat(110, 74, 70, HONEY)
    + t(110, 128, "</>", 14, HONEY, M, 700))
add("C16", "maskot", "Kondansatör · şarjlı", 200, 200, 48, circle(100, 98, CREAM)
    + f'<path d="M86 140 V170 M114 140 V176" stroke="{NAVY4}" stroke-width="6" stroke-linecap="round"/>'
    + f'<rect x="58" y="44" width="84" height="100" rx="20" fill="{NAVY}"/><rect x="58" y="44" width="16" height="100" rx="8" fill="{NAVY4}"/>'
    + face(104, 92, 54, "happy", W) + bolt(146, 40, 26))
add("C17", "maskot", "LED · parla", 200, 200, 48, circle(100, 98, NAVY9)
    + f'<path d="M86 132 V174 M114 132 V166" stroke="{NAVY4}" stroke-width="6" stroke-linecap="round"/>'
    + f'<path d="M62 132 V84 A38 38 0 0 1 138 84 V132 Z" fill="{SAGE}"/><rect x="56" y="126" width="88" height="12" rx="4" fill="{SAGEL}"/>'
    + face(100, 96, 54, "wink", W) + f'<path d="M30 60 l14 8 M170 60 l-14 8 M100 22 v14" stroke="{SAGEL}" stroke-width="4" stroke-linecap="round"/>')
add("C18", "maskot", "Bulutta", 240, 170, 55, rrect(240, 170, 30, SKY) + cloud(120, 78, 130) + face(120, 80, 50, "happy")
    + t(120, 148, "living in the cloud", 15, NAVY9, F, 700))
add("C19", "maskot", "Roket · fırlatma günü", 200, 200, 48, circle(100, 98, NAVY) + rocket(100, 86, 110)
    + star(46, 60, 7, W) + star(152, 52, 6, HONEY) + star(150, 130, 5, W) + t(100, 172, "launch day", 15, W, F, 700))
add("C20", "maskot", "Spagetti kulesi", 200, 220, 48, rrect(200, 220, 30, CREAM)
    + f'<path d="M100 54 L62 176 M100 54 L138 176 M70 150 H130 M78 122 H122 M88 96 H112 M62 176 H138" stroke="{HONEY}" stroke-width="4" stroke-linecap="round"/>'
    + marshmallow(100, 44, 40) + t(100, 202, "tallest tower!", 15, NAVY9, F, 700))

# ---------------------------------------------------------------- D · useful labels

def label(sid, name, text, sub, fill, fg=W, w=300, h=110, mm=60, icon=""):
    add(sid, "etiket", name, w, h, mm, rrect(w, h, 22, fill) + icon + t(w / 2 + (18 if icon else 0), h / 2 + (2 if sub else 10), text, 28, fg, F, 700)
        + (t(w / 2 + (18 if icon else 0), h / 2 + 26, sub, 13, fg, M, 600) if sub else ""))


label("D01", "TODO", "TODO", "", NAVY, icon=f'<rect x="34" y="34" width="40" height="40" rx="8" fill="none" stroke="{W}" stroke-width="5"/>')
label("D02", "Devam ediyor", "IN PROGRESS", "", HONEY, NAVY9, icon=f'<circle cx="54" cy="55" r="20" fill="none" stroke="{NAVY9}" stroke-width="5" stroke-dasharray="70 40"/>')
label("D03", "Bitti", "DONE", "", SAGE, icon=check(56, 55, 40))
add("D04", "etiket", "BUG etiketi", 300, 110, 60, rrect(300, 110, 22, BRICK) + bug(60, 58, 52, CREAM) + t(170, 68, "BUG", 34, W, F, 700))
label("D05", "Kırılgan prototip", "FRAGILE", "prototype · handle with care", HONEYL, NAVY9)
label("D06", "Fişten çekme", "DO NOT UNPLUG", "", BRICK, icon=bolt(30, 32, 46, W))
add("D07", "etiket", "Şarj oluyor", 300, 110, 60, rrect(300, 110, 22, SAGEL) + battery(70, 55, 64, 0.55, SAGE) + bolt(60, 38, 30, HONEY)
    + t(190, 66, "charging…", 26, NAVY9, F, 700))
add("D08", "etiket", "Hello my name is", 280, 190, 65, rrect(280, 190, 22, NAVY)
    + f'<rect x="10" y="74" width="260" height="96" fill="{W}"/>' + t(140, 46, "HELLO", 30, W, F, 700) + t(140, 66, "my name is", 13, HONEYL, M, 600)
    + f'<path d="M36 146 H244" stroke="{NAVY4}" stroke-width="2" stroke-dasharray="4 5"/>')
add("D09", "etiket", "Takım: ___", 300, 110, 60, rrect(300, 110, 22, W, stroke=SAGE) + t(30, 64, "TEAM", 24, SAGE, F, 700, "start")
    + f'<path d="M110 70 H270" stroke="{NAVY4}" stroke-width="2.5" stroke-dasharray="5 5"/>')
add("D10", "etiket", "IEC Lab malı", 300, 110, 60, rrect(300, 110, 22, NAVY9) + gear(56, 55, 26, 20, 10, HONEY, 9, NAVY9)
    + t(176, 52, "PROPERTY OF", 14, HONEYL, M, 700, ls=2) + t(176, 80, "IEC LAB", 28, W, F, 700))
label("D11", "Laba geri getir", "RETURN TO LAB", "thank you!", SKY, NAVY9)
add("D12", "etiket", "Test edildi", 220, 200, 50, circle(110, 100, W) + f'<circle cx="110" cy="100" r="78" fill="none" stroke="{SAGE}" stroke-width="5"/>'
    + check(110, 82, 40, SAGE, 10) + t(110, 136, "TESTED", 22, SAGE, F, 700) + t(110, 158, "date ____", 12, NAVY9, M, 600))
label("D13", "Ortak laptop", "SHARED LAPTOP", "please log out", NAVY4)
label("D14", "Sıcak havya", "HOT! 400 °C", "soldering iron · do not touch", BRICK)
add("D15", "etiket", "Gözlük tak", 220, 200, 50, circle(110, 100, HONEY)
    + f'<rect x="54" y="74" width="48" height="34" rx="14" fill="{NAVY9}"/><rect x="118" y="74" width="48" height="34" rx="14" fill="{NAVY9}"/>'
    + f'<path d="M102 88 H118" stroke="{NAVY9}" stroke-width="5"/>' + t(110, 140, "GOGGLES", 20, NAVY9, F, 700) + t(110, 160, "ON", 16, W, F, 700))
add("D16", "etiket", "Su iç, sonra debug", 200, 230, 48, rrect(200, 230, 34, SKY)
    + f'<path d="M100 40 C80 72 66 92 66 112 A34 34 0 0 0 134 112 C134 92 120 72 100 40 Z" fill="{NAVY4}"/>'
    + face(100, 116, 40, "happy", W) + t(100, 182, "hydrate,", 18, NAVY9, F, 600) + t(100, 204, "then debug", 18, NAVY, F, 700))

# ---------------------------------------------------------------- E · events

add("E01", "etkinlik", "IUS DevHack 2027", 300, 130, 72, ticket(300, 130, NAVY9) + t(150, 56, "IUS DEVHACK", 26, W, F, 700)
    + t(150, 84, "2027 · 24 HOURS", 15, HONEY, M, 700, ls=2) + f'<path d="M60 100 H240" stroke="{NAVY4}" stroke-width="2" stroke-dasharray="3 6"/>')
add("E02", "etkinlik", "DevHack'ten sağ çıktım", 200, 200, 48, burst(100, 98, 14, HONEY) + face(100, 78, 60, "tired")
    + t(100, 132, "I SURVIVED", 17, NAVY9, F, 700) + t(100, 154, "DEVHACK", 20, W, F, 700))
add("E03", "etkinlik", "IUS TechSummit 2027", 300, 130, 72, rrect(300, 130, 24, SAGE)
    + f'<path d="M30 96 L70 54 L100 82 L130 46 L170 96 Z" fill="{SAGEL}" opacity="0.6"/>' + t(190, 60, "TECHSUMMIT", 24, W, F, 700)
    + t(190, 86, "IUS · 2027", 15, SAGEL, M, 700, ls=2))
add("E04", "etkinlik", "Algolab", 220, 200, 52, rrect(220, 200, 30, NAVY)
    + t(110, 70, "ALGOLAB", 28, W, F, 700) + t(110, 108, ">>> python", 15, HONEY, M, 600) + t(110, 132, ">> matlab", 15, SAGEL, M, 600)
    + t(110, 168, "fastest code wins", 13, SKY, F, 600))
add("E05", "etkinlik", "Prompt Wars", 220, 200, 52, circle(110, 100, BRICK) + wizard_hat(110, 80, 70, NAVY9)
    + t(110, 146, "PROMPT", 22, W, F, 700) + t(110, 170, "WARS", 22, CREAM, F, 700))
add("E06", "etkinlik", "Merlin Düellosu", 200, 200, 48, circle(100, 98, NAVY9) + wizard_hat(100, 80, 76, NAVY)
    + t(100, 150, "MERLIN DUEL", 17, HONEY, F, 700) + t(100, 170, "say the word", 12, SKY, M, 600))
add("E07", "etkinlik", "Marshmallow şampiyonu", 200, 220, 48, rrect(200, 220, 30, HONEYL) + trophy(100, 78, 100)
    + t(100, 162, "MARSHMALLOW", 16, NAVY9, F, 700) + t(100, 186, "CHAMPION", 20, NAVY, F, 700))
add("E08", "etkinlik", "Atölye tamam", 200, 200, 45, circle(100, 98, SAGE) + check(100, 80, 54) + t(100, 146, "WORKSHOP", 20, W, F, 700)
    + t(100, 166, "completed", 13, SAGEL, M, 600))
add("E09", "etkinlik", "IEC Pass 10/10", 300, 150, 72, rrect(300, 150, 22, NAVY) + t(150, 44, "IEC PASS", 20, HONEY, F, 700)
    + "".join(f'<circle cx="{50 + (i % 5) * 50}" cy="{76 + (i // 5) * 40}" r="15" fill="{HONEY}"/>' + check(50 + (i % 5) * 50, 76 + (i // 5) * 40, 14, NAVY9, 3.4)
              for i in range(10)))
add("E10", "etkinlik", "Demo Day", 220, 200, 52, rrect(220, 200, 30, NAVY9)
    + f'<path d="M70 20 L40 170 H180 L150 20 Z" fill="{HONEYL}" opacity="0.25"/>' + robot(110, 98, 60, W)
    + t(110, 176, "DEMO DAY", 20, HONEY, F, 700))
add("E11", "etkinlik", "Yıl sonu sergisi", 300, 120, 70, tag(300, 120, HONEY) + t(180, 58, "YEAR-END EXPO", 22, NAVY9, F, 700)
    + t(180, 84, "come see what we built", 12, NAVY9, M, 600))
add("E12", "etkinlik", "Çevrim içi söyleşi", 200, 200, 45, circle(100, 98, SKY) + mic(100, 86, 90) + t(100, 166, "online talk", 16, NAVY9, F, 700))
add("E13", "etkinlik", "Takım çalışması", 220, 200, 52, rrect(220, 200, 30, SAGEL)
    + gear(82, 84, 40, 32, 10, NAVY, 13, SAGEL) + gear(140, 112, 32, 25, 9, HONEY, 10, SAGEL, 0.3)
    + t(110, 172, "better together", 17, NAVY9, F, 700))
add("E14", "etkinlik", "Sertifika kazandım", 200, 230, 48, rrect(200, 230, 26, W, stroke=HONEY)
    + f'<rect x="38" y="36" width="124" height="88" rx="6" fill="{CREAM}" stroke="{HONEY}" stroke-width="2"/>'
    + f'<path d="M58 62 H142 M58 80 H142 M58 98 H112" stroke="{NAVY4}" stroke-width="4" stroke-linecap="round"/>'
    + f'<circle cx="140" cy="122" r="20" fill="{HONEY}"/><path d="M128 138 L122 166 L140 156 L158 166 L152 138" fill="{HONEY}"/>'
    + t(84, 178, "certified!", 18, NAVY, F, 700) + t(100, 206, "verify online ✓", 11, SAGE, M, 600))

# ---------------------------------------------------------------- F · Sarajevo and languages

add("F01", "sarajevo", "Saraybosna mühendisi", 200, 220, 48, rrect(200, 220, 30, SKY) + sebilj(100, 112, 110)
    + t(100, 180, "SARAJEVO", 20, NAVY9, F, 700) + t(100, 200, "engineer", 14, NAVY, M, 600))
add("F02", "sarajevo", "Kahva & kod", 220, 200, 52, circle(110, 100, CREAM) + dzezva(98, 86, 62)
    + t(110, 152, "kahva & kod", 20, NAVY9, F, 700) + t(110, 172, "Bosnian coffee build", 10, NAVY, M, 600))
add("F03", "sarajevo", "Çay & kod", 200, 200, 48, circle(100, 98, SAGEL) + tea_glass(100, 82, 76)
    + t(100, 160, "çay & kod", 20, NAVY9, F, 700))
add("F04", "sarajevo", "Hello World · 3 dil", 300, 150, 72, rrect(300, 150, 22, NAVY9)
    + t(150, 50, "Hello, World!", 20, W, M, 700) + t(150, 82, "Merhaba, Dünya!", 20, HONEY, M, 700) + t(150, 114, "Zdravo, svijete!", 20, SAGEL, M, 700))
add("F05", "sarajevo", "Ćevapi ile çalışır", 300, 120, 70, rrect(300, 120, 58, HONEY)
    + "".join(f'<rect x="{40 + i * 13}" y="{40 + (i % 2) * 6}" width="11" height="40" rx="5.5" fill="{BRICK}"/>' for i in range(5))
    + t(190, 66, "ĆEVAPI", 26, NAVY9, F, 700) + t(190, 88, "powered", 14, W, M, 700, ls=2))
add("F06", "sarajevo", "Baščaršija → Lab", 260, 200, 60, rrect(260, 200, 26, SAGEL)
    + f'<rect x="124" y="40" width="10" height="148" fill="{NAVY9}"/>'
    + f'<path d="M30 52 H186 L206 72 L186 92 H30 Z" fill="{NAVY}"/><path d="M230 108 H74 L54 128 L74 148 H230 Z" fill="{HONEY}"/>'
    + t(106, 79, "BAŠČARŠIJA", 15, W, F, 700) + t(152, 135, "IEC LAB 50 m", 15, NAVY9, F, 700))
add("F07", "sarajevo", "TR · EN · BS", 300, 110, 70, rrect(300, 110, 54, PAPER, stroke=NAVY)
    + f'<rect x="22" y="22" width="80" height="66" rx="26" fill="{BRICK}"/><rect x="110" y="22" width="80" height="66" rx="26" fill="{NAVY}"/><rect x="198" y="22" width="80" height="66" rx="26" fill="{HONEY}"/>'
    + t(62, 64, "TR", 24, W, F, 700) + t(150, 64, "EN", 24, W, F, 700) + t(238, 64, "BS", 24, NAVY9, F, 700))
add("F08", "sarajevo", "Sarajevo 518 m", 200, 200, 45, circle(100, 98, NAVY)
    + f'<path d="M34 132 L72 76 L96 104 L124 62 L166 132 Z" fill="{SAGE}"/><path d="M124 62 L112 80 L124 76 L134 84 Z" fill="{W}"/>'
    + t(100, 154, "SARAJEVO", 14, W, M, 700, ls=1) + t(100, 172, "↑ 518 m", 12, HONEYL, M, 700))
add("F09", "sarajevo", "Polako… derleniyor", 260, 150, 60, bubble(260, 150, SKY) + t(130, 58, "polako…", 28, NAVY9, F, 700)
    + t(130, 86, "compiling", 16, NAVY, M, 600))
add("F10", "sarajevo", "Hajde, deploy!", 260, 120, 60, rrect(260, 120, 58, SAGE) + rocket(56, 60, 56) + t(160, 70, "Hajde, deploy!", 22, W, F, 700))
add("F11", "sarajevo", "Kolay gelsin", 200, 200, 45, circle(100, 98, HONEYL) + gear(100, 80, 36, 29, 10, NAVY, 12, HONEYL)
    + t(100, 142, "kolay", 22, NAVY9, F, 700) + t(100, 166, "gelsin!", 22, HONEY, F, 700))
add("F12", "sarajevo", "Inženjer", 300, 110, 70, tag(300, 110, NAVY) + t(180, 56, "INŽENJER", 26, W, F, 700)
    + t(180, 80, "engineer · mühendis", 12, SKY, M, 600))

json.dump(S, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
print(len(S), "stickers;", {c: sum(1 for s in S if s["cat"] == c) for c in dict.fromkeys(s["cat"] for s in S)})
