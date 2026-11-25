#!/usr/bin/env python3
"""Build the front page for Tuesday 24 November 2026.

Draws a 1024x1024 newspaper front page with Pillow: masthead, numbers
strip, seven featured stories with full decks, a drawn world map with
markers, a UTC timeline, a numbered list of stories 8-40 grouped by
region, and a DATE CHECK box. Deterministic: no randomness, no network,
no timestamps.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (122, 31, 31)
BLACK = (15, 15, 15)
TEAL = (15, 92, 92)
GREY = (110, 110, 105)
LIGHT_LINE = (205, 198, 182)
WHITE = (255, 255, 255)
OCEAN = (234, 242, 247)
LAND = (216, 205, 178)
LAND_EDGE = (154, 139, 111)
GRID = (216, 226, 232)
YELLOW = (255, 243, 196)
YELLOW_EDGE = (180, 150, 60)
MARKER = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) points, equirectangular.

NORTH_AMERICA = [
    (-168, 66), (-155, 71), (-140, 70), (-125, 72), (-110, 73),
    (-95, 80), (-80, 73), (-65, 62), (-55, 52), (-60, 45),
    (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21),
    (-97, 16), (-105, 20), (-112, 29), (-120, 34), (-124, 42),
    (-125, 49), (-135, 58), (-150, 60), (-162, 58),
]
GREENLAND = [(-55, 60), (-45, 60), (-32, 68), (-22, 70), (-30, 76),
             (-45, 78), (-58, 74), (-60, 68)]
SOUTH_AMERICA = [
    (-79, 9), (-72, 11), (-62, 9), (-52, 5), (-44, -3), (-35, -8),
    (-40, -20), (-48, -28), (-57, -38), (-65, -45), (-70, -52),
    (-73, -40), (-72, -20), (-77, -12), (-81, -5), (-80, 2),
]
EUROPE = [
    (-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
    (12, 55), (18, 56), (21, 59), (28, 60), (30, 55), (28, 48),
    (23, 45), (19, 42), (12, 44), (8, 39), (3, 38), (-2, 37),
]
AFRICA = [
    (-17, 15), (-16, 20), (-10, 30), (-5, 35), (10, 37), (20, 32),
    (30, 31), (33, 27), (35, 22), (39, 15), (43, 11), (48, 11),
    (51, 10), (44, 0), (40, -10), (36, -18), (32, -26), (28, -33),
    (20, -35), (16, -28), (12, -18), (9, -1), (9, 4), (0, 6),
    (-8, 5), (-13, 8), (-17, 12),
]
ASIA = [
    (30, 70), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73),
    (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
    (150, 70), (160, 69), (170, 66), (178, 65), (170, 60), (162, 58),
    (158, 52), (150, 45), (142, 42), (135, 35), (130, 33), (127, 35),
    (122, 30), (120, 25), (115, 22), (110, 20), (108, 15), (105, 9),
    (103, 7), (100, 8), (98, 12), (95, 16), (92, 21), (89, 22),
    (86, 20), (80, 15), (77, 8), (75, 10), (72, 20), (68, 23),
    (62, 25), (57, 27), (52, 28), (48, 30), (44, 32), (40, 36),
    (36, 36), (30, 38), (30, 42), (28, 45), (30, 50), (28, 55),
    (30, 60), (30, 65),
]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38),
         (141, 41), (140, 44), (138, 40), (135, 37), (132, 34)]
MADAGASCAR = [(44, -16), (47, -15), (50, -17), (48, -22), (45, -25),
              (43, -20)]
NEW_ZEALAND = [(167, -45), (170, -42), (174, -39), (176, -38),
               (174, -41), (170, -44)]
AUSTRALIA = [
    (113, -22), (114, -30), (115, -33), (118, -35), (124, -33),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
    (146, -39), (150, -37), (150, -32), (146, -28), (142, -22),
    (142, -15), (140, -12), (136, -12), (132, -11), (128, -14),
    (124, -16), (120, -20), (114, -21),
]
ISLANDS = [(105, -2), (113, -2), (120, -4), (128, -3), (136, -4),
           (141, -8)]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, AFRICA,
              ASIA, UK, JAPAN, MADAGASCAR, NEW_ZEALAND, AUSTRALIA]

# (number, lon, lat) for the seven featured stories.
MARKERS = [
    (1, 121, 23.5),    # Taiwan — markets rally
    (2, 35.2, 47.8),   # Zaporizhzhia
    (3, 98.5, 39.8),   # Jiuquan — Shenzhou-24
    (4, 87.9, 27.6),   # Taplejung — Nepal quake
    (5, 130.9, 37.5),  # Ulleung — KADIZ
    (6, 32.5, 15.6),   # Khartoum
    (7, 56.0, 25.8),   # Ras Al Khaimah
]


def draw_map(draw, x0, y0, w, h):
    """Draw a simplified world map with numbered story markers."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=OCEAN,
                   outline=LAND_EDGE, width=1)

    def px(lon, lat):
        return (x0 + (lon + 170) * w / 360.0,
                y0 + (80 - lat) * h / 135.0)

    # Graticule.
    for lon in range(-150, 181, 30):
        gx, _ = px(lon, 0)
        draw.line([(gx, y0), (gx, y0 + h)], fill=GRID, width=1)
    for lat in range(-30, 81, 30):
        _, gy = px(0, lat)
        draw.line([(x0, gy), (x0 + w, gy)], fill=GRID, width=1)

    # Continents.
    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # Small islands as ellipses.
    for lon, lat in ISLANDS:
        cx, cy = px(lon, lat)
        draw.ellipse([cx - 5, cy - 2, cx + 5, cy + 2], fill=LAND,
                     outline=LAND_EDGE)

    # Numbered markers.
    num_font = SANS_B(10)
    for num, lon, lat in MARKERS:
        cx, cy = px(lon, lat)
        r = 8
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MARKER,
                     outline=WHITE, width=2)
        label = str(num)
        tw = draw.textlength(label, font=num_font)
        draw.text((cx - tw / 2, cy - 7), label, font=num_font, fill=WHITE)


# ---------------------------------------------------------------- content
FEATURED = [
    ("ASIA-PACIFIC", "Asian markets rally as chips rebound",
     "Taiwan's Taiex jumps 9.1%, Korea's Kospi 7.5% and Japan's Nikkei "
     "4.5% \u2014 the year's best day for Asian shares. The chip rebound "
     "follows Monday's Wall Street surge and eases fears of an AI sell-off."),
    ("EUROPE", "Russian strike hits Zaporizhzhia",
     "A Russian attack overnight kills 2 and wounds 22, including two "
     "children. The strike shows the war still hitting civilians hard "
     "while diplomacy stalls."),
    ("ASIA-PACIFIC", "Shenzhou-24 crew named \u2014 a first for Tiangong",
     "Tang Hongbo and Wu Yi will fly with Pakistan's Muhammad Zeeshan "
     "Ali \u2014 the first foreign astronaut to visit Tiangong. A milestone "
     "for China's station and for Pakistan."),
    ("ASIA-PACIFIC", "Nepal quake shakes Taplejung",
     "A magnitude 5.3 tremor shakes Taplejung near the Nepal\u2013Tibet "
     "border, felt in Sikkim and North Bengal. No casualties reported \u2014 "
     "but a reminder of Himalayan seismic risk."),
    ("ASIA-PACIFIC", "Russian jets enter Korea's air defence zone",
     "Several Russian jets enter Korea's air defence zone near Ulleung; "
     "fighters scramble and a shelter alert sounds. No airspace violation "
     "\u2014 Seoul will summon Moscow's attach\u00e9."),
    ("WORLD", "UN agrees two years of talks on \u2018killer robots\u2019",
     "States agree to two years of talks on rules for lethal autonomous "
     "weapons. The first global attempt to govern AI weapons moves from "
     "debate to negotiation."),
    ("AFRICA", "Drones hit homes and a UN building in Khartoum",
     "Drones hit homes and a UN building in Khartoum; the UN blames "
     "strikes launched from Ethiopian soil. Sudan's war is spilling "
     "across its borders."),
]

TIMELINE = [
    ("OVERNIGHT", "Russian strike hits Zaporizhzhia: 2 killed, 22 wounded"),
    ("01:32", "Nepal earthquake M5.3 shakes Taplejung"),
    ("03:18", "UK destitution report: record 3.8m people"),
    ("08:00", "Asian markets rally: Taiex +9.1%, Kospi +7.5%"),
    ("09:00", "German Ifo 90.6, highest in over 3 years"),
    ("EVENING", "Shenzhou-24 crew named, incl. Pakistan's first astronaut"),
]

NUMBERS = [
    ("+9.1%", "Taiex, Taiwan"),
    ("+7.5%", "Kospi, Korea"),
    ("90.6", "German Ifo"),
    ("3.8m", "UK destitute"),
    ("11", "killed, UAE crash"),
]

# (region, number, headline) — stories 8 to 40, grouped by region.
LISTED = [
    ("ASIA-PACIFIC", 8, "Japan factory PMI flash 53.7"),
    ("ASIA-PACIFIC", 9, "Singapore Q3 GDP +6.1%, outlook raised"),
    ("ASIA-PACIFIC", 10, "PBOC sets yuan reference at 6.6757"),
    ("ASIA-PACIFIC", 11, "ANZ pulls RBA cut call to Jun 2027"),
    ("ASIA-PACIFIC", 12, "India shut for Guru Nanak; oil bill +60%"),
    ("ASIA-PACIFIC", 13, "India SC bails Godhra convict (medical)"),
    ("ASIA-PACIFIC", 14, "SpiceJet crisis; pilots' union seeks help"),
    ("ASIA-PACIFIC", 15, "Afghanistan drought deepens"),
    ("ASIA-PACIFIC", 16, "Myanmar govt criticises ASEAN move"),
    ("ASIA-PACIFIC", 17, "China, Swiss envoys talk Korea in Nanjing"),
    ("EUROPE", 18, "German Ifo 90.6, best in 3+ years"),
    ("EUROPE", 19, "Hungary's Magyar to meet Zelenskyy"),
    ("EUROPE", 20, "Belgium PM meets king; no budget deal"),
    ("EUROPE", 21, "Belgium publishes 22nd sanctions package"),
    ("EUROPE", 22, "Thousands protest living costs in Lisbon"),
    ("EUROPE", 23, "12,000 evacuated at Manchester concert"),
    ("EUROPE", 24, "UK destitution hits record 3.8m \u2014 JRF"),
    ("EUROPE", 25, "Ferrari unveils 296 Challenge in Spain"),
    ("EUROPE", 26, "Ukraine MP Labaziuk jailed 7 years"),
    ("EUROPE", 27, "Two diplomats expelled over Russia links"),
    ("EUROPE", 28, "Moscow tows drone-hit vessel off Finland"),
    ("EUROPE", 29, "Albania denies role in Libya ship strike"),
    ("EUROPE", 30, "Ukraine shares clips of ship strikes"),
    ("MIDDLE EAST", 31, "UAE bus-truck crash kills 11"),
    ("MIDDLE EAST", 32, "Israel strike kills at least 3 in Gaza"),
    ("MIDDLE EAST", 33, "Iraqi PM makes first visit to Egypt"),
    ("MIDDLE EAST", 34, "Turkey, Egypt talk economy and Libya"),
    ("NORTH AMERICA", 35, "NBA: Blazers end 76ers' streak"),
    ("NORTH AMERICA", 36, "Trump halts Army lead explosives in Iowa"),
    ("NORTH AMERICA", 37, "Mamdani opens 440,000+ NYC 9/11 files"),
    ("NORTH AMERICA", 38, "US envoy: Russian losses outpace enlistment"),
    ("LATIN AMERICA", 39, "Bolsonaro's son alleges bias in courts"),
    ("OCEANIA", 40, "Solomon Islands ends China security pact"),
]

REGION_COLORS = {
    "ASIA-PACIFIC": (15, 92, 92),
    "EUROPE": (31, 68, 140),
    "MIDDLE EAST": (146, 90, 10),
    "AFRICA": (140, 40, 40),
    "NORTH AMERICA": (90, 50, 120),
    "LATIN AMERICA": (20, 110, 60),
    "OCEANIA": (10, 90, 140),
    "WORLD": (60, 60, 60),
}


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top rule and masthead.
    d.rectangle([0, 0, W, 7], fill=RED)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(38)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 12), title, font=tf, fill=RED)
    d.rectangle([16, 56, W - 16, 82], fill=BLACK)
    band = "TUESDAY  24  NOVEMBER  2026      \u2022      40  STORIES  \u2022      7  REGIONS"
    bf = SANS_B(16)
    bw = d.textlength(band, font=bf)
    d.text(((W - bw) / 2, 60), band, font=bf, fill=WHITE)

    # Numbers strip.
    stats = NUMBERS
    gap, x = 6, 16
    box_w = (W - 32 - gap * (len(stats) - 1)) / len(stats)
    for i, (num, label) in enumerate(stats):
        bx = x + i * (box_w + gap)
        d.rectangle([bx, 90, bx + box_w, 132], fill=WHITE,
                    outline=LIGHT_LINE, width=1)
        nf = SANS_B(21)
        nw = d.textlength(num, font=nf)
        d.text((bx + (box_w - nw) / 2, 93), num, font=nf, fill=INK)
        lf = SANS(10)
        lw = d.textlength(label, font=lf)
        d.text((bx + (box_w - lw) / 2, 118), label, font=lf, fill=GREY)

    # Section divider.
    d.line([(16, 140), (W - 16, 140)], fill=INK, width=2)

    # ---- Left column: featured stories.
    d.text((16, 148), "TOP OF THE DAY", font=SANS_B(13), fill=INK)
    d.line([(16, 168), (628, 168)], fill=LIGHT_LINE, width=1)
    y = 176
    for region, headline, deck in FEATURED:
        color = REGION_COLORS.get(region, INK)
        d.text((16, y), region, font=SANS_B(11), fill=color)
        y += 14
        d.text((16, y), headline, font=SANS_B(15), fill=INK)
        y += 20
        lines = wrap(d, deck, SANS(12), 612)
        y = draw_lines(d, lines[:3], SANS(12), 16, y, INK, 15)
        y += 4
        d.line([(16, y), (628, y)], fill=LIGHT_LINE, width=1)
        y += 9
    # y should end near 690; leave the rest as margin.

    # ---- Right column: map panel.
    d.rectangle([644, 140, 1008, 402], fill=WHITE, outline=LIGHT_LINE,
                width=1)
    d.text((654, 148), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
    d.text((868, 150), "1\u20137 = top stories", font=SANS(10), fill=GREY)
    draw_map(d, 652, 172, 348, 204)
    d.text((654, 382), "Markers match the seven top stories at left.",
           font=SANS(10), fill=GREY)

    # ---- Right column: UTC timeline panel.
    d.rectangle([644, 412, 1008, 700], fill=WHITE, outline=LIGHT_LINE,
                width=1)
    d.text((654, 420), "TUESDAY IN UTC", font=SANS_B(13), fill=INK)
    d.text((654, 438), "When the news broke", font=SANS(10), fill=GREY)
    ty = 460
    for when, what in TIMELINE:
        d.text((654, ty), when, font=SANS_B(12), fill=RED)
        lines = wrap(d, what, SANS(11), 258)
        draw_lines(d, lines[:2], SANS(11), 740, ty, INK, 14)
        ty += 38
        if when != TIMELINE[-1][0]:
            d.line([(654, ty - 4), (998, ty - 4)], fill=LIGHT_LINE, width=1)

    # ---- List section: stories 8-40 in three columns.
    d.line([(16, 708), (W - 16, 708)], fill=INK, width=2)
    d.text((16, 716), "MORE FROM TUESDAY \u2014 STORIES 8 TO 40",
           font=SANS_B(13), fill=INK)
    cols = [
        LISTED[0:10],
        LISTED[10:23],
        LISTED[23:33],
    ]
    col_x = [16, 356, 696]
    for ci, items in enumerate(cols):
        cx = col_x[ci]
        cy = 740
        cur_region = None
        for region, num, headline in items:
            if region != cur_region:
                cur_region = region
                d.text((cx, cy), region, font=SANS_B(11),
                       fill=REGION_COLORS.get(region, INK))
                cy += 16
            d.text((cx, cy), "%d." % num, font=SANS_B(11), fill=INK)
            d.text((cx + 26, cy), headline, font=SANS(11), fill=INK)
            cy += 15

    # ---- Footer.
    d.rectangle([16, 966, 648, 1016], fill=YELLOW, outline=YELLOW_EDGE,
                width=1)
    d.text((26, 972), "DATE CHECK", font=SANS_B(12), fill=INK)
    check = ("Every story on this page was verified as Tuesday 24 November "
             "2026. Stories from Monday 23 November or earlier were checked "
             "and left out.")
    draw_lines(d, wrap(d, check, SANS(11), 600), SANS(11), 26, 988, INK, 14)
    foot = ["Compiled from verified reports",
            "Tuesday 24 November 2026",
            "make.fun bounty news-image-20261124"]
    fy = 970
    for line in foot:
        fw = d.textlength(line, font=SANS(10))
        d.text((1008 - fw, fy), line, font=SANS(10), fill=GREY)
        fy += 14

    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
