# Carousel — Slide 01 / cover

**File:** `output/slide-01.png` — 1080 × 1350 px (4:5), RGB PNG
**Source:** `assets/photo-source.png` + `scripts/build_slide.py` (type is rendered in code, never generated)

---

## Design system

| Token | Value | Use |
| --- | --- | --- |
| Ground | `#0A0A0A` | near-black base, fade target |
| Type / white | `#F3F0EC` | headline line 1, support, furniture-adjacent white |
| Accent | `#E8191D` | **only** on "STOP THE SCROLL", "WARNING:", the bar, the pill |
| Furniture grey | `#969390` | handle and counter, nothing else |

- **Display:** Anton (Google Fonts, OFL) — condensed grotesque, tracking **−0.035 em**, 156.8 px.
- **Body:** Inter Variable (OFL), optical size 14 — weight 700 for the kicker and pill, 400 italic for the support line.
- **Margins:** 86 px each side (8%). Nothing touches the edge.
- **Grid:** centre axis at 540 px. Headline cap-top 807 px → pill base 1264 px → footer baseline 1300 px.

## Type stack, top to bottom

| Element | Copy | Spec |
| --- | --- | --- |
| Kicker | `WARNING:` | Inter 700, 28 px, caps, +0.27 em, red, centred, baseline 775 |
| Headline 1 | `6 HOOKS THAT` | Anton 156.8 px, off-white, baseline 942 |
| Headline 2 | `STOP THE SCROLL` | Anton 156.8 px, red, baseline 1078 (same optical size, tight 0.865 em leading) |
| Support | `on a clothing ad.` | Inter Italic 400, 33 px, off-white, baseline 1124 |
| Bar | — (graphic) | 188 × 12 px red bar, fully rounded, top 1154 |
| Pill | `SWIPE FOR ALL 6 >>>` | Inter 700, 26 px, white on translucent red (α 202) with a two-stage glow, 1188–1264 |
| Furniture | `@lvlsmarketing` / `1/8` | Inter 500, 21 px, grey, baseline 1300, left and right margin |

## Photographic treatment

1. Downloaded plate cover-cropped to 4:5, resampled to 2160 × 2700.
2. Cool-purple dusk grade: violet in the shadows, neutral highlight rolloff, warmth pulled out of the horizon so red is the only warm accent left.
3. Photo fades to near-black across the lower 45% (fade starts at 40% height), plus a soft superellipse panel behind the type block so the copy clears the figure's waist without a visible band.
4. Vignette, faint multi-octave paper-crumple shading with three long fold creases, and fine emulsion grain — all subtle, all in 8-bit-scale deltas.
5. Type is drawn at 2× and the whole frame is downsampled with Lanczos for clean edges at 1080 px.

## Notes

- No clothing logos, no legible text in the photograph.
- Red appears exactly four times: kicker, headline line 2, bar, pill. No orange/yellow/blue anywhere.
- Headline stays legible at 324 px wide (see `output/slide-01-thumb.png`).

## Rebuild

```bash
pip install --break-system-packages pillow numpy
python3 scripts/build_slide.py
```
