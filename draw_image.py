#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: one deterministic 1024x1024 PNG.

Draws everything from code; no downloads, no randomness, no network.
Run:  python3 draw_image.py   ->  entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# Palette
PAPER = (247, 243, 234)      # #f7f3ea off-white paper
NAVY = (20, 38, 74)          # #14264a masthead band
NAVY_DARK = (11, 26, 51)     # backing strip inside hero
GOLD = (216, 176, 68)        # gold accents / date
GOLD_RULE = (203, 158, 52)
SEA = (13, 38, 70)           # deep blue hero sea
SEA_WAVE = (26, 60, 102)
SHIP_GREY = (158, 158, 158)
EXPLODE = (255, 157, 0)      # orange burst
EXPLODE_CORE = (255, 215, 90)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
TEXT_DARK = (33, 37, 41)
TEXT_MUTE = (90, 90, 96)
BOTTOM = (233, 231, 221)     # light grey bottom strip
STRIP_NAVY = (26, 54, 98)
STRIP_RED = (176, 42, 42)
STRIP_GREY = (68, 68, 68)
STRIP_GREEN = (46, 125, 50)

FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_font_cache = {}


def font(path, size):
    key = (path, int(size))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, int(size))
    return _font_cache[key]


def fit_size(draw, text, path, max_w, max_size, min_size=10):
    """Largest font size <= max_size whose text fits max_w."""
    size = max_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, size
        size -= 1
    f = font(path, min_size)
    return f, min_size


def wrap_lines(draw, text, path, size, max_w):
    """Greedy word wrap at a fixed size (words assumed short enough)."""
    f = font(path, size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text(draw, xy, lines, path, size, fill, align="center", line_gap=1.25, max_w=None):
    """Draw centred (or left-aligned) multi-line text starting at xy (top-left of first line)."""
    x, y = xy
    f = font(path, size)
    ascent, descent = f.getmetrics()
    line_h = int((ascent - descent) * line_gap) or int(size * 1.2)
    for line in lines:
        w = draw.textlength(line, font=f)
        if align == "center":
            tx = x - w / 2
        else:
            tx = x
        draw.text((tx, y), line, font=f, fill=fill)
        y += line_h
    return y


def rect(draw, x0, y0, x1, y1, fill, radius=0):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill)


def star5(draw, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(5):
        a = math.radians(rot + i * 72)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        a = math.radians(rot + 72 + i * 72)
        pts.append((cx + r * 0.38 * math.cos(a), cy + r * 0.38 * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_skyscraper(draw, cx, cy, s):
    # building + antenna + windows
    bw, bh = s * 0.42, s * 0.72
    draw.rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], fill=TEXT_DARK)
    draw.line([cx, cy - bh / 2 - s * 0.28, cx, cy - bh / 2], fill=TEXT_DARK, width=2)
    ws = s * 0.09
    for dy in (-bh / 2 + s * 0.10, -bh / 2 + s * 0.34, -bh / 2 + s * 0.58):
        for dx in (-bw / 2 + s * 0.14, bw / 2 - s * 0.14 - ws):
            draw.rectangle([dx, dy, dx + ws, dy + ws], fill=(200, 200, 200))


def icon_medal(draw, cx, cy, s):
    draw.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=(230, 190, 60),
                 outline=(150, 110, 30), width=2)
    star5(draw, cx, cy, s * 0.30, (255, 255, 255))
    draw.rectangle([cx - s * 0.09, cy + s / 2, cx + s * 0.09, cy + s * 0.62], fill=(160, 130, 40))


def icon_courthouse(draw, cx, cy, s):
    h = s * 0.62
    draw.rectangle([cx - s / 2, cy - h / 2, cx + s / 2, cy + h / 2], fill=TEXT_DARK)
    draw.polygon([(cx - s / 2, cy - h / 2), (cx + s / 2, cy - h / 2), (cx, cy - h / 2 - s * 0.42)],
                 fill=TEXT_DARK)
    cw = s * 0.16
    for dx in (-s * 0.30, s * 0.30 - cw):
        draw.rectangle([cx + dx, cy + h * 0.10, cx + dx + cw, cy + h / 2], fill=(120, 120, 120))


def icon_football(draw, cx, cy, s):
    draw.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=TEXT_DARK, width=3)
    star5(draw, cx, cy, s * 0.22, TEXT_DARK)
    for dx, dy in ((-s * 0.42, -s * 0.30), (s * 0.42, -s * 0.30), (-s * 0.42, s * 0.30), (s * 0.42, s * 0.30)):
        star5(draw, cx + dx, cy + dy, s * 0.11, TEXT_DARK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- Masthead band ----------------
    band_h = 150
    rect(d, 0, 0, W, band_h, NAVY)
    f, sz = fit_size(d, "WORLD NEWS", FONT_SERIF_B, W - 120, 56)
    draw_text(d, (W / 2, 10), ["WORLD NEWS"], FONT_SERIF_B, sz, WHITE)
    f, sz = fit_size(d, "WEDNESDAY 25 NOVEMBER 2026", FONT_SANS_B, W - 120, 26)
    draw_text(d, (W / 2, 92), ["WEDNESDAY 25 NOVEMBER 2026"], FONT_SANS_B, sz, GOLD)
    rect(d, 0, band_h, W, band_h + 6, GOLD_RULE)

    # ---------------- Hero panel ----------------
    h0, h1 = band_h + 10, band_h + 10 + 320   # 128 .. 438
    rect(d, 0, h0, W, h1, SEA)
    # waves at the bottom of the sea
    waterline = h1 - 14
    for x in range(-120, W + 120, 110):
        for phase, amp in ((0, 11), (60, 7)):
            d.arc([x + phase, waterline - amp, x + 150 + phase, waterline + amp],
                  180, 360, fill=SEA_WAVE, width=3)

    # explosion at the ship
    ship_cx = W // 2
    d.polygon(_burst(ship_cx, waterline - 8, 48, 22, 16), fill=EXPLODE)
    d.polygon(_burst(ship_cx, waterline - 8, 24, 10, 16), fill=EXPLODE_CORE)

    # drone above the ship
    d.line([ship_cx - 22, waterline - 130, ship_cx + 22, waterline - 130], fill=SHIP_GREY, width=3)
    d.ellipse([ship_cx - 12, waterline - 136, ship_cx + 12, waterline - 124], fill=(90, 90, 90))
    for dx, dy in ((-16, -132), (16, -132), (-16, -128), (16, -128)):
        d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(30, 30, 30))

    # warship silhouette grey
    wl = waterline
    d.polygon([(ship_cx - 110, wl), (ship_cx + 110, wl),
               (ship_cx + 92, wl - 30), (ship_cx + 28, wl - 46), (ship_cx - 28, wl - 46),
               (ship_cx - 92, wl - 30)], fill=SHIP_GREY)
    d.rectangle([ship_cx + 18, wl - 78, ship_cx + 72, wl - 46], fill=SHIP_GREY)   # bridge
    d.rectangle([ship_cx + 18, wl - 84, ship_cx + 72, wl - 78], fill=SHIP_GREY)   # bridge roof
    d.rectangle([ship_cx - 56, wl - 52, ship_cx - 38, wl - 46], fill=SHIP_GREY)   # funnel

    # hero headline with dark backing strip sized from actual text
    f, sz = fit_size(d, "UKRAINE SINKS RUSSIAN", FONT_SANS_B, W - 180, 40)
    line_h = int(sz * 1.35)
    strip_h = 2 * line_h + 24
    rect(d, 30, h0 + 14, W - 30, h0 + 14 + strip_h, NAVY_DARK, radius=8)
    draw_text(d, (W / 2, h0 + 26), ["UKRAINE SINKS RUSSIAN"], FONT_SANS_B, sz, WHITE)
    draw_text(d, (W / 2, h0 + 26 + line_h), ["WARSHIP OFF LIBYA"], FONT_SANS_B, sz, WHITE)

    # hero subline: just below the headline strip, clear of the ship art
    sub = "Seven naval drones sank the corvette Merkury at Benghazi; cargo ship Angara also hit."
    lines = wrap_lines(d, sub, FONT_SANS, 16, W - 140)
    draw_text(d, (W / 2, h0 + 14 + strip_h + 12), lines, FONT_SANS, 16, WHITE)

    # ---------------- 2x2 grid ----------------
    g0, card_w, card_h, gap = 450, 495, 200, 12
    xs = [12, 12 + card_w + gap]
    ys = [g0, g0 + card_h + gap]

    cards = [
        dict(strip=STRIP_NAVY, icon=icon_skyscraper,
             head="HOUTHI DRONE HITS RIYADH'S TALLEST TOWER",
             sub="Second strike in a week on the PIF Tower; 11 wounded."),
        dict(strip=STRIP_RED, icon=icon_medal,
             head="TRUMP PARDONS TURKEYS FREEDOM & FEATHERS",
             sub="Medal of Freedom for Rudy Giuliani the same day."),
        dict(strip=STRIP_GREY, icon=icon_courthouse,
             head="SARKOZY AND BRUNI ORDERED TO TRIAL",
             sub="Ex-president and wife face trial over Libya case."),
        dict(strip=STRIP_GREEN, icon=icon_football,
             head="REAL MADRID HIT PSV FOR FIVE",
             sub="Bellingham stunner, Mbappe brace in 5-1 win."),
    ]

    for pos, card in enumerate(cards):
        x0 = xs[pos % 2]
        y0 = ys[pos // 2]
        x1, y1 = x0 + card_w, y0 + card_h
        rect(d, x0, y0, x1, y1, CARD, radius=6)
        rect(d, x0, y0, x1, y0 + 10, card["strip"])
        card["icon"](d, x0 + 50, y0 + 88, 56)
        tx = x0 + 110
        tw = x1 - tx - 16
        f, sz = fit_size(d, card["head"], FONT_SANS_B, tw, 22)
        head_lines = wrap_lines(d, card["head"], FONT_SANS_B, sz, tw)
        # keep headline to at most 2 lines by shrinking if needed
        while len(head_lines) > 2 and sz > 14:
            sz -= 1
            f = font(FONT_SANS_B, sz)
            head_lines = wrap_lines(d, card["head"], FONT_SANS_B, sz, tw)
        draw_text(d, (tx + tw / 2, y0 + 28), head_lines, FONT_SANS_B, sz, TEXT_DARK)
        f, sz = fit_size(d, card["sub"], FONT_SANS, tw, 16)
        sub_lines = wrap_lines(d, card["sub"], FONT_SANS, sz, tw)
        while len(sub_lines) > 2 and sz > 11:
            sz -= 1
            f = font(FONT_SANS, sz)
            sub_lines = wrap_lines(d, card["sub"], FONT_SANS, sz, tw)
        draw_text(d, (tx + tw / 2, y0 + 28 + len(head_lines) * int(sz * 1.45) + 14),
                  sub_lines, FONT_SANS, sz, TEXT_MUTE)

    # ---------------- Bottom strip ----------------
    b0, b1 = 870, 940
    rect(d, 0, b0, W, b1, BOTTOM)
    also = "ALSO: NATO early-warning aircraft for Poland   •   Iran faces winter gas crisis   •   UN warns over Gaza hardship"
    f, sz = fit_size(d, also, FONT_SANS, W - 80, 17)
    draw_text(d, (W / 2, b0 + (b1 - b0) / 2 - sz / 2 + 2), [also], FONT_SANS, sz, TEXT_DARK)

    # ---------------- Footer ----------------
    foot = "25 NOVEMBER 2026 — THE DAY IN ONE IMAGE"
    f, sz = fit_size(d, foot, FONT_SANS_B, W - 80, 22)
    draw_text(d, (W / 2, 970), [foot], FONT_SANS_B, sz, TEXT_DARK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


def _burst(cx, cy, rout, rin, n):
    pts = []
    for i in range(2 * n):
        a = math.radians(i * 180 / n - 90)
        r = rout if i % 2 == 0 else rin
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


if __name__ == "__main__":
    main()