#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page, 1024x1024 PNG.

Newspaper style, like the entries leading the sister bounties:
40 stories, 7 regions, every one happened or was first reported on
Tuesday 24 November 2026 (UTC), with a date check at the foot.
Stories verified against Reuters / AP / AFP / Al Jazeera / WSJ /
Nature, plus the OneTurn daily edition.

Verified Tuesday 24 Nov 2026 (40 stories):
 1 Asian markets rally (Taiex +9.1%, Kospi +7.5%, Nikkei +4.5%)
 2 Nepal earthquake M5.3/5.6 in Koshi, no casualties
 3 Shenzhou-24 crew named; first Pakistani astronaut to Tiangong
 4 Japan manufacturing PMI flash 53.7
 5 Singapore Q3 GDP +6.1%
 6 PBOC sets USD/CNY reference 6.6757
 7 ANZ brings forward RBA rate-cut call to June 2027
 8 India markets shut for Guru Nanak Jayanti; oil import bill +60%
 9 India SC grants bail to Godhra convict (medical grounds)
10 SpiceJet financial crisis; pilots seek intervention
11 Ferrari unveils 296 Challenge Stradale and Evo in Spain
12 Afghanistan drought deepens
13 Myanmar criticises ASEAN decision
14 Russian attack on Zaporizhzhia kills 2, wounds 22
15 Russian aircraft enter KADIZ near Ulleung (no airspace violation)
16 UK destitution at record 3.8m people (JRF study)
17 Belgium PM meets king again, no budget deal
18 Belgium publishes 22nd Russia sanctions package
19 Thousands protest living costs in Lisbon
20 ~12,000 evacuated at Don Toliver concert in Manchester
21 Israel strike kills at least 3 in southern Gaza
22 Iraqi PM makes first official visit to Egypt
23 Turkey and Egypt talk economy and Libya de-escalation
24 China and Swiss envoys discuss Korea in Nanjing
25 Drones hit homes and a UN building in Khartoum
26 Solomon Islands ends 2022 security pact with China
27 Trump orders Army to halt lead explosives in Iowa
28 Mamdani expands NYC 9/11 records portal to 440,000+ files
29 Flavio Bolsonaro alleges bias in Brazil's judiciary
30 NBA: Blazers end 76ers' streak; Pacers beat Thunder; Lakers win
31 UN agrees 2 years of talks on lethal autonomous weapons
32 US envoy Waltz: Russian losses outpace monthly enlistment
33 Moscow tows drone-hit vessel off Finland
34 Albania denies role in Libya drone strike on Russian ship
35 Ukraine shares clips of strikes on Russian ships off Libya
36 Ukrainian MP Labaziuk jailed 7 years for corruption
37 Two diplomats expelled over Russian intel links
38 Bus-truck crash kills 11 in Ras Al Khaimah, UAE
39 German Ifo business climate rises to 90.6, a 3-year high
40 Hungary PM Magyar to meet Zelenskyy in western Ukraine

Deliberately LEFT OUT (earlier days, however big):
India-Nepal train launch, Dymer toll updates, Nvidia/Huang
reinstatement, India-NZ Test draw, Sensex fall, US Iran sanctions,
Qatar PM warning, Brussels protest, France bird flu, Denmark school
threats, Houthi Hodeida claim, Arm CEO contract (all Mon 23 Nov);
COP31 collapse, Merkury sinking, Alcaraz, Liverpool 4-0 (22 Nov);
El Chapo capture, Mayon eruption (21 Nov).

Deterministic: solid colours + DejaVu fonts only, no randomness,
no network, no timestamps. Re-running writes identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (245, 239, 224)
PAPER = (255, 252, 244)
NAVY = (16, 34, 56)
INK = (22, 26, 32)
GREY = (88, 92, 98)
RED = (172, 28, 28)
TEAL = (0, 102, 102)
GOLD = (214, 158, 0)
GREEN = (34, 120, 70)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_SERIF = lambda s: font("DejaVuSerif-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)
F_SANSB = lambda s: font("DejaVuSans-Bold", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, max_w, fill, lh=None):
    h = lh or int(fnt.size * 1.28)
    for ln in wrap(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += h
    return y

def centre(text, fnt, y, fill, x0=0, x1=W):
    w = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)

# ---------- top bar ----------
d.rectangle([0, 0, W, 26], fill=NAVY)
centre("THE WORLD IN ONE DAY  •  40 STORIES  •  7 REGIONS  •  EVERY ONE DATED TUESDAY 24 NOVEMBER 2026",
       F_SANSB(13), 5, (255, 255, 255))

# ---------- masthead ----------
d.text((24, 30), "Tuesday 24 November 2026", font=F_SERIF(48), fill=INK)
d.text((24, 88), "Asian markets rally  •  Zaporizhzhia hit overnight  •  Ifo at a 3-year high",
       font=F_SERIF(18), fill=RED)
d.line([24, 118, W - 24, 118], fill=INK, width=2)

# ---------- numbers strip ----------
nums = [("+9.1%", "Taiex rallies"),
        ("+7.5%", "Kospi rallies"),
        ("+4.5%", "Nikkei rallies"),
        ("90.6", "German Ifo"),
        ("3.8m", "UK destitute"),
        ("11", "killed in UAE crash")]
x = 24
bw = (W - 48 - 5 * 8) / 6
for n, lab in nums:
    d.rectangle([x, 126, x + bw, 168], fill=PAPER, outline=(200, 190, 160))
    centre(n, F_SANSB(22), 129, RED, x, x + bw)
    centre(lab, F_SANS(10), 154, GREY, x, x + bw)
    x += bw + 8

# ---------- region bar ----------
regs = [("EUROPE", (30, 90, 160)), ("MIDDLE EAST", RED), ("ASIA-PACIFIC", (204, 120, 0)),
        ("AMERICAS", TEAL), ("AFRICA", (34, 120, 70)), ("OCEANIA", (110, 60, 140)),
        ("WORLD", (90, 90, 90))]
x = 24
rw = (W - 48) / 7
for name, col in regs:
    d.rectangle([x, 176, x + rw - 2, 196], fill=col)
    centre(name, F_SANSB(11), 181, (255, 255, 255), x, x + rw - 2)
    x += rw

# ---------- scenes (flat, drawn in code) ----------
def scene_markets_up(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 22, 40))
    for gy in (24, 48, 72):
        d.line([x + 10, y + gy, x + w - 10, y + gy], fill=(40, 55, 80), width=1)
    # rising bars
    bars = [(20, 84), (60, 74), (100, 66), (140, 52), (180, 42), (220, 30), (260, 18)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 22, y + h - 14], fill=GREEN)
    # rising line
    pts = [(x + 20, y + 72), (x + 70, y + 62), (x + 120, y + 54), (x + 170, y + 40),
           (x + 220, y + 28), (x + 270, y + 16)]
    d.line(pts, fill=(255, 210, 90), width=3)
    for px_, py_ in pts:
        d.ellipse([px_ - 3, py_ - 3, px_ + 3, py_ + 3], fill=(255, 210, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 45, 70))
    d.text((x + 10, y + h - 13), "TAIEX +9.1%   KOSPI +7.5%   NIKKEI +4.5%", font=F_SANSB(9), fill=(255, 255, 255))

def scene_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
    for sx, sy in [(20, 12), (70, 30), (140, 10), (210, 26), (270, 14), (110, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # apartment block, lit windows, one dark collapsed corner
    d.rectangle([x + 18, y + 30, x + 108, y + h], fill=(52, 58, 74))
    for r in range(4):
        for c in range(3):
            col = (255, 200, 80) if (r + c) % 2 else (30, 34, 48)
            d.rectangle([x + 28 + c * 28, y + 40 + r * 18, x + 44 + c * 28, y + 52 + r * 18], fill=col)
    d.polygon([(x + 108, y + 30), (x + 150, y + h), (x + 108, y + h)], fill=(30, 34, 48))
    # rescue lights at the rubble
    for lx in (170, 210, 250):
        d.polygon([(x + lx, y + h - 34), (x + lx - 8, y + h - 14), (x + lx + 8, y + h - 14)],
                  fill=(255, 220, 120))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(20, 28, 50))

def scene_space(x, y, w, h):
    # Drawn on a temp layer so the Earth arc cannot paint past the scene.
    s = Image.new("RGB", (w, h), (8, 14, 36))
    sd = ImageDraw.Draw(s)
    for sx, sy in [(24, 14), (80, 30), (150, 10), (220, 26), (280, 12), (120, 44), (190, 48)]:
        sd.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # Earth arc at the bottom, clipped to the scene by the temp layer
    sd.ellipse([-40, h - 30, w + 40, h + 90], fill=(30, 90, 160))
    sd.arc([-40, h - 30, w + 40, h + 90], 180, 360, fill=(120, 180, 240), width=3)
    # rocket climbing
    rx, ry = w // 2 - 10, 12
    sd.polygon([(rx + 10, ry), (rx + 20, ry + 22), (rx, ry + 22)], fill=(230, 230, 230))
    sd.rectangle([rx + 2, ry + 22, rx + 18, ry + 40], fill=(200, 200, 200))
    sd.polygon([(rx + 2, ry + 40), (rx - 6, ry + 52), (rx + 2, ry + 44)], fill=(172, 28, 28))
    sd.polygon([(rx + 18, ry + 40), (rx + 26, ry + 52), (rx + 18, ry + 44)], fill=(172, 28, 28))
    sd.polygon([(rx + 10, ry + 40), (rx + 4, ry + 58), (rx + 16, ry + 58)], fill=(255, 140, 0))
    # station ring
    sd.ellipse([34, 52, 74, 66], outline=(255, 210, 90), width=2)
    img.paste(s, (x, y))

def scene_mini(x, y, w, h, kind):
    skies = {"talks": (30, 90, 160), "plane": (90, 150, 200), "cricket": (40, 120, 60),
             "storm": (70, 70, 80), "fire": (60, 30, 30), "gaza": (180, 170, 140),
             "quake": (120, 100, 60), "crash": (90, 90, 100), "nba": (200, 100, 20)}
    d.rectangle([x, y, x + w, y + h], fill=skies[kind])
    if kind == "talks":
        for bx in (30, w - 62):
            d.rectangle([x + bx, y + 16, x + bx + 32, y + h - 8], fill=(255, 255, 255))
            d.rectangle([x + bx + 6, y + 20, x + bx + 26, y + 28], fill=(30, 90, 160))
        d.ellipse([x + w // 2 - 8, y + 8, x + w // 2 + 8, y + 24], fill=(255, 210, 90))
    elif kind == "plane":
        d.ellipse([x + 40, y + 16, x + w - 40, y + 30], fill=(255, 255, 255))
        d.polygon([(x + w // 2 - 10, y + 22), (x + w // 2 + 60, y + 34), (x + w // 2 + 10, y + 30)],
                  fill=(150, 160, 175))
        d.polygon([(x + w // 2 - 30, y + 22), (x + w // 2 - 60, y + 30), (x + w // 2 - 20, y + 30)],
                  fill=(150, 160, 175))
        for wx in range(60, w - 50, 18):
            d.ellipse([x + wx, y + 19, x + wx + 5, y + 24], fill=(30, 90, 160))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(200, 210, 220))
    elif kind == "cricket":
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 160, 80))
        d.rectangle([x + w // 2 - 4, y + 8, x + w // 2 + 4, y + h - 16], fill=(220, 180, 120))
        d.ellipse([x + w - 30, y + 12, x + w - 16, y + 26], fill=(200, 30, 30))
    elif kind == "storm":
        d.ellipse([x + 30, y + 6, x + 110, y + 26], fill=(40, 40, 50))
        d.ellipse([x + 70, y + 2, x + 150, y + 22], fill=(50, 50, 60))
        for rx in range(40, w - 20, 22):
            d.line([x + rx, y + 30, x + rx - 6, y + 42], fill=(150, 200, 255), width=2)
        d.polygon([(x + w - 60, y + 12), (x + w - 44, y + 30), (x + w - 56, y + 30),
                   (x + w - 38, y + 46), (x + w - 62, y + 46)], fill=(255, 220, 0))
    elif kind == "fire":
        d.polygon([(x + w // 2, y + 6), (x + w // 2 - 26, y + h - 8), (x + w // 2 + 26, y + h - 8)],
                  fill=(255, 140, 0))
        d.polygon([(x + w // 2, y + 24), (x + w // 2 - 12, y + h - 8), (x + w // 2 + 12, y + h - 8)],
                  fill=(255, 220, 0))
    elif kind == "gaza":
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 120, 120))
        d.rectangle([x + 16, y + 20, x + w - 16, y + 40], fill=(255, 255, 255))
        d.rectangle([x + 16, y + 20, x + w - 16, y + 28], fill=(220, 60, 60))
        d.ellipse([x + 30, y + 40, x + 46, y + 52], fill=(10, 10, 10))
        d.ellipse([x + w - 46, y + 40, x + w - 30, y + 52], fill=(10, 10, 10))
    elif kind == "quake":
        # cracked ground, mountain ridge
        d.polygon([(x, y + h), (x + 60, y + 8), (x + 140, y + 26), (x + 220, y + 6),
                   (x + w, y + 22), (x + w, y + h)], fill=(90, 75, 50))
        d.line([(x + w // 2 - 30, y + h), (x + w // 2 - 10, y + h - 16),
                (x + w // 2 + 12, y + h - 8), (x + w // 2 + 30, y + h - 22)],
               fill=(40, 30, 20), width=3)
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(60, 50, 35))
    elif kind == "crash":
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 70, 78))
        d.line([x, y + h - 8, x + w, y + h - 8], fill=(255, 255, 255), width=2)
        d.rectangle([x + 30, y + 14, x + 110, y + 34], fill=(30, 90, 160))
        d.rectangle([x + 190, y + 18, x + 250, y + 34], fill=(200, 60, 40))
        for sx, sy in [(150, 10), (158, 20), (142, 22), (166, 12)]:
            d.line([x + sx - 8, y + sy, x + sx + 8, y + sy], fill=(255, 220, 0), width=2)
            d.line([x + sx, y + sy - 8, x + sx, y + sy + 8], fill=(255, 220, 0), width=2)
    elif kind == "nba":
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 70, 30))
        d.ellipse([x + w // 2 - 16, y + 6, x + w // 2 + 16, y + 38], fill=(230, 120, 40),
                  outline=(120, 60, 10), width=2)
        d.line([x + w // 2 - 16, y + 22, x + w // 2 + 16, y + 22], fill=(120, 60, 10), width=2)
        d.arc([x + w // 2 - 16, y + 6, x + w // 2 + 16, y + 38], 300, 60, fill=(120, 60, 10), width=2)

# ---------- top 3 panels ----------
top = [
    ("1  •  MARKETS  •  ASIA RALLIES", "Asian markets rally hard",
     "Taiex +9.1%, Kospi +7.5%, Nikkei +4.5% as chip shares rebound after Monday's Wall Street surge.", scene_markets_up),
    ("2  •  ZAPORIZHZHIA  •  OVERNIGHT", "Zaporizhzhia hit overnight",
     "Russian attack kills 2 and wounds 22, including 2 children, in Ukraine's Zaporizhzhia region.", scene_ukraine),
    ("3  •  SPACE  •  SHENZHOU-24", "Shenzhou-24 crew named",
     "China names Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali; first foreign astronaut to visit Tiangong.", scene_space),
]
px, py, pw, ph, pgap = 24, 204, 312, 210, 16
for i, (kick, head, body, scene) in enumerate(top):
    x = px + i * (pw + pgap)
    d.rectangle([x, py, x + pw, py + ph], fill=PAPER, outline=(200, 190, 160))
    scene(x + 1, py + 1, pw - 2, 88)
    d.text((x + 10, py + 96), kick, font=F_SANSB(11), fill=RED)
    yy = para(head, F_SERIF(21), x + 10, py + 114, pw - 20, INK, lh=23)
    para(body, F_SANS(13), x + 10, yy + 4, pw - 20, GREY, lh=16)

# ---------- second row: 6 cards ----------
cards = [
    ("4  NEPAL  •  EARTHQUAKE", "Quake hits Nepal's Koshi",
     "M5.3/5.6 quake in Taplejung, Koshi; felt in Sikkim; no casualties reported.", "quake"),
    ("5  KOREA  •  KADIZ", "Russian jets enter KADIZ",
     "Several Russian jets enter KADIZ near Ulleung; jets scrambled; no airspace violation.", "plane"),
    ("6  UNITED NATIONS  •  WEAPONS", "UN agrees killer-robot talks",
     "Two years of talks agreed on rules for lethal autonomous weapons.", "talks"),
    ("7  KHARTOUM  •  DRONES", "Drones hit Khartoum homes",
     "Drones hit homes and a UN building; UN blames strikes from Ethiopian soil.", "fire"),
    ("8  RAS AL KHAIMAH  •  CRASH", "Bus crash kills 11 in UAE",
     "Bus-truck collision in Ras Al Khaimah kills 11, interior ministry says.", "crash"),
    ("9  NBA  •  MONDAY NIGHT", "NBA: streaks end, Spurs roll",
     "Blazers end 76ers' streak; Pacers beat Thunder; Lakers, Bucks, Spurs win.", "nba"),
]
cx, cy, cw, ch = 24, 422, 312, 136
for i, (kick, head, body, kind) in enumerate(cards):
    x = cx + (i % 3) * (cw + pgap)
    y = cy + (i // 3) * (ch + 8)
    d.rectangle([x, y, x + cw, y + ch], fill=PAPER, outline=(200, 190, 160))
    scene_mini(x + 1, y + 1, cw - 2, 44, kind)
    d.text((x + 10, y + 52), kick, font=F_SANSB(11), fill=RED)
    yy = para(head, F_SERIF(17), x + 10, y + 70, cw - 20, INK, lh=19)
    para(body, F_SANS(12), x + 10, yy + 3, cw - 20, GREY, lh=14)

# ---------- also list ----------
ly = 710
d.text((24, ly), "ALSO ON TUESDAY 24 NOVEMBER", font=F_SANSB(14), fill=INK)
d.line([24, ly + 20, W - 24, ly + 20], fill=INK, width=1)
also_left = [
    "10  Japan manufacturing PMI flash 53.7.",
    "11  Singapore Q3 GDP +6.1%; forecast lifted to ~6%.",
    "12  PBOC sets USD/CNY reference rate at 6.6757.",
    "13  ANZ brings forward RBA rate-cut call to June 2027.",
    "14  India markets shut for Guru Nanak Jayanti; oil import bill +60%.",
    "15  India's top court grants bail to Godhra convict (medical).",
    "16  SpiceJet in financial crisis; pilots' union seeks help.",
    "17  Ferrari unveils 296 Challenge Stradale and Evo in Spain.",
    "18  Afghanistan drought deepens; millions pushed into despair.",
    "19  Myanmar's military-backed government criticises ASEAN.",
    "20  UK destitution at a record 3.8m people, JRF study finds.",
    "21  Belgium PM meets king again; still no budget deal.",
    "22  Belgium publishes 22nd Russia sanctions package.",
    "23  Thousands protest living costs in Lisbon.",
    "24  ~12,000 evacuated at Don Toliver concert in Manchester.",
    "25  Israel strike kills at least 3 in southern Gaza.",
]
also_right = [
    "26  Iraqi PM makes first official visit to Egypt.",
    "27  Turkey and Egypt talk economy and Libya de-escalation.",
    "28  China and Swiss envoys discuss Korea in Nanjing.",
    "29  Solomon Islands ends 2022 security pact with China.",
    "30  Trump orders Army to halt lead explosives in Iowa.",
    "31  Mamdani expands NYC 9/11 records portal to 440,000+ files.",
    "32  Flavio Bolsonaro alleges bias in Brazil's judiciary.",
    "33  US envoy Waltz: Russian losses outpace monthly enlistment.",
    "34  Moscow tows drone-hit vessel off Finland.",
    "35  Albania denies role in Libya drone strike on Russian ship.",
    "36  Ukraine shares clips of strikes on Russian ships off Libya.",
    "37  Ukrainian MP Labaziuk jailed 7 years for corruption.",
    "38  Two diplomats expelled over Russian intel links.",
    "39  German Ifo business climate rises to 90.6, a 3-year high.",
    "40  Hungary's Magyar to meet Zelenskyy in western Ukraine.",
]
y = ly + 28
for t in also_left:
    y = para(t, F_SANS(10), 24, y, 470, INK, lh=12)
y = ly + 28
for t in also_right:
    y = para(t, F_SANS(10), 512, y, 488, INK, lh=12)

# ---------- date check + footer ----------
d.rectangle([24, 940, W - 24, 978], fill=(255, 255, 255), outline=RED)
d.text((32, 946), "DATE CHECK", font=F_SANSB(12), fill=RED)
para("Every story here happened or was first reported on Tue 24 Nov 2026 (UTC). Left out: India-Nepal train, Dymer toll, Nvidia/Huang, India-NZ draw (23 Nov); COP31, Merkury, Alcaraz, Liverpool 4-0 (22 Nov); El Chapo, Mayon (21 Nov).",
     F_SANS(10), 128, 946, W - 152, INK, lh=13)
centre("Sources: Reuters  •  AP  •  AFP  •  Al Jazeera  •  WSJ  •  Nature  —  Scenes are drawn illustrations, not photographs.",
       F_SANS(10), 990, GREY)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
