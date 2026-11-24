# The Tuesday Ledger — 24 November 2026

[![Make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/astiip/news-image-20261124-bot/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/astiip/news-image-20261124-bot/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page picture-first newspaper for Tuesday 24 November 2026, rendered
as a 1024×1024 image. It iterates our own v3 layout system
(news-image-20261123, "The Monday Ledger", 31 stories) — same geometry,
new day, new art, new stories: **32 stories / 7 regions**.

**Date honesty:** the page is built on Tuesday morning (~10:00 WIB), so
most of the day's news is Monday's news first reported overnight plus
Tuesday's own early stories. The masthead names TUESDAY 24 NOVEMBER 2026;
every story carries its own dateline, and the DATE CHECK lists every story
that is NOT Tuesday's. Nothing is backdated to Tuesday.

**The three leads:**
1. **Asia rallies on Huang's return (TUE 24 NOV)** — Tokyo +4.5%, Seoul
   +7.5%, Taipei +9.1% as Asia buys the AI rebound; MSCI Asia ex-Japan
   +4.6%.
2. **Huang is back at Nvidia (MON 23 NOV)** — reinstated 11 days after he
   quit; shares jump 31.5%, their best day in 23 years; Trump pressed
   the board to bring him back.
3. **Modi–Shah launch Nepal train (MON 23 NOV)** — the Saryu–Kamala
   Express, Ayodhya–Janakpur, 604 km; India pledges Rs 15,000 crore
   and signs 8 MoUs.

**Design:** masthead with a giant serif date, a full-width illustrated lead
(Asian skyline with climbing green bars), two more illustrated leads (a
chip with a green arrow; the Saryu–Kamala Express at dawn with Indian and
Nepali flags), a six-figure number strip, a Saturday→Tuesday timeline,
eight medium cards (including a new flame icon for Gaza and a new shield
icon for the CrowdStrike deal), a 21-item numbered index, a dotted world
map with 11 numbered pins, and a red DATE CHECK that names every
earlier story on the page that is NOT Tuesday's news. Every story carries
its own dateline; where reports differ, the card says so.

## Run

```bash
python3 render.py        # writes entry.png (1024x1024, PIL only)
python3 verify.py        # checks the data before rendering
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to the output dir
```

## Sources

Reuters · AP · AFP · CNN · Basarnas · NATO · MEA · PTI. Figures as
reported 24 Nov 2026, 10:00 WIB. Every figure was verified from fresh
searches on Tuesday 24 November 2026; nothing is copied from other entries.

## Caveats

- **Dymer toll updated.** v3 said "14 unaccounted" (Monday's figure).
  The toll is now 11 dead in the Dymer flat (458 drones + 45 missiles
  overnight, 406 drones downed); 15 killed in the Kyiv region and
  Zaporizhzhia in all.
- **COP31 "first since" claims differ by source** (CNN: first major
  breakdown since Copenhagen 2009; The Times: no deal since COP6 2000)
  — the page prints neither, only "collapses, no deal".
- **Guwahati cricket figures were NOT used.** Search results for the
  Guwahati Test are from November 2025, not 2026.
- **Nepal delegation size is NOT printed.** Reports disagree (34 vs 35);
  the page prints no delegation number.
- **Tajikistan is dated MON 23 NOV** (the day the UN published the ICC
  withdrawal notice), not FRI 20 NOV (the day the notice was filed);
  the card says the exit takes effect 20 Nov 2027.
