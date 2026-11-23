#!/usr/bin/env python3
"""Render the 23 November 2026 world-news poster (1024x1024 PNG).

A broadsheet front page drawn with PIL + DejaVu only. Deterministic:
same script, same bytes (PIL writes no timestamps into PNG data).

Stories verified against live reporting on Monday 23 Nov 2026
(AP, Reuters, AFP, BBC, Al Jazeera, CNN, Politico):
- COP31 collapses with no deal: the UN climate summit in Antalya,
  Turkey, ends Sunday with no agreement - the longest summit in
  history, 44+ hours overtime. The final "Antalya Pact" draft did
  not mention fossil fuels once; the EU refused it, the UN chief
  is "deeply disappointed".
- Gulf war widens: Houthis strike Riyadh for a third straight day;
  at least 25 tankers hit in and around the Strait of Hormuz in
  seven days; the Saudi-led coalition intercepts a Houthi missile.
- Ukraine: a Russian drone hits an apartment block in Dymer near
  Kyiv, 14 people missing; the Sparta II is still burning off
  Finland after a drone strike.
- BepiColombo reaches Mercury: the Europe-Japan probe enters orbit
  after an eight-year journey; only the second mission to orbit
  the planet.
- Indonesia factory fire: 3 dead, dozens missing after a candy
  factory fire in Banten; rescuers search for 36 missing.
- South Korea: the education minister resigns amid an AI-driven
  exam cheating scandal.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 230)
INK = (20, 18, 16)
NAVY = (24, 38, 68)
RED = (198, 12, 48)
TEAL = (13, 102, 102)
AMBER = (178, 108, 0)
SKY = (36, 110, 168)
GREY = (96, 90, 80)
CARD = (255, 255, 255)
GOLD = (214, 164, 32)
NIGHT = (16, 24, 48)
ORANGE = (232, 116, 0)
GREEN = (34, 120, 60)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


FB = lambda s: font("DejaVuSans-Bold.ttf", s)
FR = lambda s: font("DejaVuSans.ttf", s)
FSB = lambda s: font("DejaVuSerif-Bold.ttf", s)
FSR = lambda s: font("DejaVuSerif.ttf", s)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, max_w, fill, leading=None, max_lines=None):
    """Draw wrapped text; return y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def burst(d, cx, cy, r, color):
    """Starburst: 8 spikes + filled core."""
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(cx, cy), (cx + int(r * math.cos(a)),
                           cy + int(r * math.sin(a)))],
               fill=color, width=5)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
              fill=color)


def card(d, x, y, w, h, kicker_text, kicker_color, headline_text,
         body_text, head_size=25, body_size=16, head_lines=2,
         body_lines=4):
    """One story card; returns bottom y. Warns if text would overflow."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=CARD)
    ix, iy = x + 16, y + 14
    iw = w - 32
    d.text((ix, iy), kicker_text, font=FB(14), fill=kicker_color)
    iy += 22
    iy = para(d, headline_text, FSB(head_size), ix, iy, iw, INK,
              leading=int(head_size * 1.12), max_lines=head_lines)
    iy += 4
    iy = para(d, body_text, FR(body_size), ix, iy, iw, INK,
              leading=int(body_size * 1.3), max_lines=body_lines)
    if iy > y + h - 8:
        print(f"WARNING: card '{kicker_text}' overflows by "
              f"{iy - (y + h - 8)}px")
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44  # margin

    # ---- Masthead ----
    d.text((M, 24), "THE WORLD IN ONE DAY", font=FSB(56), fill=INK)
    rule(d, M, 96, W - M, INK, 4)
    d.text((M, 108), "MONDAY 23 NOVEMBER 2026", font=FB(24), fill=RED)
    right_tag = "ONE DAY  \u2022  ONE IMAGE"
    d.text((W - M - d.textlength(right_tag, font=FB(24)), 108),
           right_tag, font=FB(24), fill=NAVY)
    rule(d, M, 142, W - M, INK, 2)

    # ---- Lead story: COP31 collapses, with cracked-globe illustration ----
    y = 158
    d.text((M, y), "LEAD  \u2022  CLIMATE", font=FB(15), fill=RED)
    y += 24
    y = para(d, "COP31 collapses with no deal",
             FSB(38), M, y, 580, INK, leading=44, max_lines=2)
    y += 8
    y = para(d, "The UN climate summit in Antalya, Turkey, ends "
                "Sunday with no agreement \u2014 the longest summit "
                "in history. The final draft did not mention "
                "fossil fuels once.",
             FR(18), M, y, 560, INK, leading=24, max_lines=4)
    # illustration: dark hall, cracked globe, NO DEAL stamp — drawn on
    # its own layer so nothing can spill past the box edge.
    ix0, iy0, ix1, iy1 = 640, 158, W - M, 386
    art = Image.new("RGB", (ix1 - ix0, iy1 - iy0), (12, 40, 44))
    a = ImageDraw.Draw(art)
    # globe
    cx, cy, r = 160, 108, 72
    a.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL,
              outline=GOLD, width=3)
    a.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
              outline=(90, 180, 180), width=2)
    a.line([(cx - r, cy), (cx + r, cy)], fill=(90, 180, 180), width=2)
    a.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
          fill=(90, 180, 180), width=2)
    # crack across the globe
    crack = [(cx - 52, cy - 66), (cx - 18, cy - 30), (cx - 40, cy + 2),
             (cx + 6, cy + 34), (cx - 8, cy + 66), (cx + 30, cy + 74)]
    a.line(crack, fill=RED, width=6)
    a.line(crack, fill=(255, 255, 255), width=2)
    # empty chairs row at the bottom of the hall
    for i in range(5):
        x0 = 28 + i * 62
        a.rectangle([x0, iy1 - iy0 - 52, x0 + 34, iy1 - iy0 - 30],
                    outline=(120, 140, 150), width=2)
        a.line([(x0 + 4, iy1 - iy0 - 30), (x0 + 4, iy1 - iy0 - 14)],
               fill=(120, 140, 150), width=2)
        a.line([(x0 + 30, iy1 - iy0 - 30), (x0 + 30, iy1 - iy0 - 14)],
               fill=(120, 140, 150), width=2)
    a.rectangle([0, iy1 - iy0 - 26, ix1 - ix0, iy1 - iy0],
                fill=(10, 16, 32))
    a.text((12, iy1 - iy0 - 22), "Antalya  \u2022  44 hours overtime  \u2022  no deal",
           font=FB(14), fill=CARD)
    img.paste(art, (ix0, iy0))
    d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=2)
    d.text((M, 398), "EU: \u201cIt is unconscionable that a climate pact "
           "would make no mention of fossil fuels.\u201d",
           font=FSR(16), fill=GREY)
    rule(d, M, 428, W - M, INK, 2)

    # ---- Grid: 2 x 2 ----
    gy = 446
    gw, gh = 452, 196
    gx2 = M + gw + 32
    card(d, M, gy, gw, gh, "MIDDLE EAST  \u2022  THE GULF", RED,
         "Gulf war widens as tankers are hit",
         "Houthis strike Riyadh for a third straight day; at least "
         "25 tankers have been hit in and around the Strait of "
         "Hormuz in a week. The Saudi-led coalition intercepts a "
         "Houthi missile.", head_lines=2, body_lines=4)
    card(d, gx2, gy, gw, gh, "UKRAINE  \u2022  KYIV REGION", NAVY,
         "Drone hits flats near Kyiv; 14 missing",
         "A Russian drone strikes an apartment block in Dymer, "
         "leaving 14 people missing. The Sparta II is still "
         "burning off Finland after a drone attack.",
         head_lines=2, body_lines=4)
    gy += gh + 14
    card(d, M, gy, gw, gh, "ASIA  \u2022  INDONESIA", ORANGE,
         "Factory fire: dozens missing",
         "Three people are dead after a candy factory fire in "
         "Banten province. Rescuers are searching for 36 workers "
         "still missing in the rubble.",
         head_lines=2, body_lines=4)
    card(d, gx2, gy, gw, gh, "ASIA  \u2022  SOUTH KOREA", AMBER,
         "Minister quits over AI exam scandal",
         "South Korea\u2019s education minister resigns amid an "
         "AI-driven exam cheating scandal that has shaken the "
         "country\u2019s university entrance system.",
         head_lines=2, body_lines=4)

    # ---- Bottom strip: BepiColombo reaches Mercury ----
    by = gy + gh + 14
    bh = 104
    d.rectangle([M, by, W - M, by + bh], outline=INK, width=2, fill=CARD)
    bx0, bx1 = W - M - 300, W - M
    d.rectangle([bx0, by, bx1, by + bh], fill=NIGHT)
    rnd = random.Random(20261123)
    for _ in range(22):
        sx = rnd.randint(bx0 + 6, bx1 - 6)
        sy = rnd.randint(by + 6, by + bh - 6)
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=CARD)
    # Mercury: cratered disc
    mx, my, mr = bx0 + 150, by + bh // 2, 30
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(216, 160, 110),
              outline=(160, 110, 70), width=2)
    for (ox, oy, cr) in ((-12, -8, 6), (10, 4, 8), (-4, 12, 5), (14, -12, 4)):
        d.ellipse([mx + ox - cr, my + oy - cr, mx + ox + cr, my + oy + cr],
                  outline=(160, 110, 70), width=2)
    d.text((M + 16, by + 10), "SPACE  \u2022  MERCURY",
           font=FB(14), fill=SKY)
    para(d, "BepiColombo reaches Mercury", FSB(26), M + 16, by + 34, 560,
         INK, leading=30, max_lines=1)
    para(d, "The Europe-Japan probe enters orbit after an "
            "eight-year journey \u2014 only the second mission "
            "ever to orbit the planet.",
         FR(15), M + 16, by + 66, 560, INK, leading=18, max_lines=2)

    # ---- Footer ----
    fy = by + bh + 10
    rule(d, M, fy, W - M, INK, 2)
    d.text((M, fy + 8), "Also: Pentagon releases 43 more UAP files  \u2022  "
           "Democrats win a historic House majority  \u2022  UN "
           "lethal-AI talks continue, no binding rules",
           font=FR(13), fill=GREY)
    d.text((M, fy + 27), "Sources: AP, Reuters, AFP, BBC, Al Jazeera, "
           "CNN, Politico \u2014 23 Nov 2026  \u2022  Six stories, "
           "one day. Drawn from live reporting; no invented facts.",
           font=FR(13), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
