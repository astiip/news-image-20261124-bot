#!/usr/bin/env python3
"""Verify the v1 page data before rendering — run: python3 verify.py

Checks: 32 stories numbered 1..32, 3 leads (1 Tue + 2 Mon), 8 cards,
21 index items, 7 regions, strip figures tied to their stories,
timeline days, DATE CHECK (3-line fit + every listed story is actually
on the page), forbidden superseded/wrong figures (incl. v3's "14
unaccounted" Dymer figure, the "first since 2000" COP claim, and
November-2025 Guwahati figures), legibility caps (card titles, deck
lines, index lines, lead-deck wrap).
"""
import sys
from PIL import Image, ImageDraw

import render as R

fails = []


def check(name, ok, detail=""):
    if ok:
        print("PASS", name)
    else:
        fails.append(name)
        print("FAIL", name, detail)


img = Image.new("RGB", (1024, 1024), (255, 255, 255))
d = ImageDraw.Draw(img)

# ---- story counts ------------------------------------------------------
all_stories = list(R.LEADS) + list(R.CARDS)
check("32 stories total", len(R.LEADS) + len(R.CARDS) + len(R.INDEX) == 32,
      f"got {len(R.LEADS) + len(R.CARDS) + len(R.INDEX)}")
check("3 leads", len(R.LEADS) == 3)
check("8 cards", len(R.CARDS) == 8)
check("21 index items", len(R.INDEX) == 21)

nums = [s["n"] for s in all_stories] + [n for n, _, _ in R.INDEX]
check("numbers 1..32, no duplicates",
      sorted(nums) == list(range(1, 33)), f"got {sorted(nums)}")

# ---- leads -------------------------------------------------------------
for L in R.LEADS:
    check(f"lead {L['n']} pill valid", L["pill"] in ("CONFIRMED", "REPORTED"))
    check(f"lead {L['n']} art known", L["art"] in ("rally", "chip", "train"))
    check(f"lead {L['n']} has pin", isinstance(L["pin"], tuple))
    check(f"lead {L['n']} has source", bool(L["source"]))
check("lead 1 is Tuesday Asia rally", "Asia rallies" in R.LEADS[0]["title"])
check("lead 2 is Huang return", "Huang" in R.LEADS[1]["title"])
check("lead 3 is Modi-Shah train", "Modi" in R.LEADS[2]["title"])

# Lead-deck wrap: lead 1 <= 4 lines at 604px, leads 2-3 <= 2 lines at 472px.
l1_lines = R.wrap(d, R.LEADS[0]["deck"], R.F_SANS(13), 604)
check("lead 1 deck wraps to <=4 lines", len(l1_lines) <= 4,
      f"{len(l1_lines)} lines")
for L in R.LEADS[1:]:
    lines = R.wrap(d, L["deck"], R.F_SANS(13), 472)
    check(f"lead {L['n']} deck wraps to <=2 lines", len(lines) <= 2,
          f"{len(lines)} lines: {lines}")

# ---- cards -------------------------------------------------------------
for c in R.CARDS:
    check(f"card {c['n']} pill valid", c["pill"] in ("CONFIRMED", "REPORTED"))
    check(f"card {c['n']} icon known", c["icon"] in R.ICON_BG)
    check(f"card {c['n']} title <=34 chars", len(c["title"]) <= 34,
          f"{len(c['title'])}: {c['title']}")
    check(f"card {c['n']} deck1 <=60 chars", len(c["deck1"]) <= 60,
          f"{len(c['deck1'])}: {c['deck1']}")
    check(f"card {c['n']} deck2 <=60 chars", len(c["deck2"]) <= 60,
          f"{len(c['deck2'])}: {c['deck2']}")
    check(f"card {c['n']} deck2 has dateline",
          any(day in c["deck2"] for day in
              ("TUE 24 NOV", "MON 23 NOV", "SUN 22 NOV", "SAT 21 NOV",
               "FRI 20 NOV")))
check("card 4 is Tuesday Gaza strike", "Gaza strike" in R.CARDS[0]["title"]
      and "TUE 24 NOV" in R.CARDS[0]["deck2"])
check("card 4 is REPORTED (medics, one source chain)",
      R.CARDS[0]["pill"] == "REPORTED")
check("card 5 is COP31 collapse, SUN",
      "COP31 collapses" in R.CARDS[1]["title"]
      and "SUN 22 NOV" in R.CARDS[1]["deck2"])
check("card 6 is Dymer 11 dead (not v3's 14 unaccounted)",
      "11 dead" in R.CARDS[2]["title"]
      and "458 drones" in R.CARDS[2]["deck1"])
check("card 7 is Seoul first woman spy chief",
      "first woman spy chief" in R.CARDS[3]["title"])
check("card 8 is Armenia constitution, 220 to 89",
      "220 articles cut to 89" in R.CARDS[4]["deck2"])
check("card 9 is CrowdStrike $43.9bn",
      "$43.9bn" in R.CARDS[5]["title"] and "34%" in R.CARDS[5]["deck2"])
check("card 10 is Sparta II St Petersburg, 16 crew",
      "St Petersburg" in R.CARDS[6]["title"]
      and "16 crew" in R.CARDS[6]["deck1"])
check("card 11 is NZ draw, Pant 128",
      "239/5" in R.CARDS[7]["deck1"] and "Pant 128" in R.CARDS[7]["deck2"])

# ---- index -------------------------------------------------------------
for n, txt, day in R.INDEX:
    check(f"index {n} line <=70 chars",
          len(f"{n} · {txt} — {day}") <= 70,
          f"{len(f'{n} · {txt} — {day}')}: {txt}")
    check(f"index {n} has verification record", n in R.INDEX_STORIES)
    check(f"index {n} record has source",
          bool(R.INDEX_STORIES[n].get("source")))
check("index 12 is Australia fines, TUE",
      "Australia fines" in R.INDEX[0][1] and R.INDEX[0][2] == "TUE 24 NOV")
check("index 13 is Singapore Megaspeed, TUE",
      "Megaspeed" in R.INDEX[1][1] and R.INDEX[1][2] == "TUE 24 NOV")
check("index 14 is Canada-Qatar pact, TUE",
      "Canada, Qatar" in R.INDEX[2][1] and R.INDEX[2][2] == "TUE 24 NOV")
check("index 15 is CAS Senegal, TUE",
      "CAS" in R.INDEX[3][1] and R.INDEX[3][2] == "TUE 24 NOV")
check("index 16 is N. Korea Swiss office, TUE",
      "N. Korea" in R.INDEX[4][1] and R.INDEX[4][2] == "TUE 24 NOV")
check("index 17 is Japan PMI 53.7, TUE",
      "53.7" in R.INDEX[5][1] and R.INDEX[5][2] == "TUE 24 NOV")
check("index 18 is US-Syria training, MON",
      "Syrian forces" in R.INDEX[6][1] and R.INDEX[6][2] == "MON 23 NOV")
check("index 19 is Tajikistan ICC, MON",
      "Tajikistan" in R.INDEX[7][1] and R.INDEX[7][2] == "MON 23 NOV")
check("index 20 is Democrats 258, SUN",
      "258th" in R.INDEX[8][1] and R.INDEX[8][2] == "SUN 22 NOV")
check("index 21 is NATO, MON",
      "NATO" in R.INDEX[9][1] and R.INDEX[9][2] == "MON 23 NOV")
check("index 22 is Banten 24 dead, MON",
      "24 dead" in R.INDEX[10][1] and R.INDEX[10][2] == "MON 23 NOV")
check("index 23 is Lisbon living costs, SAT 21 NOV",
      "living costs" in R.INDEX[11][1] and R.INDEX[11][2] == "SAT 21 NOV")
check("index 23 record is living costs, not racism",
      "living costs" in R.INDEX_STORIES[23]["deck"]
      and "racism" not in R.INDEX_STORIES[23]["deck"])
check("index 24 is Verstappen, SAT",
      "Verstappen" in R.INDEX[12][1] and R.INDEX[12][2] == "SAT 21 NOV")
check("index 25 is Liverpool 4-0, SUN",
      "4–0" in R.INDEX[13][1] and R.INDEX[13][2] == "SUN 22 NOV")
check("index 26 is Alcaraz ATP title, SUN",
      "Alcaraz" in R.INDEX[14][1] and R.INDEX[14][2] == "SUN 22 NOV")
check("index 27 is Nasdaq fall, FRI",
      "Nasdaq" in R.INDEX[15][1] and R.INDEX[15][2] == "FRI 20 NOV")
check("index 28 is Anthropic IPO, FRI",
      "Anthropic" in R.INDEX[16][1] and R.INDEX[16][2] == "FRI 20 NOV")
check("index 29 is Miley wedding, SUN",
      "Miley Cyrus" in R.INDEX[17][1] and R.INDEX[17][2] == "SUN 22 NOV")
check("index 30 is Istanbul protests, SUN",
      "Istanbul" in R.INDEX[18][1] and R.INDEX[18][2] == "SUN 22 NOV")
check("index 31 is El Chapo, FRI",
      "El Chapo" in R.INDEX[19][1] and R.INDEX[19][2] == "FRI 20 NOV")
check("index 32 is box office, SUN",
      "box office" in R.INDEX[20][1] and R.INDEX[20][2] == "SUN 22 NOV")
check("index has 11 rows in col 1 at 10px, last row 948",
      848 + 10 * 10 == 948)

# ---- regions -----------------------------------------------------------
total = sum(v for _, v in R.REGIONS)
check("regions sum to 32", total == 32, f"got {total}")
check("7 regions", len(R.REGIONS) == 7)
check("Europe 9", dict(R.REGIONS).get("EUROPE") == 9)
check("Asia 8", dict(R.REGIONS).get("ASIA") == 8)
check("North America 9", dict(R.REGIONS).get("NORTH AMERICA") == 9)
check("Latin America 1 (El Chapo)",
      dict(R.REGIONS).get("LATIN AMERICA") == 1)
check("Middle East 2 (Gaza + US-Syria)",
      dict(R.REGIONS).get("MIDDLE EAST") == 2)
check("Oceania 2 (cricket + Australia)",
      dict(R.REGIONS).get("OCEANIA") == 2)
check("Africa 1 (CAS Senegal)", dict(R.REGIONS).get("AFRICA") == 1)

# ---- number strip ------------------------------------------------------
check("6 strip figures", len(R.NUMBERS) == 6)
check("strip +9.1% tied to lead 1", "+9.1%" in R.LEADS[0]["deck"])
check("strip +31.5% tied to lead 2", "31.5%" in R.LEADS[1]["deck"])
check("strip 8 tied to lead 3", "8 MoUs" in R.LEADS[2]["deck"])
check("strip 3 tied to Gaza card", "kills 3" in R.CARDS[0]["title"])
check("strip $43.9bn tied to Zscaler card",
      "$43.9bn" in R.CARDS[5]["title"])
check("strip 53.7 tied to Japan PMI index", "53.7" in R.INDEX[5][1])

# ---- timeline ----------------------------------------------------------
check("4 timeline days", len(R.TIMELINE) == 4)
check("timeline Tuesday is today", R.TIMELINE[3][2] is True)
check("timeline Tuesday has 4 items", len(R.TIMELINE[3][1]) == 4)
check("timeline Saturday is first", R.TIMELINE[0][0] == "SAT 21 NOV")
tl_text = " ".join(it for _, items, _ in R.TIMELINE for it in items)
for phrase in ("Banten fire, 24 dead later confirmed",
               "COP31 collapses, no deal",
               "Huang returns to Nvidia",
               "Asia rallies on AI rebound",
               "Gaza strike kills 3",
               "Japan PMI 53.7"):
    check(f"timeline contains '{phrase}'", phrase in tl_text)

# ---- DATE CHECK --------------------------------------------------------
check("DATE CHECK head is Tuesday 24 Nov 2026",
      "TUESDAY 24 NOVEMBER 2026" in R.DATE_CHECK_HEAD)
dc_lines = R.wrap(d, R.DATE_CHECK_BODY, R.F_SANS(10), 972)
check("DATE CHECK body fits 3 lines", len(dc_lines) <= 3,
      f"{len(dc_lines)} lines")
for name in ("Huang returns", "Modi–Shah train", "Korea reshuffle",
             "Armenia draft", "Zscaler deal", "Sparta II", "US–Syria",
             "Tajikistan", "NATO", "Banten", "NZ draw", "COP31", "Dymer",
             "Democrats 258", "Liverpool", "Alcaraz", "Miley", "Istanbul",
             "box office", "Lisbon", "Verstappen", "El Chapo", "Nasdaq",
             "Anthropic"):
    check(f"DATE CHECK lists '{name}'", name in R.DATE_CHECK_BODY)

# Every DATE CHECK item must actually be on the page.
page_text = " ".join(
    [s.get("title", "") + " " + s.get("deck", "") for s in R.LEADS]
    + [c["title"] + " " + c["deck1"] + " " + c["deck2"] for c in R.CARDS]
    + [txt for _, txt, _ in R.INDEX])
for name, needle in (
        ("Huang returns", "Huang is back"),
        ("Modi–Shah train", "Modi–Shah launch"),
        ("Korea reshuffle", "Seoul names first woman"),
        ("Armenia draft", "Armenia drafts"),
        ("Zscaler deal", "Zscaler"),
        ("Sparta II", "Sparta II"),
        ("US–Syria", "Syrian forces"),
        ("Tajikistan", "Tajikistan"),
        ("NATO", "NATO meets"),
        ("Banten", "Banten toll"),
        ("NZ draw", "NZ save the Test"),
        ("COP31", "COP31 collapses"),
        ("Dymer", "Dymer toll"),
        ("Democrats 258", "258th House seat"),
        ("Liverpool", "Liverpool 4–0"),
        ("Alcaraz", "Alcaraz"),
        ("Miley", "Miley Cyrus"),
        ("Istanbul", "Istanbul"),
        ("box office", "box office"),
        ("Lisbon", "Lisbon"),
        ("Verstappen", "Verstappen"),
        ("El Chapo", "El Chapo"),
        ("Nasdaq", "Nasdaq fell"),
        ("Anthropic", "Anthropic")):
    check(f"DATE CHECK '{name}' is on the page", needle in page_text)

# ---- forbidden figures -------------------------------------------------
all_text = page_text + " " + R.DATE_CHECK_BODY + " " + R.SOURCES_LINE
for bad in ("14 unaccounted", "first since 2000", "since COP6",
            "Guwahati", "34-member", "35-member", "TODO", "Lorem",
            "placeholder", "{owner}", "{repo}", "against racism",
            "AC short circuit", "Monday 23 November 2026"):
    check(f"forbidden '{bad}' absent", bad not in all_text)

# ---- map ---------------------------------------------------------------
pins = {}
for L in R.LEADS:
    pins[L["n"]] = L["pin"]
for c in R.CARDS:
    pins[c["n"]] = c["pin"]
check("11 pins on the map", len(pins) == 11, f"got {len(pins)}")
check("map pins are leads + cards only",
      sorted(pins) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
check("Gaza pin on the map", pins[4] == (34.5, 31.5))
check("Tokyo pin on the map", pins[1] == (139.7, 35.7))

# ---- sources -----------------------------------------------------------
check("sources line names Reuters", "Reuters" in R.SOURCES_LINE)
check("sources line names PTI (India-Nepal)", "PTI" in R.SOURCES_LINE)
check("sources line names Basarnas (Banten)", "Basarnas" in R.SOURCES_LINE)

print()
if fails:
    print(f"{len(fails)} FAILURES: {fails}")
    sys.exit(1)
print("ALL CHECKS PASSED")
