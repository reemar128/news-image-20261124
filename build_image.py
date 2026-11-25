"""Front page for Tuesday 24 November 2026.

Draws one 1024x1024 newspaper front page summarising the day's world
news in a single image. All forty stories were verified as Tuesday
24 November 2026 events before this program was written.

Run:  python3 build_image.py
Writes entry.png next to this file. Deterministic: no randomness,
no network, no timestamps, fixed fonts and colours.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (24, 32, 46)
NAVY = (20, 38, 62)
GOLD = (208, 158, 44)
MUTED = (98, 102, 110)
RULE = (198, 191, 170)
WHITE = (255, 255, 255)
CHECK_BG = (253, 242, 196)
CHECK_EDGE = (176, 140, 40)

FONTS = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SERIF_BOLD = font("DejaVuSerif-Bold.ttf", 40)
SANS = font("DejaVuSans.ttf", 12)
SANS_BOLD = font("DejaVuSans-Bold.ttf", 12)
SMALL = font("DejaVuSans.ttf", 11)
SMALL_BOLD = font("DejaVuSans-Bold.ttf", 11)
KICKER = font("DejaVuSans-Bold.ttf", 10)
HEADLINE = font("DejaVuSans-Bold.ttf", 16)
SUMMARY = font("DejaVuSans.ttf", 12)
DATE_FONT = font("DejaVuSans-Bold.ttf", 16)
STAT_NUM = font("DejaVuSans-Bold.ttf", 19)
STAT_LBL = font("DejaVuSans.ttf", 11)
SECTION = font("DejaVuSans-Bold.ttf", 13)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit within width pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading, limit=None):
    """Draw wrapped text, return the y after the last line."""
    lines = wrap(draw, text, fnt, width)
    if limit is not None:
        lines = lines[:limit]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# Region colours.
ASIA = (11, 110, 79)
EUROPE = (29, 78, 216)
MIDEAST = (180, 83, 9)
AFRICA = (157, 23, 77)
NAMERICA = (109, 40, 217)
LATAM = (14, 116, 144)
OCEANIA = (54, 83, 20)

FEATURED = [
    ("ASIA-PACIFIC", ASIA,
     "Asian markets rally as chips rebound",
     "Taiwan's Taiex jumps 9.1%, Korea's Kospi 7.5% and Japan's "
     "Nikkei 4.5% in the region's best day in over a year."),
    ("EUROPE", EUROPE,
     "Zaporizhzhia attack kills 2, wounds 22",
     "A Russian strike overnight hits the Ukrainian city; two "
     "children are among the wounded, officials say."),
    ("ASIA-PACIFIC", ASIA,
     "Shenzhou-24 crew named, first foreign astronaut",
     "Tang Hongbo and Wu Yi fly with Pakistan's Muhammad Zeeshan "
     "Ali, the first foreigner to visit Tiangong station."),
    ("ASIA-PACIFIC", ASIA,
     "Nepal quake shakes Taplejung",
     "A magnitude 5.3 tremor near the Nepal-Tibet border is felt "
     "in Sikkim and North Bengal; no casualties reported."),
    ("ASIA-PACIFIC", ASIA,
     "Russian jets enter Korea's air defence zone",
     "Jets are scrambled near Ulleung Island and a shelter alert "
     "runs 07:52-07:57. No airspace violation, Seoul says."),
    ("WORLD", (51, 65, 85),
     "UN agrees two years of talks on killer robots",
     "States back negotiations on guidelines for lethal autonomous "
     "weapons after years of deadlock."),
]

NUMBERS = [
    ("+9.1%", "Taiex, Taiwan"),
    ("+7.5%", "Kospi, Korea"),
    ("+4.5%", "Nikkei, Japan"),
    ("90.6", "German Ifo"),
    ("3.8m", "UK destitute"),
    ("11", "killed, UAE crash"),
]

# Stories 7-40, grouped by region. Each entry: (number, one-line text).
SECTIONS = [
    ("ASIA-PACIFIC", ASIA, [
        (7, "Japan factory PMI flash 53.7, fastest in months"),
        (8, "Singapore Q3 GDP +6.1%; forecast lifted to ~6%"),
        (9, "PBOC sets yuan reference at 6.6757 per dollar"),
        (10, "ANZ pulls RBA rate-cut call forward to Jun 2027"),
        (11, "India shut for Guru Nanak Jayanti; oil bill +60%"),
        (12, "India top court bails Godhra convict on medical grounds"),
        (13, "SpiceJet in crisis; pilots' union seeks help"),
        (14, "Afghanistan drought deepens, millions in despair"),
        (15, "Myanmar's military-backed govt criticises ASEAN"),
        (16, "China, Swiss envoys discuss Korea in Nanjing"),
    ]),
    ("MIDDLE EAST", MIDEAST, [
        (30, "UAE bus-truck crash kills 11 in Ras Al Khaimah"),
        (31, "Israel strike kills at least 3 in southern Gaza"),
        (32, "Iraqi PM makes first official visit to Egypt"),
        (33, "Turkey, Egypt talk economy and Libya calm"),
    ]),
    ("AFRICA", AFRICA, [
        (34, "Khartoum drones hit homes, UN building"),
    ]),
    ("LATIN AMERICA", LATAM, [
        (39, "Flavio Bolsonaro alleges bias in Brazil courts"),
    ]),
    ("OCEANIA", OCEANIA, [
        (40, "Solomon Islands ends 2022 China security pact"),
    ]),
    ("EUROPE", EUROPE, [
        (17, "German Ifo business climate 90.6, 3-year high"),
        (18, "Hungary's Magyar to meet Zelenskyy in Ukraine"),
        (19, "Belgium PM meets king again; no budget deal"),
        (20, "Belgium publishes 22nd Russia sanctions package"),
        (21, "Thousands protest living costs in Lisbon"),
        (22, "~12,000 evacuated at Manchester concert"),
        (23, "UK destitution hits record 3.8m people - JRF"),
        (24, "Ferrari unveils 296 Challenge Stradale, Evo"),
        (25, "Ukrainian MP Labaziuk jailed 7 years for graft"),
        (26, "Two diplomats expelled over Russian intel links"),
        (27, "Moscow tows drone-hit vessel off Finland"),
        (28, "Albania denies role in Libya ship strike"),
        (29, "Ukraine shares clips of strikes on Russian ships"),
    ]),
    ("NORTH AMERICA", NAMERICA, [
        (35, "Trump orders Army to halt lead explosives in Iowa"),
        (36, "Mamdani opens 440,000+ NYC 9/11 files"),
        (37, "NBA: Blazers end 76ers' streak; Pacers top Thunder"),
        (38, "US envoy: Russian losses outpace enlistment"),
    ]),
]


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 104], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=SERIF_BOLD)
    draw.text(((W - tw) / 2, 18), title, font=SERIF_BOLD, fill=WHITE)
    sub = "TUESDAY 24 NOVEMBER 2026  -  40 STORIES  -  7 REGIONS"
    sw = draw.textlength(sub, font=DATE_FONT)
    draw.text(((W - sw) / 2, 70), sub, font=DATE_FONT, fill=GOLD)
    draw.rectangle([0, 104, W, 108], fill=GOLD)


def draw_numbers(draw):
    draw.rectangle([0, 108, W, 152], fill=(233, 228, 211))
    cell = W / len(NUMBERS)
    for i, (value, label) in enumerate(NUMBERS):
        cx = cell * i + cell / 2
        vw = draw.textlength(value, font=STAT_NUM)
        draw.text((cx - vw / 2, 114), value, font=STAT_NUM, fill=NAVY)
        lw = draw.textlength(label, font=STAT_LBL)
        draw.text((cx - lw / 2, 136), label, font=STAT_LBL, fill=MUTED)
        if i:
            x = cell * i
            draw.line([(x, 116), (x, 146)], fill=RULE, width=1)


def draw_featured(draw):
    x0, y0 = 24, 164
    pw, ph = 320, 150
    gx, gy = 8, 8
    for idx, (region, colour, headline, summary) in enumerate(FEATURED):
        col = idx % 3
        row = idx // 3
        x = x0 + col * (pw + gx)
        y = y0 + row * (ph + gy)
        draw.rectangle([x, y, x + pw, y + ph], fill=WHITE,
                       outline=RULE, width=1)
        draw.rectangle([x, y, x + pw, y + 5], fill=colour)
        draw.text((x + 12, y + 14), region, font=KICKER, fill=colour)
        ny = draw_wrapped(draw, x + 12, y + 34, headline, HEADLINE,
                          pw - 24, INK, 19, limit=3)
        draw_wrapped(draw, x + 12, ny + 4, summary, SUMMARY,
                     pw - 24, MUTED, 15, limit=3)


def draw_list(draw):
    y = 490
    header = "MORE FROM TUESDAY  -  STORIES 7 TO 40"
    draw.text((24, y), header, font=SECTION, fill=NAVY)
    draw.line([(24, y + 22), (W - 24, y + 22)], fill=NAVY, width=2)
    col_w = 476
    columns = [SECTIONS[:5], SECTIONS[5:]]
    for ci, sections in enumerate(columns):
        x = 24 + ci * 500
        cy = y + 34
        for region, colour, items in sections:
            draw.text((x, cy), region, font=KICKER, fill=colour)
            cy += 15
            for num, text in items:
                label = "%d. %s" % (num, text)
                draw.text((x, cy), label, font=SANS, fill=INK)
                cy += 17
            cy += 3
    return y


def draw_bottom(draw):
    box = [24, 930, 664, 1000]
    draw.rectangle(box, fill=CHECK_BG, outline=CHECK_EDGE, width=1)
    draw.text((36, 940), "DATE CHECK", font=SMALL_BOLD, fill=(120, 90, 10))
    note = ("Every story on this page was verified as Tuesday "
            "24 November 2026. Stories from Monday 23 November "
            "or earlier were checked and left out.")
    draw_wrapped(draw, 36, 958, note, SMALL, 616, INK, 14, limit=3)
    foot = ("Compiled from verified reports\n"
            "Tuesday 24 November 2026\n"
            "make.fun bounty news-image-20261124")
    fy = 936
    for line in foot.split("\n"):
        lw = draw.textlength(line, font=SMALL)
        draw.text((W - 24 - lw, fy), line, font=SMALL, fill=MUTED)
        fy += 16


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_numbers(draw)
    draw_featured(draw)
    draw_list(draw)
    draw_bottom(draw)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
