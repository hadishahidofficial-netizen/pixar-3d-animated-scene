# 5 Email Flows — Q4 carousel (7 slides)

A 4:5 Instagram carousel in the dark cinematic streetwear-agency style of the
reference set (tablet-analytics / foggy portrait look): near-black page, one warm
orange accent, condensed uppercase display type, small furniture marks.

| # | File | Headline |
|---|------|----------|
| 1 | `slide-01.png` | 5 EMAIL **FLOWS** — every clothing brand needs. |
| 2 | `slide-02.png` | Q4 IS **35–40%** OF YOUR YEAR. |
| 3 | `slide-03.png` | THE 5 **FLOWS.** |
| 4 | `slide-04.png` | TIMING BEATS COPY. |
| 5 | `slide-05.png` | 3 EMAILS. **ONE CART.** |
| 6 | `slide-06.png` | DON’T JUST SURVIVE **Q4.** OWN IT. |
| 7 | `slide-07.png` | LET’S BUILD **YOUR Q4.** + DM CTA |

- `index.html` — swipeable preview (drag / arrow keys / dot nav / “View all 7”).
- `jpg/` — Instagram-ready JPGs (q92, 4:4:4, ~250–290 KB each).
- `overview.png` — single strip of all seven slides.
- `caption.md` — caption, hashtags and posting notes.
- `fonts/` — the exact Barlow / Barlow Condensed cuts baked into the type.

## Design system (locked)

```
canvas      1080 × 1350 (4:5)          margin   86 px (8%)
background  #080808                    paper    #F4F1EC
accent      #E95C24  (max 3 uses/slide: square, rule+diamond, one type element)
display     Barlow Condensed Bold 700 / Bold Italic 700 (accent words)
body        Barlow Regular 400 / Medium 500
grain       35 mm-style monochrome noise, vignette ~16%
```

Furniture on every slide: orange square + `CLOTHING BRAND EMAIL` (top-left),
`@lvlsmarketing` (top-right), hairline rule with orange diamond, footer line and
`n/7` counter (bottom).

## Rebuild

```bash
python3 -m pip install pillow numpy        # one-time
python3 scripts/build_carousel.py          # writes carousel/slide-01..07.png
```

The script (`scripts/build_carousel.py`) is the single source of truth for the
copy: edit the `lines` / `lede` / `rows` values in each `slide_*` function and
re-run. Every block is measured before drawing, so changes can’t collide.

Photos live in `assets/bg/` (AI-generated, no logos, no readable text). Swap a
file with the same name to re-skin a slide; the crop, grade and fade are applied
automatically.
