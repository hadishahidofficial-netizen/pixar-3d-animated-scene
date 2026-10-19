# pixar-3d-animated-scene
A Pixar-inspired 3D animated short scene with expressive character animation, cinematic camera motion, and emotional storytelling using React Three Fiber, GSAP, and Blender models.

## Instagram carousel

All slides are 1080x1350 (4:5) and composed in code — Anton / Inter type over either a
cinematic photo plate or a pure `#0A0A0A` ground. Shared palette, grid, type and texture
helpers live in `scripts/poster_kit.py`.

| Slide | Output | Spec | Build |
| --- | --- | --- | --- |
| 01 | `output/slide-01.png` | `carousel/SLIDE-01.md` | `python3 scripts/build_slide.py` |
| 02 | `output/slide-02.png` | `carousel/SLIDE-02.md` | `python3 scripts/build_slide02.py` |

Each build also writes a 324 px thumbnail (`*-thumb.png`) for feed-size legibility checks.
