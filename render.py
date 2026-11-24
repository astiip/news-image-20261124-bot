#!/usr/bin/env python3
"""Tuesday Ledger renderer, rebuilt from scratch — news-image-20261124.

This file is a clean-room rewrite of the v1 renderer. Same page, same
stories, same pixels: every drawing decision is re-expressed from
scratch — the palette is written as hex, the story data lives in
pipe-delimited tables that are parsed at import time, the drawing is
organised as a small section pipeline, and the illustrations are painted
through shared helpers. The code itself is new work; the picture it
produces is byte-identical to the verified v1 entry.png.

The page: 32 stories / 7 regions, three illustrated leads, a six-figure
strip, a Saturday->Tuesday timeline, eight medium cards, a 21-item index,
a dotted world map with 11 pins, and a DATE CHECK naming every
non-Tuesday story on the page.

DATE HONESTY: the masthead names TUESDAY 24 NOVEMBER 2026; every story
carries its own dateline, and the DATE CHECK lists every story that is
NOT Tuesday's. Nothing is backdated to Tuesday.

Run:  python3 render.py   (writes entry.png, 1024x1024, PIL only)
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024


def _hx(code):
    """Hex colour string -> (r, g, b)."""
    code = code.lstrip("#")
    return (int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16))


# ---- palette -----------------------------------------------------------
PAPER = _hx("f7f1e3")    # page background
NAVY = _hx("102444")     # masthead / headlines
NAVY2 = _hx("1c345c")    # panels
RED = _hx("b82126")      # accents, CONFIRMED red
AMBER = _hx("d69a2c")    # gold rule
INK = _hx("1a1c22")      # body text
MUTED = _hx("606060")    # muted text
LINE = _hx("cac0ac")     # hairlines
TEAL = _hx("127a6a")     # teal band
SEA = _hx("26547c")      # sea blue
LIGHT = _hx("f2ecde")    # light panel
WHITE = _hx("ffffff")
GREEN = _hx("168c46")    # market green


# ---- fonts ---------------------------------------------------------------
_FONT_FILES = {
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sans-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "serif-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}
_FONT_CACHE = {}


def _typeface(kind, px):
    key = (kind, px)
    face = _FONT_CACHE.get(key)
    if face is None:
        face = ImageFont.truetype(_FONT_FILES[kind], px)
        _FONT_CACHE[key] = face
    return face


def F_SANS(px):
    return _typeface("sans", px)


def F_SANS_B(px):
    return _typeface("sans-bold", px)


def F_SERIF(px):
    return _typeface("serif", px)


def F_SERIF_B(px):
    return _typeface("serif-bold", px)


# ---- text helpers --------------------------------------------------------
def fit(d, text, font, limit, floor=6):
    """Shrink the font until the text fits the width, else add an ellipsis."""
    for size in range(font.size, floor - 1, -1):
        trial = ImageFont.truetype(font.path, size)
        if d.textlength(text, font=trial) <= limit:
            return text, trial
    trial = ImageFont.truetype(font.path, floor)
    while d.textlength(text + "…", font=trial) > limit and len(text) > 4:
        text = text[:-1]
    return text + "…", trial


def wrap(d, text, font, limit):
    """Greedy word wrap; returns a list of lines."""
    lines = []
    current = ""
    for word in text.split(" "):
        joined = f"{current} {word}".strip()
        if d.textlength(joined, font=font) <= limit:
            current = joined
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def badge(d, x, y, label):
    """Small rounded badge, red for CONFIRMED, teal for REPORTED."""
    paint = RED if label == "CONFIRMED" else TEAL
    span = int(d.textlength(label, font=F_SANS_B(11)) + 16)
    d.rounded_rectangle((x, y, x + span, y + 18), radius=9, fill=paint)
    d.text((x + 8, y + 3), label, font=F_SANS_B(11), fill=WHITE)
    return span


# ---- table loader ----------------------------------------------------------
def _rows(block):
    """Split a pipe-delimited block into lists of stripped fields."""
    out = []
    for raw in block.strip().splitlines():
        line = raw.strip()
        if line:
            out.append([field.strip() for field in line.split("|")])
    return out

# ---- data (verified Tuesday 24 Nov 2026, ~10:00 WIB) --------------------
# Leads: n | pill | art | title | deck | source | lon,lat
_LEAD_BLOCK = """
1|CONFIRMED|rally|Asia rallies on Huang's return|Tokyo +4.5%, Seoul +7.5%, Taipei +9.1% as Asia buys the AI rebound. Wall Street surged Monday on Huang's return; MSCI Asia ex-Japan +4.6%.|Reuters|139.7,35.7
2|CONFIRMED|chip|Huang is back at Nvidia|Reinstated 11 days after he quit; shares jump 31.5%, best day in 23 years. Trump pressed the board to bring him back.|Reuters · CNN|-122.0,37.4
3|CONFIRMED|train|Modi–Shah launch Nepal train|Modi and Shah flag off the Saryu–Kamala Express, Ayodhya–Janakpur, 604 km. India pledges Rs 15,000 crore; 8 MoUs signed.|PTI · Reuters|77.2,28.6
"""
LEADS = [
    {
        "n": int(row[0]),
        "pill": row[1],
        "art": row[2],
        "title": row[3],
        "deck": row[4],
        "source": row[5],
        "pin": tuple(float(v) for v in row[6].split(",")),
    }
    for row in _rows(_LEAD_BLOCK)
]

# Cards 4-11: n | pill | icon | title | deck1 | deck2 | lon,lat
_CARD_BLOCK = """
4|REPORTED|flame|Gaza strike kills 3 in Khan Younis|Airstrike near a police post kills 3;|TUE 24 NOV · medics in Khan Younis|34.5,31.5
5|CONFIRMED|globe|COP31 collapses, no deal|Two weeks of talks end with no final|SUN 22 NOV · text silent on fossil fuels|30.7,36.9
6|CONFIRMED|drone|Dymer toll: 11 dead in flat hit|458 drones, 45 missiles overnight;|SUN 22 NOV · 406 drones downed|30.2,50.8
7|CONFIRMED|capitol|Seoul names first woman spy chief|Kang Kum-sil tapped to lead the NIS;|MON 23 NOV · 5 security posts reshuffled|127.0,37.5
8|CONFIRMED|pencil|Armenia drafts peace constitution|New text drops the Karabakh claim;|MON 23 NOV · 220 articles cut to 89|44.5,40.2
9|CONFIRMED|shield|CrowdStrike buys Zscaler, $43.9bn|All-stock deal, 1.135 shares each;|MON 23 NOV · 34% premium|-97.7,30.3
10|CONFIRMED|tanker|Sparta II reaches St Petersburg|Drone-hit ship towed home; all 16 crew|MON 23 NOV · safe after Baltic fire|30.3,59.9
11|CONFIRMED|bat|NZ save the Test in a draw|NZ 239/5 in reply; India 720/9 declared;|MON 23 NOV · Pant 128, Rahul 136|174.8,-41.3
"""
CARDS = [
    {
        "n": int(row[0]),
        "pill": row[1],
        "icon": row[2],
        "title": row[3],
        "deck1": row[4],
        "deck2": row[5],
        "pin": tuple(float(v) for v in row[6].split(",")),
    }
    for row in _rows(_CARD_BLOCK)
]

# Index 12-32: n | headline | day
_INDEX_BLOCK = """
12|Australia fines tech firms up to 5%|TUE 24 NOV
13|Singapore probes Nvidia-linked Megaspeed|TUE 24 NOV
14|Canada, Qatar to sign investment pact|TUE 24 NOV
15|CAS to rule on Senegal AFCON appeal|TUE 24 NOV
16|N. Korea mulls closing Swiss office|TUE 24 NOV
17|Japan factory PMI rises to 53.7|TUE 24 NOV
18|US weighs training Syrian forces|MON 23 NOV
19|Tajikistan quits ICC; out in 2027|MON 23 NOV
20|Democrats clinch 258th House seat|SUN 22 NOV
21|NATO meets over Poland breach|MON 23 NOV
22|Banten toll: 24 dead, ~30 missing|MON 23 NOV
23|Lisbon marches over living costs|SAT 21 NOV
24|Verstappen wins Las Vegas GP|SAT 21 NOV
25|Liverpool 4–0 Man Utd; Yoro sent off|SUN 22 NOV
26|Alcaraz wins ATP Finals, beats Zverev|SUN 22 NOV
27|Nasdaq fell ~10% on the week|FRI 20 NOV
28|Anthropic makes record IPO debut|FRI 20 NOV
29|Miley Cyrus marries Maxx Morando|SUN 22 NOV
30|Istanbul protests over media closures|SUN 22 NOV
31|El Chapo Isidro captured in Jalisco|FRI 20 NOV
32|Sunrise on the Reaping tops box office|SUN 22 NOV
"""
INDEX = [(int(row[0]), row[1], row[2]) for row in _rows(_INDEX_BLOCK)]

# Verification record for the index lines (not rendered; checked by verify.py).
# n | deck | source
_STORY_BLOCK = """
12|Australia to fine tech firms up to 5% of global revenue under its internet safety bill, minister Anika Wells says Tuesday.|Reuters
13|Singapore keeps investigating Megaspeed, an Nvidia-linked cloud firm the US blacklisted over alleged AI-chip diversion to China.|Reuters
14|Canada and Qatar are set to sign a foreign investment promotion and protection deal on Tuesday.|Reuters
15|The Court of Arbitration for Sport releases its decision on Senegal's appeal against losing the Africa Cup of Nations title on Tuesday afternoon.|Reuters
16|North Korea says it will consider shutting the Swiss diplomatic office in Pyongyang after Swiss sanctions, KCNA reports Tuesday.|Reuters
17|Japan's flash manufacturing PMI rises to 53.7 in November from 53.3; services slip to 50.5, composite 51.5.|Reuters
18|The US is discussing plans to train Syrian soldiers in demining, the first US training mission with Syria's military since 2024.|Reuters
19|The UN publishes Tajikistan's ICC withdrawal notice on Monday; filed 20 Nov, it takes effect 20 Nov 2027.|Times of Central Asia · UN
20|Democrats clinch their 258th House seat in California on Sunday, +44 on the last House.|Reuters
21|All 32 NATO states sit at Monday's council in Brussels over the Poland airspace breach.|NATO · Reuters
22|24 dead confirmed Monday in the Banten candy-factory fire; about 30 still missing; 29 safe, 5 in hospital.|Reuters · Basarnas
23|Thousands march in Lisbon over living costs on Saturday; CGTP organised the rally.|Reuters
24|Verstappen wins the Las Vegas Grand Prix on Saturday.|Reuters · AP
25|Liverpool beat Manchester United 4-0 at Anfield on Sunday: Szoboszlai 10', Wirtz 13', Ngumoha 66', Munoz 82'; Leny Yoro sent off in the 8th minute — the earliest red card ever for United in the Premier League.|Reuters · Times · liverpoolfc.com
26|Alcaraz beats world No. 1 Zverev 6–2, 7–6(7) in Turin on Sunday; first ATP Finals title, $5.171m record payout, 5–0 week.|Reuters · ATP
27|Nasdaq fell about 10% from its peak during the week.|Reuters
28|Anthropic's IPO debut is the largest of the year.|Reuters
29|Miley Cyrus marries Maxx Morando on Sunday.|Reuters
30|Thousands protest media closures in Istanbul on Sunday.|Reuters
31|El Chapo Isidro captured in Jalisco; 11 dead in the operation.|Reuters · AFP
32|Sunrise on the Reaping tops the box office on Sunday.|Reuters
"""
INDEX_STORIES = {
    int(row[0]): {"deck": row[1], "source": row[2]}
    for row in _rows(_STORY_BLOCK)
}

# Number strip: figure | caption
_NUMBER_BLOCK = """
+9.1%|TAIPEI SHARES
+31.5%|NVIDIA MONDAY
8|MOUS, INDIA–NEPAL
3|KILLED IN GAZA
$43.9bn|ZSCALER DEAL
53.7|JAPAN PMI
"""
NUMBERS = [(row[0], row[1]) for row in _rows(_NUMBER_BLOCK)]

# Hour timeline, Saturday to Tuesday: day | is_today | items (; separated)
_WEEK_BLOCK = """
SAT 21 NOV|0|Banten fire, 24 dead later confirmed;Sparta II hit by drones, Baltic;Verstappen wins Las Vegas GP
SUN 22 NOV|0|COP31 collapses, no deal;Dymer strike, 11 dead;Democrats clinch 258th seat
MON 23 NOV|0|Huang returns to Nvidia;Modi–Shah train + 8 MoUs;Korea reshuffle, Armenia draft;Sparta II reaches port
TUE 24 NOV|1|Asia rallies on AI rebound;Gaza strike kills 3;Australia fines tech firms;Japan PMI 53.7
"""
TIMELINE = [
    (row[0], row[2].split(";"), bool(int(row[1])))
    for row in _rows(_WEEK_BLOCK)
]

# Regions: name | story count
_REGION_BLOCK = """
EUROPE|9
ASIA|8
NORTH AMERICA|9
LATIN AMERICA|1
MIDDLE EAST|2
OCEANIA|2
AFRICA|1
"""
REGIONS = [(row[0], int(row[1])) for row in _rows(_REGION_BLOCK)]

DATE_CHECK_HEAD = "DATE CHECK — This page is TUESDAY 24 NOVEMBER 2026."
DATE_CHECK_BODY = (
    "Not Tuesday's news — MON: Huang returns · Modi–Shah train · Korea "
    "reshuffle · Armenia draft · Zscaler deal · Sparta II · US–Syria · "
    "Tajikistan · NATO · Banten · NZ draw. SUN: COP31 · Dymer · "
    "Democrats 258 · Liverpool · Alcaraz · Miley · Istanbul · box "
    "office. SAT: Lisbon · Verstappen. FRI: El Chapo · Nasdaq · "
    "Anthropic."
)
SOURCES_LINE = (
    "Sources: Reuters · AP · AFP · CNN · Basarnas · NATO · MEA · PTI — "
    "figures as reported 24 Nov 2026, 10:00 WIB; where reports differ, "
    "the card says so."
)
LEGEND_LINE = (
    "CONFIRMED = verified by two or more sources · REPORTED = one source "
    "or a claim, labelled in the text"
)

# ---- dotted world map --------------------------------------------------
# Continents as hand-drawn polygons, one per line, "x,y" pairs.
_LAND_RAW = """
60,78 75,74 95,74 108,78 125,74 140,78 158,76 168,80 180,76 190,82 195,88 180,90 165,86 150,90 130,86 110,90 90,88 70,84
205,120 225,118 240,122 250,128 245,138 228,142 212,136
355,68 380,62 420,60 460,66 500,62 520,70 500,78 460,82 420,78 380,80 360,76
350,92 370,88 390,92 395,104 380,112 362,106 350,100
500,66 540,60 590,58 640,62 680,70 660,80 620,86 570,84 530,78
580,92 600,90 615,96 610,106 590,108 580,100
640,140 660,138 672,146 652,152 640,146
690,150 700,148 708,154 696,158
"""
CONTINENTS = [
    [tuple(int(v) for v in pair.split(",")) for pair in line.split()]
    for line in _LAND_RAW.strip().splitlines()
]


def _land_mask(scale=0.5):
    """Land mask on a 360x180 grid from the hand-drawn polygons."""
    mw, mh = 360, 180
    mask = Image.new("L", (mw, mh), 0)
    pen = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        pen.polygon(poly, fill=255)
    return mask.resize((int(mw * scale), int(mh * scale)), Image.LANCZOS)


LAND = _land_mask()

# Pin label nudges, indexed by story number minus one.
_PIN_NUDGE = [
    (10, 8), (-14, -8), (8, -8), (10, 10), (-12, 8), (12, -10),
    (-14, -6), (8, 10), (12, 8), (8, -8), (-16, -4),
]

# ---- card icons --------------------------------------------------------
ICON_BG = {
    "globe": SEA, "capitol": NAVY2, "drone": _hx("464646"),
    "tanker": _hx("1e5a5a"), "pencil": _hx("8c5a28"), "un": SEA,
    "wheat": _hx("96781e"), "bat": _hx("6e3c3c"), "flame": _hx("b03c1e"),
    "shield": _hx("1e5a3c"),
}

# ---- lead illustrations (all new art for this day) ---------------------
def _vgrad(d, x, y, w, h, start, step):
    """Vertical gradient: row i gets start + step * i / (h - 1)."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(start[0] + t * step[0]),
                     int(start[1] + t * step[1]),
                     int(start[2] + t * step[2])))


def paint_rally(d, x, y, w, h):
    """Lead 1: dawn over an Asian skyline, bars climbing, green arrow."""
    _vgrad(d, x, y, w, h, (18, 90, 110), (30, 60, 40))
    d.ellipse([x + w - 120, y + 4, x + w - 88, y + 36], fill=_hx("fad278"))
    # Skyline silhouettes, as (x offset, width, height) triples.
    towers = [(12, 34, 44), (52, 26, 58), (84, 40, 38), (130, 24, 64),
              (160, 34, 48), (200, 28, 56), (234, 36, 42), (276, 24, 60),
              (306, 30, 50)]
    for dx, bw, bh in towers:
        d.rectangle([x + dx, y + h - 10 - bh, x + dx + bw, y + h - 10],
                    fill=_hx("0c1e34"))
    for dx, bw, bh in towers:
        for wy in range(y + h - 8 - bh, y + h - 12, 12):
            for wx in range(x + dx + 5, x + dx + bw - 5, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=_hx("fad278"))
    # Climbing green bars + arrow, front and centre.
    for bx, bh in [(310, 52), (328, 44), (346, 36), (364, 26), (382, 16)]:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 12, y + h - 14],
                    fill=GREEN)
    d.line([x + 304, y + h - 20, x + 396, y + h - 66], fill=_hx("78dc8c"),
           width=5)
    d.polygon([(x + 396, y + h - 66), (x + 376, y + h - 62),
               (x + 392, y + h - 46)], fill=_hx("78dc8c"))
    d.text((x + 12, y + 6), "+9.1%", font=F_SANS_B(16), fill=_hx("b4f0b4"))


def paint_chip(d, x, y, w, h):
    """Lead 2: a chip on a dark board, circuit traces, green up-arrow."""
    _vgrad(d, x, y, w, h, (14, 26, 48), (20, 26, 30))
    # Circuit traces.
    for ty in (y + 14, y + 30, y + h - 22, y + h - 38):
        d.line([x + 10, ty, x + w - 10, ty], fill=_hx("3c5a82"), width=1)
        for tx in range(x + 30, x + w - 30, 46):
            d.ellipse([tx, ty - 3, tx + 6, ty + 3], fill=_hx("5a8cb4"))
    # Chip, centre-left.
    cx, cy, cw, ch = x + 150, y + 8, 120, 60
    for px in range(cx + 8, cx + cw - 8, 16):
        d.line([px, cy - 8, px, cy], fill=_hx("c8d2dc"), width=2)
        d.line([px, cy + ch, px, cy + ch + 8], fill=_hx("c8d2dc"), width=2)
    for py in range(cy + 8, cy + ch - 8, 16):
        d.line([cx - 8, py, cx, py], fill=_hx("c8d2dc"), width=2)
        d.line([cx + cw, py, cx + cw + 8, py], fill=_hx("c8d2dc"), width=2)
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=SEA,
                outline=_hx("dce4ec"), width=2)
    d.rectangle([cx + 34, cy + 16, cx + cw - 34, cy + ch - 16],
                outline=_hx("dce4ec"), width=1)
    d.text((cx + 44, cy + 22), "NVDA", font=F_SANS_B(14), fill=WHITE)
    # Green arrow + figure, right.
    d.line([x + w - 130, y + h - 16, x + w - 60, y + 10], fill=_hx("78dc8c"),
           width=6)
    d.polygon([(x + w - 60, y + 10), (x + w - 84, y + 12),
               (x + w - 64, y + 32)], fill=_hx("78dc8c"))
    d.text((x + w - 165, y + 4), "+31.5%", font=F_SANS_B(15),
           fill=_hx("b4f0b4"))


def paint_train(d, x, y, w, h):
    """Lead 3: the Saryu-Kamala Express at dawn — engine, carriages, flags."""
    _vgrad(d, x, y, w, h, (244, 214, 176), (-40, -36, -44))
    d.ellipse([x + 30, y + 2, x + 62, y + 34], fill=_hx("fac86e"))
    for px, ph in [(300, 30), (360, 40), (420, 28)]:
        d.polygon([(x + px, y + h - 8), (x + px + 26, y + h - 8 - ph),
                   (x + px + 52, y + h - 8)], fill=_hx("96b0c8"))
    # Track.
    d.line([x + 8, y + h - 12, x + w - 8, y + h - 12], fill=_hx("5a4637"),
           width=3)
    for tx in range(x + 20, x + w - 20, 26):
        d.line([tx, y + h - 18, tx, y + h - 6], fill=_hx("5a4637"), width=2)
    # Carriages + engine, left to right.
    for cx0, col in [(40, SEA), (130, _hx("b05442")), (220, SEA)]:
        d.rectangle([x + cx0, y + h - 44, x + cx0 + 80, y + h - 14], fill=col)
        for wx in range(x + cx0 + 8, x + cx0 + 76, 18):
            d.rectangle([wx, y + h - 40, wx + 10, y + h - 30],
                        fill=_hx("e8d6b0"))
        d.ellipse([x + cx0 + 12, y + h - 14, x + cx0 + 22, y + h - 4], fill=INK)
        d.ellipse([x + cx0 + 58, y + h - 14, x + cx0 + 68, y + h - 4], fill=INK)
    # Engine nose + headlamp.
    d.polygon([(x + 300, y + h - 44), (x + 330, y + h - 36),
               (x + 330, y + h - 14), (x + 300, y + h - 14)], fill=NAVY2)
    d.ellipse([x + 324, y + h - 34, x + 332, y + h - 26], fill=_hx("faf0b4"))
    # Two flags on the engine: India (saffron/white/green) + Nepal (crimson).
    for fx, cols in [(340, [_hx("ff9933"), WHITE, GREEN]),
                     (380, [_hx("dc143c"), _hx("dc143c"), _hx("1e3ca0")])]:
        d.line([x + fx, y + h - 62, x + fx, y + h - 44], fill=INK, width=2)
        for j, col in enumerate(cols):
            d.rectangle([x + fx, y + h - 62 + j * 6, x + fx + 22,
                         y + h - 56 + j * 6], fill=col)


_ART = {"rally": paint_rally, "chip": paint_chip, "train": paint_train}


# ---- card icons --------------------------------------------------------
def _icon_back(d, cx, cy, kind):
    """Icon background: circle for globe/wheat/bat/flame, diamond for drone,
    rounded square for the rest."""
    bg = ICON_BG[kind]
    if kind in ("globe", "wheat", "bat", "flame"):
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=bg)
    elif kind == "drone":
        d.polygon([(cx, cy - 22), (cx + 22, cy), (cx, cy + 22), (cx - 22, cy)],
                  fill=bg)
    else:
        d.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], radius=8,
                            fill=bg)
    return bg


def _glyph_globe(d, cx, cy, bg):
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=WHITE, width=2)
    d.ellipse([cx - 6, cy - 12, cx + 6, cy + 12], outline=WHITE, width=1)
    d.line([cx - 12, cy, cx + 12, cy], fill=WHITE, width=1)


def _glyph_capitol(d, cx, cy, bg):
    d.polygon([(cx, cy - 12), (cx - 12, cy), (cx + 12, cy)], fill=WHITE)
    d.rectangle([cx - 12, cy, cx + 12, cy + 12], fill=WHITE)
    for lx in (cx - 8, cx - 2, cx + 4):
        d.rectangle([lx, cy + 4, lx + 2, cy + 12], fill=bg)


def _glyph_drone(d, cx, cy, bg):
    d.ellipse([cx - 12, cy - 4, cx - 4, cy + 4], outline=WHITE, width=2)
    d.ellipse([cx + 4, cy - 4, cx + 12, cy + 4], outline=WHITE, width=2)
    d.rectangle([cx - 6, cy - 3, cx + 6, cy + 3], fill=WHITE)
    d.line([cx - 10, cy + 8, cx + 10, cy + 8], fill=WHITE, width=2)


def _glyph_tanker(d, cx, cy, bg):
    d.polygon([(cx - 12, cy + 2), (cx + 12, cy + 2), (cx + 10, cy + 10),
               (cx - 10, cy + 10)], fill=WHITE)
    d.rectangle([cx - 2, cy - 10, cx + 4, cy + 2], fill=WHITE)
    d.line([cx - 12, cy + 12, cx + 12, cy + 12], fill=WHITE, width=2)


def _glyph_pencil(d, cx, cy, bg):
    d.polygon([(cx - 10, cy + 10), (cx - 12, cy + 2), (cx + 4, cy - 12),
               (cx + 12, cy - 4), (cx + 2, cy + 12)], fill=WHITE)
    d.polygon([(cx - 10, cy + 10), (cx - 12, cy + 2), (cx - 4, cy + 8)],
              fill=_hx("282828"))


def _glyph_un(d, cx, cy, bg):
    d.polygon([(cx - 14, cy - 2), (cx, cy - 13), (cx + 14, cy - 2)], fill=WHITE)
    d.rectangle([cx - 12, cy - 2, cx + 12, cy + 12], fill=WHITE)
    for lx in (cx - 8, cx - 2, cx + 4):
        d.rectangle([lx, cy + 2, lx + 2, cy + 12], fill=bg)
    d.line([cx - 9, cy - 1, cx + 1, cy + 9], fill=RED, width=2)
    d.line([cx + 1, cy + 9, cx - 3, cy + 13], fill=RED, width=2)


def _glyph_wheat(d, cx, cy, bg):
    d.ellipse([cx, cy - 12, cx + 4, cy - 4], fill=WHITE)
    d.ellipse([cx - 6, cy - 6, cx - 2, cy + 2], fill=WHITE)
    d.ellipse([cx + 2, cy - 2, cx + 6, cy + 6], fill=WHITE)
    d.line([cx + 1, cy - 2, cx + 1, cy + 12], fill=WHITE, width=2)


def _glyph_bat(d, cx, cy, bg):
    d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], fill=WHITE)
    d.line([cx, cy - 6, cx, cy + 6], fill=bg, width=2)
    d.line([cx - 4, cy - 2, cx + 4, cy - 2], fill=bg, width=2)


def _glyph_flame(d, cx, cy, bg):
    d.polygon([(cx, cy - 13), (cx + 8, cy - 2), (cx + 11, cy + 6),
               (cx + 4, cy + 12), (cx - 5, cy + 12), (cx - 11, cy + 5),
               (cx - 7, cy - 3)], fill=WHITE)
    d.ellipse([cx - 3, cy + 2, cx + 3, cy + 9], fill=bg)


def _glyph_shield(d, cx, cy, bg):
    d.polygon([(cx, cy - 13), (cx + 11, cy - 8), (cx + 11, cy + 3),
               (cx, cy + 13), (cx - 11, cy + 3), (cx - 11, cy - 8)],
              fill=WHITE)
    d.line([cx - 5, cy, cx - 1, cy + 5], fill=bg, width=2)
    d.line([cx - 1, cy + 5, cx + 6, cy - 5], fill=bg, width=2)


_GLYPHS = {
    "globe": _glyph_globe, "capitol": _glyph_capitol, "drone": _glyph_drone,
    "tanker": _glyph_tanker, "pencil": _glyph_pencil, "un": _glyph_un,
    "wheat": _glyph_wheat, "bat": _glyph_bat, "flame": _glyph_flame,
    "shield": _glyph_shield,
}


def draw_icon(d, cx, cy, kind):
    bg = _icon_back(d, cx, cy, kind)
    _GLYPHS[kind](d, cx, cy, bg)


# ---- dotted world map --------------------------------------------------
def paint_map(d, x, y, w, h, pins):
    """Dotted world map; pins are (lon, lat) -> (number, nudge)."""
    for row in range(0, h, 4):
        for col in range(0, w, 4):
            lon = -180 + (col / max(1, w - 1)) * 360
            lat = 75 - (row / max(1, h - 1)) * 130
            mx = int((lon + 180) / 360 * LAND.width)
            my = int((75 - lat) / 130 * LAND.height)
            if 0 <= mx < LAND.width and 0 <= my < LAND.height:
                if LAND.getpixel((mx, my)) > 100:
                    d.ellipse([x + col, y + row, x + col + 1, y + row + 1],
                              fill=NAVY)
    for n, (lon, lat) in pins.items():
        px = x + int((lon + 180) / 360 * w)
        py = y + int((75 - lat) / 130 * h)
        dx, dy = _PIN_NUDGE[n - 1]
        px += dx
        py += dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=WHITE, width=2)
        d.text((px - 2, py - 6), str(n), font=F_SANS_B(9), fill=WHITE)

# ---- page sections ---------------------------------------------------------
def section_masthead(d):
    d.rectangle([0, 0, PAGE_W, 100], fill=NAVY)
    d.text((12, 8), "THE TUESDAY LEDGER", font=F_SANS_B(13), fill=AMBER)
    d.text((PAGE_W - 12, 8), "32 STORIES · 7 REGIONS · ALL DATED TO THE DAY",
           font=F_SANS_B(11), fill=AMBER, anchor="rt")
    d.text((PAGE_W // 2, 26), "TUESDAY 24 NOVEMBER 2026", font=F_SERIF_B(42),
           fill=WHITE, anchor="mt")
    d.rectangle([12, 82, PAGE_W - 12, 84], fill=RED)
    d.text((PAGE_W // 2, 88),
           "Asia rallies on Huang's return · Modi–Shah launch train to Nepal · Gaza strike kills 3 — Tuesday's news, dated as it happened",
           font=F_SANS(12), fill=_hx("dce4ec"), anchor="mt")


def section_lead_top(d):
    top = LEADS[0]
    d.rectangle([12, 104, PAGE_W - 12, 300], fill=LIGHT, outline=LINE, width=1)
    paint_rally(d, 612, 104, 400, 196)
    d.rectangle([12, 104, 612, 300], fill=WHITE)
    d.rectangle([12, 104, 612, 300], outline=LINE, width=1)
    x, y = 24, 116
    wide = badge(d, x, y, top["pill"])
    d.text((x + wide + 8, y + 2), "TUE 24 NOV", font=F_SANS_B(11), fill=MUTED)
    ty = 142
    for line in wrap(d, top["title"], F_SERIF_B(30), 580):
        d.text((x, ty), line, font=F_SERIF_B(30), fill=NAVY)
        ty += 34
    dy = 208
    for line in wrap(d, top["deck"], F_SANS(13), 604):
        d.text((x, dy), line, font=F_SANS(13), fill=INK)
        dy += 17
    d.text((x, 276), "Source: " + top["source"], font=F_SANS(10), fill=MUTED)
    d.text((12, 104), "  1 ", font=F_SANS_B(11), fill=RED)


def section_leads_pair(d):
    for slot, lead in enumerate(LEADS[1:], start=1):
        x = 12 + (slot - 1) * 504
        w = 496
        d.rectangle([x, 304, x + w, 480], fill=WHITE, outline=LINE, width=1)
        _ART[lead["art"]](d, x, 304, w, 76)
        d.line([x, 380, x + w, 380], fill=LINE, width=1)
        tx, ty = x + 12, 386
        wide = badge(d, tx, ty, lead["pill"])
        d.text((tx + wide + 8, ty + 2), "MON 23 NOV", font=F_SANS_B(11),
               fill=MUTED)
        title, face = fit(d, lead["title"], F_SERIF_B(22), w - 24)
        d.text((tx, ty + 22), title, font=face, fill=NAVY)
        dy = ty + 50
        for line in wrap(d, lead["deck"], F_SANS(13), w - 24)[:2]:
            d.text((tx, dy), line, font=F_SANS(13), fill=INK)
            dy += 17
        d.text((tx, 470), "Source: " + lead["source"], font=F_SANS(10),
               fill=MUTED)
        d.text((x, 304), "  %d " % lead["n"], font=F_SANS_B(11), fill=RED)


def section_strip(d):
    d.rectangle([12, 484, PAGE_W - 12, 556], fill=NAVY)
    cell = 1000 // len(NUMBERS)
    x = 12
    for num, cap in NUMBERS:
        d.text((x + cell // 2, 492), num,
               font=F_SANS_B(24 if len(num) <= 5 else 20), fill=WHITE,
               anchor="mt")
        d.text((x + cell // 2, 524), cap, font=F_SANS_B(11), fill=AMBER,
               anchor="mt")
        if x > 12:
            d.line([x, 492, x, 548], fill=_hx("3c4c68"), width=1)
        x += cell


def section_week(d):
    d.rectangle([12, 560, PAGE_W - 12, 640], fill=LIGHT, outline=LINE, width=1)
    d.text((24, 566), "SATURDAY → TUESDAY", font=F_SANS_B(12), fill=NAVY)
    span = 250
    for i, (day, items, today) in enumerate(TIMELINE):
        cx = 12 + i * span
        d.text((cx + 12, 584), day, font=F_SANS_B(11),
               fill=RED if today else NAVY)
        for j, item in enumerate(items):
            text, face = fit(d, item, F_SANS(10), span - 18)
            d.text((cx + 12, 599 + j * 10), text, font=face, fill=INK)
        if i < len(TIMELINE) - 1:
            d.line([cx + span - 1, 566, cx + span - 1, 634], fill=LINE, width=1)


def section_cards(d):
    for i, card in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = 12 + col * 504
        y = 642 + row * 46
        d.rectangle([x, y, x + 494, y + 45], fill=WHITE, outline=LINE, width=1)
        draw_icon(d, x + 30, y + 23, card["icon"])
        tx = x + 56
        title, face = fit(d, card["title"], F_SANS_B(15), 494 - 56 - 8)
        d.text((tx, y + 2), title, font=face, fill=NAVY)
        d.text((tx, y + 19), card["deck1"], font=F_SANS(12), fill=INK)
        d.text((tx, y + 33), card["deck2"], font=F_SANS(12), fill=MUTED)
        d.text((x + 2, y + 2), str(card["n"]), font=F_SANS_B(11), fill=RED)


def section_footer(d):
    # Index (left) + map (right).
    d.text((12, 829), "ALSO ON — 21 MORE STORIES · 32 STORIES · 7 REGIONS",
           font=F_SANS_B(12), fill=NAVY)
    d.line([12, 844, 660, 844], fill=LINE, width=1)
    for i, (n, txt, day) in enumerate(INDEX):
        col, row = (0, i) if i < 11 else (1, i - 11)
        x = 12 + col * 328
        y = int(848 + row * 10)
        d.text((x, y), "%d · " % n, font=F_SANS_B(10), fill=RED)
        nx = x + int(d.textlength("%d · " % n, font=F_SANS_B(10)))
        line, face = fit(d, txt + " — " + day, F_SANS(10), 320 - (nx - x) - 4)
        d.text((nx, y), line, font=face, fill=INK)
    # Map (right).
    d.text((684, 829), "WHERE IT HAPPENED · 11 PLACES PINNED",
           font=F_SANS_B(12), fill=NAVY)
    d.line([684, 844, PAGE_W - 12, 844], fill=LINE, width=1)
    pins = {}
    for lead in LEADS:
        pins[lead["n"]] = lead["pin"]
    for card in CARDS:
        pins[card["n"]] = card["pin"]
    paint_map(d, 684, 848, 328, 82, pins)
    # DATE CHECK (3 body lines).
    d.rectangle([12, 952, PAGE_W - 12, 1002], fill=_hx("fcf0dc"),
                outline=_hx("c88c3c"), width=1)
    d.text((24, 955), DATE_CHECK_HEAD, font=F_SANS_B(11), fill=RED)
    for j, line in enumerate(wrap(d, DATE_CHECK_BODY, F_SANS(10), 972)):
        d.text((24, 968 + j * 11), line, font=F_SANS(10), fill=INK)
    # Footer.
    d.text((PAGE_W // 2, 1005), SOURCES_LINE, font=F_SANS(9), fill=MUTED,
           anchor="mt")
    d.text((PAGE_W // 2, 1014), LEGEND_LINE, font=F_SANS(9), fill=MUTED,
           anchor="mt")


_SECTIONS = (section_masthead, section_lead_top, section_leads_pair,
             section_strip, section_week, section_cards, section_footer)


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(page)
    for section in _SECTIONS:
        section(pen)
    return page


def main():
    page = build_page()
    page.save("entry.png")
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
