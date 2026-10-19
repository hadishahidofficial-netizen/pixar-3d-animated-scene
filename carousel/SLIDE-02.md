# Carousel — Slide 02

**File:** `output/slide-02.png` — 1080 × 1350 px (4:5), RGB PNG
**Build:** `python3 scripts/build_slide02.py` (type only; nothing is generated imagery)

---

## Layout

Pure black type slide. Measured positions below are ink bounds in the final 1080 px canvas.

| y | Element |
| --- | --- |
| 227–247 | red label |
| 352 | headline line 1 cap-top |
| 618 / 902 | headline baselines (lead 283.6 px, cap height 266 px) |
| 978–994 | red bar (16 px, spans the full 908 px measure) |
| 1072 / 1125 | support line baselines |
| 1300 | footer baseline |
| 1125–1350 | 225 px of empty black |

X: everything sits on the 86 px margin (8%); headline ink runs 86 → 994, bar runs 86 → 994, so headline ink width = bar width exactly.

## Type

| Element | Copy | Spec |
| --- | --- | --- |
| Label | `HOOK 01 / 06 · PROBLEM` | Inter 700, 24 px, +0.22 em, red, left |
| Headline 1 | `OPEN ON` | Anton 310.2 px, off-white `#F3F0EC`, −0.035 em |
| Headline 2 | `THE PAIN` | Anton 310.2 px, red `#E8191D`, −0.035 em |
| Bar | — (graphic) | 908 × 16 px, sharp corners, red |
| Support 1 | `The problem your product solves.` | Inter 400, 36.6 px, off-white |
| Support 2 | `Like a hoodie that loses its shape after one wash.` | Inter 400, 36.6 px, off-white |
| Footer | `@lvlsmarketing` / `2/8` | Inter 500, 21 px, grey `#969390` |

Both headline lines are set at the **same** point size — line 1 is not stretched. The size is solved as a fixed point so the *rendered ink* of the wider line ("THE PAIN") fills the 908 px measure; left side bearings (9.5 px and 3.0 px) are compensated so both lines start on the exact margin, not on their advance origin.

## Ground

- `#0A0A0A` base; all four corners measure exactly `(10, 10, 10)`.
- Faint multi-octave crumple shading plus four long fold creases, peak-to-peak ≈ 5 levels — present on close inspection, invisible as a "filter".
- Fine emulsion grain, σ ≈ 3.6 levels.
- No gradients, no second accent. Red exists in exactly three horizontal bands: label, headline line 2, and the bar.

## Notes

- The brief puts signal red on both "the single key phrase" and the bar; here the key phrase is headline line 2, so the red bar is additionally called out in the `[LAYOUT]` block. If red should appear on *only one* of them, drop the bar to off-white — one-line change at the marked block in `build_slide02.py`.
- Legible at 324 px wide: see `output/slide-02-thumb.png`.

## Rebuild

```bash
pip install --break-system-packages pillow numpy
python3 scripts/build_slide02.py
```
