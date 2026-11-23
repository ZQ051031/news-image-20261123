#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper-style poster: THE WORLD IN ONE PICTURE.

Six panels summarise the world news of Monday 23 November 2026. Every
pictogram is drawn by hand with Pillow vector shapes -- no external images,
no network, no randomness, no timestamps. Output is fully deterministic:
running the program twice produces byte-identical PNG files.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
TITLE_FONT = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
HEAD_FONT = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
BODY_FONT = os.path.join(FONT_DIR, "DejaVuSans.ttf")

INK = (18, 20, 24)
PAPER = (247, 243, 235)
HEADER_BG = (16, 22, 34)
HEADER_FG = (245, 240, 228)
ACCENT = (214, 48, 49)
MUTED = (96, 100, 108)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_panel(draw, x, y, w, h, bg, tag, tag_bg, headline, body,
               pictogram):
    """One news panel: coloured card, pictogram, headline, body text."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=bg)
    # Pictogram band at the top of the panel.
    pictogram(draw, x, y, w)
    # Kicker tag.
    tag_f = font(HEAD_FONT, 17)
    tw = draw.textlength(tag, font=tag_f)
    draw.rounded_rectangle([x + 16, y + 14, x + 16 + tw + 18, y + 40],
                           radius=8, fill=tag_bg)
    draw.text((x + 25, y + 17), tag, font=tag_f, fill=(255, 255, 255))
    # Headline.
    head_f = font(HEAD_FONT, 25)
    lines = wrap(draw, headline, head_f, w - 32)
    ty = y + 196
    for line in lines:
        draw.text((x + 16, ty), line, font=head_f, fill=INK)
        ty += 30
    # Body.
    body_f = font(BODY_FONT, 18)
    ty += 6
    for line in wrap(draw, body, body_f, w - 32):
        draw.text((x + 16, ty), line, font=body_f, fill=(52, 56, 64))
        ty += 24


# ---------------------------------------------------------------- pictograms
# Each takes (draw, x, y, w) and draws inside the panel's top band
# (y .. y+180, width w). All coordinates are offsets from the panel origin.

def pic_globe(draw, x, y, w):
    cx, cy, r = x + w // 2, y + 96, 62
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 132, 110),
                 outline=(16, 60, 48), width=4)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(247, 243, 235),
                 width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340,
             fill=(247, 243, 235), width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 160,
             fill=(247, 243, 235), width=3)
    draw.line([cx - r + 6, cy, cx + r - 6, cy], fill=(247, 243, 235), width=3)
    draw.line([cx, cy - r + 6, cx, cy + r - 6], fill=(247, 243, 235), width=3)
    # Sun with rays, top right.
    sx, sy = x + w - 52, y + 44
    draw.ellipse([sx - 16, sy - 16, sx + 16, sy + 16], fill=(232, 148, 32))
    for dx, dy in [(0, -28), (0, 28), (-28, 0), (28, 0),
                   (-20, -20), (20, -20), (-20, 20), (20, 20)]:
        draw.line([sx + dx * 0.6, sy + dy * 0.6, sx + dx, sy + dy],
                  fill=(232, 148, 32), width=4)
    # Broken pact: a torn document bottom left.
    draw.polygon([(x + 30, y + 128), (x + 78, y + 128), (x + 78, y + 166),
                  (x + 66, y + 156), (x + 54, y + 166), (x + 42, y + 156),
                  (x + 30, y + 166)], fill=(255, 255, 255),
                 outline=(16, 60, 48), width=3)
    draw.line([x + 38, y + 140, x + 70, y + 140], fill=(214, 48, 49), width=3)
    draw.line([x + 38, y + 149, x + 70, y + 149], fill=(214, 48, 49), width=3)


def pic_tanker(draw, x, y, w):
    # Sea.
    draw.rectangle([x + 16, y + 128, x + w - 16, y + 176], fill=(32, 86, 138))
    for wx in range(x + 24, x + w - 24, 46):
        draw.arc([wx, y + 138, wx + 34, y + 158], 0, 180,
                 fill=(247, 243, 235), width=3)
    # Hull.
    draw.polygon([(x + 60, y + 96), (x + w - 60, y + 96), (x + w - 84, y + 132),
                  (x + 84, y + 132)], fill=(60, 64, 72))
    draw.rectangle([x + 60, y + 88, x + w - 60, y + 100], fill=(214, 48, 49))
    # Containers.
    for i, c in enumerate([(232, 148, 32), (38, 132, 110), (214, 48, 49)]):
        cx0 = x + 92 + i * 52
        draw.rectangle([cx0, y + 58, cx0 + 44, y + 88], fill=c,
                       outline=(18, 20, 24), width=2)
    # Bridge tower.
    draw.rectangle([x + w - 116, y + 52, x + w - 88, y + 88],
                   fill=(247, 243, 235), outline=(18, 20, 24), width=2)
    # Flame above the ship.
    fx, fy = x + w // 2 - 90, y + 30
    draw.polygon([(fx, fy + 26), (fx + 12, fy), (fx + 20, fy + 14),
                  (fx + 30, fy - 6), (fx + 40, fy + 26)],
                 fill=(232, 120, 32))
    # Warning triangle, top right.
    tx, ty = x + w - 66, y + 108
    draw.polygon([(tx, ty), (tx + 34, ty + 52), (tx - 34, ty + 52)],
                 fill=(245, 196, 66), outline=(18, 20, 24), width=2)
    draw.text((tx - 3, ty + 14), "!", font=font(HEAD_FONT, 26),
              fill=(18, 20, 24))


def pic_factory_fire(draw, x, y, w):
    # Factory block.
    draw.rectangle([x + 52, y + 96, x + w - 52, y + 168], fill=(96, 100, 108))
    draw.rectangle([x + 52, y + 96, x + w - 52, y + 110], fill=(60, 64, 72))
    for i in range(4):
        wx0 = x + 70 + i * 56
        draw.rectangle([wx0, y + 122, wx0 + 30, y + 152],
                       fill=(247, 220, 120))
    # Chimney.
    draw.polygon([(x + w - 108, y + 168), (x + w - 108, y + 58),
                  (x + w - 84, y + 58), (x + w - 84, y + 168)],
                 fill=(120, 58, 58))
    # Smoke puffs.
    for i, (sx, sy, sr) in enumerate([(x + w - 96, y + 44, 14),
                                      (x + w - 82, y + 26, 18),
                                      (x + w - 60, y + 14, 12)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(170, 172, 178))
    # Big flame rising from the roof.
    fx = x + w // 2 - 16
    draw.polygon([(fx - 34, y + 100), (fx - 8, y + 44), (fx + 2, y + 66),
                  (fx + 18, y + 30), (fx + 34, y + 64), (fx + 42, y + 100)],
                 fill=(232, 120, 32))
    draw.polygon([(fx - 14, y + 100), (fx - 2, y + 66), (fx + 6, y + 82),
                  (fx + 16, y + 60), (fx + 20, y + 100)],
                 fill=(245, 196, 66))


def pic_quake(draw, x, y, w):
    # Seismograph trace.
    pts = []
    base = y + 84
    xs = list(range(x + 24, x + w - 24, 12))
    amps = [0, 4, -3, 6, -5, 34, -42, 26, -18, 8, -6, 4, -3, 2, 0, 3, -2, 0]
    for i, px in enumerate(xs):
        pts.append((px, base + amps[i % len(amps)]))
    draw.line(pts, fill=(214, 48, 49), width=4, joint="curve")
    # Cracked ground.
    draw.polygon([(x + 24, y + 150), (x + 96, y + 118), (x + 150, y + 150),
                  (x + 196, y + 122), (x + w - 40, y + 150),
                  (x + w - 24, y + 176), (x + 24, y + 176)],
                 fill=(146, 104, 60))
    draw.line([(x + 96, y + 118), (x + 116, y + 142), (x + 104, y + 176)],
              fill=(60, 40, 20), width=4)
    draw.line([(x + 196, y + 122), (x + 176, y + 148), (x + 188, y + 176)],
              fill=(60, 40, 20), width=4)
    # Tilted house.
    hx, hy = x + 150, y + 96
    draw.polygon([(hx, hy - 22), (hx + 34, hy), (hx - 34, hy)],
                 fill=(120, 58, 58))
    draw.rectangle([hx - 26, hy, hx + 26, hy + 28], fill=(247, 243, 235),
                   outline=(18, 20, 24), width=2)
    draw.rectangle([hx - 6, hy + 10, hx + 6, hy + 28], fill=(60, 64, 72))
    # Power pylon, leaning.
    px0, py0 = x + 60, y + 120
    draw.line([px0, py0, px0 + 22, py0 - 62], fill=(40, 44, 52), width=5)
    draw.line([px0 + 8, py0, px0 + 34, py0 - 58], fill=(40, 44, 52), width=4)
    draw.line([px0 - 8, py0 - 40, px0 + 40, py0 - 46], fill=(40, 44, 52),
              width=4)
    # "6.7" magnitude badge.
    draw.rounded_rectangle([x + w - 96, y + 20, x + w - 24, y + 52],
                           radius=8, fill=(18, 20, 24))
    draw.text((x + w - 86, y + 25), "M 6.7", font=font(HEAD_FONT, 20),
              fill=(245, 196, 66))


def pic_drone_ship(draw, x, y, w):
    # Night sky band.
    draw.rectangle([x + 16, y + 16, x + w - 16, y + 118], fill=(24, 38, 58))
    for sx, sy in [(x + 40, y + 30), (x + 90, y + 52), (x + 140, y + 28),
                    (x + 200, y + 44), (x + 250, y + 30), (x + 280, y + 56)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(247, 243, 235))
    # Drone silhouette.
    dx, dy = x + w // 2, y + 58
    draw.ellipse([dx - 26, dy - 10, dx + 26, dy + 10], fill=(200, 204, 210))
    for ox in (-34, 34):
        draw.ellipse([dx + ox - 14, dy - 6, dx + ox + 14, dy + 6],
                     fill=(140, 144, 152))
        draw.line([dx + ox - 20, dy, dx + ox + 20, dy], fill=(247, 243, 235),
                  width=2)
    draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(214, 48, 49))
    # Searchlight beam down to the sea.
    draw.polygon([(dx - 8, dy + 10), (dx + 8, dy + 10), (dx + 34, y + 118),
                  (dx - 34, y + 118)], fill=(245, 196, 66))
    # Burning ship on the water.
    draw.rectangle([x + 16, y + 128, x + w - 16, y + 176], fill=(32, 86, 138))
    draw.polygon([(x + 64, y + 118), (x + w - 64, y + 118),
                  (x + w - 88, y + 148), (x + 88, y + 148)],
                 fill=(60, 64, 72))
    draw.rectangle([x + 130, y + 92, x + 158, y + 118], fill=(247, 243, 235),
                   outline=(18, 20, 24), width=2)
    fx = x + w // 2 + 40
    draw.polygon([(fx - 22, y + 118), (fx - 4, y + 78), (fx + 4, y + 96),
                  (fx + 16, y + 70), (fx + 26, y + 118)],
                 fill=(232, 120, 32))


def pic_sport_film(draw, x, y, w):
    # Football, left.
    cx, cy, r = x + 84, y + 96, 56
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=(18, 20, 24), width=4)
    draw.polygon([(cx, cy - 16), (cx + 15, cy - 5), (cx + 9, cy + 13),
                  (cx - 9, cy + 13), (cx - 15, cy - 5)], fill=(18, 20, 24))
    for px, py in [(cx, cy - 44), (cx + 42, cy - 14), (cx + 26, cy + 38),
                   (cx - 26, cy + 38), (cx - 42, cy - 14)]:
        draw.line([cx, cy, px, py], fill=(18, 20, 24), width=3)
    # Scoreboard.
    sb_f = font(HEAD_FONT, 19)
    sb_text = "LIV 4-0 MUN"
    sb_x0, sb_x1 = x + 158, x + w - 16
    draw.rounded_rectangle([sb_x0, y + 40, sb_x1, y + 84], radius=8,
                           fill=(16, 60, 48))
    sb_tw = draw.textlength(sb_text, font=sb_f)
    draw.text((sb_x0 + (sb_x1 - sb_x0 - sb_tw) / 2, y + 50), sb_text,
              font=sb_f, fill=(255, 255, 255))
    # Golden trophy, right.
    tx, ty = x + w - 78, y + 128
    draw.polygon([(tx - 26, ty - 24), (tx - 26, ty + 6), (tx - 10, ty + 6),
                  (tx - 6, ty + 26), (tx + 6, ty + 26), (tx + 10, ty + 6),
                  (tx + 26, ty + 6), (tx + 26, ty - 24)],
                 fill=(232, 178, 32))
    draw.arc([tx - 40, ty - 26, tx - 10, ty + 4], 90, 270,
             fill=(232, 178, 32), width=6)
    draw.arc([tx + 10, ty - 26, tx + 40, ty + 4], 270, 90,
             fill=(232, 178, 32), width=6)
    draw.rectangle([tx - 14, ty + 26, tx + 14, ty + 34], fill=(180, 134, 16))
    draw.rectangle([tx - 22, ty + 34, tx + 22, ty + 42], fill=(180, 134, 16))
    # Film reel, bottom left of the band.
    rx, ry = x + 190, y + 136
    draw.ellipse([rx - 26, ry - 26, rx + 26, ry + 26], fill=(60, 64, 72),
                 outline=(18, 20, 24), width=3)
    for a in range(0, 360, 60):
        import math
        px = rx + int(15 * math.cos(math.radians(a)))
        py = ry + int(15 * math.sin(math.radians(a)))
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(247, 243, 235))
    draw.ellipse([rx - 5, ry - 5, rx + 5, ry + 5], fill=(232, 178, 32))


# ------------------------------------------------------------------ panels

PANELS = [
    dict(bg=(226, 240, 232), tag="CLIMATE", tag_bg=(38, 132, 110),
         headline="COP31 collapses in Antalya",
         body=("Talks end with no pact after record overtime. "
               "Fossil-fuel language is stripped from the text as "
               "delegates leave empty-handed."),
         pic=pic_globe),
    dict(bg=(224, 234, 245), tag="MIDDLE EAST", tag_bg=(32, 86, 138),
         headline="Tanker attacks in the Strait of Hormuz",
         body=("A sailor is missing after strikes on shipping. "
               "Trump warns of fresh US strikes on Iran after "
               "1 January."),
         pic=pic_tanker),
    dict(bg=(250, 232, 224), tag="INDONESIA", tag_bg=(190, 74, 32),
         headline="Candy-factory fire in Banten",
         body=("Three dead and around 30 people missing after a "
               "blaze sweeps a candy factory in Banten province."),
         pic=pic_factory_fire),
    dict(bg=(244, 236, 220), tag="PERU", tag_bg=(146, 104, 60),
         headline="Magnitude 6.7 quake hits Junin",
         body=("One dead, 16 injured and about 93,000 homes "
               "without power after a powerful quake in central "
               "Peru."),
         pic=pic_quake),
    dict(bg=(228, 232, 240), tag="UKRAINE / BALTIC", tag_bg=(52, 64, 96),
         headline="Drones over Kyiv, ship ablaze off Finland",
         body=("A Russian drone strike leaves 14 missing in the "
               "Kyiv region, while a Russian cargo ship burns "
               "off Finland."),
         pic=pic_drone_ship),
    dict(bg=(232, 242, 228), tag="SPORT & FILM", tag_bg=(90, 130, 48),
         headline="Liverpool 4-0 in Pochettino debut",
         body=("Liverpool thrash Manchester United 4-0 as "
               "Pochettino takes charge. At the Golden Horse "
               "Awards, Angela Yuen and Anson Kong win."),
         pic=pic_sport_film),
]


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Header band.
    draw.rectangle([0, 0, W, 118], fill=HEADER_BG)
    draw.rectangle([0, 118, W, 122], fill=ACCENT)
    title_f = font(TITLE_FONT, 44)
    title = "THE WORLD IN ONE PICTURE"
    draw.text(((W - draw.textlength(title, font=title_f)) / 2, 16),
              title, font=title_f, fill=HEADER_FG)
    sub_f = font(BODY_FONT, 21)
    sub = "MONDAY 23 NOVEMBER 2026  |  SIX STORIES, ONE PAGE"
    draw.text(((W - draw.textlength(sub, font=sub_f)) / 2, 72),
              sub, font=sub_f, fill=(190, 196, 208))

    # 3 x 2 grid of panels.
    margin, gutter = 16, 12
    pw = (W - 2 * margin - 2 * gutter) // 3
    ph = (H - 122 - margin - gutter - 32) // 2
    for i, p in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = margin + col * (pw + gutter)
        y = 122 + margin + row * (ph + gutter)
        draw_panel(draw, x, y, pw, ph, p["bg"], p["tag"], p["tag_bg"],
                   p["headline"], p["body"], p["pic"])

    # Footer.
    foot_f = font(BODY_FONT, 15)
    foot = "Hand-drawn with Python + Pillow  |  No photographs, no network"
    draw.text(((W - draw.textlength(foot, font=foot_f)) / 2, H - 26),
              foot, font=foot_f, fill=MUTED)

    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG", optimize=True)
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
