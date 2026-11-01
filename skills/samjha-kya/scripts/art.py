"""Flat cartoon kit: characters, bubbles and props as SVG strings.

Every panel is a 320x170 viewBox with the floor at y=150. Characters are drawn with their feet at (x, y).
Text arguments take a list of rows, or a plain string that is wrapped to fit the given width.
"""
from html import escape

INK = "#1c1b19"
TEAL = "#0f5f6b"
TEAL2 = "#2a8a96"
FACE = "#e4f3f4"
HALDI = "#e0a526"
CORAL = "#d9573f"
CREAM = "#fbf1df"
FLOOR = "#f0dfbd"
PAPER = "#fffdf9"
SKIN = "#e3a87f"
SKIN2 = "#c98b5e"
GREY = "#a8a39b"
BLUE = "#4b55b0"
GREEN = "#2a7a3e"
WOOD = "#b98a52"


def e(s):
    return escape(str(s), quote=True)


def _greedy(words, per):
    rows, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > per:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return rows + ([cur] if cur else [])


def wrap(s, width, fs):
    """Split a string into rows that fit `width` units at font size `fs` (bold sans averages ~0.58 em).
    Rows are balanced, so a bubble never ends on one lonely word. A list is treated as rows to keep."""
    if not isinstance(s, str):
        return [r for row in s for r in (wrap(str(row), width, fs) if str(row).strip() else [""])]
    per = max(4, int(width / (fs * 0.58)))
    words = s.split()
    rows = _greedy(words, per)
    if len(rows) > 1:
        for p in range(max(4, -(-len(s) // len(rows))), per + 1):
            even = _greedy(words, p)
            if len(even) == len(rows):
                return even
    return rows


def svg(inner, label, floor=True):
    fl = f'<rect y="150" width="320" height="20" fill="{FLOOR}"/>' if floor else ""
    return (f'<svg viewBox="0 0 320 170" role="img" aria-label="{e(label)}">'
            f'<rect width="320" height="170" fill="{CREAM}"/>{fl}{inner}</svg>')


def text(x, y, s, fs: float = 11, anchor="middle", fill=INK, weight=600, italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{fill}" '
            f'font-weight="{weight}"{st}>{e(s)}</text>')


def lines(x, y, rows, fs: float = 11, anchor="middle", fill=INK, weight=600, lh=1.22):
    return "".join(text(x, y + i * fs * lh, r, fs, anchor, fill, weight) for i, r in enumerate(rows))


def bubble(x, y, w, rows, tx, ty, fs: float = 11, fill="#fff", weight=600, color=INK):
    """Speech bubble with its top-left at (x, y) and a tail pointing at (tx, ty)."""
    rows = wrap(rows, w - 12, fs)
    h = 10 + len(rows) * fs * 1.22
    bx = min(max(tx, x + 14), x + w - 14)
    if ty > y + h:
        tail = f"M{bx - 6} {y + h - 1} L{tx} {ty} L{bx + 6} {y + h - 1}"
    else:
        tail = f"M{bx - 6} {y + 1} L{tx} {ty} L{bx + 6} {y + 1}"
    return (f'<g class="bub" data-w="{w}"><path d="{tail}" fill="{fill}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" rx="9" fill="{fill}" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="{bx - 5}" y="{y + h - 3 if ty > y + h else y + 0.8}" width="10" height="2.4" fill="{fill}"/>'
            + lines(x + w / 2, y + 4 + fs, rows, fs, fill=color, weight=weight) + "</g>")


def think(x, y, w, rows, tx, ty, fs: float = 10):
    rows = wrap(rows, w - 14, fs)
    h = 10 + len(rows) * fs * 1.22
    cx, cy = x + w / 2, y + h
    dots = (f'<circle cx="{(cx * 2 + tx) / 3:.0f}" cy="{(cy * 2 + ty) / 3:.0f}" r="3.5" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
            f'<circle cx="{(cx + tx * 2) / 3:.0f}" cy="{(cy + ty * 2) / 3:.0f}" r="2.2" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
    return (f'<g class="bub" data-w="{w}">' + dots + f'<rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" rx="{h / 2:.1f}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
            + lines(x + w / 2, y + 4 + fs, rows, fs, weight=500) + "</g>")


def _mouth(mood, y):
    if mood == "smile":
        return f'<path d="M-6 {y} Q0 {y + 5} 6 {y}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
    if mood == "grin":
        return f'<path d="M-8 {y - 1} Q0 {y + 8} 8 {y - 1} Z" fill="{INK}"/>'
    if mood == "o":
        return f'<ellipse cx="0" cy="{y + 1}" rx="3" ry="4" fill="{INK}"/>'
    if mood == "sad":
        return f'<path d="M-6 {y + 3} Q0 {y - 2} 6 {y + 3}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
    return f'<path d="M-6 {y + 1} L6 {y + 1}" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'


def chintu(x, y, s=1.0, mood="smile", hat=None, arms="down", eyes="dot", tint=TEAL):
    """Chintu, the robot who read the entire internet. mood: smile | grin | o | sad | flat.
    hat: None | 'grad' | 'chef'. arms: down | up | wave | hold. eyes: dot | up | x | shades."""
    if arms == "up":
        a = (f'<rect x="-30" y="-62" width="8" height="26" rx="4" fill="{tint}" transform="rotate(-20 -26 -40)"/>'
             f'<rect x="22" y="-62" width="8" height="26" rx="4" fill="{tint}" transform="rotate(20 26 -40)"/>')
    elif arms == "wave":
        a = (f'<rect x="-26" y="-38" width="8" height="24" rx="4" fill="{tint}"/>'
             f'<rect x="22" y="-62" width="8" height="26" rx="4" fill="{tint}" transform="rotate(25 26 -40)"/>')
    elif arms == "hold":
        a = (f'<rect x="-30" y="-36" width="22" height="8" rx="4" fill="{tint}"/>'
             f'<rect x="8" y="-36" width="22" height="8" rx="4" fill="{tint}"/>')
    else:
        a = (f'<rect x="-26" y="-38" width="8" height="24" rx="4" fill="{tint}"/>'
             f'<rect x="18" y="-38" width="8" height="24" rx="4" fill="{tint}"/>')
    if eyes == "shades":
        ey = f'<rect x="-15" y="-73" width="30" height="8" rx="3" fill="{INK}"/>'
    elif eyes == "x":
        ey = (f'<path d="M-11 -72 l6 6 M-5 -72 l-6 6 M5 -72 l6 6 M11 -72 l-6 6" stroke="{INK}" stroke-width="2"/>')
    elif eyes == "up":
        ey = f'<circle cx="-8" cy="-71" r="3.5" fill="{INK}"/><circle cx="8" cy="-71" r="3.5" fill="{INK}"/>'
    else:
        ey = f'<circle cx="-8" cy="-69" r="3.5" fill="{INK}"/><circle cx="8" cy="-69" r="3.5" fill="{INK}"/>'
    h = ""
    if hat == "grad":
        h = (f'<path d="M-26 -88 L0 -98 L26 -88 L0 -79 Z" fill="{INK}"/>'
             f'<path d="M20 -87 L22 -76" stroke="{HALDI}" stroke-width="2"/><circle cx="22" cy="-75" r="2.5" fill="{HALDI}"/>')
    elif hat == "chef":
        h = (f'<rect x="-15" y="-92" width="30" height="10" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
             f'<circle cx="-10" cy="-96" r="8" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
             f'<circle cx="0" cy="-100" r="9" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
             f'<circle cx="10" cy="-96" r="8" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
             f'<rect x="-14" y="-91" width="28" height="8" fill="#fff"/>')
    ant = "" if hat else (f'<line x1="0" y1="-84" x2="0" y2="-93" stroke="{INK}" stroke-width="2"/>'
                          f'<circle cx="0" cy="-95" r="4" fill="{HALDI}"/>')
    return (f'<g class="who" transform="translate({x} {y}) scale({s})">'
            f'<rect x="-14" y="-7" width="10" height="7" rx="2" fill="{INK}"/><rect x="4" y="-7" width="10" height="7" rx="2" fill="{INK}"/>'
            f'{a}<rect x="-18" y="-42" width="36" height="37" rx="8" fill="{TEAL2}"/>'
            f'<rect x="-7" y="-33" width="14" height="9" rx="2" fill="{HALDI}"/>'
            f'<rect x="-4" y="-47" width="8" height="6" fill="{INK}"/>'
            f'{ant}<rect x="-24" y="-84" width="48" height="39" rx="10" fill="{tint}"/>'
            f'<rect x="-18" y="-79" width="36" height="28" rx="7" fill="{FACE}"/>'
            f'{ey}{_mouth(mood, -60)}{h}</g>')


def _human(x, y, s, shirt, skin, hair, mood, extra_back="", extra_front="", arms="down"):
    if arms == "up":
        a = (f'<rect x="-27" y="-62" width="8" height="26" rx="4" fill="{shirt}" transform="rotate(-25 -23 -40)"/>'
             f'<rect x="19" y="-62" width="8" height="26" rx="4" fill="{shirt}" transform="rotate(25 23 -40)"/>')
    elif arms == "point":
        a = (f'<rect x="-25" y="-38" width="8" height="24" rx="4" fill="{shirt}"/>'
             f'<rect x="16" y="-40" width="24" height="8" rx="4" fill="{shirt}" transform="rotate(-15 18 -36)"/>')
    elif arms == "hold":
        a = (f'<rect x="-28" y="-36" width="20" height="8" rx="4" fill="{shirt}"/>'
             f'<rect x="8" y="-36" width="20" height="8" rx="4" fill="{shirt}"/>')
    else:
        a = (f'<rect x="-25" y="-38" width="8" height="24" rx="4" fill="{shirt}"/>'
             f'<rect x="17" y="-38" width="8" height="24" rx="4" fill="{shirt}"/>')
    mouth = {"smile": f'<path d="M-5 -50 Q0 -46 5 -50" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>',
             "o": f'<ellipse cx="0" cy="-49" rx="2.6" ry="3.4" fill="{INK}"/>',
             "flat": f'<path d="M-5 -49 L5 -49" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>',
             "sad": f'<path d="M-5 -47 Q0 -51 5 -47" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>',
             "grin": f'<path d="M-6 -51 Q0 -44 6 -51 Z" fill="{INK}"/>'}[mood if mood in ("smile", "o", "flat", "sad", "grin") else "flat"]
    return (f'<g class="who" transform="translate({x} {y}) scale({s})">{extra_back}'
            f'<rect x="-12" y="-9" width="10" height="9" rx="2" fill="{INK}"/><rect x="2" y="-9" width="10" height="9" rx="2" fill="{INK}"/>'
            f'{a}<path d="M-19 -6 L-17 -38 Q0 -45 17 -38 L19 -6 Z" fill="{shirt}"/>'
            f'<rect x="-4" y="-44" width="8" height="6" fill="{skin}"/>'
            f'<circle cx="0" cy="-58" r="15" fill="{skin}"/>{hair}'
            f'<circle cx="-5.5" cy="-59" r="1.9" fill="{INK}"/><circle cx="5.5" cy="-59" r="1.9" fill="{INK}"/>'
            f'{mouth}{extra_front}</g>')


def sharma(x, y, s=1.0, mood="flat", brow="skeptic", arms="down"):
    """Sharma ji, the sceptic: grey hair, specs, moustache. 'Data dikhao.'
    mood: flat | smile | o | sad | grin. brow: skeptic | flat. arms: down | up | point | hold."""
    hair = (f'<path d="M-15 -60 Q-15 -76 0 -75 Q15 -76 15 -60 Q13 -68 0 -68 Q-13 -68 -15 -60 Z" fill="{GREY}"/>')
    specs = (f'<rect x="-10.5" y="-62.5" width="9" height="7" rx="2" fill="none" stroke="{INK}" stroke-width="1.5"/>'
             f'<rect x="1.5" y="-62.5" width="9" height="7" rx="2" fill="none" stroke="{INK}" stroke-width="1.5"/>'
             f'<path d="M-1.5 -60 L1.5 -60" stroke="{INK}" stroke-width="1.5"/>')
    brows = (f'<path d="M-10 -66 L-2 -65" stroke="{INK}" stroke-width="1.6"/><path d="M2 -66 L10 -69" stroke="{INK}" stroke-width="1.6"/>'
             if brow == "skeptic" else
             f'<path d="M-10 -66 L-2 -66" stroke="{INK}" stroke-width="1.6"/><path d="M2 -66 L10 -66" stroke="{INK}" stroke-width="1.6"/>')
    tache = f'<path d="M-8 -54.5 Q0 -58.5 8 -54.5 Q4 -52.8 0 -54 Q-4 -52.8 -8 -54.5 Z" fill="{INK}"/>'
    return _human(x, y, s, BLUE, SKIN, hair, mood, extra_front=specs + brows + tache, arms=arms)


def pinky(x, y, s=1.0, mood="smile", arms="down"):
    """Pinky, the eager learner: hair bun with a coral clip, earrings. Same moods and arms as sharma()."""
    hair = (f'<path d="M-15 -57 Q-16 -75 0 -75 Q16 -75 15 -57 Q10 -68 0 -68 Q-10 -68 -15 -57 Z" fill="#2b2320"/>'
            f'<circle cx="0" cy="-78" r="7" fill="#2b2320"/><rect x="-6" y="-75" width="12" height="3" rx="1.5" fill="{CORAL}"/>'
            f'<circle cx="-15" cy="-53" r="1.8" fill="{HALDI}"/><circle cx="15" cy="-53" r="1.8" fill="{HALDI}"/>')
    return _human(x, y, s, CORAL, SKIN2, hair, mood, arms=arms)


def person(x, y, s=1.0, mood="flat", shirt=GREY, arms="down", hair_col="#4a403a", hair="short", bindi=False, skin=SKIN):
    """An extra (mummy, a cousin, the chaiwala). hair: short | bun | long | bald | grey (short and grey)."""
    top = f'<path d="M-15 -60 Q-15 -76 0 -75 Q15 -76 15 -60 Q12 -70 0 -70 Q-12 -70 -15 -60 Z" fill="{GREY if hair == "grey" else hair_col}"/>'
    if hair == "bun":
        top = (f'<path d="M-15 -57 Q-16 -75 0 -75 Q16 -75 15 -57 Q10 -68 0 -68 Q-10 -68 -15 -57 Z" fill="{hair_col}"/>'
               f'<circle cx="0" cy="-78" r="7" fill="{hair_col}"/>')
    elif hair == "long":
        top = (f'<path d="M-17 -40 Q-19 -76 0 -76 Q19 -76 17 -40 L12 -42 Q13 -66 0 -68 Q-13 -66 -12 -42 Z" fill="{hair_col}"/>')
    elif hair == "bald":
        top = f'<path d="M-15 -58 Q-15 -64 -12 -66 M15 -58 Q15 -64 12 -66" stroke="{GREY}" stroke-width="3" fill="none"/>'
    dot = f'<circle cx="0" cy="-66" r="1.6" fill="{CORAL}"/>' if bindi else ""
    return _human(x, y, s, shirt, skin, top, mood, extra_front=dot, arms=arms)


def desk(x, y, w=90):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="7" rx="2" fill="{WOOD}"/>'
            f'<rect x="{x + 6}" y="{y + 7}" width="6" height="{150 - y - 7}" fill="#9a6f3c"/>'
            f'<rect x="{x + w - 12}" y="{y + 7}" width="6" height="{150 - y - 7}" fill="#9a6f3c"/>')


def monitor(x, y, w, h, rows, fs: float = 9, screen="#fff", color=INK, facing=True):
    rows = wrap(rows, w - 10, fs)
    return (f'<rect x="{x + w / 2 - 4}" y="{y + h}" width="8" height="8" fill="{INK}"/>'
            f'<rect x="{x + w / 2 - 14}" y="{y + h + 7}" width="28" height="3" rx="1.5" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{INK}"/>'
            + (f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="2" fill="{screen}"/>'
               + lines(x + w / 2, y + 6 + fs, rows, fs, fill=color) if facing else ""))


def paper(x, y, w, h, rows=(), fs: float = 8, rot=0, fill=PAPER, color=INK, weight=600, anchor="middle"):
    rows = wrap(rows, w - 10, fs)
    tx = x + w / 2 if anchor == "middle" else x + 6
    t = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
    return (f'<g class="lbl"{t}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>'
            + lines(tx, y + 5 + fs, rows, fs, anchor=anchor, fill=color, weight=weight) + "</g>")


def sticky(x, y, label, rot=0, fill=HALDI, fs: float = 8.5):
    """A sticky note that grows to fit its label."""
    w = max(24, len(str(label)) * fs * 0.62 + 8)
    return (f'<g transform="rotate({rot} {x + w / 2} {y + 11})"><rect x="{x}" y="{y}" width="{w:.1f}" height="22" fill="{fill}"/>'
            + text(x + w / 2, y + 11 + fs * 0.36, label, fs, fill=INK, weight=800) + "</g>")


def stamp(x, y, label, color=CORAL, rot=-12, fs: float = 13, w=None):
    w = w or len(label) * fs * 0.68 + 14
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x - w / 2}" y="{y - fs}" width="{w}" height="{fs * 1.6}" rx="4" '
            f'fill="none" stroke="{color}" stroke-width="2.4"/>' + text(x, y + fs * 0.25, label, fs, fill=color, weight=800) + "</g>")


def books(x, y, n=5, w=34):
    cols = [CORAL, TEAL2, HALDI, BLUE, GREEN, "#8a5a9e"]
    out = ""
    for i in range(n):
        ww = w - (i % 3) * 3
        out += f'<rect x="{x - ww / 2 + (i % 2) * 2}" y="{y - (i + 1) * 8}" width="{ww}" height="7" rx="1.5" fill="{cols[i % len(cols)]}"/>'
    return out


def shelf(x, y, w=70, rows=3):
    cols = [CORAL, TEAL2, HALDI, BLUE, GREEN, "#8a5a9e", GREY]
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{150 - y}" fill="#9a6f3c"/>'
    rh = (150 - y - 6) / rows
    for r in range(rows):
        top = y + 3 + r * rh
        out += f'<rect x="{x + 3}" y="{top}" width="{w - 6}" height="{rh - 3}" fill="#6e4d27"/>'
        bx = x + 5
        i = r * 3
        while bx < x + w - 9:
            bw = 5 + (i * 7) % 4
            bh = rh - 6 - (i * 5) % 6
            out += f'<rect x="{bx}" y="{top + rh - 3 - bh}" width="{bw}" height="{bh}" fill="{cols[i % len(cols)]}"/>'
            bx += bw + 1
            i += 1
    return out


# ---------- props for everyday topics ----------

def arrow(x1, y1, x2, y2, color=INK, w=1.8):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - 8 * math.cos(a - 0.45), y2 - 8 * math.sin(a - 0.45)
    hx2, hy2 = x2 - 8 * math.cos(a + 0.45), y2 - 8 * math.sin(a + 0.45)
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{hx1:.1f} {hy1:.1f} L{x2} {y2} L{hx2:.1f} {hy2:.1f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def board(x, y, w, h, rows, fs: float = 9, title=None):
    """A whiteboard on legs. rows: list or string (wrapped)."""
    rows = wrap(rows, w - 14, fs)
    top = y + 8 + fs + (fs * 1.3 if title else 0)
    return (f'<rect x="{x + 10}" y="{y + h}" width="4" height="{max(0, 150 - y - h)}" fill="{GREY}"/>'
            f'<rect x="{x + w - 14}" y="{y + h}" width="4" height="{max(0, 150 - y - h)}" fill="{GREY}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
            + (text(x + w / 2, y + 6 + fs, title, fs, weight=800, fill=TEAL) if title else "")
            + lines(x + w / 2, top, rows, fs, weight=600))


def phone(x, y, rows=(), fs: float = 7, h=64, w=36, screen="#fff", color=INK):
    """A phone with its top-left at (x, y); rows are short lines on the screen."""
    rows = wrap(rows, w - 8, fs)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK}"/>'
            f'<rect x="{x + 3}" y="{y + 7}" width="{w - 6}" height="{h - 14}" rx="2" fill="{screen}"/>'
            + lines(x + w / 2, y + 10 + fs, rows, fs, fill=color))


def clock(x, y, r=16, hour=9, minute=0, color=INK):
    import math
    ha = math.radians((hour % 12 + minute / 60) * 30 - 90)
    ma = math.radians(minute * 6 - 90)
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{color}" stroke-width="2"/>'
            + "".join(f'<circle cx="{x + (r - 4) * math.cos(math.radians(i * 30)):.1f}" cy="{y + (r - 4) * math.sin(math.radians(i * 30)):.1f}" r="1" fill="{color}"/>' for i in range(12))
            + f'<path d="M{x} {y} L{x + r * 0.5 * math.cos(ha):.1f} {y + r * 0.5 * math.sin(ha):.1f}" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M{x} {y} L{x + r * 0.8 * math.cos(ma):.1f} {y + r * 0.8 * math.sin(ma):.1f}" stroke="{CORAL}" stroke-width="1.6" stroke-linecap="round"/>')


def bed(x, y=150, w=120, sleeper=False):
    """A bed whose legs stand on the floor at y; x is the left edge."""
    z = (text(x + w - 18, y - 52, "z", 12, fill=BLUE, weight=800) + text(x + w - 8, y - 64, "z", 15, fill=BLUE, weight=800)) if sleeper else ""
    head = (f'<circle cx="{x + 26}" cy="{y - 34}" r="11" fill="{SKIN}"/><path d="M{x + 18} {y - 36} q8 4 16 0" stroke="{INK}" stroke-width="1.5" fill="none"/>' if sleeper else "")
    return (f'<rect x="{x}" y="{y - 56}" width="10" height="56" rx="3" fill="{WOOD}"/>'
            f'<rect x="{x + w - 8}" y="{y - 36}" width="8" height="36" rx="3" fill="{WOOD}"/>'
            f'<rect x="{x + 6}" y="{y - 28}" width="{w - 10}" height="14" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="{x + 12}" y="{y - 38}" width="26" height="12" rx="5" fill="{CREAM}" stroke="{INK}" stroke-width="1.2"/>'
            + head + f'<rect x="{x + 36}" y="{y - 32}" width="{w - 44}" height="14" rx="5" fill="{BLUE}"/>' + z)


def moon(x, y, r=12):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{HALDI}"/>'
            f'<circle cx="{x + r * 0.45:.1f}" cy="{y - r * 0.3:.1f}" r="{r * 0.85:.1f}" fill="{CREAM}"/>')


def sun(x, y, r=12):
    import math
    rays = "".join(f'<path d="M{x + (r + 3) * math.cos(math.radians(a)):.1f} {y + (r + 3) * math.sin(math.radians(a)):.1f} '
                   f'L{x + (r + 8) * math.cos(math.radians(a)):.1f} {y + (r + 8) * math.sin(math.radians(a)):.1f}" stroke="{HALDI}" stroke-width="2.2" stroke-linecap="round"/>'
                   for a in range(0, 360, 45))
    return rays + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{HALDI}"/>'


def chai(x, y, s=1.0, steam=True):
    """A cutting-chai glass standing at (x, y)."""
    st = (f'<path d="M-4 -26 q-4 -6 0 -12 q4 -6 0 -12" fill="none" stroke="{GREY}" stroke-width="1.6"/>'
          f'<path d="M4 -24 q-4 -6 0 -12" fill="none" stroke="{GREY}" stroke-width="1.6"/>') if steam else ""
    return (f'<g transform="translate({x} {y}) scale({s})">{st}<path d="M-9 -20 L9 -20 L7 0 L-7 0 Z" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'
            f'<path d="M-8.2 -13 L8.2 -13 L7 0 L-7 0 Z" fill="{WOOD}"/></g>')


def coin(x, y, r=10, label="\u20b9", fill=HALDI):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.3"/>'
            f'<circle cx="{x}" cy="{y}" r="{r - 3}" fill="none" stroke="{INK}" stroke-width="0.8" opacity=".5"/>'
            + text(x, y + r * 0.38, label, r * 1.05, weight=800))


def coins(x, y, n=5, r=9):
    """A stack of n coins standing on y."""
    return "".join(f'<ellipse cx="{x}" cy="{y - 4 - i * 5}" rx="{r}" ry="4" fill="{HALDI}" stroke="{INK}" stroke-width="1"/>' for i in range(n))


def calendar(x, y, top="MON", big="1", w=40, h=44, color=CORAL, fs: float = 9):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="13" rx="4" fill="{color}"/><rect x="{x}" y="{y + 8}" width="{w}" height="5" fill="{color}"/>'
            + text(x + w / 2, y + 10, top, fs, fill="#fff", weight=800) + text(x + w / 2, y + h - 9, big, 18, weight=800))


def bulb(x, y, on=True):
    glow = "".join(f'<path d="M{x + dx} {y + dy} l{ex} {ey}" stroke="{HALDI}" stroke-width="2" stroke-linecap="round"/>'
                   for dx, dy, ex, ey in ((-16, -14, -6, -5), (16, -14, 6, -5), (0, -22, 0, -7), (-18, 2, -7, 0), (18, 2, 7, 0))) if on else ""
    return (glow + f'<circle cx="{x}" cy="{y - 2}" r="12" fill="{HALDI if on else "#fff"}" stroke="{INK}" stroke-width="1.4"/>'
            f'<rect x="{x - 6}" y="{y + 9}" width="12" height="8" rx="2" fill="{GREY}" stroke="{INK}" stroke-width="1"/>')


def plant(x, y=150, h=34):
    return (f'<path d="M{x} {y - 14} q-14 -{h * 0.6:.0f} -4 -{h}" fill="none" stroke="{GREEN}" stroke-width="2"/>'
            f'<ellipse cx="{x - 9}" cy="{y - h * 0.7:.0f}" rx="9" ry="4" fill="{GREEN}" transform="rotate(-30 {x - 9} {y - h * 0.7:.0f})"/>'
            f'<ellipse cx="{x + 7}" cy="{y - h * 0.5:.0f}" rx="9" ry="4" fill="{GREEN}" transform="rotate(25 {x + 7} {y - h * 0.5:.0f})"/>'
            f'<path d="M{x - 11} {y - 15} L{x + 11} {y - 15} L{x + 8} {y} L{x - 8} {y} Z" fill="{CORAL}"/>')


def sign(x, y, w, rows, fs: float = 9, fill=HALDI, color=INK, rot=0):
    """A flat label box (a shop board, a tag) with its top-left at (x, y)."""
    rows = wrap(rows, w - 10, fs)
    h = 8 + len(rows) * fs * 1.22
    t = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
    return (f'<g class="lbl"{t}><rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" rx="5" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>'
            + lines(x + w / 2, y + 3 + fs, rows, fs, fill=color, weight=700) + "</g>")


def heart(x, y, s=1.0, fill=CORAL):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 6 C-10 -2 -10 -12 -4 -14 C0 -15 0 -11 0 -10 C0 -11 0 -15 4 -14 C10 -12 10 -2 0 6 Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="1"/>')


def line_chart(x, y, w, h, values, color=TEAL2, labels=None, fs: float = 8):
    """Axes plus a line through `values` (any scale). Optional labels under the first and last point."""
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    pts = [(x + i * w / max(1, len(values) - 1), y + h - (v - lo) / span * h) for i, v in enumerate(values)]
    path = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    out = (f'<path d="M{x} {y - 4} L{x} {y + h} L{x + w + 4} {y + h}" fill="none" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>'
           + "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{color}"/>' for px, py in pts))
    if labels:
        out += text(pts[0][0], y + h + fs + 3, labels[0], fs, weight=600) + text(pts[-1][0], y + h + fs + 3, labels[-1], fs, weight=600)
    return out


def tick(x, y, s=1.0, color=GREEN):
    return f'<path transform="translate({x} {y}) scale({s})" d="M-8 0 L-2 6 L9 -7" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'


def cross(x, y, s=1.0, color=CORAL):
    return f'<path transform="translate({x} {y}) scale({s})" d="M-7 -7 L7 7 M7 -7 L-7 7" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>'


# ---------- layout helpers ----------

def duo(left, lb, right, rb, label, extra=""):
    """Two characters, each with a speech bubble. left/right are SVG strings drawn at x=70 and x=240.
    lb/rb are (rows, fs) or None."""
    out = extra + left + right
    if lb:
        out += bubble(8, 10, 130, lb[0], 70, 58, fs=lb[1] if len(lb) > 1 else 10)
    if rb:
        out += bubble(176, 10, 136, rb[0], 240, 58, fs=rb[1] if len(rb) > 1 else 10)
    return svg(out, label)


def bars(items, x=110, y=28, step=24, scale=1.6):
    """Horizontal bars: items = [(label, value, colour, value_text)]."""
    out = ""
    for i, (lab, v, col, vt) in enumerate(items):
        yy = y + i * step
        out += (text(x - 6, yy + 12, lab, 10, anchor="end", weight=600)
                + f'<rect x="{x}" y="{yy}" width="{max(2, v * scale):.1f}" height="16" rx="3" fill="{col}"/>'
                + text(x + max(2, v * scale) + 4, yy + 12, vt, 9, anchor="start", weight=500))
    return out


def layers(rows, x=20, y=16, w=200, h=20, gap=3):
    """Stacked labelled bands (a desk / a call / a pipeline)."""
    out = ""
    for i, (lab, col, note) in enumerate(rows):
        yy = y + i * (h + gap)
        out += (f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="4" fill="{col}"/>'
                + text(x + 8, yy + h / 2 + 4, lab, 9.5, anchor="start", weight=700, fill="#fff" if col not in (HALDI, PAPER, "#fff", "#f3dfb0") else INK)
                + (text(x + w + 6, yy + h / 2 + 4, note, 8.5, anchor="start", weight=500, fill="#6d675f") if note else ""))
    return out


def flow(steps, y=60, x0=14, w=56, gap=20, h=34, cols=None, fs: float = 9):
    """Left-to-right boxes joined by arrows."""
    cols = cols or [TEAL2, HALDI, CORAL, BLUE, GREEN, TEAL]
    out = ""
    for i, s in enumerate(steps):
        x = x0 + i * (w + gap)
        rows = s if isinstance(s, (list, tuple)) else [s]
        c = cols[i % len(cols)]
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}"/>'
                + lines(x + w / 2, y + h / 2 + fs / 2 - (len(rows) - 1) * fs * 0.6, rows, fs, fill="#fff" if c != HALDI else INK, weight=700))
        if i < len(steps) - 1:
            ax = x + w + 2
            out += (f'<path d="M{ax} {y + h / 2} L{ax + gap - 6} {y + h / 2}" stroke="{INK}" stroke-width="1.6"/>'
                    f'<path d="M{ax + gap - 9} {y + h / 2 - 4} L{ax + gap - 4} {y + h / 2} L{ax + gap - 9} {y + h / 2 + 4}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    return out
