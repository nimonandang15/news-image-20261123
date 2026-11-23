#!/usr/bin/env python3
"""Monday 23 November 2026, the world in one image.

Builds a 1024 by 1024 broadsheet front page with PIL and the DejaVu
faces, then saves it as entry.png. Running the script twice gives the
same bytes both times: every random choice is seeded, and PIL stores
no timestamps in the PNG it writes.

The six stories on the page, all checked against live reporting on
Monday 23 November 2026 (AP, Reuters, AFP, BBC, Al Jazeera, CNN,
Politico):

- COP31 ends with no deal. The Antalya summit closes on Sunday after
  44 hours of overtime, the longest climate summit ever, and the final
  "Antalya Pact" draft never once says "fossil fuels". The EU walks
  away; the UN secretary-general is deeply disappointed.
- The Gulf war widens. Houthis hit Riyadh for a third day running,
  at least 25 tankers have been struck in or near the Strait of
  Hormuz inside a week, and the Saudi-led coalition shoots down a
  Houthi missile.
- A Russian drone hits a block of flats in Dymer, near Kyiv, and 14
  people are missing. The Sparta II is still on fire off Finland.
- A candy factory burns in Banten, Indonesia: three dead, 36 workers
  still missing as rescuers dig through the rubble.
- South Korea's education minister resigns over an AI exam-cheating
  scandal.
- BepiColombo slips into orbit around Mercury after eight years of
  travel, only the second mission ever to do so.
"""
import math
import random
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 44
PAPER_RGB = (247, 242, 230)
INK_RGB = (20, 18, 16)
CRIMSON_RGB = (198, 12, 48)
NAVY_RGB = (24, 38, 68)
TEAL_RGB = (13, 102, 102)
OCHRE_RGB = (178, 108, 0)
SKY_RGB = (36, 110, 168)
GREY_RGB = (96, 90, 80)
WHITE_RGB = (255, 255, 255)
GOLD_RGB = (214, 164, 32)
MIDNIGHT_RGB = (16, 24, 48)
EMBER_RGB = (232, 116, 0)
LEAF_RGB = (34, 120, 60)
PALE_RGB = (232, 226, 210)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


@lru_cache(maxsize=None)
def typeface(path, size):
    return ImageFont.truetype(FONT_DIR + path, size)


def sans_bold(size):
    return typeface("DejaVuSans-Bold.ttf", size)


def sans(size):
    return typeface("DejaVuSans.ttf", size)


def serif_bold(size):
    return typeface("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return typeface("DejaVuSerif.ttf", size)


def split_lines(canvas, words, face, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines = []
    current = ""
    for word in words.split():
        trial = word if not current else current + " " + word
        if canvas.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def block(canvas, text, face, x, y, width, fill, spacing=None, limit=None):
    """Draw a wrapped paragraph; return the y just under its last line."""
    gap = spacing if spacing is not None else int(face.size * 1.28)
    rows = split_lines(canvas, text, face, width)
    if limit is not None:
        rows = rows[:limit]
    for row in rows:
        canvas.text((x, y), row, font=face, fill=fill)
        y += gap
    return y


def hrule(canvas, y, colour, thick=2, x0=None, x1=None):
    left = EDGE if x0 is None else x0
    right = PAGE - EDGE if x1 is None else x1
    canvas.line([(left, y), (right, y)], fill=colour, width=thick)


def star(canvas, cx, cy, radius, colour):
    """Eight-spike starburst with a filled centre."""
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        canvas.line(
            [(cx, cy),
             (cx + int(radius * math.cos(radians)),
              cy + int(radius * math.sin(radians)))],
            fill=colour, width=5)
    half = radius // 2
    canvas.ellipse([cx - half, cy - half, cx + half, cy + half],
                   fill=colour)


def story_card(canvas, box, kicker, kicker_rgb, head, body):
    """One white card with a kicker, a serif headline and body copy."""
    x, y, w, h = box
    canvas.rectangle([x, y, x + w, y + h], outline=INK_RGB, width=2,
                     fill=WHITE_RGB)
    inner_x, inner_y = x + 16, y + 14
    inner_w = w - 32
    canvas.text((inner_x, inner_y), kicker, font=sans_bold(14),
                fill=kicker_rgb)
    inner_y += 22
    inner_y = block(canvas, head, serif_bold(25), inner_x, inner_y,
                    inner_w, INK_RGB, spacing=int(25 * 1.12), limit=2)
    inner_y += 4
    inner_y = block(canvas, body, sans(16), inner_x, inner_y, inner_w,
                    INK_RGB, spacing=int(16 * 1.3), limit=4)
    if inner_y > y + h - 8:
        print("WARNING: %s overflows by %dpx"
              % (kicker, inner_y - (y + h - 8)))


GRID_STORIES = [
    ("MIDDLE EAST  \u2022  THE GULF", CRIMSON_RGB,
     "Gulf war widens as tankers are hit",
     "Houthis strike Riyadh for a third straight day; at least "
     "25 tankers have been hit in and around the Strait of "
     "Hormuz in a week. The Saudi-led coalition intercepts a "
     "Houthi missile."),
    ("UKRAINE  \u2022  KYIV REGION", NAVY_RGB,
     "Drone hits flats near Kyiv; 14 missing",
     "A Russian drone strikes an apartment block in Dymer, "
     "leaving 14 people missing. The Sparta II is still "
     "burning off Finland after a drone attack."),
    ("ASIA  \u2022  INDONESIA", EMBER_RGB,
     "Factory fire: dozens missing",
     "Three people are dead after a candy factory fire in "
     "Banten province. Rescuers are searching for 36 workers "
     "still missing in the rubble."),
    ("ASIA  \u2022  SOUTH KOREA", OCHRE_RGB,
     "Minister quits over AI exam scandal",
     "South Korea\u2019s education minister resigns amid an "
     "AI-driven exam cheating scandal that has shaken the "
     "country\u2019s university entrance system."),
]


def draw_poster():
    sheet = Image.new("RGB", (PAGE, PAGE), PAPER_RGB)
    canvas = ImageDraw.Draw(sheet)

    # Masthead.
    canvas.text((EDGE, 24), "THE WORLD IN ONE DAY",
                font=serif_bold(56), fill=INK_RGB)
    hrule(canvas, 96, INK_RGB, 4)
    canvas.text((EDGE, 108), "MONDAY 23 NOVEMBER 2026",
                font=sans_bold(24), fill=CRIMSON_RGB)
    tag = "ONE DAY  \u2022  ONE IMAGE"
    tag_w = canvas.textlength(tag, font=sans_bold(24))
    canvas.text((PAGE - EDGE - tag_w, 108), tag,
                font=sans_bold(24), fill=NAVY_RGB)
    hrule(canvas, 142, INK_RGB, 2)

    # Lead story: COP31, with a cracked globe on a dark panel.
    top = 158
    canvas.text((EDGE, top), "LEAD  \u2022  CLIMATE",
                font=sans_bold(15), fill=CRIMSON_RGB)
    top += 24
    top = block(canvas, "COP31 collapses with no deal",
                serif_bold(38), EDGE, top, 580, INK_RGB, spacing=44,
                limit=2)
    top += 8
    top = block(canvas,
                "The UN climate summit in Antalya, Turkey, ends "
                "Sunday with no agreement \u2014 the longest summit "
                "in history. The final draft did not mention "
                "fossil fuels once.",
                sans(18), EDGE, top, 560, INK_RGB, spacing=24, limit=4)
    art_x0, art_y0 = 640, 158
    art_x1, art_y1 = PAGE - EDGE, 386
    panel = Image.new("RGB", (art_x1 - art_x0, art_y1 - art_y0),
                      (12, 40, 44))
    art = ImageDraw.Draw(panel)
    globe_cx, globe_cy, globe_r = 160, 108, 72
    art.ellipse([globe_cx - globe_r, globe_cy - globe_r,
                 globe_cx + globe_r, globe_cy + globe_r],
                fill=TEAL_RGB, outline=GOLD_RGB, width=3)
    art.ellipse([globe_cx - globe_r // 2, globe_cy - globe_r,
                 globe_cx + globe_r // 2, globe_cy + globe_r],
                outline=(90, 180, 180), width=2)
    art.line([(globe_cx - globe_r, globe_cy),
              (globe_cx + globe_r, globe_cy)],
             fill=(90, 180, 180), width=2)
    art.arc([globe_cx - globe_r, globe_cy - globe_r // 2,
             globe_cx + globe_r, globe_cy + globe_r // 2],
            200, 340, fill=(90, 180, 180), width=2)
    crack = [(globe_cx - 52, globe_cy - 66),
             (globe_cx - 18, globe_cy - 30),
             (globe_cx - 40, globe_cy + 2),
             (globe_cx + 6, globe_cy + 34),
             (globe_cx - 8, globe_cy + 66),
             (globe_cx + 30, globe_cy + 74)]
    art.line(crack, fill=CRIMSON_RGB, width=6)
    art.line(crack, fill=WHITE_RGB, width=2)
    for seat in range(5):
        seat_x = 28 + seat * 62
        seat_top = art_y1 - art_y0 - 52
        art.rectangle([seat_x, seat_top, seat_x + 34, seat_top + 22],
                      outline=(120, 140, 150), width=2)
        art.line([(seat_x + 4, seat_top + 22),
                  (seat_x + 4, seat_top + 38)],
                 fill=(120, 140, 150), width=2)
        art.line([(seat_x + 30, seat_top + 22),
                  (seat_x + 30, seat_top + 38)],
                 fill=(120, 140, 150), width=2)
    art.rectangle([0, art_y1 - art_y0 - 26, art_x1 - art_x0,
                   art_y1 - art_y0], fill=(10, 16, 32))
    art.text((12, art_y1 - art_y0 - 22),
             "Antalya  \u2022  44 hours overtime  \u2022  no deal",
             font=sans_bold(14), fill=WHITE_RGB)
    sheet.paste(panel, (art_x0, art_y0))
    canvas.rectangle([art_x0, art_y0, art_x1, art_y1],
                     outline=INK_RGB, width=2)
    canvas.text((EDGE, 398),
                "EU: \u201cIt is unconscionable that a climate pact "
                "would make no mention of fossil fuels.\u201d",
                font=serif(16), fill=GREY_RGB)
    hrule(canvas, 428, INK_RGB, 2)

    # Two rows of two story cards.
    grid_y = 446
    card_w, card_h = 452, 196
    second_x = EDGE + card_w + 32
    for index, (kicker, tint, head, body) in enumerate(GRID_STORIES):
        col = index % 2
        row = index // 2
        story_card(canvas,
                   (EDGE if col == 0 else second_x,
                    grid_y + row * (card_h + 14),
                    card_w, card_h),
                   kicker, tint, head, body)

    # Bottom strip: BepiColombo at Mercury.
    strip_y = grid_y + 2 * card_h + 14 + 14
    strip_h = 104
    canvas.rectangle([EDGE, strip_y, PAGE - EDGE, strip_y + strip_h],
                     outline=INK_RGB, width=2, fill=WHITE_RGB)
    sky_x0, sky_x1 = PAGE - EDGE - 300, PAGE - EDGE
    canvas.rectangle([sky_x0, strip_y, sky_x1, strip_y + strip_h],
                     fill=MIDNIGHT_RGB)
    rng = random.Random(20261123)
    for _ in range(22):
        speck_x = rng.randint(sky_x0 + 6, sky_x1 - 6)
        speck_y = rng.randint(strip_y + 6, strip_y + strip_h - 6)
        canvas.ellipse([speck_x - 1, speck_y - 1, speck_x + 1, speck_y + 1],
                       fill=WHITE_RGB)
    planet_cx = sky_x0 + 150
    planet_cy = strip_y + strip_h // 2
    planet_r = 30
    canvas.ellipse([planet_cx - planet_r, planet_cy - planet_r,
                    planet_cx + planet_r, planet_cy + planet_r],
                   fill=(216, 160, 110), outline=(160, 110, 70), width=2)
    for off_x, off_y, crater_r in ((-12, -8, 6), (10, 4, 8),
                                   (-4, 12, 5), (14, -12, 4)):
        canvas.ellipse([planet_cx + off_x - crater_r,
                        planet_cy + off_y - crater_r,
                        planet_cx + off_x + crater_r,
                        planet_cy + off_y + crater_r],
                       outline=(160, 110, 70), width=2)
    canvas.text((EDGE + 16, strip_y + 10), "SPACE  \u2022  MERCURY",
                font=sans_bold(14), fill=SKY_RGB)
    block(canvas, "BepiColombo reaches Mercury", serif_bold(26),
          EDGE + 16, strip_y + 34, 560, INK_RGB, spacing=30, limit=1)
    block(canvas,
          "The Europe-Japan probe enters orbit after an "
          "eight-year journey \u2014 only the second mission "
          "ever to orbit the planet.",
          sans(15), EDGE + 16, strip_y + 66, 560, INK_RGB, spacing=18,
          limit=2)

    # Footer: the day's other briefs, then the sources.
    foot_y = strip_y + strip_h + 10
    hrule(canvas, foot_y, INK_RGB, 2)
    canvas.text((EDGE, foot_y + 8),
                "Also: Pentagon releases 43 more UAP files  \u2022  "
                "Democrats win a historic 258-seat majority  \u2022  UN "
                "lethal-AI talks continue, no binding rules",
                font=sans(13), fill=GREY_RGB)
    canvas.text((EDGE, foot_y + 27),
                "Sources: AP, Reuters, AFP, BBC, Al Jazeera, "
                "CNN, Politico \u2014 23 Nov 2026  \u2022  Six stories, "
                "one day. Drawn from live reporting; no invented facts.",
                font=sans(13), fill=GREY_RGB)

    sheet.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    draw_poster()
