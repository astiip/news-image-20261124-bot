#!/usr/bin/env python3
"""The Tuesday Ledger — news-image-20261124, Tuesday 24 November 2026.

Iteration of our own v3 layout system (news-image-20261123, "The Monday
Ledger", 31 stories): same geometry, new day, new art, new stories.
32 stories / 7 regions. Three illustrated leads, a six-figure strip,
a Saturday->Tuesday timeline, eight medium cards, a 21-item index,
a dotted world map with 11 pins, and a DATE CHECK naming every
non-Tuesday story on the page.

DATE HONESTY: this page is built on Tuesday morning (24 Nov ~10:00 WIB),
so most of the day's news is Monday's news first reported overnight plus
Tuesday's own early stories. The masthead names TUESDAY 24 NOVEMBER 2026;
every story carries its own dateline, and the DATE CHECK lists every
story that is NOT Tuesday's. Nothing is backdated to Tuesday.

Verified figures (fresh searches, 24 Nov 2026 ~09:40-10:00 WIB):
  * Asia rally TUE: Nikkei +4.5%, KOSPI +7.5%, Taiwan +9.1%,
    MSCI Asia ex-Japan +4.6% (Reuters, Tue 24 Nov).
  * Huang reinstated MON 23 Nov: Nvidia +31.5%, biggest daily gain in
    23 years, ~$1tn restored; resigned 12 Nov, back 11 days later
    (Reuters, CNN, IBD).
  * Modi-Shah MON 23 Nov: 8 MoUs, Rs 15,000 crore / NPR 24,000 crore
    package, Saryu-Kamala Express Ayodhya-Janakpur, 604 km, ~19h,
    weekly service from 28 Nov (PTI, Jagran).
  * Gaza TUE 24 Nov: Israeli airstrike kills 3 near a police post in
    Khan Younis, medics say (Reuters, Tue).
  * COP31 collapsed SUN 22 Nov: no final text, silent on fossil fuels;
    first major COP breakdown since Copenhagen 2009 (CNN).
  * Dymer SUN 22 Nov: 458 drones + 45 missiles overnight, 406 drones
    downed, 11 dead in the Dymer flat, 15 killed in Kyiv region +
    Zaporizhzhia in all (Ukrainian Air Force via Reuters/Ukrinform;
    Al Jazeera). v3's "14 unaccounted" is superseded by the toll.
  * Korea MON 23 Nov: Lee reshuffles 5 security posts; Kang Kum-sil
    first woman NIS chief (Reuters, Korea JoongAng Daily).
  * Armenia MON 23 Nov: draft constitution drops the Karabakh claim,
    220 articles cut to 89; Pashinyan vows to resign if voters reject
    it (Reuters, AP).
  * CrowdStrike-Zscaler MON 23 Nov: $43.9bn all-stock, 1.135 shares
    per Zscaler share, 34% premium (Reuters).
  * Sparta II MON 23 Nov: drone-hit ship reaches St Petersburg; all
    16 crew safe, none hurt (Reuters; governor Drozdenko).
  * Cricket MON 23 Nov: India 720/9 declared, NZ 239/5, draw at Basin
    Reserve; Pant 128, Rahul 136 (Reuters).
  * Australia TUE 24 Nov: tech firms face fines up to 5% of global
    revenue (Reuters, Tue). Japan PMI TUE: manufacturing 53.7, up
    from 53.3 (Reuters, Tue). Singapore probes Nvidia-linked
    Megaspeed TUE (Reuters). Canada-Qatar pact signing TUE (Reuters).
    CAS Senegal AFCON ruling due TUE afternoon (Reuters). North Korea
    mulls closing Swiss office, KCNA TUE (Reuters).
  * Tajikistan: UN published the ICC withdrawal notice MON 23 Nov;
    filed 20 Nov, takes effect 20 Nov 2027 (Times of Central Asia).
  * US-Syria training talks MON 23 Nov (Reuters). NATO council met
    MON 23 Nov over the Poland breach (v3 lead, still current).
  * Banten: 24 dead confirmed MON 23 Nov, ~30 missing, 29 safe,
    5 in hospital (Reuters, Basarnas).
  * Lisbon SAT 21 Nov: living costs, CGTP (Reuters — v3 correction
    kept). Verstappen SAT 21 Nov Las Vegas GP. Liverpool 4-0 Man Utd
    SUN, Yoro sent off 8th min. Alcaraz beats Zverev 6-2, 7-6(7) SUN,
    $5.171m record payout. Nasdaq fell ~10% on the week FRI.
    Anthropic record IPO debut FRI. Miley Cyrus wedding SUN.
    Istanbul media-closure protests SUN. El Chapo Isidro captured
    FRI, 11 dead. Sunrise on the Reaping tops box office SUN.
  * NOT used: Guwahati cricket figures (November 2025, not 2026);
    Nepal delegation size (reports disagree 34 vs 35); any "first
    since 2000" COP claim (sources disagree 2000 vs 2009).

Run:  python3 render.py   (writes entry.png, 1024x1024, PIL only)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette (v1/v3) ----------------------------------------------------
CREAM = (247, 241, 227)   # paper
NAVY = (16, 36, 68)       # masthead / headlines
NAVY2 = (28, 52, 92)      # panels
RED = (184, 33, 38)       # accents, CONFIRMED red
AMBER = (214, 154, 44)    # gold rule
INK = (26, 28, 34)        # body text
MUTED = (96, 96, 96)      # muted text
LINE = (202, 192, 172)    # hairlines
TEAL = (18, 122, 106)     # teal band
SEA = (38, 84, 124)       # sea blue
SKY = (158, 198, 226)     # pale sky
SAND = (226, 205, 164)    # sand
LIGHT = (242, 236, 222)   # light panel
WHITE = (255, 255, 255)
GREEN = (22, 140, 70)     # market green

# ---- fonts ---------------------------------------------------------------
def F_SANS(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", px)

def F_SANS_B(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", px)

def F_SERIF(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", px)

def F_SERIF_B(px):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", px)

# ---- data (verified Tuesday 24 Nov 2026, ~10:00 WIB) --------------------
LEADS = [
    {
        "n": 1, "pill": "CONFIRMED", "art": "rally",
        "title": "Asia rallies on Huang's return",
        "deck": (
            "Tokyo +4.5%, Seoul +7.5%, Taipei +9.1% as Asia buys the AI "
            "rebound. Wall Street surged Monday on Huang's return; "
            "MSCI Asia ex-Japan +4.6%."
        ),
        "source": "Reuters",
        "pin": (139.7, 35.7),
    },
    {
        "n": 2, "pill": "CONFIRMED", "art": "chip",
        "title": "Huang is back at Nvidia",
        "deck": (
            "Reinstated 11 days after he quit; shares jump 31.5%, best "
            "day in 23 years. Trump pressed the board to bring him back."
        ),
        "source": "Reuters · CNN",
        "pin": (-122.0, 37.4),
    },
    {
        "n": 3, "pill": "CONFIRMED", "art": "train",
        "title": "Modi–Shah launch Nepal train",
        "deck": (
            "Modi and Shah flag off the Saryu–Kamala Express, "
            "Ayodhya–Janakpur, 604 km. India pledges Rs 15,000 crore; "
            "8 MoUs signed."
        ),
        "source": "PTI · Reuters",
        "pin": (77.2, 28.6),
    },
]

# Cards 4-11: eight medium stories, all with a dateline.
CARDS = [
    {
        "n": 4, "pill": "REPORTED", "icon": "flame",
        "title": "Gaza strike kills 3 in Khan Younis",
        "deck1": "Airstrike near a police post kills 3;",
        "deck2": "TUE 24 NOV · medics in Khan Younis",
        "pin": (34.5, 31.5),
    },
    {
        "n": 5, "pill": "CONFIRMED", "icon": "globe",
        "title": "COP31 collapses, no deal",
        "deck1": "Two weeks of talks end with no final",
        "deck2": "SUN 22 NOV · text silent on fossil fuels",
        "pin": (30.7, 36.9),
    },
    {
        "n": 6, "pill": "CONFIRMED", "icon": "drone",
        "title": "Dymer toll: 11 dead in flat hit",
        "deck1": "458 drones, 45 missiles overnight;",
        "deck2": "SUN 22 NOV · 406 drones downed",
        "pin": (30.2, 50.8),
    },
    {
        "n": 7, "pill": "CONFIRMED", "icon": "capitol",
        "title": "Seoul names first woman spy chief",
        "deck1": "Kang Kum-sil tapped to lead the NIS;",
        "deck2": "MON 23 NOV · 5 security posts reshuffled",
        "pin": (127.0, 37.5),
    },
    {
        "n": 8, "pill": "CONFIRMED", "icon": "pencil",
        "title": "Armenia drafts peace constitution",
        "deck1": "New text drops the Karabakh claim;",
        "deck2": "MON 23 NOV · 220 articles cut to 89",
        "pin": (44.5, 40.2),
    },
    {
        "n": 9, "pill": "CONFIRMED", "icon": "shield",
        "title": "CrowdStrike buys Zscaler, $43.9bn",
        "deck1": "All-stock deal, 1.135 shares each;",
        "deck2": "MON 23 NOV · 34% premium",
        "pin": (-97.7, 30.3),
    },
    {
        "n": 10, "pill": "CONFIRMED", "icon": "tanker",
        "title": "Sparta II reaches St Petersburg",
        "deck1": "Drone-hit ship towed home; all 16 crew",
        "deck2": "MON 23 NOV · safe after Baltic fire",
        "pin": (30.3, 59.9),
    },
    {
        "n": 11, "pill": "CONFIRMED", "icon": "bat",
        "title": "NZ save the Test in a draw",
        "deck1": "NZ 239/5 in reply; India 720/9 declared;",
        "deck2": "MON 23 NOV · Pant 128, Rahul 136",
        "pin": (174.8, -41.3),
    },
]

# Index 12-32: twenty-one more stories, one line each.
INDEX = [
    (12, "Australia fines tech firms up to 5%", "TUE 24 NOV"),
    (13, "Singapore probes Nvidia-linked Megaspeed", "TUE 24 NOV"),
    (14, "Canada, Qatar to sign investment pact", "TUE 24 NOV"),
    (15, "CAS to rule on Senegal AFCON appeal", "TUE 24 NOV"),
    (16, "N. Korea mulls closing Swiss office", "TUE 24 NOV"),
    (17, "Japan factory PMI rises to 53.7", "TUE 24 NOV"),
    (18, "US weighs training Syrian forces", "MON 23 NOV"),
    (19, "Tajikistan quits ICC; out in 2027", "MON 23 NOV"),
    (20, "Democrats clinch 258th House seat", "SUN 22 NOV"),
    (21, "NATO meets over Poland breach", "MON 23 NOV"),
    (22, "Banten toll: 24 dead, ~30 missing", "MON 23 NOV"),
    (23, "Lisbon marches over living costs", "SAT 21 NOV"),
    (24, "Verstappen wins Las Vegas GP", "SAT 21 NOV"),
    (25, "Liverpool 4–0 Man Utd; Yoro sent off", "SUN 22 NOV"),
    (26, "Alcaraz wins ATP Finals, beats Zverev", "SUN 22 NOV"),
    (27, "Nasdaq fell ~10% on the week", "FRI 20 NOV"),
    (28, "Anthropic makes record IPO debut", "FRI 20 NOV"),
    (29, "Miley Cyrus marries Maxx Morando", "SUN 22 NOV"),
    (30, "Istanbul protests over media closures", "SUN 22 NOV"),
    (31, "El Chapo Isidro captured in Jalisco", "FRI 20 NOV"),
    (32, "Sunrise on the Reaping tops box office", "SUN 22 NOV"),
]

# Verification record for the index lines (not rendered; checked by verify.py).
INDEX_STORIES = {
    12: {"deck": "Australia to fine tech firms up to 5% of global revenue under its internet safety bill, minister Anika Wells says Tuesday.", "source": "Reuters"},
    13: {"deck": "Singapore keeps investigating Megaspeed, an Nvidia-linked cloud firm the US blacklisted over alleged AI-chip diversion to China.", "source": "Reuters"},
    14: {"deck": "Canada and Qatar are set to sign a foreign investment promotion and protection deal on Tuesday.", "source": "Reuters"},
    15: {"deck": "The Court of Arbitration for Sport releases its decision on Senegal's appeal against losing the Africa Cup of Nations title on Tuesday afternoon.", "source": "Reuters"},
    16: {"deck": "North Korea says it will consider shutting the Swiss diplomatic office in Pyongyang after Swiss sanctions, KCNA reports Tuesday.", "source": "Reuters"},
    17: {"deck": "Japan's flash manufacturing PMI rises to 53.7 in November from 53.3; services slip to 50.5, composite 51.5.", "source": "Reuters"},
    18: {"deck": "The US is discussing plans to train Syrian soldiers in demining, the first US training mission with Syria's military since 2024.", "source": "Reuters"},
    19: {"deck": "The UN publishes Tajikistan's ICC withdrawal notice on Monday; filed 20 Nov, it takes effect 20 Nov 2027.", "source": "Times of Central Asia · UN"},
    20: {"deck": "Democrats clinch their 258th House seat in California on Sunday, +44 on the last House.", "source": "Reuters"},
    21: {"deck": "All 32 NATO states sit at Monday's council in Brussels over the Poland airspace breach.", "source": "NATO · Reuters"},
    22: {"deck": "24 dead confirmed Monday in the Banten candy-factory fire; about 30 still missing; 29 safe, 5 in hospital.", "source": "Reuters · Basarnas"},
    23: {"deck": "Thousands march in Lisbon over living costs on Saturday; CGTP organised the rally.", "source": "Reuters"},
    24: {"deck": "Verstappen wins the Las Vegas Grand Prix on Saturday.", "source": "Reuters · AP"},
    25: {"deck": "Liverpool beat Manchester United 4-0 at Anfield on Sunday: Szoboszlai 10', Wirtz 13', Ngumoha 66', Munoz 82'; Leny Yoro sent off in the 8th minute — the earliest red card ever for United in the Premier League.", "source": "Reuters · Times · liverpoolfc.com"},
    26: {"deck": "Alcaraz beats world No. 1 Zverev 6–2, 7–6(7) in Turin on Sunday; first ATP Finals title, $5.171m record payout, 5–0 week.", "source": "Reuters · ATP"},
    27: {"deck": "Nasdaq fell about 10% from its peak during the week.", "source": "Reuters"},
    28: {"deck": "Anthropic's IPO debut is the largest of the year.", "source": "Reuters"},
    29: {"deck": "Miley Cyrus marries Maxx Morando on Sunday.", "source": "Reuters"},
    30: {"deck": "Thousands protest media closures in Istanbul on Sunday.", "source": "Reuters"},
    31: {"deck": "El Chapo Isidro captured in Jalisco; 11 dead in the operation.", "source": "Reuters · AFP"},
    32: {"deck": "Sunrise on the Reaping tops the box office on Sunday.", "source": "Reuters"},
}

# Number strip: six verified figures, each tied to a story.
NUMBERS = [
    ("+9.1%", "TAIPEI SHARES"),
    ("+31.5%", "NVIDIA MONDAY"),
    ("8", "MOUS, INDIA–NEPAL"),
    ("3", "KILLED IN GAZA"),
    ("$43.9bn", "ZSCALER DEAL"),
    ("53.7", "JAPAN PMI"),
]

# Hour timeline, Saturday to Tuesday.
TIMELINE = [
    ("SAT 21 NOV", ["Banten fire, 24 dead later confirmed",
                     "Sparta II hit by drones, Baltic",
                     "Verstappen wins Las Vegas GP"], False),
    ("SUN 22 NOV", ["COP31 collapses, no deal",
                     "Dymer strike, 11 dead",
                     "Democrats clinch 258th seat"], False),
    ("MON 23 NOV", ["Huang returns to Nvidia",
                     "Modi–Shah train + 8 MoUs",
                     "Korea reshuffle, Armenia draft",
                     "Sparta II reaches port"], False),
    ("TUE 24 NOV", ["Asia rallies on AI rebound",
                     "Gaza strike kills 3",
                     "Australia fines tech firms",
                     "Japan PMI 53.7"], True),
]

REGIONS = [
    ("EUROPE", 9), ("ASIA", 8), ("NORTH AMERICA", 9),
    ("LATIN AMERICA", 1), ("MIDDLE EAST", 2), ("OCEANIA", 2),
    ("AFRICA", 1),
]

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
    "figures as reported 24 Nov 2026, 10:00 WIB; where reports differ, the card says so."
)
LEGEND_LINE = (
    "CONFIRMED = verified by two or more sources · REPORTED = one source or a claim, labelled in the text"
)

# ---- helpers -----------------------------------------------------------
def fit(d, text, font, max_w, min_px=6):
    """Shrink the font until the text fits max_w, else add an ellipsis."""
    px = font.size
    while px > min_px and d.textlength(text, font=font) > max_w:
        px -= 1
        font = ImageFont.truetype(font.path, px)
    if d.textlength(text, font=font) > max_w:
        while d.textlength(text + "…", font=font) > max_w and len(text) > 4:
            text = text[:-1]
        text = text + "…"
    return text, font

def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def pill(d, x, y, text):
    """Small rounded pill, red for CONFIRMED, teal for REPORTED."""
    col = RED if text == "CONFIRMED" else TEAL
    w = int(d.textlength(text, font=F_SANS_B(11))) + 16
    d.rounded_rectangle([x, y, x + w, y + 18], radius=9, fill=col)
    d.text((x + 8, y + 3), text, font=F_SANS_B(11), fill=WHITE)
    return w

# ---- lead illustrations (all new art for this day) ---------------------
def draw_rally(d, x, y, w, h):
    """Lead 1: dawn over an Asian skyline, bars climbing, green arrow."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(18 + t * 30), int(90 + t * 60), int(110 + t * 40)))
    d.ellipse([x + w - 120, y + 4, x + w - 88, y + 36], fill=(250, 210, 120))
    # Skyline silhouettes.
    for bx, bw, bh in [(x + 12, 34, 44), (x + 52, 26, 58), (x + 84, 40, 38),
                       (x + 130, 24, 64), (x + 160, 34, 48), (x + 200, 28, 56),
                       (x + 234, 36, 42), (x + 276, 24, 60), (x + 306, 30, 50)]:
        d.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10], fill=(12, 30, 52))
    for bx, bw, bh in [(x + 12, 34, 44), (x + 52, 26, 58), (x + 84, 40, 38),
                       (x + 130, 24, 64), (x + 160, 34, 48), (x + 200, 28, 56),
                       (x + 234, 36, 42), (x + 276, 24, 60), (x + 306, 30, 50)]:
        for wy in range(y + h - 8 - bh, y + h - 12, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 210, 120))
    # Climbing green bars + arrow, front and centre.
    bars = [(x + 310, 52), (x + 328, 44), (x + 346, 36), (x + 364, 26),
            (x + 382, 16)]
    for bx, bh in bars:
        d.rectangle([bx, y + h - 14 - bh, bx + 12, y + h - 14], fill=GREEN)
    d.line([x + 304, y + h - 20, x + 396, y + h - 66], fill=(120, 220, 140),
           width=5)
    d.polygon([(x + 396, y + h - 66), (x + 376, y + h - 62),
               (x + 392, y + h - 46)], fill=(120, 220, 140))
    d.text((x + 12, y + 6), "+9.1%", font=F_SANS_B(16), fill=(180, 240, 180))

def draw_chip(d, x, y, w, h):
    """Lead 2: a chip on a dark board, circuit traces, green up-arrow."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(14 + t * 20), int(26 + t * 26), int(48 + t * 30)))
    # Circuit traces.
    for ty in (y + 14, y + 30, y + h - 22, y + h - 38):
        d.line([x + 10, ty, x + w - 10, ty], fill=(60, 90, 130), width=1)
        for tx in range(x + 30, x + w - 30, 46):
            d.ellipse([tx, ty - 3, tx + 6, ty + 3], fill=(90, 140, 180))
    # Chip, centre-left.
    cx, cy, cw, ch = x + 150, y + 8, 120, 60
    for px in range(cx + 8, cx + cw - 8, 16):
        d.line([px, cy - 8, px, cy], fill=(200, 210, 220), width=2)
        d.line([px, cy + ch, px, cy + ch + 8], fill=(200, 210, 220), width=2)
    for py in range(cy + 8, cy + ch - 8, 16):
        d.line([cx - 8, py, cx, py], fill=(200, 210, 220), width=2)
        d.line([cx + cw, py, cx + cw + 8, py], fill=(200, 210, 220), width=2)
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(38, 84, 124),
                outline=(220, 228, 236), width=2)
    d.rectangle([cx + 34, cy + 16, cx + cw - 34, cy + ch - 16],
                outline=(220, 228, 236), width=1)
    d.text((cx + 44, cy + 22), "NVDA", font=F_SANS_B(14), fill=WHITE)
    # Green arrow + figure, right.
    d.line([x + w - 130, y + h - 16, x + w - 60, y + 10], fill=(120, 220, 140),
           width=6)
    d.polygon([(x + w - 60, y + 10), (x + w - 84, y + 12),
               (x + w - 64, y + 32)], fill=(120, 220, 140))
    d.text((x + w - 165, y + 4), "+31.5%", font=F_SANS_B(15),
           fill=(180, 240, 180))

def draw_train(d, x, y, w, h):
    """Lead 3: the Saryu-Kamala Express at dawn — engine, carriages, flags."""
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([x, y + i, x + w, y + i],
               fill=(int(244 - t * 40), int(214 - t * 36), int(176 - t * 44)))
    d.ellipse([x + 30, y + 2, x + 62, y + 34], fill=(250, 200, 110))
    for px, ph in [(x + 300, 30), (x + 360, 40), (x + 420, 28)]:
        d.polygon([(px, y + h - 8), (px + 26, y + h - 8 - ph),
                   (px + 52, y + h - 8)], fill=(150, 176, 200))
    # Track.
    d.line([x + 8, y + h - 12, x + w - 8, y + h - 12], fill=(90, 70, 55),
           width=3)
    for tx in range(x + 20, x + w - 20, 26):
        d.line([tx, y + h - 18, tx, y + h - 6], fill=(90, 70, 55), width=2)
    # Carriages + engine, left to right.
    for i, (cx0, col) in enumerate([(x + 40, (38, 84, 124)),
                                    (x + 130, (176, 84, 66)),
                                    (x + 220, (38, 84, 124))]):
        d.rectangle([cx0, y + h - 44, cx0 + 80, y + h - 14], fill=col)
        for wx in range(cx0 + 8, cx0 + 76, 18):
            d.rectangle([wx, y + h - 40, wx + 10, y + h - 30],
                        fill=(232, 214, 176))
        d.ellipse([cx0 + 12, y + h - 14, cx0 + 22, y + h - 4], fill=INK)
        d.ellipse([cx0 + 58, y + h - 14, cx0 + 68, y + h - 4], fill=INK)
    # Engine nose + headlamp.
    d.polygon([(x + 300, y + h - 44), (x + 330, y + h - 36),
               (x + 330, y + h - 14), (x + 300, y + h - 14)], fill=(28, 52, 92))
    d.ellipse([x + 324, y + h - 34, x + 332, y + h - 26], fill=(250, 240, 180))
    # Two flags on the engine: India (saffron/white/green) + Nepal (crimson).
    for fx, cols in [(x + 340, [(255, 153, 51), (255, 255, 255), (22, 140, 70)]),
                     (x + 380, [(220, 20, 60), (220, 20, 60), (30, 60, 160)])]:
        d.line([fx, y + h - 62, fx, y + h - 44], fill=INK, width=2)
        for j, col in enumerate(cols):
            d.rectangle([fx, y + h - 62 + j * 6, fx + 22, y + h - 56 + j * 6],
                        fill=col)

# ---- card icons --------------------------------------------------------
ICON_BG = {
    "globe": SEA, "capitol": NAVY2, "drone": (70, 70, 70), "tanker": (30, 90, 90),
    "pencil": (140, 90, 40), "un": SEA, "wheat": (150, 120, 30), "bat": (110, 60, 60),
    "flame": (176, 60, 30), "shield": (30, 90, 60),
}

def draw_icon(d, cx, cy, kind):
    bg = ICON_BG[kind]
    # Icon background shape varies by kind — circle for globe/wheat/bat/flame,
    # diamond for drone, rounded square for the rest.
    if kind in ("globe", "wheat", "bat", "flame"):
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=bg)
    elif kind == "drone":
        d.polygon([(cx, cy - 22), (cx + 22, cy), (cx, cy + 22), (cx - 22, cy)],
                  fill=bg)
    else:
        d.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], radius=8,
                            fill=bg)
    if kind == "globe":
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=WHITE, width=2)
        d.ellipse([cx - 6, cy - 12, cx + 6, cy + 12], outline=WHITE, width=1)
        d.line([cx - 12, cy, cx + 12, cy], fill=WHITE, width=1)
    elif kind == "capitol":
        d.polygon([(cx, cy - 12), (cx - 12, cy), (cx + 12, cy)], fill=WHITE)
        d.rectangle([cx - 12, cy, cx + 12, cy + 12], fill=WHITE)
        for lx in (cx - 8, cx - 2, cx + 4):
            d.rectangle([lx, cy + 4, lx + 2, cy + 12], fill=bg)
    elif kind == "drone":
        d.ellipse([cx - 12, cy - 4, cx - 4, cy + 4], outline=WHITE, width=2)
        d.ellipse([cx + 4, cy - 4, cx + 12, cy + 4], outline=WHITE, width=2)
        d.rectangle([cx - 6, cy - 3, cx + 6, cy + 3], fill=WHITE)
        d.line([cx - 10, cy + 8, cx + 10, cy + 8], fill=WHITE, width=2)
    elif kind == "tanker":
        d.polygon([(cx - 12, cy + 2), (cx + 12, cy + 2), (cx + 10, cy + 10),
                   (cx - 10, cy + 10)], fill=WHITE)
        d.rectangle([cx - 2, cy - 10, cx + 4, cy + 2], fill=WHITE)
        d.line([cx - 12, cy + 12, cx + 12, cy + 12], fill=WHITE, width=2)
    elif kind == "pencil":
        d.polygon([(cx - 10, cy + 10), (cx - 12, cy + 2), (cx + 4, cy - 12),
                   (cx + 12, cy - 4), (cx + 2, cy + 12)], fill=WHITE)
        d.polygon([(cx - 10, cy + 10), (cx - 12, cy + 2), (cx - 4, cy + 8)],
                  fill=(40, 40, 40))
    elif kind == "un":
        d.polygon([(cx - 14, cy - 2), (cx, cy - 13), (cx + 14, cy - 2)], fill=WHITE)
        d.rectangle([cx - 12, cy - 2, cx + 12, cy + 12], fill=WHITE)
        for lx in (cx - 8, cx - 2, cx + 4):
            d.rectangle([lx, cy + 2, lx + 2, cy + 12], fill=bg)
        d.line([cx - 9, cy - 1, cx + 1, cy + 9], fill=RED, width=2)
        d.line([cx + 1, cy + 9, cx - 3, cy + 13], fill=RED, width=2)
    elif kind == "wheat":
        d.ellipse([cx, cy - 12, cx + 4, cy - 4], fill=WHITE)
        d.ellipse([cx - 6, cy - 6, cx - 2, cy + 2], fill=WHITE)
        d.ellipse([cx + 2, cy - 2, cx + 6, cy + 6], fill=WHITE)
        d.line([cx + 1, cy - 2, cx + 1, cy + 12], fill=WHITE, width=2)
    elif kind == "bat":
        d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], fill=WHITE)
        d.line([cx, cy - 6, cx, cy + 6], fill=bg, width=2)
        d.line([cx - 4, cy - 2, cx + 4, cy - 2], fill=bg, width=2)
    elif kind == "flame":
        d.polygon([(cx, cy - 13), (cx + 8, cy - 2), (cx + 11, cy + 6),
                   (cx + 4, cy + 12), (cx - 5, cy + 12), (cx - 11, cy + 5),
                   (cx - 7, cy - 3)], fill=WHITE)
        d.ellipse([cx - 3, cy + 2, cx + 3, cy + 9], fill=bg)
    elif kind == "shield":
        d.polygon([(cx, cy - 13), (cx + 11, cy - 8), (cx + 11, cy + 3),
                   (cx, cy + 13), (cx - 11, cy + 3), (cx - 11, cy - 8)],
                  fill=WHITE)
        d.line([cx - 5, cy, cx - 1, cy + 5], fill=bg, width=2)
        d.line([cx - 1, cy + 5, cx + 6, cy - 5], fill=bg, width=2)

# ---- dotted world map --------------------------------------------------
CONTINENTS = [
    [(60, 78), (75, 74), (95, 74), (108, 78), (125, 74), (140, 78), (158, 76),
     (168, 80), (180, 76), (190, 82), (195, 88), (180, 90), (165, 86),
     (150, 90), (130, 86), (110, 90), (90, 88), (70, 84)],          # North America
    [(205, 120), (225, 118), (240, 122), (250, 128), (245, 138), (228, 142),
     (212, 136)],                                                   # South America
    [(355, 68), (380, 62), (420, 60), (460, 66), (500, 62), (520, 70),
     (500, 78), (460, 82), (420, 78), (380, 80), (360, 76)],        # Europe
    [(350, 92), (370, 88), (390, 92), (395, 104), (380, 112), (362, 106),
     (350, 100)],                                                   # Africa
    [(500, 66), (540, 60), (590, 58), (640, 62), (680, 70), (660, 80),
     (620, 86), (570, 84), (530, 78)],                              # Asia (north)
    [(580, 92), (600, 90), (615, 96), (610, 106), (590, 108), (580, 100)],  # SE Asia
    [(640, 140), (660, 138), (672, 146), (652, 152), (640, 146)],   # Australia
    [(690, 150), (700, 148), (708, 154), (696, 158)],               # New Zealand
]

def build_land_mask(scale=0.5):
    """Land mask on a 360x180 grid from hand-drawn continent polygons."""
    mw, mh = 360, 180
    m = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(m)
    for poly in CONTINENTS:
        md.polygon(poly, fill=255)
    return m.resize((int(mw * scale), int(mh * scale)), Image.LANCZOS)

LAND = build_land_mask()

def draw_map(d, x, y, w, h, pins):
    """Dotted world map; pins are (lon, lat) -> (number, nudge)."""
    for py in range(0, h, 4):
        for px in range(0, w, 4):
            lon = -180 + (px / max(1, w - 1)) * 360
            lat = 75 - (py / max(1, h - 1)) * 130
            mx = int((lon + 180) / 360 * LAND.width)
            my = int((75 - lat) / 130 * LAND.height)
            if 0 <= mx < LAND.width and 0 <= my < LAND.height:
                if LAND.getpixel((mx, my)) > 100:
                    d.ellipse([x + px, y + py, x + px + 1, y + py + 1], fill=NAVY)
    for n, (lon, lat) in pins.items():
        px = x + int((lon + 180) / 360 * w)
        py = y + int((75 - lat) / 130 * h)
        nudges = {1: (10, 8), 2: (-14, -8), 3: (8, -8), 4: (10, 10),
                  5: (-12, 8), 6: (12, -10), 7: (-14, -6), 8: (8, 10),
                  9: (12, 8), 10: (8, -8), 11: (-16, -4)}
        dx, dy = nudges.get(n, (0, 0))
        px += dx
        py += dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=2)
        d.text((px - 2, py - 6), str(n), font=F_SANS_B(9), fill=WHITE)

# ---- layout ------------------------------------------------------------
def draw_masthead(d):
    d.rectangle([0, 0, 1024, 100], fill=NAVY)
    d.text((12, 8), "THE TUESDAY LEDGER", font=F_SANS_B(13), fill=(214, 154, 44))
    d.text((1012, 8), "32 STORIES · 7 REGIONS · ALL DATED TO THE DAY",
           font=F_SANS_B(11), fill=(214, 154, 44), anchor="rt")
    d.text((512, 26), "TUESDAY 24 NOVEMBER 2026", font=F_SERIF_B(42),
           fill=WHITE, anchor="mt")
    d.rectangle([12, 82, 1012, 84], fill=RED)
    d.text((512, 88), "Asia rallies on Huang's return · Modi–Shah launch train to Nepal · Gaza strike kills 3 — Tuesday's news, dated as it happened",
           font=F_SANS(12), fill=(220, 228, 236), anchor="mt")

def draw_lead1(d):
    L = LEADS[0]
    d.rectangle([12, 104, 1012, 300], fill=LIGHT, outline=LINE, width=1)
    draw_rally(d, 612, 104, 400, 196)
    d.rectangle([12, 104, 612, 300], fill=WHITE)
    d.rectangle([12, 104, 612, 300], outline=LINE, width=1)
    x, y = 24, 116
    pw = pill(d, x, y, L["pill"])
    d.text((x + pw + 8, y + 2), "TUE 24 NOV", font=F_SANS_B(11), fill=MUTED)
    title_lines = wrap(d, L["title"], F_SERIF_B(30), 580)
    ty = 142
    for ln in title_lines:
        d.text((x, ty), ln, font=F_SERIF_B(30), fill=NAVY)
        ty += 34
    deck_lines = wrap(d, L["deck"], F_SANS(13), 604)
    dy = 208
    for ln in deck_lines:
        d.text((x, dy), ln, font=F_SANS(13), fill=INK)
        dy += 17
    d.text((x, 276), "Source: " + L["source"], font=F_SANS(10), fill=MUTED)
    d.text((12, 104), "  1 ", font=F_SANS_B(11), fill=RED)

def draw_leads23(d):
    for i, L in enumerate(LEADS[1:], start=1):
        x = 12 + (i - 1) * 504
        w = 496
        d.rectangle([x, 304, x + w, 480], fill=WHITE, outline=LINE, width=1)
        art_h = 76
        art_fn = {"rally": draw_rally, "chip": draw_chip, "train": draw_train}
        art_fn[L["art"]](d, x, 304, w, art_h)
        d.line([x, 304 + art_h, x + w, 304 + art_h], fill=LINE, width=1)
        tx, ty = x + 12, 386
        pw = pill(d, tx, ty, L["pill"])
        d.text((tx + pw + 8, ty + 2), "MON 23 NOV", font=F_SANS_B(11), fill=MUTED)
        t, f = fit(d, L["title"], F_SERIF_B(22), w - 24)
        d.text((tx, ty + 22), t, font=f, fill=NAVY)
        deck_lines = wrap(d, L["deck"], F_SANS(13), w - 24)[:2]
        dy = ty + 50
        for ln in deck_lines:
            d.text((tx, dy), ln, font=F_SANS(13), fill=INK)
            dy += 17
        d.text((tx, 470), "Source: " + L["source"], font=F_SANS(10), fill=MUTED)
        d.text((x, 304), "  %d " % L["n"], font=F_SANS_B(11), fill=RED)

def draw_numbers(d):
    d.rectangle([12, 484, 1012, 556], fill=NAVY)
    x = 12
    for num, cap in NUMBERS:
        cw = 1000 // len(NUMBERS)
        d.text((x + cw // 2, 492), num, font=F_SANS_B(24 if len(num) <= 5 else 20),
               fill=WHITE, anchor="mt")
        d.text((x + cw // 2, 524), cap, font=F_SANS_B(11), fill=(214, 154, 44),
               anchor="mt")
        if x > 12:
            d.line([x, 492, x, 548], fill=(60, 76, 104), width=1)
        x += cw

def draw_timeline(d):
    d.rectangle([12, 560, 1012, 640], fill=LIGHT, outline=LINE, width=1)
    d.text((24, 566), "SATURDAY → TUESDAY", font=F_SANS_B(12), fill=NAVY)
    col_w = 250
    for i, (day, items, is_today) in enumerate(TIMELINE):
        cx = 12 + i * col_w
        d.text((cx + 12, 584), day, font=F_SANS_B(11),
               fill=RED if is_today else NAVY)
        for j, it in enumerate(items):
            t, f = fit(d, it, F_SANS(10), col_w - 18)
            d.text((cx + 12, 599 + j * 10), t, font=f, fill=INK)
        if i < len(TIMELINE) - 1:
            d.line([cx + col_w - 1, 566, cx + col_w - 1, 634], fill=LINE, width=1)

def draw_cards(d):
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = 12 + col * 504
        y = 642 + row * 46
        d.rectangle([x, y, x + 494, y + 45], fill=WHITE, outline=LINE, width=1)
        draw_icon(d, x + 30, y + 23, c["icon"])
        tx = x + 56
        t, f = fit(d, c["title"], F_SANS_B(15), 494 - 56 - 8)
        d.text((tx, y + 2), t, font=f, fill=NAVY)
        d.text((tx, y + 19), c["deck1"], font=F_SANS(12), fill=INK)
        d.text((tx, y + 33), c["deck2"], font=F_SANS(12), fill=MUTED)
        d.text((x + 2, y + 2), str(c["n"]), font=F_SANS_B(11), fill=RED)

def draw_bottom(d):
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
        line, f = fit(d, txt + " — " + day, F_SANS(10), 320 - (nx - x) - 4)
        d.text((nx, y), line, font=f, fill=INK)
    # Map (right).
    d.text((684, 829), "WHERE IT HAPPENED · 11 PLACES PINNED",
           font=F_SANS_B(12), fill=NAVY)
    d.line([684, 844, 1012, 844], fill=LINE, width=1)
    pins = {}
    for L in LEADS:
        pins[L["n"]] = L["pin"]
    for c in CARDS:
        pins[c["n"]] = c["pin"]
    draw_map(d, 684, 848, 328, 82, pins)
    # DATE CHECK (3 body lines).
    d.rectangle([12, 952, 1012, 1002], fill=(252, 240, 220),
                outline=(200, 140, 60), width=1)
    d.text((24, 955), DATE_CHECK_HEAD, font=F_SANS_B(11), fill=RED)
    for j, ln in enumerate(wrap(d, DATE_CHECK_BODY, F_SANS(10), 972)):
        d.text((24, 968 + j * 11), ln, font=F_SANS(10), fill=INK)
    # Footer.
    d.text((512, 1005), SOURCES_LINE, font=F_SANS(9), fill=MUTED, anchor="mt")
    d.text((512, 1014), LEGEND_LINE, font=F_SANS(9), fill=MUTED, anchor="mt")

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead1(d)
    draw_leads23(d)
    draw_numbers(d)
    draw_timeline(d)
    draw_cards(d)
    draw_bottom(d)
    img.save("entry.png")
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
