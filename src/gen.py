"""IEC sticker set: ~200 original stickers drawn as SVG in the club palette (set 2 added 2026-10-29).

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
    out = f'<circle cx="{c}" cy="{c}" r="{r}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut"/>'
    out += f'<circle class="sk-pnl" cx="{c}" cy="{c}" r="{r - 10}" fill="{fill}"/>'
    if ring:
        out += f'<circle cx="{c}" cy="{c}" r="{r - 17}" fill="none" stroke="{ring}" stroke-width="2.5" stroke-dasharray="1 6" stroke-linecap="round"/>'
    return out


def rrect(w, h, rad, fill, inset=10, stroke=None):
    out = f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rad}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut"/>'
    out += f'<rect class="sk-pnl" x="{inset}" y="{inset}" width="{w - 2 * inset}" height="{h - 2 * inset}" rx="{max(rad - inset + 2, 2)}" fill="{fill}"'
    out += (f' stroke="{stroke}" stroke-width="3"/>' if stroke else "/>")
    return out


def hexagon(c, r, fill):
    def pts(rr):
        return " ".join(f"{c + rr * math.cos(math.radians(60 * i - 90)):.1f},{c + rr * math.sin(math.radians(60 * i - 90)):.1f}"
                        for i in range(6))
    return (f'<polygon points="{pts(r)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
            f'<polygon class="sk-pnl" points="{pts(r - 11)}" fill="{fill}" stroke-linejoin="round"/>')


def burst(c, r, n, fill):
    def pts(r1, r2):
        return " ".join(f"{c + (r1 if i % 2 == 0 else r2) * math.cos(math.pi * i / n):.1f},"
                        f"{c + (r1 if i % 2 == 0 else r2) * math.sin(math.pi * i / n):.1f}" for i in range(2 * n))
    return (f'<polygon points="{pts(r, r - 9)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
            f'<polygon class="sk-pnl" points="{pts(r - 10, r - 19)}" fill="{fill}" stroke-linejoin="round"/>')


def shield(w, h, fill):
    def p(i):
        return (f"M{w / 2} {i} L{w - i} {i + 14} L{w - i} {h * 0.5} Q{w - i} {h * 0.82} {w / 2} {h - i} "
                f"Q{i} {h * 0.82} {i} {h * 0.5} L{i} {i + 14} Z")
    return (f'<path d="{p(2)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
            f'<path class="sk-pnl" d="{p(12)}" fill="{fill}"/>')


def bubble(w, h, fill, tail_x=None):
    tx = tail_x or w * 0.28

    def p(i, r):
        b = h - 34
        return (f"M{i + r} {i} H{w - i - r} Q{w - i} {i} {w - i} {i + r} V{b - r} Q{w - i} {b} {w - i - r} {b} "
                f"H{tx + 22} L{tx - 6} {h - i - 4} L{tx + 2} {b} H{i + r} Q{i} {b} {i} {b - r} V{i + r} Q{i} {i} {i + r} {i} Z")
    return (f'<path d="{p(2, 26)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
            f'<path class="sk-pnl" d="{p(11, 18)}" fill="{fill}" stroke-linejoin="round"/>')


def tag(w, h, fill):
    def p(i):
        return f"M{h / 2 + i * 0.4} {i} H{w - i - 14} Q{w - i} {i} {w - i} {i + 14} V{h - i - 14} Q{w - i} {h - i} {w - i - 14} {h - i} H{h / 2 + i * 0.4} L{i} {h / 2} Z"
    return (f'<path d="{p(2)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
            f'<path class="sk-pnl" d="{p(11)}" fill="{fill}" stroke-linejoin="round"/>'
            f'<circle cx="{h / 2 + 4}" cy="{h / 2}" r="7" fill="{W}"/>')


def ticket(w, h, fill):
    def p(i, notch):
        return (f"M{i} {i} H{w - i} V{h / 2 - notch} A{notch} {notch} 0 0 0 {w - i} {h / 2 + notch} V{h - i} H{i} "
                f"V{h / 2 + notch} A{notch} {notch} 0 0 0 {i} {h / 2 - notch} Z")
    return (f'<path d="{p(2, 16)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
            f'<path class="sk-pnl" d="{p(11, 9)}" fill="{fill}"/>')


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


def ohm(cx, cy, k, color, width):
    """Omega drawn as a stroke (our fonts have no Greek)."""
    return (f'<path d="M{cx - k:.1f} {cy + k * 0.9:.1f} H{cx - k * 0.42:.1f} Q{cx - k * 1.05:.1f} {cy + k * 0.2:.1f} {cx - k * 0.9:.1f} {cy - k * 0.3:.1f} '
            f'A{k * 0.95:.1f} {k * 0.95:.1f} 0 1 1 {cx + k * 0.9:.1f} {cy - k * 0.3:.1f} Q{cx + k * 1.05:.1f} {cy + k * 0.2:.1f} {cx + k * 0.42:.1f} {cy + k * 0.9:.1f} '
            f'H{cx + k:.1f}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------------------------------------------------------- A · IEC identity

def wordmark_gear(cx, cy, s):
    return gear(cx, cy, s * 0.62, s * 0.5, 14, NAVY, s * 0.36, W) + t(cx, cy + s * 0.13, "IEC", s * 0.36, NAVY9, G, 700)


add("A01", "kimlik", "IEC dişli rozet", 200, 200, 50, hexagon(100, 98, NAVY9) + wordmark_gear(100, 92, 120)
    + t(100, 158, "ENGINEERING", 10.5, W, M, 700, ls=1.2) + t(100, 172, "CLUB", 11, HONEY, M, 700, ls=2))
add("A02", "kimlik", "IEC · Sarajevo · 2026", 200, 200, 50, circle(100, 98, SKY, NAVY4)
    + f'<path id="arcA02" d="M30 104 A70 70 0 0 1 170 104" fill="none"/>'
    + f'<text font-family="{M}" font-size="11.5" font-weight="700" fill="{NAVY}" letter-spacing="1.6"><textPath href="#arcA02" startOffset="50%" text-anchor="middle">IUS ENGINEERING CLUB</textPath></text>'
    + gear(100, 112, 34, 27, 10, NAVY, 14, SKY) + t(100, 165, "SARAJEVO · 2026", 10, NAVY9, M, 700, ls=0.8))
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
    + t(196, 66, "Ohm my God", 24, W, F, 700) + ohm(196, 85, 7, HONEY, 2.6))
add("B04", "espri", "Resistance is futile", 220, 220, 52, circle(110, 108, SKY) + resistor(110, 82, 70)
    + t(110, 140, "RESISTANCE", 18, NAVY9, F, 700) + t(110, 162, "IS FUTILE", 18, NAVY9, F, 700) + t(110, 182, "(if < 1 ohm)", 13, NAVY, M, 600))
add("B05", "espri", "Trust me, I'm an engineer", 300, 130, 72, rrect(300, 130, 24, HONEY) + gear(52, 65, 30, 24, 10, NAVY9, 11, HONEY)
    + t(178, 58, "Trust me,", 26, NAVY9, F, 700) + t(178, 90, "I'm an engineer", 21, W, F, 700))
add("B06", "espri", "I void warranties", 200, 200, 48, burst(100, 98, 14, BRICK) + wrench(100, 78, 70, W)
    + t(100, 138, "I VOID", 20, W, F, 700) + t(100, 160, "WARRANTIES", 15, CREAM, M, 700))
add("B07", "espri", "Ctrl + Z", 300, 120, 70, rrect(300, 120, 26, SKY) + keycap(28, 30, 96, "Ctrl") + t(150, 66, "+", 28, NAVY9, F, 700)
    + keycap(176, 30, 96, "Z"))
add("B08", "espri", "404: sleep not found", 220, 200, 52, rrect(220, 200, 30, NAVY9) + t(110, 92, "404", 58, HONEY, M, 700)
    + t(110, 128, "sleep", 22, W, F, 600) + t(110, 154, "not found", 22, W, F, 600) + t(172, 58, "z", 16, SKY, F, 700) + t(186, 44, "z", 12, SKY, F, 700))
add("B09", "espri", "Coffee → Code", 300, 120, 70, rrect(300, 120, 58, CREAM, stroke=HONEY) + cup(58, 62, 52)
    + t(170, 72, "coffee", 22, NAVY9, F, 600) + f'<path d="M208 65 H229 M222 58 L230 65 L222 72" fill="none" stroke="{HONEY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' + t(254, 72, "</>", 20, NAVY, M, 700))
add("B10", "espri", "Hello, World!", 260, 180, 60, rrect(260, 180, 20, PAPER)
    + terminal(22, 22, 216, 136, [("$ ./hello", SAGEL), ("Hello, World!", HONEY), ("$ _", W)]))
add("B11", "espri", "There's no place like 127.0.0.1", 220, 220, 52, circle(110, 108, SAGEL)
    + f'<path d="M70 104 L110 66 L150 104 V140 H70 Z" fill="{W}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    + f'<rect x="100" y="114" width="20" height="26" fill="{HONEY}"/>' + t(110, 162, "no place like", 15, NAVY9, F, 600)
    + t(110, 182, "127.0.0.1", 18, NAVY, M, 700))
add("B12", "espri", "git push --force", 220, 200, 52,
    f'<path d="M110 6 L214 190 H6 Z" fill="{W}" stroke="{CUT}" stroke-width="1.4" class="sk-cut" stroke-linejoin="round"/>'
    f'<path class="sk-pnl" d="M110 26 L196 180 H24 Z" fill="{HONEY}" stroke-linejoin="round"/>'
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
    + f'<circle cx="100" cy="46" r="19" fill="{NAVY}"/><circle cx="100" cy="94" r="19" fill="{NAVY}"/>'
    + f'<path d="M114 106 Q112 128 92 138" fill="none" stroke="{NAVY}" stroke-width="11" stroke-linecap="round"/>'
    + face(100, 48, 30, "confused", W) + face(100, 96, 30, "sleepy", W) + t(100, 160, "forgot me", 14, NAVY9, F, 700) + t(100, 176, "again?", 14, NAVY9, F, 700))
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
        body += t(100, 171, label, 15, NAVY9, F, 700)
    add(sid, "maskot", name, 200, 200, 48, body)


gear_mascot("C01", "Dişli · mutlu", "happy", label="hi!")
gear_mascot("C02", "Dişli · uykulu", "sleepy", t(150, 48, "z", 13, NAVY, F, 700), "5 more min", NAVY4, SKY)
gear_mascot("C03", "Dişli · kahveli", "coffee", cup(150, 128, 36), "fuelled", HONEY, CREAM)
gear_mascot("C04", "Dişli · havalı", "cool", "", "cool gear", SAGE, SAGEL)
gear_mascot("C05", "Dişli · aşık", "love", t(82, 172, "I", 15, NAVY9, F, 700) + heart(97, 166, 6) + t(121, 172, "eng", 15, NAVY9, F, 700), None, BRICK, CREAM)
gear_mascot("C06", "Dişli · şaşkın", "confused", t(146, 58, "?!", 20, BRICK, F, 700), "debugging", NAVY4, SKY)
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
    + t(100, 170, "smart chip", 15, NAVY9, F, 700))
add("C12", "maskot", "Robot · beep boop", 200, 200, 48, circle(100, 98, SAGEL) + robot(100, 100, 92, W)
    + t(100, 170, "beep boop", 16, NAVY9, F, 700))
add("C13", "maskot", "Lastik ördek", 200, 200, 48, circle(100, 98, NAVY) + duck(104, 90, 90, HONEY)
    + t(100, 168, "quack.", 18, W, F, 700))
add("C14", "maskot", "Marshmallow", 200, 200, 48, circle(100, 98, HONEYL) + marshmallow(100, 90, 96)
    + t(100, 158, "squishy but", 13, NAVY9, F, 700) + t(100, 174, "stable", 13, NAVY9, F, 700))
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
add("D12", "etiket", "Test edildi", 220, 220, 50, circle(110, 100, W) + '<g transform="translate(0 10)">' + (f'<circle cx="110" cy="100" r="78" fill="none" stroke="{SAGE}" stroke-width="5"/>'
    + check(110, 82, 40, SAGE, 10) + t(110, 136, "TESTED", 22, SAGE, F, 700) + t(110, 158, "date ____", 12, NAVY9, M, 600)) + '</g>')
label("D13", "Ortak laptop", "SHARED LAPTOP", "please log out", NAVY4)
label("D14", "Sıcak havya", "HOT! 400 °C", "soldering iron · do not touch", BRICK)
add("D15", "etiket", "Gözlük tak", 220, 220, 50, circle(110, 100, HONEY) + '<g transform="translate(0 10)">' + (f'<rect x="54" y="74" width="48" height="34" rx="14" fill="{NAVY9}"/><rect x="118" y="74" width="48" height="34" rx="14" fill="{NAVY9}"/>'
    + f'<path d="M102 88 H118" stroke="{NAVY9}" stroke-width="5"/>' + t(110, 140, "GOGGLES", 20, NAVY9, F, 700) + t(110, 160, "ON", 16, W, F, 700)) + '</g>')
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
add("E05", "etkinlik", "Prompt Wars", 220, 220, 52, circle(110, 100, BRICK) + '<g transform="translate(0 10)">' + (wizard_hat(110, 80, 70, NAVY9)
    + t(110, 146, "PROMPT", 22, W, F, 700) + t(110, 170, "WARS", 22, CREAM, F, 700)) + '</g>')
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
add("F02", "sarajevo", "Kahva & kod", 220, 220, 52, circle(110, 100, CREAM) + '<g transform="translate(0 10)">' + (dzezva(98, 86, 62)
    + t(110, 152, "kahva & kod", 20, NAVY9, F, 700) + t(110, 172, "Bosnian coffee", 10, NAVY, M, 600)) + '</g>')
add("F03", "sarajevo", "Çay & kod", 200, 200, 48, circle(100, 98, SAGEL) + tea_glass(100, 82, 76)
    + t(100, 160, "çay & kod", 20, NAVY9, F, 700))
add("F04", "sarajevo", "Hello World · 3 dil", 300, 150, 72, rrect(300, 150, 22, NAVY9)
    + t(150, 50, "Hello, World!", 20, W, M, 700) + t(150, 82, "Merhaba, Dünya!", 20, HONEY, M, 700) + t(150, 114, "Zdravo, svijete!", 20, SAGEL, M, 700))
add("F05", "sarajevo", "Ćevapi ile çalışır", 300, 120, 70, rrect(300, 120, 58, HONEY)
    + "".join(f'<rect x="{40 + i * 13}" y="{40 + (i % 2) * 6}" width="11" height="40" rx="5.5" fill="{BRICK}"/>' for i in range(5))
    + t(190, 66, "ĆEVAPI", 26, NAVY9, G, 700) + t(190, 88, "powered", 14, W, M, 700, ls=2))
add("F06", "sarajevo", "Baščaršija → Lab", 260, 200, 60, rrect(260, 200, 26, SAGEL)
    + f'<rect x="124" y="40" width="10" height="148" fill="{NAVY9}"/>'
    + f'<path d="M30 52 H186 L206 72 L186 92 H30 Z" fill="{NAVY}"/><path d="M230 108 H74 L54 128 L74 148 H230 Z" fill="{HONEY}"/>'
    + t(106, 79, "BAŠČARŠIJA", 14, W, G, 700) + t(152, 135, "IEC LAB 50 m", 15, NAVY9, F, 700))
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

# ---------------------------------------------------------------- set 2 (2026-10-29): logo, bee, cute hardware, badges, hex, jokes
# The club seal is the official PNG (assets/), never redrawn. Shapes stay scissor-friendly.

SEAL, SEAL_W = "assets/seal.png", "assets/seal-white.png"


def seal(cx, cy, d, white=False):
    return (f'<image href="{SEAL_W if white else SEAL}" x="{cx - d / 2:.1f}" y="{cy - d / 2:.1f}" '
            f'width="{d}" height="{d}"/>')


def hexs(fill, w=174, h=200):
    """Point-up hex in a tight box: at mm=44 it is the common 2 in laptop hex (44 x 51 mm)."""
    cx, cy = w / 2, h / 2

    def pts(r):
        return " ".join(f"{cx + r * math.cos(math.radians(60 * i - 90)):.1f},{cy + r * math.sin(math.radians(60 * i - 90)):.1f}"
                        for i in range(6))
    return (f'<polygon class="sk-cut" points="{pts(98)}" fill="{W}" stroke="{CUT}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<polygon class="sk-pnl" points="{pts(87)}" fill="{fill}" stroke-linejoin="round"/>')


def scallop(c, R, n, fill):
    """Rosette badge: n bumps; the panel keeps a safe disc of radius R - 10."""
    def d(r):
        pts = [(c + r * math.cos(2 * math.pi * i / n - math.pi / 2), c + r * math.sin(2 * math.pi * i / n - math.pi / 2))
               for i in range(n + 1)]
        a = 2 * r * math.sin(math.pi / n) * 0.62
        return f"M{pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(f"A{a:.1f} {a:.1f} 0 0 1 {x:.1f} {y:.1f}" for x, y in pts[1:]) + " Z"
    return (f'<path class="sk-cut" d="{d(R)}" fill="{W}" stroke="{CUT}" stroke-width="1.4"/>'
            f'<path class="sk-pnl" d="{d(R - 10)}" fill="{fill}"/>')


def honeycomb(inside, cell, color, x0, y0, x1, y1, width=1.6):
    """Hex cells that lie fully inside the region tested by inside(x, y)."""
    out, dx, dy = [], cell * math.sqrt(3), cell * 1.5
    for j in range(int((y1 - y0) / dy) + 3):
        for i in range(int((x1 - x0) / dx) + 3):
            x, y = x0 + i * dx + (dx / 2 if j % 2 else 0), y0 + j * dy
            v = [(x + cell * math.cos(math.radians(60 * k - 90)), y + cell * math.sin(math.radians(60 * k - 90))) for k in range(6)]
            if all(inside(a, b) for a, b in v):
                out.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in v)}" fill="none" stroke="{color}" stroke-width="{width}"/>')
    return "".join(out)


def in_hex(cx, cy, r):
    return lambda x, y: abs(x - cx) <= r * 0.866 and abs(y - cy) <= r - abs(x - cx) * 0.577


def in_circle(cx, cy, r):
    return lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def limb(x1, y1, x2, y2, s):
    return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{INK}" stroke-width="{s * 0.06:.1f}" stroke-linecap="round"/>'


def bee(cx, cy, s, kind="happy", wing=SKY):
    """Round honey bee. Box: x cx +- 0.5s, y cy - 0.73s .. cy + 0.59s."""
    r, sw = s / 2, s * 0.035
    o = ""
    for d in (-1, 1):
        wx, wy = cx + d * r * 0.62, cy - r * 0.78
        o += (f'<ellipse cx="{wx:.1f}" cy="{wy:.1f}" rx="{r * 0.4:.1f}" ry="{r * 0.27:.1f}" transform="rotate({-28 * d} {wx:.1f} {wy:.1f})" '
              f'fill="{wing}" stroke="{INK}" stroke-width="{sw:.1f}"/>')
        o += (f'<path d="M{cx + d * r * 0.22:.1f} {cy - r * 0.9:.1f} Q{cx + d * r * 0.26:.1f} {cy - r * 1.28:.1f} {cx + d * r * 0.5:.1f} {cy - r * 1.34:.1f}" '
              f'fill="none" stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round"/>'
              f'<circle cx="{cx + d * r * 0.5:.1f}" cy="{cy - r * 1.34:.1f}" r="{r * 0.1:.1f}" fill="{INK}"/>')
    o += (f'<path d="M{cx - r * 0.13:.1f} {cy + r * 0.95:.1f} L{cx:.1f} {cy + r * 1.17:.1f} L{cx + r * 0.13:.1f} {cy + r * 0.95:.1f} Z" '
          f'fill="{INK}" stroke-linejoin="round"/>')
    o += f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{HONEY}"/>'
    for y1, y2 in ((0.3, 0.5), (0.68, 0.84)):
        a, b = cy + r * y1, cy + r * y2
        xa, xb = r * math.sqrt(1 - y1 * y1), r * math.sqrt(1 - y2 * y2)
        o += (f'<path d="M{cx - xa:.1f} {a:.1f} H{cx + xa:.1f} A{r:.1f} {r:.1f} 0 0 1 {cx + xb:.1f} {b:.1f} H{cx - xb:.1f} '
              f'A{r:.1f} {r:.1f} 0 0 1 {cx - xa:.1f} {a:.1f} Z" fill="{NAVY9}"/>')
    o += f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{INK}" stroke-width="{sw:.1f}"/>'
    return o + face(cx, cy - r * 0.22, s * 0.6, kind)


def hardhat(cx, cy, r):
    yb, yt = cy - r * 0.62, cy - r * 1.16
    return (f'<path d="M{cx - r * 0.74:.1f} {yb:.1f} Q{cx - r * 0.74:.1f} {yt:.1f} {cx:.1f} {yt:.1f} Q{cx + r * 0.74:.1f} {yt:.1f} {cx + r * 0.74:.1f} {yb:.1f} Z" '
            f'fill="{W}" stroke="{INK}" stroke-width="{r * 0.07:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{cx:.1f} {yt + r * 0.06:.1f} V{yb:.1f}" stroke="{HONEY}" stroke-width="{r * 0.16:.1f}"/>'
            f'<rect x="{cx - r * 0.95:.1f}" y="{yb - r * 0.06:.1f}" width="{r * 1.9:.1f}" height="{r * 0.15:.1f}" rx="{r * 0.075:.1f}" '
            f'fill="{W}" stroke="{INK}" stroke-width="{r * 0.07:.1f}"/>')


def gradcap(cx, cy, r):
    top = cy - r * 1.02
    return (f'<path d="M{cx - r * 0.55:.1f} {cy - r * 0.74:.1f} Q{cx:.1f} {cy - r * 0.6:.1f} {cx + r * 0.55:.1f} {cy - r * 0.74:.1f} '
            f'V{top + r * 0.1:.1f} H{cx - r * 0.55:.1f} Z" fill="{NAVY9}"/>'
            f'<polygon points="{cx - r:.1f},{top:.1f} {cx:.1f},{top - r * 0.32:.1f} {cx + r:.1f},{top:.1f} {cx:.1f},{top + r * 0.32:.1f}" '
            f'fill="{NAVY9}" stroke="{INK}" stroke-width="{r * 0.05:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{cx:.1f} {top:.1f} L{cx + r * 0.8:.1f} {top + r * 0.1:.1f} V{top + r * 0.52:.1f}" fill="none" stroke="{HONEY}" '
            f'stroke-width="{r * 0.07:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{cx + r * 0.8:.1f}" cy="{top + r * 0.58:.1f}" r="{r * 0.1:.1f}" fill="{HONEY}"/>')


def headphones(cx, cy, r, fill=BRICK):
    return (f'<path d="M{cx - r * 0.98:.1f} {cy - r * 0.12:.1f} Q{cx - r * 1.02:.1f} {cy - r * 1.28:.1f} {cx:.1f} {cy - r * 1.24:.1f} '
            f'Q{cx + r * 1.02:.1f} {cy - r * 1.28:.1f} {cx + r * 0.98:.1f} {cy - r * 0.12:.1f}" fill="none" stroke="{INK}" '
            f'stroke-width="{r * 0.12:.1f}" stroke-linecap="round"/>'
            + "".join(f'<rect x="{cx + d * r * 0.97 - r * 0.17:.1f}" y="{cy - r * 0.44:.1f}" width="{r * 0.34:.1f}" height="{r * 0.62:.1f}" '
                      f'rx="{r * 0.15:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{r * 0.06:.1f}"/>' for d in (-1, 1)))


def helmet(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy - r * 0.12:.1f}" r="{r * 1.5:.1f}" fill="{W}" fill-opacity="0.18" stroke="{W}" stroke-width="{r * 0.1:.1f}"/>'
            f'<path d="M{cx - r * 1.05:.1f} {cy - r * 0.6:.1f} A{r * 1.2:.1f} {r * 1.2:.1f} 0 0 1 {cx - r * 0.3:.1f} {cy - r * 1.3:.1f}" '
            f'fill="none" stroke="{W}" stroke-width="{r * 0.12:.1f}" stroke-linecap="round" opacity="0.8"/>')


def partyhat(cx, cy, r):
    return (f'<path d="M{cx - r * 0.34:.1f} {cy - r * 0.86:.1f} L{cx + r * 0.12:.1f} {cy - r * 1.62:.1f} L{cx + r * 0.38:.1f} {cy - r * 0.82:.1f} Z" '
            f'fill="{BRICK}" stroke="{INK}" stroke-width="{r * 0.06:.1f}" stroke-linejoin="round"/>'
            f'<circle cx="{cx - r * 0.02:.1f}" cy="{cy - r * 1.02:.1f}" r="{r * 0.06:.1f}" fill="{W}"/>'
            f'<circle cx="{cx + r * 0.16:.1f}" cy="{cy - r * 1.24:.1f}" r="{r * 0.06:.1f}" fill="{W}"/>'
            f'<circle cx="{cx + r * 0.12:.1f}" cy="{cy - r * 1.68:.1f}" r="{r * 0.12:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{r * 0.05:.1f}"/>')


def confetti(items):
    return "".join(f'<rect x="{x - 3}" y="{y - 1.6}" width="6" height="3.2" rx="1" fill="{c}" transform="rotate({a} {x} {y})"/>'
                   for x, y, c, a in items)


def iron(x, y, s, ang, handle=BRICK):
    """Soldering iron, tip at (x, y); the handle points along ang degrees."""
    return (f'<g transform="rotate({ang} {x} {y})">'
            f'<path d="M{x} {y} L{x + s * 0.2:.1f} {y - s * 0.04:.1f} V{y + s * 0.04:.1f} Z" fill="{INK}" stroke="{INK}" stroke-width="{s * 0.02:.1f}" stroke-linejoin="round"/>'
            f'<rect x="{x + s * 0.18:.1f}" y="{y - s * 0.03:.1f}" width="{s * 0.38:.1f}" height="{s * 0.06:.1f}" fill="{NAVY4}"/>'
            f'<rect x="{x + s * 0.54:.1f}" y="{y - s * 0.085:.1f}" width="{s * 0.5:.1f}" height="{s * 0.17:.1f}" rx="{s * 0.085:.1f}" '
            f'fill="{handle}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/></g>')


def smoke(x, y, k):
    return (f'<path d="M{x} {y} q-{k * 0.5} -{k * 0.6} 0 -{k * 1.2} t0 -{k * 1.2} M{x + k * 0.9} {y - k * 0.3} q-{k * 0.5} -{k * 0.6} 0 -{k * 1.2}" '
            f'fill="none" stroke="{NAVY4}" stroke-width="{k * 0.32:.1f}" stroke-linecap="round"/>')


def magnifier(cx, cy, r, glass=W):
    return (f'<path d="M{cx + r * 0.72:.1f} {cy + r * 0.72:.1f} L{cx + r * 1.55:.1f} {cy + r * 1.55:.1f}" stroke="{INK}" stroke-width="{r * 0.34:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{glass}" fill-opacity="0.85" stroke="{INK}" stroke-width="{r * 0.16:.1f}"/>')


def book(cx, cy, s):
    o = f'<path d="M{cx - s * 0.54:.1f} {cy - s * 0.2:.1f} V{cy + s * 0.32:.1f} H{cx + s * 0.54:.1f} V{cy - s * 0.2:.1f} Z" fill="{NAVY}"/>'
    for d in (-1, 1):
        o += (f'<path d="M{cx:.1f} {cy - s * 0.2:.1f} Q{cx + d * s * 0.25:.1f} {cy - s * 0.32:.1f} {cx + d * s * 0.5:.1f} {cy - s * 0.24:.1f} '
              f'V{cy + s * 0.24:.1f} Q{cx + d * s * 0.25:.1f} {cy + s * 0.18:.1f} {cx:.1f} {cy + s * 0.28:.1f} Z" fill="{W}" stroke="{INK}" '
              f'stroke-width="{s * 0.03:.1f}" stroke-linejoin="round"/>')
        for k in range(3):
            y = cy - s * 0.12 + k * s * 0.1
            o += f'<path d="M{cx + d * s * 0.1:.1f} {y:.1f} H{cx + d * s * 0.4:.1f}" stroke="{NAVY4}" stroke-width="{s * 0.025:.1f}" stroke-linecap="round"/>'
    return o


def burek(cx, cy, s):
    pts = " ".join(f"{cx + 0.035 * s * a * math.cos(a):.1f},{cy - s * 0.02 + 0.02 * s * a * math.sin(a):.1f}" for a in [i * 0.25 for i in range(0, 58)])
    return (f'<ellipse cx="{cx}" cy="{cy + s * 0.08:.1f}" rx="{s * 0.6:.1f}" ry="{s * 0.2:.1f}" fill="{W}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            f'<ellipse cx="{cx}" cy="{cy - s * 0.02:.1f}" rx="{s * 0.5:.1f}" ry="{s * 0.3:.1f}" fill="{HONEYL}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            f'<polyline points="{pts}" fill="none" stroke="{HONEY}" stroke-width="{s * 0.045:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def sign(x, y, w, h, fill, stroke=INK):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h * 0.16:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2.6"/>'


def nut(cx, cy, s, kind="happy", fill=NAVY4, hole=PAPER):
    """Hex nut seen from above: eyes either side of the hole, smile below it."""
    pts = " ".join(f"{cx + s * 0.5 * math.cos(math.radians(60 * i)):.1f},{cy + s * 0.5 * math.sin(math.radians(60 * i)):.1f}" for i in range(6))
    return (f'<polygon points="{pts}" fill="{fill}" stroke="{INK}" stroke-width="{s * 0.035:.1f}" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{s * 0.4:.1f}" fill="none" stroke="{W}" stroke-width="{s * 0.03:.1f}" opacity="0.45"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{s * 0.13:.1f}" fill="{hole}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            + face(cx, cy + s * 0.064, s * 0.8, kind))


def screw(cx, cy, s, kind="happy", head=PAPER, shank=NAVY4):
    """Screw with a face on its dome head. Box: x cx +- 0.46s, y cy - 0.56s .. cy + 0.6s."""
    sw = s * 0.035
    o = (f'<rect x="{cx - s * 0.15:.1f}" y="{cy - s * 0.22:.1f}" width="{s * 0.3:.1f}" height="{s * 0.62:.1f}" fill="{shank}" stroke="{INK}" stroke-width="{sw:.1f}"/>'
         f'<path d="M{cx - s * 0.15:.1f} {cy + s * 0.4:.1f} L{cx:.1f} {cy + s * 0.6:.1f} L{cx + s * 0.15:.1f} {cy + s * 0.4:.1f} Z" fill="{shank}" '
         f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>')
    for k in range(5):
        y0 = cy - s * 0.1 + k * s * 0.11
        o += (f'<path d="M{cx - s * 0.15:.1f} {y0 + s * 0.05:.1f} L{cx + s * 0.15:.1f} {y0 - s * 0.03:.1f}" stroke="{W}" '
              f'stroke-width="{s * 0.028:.1f}" stroke-linecap="round"/>')
    o += (f'<path d="M{cx - s * 0.46:.1f} {cy - s * 0.18:.1f} Q{cx - s * 0.46:.1f} {cy - s * 0.56:.1f} {cx:.1f} {cy - s * 0.56:.1f} '
          f'Q{cx + s * 0.46:.1f} {cy - s * 0.56:.1f} {cx + s * 0.46:.1f} {cy - s * 0.18:.1f} Z" fill="{head}" stroke="{INK}" '
          f'stroke-width="{sw:.1f}" stroke-linejoin="round"/>')
    return o + face(cx, cy - s * 0.31, s * 0.42, kind)


def gear_face(cx, cy, s, fill, kind="happy", rot=0):
    return gear(cx, cy, s * 0.5, s * 0.4, 10, fill, rot=rot) + f'<circle cx="{cx}" cy="{cy}" r="{s * 0.33:.1f}" fill="{fill}"/>' + face(cx, cy, s * 0.5, kind)


def transistor(cx, cy, s, kind="happy"):
    o = "".join(f'<path d="M{cx + d * s * 0.17:.1f} {cy + s * 0.12:.1f} V{cy + s * 0.58:.1f}" stroke="{NAVY4}" stroke-width="{s * 0.06:.1f}" stroke-linecap="round"/>'
                for d in (-1, 0, 1))
    o += (f'<path d="M{cx - s * 0.34:.1f} {cy + s * 0.16:.1f} V{cy - s * 0.08:.1f} Q{cx - s * 0.34:.1f} {cy - s * 0.42:.1f} {cx:.1f} {cy - s * 0.42:.1f} '
          f'Q{cx + s * 0.34:.1f} {cy - s * 0.42:.1f} {cx + s * 0.34:.1f} {cy - s * 0.08:.1f} V{cy + s * 0.16:.1f} Z" fill="{NAVY9}" stroke="{INK}" '
          f'stroke-width="{s * 0.035:.1f}" stroke-linejoin="round"/>')
    return o + face(cx, cy - s * 0.08, s * 0.44, kind, W)


def diode(cx, cy, s, kind="happy"):
    return (f'<path d="M{cx - s * 0.75:.1f} {cy} H{cx + s * 0.75:.1f}" stroke="{NAVY4}" stroke-width="{s * 0.06:.1f}" stroke-linecap="round"/>'
            f'<rect x="{cx - s * 0.42:.1f}" y="{cy - s * 0.2:.1f}" width="{s * 0.84:.1f}" height="{s * 0.4:.1f}" rx="{s * 0.2:.1f}" fill="{NAVY9}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<rect x="{cx + s * 0.2:.1f}" y="{cy - s * 0.2:.1f}" width="{s * 0.09:.1f}" height="{s * 0.4:.1f}" fill="{HONEYL}"/>'
            + face(cx - s * 0.08, cy, s * 0.36, kind, W))


def knob(cx, cy, s, kind="happy"):
    o = "".join(f'<path d="M{cx + s * 0.5 * math.cos(math.radians(a)):.1f} {cy + s * 0.5 * math.sin(math.radians(a)):.1f} '
                f'L{cx + s * 0.6 * math.cos(math.radians(a)):.1f} {cy + s * 0.6 * math.sin(math.radians(a)):.1f}" stroke="{c}" '
                f'stroke-width="{s * 0.05:.1f}" stroke-linecap="round"/>'
                for a, c in [(135 + 27 * i, SAGE if i < 5 else (HONEY if i < 8 else BRICK)) for i in range(11)])
    o += gear(cx, cy, s * 0.42, s * 0.38, 18, NAVY9)
    o += f'<circle cx="{cx}" cy="{cy}" r="{s * 0.36:.1f}" fill="{NAVY}"/>'
    o += f'<circle cx="{cx + s * 0.25 * math.cos(math.radians(-50)):.1f}" cy="{cy + s * 0.25 * math.sin(math.radians(-50)):.1f}" r="{s * 0.045:.1f}" fill="{HONEY}"/>'
    return o + face(cx, cy + s * 0.04, s * 0.42, kind, W)


def devboard(cx, cy, s, kind="happy"):
    w, h = s * 1.2, s * 0.76
    o = (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{s * 0.07:.1f}" fill="{SAGE}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
         f'<rect x="{cx - w / 2 - s * 0.06:.1f}" y="{cy - s * 0.12:.1f}" width="{s * 0.2:.1f}" height="{s * 0.24:.1f}" rx="{s * 0.03:.1f}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>')
    for i in range(10):
        x = cx - w * 0.36 + i * w * 0.08
        o += (f'<rect x="{x:.1f}" y="{cy - h / 2 + s * 0.05:.1f}" width="{s * 0.05:.1f}" height="{s * 0.05:.1f}" fill="{HONEY}"/>'
              f'<rect x="{x:.1f}" y="{cy + h / 2 - s * 0.1:.1f}" width="{s * 0.05:.1f}" height="{s * 0.05:.1f}" fill="{HONEY}"/>')
    o += f'<circle cx="{cx + w * 0.38:.1f}" cy="{cy - h * 0.18:.1f}" r="{s * 0.035:.1f}" fill="{BRICK}"/>'
    o += f'<rect x="{cx - s * 0.24:.1f}" y="{cy - s * 0.2:.1f}" width="{s * 0.48:.1f}" height="{s * 0.4:.1f}" rx="{s * 0.06:.1f}" fill="{NAVY9}"/>'
    return o + face(cx, cy, s * 0.36, kind, W)


def servo(cx, cy, s, kind="happy"):
    return (f'<rect x="{cx - s * 0.62:.1f}" y="{cy - s * 0.04:.1f}" width="{s * 1.24:.1f}" height="{s * 0.1:.1f}" rx="{s * 0.04:.1f}" fill="{NAVY9}"/>'
            f'<rect x="{cx - s * 0.48:.1f}" y="{cy - s * 0.3:.1f}" width="{s * 0.96:.1f}" height="{s * 0.6:.1f}" rx="{s * 0.08:.1f}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<circle cx="{cx - s * 0.22:.1f}" cy="{cy - s * 0.36:.1f}" r="{s * 0.11:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            f'<rect x="{cx - s * 0.52:.1f}" y="{cy - s * 0.41:.1f}" width="{s * 0.6:.1f}" height="{s * 0.1:.1f}" rx="{s * 0.05:.1f}" fill="{W}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            + face(cx + s * 0.04, cy + s * 0.02, s * 0.42, kind, INK))


def multimeter(cx, cy, s, kind="happy"):
    return (f'<rect x="{cx - s * 0.36:.1f}" y="{cy - s * 0.5:.1f}" width="{s * 0.72:.1f}" height="{s:.1f}" rx="{s * 0.1:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<rect x="{cx - s * 0.26:.1f}" y="{cy - s * 0.4:.1f}" width="{s * 0.52:.1f}" height="{s * 0.34:.1f}" rx="{s * 0.05:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy + s * 0.14:.1f}" r="{s * 0.15:.1f}" fill="{NAVY9}"/>'
            f'<path d="M{cx} {cy + s * 0.14:.1f} L{cx + s * 0.08:.1f} {cy + s * 0.04:.1f}" stroke="{W}" stroke-width="{s * 0.035:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{cx - s * 0.14:.1f}" cy="{cy + s * 0.39:.1f}" r="{s * 0.045:.1f}" fill="{INK}"/><circle cx="{cx + s * 0.14:.1f}" cy="{cy + s * 0.39:.1f}" r="{s * 0.045:.1f}" fill="{BRICK}"/>'
            + face(cx, cy - s * 0.22, s * 0.36, kind))


def printer3d(cx, cy, s, kind="happy"):
    return (f'<rect x="{cx - s * 0.5:.1f}" y="{cy - s * 0.52:.1f}" width="{s:.1f}" height="{s * 0.86:.1f}" rx="{s * 0.06:.1f}" fill="none" stroke="{NAVY9}" stroke-width="{s * 0.07:.1f}"/>'
            f'<rect x="{cx - s * 0.46:.1f}" y="{cy - s * 0.32:.1f}" width="{s * 0.92:.1f}" height="{s * 0.06:.1f}" fill="{NAVY4}"/>'
            f'<path d="M{cx + s * 0.02:.1f} {cy - s * 0.36:.1f} h{s * 0.16:.1f} v{s * 0.14:.1f} l-{s * 0.08:.1f} {s * 0.08:.1f} l-{s * 0.08:.1f} -{s * 0.08:.1f} Z" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.025:.1f}" stroke-linejoin="round"/>'
            + heart(cx + s * 0.1, cy + s * 0.08, s * 0.09)
            + f'<rect x="{cx - s * 0.4:.1f}" y="{cy + s * 0.2:.1f}" width="{s * 0.8:.1f}" height="{s * 0.06:.1f}" fill="{NAVY4}"/>'
            f'<rect x="{cx - s * 0.56:.1f}" y="{cy + s * 0.32:.1f}" width="{s * 1.12:.1f}" height="{s * 0.32:.1f}" rx="{s * 0.07:.1f}" fill="{NAVY}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            + face(cx, cy + s * 0.48, s * 0.3, kind, W))


def magnet(cx, cy, s, kind="happy"):
    ro, ri = s * 0.46, s * 0.13
    top, mid = cy - s * 0.4, cy + s * 0.02
    o = (f'<path d="M{cx - ro:.1f} {top:.1f} V{mid:.1f} A{ro:.1f} {ro:.1f} 0 0 0 {cx + ro:.1f} {mid:.1f} V{top:.1f} H{cx + ri:.1f} V{mid:.1f} '
         f'A{ri:.1f} {ri:.1f} 0 0 1 {cx - ri:.1f} {mid:.1f} V{top:.1f} Z" fill="{BRICK}" stroke="{INK}" stroke-width="{s * 0.035:.1f}" stroke-linejoin="round"/>')
    for x in (cx - ro, cx + ri):
        o += f'<rect x="{x:.1f}" y="{top:.1f}" width="{ro - ri:.1f}" height="{s * 0.14:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
    return o + face(cx, mid + s * 0.28, s * 0.3, kind, W)


def atom(cx, cy, s, kind="happy"):
    o = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.5:.1f}" ry="{s * 0.18:.1f}" transform="rotate({a} {cx} {cy})" fill="none" '
                f'stroke="{NAVY}" stroke-width="{s * 0.035:.1f}"/>' for a in (0, 60, 120))
    for a in (0, 60, 120):
        x = cx + s * 0.5 * math.cos(math.radians(a))
        y = cy + s * 0.5 * math.sin(math.radians(a))
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.05:.1f}" fill="{SAGE}"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{s * 0.22:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
    return o + face(cx, cy + s * 0.01, s * 0.3, kind)


def calculator(cx, cy, s, kind="happy"):
    o = (f'<rect x="{cx - s * 0.36:.1f}" y="{cy - s * 0.5:.1f}" width="{s * 0.72:.1f}" height="{s:.1f}" rx="{s * 0.09:.1f}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
         f'<rect x="{cx - s * 0.27:.1f}" y="{cy - s * 0.41:.1f}" width="{s * 0.54:.1f}" height="{s * 0.3:.1f}" rx="{s * 0.04:.1f}" fill="{SAGEL}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>')
    for j in range(3):
        for i in range(3):
            o += (f'<rect x="{cx - s * 0.25 + i * s * 0.18:.1f}" y="{cy - s * 0.02 + j * s * 0.15:.1f}" width="{s * 0.13:.1f}" height="{s * 0.1:.1f}" '
                  f'rx="{s * 0.025:.1f}" fill="{HONEY if (i, j) == (2, 2) else W}"/>')
    return o + face(cx, cy - s * 0.26, s * 0.3, kind)


def floppy(cx, cy, s, kind="happy"):
    h = s * 0.48
    return (f'<path d="M{cx - h:.1f} {cy - h:.1f} H{cx + h * 0.7:.1f} L{cx + h:.1f} {cy - h * 0.7:.1f} V{cy + h:.1f} H{cx - h:.1f} Z" fill="{NAVY}" stroke="{INK}" stroke-width="{s * 0.035:.1f}" stroke-linejoin="round"/>'
            f'<rect x="{cx - h * 0.5:.1f}" y="{cy - h:.1f}" width="{h:.1f}" height="{h * 0.56:.1f}" fill="{NAVY4}"/>'
            f'<rect x="{cx + h * 0.12:.1f}" y="{cy - h * 0.9:.1f}" width="{h * 0.22:.1f}" height="{h * 0.38:.1f}" fill="{NAVY9}"/>'
            f'<rect x="{cx - h * 0.72:.1f}" y="{cy - h * 0.1:.1f}" width="{h * 1.44:.1f}" height="{h * 0.98:.1f}" rx="{s * 0.04:.1f}" fill="{PAPER}"/>'
            + face(cx, cy + h * 0.38, s * 0.42, kind))


def usb(cx, cy, s, kind="happy"):
    return (f'<rect x="{cx - s * 0.17:.1f}" y="{cy - s * 0.6:.1f}" width="{s * 0.34:.1f}" height="{s * 0.28:.1f}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            f'<rect x="{cx - s * 0.1:.1f}" y="{cy - s * 0.52:.1f}" width="{s * 0.06:.1f}" height="{s * 0.06:.1f}" fill="{INK}"/>'
            f'<rect x="{cx + s * 0.04:.1f}" y="{cy - s * 0.52:.1f}" width="{s * 0.06:.1f}" height="{s * 0.06:.1f}" fill="{INK}"/>'
            f'<rect x="{cx - s * 0.27:.1f}" y="{cy - s * 0.34:.1f}" width="{s * 0.54:.1f}" height="{s * 0.84:.1f}" rx="{s * 0.12:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy + s * 0.36:.1f}" r="{s * 0.05:.1f}" fill="{NAVY9}"/>'
            + face(cx, cy + s * 0.02, s * 0.4, kind))


def enter_key(cx, cy, s, kind="happy"):
    return (f'<rect x="{cx - s * 0.5:.1f}" y="{cy - s * 0.44:.1f}" width="{s:.1f}" height="{s * 0.92:.1f}" rx="{s * 0.16:.1f}" fill="{NAVY9}"/>'
            f'<rect x="{cx - s * 0.44:.1f}" y="{cy - s * 0.42:.1f}" width="{s * 0.88:.1f}" height="{s * 0.74:.1f}" rx="{s * 0.12:.1f}" fill="{W}"/>'
            + t(cx - s * 0.36, cy - s * 0.24, "enter", s * 0.13, NAVY, M, 700, "start")
            + face(cx, cy + s * 0.04, s * 0.5, kind))


def mouse_pc(cx, cy, s, kind="happy"):
    return (f'<path d="M{cx:.1f} {cy + s * 0.42:.1f} Q{cx + s * 0.1:.1f} {cy + s * 0.62:.1f} {cx + s * 0.4:.1f} {cy + s * 0.56:.1f}" fill="none" stroke="{INK}" stroke-width="{s * 0.04:.1f}" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{cx + d * s * 0.22:.1f}" cy="{cy - s * 0.38:.1f}" r="{s * 0.13:.1f}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
                      f'<circle cx="{cx + d * s * 0.22:.1f}" cy="{cy - s * 0.38:.1f}" r="{s * 0.07:.1f}" fill="{PEACH}"/>' for d in (-1, 1))
            + f'<rect x="{cx - s * 0.3:.1f}" y="{cy - s * 0.42:.1f}" width="{s * 0.6:.1f}" height="{s * 0.86:.1f}" rx="{s * 0.3:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<path d="M{cx:.1f} {cy - s * 0.42:.1f} V{cy - s * 0.14:.1f}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
            f'<rect x="{cx - s * 0.035:.1f}" y="{cy - s * 0.32:.1f}" width="{s * 0.07:.1f}" height="{s * 0.12:.1f}" rx="{s * 0.035:.1f}" fill="{BRICK}"/>'
            + face(cx, cy + s * 0.1, s * 0.38, kind))


def router(cx, cy, s, kind="happy"):
    o = "".join(f'<path d="M{cx - s * 0.22 * k:.1f} {cy - s * 0.38 - s * 0.1 * k:.1f} Q{cx:.1f} {cy - s * 0.56 - s * 0.14 * k:.1f} {cx + s * 0.22 * k:.1f} {cy - s * 0.38 - s * 0.1 * k:.1f}" '
                f'fill="none" stroke="{HONEY}" stroke-width="{s * 0.05:.1f}" stroke-linecap="round"/>' for k in (1, 2))
    o += "".join(f'<path d="M{cx + d * s * 0.36:.1f} {cy - s * 0.14:.1f} V{cy - s * 0.44:.1f}" stroke="{INK}" stroke-width="{s * 0.06:.1f}" stroke-linecap="round"/>' for d in (-1, 1))
    o += f'<rect x="{cx - s * 0.5:.1f}" y="{cy - s * 0.16:.1f}" width="{s:.1f}" height="{s * 0.5:.1f}" rx="{s * 0.12:.1f}" fill="{NAVY9}"/>'
    o += "".join(f'<circle cx="{cx - s * 0.3 + i * s * 0.12:.1f}" cy="{cy + s * 0.24:.1f}" r="{s * 0.025:.1f}" fill="{SAGE}"/>' for i in range(3))
    return o + face(cx + s * 0.12, cy + s * 0.06, s * 0.36, kind, W)


def rover(cx, cy, s, kind="happy"):
    o = (f'<path d="M{cx + s * 0.18:.1f} {cy - s * 0.12:.1f} V{cy - s * 0.36:.1f}" stroke="{INK}" stroke-width="{s * 0.05:.1f}"/>'
         f'<rect x="{cx - s * 0.04:.1f}" y="{cy - s * 0.6:.1f}" width="{s * 0.44:.1f}" height="{s * 0.26:.1f}" rx="{s * 0.06:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
         + face(cx + s * 0.18, cy - s * 0.47, s * 0.26, kind)
         + f'<rect x="{cx - s * 0.56:.1f}" y="{cy - s * 0.24:.1f}" width="{s * 0.5:.1f}" height="{s * 0.1:.1f}" fill="{SKY}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
         f'<rect x="{cx - s * 0.5:.1f}" y="{cy - s * 0.14:.1f}" width="{s:.1f}" height="{s * 0.32:.1f}" rx="{s * 0.07:.1f}" fill="{NAVY4}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>')
    for x in (-0.36, 0, 0.36):
        o += (f'<circle cx="{cx + s * x:.1f}" cy="{cy + s * 0.3:.1f}" r="{s * 0.13:.1f}" fill="{INK}"/>'
              f'<circle cx="{cx + s * x:.1f}" cy="{cy + s * 0.3:.1f}" r="{s * 0.05:.1f}" fill="{NAVY4}"/>')
    return o


def drone(cx, cy, s, kind="happy"):
    o = ""
    for d in (-1, 1):
        o += f'<path d="M{cx:.1f} {cy:.1f} L{cx + d * s * 0.42:.1f} {cy - s * 0.16:.1f}" stroke="{NAVY9}" stroke-width="{s * 0.06:.1f}" stroke-linecap="round"/>'
        o += f'<ellipse cx="{cx + d * s * 0.42:.1f}" cy="{cy - s * 0.2:.1f}" rx="{s * 0.2:.1f}" ry="{s * 0.045:.1f}" fill="{SKY}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
        o += f'<path d="M{cx + d * s * 0.22:.1f} {cy + s * 0.18:.1f} l{d * s * 0.08:.1f} {s * 0.12:.1f}" stroke="{INK}" stroke-width="{s * 0.04:.1f}" stroke-linecap="round"/>'
    o += f'<rect x="{cx - s * 0.26:.1f}" y="{cy - s * 0.12:.1f}" width="{s * 0.52:.1f}" height="{s * 0.32:.1f}" rx="{s * 0.12:.1f}" fill="{NAVY}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
    return o + face(cx, cy + s * 0.04, s * 0.3, kind, W)


def fat_bolt(x, y, s, kind="happy"):
    pts = [(0.62, 0), (0.08, 0.58), (0.42, 0.58), (0.3, 1.0), (0.92, 0.38), (0.56, 0.38), (0.74, 0)]
    o = (f'<polygon points="{" ".join(f"{x + a * s:.1f},{y + b * s:.1f}" for a, b in pts)}" fill="{HONEY}" stroke="{INK}" '
         f'stroke-width="{s * 0.035:.1f}" stroke-linejoin="round"/>')
    return o + face(x + s * 0.45, y + s * 0.44, s * 0.26, kind)


def cookie(cx, cy, r, bite_fill, kind="shock"):
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{HONEY}" stroke="{INK}" stroke-width="{r * 0.05:.1f}"/>'
    for a, k in ((-55, 0.3), (-25, 0.24), (-80, 0.22)):
        o += f'<circle cx="{cx + r * math.cos(math.radians(a)):.1f}" cy="{cy + r * math.sin(math.radians(a)):.1f}" r="{r * k:.1f}" fill="{bite_fill}"/>'
    for dx, dy, a in ((-0.55, -0.15, 20), (-0.25, 0.55, -30), (0.45, 0.42, 45), (0.6, 0.1, 10), (-0.5, 0.3, 60)):
        o += f'<rect x="{cx + r * dx - r * 0.07:.1f}" y="{cy + r * dy - r * 0.05:.1f}" width="{r * 0.14:.1f}" height="{r * 0.1:.1f}" rx="{r * 0.03:.1f}" fill="{NAVY9}" transform="rotate({a} {cx + r * dx:.1f} {cy + r * dy:.1f})"/>'
    return o + face(cx - r * 0.05, cy + r * 0.05, r * 0.9, kind)


def glyph(kind, cx, cy, k, color, width):
    """Hand-drawn pi, lambda and sigma (no Greek in our fonts)."""
    d = {"pi": f"M{cx - k} {cy - k * 0.7} Q{cx} {cy - k * 0.95} {cx + k} {cy - k * 0.78} M{cx - k * 0.45} {cy - k * 0.78} Q{cx - k * 0.45} {cy + k * 0.3} {cx - k * 0.75} {cy + k * 0.95} "
                f"M{cx + k * 0.42} {cy - k * 0.8} Q{cx + k * 0.35} {cy + k * 0.6} {cx + k * 0.85} {cy + k * 0.85}",
         "lambda": f"M{cx - k * 0.7} {cy - k} Q{cx - k * 0.1} {cy - k * 1.05} {cx + k * 0.1} {cy - k * 0.4} L{cx + k * 0.75} {cy + k} M{cx + k * 0.12} {cy - k * 0.3} L{cx - k * 0.7} {cy + k}",
         "sigma": f"M{cx + k * 0.8} {cy - k * 0.95} H{cx - k * 0.75} L{cx + k * 0.15} {cy} L{cx - k * 0.75} {cy + k * 0.95} H{cx + k * 0.8}"}[kind]
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def owl(cx, cy, s):
    o = (f'<path d="M{cx - s * 0.36:.1f} {cy - s * 0.3:.1f} L{cx - s * 0.3:.1f} {cy - s * 0.52:.1f} L{cx - s * 0.12:.1f} {cy - s * 0.36:.1f} Z '
         f'M{cx + s * 0.36:.1f} {cy - s * 0.3:.1f} L{cx + s * 0.3:.1f} {cy - s * 0.52:.1f} L{cx + s * 0.12:.1f} {cy - s * 0.36:.1f} Z" fill="{NAVY4}" stroke-linejoin="round"/>'
         f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.4:.1f}" ry="{s * 0.44:.1f}" fill="{NAVY4}"/>'
         f'<ellipse cx="{cx}" cy="{cy + s * 0.16:.1f}" rx="{s * 0.24:.1f}" ry="{s * 0.22:.1f}" fill="{SKY}"/>')
    for d in (-1, 1):
        o += (f'<circle cx="{cx + d * s * 0.17:.1f}" cy="{cy - s * 0.12:.1f}" r="{s * 0.15:.1f}" fill="{W}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
              f'<circle cx="{cx + d * s * 0.15:.1f}" cy="{cy - s * 0.11:.1f}" r="{s * 0.075:.1f}" fill="{INK}"/>'
              f'<circle cx="{cx + d * s * 0.13:.1f}" cy="{cy - s * 0.14:.1f}" r="{s * 0.025:.1f}" fill="{W}"/>')
    return o + f'<path d="M{cx - s * 0.06:.1f} {cy + s * 0.02:.1f} L{cx + s * 0.06:.1f} {cy + s * 0.02:.1f} L{cx:.1f} {cy + s * 0.11:.1f} Z" fill="{HONEY}"/>'


def bird(cx, cy, s):
    o = "".join(f'<path d="M{cx + s * 0.32 + s * 0.2 * math.cos(math.radians(a)):.1f} {cy - s * 0.3 + s * 0.2 * math.sin(math.radians(a)):.1f} '
                f'l{s * 0.08 * math.cos(math.radians(a)):.1f} {s * 0.08 * math.sin(math.radians(a)):.1f}" stroke="{HONEYL}" stroke-width="{s * 0.04:.1f}" stroke-linecap="round"/>'
                for a in range(-180, 1, 45))
    o += f'<circle cx="{cx + s * 0.32:.1f}" cy="{cy - s * 0.3:.1f}" r="{s * 0.14:.1f}" fill="{HONEYL}"/>'
    o += (f'<ellipse cx="{cx - s * 0.04:.1f}" cy="{cy + s * 0.06:.1f}" rx="{s * 0.36:.1f}" ry="{s * 0.32:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
          f'<path d="M{cx - s * 0.2:.1f} {cy + s * 0.08:.1f} q{s * 0.18:.1f} {s * 0.2:.1f} {s * 0.34:.1f} 0" fill="{HONEYL}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
          f'<path d="M{cx + s * 0.3:.1f} {cy - s * 0.02:.1f} l{s * 0.16:.1f} {s * 0.05:.1f} l-{s * 0.16:.1f} {s * 0.06:.1f} Z" fill="{BRICK}"/>'
          f'<circle cx="{cx + s * 0.14:.1f}" cy="{cy - s * 0.06:.1f}" r="{s * 0.045:.1f}" fill="{INK}"/>')
    return o


def flag_checkered(cx, cy, s):
    o = f'<path d="M{cx - s * 0.36:.1f} {cy + s * 0.5:.1f} V{cy - s * 0.48:.1f}" stroke="{INK}" stroke-width="{s * 0.06:.1f}" stroke-linecap="round"/>'
    for j in range(3):
        for i in range(4):
            o += (f'<rect x="{cx - s * 0.33 + i * s * 0.17:.1f}" y="{cy - s * 0.46 + j * s * 0.17:.1f}" width="{s * 0.17:.1f}" height="{s * 0.17:.1f}" '
                  f'fill="{INK if (i + j) % 2 == 0 else W}"/>')
    return o + f'<rect x="{cx - s * 0.33:.1f}" y="{cy - s * 0.46:.1f}" width="{s * 0.68:.1f}" height="{s * 0.51:.1f}" fill="none" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'


def clock(cx, cy, r):
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{W}" stroke="{INK}" stroke-width="{r * 0.1:.1f}"/>'
    o += "".join(f'<path d="M{cx + r * 0.72 * math.cos(math.radians(a)):.1f} {cy + r * 0.72 * math.sin(math.radians(a)):.1f} '
                 f'L{cx + r * 0.84 * math.cos(math.radians(a)):.1f} {cy + r * 0.84 * math.sin(math.radians(a)):.1f}" stroke="{INK}" stroke-width="{r * 0.07:.1f}" stroke-linecap="round"/>'
                 for a in range(0, 360, 30))
    return o + (f'<path d="M{cx} {cy} V{cy - r * 0.55:.1f} M{cx} {cy} L{cx + r * 0.4:.1f} {cy + r * 0.18:.1f}" stroke="{BRICK}" stroke-width="{r * 0.1:.1f}" stroke-linecap="round"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r * 0.08:.1f}" fill="{INK}"/>')


def goggles(cx, cy, s):
    return (f'<path d="M{cx - s * 0.55:.1f} {cy:.1f} H{cx + s * 0.55:.1f}" stroke="{NAVY9}" stroke-width="{s * 0.1:.1f}" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{cx + d * s * 0.24:.1f}" cy="{cy}" r="{s * 0.2:.1f}" fill="{SKY}" stroke="{INK}" stroke-width="{s * 0.05:.1f}"/>'
                      f'<path d="M{cx + d * s * 0.24 - s * 0.1:.1f} {cy - s * 0.06:.1f} q{s * 0.05:.1f} -{s * 0.07:.1f} {s * 0.12:.1f} -{s * 0.06:.1f}" fill="none" stroke="{W}" stroke-width="{s * 0.035:.1f}" stroke-linecap="round"/>'
                      for d in (-1, 1)))


def cursor(x, y, s, fill):
    return (f'<path d="M{x} {y} L{x:.1f} {y + s:.1f} L{x + s * 0.28:.1f} {y + s * 0.74:.1f} L{x + s * 0.46:.1f} {y + s * 1.08:.1f} L{x + s * 0.6:.1f} {y + s:.1f} '
            f'L{x + s * 0.42:.1f} {y + s * 0.68:.1f} L{x + s * 0.76:.1f} {y + s * 0.66:.1f} Z" fill="{fill}" stroke="{INK}" stroke-width="{s * 0.06:.1f}" stroke-linejoin="round"/>')


def pcb_icon(cx, cy, s):
    o = f'<rect x="{cx - s * 0.5:.1f}" y="{cy - s * 0.36:.1f}" width="{s:.1f}" height="{s * 0.72:.1f}" rx="{s * 0.08:.1f}" fill="{SAGE}" stroke="{INK}" stroke-width="{s * 0.04:.1f}"/>'
    o += (f'<path d="M{cx - s * 0.36:.1f} {cy - s * 0.2:.1f} H{cx - s * 0.16:.1f} M{cx - s * 0.36:.1f} {cy + s * 0.2:.1f} H{cx - s * 0.2:.1f} V{cy + s * 0.06:.1f} '
          f'M{cx + s * 0.16:.1f} {cy:.1f} H{cx + s * 0.36:.1f} M{cx + s * 0.16:.1f} {cy - s * 0.18:.1f} H{cx + s * 0.3:.1f} V{cy - s * 0.24:.1f}" stroke="{HONEYL}" stroke-width="{s * 0.04:.1f}" stroke-linecap="round" fill="none"/>')
    o += "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.04:.1f}" fill="{HONEY}"/>'
                 for x, y in ((cx - s * 0.38, cy - s * 0.2), (cx - s * 0.38, cy + s * 0.2), (cx + s * 0.38, cy), (cx + s * 0.3, cy - s * 0.26)))
    return o + f'<rect x="{cx - s * 0.16:.1f}" y="{cy - s * 0.16:.1f}" width="{s * 0.32:.1f}" height="{s * 0.32:.1f}" rx="{s * 0.04:.1f}" fill="{NAVY9}"/>'


def power_icon(cx, cy, r, color=W):
    return (f'<path d="M{cx - r * 0.62:.1f} {cy - r * 0.6:.1f} A{r * 0.88:.1f} {r * 0.88:.1f} 0 1 0 {cx + r * 0.62:.1f} {cy - r * 0.6:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="{r * 0.2:.1f}" stroke-linecap="round"/>'
            f'<path d="M{cx} {cy - r * 1.02:.1f} V{cy - r * 0.2:.1f}" stroke="{color}" stroke-width="{r * 0.2:.1f}" stroke-linecap="round"/>')


def honey_jar(cx, cy, s):
    return (f'<rect x="{cx - s * 0.36:.1f}" y="{cy - s * 0.3:.1f}" width="{s * 0.72:.1f}" height="{s * 0.78:.1f}" rx="{s * 0.16:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<rect x="{cx - s * 0.4:.1f}" y="{cy - s * 0.46:.1f}" width="{s * 0.8:.1f}" height="{s * 0.18:.1f}" rx="{s * 0.06:.1f}" fill="{NAVY}" stroke="{INK}" stroke-width="{s * 0.035:.1f}"/>'
            f'<path d="M{cx - s * 0.12:.1f} {cy - s * 0.29:.1f} v{s * 0.1:.1f} a{s * 0.04:.1f} {s * 0.04:.1f} 0 0 0 {s * 0.08:.1f} 0 v-{s * 0.1:.1f} Z" fill="{HONEY}"/>'
            f'<rect x="{cx - s * 0.26:.1f}" y="{cy - s * 0.02:.1f}" width="{s * 0.52:.1f}" height="{s * 0.3:.1f}" rx="{s * 0.05:.1f}" fill="{PAPER}"/>'
            + t(cx, cy + s * 0.18, "</>", s * 0.17, NAVY, M, 700))


def git_graph(cx, cy, s, color=W, node=HONEY):
    return (f'<path d="M{cx - s * 0.2:.1f} {cy + s * 0.5:.1f} V{cy - s * 0.5:.1f} M{cx - s * 0.2:.1f} {cy + s * 0.22:.1f} Q{cx - s * 0.2:.1f} {cy - s * 0.04:.1f} {cx + s * 0.22:.1f} {cy - s * 0.12:.1f} V{cy - s * 0.32:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{s * 0.08:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.1:.1f}" fill="{f}" stroke="{color}" stroke-width="{s * 0.05:.1f}"/>'
                      for x, y, f in ((cx - s * 0.2, cy + s * 0.36, node), (cx - s * 0.2, cy - s * 0.36, node), (cx + s * 0.22, cy - s * 0.36, BRICK))))


def mountains(x0, y0, w, h):
    return (f'<path d="M{x0} {y0 + h} L{x0 + w * 0.28} {y0 + h * 0.3} L{x0 + w * 0.45} {y0 + h * 0.62} L{x0 + w * 0.66} {y0} L{x0 + w} {y0 + h} Z" fill="{SAGE}"/>'
            f'<path d="M{x0 + w * 0.66} {y0} L{x0 + w * 0.58} {y0 + h * 0.22} L{x0 + w * 0.66} {y0 + h * 0.17} L{x0 + w * 0.73} {y0 + h * 0.24} Z" fill="{W}"/>')


def proton(cx, cy, r, kind="happy"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BRICK}" stroke="{INK}" stroke-width="{r * 0.06:.1f}"/>'
            f'<circle cx="{cx + r * 0.72:.1f}" cy="{cy - r * 0.72:.1f}" r="{r * 0.3:.1f}" fill="{W}" stroke="{INK}" stroke-width="{r * 0.05:.1f}"/>'
            f'<path d="M{cx + r * 0.58:.1f} {cy - r * 0.72:.1f} H{cx + r * 0.86:.1f} M{cx + r * 0.72:.1f} {cy - r * 0.86:.1f} V{cy - r * 0.58:.1f}" stroke="{BRICK}" stroke-width="{r * 0.09:.1f}" stroke-linecap="round"/>'
            + face(cx, cy + r * 0.04, r * 1.2, kind, W))


def house_ohm(cx, cy, s):
    return (f'<rect x="{cx - s * 0.36:.1f}" y="{cy - s * 0.06:.1f}" width="{s * 0.72:.1f}" height="{s * 0.5:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{s * 0.03:.1f}"/>'
            f'<rect x="{cx + s * 0.18:.1f}" y="{cy - s * 0.46:.1f}" width="{s * 0.1:.1f}" height="{s * 0.24:.1f}" fill="{BRICK}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
            f'<path d="M{cx - s * 0.5:.1f} {cy - s * 0.04:.1f} L{cx:.1f} {cy - s * 0.5:.1f} L{cx + s * 0.5:.1f} {cy - s * 0.04:.1f} Z" fill="{NAVY}" stroke="{INK}" stroke-width="{s * 0.03:.1f}" stroke-linejoin="round"/>'
            + ohm(cx, cy - s * 0.18, s * 0.1, W, s * 0.035)
            + f'<rect x="{cx - s * 0.08:.1f}" y="{cy + s * 0.18:.1f}" width="{s * 0.16:.1f}" height="{s * 0.26:.1f}" rx="{s * 0.06:.1f}" fill="{HONEY}" stroke="{INK}" stroke-width="{s * 0.025:.1f}"/>'
            f'<rect x="{cx - s * 0.28:.1f}" y="{cy + s * 0.06:.1f}" width="{s * 0.14:.1f}" height="{s * 0.12:.1f}" fill="{SKY}" stroke="{INK}" stroke-width="{s * 0.02:.1f}"/>'
            f'<rect x="{cx + s * 0.14:.1f}" y="{cy + s * 0.06:.1f}" width="{s * 0.14:.1f}" height="{s * 0.12:.1f}" fill="{SKY}" stroke="{INK}" stroke-width="{s * 0.02:.1f}"/>')


def bread(cx, cy, s):
    o = (f'<path d="M{cx - s * 0.5:.1f} {cy + s * 0.3:.1f} V{cy - s * 0.08:.1f} Q{cx - s * 0.62:.1f} {cy - s * 0.36:.1f} {cx - s * 0.3:.1f} {cy - s * 0.38:.1f} '
         f'H{cx + s * 0.3:.1f} Q{cx + s * 0.62:.1f} {cy - s * 0.36:.1f} {cx + s * 0.5:.1f} {cy - s * 0.08:.1f} V{cy + s * 0.3:.1f} Z" fill="{HONEYL}" stroke="{HONEY}" stroke-width="{s * 0.06:.1f}" stroke-linejoin="round"/>'
         f'<path d="M{cx - s * 0.4:.1f} {cy - s * 0.16:.1f} H{cx + s * 0.4:.1f}" stroke="{BRICK}" stroke-width="{s * 0.02:.1f}"/>'
         f'<path d="M{cx - s * 0.4:.1f} {cy + s * 0.22:.1f} H{cx + s * 0.4:.1f}" stroke="{NAVY}" stroke-width="{s * 0.02:.1f}"/>')
    for j in range(4):
        for i in range(9):
            o += f'<circle cx="{cx - s * 0.36 + i * s * 0.09:.1f}" cy="{cy - s * 0.08 + j * s * 0.08:.1f}" r="{s * 0.017:.1f}" fill="{INK}" opacity="0.55"/>'
    return o

# ---------------------------------------------------------------- G · with the club seal

add("G01", "logolu", "Mühür · klasik", 200, 200, 50, circle(100, 98, NAVY) + seal(100, 100, 168))
add("G02", "logolu", "Mühür · beyaz", 200, 200, 50, circle(100, 98, SAGE) + seal(100, 100, 160, True))
add("G03", "logolu", "Mühür · bal halkası", 200, 200, 50, circle(100, 98, HONEY, HONEYL) + seal(100, 100, 148))
add("G04", "logolu", "Mühür · MEMBER", 200, 236, 48, rrect(200, 236, 30, SKY) + seal(100, 92, 150)
    + f'<rect x="34" y="178" width="132" height="36" rx="18" fill="{NAVY}"/>' + t(100, 203, "MEMBER", 19, W, F, 700, ls=2))
add("G05", "logolu", "Mühür · laptop bandı", 320, 120, 75, rrect(320, 120, 22, NAVY) + seal(64, 60, 90)
    + t(122, 52, "IUS ENGINEERING", 19, W, G, 700, "start") + t(122, 76, "CLUB", 19, HONEY, G, 700, "start")
    + t(122, 96, "SARAJEVO · EST. 2026", 10.5, SKY, M, 600, "start", ls=1))
add("G06", "logolu", "Mühür · hex", 174, 200, 44, hexs(NAVY) + seal(87, 100, 140, True))
add("G07", "logolu", "I love IEC", 300, 120, 70, rrect(300, 120, 60, PAPER, stroke=NAVY) + t(60, 78, "I", 46, NAVY9, F, 700)
    + heart(114, 62, 20) + seal(222, 60, 88))
add("G08", "logolu", "Mühür · rozet", 220, 220, 50, scallop(110, 96, 18, SAGE) + seal(110, 110, 150))
add("G09", "logolu", "Mühür · dişli", 220, 220, 52, circle(110, 108, NAVY9) + gear(110, 110, 94, 84, 20, HONEY, 78, NAVY9)
    + seal(110, 110, 148))
add("G10", "logolu", "Mühür · kurucu üye", 220, 220, 52, burst(110, 108, 18, HONEY) + seal(110, 92, 118)
    + t(110, 172, "FOUNDING", 16, NAVY9, F, 700) + t(110, 190, "2026", 12, W, M, 700, ls=1))
add("G11", "logolu", "Robot · logolu tabela", 220, 250, 50, rrect(220, 250, 30, SKY)
    + limb(86, 108, 56, 178, 80) + limb(134, 108, 164, 178, 80) + robot(110, 80, 78) + seal(110, 182, 104)
    + f'<circle cx="55" cy="180" r="6" fill="{INK}"/><circle cx="165" cy="180" r="6" fill="{INK}"/>')
add("G12", "logolu", "Mühür · şişe bandı", 130, 300, 32, rrect(130, 300, 30, NAVY) + seal(65, 70, 100, True)
    + t(65, 162, "BUILD", 22, W, F, 700) + t(65, 196, "BREAK", 22, HONEY, F, 700) + t(65, 230, "LEARN", 22, SKY, F, 700)
    + t(65, 268, "IEC · 2026", 10, SKY, M, 600, ls=1))
add("G13", "logolu", "Laba geldim damgası", 280, 180, 66, rrect(280, 180, 16, CREAM)
    + f'<rect x="18" y="18" width="244" height="144" rx="10" fill="none" stroke="{BRICK}" stroke-width="2.4" stroke-dasharray="7 5"/>'
    + seal(80, 90, 100) + t(206, 76, "VISITED", 22, BRICK, G, 700) + t(206, 104, "IEC LAB", 22, NAVY9, G, 700)
    + t(206, 128, "SARAJEVO · 2026", 10, NAVY, M, 600, ls=0.5))
add("G14", "logolu", "Mühür · mini", 120, 120, 30, circle(60, 58, NAVY) + seal(60, 60, 92))

# ---------------------------------------------------------------- I · the IEC bee

add("I01", "ari", "Arı · merhaba", 220, 220, 50, circle(110, 108, SKY) + limb(140, 100, 166, 70, 84) + bee(110, 94, 84)
    + f'<path d="M172 58 q5 6 0 12 M179 53 q8 8 0 19" fill="none" stroke="{NAVY4}" stroke-width="3" stroke-linecap="round"/>'
    + t(110, 180, "bzz, hi!", 20, NAVY9, F, 700))
add("I02", "ari", "Arı · kodluyor", 240, 220, 55, rrect(240, 220, 30, CREAM) + bee(120, 86, 80)
    + f'<rect x="66" y="104" width="108" height="70" rx="8" fill="{NAVY4}" stroke="{INK}" stroke-width="2.6"/>' + seal(120, 139, 44)
    + f'<rect x="54" y="172" width="132" height="10" rx="5" fill="{NAVY9}"/>' + limb(90, 100, 78, 108, 80) + limb(150, 100, 162, 108, 80)
    + t(120, 199, "coding...", 18, NAVY9, F, 700))
add("I03", "ari", "Arı · lehimliyor", 220, 220, 50, circle(110, 108, SAGEL) + bee(96, 92, 80) + iron(166, 140, 50, 225)
    + limb(128, 104, 142, 116, 80) + smoke(171, 131, 6) + t(110, 182, "solder time", 18, NAVY9, F, 700))
add("I04", "ari", "Arı · uykuda", 220, 220, 50, circle(110, 108, NAVY) + bee(104, 98, 84, "sleepy")
    + t(150, 92, "z", 10, HONEYL, F, 700) + t(158, 80, "z", 13, HONEYL, F, 700) + t(170, 64, "z", 17, HONEYL, F, 700)
    + t(110, 180, "sleep mode", 13, HONEYL, M, 700, ls=1))
add("I05", "ari", "Arı · kahve", 220, 220, 50, circle(110, 108, CREAM) + bee(110, 88, 78) + cup(104, 134, 40)
    + limb(80, 112, 90, 128, 78) + limb(140, 112, 124, 126, 78) + t(110, 186, "kahva first", 17, NAVY9, F, 700))
add("I06", "ari", "Arı · baret", 220, 220, 50, circle(110, 108, HONEYL) + bee(110, 96, 84) + hardhat(110, 96, 42)
    + t(110, 180, "builder bee", 18, NAVY9, F, 700))
add("I07", "ari", "Arı · mezun", 220, 220, 50, circle(110, 108, SKY) + bee(110, 98, 80) + gradcap(110, 98, 40)
    + t(110, 180, "Bee.Sc.", 22, NAVY9, F, 700))
add("I08", "ari", "Arı · kupa", 220, 220, 50, circle(110, 108, NAVY9)
    + confetti([(60, 70, HONEY, 20), (158, 62, SKY, -30), (66, 128, BRICK, 45), (156, 124, SAGE, 10), (140, 44, W, 60), (78, 44, HONEYL, -20)])
    + bee(110, 86, 74) + trophy(110, 138, 40) + limb(82, 112, 92, 128, 74) + limb(138, 112, 128, 128, 74)
    + t(110, 186, "winner", 18, HONEY, F, 700))
add("I09", "ari", "Arı · kalp", 220, 220, 50, circle(110, 108, SKY) + bee(110, 90, 80) + heart(110, 134, 15)
    + limb(80, 112, 98, 130, 80) + limb(140, 112, 122, 130, 80) + t(110, 182, "bee kind", 19, NAVY9, F, 700))
add("I10", "ari", "Arı · astronot", 220, 220, 50, circle(110, 108, NAVY9)
    + star(54, 70, 5, W) + star(166, 82, 4, HONEYL) + star(62, 140, 3.5, HONEYL) + star(160, 146, 4.5, W)
    + bee(110, 100, 72) + helmet(110, 100, 36) + t(110, 184, "space bee", 13, W, M, 700, ls=1))
add("I11", "ari", "Arı · dedektif", 220, 220, 50, circle(110, 108, HONEYL) + bee(94, 90, 76) + magnifier(148, 118, 20)
    + bug(148, 119, 20) + f'<circle cx="148" cy="118" r="20" fill="none" stroke="{INK}" stroke-width="3.2"/>'
    + t(110, 182, "found it!", 19, NAVY9, F, 700))
add("I12", "ari", "Arı · tamirci", 220, 220, 50, circle(110, 108, SAGEL) + bee(100, 92, 78)
    + f'<g transform="translate(304 0) scale(-1 1)">{wrench(152, 120, 50, NAVY4)}</g>' + limb(126, 112, 134, 130, 78)
    + t(110, 182, "fixed it!", 19, NAVY9, F, 700))
add("I13", "ari", "Arı · parti", 220, 220, 50, circle(110, 108, SKY)
    + confetti([(56, 84, HONEY, 30), (164, 92, BRICK, -20), (62, 132, SAGE, 70), (158, 136, NAVY, 15), (150, 52, HONEY, -45)])
    + bee(110, 98, 80) + partyhat(110, 98, 40) + t(110, 182, "ship it!", 20, NAVY9, F, 700))
add("I14", "ari", "Arı · kitap", 220, 220, 50, circle(110, 108, CREAM) + bee(110, 86, 76) + book(110, 136, 64)
    + t(110, 186, "exam mode", 17, NAVY9, F, 700))
add("I15", "ari", "Arı · odak modu", 220, 220, 50, circle(110, 108, NAVY) + bee(110, 98, 80) + headphones(110, 98, 40)
    + "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{HONEYL}"/><path d="M{x + 4} {y} V{y - 16} q6 2 8 9" fill="none" '
              f'stroke="{HONEYL}" stroke-width="2.6" stroke-linecap="round"/>' for x, y in ((48, 92), (160, 72)))
    + t(110, 182, "focus mode", 13, HONEYL, M, 700, ls=1))
add("I16", "ari", "Arı · LGTM", 240, 180, 58, rrect(240, 180, 28, SAGEL) + bee(70, 90, 74) + limb(100, 100, 126, 92, 74)
    + sign(124, 46, 98, 76, W) + t(173, 88, "LGTM", 26, SAGE, G, 700) + check(173, 104, 16, NAVY, 4)
    + t(120, 158, "looks good to me", 10, NAVY, M, 600, ls=0.5))
add("I17", "ari", "Arı · kovan zihni", 260, 170, 62, rrect(260, 170, 30, NAVY9)
    + honeycomb(lambda x, y: 20 <= x <= 240 and 20 <= y <= 150, 11, NAVY, 10, 10, 250, 160, 1.4)
    + bee(70, 88, 46) + bee(130, 78, 46, "wink") + bee(190, 88, 46) + t(130, 146, "hive mind", 20, HONEY, F, 700))
add("I18", "ari", "Arı · burek molası", 220, 220, 50, circle(110, 108, CREAM) + bee(110, 86, 76, "love") + burek(110, 138, 60)
    + t(110, 186, "burek break", 17, NAVY9, F, 700))
add("I19", "ari", "Arı · Saraybosna", 240, 220, 55, rrect(240, 220, 30, SKY) + sebilj(176, 130, 78) + bee(78, 102, 72)
    + t(120, 198, "Sarajevo bee", 19, NAVY9, F, 700))
add("I20", "ari", "Arı · IEC logosu", 220, 220, 50, circle(110, 108, HONEYL) + bee(110, 70, 62) + seal(110, 138, 84))

# ---------------------------------------------------------------- H · cute hardware

add("H01", "tatli", "Vida · mutlu", 220, 220, 48, circle(110, 108, SKY) + screw(110, 104, 112))
add("H02", "tatli", "Somun · aşık", 220, 220, 48, circle(110, 108, SAGEL) + nut(110, 106, 110, "love", hole=SAGEL))
add("H03", "tatli", "Vida & somun · tam uyum", 260, 200, 60, rrect(260, 200, 28, HONEYL) + screw(78, 92, 96)
    + nut(184, 104, 92, "wink", hole=HONEYL) + heart(131, 70, 11) + t(130, 182, "perfect fit", 20, NAVY9, F, 700))
add("H04", "tatli", "Dişliler · iyi kavrar", 270, 200, 62, rrect(270, 200, 28, SKY) + gear_face(92, 92, 116, HONEY)
    + gear_face(188, 98, 100, NAVY4, "wink", 0.16) + t(135, 180, "we mesh well", 18, NAVY9, F, 700))
add("H05", "tatli", "Transistör · açık", 220, 220, 48, circle(110, 108, HONEYL) + transistor(110, 92, 110)
    + t(110, 182, "switched on", 18, NAVY9, F, 700))
add("H06", "tatli", "Diyot · tek yön", 300, 130, 70, rrect(300, 130, 26, SKY) + diode(98, 65, 100)
    + t(232, 58, "one way", 21, NAVY9, F, 700) + t(232, 84, "only", 21, BRICK, F, 700)
    + f'<path d="M208 102 H254 M245 94 L255 102 L245 110" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
add("H07", "tatli", "Potansiyometre · aç sesi", 220, 220, 48, circle(110, 108, PAPER) + knob(110, 100, 110)
    + t(110, 184, "turn it up", 18, NAVY9, F, 700))
add("H08", "tatli", "Geliştirme kartı", 260, 180, 60, rrect(260, 180, 26, SKY) + devboard(130, 86, 150)
    + t(130, 164, "it blinks!", 18, NAVY9, F, 700))
add("H09", "tatli", "Servo · hemen", 220, 220, 48, circle(110, 108, HONEYL) + servo(110, 110, 120)
    + t(110, 182, "on it!", 20, NAVY9, F, 700))
add("H10", "tatli", "Multimetre · vibe check", 220, 220, 48, circle(110, 108, SKY) + multimeter(110, 96, 112)
    + t(110, 184, "vibe check", 18, NAVY9, F, 700))
add("H11", "tatli", "Havya · çok sıcak", 300, 120, 72, rrect(300, 120, 60, NAVY9)
    + f'<path d="M24 60 L52 54 V66 Z" fill="{SKY}" stroke="{SKY}" stroke-width="2" stroke-linejoin="round"/>'
    + f'<rect x="50" y="56" width="40" height="8" fill="{NAVY4}"/><rect x="88" y="50" width="12" height="20" rx="3" fill="{SKY}"/>'
    + f'<rect x="98" y="40" width="88" height="40" rx="20" fill="{BRICK}" stroke="{INK}" stroke-width="2.4"/>' + face(142, 60, 34, "happy", W)
    + smoke(30, 47, 7) + t(242, 56, "too hot", 19, HONEY, F, 700) + t(242, 80, "to handle", 16, W, F, 700))
add("H12", "tatli", "3D yazıcı · kalp basıyor", 220, 220, 48, circle(110, 108, SAGEL) + printer3d(110, 100, 110))
add("H13", "tatli", "Mıknatıs · çekici", 220, 220, 48, circle(110, 108, SKY) + heart(58, 74, 6) + heart(164, 70, 7) + heart(150, 44, 5)
    + magnet(110, 96, 110) + t(110, 182, "attractive", 19, NAVY9, F, 700))
add("H14", "tatli", "Atom · önemlisin", 220, 220, 48, circle(110, 108, PAPER) + atom(110, 100, 120)
    + t(110, 184, "you matter", 19, NAVY9, F, 700))
add("H15", "tatli", "Hesap makinesi", 220, 220, 48, circle(110, 108, HONEYL) + calculator(110, 98, 112)
    + t(110, 184, "I count on you", 16, NAVY9, F, 700))
add("H16", "tatli", "Disket · kaydedildi", 220, 220, 48, circle(110, 108, SKY) + floppy(110, 100, 110)
    + t(110, 182, "saved!", 20, NAVY9, F, 700))
add("H17", "tatli", "USB · üçüncü deneme", 220, 220, 48, circle(110, 108, SAGEL) + usb(110, 102, 116)
    + t(110, 184, "3rd try lucky", 16, NAVY9, F, 700))
add("H18", "tatli", "Enter tuşu", 200, 200, 45, rrect(200, 200, 30, SKY) + enter_key(100, 100, 150))
add("H19", "tatli", "Fare · fare", 220, 220, 48, circle(110, 108, HONEYL) + mouse_pc(108, 100, 120))
add("H20", "tatli", "Router · tam çekiyor", 220, 220, 48, circle(110, 108, SKY) + router(110, 108, 120)
    + t(110, 184, "full bars", 18, NAVY9, F, 700))
add("H21", "tatli", "Rover · kaşif", 260, 180, 60, rrect(260, 180, 26, HONEYL) + rover(132, 108, 130))
add("H22", "tatli", "Drone · yüksekten", 220, 220, 48, circle(110, 108, SKY) + drone(110, 104, 120)
    + t(110, 176, "fly high", 18, NAVY9, F, 700))

# ---------------------------------------------------------------- J · achievement badges


def badge(sid, name, fill, icon, l1, l2, c1=W, c2=HONEY):
    def fs(s):
        return min(17, round(112 / (len(s) * 0.64), 1))
    add(sid, "rozet", name, 220, 220, 48, scallop(110, 96, 18, fill) + icon + t(110, 142, l1, fs(l1), c1, F, 700)
        + t(110, 164, l2, fs(l2), c2, F, 700))


badge("J01", "İlk commit", NAVY, f'<path d="M74 84 H146" stroke="{W}" stroke-width="6" stroke-linecap="round"/>'
      f'<circle cx="110" cy="84" r="15" fill="{HONEY}" stroke="{W}" stroke-width="5"/>', "FIRST", "COMMIT")
badge("J02", "İlk devre kartı", NAVY9, pcb_icon(110, 84, 70), "FIRST", "PCB")
badge("J03", "Lehimden sağ çıktım", BRICK, iron(128, 104, 66, 225, HONEY) + star(140, 64, 7, HONEYL), "SOLDER", "SURVIVOR", W, HONEYL)
badge("J04", "Labda 100 saat", HONEY, clock(110, 84, 30), "100 HOURS", "IN THE LAB", NAVY9, W)
badge("J05", "Bug avcısı", SAGE, f'<circle cx="110" cy="84" r="27" fill="none" stroke="{W}" stroke-width="4"/>'
      f'<path d="M110 50 V62 M110 106 V118 M76 84 H88 M132 84 H144" stroke="{W}" stroke-width="4" stroke-linecap="round"/>'
      + bug(110, 86, 40), "BUG", "HUNTER", W, NAVY9)
badge("J06", "Gece kuşu", NAVY9, f'<circle cx="140" cy="60" r="12" fill="{HONEYL}"/><circle cx="146" cy="56" r="10" fill="{NAVY9}"/>'
      + owl(108, 88, 64), "NIGHT", "OWL")
badge("J07", "Erkenci kuş", SKY, bird(106, 88, 70), "EARLY", "BIRD", NAVY9, BRICK)
badge("J08", "Takım kaptanı", NAVY, f'<circle cx="110" cy="84" r="28" fill="{W}"/>' + t(110, 96, "C", 34, NAVY, G, 700), "TEAM", "CAPTAIN")
badge("J09", "Demo kahramanı", BRICK, star(110, 84, 34, HONEY) + face(110, 88, 26, "happy"), "DEMO", "HERO", W, HONEYL)
badge("J10", "Kod incelemecisi", SAGE, magnifier(104, 80, 20) + check(104, 81, 18, SAGE, 5), "CODE", "REVIEWER", W, NAVY9)
badge("J11", "Eşli programlama", NAVY9, cursor(84, 60, 40, HONEY) + cursor(118, 66, 40, SKY), "PAIR", "PROGRAMMER")
badge("J12", "Atölye konuşmacısı", HONEY, mic(110, 86, 64), "WORKSHOP", "SPEAKER", NAVY9, W)
badge("J13", "Hackathon bitirdim", NAVY, flag_checkered(114, 86, 64), "HACKATHON", "FINISHER")
badge("J14", "Açık kaynak", BRICK, heart(110, 84, 24, W) + t(110, 90, "</>", 14, BRICK, M, 700), "OPEN", "SOURCE", W, HONEYL)
badge("J15", "Mentorun seçimi", SAGE, star(110, 84, 34, HONEYL) + check(110, 86, 15, NAVY, 4.5), "MENTOR'S", "PICK", W, NAVY9)
badge("J16", "Önce güvenlik", HONEY, goggles(110, 84, 92), "SAFETY", "FIRST", NAVY9, W)

# ---------------------------------------------------------------- K · laptop hexes (44 x 51 mm)

add("K01", "hex", "IEC petek", 174, 200, 44, hexs(HONEY)
    + honeycomb(in_hex(87, 100, 82), 12, HONEYL, 87 - 7 * 12 * math.sqrt(3), 100 - 6 * 18, 87 + 7 * 12 * math.sqrt(3), 100 + 6 * 18, 1.8)
    + f'<rect x="22" y="62" width="130" height="80" rx="16" fill="{HONEY}"/>'
    + t(87, 112, "IEC", 56, NAVY9, G, 700) + t(87, 130, "ENGINEERING CLUB", 8.5, NAVY9, M, 700, ls=0.8))
add("K02", "hex", "Arı · hex", 174, 200, 44, hexs(SKY)
    + honeycomb(in_hex(87, 100, 80), 14, W, 87 - 6 * 14 * math.sqrt(3), 100 - 5 * 21, 87 + 6 * 14 * math.sqrt(3), 100 + 5 * 21, 1.6)
    + bee(87, 108, 84))
add("K03", "hex", "Hive mind", 174, 200, 44, hexs(NAVY9)
    + "".join(f'<polygon points="{" ".join(f"{x + 12 * math.cos(math.radians(60 * k - 90)):.1f},{y + 12 * math.sin(math.radians(60 * k - 90)):.1f}" for k in range(6))}" fill="{c}"/>'
              for x, y, c in ((76.6, 74, HONEY), (97.4, 74, HONEYL), (87, 56, HONEY)))
    + t(87, 124, "HIVE", 30, HONEY, G, 700) + t(87, 152, "MIND", 30, W, G, 700))
add("K04", "hex", "</> build things", 174, 200, 44, hexs(NAVY) + t(87, 116, "</>", 48, W, M, 700)
    + t(87, 146, "build things", 10, HONEYL, M, 600, ls=0.5))
add("K05", "hex", "git branch", 174, 200, 44, hexs(SAGE) + git_graph(87, 88, 90) + t(87, 156, "branch out", 15, W, F, 700))
add("K06", "hex", "Pi", 174, 200, 44, hexs(PAPER) + glyph("pi", 87, 92, 40, NAVY, 11) + t(87, 156, "3.14159", 13, NAVY9, M, 700, ls=1))
add("K07", "hex", "Lambda", 174, 200, 44, hexs(NAVY4) + glyph("lambda", 87, 92, 40, HONEY, 11) + t(87, 156, "lambda", 13, W, M, 700, ls=1))
add("K08", "hex", "Sigma · sum it up", 174, 200, 44, hexs(BRICK) + glyph("sigma", 87, 92, 38, W, 11) + t(87, 156, "sum it up", 13, W, M, 700))
add("K09", "hex", "Ohm-azing", 174, 200, 44, hexs(SAGEL) + ohm(87, 92, 34, NAVY, 11) + t(87, 156, "ohm-azing", 13, NAVY9, M, 700))
add("K10", "hex", "Curly crew", 174, 200, 44, hexs(HONEYL) + t(87, 118, "{ }", 54, NAVY, M, 700) + t(87, 150, "curly crew", 13, NAVY9, F, 700))
add("K11", "hex", "0x1EC", 174, 200, 44, hexs(NAVY9) + t(87, 104, "0x1EC", 30, HONEY, M, 700) + t(87, 134, "= IEC", 18, W, M, 700)
    + t(87, 154, "in hex", 10, SKY, M, 600))
add("K12", "hex", "Sarajevo · hex", 174, 200, 44, hexs(NAVY) + mountains(35, 70, 104, 62) + t(87, 156, "SARAJEVO", 12, W, M, 700, ls=1.5))
add("K13", "hex", "Bal kavanozu · sweet code", 174, 200, 44, hexs(SKY) + honey_jar(87, 104, 100))
add("K14", "hex", "Build · Break · Learn", 174, 200, 44, hexs(HONEY) + t(87, 82, "BUILD", 24, NAVY9, F, 700)
    + t(87, 112, "BREAK", 24, W, F, 700) + t(87, 142, "LEARN", 24, NAVY9, F, 700))

# ---------------------------------------------------------------- L · more engineering jokes

add("L01", "espri2", "Watt's up?", 220, 220, 50, circle(110, 108, NAVY9)
    + "".join(f'<path d="M{110 + 44 * math.cos(math.radians(a)):.1f} {80 + 44 * math.sin(math.radians(a)):.1f} L{110 + 53 * math.cos(math.radians(a)):.1f} '
              f'{80 + 53 * math.sin(math.radians(a)):.1f}" stroke="{HONEYL}" stroke-width="4" stroke-linecap="round"/>' for a in (-150, -120, -90, -60, -30))
    + bulb(110, 80, 70) + face(110, 78, 40, "happy") + t(110, 170, "Watt's up?", 20, W, F, 700))
add("L02", "espri2", "Ohm sweet ohm", 240, 200, 58, rrect(240, 200, 28, SAGEL) + house_ohm(120, 92, 130)
    + t(120, 182, "ohm sweet ohm", 19, NAVY9, F, 700))
add("L03", "espri2", "Stay positive", 220, 220, 50, circle(110, 108, HONEYL) + proton(108, 96, 46) + t(110, 180, "stay positive", 17, NAVY9, F, 700))
add("L04", "espri2", "Nuts about engineering", 300, 130, 70, rrect(300, 130, 26, SKY) + nut(70, 65, 96, "love", hole=SKY)
    + t(196, 60, "nuts about", 20, NAVY9, F, 700) + t(196, 88, "engineering", 22, NAVY, F, 700))
add("L05", "espri2", "Screw it, let's build it", 300, 130, 70, rrect(300, 130, 65, HONEYL) + screw(62, 64, 84)
    + t(186, 58, "screw it,", 22, NAVY9, F, 700) + t(186, 88, "let's build it", 19, BRICK, F, 700))
add("L06", "espri2", "Byte me", 220, 220, 50, circle(110, 108, CREAM) + cookie(110, 92, 52, CREAM) + t(110, 178, "byte me", 22, NAVY9, F, 700))
add("L07", "espri2", "It's a breadboard", 260, 190, 60, rrect(260, 190, 26, CREAM) + bread(130, 88, 170)
    + t(130, 170, "it's a breadboard", 17, NAVY9, F, 700))
add("L08", "espri2", "Current mood", 260, 150, 60, rrect(260, 150, 26, NAVY) + fat_bolt(30, 22, 106)
    + t(184, 68, "current", 26, W, F, 700) + t(184, 100, "mood", 26, HONEY, F, 700))
add("L09", "espri2", "Plot twist: typo", 280, 170, 64, bubble(280, 170, SKY) + t(140, 64, "plot twist:", 24, NAVY9, F, 700)
    + t(140, 100, "it was a typo", 22, BRICK, F, 700))
add("L10", "espri2", "Ask me about my side project", 300, 140, 70, rrect(300, 140, 24, HONEYL) + rocket(60, 68, 72)
    + t(184, 62, "ask me about", 18, NAVY, F, 600) + t(184, 92, "my side project", 21, NAVY9, F, 700))
add("L11", "espri2", "Kapatıp açtın mı?", 220, 220, 50, circle(110, 108, SAGE) + power_icon(110, 82, 34)
    + t(110, 150, "turned it off", 17, W, F, 700) + t(110, 172, "and on again?", 17, SAGEL, F, 700))
add("L12", "espri2", "Powered by snacks", 300, 120, 70, rrect(300, 120, 60, HONEY) + battery(70, 60, 64, 0.75, SAGE)
    + t(190, 54, "powered by", 18, NAVY9, F, 600) + t(190, 84, "snacks", 26, W, F, 700))
add("L13", "espri2", "final_final_v2", 300, 110, 70, rrect(300, 110, 20, NAVY9) + t(26, 48, "$ git commit -m", 15, SKY, M, 600, "start")
    + t(26, 78, '"final_final_v2"', 17, HONEY, M, 700, "start") + f'<rect x="196" y="64" width="10" height="18" fill="{HONEYL}"/>')
add("L14", "espri2", "I can fix that (probably)", 300, 130, 70, rrect(300, 130, 24, SKY) + wrench(62, 70, 74, NAVY)
    + t(186, 64, "I can fix that", 22, NAVY9, F, 700) + t(186, 92, "(probably)", 15, NAVY, M, 600))

json.dump(S, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
print(len(S), "stickers;", {c: sum(1 for s in S if s["cat"] == c) for c in dict.fromkeys(s["cat"] for s in S)})
