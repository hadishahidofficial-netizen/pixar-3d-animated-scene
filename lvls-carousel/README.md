# LVLS Agency — Instagram Carousel: “5 email flows every clothing brand needs”

Code-built creative for the **Thu 15 Oct** post (8:00 AM ET / 5:00 PM PKT).
7 slides · 4:5 feed (1080×1350) primary · plus 1:1, 9:16 and a light-theme alternate.
Everything is drawn from code (Pillow) — no design-tool licence, no AI imagery,
infinitely editable.

## Quick start

```bash
pip install pillow numpy          # python 3.10+
python3 src/build.py              # renders every variant into exports/
python3 src/build.py --variants feed,feed-light   # or pick a subset
```

Open `exports/index.html` (or serve `exports/`) for the proof sheet with
download links and the ready-to-paste caption.

## What's in the box

| Path | Purpose |
|---|---|
| `src/content.py` | **All copy**: slides, bullets, caption, hashtags, handle, post date |
| `src/theme.py` | Palettes (dark + light), fonts, layout metrics |
| `src/drawkit.py` | Backgrounds (gradient/glow/grain), typography, marker highlights, chips |
| `src/icons.py` | 18 hand-built line icons on a 24-grid (envelope, cart-bag, eye, heart, moon…) |
| `src/slides.py` | Slide layouts: cover / flow / CTA + shared chrome & footer |
| `src/build.py` | Render pipeline, contact sheets, HTML proof sheet |
| `assets/fonts/` | Archivo (Expanded/Condensed/Regular) + Instrument Serif Italic (OFL) |
| `exports/` | Rendered PNG/JPG (git-ignored — regenerate, don't commit) |

## Design system

- **Type**: Archivo Expanded Black for display (tight, −2 tracking), Archivo Condensed
  Bold for bullets, Archivo Medium tracked-out for labels, Instrument Serif Italic for
  the single “editorial” accent word per slide.
- **Colour (dark)**: near-black warm charcoal canvas, bone ink `#F5F3EE`,
  signal orange `#FF6A00` (marker highlights, icons, CTA), muted greys for metadata.
- **Chrome on every slide**: LVLS wordmark + handle, `NN/07` counter, 7-step progress
  pips, flow label, hairline rules, orange corner tab, ghost numeral, save/swipe footer.
- **Marker highlight**: the key phrase of each headline sits on a slightly slanted,
  hand-drawn orange bar (seeded jitter so every slide differs subtly).

## Script analysis (why the slides are built this way)

The source script is strong: one idea per slide, on-slide lines are scannable, and the
CTA is a single keyword DM. The build keeps **every on-slide line verbatim** and adds a
display headline per slide so the carousel reads as design, not as a bullet list:

1. **Cover** — number-led hook (“5 EMAIL FLOWS”) + the full checklist as a teaser rail.
   Numbers and lists are the highest-save hook format for agency content.
2. **Welcome** — “first impression on autopilot”: story → best sellers → incentive
   *only if it fits* (the script's price-position caveat is kept on-slide; it signals
   strategy, not template-selling).
3. **Abandoned cart** — speed + exact product + objection handling (sizing/shipping are
   the two real fashion killers; giving them a line is the slide's payoff).
4. **Browse abandonment** — differentiated from cart in one line: “viewed, never added”.
5. **Post-purchase** — thank → teach (care/styling) → review *after delivery*: the order
   matches the customer timeline, which is why it converts.
6. **Winback** — “one repurchase cycle” is the sharpest line in the script; the slide
   pairs it with “newness, not discount” to protect margin.
7. **CTA** — save + share + one DM keyword (AUDIT). One action verb per line, button
   repeats the exact keyword people must type.

Optional tweaks to test later (not applied):
- A/B cover hook: “Your clothing brand is leaking revenue in 5 places.”
- Slide 3 alt headline: “The cart isn't lost. It's waiting.”
- Add a Klaviyo/ESP logo strip on slide 7 if the audience is already ESP-literate.

## Posting checklist

- [ ] Replace `HANDLE` in `src/content.py` (`@yourhandle`) and re-run the build.
- [ ] Upload `exports/feed/lvls-email-flows-feed-01..07.png` in order, 8:00 AM ET.
- [ ] Caption + hashtags: copy from `exports/index.html`.
- [ ] Set the DM keyword **AUDIT** in your automation (ManyChat/Klaviyo) before posting.
- [ ] First comment: pin a 1-line case-study teaser to farm replies.
- [ ] Alt text per slide: “Slide N of 7 — <flow name>: <three on-slide lines>”.

## Fonts licence

Archivo (Omnibus-Type) and Instrument Serif (Rodrigo Fuenzalida / Google) are both
SIL Open Font License 1.1 — free for commercial use, embedded here as TTF assets.
